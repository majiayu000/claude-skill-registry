from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("check_canonical_categories")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_skill(root: Path, category: str, name: str, metadata_category: str) -> None:
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / "SKILL.md").write_text("# Skill\n\nDoes useful work.\n", encoding="utf-8")
    _write_json(
        skill_dir / "metadata.json",
        {"name": name, "category": metadata_category, "repo": "owner/repo"},
    )


def test_skills_dir_rejects_legacy_directory_and_metadata_mismatch(tmp_path):
    gate = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "docs", "legacy-doc", "docs")
    _write_skill(skills_dir, "development", "misfiled", "documents")

    report = gate.build_report(skills_dirs=[skills_dir])
    codes = {item["code"] for item in report["errors"]}

    assert report["error_count"] == 3
    assert "category-legacy" in codes
    assert "category-mismatch" in codes


def test_registry_shards_reject_noncanonical_categories(tmp_path):
    gate = _load_module()
    shards_dir = tmp_path / "registry-shards"
    _write_json(
        shards_dir / "00.json",
        {
            "skills": [
                {"name": "ok", "category": "development"},
                {"name": "legacy", "category": "technical-integration"},
                {"name": "unknown", "category": "moonbase"},
            ]
        },
    )

    report = gate.build_report(registry_shards_dirs=[shards_dir])
    codes = [item["code"] for item in report["errors"]]

    assert codes == ["category-legacy", "category-unknown"]


def test_registry_gate_accepts_empty_registry_shard(tmp_path):
    gate = _load_module()
    shards_dir = tmp_path / "registry-shards"
    _write_json(shards_dir / "00.json", {"skills": []})

    report = gate.build_report(registry_shards_dirs=[shards_dir])

    assert report["error_count"] == 0


def test_publish_gate_rejects_category_whitespace(tmp_path):
    gate = _load_module()
    shards_dir = tmp_path / "registry-shards"
    _write_json(shards_dir / "00.json", {"skills": [{"name": "bad", "category": "documents "}]})

    report = gate.build_report(registry_shards_dirs=[shards_dir])

    assert report["error_count"] == 1
    assert report["errors"][0]["code"] == "category-format"


def test_docs_gate_rejects_legacy_category_artifacts_and_search_codes(tmp_path):
    gate = _load_module()
    docs_dir = tmp_path / "docs"
    _write_json(
        docs_dir / "categories" / "index.json",
        {"categories": [{"name": "docs", "code": "docs", "count": 1}]},
    )
    _write_json(
        docs_dir / "categories" / "docs.json",
        {"category": "docs", "code": "docs", "deprecated_full_payload": True, "skills": []},
    )
    _write_json(
        docs_dir / "categories" / "docs" / "manifest.json",
        {"category": "docs", "code": "docs", "parts": []},
    )
    _write_json(
        docs_dir / "categories" / "docs" / "part-000.json",
        {"category": "docs", "code": "docs", "skills": [{"category": "docs"}]},
    )
    _write_json(docs_dir / "search-index-lite.json", {"skills": [{"category": "docs"}]})
    _write_json(docs_dir / "search-shards" / "part-000.json", {"s": [{"c": "docs"}]})
    _write_json(
        docs_dir / "stats.json",
        {"category_counts": [{"name": "docs", "code": "docs", "count": 1}]},
    )

    report = gate.build_report(docs_dirs=[docs_dir])
    codes = {item["code"] for item in report["errors"]}

    assert "category-legacy" in codes
    assert "category-code-noncanonical" in codes
    assert report["error_count"] >= 8


def test_docs_gate_rejects_category_count_drift(tmp_path):
    gate = _load_module()
    docs_dir = tmp_path / "docs"
    _write_json(
        docs_dir / "categories" / "index.json",
        {
            "categories": [
                {
                    "name": "documents",
                    "code": "doc",
                    "count": 2,
                    "manifest": "categories/documents/manifest.json",
                }
            ]
        },
    )
    _write_json(
        docs_dir / "categories" / "documents.json",
        {"category": "documents", "code": "doc", "count": 1},
    )
    _write_json(
        docs_dir / "categories" / "documents" / "manifest.json",
        {
            "category": "documents",
            "code": "doc",
            "count": 1,
            "part_count": 1,
            "parts": [{"path": "categories/documents/part-000.json", "count": 1}],
        },
    )
    _write_json(
        docs_dir / "categories" / "documents" / "part-000.json",
        {"category": "documents", "code": "doc", "count": 1, "skills": []},
    )
    _write_json(
        docs_dir / "stats.json",
        {"category_counts": [{"name": "documents", "code": "doc", "count": 1}]},
    )

    report = gate.build_report(docs_dirs=[docs_dir])
    codes = [item["code"] for item in report["errors"]]

    assert "category-count-mismatch" in codes


def test_publish_gate_accepts_canonical_shapes(tmp_path):
    gate = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "documents", "docx", "documents")
    shards_dir = tmp_path / "registry-shards"
    _write_json(shards_dir / "00.json", {"skills": [{"name": "docx", "category": "documents"}]})
    docs_dir = tmp_path / "docs"
    _write_json(
        docs_dir / "categories" / "index.json",
        {"categories": [{"name": "documents", "code": "doc", "count": 1}]},
    )
    _write_json(
        docs_dir / "categories" / "documents.json",
        {
            "category": "documents",
            "code": "doc",
            "count": 1,
            "deprecated_full_payload": True,
            "manifest": "categories/documents/manifest.json",
        },
    )
    _write_json(
        docs_dir / "categories" / "documents" / "manifest.json",
        {
            "category": "documents",
            "code": "doc",
            "count": 1,
            "part_count": 1,
            "parts": [{"path": "categories/documents/part-000.json", "count": 1}],
        },
    )
    _write_json(
        docs_dir / "categories" / "documents" / "part-000.json",
        {
            "category": "documents",
            "code": "doc",
            "count": 1,
            "skills": [{"category": "documents"}],
        },
    )
    _write_json(docs_dir / "search-index-lite.json", {"skills": [{"category": "documents"}]})
    _write_json(docs_dir / "search-shards" / "part-000.json", {"s": [{"c": "doc"}]})
    _write_json(
        docs_dir / "stats.json",
        {"category_counts": [{"name": "documents", "code": "doc", "count": 1}]},
    )

    report = gate.build_report(
        skills_dirs=[skills_dir],
        registry_shards_dirs=[shards_dir],
        docs_dirs=[docs_dir],
    )

    assert report["error_count"] == 0
