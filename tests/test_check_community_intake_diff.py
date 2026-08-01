import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from check_community_intake_diff import (  # noqa: E402
    CommunityIntakeInput,
    validate_community_intake_diff,
    validate_community_intake_text,
)

CATALOG_PATH = Path("sources/community.json")


def make_skill(name: str) -> dict[str, object]:
    return {
        "name": name,
        "repo": f"acme/{name}",
        "path": "",
        "description": name.upper(),
        "category": "development",
        "tags": [name[0]],
        "stars": 0,
    }


def git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def write_catalog(repo: Path, skills: list[dict[str, object]], message: str) -> None:
    target = repo / CATALOG_PATH
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(render_catalog(skills), encoding="utf-8")
    git(repo, "add", str(CATALOG_PATH))
    git(repo, "commit", "-m", message)


def init_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    return repo


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


def test_stale_branch_is_not_treated_as_entry_removal(tmp_path, monkeypatch):
    """A branch cut before base gained new entries must still pass: those entries
    are missing from head because of the fork point, not because the PR removed them."""
    repo = init_repo(tmp_path)
    write_catalog(repo, [make_skill("alpha")], "seed")
    fork_point = git(repo, "rev-parse", "HEAD")

    git(repo, "checkout", "-b", "intake")
    write_catalog(repo, [make_skill("alpha"), make_skill("gamma")], "add gamma")
    head_ref = git(repo, "rev-parse", "HEAD")

    git(repo, "checkout", "main")
    write_catalog(repo, [make_skill("alpha"), make_skill("beta")], "add beta upstream")
    base_ref = git(repo, "rev-parse", "HEAD")
    assert base_ref != fork_point

    monkeypatch.chdir(repo)
    config = CommunityIntakeInput(base_ref=base_ref, head_ref=head_ref, path=CATALOG_PATH)

    assert validate_community_intake_diff(config) == []


def test_removal_relative_to_fork_point_is_still_rejected(tmp_path, monkeypatch):
    repo = init_repo(tmp_path)
    write_catalog(repo, [make_skill("alpha"), make_skill("beta")], "seed")

    git(repo, "checkout", "-b", "intake")
    write_catalog(repo, [make_skill("alpha")], "drop beta")
    head_ref = git(repo, "rev-parse", "HEAD")

    git(repo, "checkout", "main")
    base_ref = git(repo, "rev-parse", "HEAD")

    monkeypatch.chdir(repo)
    config = CommunityIntakeInput(base_ref=base_ref, head_ref=head_ref, path=CATALOG_PATH)

    assert validate_community_intake_diff(config) == [
        "community intake PRs must not remove catalog entries"
    ]


def test_unrelated_histories_fail_closed(tmp_path, monkeypatch):
    repo = init_repo(tmp_path)
    write_catalog(repo, [make_skill("alpha")], "seed")
    head_ref = git(repo, "rev-parse", "HEAD")

    git(repo, "checkout", "--orphan", "detached")
    write_catalog(repo, [make_skill("beta")], "unrelated root")
    base_ref = git(repo, "rev-parse", "HEAD")

    monkeypatch.chdir(repo)
    config = CommunityIntakeInput(base_ref=base_ref, head_ref=head_ref, path=CATALOG_PATH)

    errors = validate_community_intake_diff(config)
    assert len(errors) == 1
    assert "merge base" in errors[0]
