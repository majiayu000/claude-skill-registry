#!/usr/bin/env python3
"""
Rebuild registry.json from downloaded skills.

Scans archived SKILL.md files recursively and rebuilds the registry index.
"""

import json
import logging
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from utils import extract_description, load_metadata

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def utc_now_isoformat() -> str:
    """Return a stable UTC timestamp with trailing Z."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def safe_write_registry(registry_path: Path, registry: dict) -> bool:
    """Safely write registry.json with atomic operation"""
    temp_path = registry_path.with_suffix('.json.tmp')
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, ensure_ascii=False, separators=(",", ":"))

        temp_path.rename(registry_path)
        return True
    except Exception as e:
        logger.error(f"Failed to write registry: {e}")
        if temp_path.exists():
            temp_path.unlink()
        return False


def scan_skills(skills_dir: Path) -> list:
    """
    Scan archived skills and build index.

    Supports archive layout:
    - <archive-root>/**/SKILL.md

    Metadata is optional for indexing. If metadata.json exists, it augments fields;
    otherwise fallback values are derived from path/content.
    """
    skills: list[dict] = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    for skill_md in skills_dir.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        rel_dir = skill_dir.relative_to(skills_dir)
        rel_parts = rel_dir.parts

        metadata = load_metadata(skill_dir)

        # Determine name
        name = metadata.get("name") or (rel_parts[-1] if rel_parts else skill_dir.name)

        # Determine category (prefer explicit metadata, then infer from path)
        inferred_category = rel_parts[0] if rel_parts else "other"
        category = metadata.get("category") or inferred_category

        # Read SKILL.md for description
        try:
            content = skill_md.read_text(encoding="utf-8")
            description = metadata.get("description") or extract_description(content)
        except UnicodeDecodeError as e:
            logger.warning(f"Encoding error reading {skill_md}: {e}")
            description = ""
        except Exception as e:
            logger.warning(f"Error reading {skill_md}: {e}")
            description = ""

        # Repo/path/branch normalization across different metadata formats
        repo = metadata.get("repo", "")
        github_path = (
            metadata.get("github_path")
            or metadata.get("path")
            or "/".join(rel_parts)
        )
        github_branch = (
            metadata.get("github_branch")
            or metadata.get("branch")
            or "main"
        )

        skill_entry = {
            "name": name,
            "description": description[:200] if description else f"Skill: {name}",
            "repo": repo,
            "path": github_path,
            "branch": github_branch,
            "category": category,
            "tags": metadata.get("tags", []),
            "stars": metadata.get("stars", 0),
            "source": metadata.get("source", "local"),
        }

        for key in ("author", "source_url", "license", "distribution", "permission_note"):
            value = metadata.get(key, "")
            if value not in ("", None):
                skill_entry[key] = value

        skills.append(skill_entry)

    return skills


def cleanup_orphan_metadata(skills_dir: Path) -> int:
    """
    Remove metadata.json files whose directories do not contain SKILL.md.

    This keeps archive parity clean without enforcing strict metadata schema checks.
    """
    skill_dirs = {p.parent for p in skills_dir.rglob("SKILL.md")}
    removed = 0

    for metadata_path in skills_dir.rglob("metadata.json"):
        if metadata_path.parent in skill_dirs:
            continue
        try:
            metadata_path.unlink()
            removed += 1
        except Exception as e:
            logger.warning(f"Failed to remove orphan metadata {metadata_path}: {e}")

    return removed


def sanitize_category(category: str) -> str:
    """Sanitize category name for use as filename."""
    # Replace / and other problematic characters with -
    return category.replace("/", "-").replace("\\", "-").replace(":", "-")


def build_category_indexes(skills: list, output_dir: Path):
    """Build category-based indexes."""
    categories = defaultdict(list)

    for skill in skills:
        cat = skill.get("category", "other")
        # Sanitize category for filename safety
        safe_cat = sanitize_category(cat)
        categories[safe_cat].append(skill)

    output_dir.mkdir(exist_ok=True)

    for cat, cat_skills in categories.items():
        cat_file = output_dir / f"{cat}.json"
        cat_data = {
            "category": cat,
            "count": len(cat_skills),
            "updated_at": utc_now_isoformat(),
            "skills": sorted(cat_skills, key=lambda x: (-x.get("stars", 0), x["name"])),
        }
        with open(cat_file, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)
        print(f"  {cat}: {len(cat_skills)} skills")

    # Index file
    index = {
        "updated_at": utc_now_isoformat(),
        "categories": [
            {"name": cat, "count": len(skills)}
            for cat, skills in sorted(categories.items())
        ]
    }
    with open(output_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


def load_plugins(sources_dir: Path) -> list:
    """Load plugins from sources/plugins.json."""
    plugins_path = sources_dir / "plugins.json"
    if not plugins_path.exists():
        return []
    try:
        with open(plugins_path, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("plugins", [])
    except Exception as e:
        logger.warning(f"Failed to load plugins: {e}")
        return []


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Rebuild registry.json from downloaded skills")
    parser.add_argument("--skills-dir", default="skills", help="Skills directory to scan")
    parser.add_argument("--registry", default="registry.json", help="Output registry.json path")
    parser.add_argument("--categories-dir", default="categories", help="Output categories directory")
    parser.add_argument("--skip-categories", action="store_true", help="Do not write category index files")

    args = parser.parse_args()

    def _main_from_args() -> None:
        script_dir = Path(__file__).parent
        registry_dir = script_dir.parent

        skills_dir = (registry_dir / args.skills_dir).resolve()
        registry_path = (registry_dir / args.registry).resolve()
        categories_dir = (registry_dir / args.categories_dir).resolve()
        sources_dir = (registry_dir / "sources").resolve()

        print("=" * 60)
        print("REBUILDING REGISTRY FROM DOWNLOADED SKILLS")
        print("=" * 60)
        print()

        print("Cleaning orphan metadata.json files...")
        orphan_removed = cleanup_orphan_metadata(skills_dir)
        print(f"Removed {orphan_removed} orphan metadata files")
        print()

        print(f"Scanning skills directory: {skills_dir}")
        skills = scan_skills(skills_dir)
        print(f"Found {len(skills)} skills")
        print()

        # Remove duplicates by repo:path (more accurate than name-only)
        # This prevents losing skills with same name but different sources
        seen = set()
        unique_skills = []
        duplicates_removed = 0

        for s in skills:
            # Use repo:path as unique key (most accurate)
            repo = s.get("repo", "")
            path = s.get("path", "")

            if repo and path:
                key = f"{repo}:{path}"
            elif repo:
                key = repo
            else:
                # Fallback to category:name for local skills without repo
                key = f"{s.get('category', 'other')}:{s['name']}"

            if key not in seen:
                seen.add(key)
                unique_skills.append(s)
            else:
                duplicates_removed += 1

        print(f"Duplicates removed: {duplicates_removed}")
        print(f"Unique skills: {len(unique_skills)}")
        print()

        # Sort by stars then name
        unique_skills.sort(key=lambda x: (-x.get("stars", 0), x["name"].lower()))

        # Load plugins
        plugins = load_plugins(sources_dir)
        print(f"Plugins loaded: {len(plugins)}")
        print()

        archive_skill_md_count_raw = sum(1 for _ in skills_dir.rglob("SKILL.md"))
        archive_metadata_count_raw = sum(1 for _ in skills_dir.rglob("metadata.json"))

        # Build registry
        registry = {
            "version": "2.1.0",
            "updated_at": utc_now_isoformat(),
            "total_count": len(unique_skills),
            "plugin_count": len(plugins),
            "archive_skill_md_count_raw": archive_skill_md_count_raw,
            "archive_metadata_count_raw": archive_metadata_count_raw,
            "registry_skill_count_dedup": len(unique_skills),
            "skills": unique_skills,
            "plugins": plugins,
        }

        if safe_write_registry(registry_path, registry):
            print(f"Written {registry_path} with {len(unique_skills)} skills, {len(plugins)} plugins")
        else:
            print("Failed to write registry!")
            return
        print()

        if not args.skip_categories:
            print(f"Building category indexes: {categories_dir}")
            build_category_indexes(unique_skills, categories_dir)
            print()

            # Stats
            print("=" * 60)
            print("CATEGORY DISTRIBUTION")
            print("=" * 60)
            cat_counts = defaultdict(int)
            for s in unique_skills:
                cat_counts[s.get("category", "other")] += 1

            for cat, count in sorted(cat_counts.items(), key=lambda x: -x[1]):
                pct = count / len(unique_skills) * 100 if unique_skills else 0
                bar = "█" * int(pct / 2)
                print(f"  {cat:15} {count:6} ({pct:5.1f}%) {bar}")

            print()

        print("=" * 60)
        print("DONE!")
        print("=" * 60)

    _main_from_args()
