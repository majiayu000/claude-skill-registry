#!/usr/bin/env python3
"""Audit category quality across a skill archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from category_taxonomy import (
    UnknownCategoryError,
    category_aliases,
    category_keywords,
    category_slug,
    get_taxonomy,
    resolve_category,
)
from utils import extract_frontmatter, load_metadata, skill_semantic_fields


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


def normalized_haystack(text: str) -> str:
    return f" {category_slug(text).replace('-', ' ')} "


def keyword_hits(haystack: str, keywords: list[str]) -> list[str]:
    hits: list[str] = []
    for keyword in keywords:
        needle = f" {category_slug(keyword).replace('-', ' ')} "
        if needle in haystack:
            hits.append(keyword)
    return hits


def score_categories(text: str, keyword_map: dict[str, list[str]]) -> dict[str, list[str]]:
    scores: dict[str, list[str]] = {}
    haystack = normalized_haystack(text)
    for category, keywords in keyword_map.items():
        hits = keyword_hits(haystack, keywords)
        if hits:
            scores[category] = hits
    return scores


def read_text_prefix(path: Path, max_chars: int = 8192) -> str:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        return handle.read(max_chars)


def best_suggestion(
    current_category: str,
    text: str,
    keyword_map: dict[str, list[str]],
    *,
    min_score: int,
    min_delta: int,
) -> dict[str, Any] | None:
    scores = score_categories(text, keyword_map)
    if not scores:
        return None

    ranked = sorted(scores.items(), key=lambda item: (-len(item[1]), item[0]))
    suggested_category, hits = ranked[0]
    current_score = len(scores.get(current_category, []))
    suggested_score = len(hits)
    if suggested_category == current_category:
        return None
    if suggested_score < min_score:
        return None
    if current_category != "other" and suggested_score - current_score < min_delta:
        return None

    reason = f"matched {suggested_score} {suggested_category} keyword(s)"
    if current_score:
        reason += f" versus {current_score} current-category keyword(s)"

    return {
        "suggested_category": suggested_category,
        "score": suggested_score,
        "current_score": current_score,
        "signals": hits,
        "reason": reason,
    }


def compact_examples(items: list[dict[str, Any]], limit: int) -> list[dict[str, Any]]:
    return items[: max(limit, 0)]


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_digest(value: Any) -> str:
    payload = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _sample_identity(seed: str, category: str, rel: Path) -> str:
    return hashlib.sha256(f"{seed}|{category}|{rel.as_posix()}".encode()).hexdigest()


def build_stratified_sample(
    skills_dir: Path,
    *,
    content_chars: int = 2048,
    taxonomy: Any | None = None,
) -> dict[str, Any]:
    taxonomy = taxonomy or get_taxonomy()
    policy = taxonomy.audit_sampling
    eligible = set(policy.categories)
    candidates: dict[str, list[dict[str, Any]]] = {
        category: [] for category in policy.categories
    }
    errors: list[str] = []

    for skill_dir, rel in iter_skill_dirs(skills_dir):
        metadata = load_metadata(skill_dir)
        declared = (
            metadata.get("category")
            if isinstance(metadata.get("category"), str)
            else rel.parts[0] if rel.parts else taxonomy.default_category
        )
        current_category = resolve_category(declared, allow_unknown=True)
        if current_category not in eligible:
            continue
        candidates[current_category].append(
            {
                "skill_dir": skill_dir,
                "rel": rel,
                "sample_key": _sample_identity(
                    policy.seed,
                    current_category,
                    rel,
                ),
            }
        )

    strata: list[dict[str, Any]] = []
    digest_inputs: list[dict[str, str]] = []
    for category in policy.categories:
        population = sorted(
            candidates[category],
            key=lambda item: (item["sample_key"], item["rel"].as_posix()),
        )
        if len(population) < policy.per_category:
            errors.append(
                f"{category}: population {len(population)} is below quota "
                f"{policy.per_category}"
            )

        samples: list[dict[str, Any]] = []
        for candidate in population[: policy.per_category]:
            skill_dir = candidate["skill_dir"]
            rel = candidate["rel"]
            skill_path = skill_dir / "SKILL.md"
            metadata_path = skill_dir / "metadata.json"
            if not metadata_path.is_file():
                errors.append(f"{rel.as_posix()}: metadata.json is missing")
                continue

            content = read_text_prefix(skill_path, max_chars=max(content_chars, 8192))
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
            excerpt = " ".join(content[:content_chars].split())
            samples.append(
                {
                    "path": rel.as_posix(),
                    "name": semantics["name"],
                    "current_category": category,
                    "description": semantics["description"],
                    "content_excerpt": excerpt,
                    "semantic_sources": semantics["sources"],
                    "source_sha256": file_sha256(skill_path),
                    "metadata_sha256": file_sha256(metadata_path),
                    "sample_key": candidate["sample_key"],
                }
            )

        stratum_digest = canonical_digest(samples)
        digest_inputs.append({"category": category, "digest": stratum_digest})
        strata.append(
            {
                "category": category,
                "population_count": len(population),
                "sample_count": len(samples),
                "quota": policy.per_category,
                "digest": stratum_digest,
                "samples": samples,
            }
        )

    overall_digest = canonical_digest(digest_inputs)
    return {
        "schema_version": policy.schema_version,
        "status": "failed" if errors else "complete",
        "skills_dir": str(skills_dir),
        "policy": {
            "seed": policy.seed,
            "per_category": policy.per_category,
            "categories": list(policy.categories),
            "content_chars": content_chars,
        },
        "sample_count": sum(stratum["sample_count"] for stratum in strata),
        "digest": overall_digest,
        "strata": strata,
        "errors": errors,
    }


def build_report(
    skills_dir: Path,
    *,
    include_frontmatter: bool = False,
    content_chars: int = 0,
    min_score: int = 2,
    min_delta: int = 2,
    small_category_threshold: int = 10,
    limit_candidates: int = 100,
    limit_examples: int = 20,
) -> dict[str, Any]:
    aliases = category_aliases()
    keyword_map = category_keywords()
    category_counts: Counter[str] = Counter()
    unknown_counts: Counter[str] = Counter()
    alias_usages: list[dict[str, Any]] = []
    category_conflicts: list[dict[str, Any]] = []
    layout_issues: list[dict[str, Any]] = []
    candidates: list[dict[str, Any]] = []
    total_skills = 0
    standard_layout_skills = 0

    for skill_dir, rel in iter_skill_dirs(skills_dir):
        total_skills += 1
        if len(rel.parts) == 3:
            standard_layout_skills += 1
        else:
            layout_issues.append(
                {
                    "path": str(rel),
                    "expected": "<category>/<skill>/SKILL.md",
                    "depth": len(rel.parts),
                }
            )
        content = read_text_prefix(skill_dir / "SKILL.md", max_chars=max(content_chars, 8192))
        frontmatter = extract_frontmatter(content)
        category_frontmatter = frontmatter if include_frontmatter or content_chars > 0 else {}
        metadata = load_metadata(skill_dir)

        dir_category = rel.parts[0] if rel.parts else "other"
        raw_sources = {
            "directory": dir_category,
            "metadata": metadata.get("category") if isinstance(metadata.get("category"), str) else "",
            "frontmatter": (
                category_frontmatter.get("category")
                if isinstance(category_frontmatter.get("category"), str)
                else ""
            ),
        }
        declared_category = raw_sources["metadata"] or raw_sources["frontmatter"] or raw_sources["directory"]
        current_category = resolve_category(declared_category, allow_unknown=True)
        category_counts[current_category] += 1

        if current_category not in keyword_map and current_category not in {"other"}:
            try:
                resolve_category(current_category)
            except UnknownCategoryError:
                unknown_counts[current_category] += 1

        resolved_sources = {
            source: resolve_category(value, allow_unknown=True)
            for source, value in raw_sources.items()
            if value
        }
        semantics = skill_semantic_fields(
            skill_dir,
            metadata=metadata,
            frontmatter=frontmatter,
            rel=rel,
            content=content,
            content_chars=content_chars,
        )
        if len(set(resolved_sources.values())) > 1:
            category_conflicts.append(
                {
                    "path": str(rel),
                    "name": semantics["name"],
                    "resolved_sources": resolved_sources,
                    "raw_sources": {k: v for k, v in raw_sources.items() if v},
                }
            )

        for source, value in raw_sources.items():
            alias_slug = category_slug(value)
            if alias_slug in aliases:
                alias_usages.append(
                    {
                        "path": str(rel),
                        "source": source,
                        "alias": alias_slug,
                        "canonical_category": aliases[alias_slug],
                    }
                )

        text = str(semantics["text"])
        suggestion = best_suggestion(
            current_category,
            text,
            keyword_map,
            min_score=min_score,
            min_delta=min_delta,
        )
        if suggestion:
            candidates.append(
                {
                    "path": str(rel),
                    "name": semantics["name"],
                    "current_category": current_category,
                    **suggestion,
                }
            )

    candidates.sort(key=lambda item: (-item["score"], item["current_category"], item["path"]))
    nonzero_counts = dict(sorted(category_counts.items()))
    small_categories = [
        {"category": category, "count": count}
        for category, count in sorted(category_counts.items(), key=lambda item: (item[1], item[0]))
        if 0 < count <= small_category_threshold
    ]
    large_categories = [
        {"category": category, "count": count}
        for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0]))[:10]
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "skills_dir": str(skills_dir),
        "total_skills": total_skills,
        "standard_layout_skill_count": standard_layout_skills,
        "layout_issue_count": len(layout_issues),
        "layout_issues": compact_examples(layout_issues, limit_examples),
        "category_count": len(nonzero_counts),
        "category_counts": nonzero_counts,
        "large_categories": large_categories,
        "small_categories": small_categories,
        "unknown_categories": [
            {"category": category, "count": count}
            for category, count in sorted(unknown_counts.items())
        ],
        "alias_usages": compact_examples(alias_usages, limit_examples),
        "alias_usage_count": len(alias_usages),
        "category_conflicts": compact_examples(category_conflicts, limit_examples),
        "category_conflict_count": len(category_conflicts),
        "candidate_reclassifications": compact_examples(candidates, limit_candidates),
        "candidate_reclassification_count": len(candidates),
        "notes": [
            "Candidates are heuristic review targets, not automatic migrations.",
            "The audit scores every category, including non-other categories.",
            "Semantic scoring reads SKILL.md frontmatter before metadata.json.",
            "Pass --include-frontmatter to audit frontmatter category sources; pass --content-chars for deeper body scans.",
            "Layout issues catch nested paths such as category/category/skill/SKILL.md.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, default=Path("skills"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--include-frontmatter", action="store_true")
    parser.add_argument("--content-chars", type=int, default=0)
    parser.add_argument("--min-score", type=int, default=2)
    parser.add_argument("--min-delta", type=int, default=2)
    parser.add_argument("--small-category-threshold", type=int, default=10)
    parser.add_argument("--limit-candidates", type=int, default=100)
    parser.add_argument("--limit-examples", type=int, default=20)
    parser.add_argument(
        "--stratified-sample",
        action="store_true",
        help="Emit the deterministic per-category review sample instead of the heuristic report.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.stratified_sample:
        report = build_stratified_sample(
            args.skills_dir,
            content_chars=args.content_chars or 2048,
        )
    else:
        report = build_report(
            args.skills_dir,
            include_frontmatter=args.include_frontmatter,
            content_chars=args.content_chars,
            min_score=args.min_score,
            min_delta=args.min_delta,
            small_category_threshold=args.small_category_threshold,
            limit_candidates=args.limit_candidates,
            limit_examples=args.limit_examples,
        )
    payload = json.dumps(report, indent=2, ensure_ascii=False)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)
    return 1 if report.get("status") == "failed" else 0


if __name__ == "__main__":
    raise SystemExit(main())
