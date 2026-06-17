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


def test_accepts_category_only_canonicalization_of_existing_entries():
    base = render_catalog(
        [
            {
                "name": "bridge",
                "repo": "acme/bridge",
                "path": "",
                "description": "Bridge chat systems.",
                "category": "messaging",
                "tags": ["chat"],
                "stars": 0,
            }
        ]
    )
    head = render_catalog(
        [
            {
                "name": "bridge",
                "repo": "acme/bridge",
                "path": "",
                "description": "Bridge chat systems.",
                "category": "communication",
                "tags": ["chat"],
                "stars": 0,
            }
        ]
    )

    assert validate_community_intake_text(base, head) == []


def test_rejects_category_rewrite_from_already_canonical_existing_entry():
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
            }
        ]
    )
    head = render_catalog(
        [
            {
                "name": "alpha",
                "repo": "acme/alpha",
                "path": "",
                "description": "A",
                "category": "documents",
                "tags": ["a"],
                "stars": 0,
            }
        ]
    )

    assert validate_community_intake_text(base, head) == [
        "community intake PRs must preserve the existing `skills` list and append new entries at the end"
    ]


def test_rejects_category_canonicalization_with_whitespace():
    base = render_catalog(
        [
            {
                "name": "bridge",
                "repo": "acme/bridge",
                "path": "",
                "description": "Bridge chat systems.",
                "category": "messaging",
                "tags": ["chat"],
                "stars": 0,
            }
        ]
    )
    head = render_catalog(
        [
            {
                "name": "bridge",
                "repo": "acme/bridge",
                "path": "",
                "description": "Bridge chat systems.",
                "category": "communication ",
                "tags": ["chat"],
                "stars": 0,
            }
        ]
    )

    assert validate_community_intake_text(base, head) == [
        "community intake PRs must preserve the existing `skills` list and append new entries at the end"
    ]


def test_accepts_final_existing_entry_metadata_correction():
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
                "path": "template",
                "description": "B",
                "category": "productivity",
                "tags": ["b"],
                "stars": 0,
                "source_url": "https://github.com/acme/beta/blob/main/template/SKILL.md",
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
                "path": "skills/beta",
                "description": "B",
                "category": "productivity",
                "tags": ["b"],
                "stars": 0,
                "source_url": "https://github.com/acme/beta/blob/main/skills/beta/SKILL.md",
            },
        ]
    )

    assert validate_community_intake_text(base, head) == []


def test_rejects_final_existing_entry_identity_rewrite():
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
            }
        ]
    )
    head = render_catalog(
        [
            {
                "name": "beta",
                "repo": "acme/beta",
                "path": "",
                "description": "B",
                "category": "development",
                "tags": ["b"],
                "stars": 0,
            }
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


def test_rejects_appended_top_level_metadata_fields():
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
        ]
    ).replace('  ]\n}', '  ],\n  "owner": "acme"\n}')

    assert validate_community_intake_text(base, head) == [
        "top-level metadata fields other than `skills` must not change in community intake PRs"
    ]
