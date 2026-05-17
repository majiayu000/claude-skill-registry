#!/usr/bin/env python3
"""Writers for bounded static Pages index artifacts."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from rebuild_registry import artifact_reference, file_sha256, safe_write_gzip_json, safe_write_json

DEFAULT_PART_TARGET_BYTES = 8 * 1024 * 1024


@dataclass(frozen=True)
class SearchArtifactStats:
    shard_count: int
    largest_shard_bytes: int
    largest_shard_gzip_bytes: int
    index_size_bytes: int
    index_size_gzip_bytes: int


@dataclass(frozen=True)
class CategoryArtifactStats:
    categories: list[dict]
    shard_count: int
    largest_part_bytes: int
    largest_part_gzip_bytes: int


def compact_json_bytes(payload: object) -> bytes:
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip().lower()).strip("-._")
    return slug or "other"


def remove_generated_children(path: Path) -> int:
    if not path.exists():
        return 0

    removed = 0
    for child in path.iterdir():
        if child.is_symlink() or child.is_file():
            child.unlink()
        elif child.is_dir():
            shutil.rmtree(child)
        removed += 1
    return removed


def chunk_records(records: list[dict], target_bytes: int = DEFAULT_PART_TARGET_BYTES) -> list[list[dict]]:
    if target_bytes <= 0:
        raise ValueError("target_bytes must be positive")
    if not records:
        return []

    chunks: list[list[dict]] = []
    current: list[dict] = []
    current_size = 2

    for record in records:
        record_size = len(compact_json_bytes(record))
        added_size = record_size + (1 if current else 0)
        if current and current_size + added_size > target_bytes:
            chunks.append(current)
            current = []
            current_size = 2

        current.append(record)
        current_size += record_size + (1 if len(current) > 1 else 0)

    if current:
        chunks.append(current)
    return chunks


def build_part_entry(path: Path, gzip_path: Path, count: int, base_dir: Path) -> dict:
    return {
        "path": artifact_reference(path, base_dir),
        "gzip_path": artifact_reference(gzip_path, base_dir),
        "count": count,
        "bytes": path.stat().st_size,
        "gzip_bytes": gzip_path.stat().st_size,
        "sha256": file_sha256(path),
    }


def write_search_artifacts(
    search_records: list[dict],
    output_dir: Path,
    *,
    version: str,
    updated_at: str,
    target_part_bytes: int = DEFAULT_PART_TARGET_BYTES,
) -> SearchArtifactStats:
    output_dir.mkdir(parents=True, exist_ok=True)
    shards_dir = output_dir / "search-shards"
    remove_generated_children(shards_dir)
    shards_dir.mkdir(parents=True, exist_ok=True)

    chunks = chunk_records(search_records, target_part_bytes)
    part_count = len(chunks)
    shard_entries: list[dict] = []

    for idx, chunk in enumerate(chunks):
        payload = {
            "schema_version": 1,
            "v": version,
            "part": idx,
            "part_count": part_count,
            "count": len(chunk),
            "s": chunk,
        }
        part_path = shards_dir / f"part-{idx:03d}.json"
        gzip_path = shards_dir / f"part-{idx:03d}.json.gz"
        safe_write_json(part_path, payload)
        safe_write_gzip_json(gzip_path, payload)
        shard_entries.append(build_part_entry(part_path, gzip_path, len(chunk), output_dir))

    manifest = {
        "schema_version": 1,
        "v": version,
        "updated_at": updated_at,
        "total_count": len(search_records),
        "shard_strategy": "bounded-sequential-stars-desc",
        "record_schema": "search-mini-v2",
        "shard_count": part_count,
        "largest_shard_bytes": max((entry["bytes"] for entry in shard_entries), default=0),
        "largest_shard_gzip_bytes": max(
            (entry["gzip_bytes"] for entry in shard_entries),
            default=0,
        ),
        "shards": shard_entries,
    }
    safe_write_json(output_dir / "search-index-manifest.json", manifest)

    pointer = {
        "v": version,
        "t": len(search_records),
        "deprecated_full_payload": True,
        "manifest": "search-index-manifest.json",
        "message": "Full search payload moved to search-shards/*.json",
    }
    index_path = output_dir / "search-index.json"
    index_gz_path = output_dir / "search-index.json.gz"
    safe_write_json(index_path, pointer)
    safe_write_gzip_json(index_gz_path, pointer)

    return SearchArtifactStats(
        shard_count=part_count,
        largest_shard_bytes=manifest["largest_shard_bytes"],
        largest_shard_gzip_bytes=manifest["largest_shard_gzip_bytes"],
        index_size_bytes=index_path.stat().st_size,
        index_size_gzip_bytes=index_gz_path.stat().st_size,
    )


def write_category_artifacts(
    categories: dict[str, list[dict]],
    categories_dir: Path,
    *,
    updated_at: str,
    category_code: Callable[[str], str],
    target_part_bytes: int = DEFAULT_PART_TARGET_BYTES,
) -> CategoryArtifactStats:
    categories_dir.mkdir(parents=True, exist_ok=True)
    remove_generated_children(categories_dir)
    categories_dir.mkdir(parents=True, exist_ok=True)

    category_entries: list[dict] = []
    total_part_count = 0
    largest_part_bytes = 0
    largest_part_gzip_bytes = 0

    for category, cat_skills in sorted(categories.items()):
        code = category_code(category)
        slug = safe_slug(category)
        category_dir = categories_dir / slug
        category_dir.mkdir(parents=True, exist_ok=True)

        sorted_skills = sorted(
            cat_skills,
            key=lambda item: (
                -int(item.get("stars", 0) or 0),
                str(item.get("name", "")).lower(),
                str(item.get("install", "")),
            ),
        )
        chunks = chunk_records(sorted_skills, target_part_bytes)
        part_entries: list[dict] = []
        part_count = len(chunks)

        for idx, chunk in enumerate(chunks):
            payload = {
                "schema_version": 1,
                "category": category,
                "code": code,
                "updated_at": updated_at,
                "part": idx,
                "part_count": part_count,
                "count": len(chunk),
                "skills": chunk,
            }
            part_path = category_dir / f"part-{idx:03d}.json"
            gzip_path = category_dir / f"part-{idx:03d}.json.gz"
            safe_write_json(part_path, payload)
            safe_write_gzip_json(gzip_path, payload)
            entry = build_part_entry(part_path, gzip_path, len(chunk), categories_dir.parent)
            part_entries.append(entry)
            largest_part_bytes = max(largest_part_bytes, entry["bytes"])
            largest_part_gzip_bytes = max(largest_part_gzip_bytes, entry["gzip_bytes"])

        manifest_path = category_dir / "manifest.json"
        manifest = {
            "schema_version": 1,
            "category": category,
            "code": code,
            "updated_at": updated_at,
            "count": len(sorted_skills),
            "part_count": part_count,
            "largest_part_bytes": max((entry["bytes"] for entry in part_entries), default=0),
            "largest_part_gzip_bytes": max(
                (entry["gzip_bytes"] for entry in part_entries),
                default=0,
            ),
            "parts": part_entries,
        }
        safe_write_json(manifest_path, manifest)

        pointer_path = categories_dir / f"{slug}.json"
        pointer = {
            "category": category,
            "code": code,
            "count": len(sorted_skills),
            "updated_at": updated_at,
            "deprecated_full_payload": True,
            "manifest": artifact_reference(manifest_path, categories_dir.parent),
            "message": "Category payload moved to category manifest parts",
        }
        safe_write_json(pointer_path, pointer)

        category_entries.append(
            {
                "name": category,
                "code": code,
                "count": len(sorted_skills),
                "path": artifact_reference(pointer_path, categories_dir.parent),
                "manifest": artifact_reference(manifest_path, categories_dir.parent),
                "part_count": part_count,
                "largest_part_bytes": manifest["largest_part_bytes"],
                "largest_part_gzip_bytes": manifest["largest_part_gzip_bytes"],
            }
        )
        total_part_count += part_count

    safe_write_json(
        categories_dir / "index.json",
        {
            "updated_at": updated_at,
            "categories": category_entries,
        },
    )

    return CategoryArtifactStats(
        categories=category_entries,
        shard_count=total_part_count,
        largest_part_bytes=largest_part_bytes,
        largest_part_gzip_bytes=largest_part_gzip_bytes,
    )
