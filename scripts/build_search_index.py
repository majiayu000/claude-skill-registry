#!/usr/bin/env python3
"""
Build Search Index v2.0 - Generate lightweight search index.

Primary source is the archived skills tree, scanned recursively:
- <archive-root>/**/SKILL.md

Output files:
- search-index.json - Compatibility pointer to search shard manifest
- search-index-manifest.json + search-shards/*.json - Full search records
- categories/index.json + categories/<category>/manifest.json - Category parts
- featured.json - Top 100 skills by stars
- stats.json - Explicit raw/indexed/deduplicated counters
"""

import argparse
import base64
import gzip
import hashlib
import json
import logging
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from index_artifacts import write_category_artifacts, write_search_artifacts
from plugin_index import build_plugins_index, load_plugins_from_registry, load_plugins_from_source
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

# First-paint catalog index used by the static Pages app. Full search shards
# remain available through search-index.json as a compatibility pointer.
LITE_INDEX_LIMIT = 5000


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


def get_stable_id(install: str, branch: str) -> str:
    """Build a stable URL-safe skill id from install path and branch."""
    key = f"{install}|{branch or 'main'}".encode("utf-8")
    digest = hashlib.sha256(key).digest()
    return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=").lower()


def infer_install_status(repo: str, path: str, install: str) -> str:
    """Classify whether the install path is clearly usable from registry metadata."""
    if not install:
        return "broken"
    if install.startswith("local/"):
        return "unknown"
    if repo and path:
        return "known_good"
    if repo:
        return "unknown"
    return "risky"


def infer_security_status(skill: Dict[str, Any]) -> str:
    """Return per-skill security status when available; otherwise unknown."""
    status = skill.get("security_status") or skill.get("security")
    if isinstance(status, str):
        normalized = status.lower()
        if normalized in {"passed", "failed", "unknown"}:
            return normalized
    return "unknown"


def infer_compatible_agents(skill: Dict[str, Any]) -> List[str]:
    """Infer a conservative compatible-agent hint from metadata and path."""
    haystack = " ".join(
        str(part)
        for part in [
            skill.get("name", ""),
            skill.get("description", ""),
            skill.get("repo", ""),
            skill.get("path", ""),
            " ".join(skill.get("tags", []) or []),
        ]
        if part
    ).lower()
    agents = []
    if ".claude/" in haystack or "/skills/" in haystack or "claude" in haystack:
        agents.append("Claude Code")
    if "codex" in haystack:
        agents.append("Codex CLI")
    if "gemini" in haystack:
        agents.append("Gemini CLI")
    if "cursor" in haystack:
        agents.append("Cursor")
    return agents[:5]


