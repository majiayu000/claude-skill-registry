from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("report_canonical_category_targets")


def _write_shard(root: Path) -> None:
    root.mkdir()
    (root / "00.json").write_text(
        json.dumps(
            {
                "skills": [
                    {"name": "canonical", "category": "development"},
                    {"name": "legacy", "category": "docs"},
                    {"name": "review", "category": "applied"},
                    {"name": "unknown", "category": "surprise"},
                ]
            }
        ),
        encoding="utf-8",
    )


def test_reports_canonical_legacy_review_and_unknown_targets(tmp_path):
    reporter = _load_module()
    shards_dir = tmp_path / "shards"
    _write_shard(shards_dir)

    report = reporter.build_report(shards_dir)

    assert report["total_skills"] == 4
    assert report["target_category_counts"]["development"] == 1
    assert report["target_category_counts"]["documents"] == 1
    assert report["target_category_counts"]["review-required"] == 1
    assert report["target_category_counts"]["unknown"] == 1
    assert report["reason_counts"] == {
        "canonical": 1,
        "legacy_migration": 1,
        "legacy_review": 1,
        "unknown": 1,
    }
