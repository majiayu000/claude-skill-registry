#!/usr/bin/env python3
"""
Backfill attribution and license metadata for archived skills.

The script is intentionally resumable:
- repo license lookups are cached in a JSON file
- dry-run is the default
- --apply is required before metadata files are modified
"""

from __future__ import annotations

import argparse
import base64
import http.client
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from utils import build_legal_metadata, normalize_license, normalize_repo

LEGAL_FIELDS = (
    "author",
    "source_url",
    "license",
    "copyright",
    "permission_note",
    "distribution",
)

PLACEHOLDER_VALUES = {"", "n/a", "na", "none", "null", "tbd", "unknown"}


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def is_missing(value: Any) -> bool:
    return str(value or "").strip().lower() in PLACEHOLDER_VALUES


def needs_backfill(metadata: dict[str, Any]) -> bool:
    return any(is_missing(metadata.get(field)) for field in LEGAL_FIELDS)


def skill_source_path(metadata: dict[str, Any]) -> str:
    return str(
        metadata.get("github_path") or metadata.get("path") or metadata.get("install") or ""
    ).strip()


def skill_branch(metadata: dict[str, Any]) -> str:
    return str(metadata.get("github_branch") or metadata.get("branch") or "main").strip() or "main"


def extract_copyright_notice(license_text: str) -> str:
    for line in license_text.splitlines():
        text = line.strip()
        if re.match(
            r"^(copyright\s+(?:\(c\)|©|\d{4})|\(c\)\s+\d{4}|©\s*\d{4})(?=\s|$)",
            text,
            flags=re.IGNORECASE,
        ):
            return text
    return ""


def github_request(url: str, token: str, timeout: int) -> dict[str, Any]:
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "claude-skill-registry-license-backfill",
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_repo_license(repo: str, token: str, timeout: int) -> dict[str, str]:
    url = f"https://api.github.com/repos/{repo}/license"
    for attempt in range(3):
        try:
            payload = github_request(url, token=token, timeout=timeout)
            break
        except urllib.error.HTTPError as exc:
            if exc.code in {403, 404, 451}:
                return {"license": "NOASSERTION", "copyright": "", "error": f"http_{exc.code}"}
            raise
        except (TimeoutError, http.client.IncompleteRead, urllib.error.URLError, OSError) as exc:
            if attempt < 2:
                time.sleep(1 + attempt)
                continue
            reason = getattr(exc, "reason", exc)
            return {
                "license": "NOASSERTION",
                "copyright": "",
                "error": f"fetch_error:{reason}",
            }
    else:  # pragma: no cover - loop always returns or breaks
        return {"license": "NOASSERTION", "copyright": "", "error": "fetch_failed"}

    license_payload = payload.get("license") or {}
    spdx = normalize_license(str(license_payload.get("spdx_id") or "NOASSERTION"))
    content = str(payload.get("content") or "")
    license_text = ""
    if content:
        try:
            license_text = base64.b64decode(content, validate=False).decode(
                "utf-8", errors="ignore"
            )
        except Exception:
            license_text = ""

    return {
        "license": spdx,
        "copyright": extract_copyright_notice(license_text),
        "license_url": str(payload.get("html_url") or ""),
    }


def load_or_fetch_license(
    repo: str,
    cache: dict[str, dict[str, str]],
    *,
    fetch: bool,
    token: str,
    timeout: int,
    sleep_seconds: float,
) -> dict[str, str]:
    if repo in cache:
        return cache[repo]
    if not fetch:
        cache[repo] = {"license": "NOASSERTION", "copyright": "", "error": "not_fetched"}
        return cache[repo]

    result = fetch_repo_license(repo, token=token, timeout=timeout)
    cache[repo] = result
    if sleep_seconds > 0:
        time.sleep(sleep_seconds)
    return result


