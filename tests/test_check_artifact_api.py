from __future__ import annotations

import gzip
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import build_registry_summary  # noqa: E402
import build_search_index  # noqa: E402
import check_artifact_api  # noqa: E402
import rebuild_registry  # noqa: E402


def _read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _rewrite(path: Path, mutate) -> None:
    payload = _read(path)
    mutate(payload)
    rebuild_registry.safe_write_json(path, payload)


def build_generated_fixture(root: Path) -> Path:
    generated_at = "2026-07-11T00:00:00Z"
    plugins = [{"name": "demo-plugin", "repo": "owner/plugins"}]
    skills = [
        {
            "name": "alpha",
            "description": "Alpha skill",
            "repo": "owner/alpha",
            "path": "skills/alpha/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo"],
            "stars": 2,
            "install": "owner/alpha/skills/alpha/SKILL.md",
            "source": "test",
        },
        {
            "name": "beta",
            "description": "Beta skill",
            "repo": "owner/beta",
            "path": "skills/beta/SKILL.md",
            "branch": "main",
            "category": "testing",
            "tags": ["demo"],
            "stars": 1,
            "install": "owner/beta/skills/beta/SKILL.md",
            "source": "test",
        },
    ]
    sources = root / "sources"
    sources.mkdir(parents=True)
    rebuild_registry.safe_write_json(sources / "plugins.json", {"plugins": plugins})

    entries = rebuild_registry.write_registry_shards(
        skills,
        root / "registry-shards",
        generated_at,
        reference_base=root,
    )
    manifest = rebuild_registry.build_registry_manifest(
        generated_at=generated_at,
        total_count=len(skills),
        plugin_count=len(plugins),
        shards=entries,
        summary_path="registry_summary.json",
        plugins_path="sources/plugins.json",
    )
    rebuild_registry.safe_write_json(root / "registry-manifest.json", manifest)
    pointer = rebuild_registry.build_compatibility_registry(
        generated_at=generated_at,
        total_count=len(skills),
        plugin_count=len(plugins),
        archive_skill_md_count_raw=len(skills),
        archive_metadata_count_raw=len(skills),
        manifest_path="registry-manifest.json",
    )
    rebuild_registry.safe_write_json(root / "registry.json", pointer)
    summary = build_registry_summary.build_registry_summary(
        root / "registry.json", sources / "plugins.json"
    )
    build_registry_summary.write_summary(root / "registry_summary.json", summary)

    docs = root / "docs"
    build_search_index.build_plugins_index(plugins, docs, updated_at=generated_at)
    build_search_index.build_search_index(
        skills,
        docs,
        source_name="generated fixture",
        archive_skill_md_count_raw=len(skills),
        archive_metadata_count_raw=len(skills),
        registry_skill_count_dedup=len(skills),
    )
    provenance = {
        "generated_at": generated_at,
        "core_repo": "owner/core",
        "core_sha": "a" * 40,
        "data_repo": "owner/data",
        "data_sha": "b" * 40,
    }
    rebuild_registry.safe_write_json(root / "provenance" / "merge-source.json", provenance)
    return docs


def _codes(report: check_artifact_api.ValidationReport) -> set[str]:
    return {error.code for error in report.errors}


def test_production_writers_generate_valid_v1_fixture(tmp_path):
    docs = build_generated_fixture(tmp_path)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert report.errors == []
    assert report.checked_files >= 520
    assert report.totals == {
        "registry": [2, 2, 2],
        "scan": [2, 2, 2],
        "stable": [2, 2, 2, 2, 2],
    }


def test_production_writers_keep_raw_duplicate_count_out_of_same_set_totals(tmp_path):
    docs = build_generated_fixture(tmp_path)
    duplicate_skills = [
        {
            "name": "Lower-ranked duplicate",
            "description": "short",
            "repo": "owner/alpha",
            "path": "skills/alpha/SKILL.md",
            "branch": "main",
            "category": "other",
            "tags": ["duplicate"],
            "stars": 1,
            "install": "owner/alpha/skills/alpha/SKILL.md",
            "source": "test",
        },
        {
            "name": "alpha",
            "description": "Alpha skill",
            "repo": "owner/alpha",
            "path": "skills/alpha/SKILL.md",
            "branch": "main",
            "category": "development",
            "tags": ["demo"],
            "stars": 2,
            "install": "owner/alpha/skills/alpha/SKILL.md",
            "source": "test",
        },
        {
            "name": "beta",
            "description": "Beta skill",
            "repo": "owner/beta",
            "path": "skills/beta/SKILL.md",
            "branch": "main",
            "category": "testing",
            "tags": ["demo"],
            "stars": 1,
            "install": "owner/beta/skills/beta/SKILL.md",
            "source": "test",
        },
    ]
    build_search_index.build_search_index(
        duplicate_skills,
        docs,
        source_name="fixture with duplicate stable key",
        archive_skill_md_count_raw=len(duplicate_skills),
        archive_metadata_count_raw=len(duplicate_skills),
        registry_skill_count_dedup=2,
    )

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)
    stats = _read(docs / "stats.json")
    lite = _read(docs / "search-index-lite.json")

    assert report.errors == []
    assert report.totals["scan"] == [2, 2, 2]
    assert stats["indexed_skill_count_scan_shape"] == 2
    assert stats["archive_skill_md_count_raw"] == 3
    assert lite["raw_count"] == 3


