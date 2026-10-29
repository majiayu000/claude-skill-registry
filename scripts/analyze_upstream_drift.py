#!/usr/bin/env python3
"""Compare digest-checked archived SKILL.md bytes with fixed upstream branch heads.

Deterministic primary order: adds_execution > adds_network > widens_permissions >
changes_code_examples > instructions_changed > cosmetic. Execution means a new
download-and-run, package installer (npx/uvx/pip install), interpreter-script, or
./script command. A new/edited executable-language fence without a new command
is a code-example signal, subordinate to network and permission changes.
All matching signals remain in flags. Compare
whitespace-normalized blocks/commands as sets, not individual diff lines. Network
means a new HTTP(S) URL (including a new URL on an existing domain); report new
hostnames separately (localhost and loopback URLs are excluded). Permission fields named allowed-tools, tools, tool,
permissions or permission, at any frontmatter depth, widen when their flattened
values gain tokens; false/null values grant no tokens. This is a textual
heuristic, not permission semantics.
Instructions means >6 added+removed nonempty body lines after removing whitespace
and Markdown formatting characters; all remaining edits are cosmetic, including
potentially meaningful tiny edits and currently identical bytes (flagged
identical_bytes). Raw added/removed line counts are also stored.

Closed executable fences: sh, bash, shell, zsh, console, terminal, python,
python3, py, javascript, js, typescript, ts, powershell, ps1, ruby, perl, php,
go, rust, c, cpp, sql. An edit within an existing executable block counts as
a new block if its whitespace-normalized contents differ. Shell backslash-newline
continuations are joined for command matching. Download-and-run matches curl/wget
piped to sh/bash/python; interpreter-script matches python/bash/sh/node/ruby/perl
with a .py/.sh/.js/.mjs/.rb/.pl path; ./ commands accept extensionless names or
.sh/.py/.js/.mjs/.cjs/.rb/.pl/.ps1. Plain text/JSON/YAML fences are not execution
signals by themselves. Body normalization removes whitespace and `*_#>|~-;
other punctuation and letter case remain significant. YAML permission tokens
are split on whitespace/commas, keeping mapping paths and ignoring list order.
Non-permission frontmatter changes do not contribute to the body-line threshold.
If the concatenated normalized body lines are identical, reflow alone contributes
zero changed body lines.

Not a safety verdict: examples, documentation and modified existing code blocks
can trigger flags; unfenced code, prose permissions and non-HTTP links can escape
them. No code is executed. Only SKILL.md is compared, not bundled assets. A path
404 triggers a recursive tree lookup at the same commit. A replacement SKILL.md
matches if its parent directory equals the archived directory name, or its YAML
frontmatter name equals the archived frontmatter name. Directory matches take
precedence; ties use the lexicographically first path. Moved files retain their
normal content classification in moved_change_class. No match in a complete
search means removed. Failed/truncated trees or incomplete name searches mean
path_missing_unchecked, never assumed removal. Other comparison failures are
fetch_failed. Evidence contains only raw added lines, at most four per snippet.
The unavailable cohort is rechecked: head 404 + repository 404 => repo_404
(includes private/inaccessible repos); head 404 + accessible repo =>
branch_not_found; other failures => other; recovered heads => available_now.
If metadata lacks a branch, only repository availability is checked: a 404 is
repo_404, an accessible repository is other (branch unknown). Source-path metadata
defects do not prevent checking repository/branch availability.

Cache fixes the data main SHA and each upstream head on first successful fetch;
reuse the same directory to resume that observation, a fresh directory to refresh.
Successful responses and 404s are cached; transient errors are retried twice
and never cached. 403/429 are reported explicitly, without retry storms. Every
selected pin produces a row; fetch_failed/unchecked/other make the command exit
nonzero. --cache-only makes no network requests. Authentication comes only from
GITHUB_TOKEN when set; no CLI credential lookup is performed.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import http.client
import json
import os
import re
import threading
import time
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urlsplit

import yaml
from audit_skill_assets import canonical_source_identity_from_metadata
from build_static_skill_pages import PUBLIC_SITE, skill_page_slug
from resolve_install_pins import sha256_digest
from skill_content_history import load_history
from utils import split_frontmatter_content
from verify_upstream_assets import GitHubApiError, GitHubClient

DATA_REPO = "majiayu000/claude-skill-registry-data"
CONTENT_CLASSES = ("adds_execution", "adds_network", "widens_permissions", "changes_code_examples", "instructions_changed", "cosmetic")
CLASSES = (*CONTENT_CLASSES, "moved", "removed", "path_missing_unchecked", "fetch_failed")
CLASS_LABELS = dict(zip(CLASSES, (
    "Adds new commands to run", "Adds new external URLs", "Widens tool permissions",
    "Changes code examples", "Rewrites instructions", "Small edits",
    "Moved within the repository", "Removed from the repository",
    "Could not check", "Could not compare",
), strict=True))
EXEC_LANGUAGES = {"sh", "bash", "shell", "zsh", "console", "terminal", "python", "python3", "py", "javascript", "js", "typescript", "ts", "powershell", "ps1", "ruby", "perl", "php", "go", "rust", "c", "cpp", "sql"}
URL_RE = re.compile(r"https?://[^\s<>\"'`\[\]{}]+")
COMMAND_RE = re.compile(
    r"(?:\b(?:curl|wget)\b[^\n]*?\|\s*(?:sh|bash|python[23]?)[^\n]*"
    r"|\b(?:npx|uvx)\s+[^\n`]+|\b(?:python[23]?\s+-m\s+)?pip[3]?\s+install\s+[^\n`]+"
    r"|\b(?:python[23]?|bash|sh|node|ruby|perl)\s+[\w./-]+\.(?:py|sh|js|mjs|rb|pl)\b[^\n`]*"
    r"|(?<![\w/(])\./(?:[\w-]+/)*[\w-]+(?:\.(?:sh|py|js|mjs|cjs|rb|pl|ps1))?(?=[\s`]|$))"
)
PERMISSION_KEYS = {"allowed-tools", "tools", "tool", "permissions", "permission"}
METHODOLOGY = __doc__


def normalized(value: str) -> str:
    return " ".join(value.split())


def code_blocks(text: str) -> dict[str, str]:
    blocks, fence, language, lines = {}, "", "", []
    for line in text.splitlines():
        match = re.match(r"^\s*(`{3,}|~{3,})([^\s`]*)\s*$", line)
        if match and not fence:
            fence, language, lines = match[1], match[2].lower(), []
        elif fence and re.fullmatch(r"\s*" + re.escape(fence[0]) + "{" + str(len(fence)) + r",}\s*", line):
            content = "\n".join(lines)
            if normalized(content) and language in EXEC_LANGUAGES:
                blocks[normalized(content)] = content
            fence = ""
        elif fence:
            lines.append(line)
    return blocks


def permission_tokens(meta: Any, prefix: str = "") -> set[str]:
    def flatten(value: Any, path: str) -> set[str]:
        if value is None or value is False:
            return set()
        if isinstance(value, dict):
            return set().union(*(flatten(item, f"{path}/{key}") for key, item in value.items()))
        if isinstance(value, list):
            return set().union(*(flatten(item, path) for item in value))
        return {path + ":" + token for token in re.findall(r"[^\s,]+", str(value))}

    tokens = set()
    if isinstance(meta, dict):
        for key, value in meta.items():
            path = f"{prefix}/{key}"
            if str(key).lower().replace("_", "-") in PERMISSION_KEYS:
                tokens |= flatten(value, path)
            elif isinstance(value, dict):
                tokens |= permission_tokens(value, path)
    return tokens


def classify(old: bytes, new: bytes) -> dict[str, Any]:
    before, after = old.decode("utf-8"), new.decode("utf-8")
    flags = []
    if old == new:
        flags.append("identical_bytes")

    blocks_old, blocks_new = code_blocks(before), code_blocks(after)
    added_blocks = blocks_new.keys() - blocks_old.keys()
    example_lines = {line for key in added_blocks for line in blocks_new[key].splitlines() if line.strip()}
    if added_blocks:
        flags.append("new_code_block")
    commands_old = {normalized(m.group()) for m in COMMAND_RE.finditer(re.sub(r"\\\r?\n\s*", " ", before))}
    commands_new = {normalized(m.group()) for m in COMMAND_RE.finditer(re.sub(r"\\\r?\n\s*", " ", after))}
    added_commands = commands_new - commands_old
    if added_commands:
        flags.append("new_execution_command")
    def urls(text: str) -> set[str]:
        return {url for match in URL_RE.finditer(text)
                if (url := match.group().rstrip(".,;:!?)"))
                and urlsplit(url).hostname not in {None, "localhost", "127.0.0.1", "::1"}}

    urls_old, urls_new = urls(before), urls(after)
    domains_old = {urlsplit(url).hostname for url in urls_old}
    domains_new = {urlsplit(url).hostname for url in urls_new}
    added_urls = urls_new - urls_old
    if added_urls:
        flags.append("new_url")
    new_domains = sorted(domain for domain in domains_new - domains_old if domain)
    if new_domains:
        flags.append("new_domain")
    meta_old, body_old = split_frontmatter_content(before)
    meta_new, body_new = split_frontmatter_content(after)
    try:
        permissions_old = permission_tokens(yaml.safe_load(meta_old) if meta_old else {})
        permissions_new = permission_tokens(yaml.safe_load(meta_new) if meta_new else {})
        if permissions_new - permissions_old:
            flags.append("permission_added_or_widened")
    except yaml.YAMLError:
        flags.append("frontmatter_unparsed")
    def strip_format(text):
        return [value for line in text.splitlines() if (value := re.sub(r"[\s`*_#>|~\-]", "", line))]
    def changes(before: list[str], after: list[str]) -> tuple[list[str], list[str]]:
        added, removed = [], []
        for tag, start, end, new_start, new_end in difflib.SequenceMatcher(None, before, after).get_opcodes():
            if tag in {"replace", "delete"}:
                removed.extend(before[start:end])
            if tag in {"replace", "insert"}:
                added.extend(after[new_start:new_end])
        return added, removed

    normalized_old, normalized_new = strip_format(body_old), strip_format(body_new)
    body_added, body_removed = changes(normalized_old, normalized_new) if "".join(normalized_old) != "".join(normalized_new) else ([], [])
    changed_lines = len(body_added) + len(body_removed)
    if changed_lines > 6:
        flags.append("substantive_lines")
    added, removed = changes(before.splitlines(), after.splitlines())
    primary = ("adds_execution" if "new_execution_command" in flags else
               "adds_network" if "new_url" in flags else
               "widens_permissions" if "permission_added_or_widened" in flags else
               "changes_code_examples" if "new_code_block" in flags else
               "instructions_changed" if changed_lines > 6 else "cosmetic")
    # Detection uses normalization; quotations always come from the raw diff.
    body_start = len(after.splitlines()) - len(body_new.splitlines())
    chunks = []
    for tag, _, _, start, end in difflib.SequenceMatcher(None, before.splitlines(), after.splitlines()).get_opcodes():
        if tag in {"replace", "insert"}:
            lines = after.splitlines()[start:end]
            matches = [i for i, line in enumerate(lines) if (
                (primary == "adds_execution" and any(
                    command in normalized(line) or command.startswith(normalized(line.rstrip("\\")).strip("`"))
                    for command in added_commands) and line.strip(" `\\")) or
                (primary == "adds_network" and any(url in line for url in added_urls)) or
                (primary == "widens_permissions" and re.search(r"(?:allowed[_-]tools|tools?|permissions?)\s*:", line)) or
                (primary == "changes_code_examples" and line in example_lines) or
                (primary == "instructions_changed" and start + i >= body_start and bool(strip_format(line)))
            )]
            preferred = matches[0] if matches else 0
            chunks.append((bool(matches), "\n".join(lines[preferred:preferred + 4])))
    evidence = [snippet for _, snippet in sorted(chunks, key=lambda item: not item[0]) if snippet.strip()][:3]
    return {"class": primary, "flags": flags, "lines_added": len(added),
            "lines_removed": len(removed), "changed_body_lines": changed_lines,
            "new_domains": new_domains, "evidence": evidence[:3]}


class CachedFetcher:
    """Small disk response cache; caches contain public content, never request headers."""

    def __init__(self, cache: Path, token: str, *, cache_only: bool = False):
        self.cache, self.client = cache, GitHubClient(token)
        self.cache_only = cache_only
        cache.mkdir(parents=True, exist_ok=True)

    def _cached(self, key: str, fetch: Any, *, cache_404: bool = False) -> bytes:
        path = self.cache / (hashlib.sha256(key.encode()).hexdigest() + ".json")
        if path.exists():
            record = json.loads(path.read_text())
        else:
            if self.cache_only:
                raise GitHubApiError(0, f"Not cached (cache-only replay): {key}")
            for attempt in range(3):
                try:
                    value = fetch()
                    record = {"status": 200, "body": value.hex(), "fetched_at": datetime.now(timezone.utc).isoformat()}
                    break
                except GitHubApiError as exc:
                    if exc.status == 404 and cache_404:
                        record = {"status": 404, "body": "", "fetched_at": datetime.now(timezone.utc).isoformat()}
                        break
                    if attempt < 2 and (exc.status == 0 or exc.status >= 500):
                        time.sleep(2 ** attempt)
                        continue
                    raise
            temporary = path.with_suffix(f".{threading.get_ident()}.tmp")
            temporary.write_text(json.dumps(record))
            temporary.replace(path)
        if record["status"] != 200:
            raise GitHubApiError(record["status"], f"HTTP {record['status']}: {key}")
        return bytes.fromhex(record["body"])

    def api(self, path: str) -> dict:
        def fetch() -> bytes:
            try:
                return json.dumps(self.client.get_json(path)).encode()
            except (http.client.HTTPException, OSError, ValueError) as exc:
                # A large tree can be cut off mid-body; treat it as transient so it is retried.
                raise GitHubApiError(0, f"Transport failure: {exc!r}"[:300]) from exc

        return json.loads(self._cached("api:" + path, fetch, cache_404=True))

    def head(self, repo: str, branch: str) -> str:
        # Reuse GitHubClient's response/identity validation and cache the resolved SHA.
        return self._cached(f"head:{repo}:{branch}", lambda: self.client.branch_sha(repo, branch).encode(), cache_404=True).decode()

    def tree(self, repo: str, commit: str) -> list[str]:
        payload = self.api(f"/repos/{repo}/git/trees/{commit}?recursive=1")
        if payload.get("truncated") is not False or not isinstance(payload.get("tree"), list):
            raise GitHubApiError(0, "GitHub tree is truncated or lacks entries; move search incomplete")
        paths = []
        for entry in payload["tree"]:
            if not isinstance(entry, dict) or not isinstance(entry.get("path"), str) or not isinstance(entry.get("type"), str):
                raise GitHubApiError(0, "GitHub tree contains a malformed entry; move search incomplete")
            if entry["type"] == "blob" and entry["path"].split("/")[-1] == "SKILL.md":
                paths.append(entry["path"])
        return sorted(paths)

    def raw(self, repo: str, commit: str, path: str) -> bytes:
        url = f"https://raw.githubusercontent.com/{repo}/{quote(commit, safe='')}/{quote(path, safe='/')}"

        def fetch() -> bytes:
            try:
                with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310
                    return response.read()
            except urllib.error.HTTPError as exc:
                raise GitHubApiError(exc.code, f"HTTP {exc.code}: {url}") from exc
            except (http.client.HTTPException, OSError) as exc:
                raise GitHubApiError(0, f"Transport failure: {exc}") from exc

        return self._cached(url, fetch, cache_404=True)


def day(value: Any) -> str:
    """Calendar day of an ISO timestamp, for reader-facing text."""
    return str(value or "")[:10]


def failure(exc: Exception) -> str:
    return str(exc)[:300]


def frontmatter_name(content: bytes) -> str | None:
    frontmatter, _ = split_frontmatter_content(content.decode("utf-8"))
    metadata = yaml.safe_load(frontmatter) if frontmatter else None
    name = metadata.get("name") if isinstance(metadata, dict) else None
    return name if isinstance(name, str) and name else None


def check_missing_paths(rows: list[dict], fetcher: Any) -> None:
    """Search once per repository/commit; share candidate bytes across missing skills."""
    archives = {row["id"]: row.pop("_archived") for row in rows}
    repo, commit = rows[0]["repo"], rows[0]["upstream_commit"]
    try:
        paths = fetcher.tree(repo, commit)
    except GitHubApiError as exc:
        for row in rows:
            row["reason"] = "Source path is missing; move search unchecked: " + failure(exc)
        return

    contents: dict[str, bytes | Exception] = {}

    def read(path: str) -> bytes:
        if path not in contents:
            try:
                contents[path] = fetcher.raw(repo, commit, path)
            except GitHubApiError as exc:
                contents[path] = exc
        value = contents[path]
        if isinstance(value, Exception):
            raise value
        return value

    pending = []
    for row in rows:
        directory = row["archive_path"].split("/")[-2]
        matches = [path for path in paths if path.split("/")[-2:-1] == [directory]]
        if matches:
            row["moved_path"] = matches[0]
        else:
            try:
                name = frontmatter_name(archives[row["id"]])
                pending.append((row, name))
            except (UnicodeError, yaml.YAMLError) as exc:
                row["reason"] = "Archived name could not be checked: " + failure(exc)

    names: dict[str, str] = {}
    incomplete = None
    if any(name for _, name in pending):
        for path in paths:
            try:
                name = frontmatter_name(read(path))
                if name:
                    names.setdefault(name, path)
            except (GitHubApiError, UnicodeError, yaml.YAMLError) as exc:
                incomplete = failure(exc)
    for row, name in pending:
        if name and name in names:
            row["moved_path"] = names[name]
        elif name and incomplete:
            row["reason"] = "Source path is missing; frontmatter name search incomplete: " + incomplete
        else:
            row.update({"class": "removed", "reason": "No matching SKILL.md in the complete resolved commit tree"})

    for row in rows:
        if path := row.get("moved_path"):
            row.update({"class": "moved", "moved_change_class": "fetch_failed",
                        "original_upstream_path": row["upstream_path"], "upstream_path": path,
                        "upstream_url": f"https://github.com/{repo}/blob/{commit}/{quote(path, safe='/')}"})
            row.pop("reason", None)
            try:
                current = read(path)
                result = classify(archives[row["id"]], current)
                row.update(result, moved_change_class=result["class"], current_digest=sha256_digest(current))
            except (GitHubApiError, ValueError, UnicodeError) as exc:
                row["reason"] = "Moved file comparison failed: " + failure(exc)
            row["class"] = "moved"


def analyze(pins: dict[str, dict], history: dict[str, list[dict]], fetcher: Any, *, workers: int = 8,
            catalog: dict[str, dict] | None = None) -> dict[str, Any]:
    """One result per selected pin, including explicit failures. Fetcher is injectable."""
    selected = [(key, pin) for key, pin in sorted(pins.items()) if pin.get("status") in {"upstream_changed", "upstream_unavailable"}]
    archive_commit = fetcher.head(DATA_REPO, "main")
    catalog = catalog or {}

    def prepare(item: tuple[str, dict]) -> dict:
        key, pin = item
        row = {"id": key, "pin_status": pin["status"], "repo": pin.get("repo", ""),
               "branch": pin.get("branch", ""), "upstream_path": "", "archive_path": pin["archive_path"],
               "class": "fetch_failed", "flags": [], "lines_added": None, "lines_removed": None,
               "new_domains": [], "evidence": [], "pin_checked_at": pin.get("checked_at"),
               "archive_digest": pin["digest"], "original_error": pin.get("error"),
               "archive_url": f"https://github.com/{DATA_REPO}/blob/{archive_commit}/{quote(pin['archive_path'], safe='/')}",
               "history_first_seen": (history.get(key) or [{}])[0].get("first_seen")}
        try:
            if pin["status"] == "upstream_changed":
                archived = fetcher.raw(DATA_REPO, archive_commit, pin["archive_path"])
                if sha256_digest(archived) != pin["digest"]:
                    raise ValueError("Archive digest mismatch: data main no longer contains the pinned scanned bytes")
                row["_archived"] = archived
            meta_path = pin["archive_path"].rsplit("/", 1)[0] + "/metadata.json"
            metadata = json.loads(fetcher.raw(DATA_REPO, archive_commit, meta_path))
            if not isinstance(metadata, dict):
                raise ValueError("Archive metadata is not an object")
            row.update(name=metadata.get("name", key), archived_at=metadata.get("downloaded_at"))
            repo, path, error = canonical_source_identity_from_metadata(metadata)
            if error and (pin["status"] == "upstream_changed" or error == "invalid_repo"):
                raise ValueError(f"Archive metadata: {error}")
            if error:
                row["metadata_error"] = error
            if pin.get("repo") and pin["repo"].casefold() != repo.casefold():
                raise ValueError("Pin/archive repository identity mismatch")
            row.update(repo=repo, upstream_path=path,
                       branch=pin.get("branch") or metadata.get("github_branch") or metadata.get("branch") or "")
            record = catalog.get(key)
            row["guide_url"] = f"{PUBLIC_SITE}skills/{skill_page_slug(record)}/" if record else f"https://github.com/{repo}"
        except (GitHubApiError, ValueError, UnicodeError) as exc:
            row["reason"] = failure(exc)
        return row

    with ThreadPoolExecutor(max_workers=workers) as pool:
        rows = list(pool.map(prepare, selected))
        targets = sorted({(row["repo"], row["branch"]) for row in rows if "reason" not in row})

        def resolve(target: tuple[str, str]) -> tuple[tuple[str, str], dict]:
            repo, branch = target
            try:
                if not branch:
                    fetcher.api(f"/repos/{repo}")
                    return target, {"reason": "Archive metadata lacks upstream branch; repository is accessible", "availability": "other"}
                return target, {"commit": fetcher.head(repo, branch)}
            except GitHubApiError as exc:
                reason = "other"
                if exc.status == 404 and not branch:
                    reason = "repo_404"
                elif exc.status == 404:
                    try:
                        fetcher.api(f"/repos/{repo}")
                        reason = "branch_not_found"
                    except GitHubApiError as repo_exc:
                        if repo_exc.status == 404:
                            reason = "repo_404"
                        else:
                            return target, {"reason": failure(repo_exc), "availability": "other"}
                return target, {"reason": failure(exc), "availability": reason}

        heads = dict(pool.map(resolve, targets))

        def compare(row: dict) -> dict:
            archived = row.pop("_archived", None)
            if "reason" not in row:
                head = heads[(row["repo"], row["branch"])]
                if "commit" not in head:
                    row.update(head)
                else:
                    row["upstream_commit"] = head["commit"]
                    row["upstream_url"] = f"https://github.com/{row['repo']}/blob/{head['commit']}/{quote(row['upstream_path'], safe='/')}"
                    if row["pin_status"] == "upstream_unavailable":
                        row["availability"] = "available_now"
                    else:
                        try:
                            current = fetcher.raw(row["repo"], head["commit"], row["upstream_path"])
                            row.update(classify(archived, current), current_digest=sha256_digest(current))
                        except GitHubApiError as exc:
                            if exc.status == 404:
                                row.update({"class": "path_missing_unchecked", "_archived": archived})
                            else:
                                row["reason"] = failure(exc)
                        except (ValueError, UnicodeError) as exc:
                            row["reason"] = failure(exc)
            if row["pin_status"] == "upstream_unavailable":
                row.pop("class")
                row.setdefault("availability", "other")
            return row

        rows = list(pool.map(compare, rows))
        missing: dict[tuple[str, str], list[dict]] = {}
        for row in rows:
            if "_archived" in row:
                missing.setdefault((row["repo"], row["upstream_commit"]), []).append(row)
        list(pool.map(lambda group: check_missing_paths(group, fetcher), missing.values()))
    changed = [row for row in rows if row["pin_status"] == "upstream_changed"]
    unavailable = [row for row in rows if row["pin_status"] == "upstream_unavailable"]
    counts = Counter(row["class"] for row in changed)
    availability = Counter(row["availability"] for row in unavailable)
    recorded_errors = Counter(
        "branch_not_found" if "branch not found" in str(row.get("original_error", "")).lower() else
        "generic_404" if "404" in str(row.get("original_error", "")) else "other"
        for row in unavailable
    )
    pin_dates = sorted({pin["checked_at"] for _, pin in selected if pin.get("checked_at")})
    history_dates = sorted({row["history_first_seen"] for row in rows if row.get("history_first_seen")})
    moved_failures = sum(row.get("moved_change_class") == "fetch_failed" for row in changed)
    return {"schema_version": 2, "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
            "archive_repo": DATA_REPO, "archive_commit": archive_commit, "methodology": METHODOLOGY,
            "pin_checked_range": [pin_dates[0], pin_dates[-1]] if pin_dates else [],
            "history_since": history_dates[0] if history_dates else None,
            "summary": {"pins_total": len(pins), "changed_total": len(changed), "unavailable_total": len(unavailable),
                        "class_counts": {key: counts[key] for key in CLASSES},
                        "class_percentages": {key: round(counts[key] * 100 / len(changed), 2) if changed else 0 for key in CLASSES},
                        "unavailable_reasons": {key: availability[key] for key in ("repo_404", "branch_not_found", "other", "available_now")},
                        "original_unavailable_errors": {key: recorded_errors[key] for key in ("branch_not_found", "generic_404", "other")},
                        "failure_count": counts["fetch_failed"] + counts["path_missing_unchecked"] + moved_failures + availability["other"]},
            "skills": changed, "unavailable": unavailable}


def example_rows(data: dict) -> list[dict]:
    """Cover each confirmed class, preferring readable, moderate-sized diffs."""
    candidates = sorted(
        (row for row in data["skills"] if row.get("upstream_url") and row["class"] in (*CONTENT_CLASSES, "moved", "removed")),
        key=lambda row: (not bool(row["evidence"]),
                         any(len(line) > 250 for snippet in row["evidence"] for line in snippet.splitlines()),
                         any(len(snippet) > 400 for snippet in row["evidence"]),
                         abs((row["lines_added"] or 0) + (row["lines_removed"] or 0) - 20), row["id"]),
    )
    chosen = []
    for primary in (*CONTENT_CLASSES, "moved", "removed"):
        match = next((row for row in candidates if row["class"] == primary), None)
        if match:
            chosen.append(match)
    return chosen


def render_report(data: dict) -> str:
    def esc(value):
        return html.escape(str(value), quote=True)

    summary = data["summary"]
    counts = summary["class_counts"]
    availability = summary["unavailable_reasons"]
    content_counts = Counter(row.get("moved_change_class", row["class"]) for row in data["skills"])
    substantive = sum(content_counts[key] for key in CONTENT_CLASSES[:-1])
    signals = Counter(flag for row in data["skills"] for flag in row["flags"])
    share = summary["changed_total"] * 100 / summary["pins_total"] if summary["pins_total"] else 0
    url = f"{PUBLIC_SITE}reports/skill-drift-2026-10/"
    title = "When skill guides change after a registry scan | October 2026"
    description = (f"The registry flagged {summary['changed_total']:,} of {summary['pins_total']:,} skill guides "
                   f"as changed. A cached comparison separates new commands, code examples, moves and removals.")
    observed = data.get("observation_finished_at", data["generated_at"])
    table = "".join(
        f'<tr><th scope="row">{CLASS_LABELS[key]}</th><td>{count:,}</td><td>{summary["class_percentages"][key]:.2f}%</td></tr>'
        for key, count in counts.items()
    )
    availability_labels = {
        "repo_404": "Repository unavailable or inaccessible",
        "branch_not_found": "Recorded branch no longer found",
        "available_now": "Source available again",
        "other": "Could not check availability",
    }
    availability_list = "".join(f"<li>{label}: <strong>{availability[key]:,}</strong></li>" for key, label in availability_labels.items())
    descriptions = {
        "adds_execution": "The upstream guide introduces a command to run that was absent from the archived version.",
        "adds_network": "The upstream guide adds an external URL that was absent from the archived version.",
        "widens_permissions": "The upstream frontmatter adds a tool or permission token.",
        "changes_code_examples": "The upstream guide adds or edits a code example without introducing a detected execution command.",
        "instructions_changed": "The upstream guide changes more than six substantive body lines.",
        "cosmetic": "The edits fall below the instruction-change threshold and introduce none of the higher-priority signals.",
        "removed": "The recorded file is missing and no matching guide was found in the complete upstream commit tree.",
    }
    examples = []
    for row in example_rows(data):
        primary = row["class"]
        explanation = (f"The guide moved to {row['moved_path']}; its content comparison is classified as “{CLASS_LABELS[row['moved_change_class']]}”."
                       if primary == "moved" else descriptions[primary])
        raw = row["evidence"][0] if row["evidence"] else ""
        if primary == "adds_execution" and (command := COMMAND_RE.search(re.sub(r"\\\r?\n\s*", " ", raw))):
            explanation = f"The guide now includes a command to run “{command.group().strip()[:150]}”."
        elif primary == "adds_network" and (link := URL_RE.search(raw)):
            explanation = f"The guide adds a link to {link.group().rstrip('.,;:!?)')}."
        elif primary in {"widens_permissions", "changes_code_examples", "instructions_changed", "cosmetic"} and raw:
            detail = next((line.strip() for line in raw.splitlines() if line.strip()), "")
            explanation = descriptions[primary].rstrip(".") + f", including “{detail[:180]}”."
        snippet = (f'<pre><code>{esc(row["evidence"][0])}</code></pre>' if row["evidence"] else
                   '<p class="note">No added lines are available to quote for this comparison.</p>')
        examples.append(f'''<li><h3>{esc(row.get('name', row['id']))}</h3>
<p class="note">{esc(row['repo'])} · {CLASS_LABELS[primary]}</p><p>{esc(explanation)}</p>{snippet}
<p><a href="{esc(row['archive_url'])}">Archived file at {esc(data['archive_commit'][:12])}</a> ·
<a href="{esc(row['upstream_url'])}">Upstream file at {esc(row['upstream_commit'][:12])}</a></p></li>''')
    structured = {"@context": "https://schema.org", "@type": "Article", "headline": title,
                  "description": description, "datePublished": observed[:10], "dateModified": data["generated_at"],
                  "mainEntityOfPage": url, "author": {"@type": "Organization", "name": "Claude Skill Registry"}}
    languages = ", ".join(sorted(EXEC_LANGUAGES))
    identical = signals["identical_bytes"]
    moved_failures = sum(row.get("moved_change_class") == "fetch_failed" for row in data["skills"])
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title><meta name="description" content="{esc(description)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary"><meta name="twitter:title" content="{esc(title)}"><meta name="twitter:description" content="{esc(description)}">
<script type="application/ld+json">{json.dumps(structured).replace('<', chr(92) + 'u003c')}</script>
<style>
:root{{--ink:#182238;--muted:#647087;--border:#e1e6ef;--accent:#4b46c6;--page:#f7f8fc;--surface:#fff;--code:#eef0f8;color-scheme:light}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--page);color:var(--ink);font:16px/1.7 system-ui,sans-serif}}
a{{color:var(--accent);overflow-wrap:anywhere}}header,main,footer{{max-width:808px;margin:auto;padding:1.5rem}}
header,footer{{border-bottom:1px solid var(--border)}}h1{{font-size:clamp(2rem,5vw,3rem);line-height:1.2;margin:.7rem 0 1.4rem}}
h2{{font-size:1.4rem;line-height:1.3}}h3{{font-size:1.1rem}}section{{margin:2.5rem 0}}.intro{{font-size:1.18rem}}.note,footer{{color:var(--muted);font-size:.9rem}}
.numbers{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.5rem 0}}.numbers div{{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1rem}}
.numbers strong{{display:block;font-size:2rem;line-height:1.3;color:var(--accent)}}.table-scroll{{overflow-x:auto}}table{{width:100%;min-width:480px;border-collapse:collapse;background:var(--surface)}}
th,td{{text-align:left;padding:.65rem;border-bottom:1px solid var(--border)}}td{{text-align:right;white-space:nowrap}}th{{font-weight:500}}
pre{{white-space:pre;overflow-x:auto;background:var(--code);padding:1rem;border-radius:8px;font:14px/1.6 ui-monospace,SFMono-Regular,Consolas,monospace}}
code{{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}}li{{margin:.7rem 0;overflow-wrap:anywhere}}.examples{{padding-left:1.4rem}}.examples>li{{margin-bottom:2.5rem}}
details{{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:1rem}}summary{{cursor:pointer;font-weight:600}}.limits{{font-size:.9rem;color:var(--muted)}}
@media(prefers-color-scheme:dark){{:root{{--ink:#e3e6f6;--muted:#a3aec3;--border:#35405a;--accent:#b2adff;--page:#131a29;--surface:#1c2538;--code:#202b41;color-scheme:dark}}}}
@media(max-width:600px){{main,header,footer{{padding:1rem}}.numbers{{gap:.6rem}}.numbers div{{padding:.8rem}}.numbers strong{{font-size:1.6rem}}}}
</style><script defer src="../../js/analytics.js"></script></head><body><header><a href="{PUBLIC_SITE}">Claude Skill Registry</a> / Research reports</header><main><article>
<p class="note">Observed {esc(observed[:10])} · October 2026 snapshot</p>
<h1>When skill guides change after a registry scan</h1>
<p class="intro">The registry’s checks flagged {summary['changed_total']:,} of {summary['pins_total']:,} skill guides ({share:.1f}%) as no longer matching the version it scanned.</p>
<div class="numbers">
<div><strong>{summary['changed_total']:,} / {summary['pins_total']:,}</strong>guides flagged as changed</div>
<div><strong>{counts['moved'] + counts['removed']:,}</strong>confirmed moved or removed<br><span class="note">{counts['moved']:,} moved, {counts['removed']:,} removed; see search coverage under <a href="#limits">Limits</a></span></div>
<div><strong>{substantive:,}</strong>guides with substantive edits</div>
<div><strong>{summary['unavailable_total']:,}</strong>sources previously unavailable</div>
</div>
<p>Among the files compared, <strong>{signals['new_execution_command']:,}</strong> added new commands to run, <strong>{signals['new_url']:,}</strong> added new external URLs, and <strong>{signals['permission_added_or_widened']:,}</strong> widened tool permissions. These signals can overlap. Substantive edits also include changed code examples and larger instruction rewrites.</p>
<p>These are changes to review, not safety verdicts. A new URL may be a citation, and a command may be an example. The results do not establish author intent.</p>
<section><h2>What changed</h2><p>Each of the {summary['changed_total']:,} flagged guides has one primary label. Higher-priority signals take precedence; all detected signals remain in the downloadable data. Moved guides keep a separate content comparison.</p>
<div class="table-scroll" role="region" aria-label="Change classifications" tabindex="0"><table><thead><tr><th scope="col">Change</th><th scope="col">Guides</th><th scope="col">Share of flagged guides</th></tr></thead><tbody>{table}</tbody></table></div>
<p class="note">“Small edits” includes {identical:,} guides whose bytes now match the archive again. Small textual changes can still affect meaning.</p></section>
<section><h2>The sources that disappeared</h2><p>Separately, the registry had recorded {summary['unavailable_total']:,} unavailable sources. Rechecking the recorded repository and branch gives:</p><ul>{availability_list}</ul>
<p>A repository returning “not found” may be private or inaccessible; this does not prove deletion. An accessible repository with no recorded branch stays unresolved. Recovered sources are counted here without a new content comparison.</p></section>
<section><h2>Examples you can inspect</h2><p>These examples cover the confirmed change types and favor moderate diffs. Each snippet quotes up to four added lines with their original spacing. The links fix both versions to commits; a removal link points to the missing upstream location.</p><ol class="examples">{''.join(examples)}</ol></section>
<section><h2>How we measured</h2>
<p>We selected guides that the registry’s install-pin checks had marked as changed or unavailable. For each changed guide, we verified the archived file against its recorded SHA-256 digest before comparing it. We resolved each upstream branch once and used that commit for file retrieval, move searches and evidence links. When the recorded path was missing, we searched the same commit tree for a guide with the archived directory name or frontmatter name. We then applied textual rules to distinguish commands, URLs, permission additions, code examples and instruction edits. The observations span {esc(day(data.get('observation_started_at', data['generated_at'])))} through {esc(day(observed))} (UTC). These are observations at different times, rather than one simultaneous snapshot of every source.</p>
<p class="note">Input checks: {esc(' through '.join(day(value) for value in data['pin_checked_range']) or 'not recorded')}. Content history starts {esc(day(data['history_since']) or 'not recorded')}; this is not the date an author edited a file. <a href="https://github.com/{DATA_REPO}/tree/{data['archive_commit']}">Archive snapshot at {esc(data['archive_commit'][:12])}</a>.</p>
<details><summary>Precise comparison rules</summary><ul>
<li>Priority is: adds new commands to run, adds new external URLs, widens tool permissions, changes code examples, rewrites instructions, then small edits. Flags can overlap; primary labels cannot.</li>
<li>A new command is a download using curl or wget piped to sh, bash or Python; an npx, uvx or pip install command; Python, bash, sh, Node, Ruby or Perl followed by a script path; or a relative executable beginning with <code>./</code>. Interpreter script suffixes are .py, .sh, .js, .mjs, .rb and .pl; relative executables also accept .cjs, .ps1 or no suffix. Commands are compared as whitespace-normalized sets, joining shell backslash-newline continuations. A changed command counts as new even inside an example.</li>
<li>A closed, nonempty fenced block in one of these languages is a code example: {esc(languages)}. A block is changed when its whitespace-normalized content is new. Plain text, JSON and YAML fences do not qualify by themselves.</li>
<li>New external URLs are new HTTP or HTTPS URLs, including new paths on an existing domain. Localhost and loopback addresses are excluded. New hostnames are recorded separately.</li>
<li>Frontmatter fields named allowed-tools, allowed_tools, tools, tool, permissions or permission are checked at any mapping depth. Added flattened tokens count as wider permissions; list order is ignored, values split on whitespace or commas, mapping paths are kept, and false or null grants no tokens. This does not model tool-specific permission semantics. Unparseable YAML is flagged.</li>
<li>Instruction rewrites exceed six added plus removed nonempty body lines after removing whitespace and Markdown formatting characters (<code>` * _ # &gt; | ~ -</code>). Letter case and other punctuation remain significant. Paragraph reflow with identical joined normalized text counts as zero; other frontmatter changes do not count toward this threshold. Remaining edits, including identical bytes, are small edits.</li>
<li>A moved guide must be a SKILL.md in the same resolved commit with a matching parent directory or archived frontmatter name. Directory matches take precedence, then the lexicographically first matching path. Its content is compared normally. No match after a complete search means removed; failed or truncated trees and incomplete name searches remain unchecked.</li>
<li>Unavailable sources are checked independently: a missing repository is unavailable or inaccessible; an accessible repository with a missing recorded branch has a branch failure. Unknown branches and other errors remain unresolved.</li>
<li>Only SKILL.md is compared; bundled assets are outside this report. No commands are run. Successful responses and missing-file responses are cached. Transient errors are retried twice and not cached; rate-limit responses are reported without repeated retries. Reusing the cache preserves previously resolved commits.</li>
</ul></details></section>
<section><h2>What this means for you</h2>
<p><strong>Users:</strong> Prefer installs pinned to a commit and digest. For a registry guide offering verified installation, use <code>npx skills add &lt;registry guide URL&gt;</code> and check its recorded commit and digest. Re-read SKILL.md and review bundled files before updating. A pin identifies the checked bytes; it is not a guarantee of safety.</p>
<p><strong>Authors:</strong> Tag releases, keep skill paths stable, and describe changes so users can make informed update decisions.</p>
<p><strong>Registries and installers:</strong> Pin content by commit and digest, and show content history so users can see what changed after a scan.</p></section>
<section class="limits" id="limits"><h2>Limits</h2><p>{counts['path_missing_unchecked']:,} missing-path searches could not be completed; {counts['fetch_failed']:,} content comparisons and {moved_failures:,} moved-file comparisons failed; {availability['other']:,} availability checks remain unresolved. Every affected row retains its reason in the data. Unchecked paths are neither confirmed moves nor confirmed removals.</p>
<p>Textual heuristics can miss unfenced code, prose permissions and non-HTTP links. Formatting normalization can hide meaningful small edits. Cached errors and missing responses reflect the observation, not guaranteed current availability.</p></section>
<p><a href="data.json">Download the complete data</a> · <a href="https://github.com/majiayu000/claude-skill-registry-core/blob/main/scripts/analyze_upstream_drift.py">Analyzer source</a></p>
</article></main><footer>Claude Skill Registry · Observations with explicit uncertainty.</footer></body></html>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pins", type=Path, default=Path("install-pins.json"))
    parser.add_argument("--history", type=Path, default=Path("skill-content-history.json"))
    parser.add_argument("--catalog", type=Path, help="Optional docs/page-catalog.json; otherwise link repositories")
    parser.add_argument("--cache", type=Path, default=Path(".cache/upstream-drift-2026-10"))
    parser.add_argument("--output", type=Path, default=Path("docs/reports/skill-drift-2026-10"))
    parser.add_argument("--workers", type=int, default=8, choices=range(1, 17))
    parser.add_argument("--cache-only", action="store_true", help="Replay cached responses without network requests; uncached checks stay unresolved")
    args = parser.parse_args()
    token = os.environ.get("GITHUB_TOKEN", "")
    pins = json.loads(args.pins.read_text())["pins"]
    catalog = {row["id"]: row for row in json.loads(args.catalog.read_text())["skills"]} if args.catalog else {}
    fetcher = CachedFetcher(args.cache, token, cache_only=args.cache_only)
    data = analyze(pins, load_history(args.history), fetcher, workers=args.workers, catalog=catalog)
    timestamps = [json.loads(path.read_text())["fetched_at"] for path in args.cache.glob("*.json")]
    data["observation_started_at"], data["observation_finished_at"] = min(timestamps, default=data["generated_at"]), max(timestamps, default=data["generated_at"])
    data["inputs"] = {"pins_sha256": sha256_digest(args.pins.read_bytes()), "history_sha256": sha256_digest(args.history.read_bytes())}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "data.json").write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (args.output / "index.html").write_text(render_report(data), encoding="utf-8")
    print(json.dumps(data["summary"], indent=2))
    return 1 if data["summary"]["failure_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
