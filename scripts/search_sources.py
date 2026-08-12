#!/usr/bin/env python3
"""Source loaders for search index generation."""

import json
import logging
import re
from datetime import datetime
from pathlib import Path, PurePosixPath
from typing import Any, Dict, List, Optional

from archive_preflight import iter_canonical_archive_paths
from audit_skill_assets import canonical_source_identity_from_metadata
from category_taxonomy import resolve_category
from sync_download_support import bundled_file_blobs_match, exact_source_branch
from sync_pipeline_support import has_case_conflicting_paths, is_safe_portable_relative_path
from utils import (
    extract_description,
    get_repo_suffix,
    is_declared_bundled_skill_file,
    load_metadata,
)

logger = logging.getLogger(__name__)
SHA_PATTERN = re.compile(r"^[0-9a-fA-F]{40}$")
ASSET_FIELDS = {
    "asset_state",
    "asset_liveness",
    "bundled_file_count",
    "github_commit_sha",
    "assets_verified_at",
    "assets_liveness_checked_at",
    "assets_liveness_sha",
}
RESERVED_ARCHIVE_FILES = {"skill.md", "metadata.json"}


def legacy_asset_free_record(record: dict) -> dict:
    """Project a search record onto the fields used by the pre-asset dedupe rank."""
    return {key: value for key, value in record.items() if key not in ASSET_FIELDS}


def _valid_timestamp(value: object) -> bool:
    if not isinstance(value, str) or not value or value != value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return parsed.tzinfo is not None


def is_root_mounted_path(path: str) -> bool:
    """Empty or '.' path means SKILL.md lives at the repo root."""
    if path is None:
        return True
    stripped = str(path).strip()
    return stripped == "" or stripped == "."


def has_install_location(path: str) -> bool:
    """True when path identifies a real install location (subdir or repo root)."""
    return bool(path) or is_root_mounted_path(path)


def infer_install_status(repo: str, path: str, install: str) -> str:
    """Classify whether the registry metadata provides a usable install path."""
    if not install:
        return "broken"
    if install.startswith("local/"):
        return "unknown"
    if repo and has_install_location(path):
        return "known_good"
    if repo:
        return "unknown"
    return "risky"


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


def asset_ranking_penalty(skill: Dict[str, Any]) -> float:
    """Return a small down-rank only penalty for non-live asset evidence."""
    if skill.get("asset_state") == "verified":
        return {"live": 0.0, "partial": 0.25, "moved": 0.5, "gone": 0.75}.get(
            skill.get("asset_liveness"), 0.1
        )
    return 0.1


def validated_published_asset_fields(record: dict) -> dict:
    """Return only complete, internally consistent published asset evidence."""
    count = record.get("bundled_file_count")
    pinned_sha = record.get("github_commit_sha")
    verified_at = record.get("assets_verified_at")
    if (
        record.get("asset_state") != "verified"
        or isinstance(count, bool)
        or not isinstance(count, int)
        or count < 1
        or not isinstance(pinned_sha, str)
        or not SHA_PATTERN.fullmatch(pinned_sha)
        or not _valid_timestamp(verified_at)
    ):
        return {}

    fields = {
        "asset_state": "verified",
        "bundled_file_count": count,
        "github_commit_sha": pinned_sha.lower(),
        "assets_verified_at": verified_at,
    }
    liveness = record.get("asset_liveness")
    checked_at = record.get("assets_liveness_checked_at")
    liveness_sha = record.get("assets_liveness_sha")
    if liveness not in {"live", "partial", "moved", "gone"}:
        return fields
    if not _valid_timestamp(checked_at):
        return fields
    if liveness_sha is not None and (
        not isinstance(liveness_sha, str) or not SHA_PATTERN.fullmatch(liveness_sha)
    ):
        return fields
    if liveness in {"live", "partial"} and liveness_sha is None:
        return fields
    if liveness == "gone" and liveness_sha is not None:
        return fields
    fields.update(
        {
            "asset_liveness": liveness,
            "assets_liveness_checked_at": checked_at,
        }
    )
    if liveness_sha is not None:
        fields["assets_liveness_sha"] = liveness_sha.lower()
    return fields