@pytest.mark.parametrize(
    ("path", "mutate", "expected"),
    [
        ("registry.json", lambda value: value.__setitem__("schema_version", 2), "unknown_schema"),
        ("registry.json", lambda value: value.__setitem__("unexpected", 1), "invalid_pointer_shape"),
        ("registry.json", lambda value: value.__setitem__("total_count", False), "invalid_count"),
        ("docs/search-index.json", lambda value: value.__setitem__("s", []), "pointer_contains_payload"),
        ("docs/search-index.json", lambda value: value.__setitem__("t", 3), "count_alias_conflict"),
        (
            "docs/search-index-manifest.json",
            lambda value: value.__setitem__("total_count", 3),
            "manifest_total_mismatch",
        ),
        (
            "docs/search-index-manifest.json",
            lambda value: value.__setitem__("shard_count", 7),
            "entry_count_mismatch",
        ),
        (
            "docs/search-index-manifest.json",
            lambda value: value.__setitem__("unexpected", []),
            "invalid_manifest_shape",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].pop("sha256"),
            "invalid_entry_shape",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("unexpected", 1),
            "invalid_entry_shape",
        ),
        (
            "docs/search-shards/part-000.json",
            lambda value: value.__setitem__("skills", value.pop("s")),
            "invalid_payload_key",
        ),
        (
            "docs/search-shards/part-000.json",
            lambda value: value.__setitem__("count", 7),
            "payload_count_mismatch",
        ),
        (
            "docs/search-shards/part-000.json",
            lambda value: value.__setitem__("part", 9),
            "payload_identity_mismatch",
        ),
        (
            "docs/search-shards/part-000.json",
            lambda value: value.__setitem__("unexpected", []),
            "unknown_payload_field",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("path", "../outside.json"),
            "path_escape",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("path", "/outside.json"),
            "path_escape",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("path", "registry-shards/missing.json"),
            "missing_or_escaped_path",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("bytes", 1),
            "bytes_mismatch",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("gzip_bytes", 1),
            "gzip_bytes_mismatch",
        ),
        (
            "registry-manifest.json",
            lambda value: value["shards"][0].__setitem__("sha256", "0" * 64),
            "sha256_mismatch",
        ),
        (
            "docs/stats.json",
            lambda value: value.__setitem__("registry_skill_count_dedup", 3),
            "group_total_mismatch",
        ),
        (
            "docs/stats.json",
            lambda value: value.__setitem__("lite_index_count", 3),
            "group_total_mismatch",
        ),
    ],
    ids=[
        "schema",
        "pointer-unknown-field",
        "boolean-count",
        "pointer-payload",
        "alias",
        "manifest-count",
        "manifest-entry-count",
        "manifest-unknown-field",
        "entry-missing-field",
        "entry-unknown-field",
        "payload-key",
        "payload-count",
        "payload-identity",
        "payload-unknown-field",
        "path-escape",
        "absolute-path",
        "missing-path",
        "bytes",
        "gzip-bytes",
        "hash",
        "registry-cross-total",
        "stable-cross-total",
    ],
)
def test_validator_rejects_single_fact_mutations(tmp_path, path, mutate, expected):
    docs = build_generated_fixture(tmp_path)
    _rewrite(tmp_path / path, mutate)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert expected in _codes(report)


