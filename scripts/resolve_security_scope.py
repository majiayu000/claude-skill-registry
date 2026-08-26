#!/usr/bin/env python3
"""Resolve the exact full or Git-diff security scan target set."""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from security_scope import discover_scan_targets, resolve_scan_paths


def _git_paths(skills_dir: Path) -> list[str]:
    commands = (
        ["git", "-C", str(skills_dir), "diff", "--name-only", "-z", "--diff-filter=ACMRTUXB"],
        ["git", "-C", str(skills_dir), "ls-files", "--others", "--exclude-standard", "-z"],
    )
    raw_paths: list[bytes] = []
    for command in commands:
        completed = subprocess.run(command, check=True, capture_output=True)
        raw_paths.extend(part for part in completed.stdout.split(b"\0") if part)
    try:
        return [path.decode("utf-8") for path in raw_paths]
    except UnicodeDecodeError as exc:
        raise RuntimeError("Git returned a non-UTF-8 archive path") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--skills-dir", type=Path, required=True)
    parser.add_argument("--mode", choices=("full", "incremental"), required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.mode == "full":
        targets = discover_scan_targets(args.skills_dir)
    else:
        targets = resolve_scan_paths(
            args.skills_dir,
            _git_paths(args.skills_dir),
            fail_unmapped=True,
        )

    root = Path(args.skills_dir).resolve()
    payload = b"".join(
        target.resolve().relative_to(root).as_posix().encode("utf-8") + b"\0"
        for target in targets
    )
    args.output.write_bytes(payload)
    print(len(targets))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
