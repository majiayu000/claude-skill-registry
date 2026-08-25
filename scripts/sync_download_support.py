#!/usr/bin/env python3
"""Pure helpers for exact and bundled sync downloads."""

import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any
from urllib.parse import quote

from security_blocklist import blocked_metadata_source
from sync_pipeline_support import (
    GITHUB_API_BASE,
    MAX_BUNDLED_FILES_PER_SKILL,
    MAX_BUNDLED_TOTAL_BYTES,
    BundledListingError,
    bundled_relative_path,
    has_case_conflicting_paths,
    is_safe_bundled_file,
    is_submodule_contents_entry,
    is_valid_git_source_ref,
    should_recurse_bundled_dir,
    skill_source_dir,
)
from sync_pipeline_support import MAX_BUNDLED_FILE_BYTES as MAX_BUNDLED_FILE_BYTES
from utils import build_legal_metadata, classify_license, normalize_license

SHA_PATTERN = re.compile(r"[0-9a-fA-F]{40}")
MAX_SKILL_FILE_BYTES = 1_000_000
GITHUB_RAW_BASE = "https://raw.githubusercontent.com"


def asset_redistribution_approved(skill: dict) -> bool:
    """Return whether metadata explicitly permits bundled-asset redistribution."""
    license_name = normalize_license(str(skill.get("license") or ""))
    distribution = str(skill.get("distribution") or "").strip()
    return classify_license(license_name) == "compatible" and distribution == "compatible"


def select_bundled_file_entries(candidates: list[dict]) -> tuple[list[dict], bool]:
    """Apply bundle limits and report whether eligible files were omitted."""
    relative_paths = [entry["relative_path"] for entry in candidates]
    if has_case_conflicting_paths(relative_paths):
        raise BundledListingError(".", "case-conflicting bundled paths")
    selected = []
    total_size = 0
    truncated = False
    for entry in sorted(candidates, key=lambda item: item["relative_path"]):
        if len(selected) >= MAX_BUNDLED_FILES_PER_SKILL:
            truncated = True
            continue
        if total_size + entry["size"] > MAX_BUNDLED_TOTAL_BYTES:
            truncated = True
            continue
        selected.append(entry)
        total_size += entry["size"]
    return selected, truncated


async def collect_contents_bundled_file_entries(
    session: Any,
    repo: str,
    branch: str,
    resolved_skill_path: str,
    *,
    listing_fetcher: Any,
) -> tuple[list[dict], bool]:
    """Collect ordinary Contents API entries and report any support-scope omission."""
    source_dir = skill_source_dir(resolved_skill_path)
    queue = [source_dir]
    seen_dirs = set()
    candidates: list[dict] = []
    incomplete = False
    while queue:
        current_dir = queue.pop(0)
        if current_dir in seen_dirs:
            continue
        seen_dirs.add(current_dir)

        for entry in await listing_fetcher(session, repo, branch, current_dir):
            entry_type = entry.get("type")
            repo_path = str(entry.get("path") or "").strip("/")
            rel_path = bundled_relative_path(source_dir, repo_path)
            if not rel_path:
                continue
            root_component = rel_path.split("/", 1)[0]
            support_scope = should_recurse_bundled_dir(root_component) or is_safe_bundled_file(
                rel_path, 0, reject_nonportable=True
            )
            if is_submodule_contents_entry(entry):
                incomplete = incomplete or support_scope
                continue
            if entry_type == "dir":
                if should_recurse_bundled_dir(rel_path):
                    queue.append(repo_path)
                elif support_scope:
                    incomplete = True
                continue
            if entry_type != "file":
                incomplete = incomplete or support_scope
                continue
            try:
                size = int(entry.get("size") or 0)
            except (TypeError, ValueError):
                size = -1
            eligible_file = is_safe_bundled_file(
                rel_path, 0, reject_nonportable=True
            )
            if is_safe_bundled_file(rel_path, size, reject_nonportable=True):
                candidates.append(
                    {
                        "repo_path": repo_path,
                        "relative_path": rel_path,
                        "download_url": entry.get("download_url") or "",
                        "size": size,
                        "sha": entry.get("sha") or "",
                    }
                )
            elif eligible_file:
                incomplete = True

    selected, truncated = select_bundled_file_entries(candidates)
    return selected, truncated or incomplete


def exact_source_branch(skill: dict) -> str:
    """Return a safe recorded source branch for immutable exact downloads."""
    branches = []
    for field in ("github_branch", "branch"):
        if field not in skill:
            continue
        raw_branch = skill[field]
        if not isinstance(raw_branch, str):
            return ""
        branch = raw_branch.strip()
        if not is_valid_git_source_ref(branch):
            return ""
        branches.append(branch)
    if not branches or any(branch != branches[0] for branch in branches[1:]):
        return ""
    return branches[0]


