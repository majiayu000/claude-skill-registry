#!/usr/bin/env python3
"""
Build Search Index v2.0 - Generate lightweight search index.

Primary source is the archived skills tree, scanned recursively:
- <archive-root>/**/SKILL.md

Output files:
- search-index.json - Minimal index (~1-2MB gzip)
- categories/*.json - Category-based indexes
- featured.json - Top 100 skills by stars
- stats.json - Explicit raw/indexed/deduplicated counters
"""

import argparse
import gzip
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils import extract_description, get_repo_suffix, load_metadata

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


def utc_now_isoformat() -> str:
    """Return a stable UTC timestamp with trailing Z."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


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
    """Recursively scan archive root and index one entry per SKILL.md file."""
    skills = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    for skill_md in skills_dir.rglob("SKILL.md"):
        skill_dir = skill_md.parent
        rel_parts = skill_dir.relative_to(skills_dir).parts
        category_name = rel_parts[0] if rel_parts else "other"
        metadata = load_metadata(skill_dir)
        dir_name = skill_dir.name

        # Get skill name (from metadata or directory)
        name = metadata.get("name") or dir_name

        # Remove repo suffix from dir_name if metadata repo is available
        if name == dir_name:
            repo_for_suffix = metadata.get("repo", "")
            suffix = get_repo_suffix(repo_for_suffix)
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

        if github_path and repo:
            install = f"{repo}/{github_path}"
        elif repo:
            install = repo
        else:
            install = f"local/{'/'.join(rel_parts)}" if rel_parts else f"local/{name}"

        tags = metadata.get("tags", [])
        if not isinstance(tags, list):
            tags = []

        stars = metadata.get("stars", 0)
        try:
            stars = int(stars)
        except (TypeError, ValueError):
            stars = 0

        skill_entry = {
            "name": name,
            "dir_name": dir_name,
            "description": description,
            "repo": repo,
            "path": github_path,
            "branch": github_branch,
            "category": category,
            "tags": tags,
            "stars": stars,
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

    total = registry.get("registry_skill_count_dedup")
    if isinstance(total, int):
        return total

    total = registry.get("total_count")
    if isinstance(total, int):
        return total

    skills = registry.get("skills")
    if isinstance(skills, list):
        return len(skills)

    return None


def count_named_files(skills_dir: Path, filename: str) -> Optional[int]:
    """Count matching files recursively without full metadata parsing."""
    if not skills_dir.exists():
        return None
    try:
        return sum(1 for _ in skills_dir.rglob(filename))
    except Exception:
        return None


def build_search_index(
    skills: List[Dict],
    output_dir: Path,
    source_name: str = "skills",
    archive_skill_md_count_raw: Optional[int] = None,
    archive_metadata_count_raw: Optional[int] = None,
    registry_skill_count_dedup: Optional[int] = None,
) -> Dict[str, Any]:
    """Build the lightweight search index."""
    logger.info(f"Building index from {len(skills)} {source_name}...")

    # Build minimal search index
    search_index = {
        "v": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
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
        "updated_at": utc_now_isoformat(),
        "categories": []
    }

    for category, cat_skills in sorted(categories.items()):
        cat_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)

        cat_data = {
            "category": category,
            "code": get_category_code(category),
            "count": len(cat_skills),
            "updated_at": utc_now_isoformat(),
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
        "updated_at": utc_now_isoformat(),
        "count": len(featured_skills),
        "skills": featured_skills
    }
    with open(output_dir / "featured.json", 'w', encoding='utf-8') as f:
        json.dump(featured_data, f, ensure_ascii=False, indent=2)

    logger.info(f"  featured.json: {len(featured_skills)} skills")

    # Write stats
    plugins_count_path = output_dir / "plugins.json"
    plugin_count = 0
    if plugins_count_path.exists():
        try:
            with open(plugins_count_path, 'r', encoding='utf-8') as f:
                plugin_count = json.load(f).get("count", 0)
        except Exception:
            pass

    indexed_skill_count_scan_shape = len(skills)
    stats = {
        "updated_at": utc_now_isoformat(),
        "archive_skill_md_count_raw": archive_skill_md_count_raw,
        "archive_metadata_count_raw": archive_metadata_count_raw,
        "indexed_skill_count_scan_shape": indexed_skill_count_scan_shape,
        "registry_skill_count_dedup": registry_skill_count_dedup,
        "total_plugins": plugin_count,
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

    logger.info("\nIndex build complete!")
    logger.info(f"  Indexed skills: {indexed_skill_count_scan_shape}")
    if archive_skill_md_count_raw is not None:
        logger.info(f"  Archive SKILL.md count (raw): {archive_skill_md_count_raw}")
    if archive_metadata_count_raw is not None:
        logger.info(f"  Archive metadata.json count (raw): {archive_metadata_count_raw}")
    if registry_skill_count_dedup is not None:
        logger.info(f"  Registry deduplicated count: {registry_skill_count_dedup}")
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
        name = skill.get('name', 'unknown')
        if repo and path:
            skill['install'] = f"{repo}/{path}"
        elif repo:
            skill['install'] = repo
        elif path:
            skill['install'] = f"local/{path}"
        else:
            skill['install'] = f"local/{name}"

    return skills


def load_plugins_from_registry(registry_path: Path) -> List[Dict]:
    """Load plugins from registry.json."""
    if not registry_path.exists():
        return []
    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        return registry.get('plugins', [])
    except Exception:
        return []


def load_plugins_from_source(sources_dir: Path) -> List[Dict]:
    """Load plugins from sources/plugins.json."""
    plugins_path = sources_dir / "plugins.json"
    if not plugins_path.exists():
        return []
    try:
        with open(plugins_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('plugins', [])
    except Exception:
        return []


def build_plugins_index(
    plugins: List[Dict],
    output_dir: Path,
) -> None:
    """Write plugins.json to output directory."""
    if not plugins:
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    plugins_data = {
        "updated_at": utc_now_isoformat(),
        "count": len(plugins),
        "plugins": plugins,
    }
    with open(output_dir / "plugins.json", 'w', encoding='utf-8') as f:
        json.dump(plugins_data, f, ensure_ascii=False, indent=2)

    logger.info(f"  plugins.json: {len(plugins)} plugins")


def main():
    parser = argparse.ArgumentParser(description='Build search index for skill registry')
    parser.add_argument('--skills-dir', '-s', default='skills', help='Skills directory')
    parser.add_argument('--registry', '-r', default='registry.json', help='Registry.json (fallback)')
    parser.add_argument('--output', '-o', default='docs', help='Output directory')
    parser.add_argument(
        '--use-registry',
        action='store_true',
        help='Fallback to registry.json only when skills dir is unavailable',
    )

    args = parser.parse_args()

    skills_dir = Path(args.skills_dir)
    registry_path = Path(args.registry)
    output_dir = Path(args.output)

    archive_skill_md_count_raw: Optional[int] = None
    archive_metadata_count_raw: Optional[int] = None
    registry_skill_count_dedup: Optional[int] = None

    # Canonical mode: recursively scan archive tree whenever available.
    if skills_dir.exists():
        logger.info(f"Scanning archive recursively from {skills_dir}")
        if args.use_registry:
            logger.info("Ignoring --use-registry because skills directory exists.")
        skills = scan_skills_v2(skills_dir)
        source_name = "archived skills (recursive)"
        archive_skill_md_count_raw = count_named_files(skills_dir, "SKILL.md")
        archive_metadata_count_raw = count_named_files(skills_dir, "metadata.json")
        registry_skill_count_dedup = load_registry_count(registry_path)
        if registry_skill_count_dedup is None:
            registry_skill_count_dedup = len(skills)
    elif registry_path.exists():
        logger.info(f"Loading from registry: {registry_path}")
        skills = load_from_registry(registry_path)
        source_name = "registry entries"
        registry_skill_count_dedup = len(skills)
    else:
        logger.error("No skills source found!")
        exit(1)

    if not skills:
        logger.error("No skills found!")
        exit(1)

    # Load plugins
    sources_dir = Path(__file__).parent.parent / "sources"
    plugins = load_plugins_from_source(sources_dir)
    if not plugins:
        plugins = load_plugins_from_registry(registry_path)
    if plugins:
        logger.info(f"Loaded {len(plugins)} plugins")

    # Build plugins index first (so stats can read it)
    build_plugins_index(plugins, output_dir)

    build_search_index(
        skills,
        output_dir,
        source_name,
        archive_skill_md_count_raw=archive_skill_md_count_raw,
        archive_metadata_count_raw=archive_metadata_count_raw,
        registry_skill_count_dedup=registry_skill_count_dedup,
    )


if __name__ == '__main__':
    main()
