from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("check_category_artifacts")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_category_artifact_guard_accepts_pointer_and_parts(tmp_path):
    guard = _load_module()
    categories_dir = tmp_path / "docs" / "categories"
    _write_json(
        categories_dir / "development.json",
        {
            "category": "development",
            "deprecated_full_payload": True,
            "manifest": "categories/development/manifest.json",
        },
    )
    _write_json(
        categories_dir / "development" / "manifest.json",
        {"parts": [{"path": "categories/development/part-000.json"}]},
    )
    _write_json(categories_dir / "development" / "part-000.json", {"skills": []})

    report = guard.build_report(categories_dir, pointer_max_bytes=1024, part_max_bytes=1024)

    assert report["error_count"] == 0
    assert report["pointer_count"] == 1
    assert report["part_count"] == 1


def test_category_artifact_guard_rejects_full_legacy_payload(tmp_path):
    guard = _load_module()
    categories_dir = tmp_path / "docs" / "categories"
    _write_json(
        categories_dir / "other.json",
        {
            "category": "other",
            "deprecated_full_payload": False,
            "skills": [{"name": "too-large"}],
        },
    )

    report = guard.build_report(categories_dir, pointer_max_bytes=1024, part_max_bytes=1024)
    codes = {item["code"] for item in report["errors"]}

    assert "category-pointer-not-marked" in codes
    assert "category-pointer-contains-skills" in codes
    assert "category-pointer-missing-manifest" in codes


def test_category_artifact_guard_rejects_oversized_pointer(tmp_path):
    guard = _load_module()
    categories_dir = tmp_path / "docs" / "categories"
    _write_json(
        categories_dir / "other.json",
        {
            "category": "other",
            "deprecated_full_payload": True,
            "manifest": "categories/other/manifest.json",
            "padding": "x" * 200,
        },
    )
    _write_json(categories_dir / "other" / "manifest.json", {"parts": []})

    report = guard.build_report(categories_dir, pointer_max_bytes=100, part_max_bytes=1024)

    assert report["error_count"] == 1
    assert report["errors"][0]["code"] == "category-pointer-too-large"
