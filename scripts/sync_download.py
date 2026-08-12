#!/usr/bin/env python3
# ruff: noqa: E402
"""Download execution for the sync pipeline."""

import asyncio
import json
import os
import shutil
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from security_blocklist import blocked_metadata_source, load_security_blocklist
from sync_download_support import (
    asset_redistribution_approved,
    build_archived_skill_metadata,
    classify_download_result,
    collect_contents_bundled_file_entries,
    collect_pinned_tree_entries,
    content_matches_git_blob,
    download_bundled_files_to_directory,
    exact_source_branch,
    read_response_bytes_limited,
    resolve_exact_commit_sha,
)
from sync_pipeline_support import (
    DEFAULT_LEARNING_PRIORS_PATH,
    DEFAULT_MANIFEST_PATH,
    GITHUB_API_BASE,
    ROOT_DIR,
    BundledListingError,
    build_branch_probe_order,
    build_manifest_key,
    build_relative_candidates,
    build_relative_probe_order,
    filter_pending_skills,
    is_safe_portable_relative_path,
    load_acquisition_manifest,
    load_learning_priors,
    logger,
    normalize_download_repo,
    normalize_repo_path,
    normalize_skill_frontmatter_description,
    not_found_cooldown_hours,
    prune_negative_cache,
    remove_ci_untracked_archive_files,
    requires_complete_bundled_archive,
    sanitize_category,
    save_acquisition_manifest,
    save_learning_priors,
    select_shard_skills,
    skill_key,
    to_utc_iso,
    utc_now,
    validate_existing_archive_sources,
)
from utils import (
    build_skill_key,
    ensure_unique_dir,
    normalize_name,
)


