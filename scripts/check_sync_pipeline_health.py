#!/usr/bin/env python3
"""
Fail the sync pipeline when critical discovery/download/security steps break.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

BLOCKING_OUTCOMES = {"failure", "cancelled", "timed_out"}
ALLOWED_OUTCOMES = {"success", "skipped", "not-run", ""}
REQUIRED_SECURITY_KEYS = {"total", "passed", "failed"}


@dataclass(frozen=True)
class PipelineHealthInput:
    discovery_outcome: str
    download_outcome: str
    security_outcome: str
    security_report: Path
    require_security_report: bool


def normalize_outcome(value: str) -> str:
    return value.strip().lower()


def _validate_step(step_name: str, outcome: str) -> list[str]:
    normalized = normalize_outcome(outcome)
    if normalized in BLOCKING_OUTCOMES:
        return [f"{step_name} step failed with outcome={normalized}"]
    if normalized not in ALLOWED_OUTCOMES:
        return [f"{step_name} step returned unknown outcome={normalized or '<empty>'}"]
    return []


def _validate_security_report(report_path: Path) -> list[str]:
    if not report_path.exists():
        return [f"required security report is missing: {report_path}"]

    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"security report is not valid JSON: {exc}"]

    missing = sorted(REQUIRED_SECURITY_KEYS - set(payload))
    if missing:
        return [f"security report is missing keys: {', '.join(missing)}"]

    invalid_keys = [
        key for key in REQUIRED_SECURITY_KEYS if not isinstance(payload.get(key), int)
    ]
    if invalid_keys:
        return [f"security report has non-integer fields: {', '.join(sorted(invalid_keys))}"]

    return []


def validate_pipeline_health(pipeline_input: PipelineHealthInput) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_step("discovery", pipeline_input.discovery_outcome))
    errors.extend(_validate_step("download", pipeline_input.download_outcome))
    errors.extend(_validate_step("security", pipeline_input.security_outcome))

    if pipeline_input.require_security_report and normalize_outcome(
        pipeline_input.security_outcome
    ) == "success":
        errors.extend(_validate_security_report(pipeline_input.security_report))

    return errors


def parse_args() -> PipelineHealthInput:
    parser = argparse.ArgumentParser(
        description="Validate selected sync-data step outcomes before publish/commit."
    )
    parser.add_argument("--discovery-outcome", required=True)
    parser.add_argument("--download-outcome", required=True)
    parser.add_argument("--security-outcome", required=True)
    parser.add_argument("--security-report", default="security-report.json")
    parser.add_argument("--require-security-report", action="store_true")
    args = parser.parse_args()

    return PipelineHealthInput(
        discovery_outcome=args.discovery_outcome,
        download_outcome=args.download_outcome,
        security_outcome=args.security_outcome,
        security_report=Path(args.security_report),
        require_security_report=args.require_security_report,
    )


def main() -> int:
    pipeline_input = parse_args()
    errors = validate_pipeline_health(pipeline_input)
    if errors:
        print("Sync pipeline health check failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Sync pipeline health check passed "
        f"(discovery={normalize_outcome(pipeline_input.discovery_outcome)}, "
        f"download={normalize_outcome(pipeline_input.download_outcome)}, "
        f"security={normalize_outcome(pipeline_input.security_outcome)})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
