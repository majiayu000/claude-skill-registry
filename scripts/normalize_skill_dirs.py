#!/usr/bin/env python3
"""
Normalize skill directory names to the repo-suffix scheme.

Layout:
  <skills_dir>/<category>/<skill>/SKILL.md

Rules:
  - Base name from metadata.name (normalized)
  - Conflicts: {name}-{owner}-{repo}
  - If repo missing: {name}-{short-hash}
  - Winner keeps base name (official > stars > repo)
"""

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, List

from utils import (
    normalize_name,
    normalize_category,
    build_skill_key,
    get_repo_suffix,
    short_hash,
    normalize_repo,
    build_legal_metadata,
    load_metadata,
)

OFFICIAL_REPOS = {"anthropics/skills", "anthropics/claude-code"}


def derive_base_name(dir_name: str, meta: dict) -> str:
    name = meta.get("name")
    if name:
        return normalize_name(name)
    repo = meta.get("repo", "")
    suffix = get_repo_suffix(repo)
    if suffix and dir_name.endswith(f"-{suffix}"):
        return normalize_name(dir_name[: -(len(suffix) + 1)])
    return normalize_name(dir_name)


def compute_key(meta: dict, base_name: str, category: str) -> str:
    repo = normalize_repo(meta.get("repo", ""))
    path = meta.get("github_path") or meta.get("path") or ""
    return build_skill_key(repo, path, name=base_name, category=category)


def plan_normalization(skills_dir: Path) -> Dict[str, List[dict]]:
    """Return planned renames per category."""
    planned: Dict[str, List[dict]] = defaultdict(list)

    for category_dir in sorted(skills_dir.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue

        category = normalize_category(category_dir.name) or "other"

        # Group by base name
        groups: Dict[str, List[dict]] = defaultdict(list)
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue

            meta = load_metadata(skill_dir)
            base_name = derive_base_name(skill_dir.name, meta)
            repo = normalize_repo(meta.get("repo", ""))
            stars = meta.get("stars", 0) or 0
            key = compute_key(meta, base_name, category)

            groups[base_name].append({
                "category": category,
                "dir": skill_dir,
                "dir_name": skill_dir.name,
                "base_name": base_name,
                "repo": repo,
                "stars": stars,
                "key": key,
                "meta": meta,
            })

        # Resolve conflicts per base name
        used_lower: set[str] = set()
        for base_name, entries in groups.items():
            if len(entries) == 1:
                winner = entries[0]
                desired = base_name
                planned[category].append({**winner, "desired_name": desired})
                used_lower.add(desired.lower())
                continue

            def sort_key(e: dict):
                return (
                    e["repo"] in OFFICIAL_REPOS,
                    e["stars"],
                    e["repo"],
                    e["dir_name"],
                )

            sorted_entries = sorted(entries, key=sort_key, reverse=True)
            winner = sorted_entries[0]

            # Winner keeps base name if available
            desired_winner = base_name
            if desired_winner.lower() in used_lower:
                suffix = get_repo_suffix(winner["repo"]) or short_hash(winner["key"] or base_name)
                desired_winner = f"{base_name}-{suffix}"
                counter = 2
                while desired_winner.lower() in used_lower:
                    desired_winner = f"{base_name}-{suffix}-{counter}"
                    counter += 1

            planned[category].append({**winner, "desired_name": desired_winner})
            used_lower.add(desired_winner.lower())

            for entry in sorted_entries[1:]:
                suffix = get_repo_suffix(entry["repo"]) or short_hash(entry["key"] or base_name)
                desired = f"{base_name}-{suffix}"

                # Ensure unique within category
                candidate = desired
                if candidate.lower() in used_lower:
                    extra = short_hash(entry["key"] or candidate)
                    candidate = f"{desired}-{extra}"
                    counter = 2
                    while candidate.lower() in used_lower:
                        candidate = f"{desired}-{extra}-{counter}"
                        counter += 1

                planned[category].append({**entry, "desired_name": candidate})
                used_lower.add(candidate.lower())

    return planned


def apply_plan(plan: Dict[str, List[dict]], dry_run: bool = True) -> None:
    total = sum(len(items) for items in plan.values())
    changes = sum(1 for items in plan.values() for e in items if e["dir_name"] != e["desired_name"])

    print(f"Planned skills: {total}")
    print(f"Renames needed: {changes}")

    if dry_run:
        shown = 0
        for category, items in plan.items():
            for e in items:
                if e["dir_name"] != e["desired_name"]:
                    print(f"  {category}/{e['dir_name']} -> {category}/{e['desired_name']}")
                    shown += 1
                if shown >= 20:
                    print("  ...")
                    return
        return

    # First pass: move to temp names to avoid collisions
    temp_moves = []
    for category, items in plan.items():
        for e in items:
            if e["dir_name"] == e["desired_name"]:
                continue
            src = e["dir"]
            tmp_name = f"{e['dir_name']}__tmp-{short_hash(e['dir_name'] + e['desired_name'])}"
            tmp = src.parent / tmp_name
            if tmp.exists():
                shutil.rmtree(tmp)
            src.rename(tmp)
            temp_moves.append((tmp, src.parent / e["desired_name"], e))

    # Second pass: move temp to final
    for tmp, final, e in temp_moves:
        if final.exists():
            base = final.name
            suffix = short_hash(e["key"] or base)
            candidate = f"{base}-{suffix}"
            counter = 2
            while (final.parent / candidate).exists():
                candidate = f"{base}-{suffix}-{counter}"
                counter += 1
            final = final.parent / candidate
            e["desired_name"] = final.name
        tmp.rename(final)
        e["dir"] = final

    # Update metadata
    for category, items in plan.items():
        for e in items:
            meta = e["meta"] or {}
            meta["dir_name"] = e["desired_name"]
            meta["category"] = category
            if not meta.get("name"):
                meta["name"] = e["base_name"]
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
            meta_path = e["dir"] / "metadata.json"
            meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    print("Normalization complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize skill directory names")
    parser.add_argument("--skills-dir", default="skills", help="Skills root directory")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")

    args = parser.parse_args()
    skills_dir = Path(args.skills_dir)

    if not skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    plan = plan_normalization(skills_dir)
    apply_plan(plan, dry_run=not args.apply)


if __name__ == "__main__":
    main()
