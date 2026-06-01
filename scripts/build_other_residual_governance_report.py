#!/usr/bin/env python3
"""Build a report-only governance summary for live residual category skills."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from audit_category_quality import best_suggestion, read_text_prefix
from category_taxonomy import category_keywords
from utils import extract_frontmatter, load_metadata, skill_semantic_fields

SCHEMA_VERSION = 1


def utc_now_isoformat() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def iter_category_skill_dirs(skills_dir: Path, category: str):
    category_dir = skills_dir / category
    if not category_dir.exists():
        return
    for skill_file in sorted(category_dir.glob("*/SKILL.md")):
        yield skill_file.parent, skill_file.relative_to(skills_dir)


def frontmatter_status(content: str) -> tuple[str, str]:
    if not content.startswith("---"):
        return "no_frontmatter", "SKILL.md does not begin with YAML frontmatter"
    end_index = content.find("---", 3)
    if end_index == -1:
        return "invalid_frontmatter", "frontmatter is not terminated"
    try:
        payload = yaml.safe_load(content[3:end_index].strip())
    except yaml.YAMLError as exc:
        return "invalid_frontmatter", f"frontmatter YAML parse error: {exc}"
    if not isinstance(payload, dict):
        return "invalid_frontmatter", "frontmatter is not a mapping"
    return "ok", ""


def load_security_statuses(security_report: Path | None) -> dict[str, dict[str, Any]]:
    if security_report is None or not security_report.exists():
        return {}
    payload = json.loads(security_report.read_text(encoding="utf-8"))
    statuses: dict[str, dict[str, Any]] = {}
    skills = payload.get("skills") if isinstance(payload, Mapping) else []
    if not isinstance(skills, list):
        return statuses
    for item in skills:
        if not isinstance(item, Mapping):
            continue
        path = item.get("path")
        if isinstance(path, str) and path:
            statuses[path] = dict(item)
    return statuses


def issue_types(item: Mapping[str, Any] | None) -> list[str]:
    if not item:
        return []
    issues = item.get("issues")
    if not isinstance(issues, list):
        return []
    values = []
    for issue in issues:
        if isinstance(issue, Mapping) and isinstance(issue.get("type"), str):
            values.append(str(issue["type"]))
    return values


def classify_bucket(
    *,
    security: Mapping[str, Any] | None,
    frontmatter: str,
    suggestion: dict[str, Any] | None,
    description: str,
    tags: list[str],
) -> str:
    if security and security.get("safe") is False:
        return "security_failed"
    if frontmatter != "ok":
        return "structure_review"
    if suggestion:
        return "semantic_review_candidate"
    if not description and not tags:
        return "low_context"
    return "manual_taxonomy_review"


def build_report(
    skills_dir: Path,
    *,
    category: str = "other",
    security_report: Path | None = None,
    content_chars: int = 2000,
    min_score: int = 2,
    min_delta: int = 2,
    limit_examples: int = 20,
) -> dict[str, Any]:
    security_statuses = load_security_statuses(security_report)
    keyword_map = category_keywords()
    bucket_counts: Counter[str] = Counter()
    frontmatter_counts: Counter[str] = Counter()
    suggested_category_counts: Counter[str] = Counter()
    security_issue_counts: Counter[str] = Counter()
    examples: dict[str, list[dict[str, Any]]] = {}
    total = 0

    for skill_dir, rel in iter_category_skill_dirs(skills_dir, category):
        total += 1
        content = read_text_prefix(skill_dir / "SKILL.md", max_chars=max(content_chars, 8192))
        metadata = load_metadata(skill_dir)
        frontmatter = extract_frontmatter(content)
        semantics = skill_semantic_fields(
            skill_dir,
            metadata=metadata,
            frontmatter=frontmatter,
            rel=rel,
            content=content,
            content_chars=content_chars,
        )
        frontmatter_state, frontmatter_reason = frontmatter_status(content)
        frontmatter_counts[frontmatter_state] += 1
        suggestion = best_suggestion(
            category,
            str(semantics["text"]),
            keyword_map,
            min_score=min_score,
            min_delta=min_delta,
        )
        if suggestion:
            suggested_category_counts[str(suggestion["suggested_category"])] += 1

        security = security_statuses.get(str(rel))
        for issue_type in issue_types(security):
            security_issue_counts[issue_type] += 1

        bucket = classify_bucket(
            security=security,
            frontmatter=frontmatter_state,
            suggestion=suggestion,
            description=str(semantics.get("description") or ""),
            tags=list(semantics.get("tags") or []),
        )
        bucket_counts[bucket] += 1

        bucket_examples = examples.setdefault(bucket, [])
        if len(bucket_examples) < limit_examples:
            item: dict[str, Any] = {
                "path": str(rel),
                "name": semantics["name"],
                "description": semantics["description"],
                "semantic_sources": semantics["sources"],
                "frontmatter_status": frontmatter_state,
            }
            if frontmatter_reason:
                item["frontmatter_reason"] = frontmatter_reason
            if suggestion:
                item["suggested_category"] = suggestion["suggested_category"]
                item["score"] = suggestion["score"]
                item["signals"] = suggestion["signals"]
            if security:
                item["security_safe"] = security.get("safe")
                item["security_issue_types"] = issue_types(security)
            bucket_examples.append(item)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now_isoformat(),
        "skills_dir": str(skills_dir),
        "category": category,
        "total": total,
        "policy": {
            "content_chars": content_chars,
            "min_score": min_score,
            "min_delta": min_delta,
            "security_report": str(security_report) if security_report else "",
        },
        "bucket_counts": sorted_counter(bucket_counts),
        "frontmatter_status_counts": sorted_counter(frontmatter_counts),
        "suggested_category_counts": sorted_counter(suggested_category_counts),
        "security_issue_counts": sorted_counter(security_issue_counts),
        "examples": examples,
        "notes": [
            "This is report-only and does not mutate archive contents.",
            "security_failed residuals should stay out of canonical categories until fixed.",
            "semantic_review_candidate residuals are review queues, not automatic moves.",
        ],
    }


def print_report(report: dict[str, Any]) -> None:
    print("Other residual governance report")
    print(f"Category: {report['category']}")
    print(f"Total: {report['total']}")
    print(f"Buckets: {report['bucket_counts']}")
    print(f"Frontmatter: {report['frontmatter_status_counts']}")
    print(f"Suggested targets: {report['suggested_category_counts']}")
    print(f"Security issues: {report['security_issue_counts']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--category", default="other")
    parser.add_argument("--security-report", type=Path)
    parser.add_argument("--content-chars", type=int, default=2000)
    parser.add_argument("--min-score", type=int, default=2)
    parser.add_argument("--min-delta", type=int, default=2)
    parser.add_argument("--limit-examples", type=int, default=20)
    parser.add_argument("--output-json", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(
        args.skills_dir,
        category=args.category,
        security_report=args.security_report,
        content_chars=args.content_chars,
        min_score=args.min_score,
        min_delta=args.min_delta,
        limit_examples=args.limit_examples,
    )
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
