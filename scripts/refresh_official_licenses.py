#!/usr/bin/env python3
"""Refresh license metadata of official archives from their upstream source.

Archives are never re-downloaded, so a later upstream relicense would otherwise
never reach the registry. For every archive whose repo is listed in
``policy/official-sources.json`` this reads the upstream SKILL.md and license
files from raw.githubusercontent.com (no API quota) and applies the upstream
license when the archived Markdown body still matches the upstream body. An
older archived version keeps the terms it was published under, unless it is a
single-file archive without an open-source license and upstream now has one:
then the archived SKILL.md is replaced with the current upstream file.

Dry-run is the default; ``--apply`` writes changes. Fetch errors exit nonzero.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Callable
from urllib.parse import quote

from audit_skill_assets import canonical_source_identity_from_metadata
from official_sources import is_official_repo
from sync_download_support import exact_source_branch
from utils import (
    classify_license,
    extract_frontmatter,
    infer_author,
    is_unresolved_license,
    resolve_license,
    with_resolved_license,
)
from withheld_archives import body_allowed, body_fingerprint, iter_archive_dirs, read_metadata

RAW_BASE = "https://raw.githubusercontent.com"
LICENSE_FILENAMES = ("LICENSE.txt", "LICENSE", "LICENSE.md")
LEGAL_KEYS = ("license", "distribution", "permission_note", "license_class", "author")

Fetcher = Callable[[str], "str | None"]


def fetch_raw(url: str, timeout: int = 20) -> str | None:
    """Return the file text, None for a missing file; other failures raise."""
    request = urllib.request.Request(url, headers={"User-Agent": "claude-skill-registry"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise


def detect_license_text(text: str) -> str:
    """Identify common full license texts; return '' when unsure."""
    flat = " ".join(text.split())
    if "Apache License" in flat and "Version 2.0" in flat:
        return "Apache-2.0"
    if "Permission is hereby granted, free of charge" in flat and 'PROVIDED "AS IS"' in flat:
        return "MIT"
    return ""


def upstream_license(repo: str, branch: str, skill_path: str, fetch: Fetcher) -> tuple[str, str]:
    """Return (license, upstream SKILL.md text); ('', '') when the skill is gone upstream."""
    base = f"{RAW_BASE}/{repo}/{quote(branch, safe='')}"
    skill_text = fetch(f"{base}/{quote(skill_path, safe='/')}")
    if skill_text is None:
        return "", ""
    declared = extract_frontmatter(skill_text).get("license")
    if not is_unresolved_license(declared) and classify_license(str(declared)) == "compatible":
        return resolve_license(declared), skill_text
    skill_dir = PurePosixPath(skill_path).parent
    directories = [skill_dir] if str(skill_dir) not in {"", "."} else []
    for directory in [*directories, PurePosixPath("")]:
        for filename in LICENSE_FILENAMES:
            path = (directory / filename).as_posix()
            text = fetch(f"{base}/{quote(path, safe='/')}")
            if text is not None and (detected := detect_license_text(text)):
                return detected, skill_text
    return resolve_license(declared), skill_text


def archived_fingerprint(skill_dir: Path, metadata: dict) -> str:
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        return body_fingerprint(skill_md.read_text(encoding="utf-8"))
    return str(metadata.get("content_fingerprint") or "")


def refresh_archives(skills_dir: Path, *, apply: bool, fetch: Fetcher = fetch_raw) -> dict:
    summary: dict = {"official": 0, "updated": [], "body_refreshed": [], "unchanged": 0,
                     "body_differs": [], "upstream_missing": [], "no_source_path": [],
                     "errors": []}
    for skill_dir in iter_archive_dirs(skills_dir):
        metadata = read_metadata(skill_dir)
        if not is_official_repo(str(metadata.get("repo") or "")):
            continue
        summary["official"] += 1
        label = skill_dir.relative_to(skills_dir).as_posix()
        repo, skill_path, error = canonical_source_identity_from_metadata(metadata)
        if error:
            summary["no_source_path"].append(f"{label}: {error}")
            continue
        branch = exact_source_branch(metadata) or "main"
        try:
            license_name, upstream_text = upstream_license(repo, branch, skill_path, fetch)
        except Exception as exc:  # noqa: BLE001 - every failure is reported and fails the run
            summary["errors"].append(f"{label}: {type(exc).__name__}: {exc}")
            continue
        if not upstream_text:
            summary["upstream_missing"].append(label)
            continue
        refreshed = with_resolved_license(metadata, license_name)
        refreshed["author"] = infer_author(repo, str(metadata.get("author") or ""))
        if archived_fingerprint(skill_dir, metadata) != body_fingerprint(upstream_text):
            single_file = not metadata.get("bundled_files") and not metadata.get("github_commit_sha")
            relicensed = not body_allowed(metadata) and body_allowed(refreshed)
            if not (single_file and relicensed):
                summary["body_differs"].append(label)
                continue
            summary["body_refreshed"].append(f"{label}: {metadata.get('license')} -> {refreshed['license']}")
            if apply:
                refreshed["downloaded_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
                refreshed.pop("content_fingerprint", None)
                (skill_dir / "SKILL.md").write_text(upstream_text, encoding="utf-8")
                (skill_dir / "metadata.json").write_text(
                    json.dumps(refreshed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
                )
            continue
        if all(refreshed.get(key) == metadata.get(key) for key in LEGAL_KEYS):
            summary["unchanged"] += 1
            continue
        summary["updated"].append(f"{label}: {metadata.get('license')} -> {refreshed['license']}")
        if apply:
            (skill_dir / "metadata.json").write_text(
                json.dumps(refreshed, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
    return summary


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--apply", action="store_true", help="write refreshed metadata")
    args = parser.parse_args(argv)
    summary = refresh_archives(args.skills_dir, apply=args.apply, fetch=fetch_raw)
    print(json.dumps({**summary, "applied": args.apply}, indent=2))
    if summary["errors"]:
        print(f"error: {len(summary['errors'])} official archives could not be refreshed", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
