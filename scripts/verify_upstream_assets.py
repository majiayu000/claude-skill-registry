#!/usr/bin/env python3
"""Verify claimed bundled assets against upstream GitHub repositories.

Usage:
  python scripts/verify_upstream_assets.py <targets.jsonl> <out.jsonl>

Input: JSONL from `audit_skill_assets.py targets` (repo, dir, stars, name).
One tree API call per unique repo; each skill dir is located in the tree and
its sibling files classified. Statuses: EXEC, REF_ASSET, BARE, not_found,
root_ambiguous, repo_error. Summary JSON is printed to stderr.
"""
from __future__ import annotations

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_asset_audit import classify_files, fetch_repo_tree, verdict_from_counts


def resolve_skill_dir(target: dict, skill_dirs: list[str]) -> str | None:
    """Match a target to a SKILL.md-containing dir in the upstream tree."""
    declared = target.get("dir") or ""
    if declared and declared in skill_dirs:
        return declared
    name = target.get("name") or ""
    candidates = [d for d in skill_dirs if os.path.basename(d) == name]
    if not candidates and name:
        candidates = [d for d in skill_dirs if name in d]
    return candidates[0] if candidates else None


def verify_repo(repo: str, targets: list[dict]) -> list[dict]:
    try:
        paths = fetch_repo_tree(repo)
    except Exception as exc:  # noqa: BLE001 — recorded per row
        return [{**t, "status": "repo_error", "error": str(exc)[:200]} for t in targets]
    skill_dirs = [os.path.dirname(p) for p in paths if os.path.basename(p) == "SKILL.md"]
    rows = []
    for target in targets:
        resolved = resolve_skill_dir(target, skill_dirs)
        if resolved is None:
            rows.append({**target, "status": "not_found"})
            continue
        if resolved == "":
            rows.append({**target, "status": "root_ambiguous"})
            continue
        siblings = [p for p in paths if p.startswith(resolved + "/")]
        counts = classify_files(siblings)
        rows.append({
            **target,
            "resolved_dir": resolved,
            "status": verdict_from_counts(counts),
            **counts,
        })
    return rows


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    targets = [json.loads(line) for line in open(sys.argv[1], encoding="utf-8")]
    by_repo: dict[str, list[dict]] = collections.defaultdict(list)
    for target in targets:
        by_repo[target["repo"]].append(target)

    summary: collections.Counter = collections.Counter()
    with open(sys.argv[2], "w", encoding="utf-8") as out:
        for i, (repo, repo_targets) in enumerate(sorted(by_repo.items()), 1):
            for row in verify_repo(repo, repo_targets):
                summary[row["status"]] += 1
                out.write(json.dumps(row) + "\n")
            if i % 25 == 0:
                print(f"[{i}/{len(by_repo)}] verified", file=sys.stderr)
    print(json.dumps(dict(summary), indent=2), file=sys.stderr)


if __name__ == "__main__":
    main()
