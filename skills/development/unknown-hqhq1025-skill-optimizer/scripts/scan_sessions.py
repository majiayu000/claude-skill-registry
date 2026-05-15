#!/usr/bin/env python3
"""Summarize coding-agent session history into recurring workflow signals.

This script intentionally emits sanitized metadata and short snippets only. It
is a first-pass miner for skill candidates, not a full transcript exporter.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Iterable


INTENT_PATTERNS = {
    "review": r"\b(review|审查|看一下|检查|读一下|actual file|diff)\b",
    "debug": r"\b(debug|fix|修|报错|失败|error|failing|root cause|根因)\b",
    "publish": r"\b(commit|push|PR|merge|发布|开源|publish|release)\b",
    "deploy_remote": r"\b(ssh|远端|remote|tunnel|端口|公网|内网|host|server|服务)\b",
    "research": r"\b(research|调研|查一下|论文|paper|arxiv|资料)\b",
    "install_setup": r"\b(install|安装|配置|setup|登录|auth|cli)\b",
    "docs_write": r"\b(文档|README|AGENTS\.md|CLAUDE\.md|notes|总结|整理)\b",
    "skill_work": r"\b(skill|skills|SKILL\.md|技能)\b",
    "frontend": r"\b(UI|frontend|页面|网站|design|browser|screenshot|Playwright)\b",
    "data_doc": r"\b(pdf|docx|xlsx|spreadsheet|slides|表格|文档|PPT)\b",
}

DEFAULT_PATTERNS = Path(__file__).resolve().parents[1] / "references" / "patterns.json"

SKIP_USER_PREFIXES = (
    "# AGENTS.md instructions",
    "<environment_context>",
    "You are a helpful assistant. You will be presented",
    "<command-name>",
    "Automation:",
)


@dataclass
class SessionRecord:
    path: Path
    platform: str
    mtime: datetime
    cwd: str = ""
    user_messages: list[str] = field(default_factory=list)
    assistant_messages: list[str] = field(default_factory=list)
    tools: Counter[str] = field(default_factory=Counter)

    @property
    def key(self) -> str:
        return f"{self.platform}:{self.path}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", default=str(Path.home() / ".codex/sessions"))
    parser.add_argument("--codex-archive", default=str(Path.home() / ".codex/archived_sessions"))
    parser.add_argument("--codex-rollout-summaries", default=str(Path.home() / ".codex/memories/rollout_summaries"))
    parser.add_argument("--claude", default=str(Path.home() / ".claude/projects"))
    parser.add_argument("--claude-sessions", default=str(Path.home() / ".claude/sessions"))
    parser.add_argument("--gemini", default=str(Path.home() / ".gemini"))
    parser.add_argument("--opencode", default=str(Path.home() / ".config/opencode"))
    parser.add_argument("--cursor", default=str(Path.home() / ".cursor"))
    parser.add_argument("--days", type=int, default=30)
    parser.add_argument("--limit", type=int, default=300)
    parser.add_argument("--min-count", type=int, default=3)
    parser.add_argument("--include-archives", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--include-summaries", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument(
        "--export",
        action="append",
        default=[],
        help="Additional exported transcript file or directory (.jsonl, .json, .md, .txt). Repeatable.",
    )
    parser.add_argument(
        "--patterns",
        default=str(DEFAULT_PATTERNS),
        help="Workflow pattern JSON file. Defaults to the bundled references/patterns.json.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def cutoff_for(days: int) -> datetime:
    return datetime.now(timezone.utc) - timedelta(days=days)


def recent_jsonl_files(root: str, days: int, limit: int) -> list[Path]:
    base = Path(root).expanduser()
    if not base.exists():
        return []
    cutoff = cutoff_for(days).timestamp()
    files = [p for p in base.rglob("*.jsonl") if p.is_file() and p.stat().st_mtime >= cutoff]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit]


def recent_files(root: str, patterns: tuple[str, ...], days: int, limit: int) -> list[Path]:
    base = Path(root).expanduser()
    if not base.exists():
        return []
    cutoff = cutoff_for(days).timestamp()
    files: list[Path] = []
    for pattern in patterns:
        files.extend(
            p
            for p in base.rglob(pattern)
            if p.is_file()
            and p.stat().st_mtime >= cutoff
            and "antigravity-browser-profile" not in p.parts
            and "node_modules" not in p.parts
            and "extensions" not in p.parts
        )
    files = sorted(set(files), key=lambda p: p.stat().st_mtime, reverse=True)
    return files[:limit]


def content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("input_text")
                if text:
                    parts.append(str(text))
            elif isinstance(item, str):
                parts.append(item)
        return "\n".join(parts)
    return ""


def sanitize(text: str, max_len: int = 180) -> str:
    text = re.sub(r"/Users/[^/\s]+", "/Users/<user>", text)
    text = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "<email>", text)
    text = re.sub(r"\b(?:gho|sk|xox[baprs])-[-A-Za-z0-9_]{12,}\b", "<token>", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[: max_len - 1] + "…" if len(text) > max_len else text


def is_real_user_message(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    if stripped in {"/clear", "clear"}:
        return False
    if stripped.startswith("[Request interrupted"):
        return False
    noisy_substrings = (
        "Download the React DevTools",
        "Electron Security Warning",
        "Added 1 line, removed",
        "⏺ Update(",
        "VM4 sandbox_bundle",
        "agent.turn_end",
        "agent.end",
    )
    if any(needle in stripped for needle in noisy_substrings):
        return False
    return not any(stripped.startswith(prefix) for prefix in SKIP_USER_PREFIXES)


def parse_codex(path: Path) -> SessionRecord:
    rec = SessionRecord(
        path=path,
        platform="codex",
        mtime=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc),
    )
    for line in path.read_text(errors="ignore").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        typ = obj.get("type")
        payload = obj.get("payload") or {}
        if typ == "session_meta":
            rec.cwd = payload.get("cwd", rec.cwd) or rec.cwd
            continue
        if typ == "event_msg":
            msg = str(payload.get("message") or payload.get("msg") or "")
            for name in re.findall(r"\b(exec_command|apply_patch|web\.run|tool_search|spawn_agent|wait_agent)\b", msg):
                rec.tools[name] += 1
            continue
        if typ != "response_item":
            continue
        role = payload.get("role")
        text = content_to_text(payload.get("content"))
        if role == "user" and is_real_user_message(text):
            rec.user_messages.append(text)
        elif role == "assistant":
            rec.assistant_messages.append(text)
        item_type = payload.get("type")
        if item_type in {"function_call", "tool_call"}:
            name = payload.get("name") or payload.get("tool_name")
            if name:
                rec.tools[str(name)] += 1
    return rec


def parse_claude(path: Path) -> SessionRecord:
    rec = SessionRecord(
        path=path,
        platform="claude",
        mtime=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc),
    )
    for line in path.read_text(errors="ignore").splitlines():
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        cwd = obj.get("cwd") or obj.get("projectPath")
        if cwd:
            rec.cwd = cwd
        msg = obj.get("message") if isinstance(obj.get("message"), dict) else obj
        role = msg.get("role") or obj.get("type")
        text = content_to_text(msg.get("content"))
        if role == "user" and is_real_user_message(text):
            rec.user_messages.append(text)
        elif role == "assistant":
            rec.assistant_messages.append(text)
        for match in re.finditer(r"'name': '([^']+)'|\"name\": \"([^\"]+)\"", line):
            name = match.group(1) or match.group(2)
            if name:
                rec.tools[name] += 1
    return rec


def parse_markdown_export(path: Path, platform: str) -> SessionRecord:
    rec = SessionRecord(
        path=path,
        platform=platform,
        mtime=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc),
        cwd=str(path.parent),
    )
    text = path.read_text(errors="ignore")
    # Common exported transcript shapes: "User:", markdown headings, or task files.
    user_chunks = re.findall(
        r"(?ims)^(?:#{1,4}\s*)?(?:user|human|prompt|task|request|用户|任务)\s*:?\s*(.+?)(?=^(?:#{1,4}\s*)?(?:assistant|agent|model|user|human|prompt|task|request|用户|助手|任务)\s*:|\Z)",
        text,
    )
    if user_chunks:
        for chunk in user_chunks:
            if is_real_user_message(chunk):
                rec.user_messages.append(chunk)
    else:
        # Antigravity/Gemini task.md and walkthrough.md often encode one task-like document.
        first_section = "\n".join(line for line in text.splitlines()[:80] if line.strip())
        if is_real_user_message(first_section):
            rec.user_messages.append(first_section)
    for name in re.findall(r"\b(?:Tool|tool|command|cmd)\s*[:=]\s*`?([A-Za-z0-9_.:-]+)", text):
        rec.tools[name] += 1
    return rec


def iter_json_objects(path: Path) -> Iterable[dict]:
    text = path.read_text(errors="ignore")
    if path.suffix == ".jsonl":
        for line in text.splitlines():
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(obj, dict):
                yield obj
        return
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return
    if isinstance(obj, list):
        for item in obj:
            if isinstance(item, dict):
                yield item
    elif isinstance(obj, dict):
        yield obj


def extract_messages_from_json_obj(obj) -> Iterable[tuple[str, str]]:
    if isinstance(obj, dict):
        role = obj.get("role") or obj.get("author") or obj.get("type") or obj.get("speaker")
        content = obj.get("content") or obj.get("text") or obj.get("message") or obj.get("prompt")
        if isinstance(content, dict):
            content = content.get("text") or content.get("content")
        text = content_to_text(content)
        if role and text:
            yield str(role).lower(), text
        for value in obj.values():
            yield from extract_messages_from_json_obj(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from extract_messages_from_json_obj(item)


def parse_json_export(path: Path, platform: str) -> SessionRecord:
    rec = SessionRecord(
        path=path,
        platform=platform,
        mtime=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc),
        cwd=str(path.parent),
    )
    for obj in iter_json_objects(path):
        for role, text in extract_messages_from_json_obj(obj):
            if role in {"user", "human", "prompt", "request"} and is_real_user_message(text):
                rec.user_messages.append(text)
            elif role in {"assistant", "agent", "model"}:
                rec.assistant_messages.append(text)
        for name in re.findall(r'"(?:tool|name|command)"\s*:\s*"([^"]+)"', json.dumps(obj, ensure_ascii=False)):
            rec.tools[name] += 1
    return rec


def parse_rollout_summary(path: Path) -> SessionRecord:
    rec = SessionRecord(
        path=path,
        platform="codex-summary",
        mtime=datetime.fromtimestamp(path.stat().st_mtime, timezone.utc),
        cwd=str(path.parent),
    )
    text = path.read_text(errors="ignore")
    snippets = []
    for line in text.splitlines():
        if any(
            token in line
            for token in (
                "desc:",
                "learnings:",
                "用户",
                "默认",
                "workflow",
                "runbook",
                "skill",
                "remote",
                "paper",
                "website",
                "review",
            )
        ):
            snippets.append(line.strip())
    if not snippets:
        snippets = [line.strip() for line in text.splitlines()[:80] if line.strip()]
    joined = "\n".join(snippets[:20])
    if is_real_user_message(joined):
        rec.user_messages.append(joined)
    return rec


def parse_export_path(path: Path, platform: str) -> list[SessionRecord]:
    if path.is_dir():
        records = []
        for child in recent_files(str(path), ("*.jsonl", "*.json", "*.md", "*.txt"), days=3650, limit=1000):
            records.extend(parse_export_path(child, platform))
        return records
    suffix = path.suffix.lower()
    if suffix in {".json", ".jsonl"}:
        return [parse_json_export(path, platform)]
    if suffix in {".md", ".txt", ".log"}:
        return [parse_markdown_export(path, platform)]
    return []


def add_records(records: list[SessionRecord], new_records: Iterable[SessionRecord], seen: set[str]) -> None:
    for rec in new_records:
        key = rec.key
        if key in seen:
            continue
        seen.add(key)
        records.append(rec)


def classify(text: str) -> set[str]:
    labels = set()
    for label, pattern in INTENT_PATTERNS.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            labels.add(label)
    return labels or {"other"}


def load_workflow_patterns(path: str) -> dict:
    pattern_path = Path(path).expanduser()
    if not pattern_path.exists():
        return {}
    data = json.loads(pattern_path.read_text(errors="ignore"))
    return data if isinstance(data, dict) else {}


def classify_workflows(text: str, patterns: dict) -> set[str]:
    labels = set()
    for label, spec in patterns.items():
        flags = 0 if spec.get("case_sensitive") else re.IGNORECASE
        if re.search(spec["pattern"], text, flags=flags):
            labels.add(label)
    return labels


def project_key(cwd: str) -> str:
    if not cwd:
        return "(unknown)"
    parts = Path(cwd).parts
    return "/".join(parts[-2:]) if len(parts) >= 2 else cwd


def summarize(records: Iterable[SessionRecord], min_count: int, workflow_patterns: dict) -> dict:
    records = list(records)
    intent_counts: Counter[str] = Counter()
    intent_examples: dict[str, list[str]] = defaultdict(list)
    intent_projects: dict[str, Counter[str]] = defaultdict(Counter)
    workflow_counts: Counter[str] = Counter()
    workflow_examples: dict[str, list[str]] = defaultdict(list)
    workflow_projects: dict[str, Counter[str]] = defaultdict(Counter)
    tool_counts: Counter[str] = Counter()

    for rec in records:
        tool_counts.update(rec.tools)
        user_texts = rec.user_messages[:8]
        text = "\n".join(user_texts)
        labels = classify(text)
        for label in labels:
            intent_counts[label] += 1
            intent_projects[label][project_key(rec.cwd)] += 1
            if len(intent_examples[label]) < 5 and rec.user_messages:
                intent_examples[label].append(sanitize(next((m for m in user_texts if classify(m) and label in classify(m)), rec.user_messages[0])))
        for message in user_texts:
            for label in classify_workflows(message, workflow_patterns):
                workflow_counts[label] += 1
                workflow_projects[label][project_key(rec.cwd)] += 1
                if len(workflow_examples[label]) < 5:
                    workflow_examples[label].append(sanitize(message))

    candidates = []
    for label, count in intent_counts.most_common():
        if count < min_count or label == "other":
            continue
        projects = intent_projects[label].most_common(3)
        score = 5 if count >= 12 else 4 if count >= 6 else 3
        candidates.append(
            {
                "intent": label,
                "score": score,
                "count": count,
                "projects": projects,
                "examples": intent_examples[label],
            }
        )
    workflow_candidates = []
    for label, count in workflow_counts.most_common():
        if count < min_count:
            continue
        spec = workflow_patterns[label]
        projects = workflow_projects[label].most_common(3)
        project_spread = len(workflow_projects[label])
        score = 5 if count >= 20 and project_spread >= 2 else 4 if count >= 6 else 3
        workflow_candidates.append(
            {
                "name": label,
                "score": score,
                "count": count,
                "direction": spec["direction"],
                "why": spec["why"],
                "projects": projects,
                "examples": workflow_examples[label],
            }
        )
    return {
        "sessions_scanned": len(records),
        "date_range_days": None,
        "platforms": Counter(rec.platform for rec in records),
        "unsupported_sources": [],
        "top_tools": tool_counts.most_common(15),
        "top_intents": intent_counts.most_common(),
        "workflow_candidates": workflow_candidates,
        "candidates": candidates,
    }


def emit_markdown(summary: dict) -> None:
    print("# Skill Candidate Scan")
    print()
    print(f"Sessions scanned: {summary['sessions_scanned']}")
    print("Platforms: " + ", ".join(f"{k}={v}" for k, v in summary["platforms"].items()))
    if summary["platforms"].get("codex-summary"):
        print("Note: codex-summary entries are compressed memory evidence, not raw transcripts.")
    if summary["unsupported_sources"]:
        print("Unsupported or empty sources: " + "; ".join(summary["unsupported_sources"]))
    print()
    print("## Top Intent Clusters")
    for label, count in summary["top_intents"]:
        print(f"- {label}: {count}")
    print()
    print("## Top Tool Signals")
    for name, count in summary["top_tools"]:
        print(f"- {name}: {count}")
    print()
    print("## Workflow Candidate Skills")
    for c in summary["workflow_candidates"]:
        print(f"### {c['name']} (score {c['score']}/5, {c['count']} hits, {c['direction']})")
        print(f"Why: {c['why']}")
        projects = ", ".join(f"{name} ({count})" for name, count in c["projects"])
        print(f"Projects: {projects or 'n/a'}")
        for ex in c["examples"]:
            print(f"- Example: {ex}")
        print()
    print("## Broad Intent Clusters")
    for c in summary["candidates"]:
        print(f"### {c['intent']} (score {c['score']}/5, {c['count']} sessions)")
        projects = ", ".join(f"{name} ({count})" for name, count in c["projects"])
        print(f"Projects: {projects or 'n/a'}")
        for ex in c["examples"]:
            print(f"- Example: {ex}")
        print()


def main() -> int:
    args = parse_args()
    records = []
    seen: set[str] = set()
    for path in recent_jsonl_files(args.codex, args.days, args.limit):
        add_records(records, [parse_codex(path)], seen)
    if args.include_archives:
        for path in recent_jsonl_files(args.codex_archive, args.days, args.limit):
            add_records(records, [parse_codex(path)], seen)
    for path in recent_jsonl_files(args.claude, args.days, args.limit):
        add_records(records, [parse_claude(path)], seen)
    if args.include_archives:
        for path in recent_jsonl_files(args.claude_sessions, args.days, args.limit):
            add_records(records, [parse_claude(path)], seen)
    for path in recent_files(
        args.gemini,
        ("task.md", "walkthrough.md", "implementation_plan.md", "session-*.json", "logs.json"),
        args.days,
        args.limit,
    ):
        add_records(records, parse_export_path(path, "gemini"), seen)
    if args.include_summaries:
        for path in recent_files(args.codex_rollout_summaries, ("*.md", "*.jsonl"), args.days, args.limit):
            add_records(records, [parse_rollout_summary(path)], seen)
    for export in args.export:
        add_records(records, parse_export_path(Path(export).expanduser(), "export"), seen)
    workflow_patterns = load_workflow_patterns(args.patterns)
    summary = summarize(records, args.min_count, workflow_patterns)
    summary["date_range_days"] = args.days
    summary["patterns_file"] = str(Path(args.patterns).expanduser())
    unsupported = []
    for label, root in {
        "gemini": args.gemini,
        "opencode": args.opencode,
        "cursor": args.cursor,
    }.items():
        p = Path(root).expanduser()
        if not p.exists():
            unsupported.append(f"{label}: not found at {p}")
            continue
        if label == "gemini":
            found = recent_files(str(p), ("task.md", "walkthrough.md", "implementation_plan.md", "session-*.json", "logs.json"), args.days, args.limit)
            if not found:
                unsupported.append(f"{label}: no recent known transcript/task export files found at {p}")
            continue
        known = list(p.rglob("*.jsonl"))
        if known:
            unsupported.append(f"{label}: found JSONL but native parser is not implemented ({p}); pass files via --export for generic parsing")
        else:
            unsupported.append(f"{label}: no known native transcript format found at {p}; pass exported .json/.jsonl/.md/.txt via --export")
    summary["unsupported_sources"] = unsupported
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2, default=dict))
    else:
        emit_markdown(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
