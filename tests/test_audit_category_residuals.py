from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("audit_category_residuals")


def _write_skill(
    root: Path,
    category: str,
    dirname: str,
    *,
    name: str | None = None,
    repo: str = "",
    path: str = "",
    body: str | None = None,
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
        body if body is not None else f"---\nname: {name or dirname}\n---\n\n{dirname}",
        encoding="utf-8",
    )


def _write_classification(path: Path, rows: list[dict]) -> None:
    path.write_text(
        "".join(json.dumps(row, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def test_report_separates_missing_sources_from_current_residuals(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "low-confidence")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/low-confidence/SKILL.md",
                "name": "low-confidence",
                "current_category": "other",
                "llm_category": "devops",
                "confidence": 0.4,
                "status": "ok",
            },
            {
                "path": "other/already-moved/SKILL.md",
                "name": "already-moved",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    assert report["summary"]["scoped_archive_skill_count"] == 1
    assert report["summary"]["source_state_counts"] == {"exists": 1, "missing": 1}
    assert report["summary"]["scoped_existing_source_count"] == 1
    assert report["summary"]["candidate_move_count"] == 0
    assert report["summary"]["primary_reason_counts"] == {
        "confidence below threshold": 1,
        "source directory missing": 1,
    }


def test_report_counts_candidates_and_stable_key_conflicts(tmp_path):
    audit = _load_module()
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
    _write_skill(skills_dir, "other", "movable")
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
                "path": "other/movable/SKILL.md",
                "name": "movable",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    conflict = "target category already contains a skill with the same stable key"
    assert report["summary"]["candidate_move_count"] == 1
    assert report["summary"]["blocked_existing_key_count"] == 1
    assert report["summary"]["primary_reason_counts"][audit.MOVABLE_REASON] == 1
    assert report["summary"]["primary_reason_counts"][conflict] == 1
    assert report["summary"]["same_policy_plan_summary"]["movable_count"] == 1
    assert report["summary"]["same_policy_plan_summary"]["blocked_count"] == 1


def test_report_can_emit_stable_key_conflict_details(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(
        skills_dir,
        "development",
        "already-there",
        name="duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
        body="same skill body",
    )
    _write_skill(
        skills_dir,
        "other",
        "duplicate",
        repo="owner/repo",
        path=".claude/skills/duplicate/SKILL.md",
        body="same skill body",
    )
    _write_skill(
        skills_dir,
        "development",
        "already-there-different",
        name="different",
        repo="owner/different",
        path=".claude/skills/different/SKILL.md",
        body="target body",
    )
    _write_skill(
        skills_dir,
        "other",
        "different",
        repo="owner/different",
        path=".claude/skills/different/SKILL.md",
        body="source body",
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
            },
            {
                "path": "other/different/SKILL.md",
                "name": "different",
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            },
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        conflict_detail_limit=10,
    )

    details = report["details"]["stable_key_conflicts"]
    assert len(details) == 2
    by_name = {detail["classification_name"]: detail for detail in details}
    duplicate = by_name["duplicate"]
    different = by_name["different"]
    assert duplicate["source_path"] == "other/duplicate"
    assert duplicate["target_path"] == "development/already-there"
    assert duplicate["skill_content_equal"] is True
    assert duplicate["metadata_identity_equal"] is True
    assert duplicate["source_skill_sha256"] == duplicate["target_skill_sha256"]
    assert different["target_path"] == "development/already-there-different"
    assert different["skill_content_equal"] is False
    assert different["metadata_identity_equal"] is True
    assert report["summary"]["stable_key_conflict_detail_count"] == 2
    assert report["summary"]["stable_key_conflict_detail_summary"] == {
        "metadata_identity_equal": 2,
        "skill_content_equal": 1,
    }


def test_report_conflict_detail_limit_is_bounded(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    for name in ("one", "two"):
        _write_skill(
            skills_dir,
            "development",
            f"target-{name}",
            name=name,
            repo=f"owner/{name}",
            path=f".claude/skills/{name}/SKILL.md",
        )
        _write_skill(
            skills_dir,
            "other",
            name,
            repo=f"owner/{name}",
            path=f".claude/skills/{name}/SKILL.md",
        )
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": f"other/{name}/SKILL.md",
                "name": name,
                "current_category": "other",
                "llm_category": "development",
                "confidence": 0.95,
                "status": "ok",
            }
            for name in ("one", "two")
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        conflict_detail_limit=1,
    )

    assert report["summary"]["blocked_existing_key_count"] == 2
    assert report["summary"]["stable_key_conflict_detail_count"] == 1
    assert len(report["details"]["stable_key_conflicts"]) == 1


def test_report_limits_examples_for_excluded_target_category(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "security-one")
    _write_skill(skills_dir, "other", "security-two")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/security-one/SKILL.md",
                "name": "security-one",
                "current_category": "other",
                "llm_category": "security",
                "confidence": 0.95,
                "status": "ok",
            },
            {
                "path": "other/security-two/SKILL.md",
                "name": "security-two",
                "current_category": "other",
                "llm_category": "security",
                "confidence": 0.96,
                "status": "ok",
            },
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
        to_categories={"devops"},
        limit_examples=1,
    )

    reason = "target category excluded by filter"
    assert report["summary"]["primary_reason_counts"] == {reason: 2}
    bucket = {item["reason"]: item for item in report["buckets"]}[reason]
    assert bucket["target_categories"] == [{"value": "security", "count": 2}]
    assert len(bucket["examples"]) == 1


def test_report_blocks_review_target_status_by_default(tmp_path):
    audit = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other", "legacy-applied")
    classification = tmp_path / "classification.jsonl"
    _write_classification(
        classification,
        [
            {
                "path": "other/legacy-applied/SKILL.md",
                "name": "legacy-applied",
                "current_category": "other",
                "llm_category": "applied",
                "confidence": 0.95,
                "status": "ok",
            }
        ],
    )

    report = audit.build_report(
        skills_dir=skills_dir,
        classification_jsonl=classification,
        from_categories={"other"},
    )

    reason = "target category status 'legacy' excluded by filter"
    assert report["summary"]["primary_reason_counts"] == {reason: 1}
    assert report["buckets"][0]["target_status_counts"] == {"legacy": 1}