def score_skill_quality(skill: Dict[str, Any], install_status: str, security_status: str) -> Dict[str, Any]:
    """Compute a transparent first-pass quality score from existing metadata."""
    description = str(skill.get("description", "") or "")
    repo = str(skill.get("repo", "") or "")
    path = str(skill.get("path", "") or "")
    tags = skill.get("tags", []) or []
    stars = int(skill.get("stars", 0) or 0)

    components = {
        "description": 20 if len(description) >= 80 else 12 if len(description) >= 30 else 4,
        "repo": 15 if repo and "/" in repo else 0,
        "path": 15 if path else 0,
        "tags": 10 if len(tags) >= 3 else 6 if tags else 0,
        "install": 20 if install_status == "known_good" else 8 if install_status == "unknown" else 0,
        "security": 10 if security_status == "passed" else 4 if security_status == "unknown" else 0,
        "popularity": 10 if stars >= 1000 else 6 if stars >= 100 else 3 if stars > 0 else 0,
    }
    score = sum(components.values())
    if install_status in {"broken", "risky"}:
        score = min(score, 45)
    if security_status == "failed":
        score = min(score, 50)

    if security_status == "failed" or install_status == "broken":
        grade = "blocked"
    elif score >= 85:
        grade = "S"
    elif score >= 70:
        grade = "A"
    elif score >= 55:
        grade = "B"
    elif score >= 40:
        grade = "C"
    else:
        grade = "unknown"

    return {
        "quality_score": score,
        "quality_grade": grade,
        "score_inputs": components,
    }


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
    lite_skills_by_key: Dict[str, Dict[str, Any]] = {}
    quality_records_by_id: Dict[str, Dict[str, Any]] = {}
    security_records_by_id: Dict[str, Dict[str, Any]] = {}
    ranking_records_by_id: Dict[str, Dict[str, Any]] = {}

    for skill in skills:
        name = skill.get('name', '')
        description = skill.get('description', '')
        category = skill.get('category', 'other')
        tags = skill.get('tags', [])
        stars = skill.get('stars', 0)
        repo = skill.get('repo', '')
        install = skill.get('install', repo)
        branch = skill.get('branch', 'main')
        path = skill.get('path', '')
        skill_id = get_stable_id(install, branch)
        owner = repo.split("/", 1)[0] if "/" in repo else ""
        install_status = infer_install_status(repo, path, install)
        security_status = infer_security_status(skill)
        compatible_agents = infer_compatible_agents(skill)
        quality = score_skill_quality(skill, install_status, security_status)
        quality_score = quality["quality_score"]
        quality_grade = quality["quality_grade"]
        trust_score = min(
            100,
            (30 if repo and "/" in repo else 0)
            + (25 if path else 0)
            + (20 if install_status == "known_good" else 8 if install_status == "unknown" else 0)
            + (15 if security_status != "failed" else 0)
            + (10 if stars > 0 else 0),
        )

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
            "path": path,
            "branch": branch,
            "category": category,
            "tags": tags[:10] if tags else [],
            "stars": stars,
            "install": install,
            "source": skill.get('source', ''),
            "id": skill_id,
            "owner": owner,
            "quality_grade": quality_grade,
            "quality_score": quality_score,
            "security_status": security_status,
            "install_status": install_status,
            "trust_score": trust_score,
            "compatible_agents": compatible_agents,
        }

        # Add to category
        if category not in categories:
            categories[category] = []
        categories[category].append(full_record)

        # Track for featured
        if stars > 0:
            featured_skills.append(full_record)

        lite_record = {
            "id": skill_id,
            "name": name,
            "description": truncate_text(description, 180),
            "category": category,
            "tags": tags[:8] if tags else [],
            "repo": repo,
            "owner": owner,
            "path": path,
            "install": install,
            "branch": branch,
            "stars": stars,
            "source": skill.get("source", ""),
            "quality_grade": quality_grade,
            "security_status": security_status,
            "install_status": install_status,
            "quality_score": quality_score,
            "trust_score": trust_score,
            "compatible_agents": compatible_agents,
            "_description_length": len(description),
        }
        dedupe_key = f"{install}|{branch}"
        existing = lite_skills_by_key.get(dedupe_key)
        if not existing or (
            stars,
            quality_score,
            len(description),
        ) > (
            int(existing.get("stars", 0) or 0),
            int(existing.get("quality_score", 0) or 0),
            int(existing.get("_description_length", 0) or 0),
        ):
            lite_skills_by_key[dedupe_key] = lite_record
            quality_records_by_id[skill_id] = {
                "id": skill_id,
                "install": install,
                "branch": branch,
                "quality_grade": quality_grade,
                "quality_score": quality_score,
                "score_inputs": quality["score_inputs"],
            }
            security_records_by_id[skill_id] = {
                "id": skill_id,
                "install": install,
                "branch": branch,
                "security_status": security_status,
                "install_status": install_status,
            }
            ranking_records_by_id[skill_id] = {
                "id": skill_id,
                "install": install,
                "branch": branch,
                "stars": stars,
                "quality_score": quality_score,
                "trust_score": trust_score,
                "recommended_score": round(
                    quality_score * 0.45
                    + trust_score * 0.30
                    + min(100, stars ** 0.5) * 0.25,
                    2,
                ),
            }

    # Sort by stars
    search_index["s"].sort(key=lambda x: x.get("r", 0), reverse=True)
    featured_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)
    featured_skills = featured_skills[:100]
    all_lite_skills = sorted(
        lite_skills_by_key.values(),
        key=lambda x: (
            x.get("quality_score", 0),
            x.get("trust_score", 0),
            x.get("stars", 0),
        ),
        reverse=True,
    )
    all_lite_skills = [
        {key: value for key, value in skill.items() if not key.startswith("_")}
        for skill in all_lite_skills
    ]
    lite_skills = all_lite_skills[:LITE_INDEX_LIMIT]
    ranking_records = sorted(
        ranking_records_by_id.values(),
        key=lambda x: x.get("recommended_score", 0),
        reverse=True,
    )

    # Create output directories
    output_dir.mkdir(parents=True, exist_ok=True)
    categories_dir = output_dir / "categories"
    categories_dir.mkdir(exist_ok=True)

    search_artifacts = write_search_artifacts(
        search_index["s"],
        output_dir,
        version=search_index["v"],
        updated_at=utc_now_isoformat(),
    )
    logger.info(
        f"  search-index.json pointer: {search_artifacts.index_size_bytes / 1024 / 1024:.2f} MB"
    )
    logger.info(
        f"  search shards: {search_artifacts.shard_count} "
        f"(largest {search_artifacts.largest_shard_bytes / 1024 / 1024:.2f} MB)"
    )

    # Write SkillHub Plus lite and scoring indexes.
    lite_index = {
        "version": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "updated_at": utc_now_isoformat(),
        "total_count": len(all_lite_skills),
        "included_count": len(lite_skills),
        "limit": LITE_INDEX_LIMIT,
        "raw_count": len(skills),
        "dedupe_key": "install|branch",
        "skills": lite_skills,
    }
    search_index_lite_path = output_dir / "search-index-lite.json"
    with open(search_index_lite_path, "w", encoding="utf-8") as f:
        json.dump(lite_index, f, ensure_ascii=False, separators=(",", ":"))

    search_index_lite_gz_path = output_dir / "search-index-lite.json.gz"
    with gzip.open(search_index_lite_gz_path, "wt", encoding="utf-8") as f:
        json.dump(lite_index, f, ensure_ascii=False, separators=(",", ":"))

    quality_index_path = output_dir / "quality-index.json"
    with open(quality_index_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "updated_at": utc_now_isoformat(),
                "count": len(quality_records_by_id),
                "records": list(quality_records_by_id.values()),
            },
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    security_index_path = output_dir / "security-index.json"
    with open(security_index_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "updated_at": utc_now_isoformat(),
                "count": len(security_records_by_id),
                "records": list(security_records_by_id.values()),
            },
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    ranking_index_path = output_dir / "ranking-index.json"
    with open(ranking_index_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "updated_at": utc_now_isoformat(),
                "count": len(ranking_records),
                "records": ranking_records,
            },
            f,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    logger.info(
        f"  search-index-lite.json: {search_index_lite_path.stat().st_size / 1024 / 1024:.2f} MB"
    )
    logger.info(f"  quality-index.json: {quality_index_path.stat().st_size / 1024 / 1024:.2f} MB")
    logger.info(f"  security-index.json: {security_index_path.stat().st_size / 1024 / 1024:.2f} MB")
    logger.info(f"  ranking-index.json: {ranking_index_path.stat().st_size / 1024 / 1024:.2f} MB")

    category_artifacts = write_category_artifacts(
        categories,
        categories_dir,
        updated_at=utc_now_isoformat(),
        category_code=get_category_code,
    )
    for category in category_artifacts.categories:
        logger.info(
            f"  {category['manifest']}: {category['count']} skills in "
            f"{category['part_count']} part(s)"
        )

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
    repo_counts: Counter[str] = Counter()
    for record in search_index["s"]:
        install = str(record.get("i") or "")
        parts = install.split("/")
        repo = f"{parts[0]}/{parts[1]}" if len(parts) >= 2 else install
        if repo:
            repo_counts[repo] += 1

    category_counts = [
        {
            "name": category["name"],
            "code": category["code"],
            "count": category["count"],
        }
        for category in category_artifacts.categories
    ]
    official_skill_count = sum(
        category["count"] for category in category_counts if category["code"] == "off"
    )

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
        "category_counts": category_counts,
        "unique_repo_count": len(repo_counts),
        "official_skill_count": official_skill_count,
        "top_repositories": [
            {"repo": repo, "count": count}
            for repo, count in repo_counts.most_common(10)
        ],
        "featured_count": len(featured_skills),
        "index_size_bytes": search_artifacts.index_size_bytes,
        "index_size_gzip_bytes": search_artifacts.index_size_gzip_bytes,
        "search_shard_count": search_artifacts.shard_count,
        "search_largest_shard_bytes": search_artifacts.largest_shard_bytes,
        "search_largest_shard_gzip_bytes": search_artifacts.largest_shard_gzip_bytes,
        "category_shard_count": category_artifacts.shard_count,
        "category_largest_part_bytes": category_artifacts.largest_part_bytes,
        "category_largest_part_gzip_bytes": category_artifacts.largest_part_gzip_bytes,
        "lite_index_count": len(all_lite_skills),
        "lite_index_included_count": len(lite_skills),
        "lite_index_size_bytes": search_index_lite_path.stat().st_size,
        "lite_index_gzip_size_bytes": search_index_lite_gz_path.stat().st_size,
        "quality_index_size_bytes": quality_index_path.stat().st_size,
        "security_index_size_bytes": security_index_path.stat().st_size,
        "ranking_index_size_bytes": ranking_index_path.stat().st_size,
        "largest_generated_file_bytes": max(
            search_artifacts.largest_shard_bytes,
            category_artifacts.largest_part_bytes,
            search_index_lite_path.stat().st_size,
            search_index_lite_gz_path.stat().st_size,
            quality_index_path.stat().st_size,
            security_index_path.stat().st_size,
            ranking_index_path.stat().st_size,
            (output_dir / "featured.json").stat().st_size,
        ),
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
    logger.info(f"  Lite index count: {len(lite_skills)} / {len(all_lite_skills)}")
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
    build_plugins_index(plugins, output_dir, updated_at=utc_now_isoformat())
    if plugins:
        logger.info(f"  plugins.json: {len(plugins)} plugins")

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
