#!/usr/bin/env python3
"""Independent registry shard identity and record-placement checks."""

from __future__ import annotations

import hashlib

CANONICAL_REGISTRY_SHARD_IDS = frozenset(f"{index:02x}" for index in range(256))


def _skill_install_key(skill: dict) -> str:
    repo = skill.get("repo", "")
    path = skill.get("path", "")
    name = skill.get("name", "unknown")
    category = skill.get("category", "other")
    if repo and path:
        return f"{repo}/{path}"
    if repo:
        return str(repo)
    if path:
        return f"local/{path}"
    return f"local/{category}/{name}"


def _record_shard_id(skill: dict) -> str:
    branch = skill.get("branch", "main") or "main"
    key = f"{_skill_install_key(skill)}|{branch}".encode()
    return hashlib.sha256(key).hexdigest()[:2]


def registry_entry_errors(entry: dict, seen_ids: set[str]) -> tuple[str, ...]:
    shard_id = entry.get("id")
    if not isinstance(shard_id, str) or shard_id not in CANONICAL_REGISTRY_SHARD_IDS:
        return ("invalid_registry_shard_id",)
    errors: list[str] = []
    if shard_id in seen_ids:
        errors.append("duplicate_registry_shard_id")
    seen_ids.add(shard_id)
    if entry.get("path") != f"registry-shards/{shard_id}.json":
        errors.append("registry_shard_path_mismatch")
    if entry.get("gzip_path") != f"registry-shards/{shard_id}.json.gz":
        errors.append("registry_shard_path_mismatch")
    return tuple(dict.fromkeys(errors))


def registry_payload_errors(entry: dict, payload: dict) -> tuple[str, ...]:
    shard_id = entry.get("id")
    errors: set[str] = set()
    if payload.get("shard") != shard_id:
        errors.add("registry_shard_identity_mismatch")
    skills = payload.get("skills")
    if isinstance(skills, list):
        for skill in skills:
            if not isinstance(skill, dict) or _record_shard_id(skill) != shard_id:
                errors.add("registry_record_placement_mismatch")
    return tuple(sorted(errors))


def registry_shard_set_is_complete(shard_ids: set[str], entry_count: int) -> bool:
    return entry_count == 256 and shard_ids == CANONICAL_REGISTRY_SHARD_IDS
