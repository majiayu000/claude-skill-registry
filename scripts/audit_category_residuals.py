#!/usr/bin/env python3
"""Explain residual category migration blockers without modifying the archive."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from apply_category_migration import (
    ClassificationRow,
    build_apply_plan,
    category_state,
    load_classification_rows,
    metadata_key,
    parse_csv,
    row_is_eligible,
    select_unique_target,
)
from category_taxonomy import get_taxonomy
from plan_category_migration import iter_skill_dirs
from utils import canonical_metadata_identity, load_metadata, normalize_name, normalize_repo

SCHEMA_VERSION = 1
MOVABLE_REASON = "movable candidate under selected policy"
CONFLICT_METADATA_IDENTITY_FIELDS = (
    "name",
    "repo",
    "path",
    "github_path",
    "github_branch",
    "branch",
    "source_url",
    "license",
    "author",
)


def count_archive_categories(skills_dir: Path) -> Counter[str]:
    counts: Counter[str] = Counter()
    for _skill_dir, rel in iter_skill_dirs(skills_dir):
        category = rel.parts[0] if rel.parts else "other"
        counts[category] += 1
    return counts


def standard_skill_rel(path: str) -> Path | None:
    rel = Path(path)
    if len(rel.parts) != 3 or rel.name != "SKILL.md":
        return None
    return rel


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def sorted_largest(counter: Counter[str], *, limit: int) -> list[dict[str, Any]]:
    return [
        {"value": value, "count": count}
        for value, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))[
            : max(limit, 0)
        ]
    ]


def row_example(
    row: ClassificationRow,
    *,
    source_exists: bool,
    source_category: str,
    reason: str,
    target_status: str,
    target_path: str = "",
) -> dict[str, Any]:
    example = {
        "path": row.path,
        "name": row.name,
        "source_exists": source_exists,
        "source_category": source_category,
        "classification_current_category": row.current_category,
        "target_category": row.target_category,
        "target_status": target_status,
        "confidence": row.confidence,
        "status": row.status,
        "reason": reason,
    }
    if target_path:
        example["target_path"] = target_path
    return example


def add_bucket_example(
    examples: dict[str, list[dict[str, Any]]],
    reason: str,
    example: dict[str, Any],
    *,
    limit: int,
) -> None:
    bucket = examples[reason]
    if len(bucket) < limit:
        bucket.append(example)


def file_sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metadata_identity(metadata: dict[str, Any]) -> dict[str, Any]:
    return canonical_metadata_identity(metadata, CONFLICT_METADATA_IDENTITY_FIELDS)


def stable_key_conflict_detail(
    *,
    skills_dir: Path,
    row: ClassificationRow,
    source_dir: Path,
    target_dir_rel: Path,
    target_category: str,
    target_status: str,
    key: str,
) -> dict[str, Any]:
    target_dir = skills_dir / target_dir_rel
    source_metadata = load_metadata(source_dir)
    target_metadata = load_metadata(target_dir) if target_dir.exists() else {}
    source_identity = metadata_identity(source_metadata)
    target_identity = metadata_identity(target_metadata)
    source_skill_hash = file_sha256(source_dir / "SKILL.md")
    target_skill_hash = file_sha256(target_dir / "SKILL.md")
    return {
        "source_path": str(source_dir.relative_to(skills_dir)),
        "source_skill": str(source_dir.relative_to(skills_dir) / "SKILL.md"),
        "target_path": str(target_dir_rel),
        "target_skill": str(target_dir_rel / "SKILL.md"),
        "target_exists": target_dir.exists(),
        "target_category": target_category,
        "target_status": target_status,
        "classification_name": row.name,
        "confidence": row.confidence,
        "key": key,
        "source_metadata_identity": source_identity,
        "target_metadata_identity": target_identity,
        "metadata_identity_equal": source_identity == target_identity,
        "source_skill_sha256": source_skill_hash,
        "target_skill_sha256": target_skill_hash,
        "skill_content_equal": bool(source_skill_hash and source_skill_hash == target_skill_hash),
    }


def blocker_reasons(
    row: ClassificationRow,
    *,
    min_confidence: float,
    from_categories: set[str],
    to_categories: set[str],
    target_statuses: set[str],
    allow_target_other: bool,
) -> list[str]:
    taxonomy = get_taxonomy()
    reasons: list[str] = []
    if row.status != "ok":
        reasons.append("classification status is not ok")
    if not row.path or not row.path.endswith("/SKILL.md"):
        reasons.append("classification path is not a SKILL.md path")
    if row.confidence is None or row.confidence < min_confidence:
        reasons.append("confidence below threshold")
    if from_categories and row.current_category not in from_categories:
        reasons.append("classification current category excluded by filter")
    if to_categories and row.target_category not in to_categories:
        reasons.append("target category excluded by filter")
    if row.current_category == row.target_category:
        reasons.append("classification target matches current category")
    if row.target_category == "other" and not allow_target_other:
        reasons.append("target category other requires --allow-target-other")
    target_status = taxonomy.category_status(row.target_category)
    if "any" not in target_statuses and target_status not in target_statuses:
        reasons.append(f"target category status {target_status!r} excluded by filter")
    return reasons


def build_report(
    *,
    skills_dir: Path,
    classification_jsonl: Path,
    min_confidence: float = 0.9,
    from_categories: set[str] | None = None,
    to_categories: set[str] | None = None,
    target_statuses: set[str] | None = None,
    allow_target_other: bool = False,
    limit_examples: int = 20,
    top_targets: int = 20,
    conflict_detail_limit: int = 0,
) -> dict[str, Any]:
    taxonomy = get_taxonomy()
    from_categories = from_categories or set()
    to_categories = to_categories or set()
    target_statuses = target_statuses or {"active"}
    rows = load_classification_rows(classification_jsonl)
    archive_counts = count_archive_categories(skills_dir)
    state = category_state(skills_dir)
    same_policy_plan = build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification_jsonl,
        min_confidence=min_confidence,
        from_categories=from_categories,
        to_categories=to_categories,
        target_statuses=target_statuses,
        allow_target_other=allow_target_other,
    )

    classification_status_counts = Counter(row.status for row in rows)
    target_category_counts = Counter(row.target_category for row in rows)
    target_status_counts: Counter[str] = Counter()
    source_state_counts: Counter[str] = Counter()
    existing_source_category_counts: Counter[str] = Counter()
    scoped_source_category_counts: Counter[str] = Counter()
    primary_reason_counts: Counter[str] = Counter()
    all_blocker_reason_counts: Counter[str] = Counter()
    reason_target_counts: dict[str, Counter[str]] = defaultdict(Counter)
    reason_target_status_counts: dict[str, Counter[str]] = defaultdict(Counter)
    examples: dict[str, list[dict[str, Any]]] = defaultdict(list)
    conflict_details: list[dict[str, Any]] = []
    conflict_detail_summary: Counter[str] = Counter()

    candidate_move_count = 0
    blocked_existing_key_count = 0
    scoped_existing_source_count = 0

    for row in rows:
        target_status = taxonomy.category_status(row.target_category)
        target_status_counts[target_status] += 1
        rel = standard_skill_rel(row.path)
        if rel is None:
            source_state_counts["non_standard_path"] += 1
            reason = "source path is not standard <category>/<skill>/SKILL.md"
            primary_reason_counts[reason] += 1
            reason_target_counts[reason][row.target_category] += 1
            reason_target_status_counts[reason][target_status] += 1
            add_bucket_example(
                examples,
                reason,
                row_example(
                    row,
                    source_exists=False,
                    source_category="",
                    reason=reason,
                    target_status=target_status,
                ),
                limit=limit_examples,
            )
            continue

        source_dir = skills_dir / rel.parent
        source_category = rel.parts[0]
        if not source_dir.exists():
            source_state_counts["missing"] += 1
            reason = "source directory missing"
            primary_reason_counts[reason] += 1
            reason_target_counts[reason][row.target_category] += 1
            reason_target_status_counts[reason][target_status] += 1
            add_bucket_example(
                examples,
                reason,
                row_example(
                    row,
                    source_exists=False,
                    source_category=source_category,
                    reason=reason,
                    target_status=target_status,
                ),
                limit=limit_examples,
            )
            continue

        source_state_counts["exists"] += 1
        existing_source_category_counts[source_category] += 1
        if from_categories and source_category not in from_categories:
            reason = "current archive category excluded by filter"
            primary_reason_counts[reason] += 1
            reason_target_counts[reason][row.target_category] += 1
            reason_target_status_counts[reason][target_status] += 1
            add_bucket_example(
                examples,
                reason,
                row_example(
                    row,
                    source_exists=True,
                    source_category=source_category,
                    reason=reason,
                    target_status=target_status,
                ),
                limit=limit_examples,
            )
            continue

        scoped_existing_source_count += 1
        scoped_source_category_counts[source_category] += 1
        reasons = blocker_reasons(
            row,
            min_confidence=min_confidence,
            from_categories=from_categories,
            to_categories=to_categories,
            target_statuses=target_statuses,
            allow_target_other=allow_target_other,
        )
        for blocker in reasons:
            all_blocker_reason_counts[blocker] += 1
        eligible, reason = row_is_eligible(
            row,
            min_confidence=min_confidence,
            from_categories=from_categories,
            to_categories=to_categories,
            target_statuses=target_statuses,
            allow_target_other=allow_target_other,
        )
        target_path = ""
        if eligible:
            target_category = taxonomy.resolve(row.target_category, allow_unknown=True)
            metadata = load_metadata(source_dir)
            repo = normalize_repo(metadata.get("repo", ""))
            name = row.name or metadata.get("name") or source_dir.name
            key = metadata_key(source_dir, category=target_category, name=normalize_name(name))
            operation, target_dir_rel, operation_reason = select_unique_target(
                state=state,
                source_dir_rel=rel.parent,
                target_category=target_category,
                base_name=source_dir.name,
                key=key,
                repo=repo,
            )
            target_path = str(target_dir_rel / "SKILL.md")
            if operation == "move":
                reason = MOVABLE_REASON
                candidate_move_count += 1
            else:
                reason = operation_reason
                if operation == "blocked_existing_key":
                    blocked_existing_key_count += 1
                    if len(conflict_details) < max(conflict_detail_limit, 0):
                        detail = stable_key_conflict_detail(
                            skills_dir=skills_dir,
                            row=row,
                            source_dir=source_dir,
                            target_dir_rel=target_dir_rel,
                            target_category=target_category,
                            target_status=target_status,
                            key=key,
                        )
                        conflict_details.append(detail)
                        if detail["skill_content_equal"]:
                            conflict_detail_summary["skill_content_equal"] += 1
                        if detail["metadata_identity_equal"]:
                            conflict_detail_summary["metadata_identity_equal"] += 1
                        if not detail["target_exists"]:
                            conflict_detail_summary["target_missing"] += 1
                all_blocker_reason_counts[reason] += 1

        primary_reason_counts[reason] += 1
        reason_target_counts[reason][row.target_category] += 1
        reason_target_status_counts[reason][target_status] += 1
        add_bucket_example(
            examples,
            reason,
            row_example(
                row,
                source_exists=True,
                source_category=source_category,
                reason=reason,
                target_status=target_status,
                target_path=target_path,
            ),
            limit=limit_examples,
        )

    scoped_archive_skill_count = (
        sum(archive_counts[category] for category in from_categories)
        if from_categories
        else sum(archive_counts.values())
    )
    scoped_archive_classification_gap = (
        scoped_archive_skill_count - scoped_existing_source_count
    )
    buckets = [
        {
            "reason": reason,
            "count": count,
            "target_categories": sorted_largest(
                reason_target_counts[reason],
                limit=top_targets,
            ),
            "target_status_counts": sorted_counter(reason_target_status_counts[reason]),
            "examples": examples.get(reason, []),
        }
        for reason, count in sorted(
            primary_reason_counts.items(),
            key=lambda item: (-item[1], item[0]),
        )
    ]

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(skills_dir),
        "classification_jsonl": str(classification_jsonl),
        "policy": {
            "min_confidence": min_confidence,
            "from_categories": sorted(from_categories),
            "to_categories": sorted(to_categories),
            "target_statuses": sorted(target_statuses),
            "allow_target_other": allow_target_other,
            "apply_mode": "report-only",
            "example_limit_per_reason": limit_examples,
            "top_targets_per_reason": top_targets,
            "conflict_detail_limit": conflict_detail_limit,
        },
        "summary": {
            "classification_row_count": len(rows),
            "archive_skill_count": sum(archive_counts.values()),
            "scoped_archive_skill_count": scoped_archive_skill_count,
            "scoped_archive_classification_gap": scoped_archive_classification_gap,
            "classification_status_counts": sorted_counter(classification_status_counts),
            "archive_category_counts": sorted_counter(archive_counts),
            "source_state_counts": sorted_counter(source_state_counts),
            "existing_source_category_counts": sorted_counter(existing_source_category_counts),
            "scoped_source_category_counts": sorted_counter(scoped_source_category_counts),
            "scoped_existing_source_count": scoped_existing_source_count,
            "candidate_move_count": candidate_move_count,
            "blocked_existing_key_count": blocked_existing_key_count,
            "stable_key_conflict_detail_count": len(conflict_details),
            "stable_key_conflict_detail_summary": sorted_counter(conflict_detail_summary),
            "primary_reason_counts": sorted_counter(primary_reason_counts),
            "all_blocker_reason_counts": sorted_counter(all_blocker_reason_counts),
            "target_category_counts": sorted_counter(target_category_counts),
            "target_status_counts": sorted_counter(target_status_counts),
            "same_policy_plan_summary": same_policy_plan["summary"],
        },
        "buckets": buckets,
        "details": {
            "stable_key_conflicts": conflict_details,
        },
        "notes": [
            "This report is read-only and never moves, deletes, or rewrites skills.",
            "same_policy_plan_summary is generated by apply_category_migration.py with the same flags.",
            "primary_reason_counts are mutually exclusive and explain the current archive state first.",
            "all_blocker_reason_counts can exceed scoped_existing_source_count because one row may have multiple blockers.",
            "source directory missing usually means the classification row points at a pre-migration path that has already moved.",
            "scoped_archive_classification_gap is scoped_archive_skill_count minus "
            "scoped_existing_source_count; positive values indicate archive skills "
            "not covered by the classification file or duplicate classification coverage.",
            "stable_key_conflicts detail is bounded by --conflict-detail-limit and includes "
            "content hashes so duplicate removal is not inferred from the stable key alone.",
        ],
    }


def print_text_report(report: dict[str, Any], *, limit: int) -> None:
    summary = report["summary"]
    print("Category residual audit")
    print(f"Classification rows: {summary['classification_row_count']}")
    print(f"Archive skills: {summary['archive_skill_count']}")
    print(f"Scoped archive skills: {summary['scoped_archive_skill_count']}")
    print(f"Scoped existing classified sources: {summary['scoped_existing_source_count']}")
    print(f"Scoped archive/classification gap: {summary['scoped_archive_classification_gap']}")
    print(f"Candidate moves: {summary['candidate_move_count']}")
    print(f"Primary reasons: {summary['primary_reason_counts']}")
    for bucket in report["buckets"][: max(limit, 0)]:
        print(f"- {bucket['count']} {bucket['reason']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--classification-jsonl", type=Path, required=True)
    parser.add_argument("--min-confidence", type=float, default=0.9)
    parser.add_argument("--from-category", action="append")
    parser.add_argument("--to-category", action="append")
    parser.add_argument(
        "--target-status",
        action="append",
        choices=["active", "legacy", "review", "deprecated", "unknown", "any"],
        default=["active"],
    )
    parser.add_argument("--allow-target-other", action="store_true")
    parser.add_argument("--limit-examples", type=int, default=20)
    parser.add_argument("--top-targets", type=int, default=20)
    parser.add_argument(
        "--conflict-detail-limit",
        type=int,
        default=0,
        help="Emit up to N stable-key conflict details with source/target hashes",
    )
    parser.add_argument("--preview-limit", type=int, default=20)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {args.skills_dir}")
    if not args.classification_jsonl.exists():
        raise SystemExit(f"Classification JSONL not found: {args.classification_jsonl}")
    report = build_report(
        skills_dir=args.skills_dir,
        classification_jsonl=args.classification_jsonl,
        min_confidence=args.min_confidence,
        from_categories=parse_csv(args.from_category),
        to_categories=parse_csv(args.to_category),
        target_statuses=set(args.target_status),
        allow_target_other=args.allow_target_other,
        limit_examples=args.limit_examples,
        top_targets=args.top_targets,
        conflict_detail_limit=args.conflict_detail_limit,
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
