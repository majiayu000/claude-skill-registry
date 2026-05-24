#!/usr/bin/env python3
"""Build residual category cleanup worksets from current archive state."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apply_category_migration import ClassificationRow, load_classification_rows
from audit_category_quality import read_text_prefix
from audit_category_residuals import standard_skill_rel
from category_taxonomy import get_taxonomy
from plan_category_migration import iter_skill_dirs
from utils import extract_frontmatter, load_metadata, skill_semantic_fields

SCHEMA_VERSION = 1


def file_sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_sha256(value: str) -> str:
    if not value:
        return ""
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def work_item_for_skill(
    *,
    skills_dir: Path,
    skill_dir: Path,
    rel: Path,
    workset: str,
    reason: str,
    classification: ClassificationRow | None = None,
    content_chars: int = 1600,
) -> dict[str, Any]:
    content = read_text_prefix(skill_dir / "SKILL.md", max_chars=max(content_chars, 8192))
    source_sha256 = file_sha256(skill_dir / "SKILL.md")
    metadata_sha256 = file_sha256(skill_dir / "metadata.json")
    metadata = load_metadata(skill_dir)
    frontmatter = extract_frontmatter(content)
    semantics = skill_semantic_fields(
        skill_dir,
        metadata=metadata,
        frontmatter=frontmatter,
        rel=rel,
        content=content,
        content_chars=content_chars,
    )
    item: dict[str, Any] = {
        "workset": workset,
        "reason": reason,
        "path": str(rel),
        "skill_dir": str(skill_dir.relative_to(skills_dir)),
        "name": semantics["name"],
        "description": semantics["description"],
        "tags": semantics["tags"],
        "current_category": rel.parts[0] if rel.parts else "other",
        "metadata": {
            "name": metadata.get("name", ""),
            "repo": metadata.get("repo", ""),
            "path": metadata.get("path") or metadata.get("github_path") or "",
            "source_url": metadata.get("source_url", ""),
            "category": metadata.get("category", ""),
        },
        "semantic_sources": semantics["sources"],
        "source_sha256": source_sha256,
        "metadata_sha256": metadata_sha256,
        "semantic_text_sha256": text_sha256(str(semantics.get("text") or "")),
        "content_excerpt": content[:content_chars],
    }
    if classification:
        item["previous_classification"] = {
            "llm_category": classification.target_category,
            "confidence": classification.confidence,
            "status": classification.status,
            "current_category": classification.current_category,
        }
    return item


def existing_scoped_rows(
    *,
    skills_dir: Path,
    rows: list[ClassificationRow],
    from_categories: set[str],
) -> list[tuple[ClassificationRow, Path, Path]]:
    existing: list[tuple[ClassificationRow, Path, Path]] = []
    for row in rows:
        rel = standard_skill_rel(row.path)
        if rel is None:
            continue
        source_dir = skills_dir / rel.parent
        if not source_dir.exists():
            continue
        source_category = rel.parts[0]
        if from_categories and source_category not in from_categories:
            continue
        existing.append((row, rel, source_dir))
    return existing


def load_conflict_details(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    details = payload.get("details", {}).get("stable_key_conflicts", [])
    if not isinstance(details, list):
        raise ValueError("conflict detail report has invalid details.stable_key_conflicts")
    return [detail for detail in details if isinstance(detail, dict)]


def conflict_cluster(detail: dict[str, Any]) -> str:
    content_equal = bool(detail.get("skill_content_equal"))
    metadata_equal = bool(detail.get("metadata_identity_equal"))
    if content_equal and metadata_equal:
        return "exact_duplicate"
    if content_equal:
        return "content_equal_metadata_drift"
    if metadata_equal:
        return "content_drift_metadata_equal"
    return "content_and_metadata_drift"


def build_worksets(
    *,
    skills_dir: Path,
    classification_jsonl: Path,
    from_categories: set[str] | None = None,
    min_confidence: float = 0.9,
    conflict_detail_report: Path | None = None,
    content_chars: int = 1600,
) -> dict[str, Any]:
    taxonomy = get_taxonomy()
    from_categories = from_categories or {"other"}
    rows = load_classification_rows(classification_jsonl)
    existing_rows = existing_scoped_rows(
        skills_dir=skills_dir,
        rows=rows,
        from_categories=from_categories,
    )
    existing_paths = {str(rel) for _row, rel, _source_dir in existing_rows}

    gap_items: list[dict[str, Any]] = []
    archive_counts: Counter[str] = Counter()
    for skill_dir, rel in iter_skill_dirs(skills_dir):
        category = rel.parts[0] if rel.parts else "other"
        archive_counts[category] += 1
        if from_categories and category not in from_categories:
            continue
        if str(rel) not in existing_paths:
            gap_items.append(
                work_item_for_skill(
                    skills_dir=skills_dir,
                    skill_dir=skill_dir,
                    rel=rel,
                    workset="classification_gap",
                    reason="current archive skill has no live classification row",
                    content_chars=content_chars,
                )
            )

    low_confidence_items: list[dict[str, Any]] = []
    review_target_items: list[dict[str, Any]] = []
    target_other_items: list[dict[str, Any]] = []
    for row, rel, source_dir in existing_rows:
        target_status = taxonomy.category_status(row.target_category)
        if row.confidence is None or row.confidence < min_confidence:
            low_confidence_items.append(
                work_item_for_skill(
                    skills_dir=skills_dir,
                    skill_dir=source_dir,
                    rel=rel,
                    workset="low_confidence",
                    reason="previous classification confidence below threshold",
                    classification=row,
                    content_chars=content_chars,
                )
            )
            continue
        if row.target_category == "other":
            target_other_items.append(
                work_item_for_skill(
                    skills_dir=skills_dir,
                    skill_dir=source_dir,
                    rel=rel,
                    workset="target_other",
                    reason="previous classification target remained other",
                    classification=row,
                    content_chars=content_chars,
                )
            )
            continue
        if target_status in {"legacy", "review"}:
            review_target_items.append(
                work_item_for_skill(
                    skills_dir=skills_dir,
                    skill_dir=source_dir,
                    rel=rel,
                    workset="review_target",
                    reason="previous classification target is not a publishable category",
                    classification=row,
                    content_chars=content_chars,
                )
            )

    conflict_details = load_conflict_details(conflict_detail_report)
    conflict_clusters = Counter(conflict_cluster(detail) for detail in conflict_details)
    conflict_target_counts = Counter(
        str(detail.get("target_category") or "") for detail in conflict_details
    )

    worksets = {
        "classification_gap": gap_items,
        "low_confidence": low_confidence_items,
        "review_target": review_target_items,
        "target_other": target_other_items,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(skills_dir),
        "classification_jsonl": str(classification_jsonl),
        "policy": {
            "from_categories": sorted(from_categories),
            "min_confidence": min_confidence,
            "content_chars": content_chars,
            "apply_mode": "report-only",
        },
        "summary": {
            "classification_row_count": len(rows),
            "archive_category_counts": sorted_counter(archive_counts),
            "scoped_existing_classification_count": len(existing_rows),
            "workset_counts": {
                name: len(items) for name, items in sorted(worksets.items())
            },
            "conflict_detail_count": len(conflict_details),
            "conflict_clusters": sorted_counter(conflict_clusters),
            "conflict_target_category_counts": sorted_counter(conflict_target_counts),
        },
        "worksets": worksets,
        "notes": [
            "This report does not modify archive files.",
            "classification_gap contains live archive paths absent from the classification JSONL.",
            "low_confidence and review_target rows should be reclassified before apply.",
            "conflict clusters are diagnostic; content drift conflicts must not be auto-deleted.",
        ],
    }


def write_workset_jsonl(report: dict[str, Any], output_dir: Path) -> dict[str, str]:
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    for name, items in report["worksets"].items():
        path = output_dir / f"{name}.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for item in items:
                handle.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")
        paths[name] = str(path)
    return paths


def print_text_report(report: dict[str, Any], *, limit: int) -> None:
    summary = report["summary"]
    print("Residual category worksets")
    print(f"Classification rows: {summary['classification_row_count']}")
    print(f"Scoped existing classifications: {summary['scoped_existing_classification_count']}")
    print(f"Worksets: {summary['workset_counts']}")
    print(f"Conflict clusters: {summary['conflict_clusters']}")
    for name, items in report["worksets"].items():
        for item in items[: max(limit, 0)]:
            print(f"- {name} {item['path']}")


def parse_csv(values: list[str] | None) -> set[str]:
    if not values:
        return set()
    parsed: set[str] = set()
    for value in values:
        parsed.update(part.strip() for part in value.split(",") if part.strip())
    return parsed


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--classification-jsonl", type=Path, required=True)
    parser.add_argument("--from-category", action="append")
    parser.add_argument("--min-confidence", type=float, default=0.9)
    parser.add_argument("--conflict-detail-report", type=Path)
    parser.add_argument("--content-chars", type=int, default=1600)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--workset-output-dir", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--preview-limit", type=int, default=3)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_worksets(
        skills_dir=args.skills_dir,
        classification_jsonl=args.classification_jsonl,
        from_categories=parse_csv(args.from_category) or {"other"},
        min_confidence=args.min_confidence,
        conflict_detail_report=args.conflict_detail_report,
        content_chars=args.content_chars,
    )
    if args.workset_output_dir:
        report["workset_files"] = write_workset_jsonl(report, args.workset_output_dir)
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
