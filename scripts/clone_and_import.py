#!/usr/bin/env python3
"""
Clone and Import Skills - No GitHub API needed!
Clones awesome-claude-skills repos and imports SKILL.md files.
"""

import json
import logging
import subprocess
from datetime import datetime
from pathlib import Path

from utils import (
    build_legal_metadata,
    build_skill_key,
    ensure_unique_dir,
    extract_frontmatter,
    guess_category,
    normalize_category,
    normalize_name,
    normalize_repo,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

# Repos to clone (no API needed, just git clone)
REPOS_TO_CLONE = [
    # Official
    "https://github.com/anthropics/skills.git",

    # Awesome lists with skills
    "https://github.com/travisvn/awesome-claude-skills.git",
    "https://github.com/ComposioHQ/awesome-claude-skills.git",
    "https://github.com/BehiSecc/awesome-claude-skills.git",
    "https://github.com/VoltAgent/awesome-claude-skills.git",
    "https://github.com/alirezarezvani/claude-skills.git",
    "https://github.com/hesreallyhim/awesome-claude-code.git",
    "https://github.com/karanb192/awesome-claude-skills.git",
    "https://github.com/abubakarsiddik31/claude-skills-collection.git",
    "https://github.com/Chat2AnyLLM/awesome-claude-skills.git",

    # Skill factories
    "https://github.com/alirezarezvani/claude-code-skill-factory.git",

    # Community submissions
    "https://github.com/faceleg/claude-skill-git.git",
    "https://github.com/superlowburn/agentrank.git",
]


def _repo_slug(repo_url: str) -> str:
    repo_url = repo_url.replace(".git", "")
    repo_url = repo_url.replace("https://github.com/", "")
    return normalize_repo(repo_url)


REPO_BY_DIR = {url.split("/")[-1].replace(".git", ""): _repo_slug(url) for url in REPOS_TO_CLONE}

def _parse_skill_frontmatter(content: str) -> dict:
    """Parse YAML frontmatter from SKILL.md using safe_load."""
    fm = extract_frontmatter(content)
    metadata: dict = {}
    for key in ("name", "description", "category"):
        if fm.get(key):
            metadata[key] = str(fm[key])
    if isinstance(fm.get("tags"), list):
        metadata["tags"] = fm["tags"]
    return metadata


def clone_repo(repo_url: str, target_dir: Path) -> bool:
    """Clone a repo using git."""
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    clone_path = target_dir / repo_name

    if clone_path.exists():
        logger.info(f"  Already cloned: {repo_name}")
        return True

    try:
        logger.info(f"  Cloning: {repo_name}")
        subprocess.run(
            ["git", "clone", "--depth", "1", repo_url, str(clone_path)],
            capture_output=True,
            timeout=120,
            check=True
        )
        return True
    except subprocess.TimeoutExpired:
        logger.warning(f"  Timeout cloning {repo_name}")
        return False
    except subprocess.CalledProcessError as e:
        logger.warning(f"  Failed to clone {repo_name}: {e}")
        return False


def find_skill_files(repo_dir: Path) -> list:
    """Find all SKILL.md files in a repo."""
    skills = []

    for skill_file in repo_dir.rglob("SKILL.md"):
        # Skip if in node_modules or .git
        if "node_modules" in str(skill_file) or ".git" in str(skill_file):
            continue

        skills.append(skill_file)

    return skills


def import_skill(skill_file: Path, skills_dir: Path, repo_slug: str, stats: dict) -> bool:
    """Import a single SKILL.md file."""
    try:
        content = skill_file.read_text(encoding="utf-8")
    except Exception as e:
        logger.debug(f"  Failed to read {skill_file}: {e}")
        stats["errors"] += 1
        return False

    # Validate content
    if len(content) < 50:
        stats["skipped"] += 1
        return False

    # Parse frontmatter
    metadata = _parse_skill_frontmatter(content)

    # Determine skill name
    skill_name = metadata.get("name", "")
    if not skill_name:
        # Use parent directory name
        skill_name = skill_file.parent.name
    skill_name = normalize_name(skill_name)

    if not skill_name or skill_name == "unknown":
        stats["skipped"] += 1
        return False

    # Determine category
    raw_category = metadata.get("category", "")
    category = normalize_category(raw_category) if raw_category else ""
    if not category or category == "unknown":
        category = guess_category(str(skill_file) + " " + content[:1000])

    # Target directory (case-safe)
    rel_path = ""
    try:
        rel_path = str(skill_file.relative_to(skill_file.parents[2])).replace("\\", "/")
    except Exception:
        rel_path = str(skill_file.name)
    key = build_skill_key(repo_slug, rel_path, name=skill_name, category=category)
    target_dir = ensure_unique_dir(skills_dir / category, skill_name, key, repo=repo_slug)
    target_file = target_dir / "SKILL.md"

    if target_file.exists():
        stats["skipped"] += 1
        return False

    # Create directory and copy
    target_dir.mkdir(parents=True, exist_ok=True)
    target_file.write_text(content, encoding="utf-8")

    # Create metadata
    legal_meta = build_legal_metadata(
        repo=repo_slug,
        path=rel_path,
        branch="main",
    )
    meta = {
        "name": skill_name,
        "description": metadata.get("description", "")[:200],
        "category": category,
        "tags": metadata.get("tags", []),
        "repo": repo_slug,
        "source": f"github.com/{repo_slug}",
        "source_path": rel_path,
        "dir_name": target_dir.name,
        "imported_at": datetime.utcnow().isoformat() + "Z",
        **legal_meta,
    }
    (target_dir / "metadata.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

    stats["imported"] += 1
    return True


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    project_dir = script_dir.parent
    skills_dir = project_dir / "skills"

    # Create temp directory for cloning
    clone_dir = project_dir / ".clone_cache"
    clone_dir.mkdir(exist_ok=True)

    logger.info("=" * 60)
    logger.info("CLONE AND IMPORT SKILLS")
    logger.info("=" * 60)
    logger.info(f"Clone cache: {clone_dir}")
    logger.info(f"Skills dir: {skills_dir}")
    logger.info(f"Repos to clone: {len(REPOS_TO_CLONE)}")
    logger.info("")

    stats = {
        "repos_cloned": 0,
        "skills_found": 0,
        "imported": 0,
        "skipped": 0,
        "errors": 0,
    }

    # Phase 1: Clone repos
    logger.info("=== Phase 1: Cloning Repos ===")
    for repo_url in REPOS_TO_CLONE:
        if clone_repo(repo_url, clone_dir):
            stats["repos_cloned"] += 1

    logger.info(f"Cloned {stats['repos_cloned']}/{len(REPOS_TO_CLONE)} repos")
    logger.info("")

    # Phase 2: Find and import skills
    logger.info("=== Phase 2: Importing Skills ===")

    for repo_dir in clone_dir.iterdir():
        if not repo_dir.is_dir() or repo_dir.name.startswith("."):
            continue

        repo_name = repo_dir.name
        repo_slug = REPO_BY_DIR.get(repo_name, repo_name)
        skill_files = find_skill_files(repo_dir)
        stats["skills_found"] += len(skill_files)

        logger.info(f"  {repo_name}: {len(skill_files)} SKILL.md files")

        for skill_file in skill_files:
            import_skill(skill_file, skills_dir, repo_slug, stats)

    # Count total skills
    total_skills = sum(1 for _ in skills_dir.rglob("SKILL.md"))

    # Summary
    logger.info("")
    logger.info("=" * 60)
    logger.info("IMPORT COMPLETE")
    logger.info("=" * 60)
    logger.info(f"  Repos cloned:    {stats['repos_cloned']}")
    logger.info(f"  Skills found:    {stats['skills_found']}")
    logger.info(f"  Imported:        {stats['imported']}")
    logger.info(f"  Skipped:         {stats['skipped']}")
    logger.info(f"  Errors:          {stats['errors']}")
    logger.info("-" * 60)
    logger.info(f"  TOTAL SKILLS:    {total_skills}")
    logger.info("=" * 60)

    # Cleanup prompt
    print(f"\nClone cache at: {clone_dir}")
    print("Run 'rm -rf .clone_cache' to clean up after import.")


if __name__ == "__main__":
    main()
