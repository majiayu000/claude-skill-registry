#!/usr/bin/env python3
"""Source loaders for search index generation."""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

from category_taxonomy import resolve_category
from utils import (
    extract_description,
    get_repo_suffix,
    is_declared_bundled_skill_file,
    load_metadata,
)

logger = logging.getLogger(__name__)


def scan_skills_v2(skills_dir: Path) -> List[Dict]:
    """Recursively scan archive root and index one entry per archive skill."""
    skills = []

    if not skills_dir.exists():
        logger.warning(f"Skills directory not found: {skills_dir}")
        return skills

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