@pytest.mark.parametrize(
    ("path", "mutate", "expected"),
    [
        ("registry-manifest.json", lambda v: v.__setitem__("shard_strategy", "other"), "invalid_manifest_semantics"),
        ("registry-manifest.json", lambda v: v.__setitem__("record_key", "name"), "invalid_manifest_semantics"),
        ("registry-manifest.json", lambda v: v.__setitem__("provenance", []), "invalid_manifest_semantics"),
        ("registry-manifest.json", lambda v: v.__setitem__("provenance", {"unexpected": "value"}), "invalid_manifest_semantics"),
        ("docs/search-index-manifest.json", lambda v: v.__setitem__("record_schema", "other"), "invalid_manifest_semantics"),
        ("docs/quality-index-manifest.json", lambda v: v.__setitem__("shard_strategy", "other"), "invalid_manifest_semantics"),
        ("docs/security-index-manifest.json", lambda v: v.__setitem__("record_schema", "other"), "invalid_manifest_semantics"),
        ("docs/ranking-index-manifest.json", lambda v: v.__setitem__("shard_strategy", "other"), "invalid_manifest_semantics"),
        ("docs/categories/development.json", lambda v: v.__setitem__("updated_at", "other"), "category_manifest_mismatch"),
        ("docs/categories/development/manifest.json", lambda v: v.__setitem__("part_strategy", "other"), "category_identity_mismatch"),
        ("docs/categories/development/part-000.json", lambda v: v.__setitem__("code", "other"), "payload_identity_mismatch"),
        ("docs/featured.json", lambda v: v.__setitem__("unexpected", []), "invalid_public_document_shape"),
        ("docs/plugins.json", lambda v: v.__setitem__("count", 9), "public_document_count_mismatch"),
        ("provenance/merge-source.json", lambda v: v.__setitem__("core_sha", "bad"), "invalid_provenance"),
    ],
    ids=[
        "registry-strategy", "registry-key", "registry-provenance-type", "registry-provenance-shape", "search-schema",
        "quality-strategy", "security-schema", "ranking-strategy", "category-pointer-time",
        "category-strategy", "category-part-code", "featured-shape", "plugin-count",
        "merge-provenance",
    ],
)
def test_validator_rejects_reviewer_semantic_probes(tmp_path, path, mutate, expected):
    docs = build_generated_fixture(tmp_path)
    _rewrite(tmp_path / path, mutate)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert expected in _codes(report)


@pytest.mark.parametrize("path", ["docs/featured.json", "docs/plugins.json"])
def test_validator_requires_public_documents(tmp_path, path):
    docs = build_generated_fixture(tmp_path)
    (tmp_path / path).unlink()

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert "missing_or_escaped_path" in _codes(report)


@pytest.mark.parametrize("probe", ["duplicate", "invalid-id", "path"], ids=str)
def test_validator_rejects_registry_shard_entry_placement_probes(tmp_path, probe):
    docs = build_generated_fixture(tmp_path)
    manifest_path = tmp_path / "registry-manifest.json"
    manifest = _read(manifest_path)
    if probe == "duplicate":
        manifest["shards"][1] = dict(manifest["shards"][0])
        expected = "duplicate_registry_shard_id"
    elif probe == "invalid-id":
        manifest["shards"][0]["id"] = "GG"
        expected = "invalid_registry_shard_id"
    else:
        manifest["shards"][0]["path"] = manifest["shards"][1]["path"]
        expected = "registry_shard_path_mismatch"
    rebuild_registry.safe_write_json(manifest_path, manifest)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert expected in _codes(report)


def test_validator_recomputes_registry_record_placement_after_integrity_refresh(tmp_path):
    docs = build_generated_fixture(tmp_path)
    manifest_path = tmp_path / "registry-manifest.json"
    manifest = _read(manifest_path)
    entry = next(item for item in manifest["shards"] if item["count"])
    plain_path = tmp_path / entry["path"]
    gzip_path = tmp_path / entry["gzip_path"]
    payload = _read(plain_path)
    skill = payload["skills"][0]
    for suffix in range(1, 1000):
        skill["branch"] = f"placement-drift-{suffix}"
        if rebuild_registry.registry_shard_id(skill) != entry["id"]:
            break
    rebuild_registry.safe_write_json(plain_path, payload)
    rebuild_registry.safe_write_gzip_json(gzip_path, payload)
    entry["bytes"] = plain_path.stat().st_size
    entry["gzip_bytes"] = gzip_path.stat().st_size
    entry["sha256"] = rebuild_registry.file_sha256(plain_path)
    rebuild_registry.safe_write_json(manifest_path, manifest)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert "registry_record_placement_mismatch" in _codes(report)
    assert not {"bytes_mismatch", "gzip_bytes_mismatch", "sha256_mismatch"} & _codes(report)


