from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import remediate_archive_security as remediation  # noqa: E402
import security_scanner  # noqa: E402
from skill_frontmatter import normalize_skill_frontmatter  # noqa: E402


def write_skill(root: Path, name: str, content: str) -> Path:
    skill_dir = root / "development" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": name,
                "description": f"Archive metadata description for {name}.",
                "repo": f"owner/{name}",
                "github_path": f"skills/{name}",
                "github_branch": "main",
            }
        ),
        encoding="utf-8",
    )
    return skill_dir


def scan(root: Path) -> dict:
    return security_scanner.scan_directory(root, quiet=True, require_metadata=True)


def test_normalize_skill_frontmatter_repairs_invalid_and_absent_mappings():
    invalid = "---\nname: demo\ndescription: Invalid: unquoted colon\n---\n# Demo\n"
    repaired = normalize_skill_frontmatter(
        invalid,
        {"name": "Demo Skill", "description": "A valid archive description."},
    )
    absent = normalize_skill_frontmatter(
        "# Demo\n\nThis body paragraph supplies a sufficiently long description.\n",
        {"name": "Demo Skill", "description": ""},
    )

    scanner = security_scanner.SecurityScanner()
    assert scanner._extract_frontmatter(repaired) == {
        "name": "demo-skill",
        "description": "A valid archive description.",
    }
    assert "description: This body paragraph supplies" in absent

    unterminated = (
        "---\nname: demo\ndescription: Unterminated metadata\n"
        "# Demo\n\n| Topic | Reference |\n| --------- | ---------------- |\n"
    )
    repaired_unterminated = normalize_skill_frontmatter(
        unterminated,
        {"name": "Demo Skill", "description": ""},
    )
    assert scanner._extract_frontmatter(repaired_unterminated) == {
        "name": "demo-skill",
        "description": "Archived skill guidance for demo-skill.",
    }
    assert unterminated in repaired_unterminated


def test_plan_and_apply_repairs_format_only_and_quarantines_security_errors(tmp_path):
    skills_dir = tmp_path / "skills"
    invalid_dir = write_skill(
        skills_dir,
        "invalid-yaml",
        "---\nname: invalid-yaml\ndescription: Invalid: unquoted colon\n---\n# Demo\n",
    )
    dangerous_dir = write_skill(
        skills_dir,
        "dangerous",
        "---\nname: dangerous\ndescription: A valid dangerous fixture description.\n---\n"
        "# Demo\n\neval(user_input)\n",
    )
    report = scan(skills_dir)

    plan = remediation.build_plan(skills_dir, report)

    assert [(item.path, item.action) for item in plan] == [
        ("development/dangerous/SKILL.md", "quarantine"),
        ("development/invalid-yaml/SKILL.md", "normalize_frontmatter"),
    ]

    remediation.apply_plan(skills_dir, plan)

    assert not dangerous_dir.exists()
    assert invalid_dir.exists()
    final_report = scan(skills_dir)
    assert (final_report["total"], final_report["passed"], final_report["failed"]) == (1, 1, 0)


def test_apply_validates_every_target_before_mutating_archive(tmp_path):
    skills_dir = tmp_path / "skills"
    invalid_dir = write_skill(
        skills_dir,
        "a-invalid-yaml",
        "---\nname: a-invalid-yaml\ndescription: Invalid: unquoted colon\n---\n# Demo\n",
    )
    dangerous_dir = write_skill(
        skills_dir,
        "z-dangerous",
        "---\nname: z-dangerous\ndescription: A valid dangerous fixture description.\n---\n"
        "# Demo\n\neval(user_input)\n",
    )
    original_invalid = (invalid_dir / "SKILL.md").read_text(encoding="utf-8")
    plan = remediation.build_plan(skills_dir, scan(skills_dir))
    with (dangerous_dir / "SKILL.md").open("a", encoding="utf-8") as handle:
        handle.write("# changed after planning\n")

    with pytest.raises(ValueError, match="changed after planning"):
        remediation.apply_plan(skills_dir, plan)

    assert (invalid_dir / "SKILL.md").read_text(encoding="utf-8") == original_invalid
    assert dangerous_dir.exists()


