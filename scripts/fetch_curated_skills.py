#!/usr/bin/env python3
"""Fetch full upstream directories for verified EXEC/REF_ASSET skills.

Usage:
  python scripts/fetch_curated_skills.py <verified.jsonl> <dest_dir> <report.json>

Input: JSONL from verify_upstream_assets.py; only rows with status EXEC or
REF_ASSET are fetched. Layout: <dest>/<owner>__<repo>/<skill_basename>/...
with a _provenance.json per skill recording source, stars, and fetch errors.
"""
from __future__ import annotations

import collections
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_asset_audit import fetch_repo_tree


def fetch_file(repo: str, path: str, local_path: str) -> None:
    result = subprocess.run(
        ["gh", "api", f"repos/{repo}/contents/{path}",
         "-H", "Accept: application/vnd.github.raw"],
        capture_output=True,
        timeout=120,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode(errors="replace")[:150])
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    with open(local_path, "wb") as fh:
        fh.write(result.stdout)


def fetch_skill(repo: str, target: dict, dest: str) -> dict:
    skill_dir = target["resolved_dir"]
    prefix = skill_dir + "/"
    paths = [p for p in target["_tree"] if p.startswith(prefix)]
    if not paths:
        return {**target, "fetch": "gone"}
    local_root = os.path.join(dest, repo.replace("/", "__"), os.path.basename(skill_dir))
    fetched, errors = 0, []
    for path in paths:
        try:
            fetch_file(repo, path, os.path.join(local_root, path[len(prefix):]))
            fetched += 1
        except (RuntimeError, subprocess.TimeoutExpired) as exc:
            errors.append({"path": path, "error": str(exc)})
    provenance = {
        "repo": repo,
        "dir": skill_dir,
        "stars": target.get("stars"),
        "fetched_files": fetched,
        "errors": errors,
        "source": f"https://github.com/{repo}/tree/HEAD/{skill_dir}",
    }
    with open(os.path.join(local_root, "_provenance.json"), "w", encoding="utf-8") as fh:
        json.dump(provenance, fh, indent=2)
    return {**{k: v for k, v in target.items() if k != "_tree"},
            "fetch": "ok" if not errors else "partial",
            "files_fetched": fetched, "files_failed": len(errors), "local": local_root}


def main() -> None:
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    verified_path, dest, report_path = sys.argv[1:4]
    rows = [json.loads(line) for line in open(verified_path, encoding="utf-8")]
    targets = [r for r in rows if r.get("status") in ("EXEC", "REF_ASSET")]
    by_repo: dict[str, list[dict]] = collections.defaultdict(list)
    for target in targets:
        by_repo[target["repo"]].append(target)

    report = []
    for i, (repo, repo_targets) in enumerate(sorted(by_repo.items()), 1):
        try:
            tree = fetch_repo_tree(repo)
        except Exception as exc:  # noqa: BLE001 — recorded per row
            report.extend({**t, "fetch": "repo_error", "error": str(exc)[:200]}
                          for t in repo_targets)
            continue
        for target in repo_targets:
            report.append(fetch_skill(repo, {**target, "_tree": tree}, dest))
        print(f"[{i}/{len(by_repo)}] {repo}", file=sys.stderr)

    with open(report_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    summary = collections.Counter(r["fetch"] for r in report)
    print(json.dumps(dict(summary), indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
