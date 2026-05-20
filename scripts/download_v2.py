#!/usr/bin/env python3
"""
Skill Downloader v2.0 - Category-based organization with smart conflict resolution

Directory structure:
    skills/{category}/{skill-name}/SKILL.md

Conflict resolution (Option A):
    - First skill with a name gets the simple name
    - Conflicts get repo suffix: {name}-{owner}-{repo}
    - Priority: official (anthropics) > higher stars > first-come

Example:
    skills/
    ├── documents/
    │   ├── pdf/                              # First one
    │   └── pdf-other-owner-other-repo/       # Conflict
    ├── development/
    │   ├── doc-sync/                         # Highest stars
    │   └── doc-sync-rjmurillo-ai-agents/     # Lower stars
"""

import asyncio
import json
import logging
import os
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import aiohttp
from utils import (
    build_legal_metadata,
    build_skill_key,
    ensure_unique_dir,
    get_repo_suffix,
    iter_source_skills,
    normalize_category,
    normalize_name,
    short_hash,
)

# Configuration
MAX_CONCURRENT = 50
TIMEOUT = 15
RETRY_ATTEMPTS = 2
BATCH_SIZE = 200

GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")

# Official repos get priority
OFFICIAL_REPOS = {"anthropics/skills", "anthropics/claude-code"}

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('download_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def load_source_skills(sources_dir: Path) -> List[dict]:
    """Load source rows, preserving source-level defaults such as top-level repo."""
    skills: List[dict] = []
    if not sources_dir.exists():
        return skills
    for source_file in sources_dir.glob("*.json"):
        try:
            with open(source_file, 'r') as f:
                data = json.load(f)
            skills.extend(iter_source_skills(data))
        except Exception as e:
            logger.warning(f"Failed to load {source_file}: {e}")
    return skills


class SkillRegistry:
    """Track downloaded skills to handle conflicts."""

    def __init__(self, skills_dir: Path):
        self.skills_dir = skills_dir
        # {category: {base_name: {dir_name: skill_info}}}
        self.registry: Dict[str, Dict[str, Dict[str, dict]]] = defaultdict(lambda: defaultdict(dict))
        self._scan_existing()

    def _scan_existing(self):
        """Scan existing skills directory."""
        if not self.skills_dir.exists():
            return

        for category_dir in self.skills_dir.iterdir():
            if not category_dir.is_dir() or category_dir.name.startswith('.'):
                continue

            category = category_dir.name

            for skill_dir in category_dir.iterdir():
                if not skill_dir.is_dir():
                    continue

                skill_md = skill_dir / "SKILL.md"
                metadata_file = skill_dir / "metadata.json"

                if not skill_md.exists():
                    continue

                dir_name = skill_dir.name

                # Extract base name (remove repo suffix if present)
                # e.g., "doc-sync-owner-repo" -> "doc-sync"
                base_name = self._extract_base_name(dir_name, metadata_file)

                # Load metadata
                metadata = {}
                if metadata_file.exists():
                    try:
                        metadata = json.loads(metadata_file.read_text())
                    except Exception:
                        pass

                self.registry[category][base_name][dir_name] = {
                    "repo": metadata.get("repo", ""),
                    "stars": metadata.get("stars", 0),
                    "path": str(skill_dir),
                }

        logger.info(f"Scanned existing skills: {sum(len(names) for names in self.registry.values())} unique names")

    def _extract_base_name(self, dir_name: str, metadata_file: Path) -> str:
        """Extract base name from directory name."""
        if metadata_file.exists():
            try:
                metadata = json.loads(metadata_file.read_text())
                if metadata.get("name"):
                    return normalize_name(metadata["name"])
                repo = metadata.get("repo", "")
                suffix = get_repo_suffix(repo)
                if suffix and dir_name.endswith(f"-{suffix}"):
                    return dir_name[: -(len(suffix) + 1)]
            except Exception:
                pass

        return dir_name

    def get_dir_name(self, name: str, repo: str, category: str, stars: int) -> str:
        """
        Determine directory name for a skill, handling conflicts.

        Returns the directory name to use (may include repo suffix).
        """
        base_name = normalize_name(name)
        category = normalize_name(category) or "other"

        existing = self.registry[category].get(base_name, {})

        if not existing:
            # No conflict - use simple name
            return base_name

        # Check if this exact repo already downloaded
        for dir_name, info in existing.items():
            if info.get("repo") == repo:
                return dir_name  # Already exists

        # Conflict! Determine if this skill should get the base name
        # Priority: official > higher stars > existing keeps base name

        is_official = repo in OFFICIAL_REPOS

        # Check if any existing has the base name
        if base_name in existing:
            existing_info = existing[base_name]
            existing_is_official = existing_info.get("repo") in OFFICIAL_REPOS
            existing_stars = existing_info.get("stars", 0)

            # Should this new skill take over the base name?
            should_take_base = False

            if is_official and not existing_is_official:
                should_take_base = True
            elif not existing_is_official and not is_official and stars > existing_stars:
                should_take_base = True

            if should_take_base:
                # Rename existing to have suffix
                old_path = Path(existing_info["path"])
                existing_suffix = get_repo_suffix(existing_info.get("repo", ""))
                if not existing_suffix:
                    existing_suffix = short_hash(existing_info.get("repo", "") or base_name)
                new_dir_name = f"{base_name}-{existing_suffix}"
                new_path = old_path.parent / new_dir_name

                if old_path.exists() and not new_path.exists():
                    old_path.rename(new_path)
                    logger.info(f"Renamed {base_name} -> {new_dir_name} (priority override)")

                    # Update registry
                    self.registry[category][base_name][new_dir_name] = existing_info
                    self.registry[category][base_name][new_dir_name]["path"] = str(new_path)
                    del self.registry[category][base_name][base_name]

                return base_name  # New skill gets base name

        # This skill gets a suffix
        suffix = get_repo_suffix(repo) or short_hash(repo or base_name)
        return f"{base_name}-{suffix}"

    def register(self, name: str, repo: str, category: str, stars: int, dir_name: str, path: Path):
        """Register a downloaded skill."""
        base_name = normalize_name(name)
        category = normalize_name(category) or "other"

        self.registry[category][base_name][dir_name] = {
            "repo": repo,
            "stars": stars,
            "path": str(path),
        }


def get_url_patterns(repo: str, skill_name: str, skill_path: str = "") -> List[str]:
    """Generate URL patterns to try for downloading SKILL.md."""
    patterns = []
    branches = ["main", "master"]

    # If explicit path provided, try it first
    if skill_path:
        for branch in branches:
            if skill_path.endswith("SKILL.md"):
                patterns.append(f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_path}")
            else:
                patterns.append(f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_path}/SKILL.md")

    for branch in branches:
        # Standard Claude Code locations
        patterns.extend([
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/skills/{skill_name}/SKILL.md",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/{skill_name}/SKILL.md",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/.claude/SKILL.md",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/skills/{skill_name}/SKILL.md",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/{skill_name}/SKILL.md",
            f"{GITHUB_RAW_BASE}/{repo}/{branch}/SKILL.md",
        ])

    # Remove duplicates while preserving order
    seen = set()
    return [p for p in patterns if not (p in seen or seen.add(p))]


async def fetch_url(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Tuple[Optional[str], int]:
    """Fetch URL with status code."""
    async with semaphore:
        for attempt in range(RETRY_ATTEMPTS):
            try:
                async with session.get(url, timeout=aiohttp.ClientTimeout(total=TIMEOUT)) as resp:
                    if resp.status == 200:
                        return await resp.text(), 200
                    elif resp.status == 404:
                        return None, 404
                    elif resp.status in (403, 429):
                        await asyncio.sleep(2 ** attempt)
                        continue
                    return None, resp.status
            except Exception:
                if attempt < RETRY_ATTEMPTS - 1:
                    await asyncio.sleep(0.5)
        return None, -1


def is_valid_skill_content(content: str) -> bool:
    """Validate that content is a proper SKILL.md file."""
    if not content or len(content) < 50:
        return False

    indicators = [
        content.strip().startswith("---"),
        "description:" in content[:500].lower(),
        "# " in content[:200],
        "skill" in content[:500].lower(),
    ]
    return any(indicators)


async def download_skill(
    session: aiohttp.ClientSession,
    skill: dict,
    skills_dir: Path,
    registry: SkillRegistry,
    semaphore: asyncio.Semaphore,
    stats: dict,
) -> bool:
    """Download a single skill with conflict resolution."""

    name = skill.get("name", "")
    repo = skill.get("repo", "")
    path = skill.get("path", "")
    category = skill.get("category", "other")
    stars = skill.get("stars", 0)

    if not name or not repo:
        stats["skipped"] += 1
        return False

    # Clean repo path
    repo = repo.split("/tree/")[0]
    if repo.startswith("https://github.com/"):
        repo = repo.replace("https://github.com/", "")
    repo = repo.rstrip("/")

    # Get directory name (handles conflicts)
    category_normalized = normalize_category(category) or "other"
    dir_name = registry.get_dir_name(name, repo, category_normalized, stars)

    key = build_skill_key(repo, path, name=name, category=category_normalized)
    case_safe_dir = ensure_unique_dir(skills_dir / category_normalized, dir_name, key, repo=repo)

    # Target path (case-safe)
    dir_name = case_safe_dir.name
    skill_dir = case_safe_dir
    skill_file = skill_dir / "SKILL.md"

    # Already exists?
    if skill_file.exists():
        stats["skipped"] += 1
        return False

    # Try to download
    patterns = get_url_patterns(repo, normalize_name(name), path)

    for url in patterns[:8]:
        content, status = await fetch_url(session, url, semaphore)

        if content and is_valid_skill_content(content):
            # Extract github_path from URL
            github_path = ""
            github_branch = "main"
            try:
                url_parts = url.replace(GITHUB_RAW_BASE + "/", "").split("/")
                if len(url_parts) > 3:
                    github_branch = url_parts[2]
                    github_path = "/".join(url_parts[3:])
                    if github_path.endswith("/SKILL.md"):
                        github_path = github_path[:-9]
                    elif github_path == "SKILL.md":
                        github_path = ""
            except Exception:
                pass

            # Create directory and save
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_file.write_text(content, encoding="utf-8")

            # Save metadata
            legal_meta = build_legal_metadata(
                repo=repo,
                path=github_path or path,
                branch=github_branch,
                source_url=skill.get("source_url", ""),
                author=skill.get("author", ""),
                license_name=skill.get("license", ""),
                copyright_text=skill.get("copyright", ""),
                permission_note=skill.get("permission_note", ""),
                distribution=skill.get("distribution", ""),
            )
            metadata = {
                "name": name,
                "description": skill.get("description", "")[:200],
                "repo": repo,
                "category": category,
                "tags": skill.get("tags", []),
                "stars": stars,
                "source": skill.get("source", ""),
                "github_path": github_path,
                "github_branch": github_branch,
                "dir_name": dir_name,
                "downloaded_at": datetime.utcnow().isoformat() + "Z",
                **legal_meta,
            }
            (skill_dir / "metadata.json").write_text(
                json.dumps(metadata, indent=2, ensure_ascii=False),
                encoding="utf-8"
            )

            # Register
            registry.register(name, repo, category_normalized, stars, dir_name, skill_dir)

            stats["downloaded"] += 1
            return True

        if status == 403:
            stats["rate_limited"] += 1
            return False

    stats["not_found"] += 1
    return False


async def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    registry_dir = script_dir.parent
    skills_dir = registry_dir / "skills"

    # Load skills from sources
    skills = []

    # Load from registry.json
    registry_file = registry_dir / "registry.json"
    if registry_file.exists():
        with open(registry_file, 'r') as f:
            data = json.load(f)
            skills.extend(data.get("skills", []))

    # Load from sources
    sources_dir = registry_dir / "sources"
    skills.extend(load_source_skills(sources_dir))

    # Deduplicate by repo+name
    seen = set()
    unique_skills = []
    for s in skills:
        key = f"{s.get('repo', '')}:{s.get('name', '')}"
        if key not in seen:
            seen.add(key)
            unique_skills.append(s)

    # Sort by stars (download high-star skills first for priority)
    unique_skills.sort(key=lambda x: x.get("stars", 0), reverse=True)

    logger.info(f"Total skills to process: {len(unique_skills)}")

    # Initialize registry
    registry = SkillRegistry(skills_dir)

    # Stats
    stats = {
        "downloaded": 0,
        "skipped": 0,
        "not_found": 0,
        "rate_limited": 0,
    }

    # Headers
    headers = {"User-Agent": "Claude-Skills-Registry/2.0"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"
        logger.info("Using GitHub token")

    # Download
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT * 2)

    start_time = time.time()

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for i in range(0, len(unique_skills), BATCH_SIZE):
            batch = unique_skills[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(unique_skills) + BATCH_SIZE - 1) // BATCH_SIZE

            logger.info(f"Batch {batch_num}/{total_batches} ({len(batch)} skills)")

            tasks = [
                download_skill(session, skill, skills_dir, registry, semaphore, stats)
                for skill in batch
            ]

            await asyncio.gather(*tasks, return_exceptions=True)

            elapsed = time.time() - start_time
            rate = (stats["downloaded"] + stats["skipped"]) / elapsed if elapsed > 0 else 0

            logger.info(
                f"Progress: ✅ {stats['downloaded']} | ⏭️ {stats['skipped']} | "
                f"❌ {stats['not_found']} | ⚡ {rate:.1f}/s"
            )

            await asyncio.sleep(0.3)

    # Summary
    elapsed = time.time() - start_time
    print()
    print("=" * 60)
    print("DOWNLOAD COMPLETE")
    print("=" * 60)
    print(f"  Downloaded:    {stats['downloaded']}")
    print(f"  Skipped:       {stats['skipped']}")
    print(f"  Not found:     {stats['not_found']}")
    print(f"  Rate limited:  {stats['rate_limited']}")
    print(f"  Time:          {elapsed:.1f}s")
    print("=" * 60)

    # Count final skills
    total = sum(1 for _ in skills_dir.rglob("SKILL.md"))
    print(f"  Total skills:  {total}")


if __name__ == "__main__":
    asyncio.run(main())