async def resolve_exact_commit_sha(
    session: Any,
    repo: str,
    branch: str,
    *,
    timeout: Any,
    security_blocklist: dict,
    repo_cache: dict[str, str],
    commit_cache: dict[tuple[str, str], str],
) -> str:
    """Resolve an exact branch or pinned commit after proving repository identity."""
    cache_key = (repo, branch)
    if cache_key in commit_cache:
        return commit_cache[cache_key]

    canonical_repo = repo_cache.get(repo)
    if canonical_repo is None:
        async with session.get(f"{GITHUB_API_BASE}/repos/{repo}", timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"repository resolution failed with status {response.status}")
            payload = await response.json()
        canonical_repo = payload.get("full_name") if isinstance(payload, dict) else ""
        if not isinstance(canonical_repo, str) or canonical_repo.casefold() != repo.casefold():
            raise RuntimeError("repository resolution returned a different canonical identity")
        if blocked_metadata_source({"repo": canonical_repo}, security_blocklist):
            raise RuntimeError("repository resolution returned a blocked canonical identity")
        repo_cache[repo] = canonical_repo

    if SHA_PATTERN.fullmatch(branch):
        commit_url = f"{GITHUB_API_BASE}/repos/{canonical_repo}/commits/{branch.lower()}"
        async with session.get(commit_url, timeout=timeout) as response:
            if response.status != 200:
                raise RuntimeError(f"commit ref resolution failed with status {response.status}")
            payload = await response.json()
        resolved_sha = payload.get("sha") if isinstance(payload, dict) else ""
        if not isinstance(resolved_sha, str) or resolved_sha.casefold() != branch.casefold():
            raise RuntimeError("commit ref resolution returned a different commit identity")
        commit_cache[cache_key] = branch.lower()
        return branch.lower()

    branch_url = f"{GITHUB_API_BASE}/repos/{canonical_repo}/branches/{quote(branch, safe='')}"
    async with session.get(branch_url, timeout=timeout) as response:
        if response.status != 200:
            raise RuntimeError(f"branch resolution failed with status {response.status}")
        payload = await response.json()
    resolved_branch = payload.get("name") if isinstance(payload, dict) else ""
    commit = payload.get("commit") if isinstance(payload, dict) else None
    commit_sha = commit.get("sha") if isinstance(commit, dict) else ""
    if resolved_branch != branch:
        raise RuntimeError("branch resolution returned a different branch identity")
    if not isinstance(commit_sha, str) or not SHA_PATTERN.fullmatch(commit_sha):
        raise RuntimeError("branch resolution returned an invalid commit SHA")
    commit_cache[cache_key] = commit_sha.lower()
    return commit_sha.lower()


