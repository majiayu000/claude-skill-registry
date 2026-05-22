#!/usr/bin/env python3
"""Build a reviewable category migration plan without changing files."""

from __future__ import annotations

import argparse
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from audit_category_quality import best_suggestion, read_text_prefix
from category_taxonomy import category_slug, get_taxonomy
from utils import extract_frontmatter, load_metadata, normalize_name, skill_semantic_fields

CONFIDENCE_ORDER = {"high": 0, "medium": 1, "low": 2}


def iter_skill_dirs(skills_dir: Path):
    for dirpath, dirnames, filenames in os.walk(skills_dir):
        dirnames[:] = sorted(name for name in dirnames if not name.startswith("."))
        if "SKILL.md" not in filenames:
            continue
        skill_file = Path(dirpath) / "SKILL.md"
        rel = skill_file.relative_to(skills_dir)
        if any(part.startswith(".") for part in rel.parts):
            continue
        yield skill_file.parent, rel


def raw_category_sources(
    rel: Path,
    metadata: dict[str, Any],
    frontmatter: dict[str, Any],
) -> dict[str, str]:
    directory_category = rel.parts[0] if rel.parts else "other"
    sources = {
        "directory": directory_category,
        "metadata": metadata.get("category") if isinstance(metadata.get("category"), str) else "",
        "frontmatter": frontmatter.get("category") if isinstance(frontmatter.get("category"), str) else "",
    }
    return {source: value for source, value in sources.items() if value}


def source_categories(raw_sources: dict[str, str]) -> dict[str, str]:
    taxonomy = get_taxonomy()
    return {
        source: taxonomy.resolve(value, allow_unknown=True)
        for source, value in raw_sources.items()
    }


def confidence_for_suggestion(
    current_category: str,
    suggestion: dict[str, Any],
    *,
    high_score: int,
    high_delta: int,
) -> str:
    score = int(suggestion["score"])
    current_score = int(suggestion["current_score"])
    delta = score - current_score
    if current_category == "other" and score >= high_score:
        return "high"
    if score >= high_score and delta >= high_delta:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def build_change(
    *,
    action: str,
    confidence: str,
    rel: Path,
    skill_dir: Path,
    name: str,
    current_category: str,
    proposed_category: str,
    raw_sources: dict[str, str],
    resolved_sources: dict[str, str],
    reason: str,
    signals: list[str] | None = None,
    score: int | None = None,
    current_score: int | None = None,
) -> dict[str, Any]:
    proposed_name = normalize_name(name or skill_dir.name)
    return {
        "action": action,
        "confidence": confidence,
        "review_required": confidence != "high" or action in {"resolve_source_conflict"},
        "path": str(rel),
        "name": name or skill_dir.name,
        "current_category": current_category,
        "proposed_category": proposed_category,
        "target_path_preview": str(Path(proposed_category) / proposed_name / "SKILL.md"),
        "raw_sources": raw_sources,
        "resolved_sources": resolved_sources,
        "score": score,
        "current_score": current_score,
        "signals": signals or [],
        "reason": reason,
    }


