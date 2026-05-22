#!/usr/bin/env python3
"""
Normalize non-standard skill directory depths to:
  skills/<category>/<skill>/SKILL.md

Default mode is a dry run. Use --json for a machine-readable migration report
and --apply only after reviewing the planned destinations.
"""

from __future__ import annotations

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from category_taxonomy import resolve_category
from utils import (
    build_legal_metadata,
    build_skill_key,
    get_repo_suffix,
    load_metadata,
    normalize_category,
    normalize_name,
    normalize_repo,
    short_hash,
    write_metadata,
)

LAYOUT_EXPECTED = "<category>/<skill>/SKILL.md"
SKILLS_PREFIX_NAMES = {"skill", "skills"}


def is_standard(rel_parts: tuple[str, ...]) -> bool:
    return len(rel_parts) == 3 and rel_parts[2] == "SKILL.md" and not rel_parts[0].startswith(".")


def iter_nonstandard_skill_dirs(skills_dir: Path):
    for skill_md in sorted(skills_dir.rglob("SKILL.md")):
        rel = skill_md.relative_to(skills_dir)
        if any(part.startswith(".") for part in rel.parts):
            continue
        if not is_standard(rel.parts):
            yield skill_md.parent, rel


def infer_category(rel_parts: tuple[str, ...], meta: dict[str, Any]) -> str:
    raw_category = meta.get("category") if isinstance(meta.get("category"), str) else ""
    if raw_category:
        return normalize_category(raw_category)

    if rel_parts and rel_parts[0] in SKILLS_PREFIX_NAMES and len(rel_parts) > 1:
        return normalize_category(rel_parts[1])

    first_part = rel_parts[0] if rel_parts else "other"
    category = normalize_category(first_part)
    if category.startswith("."):
        return "other"
    return category or "other"


