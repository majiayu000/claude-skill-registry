from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path
from types import SimpleNamespace


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("audit_category_quality")


def _write_skill(root: Path, category: str, name: str, metadata: dict, body: str) -> None:
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


def test_audit_finds_candidates_outside_other(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "development",
        "auth-audit",
        {
            "name": "auth-audit",
            "category": "development",
            "description": "Security auth vulnerability OWASP audit workflow.",
            "tags": ["security", "auth", "owasp"],
        },
        "---\nname: auth-audit\n---\n\nSecurity auth vulnerability OWASP audit workflow.",
    )
    _write_skill(
        skills_dir,
        "other",
        "design-system",
        {
            "name": "design-system",
            "category": "other",
            "description": "Figma UI UX CSS component design workflow.",
            "tags": ["figma", "ui", "ux"],
        },
        "---\nname: design-system\n---\n\nFigma UI UX CSS component design workflow.",
    )

    report = audit.build_report(skills_dir, min_score=2, min_delta=2)
    candidates = {
        item["path"]: item
        for item in report["candidate_reclassifications"]
    }
    assert candidates["development/auth-audit/SKILL.md"]["suggested_category"] == "security"
    assert candidates["other/design-system/SKILL.md"]["suggested_category"] == "design"
    assert report["candidate_reclassification_count"] == 2


def test_audit_reports_alias_usage_and_source_conflict(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "engineering",
        "doc-helper",
        {
            "name": "doc-helper",
            "category": "engineering",
            "description": "Convert PDF DOCX to markdown.",
        },
        "---\nname: doc-helper\ncategory: documents\n---\n\nConvert PDF DOCX to markdown.",
    )

    report = audit.build_report(skills_dir, include_frontmatter=True)
    assert report["alias_usage_count"] == 2
    assert report["alias_usages"][0]["canonical_category"] == "development"
    assert report["category_conflict_count"] == 1
    assert report["category_conflicts"][0]["resolved_sources"]["frontmatter"] == "documents"


def test_audit_reports_nonstandard_nested_layout(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    nested_dir = skills_dir / "other" / "other" / "nested-skill"
    nested_dir.mkdir(parents=True)
    (nested_dir / "metadata.json").write_text(
        json.dumps({"name": "nested-skill", "category": "other"}),
        encoding="utf-8",
    )
    (nested_dir / "SKILL.md").write_text("---\nname: nested-skill\n---\n", encoding="utf-8")

    report = audit.build_report(skills_dir)
    assert report["total_skills"] == 1
    assert report["standard_layout_skill_count"] == 0
    assert report["layout_issue_count"] == 1
    assert report["layout_issues"][0]["path"] == "other/other/nested-skill/SKILL.md"


def test_audit_uses_frontmatter_description_when_metadata_description_missing(tmp_path):
    audit = _load_module()
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

    report = audit.build_report(skills_dir, min_score=2, min_delta=2)
    candidates = {
        item["path"]: item
        for item in report["candidate_reclassifications"]
    }

    assert candidates["other/frontmatter-devops/SKILL.md"]["suggested_category"] == "devops"


def test_stratified_sample_is_deterministic_and_records_fresh_evidence(
    tmp_path,
    monkeypatch,
):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    for category in ("integration", "data"):
        for index in range(3):
            _write_skill(
                skills_dir,
                category,
                f"{category}-{index}",
                {
                    "name": f"{category}-{index}",
                    "category": category,
                    "description": f"{category} semantic description {index}",
                },
                (
                    "---\n"
                    f"name: {category}-{index}\n"
                    f"description: {category} frontmatter description {index}\n"
                    "---\n\n"
                    + ("bounded body " * 100)
                ),
            )

    policy = SimpleNamespace(
        schema_version=1,
        seed="test-seed",
        per_category=2,
        categories=("integration", "data"),
    )
    monkeypatch.setattr(
        audit,
        "get_taxonomy",
        lambda: SimpleNamespace(audit_sampling=policy, default_category="other"),
    )

    first = audit.build_stratified_sample(skills_dir, content_chars=32)
    original_iter = audit.iter_skill_dirs
    monkeypatch.setattr(
        audit,
        "iter_skill_dirs",
        lambda root: iter(reversed(list(original_iter(root)))),
    )
    second = audit.build_stratified_sample(skills_dir, content_chars=32)

    assert first["status"] == "complete"
    assert first["sample_count"] == 4
    assert first["digest"] == second["digest"]
    assert [
        item["path"]
        for stratum in first["strata"]
        for item in stratum["samples"]
    ] == [
        item["path"]
        for stratum in second["strata"]
        for item in stratum["samples"]
    ]
    for stratum in first["strata"]:
        assert stratum["sample_count"] == stratum["quota"] == 2
        for item in stratum["samples"]:
            assert len(item["source_sha256"]) == 64
            assert len(item["metadata_sha256"]) == 64
            assert len(item["sample_key"]) == 64
            assert len(item["content_excerpt"]) <= 32
            assert item["semantic_sources"]["description"] == "frontmatter"


def test_stratified_sample_fails_when_population_is_below_quota(
    tmp_path,
    monkeypatch,
):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "integration",
        "only-one",
        {"name": "only-one", "category": "integration"},
        "---\nname: only-one\n---\n",
    )
    policy = SimpleNamespace(
        schema_version=1,
        seed="test-seed",
        per_category=2,
        categories=("integration",),
    )
    monkeypatch.setattr(
        audit,
        "get_taxonomy",
        lambda: SimpleNamespace(audit_sampling=policy, default_category="other"),
    )

    report = audit.build_stratified_sample(skills_dir)
    assert report["status"] == "failed"
    assert report["strata"][0]["population_count"] == 1
    assert "below quota" in report["errors"][0]
