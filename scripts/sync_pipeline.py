#!/usr/bin/env python3
# ruff: noqa: E402
"""Source sync and registry build helpers."""

import json
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from discover_by_topic import GitHubTopicDiscovery
from utils import build_skill_key, iter_source_skills

from crawler.skillsmp_sync import SkillsMPSync


from sync_download import download_skills
from sync_pipeline_support import _source_count, logger

def sync_skillsmp(output_path: str, max_skills: int = 50000, keep_on_empty: bool = True) -> int:
    """Sync skills from SkillsMP."""
    logger.info("=" * 60)
    logger.info("STEP 1: Syncing from SkillsMP.com")
    logger.info("=" * 60)

    output_file = Path(output_path)
    existing_count = _source_count(output_file) if output_file.exists() else 0

    syncer = SkillsMPSync()
    skills = syncer.sync(max_skills=max_skills)
    synced_count = len(skills)

    # Guardrail: avoid replacing a known non-empty source with empty output.
    if keep_on_empty and synced_count == 0 and existing_count > 0:
        logger.warning(
            "SkillsMP sync returned 0; keeping existing source file "
            f"({existing_count} skills) at {output_path}."
        )
        return existing_count

    syncer.save(output_path)

    logger.info(f"Synced {synced_count} skills to {output_path}")
    return synced_count


def sync_github_discovery(
    output_dir: str,
    output_json: str,
    token: str = "",
    max_repos: int = 0,
    max_topic_pages: int = 10,
    max_code_pages: int = 10,
    skip_code_search: bool = False,
    request_delay: float = 2.0,
) -> int:
    """Refresh discovered source via GitHub topics + code search."""
    logger.info("=" * 60)
    logger.info("STEP 1B: Syncing from GitHub discovery")
    logger.info("=" * 60)

    effective_skip_code_search = bool(skip_code_search)
    if not token and not effective_skip_code_search:
        logger.warning(
            "No GITHUB_TOKEN provided for GitHub discovery; "
            "forcing skip_code_search to avoid repeated 401 errors."
        )
        effective_skip_code_search = True

    discoverer = GitHubTopicDiscovery(
        token=token or None,
        max_repos=max_repos,
        max_topic_pages=max_topic_pages,
        max_code_pages=max_code_pages,
        skip_code_search=effective_skip_code_search,
        request_delay=request_delay,
    )
    skills = discoverer.run(output_dir=output_dir, output_json=output_json)
    logger.info(f"GitHub discovery synced {len(skills)} skills to {output_json}")
    return len(skills)


def build_unified_registry(
    sources_dir: Path,
    output_path: Path,
    include_skillsmp: bool = False,
) -> int:
    """Build unified registry from all sources."""
    logger.info("=" * 60)
    logger.info("STEP 2: Building unified registry")
    logger.info("=" * 60)

    all_skills = []
    seen = set()

    for source_file in sources_dir.glob("*.json"):
        if not include_skillsmp and source_file.name == "skillsmp.json":
            logger.info("Skipping skillsmp.json (SkillsMP source disabled)")
            continue
        logger.info(f"Loading {source_file.name}...")
        with open(source_file) as f:
            source = json.load(f)

        source_name = source.get("name", source_file.stem)

        for skill in iter_source_skills(source):
            # Create unique key
            repo = skill.get("repo", "")
            name = skill.get("name", "")
            path = skill.get("path", "")
            if isinstance(path, str) and path.strip().strip("/") == ".":
                path = ""
            key = build_skill_key(
                repo,
                path,
                name=name,
                category=skill.get("category", "development"),
            )

            if key in seen:
                continue
            seen.add(key)

            all_skills.append({
                "name": name,
                "description": skill.get("description", ""),
                "repo": repo,
                "path": path,
                "category": skill.get("category", "development"),
                "tags": skill.get("tags", []),
                "stars": skill.get("stars", 0),
                "source": source_name,
                "featured": skill.get("featured", False),
            })

    # Sort by stars (descending) then name
    all_skills.sort(key=lambda x: (-x.get("stars", 0), x["name"].lower()))

    registry = {
        "version": "2.0.0",
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_count": len(all_skills),
        "skills": all_skills,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, indent=2, ensure_ascii=False)

    logger.info(f"Built registry with {len(all_skills)} unique skills")
    return len(all_skills)

def should_fail_on_empty_download(stats: dict) -> bool:
    """Return True when the download pass failed on an empty archive."""
    downloaded = int(stats.get("downloaded", 0))
    failed = int(stats.get("failed", 0))
    skipped = int(stats.get("skipped", 0))
    return downloaded == 0 and failed > 0 and skipped == 0
