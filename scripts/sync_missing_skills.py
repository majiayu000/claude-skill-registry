#!/usr/bin/env python3
"""
Sync missing skills from a source skills root to a destination skills root.

Source layout can be:
  - flat: <src>/<skill>/SKILL.md
  - category: <src>/<category>/<skill>/SKILL.md

Destination layout:
  - category: <dest>/<category>/<skill>/SKILL.md
"""

import argparse
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, Tuple

from utils import (
    build_legal_metadata,
    build_skill_key,
    get_repo_suffix,
    load_metadata,
    normalize_category,
    normalize_name,
    normalize_repo,
    short_hash,
)


def iter_skills(root: Path, layout: str = "auto") -> Iterable[Tuple[str, Path]]:
    """Yield (category, skill_dir) from a root using specified layout."""
    if not root.exists():
        return []

    if layout == "auto":
        direct_skills = [d for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
        layout = "flat" if len(direct_skills) >= 50 else "category"

    if layout == "flat":
        for d in root.iterdir():
            if not d.is_dir():
                continue
            if not (d / "SKILL.md").exists():
                continue
            meta = load_metadata(d)
            category = normalize_category(meta.get("category", "other")) or "other"
            yield category, d
        return

    # Category layout
    for category_dir in root.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith("."):
            continue
        category = normalize_category(category_dir.name) or "other"
        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            if not (skill_dir / "SKILL.md").exists():
                continue
            yield category, skill_dir


def skill_key_from_meta(meta: dict, category: str, fallback_name: str) -> str:
    repo = normalize_repo(meta.get("repo", ""))
    path = meta.get("github_path") or meta.get("path") or ""
    name = meta.get("name") or fallback_name
    return build_skill_key(repo, path, name=name, category=category)


def build_dest_index(dest_root: Path, layout: str) -> tuple[Dict[str, Path], Dict[str, set]]:
    index: Dict[str, Path] = {}
    names_by_category: Dict[str, set] = defaultdict(set)
    for category, skill_dir in iter_skills(dest_root, layout):
        meta = load_metadata(skill_dir)
        key = skill_key_from_meta(meta, category, skill_dir.name)
        if key:
            index[key] = skill_dir
        names_by_category[category].add(skill_dir.name.lower())
    return index, names_by_category


def main() -> None:
    parser = argparse.ArgumentParser(description="Sync missing skills into destination repo")
    parser.add_argument("--src", required=True, help="Source skills root")
    parser.add_argument("--dest", required=True, help="Destination skills root")
    parser.add_argument("--src-layout", choices=["auto", "flat", "category"], default="auto")
    parser.add_argument("--dest-layout", choices=["auto", "flat", "category"], default="category")
    parser.add_argument("--apply", action="store_true", help="Apply copy (default: dry-run)")

    args = parser.parse_args()
    src_root = Path(args.src)
    dest_root = Path(args.dest)

    if not src_root.exists():
        raise SystemExit(f"Source not found: {src_root}")
    if not dest_root.exists():
        raise SystemExit(f"Destination not found: {dest_root}")

    dest_index, names_by_category = build_dest_index(dest_root, args.dest_layout)
    print(f"Destination indexed skills: {len(dest_index)}")

    to_copy = []
    for category, skill_dir in iter_skills(src_root, args.src_layout):
        meta = load_metadata(skill_dir)
        key = skill_key_from_meta(meta, category, skill_dir.name)
        if not key or key in dest_index:
            continue
        to_copy.append((category, skill_dir, key))

    print(f"Missing skills to copy: {len(to_copy)}")
    if not args.apply:
        for category, skill_dir, _ in to_copy[:20]:
            print(f"  {skill_dir} -> {dest_root / category / skill_dir.name}")
        if len(to_copy) > 20:
            print("  ...")
        return

    copied = 0
    for category, skill_dir, key in to_copy:
        meta = load_metadata(skill_dir)
        name = normalize_name(meta.get("name") or skill_dir.name)
        repo = normalize_repo(meta.get("repo", ""))

        existing_names = names_by_category.setdefault(category, set())
        if name.lower() in existing_names:
            suffix = get_repo_suffix(repo) or short_hash(key or name)
            dest_name = f"{name}-{suffix}"
            counter = 2
            while dest_name.lower() in existing_names:
                dest_name = f"{name}-{suffix}-{counter}"
                counter += 1
        else:
            dest_name = name

        dest_dir = dest_root / category / dest_name
        dest_dir.parent.mkdir(parents=True, exist_ok=True)

        if dest_dir.exists():
            dest_index[key] = dest_dir
            continue

        shutil.copytree(skill_dir, dest_dir)
        existing_names.add(dest_name.lower())

        # Update metadata with new dir name and category
        meta_path = dest_dir / "metadata.json"
        if meta_path.exists():
            try:
                meta_out = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                meta_out = {}
            meta_out["dir_name"] = dest_dir.name
            meta_out["category"] = category
            if not meta_out.get("name"):
                meta_out["name"] = name
            legal_meta = build_legal_metadata(
                repo=normalize_repo(meta_out.get("repo", "")),
                path=meta_out.get("github_path") or meta_out.get("path") or "",
                branch=meta_out.get("github_branch") or meta_out.get("branch") or "main",
                source_url=meta_out.get("source_url", ""),
                author=meta_out.get("author", ""),
                license_name=meta_out.get("license", ""),
                copyright_text=meta_out.get("copyright", ""),
                permission_note=meta_out.get("permission_note", ""),
                distribution=meta_out.get("distribution", ""),
            )
            meta_out.update(legal_meta)
            meta_path.write_text(json.dumps(meta_out, indent=2, ensure_ascii=False), encoding="utf-8")

        dest_index[key] = dest_dir
        copied += 1

    print(f"Copied {copied} skills")


if __name__ == "__main__":
    main()
