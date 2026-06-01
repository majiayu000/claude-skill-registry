from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("build_publish_readiness_report")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def test_publish_readiness_report_accepts_matching_artifacts(tmp_path):
    reporter = _load_module()
    _write_json(
        tmp_path / "docs" / "stats.json",
        {
            "archive_skill_md_count_raw": 199253,
            "archive_metadata_count_raw": 199253,
            "registry_skill_count_dedup": 157403,
            "categories": 42,
            "category_counts": [
                {"name": "development", "count": 10},
                {"name": "other", "count": 437},
            ],
        },
    )
    _write_json(
        tmp_path / "docs" / "categories" / "other" / "manifest.json",
        {"category": "other", "count": 437, "parts": []},
    )
    _write_json(
        tmp_path / "registry-manifest.json",
        {"total_count": 157403, "shards": [{"path": "registry-shards/000.json"}]},
    )
    _write_json(
        tmp_path / "provenance" / "merge-source.json",
        {"core_sha": "core123", "data_sha": "data123"},
    )
    _write_json(
        tmp_path / "provenance" / "publish-status.json",
        {"status": "passed", "checks": [{"name": "canary", "status": "passed"}]},
    )

    report = reporter.build_report(tmp_path)

    assert report["readiness"] == "ready"
    assert report["category_count"] == 437
    assert report["provenance"]["core_sha"] == "core123"
    assert report["publish_status"]["check_status_counts"] == {"passed": 1}
    assert report["error_count"] == 0


def test_publish_readiness_report_reports_count_mismatch(tmp_path):
    reporter = _load_module()
    _write_json(
        tmp_path / "docs" / "stats.json",
        {"category_counts": [{"name": "other", "count": 999}]},
    )
    _write_json(
        tmp_path / "docs" / "categories" / "other" / "manifest.json",
        {"category": "other", "count": 437},
    )
    _write_json(tmp_path / "registry-manifest.json", {"shards": []})
    _write_json(tmp_path / "provenance" / "merge-source.json", {})
    _write_json(tmp_path / "provenance" / "publish-status.json", {"status": "passed"})

    report = reporter.build_report(tmp_path)

    assert report["readiness"] == "not_ready"
    assert report["error_count"] == 1
    assert report["issues"][0]["code"] == "category-count-mismatch"
