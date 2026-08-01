from __future__ import annotations

import hashlib
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


def test_source_hash_mismatch_blocks_stale_classification(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "stale")
    skill_path = skills_dir / "other" / "stale" / "SKILL.md"
    original_hash = hashlib.sha256(skill_path.read_bytes()).hexdigest()
    skill_path.write_text("---\nname: stale\n---\n\nchanged", encoding="utf-8")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/stale/SKILL.md",
                "name": "stale",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
                "source_sha256": original_hash,
            }
        ],
    )

    plan = migrator.build_apply_plan(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    assert plan["summary"]["planned_move_count"] == 0
    assert plan["summary"]["reject_reasons"] == {
        "source SKILL.md sha256 changed since classification": 1
    }


def test_missing_source_skill_file_blocks_apply_plan(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    source_dir = skills_dir / "other" / "missing-skill"
    source_dir.mkdir(parents=True)
    (source_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "missing-skill",
                "category": "other",
                "dir_name": "missing-skill",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/missing-skill/SKILL.md",
                "name": "missing-skill",
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

    assert plan["summary"]["planned_move_count"] == 0
    assert plan["summary"]["reject_reasons"] == {"source SKILL.md missing": 1}


@pytest.mark.parametrize(
    ("source_path", "reason"),
    [
        ("../outside/SKILL.md", "source path is not standard <category>/<skill>/SKILL.md"),
        ("/outside/SKILL.md", "source path is not standard <category>/<skill>/SKILL.md"),
        ("C:/outside/SKILL.md", "source path is not standard <category>/<skill>/SKILL.md"),
        ("other\\outside\\SKILL.md", "classification path is not a SKILL.md path"),
    ],
)
def test_plan_rejects_nonstandard_source_paths(tmp_path, source_path, reason):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "SKILL.md").write_text("outside", encoding="utf-8")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": source_path,
                "name": "outside",
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
    )

    assert plan["summary"]["planned_move_count"] == 0
    assert plan["summary"]["reject_reasons"] == {reason: 1}
    assert (outside / "SKILL.md").exists()


def test_apply_plan_rejects_escaping_paths(tmp_path):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    outside = tmp_path / "outside"
    outside.mkdir()
    (outside / "SKILL.md").write_text("outside", encoding="utf-8")
    plan = {
        "moves": [
            {
                "operation": "move",
                "source_path": "../outside",
                "target_path": "devops/outside",
            }
        ]
    }

    with pytest.raises(ValueError, match="invalid source or target path"):
        migrator.apply_plan(skills_dir, plan)

    assert (outside / "SKILL.md").exists()


def test_plan_and_apply_reject_symlinked_skill_path(tmp_path, monkeypatch):
    migrator = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "victim")
    victim_dir = skills_dir / "other" / "victim"
    source_dir = skills_dir / "other" / "alias"
    try:
        source_dir.symlink_to(victim_dir, target_is_directory=True)
    except OSError:
        path_type = type(source_dir)
        original_is_symlink = path_type.is_symlink

        def is_symlink(path):
            return path == source_dir or original_is_symlink(path)

        monkeypatch.setattr(path_type, "is_symlink", is_symlink)
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/alias/SKILL.md",
                "name": "alias",
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
    )

    assert plan["summary"]["planned_move_count"] == 0
    with pytest.raises(ValueError, match="plan path escapes skills directory"):
        migrator.apply_plan(
            skills_dir,
            {
                "moves": [
                    {
                        "operation": "move",
                        "source_path": "other/alias",
                        "target_path": "devops/alias",
                    }
                ]
            },
        )
    metadata = json.loads((victim_dir / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["category"] == "other"
    assert metadata["dir_name"] == "victim"


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
        "target category status 'legacy' excluded by filter": 1,
    }
