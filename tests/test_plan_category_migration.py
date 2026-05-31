from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("plan_category_migration")


def _write_skill(root: Path, category: str, name: str, metadata: dict, body: str = "") -> None:
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(
        body or f"---\nname: {name}\n---\n\n{metadata.get('description', '')}",
        encoding="utf-8",
    )


def test_plan_includes_legacy_migration_and_heuristic_reclassify(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "docs",
        "pdf-helper",
        {
            "name": "pdf-helper",
            "category": "docs",
            "description": "PDF DOCX markdown conversion helper.",
        },
    )
    _write_skill(
        skills_dir,
        "other",
        "devops-helper",
        {
            "name": "devops-helper",
            "category": "other",
            "description": "Docker Kubernetes CI CD deploy infrastructure workflow.",
            "tags": ["docker", "kubernetes", "ci", "cd"],
        },
    )

    plan = planner.build_plan(skills_dir, min_score=2, min_delta=2)
    changes = {item["path"]: item for item in plan["changes"]}

    assert changes["docs/pdf-helper/SKILL.md"]["action"] == "legacy_category_migration"
    assert changes["docs/pdf-helper/SKILL.md"]["proposed_category"] == "documents"
    assert changes["other/devops-helper/SKILL.md"]["action"] == "heuristic_reclassify"
    assert changes["other/devops-helper/SKILL.md"]["confidence"] == "high"
    assert changes["other/devops-helper/SKILL.md"]["proposed_category"] == "devops"
    assert plan["summary"]["planned_change_count"] == 2


def test_plan_reports_alias_and_source_conflict(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "engineering",
        "builder",
        {
            "name": "builder",
            "category": "engineering",
            "description": "Build framework compile debug helper.",
        },
    )
    _write_skill(
        skills_dir,
        "development",
        "conflicted",
        {
            "name": "conflicted",
            "category": "development",
            "description": "Product roadmap PRD backlog helper.",
        },
        "---\nname: conflicted\ncategory: product\n---\n\nProduct roadmap PRD backlog helper.",
    )

    plan = planner.build_plan(skills_dir, include_frontmatter=True)
    changes = {item["path"]: item for item in plan["changes"]}

    assert changes["engineering/builder/SKILL.md"]["action"] == "legacy_category_migration"
    assert changes["engineering/builder/SKILL.md"]["proposed_category"] == "development"
    assert changes["engineering/builder/SKILL.md"]["review_required"] is True
    assert changes["development/conflicted/SKILL.md"]["action"] == "resolve_source_conflict"
    assert changes["development/conflicted/SKILL.md"]["review_required"] is True


def test_plan_routes_broad_legacy_slug_to_review_queue(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "applied",
        "broad",
        {
            "name": "broad",
            "category": "applied",
            "description": "Legacy imported bucket with no precise category.",
        },
    )

    plan = planner.build_plan(skills_dir)
    change = {item["path"]: item for item in plan["changes"]}[
        "applied/broad/SKILL.md"
    ]

    assert change["action"] == "legacy_category_review"
    assert change["proposed_category"] == "other"
    assert change["review_required"] is True


def test_plan_reports_source_conflict_before_legacy_migration(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "product",
        "misfiled-docs",
        {
            "name": "misfiled-docs",
            "category": "docs",
            "description": "Product roadmap documentation helper.",
        },
    )

    plan = planner.build_plan(skills_dir)
    change = {item["path"]: item for item in plan["changes"]}[
        "product/misfiled-docs/SKILL.md"
    ]

    assert change["action"] == "resolve_source_conflict"
    assert change["current_category"] == "docs"
    assert change["proposed_category"] == "docs"
    assert change["review_required"] is True


def test_plan_does_not_hide_source_conflicts_by_alias_normalization(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "development",
        "metadata-alias",
        {
            "name": "metadata-alias",
            "category": "engineering",
            "description": "Build framework compile debug helper.",
        },
    )

    plan = planner.build_plan(skills_dir)
    change = {item["path"]: item for item in plan["changes"]}[
        "development/metadata-alias/SKILL.md"
    ]

    assert change["action"] == "resolve_source_conflict"
    assert change["current_category"] == "engineering"
    assert change["raw_sources"] == {
        "directory": "development",
        "metadata": "engineering",
    }
    assert change["resolved_sources"] == {
        "directory": "development",
        "metadata": "engineering",
    }
    assert change["review_required"] is True


def test_plan_uses_frontmatter_description_when_metadata_description_missing(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "other",
        "frontmatter-devops",
        {
            "name": "frontmatter-devops",
            "category": "other",
        },
        (
            "---\n"
            "name: frontmatter-devops\n"
            "description: Docker Kubernetes CI CD deploy infrastructure workflow.\n"
            "tags:\n"
            "  - docker\n"
            "  - kubernetes\n"
            "---\n"
        ),
    )

    plan = planner.build_plan(skills_dir, min_score=2, min_delta=2)
    change = {item["path"]: item for item in plan["changes"]}[
        "other/frontmatter-devops/SKILL.md"
    ]

    assert change["action"] == "heuristic_reclassify"
    assert change["proposed_category"] == "devops"


def test_plan_does_not_use_body_description_when_content_chars_zero(tmp_path):
    planner = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "other",
        "quiet-helper",
        {
            "name": "quiet-helper",
            "category": "other",
        },
        (
            "---\n"
            "name: quiet-helper\n"
            "---\n\n"
            "Docker Kubernetes CI CD deploy infrastructure workflow.\n"
        ),
    )

    default_plan = planner.build_plan(skills_dir, min_score=2, min_delta=2)
    scanned_body_plan = planner.build_plan(
        skills_dir,
        content_chars=200,
        min_score=2,
        min_delta=2,
    )

    assert default_plan["changes"] == []
    change = {item["path"]: item for item in scanned_body_plan["changes"]}[
        "other/quiet-helper/SKILL.md"
    ]
    assert change["action"] == "heuristic_reclassify"
    assert change["proposed_category"] == "devops"