async def collect_pinned_tree_entries(
    session: Any,
    repo: str,
    commit_sha: str,
    resolved_skill_path: str,
    *,
    timeout: Any,
    tree_cache: dict[tuple[str, str], list[dict]],
) -> tuple[list[dict], bool, dict]:
    """Collect a complete, regular-file-only bundle from one immutable Git tree."""
    cache_key = (repo, commit_sha)
    entries = tree_cache.get(cache_key)
    if entries is None:
        url = f"{GITHUB_API_BASE}/repos/{repo}/git/trees/{commit_sha}?recursive=1"
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    raise BundledListingError(".", f"tree status {response.status}")
                payload = await response.json()
        except BundledListingError:
            raise
        except Exception as exc:
            reason = str(exc) or exc.__class__.__name__
            raise BundledListingError(".", reason) from exc
        if not isinstance(payload, dict) or payload.get("truncated") is not False:
            raise BundledListingError(".", "truncated or malformed Git tree")
        entries = payload.get("tree")
        if not isinstance(entries, list) or any(not isinstance(entry, dict) for entry in entries):
            raise BundledListingError(".", "malformed Git tree entries")
        tree_cache[cache_key] = entries

    source_entry = next(
        (entry for entry in entries if entry.get("path") == resolved_skill_path),
        None,
    )
    if (
        not isinstance(source_entry, dict)
        or source_entry.get("type") != "blob"
        or source_entry.get("mode") not in {"100644", "100755"}
    ):
        raise BundledListingError(resolved_skill_path, "source skill is not a regular blob")
    source_size = source_entry.get("size")
    source_sha = source_entry.get("sha")
    if (
        isinstance(source_size, bool)
        or not isinstance(source_size, int)
        or source_size < 0
        or source_size > MAX_SKILL_FILE_BYTES
    ):
        raise BundledListingError(resolved_skill_path, "source skill has an invalid size")
    if not isinstance(source_sha, str) or not SHA_PATTERN.fullmatch(source_sha):
        raise BundledListingError(resolved_skill_path, "source skill lacks a valid object ID")
    source_blob = {
        "repo_path": resolved_skill_path,
        "size": source_size,
        "sha": source_sha.lower(),
    }

    source_dir = skill_source_dir(resolved_skill_path)
    candidates = []
    omitted_eligible_file = False
    for entry in entries:
        repo_path = entry.get("path")
        if not isinstance(repo_path, str) or repo_path == resolved_skill_path:
            continue
        rel_path = bundled_relative_path(source_dir, repo_path)
        if not rel_path:
            continue
        try:
            size = int(entry.get("size") or 0)
        except (TypeError, ValueError):
            size = -1
        parts = PurePosixPath(rel_path).parts
        eligible_at_size = is_safe_bundled_file(rel_path, size, reject_nonportable=True)
        eligible_without_size_limit = is_safe_bundled_file(rel_path, 0, reject_nonportable=True)
        in_support_scope = eligible_at_size or (
            bool(parts) and should_recurse_bundled_dir(parts[0])
        )
        entry_type = entry.get("type")
        mode = entry.get("mode")
        if entry_type == "tree" and mode == "040000":
            continue
        if entry_type != "blob" or mode not in {"100644", "100755"}:
            if in_support_scope:
                raise BundledListingError(repo_path, f"unsupported Git object mode {mode}")
            continue
        if not eligible_at_size:
            if eligible_without_size_limit:
                omitted_eligible_file = True
            continue
        blob_sha = entry.get("sha")
        if not isinstance(blob_sha, str) or not SHA_PATTERN.fullmatch(blob_sha):
            raise BundledListingError(repo_path, "regular blob lacks a valid object ID")
        candidates.append(
            {
                "repo_path": repo_path,
                "relative_path": rel_path,
                "download_url": "",
                "size": size,
                "sha": blob_sha.lower(),
                "mode": mode,
            }
        )
    selected, truncated = select_bundled_file_entries(candidates)
    return selected, truncated or omitted_eligible_file, source_blob


async def read_response_bytes_limited(response: Any, max_bytes: int) -> bytes:
    """Read a response without buffering more than the allowed byte count."""
    advertised_size = getattr(response, "content_length", None)
    if advertised_size is not None and (
        isinstance(advertised_size, bool)
        or not isinstance(advertised_size, int)
        or advertised_size < 0
        or advertised_size > max_bytes
    ):
        raise ValueError("response Content-Length exceeds or violates the byte limit")
    stream = getattr(response, "content", None)
    if stream is None or not hasattr(stream, "iter_chunked"):
        raise ValueError("response body does not expose a bounded byte stream")
    content = bytearray()
    async for chunk in stream.iter_chunked(64 * 1024):
        if not isinstance(chunk, bytes):
            raise ValueError("response body yielded a non-byte chunk")
        content.extend(chunk)
        if len(content) > max_bytes:
            raise ValueError("response body exceeds the byte limit")
    return bytes(content)


