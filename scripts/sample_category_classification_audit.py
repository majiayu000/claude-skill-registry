#!/usr/bin/env python3
"""Build a deterministic review sample for category classification batches."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apply_category_migration import load_classification_rows, parse_csv

SCHEMA_VERSION = 1


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            payload = json.loads(line)
            if not isinstance(payload, dict):
                raise ValueError(f"JSONL row {line_number} must be an object")
            rows.append(payload)
    return rows


def sample_key(row: dict[str, Any], *, seed: str) -> str:
    payload = "|".join(
        [
            seed,
            str(row.get("path") or ""),
            str(row.get("llm_category") or ""),
            str(row.get("source_sha256") or ""),
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def build_report(
    *,
    workset_jsonl: Path,
    classification_jsonl: Path,
    output_sample_size: int = 50,
    seed: str = "category-audit-v1",
    statuses: set[str] | None = None,
    min_confidence: float | None = None,
) -> dict[str, Any]:
    work_items = load_jsonl(workset_jsonl)
    work_by_path = {str(item.get("path") or ""): item for item in work_items}
    rows = load_classification_rows(classification_jsonl)
    statuses = statuses or {"ok"}
    status_counts = Counter(row.status for row in rows)
    target_counts = Counter(row.target_category for row in rows)
    matched_count = 0
    candidates: list[dict[str, Any]] = []
    missing_input_count = 0

    for row in rows:
        item = work_by_path.get(row.path)
        if item is None:
            missing_input_count += 1
            continue
        matched_count += 1
        if statuses and row.status not in statuses:
            continue
        if min_confidence is not None and (
            row.confidence is None or row.confidence < min_confidence
        ):
            continue
        candidates.append(
            {
                "path": row.path,
                "name": row.name,
                "current_category": row.current_category,
                "llm_category": row.target_category,
                "confidence": row.confidence,
                "status": row.status,
                "reason": getattr(row, "reason", ""),
                "evidence": getattr(row, "evidence", []),
                "workset": getattr(row, "workset", ""),
                "source_sha256": row.source_sha256,
                "metadata_sha256": row.metadata_sha256,
                "semantic_sources": item.get("semantic_sources", {}),
                "description": item.get("description", ""),
                "content_excerpt": item.get("content_excerpt", ""),
            }
        )

    sample_size = max(output_sample_size, 0)
    samples = sorted(candidates, key=lambda item: sample_key(item, seed=seed))[:sample_size]
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "workset_jsonl": str(workset_jsonl),
        "classification_jsonl": str(classification_jsonl),
        "policy": {
            "sample_size": output_sample_size,
            "seed": seed,
            "statuses": sorted(statuses),
            "min_confidence": min_confidence,
        },
        "summary": {
            "workset_row_count": len(work_items),
            "classification_row_count": len(rows),
            "matched_input_count": matched_count,
            "missing_input_count": missing_input_count,
            "candidate_count": len(candidates),
            "sample_count": len(samples),
            "status_counts": dict(sorted(status_counts.items())),
            "target_category_counts": dict(sorted(target_counts.items())),
        },
        "samples": samples,
        "notes": [
            "Review sample rows against SKILL.md excerpts before applying a migration plan.",
            "Sampling is deterministic for a fixed seed and classification input.",
        ],
    }


def print_text_report(report: dict[str, Any], *, limit: int) -> None:
    summary = report["summary"]
    print("Category classification sample audit")
    print(f"Classifications: {summary['classification_row_count']}")
    print(f"Candidates: {summary['candidate_count']}")
    print(f"Samples: {summary['sample_count']}")
    for sample in report["samples"][: max(limit, 0)]:
        print(
            f"- {sample['path']}: {sample['current_category']} -> "
            f"{sample['llm_category']} q={sample['confidence']}"
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workset-jsonl", type=Path, required=True)
    parser.add_argument("--classification-jsonl", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--sample-size", type=int, default=50)
    parser.add_argument("--seed", default="category-audit-v1")
    parser.add_argument("--status", action="append")
    parser.add_argument("--min-confidence", type=float)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--preview-limit", type=int, default=10)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.workset_jsonl.exists():
        raise SystemExit(f"Workset JSONL not found: {args.workset_jsonl}")
    if not args.classification_jsonl.exists():
        raise SystemExit(f"Classification JSONL not found: {args.classification_jsonl}")
    report = build_report(
        workset_jsonl=args.workset_jsonl,
        classification_jsonl=args.classification_jsonl,
        output_sample_size=args.sample_size,
        seed=args.seed,
        statuses=parse_csv(args.status) if args.status else None,
        min_confidence=args.min_confidence,
    )
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    if args.json:
        print(payload)
    else:
        print_text_report(report, limit=args.preview_limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
