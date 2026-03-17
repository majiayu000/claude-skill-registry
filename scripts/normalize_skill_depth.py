#!/usr/bin/env python3
"""
Normalize non-standard skill directory depths to:
  skills/<category>/<skill>/SKILL.md

Moves any SKILL.md found outside the standard depth into the category root
with a temporary unique name, then relies on normalize_skill_dirs.py for
final naming.
"""

import argparse
import json
import shutil
from pathlib import Path

from utils import (
    normalize_name,
    normalize_category,
    normalize_repo,
    build_skill_key,
    short_hash,
    build_legal_metadata,
    load_metadata,
    write_metadata,
)


def is_standard(rel_parts: tuple[str, ...]) -> bool:
    return len(rel_parts) == 3 and rel_parts[2] == "SKILL.md" and not rel_parts[0].startswith(".")


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize non-standard skill depths")
    parser.add_argument("--skills-dir", default="skills", help="Skills root directory")
    parser.add_argument("--apply", action="store_true", help="Apply changes (default: dry-run)")
    parser.add_argument("--max-passes", type=int, default=5, help="Max normalization passes")

    args = parser.parse_args()
    skills_dir = Path(args.skills_dir)
    if not skills_dir.exists():
        raise SystemExit(f"Skills directory not found: {skills_dir}")

    for pass_num in range(1, args.max_passes + 1):
        moves = []
        seen_dirs = set()

        for skill_md in skills_dir.rglob("SKILL.md"):
            rel = skill_md.relative_to(skills_dir)
            if is_standard(rel.parts):
                continue

            skill_dir = skill_md.parent
            if skill_dir in seen_dirs:
                continue
            seen_dirs.add(skill_dir)

            meta = load_metadata(skill_dir)
            raw_category = meta.get("category", "")
            if raw_category:
                category = normalize_category(raw_category) or "other"
            else:
                category = normalize_category(rel.parts[0] if rel.parts else "other") or "other"
                if category.startswith("."):
                    category = "other"

            name = normalize_name(meta.get("name") or skill_dir.name)
            repo = normalize_repo(meta.get("repo", ""))
            path = meta.get("github_path") or meta.get("path") or ""
            key = build_skill_key(repo, path, name=name, category=category)

            temp_base = f"{name}-{short_hash(key or name)}-depth"
            target_dir = skills_dir / category / temp_base
            counter = 2
            while target_dir.exists():
                target_dir = skills_dir / category / f"{temp_base}-{counter}"
                counter += 1

            moves.append((skill_dir, target_dir, meta, category, name))

        print(f"Pass {pass_num}: Non-standard SKILL.md dirs found: {len(moves)}")
        if not args.apply:
            for src, dest, _, _, _ in moves[:20]:
                print(f"  {src.relative_to(skills_dir)} -> {dest.relative_to(skills_dir)}")
            if len(moves) > 20:
                print("  ...")
            return

        if not moves:
            break

        for src, dest, meta, category, name in moves:
            dest.parent.mkdir(parents=True, exist_ok=True)
            if dest.exists():
                continue
            shutil.move(str(src), str(dest))

            if not meta:
                meta = {}
            meta.setdefault("name", name)
            meta["category"] = category
            meta["dir_name"] = dest.name
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
            write_metadata(dest, meta)

    print("Depth normalization complete.")


if __name__ == "__main__":
    main()
