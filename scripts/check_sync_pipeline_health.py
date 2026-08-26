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
REQUIRED_SECURITY_DECISION_KEYS = {"id", "status", "reason", "scanner", "provenance"}
REQUIRED_SECURITY_SCANNER_KEYS = {"name", "version", "ruleset_sha256"}
REQUIRED_SECURITY_PROVENANCE_KEYS = {"content_sha256", "scanned_at"}


@dataclass(frozen=True)
class PipelineHealthInput:
    discovery_outcome: str
    download_outcome: str
    security_outcome: str
    security_report: Path
    require_security_report: bool
    expected_security_paths: Path | None = None


def normalize_outcome(value: str) -> str:
    return value.strip().lower()


def _validate_step(step_name: str, outcome: str) -> list[str]:
    normalized = normalize_outcome(outcome)
    if normalized in BLOCKING_OUTCOMES:
        return [f"{step_name} step failed with outcome={normalized}"]
    if normalized not in ALLOWED_OUTCOMES:
        return [f"{step_name} step returned unknown outcome={normalized or '<empty>'}"]
    return []


def _validate_security_report(
    report_path: Path, expected_paths_path: Path | None = None
) -> list[str]:
    if not report_path.exists():
        return [f"required security report is missing: {report_path}"]

    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"security report is not valid JSON: {exc}"]

    if not isinstance(payload, dict):
        return ["security report root must be an object"]

    missing = sorted(REQUIRED_SECURITY_KEYS - set(payload))
    if missing:
        return [f"security report is missing keys: {', '.join(missing)}"]

    invalid_keys = [key for key in REQUIRED_SECURITY_KEYS if type(payload.get(key)) is not int]
    if invalid_keys:
        return [f"security report has non-integer fields: {', '.join(sorted(invalid_keys))}"]

    total = payload["total"]
    passed = payload["passed"]
    failed = payload["failed"]
    if min(total, passed, failed) < 0:
        return ["security report aggregate counts must be non-negative"]

    skills = payload.get("skills")
    if not isinstance(skills, list):
        return ["security report is missing per-skill evidence: skills"]

    report_paths: list[str] = []
    counted_passed = 0
    counted_failed = 0
    for index, skill_result in enumerate(skills):
        if not isinstance(skill_result, dict):
            return [f"security report skill result is not an object: skills[{index}]"]
        path = skill_result.get("path")
        if not isinstance(path, str) or not path.strip():
            return [f"security report has invalid skill path: skills[{index}]"]
        path = path.strip()
        if path in report_paths:
            return [f"security report contains duplicate skill path: {path}"]
        report_paths.append(path)
        decision = skill_result.get("security_decision")
        if not isinstance(decision, dict):
            return [f"security report missing security_decision for {path}"]
        missing_decision = sorted(REQUIRED_SECURITY_DECISION_KEYS - set(decision))
        if missing_decision:
            return [
                "security decision is missing keys for " f"{path}: {', '.join(missing_decision)}"
            ]
        status = decision.get("status")
        if status not in {"passed", "failed"}:
            return [f"security decision has invalid status for {path}: {status!r}"]
        safe = skill_result.get("safe")
        if not isinstance(safe, bool):
            return [f"security report has invalid safe field for {path}"]
        if (status == "passed") != safe:
            return [f"security decision status disagrees with safe field for {path}"]
        counted_passed += int(status == "passed")
        counted_failed += int(status == "failed")
        scanner = decision.get("scanner")
        if not isinstance(scanner, dict):
            return [f"security decision scanner evidence is invalid for {path}"]
        missing_scanner = sorted(REQUIRED_SECURITY_SCANNER_KEYS - set(scanner))
        if missing_scanner:
            return [
                "security decision scanner evidence is missing keys for "
                f"{path}: {', '.join(missing_scanner)}"
            ]
        provenance = decision.get("provenance")
        if not isinstance(provenance, dict):
            return [f"security decision provenance is invalid for {path}"]
        missing_provenance = sorted(REQUIRED_SECURITY_PROVENANCE_KEYS - set(provenance))
        if missing_provenance:
            return [
                "security decision provenance is missing keys for "
                f"{path}: {', '.join(missing_provenance)}"
            ]

    if (total, passed, failed) != (len(skills), counted_passed, counted_failed):
        return ["security report aggregate counts do not match skill decisions"]

    if expected_paths_path is not None:
        if not expected_paths_path.exists():
            return [f"expected security path list is missing: {expected_paths_path}"]
        try:
            expected_raw = expected_paths_path.read_bytes()
        except OSError as exc:
            return [f"cannot read expected security path list: {exc}"]
        chunks = expected_raw.split(b"\0") if b"\0" in expected_raw else expected_raw.splitlines()
        try:
            expected_paths = {chunk.decode("utf-8") for chunk in chunks if chunk}
        except UnicodeDecodeError:
            return ["expected security path list contains a non-UTF-8 path"]
        report_path_set = set(report_paths)
        if report_path_set != expected_paths:
            missing_paths = sorted(expected_paths - report_path_set)
            unexpected_paths = sorted(report_path_set - expected_paths)
            return [
                "security report path coverage mismatch: "
                f"missing={missing_paths}, unexpected={unexpected_paths}"
            ]

    if failed > 0:
        return [f"security report contains failed scans: failed={failed}"]
    return []


def validate_pipeline_health(pipeline_input: PipelineHealthInput) -> list[str]:
    errors: list[str] = []
    errors.extend(_validate_step("discovery", pipeline_input.discovery_outcome))
    errors.extend(_validate_step("download", pipeline_input.download_outcome))
    errors.extend(_validate_step("security", pipeline_input.security_outcome))

    if (
        pipeline_input.require_security_report
        and normalize_outcome(pipeline_input.security_outcome) == "success"
    ):
        errors.extend(
            _validate_security_report(
                pipeline_input.security_report,
                expected_paths_path=pipeline_input.expected_security_paths,
            )
        )

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
    parser.add_argument("--expected-security-paths")
    args = parser.parse_args()

    return PipelineHealthInput(
        discovery_outcome=args.discovery_outcome,
        download_outcome=args.download_outcome,
        security_outcome=args.security_outcome,
        security_report=Path(args.security_report),
        require_security_report=args.require_security_report,
        expected_security_paths=(
            Path(args.expected_security_paths) if args.expected_security_paths else None
        ),
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
