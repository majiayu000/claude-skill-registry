from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("build_other_residual_governance_report")


def _write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_skill(root: Path, name: str, body: str, metadata: dict | None = None) -> None:
    skill_dir = root / "skills" / "other" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    _write_json(skill_dir / "metadata.json", metadata or {"name": name, "category": "other"})


def test_other_residual_report_groups_security_structure_and_semantic_items(tmp_path):
    reporter = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir.parent, "unsafe", "# Unsafe\nNo frontmatter.")
    _write_skill(skills_dir.parent, "bare", "---\nname: bare\n---\n")
    _write_skill(
        skills_dir.parent,
        "design-helper",
        (
            "---\n"
            "name: design-helper\n"
            "description: Figma UI UX CSS component design workflow.\n"
            "---\n"
        ),
    )
    security_report = tmp_path / "security.json"
    _write_json(
        security_report,
        {
            "skills": [
                {
                    "path": "other/unsafe/SKILL.md",
                    "safe": False,
                    "issues": [{"severity": "error", "type": "no_frontmatter"}],
                }
            ]
        },
    )

    report = reporter.build_report(
        skills_dir,
        security_report=security_report,
        min_score=2,
        min_delta=2,
    )

    assert report["total"] == 3
    assert report["bucket_counts"]["security_failed"] == 1
    assert report["bucket_counts"]["low_context"] == 1
    assert report["bucket_counts"]["semantic_review_candidate"] == 1
    assert report["suggested_category_counts"]["design"] == 1
    assert report["security_issue_counts"]["no_frontmatter"] == 1


def test_other_residual_report_marks_structure_without_security_report(tmp_path):
    reporter = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir.parent, "unsafe", "# Unsafe\nNo frontmatter.")

    report = reporter.build_report(skills_dir)

    assert report["total"] == 1
    assert report["bucket_counts"] == {"structure_review": 1}
    assert report["frontmatter_status_counts"] == {"no_frontmatter": 1}
