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


def test_plan_includes_taxonomy_deprecation_and_heuristic_reclassify(tmp_path):
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

    assert changes["docs/pdf-helper/SKILL.md"]["action"] == "taxonomy_deprecation"
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

    assert changes["engineering/builder/SKILL.md"]["action"] == "normalize_alias"
    assert changes["engineering/builder/SKILL.md"]["proposed_category"] == "development"
    assert changes["development/conflicted/SKILL.md"]["action"] == "resolve_source_conflict"
    assert changes["development/conflicted/SKILL.md"]["review_required"] is True
