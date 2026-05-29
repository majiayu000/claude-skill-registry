#!/usr/bin/env python3
"""Plan or apply exact duplicate removals for category stable-key conflicts."""

from __future__ import annotations

import argparse
import json
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_category_residuals import file_sha256, metadata_identity
from apply_category_migration import parse_csv
from utils import load_metadata, write_metadata

SCHEMA_VERSION = 1
CONTENT_DRIFT_REFUSE = "refuse"
CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT = "prefer-newer-downloaded-at"
CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET = "prefer-newer-downloaded-at-or-keep-target"


def sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return dict(sorted(counter.items()))


def load_report(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("residual report must be a JSON object")
    details = payload.get("details")
    if not isinstance(details, dict) or not isinstance(
        details.get("stable_key_conflicts"), list
    ):
        raise ValueError(
            "residual report must include details.stable_key_conflicts; "
            "rerun audit_category_residuals.py with --conflict-detail-limit"
        )
    return payload


def source_category(detail: dict[str, Any]) -> str:
    source_path = Path(str(detail.get("source_path") or ""))
    return source_path.parts[0] if source_path.parts else ""


def detail_is_removable(
    detail: dict[str, Any],
    *,
    from_categories: set[str],
    require_metadata_identity: bool,
) -> tuple[bool, str]:
    if from_categories and source_category(detail) not in from_categories:
        return False, "source category excluded by filter"
    if not detail.get("target_exists"):
        return False, "target path missing"
    if not detail.get("skill_content_equal"):
        return False, "SKILL content differs"
    if require_metadata_identity and not detail.get("metadata_identity_equal"):
        return False, "metadata identity differs"
    return True, "exact duplicate"


def parse_downloaded_at(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = value.strip()
    if normalized.endswith("Z"):
        normalized = f"{normalized[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def content_drift_resolution(
    *,
    skills_dir: Path,
    detail: dict[str, Any],
    strategy: str,
) -> tuple[str, str, dict[str, str]]:
    if strategy == CONTENT_DRIFT_REFUSE:
        return "", "SKILL content differs", {}
    if strategy not in {
        CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
        CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET,
    }:
        raise ValueError(f"unsupported content drift strategy: {strategy}")

    source = skills_dir / str(detail.get("source_path") or "")
    target = skills_dir / str(detail.get("target_path") or "")
    source_metadata = load_metadata(source)
    target_metadata = load_metadata(target)
    source_downloaded_at = parse_downloaded_at(source_metadata.get("downloaded_at"))
    target_downloaded_at = parse_downloaded_at(target_metadata.get("downloaded_at"))
    context = {
        "source_downloaded_at": str(source_metadata.get("downloaded_at") or ""),
        "target_downloaded_at": str(target_metadata.get("downloaded_at") or ""),
    }
    if source_downloaded_at is None or target_downloaded_at is None:
        if strategy == CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET:
            return (
                "remove_source_keep_target",
                "target retained because downloaded_at is unavailable",
                context,
            )
        return "", "downloaded_at unavailable for content drift", context
    if source_downloaded_at == target_downloaded_at:
        if strategy == CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET:
            return (
                "remove_source_keep_target",
                "target retained because downloaded_at is tied",
                context,
            )
        return "", "downloaded_at tied for content drift", context
    if source_downloaded_at > target_downloaded_at:
        return (
            "replace_target_remove_source",
            "source downloaded_at is newer than target",
            context,
        )
    return (
        "remove_source_keep_target",
        "target downloaded_at is newer than source",
        context,
    )


def order_and_deduplicate_replacements(removals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for removal in removals:
        grouped.setdefault(str(removal.get("target_path") or ""), []).append(removal)

    ordered: list[dict[str, Any]] = []
    for target_path in sorted(grouped):
        group = grouped[target_path]
        replacements = [
            removal
            for removal in group
            if removal.get("operation") == "replace_target_remove_source"
        ]
        winner: dict[str, Any] | None = None
        if replacements:
            winner = max(
                replacements,
                key=lambda removal: parse_downloaded_at(
                    removal.get("source_downloaded_at")
                )
                or datetime.min.replace(tzinfo=timezone.utc),
            )
            for removal in replacements:
                if removal is winner:
                    continue
                removal["operation"] = "remove_source_keep_target"
                removal["reason"] = "target retained because another source in plan is newer"

        group.sort(
            key=lambda removal: (
                1 if removal.get("operation") == "replace_target_remove_source" else 0,
                str(removal.get("source_path") or ""),
            )
        )
        ordered.extend(group)
    return ordered


def build_cleanup_plan(
    *,
    residual_report: Path,
    skills_dir: Path | None = None,
    from_categories: set[str] | None = None,
    require_metadata_identity: bool = True,
    content_drift_strategy: str = CONTENT_DRIFT_REFUSE,
    limit: int | None = None,
) -> dict[str, Any]:
    report = load_report(residual_report)
    from_categories = from_categories or set()
    details = report["details"]["stable_key_conflicts"]
    selected_skills_dir = skills_dir or Path(str(report.get("skills_dir") or ""))
    max_removals = max(limit, 0) if limit is not None else None

    removals: list[dict[str, Any]] = []
    skipped_reasons: Counter[str] = Counter()
    source_counts: Counter[str] = Counter()
    target_counts: Counter[str] = Counter()
    if max_removals == 0:
        details = []

    for detail in details:
        removable, reason = detail_is_removable(
            detail,
            from_categories=from_categories,
            require_metadata_identity=require_metadata_identity,
        )
        if not removable:
            if (
                reason == "SKILL content differs"
                and detail.get("target_exists")
                and (
                    not require_metadata_identity
                    or bool(detail.get("metadata_identity_equal"))
                )
            ):
                operation, reason, context = content_drift_resolution(
                    skills_dir=selected_skills_dir,
                    detail=detail,
                    strategy=content_drift_strategy,
                )
                if not operation:
                    skipped_reasons[reason] += 1
                    continue
            else:
                skipped_reasons[reason] += 1
                continue
        else:
            operation = "remove_duplicate"
            context = {}
        source = str(detail["source_path"])
        target = str(detail["target_path"])
        removal = {
            "operation": operation,
            "source_path": source,
            "source_skill": str(detail.get("source_skill") or f"{source}/SKILL.md"),
            "target_path": target,
            "target_skill": str(detail.get("target_skill") or f"{target}/SKILL.md"),
            "target_category": str(detail.get("target_category") or ""),
            "target_status": str(detail.get("target_status") or ""),
            "key": str(detail.get("key") or ""),
            "source_skill_sha256": str(detail.get("source_skill_sha256") or ""),
            "target_skill_sha256": str(detail.get("target_skill_sha256") or ""),
            "metadata_identity_equal": bool(detail.get("metadata_identity_equal")),
            "skill_content_equal": bool(detail.get("skill_content_equal")),
            "reason": reason,
        }
        removal.update(context)
        removals.append(removal)
        source_counts[source_category(detail)] += 1
        target_counts[removal["target_category"]] += 1
        if max_removals is not None and len(removals) >= max_removals:
            break

    removals = order_and_deduplicate_replacements(removals)

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(selected_skills_dir),
        "residual_report": str(residual_report),
        "policy": {
            "from_categories": sorted(from_categories),
            "require_metadata_identity": require_metadata_identity,
            "content_drift_strategy": content_drift_strategy,
            "limit": limit,
            "apply_mode": "review-only",
        },
        "summary": {
            "conflict_detail_count": len(report["details"]["stable_key_conflicts"]),
            "planned_remove_count": len(removals),
            "skipped_reasons": sorted_counter(skipped_reasons),
            "source_category_counts": sorted_counter(source_counts),
            "target_category_counts": sorted_counter(target_counts),
        },
        "removals": removals,
        "notes": [
            "Default mode is review-only and does not modify files.",
            "Apply mode re-verifies source and target SKILL hashes before removal.",
            "Metadata identity must match by default; use --allow-metadata-identity-drift only after review.",
            "Content drift is refused by default; prefer-newer-downloaded-at requires both source and target downloaded_at values.",
        ],
    }


def apply_cleanup_plan(skills_dir: Path, plan: dict[str, Any]) -> None:
    require_metadata_identity = bool(plan.get("policy", {}).get("require_metadata_identity", True))
    for removal in plan["removals"]:
        operation = removal.get("operation")
        if operation not in {
            "remove_duplicate",
            "remove_source_keep_target",
            "replace_target_remove_source",
        }:
            raise ValueError(f"unsupported operation: {removal.get('operation')}")
        source = skills_dir / removal["source_path"]
        target = skills_dir / removal["target_path"]
        if source == target:
            raise ValueError(f"source and target are identical: {source}")
        if not source.exists():
            raise FileNotFoundError(f"planned source does not exist: {source}")
        if not target.exists():
            raise FileNotFoundError(f"planned target does not exist: {target}")
        source_hash = file_sha256(source / "SKILL.md")
        target_hash = file_sha256(target / "SKILL.md")
        if source_hash != removal.get("source_skill_sha256"):
            raise ValueError(f"source SKILL hash changed: {source}")
        if target_hash != removal.get("target_skill_sha256"):
            raise ValueError(f"target SKILL hash changed: {target}")
        if operation == "remove_duplicate" and (not source_hash or source_hash != target_hash):
            raise ValueError(f"source and target SKILL content differs: {source}")
        if require_metadata_identity:
            source_identity = metadata_identity(load_metadata(source))
            target_identity = metadata_identity(load_metadata(target))
            if source_identity != target_identity:
                raise ValueError(f"metadata identity changed or differs: {source}")
        if operation == "replace_target_remove_source":
            source_metadata = load_metadata(source)
            source_metadata["category"] = removal["target_category"]
            source_metadata["dir_name"] = target.name
            shutil.copy2(source / "SKILL.md", target / "SKILL.md")
            write_metadata(target, source_metadata)
        shutil.rmtree(source)


def print_text_report(plan: dict[str, Any], *, limit: int) -> None:
    summary = plan["summary"]
    print("Stable-key duplicate cleanup plan")
    print(f"Conflict details: {summary['conflict_detail_count']}")
    print(f"Planned removals: {summary['planned_remove_count']}")
    print(f"Skipped reasons: {summary['skipped_reasons']}")
    print(f"Targets: {summary['target_category_counts']}")
    for removal in plan["removals"][:limit]:
        print(
            f"- remove {removal['source_path']} "
            f"(duplicate of {removal['target_path']})"
        )
    if len(plan["removals"]) > limit:
        print("  ...")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--residual-report", type=Path, required=True)
    parser.add_argument("--skills-dir", type=Path)
    parser.add_argument("--from-category", action="append")
    parser.add_argument("--allow-metadata-identity-drift", action="store_true")
    parser.add_argument(
        "--content-drift-strategy",
        choices=[
            CONTENT_DRIFT_REFUSE,
            CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
            CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET,
        ],
        default=CONTENT_DRIFT_REFUSE,
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-limit", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    plan = build_cleanup_plan(
        residual_report=args.residual_report,
        skills_dir=args.skills_dir,
        from_categories=parse_csv(args.from_category),
        require_metadata_identity=not args.allow_metadata_identity_drift,
        content_drift_strategy=args.content_drift_strategy,
        limit=args.limit,
    )
    skills_dir = Path(plan["skills_dir"])
    if args.apply:
        if not skills_dir.exists():
            raise SystemExit(f"Skills directory not found: {skills_dir}")
        apply_cleanup_plan(skills_dir, plan)
        plan["policy"]["apply_mode"] = "apply"
        plan["applied_at"] = datetime.now(timezone.utc).isoformat()

    payload = json.dumps(plan, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    if args.json:
        print(payload)
    else:
        print_text_report(plan, limit=args.preview_limit)
        if args.apply:
            print("Stable-key duplicate cleanup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