async def download_skills(
    registry_path: Path,
    output_dir: Path,
    github_token: str = "",
    max_pending: int = 0,
    manifest_path: Path | None = DEFAULT_MANIFEST_PATH,
    shard_count: int = 1,
    shard_index: int = 0,
    failure_report_path: Path | None = None,
    observations_output_path: Path | None = None,
    learning_priors_path: Path | None = None,
    cleanup_ci_untracked: bool = True,
    exact_paths_only: bool = False,
    pin_commit_sha: bool = False,
) -> dict:
    """Download skills using optimized downloader."""
    logger.info("=" * 60)
    logger.info("STEP 3: Downloading SKILL.md files")
    logger.info("=" * 60)

    from collections import defaultdict

    import aiohttp
    from security_scanner import SecurityScanner

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
    manifest_file = Path(manifest_path) if manifest_path is not None else None
    manifest_entries = load_acquisition_manifest(manifest_file) if manifest_file is not None else {}
    if manifest_file is not None:
        logger.info(
            "Acquisition manifest loaded: %s entries from %s",
            len(manifest_entries),
            manifest_file,
        )
    else:
        logger.info("Acquisition manifest disabled")
    security_blocklist = load_security_blocklist()
    logger.info("Security blocklist loaded: %s repos", len(security_blocklist))
    security_scanner = SecurityScanner()
    removed_blocked_archives = validate_existing_archive_sources(
        output_dir,
        security_blocklist,
        remove_blocked=True,
    )
    removed_ci_untracked_files = (
        remove_ci_untracked_archive_files(output_dir) if cleanup_ci_untracked else 0
    )

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

    priors_file = learning_priors_path or DEFAULT_LEARNING_PRIORS_PATH
    if learning_priors_path is None and registry_path.resolve().parent != ROOT_DIR:
        priors_file = registry_path.resolve().parent / "discovery_priors.json"
    learning_priors = load_learning_priors(priors_file)
    negative_cache = learning_priors.setdefault("negative_cache", {})
    learning_state = {"dirty": False}

    cache_pruned = prune_negative_cache(negative_cache, utc_now())
    if cache_pruned:
        learning_state["dirty"] = True
        logger.info("Negative cache pruned: %s stale entries removed", cache_pruned)

    pending_all, pending_skipped, pending_skipped_rows = filter_pending_skills(
        skills,
        existing,
        negative_cache,
        utc_now(),
    )
    logger.info(
        "To download (before sharding): %s | prefilter no_repo=%s cooldown_not_found=%s",
        len(pending_all),
        pending_skipped["no_repo"],
        pending_skipped["cooldown_not_found"],
    )
    pending = select_shard_skills(pending_all, shard_count=shard_count, shard_index=shard_index)
    logger.info(
        "Shard selection: index=%s count=%s pending=%s",
        shard_index,
        shard_count,
        len(pending),
    )

    if max_pending and max_pending > 0:
        pending = pending[:max_pending]
        logger.info(f"Applying pending cap: {len(pending)} (max_pending={max_pending})")

    if not pending:
        logger.info("Nothing to download!")
        if learning_state["dirty"] or not priors_file.exists():
            learning_priors["updated_at"] = to_utc_iso(utc_now())
            save_learning_priors(priors_file, learning_priors)
            logger.info(
                "Discovery learning priors saved: %s entries in negative cache",
                len(learning_priors.get("negative_cache", {})),
            )
        if observations_output_path:
            observations_output_path.parent.mkdir(parents=True, exist_ok=True)
            with observations_output_path.open("w", encoding="utf-8") as handle:
                for skipped_skill, skipped_reason in pending_skipped_rows:
                    handle.write(
                        json.dumps(
                            {
                                "timestamp": to_utc_iso(utc_now()),
                                "shard_count": shard_count,
                                "shard_index": shard_index,
                                "name": (skipped_skill.get("name") or "").strip(),
                                "repo": (skipped_skill.get("repo") or "").strip(),
                                "path": (skipped_skill.get("path") or "").strip(),
                                "category": sanitize_category(
                                    skipped_skill.get("category", "other")
                                ),
                                "candidate_key": skill_key(skipped_skill),
                                "outcome": "skipped",
                                "failure_reason": skipped_reason,
                                "attempts": 0,
                                "manifest_hit": False,
                                "resolved_branch": "",
                                "resolved_relative_path": "",
                            },
                            ensure_ascii=False,
                        )
                        + "\n"
                    )
        return {
            "downloaded": 0,
            "failed": 0,
            "bundled_files": 0,
            "total": len(existing),
            "shard_count": shard_count,
            "shard_index": shard_index,
            "pending_before_shard": len(pending_all),
            "prefiltered_no_repo": pending_skipped["no_repo"],
            "skipped_cooldown_not_found": pending_skipped["cooldown_not_found"],
            "blocked_archives_removed": len(removed_blocked_archives),
            "ci_untracked_files_removed": removed_ci_untracked_files,
        }

    stats = {
        "downloaded": 0,
        "failed": 0,
        "skipped": len(existing),
        "bundled_files": 0,
        "url_attempts": 0,
        "manifest_hits": 0,
        "manifest_misses": 0,
        "shard_count": shard_count,
        "shard_index": shard_index,
        "pending_before_shard": len(pending_all),
        "prefiltered_no_repo": pending_skipped["no_repo"],
        "skipped_cooldown_not_found": pending_skipped["cooldown_not_found"],
        "blocked_archives_removed": len(removed_blocked_archives),
        "ci_untracked_files_removed": removed_ci_untracked_files,
    }
    failures = defaultdict(list)
    observations: list[dict] = []
    preferred_branch_by_repo = {}
    manifest_state = {"dirty": False}

    headers = {"User-Agent": "Claude-Skills-Registry/3.0"}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT * 2, ttl_dns_cache=300)
    request_timeout = aiohttp.ClientTimeout(total=TIMEOUT)

    def add_observation(
        skill: dict,
        *,
        outcome: str,
        failure_reason: str = "",
        attempts: int = 0,
        manifest_hit: bool = False,
        branch: str = "",
        relative_path: str = "",
        bundled_file_count: int = 0,
        commit_sha: str = "",
    ) -> None:
        observations.append(
            {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "shard_count": shard_count,
                "shard_index": shard_index,
                "name": (skill.get("name") or "").strip(),
                "repo": (skill.get("repo") or "").strip(),
                "path": (skill.get("path") or "").strip(),
                "category": sanitize_category(skill.get("category", "other")),
                "candidate_key": skill_key(skill),
                "outcome": outcome,
                "failure_reason": failure_reason,
                "attempts": attempts,
                "manifest_hit": manifest_hit,
                "resolved_branch": branch,
                "resolved_relative_path": relative_path,
                "resolved_commit_sha": commit_sha,
                "bundled_file_count": bundled_file_count,
            }
        )

    for skipped_skill, skipped_reason in pending_skipped_rows:
        add_observation(skipped_skill, outcome="skipped", failure_reason=skipped_reason)

    commit_sha_cache: dict[tuple[str, str], str] = {}
    repo_identity_cache: dict[str, str] = {}
    tree_cache: dict[tuple[str, str], list[dict]] = {}

    async def fetch_contents_listing(
        session: aiohttp.ClientSession,
        repo: str,
        branch: str,
        directory_path: str,
    ) -> list[dict]:
        encoded_path = quote(directory_path.strip("/"), safe="/")
        encoded_ref = quote(branch, safe="")
        path_suffix = f"/{encoded_path}" if encoded_path else ""
        url = f"{GITHUB_API_BASE}/repos/{repo}/contents{path_suffix}?ref={encoded_ref}"
        try:
            async with session.get(url, timeout=request_timeout) as resp:
                if resp.status != 200:
                    raise BundledListingError(directory_path, f"status {resp.status}")
                payload = await resp.json()
        except BundledListingError:
            raise
        except Exception as exc:
            reason = str(exc) or exc.__class__.__name__
            raise BundledListingError(directory_path, reason) from exc
        if not isinstance(payload, list):
            raise BundledListingError(directory_path, "unexpected payload")
        return payload

    async def collect_bundled_file_entries(
        session: aiohttp.ClientSession,
        repo: str,
        branch: str,
        resolved_skill_path: str,
    ) -> tuple[list[dict], bool]:
        return await collect_contents_bundled_file_entries(
            session,
            repo,
            branch,
            resolved_skill_path,
            listing_fetcher=fetch_contents_listing,
        )

    async def try_download(session: aiohttp.ClientSession, skill: dict) -> bool:
        name = (skill.get("name") or "").strip() or "unknown"
        normalized_name = normalize_name(name)
        repo = normalize_download_repo(skill.get("repo", ""))
        path = normalize_repo_path(skill.get("path", ""), repo)
        category = sanitize_category(skill.get("category", "other"))
        candidate_key = skill_key(skill)

        if not repo:
            failures["no_repo"].append(name)
            add_observation(skill, outcome="failed", failure_reason="no_repo")
            return False
        if path and not is_safe_portable_relative_path(path):
            failures["invalid_source_path"].append(name)
            add_observation(skill, outcome="failed", failure_reason="invalid_source_path")
            return False
        blocked_source = blocked_metadata_source(
            {
                **skill,
                "repo": repo,
                "path": path or skill.get("path", ""),
                "github_path": skill.get("github_path", ""),
            },
            security_blocklist,
        )
        if blocked_source:
            blocked_entry, source_field = blocked_source
            reason = blocked_entry.get("reason") or "blocked source repo"
            failures["blocked_source"].append(
                f"{blocked_entry['repo']}: {name} via {source_field} ({reason})"
            )
            add_observation(skill, outcome="failed", failure_reason="blocked_source")
            logger.warning(
                "Blocked security-listed source before download: %s via %s (%s)",
                blocked_entry["repo"],
                source_field,
                name,
            )
            return False

        manifest_key = build_manifest_key(repo, path, name, category)
        manifest_entry = manifest_entries.get(manifest_key) if manifest_file is not None else None
        if manifest_file is not None:
            if manifest_entry:
                stats["manifest_hits"] += 1
            else:
                stats["manifest_misses"] += 1

        if exact_paths_only:
            if not path or path.rsplit("/", 1)[-1].casefold() != "skill.md":
                failures["invalid_exact_path"].append(name)
                add_observation(skill, outcome="failed", failure_reason="invalid_exact_path")
                return False
            relative_candidates = [path]
        else:
            relative_candidates = build_relative_candidates(path, name, normalized_name)
            relative_candidates = build_relative_probe_order(relative_candidates, manifest_entry)
        attempts = 0
        commit_resolution_failed = False

        async with semaphore:
            if exact_paths_only and pin_commit_sha:
                recorded_branch = exact_source_branch(skill)
                if not recorded_branch:
                    failures["missing_exact_branch"].append(name)
                    add_observation(skill, outcome="failed", failure_reason="missing_exact_branch")
                    return False
                branch_order = [recorded_branch]
            else:
                branch_order = build_branch_probe_order(
                    repo, preferred_branch_by_repo, manifest_entry, BRANCHES
                )
            for branch in branch_order:
                download_ref = branch
                if pin_commit_sha:
                    try:
                        download_ref = await resolve_exact_commit_sha(
                            session,
                            repo,
                            branch,
                            timeout=request_timeout,
                            security_blocklist=security_blocklist,
                            repo_cache=repo_identity_cache,
                            commit_cache=commit_sha_cache,
                        )
                    except Exception as exc:  # noqa: BLE001 — recorded as a failed branch
                        commit_resolution_failed = True
                        logger.warning("Unable to pin %s@%s: %s", repo, branch, exc)
                        continue
                for relative_path in relative_candidates:
                    encoded_path = quote(relative_path, safe="/")
                    url = f"{GITHUB_RAW_BASE}/{repo}/{download_ref}/{encoded_path}"
                    attempts += 1
                    skill_dir = None
                    try:
                        try:
                            pinned_tree_result = (
                                await collect_pinned_tree_entries(
                                    session,
                                    repo,
                                    download_ref,
                                    relative_path,
                                    timeout=request_timeout,
                                    tree_cache=tree_cache,
                                )
                                if pin_commit_sha
                                else None
                            )
                        except BundledListingError as exc:
                            failures["bundled_listing_failed"].append(f"{name}: {exc}")
                            stats["url_attempts"] += attempts
                            add_observation(
                                skill,
                                outcome="failed",
                                failure_reason="bundled_listing_failed",
                                attempts=attempts,
                            )
                            return False
                        async with session.get(url, timeout=request_timeout) as resp:
                            if resp.status == 200:
                                if pinned_tree_result is not None:
                                    raw_content = await read_response_bytes_limited(
                                        resp, pinned_tree_result[2]["size"]
                                    )
                                    if not content_matches_git_blob(
                                        pinned_tree_result[2], raw_content
                                    ):
                                        raise ValueError(
                                            "pinned SKILL.md response does not match its Git blob"
                                        )
                                    source_text = raw_content.decode("utf-8-sig")
                                else:
                                    source_text = await resp.text()
                                content = normalize_skill_frontmatter_description(
                                    source_text, skill
                                )
                                if (
                                    content
                                    and len(content) > 50
                                    and ("---" in content[:50] or "#" in content[:100])
                                ):
                                    require_complete_archive = requires_complete_bundled_archive(
                                        content
                                    ) or (exact_paths_only and pin_commit_sha)
                                    redistribution_approved = asset_redistribution_approved(skill)
                                    if require_complete_archive and not redistribution_approved:
                                        failure_reason = "asset_redistribution_not_approved"
                                        failures[failure_reason].append(name)
                                        stats["url_attempts"] += attempts
                                        add_observation(
                                            skill,
                                            outcome="failed",
                                            failure_reason=failure_reason,
                                            attempts=attempts,
                                        )
                                        return False
                                    category_dir = output_dir / category
                                    category_dir.mkdir(parents=True, exist_ok=True)
                                    key = build_skill_key(repo, path, name=name, category=category)
                                    skill_dir = ensure_unique_dir(
                                        category_dir, normalized_name, key, repo=repo
                                    )
                                    skill_dir.mkdir(parents=True, exist_ok=True)
                                    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
                                    resolved_path = path or relative_path
                                    bundle_result = (
                                        await download_bundled_files_to_directory(
                                            session,
                                            repo,
                                            download_ref,
                                            relative_path,
                                            skill_dir,
                                            require_complete_archive,
                                            pin_commit_sha=pin_commit_sha,
                                            timeout=request_timeout,
                                            tree_cache=tree_cache,
                                            contents_collector=collect_bundled_file_entries,
                                            pinned_tree_result=pinned_tree_result,
                                        )
                                        if redistribution_approved
                                        else ([], [], "", {})
                                    )
                                    (
                                        bundled_files,
                                        bundled_failures,
                                        bundled_failure_reason,
                                        bundled_file_blobs,
                                    ) = bundle_result
                                    if bundled_failures:
                                        failure_reason = (
                                            bundled_failure_reason or "bundled_download_failed"
                                        )
                                        shutil.rmtree(skill_dir, ignore_errors=True)
                                        failures[failure_reason].append(
                                            f"{name}: {', '.join(bundled_failures)}"
                                        )
                                        stats["url_attempts"] += attempts
                                        add_observation(
                                            skill,
                                            outcome="failed",
                                            failure_reason=failure_reason,
                                            attempts=attempts,
                                            manifest_hit=manifest_entry is not None,
                                            branch=branch,
                                            relative_path=relative_path,
                                            bundled_file_count=len(bundled_files),
                                            commit_sha=download_ref if pin_commit_sha else "",
                                        )
                                        return False
                                    (skill_dir / "metadata.json").write_text(
                                        json.dumps(
                                            build_archived_skill_metadata(
                                                skill,
                                                name=name,
                                                repo=repo,
                                                resolved_path=resolved_path,
                                                branch=branch,
                                                dir_name=skill_dir.name,
                                                bundled_files=bundled_files,
                                                bundled_file_blobs=bundled_file_blobs,
                                                commit_sha=download_ref if pin_commit_sha else "",
                                                assets_verified_at=(
                                                    to_utc_iso(utc_now()) if pin_commit_sha else ""
                                                ),
                                            ),
                                            indent=2,
                                            ensure_ascii=False,
                                        ),
                                        encoding="utf-8",
                                    )
                                    is_safe, security_issues = security_scanner.scan_file(
                                        skill_dir / "SKILL.md"
                                    )
                                    if not is_safe:
                                        issue_types = sorted(
                                            {
                                                str(issue.get("type") or "unknown")
                                                for issue in security_issues
                                            }
                                        )
                                        shutil.rmtree(skill_dir, ignore_errors=True)
                                        failures["security_scan_failed"].append(
                                            f"{repo}: {name} ({', '.join(issue_types[:8])})"
                                        )
                                        stats["url_attempts"] += attempts
                                        add_observation(
                                            skill,
                                            outcome="failed",
                                            failure_reason="security_scan_failed",
                                            attempts=attempts,
                                            manifest_hit=manifest_entry is not None,
                                            branch=branch,
                                            relative_path=relative_path,
                                            bundled_file_count=len(bundled_files),
                                            commit_sha=download_ref if pin_commit_sha else "",
                                        )
                                        logger.warning(
                                            "Rejected downloaded skill after security scan: %s/%s (%s)",
                                            repo,
                                            relative_path,
                                            ", ".join(issue_types[:8]),
                                        )
                                        return False
                                    stats["bundled_files"] += len(bundled_files)
                                    preferred_branch_by_repo[repo] = branch
                                    if manifest_file is not None:
                                        manifest_entries[manifest_key] = {
                                            "repo": repo,
                                            "branch": branch,
                                            "relative_path": relative_path,
                                            **(
                                                {"commit_sha": download_ref}
                                                if pin_commit_sha
                                                else {}
                                            ),
                                            "updated_at": datetime.utcnow().isoformat() + "Z",
                                        }
                                        manifest_state["dirty"] = True
                                    stats["url_attempts"] += attempts
                                    if candidate_key in negative_cache:
                                        del negative_cache[candidate_key]
                                        learning_state["dirty"] = True
                                    add_observation(
                                        skill,
                                        outcome="downloaded",
                                        attempts=attempts,
                                        manifest_hit=manifest_entry is not None,
                                        branch=branch,
                                        relative_path=relative_path,
                                        bundled_file_count=len(bundled_files),
                                        commit_sha=download_ref if pin_commit_sha else "",
                                    )
                                    return True
                            elif resp.status == 403:
                                failures["rate_limited"].append(name)
                                stats["url_attempts"] += attempts
                                add_observation(
                                    skill,
                                    outcome="failed",
                                    failure_reason="rate_limited",
                                    attempts=attempts,
                                    manifest_hit=manifest_entry is not None,
                                )
                                return False
                    except (asyncio.TimeoutError, aiohttp.ClientError):
                        continue
                    except Exception:
                        if skill_dir is not None:
                            shutil.rmtree(skill_dir, ignore_errors=True)
                        raise

            failure_reason = "commit_resolution_failed" if commit_resolution_failed else "not_found"
            failures[failure_reason].append(name)
            stats["url_attempts"] += attempts
            now_utc = utc_now()
            entry = negative_cache.get(candidate_key)
            prev_count = int((entry or {}).get("count") or 0)
            count = prev_count + 1
            cooldown_hours = not_found_cooldown_hours(count)
            negative_cache[candidate_key] = {
                "reason": "not_found",
                "count": count,
                "last_seen_at": to_utc_iso(now_utc),
                "cooldown_until": to_utc_iso(now_utc + timedelta(hours=cooldown_hours)),
                "repo": repo,
                "path": path,
            }
            learning_state["dirty"] = True
            add_observation(
                skill,
                outcome="failed",
                failure_reason=failure_reason,
                attempts=attempts,
                manifest_hit=manifest_entry is not None,
            )
            return False

    start_time = time.time()

    async with aiohttp.ClientSession(connector=connector, headers=headers) as session:
        for i in range(0, len(pending), BATCH_SIZE):
            batch = pending[i : i + BATCH_SIZE]
            batch_num = i // BATCH_SIZE + 1
            total_batches = (len(pending) + BATCH_SIZE - 1) // BATCH_SIZE

            tasks = [try_download(session, s) for s in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for skill, result in zip(batch, results, strict=True):
                succeeded, internal_error = classify_download_result(skill, result)
                if succeeded:
                    stats["downloaded"] += 1
                else:
                    stats["failed"] += 1
                    if internal_error:
                        failures["internal_error"].append(internal_error)
                        add_observation(skill, outcome="failed", failure_reason="internal_error")

            elapsed = time.time() - start_time
            rate = stats["downloaded"] / elapsed if elapsed > 0 else 0

            logger.info(
                f"Batch {batch_num}/{total_batches}: "
                f"✅ {stats['downloaded']} | ❌ {stats['failed']} | ⚡ {rate:.1f}/s"
            )

            await asyncio.sleep(0.2)
    # Final count
    final_count = sum(1 for _ in output_dir.rglob("SKILL.md"))
    if manifest_file is not None and (manifest_state["dirty"] or not manifest_file.exists()):
        save_acquisition_manifest(manifest_file, manifest_entries)
        logger.info(
            "Acquisition manifest saved: %s entries to %s",
            len(manifest_entries),
            manifest_file,
        )

    logger.info("=" * 60)
    logger.info("DOWNLOAD COMPLETE")
    logger.info("=" * 60)
    logger.info(f"Downloaded: {stats['downloaded']}")
    logger.info(f"Bundled files archived: {stats['bundled_files']}")
    logger.info(f"Failed: {stats['failed']}")
    logger.info(f"URL attempts: {stats['url_attempts']}")
    logger.info(f"Total skills: {final_count}")

    if learning_state["dirty"] or not priors_file.exists():
        learning_priors["updated_at"] = to_utc_iso(utc_now())
        save_learning_priors(priors_file, learning_priors)
        logger.info(
            "Discovery learning priors saved: %s entries in negative cache",
            len(learning_priors.get("negative_cache", {})),
        )

    if observations_output_path:
        observations_output_path.parent.mkdir(parents=True, exist_ok=True)
        with observations_output_path.open("w", encoding="utf-8") as handle:
            for row in observations:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
        logger.info(
            "Discovery observations saved to %s (%s rows)",
            observations_output_path,
            len(observations),
        )

    # Save failure report
    failure_report = {
        "timestamp": datetime.now().isoformat(),
        "stats": dict(stats),
        "failure_reasons": {k: len(v) for k, v in failures.items()},
        "failures": dict(failures),
    }
    report_path = failure_report_path or (output_dir.parent / "failure_report.json")
    with open(report_path, "w") as f:
        json.dump(failure_report, f, indent=2)
    logger.info(f"Failure report saved to {report_path}")

    stats["total"] = final_count
    return stats
