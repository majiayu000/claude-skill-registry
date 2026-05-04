#!/usr/bin/env python3
"""Shared security blocklist helpers for source repositories."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
DEFAULT_BLOCKLIST_PATH = ROOT_DIR / "sources" / "security_blocklist.json"


def normalize_repo_id(repo: str) -> str:
    """Normalize GitHub repo identifiers to lowercase owner/name form."""
    repo = (repo or "").strip()
    for prefix in ("https://github.com/", "http://github.com/", "github.com/"):
        if repo.startswith(prefix):
            repo = repo[len(prefix):]
            break
    repo = repo.split("/tree/")[0]
    repo = repo.split("/blob/")[0]
    repo = repo.strip("/")
    parts = [part for part in repo.split("/") if part]
    if len(parts) >= 2:
        return f"{parts[0]}/{parts[1]}".lower()
    return repo.lower()


def load_security_blocklist(path: Path | None = None) -> dict[str, dict[str, Any]]:
    """Load blocked source repos keyed by normalized repo id."""
    blocklist_path = path or DEFAULT_BLOCKLIST_PATH
    if not blocklist_path.exists():
        raise FileNotFoundError(f"security blocklist is missing: {blocklist_path}")

    payload = json.loads(blocklist_path.read_text(encoding="utf-8"))
    entries = payload.get("blocked_repos", payload) if isinstance(payload, dict) else payload
    if not isinstance(entries, list):
        raise ValueError(f"security blocklist must be a list: {blocklist_path}")

    blocked: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError(f"security blocklist entry must be an object: {entry!r}")
        repo = normalize_repo_id(str(entry.get("repo") or ""))
        if not repo:
            raise ValueError(f"security blocklist entry missing repo: {entry!r}")
        action = str(entry.get("action") or "reject").strip().lower()
        if action != "reject":
            raise ValueError(f"unsupported security blocklist action for {repo}: {action}")
        blocked[repo] = {**entry, "repo": repo, "action": action}
    return blocked


def blocked_repo_entry(repo: str, blocklist: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    """Return the blocklist entry for repo, if any."""
    return blocklist.get(normalize_repo_id(repo))


def blocked_metadata_source(
    metadata: dict[str, Any],
    blocklist: dict[str, dict[str, Any]],
) -> tuple[dict[str, Any], str] | None:
    """Return the blocked repo entry and metadata field, if metadata identifies one."""
    for field in (
        "repo",
        "source",
        "source_url",
        "github_url",
        "repository",
        "repository_url",
        "html_url",
        "url",
    ):
        value = metadata.get(field)
        if not isinstance(value, str):
            continue
        entry = blocked_repo_entry(value, blocklist)
        if entry:
            return entry, field

    for field in ("github_path", "path"):
        value = metadata.get(field)
        if not isinstance(value, str):
            continue
        normalized_path = value.strip().strip("/").lower()
        for repo, entry in blocklist.items():
            if normalized_path == repo or normalized_path.startswith(f"{repo}/"):
                return entry, field

    return None
