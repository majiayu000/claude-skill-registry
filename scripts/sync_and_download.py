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
from security_blocklist import blocked_metadata_source, blocked_repo_entry, load_security_blocklist
from utils import build_legal_metadata, build_skill_key, ensure_unique_dir, normalize_name

from crawler.skillsmp_sync import SkillsMPSync


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
ACQUISITION_MANIFEST_VERSION = 1
DEFAULT_MANIFEST_PATH = ROOT_DIR / "sources" / "acquisition_manifest.json"
DEFAULT_LEARNING_PRIORS_PATH = ROOT_DIR / "sources" / "learning" / "discovery_priors.json"
GITHUB_API_BASE = "https://api.github.com"

BUNDLED_DIR_ALLOWLIST = {
    "references",
    "scripts",
    "assets",
    "templates",
    "examples",
}
BUNDLED_ROOT_FILE_ALLOWLIST = {
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "uv.lock",
    "README.md",
    "LICENSE",
    "LICENSE.md",
}
BUNDLED_REQUIRED_ROOT_FILE_HINTS = BUNDLED_ROOT_FILE_ALLOWLIST - {
    "README.md",
    "LICENSE",
    "LICENSE.md",
}
BUNDLED_FILE_EXTENSIONS = {
    ".bash",
    ".css",
    ".csv",
    ".gif",
    ".html",
    ".jpeg",
    ".jpg",
    ".js",
    ".json",
    ".jsx",
    ".j2",
    ".md",
    ".mjs",
    ".png",
    ".ps1",
    ".py",
    ".sh",
    ".svg",
    ".toml",
    ".tpl",
    ".ts",
    ".tsx",
    ".txt",
    ".yaml",
    ".yml",
}
BUNDLED_EXCLUDED_PARTS = {
    ".git",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}
MAX_BUNDLED_FILE_BYTES = 1_000_000
MAX_BUNDLED_TOTAL_BYTES = 5_000_000
MAX_BUNDLED_FILES_PER_SKILL = 100


class BundledListingError(Exception):
    """Raised when GitHub Contents API cannot list a skill support directory."""

    def __init__(self, directory_path: str, reason: str):
        self.directory_path = directory_path.strip("/") or "."
        self.reason = reason
        super().__init__(f"{self.directory_path}: {reason}")


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


def _ordered_unique(values: list[str]) -> list[str]:
    ordered = []
    seen = set()
    for value in values:
        normalized = (value or "").strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def skill_source_dir(relative_path: str) -> str:
    """Return the source directory for a resolved SKILL.md path."""
    normalized = (relative_path or "").strip().strip("/")
    if not normalized or normalized == "SKILL.md":
        return ""
    if normalized.lower().endswith("/skill.md"):
        return normalized.rsplit("/", 1)[0]
    parent = PurePosixPath(normalized).parent.as_posix()
    return "" if parent == "." else parent


def bundled_relative_path(source_dir: str, repo_path: str) -> str:
    """Return repo_path relative to source_dir using POSIX separators."""
    source_dir = (source_dir or "").strip().strip("/")
    repo_path = (repo_path or "").strip().strip("/")
    if not source_dir:
        return repo_path
    prefix = f"{source_dir}/"
    if repo_path == source_dir:
        return ""
    if not repo_path.startswith(prefix):
        return ""
    return repo_path[len(prefix):]


def should_recurse_bundled_dir(relative_path: str) -> bool:
    """Return True when a support subdirectory is safe to inspect."""
    parts = [part for part in relative_path.strip("/").split("/") if part]
    if not parts:
        return False
    if any(part.startswith(".") or part in BUNDLED_EXCLUDED_PARTS for part in parts):
        return False
    return parts[0] in BUNDLED_DIR_ALLOWLIST


def is_safe_bundled_file(relative_path: str, size: int) -> bool:
    """Return True when a bundled support file should be archived."""
    normalized = relative_path.strip("/")
    if not normalized or normalized == "SKILL.md":
        return False
    if size < 0 or size > MAX_BUNDLED_FILE_BYTES:
        return False

    parts = [part for part in normalized.split("/") if part]
    if not parts:
        return False
    if any(part.startswith(".") or part in BUNDLED_EXCLUDED_PARTS for part in parts):
        return False

    filename = parts[-1]
    if filename.lower() == "skill.md":
        return False
    if len(parts) == 1:
        return filename in BUNDLED_ROOT_FILE_ALLOWLIST

    if parts[0] not in BUNDLED_DIR_ALLOWLIST:
        return False
    if filename in BUNDLED_ROOT_FILE_ALLOWLIST:
        return True
    return PurePosixPath(filename).suffix.lower() in BUNDLED_FILE_EXTENSIONS


