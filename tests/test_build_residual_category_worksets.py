from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("build_residual_category_worksets")


def _write_skill(
    root: Path,
    rel: str,
    *,
    body: str = "---\nname: sample skill\ndescription: Sample description\n---\n\nBody",
    metadata: dict | None = None,
) -> None:
    skill_dir = root / rel
    skill_dir.mkdir(parents=True)
    payload = {
        "name": Path(rel).name,
        "category": Path(rel).parts[0],
        "dir_name": Path(rel).name,
    }
    payload.update(metadata or {})
    (skill_dir / "metadata.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


def _write_classification(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_builds_gap_low_confidence_review_and_target_other_worksets(tmp_path):
    worksets = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other/gap")
    _write_skill(skills_dir, "other/low-confidence")
    _write_skill(skills_dir, "other/review-target")
    _write_skill(skills_dir, "other/target-other")
    _write_skill(skills_dir, "development/already-classified")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/low-confidence/SKILL.md",
                "name": "low-confidence",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.5,
                "status": "ok",
            },
            {
                "path": "other/review-target/SKILL.md",
                "name": "review-target",
                "current_category": "other",
                "llm_category": "applied",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "other/target-other/SKILL.md",
                "name": "target-other",
                "current_category": "other",
                "llm_category": "other",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "development/already-classified/SKILL.md",
                "name": "already-classified",
                "current_category": "development",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    report = worksets.build_worksets(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        min_confidence=0.9,
    )

    assert report["summary"]["workset_counts"] == {
        "classification_gap": 1,
        "low_confidence": 1,
        "review_target": 1,
        "target_other": 1,
    }
    assert report["summary"]["archive_category_counts"]["other"] == 4
    assert report["summary"]["scoped_existing_classification_count"] == 3
    assert report["worksets"]["classification_gap"][0]["path"] == "other/gap/SKILL.md"
    assert report["worksets"]["classification_gap"][0]["skill_dir"] == "other/gap"
    assert report["worksets"]["low_confidence"][0]["previous_classification"] == {
        "llm_category": "development",
        "confidence": 0.5,
        "status": "ok",
        "current_category": "other",
    }


def test_summarizes_conflict_detail_clusters(tmp_path):
    worksets = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other/gap")
    classification = tmp_path / "classification.jsonl"
    _write_classification(classification, [])
    conflict_report = tmp_path / "conflicts.json"
    conflict_report.write_text(
        json.dumps(
            {
                "details": {
                    "stable_key_conflicts": [
                        {
                            "target_category": "development",
                            "skill_content_equal": True,
                            "metadata_identity_equal": True,
                        },
                        {
                            "target_category": "development",
                            "skill_content_equal": True,
                            "metadata_identity_equal": False,
                        },
                        {
                            "target_category": "data",
                            "skill_content_equal": False,
                            "metadata_identity_equal": True,
                        },
                        {
                            "target_category": "data",
                            "skill_content_equal": False,
                            "metadata_identity_equal": False,
                        },
                    ]
                }
            }
        ),
        encoding="utf-8",
    )

    report = worksets.build_worksets(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        conflict_detail_report=conflict_report,
    )

    assert report["summary"]["conflict_detail_count"] == 4
    assert report["summary"]["conflict_clusters"] == {
        "content_and_metadata_drift": 1,
        "content_drift_metadata_equal": 1,
        "content_equal_metadata_drift": 1,
        "exact_duplicate": 1,
    }
    assert report["summary"]["conflict_target_category_counts"] == {
        "data": 2,
        "development": 2,
    }


def test_writes_each_workset_as_jsonl(tmp_path):
    worksets = _load_module()
    report = {
        "worksets": {
            "classification_gap": [{"path": "other/a"}],
            "low_confidence": [],
            "review_target": [{"path": "other/b"}],
            "target_other": [],
        }
    }

    paths = worksets.write_workset_jsonl(report, tmp_path / "out")

    assert set(paths) == {
        "classification_gap",
        "low_confidence",
        "review_target",
        "target_other",
    }
    gap_rows = (tmp_path / "out" / "classification_gap.jsonl").read_text(
        encoding="utf-8"
    )
    assert json.loads(gap_rows)["path"] == "other/a"
