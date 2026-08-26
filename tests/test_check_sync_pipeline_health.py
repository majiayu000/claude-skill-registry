import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_sync_pipeline_health import PipelineHealthInput, validate_pipeline_health  # noqa: E402


def _security_report(total=1, passed=1, failed=0):
    return {
        "scanner": {
            "name": "claude-skill-registry-security-scanner",
            "version": "1.1.0",
            "ruleset_sha256": "abc123",
        },
        "generated_at": "2026-05-24T00:00:00Z",
        "total": total,
        "passed": passed,
        "failed": failed,
        "skills": [
            {
                "path": "development/demo/SKILL.md",
                "safe": failed == 0,
                "security_decision": {
                    "id": "decision123",
                    "status": "failed" if failed else "passed",
                    "reason": "errors_found" if failed else "no_errors",
                    "scanner": {
                        "name": "claude-skill-registry-security-scanner",
                        "version": "1.1.0",
                        "ruleset_sha256": "abc123",
                    },
                    "provenance": {
                        "content_sha256": "def456",
                        "scanned_at": "2026-05-24T00:00:00Z",
                    },
                },
                "issues": [],
            }
        ],
    }


def test_validate_pipeline_health_accepts_successful_steps(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps(_security_report()),
        encoding="utf-8",
    )

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
        )
    )

    assert errors == []


def test_supabase_schema_does_not_grant_anon_direct_stat_writes():
    schema = (ROOT / "supabase" / "schema.sql").read_text(encoding="utf-8")
    migration = (
        ROOT / "supabase" / "migrations" / "20260823000000_tighten_rls.sql"
    ).read_text(encoding="utf-8")

    assert 'CREATE POLICY "Anyone can update stats"' not in schema
    assert "FOR UPDATE USING (true)" not in schema
    assert "CREATE POLICY \"Anyone can insert likes\"" not in schema
    assert "CREATE POLICY \"Anyone can insert comments\"" not in schema
    assert "SET search_path = ''" in schema
    assert "p_device_id" not in schema
    assert "auth.uid()" in schema
    assert "REVOKE ALL ON TABLE public.skill_likes" in migration
    assert "pg_advisory_xact_lock" in migration


def test_validate_pipeline_health_rejects_failed_discovery(tmp_path):
    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="failure",
            download_outcome="success",
            security_outcome="success",
            security_report=tmp_path / "security-report.json",
            require_security_report=False,
        )
    )

    assert errors == ["discovery step failed with outcome=failure"]


def test_validate_pipeline_health_requires_report_when_security_passes(tmp_path):
    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=tmp_path / "security-report.json",
            require_security_report=True,
        )
    )

    assert errors == [f"required security report is missing: {tmp_path / 'security-report.json'}"]


def test_validate_pipeline_health_rejects_failed_security_report(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps(_security_report(passed=0, failed=1)),
        encoding="utf-8",
    )

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
        )
    )

    assert errors == ["security report contains failed scans: failed=1"]


def test_validate_pipeline_health_rejects_incomplete_path_coverage(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(json.dumps(_security_report()), encoding="utf-8")
    expected_paths = tmp_path / "expected-paths.txt"
    expected_paths.write_text(
        "development/demo/SKILL.md\ndevelopment/second/SKILL.md\n", encoding="utf-8"
    )

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
            expected_security_paths=expected_paths,
        )
    )

    assert errors == [
        "security report path coverage mismatch: "
        "missing=['development/second/SKILL.md'], unexpected=[]"
    ]


def test_validate_pipeline_health_allows_empty_scan_when_archive_did_not_change(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps({**_security_report(total=0, passed=0, failed=0), "skills": []}),
        encoding="utf-8",
    )
    expected_paths = tmp_path / "expected-paths.txt"
    expected_paths.write_text("", encoding="utf-8")

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
            expected_security_paths=expected_paths,
        )
    )

    assert errors == []


def test_validate_pipeline_health_rejects_inconsistent_aggregates(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps(_security_report(total=2, passed=2)), encoding="utf-8"
    )

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
        )
    )

    assert errors == ["security report aggregate counts do not match skill decisions"]


def test_validate_pipeline_health_rejects_missing_security_decision(tmp_path):
    report = _security_report()
    del report["skills"][0]["security_decision"]
    report_path = tmp_path / "security-report.json"
    report_path.write_text(json.dumps(report), encoding="utf-8")

    errors = validate_pipeline_health(
        PipelineHealthInput(
            discovery_outcome="success",
            download_outcome="success",
            security_outcome="success",
            security_report=report_path,
            require_security_report=True,
        )
    )

    assert errors == ["security report missing security_decision for development/demo/SKILL.md"]
