import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_sync_pipeline_health import PipelineHealthInput, validate_pipeline_health  # noqa: E402


def test_validate_pipeline_health_accepts_successful_steps(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps({"total": 3, "passed": 3, "failed": 0}),
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

    assert errors == [
        f"required security report is missing: {tmp_path / 'security-report.json'}"
    ]


def test_validate_pipeline_health_rejects_failed_security_report(tmp_path):
    report_path = tmp_path / "security-report.json"
    report_path.write_text(
        json.dumps({"total": 3, "passed": 2, "failed": 1}),
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
