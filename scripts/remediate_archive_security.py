#!/usr/bin/env python3
"""Repair format-only scan failures and quarantine security failures."""

from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from security_scanner import (
    SECURITY_SCANNER_NAME,
    SECURITY_SCANNER_VERSION,
    SecurityScanner,
    security_ruleset_hash,
    source_content_hash,
)
from skill_frontmatter import normalize_skill_frontmatter

FORMAT_ONLY_ERRORS = frozenset({"no_frontmatter", "yaml_parse_error"})


@dataclass(frozen=True)
class Remediation:
    path: str
    action: str
    error_types: tuple[str, ...]
    content_sha256: str
    source_repo: str
    source_path: str
    source_ref: str


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Cannot read {label}: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object: {path}")
    return value


def _safe_skill_path(skills_dir: Path, relative_path: str) -> Path:
    if not relative_path or Path(relative_path).is_absolute():
        raise ValueError(f"Invalid report skill path: {relative_path!r}")
    skill_path = (skills_dir / relative_path).resolve()
    try:
        skill_path.relative_to(skills_dir)
    except ValueError as exc:
        raise ValueError(f"Report skill path escapes archive root: {relative_path}") from exc
    if skill_path.name != "SKILL.md" or skill_path.parent == skills_dir:
        raise ValueError(f"Report path is not an archived SKILL.md: {relative_path}")
    if not skill_path.is_file() or skill_path.is_symlink():
        raise ValueError(f"Archived SKILL.md is missing or unsafe: {relative_path}")
    if skill_path.parent.is_symlink():
        raise ValueError(f"Archived skill directory cannot be a symlink: {relative_path}")
    return skill_path


def build_plan(skills_dir: Path, report: dict[str, Any]) -> list[Remediation]:
    skills_dir = skills_dir.resolve()
    scanner = report.get("scanner")
    policy = report.get("scan_policy")
    results = report.get("skills")
    if not isinstance(scanner, dict) or scanner.get("name") != SECURITY_SCANNER_NAME:
        raise ValueError("Security report has an invalid scanner identity")
    if scanner.get("version") != SECURITY_SCANNER_VERSION:
        raise ValueError("Security report scanner version does not match this core checkout")
    if scanner.get("ruleset_sha256") != security_ruleset_hash():
        raise ValueError("Security report ruleset does not match this core checkout")
    if not isinstance(policy, dict) or policy.get("require_metadata") is not True:
        raise ValueError("Security report must require archive metadata")
    if not isinstance(results, list):
        raise ValueError("Security report is missing skill decisions")

    counted_failed = sum(1 for result in results if result.get("safe") is False)
    aggregate = (report.get("total"), report.get("passed"), report.get("failed"))
    expected = (len(results), len(results) - counted_failed, counted_failed)
    if aggregate != expected:
        raise ValueError("Security report aggregate counts do not match its decisions")

    plan: list[Remediation] = []
    seen_paths: set[str] = set()
    for result in results:
        if result.get("safe") is not False:
            continue
        relative_path = result.get("path")
        if not isinstance(relative_path, str) or relative_path in seen_paths:
            raise ValueError(f"Security report has an invalid or duplicate path: {relative_path!r}")
        seen_paths.add(relative_path)
        skill_path = _safe_skill_path(skills_dir, relative_path)

        issues = result.get("issues")
        decision = result.get("security_decision")
        if not isinstance(issues, list) or not isinstance(decision, dict):
            raise ValueError(f"Security report decision is incomplete: {relative_path}")
        if decision.get("status") != "failed":
            raise ValueError(f"Failed skill has a non-failed decision: {relative_path}")
        provenance = decision.get("provenance")
        if not isinstance(provenance, dict):
            raise ValueError(f"Security decision lacks provenance: {relative_path}")

        error_types = tuple(
            sorted(
                {
                    issue.get("type")
                    for issue in issues
                    if isinstance(issue, dict)
                    and issue.get("severity") == "error"
                    and isinstance(issue.get("type"), str)
                }
            )
        )
        if not error_types:
            raise ValueError(f"Failed skill has no typed error: {relative_path}")
        expected_hash = provenance.get("content_sha256")
        actual_hash = source_content_hash(skill_path.parent)
        if not isinstance(expected_hash, str) or expected_hash != actual_hash:
            raise ValueError(f"Archived content changed after scan: {relative_path}")

        metadata = _load_json_object(skill_path.parent / "metadata.json", "archive metadata")
        action = "normalize_frontmatter" if set(error_types) <= FORMAT_ONLY_ERRORS else "quarantine"
        plan.append(
            Remediation(
                path=relative_path,
                action=action,
                error_types=error_types,
                content_sha256=actual_hash,
                source_repo=str(metadata.get("repo") or ""),
                source_path=str(metadata.get("github_path") or metadata.get("path") or ""),
                source_ref=str(metadata.get("github_branch") or metadata.get("branch") or ""),
            )
        )
    return sorted(plan, key=lambda item: item.path)