def is_submodule_contents_entry(entry: dict) -> bool:
    """Return True for GitHub Contents API submodules exposed as file entries."""
    return entry.get("type") == "submodule" or "submodule_git_url" in entry


def requires_complete_bundled_archive(skill_content: str) -> bool:
    """Return True when SKILL.md explicitly depends on bundled support files."""
    normalized = (skill_content or "").lower().replace("\\", "/")
    for dirname in BUNDLED_DIR_ALLOWLIST:
        if f"{dirname}/" in normalized:
            return True
    return any(filename.lower() in normalized for filename in BUNDLED_REQUIRED_ROOT_FILE_HINTS)


def build_manifest_key(repo: str, path: str, name: str, category: str) -> str:
    """Build a stable key for acquisition manifest lookups."""
    return build_skill_key(repo, path, name=name, category=sanitize_category(category))


def load_acquisition_manifest(path: Path) -> dict[str, dict]:
    """Load acquisition manifest entries keyed by skill key."""
    if not path.exists():
        return {}

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Failed to parse acquisition manifest %s: %s", path, exc)
        return {}

    raw_entries = payload.get("entries", payload) if isinstance(payload, dict) else {}
    if not isinstance(raw_entries, dict):
        return {}

    entries: dict[str, dict] = {}
    for raw_key, raw_entry in raw_entries.items():
        if not isinstance(raw_entry, dict):
            continue
        repo = (raw_entry.get("repo") or "").strip()
        branch = (raw_entry.get("branch") or "").strip()
        relative_path = (raw_entry.get("relative_path") or "").strip().strip("/")
        if not repo or not branch or not relative_path:
            continue
        entries[str(raw_key)] = {
            "repo": repo,
            "branch": branch,
            "relative_path": relative_path,
            "updated_at": raw_entry.get("updated_at", ""),
        }
    return entries


