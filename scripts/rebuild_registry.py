#!/usr/bin/env python3
"""
Rebuild registry.json from downloaded skills.

Scans all skills/*/SKILL.md files and rebuilds the registry index.
"""

import json
import os
import re
import logging
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import yaml

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from SKILL.md."""
    if not content.startswith("---"):
        return {}

    try:
        # Find the closing ---
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return {}

        frontmatter = content[3:end_idx].strip()
        return yaml.safe_load(frontmatter) or {}
    except Exception:
        return {}


def extract_description(content: str) -> str:
    """Extract description from content."""
    # Try frontmatter first
    fm = extract_frontmatter(content)
    if fm.get("description"):
        return fm["description"][:200]

    # Try first paragraph after frontmatter
    lines = content.split("\n")
    in_frontmatter = False

    for line in lines:
        line = line.strip()
        if line == "---":
            in_frontmatter = not in_frontmatter
            continue
        if in_frontmatter:
            continue
        if line.startswith("#"):
            continue
        if line and not line.startswith("```"):
            # Clean markdown
            line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
            line = re.sub(r'[*_`]', '', line)
            return line[:200]

    return ""


def safe_load_metadata(metadata_path: Path) -> dict:
    """Safely load metadata.json"""
    if not metadata_path.exists():
        return {}
    try:
        with open(metadata_path, encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.warning(f"JSON parse error in {metadata_path}: {e}")
        return {}
    except Exception as e:
        logger.warning(f"Error reading {metadata_path}: {e}")
        return {}


def safe_write_registry(registry_path: Path, registry: dict) -> bool:
    """Safely write registry.json with atomic operation"""
    temp_path = registry_path.with_suffix('.json.tmp')
    try:
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(registry, f, indent=2, ensure_ascii=False)

        # Backup original file
        if registry_path.exists():
            backup_path = registry_path.with_suffix('.json.bak')
            if backup_path.exists():
                backup_path.unlink()
            registry_path.rename(backup_path)

        temp_path.rename(registry_path)
        return True
    except Exception as e:
        logger.error(f"Failed to write registry: {e}")
        if temp_path.exists():
            temp_path.unlink()
        return False


def scan_skills(skills_dir: Path) -> list:
    """Scan all skills and build index."""
    skills = []

    for skill_md in skills_dir.rglob("SKILL.md"):
        rel_path = skill_md.relative_to(skills_dir)
        parts = rel_path.parts

        if len(parts) < 2:
            continue

        category = parts[0]
        name = parts[1]

        # Skip if category is 'data' (flat structure)
        if category == "data":
            # In data/, structure is data/{name}/SKILL.md
            pass

        # Read metadata.json if exists
        metadata_path = skill_md.parent / "metadata.json"
        metadata = safe_load_metadata(metadata_path)

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

        # Build install path
        repo = metadata.get("repo", "")
        github_path = metadata.get("github_path", "")
        github_branch = metadata.get("github_branch", "main")

        if github_path and repo:
            install = f"{repo}/{github_path}"
        elif repo:
            install = repo
        else:
            install = f"unknown/{name}"

        skill_entry = {
            "name": name,
            "description": description[:200] if description else f"Skill: {name}",
            "repo": repo,
            "path": github_path or str(rel_path.parent),
            "branch": github_branch,
            "category": metadata.get("category", category),
            "tags": metadata.get("tags", []),
            "stars": metadata.get("stars", 0),
            "install": install,
            "source": metadata.get("source", "local"),
        }

        skills.append(skill_entry)

    return skills


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
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "skills": sorted(cat_skills, key=lambda x: (-x.get("stars", 0), x["name"])),
        }
        with open(cat_file, "w", encoding="utf-8") as f:
            json.dump(cat_data, f, indent=2, ensure_ascii=False)
        print(f"  {cat}: {len(cat_skills)} skills")

    # Index file
    index = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "categories": [
            {"name": cat, "count": len(skills)}
            for cat, skills in sorted(categories.items())
        ]
    }
    with open(output_dir / "index.json", "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)


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

        print("=" * 60)
        print("REBUILDING REGISTRY FROM DOWNLOADED SKILLS")
        print("=" * 60)
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

        # Build registry
        registry = {
            "version": "2.0.0",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "total_count": len(unique_skills),
            "skills": unique_skills,
        }

        if safe_write_registry(registry_path, registry):
            print(f"Written {registry_path} with {len(unique_skills)} skills")
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
