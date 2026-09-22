#!/usr/bin/env python3
"""Fail a ClamAV report only on findings that are not reviewed exceptions."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path

DEFAULT_EXCEPTIONS = "security/clamav-exceptions.json"
FINDING_PATTERN = re.compile(r"^(?P<path>.+): (?P<signature>\S+) FOUND$")


@dataclass(frozen=True)
class Finding:
    path: str
    signature: str


def parse_findings(report_text: str) -> list[Finding]:
    findings: list[Finding] = []
    for line in report_text.splitlines():
        match = FINDING_PATTERN.match(line.strip())
        if match:
            findings.append(Finding(match.group("path"), match.group("signature")))
    return findings


def load_exceptions(path: Path) -> list[dict]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    exceptions = payload.get("exceptions")
    if not isinstance(exceptions, list):
        raise ValueError(f"{path} must provide an exceptions array")
    for entry in exceptions:
        missing = (
            not isinstance(entry, dict)
            or not entry.get("path")
            or not entry.get("signature")
            or not entry.get("reason")
        )
        if missing:
            raise ValueError(f"{path} entries need path, signature and reason: {entry!r}")
    return exceptions


def matching_exception(finding: Finding, exceptions: list[dict]) -> dict | None:
    """Return the reviewed exception covering this finding, if any.

    A finding is only excused by an exact signature match, so a new signature on an
    already reviewed path still fails the scan.
    """
    for entry in exceptions:
        if entry["signature"] == finding.signature and fnmatch(finding.path, entry["path"]):
            return entry
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--report",
        default="clamav-report.txt",
        help="clamscan log file to triage.",
    )
    parser.add_argument(
        "--exceptions",
        default=DEFAULT_EXCEPTIONS,
        help="JSON file listing reviewed path/signature exceptions.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_path = Path(args.report)
    if not report_path.is_file():
        print(f"ClamAV report is missing: {report_path}")
        return 1
    try:
        exceptions = load_exceptions(Path(args.exceptions))
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Unusable ClamAV exception list: {error}")
        return 1

    findings = parse_findings(report_path.read_text(encoding="utf-8", errors="replace"))
    reviewed: list[tuple[Finding, dict]] = []
    unreviewed: list[Finding] = []
    for finding in findings:
        entry = matching_exception(finding, exceptions)
        if entry is None:
            unreviewed.append(finding)
        else:
            reviewed.append((finding, entry))

    for finding, entry in reviewed:
        print(f"Reviewed ClamAV exception: {finding.path}: {finding.signature} ({entry['reason']})")
    for finding in unreviewed:
        print(f"Unreviewed ClamAV finding: {finding.path}: {finding.signature}")
    print(
        f"ClamAV findings: {len(findings)} total, "
        f"{len(reviewed)} reviewed, {len(unreviewed)} unreviewed"
    )
    return 1 if unreviewed else 0


if __name__ == "__main__":
    raise SystemExit(main())
