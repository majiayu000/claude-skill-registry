#!/usr/bin/env python3
"""Verify generated category artifacts stay sharded and pointer-only."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_POINTER_MAX_BYTES = 16 * 1024
DEFAULT_PART_MAX_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True)
class ArtifactIssue:
    severity: str
    code: str
    path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {
            "severity": self.severity,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _relative(path: Path, root: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def build_report(
    categories_dir: Path,
    *,
    pointer_max_bytes: int = DEFAULT_POINTER_MAX_BYTES,
    part_max_bytes: int = DEFAULT_PART_MAX_BYTES,
) -> dict[str, Any]:
    issues: list[ArtifactIssue] = []
    pointer_count = 0
    part_count = 0
    largest_pointer_bytes = 0
    largest_part_bytes = 0

    if not categories_dir.exists():
        issues.append(
            ArtifactIssue(
                severity="error",
                code="missing-categories-dir",
                path=str(categories_dir),
                message="categories directory does not exist",
            )
        )
    else:
        for pointer_path in sorted(categories_dir.glob("*.json")):
            if pointer_path.name == "index.json":
                continue
            pointer_count += 1
            pointer_size = pointer_path.stat().st_size
            largest_pointer_bytes = max(largest_pointer_bytes, pointer_size)
            rel_path = _relative(pointer_path, categories_dir.parent)
            if pointer_size > pointer_max_bytes:
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-pointer-too-large",
                        path=rel_path,
                        message=(
                            f"category compatibility pointer is {pointer_size} bytes; "
                            f"expected <= {pointer_max_bytes}"
                        ),
                    )
                )

            payload = load_json(pointer_path)
            if not isinstance(payload, dict):
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-pointer-shape",
                        path=rel_path,
                        message="category pointer must be a JSON object",
                    )
                )
                continue
            if payload.get("deprecated_full_payload") is not True:
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-pointer-not-marked",
                        path=rel_path,
                        message="category pointer must set deprecated_full_payload=true",
                    )
                )
            if "skills" in payload:
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-pointer-contains-skills",
                        path=rel_path,
                        message="legacy category pointer must not contain full skills payload",
                    )
                )
            manifest_ref = payload.get("manifest")
            if not isinstance(manifest_ref, str) or not manifest_ref:
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-pointer-missing-manifest",
                        path=rel_path,
                        message="category pointer must reference a manifest",
                    )
                )
                continue
            manifest_path = categories_dir.parent / manifest_ref
            if not manifest_path.exists():
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-manifest-missing",
                        path=manifest_ref,
                        message="category manifest referenced by pointer does not exist",
                    )
                )

        for part_path in sorted(categories_dir.glob("*/part-*.json")):
            part_count += 1
            part_size = part_path.stat().st_size
            largest_part_bytes = max(largest_part_bytes, part_size)
            if part_size > part_max_bytes:
                issues.append(
                    ArtifactIssue(
                        severity="error",
                        code="category-part-too-large",
                        path=_relative(part_path, categories_dir.parent),
                        message=(
                            f"category shard part is {part_size} bytes; "
                            f"expected <= {part_max_bytes}"
                        ),
                    )
                )

    errors = [issue.as_dict() for issue in issues if issue.severity == "error"]
    warnings = [issue.as_dict() for issue in issues if issue.severity == "warning"]
    return {
        "categories_dir": str(categories_dir),
        "pointer_count": pointer_count,
        "part_count": part_count,
        "largest_pointer_bytes": largest_pointer_bytes,
        "largest_part_bytes": largest_part_bytes,
        "pointer_max_bytes": pointer_max_bytes,
        "part_max_bytes": part_max_bytes,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors,
        "warnings": warnings,
    }


def print_report(report: dict[str, Any], *, limit: int) -> None:
    print("Category artifact guard")
    print(f"Pointers: {report['pointer_count']}")
    print(f"Parts: {report['part_count']}")
    print(f"Largest pointer: {report['largest_pointer_bytes']} bytes")
    print(f"Largest part: {report['largest_part_bytes']} bytes")
    print(f"Errors: {report['error_count']}")
    if report["errors"]:
        for item in report["errors"][:limit]:
            print(f"- {item['code']} {item['path']}: {item['message']}")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--categories-dir", type=Path, default=Path("docs/categories"))
    parser.add_argument("--pointer-max-kib", type=int, default=16)
    parser.add_argument("--part-max-mib", type=int, default=10)
    parser.add_argument("--output-json", type=Path)
    parser.add_argument("--limit", type=int, default=20)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    report = build_report(
        args.categories_dir,
        pointer_max_bytes=args.pointer_max_kib * 1024,
        part_max_bytes=args.part_max_mib * 1024 * 1024,
    )
    if args.output_json:
        args.output_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_json.write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    print_report(report, limit=args.limit)
    return 1 if report["error_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
