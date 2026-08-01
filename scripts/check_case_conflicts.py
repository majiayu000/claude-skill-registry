#!/usr/bin/env python3
"""
Check for case-sensitivity conflicts in skill directories.

This script detects directory names that differ only in case,
which causes issues on case-insensitive filesystems (macOS, Windows).

Usage:
    python scripts/check_case_conflicts.py [--fix]
"""

import argparse
import sys
from collections import defaultdict
from pathlib import Path


def find_case_conflicts(skills_dir: Path) -> dict:
    """Find directories that differ only in case."""
    conflicts = defaultdict(list)

    # Scan all directories
    for category_dir in skills_dir.iterdir():
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        for skill_dir in category_dir.iterdir():
            if not skill_dir.is_dir():
                continue

            # Group by lowercase name
            key = f"{category_dir.name}/{skill_dir.name.lower()}"
            conflicts[key].append(str(skill_dir.relative_to(skills_dir)))

    # Filter to only actual conflicts (more than one with same lowercase name)
    return {k: v for k, v in conflicts.items() if len(v) > 1}


def main():
    parser = argparse.ArgumentParser(description='Check for case-sensitivity conflicts')
    parser.add_argument('--skills-dir', '-s', default='skills', help='Skills directory')
    parser.add_argument('--fix', action='store_true', help='Attempt to fix conflicts')

    args = parser.parse_args()
    skills_dir = Path(args.skills_dir)

    if not skills_dir.exists():
        print(f"Error: Skills directory not found: {skills_dir}")
        sys.exit(1)

    print(f"Checking for case conflicts in {skills_dir}...")
    conflicts = find_case_conflicts(skills_dir)

    if not conflicts:
        print("✓ No case conflicts found")
        sys.exit(0)

    print(f"\n✗ Found {len(conflicts)} case conflict(s):\n")

    for key, paths in sorted(conflicts.items()):
        print(f"  Conflict: {key}")
        for p in paths:
            print(f"    - {p}")
        print()

    if args.fix:
        print("Auto-fix not implemented yet.")
        print("Please manually resolve conflicts by keeping only lowercase versions.")

    sys.exit(1)


if __name__ == "__main__":
    main()
