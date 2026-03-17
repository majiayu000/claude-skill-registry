#!/usr/bin/env python3
"""
Build Search Index v2.0 - Generate lightweight search index

Supports directory structure:
- skills/{category}/{skill-name}/SKILL.md

Output files:
- search-index.json - Minimal index (~1-2MB gzip)
- categories/*.json - Category-based indexes
- featured.json - Top 100 skills by stars
"""

import json
import gzip
from pathlib import Path
from datetime import datetime
from typing import Any, Dict, List, Optional
import argparse
import logging

from utils import get_repo_suffix, extract_description, load_metadata

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

# Category short codes
CATEGORY_CODES = {
    "development": "dev",
    "devops": "ops",
    "security": "sec",
    "documents": "doc",
    "design": "des",
    "testing": "tst",
    "product": "prd",
    "marketing": "mkt",
    "productivity": "pro",
    "data": "dat",
    "official": "off",
    "other": "oth",
}

# Known category directories (for scanning)
KNOWN_CATEGORIES = set(CATEGORY_CODES.keys()) | {"data", "other"}


def truncate_text(text: Any, max_length: int) -> str:
    """Truncate text to max length with ellipsis."""
    if not text:
        return ""
    if isinstance(text, list):
        text = " ".join(str(t) for t in text if t)
    text = str(text).strip().replace("\n", " ").replace("\r", "")
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_category_code(category: str) -> str:
    """Get short code for category."""
    if not category:
        return "oth"
    return CATEGORY_CODES.get(category.lower(), "oth")


def scan_skills_v2(skills_dir: Path) -> List[Dict]:
    """Scan skills directory with structure: skills/{category}/{skill-name}/"""
    skills = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir():
            continue
        if category_dir.name.startswith('.'):
            continue

        category_name = category_dir.name

        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            skill_md = skill_dir / "SKILL.md"
            metadata_file = skill_dir / "metadata.json"

            if not skill_md.exists():
                continue

            dir_name = skill_dir.name

            # Load metadata
            metadata = load_metadata(skill_dir) if metadata_file.exists() else {}

            # Get skill name (from metadata or directory)
            name = metadata.get("name") or dir_name

            # Remove repo suffix from dir_name if metadata repo is available
            if name == dir_name:
                repo = metadata.get("repo", "")
                suffix = get_repo_suffix(repo)
                if suffix and dir_name.endswith(f"-{suffix}"):
                    name = dir_name[: -(len(suffix) + 1)]

            # Get description
            description = metadata.get("description", "")
            if not description:
                try:
                    content = skill_md.read_text(encoding='utf-8')
                    description = extract_description(content)
                except Exception:
                    pass
            if not description:
                description = f"Skill: {name}"

            # Get category
            category = metadata.get("category", category_name)

            # Build install path
            repo = metadata.get("repo", "")
            github_path = metadata.get("github_path", "")
            github_branch = metadata.get("github_branch", "main")  # Default to main

            if github_path and repo:
                install = f"{repo}/{github_path}"
            elif repo:
                install = repo
            else:
                install = f"unknown/{name}"

            skill_entry = {
                "name": name,
                "dir_name": dir_name,
                "description": description,
                "repo": repo,
                "path": github_path,
                "branch": github_branch,
                "category": category,
                "tags": metadata.get("tags", []),
                "stars": metadata.get("stars", 0),
                "source": metadata.get("source", "downloaded"),
                "install": install,
            }

            skills.append(skill_entry)

    return skills


def load_registry_count(registry_path: Path) -> Optional[int]:
    """Load deduplicated skill count from registry.json."""
    if not registry_path.exists():
        return None
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    except Exception:
        return None

    total = registry.get("total_count")
    if isinstance(total, int):
        return total

    skills = registry.get("skills")
    if isinstance(skills, list):
        return len(skills)

    return None


def load_previous_raw_count(output_dir: Path) -> Optional[int]:
    """Try to keep raw count stable when rebuilding from deduplicated registry only."""
    stats_path = output_dir / "stats.json"
    if not stats_path.exists():
        return None
    try:
        with open(stats_path, 'r', encoding='utf-8') as f:
            stats = json.load(f)
    except Exception:
        return None

    raw_count = stats.get("raw_skill_count")
    if isinstance(raw_count, int):
        return raw_count

    # Backward-compatible fallback for older stats format
    total_skills = stats.get("total_skills")
    if isinstance(total_skills, int):
        return total_skills
    return None


