#!/usr/bin/env python3
"""
Complete sync and download pipeline.

1. (Default) Sync discovered index from GitHub
2. (Optional) Sync SkillsMP source (legacy opt-in)
3. Download SKILL.md files with optimized patterns
4. Generate reports

Usage:
    # Full pipeline
    python scripts/sync_and_download.py

    # Only sync index (no download)
    python scripts/sync_and_download.py --sync-only

    # Only download (use existing index)
    python scripts/sync_and_download.py --download-only

Environment:
    GITHUB_TOKEN - GitHub personal access token for higher rate limits
"""

import argparse
import asyncio
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from crawler.skillsmp_sync import SkillsMPSync
from discover_by_topic import GitHubTopicDiscovery
from utils import normalize_name, ensure_unique_dir, build_skill_key, build_legal_metadata


def sanitize_category(category: str) -> str:
    category = (category or "other").strip()
    if not category:
        category = "other"
    return category.replace("/", "-").replace("\\", "-").replace(":", "-")


def skill_key(skill: dict) -> str:
    repo = (skill.get("repo") or "").strip()
    path = (skill.get("path") or skill.get("github_path") or "").strip()
    if repo and path:
        return f"{repo}:{path}"
    if repo:
        return repo
    name = skill.get("name") or ""
    category = skill.get("category") or "other"
    return f"{category}:{name}"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sync_and_download.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def _source_count(path: Path) -> int:
    """Safely read source count from an existing source JSON file."""
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return 0
    skills = data.get("skills", [])
    total_count = data.get("total_count")
    if isinstance(total_count, int):
        return total_count
    if isinstance(skills, list):
        return len(skills)
    return 0


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

        for skill in source.get("skills", []):
            # Create unique key
            repo = skill.get("repo", "")
            name = skill.get("name", "")
            path = skill.get("path", "")
            key = f"{repo}/{path}/{name}"

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


