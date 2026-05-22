#!/usr/bin/env python3
# ruff: noqa: E402
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
import hashlib
import json
import logging
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import quote

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from discover_by_topic import GitHubTopicDiscovery
from security_blocklist import blocked_metadata_source, load_security_blocklist
from utils import (
    build_legal_metadata,
    build_skill_key,
    ensure_unique_dir,
    iter_source_skills,
    normalize_name,
)

from crawler.skillsmp_sync import SkillsMPSync


from sync_pipeline import (
    build_unified_registry,
    download_skills,
    logger,
    should_fail_on_empty_download,
    sync_github_discovery,
    sync_skillsmp,
)
from sync_pipeline_support import (
    MAX_BUNDLED_FILE_BYTES,
    build_branch_probe_order,
    build_relative_probe_order,
    bundled_relative_path,
    filter_pending_skills,
    is_negative_cache_active,
    is_safe_bundled_file,
    load_acquisition_manifest,
    not_found_cooldown_hours,
    prune_negative_cache,
    remove_ci_untracked_archive_files,
    save_acquisition_manifest,
    select_shard_skills,
    should_recurse_bundled_dir,
    skill_key,
    skill_source_dir,
    to_utc_iso,
    utc_now,
    validate_existing_archive_sources,
)

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
    parser.add_argument(
        "--fail-on-empty-download",
        action="store_true",
        help="Exit non-zero when download-only mode records failures but no successful downloads",
    )
    parser.add_argument(
        "--skip-ci-untracked-cleanup",
        action="store_true",
        help="Skip CI-only untracked archive cleanup before download",
    )
    parser.add_argument(
        "--cleanup-ci-untracked-archive-files-only",
        action="store_true",
        help="Only remove CI-only untracked archive leftovers, then exit",
    )
    parser.add_argument(
        "--acquisition-manifest",
        default="sources/acquisition_manifest.json",
        help="Path to acquisition manifest JSON (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--disable-acquisition-manifest",
        action="store_true",
        help="Disable manifest hints for path/branch probing",
    )
    parser.add_argument(
        "--shard-count",
        type=int,
        default=1,
        help="Total number of shards for deterministic pending partitioning",
    )
    parser.add_argument(
        "--shard-index",
        type=int,
        default=0,
        help="Current shard index (0-based)",
    )
    parser.add_argument(
        "--failure-report",
        default="failure_report.json",
        help="Failure report output path (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--observations-output",
        default="sources/learning/discovery_observations.jsonl",
        help="Download observation JSONL output path (relative to repo root unless absolute)",
    )
    parser.add_argument(
        "--learning-priors",
        default="sources/learning/discovery_priors.json",
        help="Learning priors JSON path (relative to repo root unless absolute)",
    )
    args = parser.parse_args()

    if args.shard_count <= 0:
        raise SystemExit("--shard-count must be >= 1")
    if args.shard_index < 0 or args.shard_index >= args.shard_count:
        raise SystemExit("--shard-index must be in [0, --shard-count)")

    # Paths
    script_dir = Path(__file__).parent
    registry_dir = script_dir.parent
    sources_dir = registry_dir / "sources"
    registry_path = registry_dir / "registry.json"
    output_dir = registry_dir / "skills"
    skillsmp_path = sources_dir / "skillsmp.json"
    manifest_path_arg = Path(args.acquisition_manifest)
    if args.disable_acquisition_manifest:
        acquisition_manifest = None
    elif manifest_path_arg.is_absolute():
        acquisition_manifest = manifest_path_arg
    else:
        acquisition_manifest = registry_dir / manifest_path_arg
    failure_report_arg = Path(args.failure_report)
    if failure_report_arg.is_absolute():
        failure_report = failure_report_arg
    else:
        failure_report = registry_dir / failure_report_arg
    observations_output_arg = Path(args.observations_output)
    if observations_output_arg.is_absolute():
        observations_output = observations_output_arg
    else:
        observations_output = registry_dir / observations_output_arg
    learning_priors_arg = Path(args.learning_priors)
    if learning_priors_arg.is_absolute():
        learning_priors = learning_priors_arg
    else:
        learning_priors = registry_dir / learning_priors_arg

    if args.cleanup_ci_untracked_archive_files_only:
        removed = remove_ci_untracked_archive_files(output_dir)
        logger.info("CI-only untracked archive cleanup removed %s file(s)", removed)
        return

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
                manifest_path=acquisition_manifest,
                shard_count=args.shard_count,
                shard_index=args.shard_index,
                failure_report_path=failure_report,
                observations_output_path=observations_output,
                learning_priors_path=learning_priors,
                cleanup_ci_untracked=not args.skip_ci_untracked_cleanup,
            )
        )
        if args.fail_on_empty_download and should_fail_on_empty_download(stats):
            logger.error(
                "Download gate triggered: downloaded=0 failed=%s; see failure_report.json for details",
                stats["failed"],
            )
            raise SystemExit(1)

    elapsed = time.time() - start_time

    logger.info("=" * 60)
    logger.info("PIPELINE COMPLETE")
    logger.info(f"Total time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