def verified_asset_fields(metadata: dict, skill_dir: Path, archive_root: Path) -> dict:
    """Return verified asset facets bound to their canonical source identity."""
    root = archive_root.absolute()
    candidate = skill_dir.absolute()
    if root.is_symlink():
        return {}
    try:
        relative = candidate.relative_to(root)
        candidate.resolve().relative_to(root.resolve())
    except ValueError:
        return {}
    if len(relative.parts) != 2:
        return {}
    current = root
    for part in relative.parts:
        current /= part
        if current.is_symlink():
            return {}
    if any((skill_dir / filename).is_symlink() for filename in ("SKILL.md", "metadata.json")):
        return {}
    declared = metadata.get("bundled_files")
    pinned_sha = metadata.get("github_commit_sha")
    verified_at = metadata.get("assets_verified_at")
    repo, source_path, source_error = canonical_source_identity_from_metadata(metadata)
    source_branch = exact_source_branch(metadata)
    if (
        source_error
        or not source_branch
        or metadata.get("archive_mode") != "directory"
        or not isinstance(declared, list)
        or not declared
        or not isinstance(pinned_sha, str)
        or not SHA_PATTERN.fullmatch(pinned_sha)
        or not _valid_timestamp(verified_at)
    ):
        return {}

    normalized = []
    for value in declared:
        if not is_safe_portable_relative_path(value):
            return {}
        first_component = PurePosixPath(value).parts[0].casefold()
        if first_component in RESERVED_ARCHIVE_FILES or value in normalized:
            return {}
        normalized.append(value)
    if has_case_conflicting_paths(normalized):
        return {}
    try:
        actual = []
        archive_paths = []
        for path in skill_dir.rglob("*"):
            relative = path.relative_to(skill_dir).as_posix()
            if path.is_symlink():
                return {}
            archive_paths.append(relative)
            first_component = PurePosixPath(relative).parts[0].casefold()
            if first_component in RESERVED_ARCHIVE_FILES and relative not in {
                "SKILL.md",
                "metadata.json",
            }:
                return {}
            if path.is_file():
                if relative in {"SKILL.md", "metadata.json"}:
                    continue
                actual.append(relative)
    except OSError:
        return {}
    if has_case_conflicting_paths(archive_paths):
        return {}
    if sorted(normalized) != sorted(actual):
        return {}
    if not bundled_file_blobs_match(metadata, skill_dir, normalized):
        return {}

    fields = {
        "asset_state": "verified",
        "bundled_file_count": len(normalized),
        "github_commit_sha": pinned_sha.lower(),
        "assets_verified_at": verified_at,
    }
    fields.update(
        {
            key: metadata[key]
            for key in (
                "asset_liveness",
                "assets_liveness_checked_at",
                "assets_liveness_sha",
            )
            if key in metadata
        }
    )
    published = validated_published_asset_fields(fields)
    if not published:
        return {}
    return {
        **published,
        "repo": repo,
        "path": source_path,
        "branch": source_branch,
    }