@pytest.mark.parametrize(
    ("probe", "expected"),
    [
        ("duplicate", "duplicate_search_stable_key"),
        ("missing", "invalid_search_stable_key"),
    ],
)
def test_validator_rejects_search_stable_key_probes_after_integrity_refresh(
    tmp_path, probe, expected
):
    docs = build_generated_fixture(tmp_path)
    manifest_path = docs / "search-index-manifest.json"
    manifest = _read(manifest_path)
    entry = next(item for item in manifest["shards"] if item["count"] >= 2)
    plain_path = docs / entry["path"]
    gzip_path = docs / entry["gzip_path"]
    payload = _read(plain_path)
    if probe == "duplicate":
        payload["s"][1]["i"] = payload["s"][0]["i"]
        payload["s"][1]["b"] = payload["s"][0]["b"]
    else:
        payload["s"][0].pop("i")
    rebuild_registry.safe_write_json(plain_path, payload)
    rebuild_registry.safe_write_gzip_json(gzip_path, payload)
    entry["bytes"] = plain_path.stat().st_size
    entry["gzip_bytes"] = gzip_path.stat().st_size
    entry["sha256"] = rebuild_registry.file_sha256(plain_path)
    rebuild_registry.safe_write_json(manifest_path, manifest)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert expected in _codes(report)
    assert not {"bytes_mismatch", "gzip_bytes_mismatch", "sha256_mismatch"} & _codes(report)


def test_validator_rejects_duplicate_reference_and_bad_gzip(tmp_path):
    docs = build_generated_fixture(tmp_path)
    manifest_path = tmp_path / "registry-manifest.json"
    manifest = _read(manifest_path)
    manifest["shards"][1]["path"] = manifest["shards"][0]["path"]
    rebuild_registry.safe_write_json(manifest_path, manifest)
    gzip_path = docs / "search-shards" / "part-000.json.gz"
    gzip_path.write_bytes(b"not gzip")

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert {"duplicate_reference", "invalid_gzip"} <= _codes(report)


def test_validator_rejects_duplicate_gzip_reference_and_symlink(tmp_path):
    docs = build_generated_fixture(tmp_path)
    manifest_path = tmp_path / "registry-manifest.json"
    manifest = _read(manifest_path)
    manifest["shards"][1]["gzip_path"] = manifest["shards"][0]["gzip_path"]
    target = tmp_path / manifest["shards"][0]["path"]
    symlink = tmp_path / "registry-shards" / "linked.json"
    symlink.symlink_to(target)
    manifest["shards"][0]["path"] = "registry-shards/linked.json"
    rebuild_registry.safe_write_json(manifest_path, manifest)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert {"duplicate_reference", "non_regular_file"} <= _codes(report)


def test_validator_rejects_gzip_payload_mismatch(tmp_path):
    docs = build_generated_fixture(tmp_path)
    gzip_path = docs / "quality-shards" / "part-000.json.gz"
    with gzip.open(gzip_path, "wt", encoding="utf-8") as handle:
        json.dump({"schema_version": 1, "records": []}, handle)

    report = check_artifact_api.validate_artifact_api(tmp_path, docs)

    assert "gzip_payload_mismatch" in _codes(report)


def test_validator_cli_collects_errors_and_writes_report(tmp_path):
    docs = build_generated_fixture(tmp_path)
    (docs / "search-index.json").write_text("[]", encoding="utf-8")
    (tmp_path / "registry_summary.json").write_text("{", encoding="utf-8")
    output = tmp_path / "validation.json"

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_artifact_api.py"),
            "--root",
            str(tmp_path),
            "--docs-dir",
            str(docs),
            "--output-json",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    payload = _read(output)
    assert completed.returncode == 1
    assert payload["status"] == "failed"
    assert len(payload["errors"]) >= 2
    assert "artifact-api status=failed" in completed.stdout


def test_validator_cli_never_echoes_invalid_artifact_contents(tmp_path):
    docs = build_generated_fixture(tmp_path)
    sentinel = "SENTINEL_PRIVATE_ARTIFACT_CONTENT_12345"
    (docs / "search-index.json").write_text(sentinel, encoding="utf-8")

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_artifact_api.py"),
            "--root",
            str(tmp_path),
            "--docs-dir",
            str(docs),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert sentinel not in completed.stdout
    assert sentinel not in completed.stderr


def test_validator_report_never_echoes_unknown_field_name(tmp_path):
    docs = build_generated_fixture(tmp_path)
    sentinel = "SENTINEL_PRIVATE_UNKNOWN_KEY_98765"
    output = tmp_path / "validation.json"
    _rewrite(docs / "featured.json", lambda value: value.__setitem__(sentinel, "secret"))

    completed = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "check_artifact_api.py"),
            "--root",
            str(tmp_path),
            "--docs-dir",
            str(docs),
            "--output-json",
            str(output),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert sentinel not in completed.stdout
    assert sentinel not in completed.stderr
    assert sentinel not in output.read_text(encoding="utf-8")


def test_validator_rejects_docs_dir_outside_root(tmp_path):
    outside = tmp_path.parent / "outside-docs"
    outside.mkdir(exist_ok=True)
    with pytest.raises(ValueError, match="inside root"):
        check_artifact_api.validate_artifact_api(tmp_path, outside)
