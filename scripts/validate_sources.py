#!/usr/bin/env python3
"""
Validate ``sources/*.json`` shape, repo references, and category codes.

Most contributor PRs add a row to ``sources/community.json`` (the README's
"Option 2: Submit via PR" path). The crawler later trusts those rows.
This script runs offline, prints a single-line message per problem, and
exits non-zero only when there is a structural error so it can be wired
into CI without false positives from optional / advisory checks.

Usage::

    python scripts/validate_sources.py                # validate every sources/*.json
    python scripts/validate_sources.py community.json # only one file
    python scripts/validate_sources.py --strict       # fail on warnings too
    python scripts/validate_sources.py --json         # machine-readable output
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

# -- Constants kept in sync with schema/skill.schema.json + README ---------

VALID_CATEGORIES: frozenset[str] = frozenset(
    {
        "development",
        "testing",
        "data",
        "design",
        "documents",
        "productivity",
        "devops",
        "security",
        "marketing",
        "product",
        "communication",
        "creative",
        "official",
        "other",
    }
)

REPO_PATTERN = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
TAG_PATTERN = re.compile(r"^[a-z0-9-]+$")


def _has_path_traversal(path: str) -> bool:
    """Detect ``..`` traversal segments regardless of separator style.

    ``Path("a\\..\\b").parts`` returns a single piece on POSIX runners,
    so this helper splits on both ``/`` and ``\\`` before checking.
    """
    if not path:
        return False
    for separator in ("/", "\\"):
        for segment in path.split(separator):
            if segment == "..":
                return True
    return False

# Source files produced by discovery jobs may carry intentionally partial rows.
DISCOVERY_SOURCE_FILES = frozenset({"discovered.json", "github_search.json", "crawled.json"})

# Files we may legitimately skip — auto-generated indexes, blocklists, etc.
NON_SKILL_TOPLEVEL_KEYS = ("entries", "blocked_repos", "plugins")
EXPECTED_TOPLEVEL_KEYS = ("skills", *NON_SKILL_TOPLEVEL_KEYS)


# -- Reporting -------------------------------------------------------------


@dataclass
class Issue:
    """One structural finding from validation."""

    file: str
    severity: str  # "error" | "warning"
    code: str
    message: str
    location: str = ""

    def format_line(self) -> str:
        loc = f" [{self.location}]" if self.location else ""
        return f"{self.severity.upper()} {self.file}{loc} {self.code}: {self.message}"


@dataclass
class Report:
    issues: list[Issue] = field(default_factory=list)
    files_scanned: int = 0
    skills_scanned: int = 0
    seen_keys: set[str] = field(default_factory=set)

    @property
    def errors(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "error"]

    @property
    def warnings(self) -> list[Issue]:
        return [i for i in self.issues if i.severity == "warning"]

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)


# -- Validators ------------------------------------------------------------


def _validate_string(value: Any, *, max_len: int) -> str | None:
    if not isinstance(value, str):
        return "must be a string"
    if not value.strip():
        return "must be non-empty"
    if len(value) > max_len:
        return f"must be at most {max_len} chars (got {len(value)})"
    return None


def validate_skill_entry(
    entry: Any,
    *,
    file: str,
    location: str,
    report: Report,
    require_category: bool = True,
    default_repo: str | None = None,
) -> None:
    """Validate a single skill row inside ``sources/<source>.json``.

    Required fields: ``name``, ``repo`` (or top-level ``repo`` inherited via
    ``default_repo``), ``description``.
    Optional fields: ``path``, ``category``, ``tags``, ``stars``, ``featured``.
    ``location`` is something like ``skills[3]`` so reviewers can jump to the row.
    """
    if not isinstance(entry, dict):
        report.add(
            Issue(file, "error", "E_NOT_OBJECT", "skill entry must be an object", location)
        )
        return

    # Required: name
    err = _validate_string(entry.get("name"), max_len=64)
    if err:
        report.add(Issue(file, "error", "E_NAME", f"name {err}", location))
    elif not NAME_PATTERN.match(entry["name"]):
        report.add(
            Issue(
                file,
                "warning",
                "W_NAME_PATTERN",
                "name should match ^[a-z0-9][a-z0-9-]{0,63}$ (recommended for path safety)",
                location,
            )
        )

    # Required: repo (may be inherited from top-level ``repo``).
    repo = entry.get("repo", default_repo)
    err = _validate_string(repo, max_len=140)
    if err:
        report.add(Issue(file, "error", "E_REPO", f"repo {err}", location))
    elif not REPO_PATTERN.match(repo):
        report.add(
            Issue(
                file,
                "error",
                "E_REPO_FORMAT",
                "repo must look like 'owner/name' (got '{}')".format(repo),
                location,
            )
        )

    # Required: description (community PRs sometimes ship empty strings).
    err = _validate_string(entry.get("description"), max_len=500)
    if err:
        report.add(Issue(file, "error", "E_DESCRIPTION", f"description {err}", location))
    elif len(entry["description"]) < 10:
        report.add(
            Issue(
                file,
                "warning",
                "W_DESCRIPTION_SHORT",
                "description is shorter than 10 chars; reviewers will likely ask to expand",
                location,
            )
        )

    # Optional: path
    path = entry.get("path")
    if path is not None:
        if not isinstance(path, str):
            report.add(Issue(file, "error", "E_PATH_TYPE", "path must be a string", location))
        elif path.startswith("/"):
            report.add(
                Issue(
                    file,
                    "error",
                    "E_PATH_LEADING_SLASH",
                    "path must be a repo-relative path, not start with '/'",
                    location,
                )
            )
        elif _has_path_traversal(path):
            report.add(
                Issue(file, "error", "E_PATH_TRAVERSAL", "path must not contain '..'", location)
            )

    # Optional: category — required for non-discovery sources.
    category = entry.get("category")
    if category is None:
        if require_category:
            report.add(
                Issue(
                    file,
                    "warning",
                    "W_CATEGORY_MISSING",
                    "category missing; will fall back to 'other'",
                    location,
                )
            )
    elif not isinstance(category, str):
        report.add(
            Issue(file, "error", "E_CATEGORY_TYPE", "category must be a string", location)
        )
    elif category not in VALID_CATEGORIES:
        report.add(
            Issue(
                file,
                "warning",
                "W_CATEGORY_UNKNOWN",
                f"category '{category}' is not in the known set ({sorted(VALID_CATEGORIES)})",
                location,
            )
        )

    # Optional: tags
    tags = entry.get("tags")
    if tags is not None:
        if not isinstance(tags, list):
            report.add(Issue(file, "error", "E_TAGS_TYPE", "tags must be an array", location))
        elif len(tags) > 10:
            report.add(
                Issue(
                    file,
                    "warning",
                    "W_TAGS_OVERFLOW",
                    f"tags has {len(tags)} entries; only the first 10 are surfaced",
                    location,
                )
            )
        else:
            for i, tag in enumerate(tags):
                if not isinstance(tag, str) or not TAG_PATTERN.match(tag):
                    report.add(
                        Issue(
                            file,
                            "warning",
                            "W_TAG_FORMAT",
                            f"tag #{i} '{tag!r}' should be lowercase alphanumeric with hyphens",
                            location,
                        )
                    )

    # Optional: stars
    stars = entry.get("stars")
    if stars is not None and not isinstance(stars, int):
        report.add(
            Issue(file, "warning", "W_STARS_TYPE", "stars should be an integer", location)
        )

    # Optional: featured
    featured = entry.get("featured")
    if featured is not None and not isinstance(featured, bool):
        report.add(
            Issue(
                file,
                "warning",
                "W_FEATURED_TYPE",
                "featured should be true or false",
                location,
            )
        )

    # De-duplication key across all sources. Use repo+path because the same
    # repo can host several skills under different paths.
    if isinstance(repo, str) and (path is None or isinstance(path, str)):
        key = f"{repo.strip()}:{(path or '').strip().strip('/')}"
        if key in report.seen_keys:
            report.add(
                Issue(
                    file,
                    "warning",
                    "W_DUPLICATE",
                    f"duplicate skill key '{key}' already declared in another file",
                    location,
                )
            )
        report.seen_keys.add(key)

    report.skills_scanned += 1


def validate_file(path: Path, report: Report) -> None:
    """Validate one ``sources/<name>.json`` file."""
    file_label = str(path.name)
    report.files_scanned += 1

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.add(Issue(file_label, "error", "E_NOT_FOUND", "file not found"))
        return
    except json.JSONDecodeError as exc:
        report.add(Issue(file_label, "error", "E_JSON", f"invalid JSON: {exc}"))
        return

    if not isinstance(data, dict):
        report.add(Issue(file_label, "error", "E_TOPLEVEL", "top level must be an object"))
        return

    if not any(k in data for k in EXPECTED_TOPLEVEL_KEYS):
        report.add(
            Issue(
                file_label,
                "warning",
                "W_TOPLEVEL_KEYS",
                f"missing one of {EXPECTED_TOPLEVEL_KEYS}; nothing will be ingested",
            )
        )
        return

    skills = data.get("skills")
    if skills is not None:
        if not isinstance(skills, list):
            report.add(Issue(file_label, "error", "E_SKILLS_TYPE", "skills must be an array"))
            return

        is_discovery = path.name in DISCOVERY_SOURCE_FILES
        if is_discovery:
            # Auto-discovered sources (discovered.json / github_search.json /
            # crawled.json) carry partial rows produced by crawlers — name and
            # category are derived later. Treat them as advisory: only check
            # the structural keys we always rely on.
            _validate_discovery_entries(skills, file_label, report)
            return

        # Some curated catalogs (e.g. anthropic.json) declare the repo at the
        # top level and the rows only carry path. Inherit it so per-row
        # validation does not flag a structural error that the loader handles.
        default_repo = data.get("repo") if isinstance(data.get("repo"), str) else None

        for i, entry in enumerate(skills):
            validate_skill_entry(
                entry,
                file=file_label,
                location=f"skills[{i}]",
                report=report,
                require_category=True,
                default_repo=default_repo,
            )


def _validate_discovery_entries(
    skills: list[Any], file_label: str, report: Report
) -> None:
    """Lighter validation for auto-discovered (non-curated) source files.

    The crawler emits incomplete rows (no name, no category) on purpose;
    failing here would give contributors red CI for files they did not edit.
    We still enforce repo presence + format and ``path`` safety so a poisoned
    discovery file cannot smuggle in repo strings the downloader would trust.
    """
    for i, entry in enumerate(skills):
        location = f"skills[{i}]"
        if not isinstance(entry, dict):
            report.add(
                Issue(
                    file_label,
                    "error",
                    "E_NOT_OBJECT",
                    "skill entry must be an object",
                    location,
                )
            )
            continue

        repo = entry.get("repo")
        if not isinstance(repo, str) or not repo.strip():
            report.add(
                Issue(file_label, "error", "E_REPO", "repo must be a non-empty string", location)
            )
            continue
        if not REPO_PATTERN.match(repo):
            report.add(
                Issue(
                    file_label,
                    "error",
                    "E_REPO_FORMAT",
                    f"repo must look like 'owner/name' (got '{repo}')",
                    location,
                )
            )

        path_value = entry.get("path")
        if path_value is not None and not isinstance(path_value, str):
            report.add(Issue(file_label, "error", "E_PATH_TYPE", "path must be a string", location))
        elif isinstance(path_value, str):
            if path_value.startswith("/"):
                report.add(
                    Issue(
                        file_label,
                        "error",
                        "E_PATH_LEADING_SLASH",
                        "path must be repo-relative",
                        location,
                    )
                )
            elif _has_path_traversal(path_value):
                report.add(
                    Issue(
                        file_label,
                        "error",
                        "E_PATH_TRAVERSAL",
                        "path must not contain '..'",
                        location,
                    )
                )

        report.skills_scanned += 1


# -- CLI -------------------------------------------------------------------


def discover_targets(sources_dir: Path, names: Iterable[str]) -> list[Path]:
    requested = list(names)
    if requested:
        return [sources_dir / n if not Path(n).is_absolute() else Path(n) for n in requested]
    return sorted(sources_dir.glob("*.json"))


def render_text(report: Report, *, strict: bool) -> int:
    for issue in report.issues:
        print(issue.format_line())
    print(
        f"\nScanned {report.files_scanned} file(s), {report.skills_scanned} skill row(s); "
        f"errors={len(report.errors)}, warnings={len(report.warnings)}"
    )
    if report.errors:
        return 1
    if strict and report.warnings:
        return 2
    return 0


def render_json(report: Report) -> str:
    payload = {
        "files_scanned": report.files_scanned,
        "skills_scanned": report.skills_scanned,
        "errors": [
            {
                "file": i.file,
                "code": i.code,
                "message": i.message,
                "location": i.location,
            }
            for i in report.errors
        ],
        "warnings": [
            {
                "file": i.file,
                "code": i.code,
                "message": i.message,
                "location": i.location,
            }
            for i in report.warnings
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        "files",
        nargs="*",
        help="specific source filenames (relative to sources/) or absolute paths",
    )
    parser.add_argument(
        "--sources-dir",
        default="sources",
        help="directory containing source files (default: sources)",
    )
    parser.add_argument("--strict", action="store_true", help="exit non-zero on warnings too")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    sources_dir = Path(args.sources_dir)
    if not sources_dir.exists():
        print(f"ERROR: sources directory not found: {sources_dir}", file=sys.stderr)
        return 2

    targets = discover_targets(sources_dir, args.files)
    if not targets:
        print(f"WARNING: no source files matched in {sources_dir}", file=sys.stderr)
        return 0

    report = Report()
    for path in targets:
        validate_file(path, report)

    if args.json:
        print(render_json(report))
        return 1 if report.errors else (2 if args.strict and report.warnings else 0)

    return render_text(report, strict=args.strict)


if __name__ == "__main__":
    sys.exit(main())
