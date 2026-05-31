#!/usr/bin/env python3
# ruff: noqa: E402
"""
Shared helpers for the sync/download pipeline.

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

import hashlib
import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

# Add parent to path for imports
SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))
sys.path.insert(0, str(SCRIPT_DIR))

from security_blocklist import blocked_metadata_source
from utils import (
    build_skill_key,
    normalize_category,
)


def sanitize_category(category: str) -> str:
    return normalize_category(category or "other")


def skill_key(skill: dict) -> str:
    repo = (skill.get("repo") or "").strip()
    path = (skill.get("path") or skill.get("github_path") or "").strip()
    if repo and path:
        return f"{repo}:{path}"
    if repo:
        return repo
    name = skill.get("name") or ""
    category = sanitize_category(skill.get("category") or "other")
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
    "connectors",
    "references",
    "reference",
    "scripts",
    "assets",
    "knowledge",
    "templates",
    "examples",
    "prompts",
    "rules",
}
BUNDLED_ROOT_FILE_ALLOWLIST = {
    "audit.md",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "requirements.txt",
    "pyproject.toml",
    "setup.md",
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
        if re.search(rf"(?<![a-z0-9_.-]){re.escape(dirname)}/", normalized):
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
    *,
    remove_blocked: bool = False,
) -> list[str]:
    """Validate existing archives against the source blocklist.

    By default this fails closed. The download pipeline passes
    ``remove_blocked=True`` so the scheduled data sync can purge already
    archived blocked sources and commit those deletions.
    """
    exclude = {".git", ".github-skills", ".template", ".templates", ".attic"}
    blocked_archives: list[tuple[Path, str]] = []
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

        archive_dir = meta_path.parent
        blocked_archives.append(
            (
                archive_dir,
                f"{archive_dir}: {blocked_entry['repo']} "
                f"via {source_field} ({blocked_entry.get('reason', 'security blocklist')})",
            )
        )

    if metadata_errors:
        sample = "\n".join(metadata_errors[:20])
        raise RuntimeError(
            "Cannot validate existing archive metadata for security blocklist:\n"
            f"{sample}"
        )

    if blocked_archives:
        sample = "\n".join(summary for _, summary in blocked_archives[:50])
        if remove_blocked:
            output_root = output_dir.resolve()
            removed_archives: list[str] = []
            removed_dirs: set[Path] = set()
            for archive_dir, summary in blocked_archives:
                resolved_archive_dir = archive_dir.resolve()
                try:
                    resolved_archive_dir.relative_to(output_root)
                except ValueError as exc:
                    raise RuntimeError(
                        "Refusing to remove blocked archive outside output dir: "
                        f"{archive_dir}"
                    ) from exc
                if resolved_archive_dir in removed_dirs:
                    continue
                shutil.rmtree(archive_dir)
                removed_dirs.add(resolved_archive_dir)
                removed_archives.append(summary)

            logger.warning(
                "Removed %s existing blocked archived skills before download:\n%s",
                len(removed_archives),
                "\n".join(removed_archives[:50]),
            )
            return removed_archives

        raise RuntimeError(
            "Existing archive contains blocked source repos:\n"
            f"{sample}"
        )

    return []


def remove_ci_untracked_archive_files(output_dir: Path) -> int:
    """Remove stale untracked archive files from CI data checkouts.

    The core repo still has a legacy ``skills/`` tree. In GitHub Actions the
    data repo is checked out into that same path, so old core files can remain
    as untracked files inside the data checkout and then fail incremental scans.
    Only do this cleanup in CI; local untracked files are user work.
    """
    if os.environ.get("GITHUB_ACTIONS") != "true":
        return 0
    if not (output_dir / ".git").exists():
        return 0

    result = subprocess.run(
        ["git", "-C", str(output_dir), "ls-files", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Cannot list untracked archive files in {output_dir}: {stderr}")

    output_root = output_dir.resolve()
    removed = 0
    touched_parents: set[Path] = set()
    for raw_path in result.stdout.split(b"\0"):
        if not raw_path:
            continue
        rel_path = Path(raw_path.decode("utf-8", errors="surrogateescape"))
        if rel_path.is_absolute() or ".." in rel_path.parts:
            raise RuntimeError(f"Refusing unsafe untracked archive path: {rel_path}")
        target = (output_dir / rel_path).resolve()
        try:
            target.relative_to(output_root)
        except ValueError as exc:
            raise RuntimeError(f"Refusing untracked archive path outside output dir: {target}") from exc
        if target.is_dir():
            shutil.rmtree(target)
        elif target.exists() or target.is_symlink():
            target.unlink()
        else:
            continue
        removed += 1
        touched_parents.add(target.parent)

    for parent in sorted(touched_parents, key=lambda path: len(path.parts), reverse=True):
        current = parent
        while current != output_root and current.exists():
            try:
                current.rmdir()
            except OSError:
                break
            current = current.parent

    if removed:
        logger.warning("Removed %s CI-only untracked archive file(s) before download", removed)
    return removed


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