def count_skill_files(skills_dir: Path) -> Optional[int]:
    """Count SKILL.md files quickly without full metadata parse."""
    if not skills_dir.exists():
        return None
    try:
        return sum(1 for _ in skills_dir.rglob("SKILL.md"))
    except Exception:
        return None


def build_search_index(
    skills: List[Dict],
    output_dir: Path,
    source_name: str = "skills",
    raw_skill_count: Optional[int] = None,
    dedup_skill_count: Optional[int] = None,
) -> Dict[str, Any]:
    """Build the lightweight search index."""
    logger.info(f"Building index from {len(skills)} {source_name}...")

    # Build minimal search index
    search_index = {
        "v": datetime.utcnow().strftime("%Y-%m-%d"),
        "t": len(skills),
        "s": []
    }

    # Category indexes
    categories: Dict[str, List[Dict]] = {}

    # Featured skills
    featured_skills = []

    for skill in skills:
        name = skill.get('name', '')
        description = skill.get('description', '')
        category = skill.get('category', 'other')
        tags = skill.get('tags', [])
        stars = skill.get('stars', 0)
        repo = skill.get('repo', '')
        install = skill.get('install', repo)
        branch = skill.get('branch', 'main')

        # Minimal record
        mini_record = {
            "n": name,
            "d": truncate_text(description, 80),
            "c": get_category_code(category),
            "g": tags[:5] if tags else [],
            "r": stars,
            "i": install,
            "b": branch  # branch for GitHub URL
        }
        search_index["s"].append(mini_record)

        # Full record
        full_record = {
            "name": name,
            "description": truncate_text(description, 200),
            "repo": repo,
            "path": skill.get('path', ''),
            "branch": branch,
            "category": category,
            "tags": tags[:10] if tags else [],
            "stars": stars,
            "install": install,
            "source": skill.get('source', '')
        }

        # Add to category
        if category not in categories:
            categories[category] = []
        categories[category].append(full_record)

        # Track for featured
        if stars > 0:
            featured_skills.append(full_record)

    # Sort by stars
    search_index["s"].sort(key=lambda x: x.get("r", 0), reverse=True)
    featured_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)
    featured_skills = featured_skills[:100]

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    categories_dir = output_dir / "categories"
    categories_dir.mkdir(exist_ok=True)

    # Write search index
    search_index_path = output_dir / "search-index.json"
    with open(search_index_path, 'w', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    # Write gzipped version
    search_index_gz_path = output_dir / "search-index.json.gz"
    with gzip.open(search_index_gz_path, 'wt', encoding='utf-8') as f:
        json.dump(search_index, f, ensure_ascii=False, separators=(',', ':'))

    logger.info(f"  search-index.json: {search_index_path.stat().st_size / 1024 / 1024:.2f} MB")
    logger.info(f"  search-index.json.gz: {search_index_gz_path.stat().st_size / 1024 / 1024:.2f} MB")

    # Write category indexes
    category_index = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "categories": []
    }

    for category, cat_skills in sorted(categories.items()):
        cat_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)

        cat_data = {
            "category": category,
            "code": get_category_code(category),
            "count": len(cat_skills),
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "skills": cat_skills
        }

        cat_path = categories_dir / f"{category}.json"
        with open(cat_path, 'w', encoding='utf-8') as f:
            json.dump(cat_data, f, ensure_ascii=False, indent=2)

        category_index["categories"].append({
            "name": category,
            "code": get_category_code(category),
            "count": len(cat_skills)
        })

        logger.info(f"  categories/{category}.json: {len(cat_skills)} skills")

    # Write category index
    with open(categories_dir / "index.json", 'w', encoding='utf-8') as f:
        json.dump(category_index, f, ensure_ascii=False, indent=2)

    # Write featured
    featured_data = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(featured_skills),
        "skills": featured_skills
    }
    with open(output_dir / "featured.json", 'w', encoding='utf-8') as f:
        json.dump(featured_data, f, ensure_ascii=False, indent=2)

    logger.info(f"  featured.json: {len(featured_skills)} skills")

    # Write stats
    collections_count_path = output_dir / "collections.json"
    collection_count = 0
    if collections_count_path.exists():
        try:
            with open(collections_count_path, 'r', encoding='utf-8') as f:
                collection_count = json.load(f).get("count", 0)
        except Exception:
            pass

    stats = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_skills": len(skills),
        "total_collections": collection_count,
        "raw_skill_count": raw_skill_count,
        "dedup_skill_count": dedup_skill_count,
        "categories": len(categories),
        "featured_count": len(featured_skills),
        "index_size_bytes": search_index_path.stat().st_size,
        "index_size_gzip_bytes": search_index_gz_path.stat().st_size,
    }
    # Attach latest security scan summary if available
    security_report_path = output_dir / "security-report.json"
    if security_report_path.exists():
        try:
            with open(security_report_path, 'r', encoding='utf-8') as f:
                security_report = json.load(f)
            stats["security_scan"] = {
                "total": security_report.get("total"),
                "passed": security_report.get("passed"),
                "failed": security_report.get("failed"),
            }
        except Exception:
            stats["security_scan"] = {
                "total": None,
                "passed": None,
                "failed": None,
            }
    with open(output_dir / "stats.json", 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    logger.info(f"\nIndex build complete!")
    logger.info(f"  Total skills: {len(skills)}")
    if raw_skill_count is not None:
        logger.info(f"  Raw skill count: {raw_skill_count}")
    if dedup_skill_count is not None:
        logger.info(f"  Deduplicated skill count: {dedup_skill_count}")
    logger.info(f"  Categories: {len(categories)}")

    return stats


def load_from_registry(registry_path: Path) -> List[Dict]:
    """Load skills from registry.json (fallback mode)."""
    with open(registry_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)

    skills = registry.get('skills', [])

    for skill in skills:
        repo = skill.get('repo', '')
        path = skill.get('path', '')
        skill['install'] = f"{repo}/{path}" if path else repo

    return skills


def load_collections_from_registry(registry_path: Path) -> List[Dict]:
    """Load collections from registry.json."""
    if not registry_path.exists():
        return []
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        return registry.get('collections', [])
    except Exception:
        return []


def load_collections_from_source(sources_dir: Path) -> List[Dict]:
    """Load collections from sources/collections.json."""
    collections_path = sources_dir / "collections.json"
    if not collections_path.exists():
        return []
    try:
        with open(collections_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('collections', [])
    except Exception:
        return []


def build_collections_index(
    collections: List[Dict],
    output_dir: Path,
) -> None:
    """Write collections.json to output directory."""
    if not collections:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    collections_data = {
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "count": len(collections),
        "collections": collections,
    }
    with open(output_dir / "collections.json", 'w', encoding='utf-8') as f:
        json.dump(collections_data, f, ensure_ascii=False, indent=2)

    logger.info(f"  collections.json: {len(collections)} collections")


def main():
    parser = argparse.ArgumentParser(description='Build search index for skill registry')
    parser.add_argument('--skills-dir', '-s', default='skills', help='Skills directory')
    parser.add_argument('--registry', '-r', default='registry.json', help='Registry.json (fallback)')
    parser.add_argument('--output', '-o', default='docs', help='Output directory')
    parser.add_argument('--use-registry', action='store_true', help='Force use registry.json')

    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    registry_path = Path(args.registry)
    output_dir = Path(args.output)

    raw_skill_count: Optional[int] = None
    dedup_skill_count: Optional[int] = None

    # Prefer scanning skills directory
    if not args.use_registry and skills_dir.exists():
        logger.info(f"Scanning skills from {skills_dir}")
        skills = scan_skills_v2(skills_dir)
        source_name = "verified downloaded skills"
        raw_skill_count = len(skills)
        dedup_skill_count = load_registry_count(registry_path)
        if dedup_skill_count is None:
            dedup_skill_count = len(skills)
    elif registry_path.exists():
        logger.info(f"Loading from registry: {registry_path}")
        skills = load_from_registry(registry_path)
        source_name = "registry entries"
        dedup_skill_count = len(skills)
        raw_skill_count = count_skill_files(skills_dir)
        if raw_skill_count is None:
            raw_skill_count = load_previous_raw_count(output_dir)
        if raw_skill_count is None:
            raw_skill_count = dedup_skill_count
    else:
        logger.error("No skills source found!")
        exit(1)

    if not skills:
        logger.error("No skills found!")
        exit(1)

    # Load collections
    sources_dir = Path(__file__).parent.parent / "sources"
    collections = load_collections_from_source(sources_dir)
    if not collections:
        collections = load_collections_from_registry(registry_path)
    if collections:
        logger.info(f"Loaded {len(collections)} collections")

    # Build collections index first (so stats can read it)
    build_collections_index(collections, output_dir)

    build_search_index(
        skills,
        output_dir,
        source_name,
        raw_skill_count=raw_skill_count,
        dedup_skill_count=dedup_skill_count,
    )


if __name__ == '__main__':
    main()