def test_apply_preflights_normalized_content_before_mutating_archive(tmp_path):
    skills_dir = tmp_path / "skills"
    first_dir = write_skill(skills_dir, "a-first", "# First\n")
    second_dir = write_skill(skills_dir, "z-second", "# Second\n")
    original_first = (first_dir / "SKILL.md").read_text(encoding="utf-8")
    report = scan(skills_dir)
    plan = remediation.build_plan(skills_dir, report)
    second_metadata_path = second_dir / "metadata.json"
    second_metadata = json.loads(second_metadata_path.read_text(encoding="utf-8"))
    second_metadata["description"] = "Unsafe metadata description: eval(user_input)"
    second_metadata_path.write_text(json.dumps(second_metadata), encoding="utf-8")

    with pytest.raises(ValueError, match="Planned normalized skill remains unsafe"):
        remediation.apply_plan(skills_dir, plan)

    assert (first_dir / "SKILL.md").read_text(encoding="utf-8") == original_first
    assert second_dir.exists()


def test_apply_removes_trailing_whitespace_from_repaired_skill(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = write_skill(
        skills_dir,
        "missing-frontmatter",
        "# Demo  \n\nBody text.\t\n",
    )
    report = scan(skills_dir)

    remediation.apply_plan(skills_dir, remediation.build_plan(skills_dir, report))

    repaired = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    assert "# Demo\n" in repaired
    assert "Body text.\n" in repaired
    assert "  \n" not in repaired
    assert "\t\n" not in repaired


def test_build_plan_rejects_report_aggregate_drift(tmp_path):
    skills_dir = tmp_path / "skills"
    write_skill(skills_dir, "missing-frontmatter", "# Demo\n")
    report = scan(skills_dir)
    report["failed"] = 0

    with pytest.raises(ValueError, match="aggregate counts"):
        remediation.build_plan(skills_dir, report)


def test_write_audit_contains_only_bounded_remediation_evidence(tmp_path):
    skills_dir = tmp_path / "skills"
    write_skill(skills_dir, "missing-frontmatter", "# Demo\n")
    report = scan(skills_dir)
    plan = remediation.build_plan(skills_dir, report)
    output = tmp_path / "audit.json"

    remediation.write_audit(output, report, plan, applied=False)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert payload["counts"] == {
        "total": 1,
        "normalize_frontmatter": 1,
        "quarantine": 0,
    }
    assert (
        payload["remediations"][0]["path"]
        == "development/missing-frontmatter/SKILL.md"
    )
    assert "issues" not in payload["remediations"][0]


def test_main_dry_run_writes_audit_without_changing_archive(
    tmp_path, monkeypatch, capsys
):
    skills_dir = tmp_path / "skills"
    skill_dir = write_skill(skills_dir, "missing-frontmatter", "# Demo\n")
    original = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    report_path = tmp_path / "security-report.json"
    output_path = tmp_path / "audit" / "remediation-plan.json"
    report_path.write_text(json.dumps(scan(skills_dir)), encoding="utf-8")
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "remediate_archive_security.py",
            "--skills-dir",
            str(skills_dir),
            "--security-report",
            str(report_path),
            "--output",
            str(output_path),
        ],
    )

    assert remediation.main() == 0

    audit = json.loads(output_path.read_text(encoding="utf-8"))
    assert audit["applied"] is False
    assert audit["counts"] == {
        "total": 1,
        "normalize_frontmatter": 1,
        "quarantine": 0,
    }
    assert (skill_dir / "SKILL.md").read_text(encoding="utf-8") == original
    assert "Planned: 1 total, 1 normalized, 0 quarantined" in capsys.readouterr().out
