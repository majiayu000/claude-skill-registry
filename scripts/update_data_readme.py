#!/usr/bin/env python3
"""
Refresh the data repository README archive-size line from the archive tree.
"""

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


ARCHIVE_SIZE_LINE_RE = re.compile(
    r"^- \*\*[\d,]+\*\* `SKILL\.md` files \(as of [^)]+\)$",
    re.MULTILINE,
)


def utc_today() -> str:
    """Return today's UTC date in YYYY-MM-DD."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def count_skill_md_files(archive_dir: Path) -> int:
    """Count all SKILL.md files under the archive root recursively."""
    return sum(1 for _ in archive_dir.rglob("SKILL.md"))


def render_archive_size_line(skill_count: int, as_of_date: str) -> str:
    """Render the README archive size line."""
    return f"- **{skill_count:,}** `SKILL.md` files (as of {as_of_date})"


def update_readme_text(readme_text: str, skill_count: int, as_of_date: str) -> str:
    """Replace the archive-size line in README text."""
    replacement = render_archive_size_line(skill_count, as_of_date)
    updated, replaced = ARCHIVE_SIZE_LINE_RE.subn(replacement, readme_text, count=1)
    if replaced != 1:
        raise ValueError("Could not find unique archive-size line in README.md")
    return updated


def update_readme(readme_path: Path, archive_dir: Path, as_of_date: str | None = None) -> bool:
    """Update README.md in place. Returns True when file content changed."""
    if as_of_date is None:
        as_of_date = utc_today()

    skill_count = count_skill_md_files(archive_dir)
    original = readme_path.read_text(encoding="utf-8")
    updated = update_readme_text(original, skill_count, as_of_date)

    if updated == original:
        return False

    readme_path.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh data repo README archive count")
    parser.add_argument("--archive-dir", required=True, help="Archive root to scan recursively")
    parser.add_argument("--readme", required=True, help="README.md path to update")
    parser.add_argument("--as-of-date", help="Override date in YYYY-MM-DD")
    args = parser.parse_args()

    archive_dir = Path(args.archive_dir).resolve()
    readme_path = Path(args.readme).resolve()

    changed = update_readme(readme_path, archive_dir, args.as_of_date)
    count = count_skill_md_files(archive_dir)
    print(f"README archive count: {count:,}")
    print(f"README updated: {'yes' if changed else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
