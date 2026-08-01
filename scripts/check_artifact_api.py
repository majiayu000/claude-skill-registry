#!/usr/bin/env python3
"""Validate the complete static-artifact-api-v1 publish tree."""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any

import check_registry_shard_placement as registry_placement
from artifact_api_records import is_int, search_key_errors

POINTER_REQUIRED = {
    "schema_version",
    "total_count",
    "deprecated_full_payload",
    "message",
    "manifest",
    "replacement",
    "compat_since",
    "compat_until",
}
COUNT_ALIASES = {"t", "count", "registry_skill_count_dedup"}
ENTRY_REQUIRED = {"path", "gzip_path", "count", "bytes", "gzip_bytes", "sha256"}
POINTER_EXTRA_FIELDS = {
    "registry": {
        "version",
        "updated_at",
        "plugin_count",
        "archive_skill_md_count_raw",
        "archive_metadata_count_raw",
        "registry_skill_count_dedup",
    },
    "search": {"v", "t"},
    "signal": {"updated_at", "count"},
    "category": {"category", "code", "updated_at", "count"},
}
SHARD_SEMANTICS = {
    "search-index.json": ("bounded-sequential-stars-desc", "search-mini-v2"),
    "quality-index.json": ("bounded-sequential-scan-order", "quality-v1"),
    "security-index.json": ("bounded-sequential-scan-order", "security-v1"),
    "ranking-index.json": ("bounded-sequential-score-desc", "ranking-v1"),
}

@dataclass(frozen=True)
class ArtifactError:
    code: str
    path: str
    message: str

@dataclass(frozen=True)
class ValidationReport:
    checked_files: int
    totals: dict[str, list[int]]
    errors: list[ArtifactError]
    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "status": "failed" if self.errors else "complete",
            "checked_files": self.checked_files,
            "totals": self.totals,
            "errors": [asdict(error) for error in self.errors],
        }

