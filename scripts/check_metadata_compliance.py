#!/usr/bin/env python3
"""
Validate attribution and license metadata for skills.

By default this script scans all `skills/**/metadata.json`.
When `--file-list` is provided, it validates only metadata related to changed files.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

import jsonschema
from utils import classify_license, is_valid_https_url, normalize_license, normalize_repo

PLACEHOLDER_AUTHOR_VALUES = {"", "n/a", "na", "none", "null", "tbd", "unknown"}

LICENSE_NOTICE_TEXTS = {
    "MIT": [
        'Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:',
        "",
        "The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.",
        "",
        'THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.',
    ],
}


def load_schema(schema_path: Path) -> dict:
    return json.loads(schema_path.read_text(encoding="utf-8"))


def display_path(path: Path, repo_root: Path) -> str:
    try:
        return str(path.relative_to(repo_root))
    except ValueError:
        return str(path)


def parse_file_list(
    repo_root: Path,
    skills_dir: Path,
    file_list: Path,
) -> Tuple[List[Path], List[str]]:
    """
    Resolve changed files into metadata.json targets.

    Returns:
      - metadata_paths: metadata files to validate
      - missing_metadata: changed skill files that do not have metadata.json
    """
    if not file_list.exists():
        return [], []

    targets = set()
    missing_metadata = []

    for raw_line in file_list.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw_line.strip()
        if not line:
            continue

        candidate = Path(line)
        if not candidate.is_absolute():
            candidate = (repo_root / candidate).resolve()
        else:
            candidate = candidate.resolve()

        try:
            candidate.relative_to(skills_dir)
        except ValueError:
            continue

        if candidate.name == "metadata.json":
            targets.add(candidate)
            continue

        if candidate.name == "SKILL.md":
            meta_path = candidate.parent / "metadata.json"
            if meta_path.exists():
                targets.add(meta_path)
            else:
                missing_metadata.append(display_path(meta_path, repo_root))
            continue

        if candidate.is_dir():
            meta_path = candidate / "metadata.json"
        else:
            meta_path = candidate.parent / "metadata.json"

        if meta_path.exists():
            targets.add(meta_path)

    return sorted(targets), sorted(set(missing_metadata))


def iter_all_metadata(skills_dir: Path) -> List[Path]:
    return sorted(skills_dir.rglob("metadata.json"))


def validate_single_metadata(
    metadata_path: Path,
    schema: dict,
) -> Tuple[List[str], List[str], Dict]:
    errors: List[str] = []
    warnings: List[str] = []

    try:
        raw = json.loads(metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"Invalid JSON: {exc}"], [], {}
    except Exception as exc:  # pragma: no cover - defensive
        return [f"Cannot read metadata: {exc}"], [], {}

    try:
        jsonschema.validate(instance=raw, schema=schema)
    except jsonschema.ValidationError as exc:
        path = ".".join(str(p) for p in exc.path) or "<root>"
        errors.append(f"Schema validation failed at {path}: {exc.message}")
    except jsonschema.SchemaError as exc:
        errors.append(f"Metadata schema is invalid: {exc}")

    author = str(raw.get("author", "")).strip()
    if author.lower() in PLACEHOLDER_AUTHOR_VALUES:
        errors.append("author is missing or placeholder value")

    source_url = str(raw.get("source_url", "")).strip()
    if not is_valid_https_url(source_url):
        errors.append("source_url must be a valid https URL")

    repo = normalize_repo(raw.get("repo", ""))
    if repo and "github.com" in source_url and f"github.com/{repo}" not in source_url:
        warnings.append("source_url does not appear to match repo")

    permission_note = str(raw.get("permission_note", "")).strip()
    if len(permission_note) < 10:
        errors.append("permission_note must be descriptive (>= 10 characters)")

    copyright_notice = str(raw.get("copyright", "")).strip()
    if len(copyright_notice) < 5:
        errors.append("copyright must be descriptive")

    declared_distribution = str(raw.get("distribution", "")).strip()
    normalized = normalize_license(raw.get("license", ""))
    detected_class = classify_license(normalized)

    if detected_class == "unknown":
        errors.append(
            f'license "{normalized}" is unknown; use SPDX ID or mark as NOASSERTION/restricted'
        )

    if detected_class == "restricted" and declared_distribution != "restricted":
        errors.append(f'distribution must be "restricted" for license "{normalized}"')

    if detected_class == "compatible" and declared_distribution != "compatible":
        warnings.append(
            f'distribution is "{declared_distribution}" but license "{normalized}" is compatible'
        )

    if normalized != str(raw.get("license", "")).strip():
        warnings.append(f'license normalized to "{normalized}"')

    entry = {
        "name": raw.get("name", ""),
        "local_path": (
            f"skills/{str(raw.get('category', '')).strip()}/{str(raw.get('dir_name', '')).strip()}"
        ),
        "repo": repo,
        "author": author,
        "license": normalized,
        "copyright": copyright_notice,
        "distribution": declared_distribution,
        "source_url": source_url,
        "permission_note": permission_note,
    }
    return errors, warnings, entry


def write_notices(path: Path, rows: List[Dict], scanned_count: int) -> None:
    generated_at = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    distribution_counts = Counter((row.get("distribution") or "unknown") for row in rows)

    lines = [
        "# THIRD_PARTY_NOTICES",
        "",
        f"_Generated at: {generated_at}_",
        "",
        "This repository's code and pipeline are MIT-licensed, but each third-party skill keeps its original license.",
        "Do not assume a skill is MIT unless its metadata explicitly marks it as compatible.",
        "",
        "## Summary",
        "",
        f"- Metadata entries scanned: **{scanned_count}**",
        f"- Notice rows generated: **{len(rows)}**",
        f"- Compatible entries: **{distribution_counts.get('compatible', 0)}**",
        f"- Restricted entries: **{distribution_counts.get('restricted', 0)}**",
        "",
    ]

    if not rows:
        lines.extend(
            [
                "## Entries",
                "",
                "No metadata entries were selected for this run.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "## Entries",
                "",
                "| Skill | Local path | Repo | Author | License | Copyright | Distribution | Source | Permission note |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
            ]
        )
        for row in sorted(rows, key=lambda item: (item.get("repo", ""), item.get("name", ""))):
            name = str(row.get("name", "")).replace("|", "\\|")
            local_path = str(row.get("local_path", "")).replace("|", "\\|")
            repo = str(row.get("repo", "")).replace("|", "\\|")
            author = str(row.get("author", "")).replace("|", "\\|")
            license_name = str(row.get("license", "")).replace("|", "\\|")
            copyright_notice = str(row.get("copyright", "")).replace("|", "\\|")
            distribution = str(row.get("distribution", "")).replace("|", "\\|")
            source_url = str(row.get("source_url", ""))
            permission_note = str(row.get("permission_note", "")).replace("|", "\\|")
            lines.append(
                f"| {name} | {local_path} | {repo} | {author} | {license_name} | {copyright_notice} | {distribution} | {source_url} | {permission_note} |"
            )
        lines.append("")

        license_names = sorted(
            {
                str(row.get("license", "")).strip()
                for row in rows
                if str(row.get("license", "")).strip() in LICENSE_NOTICE_TEXTS
            }
        )
        if license_names:
            lines.extend(["## License Texts", ""])
            for license_name in license_names:
                lines.extend([f"### {license_name}", ""])
                lines.extend(LICENSE_NOTICE_TEXTS[license_name])
                lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate skill metadata attribution/license compliance"
    )
    parser.add_argument("--skills-dir", default="skills", help="Skills directory root")
    parser.add_argument(
        "--metadata-schema",
        default="schema/metadata.schema.json",
        help="Path to metadata JSON schema",
    )
    parser.add_argument(
        "--file-list",
        help="Optional newline-delimited changed files list (relative to repo root)",
    )
    parser.add_argument("--output-json", help="Write JSON report to this path")
    parser.add_argument("--notices", help="Write THIRD_PARTY_NOTICES markdown to this path")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail (exit 1) when compliance errors are found",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Always exit 0 after generating report artifacts",
    )
    parser.add_argument(
        "--fail-on-warnings", action="store_true", help="Treat warnings as failures"
    )
    args = parser.parse_args()

    repo_root = Path.cwd().resolve()
    skills_dir = (repo_root / args.skills_dir).resolve()
    schema_path = (repo_root / args.metadata_schema).resolve()

    if not skills_dir.exists():
        print(f"ERROR: skills directory not found: {skills_dir}")
        return 1
    if not schema_path.exists():
        print(f"ERROR: metadata schema not found: {schema_path}")
        return 1

    schema = load_schema(schema_path)

    missing_metadata: List[str] = []
    if args.file_list:
        file_list_path = (repo_root / args.file_list).resolve()
        targets, missing_metadata = parse_file_list(repo_root, skills_dir, file_list_path)
    else:
        targets = iter_all_metadata(skills_dir)

    if not targets and not missing_metadata:
        print("No metadata targets to validate.")
        if args.notices:
            write_notices((repo_root / args.notices).resolve(), [], scanned_count=0)
        if args.output_json:
            output_path = (repo_root / args.output_json).resolve()
            output_path.write_text(
                json.dumps(
                    {
                        "scanned": 0,
                        "missing_metadata": 0,
                        "errors": 0,
                        "warnings": 0,
                        "results": [],
                    },
                    indent=2,
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )
        return 0

    results = []
    total_errors = 0
    total_warnings = 0
    valid_rows = []

    for missing in missing_metadata:
        total_errors += 1
        results.append(
            {
                "path": missing,
                "errors": ["metadata.json is missing for changed skill directory"],
                "warnings": [],
            }
        )

    for metadata_path in targets:
        errors, warnings, row = validate_single_metadata(metadata_path, schema)
        total_errors += len(errors)
        total_warnings += len(warnings)

        if row and not errors:
            valid_rows.append(row)

        results.append(
            {
                "path": display_path(metadata_path, repo_root),
                "errors": errors,
                "warnings": warnings,
            }
        )

    if args.notices:
        write_notices((repo_root / args.notices).resolve(), valid_rows, scanned_count=len(targets))

    report = {
        "scanned": len(targets),
        "missing_metadata": len(missing_metadata),
        "errors": total_errors,
        "warnings": total_warnings,
        "results": results,
    }

    if args.output_json:
        output_path = (repo_root / args.output_json).resolve()
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    print("=" * 60)
    print("METADATA COMPLIANCE REPORT")
    print("=" * 60)
    print(f"Scanned metadata files: {len(targets)}")
    print(f"Missing metadata files: {len(missing_metadata)}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")

    if total_errors > 0:
        print("\nTop failing paths:")
        shown = 0
        for row in results:
            if not row["errors"]:
                continue
            print(f"- {row['path']}")
            for message in row["errors"][:3]:
                print(f"    * {message}")
            shown += 1
            if shown >= 10:
                break

    if args.report_only:
        return 0
    if args.strict and total_errors > 0:
        return 1
    if args.strict and args.fail_on_warnings and total_warnings > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
