from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

import pytest


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("apply_category_migration")


def _write_skill(
    root: Path,
    category: str,
    dirname: str,
    *,
    name: str | None = None,
    repo: str = "",
    path: str = "",
) -> None:
    skill_dir = root / category / dirname
    skill_dir.mkdir(parents=True)
    metadata = {
        "name": name or dirname,
        "category": category,
        "dir_name": dirname,
    }
    if repo:
        metadata["repo"] = repo
    if path:
        metadata["path"] = path
    (skill_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(
        f"---\nname: {name or dirname}\n---\n\n{dirname}",
        encoding="utf-8",
    )


def _write_classification(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_build_plan_and_apply_moves_skill_and_updates_metadata(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "docker-helper")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/docker-helper/SKILL.md",
                "name": "docker-helper",
                "current_category": "other",
                "llm_category": "devops",
                "confidence": 0.95,
                "status": "ok",
            }
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        min_confidence=0.9,
    )

    assert plan["summary"]["planned_move_count"] == 1
    assert plan["moves"][0]["operation"] == "move"
    assert plan["moves"][0]["target_skill"] == "devops/docker-helper/SKILL.md"

    migrator.apply_plan(skills_dir, plan)

    assert not (skills_dir / "other" / "docker-helper").exists()
    assert (skills_dir / "devops" / "docker-helper" / "SKILL.md").exists()
    metadata = json.loads(
        (skills_dir / "devops" / "docker-helper" / "metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["category"] == "devops"
    assert metadata["dir_name"] == "docker-helper"


def test_name_conflict_uses_repo_suffix_without_overwriting(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "development", "same-name")
    _write_skill(
        skills_dir,
        "other",
        "same-name",
        repo="owner/repo",
        path=".claude/skills/same-name/SKILL.md",
    )
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/same-name/SKILL.md",
                "name": "same-name",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            }
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    assert plan["moves"][0]["operation"] == "move"
    assert plan["moves"][0]["target_path"] == "development/same-name-owner-repo"


def test_existing_target_key_is_blocked_not_deleted(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "development",
        "already-there",
        name="duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
    )
    _write_skill(
        skills_dir,
        "other",
        "duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
    )
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/duplicate/SKILL.md",
                "name": "duplicate",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            }
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    assert plan["moves"][0]["operation"] == "blocked_existing_key"
    with pytest.raises(ValueError, match="blocked move"):
        migrator.apply_plan(skills_dir, plan)
    assert (skills_dir / "other" / "duplicate" / "SKILL.md").exists()
    assert (skills_dir / "development" / "already-there" / "SKILL.md").exists()


def test_movable_only_skips_blocked_moves_and_fills_limit(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "development",
        "already-there",
        name="duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
    )
    _write_skill(
        skills_dir,
        "other",
        "duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
    )
    _write_skill(skills_dir, "other", "movable-one")
    _write_skill(skills_dir, "other", "movable-two")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/duplicate/SKILL.md",
                "name": "duplicate",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "other/movable-one/SKILL.md",
                "name": "movable-one",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "other/movable-two/SKILL.md",
                "name": "movable-two",
                "current_category": "other",
                "llm_category": "testing",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        movable_only=True,
        limit=2,
    )

    assert [move["source_skill"] for move in plan["moves"]] == [
        "other/movable-one/SKILL.md",
        "other/movable-two/SKILL.md",
    ]
    assert plan["summary"]["planned_move_count"] == 2
    assert plan["summary"]["operation_counts"] == {"move": 2}
    assert plan["summary"]["reject_reasons"] == {
        "target category already contains a skill with the same stable key": 1
    }


def test_filters_exclude_low_confidence_review_targets_and_other_targets(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "low")
    _write_skill(skills_dir, "other", "review-target")
    _write_skill(skills_dir, "other", "to-other")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/low/SKILL.md",
                "name": "low",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.5,
                "status": "ok",
            },
            {
                "path": "other/review-target/SKILL.md",
                "name": "review-target",
                "current_category": "other",
                "llm_category": "core",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "other/to-other/SKILL.md",
                "name": "to-other",
                "current_category": "other",
                "llm_category": "other",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        min_confidence=0.9,
    )

    assert plan["summary"]["planned_move_count"] == 0
    assert plan["summary"]["reject_reasons"] == {
        "classification target matches current category": 1,
        "confidence below threshold": 1,
        "target category status 'review' excluded by filter": 1,
    }
