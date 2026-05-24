#!/usr/bin/env python3
"""Report current registry category counts under canonical taxonomy targets."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from category_taxonomy import CategoryTaxonomy, get_taxonomy


def iter_registry_skills(shards_dir: Path):
    for shard_path in sorted(shards_dir.glob("*.json")):
        payload = json.loads(shard_path.read_text(encoding="utf-8"))
        skills = payload.get("skills") if isinstance(payload, dict) else None
        if not isinstance(skills, list):
            continue
        for skill in skills:
            if isinstance(skill, dict):
                yield skill


def canonical_target_for(
    raw_category: str | None,
    taxonomy: CategoryTaxonomy,
) -> tuple[str, str]:
    slug = taxonomy.resolve(raw_category, allow_unknown=True)
    if taxonomy.is_publishable(slug):
        return slug, "canonical"

    migration = taxonomy.legacy_migration(slug)
    if migration and migration.target:
        return migration.target, "legacy_migration"
    if migration:
        return "review-required", "legacy_review"
    return "unknown", "unknown"


def build_report(shards_dir: Path, taxonomy: CategoryTaxonomy | None = None) -> dict[str, Any]:
    taxonomy = taxonomy or get_taxonomy()
    source_counts: Counter[str] = Counter()
    target_counts: Counter[str] = Counter()
    reason_counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = {}
    total = 0

    for skill in iter_registry_skills(shards_dir):
        total += 1
        source = str(skill.get("category") or taxonomy.default_category)
        target, reason = canonical_target_for(source, taxonomy)
        source_counts[source] += 1
        target_counts[target] += 1
        reason_counts[reason] += 1
        if target in {"review-required", "unknown"}:
            examples.setdefault(target, [])
            if len(examples[target]) < 20:
                examples[target].append(str(skill.get("path") or skill.get("name") or ""))

    return {
        "source_shards_dir": str(shards_dir),
        "total_skills": total,
        "canonical_category_count": len(taxonomy.publishable_categories()),
        "legacy_migration_count": len(taxonomy.legacy_migrations),
        "source_category_counts": dict(sorted(source_counts.items())),
        "target_category_counts": dict(sorted(target_counts.items())),
        "reason_counts": dict(sorted(reason_counts.items())),
        "review_examples": examples,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry-shards", type=Path, default=Path("registry-shards"))
    parser.add_argument("--output-json", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args.registry_shards)
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        "Canonical target report "
        f"(skills={report['total_skills']}, targets={len(report['target_category_counts'])})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