def apply_plan(skills_dir: Path, plan: list[Remediation]) -> None:
    skills_dir = skills_dir.resolve()
    scanner = SecurityScanner(require_metadata=True)

    # Validate every target before the first mutation so a stale report cannot
    # leave a partially remediated archive.
    resolved: list[tuple[Remediation, Path, str | None]] = []
    for item in plan:
        skill_path = _safe_skill_path(skills_dir, item.path)
        if source_content_hash(skill_path.parent) != item.content_sha256:
            raise ValueError(f"Archived content changed after planning: {item.path}")
        metadata = _load_json_object(skill_path.parent / "metadata.json", "archive metadata")
        normalized: str | None = None
        if item.action == "normalize_frontmatter":
            content = skill_path.read_text(encoding="utf-8")
            normalized = normalize_skill_frontmatter(
                content,
                metadata,
                fallback_name=skill_path.parent.name,
            )
            if normalized == content:
                raise ValueError(f"Frontmatter remediation made no change: {item.path}")
            is_safe, issues = scanner.scan_content(normalized, skill_path)
            if not is_safe:
                error_types = sorted(
                    {
                        issue.get("type")
                        for issue in issues
                        if issue.get("severity") == "error"
                    }
                )
                raise ValueError(
                    f"Planned normalized skill remains unsafe: {item.path}: {error_types}"
                )
        elif item.action != "quarantine":
            raise ValueError(f"Unknown remediation action: {item.action}")
        resolved.append((item, skill_path, normalized))

    for item, skill_path, normalized in resolved:
        if item.action == "quarantine":
            shutil.rmtree(skill_path.parent)
            continue
        if normalized is None:
            raise ValueError(f"Normalized content is missing: {item.path}")
        skill_path.write_text(normalized, encoding="utf-8")


def write_audit(path: Path, report: dict[str, Any], plan: list[Remediation], applied: bool) -> None:
    payload = {
        "schema_version": 1,
        "source_report": {
            "scanner": report["scanner"],
            "generated_at": report.get("generated_at"),
            "total": report["total"],
            "passed": report["passed"],
            "failed": report["failed"],
        },
        "applied": applied,
        "counts": {
            "total": len(plan),
            "normalize_frontmatter": sum(item.action == "normalize_frontmatter" for item in plan),
            "quarantine": sum(item.action == "quarantine" for item in plan),
        },
        "remediations": [asdict(item) for item in plan],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--security-report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True, help="Audit plan/result JSON")
    parser.add_argument("--apply", action="store_true", help="Apply the plan (default is dry-run)")
    args = parser.parse_args()

    skills_dir = args.skills_dir.resolve()
    output = args.output.resolve()
    if not skills_dir.is_dir():
        raise ValueError(f"Skills directory does not exist: {skills_dir}")
    try:
        output.relative_to(skills_dir)
    except ValueError:
        pass
    else:
        raise ValueError("Audit output must be outside the archive root")

    report = _load_json_object(args.security_report.resolve(), "security report")
    plan = build_plan(skills_dir, report)
    if args.apply:
        apply_plan(skills_dir, plan)
    write_audit(output, report, plan, args.apply)

    normalized = sum(item.action == "normalize_frontmatter" for item in plan)
    quarantined = sum(item.action == "quarantine" for item in plan)
    mode = "Applied" if args.apply else "Planned"
    print(f"{mode}: {len(plan)} total, {normalized} normalized, {quarantined} quarantined")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