async def download_skills(
    registry_path: Path,
    output_dir: Path,
    github_token: str = "",
    max_pending: int = 0,
) -> dict:
    """Download skills using optimized downloader."""
    logger.info("=" * 60)
    logger.info("STEP 3: Downloading SKILL.md files")
    logger.info("=" * 60)

    # Import here to avoid circular imports
    import aiohttp
    from collections import defaultdict

    GITHUB_RAW_BASE = "https://raw.githubusercontent.com"
    BRANCHES = ("main", "master")
    MAX_CONCURRENT = 100
    TIMEOUT = 15
    BATCH_SIZE = 300

    # Load registry
    with open(registry_path) as f:
        registry = json.load(f)

    skills = registry.get("skills", [])
    logger.info(f"Total skills in registry: {len(skills)}")

    # Check existing (across all categories)
    exclude = {".git", ".github-skills", ".template", ".templates", ".attic"}
    existing = set()
    for dirpath, dirnames, filenames in os.walk(output_dir):
        dirnames[:] = [d for d in dirnames if d not in exclude]
        if "metadata.json" in filenames and "SKILL.md" in filenames:
            meta_path = Path(dirpath) / "metadata.json"
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
            existing.add(skill_key(meta))

    logger.info(f"Already downloaded: {len(existing)}")

    # Filter pending by repo/path key
    pending = [s for s in skills if skill_key(s) not in existing]
    logger.info(f"To download: {len(pending)}")

    if max_pending and max_pending > 0:
        pending = pending[:max_pending]
        logger.info(f"Applying pending cap: {len(pending)} (max_pending={max_pending})")

    if not pending:
        logger.info("Nothing to download!")
        return {"downloaded": 0, "failed": 0, "total": len(existing)}

    stats = {
        "downloaded": 0,
        "failed": 0,
        "skipped": len(existing),
        "url_attempts": 0,
    }
    failures = defaultdict(list)
    preferred_branch_by_repo = {}

    headers = {"User-Agent": "Claude-Skills-Registry/3.0"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT * 2, ttl_dns_cache=300)
    request_timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    def normalize_repo(repo: str) -> str:
        repo = (repo or "").strip()
        if repo.startswith("https://github.com/"):
            repo = repo[len("https://github.com/"):]
        repo = repo.split("/tree/")[0]
        repo = repo.split("/blob/")[0]
        return repo.rstrip("/")

    def normalize_repo_path(path: str, repo: str) -> str:
        path = (path or "").strip().replace("\\", "/").strip("/")
        if not path:
            return ""

        # Convert full GitHub blob/tree URLs to repo-relative paths when possible.
        if path.startswith("https://github.com/") and repo:
            prefix = f"https://github.com/{repo}/"
            if path.startswith(prefix):
                rest = path[len(prefix):]
                parts = rest.split("/", 2)
                if len(parts) >= 3 and parts[0] in {"blob", "tree"}:
                    return parts[2].strip("/")

        parts = path.split("/", 2)
        if len(parts) >= 3 and parts[0] in {"blob", "tree"}:
            return parts[2].strip("/")

        return path

    def build_relative_candidates(path: str, name: str, normalized_name: str) -> list[str]:
        ordered = []
        seen = set()

        def add(candidate: str):
            candidate = (candidate or "").strip().strip("/")
            if not candidate or candidate in seen:
                return
            seen.add(candidate)
            ordered.append(candidate)

        if path:
            # Most source entries have path; try these first to avoid broad probing.
            if path.lower().endswith("skill.md"):
                add(path)
            else:
                add(f"{path}/SKILL.md")
                add(path)

        name_variants = []
        for raw_name in (name, normalized_name):
            candidate = (raw_name or "").strip().strip("/")
            if candidate and candidate not in name_variants:
                name_variants.append(candidate)

        for variant in name_variants:
            add(f".claude/skills/{variant}/SKILL.md")
            add(f".claude/{variant}/SKILL.md")
            add(f"skills/{variant}/SKILL.md")
            add(f"{variant}/SKILL.md")

        add("SKILL.md")
        add(".claude/SKILL.md")
        return ordered

    def branch_order(repo: str) -> list[str]:
        preferred = preferred_branch_by_repo.get(repo)
        if preferred in BRANCHES:
            return [preferred] + [b for b in BRANCHES if b != preferred]
        return list(BRANCHES)

    async def try_download(session: aiohttp.ClientSession, skill: dict) -> bool:
        name = (skill.get("name") or "").strip() or "unknown"
        # Normalize name to prevent case conflicts on macOS/Windows
        normalized_name = normalize_name(name)
        repo = normalize_repo(skill.get("repo", ""))
        path = normalize_repo_path(skill.get("path", ""), repo)

        if not repo:
            failures["no_repo"].append(name)
            return False

        relative_candidates = build_relative_candidates(path, name, normalized_name)
        attempts = 0

        async with semaphore:
            for branch in branch_order(repo):
                for relative_path in relative_candidates:
                    url = f"{GITHUB_RAW_BASE}/{repo}/{branch}/{relative_path}"
                    attempts += 1
                    try:
                        async with session.get(url, timeout=request_timeout) as resp:
                            if resp.status == 200:
                                content = await resp.text()
                                if content and len(content) > 50 and ("---" in content[:50] or "#" in content[:100]):
                                    # Valid content - save under category with normalized name
                                    category = sanitize_category(skill.get("category", "other"))
                                    category_dir = output_dir / category
                                    category_dir.mkdir(parents=True, exist_ok=True)
                                    key = build_skill_key(repo, path, name=name, category=category)
                                    skill_dir = ensure_unique_dir(category_dir, normalized_name, key, repo=repo)
                                    skill_dir.mkdir(parents=True, exist_ok=True)
                                    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
                                    resolved_path = path or relative_path
                                    legal_meta = build_legal_metadata(
                                        repo=repo,
                                        path=resolved_path,
                                        branch=branch,
                                        source_url=skill.get("source_url", ""),
                                        author=skill.get("author", ""),
                                        license_name=skill.get("license", ""),
                                        copyright_text=skill.get("copyright", ""),
                                        permission_note=skill.get("permission_note", ""),
                                        distribution=skill.get("distribution", ""),
                                    )
                                    (skill_dir / "metadata.json").write_text(
                                        json.dumps({
                                            "name": name,
                                            "description": skill.get("description", ""),
                                            "repo": repo,
                                            "path": resolved_path,
                                            "github_branch": branch,
                                            "category": skill.get("category", ""),
                                            "tags": skill.get("tags", []),
                                            "stars": skill.get("stars", 0),
                                            "source": skill.get("source", ""),
                                            "dir_name": skill_dir.name,
                                            **legal_meta,
                                        }, indent=2, ensure_ascii=False),
                                        encoding="utf-8"
                                    )
                                    preferred_branch_by_repo[repo] = branch
                                    stats["url_attempts"] += attempts
                                    return True
                            elif resp.status == 403:
                                failures["rate_limited"].append(name)
                                stats["url_attempts"] += attempts
                                return False
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue

            failures["not_found"].append(name)
            stats["url_attempts"] += attempts
            return False

    start_time = time.time()

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for i in range(0, len(pending), BATCH_SIZE):
            batch = pending[i:i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE

            tasks = [try_download(session, s) for s in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for r in results:
                if r is True:
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1

            elapsed = time.time() - start_time
            rate = stats["downloaded"] / elapsed if elapsed > 0 else 0

            logger.info(
                f"Batch {batch_num}/{total_batches}: "
                f"✅ {stats['downloaded']} | ❌ {stats['failed']} | ⚡ {rate:.1f}/s"
            )

            await asyncio.sleep(0.2)

    # Final count
    final_count = sum(1 for _ in output_dir.rglob("SKILL.md"))

    logger.info("=" * 60)
    logger.info("DOWNLOAD COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Downloaded: {stats['downloaded']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info(f"URL attempts: {stats['url_attempts']}")
    logger.info(f"Total skills: {final_count}")

    # Save failure report
    failure_report = {
        "timestamp": datetime.now().isoformat(),
        "stats": dict(stats),
        "failure_reasons": {k: len(v) for k, v in failures.items()},
        "failures": dict(failures),
    }
    report_path = output_dir.parent / "failure_report.json"
    with open(report_path, "w") as f:
        json.dump(failure_report, f, indent=2)
    logger.info(f"Failure report saved to {report_path}")

    stats["total"] = final_count
    return stats


def main():
    parser = argparse.ArgumentParser(description="Sync and download Claude skills")
    parser.add_argument("--sync-only", action="store_true", help="Only sync index, don't download")
    parser.add_argument("--download-only", action="store_true", help="Only download, use existing index")
    parser.add_argument("--max-skills", type=int, default=50000, help="Max skills to sync from SkillsMP")
    parser.add_argument(
        "--enable-skillsmp",
        action="store_true",
        help="Enable SkillsMP sync (disabled by default)",
    )
    parser.add_argument(
        "--include-skillsmp-source",
        action="store_true",
        help="Include skillsmp.json when rebuilding registry (disabled by default)",
    )
    parser.add_argument(
        "--allow-empty-skillsmp-overwrite",
        action="store_true",
        help="Allow overwriting skillsmp.json with empty output when SkillsMP returns 0",
    )
    parser.add_argument(
        "--github-discovery",
        action="store_true",
        help="Run GitHub discovery (discover_by_topic) before rebuilding registry",
    )
    parser.add_argument(
        "--skip-github-fallback",
        action="store_true",
        help="Disable automatic GitHub discovery fallback when SkillsMP sync returns 0",
    )
    parser.add_argument(
        "--github-output",
        default="skills",
        help="Output directory for GitHub discovery downloaded skills",
    )
    parser.add_argument(
        "--github-json",
        default="sources/discovered.json",
        help="JSON output path for GitHub discovery source",
    )
    parser.add_argument(
        "--github-max-repos",
        type=int,
        default=0,
        help="Maximum repositories to scan in GitHub discovery (0 = no limit)",
    )
    parser.add_argument(
        "--github-max-topic-pages",
        type=int,
        default=10,
        help="Maximum pages per topic query in GitHub discovery",
    )
    parser.add_argument(
        "--github-max-code-pages",
        type=int,
        default=10,
        help="Maximum pages per code search query in GitHub discovery",
    )
    parser.add_argument(
        "--github-skip-code-search",
        action="store_true",
        help="Skip global code search in GitHub discovery",
    )
    parser.add_argument(
        "--github-request-delay",
        type=float,
        default=2.0,
        help="Delay between GitHub discovery API requests",
    )
    parser.add_argument(
        "--max-pending",
        type=int,
        default=0,
        help="Maximum pending skills to process during download (0 = no limit)",
    )
    args = parser.parse_args()

    # Paths
    script_dir = Path(__file__).parent
    registry_dir = script_dir.parent
    sources_dir = registry_dir / "sources"
    registry_path = registry_dir / "registry.json"
    output_dir = registry_dir / "skills"
    skillsmp_path = sources_dir / "skillsmp.json"

    github_token = os.environ.get("GITHUB_TOKEN", "")

    start_time = time.time()

    # Step 1: Sync from SkillsMP (legacy opt-in)
    skillsmp_count = 0
    if not args.download_only and args.enable_skillsmp:
        skillsmp_count = sync_skillsmp(
            str(skillsmp_path),
            max_skills=args.max_skills,
            keep_on_empty=not args.allow_empty_skillsmp_overwrite,
        )
    elif not args.download_only:
        logger.info("STEP 1: SkillsMP sync is disabled (use --enable-skillsmp to opt in)")

    # Step 1B: Optional GitHub discovery + auto fallback when SkillsMP returns empty
    if not args.download_only:
        skillsmp_unavailable = (not args.enable_skillsmp) or (skillsmp_count == 0)
        should_run_github_discovery = args.github_discovery or (
            skillsmp_unavailable and not args.skip_github_fallback
        )
        if should_run_github_discovery:
            sync_github_discovery(
                output_dir=args.github_output,
                output_json=args.github_json,
                token=github_token,
                max_repos=args.github_max_repos,
                max_topic_pages=args.github_max_topic_pages,
                max_code_pages=args.github_max_code_pages,
                skip_code_search=args.github_skip_code_search,
                request_delay=args.github_request_delay,
            )

    # Step 2: Build unified registry
    if not args.download_only:
        build_unified_registry(
            sources_dir,
            registry_path,
            include_skillsmp=(args.include_skillsmp_source or args.enable_skillsmp),
        )

    # Step 3: Download skills
    if not args.sync_only:
        stats = asyncio.run(
            download_skills(
                registry_path,
                output_dir,
                github_token,
                max_pending=args.max_pending,
            )
        )

    elapsed = time.time() - start_time

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
