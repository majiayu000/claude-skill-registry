import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_community_intake_diff import validate_community_intake_text  # noqa: E402


def render_catalog(skills: list[dict[str, object]]) -> str:
    lines = [
        "{",
        '  "name": "Community Skills",',
        '  "description": "Community-contributed Claude Code skills from GitHub ecosystem",',
        '  "skills": [',
    ]
    for index, skill in enumerate(skills):
        suffix = "," if index < len(skills) - 1 else ""
        lines.append(f"    {json.dumps(skill, ensure_ascii=False)}{suffix}")
    lines.extend(["  ]", "}"])
    return "\n".join(lines) + "\n"


def test_accepts_minimal_append_only_change():
    base = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
        ]
    )
    head = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
            {
                "name": "gamma",
                "repo": "acme/gamma",
                "path": "",
                "description": "C",
                "category": "development",
                "tags": ["c"],
                "stars": 0,
            },
        ]
    )

    assert validate_community_intake_text(base, head) == []


def test_rejects_rewrites_of_existing_entries():
    base = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
        ]
    )
    head = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A updated",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
            {
                "name": "gamma",
                "repo": "acme/gamma",
                "path": "",
                "description": "C",
                "category": "development",
                "tags": ["c"],
                "stars": 0,
            },
        ]
    )

    assert validate_community_intake_text(base, head) == [
        "community intake PRs must preserve the existing `skills` list and append new entries at the end"
    ]


def test_rejects_format_only_changes_without_new_entries():
    base = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
        ]
    )
    head = base.replace('    {"name": "alpha"', '      {"name": "alpha"', 1)

    assert validate_community_intake_text(base, head) == [
        "community intake PRs must add at least one new `skills` entry"
    ]


def test_rejects_reformatting_before_final_existing_entry():
    base = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
        ]
    )
    head = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "development",
                "tags": ["a"],
                "stars": 0,
            },
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            },
            {
                "name": "gamma",
                "repo": "acme/gamma",
                "path": "",
                "description": "C",
                "category": "development",
                "tags": ["c"],
                "stars": 0,
            },
        ]
    )
    head = head.replace('    {"name": "alpha"', '      {"name": "alpha"', 1)

    assert validate_community_intake_text(base, head) == [
        "community intake PRs must not rewrite lines before the final existing catalog entry"
    ]
