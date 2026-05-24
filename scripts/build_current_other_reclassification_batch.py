#!/usr/bin/env python3
"""Build an auditable live-archive reclassification batch for current categories."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from build_residual_category_worksets import (
    SCHEMA_VERSION,
    parse_csv,
    sorted_counter,
    work_item_for_skill,
)
from plan_category_migration import iter_skill_dirs


def build_manifest(
    *,
    batch_id: str,
    skills_dir: Path,
    output_dir: Path,
    input_jsonl: Path,
    from_categories: set[str],
    limit: int | None,
    offset: int,
    content_chars: int,
    selected: list[dict[str, Any]],
    matching_total_count: int,
    archive_counts: Counter[str],
) -> dict[str, Any]:
    classify_output = output_dir / "classification.jsonl"
    classify_report = output_dir / "classification-report.json"
    checkpoint = output_dir / "checkpoint.jsonl"
    apply_plan = output_dir / "apply-plan.json"
    sample_audit = output_dir / "sample-audit.json"
    residual_report = output_dir / "residual-report.json"
    residual_worksets_report = output_dir / "residual-worksets.json"
    residual_worksets_dir = output_dir / "residual-worksets"
    from_category_flags = " ".join(
        f"--from-category {category}" for category in sorted(from_categories)
    )
    return {
        "schema_version": SCHEMA_VERSION,
        "batch_id": batch_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(skills_dir),
        "input_jsonl": str(input_jsonl),
        "policy": {
            "from_categories": sorted(from_categories),
            "limit": limit,
            "offset": offset,
            "content_chars": content_chars,
            "apply_mode": "review-only",
        },
        "summary": {
            "archive_category_counts": sorted_counter(archive_counts),
            "matching_category_skill_count": matching_total_count,
            "selected_input_count": len(selected),
            "selected_category_counts": sorted_counter(
                Counter(str(item.get("current_category") or "") for item in selected)
            ),
        },
        "artifacts": {
            "input_jsonl": str(input_jsonl),
            "classification_jsonl": str(classify_output),
            "classification_report": str(classify_report),
            "checkpoint_jsonl": str(checkpoint),
            "apply_plan": str(apply_plan),
            "sample_audit": str(sample_audit),
            "residual_report": str(residual_report),
            "residual_worksets_report": str(residual_worksets_report),
            "residual_worksets_dir": str(residual_worksets_dir),
        },
        "commands": [
            (
                "python scripts/classify_residual_workset_with_llm.py "
                f"--workset-jsonl {input_jsonl} "
                f"--classification-output {classify_output} "
                f"--output {classify_report} "
                f"--checkpoint-jsonl {checkpoint} "
                "--api-key-env MIMO_API_KEY "
                "--base-url https://token-plan-sgp.xiaomimimo.com/v1 "
                "--model mimo-v2.5-pro --temperature 0"
            ),
            (
                "python scripts/sample_category_classification_audit.py "
                f"--workset-jsonl {input_jsonl} "
                f"--classification-jsonl {classify_output} "
                f"--output {sample_audit}"
            ),
            (
                "python scripts/apply_category_migration.py "
                f"--skills-dir {skills_dir} "
                f"--classification-jsonl {classify_output} "
                f"{from_category_flags} --min-confidence 0.9 --movable-only "
                f"--output {apply_plan}"
            ),
            (
                "python scripts/audit_category_residuals.py "
                f"--skills-dir {skills_dir} "
                f"--classification-jsonl {classify_output} "
                f"{from_category_flags} --min-confidence 0.9 "
                f"--output {residual_report}"
            ),
            (
                "python scripts/build_residual_category_worksets.py "
                f"--skills-dir {skills_dir} "
                f"--classification-jsonl {classify_output} "
                f"{from_category_flags} --min-confidence 0.9 "
                f"--output {residual_worksets_report} "
                f"--workset-output-dir {residual_worksets_dir}"
            ),
        ],
        "notes": [
            "This manifest and its input JSONL do not modify archive files.",
            "Each input row carries SKILL.md and metadata SHA-256 provenance.",
            "Run the sample audit before applying any generated move plan.",
            "The apply step refuses inactive categories and changed source hashes.",
            "Residual worksets explain classification gaps, low-confidence rows, target-other rows, and inactive targets before the next batch.",
        ],
    }


def build_batch(
    *,
    skills_dir: Path,
    output_dir: Path,
    batch_id: str,
    from_categories: set[str] | None = None,
    limit: int | None = None,
    offset: int = 0,
    content_chars: int = 1600,
) -> dict[str, Any]:
    from_categories = from_categories or {"other"}
    archive_counts: Counter[str] = Counter()
    selected: list[dict[str, Any]] = []
    matching_total_count = 0
    safe_offset = max(offset, 0)
    max_items = max(limit, 0) if limit is not None else None

    for skill_dir, rel in iter_skill_dirs(skills_dir):
        category = rel.parts[0] if rel.parts else "other"
        archive_counts[category] += 1
        if category not in from_categories:
            continue
        matching_total_count += 1
        if matching_total_count <= safe_offset:
            continue
        if max_items is not None and len(selected) >= max_items:
            continue
        selected.append(
            work_item_for_skill(
                skills_dir=skills_dir,
                skill_dir=skill_dir,
                rel=rel,
                workset="live_current_category",
                reason="live archive skill selected from current category",
                content_chars=content_chars,
            )
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    input_jsonl = output_dir / "input.jsonl"
    with input_jsonl.open("w", encoding="utf-8") as handle:
        for item in selected:
            handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

    manifest = build_manifest(
        batch_id=batch_id,
        skills_dir=skills_dir,
        output_dir=output_dir,
        input_jsonl=input_jsonl,
        from_categories=from_categories,
        limit=limit,
        offset=safe_offset,
        content_chars=content_chars,
        selected=selected,
        matching_total_count=matching_total_count,
        archive_counts=archive_counts,
    )
    manifest_path = output_dir / "manifest.json"
    manifest["manifest_json"] = str(manifest_path)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def print_text_report(manifest: dict[str, Any]) -> None:
    summary = manifest["summary"]
    print("Current category reclassification batch")
    print(f"Batch: {manifest['batch_id']}")
    print(f"Inputs: {summary['selected_input_count']}")
    print(f"Matching current categories: {summary['matching_category_skill_count']}")
    print(f"Input JSONL: {manifest['input_jsonl']}")
    print(f"Manifest: {manifest['manifest_json']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--batch-id", required=True)
    parser.add_argument("--from-category", action="append")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--content-chars", type=int, default=1600)
    parser.add_argument("--json", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {args.skills_dir}")
    manifest = build_batch(
        skills_dir=args.skills_dir,
        output_dir=args.output_dir,
        batch_id=args.batch_id,
        from_categories=parse_csv(args.from_category) or {"other"},
        limit=args.limit,
        offset=args.offset,
        content_chars=args.content_chars,
    )
    if args.json:
        print(json.dumps(manifest, indent=2, ensure_ascii=False))
    else:
        print_text_report(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