def save_acquisition_manifest(path: Path, entries: dict[str, dict]) -> None:
    """Persist acquisition manifest to disk."""
    payload = {
        "version": ACQUISITION_MANIFEST_VERSION,
        "updated_at": datetime.utcnow().isoformat() + "Z",
        "total_count": len(entries),
        "entries": entries,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def utc_now() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def to_utc_iso(ts: datetime) -> str:
    """Serialize timezone-aware datetime to UTC ISO 8601 with Z suffix."""
    return ts.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_utc_iso(value: str) -> datetime | None:
    """Parse UTC ISO string used by this pipeline."""
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def load_learning_priors(path: Path) -> dict:
    """Load learning priors JSON with minimal defaults."""
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            if isinstance(payload, dict):
                payload.setdefault("version", 1)
                payload.setdefault("repo_priors", {})
                payload.setdefault("topic_yield", {})
                payload.setdefault("query_yield", {})
                payload.setdefault("negative_cache", {})
                return payload
        except Exception as exc:
            logger.warning("Failed to parse learning priors %s: %s", path, exc)

    return {
        "version": 1,
        "repo_priors": {},
        "topic_yield": {},
        "query_yield": {},
        "negative_cache": {},
    }


def save_learning_priors(path: Path, priors: dict) -> None:
    """Persist learning priors JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(priors, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def not_found_cooldown_hours(failure_count: int) -> int:
    """Return cooldown window for repeated not_found failures."""
    if failure_count <= 1:
        return 24
    if failure_count == 2:
        return 72
    return 168


def is_negative_cache_active(entry: dict | None, now_utc: datetime) -> bool:
    """True when a negative-cache entry is still inside cooldown."""
    if not entry:
        return False
    reason = (entry.get("reason") or "").strip()
    if reason != "not_found":
        return False
    cooldown_until = parse_utc_iso(str(entry.get("cooldown_until") or ""))
    if not cooldown_until:
        return False
    return now_utc < cooldown_until


def prune_negative_cache(negative_cache: dict, now_utc: datetime) -> int:
    """Drop stale negative-cache entries that expired more than 30 days ago."""
    removed = 0
    retention_cutoff = now_utc - timedelta(days=30)
    for key in list(negative_cache.keys()):
        entry = negative_cache.get(key)
        if not isinstance(entry, dict):
            del negative_cache[key]
            removed += 1
            continue
        cooldown_until = parse_utc_iso(str(entry.get("cooldown_until") or ""))
        last_seen = parse_utc_iso(str(entry.get("last_seen_at") or ""))
        anchor = cooldown_until or last_seen
        if anchor and anchor < retention_cutoff:
            del negative_cache[key]
            removed += 1
    return removed


def filter_pending_skills(
    skills: list[dict],
    existing: set[str],
    negative_cache: dict,
    now_utc: datetime,
) -> tuple[list[dict], dict[str, int], list[tuple[dict, str]]]:
    """Filter out ineligible pending skills before download."""
    filtered: list[dict] = []
    skipped = {"existing": 0, "no_repo": 0, "cooldown_not_found": 0}
    skipped_rows: list[tuple[dict, str]] = []

    for skill in skills:
        key = skill_key(skill)
        if key in existing:
            skipped["existing"] += 1
            continue

        repo = (skill.get("repo") or "").strip()
        if not repo:
            skipped["no_repo"] += 1
            skipped_rows.append((skill, "no_repo_prefilter"))
            continue

        if is_negative_cache_active(negative_cache.get(key), now_utc):
            skipped["cooldown_not_found"] += 1
            skipped_rows.append((skill, "cooldown_not_found"))
            continue

        filtered.append(skill)

    return filtered, skipped, skipped_rows


def validate_existing_archive_sources(
    output_dir: Path,
    security_blocklist: dict[str, dict],
) -> None:
    """Fail when existing archived skills are sourced from blocked repos."""
    exclude = {".git", ".github-skills", ".template", ".templates", ".attic"}
    blocked_archives: list[str] = []
    metadata_errors: list[str] = []

    for dirpath, dirnames, filenames in os.walk(output_dir):
        dirnames[:] = [dirname for dirname in dirnames if dirname not in exclude]
        if "metadata.json" not in filenames or "SKILL.md" not in filenames:
            continue

        meta_path = Path(dirpath) / "metadata.json"
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            metadata_errors.append(f"{meta_path}: {exc}")
            continue

        blocked_source = blocked_metadata_source(meta, security_blocklist)
        if not blocked_source:
            continue
        blocked_entry, source_field = blocked_source

        blocked_archives.append(
            f"{meta_path.parent}: {blocked_entry['repo']} "
            f"via {source_field} ({blocked_entry.get('reason', 'security blocklist')})"
        )

    if metadata_errors:
        sample = "\n".join(metadata_errors[:20])
        raise RuntimeError(
            "Cannot validate existing archive metadata for security blocklist:\n"
            f"{sample}"
        )

    if blocked_archives:
        sample = "\n".join(blocked_archives[:50])
        raise RuntimeError(
            "Existing archive contains blocked source repos:\n"
            f"{sample}"
        )


def build_branch_probe_order(
    repo: str,
    preferred_branch_by_repo: dict[str, str],
    manifest_entry: dict | None,
    default_branches: tuple[str, ...],
) -> list[str]:
    """Build branch probe order with manifest hint first, then learned preference."""
    candidates = []
    if manifest_entry and manifest_entry.get("branch"):
        candidates.append(str(manifest_entry.get("branch")))
    preferred = preferred_branch_by_repo.get(repo)
    if preferred:
        candidates.append(preferred)
    candidates.extend(default_branches)
    return _ordered_unique(candidates)


def build_relative_probe_order(relative_candidates: list[str], manifest_entry: dict | None) -> list[str]:
    """Build relative-path probe order with manifest hint first."""
    candidates = []
    if manifest_entry and manifest_entry.get("relative_path"):
        candidates.append(str(manifest_entry.get("relative_path")).strip("/"))
    candidates.extend(relative_candidates)
    return _ordered_unique(candidates)


def select_shard_skills(skills: list[dict], shard_count: int, shard_index: int) -> list[dict]:
    """Select a deterministic shard subset from skills."""
    if shard_count <= 1:
        return list(skills)
    selected = []
    for skill in skills:
        key = skill_key(skill)
        digest = hashlib.sha1(key.encode("utf-8")).hexdigest()
        bucket = int(digest, 16) % shard_count
        if bucket == shard_index:
            selected.append(skill)
    return selected


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
    manifest_path: Path | None = None,
    shard_count: int = 1,
    shard_index: int = 0,
    failure_report_path: Path | None = None,
    observations_output_path: Path | None = None,
    learning_priors_path: Path | None = None,
) -> dict:
    """Download skills using optimized downloader."""
    logger.info("=" * 60)
    logger.info("STEP 3: Downloading SKILL.md files")
    logger.info("=" * 60)

    # Import here to avoid circular imports
    from collections import defaultdict

    import aiohttp

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
    manifest_file = manifest_path or DEFAULT_MANIFEST_PATH
    manifest_entries = load_acquisition_manifest(manifest_file)
    logger.info(
        "Acquisition manifest loaded: %s entries from %s",
        len(manifest_entries),
        manifest_file,
    )
    security_blocklist = load_security_blocklist()
    logger.info("Security blocklist loaded: %s repos", len(security_blocklist))
    validate_existing_archive_sources(output_dir, security_blocklist)

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
                                "category": sanitize_category(skipped_skill.get("category", "other")),
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
                "bundled_file_count": bundled_file_count,
            }
        )

    for skipped_skill, skipped_reason in pending_skipped_rows:
        add_observation(skipped_skill, outcome="skipped", failure_reason=skipped_reason)

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
    ) -> list[dict]:
        source_dir = skill_source_dir(resolved_skill_path)
        queue = [source_dir]
        seen_dirs = set()
        candidates: list[dict] = []

        while queue:
            current_dir = queue.pop(0)
            if current_dir in seen_dirs:
                continue
            seen_dirs.add(current_dir)

            for entry in await fetch_contents_listing(session, repo, branch, current_dir):
                entry_type = entry.get("type")
                if is_submodule_contents_entry(entry):
                    continue

                repo_path = str(entry.get("path") or "").strip("/")
                rel_path = bundled_relative_path(source_dir, repo_path)
                if not rel_path:
                    continue

                if entry_type == "dir":
                    if should_recurse_bundled_dir(rel_path):
                        queue.append(repo_path)
                    continue

                if entry_type != "file":
                    continue

                try:
                    size = int(entry.get("size") or 0)
                except (TypeError, ValueError):
                    size = -1
                if is_safe_bundled_file(rel_path, size):
                    candidates.append(
                        {
                            "repo_path": repo_path,
                            "relative_path": rel_path,
                            "download_url": entry.get("download_url") or "",
                            "size": size,
                        }
                    )

        selected: list[dict] = []
        total_size = 0
        for entry in sorted(candidates, key=lambda item: item["relative_path"]):
            if len(selected) >= MAX_BUNDLED_FILES_PER_SKILL:
                break
            if total_size + entry["size"] > MAX_BUNDLED_TOTAL_BYTES:
                continue
            selected.append(entry)
            total_size += entry["size"]
        return selected

    async def download_bundled_files(
        session: aiohttp.ClientSession,
        repo: str,
        branch: str,
        resolved_skill_path: str,
        skill_dir: Path,
        require_complete_archive: bool,
    ) -> tuple[list[str], list[str], str]:
        archived: list[str] = []
        failed: list[str] = []
        try:
            entries = await collect_bundled_file_entries(session, repo, branch, resolved_skill_path)
        except BundledListingError as exc:
            if not require_complete_archive:
                return archived, failed, ""
            return archived, [str(exc)], "bundled_listing_failed"
        if not entries:
            return archived, failed, ""

        skill_root = skill_dir.resolve()
        for entry in entries:
            rel_path = entry["relative_path"]
            target_path = (skill_dir / rel_path).resolve()
            try:
                target_path.relative_to(skill_root)
            except ValueError:
                failed.append(rel_path)
                continue

            url = entry["download_url"] or (
                f"{GITHUB_RAW_BASE}/{repo}/{branch}/{quote(entry['repo_path'], safe='/')}"
            )
            try:
                async with session.get(url, timeout=request_timeout) as resp:
                    if resp.status != 200:
                        failed.append(rel_path)
                        continue
                    content = await resp.read()
            except Exception:
                failed.append(rel_path)
                continue

            if len(content) > MAX_BUNDLED_FILE_BYTES:
                failed.append(rel_path)
                continue
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_bytes(content)
            archived.append(rel_path)

        if failed and not require_complete_archive:
            skill_root = skill_dir.resolve()
            for rel_path in archived:
                target_path = (skill_dir / rel_path).resolve()
                try:
                    target_path.relative_to(skill_root)
                except ValueError:
                    continue
                target_path.unlink(missing_ok=True)
            return [], [], ""

        failure_reason = "bundled_download_failed" if failed else ""
        return archived, failed, failure_reason

    async def try_download(session: aiohttp.ClientSession, skill: dict) -> bool:
        name = (skill.get("name") or "").strip() or "unknown"
        # Normalize name to prevent case conflicts on macOS/Windows
        normalized_name = normalize_name(name)
        repo = normalize_repo(skill.get("repo", ""))
        path = normalize_repo_path(skill.get("path", ""), repo)
        category = sanitize_category(skill.get("category", "other"))
        candidate_key = skill_key(skill)

        if not repo:
            failures["no_repo"].append(name)
            add_observation(skill, outcome="failed", failure_reason="no_repo")
            return False
        blocked_entry = blocked_repo_entry(repo, security_blocklist)
        if blocked_entry:
            reason = blocked_entry.get("reason") or "blocked source repo"
            failures["blocked_source"].append(f"{repo}: {name} ({reason})")
            add_observation(skill, outcome="failed", failure_reason="blocked_source")
            logger.warning("Blocked security-listed source repo: %s (%s)", repo, name)
            return False

        manifest_key = build_manifest_key(repo, path, name, category)
        manifest_entry = manifest_entries.get(manifest_key)
        if manifest_entry:
            stats["manifest_hits"] += 1
        else:
            stats["manifest_misses"] += 1

        relative_candidates = build_relative_candidates(path, name, normalized_name)
        relative_candidates = build_relative_probe_order(relative_candidates, manifest_entry)
        attempts = 0

        async with semaphore:
            for branch in build_branch_probe_order(
                repo, preferred_branch_by_repo, manifest_entry, BRANCHES
            ):
                for relative_path in relative_candidates:
                    url = f"{GITHUB_RAW_BASE}/{repo}/{branch}/{relative_path}"
                    attempts += 1
                    try:
                        async with session.get(url, timeout=request_timeout) as resp:
                            if resp.status == 200:
                                content = await resp.text()
                                if content and len(content) > 50 and ("---" in content[:50] or "#" in content[:100]):
                                    require_complete_archive = requires_complete_bundled_archive(content)
                                    # Valid content - save under category with normalized name
                                    category_dir = output_dir / category
                                    category_dir.mkdir(parents=True, exist_ok=True)
                                    key = build_skill_key(repo, path, name=name, category=category)
                                    skill_dir = ensure_unique_dir(category_dir, normalized_name, key, repo=repo)
                                    skill_dir.mkdir(parents=True, exist_ok=True)
                                    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
                                    resolved_path = path or relative_path
                                    (
                                        bundled_files,
                                        bundled_failures,
                                        bundled_failure_reason,
                                    ) = await download_bundled_files(
                                        session,
                                        repo,
                                        branch,
                                        relative_path,
                                        skill_dir,
                                        require_complete_archive,
                                    )
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
                                        )
                                        return False
                                    stats["bundled_files"] += len(bundled_files)
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
                                            "archive_mode": "directory" if bundled_files else "skill-md",
                                            "bundled_files": bundled_files,
                                            **legal_meta,
                                        }, indent=2, ensure_ascii=False),
                                        encoding="utf-8"
                                    )
                                    preferred_branch_by_repo[repo] = branch
                                    manifest_entries[manifest_key] = {
                                        "repo": repo,
                                        "branch": branch,
                                        "relative_path": relative_path,
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
                    except asyncio.TimeoutError:
                        continue
                    except Exception:
                        continue

            failures["not_found"].append(name)
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
                failure_reason="not_found",
                attempts=attempts,
                manifest_hit=manifest_entry is not None,
            )
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
    if manifest_state["dirty"] or not manifest_file.exists():
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


def should_fail_on_empty_download(stats: dict) -> bool:
    """Return True when the download pass failed on an empty archive."""
    downloaded = int(stats.get("downloaded", 0))
    failed = int(stats.get("failed", 0))
    skipped = int(stats.get("skipped", 0))
    return downloaded == 0 and failed > 0 and skipped == 0


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
