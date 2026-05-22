#!/usr/bin/env python3
"""Plan or apply audited category moves from classification results."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from category_taxonomy import get_taxonomy
from plan_category_migration import iter_skill_dirs
from utils import (
    build_skill_key,
    get_repo_suffix,
    load_metadata,
    normalize_name,
    normalize_repo,
    short_hash,
    write_metadata,
)

SCHEMA_VERSION = 1


@dataclass(frozen=True)
class ClassificationRow:
    path: str
    name: str
    current_category: str
    target_category: str
    confidence: float | None
    status: str


def load_classification_rows(path: Path) -> list[ClassificationRow]:
    rows: list[ClassificationRow] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"invalid JSONL row {line_number}: {exc}") from exc
            if not isinstance(payload, dict):
                raise ValueError(f"classification row {line_number} must be an object")
            rows.append(
                ClassificationRow(
                    path=str(payload.get("path") or ""),
                    name=str(payload.get("name") or ""),
                    current_category=str(payload.get("current_category") or ""),
                    target_category=str(payload.get("llm_category") or ""),
                    confidence=parse_confidence(payload.get("confidence")),
                    status=str(payload.get("status") or ""),
                )
            )
    return rows


def metadata_key(skill_dir: Path, *, category: str, name: str) -> str:
    meta = load_metadata(skill_dir)
    repo = normalize_repo(meta.get("repo", ""))
    path = meta.get("github_path") or meta.get("path") or ""
    return build_skill_key(repo, path, name=name, category=category)


def parse_confidence(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return float(value)


def category_state(skills_dir: Path) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = defaultdict(lambda: {"names": set(), "key_to_dir": {}})
    for skill_dir, rel in iter_skill_dirs(skills_dir):
        category = rel.parts[0]
        name = normalize_name(load_metadata(skill_dir).get("name") or skill_dir.name)
        key = metadata_key(skill_dir, category=category, name=name)
        state[category]["names"].add(skill_dir.name.lower())
        if key:
            state[category]["key_to_dir"].setdefault(key, Path(category) / skill_dir.name)
    return state


def select_unique_target(
    *,
    state: dict[str, dict[str, Any]],
    source_dir_rel: Path,
    target_category: str,
    base_name: str,
    key: str,
    repo: str,
) -> tuple[str, Path, str]:
    target_state = state[target_category]
    key_to_dir: dict[str, Path] = target_state["key_to_dir"]
    if key and key in key_to_dir and key_to_dir[key] != source_dir_rel:
        return (
            "blocked_existing_key",
            key_to_dir[key],
            "target category already contains a skill with the same stable key",
        )

    existing_names: set[str] = target_state["names"]
    base = normalize_name(base_name)
    if base.lower() not in existing_names:
        selected = Path(target_category) / base
    else:
        suffix = get_repo_suffix(repo)
        if suffix and not base.endswith(f"-{suffix}"):
            candidate_base = f"{base}-{suffix}"
        elif suffix:
            candidate_base = base
        else:
            candidate_base = f"{base}-{short_hash(key or str(source_dir_rel))}"
        candidate = candidate_base
        counter = 2
        while candidate.lower() in existing_names:
            candidate = f"{candidate_base}-{counter}"
            counter += 1
        selected = Path(target_category) / candidate

    existing_names.add(selected.name.lower())
    if key:
        key_to_dir.setdefault(key, selected)
    return ("move", selected, "classification target passed filters")


def row_is_eligible(
    row: ClassificationRow,
    *,
    min_confidence: float,
    from_categories: set[str],
    to_categories: set[str],
    target_statuses: set[str],
    allow_target_other: bool,
) -> tuple[bool, str]:
    if row.status != "ok":
        return False, "classification status is not ok"
    if not row.path or not row.path.endswith("/SKILL.md"):
        return False, "classification path is not a SKILL.md path"
    if row.confidence is None or row.confidence < min_confidence:
        return False, "confidence below threshold"
    if from_categories and row.current_category not in from_categories:
        return False, "current category excluded by filter"
    if to_categories and row.target_category not in to_categories:
        return False, "target category excluded by filter"
    if row.current_category == row.target_category:
        return False, "classification target matches current category"
    if row.target_category == "other" and not allow_target_other:
        return False, "target category other requires --allow-target-other"
    taxonomy = get_taxonomy()
    target_definition = taxonomy.categories.get(row.target_category)
    target_status = target_definition.status if target_definition else "unknown"
    if "any" not in target_statuses and target_status not in target_statuses:
        return False, f"target category status {target_status!r} excluded by filter"
    return True, "eligible"


def build_apply_plan(
    *,
    skills_dir: Path,
    classification_jsonl: Path,
    min_confidence: float = 0.9,
    from_categories: set[str] | None = None,
    to_categories: set[str] | None = None,
    target_statuses: set[str] | None = None,
    allow_target_other: bool = False,
    movable_only: bool = False,
    limit: int | None = None,
) -> dict[str, Any]:
    taxonomy = get_taxonomy()
    rows = load_classification_rows(classification_jsonl)
    from_categories = from_categories or set()
    to_categories = to_categories or set()
    target_statuses = target_statuses or {"active"}
    state = category_state(skills_dir)

    moves: list[dict[str, Any]] = []
    reject_reasons = Counter()
    row_status_counts = Counter(row.status for row in rows)
    target_counts = Counter()
    source_counts = Counter()
    max_moves = max(limit, 0) if limit is not None else None
    if max_moves == 0:
        rows = []

    for row in rows:
        eligible, reason = row_is_eligible(
            row,
            min_confidence=min_confidence,
            from_categories=from_categories,
            to_categories=to_categories,
            target_statuses=target_statuses,
            allow_target_other=allow_target_other,
        )
        if not eligible:
            reject_reasons[reason] += 1
            continue

        source_skill_rel = Path(row.path)
        if len(source_skill_rel.parts) != 3:
            reject_reasons["source path is not standard <category>/<skill>/SKILL.md"] += 1
            continue
        source_dir_rel = source_skill_rel.parent
        source_dir = skills_dir / source_dir_rel
        if not source_dir.exists():
            reject_reasons["source directory missing"] += 1
            continue
        source_category = source_skill_rel.parts[0]
        target_category = taxonomy.resolve(row.target_category, allow_unknown=True)
        meta = load_metadata(source_dir)
        repo = normalize_repo(meta.get("repo", ""))
        base_name = source_dir.name
        name = row.name or meta.get("name") or source_dir.name
        key = metadata_key(source_dir, category=target_category, name=normalize_name(name))
        operation, target_dir_rel, operation_reason = select_unique_target(
            state=state,
            source_dir_rel=source_dir_rel,
            target_category=target_category,
            base_name=base_name,
            key=key,
            repo=repo,
        )
        if movable_only and operation != "move":
            reject_reasons[operation_reason] += 1
            continue
        move = {
            "operation": operation,
            "source_path": str(source_dir_rel),
            "source_skill": str(source_skill_rel),
            "source_category": source_category,
            "current_category": row.current_category,
            "target_category": target_category,
            "target_status": taxonomy.categories[target_category].status
            if target_category in taxonomy.categories
            else "unknown",
            "target_path": str(target_dir_rel),
            "target_skill": str(target_dir_rel / "SKILL.md"),
            "name": name,
            "confidence": row.confidence,
            "key": key,
            "repo": repo,
            "reason": operation_reason,
        }
        moves.append(move)
        target_counts[target_category] += 1
        source_counts[source_category] += 1
        if max_moves is not None and len(moves) >= max_moves:
            break

    operation_counts = Counter(move["operation"] for move in moves)
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
            "movable_only": movable_only,
            "limit": limit,
            "apply_mode": "review-only",
        },
        "summary": {
            "classification_row_count": len(rows),
            "classification_status_counts": dict(sorted(row_status_counts.items())),
            "planned_move_count": len(moves),
            "movable_count": operation_counts.get("move", 0),
            "blocked_count": len(moves) - operation_counts.get("move", 0),
            "operation_counts": dict(sorted(operation_counts.items())),
            "reject_reasons": dict(sorted(reject_reasons.items())),
            "source_category_counts": dict(sorted(source_counts.items())),
            "target_category_counts": dict(sorted(target_counts.items())),
        },
        "moves": moves,
        "notes": [
            "Default mode is review-only and does not modify files.",
            "Only --apply moves directories and updates metadata.json.",
            "Blocked moves are never applied automatically.",
        ],
    }


def apply_plan(skills_dir: Path, plan: dict[str, Any]) -> None:
    blocked = [move for move in plan["moves"] if move["operation"] != "move"]
    if blocked:
        raise ValueError(f"plan contains {len(blocked)} blocked move(s)")
    for move in plan["moves"]:
        source = skills_dir / move["source_path"]
        target = skills_dir / move["target_path"]
        if not source.exists():
            raise FileNotFoundError(f"planned source does not exist: {source}")
        if target.exists():
            raise FileExistsError(f"planned target already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        meta = load_metadata(target)
        meta.setdefault("name", move["name"])
        meta["category"] = move["target_category"]
        meta["dir_name"] = target.name
        write_metadata(target, meta)


def print_text_report(plan: dict[str, Any], *, limit: int) -> None:
    summary = plan["summary"]
    print("Category apply plan")
    print(f"Classification rows: {summary['classification_row_count']}")
    print(f"Planned moves: {summary['planned_move_count']}")
    print(f"Operations: {summary['operation_counts']}")
    print(f"Targets: {summary['target_category_counts']}")
    for move in plan["moves"][:limit]:
        print(
            f"- {move['operation']} {move['source_skill']} -> "
            f"{move['target_skill']} q={move['confidence']}"
        )
    if len(plan["moves"]) > limit:
        print("  ...")


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
    parser.add_argument("--min-confidence", type=float, default=0.9)
    parser.add_argument("--from-category", action="append")
    parser.add_argument("--to-category", action="append")
    parser.add_argument(
        "--target-status",
        action="append",
        choices=["active", "review", "deprecated", "unknown", "any"],
        default=["active"],
    )
    parser.add_argument("--allow-target-other", action="store_true")
    parser.add_argument("--movable-only", action="store_true")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--preview-limit", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {args.skills_dir}")
    if not args.classification_jsonl.exists():
        raise SystemExit(f"Classification JSONL not found: {args.classification_jsonl}")
    plan = build_apply_plan(
        skills_dir=args.skills_dir,
        classification_jsonl=args.classification_jsonl,
        min_confidence=args.min_confidence,
        from_categories=parse_csv(args.from_category),
        to_categories=parse_csv(args.to_category),
        target_statuses=set(args.target_status),
        allow_target_other=args.allow_target_other,
        movable_only=args.movable_only,
        limit=args.limit,
    )
    if args.apply:
        apply_plan(args.skills_dir, plan)
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
            print("Category migration apply complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