def backfill_metadata(metadata: dict[str, Any], repo_license: dict[str, str]) -> dict[str, Any]:
    repo = normalize_repo(str(metadata.get("repo") or ""))
    license_name = metadata.get("license") or repo_license.get("license") or "NOASSERTION"
    copyright_text = metadata.get("copyright") or repo_license.get("copyright") or ""

    legal = build_legal_metadata(
        repo=repo,
        path=skill_source_path(metadata),
        branch=skill_branch(metadata),
        source_url=str(metadata.get("source_url") or ""),
        author=str(metadata.get("author") or ""),
        license_name=str(license_name),
        copyright_text=str(copyright_text),
        permission_note=str(metadata.get("permission_note") or ""),
        distribution=str(metadata.get("distribution") or ""),
    )

    updated = dict(metadata)
    for key, value in legal.items():
        if is_missing(updated.get(key)):
            updated[key] = value
    return updated


def iter_metadata_files(skills_dir: Path) -> list[Path]:
    return sorted(skills_dir.rglob("metadata.json"))


def main() -> int:
    parser = argparse.ArgumentParser(description="Backfill missing legal metadata fields")
    parser.add_argument("--skills-dir", default="skills")
    parser.add_argument("--cache", default=".tmp/repo-license-cache.json")
    parser.add_argument("--report", default="")
    parser.add_argument("--repo", action="append", default=[], help="Restrict to repo owner/name")
    parser.add_argument("--apply", action="store_true", help="Modify metadata.json files")
    parser.add_argument(
        "--fetch-github", action="store_true", help="Fetch repo licenses from GitHub"
    )
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--max-repos", type=int, default=0)
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--sleep", type=float, default=0.0)
    args = parser.parse_args()

    repo_root = Path.cwd()
    skills_dir = (repo_root / args.skills_dir).resolve()
    cache_path = (repo_root / args.cache).resolve()
    report_path = (repo_root / args.report).resolve() if args.report else None
    allowed_repos = {normalize_repo(repo) for repo in args.repo}

    if not skills_dir.exists():
        print(f"ERROR: skills directory not found: {skills_dir}", file=sys.stderr)
        return 1

    token = os.environ.get(args.token_env, "")
    cache: dict[str, dict[str, str]] = load_json(cache_path, {})
    changed_files: list[str] = []
    skipped_repos: set[str] = set()
    stats = {
        "scanned": 0,
        "eligible": 0,
        "changed": 0,
        "unchanged": 0,
        "repos_seen": 0,
        "repos_cached": len(cache),
    }

    repos_seen: set[str] = set()
    for metadata_path in iter_metadata_files(skills_dir):
        if args.max_files and stats["scanned"] >= args.max_files:
            break
        stats["scanned"] += 1

        try:
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        except Exception:
            continue

        repo = normalize_repo(str(metadata.get("repo") or ""))
        if allowed_repos and repo not in allowed_repos:
            continue
        if not repo or "/" not in repo:
            continue
        if not needs_backfill(metadata):
            continue

        stats["eligible"] += 1
        if repo not in repos_seen and args.max_repos and len(repos_seen) >= args.max_repos:
            skipped_repos.add(repo)
            continue
        repos_seen.add(repo)

        had_cache = repo in cache
        repo_license = load_or_fetch_license(
            repo,
            cache,
            fetch=args.fetch_github,
            token=token,
            timeout=args.timeout,
            sleep_seconds=args.sleep,
        )
        if not had_cache:
            write_json(cache_path, cache)
        updated = backfill_metadata(metadata, repo_license)
        if updated == metadata:
            stats["unchanged"] += 1
            continue

        stats["changed"] += 1
        changed_files.append(str(metadata_path.relative_to(skills_dir.parent)))
        if args.apply:
            metadata_path.write_text(
                json.dumps(updated, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    stats["repos_seen"] = len(repos_seen)
    stats["repos_skipped_by_limit"] = len(skipped_repos)
    write_json(cache_path, cache)

    report = {
        **stats,
        "apply": args.apply,
        "fetch_github": args.fetch_github,
        "changed_files": changed_files[:1000],
    }
    if report_path:
        write_json(report_path, report)

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
