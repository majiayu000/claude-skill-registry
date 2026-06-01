#!/usr/bin/env python3
"""Build a report-only readiness summary for a published main artifact."""

from __future__ import annotations

import argparse
import json
from collections.abc import Mapping
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1


def utc_now_isoformat() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def optional_json(path: Path, issues: list[dict[str, str]], *, label: str) -> Any:
    if not path.exists():
        issues.append(
            {
                "severity": "error",
                "code": "missing-artifact",
                "path": str(path),
                "message": f"missing {label}",
            }
        )
        return {}
    try:
        return load_json(path)
    except json.JSONDecodeError as exc:
        issues.append(
            {
                "severity": "error",
                "code": "invalid-json",
                "path": str(path),
                "message": f"{label} is not valid JSON: {exc}",
            }
        )
        return {}


def category_count(stats: Mapping[str, Any], category: str) -> int | None:
    raw_counts = stats.get("category_counts")
    if isinstance(raw_counts, list):
        for item in raw_counts:
            if isinstance(item, Mapping) and item.get("name") == category:
                count = item.get("count")
                return int(count) if isinstance(count, int) else None
    if isinstance(raw_counts, Mapping):
        count = raw_counts.get(category)
        return int(count) if isinstance(count, int) else None
    return None


def manifest_record_count(manifest: Mapping[str, Any]) -> int | None:
    for key in ("count", "record_count", "total_count", "total"):
        count = manifest.get(key)
        if isinstance(count, int):
            return count
    return None


def registry_shard_count(manifest: Mapping[str, Any]) -> int:
    shards = manifest.get("shards")
    return len(shards) if isinstance(shards, list) else 0


def summarize_publish_status(payload: Mapping[str, Any]) -> dict[str, Any]:
    checks = payload.get("checks")
    check_items = checks if isinstance(checks, list) else []
    check_status_counts: dict[str, int] = {}
    for item in check_items:
        if not isinstance(item, Mapping):
            continue
        status = str(item.get("status") or "unknown")
        check_status_counts[status] = check_status_counts.get(status, 0) + 1
    return {
        "status": payload.get("status") or "",
        "github_run_id": payload.get("github_run_id") or "",
        "github_run_url": payload.get("github_run_url") or "",
        "check_count": len(check_items),
        "check_status_counts": dict(sorted(check_status_counts.items())),
    }


def build_report(main_dir: Path, *, category: str = "other") -> dict[str, Any]:
    issues: list[dict[str, str]] = []
    docs_dir = main_dir / "docs"
    stats = optional_json(docs_dir / "stats.json", issues, label="docs stats")
    category_manifest = optional_json(
        docs_dir / "categories" / category / "manifest.json",
        issues,
        label=f"{category} category manifest",
    )
    registry_manifest = optional_json(
        main_dir / "registry-manifest.json",
        issues,
        label="registry manifest",
    )
    provenance = optional_json(
        main_dir / "provenance" / "merge-source.json",
        issues,
        label="merge provenance",
    )
    publish_status = optional_json(
        main_dir / "provenance" / "publish-status.json",
        issues,
        label="publish status",
    )

    stats_category_count = category_count(stats, category) if isinstance(stats, Mapping) else None
    manifest_category_count = (
        manifest_record_count(category_manifest)
        if isinstance(category_manifest, Mapping)
        else None
    )
    if (
        stats_category_count is not None
        and manifest_category_count is not None
        and stats_category_count != manifest_category_count
    ):
        issues.append(
            {
                "severity": "error",
                "code": "category-count-mismatch",
                "path": f"docs/categories/{category}/manifest.json",
                "message": (
                    f"docs/stats.json reports {category}={stats_category_count}, "
                    f"manifest reports {manifest_category_count}"
                ),
            }
        )

    publish_summary = (
        summarize_publish_status(publish_status)
        if isinstance(publish_status, Mapping)
        else summarize_publish_status({})
    )
    if publish_summary["status"] and publish_summary["status"] != "passed":
        issues.append(
            {
                "severity": "warning",
                "code": "publish-status-not-passed",
                "path": "provenance/publish-status.json",
                "message": f"publish status is {publish_summary['status']!r}",
            }
        )

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    readiness = "ready" if error_count == 0 else "not_ready"
    if readiness == "ready" and warning_count:
        readiness = "ready_with_warnings"

    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": utc_now_isoformat(),
        "main_dir": str(main_dir),
        "readiness": readiness,
        "category": category,
        "category_count": manifest_category_count,
        "stats_category_count": stats_category_count,
        "archive_skill_md_count_raw": stats.get("archive_skill_md_count_raw")
        if isinstance(stats, Mapping)
        else None,
        "archive_metadata_count_raw": stats.get("archive_metadata_count_raw")
        if isinstance(stats, Mapping)
        else None,
        "registry_skill_count_dedup": stats.get("registry_skill_count_dedup")
        if isinstance(stats, Mapping)
        else None,
        "category_total": stats.get("categories") if isinstance(stats, Mapping) else None,
        "registry_manifest": {
            "shard_count": registry_shard_count(registry_manifest)
            if isinstance(registry_manifest, Mapping)
            else 0,
            "record_count": manifest_record_count(registry_manifest)
            if isinstance(registry_manifest, Mapping)
            else None,
        },
        "provenance": {
            "core_repo": provenance.get("core_repo") if isinstance(provenance, Mapping) else "",
            "core_sha": provenance.get("core_sha") if isinstance(provenance, Mapping) else "",
            "data_repo": provenance.get("data_repo") if isinstance(provenance, Mapping) else "",
            "data_sha": provenance.get("data_sha") if isinstance(provenance, Mapping) else "",
            "generated_at": provenance.get("generated_at")
            if isinstance(provenance, Mapping)
            else "",
        },
        "publish_status": publish_summary,
        "issue_count": len(issues),
        "error_count": error_count,
        "warning_count": warning_count,
        "issues": issues,
        "notes": [
            "This is report-only and does not implement a publish gate.",
            "Use it for release acceptance, issue comments, and provenance review.",
        ],
    }


def print_report(report: dict[str, Any]) -> None:
    print("Publish readiness report")
    print(f"Readiness: {report['readiness']}")
    print(f"{report['category']} count: {report['category_count']}")
    print(f"Archive skills: {report['archive_skill_md_count_raw']}")
    print(f"Registry deduped skills: {report['registry_skill_count_dedup']}")
    print(f"Publish status: {report['publish_status']['status']}")
    print(f"Core SHA: {report['provenance']['core_sha']}")
    print(f"Data SHA: {report['provenance']['data_sha']}")
    print(f"Errors: {report['error_count']}")
    print(f"Warnings: {report['warning_count']}")
    for issue in report["issues"][:20]:
        print(f"- {issue['severity']} {issue['code']} {issue['path']}: {issue['message']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--main-dir", type=Path, default=Path("."))
    parser.add_argument("--category", default="other")
    parser.add_argument("--output-json", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(args.main_dir, category=args.category)
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
