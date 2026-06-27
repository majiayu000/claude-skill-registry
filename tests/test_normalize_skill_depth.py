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


def _write_skill_with_body(root: Path, rel_dir: str, metadata: dict, body: str) -> Path:
    skill_dir = _write_skill(root, rel_dir, metadata)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    return skill_dir


def test_metadata_identity_normalizes_path_and_branch_aliases():
    module = _load_module()

    assert module.metadata_identity(
        {
            "name": "demo",
            "repo": "owner/repo",
            "path": "skills/demo",
            "branch": "main",
            "license": "MIT",
        }
    ) == module.metadata_identity(
        {
            "name": "demo",
            "repo": "owner/repo",
            "github_path": "skills/demo",
            "github_branch": "main",
            "license": "MIT",
        }
    )


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


def test_depth_plan_ignores_declared_bundled_skill_markdown(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "design/deterministic-design",
        {
            "name": "deterministic-design",
            "category": "design",
            "repo": "connerkward/deterministic-design-skill",
            "bundled_files": ["design-spatial/SKILL.md"],
        },
    )
    bundled_dir = skills_dir / "design" / "deterministic-design" / "design-spatial"
    bundled_dir.mkdir()
    (bundled_dir / "SKILL.md").write_text("# Spatial helper\n", encoding="utf-8")

    plan = module.build_depth_plan(skills_dir)

    assert plan["move_count"] == 0
    assert plan["moves"] == []


def test_depth_plan_moves_undeclared_nested_skill_markdown(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "design/deterministic-design",
        {
            "name": "deterministic-design",
            "category": "design",
            "repo": "connerkward/deterministic-design-skill",
            "bundled_files": [],
        },
    )
    nested_dir = skills_dir / "design" / "deterministic-design" / "design-spatial"
    nested_dir.mkdir()
    (nested_dir / "SKILL.md").write_text("# Spatial helper\n", encoding="utf-8")

    plan = module.build_depth_plan(skills_dir)

    assert plan["move_count"] == 1
    assert plan["moves"][0]["source_path"] == "design/deterministic-design/design-spatial"
    assert plan["moves"][0]["target_path"] == "design/design-spatial"


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


def test_depth_plan_reuses_existing_target_for_same_skill_key(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    metadata = {
        "name": "auth-audit",
        "category": "security",
        "repo": "acme/security-pack",
        "path": "skills/auth-audit",
    }
    _write_skill(skills_dir, "security/auth-audit", metadata)
    _write_skill(skills_dir, "other/other/auth-audit", metadata)

    plan = module.build_depth_plan(skills_dir)

    assert plan["move_count"] == 1
    assert plan["duplicate_count"] == 1
    assert plan["moves"][0]["operation"] == "remove_duplicate"
    assert plan["moves"][0]["target_path"] == "security/auth-audit"
    assert plan["moves"][0]["skill_content_equal"] is True
    assert plan["moves"][0]["metadata_identity_equal"] is True


def test_apply_depth_plan_removes_nested_duplicate_for_same_skill_key(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    metadata = {
        "name": "auth-audit",
        "category": "security",
        "repo": "acme/security-pack",
        "path": "skills/auth-audit",
    }
    existing = _write_skill(skills_dir, "security/auth-audit", metadata)
    _write_skill(skills_dir, "other/other/auth-audit", metadata)

    plan = module.build_depth_plan(skills_dir)
    module.apply_depth_plan(skills_dir, plan)

    assert (existing / "SKILL.md").exists()
    assert not (skills_dir / "other" / "other" / "auth-audit").exists()
    assert not (skills_dir / "security" / "auth-audit-acme-security-pack").exists()


def test_depth_plan_preserves_same_key_when_skill_content_differs(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    metadata = {
        "name": "auth-audit",
        "category": "security",
        "repo": "acme/security-pack",
        "path": "skills/auth-audit",
    }
    existing = _write_skill_with_body(
        skills_dir,
        "security/auth-audit",
        metadata,
        "---\nname: auth-audit\n---\n\nExisting body\n",
    )
    _write_skill_with_body(
        skills_dir,
        "other/other/auth-audit",
        metadata,
        "---\nname: auth-audit\n---\n\nNested body changed\n",
    )

    plan = module.build_depth_plan(skills_dir)

    assert plan["duplicate_count"] == 0
    assert plan["same_key_conflict_count"] == 1
    assert plan["same_key_preserved_count"] == 1
    assert plan["moves"][0]["operation"] == "move"
    assert plan["moves"][0]["target_path"] == "security/auth-audit-acme-security-pack"
    assert plan["moves"][0]["same_key_target_path"] == "security/auth-audit"
    assert plan["moves"][0]["skill_content_equal"] is False
    assert plan["moves"][0]["metadata_identity_equal"] is True

    module.apply_depth_plan(skills_dir, plan)

    assert (existing / "SKILL.md").exists()
    assert (skills_dir / "security" / "auth-audit-acme-security-pack" / "SKILL.md").exists()
    assert not (skills_dir / "other" / "other" / "auth-audit").exists()


def test_depth_plan_preserves_same_key_when_metadata_identity_differs(tmp_path):
    module = _load_module()
    skills_dir = tmp_path / "skills"
    existing_metadata = {
        "name": "auth-audit",
        "category": "security",
        "repo": "acme/security-pack",
        "path": "skills/auth-audit",
        "author": "Existing",
    }
    nested_metadata = {
        "name": "auth-audit",
        "category": "security",
        "repo": "acme/security-pack",
        "path": "skills/auth-audit",
        "author": "Nested",
    }
    _write_skill(skills_dir, "security/auth-audit", existing_metadata)
    _write_skill(skills_dir, "other/other/auth-audit", nested_metadata)

    plan = module.build_depth_plan(skills_dir)

    assert plan["duplicate_count"] == 0
    assert plan["same_key_preserved_count"] == 1
    assert plan["moves"][0]["operation"] == "move"
    assert plan["moves"][0]["skill_content_equal"] is True
    assert plan["moves"][0]["metadata_identity_equal"] is False


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
