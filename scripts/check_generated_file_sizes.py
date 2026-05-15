#!/usr/bin/env python3
"""
Check generated artifact sizes before publish.

GitHub rejects files above 100 MiB. This guard fails earlier so the publish
pipeline stops with a clear diagnosis instead of failing during git push.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

DEFAULT_WARN_MIB = 80
DEFAULT_FAIL_MIB = 90
DEFAULT_INCLUDES = ("registry.json", "registry-shards", "docs")
IGNORED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "htmlcov",
}


@dataclass(frozen=True)
class FileSizeRecord:
    path: Path
    size_bytes: int
    status: str


@dataclass(frozen=True)
class SizeCheckResult:
    records: list[FileSizeRecord]
    warn_bytes: int
    fail_bytes: int

    @property
    def warnings(self) -> list[FileSizeRecord]:
        return [record for record in self.records if record.status == "warning"]

    @property
    def failures(self) -> list[FileSizeRecord]:
        return [record for record in self.records if record.status == "failure"]


def mib_to_bytes(value: float) -> int:
    return int(value * 1024 * 1024)


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_DIR_NAMES for part in path.parts)


def iter_files(path: Path) -> list[Path]:
    if not path.exists():
        return []
    if path.is_file():
        return [] if is_ignored(path) else [path]

    files: list[Path] = []
    for child in path.rglob("*"):
        if is_ignored(child):
            continue
        if child.is_file():
            files.append(child)
    return files


def classify_size(size_bytes: int, warn_bytes: int, fail_bytes: int) -> str:
    if size_bytes >= fail_bytes:
        return "failure"
    if size_bytes >= warn_bytes:
        return "warning"
    return "ok"


def scan_generated_files(
    root: Path,
    includes: list[str],
    warn_bytes: int,
    fail_bytes: int,
) -> SizeCheckResult:
    if warn_bytes >= fail_bytes:
        raise ValueError("warn threshold must be lower than fail threshold")

    records: list[FileSizeRecord] = []
    for include in includes:
        include_path = (root / include).resolve()
        for file_path in iter_files(include_path):
            size_bytes = file_path.stat().st_size
            records.append(
                FileSizeRecord(
                    path=file_path.relative_to(root.resolve()),
                    size_bytes=size_bytes,
                    status=classify_size(size_bytes, warn_bytes, fail_bytes),
                )
            )

    records.sort(key=lambda record: record.size_bytes, reverse=True)
    return SizeCheckResult(records=records, warn_bytes=warn_bytes, fail_bytes=fail_bytes)


def format_bytes(size_bytes: int) -> str:
    return f"{size_bytes / 1024 / 1024:.2f} MiB"


def print_report(result: SizeCheckResult, limit: int) -> None:
    print(
        "Generated artifact size check "
        f"(warn={format_bytes(result.warn_bytes)}, fail={format_bytes(result.fail_bytes)})"
    )
    if not result.records:
        print("No generated files found for the configured include paths.")
        return

    print("Largest generated files:")
    for record in result.records[:limit]:
        print(f"- {record.status:7} {format_bytes(record.size_bytes):>10} {record.path}")

    if result.warnings:
        print(f"Warnings: {len(result.warnings)} file(s) at or above warning threshold.")
    if result.failures:
        print(f"Failures: {len(result.failures)} file(s) at or above failure threshold.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check generated artifact file sizes")
    parser.add_argument("--root", default=".", help="Repository root or generated artifact root")
    parser.add_argument("--warn-mib", type=float, default=DEFAULT_WARN_MIB)
    parser.add_argument("--fail-mib", type=float, default=DEFAULT_FAIL_MIB)
    parser.add_argument(
        "--include",
        action="append",
        default=None,
        help="Generated file or directory to scan, relative to --root. Can be repeated.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of largest files to print.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    includes = args.include if args.include is not None else list(DEFAULT_INCLUDES)
    result = scan_generated_files(
        root=Path(args.root).resolve(),
        includes=includes,
        warn_bytes=mib_to_bytes(args.warn_mib),
        fail_bytes=mib_to_bytes(args.fail_mib),
    )
    print_report(result, args.limit)
    return 1 if result.failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