def build_plan(
    skills_dir: Path,
    *,
    include_frontmatter: bool = False,
    content_chars: int = 0,
    min_score: int = 2,
    min_delta: int = 2,
    high_score: int = 4,
    high_delta: int = 3,
    limit: int | None = None,
) -> dict[str, Any]:
    taxonomy = get_taxonomy()
    keyword_map = taxonomy.keyword_map()
    changes: list[dict[str, Any]] = []
    total_skills = 0
    standard_layout_skills = 0

    for skill_dir, rel in iter_skill_dirs(skills_dir):
        total_skills += 1
        if len(rel.parts) == 3:
            standard_layout_skills += 1

        content = read_text_prefix(skill_dir / "SKILL.md", max_chars=max(content_chars, 8192))
        frontmatter = extract_frontmatter(content)
        category_frontmatter = frontmatter if include_frontmatter or content_chars > 0 else {}
        metadata = load_metadata(skill_dir)
        raw_sources = raw_category_sources(rel, metadata, category_frontmatter)
        resolved_sources = source_categories(raw_sources)
        declared_category = (
            raw_sources.get("metadata")
            or raw_sources.get("frontmatter")
            or raw_sources.get("directory")
            or "other"
        )
        current_category = taxonomy.resolve(declared_category, allow_unknown=True)
        semantics = skill_semantic_fields(
            skill_dir,
            metadata=metadata,
            frontmatter=frontmatter,
            rel=rel,
            content=content,
            content_chars=content_chars,
        )
        name = str(semantics["name"])
        text = str(semantics["text"])

        source_values = set(resolved_sources.values())
        alias_sources = [
            source
            for source, value in raw_sources.items()
            if category_slug(value) in taxonomy.aliases
        ]
        if alias_sources:
            changes.append(
                build_change(
                    action="normalize_alias",
                    confidence="high" if len(source_values) == 1 else "medium",
                    rel=rel,
                    skill_dir=skill_dir,
                    name=name,
                    current_category=current_category,
                    proposed_category=current_category,
                    raw_sources=raw_sources,
                    resolved_sources=resolved_sources,
                    reason=f"category source(s) use alias: {', '.join(sorted(alias_sources))}",
                )
            )
            continue

        if len(source_values) > 1:
            changes.append(
                build_change(
                    action="resolve_source_conflict",
                    confidence="low",
                    rel=rel,
                    skill_dir=skill_dir,
                    name=name,
                    current_category=current_category,
                    proposed_category=current_category,
                    raw_sources=raw_sources,
                    resolved_sources=resolved_sources,
                    reason="directory, metadata, or frontmatter categories disagree",
                )
            )
            continue

        migration_target = taxonomy.migration_target(current_category)
        if migration_target:
            definition = taxonomy.categories[current_category]
            changes.append(
                build_change(
                    action="taxonomy_deprecation",
                    confidence="high",
                    rel=rel,
                    skill_dir=skill_dir,
                    name=name,
                    current_category=current_category,
                    proposed_category=migration_target,
                    raw_sources=raw_sources,
                    resolved_sources=resolved_sources,
                    reason=(
                        f"taxonomy marks {current_category} as {definition.status} "
                        f"with migrate_to={migration_target}"
                    ),
                )
            )
            continue

        suggestion = best_suggestion(
            current_category,
            text,
            keyword_map,
            min_score=min_score,
            min_delta=min_delta,
        )
        if suggestion:
            confidence = confidence_for_suggestion(
                current_category,
                suggestion,
                high_score=high_score,
                high_delta=high_delta,
            )
            changes.append(
                build_change(
                    action="heuristic_reclassify",
                    confidence=confidence,
                    rel=rel,
                    skill_dir=skill_dir,
                    name=name,
                    current_category=current_category,
                    proposed_category=str(suggestion["suggested_category"]),
                    raw_sources=raw_sources,
                    resolved_sources=resolved_sources,
                    reason=str(suggestion["reason"]),
                    signals=list(suggestion["signals"]),
                    score=int(suggestion["score"]),
                    current_score=int(suggestion["current_score"]),
                )
            )

    changes.sort(
        key=lambda item: (
            CONFIDENCE_ORDER.get(item["confidence"], 9),
            item["action"],
            item["current_category"],
            item["proposed_category"],
            item["path"],
        )
    )
    action_counts = Counter(change["action"] for change in changes)
    confidence_counts = Counter(change["confidence"] for change in changes)
    category_pairs = Counter(
        (change["current_category"], change["proposed_category"])
        for change in changes
    )
    emitted_changes = changes[: max(limit, 0)] if limit is not None else changes

    return {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(skills_dir),
        "policy": {
            "min_score": min_score,
            "min_delta": min_delta,
            "high_score": high_score,
            "high_delta": high_delta,
            "include_frontmatter": include_frontmatter,
            "content_chars": content_chars,
            "semantic_source_order": ["SKILL.md frontmatter", "metadata.json", "SKILL.md body", "path"],
            "apply_mode": "review-only",
        },
        "summary": {
            "total_skills": total_skills,
            "standard_layout_skill_count": standard_layout_skills,
            "planned_change_count": len(changes),
            "emitted_change_count": len(emitted_changes),
            "action_counts": dict(sorted(action_counts.items())),
            "confidence_counts": dict(sorted(confidence_counts.items())),
            "category_pair_counts": [
                {
                    "current_category": current,
                    "proposed_category": proposed,
                    "count": count,
                }
                for (current, proposed), count in sorted(
                    category_pairs.items(),
                    key=lambda item: (-item[1], item[0][0], item[0][1]),
                )
            ],
        },
        "changes": emitted_changes,
        "notes": [
            "This plan does not modify files.",
            "target_path_preview is not collision-safe; apply tooling must recompute unique paths.",
            "High-confidence heuristic entries are still reviewable, not automatically applied.",
        ],
    }


def print_text_report(plan: dict[str, Any], *, limit: int) -> None:
    summary = plan["summary"]
    print("Category migration plan")
    print(f"Total skills: {summary['total_skills']}")
    print(f"Planned changes: {summary['planned_change_count']}")
    print(f"Actions: {summary['action_counts']}")
    print(f"Confidence: {summary['confidence_counts']}")
    for change in plan["changes"][:limit]:
        print(
            f"- {change['confidence']} {change['action']} "
            f"{change['path']}: {change['current_category']} -> "
            f"{change['proposed_category']} ({change['reason']})"
        )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--include-frontmatter", action="store_true")
    parser.add_argument("--content-chars", type=int, default=0)
    parser.add_argument("--min-score", type=int, default=2)
    parser.add_argument("--min-delta", type=int, default=2)
    parser.add_argument("--high-score", type=int, default=4)
    parser.add_argument("--high-delta", type=int, default=3)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--limit-changes", type=int)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {args.skills_dir}")
    plan = build_plan(
        args.skills_dir,
        include_frontmatter=args.include_frontmatter,
        content_chars=args.content_chars,
        min_score=args.min_score,
        min_delta=args.min_delta,
        high_score=args.high_score,
        high_delta=args.high_delta,
        limit=args.limit_changes,
    )
    payload = json.dumps(plan, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    if args.json:
        print(payload)
    else:
        print_text_report(plan, limit=args.limit)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
