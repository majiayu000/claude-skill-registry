from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("normalize_skill_depth")


def _write_skill(root: Path, rel_dir: str, metadata: dict) -> Path:
    skill_dir = root / rel_dir
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    return skill_dir


def test_depth_plan_uses_metadata_category_for_nested_skill(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "other/other/auth-audit",
        {
            "name": "auth-audit",
            "category": "security",
            "repo": "acme/security-pack",
            "path": "skills/auth-audit",
        },
    )

    plan = module.build_depth_plan(skills_dir)
    assert plan["move_count"] == 1
    assert plan["moves"][0]["source_path"] == "other/other/auth-audit"
    assert plan["moves"][0]["target_path"] == "security/auth-audit"
    assert plan["moves"][0]["expected_layout"] == "<category>/<skill>/SKILL.md"


def test_depth_plan_uses_category_after_skills_prefix(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "skills/documents/doc-helper",
        {
            "name": "doc-helper",
            "repo": "acme/docs",
            "path": "skills/doc-helper",
        },
    )

    plan = module.build_depth_plan(skills_dir)
    assert plan["move_count"] == 1
    assert plan["moves"][0]["target_path"] == "documents/doc-helper"


def test_apply_depth_plan_preserves_existing_target_with_suffix(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    existing = _write_skill(
        skills_dir,
        "security/auth-audit",
        {
            "name": "auth-audit",
            "category": "security",
            "repo": "acme/existing",
        },
    )
    _write_skill(
        skills_dir,
        "other/other/auth-audit",
        {
            "name": "auth-audit",
            "category": "security",
            "repo": "acme/security-pack",
        },
    )

    plan = module.build_depth_plan(skills_dir)
    assert plan["moves"][0]["target_path"] == "security/auth-audit-acme-security-pack"

    module.apply_depth_plan(skills_dir, plan)

    assert (existing / "SKILL.md").exists()
    target = skills_dir / "security" / "auth-audit-acme-security-pack"
    assert (target / "SKILL.md").exists()
    metadata = json.loads((target / "metadata.json").read_text(encoding="utf-8"))
    assert metadata["category"] == "security"
    assert metadata["dir_name"] == "auth-audit-acme-security-pack"
    assert not (skills_dir / "other" / "other" / "auth-audit").exists()


def test_apply_depth_plan_moves_child_before_parent(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "other/other/parent",
        {
            "name": "parent",
            "category": "other",
            "repo": "acme/parent",
        },
    )
    _write_skill(
        skills_dir,
        "other/other/parent/child",
        {
            "name": "child",
            "category": "other",
            "repo": "acme/child",
        },
    )

    plan = module.build_depth_plan(skills_dir)
    assert plan["move_count"] == 2

    module.apply_depth_plan(skills_dir, plan)

    assert (skills_dir / "other" / "parent" / "SKILL.md").exists()
    assert (skills_dir / "other" / "child" / "SKILL.md").exists()
    assert not (skills_dir / "other" / "other" / "parent").exists()