class ArtifactValidator:
    def __init__(self, root: Path, docs_dir: Path) -> None:
        self.root = root.resolve()
        self.docs = docs_dir.resolve()
        self.errors: list[ArtifactError] = []
        self.checked: set[Path] = set()
        self.totals: dict[str, list[int]] = {"registry": [], "scan": [], "stable": []}
    def error(self, code: str, path: str | Path, message: str) -> None:
        display = path.as_posix() if isinstance(path, Path) else path
        self.errors.append(ArtifactError(code=code, path=display, message=message))
    def require_fields(
        self,
        payload: dict,
        path: str,
        *,
        required: set[str],
        optional: set[str] | None = None,
        code: str = "invalid_shape",
    ) -> None:
        missing = sorted(required - payload.keys())
        unknown = sorted(payload.keys() - required - (optional or set()))
        if missing:
            self.error(code, path, f"missing field count={len(missing)}")
        if unknown:
            self.error(code, path, f"unknown field count={len(unknown)}")
    def resolve_file(self, base: Path, reference: object, owner: str) -> Path | None:
        if not isinstance(reference, str) or not reference or "\\" in reference:
            self.error("invalid_path", owner, "artifact path must be a non-empty POSIX string")
            return None
        pure = PurePosixPath(reference)
        if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
            self.error("path_escape", owner, "artifact path must remain inside publish root")
            return None
        candidate = base.joinpath(*pure.parts)
        current = base
        for part in pure.parts:
            current = current / part
            if current.is_symlink():
                self.error("non_regular_file", owner, "artifact path must not traverse symlinks")
                return None
        try:
            resolved = candidate.resolve(strict=True)
            resolved.relative_to(base)
        except (FileNotFoundError, RuntimeError, ValueError):
            self.error("missing_or_escaped_path", owner, "referenced artifact is missing or escaped")
            return None
        if candidate.is_symlink() or not resolved.is_file():
            self.error("non_regular_file", owner, "artifact must be a regular non-symlink file")
            return None
        self.checked.add(resolved)
        return resolved
    def load_json(self, base: Path, reference: object, owner: str) -> tuple[Path, dict] | None:
        path = self.resolve_file(base, reference, owner)
        if path is None:
            return None
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            self.error("invalid_json", owner, "invalid UTF-8 JSON")
            return None
        if not isinstance(payload, dict):
            self.error("invalid_shape", owner, "top-level JSON must be an object")
            return None
        return path, payload
    def require_schema(self, payload: dict, path: str) -> bool:
        if payload.get("schema_version") != 1:
            self.error("unknown_schema", path, "schema_version must equal 1")
            return False
        return True
    def require_count(self, payload: dict, key: str, path: str) -> int | None:
        value = payload.get(key)
        if not is_int(value):
            self.error("invalid_count", path, "count field must be a non-negative integer")
            return None
        return value
    def require_nonempty(self, payload: dict, key: str, path: str) -> str | None:
        value = payload.get(key)
        if not isinstance(value, str) or not value:
            self.error("invalid_identity", path, "identity field must be a non-empty string")
            return None
        return value
    def check_pointer(
        self,
        base: Path,
        pointer_path: str,
        *,
        kind: str,
        aliases: set[str],
    ) -> dict | None:
        loaded = self.load_json(base, pointer_path, pointer_path)
        if loaded is None:
            return None
        _, pointer = loaded
        self.require_schema(pointer, pointer_path)
        self.require_fields(
            pointer,
            pointer_path,
            required=POINTER_REQUIRED,
            optional=POINTER_EXTRA_FIELDS[kind],
            code="invalid_pointer_shape",
        )
        total = self.require_count(pointer, "total_count", pointer_path)
        if kind == "registry":
            for key in ("plugin_count", "archive_skill_md_count_raw", "archive_metadata_count_raw"):
                self.require_count(pointer, key, pointer_path)
            for key in ("version", "updated_at"):
                self.require_nonempty(pointer, key, pointer_path)
        elif kind == "search":
            self.require_nonempty(pointer, "v", pointer_path)
        else:
            self.require_nonempty(pointer, "updated_at", pointer_path)
        if pointer.get("deprecated_full_payload") is not True:
            self.error("invalid_pointer", pointer_path, "deprecated_full_payload must be true")
        for key in ("message", "manifest", "replacement", "compat_since", "compat_until"):
            if not isinstance(pointer.get(key), str) or not pointer[key]:
                self.error("invalid_pointer", pointer_path, "pointer string field must be non-empty")
        replacement = pointer.get("replacement")
        if isinstance(replacement, str):
            pure_replacement = PurePosixPath(replacement)
            if (
                pure_replacement.is_absolute()
                or "\\" in replacement
                or "://" in replacement
                or any(part in {"", ".", ".."} for part in pure_replacement.parts)
            ):
                self.error("invalid_replacement", pointer_path, "replacement must be a safe relative pattern")
        if pointer.get("compat_since") != "static-artifact-api-v1" or pointer.get(
            "compat_until"
        ) != "static-artifact-api-v2":
            self.error("invalid_compat_window", pointer_path, "unsupported compatibility window")
        if any(key in pointer for key in ("skills", "records", "s")):
            self.error("pointer_contains_payload", pointer_path, "pointer must not contain full payload")
        for alias in COUNT_ALIASES:
            if alias in pointer and alias not in aliases:
                self.error("unknown_count_alias", pointer_path, "count alias is not allowed")
            elif alias in pointer:
                alias_count = self.require_count(pointer, alias, pointer_path)
                if total is not None and alias_count != total:
                    self.error(
                        "count_alias_conflict",
                        pointer_path,
                        "count alias conflicts with total_count",
                    )
        return pointer
    def check_file_entry(
        self,
        base: Path,
        entry: object,
        owner: str,
        *,
        allowed_fields: set[str],
        required_fields: set[str] | None = None,
    ) -> tuple[dict, dict] | None:
        if not isinstance(entry, dict):
            self.error("invalid_entry", owner, "manifest entry must be an object")
            return None
        self.require_fields(
            entry,
            owner,
            required=required_fields or ENTRY_REQUIRED,
            optional=allowed_fields - (required_fields or ENTRY_REQUIRED),
            code="invalid_entry_shape",
        )
        count = self.require_count(entry, "count", owner)
        plain = self.resolve_file(base, entry.get("path"), owner)
        compressed = self.resolve_file(base, entry.get("gzip_path"), owner)
        if plain is None or compressed is None or count is None:
            return None
        if entry.get("bytes") != plain.stat().st_size:
            self.error("bytes_mismatch", owner, "bytes does not match file size")
        if entry.get("gzip_bytes") != compressed.stat().st_size:
            self.error("gzip_bytes_mismatch", owner, "gzip_bytes does not match file size")
        digest = hashlib.sha256(plain.read_bytes()).hexdigest()
        if entry.get("sha256") != digest:
            self.error("sha256_mismatch", owner, "sha256 does not match file")
        try:
            plain_payload = json.loads(plain.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            self.error("invalid_json", owner, "plain artifact is invalid JSON")
            return None
        try:
            with gzip.open(compressed, "rt", encoding="utf-8") as handle:
                gzip_payload = json.load(handle)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, gzip.BadGzipFile):
            self.error("invalid_gzip", owner, "gzip artifact is invalid")
            return None
        if plain_payload != gzip_payload:
            self.error("gzip_payload_mismatch", owner, "gzip JSON differs from plain JSON")
        if not isinstance(plain_payload, dict):
            self.error("invalid_shape", owner, "payload must be an object")
            return None
        return entry, plain_payload
    def check_duplicate_entry_references(
        self,
        entry: dict,
        seen: set[str],
        owner: str,
    ) -> None:
        for key in ("path", "gzip_path"):
            value = entry.get(key)
            if not isinstance(value, str):
                continue
            if value in seen:
                self.error("duplicate_reference", owner, f"manifest repeats {key}")
            seen.add(value)
    def check_sharded(
        self,
        base: Path,
        pointer_path: str,
        *,
        kind: str,
        aliases: set[str],
    ) -> int | None:
        pointer = self.check_pointer(base, pointer_path, kind=kind, aliases=aliases)
        if pointer is None or not isinstance(pointer.get("manifest"), str):
            return None
        expected_manifest = (
            "registry-manifest.json"
            if kind == "registry"
            else pointer_path.removesuffix(".json") + "-manifest.json"
        )
        expected_replacement = (
            "registry-shards/*.json"
            if kind == "registry"
            else pointer_path.removesuffix("-index.json") + "-shards/part-*.json"
        )
        if pointer.get("manifest") != expected_manifest or pointer.get("replacement") != expected_replacement:
            self.error("invalid_pointer_identity", pointer_path, "pointer target identity is invalid")
        manifest_owner = f"{pointer_path}#manifest"
        loaded = self.load_json(base, pointer["manifest"], manifest_owner)
        if loaded is None:
            return None
        _, manifest = loaded
        self.require_schema(manifest, manifest_owner)
        if kind == "registry":
            self.require_fields(
                manifest,
                manifest_owner,
                required={
                    "schema_version",
                    "generated_at",
                    "total_count",
                    "plugin_count",
                    "shard_strategy",
                    "shard_count",
                    "record_key",
                    "provenance",
                    "summary",
                    "shards",
                    "plugins",
                },
                code="invalid_manifest_shape",
            )
        else:
            common_fields = {
                "schema_version",
                "updated_at",
                "total_count",
                "shard_strategy",
                "record_schema",
                "shard_count",
                "largest_shard_bytes",
                "largest_shard_gzip_bytes",
                "shards",
            }
            self.require_fields(
                manifest,
                manifest_owner,
                required=common_fields | ({"v"} if kind == "search" else set()),
                code="invalid_manifest_shape",
            )
        total = self.require_count(manifest, "total_count", manifest_owner)
        if total is not None and pointer.get("total_count") != total:
            self.error("pointer_manifest_count_mismatch", pointer_path, "pointer and manifest totals differ")
        entries = manifest.get("shards")
        entry_count = self.require_count(manifest, "shard_count", manifest_owner)
        for size_key in ("largest_shard_bytes", "largest_shard_gzip_bytes"):
            if kind != "registry":
                self.require_count(manifest, size_key, manifest_owner)
        if kind == "registry":
            plugin_count = self.require_count(manifest, "plugin_count", manifest_owner)
            pointer_plugin_count = self.require_count(pointer, "plugin_count", pointer_path)
            if plugin_count is not None and pointer_plugin_count != plugin_count:
                self.error("plugin_count_mismatch", pointer_path, "pointer and manifest plugin counts differ")
            provenance = manifest.get("provenance")
            provenance_fields = {"core_repo", "core_sha", "data_repo", "data_sha"}
            provenance_ok = isinstance(provenance, dict) and (
                not provenance
                or set(provenance) == provenance_fields
                and all(isinstance(provenance[key], str) and provenance[key] for key in provenance_fields)
            )
            if (
                manifest.get("shard_strategy") != "sha256-install-branch-prefix"
                or manifest.get("record_key") != "install|branch"
                or not provenance_ok
            ):
                self.error("invalid_manifest_semantics", manifest_owner, "registry manifest semantics are invalid")
            self.require_nonempty(manifest, "generated_at", manifest_owner)
            if manifest.get("summary") != "registry_summary.json":
                self.error("invalid_manifest_semantics", manifest_owner, "registry summary identity is invalid")
            self.resolve_file(base, manifest.get("summary"), manifest_owner)
            plugins = manifest.get("plugins")
            if not isinstance(plugins, dict):
                self.error("invalid_manifest", manifest_owner, "plugins must be an object")
            else:
                self.require_fields(
                    plugins,
                    f"{manifest_owner}#plugins",
                    required={"path", "count"},
                    code="invalid_manifest_shape",
                )
                plugins_count = self.require_count(
                    plugins, "count", f"{manifest_owner}#plugins"
                )
                if plugin_count is not None and plugins_count != plugin_count:
                    self.error(
                        "plugin_count_mismatch",
                        manifest_owner,
                        "plugins entry count differs from manifest",
                    )
                if plugins.get("path") != "sources/plugins.json":
                    self.error("invalid_manifest_semantics", manifest_owner, "plugin source identity is invalid")
                self.resolve_file(base, plugins.get("path"), manifest_owner)
        else:
            expected_strategy, expected_schema = SHARD_SEMANTICS[pointer_path]
            if manifest.get("shard_strategy") != expected_strategy or manifest.get("record_schema") != expected_schema:
                self.error("invalid_manifest_semantics", manifest_owner, "shard semantics are invalid")
            updated_at = self.require_nonempty(manifest, "updated_at", manifest_owner)
            identity_key = "v" if kind == "search" else "updated_at"
            if kind == "search":
                self.require_nonempty(manifest, "v", manifest_owner)
            if pointer.get(identity_key) != manifest.get(identity_key) or updated_at is None:
                self.error("manifest_identity_mismatch", manifest_owner, "pointer and manifest identity differ")
        if not isinstance(entries, list):
            self.error("invalid_manifest", manifest_owner, "shards must be a list")
            return total
        if entry_count is not None and entry_count != len(entries):
            self.error("entry_count_mismatch", manifest_owner, "shard_count differs from entries")
        seen: set[str] = set()
        search_keys: set[tuple[str, str]] = set()
        registry_ids: set[str] = set()
        actual_total = 0
        payload_key = "skills" if kind == "registry" else "s" if kind == "search" else "records"
        for index, raw_entry in enumerate(entries):
            owner = f"{pointer_path}#entry-{index}"
            allowed = {"path", "gzip_path", "count", "bytes", "gzip_bytes", "sha256"}
            required = set(allowed)
            if kind == "registry":
                allowed.add("id")
                required.add("id")
            checked = self.check_file_entry(
                base,
                raw_entry,
                owner,
                allowed_fields=allowed,
                required_fields=required,
            )
            if not isinstance(raw_entry, dict):
                continue
            if kind == "registry":
                for code in registry_placement.registry_entry_errors(raw_entry, registry_ids):
                    self.error(code, owner, "registry shard placement is invalid")
            self.check_duplicate_entry_references(raw_entry, seen, owner)
            if is_int(raw_entry.get("count")):
                actual_total += raw_entry["count"]
            if checked is None:
                continue
            entry, payload = checked
            self.require_schema(payload, owner)
            expected_fields = {"schema_version", "count", payload_key}
            if kind == "registry":
                expected_fields |= {"shard", "generated_at"}
                for code in registry_placement.registry_payload_errors(entry, payload):
                    self.error(code, owner, "registry shard placement is invalid")
                identity_ok = payload.get("generated_at") == manifest.get("generated_at")
            else:
                expected_fields |= {"part", "part_count"}
                if kind == "search":
                    expected_fields.add("v")
                    version_ok = payload.get("v") == manifest.get("v")
                else:
                    expected_fields.add("updated_at")
                    version_ok = payload.get("updated_at") == manifest.get("updated_at")
                identity_ok = (
                    payload.get("part") == index
                    and payload.get("part_count") == len(entries)
                    and version_ok
                )
            self.require_fields(payload, owner, required=expected_fields, code="unknown_payload_field")
            records = payload.get(payload_key)
            payload_count = self.require_count(payload, "count", owner)
            if kind != "registry":
                self.require_count(payload, "part_count", owner)
            if not identity_ok:
                self.error("payload_identity_mismatch", owner, "payload identity is invalid")
            if not isinstance(records, list):
                self.error("invalid_payload_key", owner, "payload array must be a list")
            elif payload_count != entry.get("count") or len(records) != entry.get("count"):
                self.error("payload_count_mismatch", owner, "payload count differs from entry")
            if kind == "search":
                for code in search_key_errors(records, search_keys):
                    self.error(code, owner, "search record stable key is invalid")
        if total is not None and actual_total != total:
            self.error("manifest_total_mismatch", manifest_owner, "entry counts do not sum to total_count")
        if kind == "registry" and not registry_placement.registry_shard_set_is_complete(registry_ids, len(entries)):
            self.error("registry_shard_set_mismatch", manifest_owner, "registry shard set is incomplete")
        return total
    def check_categories(self) -> int | None:
        loaded = self.load_json(self.docs, "categories/index.json", "categories/index.json")
        if loaded is None:
            return None
        _, index_payload = loaded
        self.require_schema(index_payload, "categories/index.json")
        self.require_fields(
            index_payload,
            "categories/index.json",
            required={
                "schema_version",
                "updated_at",
                "total_count",
                "category_count",
                "categories",
            },
            code="invalid_category_index_shape",
        )
        total = self.require_count(index_payload, "total_count", "categories/index.json")
        index_updated_at = self.require_nonempty(index_payload, "updated_at", "categories/index.json")
        categories = index_payload.get("categories")
        category_count = self.require_count(index_payload, "category_count", "categories/index.json")
        if not isinstance(categories, list):
            self.error("invalid_category_index", "categories/index.json", "categories must be a list")
            return total
        if category_count is not None and category_count != len(categories):
            self.error("category_count_mismatch", "categories/index.json", "category_count differs from entries")
        manifest_total = 0
        seen_paths: set[str] = set()
        for index, category in enumerate(categories):
            owner = f"categories/index.json#{index}"
            if not isinstance(category, dict):
                self.error("invalid_category_entry", owner, "category entry must be an object")
                continue
            self.require_fields(
                category,
                owner,
                required={
                    "name",
                    "code",
                    "count",
                    "path",
                    "manifest",
                    "part_count",
                    "largest_part_bytes",
                    "largest_part_gzip_bytes",
                },
                code="invalid_category_entry_shape",
            )
            for key in ("name", "code", "path", "manifest"):
                if not isinstance(category.get(key), str) or not category[key]:
                    self.error("invalid_category_entry", owner, f"{key} must be a non-empty string")
            entry_total = self.require_count(category, "count", owner)
            self.require_count(category, "part_count", owner)
            self.require_count(category, "largest_part_bytes", owner)
            self.require_count(category, "largest_part_gzip_bytes", owner)
            pointer_path = category.get("path")
            if not isinstance(pointer_path, str):
                continue
            if pointer_path in seen_paths:
                self.error("duplicate_reference", owner, "category pointer path is duplicated")
            seen_paths.add(pointer_path)
            pointer = self.check_pointer(
                self.docs,
                pointer_path,
                kind="category",
                aliases={"count"},
            )
            if pointer is None or not isinstance(pointer.get("manifest"), str):
                continue
            if (
                pointer.get("manifest") != category.get("manifest")
                or pointer.get("category") != category.get("name")
                or pointer.get("code") != category.get("code")
                or pointer.get("updated_at") != index_updated_at
            ):
                self.error("category_manifest_mismatch", pointer_path, "index and pointer manifests differ")
            expected_replacement = pointer_path.removesuffix(".json") + "/part-*.json"
            if pointer.get("replacement") != expected_replacement:
                self.error("invalid_pointer_identity", pointer_path, "category replacement is invalid")
            manifest_owner = f"{pointer_path}#manifest"
            manifest_loaded = self.load_json(self.docs, pointer["manifest"], manifest_owner)
            if manifest_loaded is None:
                continue
            _, manifest = manifest_loaded
            self.require_schema(manifest, manifest_owner)
            self.require_fields(
                manifest,
                manifest_owner,
                required={
                    "schema_version",
                    "category",
                    "code",
                    "updated_at",
                    "total_count",
                    "count",
                    "part_count",
                    "part_strategy",
                    "largest_part_bytes",
                    "largest_part_gzip_bytes",
                    "parts",
                },
                code="invalid_manifest_shape",
            )
            manifest_count = self.require_count(manifest, "total_count", manifest_owner)
            alias_count = self.require_count(manifest, "count", manifest_owner)
            manifest_parts = self.require_count(manifest, "part_count", manifest_owner)
            self.require_count(manifest, "largest_part_bytes", manifest_owner)
            self.require_count(manifest, "largest_part_gzip_bytes", manifest_owner)
            if manifest_count is not None:
                manifest_total += manifest_count
            if len({entry_total, pointer.get("total_count"), manifest_count, alias_count}) != 1:
                self.error("category_total_mismatch", pointer_path, "category totals differ")
            if (
                manifest.get("part_strategy") != "bounded-sequential-stars-desc"
                or manifest.get("category") != category.get("name")
                or manifest.get("code") != category.get("code")
                or manifest.get("updated_at") != index_updated_at
                or manifest_parts != category.get("part_count")
            ):
                self.error("category_identity_mismatch", manifest_owner, "category identity is invalid")
            parts = manifest.get("parts")
            part_count = manifest_parts
            if not isinstance(parts, list):
                self.error("invalid_manifest", manifest_owner, "parts must be a list")
                continue
            if part_count != len(parts):
                self.error("entry_count_mismatch", manifest_owner, "part_count differs from entries")
            part_total = 0
            seen_parts: set[str] = set()
            for part_index, raw_entry in enumerate(parts):
                part_owner = f"{pointer_path}#part-{part_index}"
                checked = self.check_file_entry(
                    self.docs,
                    raw_entry,
                    part_owner,
                    allowed_fields={"path", "gzip_path", "count", "bytes", "gzip_bytes", "sha256"},
                )
                if not isinstance(raw_entry, dict):
                    continue
                if is_int(raw_entry.get("count")):
                    part_total += raw_entry["count"]
                self.check_duplicate_entry_references(raw_entry, seen_parts, part_owner)
                if checked is None:
                    continue
                entry, payload = checked
                self.require_schema(payload, part_owner)
                expected = {"schema_version", "category", "code", "updated_at", "part", "part_count", "count", "skills"}
                self.require_fields(
                    payload,
                    part_owner,
                    required=expected,
                    code="unknown_payload_field",
                )
                skills = payload.get("skills")
                payload_count = self.require_count(payload, "count", part_owner)
                self.require_count(payload, "part_count", part_owner)
                if (
                    payload.get("part") != part_index
                    or payload.get("part_count") != len(parts)
                    or payload.get("category") != manifest.get("category")
                    or payload.get("code") != manifest.get("code")
                    or payload.get("updated_at") != manifest.get("updated_at")
                ):
                    self.error("payload_identity_mismatch", part_owner, "category part identity is invalid")
                if not isinstance(skills, list):
                    self.error("invalid_payload_key", part_owner, "payload array must be a list")
                elif payload_count != entry.get("count") or len(skills) != entry.get("count"):
                    self.error("payload_count_mismatch", part_owner, "category payload count differs")
            if manifest_count is not None and part_total != manifest_count:
                self.error("manifest_total_mismatch", manifest_owner, "part counts do not sum to total_count")
        if total is not None and manifest_total != total:
            self.error("category_index_total_mismatch", "categories/index.json", "category totals do not sum to total_count")
        return total
    def check_counted_document(self, path: str, fields: set[str], payload_key: str) -> None:
        loaded = self.load_json(self.docs, path, path)
        if loaded is None:
            return
        _, payload = loaded
        if "schema_version" in fields:
            self.require_schema(payload, path)
        self.require_fields(payload, path, required=fields, code="invalid_public_document_shape")
        self.require_nonempty(payload, "updated_at", path)
        count = self.require_count(payload, "count", path)
        records = payload.get(payload_key)
        if not isinstance(records, list) or count is None or len(records) != count:
            self.error("public_document_count_mismatch", path, "payload count is invalid")
    def check_simple_documents(self) -> tuple[int | None, int | None, int | None]:
        lite_loaded = self.load_json(self.docs, "search-index-lite.json", "search-index-lite.json")
        stats_loaded = self.load_json(self.docs, "stats.json", "stats.json")
        summary_loaded = self.load_json(self.root, "registry_summary.json", "registry_summary.json")
        self.check_counted_document(
            "featured.json", {"schema_version", "updated_at", "count", "skills"}, "skills"
        )
        self.check_counted_document("plugins.json", {"updated_at", "count", "plugins"}, "plugins")
        lite_total = stats_registry = summary_total = None
        if lite_loaded:
            _, lite = lite_loaded
            self.require_schema(lite, "search-index-lite.json")
            self.require_fields(
                lite,
                "search-index-lite.json",
                required={
                    "schema_version",
                    "version",
                    "updated_at",
                    "total_count",
                    "included_count",
                    "limit",
                    "raw_count",
                    "dedupe_key",
                    "skills",
                },
                code="invalid_lite_shape",
            )
            lite_total = self.require_count(lite, "total_count", "search-index-lite.json")
            included = self.require_count(lite, "included_count", "search-index-lite.json")
            self.require_count(lite, "limit", "search-index-lite.json")
            self.require_count(lite, "raw_count", "search-index-lite.json")
            skills = lite.get("skills")
            if not isinstance(skills, list) or included is None or len(skills) != included:
                self.error("lite_payload_count_mismatch", "search-index-lite.json", "skills length differs from included_count")
            if lite_total is not None and included is not None and included > lite_total:
                self.error("lite_count_mismatch", "search-index-lite.json", "included_count exceeds total_count")
        if stats_loaded:
            _, stats = stats_loaded
            self.require_schema(stats, "stats.json")
            required_stats = {
                "schema_version",
                "registry_skill_count_dedup",
                "indexed_skill_count_scan_shape",
                "lite_index_count",
            }
            missing_stats = sorted(required_stats - stats.keys())
            if missing_stats:
                self.error("invalid_stats_shape", "stats.json", f"missing field count={len(missing_stats)}")
            stats_registry = self.require_count(stats, "registry_skill_count_dedup", "stats.json")
            scan_count = self.require_count(stats, "indexed_skill_count_scan_shape", "stats.json")
            stable_count = self.require_count(stats, "lite_index_count", "stats.json")
            if scan_count is not None:
                self.totals["scan"].append(scan_count)
            if stable_count is not None:
                self.totals["stable"].append(stable_count)
        if summary_loaded:
            _, summary = summary_loaded
            self.require_schema(summary, "registry_summary.json")
            self.require_fields(
                summary,
                "registry_summary.json",
                required={"schema_version", "registry_updated_at", "total_count", "plugin_count"},
                code="invalid_summary_shape",
            )
            summary_total = self.require_count(summary, "total_count", "registry_summary.json")
            self.require_count(summary, "plugin_count", "registry_summary.json")
        return lite_total, stats_registry, summary_total
    def validate(self) -> ValidationReport:
        provenance_dir = self.root / "provenance"
        if provenance_dir.exists():
            loaded = self.load_json(
                self.root, "provenance/merge-source.json", "provenance/merge-source.json"
            )
            if loaded:
                _, provenance = loaded
                fields = {"generated_at", "core_repo", "core_sha", "data_repo", "data_sha"}
                self.require_fields(provenance, "provenance/merge-source.json", required=fields)
                for key in fields:
                    self.require_nonempty(provenance, key, "provenance/merge-source.json")
                for key in ("core_sha", "data_sha"):
                    value = provenance.get(key)
                    if not isinstance(value, str) or len(value) != 40 or any(c not in "0123456789abcdef" for c in value):
                        self.error("invalid_provenance", "provenance/merge-source.json", "source revision is invalid")
        registry_total = self.check_sharded(
            self.root, "registry.json", kind="registry", aliases={"registry_skill_count_dedup"}
        )
        search_total = self.check_sharded(self.docs, "search-index.json", kind="search", aliases={"t"})
        signal_totals = [
            self.check_sharded(self.docs, f"{name}-index.json", kind="signal", aliases={"count"})
            for name in ("quality", "security", "ranking")
        ]
        category_total = self.check_categories()
        lite_total, stats_registry, summary_total = self.check_simple_documents()
        self.totals["registry"].extend(
            value for value in (registry_total, stats_registry, summary_total) if value is not None
        )
        self.totals["scan"].extend(value for value in (search_total, category_total) if value is not None)
        self.totals["stable"].extend(
            value for value in (lite_total, *signal_totals) if value is not None
        )
        for group, values in self.totals.items():
            if not values or len(set(values)) != 1:
                self.error("group_total_mismatch", group, "same-set totals differ")
        return ValidationReport(
            checked_files=len(self.checked),
            totals=self.totals,
            errors=self.errors,
        )

def validate_artifact_api(root: Path, docs_dir: Path | None = None) -> ValidationReport:
    resolved_root = root.resolve()
    resolved_docs = (docs_dir or resolved_root / "docs").resolve()
    try:
        resolved_docs.relative_to(resolved_root)
    except ValueError as exc:
        raise ValueError("docs-dir must be inside root") from exc
    return ArtifactValidator(resolved_root, resolved_docs).validate()

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--docs-dir", type=Path)
    parser.add_argument("--output-json", type=Path)
    args = parser.parse_args()
    report = validate_artifact_api(args.root, args.docs_dir)
    payload = report.as_dict()
    if args.output_json:
        args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"artifact-api status={payload['status']} checked_files={report.checked_files} "
        f"errors={len(report.errors)}"
    )
    for error in report.errors:
        print(f"{error.code}: {error.path}: {error.message}")
    return 1 if report.errors else 0

if __name__ == "__main__":
    raise SystemExit(main())