def existing_category_state(skills_dir: Path) -> dict[str, dict[str, Any]]:
    state: dict[str, dict[str, Any]] = defaultdict(lambda: {"names": set(), "key_to_name": {}})
    for category_dir in sorted(skills_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        category = normalize_category(category_dir.name)
        for skill_dir in sorted(category_dir.iterdir()):
            if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
                continue
            meta = load_metadata(skill_dir)
            name = normalize_name(meta.get("name") or skill_dir.name)
            repo = normalize_repo(meta.get("repo", ""))
            path = meta.get("github_path") or meta.get("path") or ""
            key = build_skill_key(repo, path, name=name, category=category)
            state[category]["names"].add(skill_dir.name.lower())
            if key:
                state[category]["key_to_name"].setdefault(key, skill_dir.name)
    return state


def unique_dir_name(
    *,
    category_state: dict[str, Any],
    base_name: str,
    repo: str,
    key: str,
) -> tuple[str, bool]:
    base = normalize_name(base_name)
    key_to_name = category_state["key_to_name"]
    if key and key in key_to_name:
        return key_to_name[key], True

    if base.lower() not in category_state["names"]:
        category_state["names"].add(base.lower())
        return base, False

    suffix = get_repo_suffix(repo)
    if suffix and not base.endswith(f"-{suffix}"):
        candidate_base = f"{base}-{suffix}"
    else:
        candidate_base = f"{base}-{short_hash(key or base)}"

    candidate = candidate_base
    counter = 2
    while candidate.lower() in category_state["names"]:
        candidate = f"{candidate_base}-{counter}"
        counter += 1

    category_state["names"].add(candidate.lower())
    return candidate, False


def build_depth_plan(skills_dir: Path) -> dict[str, Any]:
    state = existing_category_state(skills_dir)
    moves: list[dict[str, Any]] = []

    for skill_dir, rel in iter_nonstandard_skill_dirs(skills_dir):
        meta = load_metadata(skill_dir)
        category = infer_category(rel.parts, meta)
        category = resolve_category(category, allow_unknown=True)
        name = normalize_name(meta.get("name") or skill_dir.name)
        repo = normalize_repo(meta.get("repo", ""))
        path = meta.get("github_path") or meta.get("path") or ""
        key = build_skill_key(repo, path, name=name, category=category)
        category_state = state[category]
        target_name, reuses_existing_key = unique_dir_name(
            category_state=category_state,
            base_name=name,
            repo=repo,
            key=key or str(rel),
        )
        target_rel = Path(category) / target_name
        moves.append(
            {
                "source_path": str(skill_dir.relative_to(skills_dir)),
                "source_skill": str(rel),
                "operation": "remove_duplicate" if reuses_existing_key else "move",
                "target_path": str(target_rel),
                "target_skill": str(target_rel / "SKILL.md"),
                "category": category,
                "name": name,
                "repo": repo,
                "key": key,
                "metadata_category": meta.get("category", ""),
                "layout_depth": len(rel.parts),
                "expected_layout": LAYOUT_EXPECTED,
            }
        )

    duplicate_count = sum(1 for move in moves if move["operation"] == "remove_duplicate")
    return {
        "skills_dir": str(skills_dir),
        "expected_layout": LAYOUT_EXPECTED,
        "move_count": len(moves),
        "duplicate_count": duplicate_count,
        "moves": moves,
    }


def skill_key_for_dir(skill_dir: Path, category: str) -> str:
    meta = load_metadata(skill_dir)
    name = normalize_name(meta.get("name") or skill_dir.name)
    repo = normalize_repo(meta.get("repo", ""))
    path = meta.get("github_path") or meta.get("path") or ""
    return build_skill_key(repo, path, name=name, category=category)


def apply_depth_plan(skills_dir: Path, plan: dict[str, Any]) -> None:
    moves = sorted(
        plan["moves"],
        key=lambda move: (-len(Path(move["source_path"]).parts), move["source_path"]),
    )
    for move in moves:
        source = skills_dir / move["source_path"]
        target = skills_dir / move["target_path"]
        if not source.exists():
            raise FileNotFoundError(f"Planned source does not exist: {source}")
        if move.get("operation") == "remove_duplicate":
            if not target.exists():
                raise FileNotFoundError(f"Duplicate target does not exist: {target}")
            if skill_key_for_dir(target, str(move["category"])) != move.get("key"):
                raise ValueError(f"Duplicate target key mismatch: {target}")
            shutil.rmtree(source)
            continue
        if target.exists():
            raise FileExistsError(f"Planned target already exists: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        source.rename(target)
        meta = load_metadata(target)
        meta.setdefault("name", move["name"])
        meta["category"] = move["category"]
        meta["dir_name"] = target.name
        legal_meta = build_legal_metadata(
            repo=normalize_repo(meta.get("repo", "")),
            path=meta.get("github_path") or meta.get("path") or "",
            branch=meta.get("github_branch") or meta.get("branch") or "main",
            source_url=meta.get("source_url", ""),
            author=meta.get("author", ""),
            license_name=meta.get("license", ""),
            copyright_text=meta.get("copyright", ""),
            permission_note=meta.get("permission_note", ""),
            distribution=meta.get("distribution", ""),
        )
        meta.update(legal_meta)
        write_metadata(target, meta)


def print_text_report(plan: dict[str, Any], *, limit: int) -> None:
    print(f"Non-standard SKILL.md dirs found: {plan['move_count']}")
    for move in plan["moves"][:limit]:
        print(f"  {move['source_path']} -> {move['target_path']}")
    if plan["move_count"] > limit:
        print("  ...")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Normalize non-standard skill depths")
    parser.add_argument("--skills-dir", default="skills", help="Skills root directory")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON report")
    parser.add_argument("--output", type=Path, help="Write the JSON report to a file")
    parser.add_argument("--limit", type=int, default=20, help="Text preview limit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    plan = build_depth_plan(skills_dir)
    if args.apply:
        apply_depth_plan(skills_dir, plan)

    if args.json or args.output:
        payload = json.dumps(plan, indent=2, ensure_ascii=False)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload + "\n", encoding="utf-8")
        if args.json:
            print(payload)
    else:
        print_text_report(plan, limit=args.limit)
        if args.apply:
            print("Depth normalization complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
