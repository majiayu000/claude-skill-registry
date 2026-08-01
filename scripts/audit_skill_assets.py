#!/usr/bin/env python3
"""Census of bundled-asset references across the archived skill corpus.

Usage:
  python scripts/audit_skill_assets.py census <data_repo_root>
  python scripts/audit_skill_assets.py targets <data_repo_root> [min_stars]

`census` prints bucket statistics (EXEC / REF / BARE) as JSON.
`targets` prints JSONL of deduped EXEC candidates at or above min_stars
(default 100) for upstream verification by verify_upstream_assets.py.
"""
from __future__ import annotations

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_asset_audit import classify_skill_text, iter_archived_skills


def _read_skill(dirpath: str) -> str:
    with open(os.path.join(dirpath, "SKILL.md"), encoding="utf-8", errors="replace") as fh:
        return fh.read()


def run_census(root: str) -> dict:
    buckets: collections.Counter = collections.Counter()
    sizes: dict[str, list[int]] = collections.defaultdict(list)
    for dirpath, _meta in iter_archived_skills(root):
        text = _read_skill(dirpath)
        bucket = classify_skill_text(text)
        buckets[bucket] += 1
        sizes[bucket].append(len(text))
    total = sum(buckets.values())
    if not total:
        raise SystemExit(f"no SKILL.md found under {root}")

    def median(values: list[int]) -> int:
        values = sorted(values)
        return values[len(values) // 2] if values else 0

    return {
        "total_skills": total,
        "buckets": dict(buckets),
        "bucket_pct": {k: round(v * 100 / total, 1) for k, v in buckets.items()},
        "median_skill_md_bytes": {k: median(v) for k, v in sizes.items()},
    }


def run_targets(root: str, min_stars: int) -> None:
    seen: set[tuple[str, str]] = set()
    for dirpath, meta in iter_archived_skills(root):
        if not meta:
            continue
        stars = meta.get("stars") or 0
        repo = meta.get("repo") or ""
        if stars < min_stars or not repo:
            continue
        if classify_skill_text(_read_skill(dirpath)) != "EXEC":
            continue
        skill_dir = os.path.dirname(meta.get("path") or "")
        key = (repo, skill_dir)
        if key in seen:
            continue
        seen.add(key)
        print(json.dumps({
            "repo": repo,
            "dir": skill_dir,
            "stars": stars,
            "name": meta.get("name", ""),
        }))


def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] not in ("census", "targets"):
        raise SystemExit(__doc__)
    mode, root = sys.argv[1], sys.argv[2]
    if mode == "census":
        print(json.dumps(run_census(root), indent=2))
    else:
        run_targets(root, int(sys.argv[3]) if len(sys.argv) > 3 else 100)


if __name__ == "__main__":
    main()