def scan_skills_v2(skills_dir: Path) -> List[Dict]:
    """Recursively scan archive root and index one entry per archive skill."""
    skills = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

    list(iter_canonical_archive_paths(skills_dir, strict_registry=True))
    for skill_md in skills_dir.rglob("SKILL.md"):
        if is_declared_bundled_skill_file(skill_md, skills_dir):
            continue
        skill_dir = skill_md.parent
        rel_parts = skill_dir.relative_to(skills_dir).parts
        category_name = rel_parts[0] if rel_parts else "other"
        metadata = load_metadata(skill_dir)
        dir_name = skill_dir.name

        name = metadata.get("name") or dir_name

        if name == dir_name:
            repo_for_suffix = metadata.get("repo", "")
            suffix = get_repo_suffix(repo_for_suffix)
            if suffix and dir_name.endswith(f"-{suffix}"):
                name = dir_name[: -(len(suffix) + 1)]

        description = metadata.get("description", "")
        if not description:
            try:
                content = skill_md.read_text(encoding="utf-8")
                description = extract_description(content)
            except Exception as exc:
                logger.warning("Failed to extract description from %s: %s", skill_md, exc)
        if not description:
            description = f"Skill: {name}"

        category = resolve_category(metadata.get("category", category_name), allow_unknown=True)

        repo = metadata.get("repo", "")
        github_path = metadata.get("github_path") or metadata.get("path") or "/".join(rel_parts)
        github_branch = metadata.get("github_branch") or metadata.get("branch") or "main"
        asset_fields = verified_asset_fields(metadata, skill_dir, skills_dir)
        if asset_fields:
            repo = asset_fields["repo"]
            github_path = asset_fields["path"]
            github_branch = asset_fields["branch"]

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
            "archive_path": skill_md.relative_to(skills_dir).as_posix(),
            "branch": github_branch,
            "category": category,
            "tags": tags,
            "stars": stars,
            "source": metadata.get("source", "downloaded"),
            "install": install,
            **asset_fields,
        }

        skills.append(skill_entry)

    return skills


def load_registry_count(registry_path: Path) -> Optional[int]:
    """Load deduplicated skill count from registry.json."""
    if not registry_path.exists():
        return None
    try:
        with open(registry_path, "r", encoding="utf-8") as f:
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


def resolve_registry_artifact(base_dir: Path, artifact_ref: str) -> Path:
    """Resolve a registry artifact path relative to a manifest or registry directory."""
    artifact_path = Path(artifact_ref)
    if artifact_path.is_absolute():
        return artifact_path
    return (base_dir / artifact_path).resolve()


def load_registry_manifest_shards(registry_path: Path, registry: Dict) -> List[Dict]:
    """Load full registry skills from a compatibility registry manifest pointer."""
    manifest_ref = registry.get("manifest")
    if not isinstance(manifest_ref, str) or not manifest_ref.strip():
        return []

    manifest_path = resolve_registry_artifact(registry_path.parent, manifest_ref)
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    skills: List[Dict] = []
    for shard in manifest.get("shards", []):
        shard_ref = shard.get("path") if isinstance(shard, dict) else None
        if not isinstance(shard_ref, str) or not shard_ref.strip():
            raise ValueError(f"Invalid registry shard reference in {manifest_path}: {shard!r}")
        shard_path = resolve_registry_artifact(manifest_path.parent, shard_ref)
        with open(shard_path, "r", encoding="utf-8") as f:
            shard_payload = json.load(f)
        shard_skills = shard_payload.get("skills")
        if not isinstance(shard_skills, list):
            raise ValueError(f"Registry shard is missing skills array: {shard_path}")
        skills.extend(shard_skills)
    return skills


def add_registry_install_fields(skills: List[Dict]) -> List[Dict]:
    """Populate install fields for registry fallback rows."""
    for skill in skills:
        canonical_repo, canonical_path, source_error = canonical_source_identity_from_metadata(
            skill
        )
        canonical_branch = exact_source_branch(skill)
        validated_assets = (
            validated_published_asset_fields(skill) if not source_error and canonical_branch else {}
        )
        for field in ASSET_FIELDS:
            skill.pop(field, None)
        if validated_assets:
            skill.update(
                {
                    "repo": canonical_repo,
                    "path": canonical_path,
                    "branch": canonical_branch,
                }
            )
        skill.update(validated_assets)
        repo = skill.get("repo", "")
        path = skill.get("path", "")
        name = skill.get("name", "unknown")
        if repo and path:
            skill["install"] = f"{repo}/{path}"
        elif repo:
            skill["install"] = repo
        elif path:
            skill["install"] = f"local/{path}"
        else:
            skill["install"] = f"local/{name}"

    return skills


def load_from_registry(registry_path: Path) -> List[Dict]:
    """Load skills from registry.json or its manifest shards (fallback mode)."""
    with open(registry_path, "r", encoding="utf-8") as f:
        registry = json.load(f)

    skills = registry.get("skills")
    if not isinstance(skills, list):
        skills = load_registry_manifest_shards(registry_path, registry)

    return add_registry_install_fields(skills)