async def download_bundled_files_to_directory(
    session: Any,
    repo: str,
    branch: str,
    resolved_skill_path: str,
    skill_dir: Path,
    require_complete_archive: bool,
    *,
    allow_empty_complete_archive: bool = False,
    pin_commit_sha: bool,
    timeout: Any,
    tree_cache: dict[tuple[str, str], list[dict]],
    contents_collector: Any,
    pinned_tree_result: tuple[list[dict], bool, dict] | None = None,
) -> tuple[list[str], list[str], str, dict[str, str]]:
    """Download a validated support bundle and return its immutable blob map."""
    archived: list[str] = []
    failed: list[str] = []
    blob_ids: dict[str, str] = {}
    try:
        if pin_commit_sha:
            entries, truncated, _source_blob = (
                pinned_tree_result
                if pinned_tree_result is not None
                else await collect_pinned_tree_entries(
                    session,
                    repo,
                    branch,
                    resolved_skill_path,
                    timeout=timeout,
                    tree_cache=tree_cache,
                )
            )
        else:
            entries, truncated = await contents_collector(
                session, repo, branch, resolved_skill_path
            )
    except BundledListingError as exc:
        if not require_complete_archive:
            return archived, failed, "", blob_ids
        return archived, [str(exc)], "bundled_listing_failed", blob_ids
    if truncated and require_complete_archive:
        message = "eligible bundled files exceed per-skill count or byte limits"
        return archived, [message], "bundled_limits_exceeded", blob_ids
    if not entries:
        if require_complete_archive and not allow_empty_complete_archive:
            return (
                archived,
                ["required bundled archive contains no eligible support files"],
                "bundled_listing_incomplete",
                blob_ids,
            )
        return archived, failed, "", blob_ids

    skill_root = skill_dir.resolve()
    for entry in entries:
        rel_path = entry["relative_path"]
        target_path = (skill_dir / rel_path).resolve()
        try:
            target_path.relative_to(skill_root)
        except ValueError:
            failed.append(rel_path)
            continue

        pinned_url = f"{GITHUB_RAW_BASE}/{repo}/{branch}/{quote(entry['repo_path'], safe='/')}"
        url = pinned_url if pin_commit_sha else entry["download_url"] or pinned_url
        try:
            async with session.get(url, timeout=timeout) as response:
                if response.status != 200:
                    failed.append(rel_path)
                    continue
                if pin_commit_sha:
                    content = await read_response_bytes_limited(response, entry["size"])
                else:
                    content = await response.read()
        except Exception:
            failed.append(rel_path)
            continue

        if not is_safe_bundled_file(rel_path, len(content)):
            failed.append(rel_path)
            continue
        if pin_commit_sha and not content_matches_git_blob(entry, content):
            failed.append(rel_path)
            continue
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_bytes(content)
        target_path.chmod(0o755 if entry.get("mode") == "100755" else 0o644)
        archived.append(rel_path)
        if pin_commit_sha:
            blob_ids[rel_path] = entry["sha"]

    if failed and not require_complete_archive:
        for rel_path in archived:
            target_path = (skill_dir / rel_path).resolve()
            try:
                target_path.relative_to(skill_root)
            except ValueError:
                continue
            target_path.unlink(missing_ok=True)
        return [], [], "", {}

    failure_reason = "bundled_download_failed" if failed else ""
    return archived, failed, failure_reason, blob_ids


def content_matches_git_blob(entry: dict, content: bytes) -> bool:
    """Match both the advertised byte length and immutable Git blob object ID."""
    expected_size = entry.get("size")
    expected_sha = entry.get("sha")
    if len(content) != expected_size or not isinstance(expected_sha, str):
        return False
    blob_header = f"blob {len(content)}\0".encode("ascii")
    actual_sha = hashlib.sha1(blob_header + content, usedforsecurity=False).hexdigest()
    return actual_sha == expected_sha.casefold()


def bundled_file_blobs_match(
    metadata: dict,
    skill_dir: Path,
    bundled_files: list[str],
) -> bool:
    """Verify that every archived support file matches its pinned Git blob ID."""
    blob_ids = metadata.get("bundled_file_blobs")
    if not isinstance(blob_ids, dict) or set(blob_ids) != set(bundled_files):
        return False
    for relative_path in bundled_files:
        expected_sha = blob_ids.get(relative_path)
        if not isinstance(expected_sha, str) or not SHA_PATTERN.fullmatch(expected_sha):
            return False
        try:
            content = (skill_dir / relative_path).read_bytes()
        except OSError:
            return False
        if not content_matches_git_blob({"size": len(content), "sha": expected_sha}, content):
            return False
    return True


def classify_download_result(skill: dict, result: object) -> tuple[bool, str]:
    """Classify an async task result and retain unexpected exception details."""
    if isinstance(result, BaseException) and not isinstance(result, Exception):
        raise result
    if result is True:
        return True, ""
    if isinstance(result, Exception):
        name = (skill.get("name") or "unknown").strip() or "unknown"
        return False, f"{name}: {type(result).__name__}: {result}"
    return False, ""


def build_archived_skill_metadata(
    skill: dict,
    *,
    name: str,
    repo: str,
    resolved_path: str,
    branch: str,
    dir_name: str,
    bundled_files: list[str],
    bundled_file_blobs: dict[str, str] | None = None,
    commit_sha: str = "",
    assets_verified_at: str = "",
) -> dict:
    """Build downloader metadata without coupling it to network control flow."""
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
    return {
        "name": name,
        "description": skill.get("description", ""),
        "repo": repo,
        "path": resolved_path,
        "github_branch": branch,
        **(
            {"github_commit_sha": commit_sha, "assets_verified_at": assets_verified_at}
            if commit_sha
            else {}
        ),
        "category": skill.get("category", ""),
        "tags": skill.get("tags", []),
        "stars": skill.get("stars", 0),
        "source": skill.get("source", ""),
        "dir_name": dir_name,
        "archive_mode": "directory" if bundled_files else "skill-md",
        "bundled_files": bundled_files,
        **(
            {"bundled_file_blobs": dict(sorted(bundled_file_blobs.items()))}
            if commit_sha and bundled_files and bundled_file_blobs
            else {}
        ),
        **legal_meta,
    }
