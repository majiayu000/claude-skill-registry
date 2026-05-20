"""
Tests for ``scripts/validate_sources.py``.

Each test seeds a temporary ``sources/<file>.json`` and runs ``main`` so the
exit-code contract (0 clean, 1 errors, 2 strict-warnings) stays observable —
that contract is what CI keys off, so a regression here changes contributor UX.
"""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    if "validate_sources" in sys.modules:
        return importlib.reload(sys.modules["validate_sources"])
    return importlib.import_module("validate_sources")


@pytest.fixture
def vs():
    return _load_module()


@pytest.fixture
def sources(tmp_path: Path) -> Path:
    d = tmp_path / "sources"
    d.mkdir()
    return d


def _write(path: Path, payload: dict | list | str) -> None:
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Happy paths
# ---------------------------------------------------------------------------


def test_clean_curated_file_returns_zero(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "ok",
            "skills": [
                {
                    "name": "demo-skill",
                    "repo": "owner/repo",
                    "description": "Long enough description.",
                    "category": "development",
                    "tags": ["python", "testing"],
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "errors=0" in captured.out
    assert "warnings=0" in captured.out


def test_anthropic_style_inherits_top_level_repo(vs, sources, capsys):
    _write(
        sources / "anthropic.json",
        {
            "name": "Anthropic",
            "repo": "anthropics/skills",
            "description": "Official",
            "skills": [
                {
                    "name": "docx",
                    "path": "skills/docx",
                    "description": "Comprehensive document creation.",
                    "category": "documents",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "errors=0" in captured.out


def test_discovery_files_only_check_repo_format(vs, sources, capsys):
    # Discovery files are expected to have null name / null description per row;
    # they must not generate errors so contributors do not see red CI on files
    # they did not edit.
    _write(
        sources / "github_search.json",
        {
            "name": "GH search",
            "skills": [
                {"repo": "owner/repo", "path": ".claude/skills/x/SKILL.md", "description": None},
                {"repo": "another/one", "description": None, "stars": 0},
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    captured = capsys.readouterr()
    assert rc == 0
    assert "errors=0" in captured.out


def test_unknown_skill_catalog_uses_full_validation(vs, sources, capsys):
    # Unknown sources/*.json catalogs are ingested by build_unified_registry,
    # so they must not get the discovery-only relaxed validation path.
    _write(
        sources / "custom.json",
        {
            "name": "Custom",
            "skills": [
                {"repo": "owner/repo"},
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_NAME" in out
    assert "E_DESCRIPTION" in out
    assert "W_CATEGORY_MISSING" in out


# ---------------------------------------------------------------------------
# Error paths (must exit 1)
# ---------------------------------------------------------------------------


def test_invalid_json_reports_error_and_exits_one(vs, sources, capsys):
    _write(sources / "community.json", "{not json")
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_JSON" in out


def test_top_level_must_be_object(vs, sources, capsys):
    _write(sources / "community.json", [])
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_TOPLEVEL" in out


def test_skills_must_be_array(vs, sources, capsys):
    _write(sources / "community.json", {"name": "x", "description": "y", "skills": "not-array"})
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_SKILLS_TYPE" in out


def test_missing_required_fields_in_curated_entry(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [{"description": "no repo no name"}],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_NAME" in out
    assert "E_REPO" in out


def test_repo_format_must_be_owner_slash_name(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "https://github.com/owner/repo",
                    "description": "Long enough description.",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_REPO_FORMAT" in out


def test_path_traversal_is_rejected(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "path": "../../etc/passwd",
                    "description": "Long enough description here.",
                    "category": "security",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_PATH_TRAVERSAL" in out


def test_windows_style_path_traversal_is_rejected(vs, sources, capsys):
    # ``Path("a\\..\\b").parts`` is a single piece on POSIX runners, so the
    # validator must split on both '/' and '\' before checking for '..'.
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "path": "a\\..\\..\\etc",
                    "description": "Long enough description here.",
                    "category": "security",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_PATH_TRAVERSAL" in out


def test_discovery_windows_style_path_traversal_is_rejected(vs, sources, capsys):
    _write(
        sources / "github_search.json",
        {
            "name": "GH search",
            "skills": [
                {
                    "repo": "owner/repo",
                    "path": "a\\..\\..\\etc",
                    "description": None,
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_PATH_TRAVERSAL" in out


def test_discovery_path_must_be_string(vs, sources, capsys):
    _write(
        sources / "github_search.json",
        {
            "name": "GH search",
            "skills": [
                {
                    "repo": "owner/repo",
                    "path": 123,
                    "description": None,
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_PATH_TYPE" in out


def test_leading_slash_path_is_rejected(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "path": "/abs/path",
                    "description": "Long enough description here.",
                    "category": "development",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "E_PATH_LEADING_SLASH" in out


# ---------------------------------------------------------------------------
# Warnings
# ---------------------------------------------------------------------------


def test_unknown_category_is_warning_not_error(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "description": "Long enough description here.",
                    "category": "moonbase",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "W_CATEGORY_UNKNOWN" in out


def test_alias_category_is_warning_not_error(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "description": "Long enough description here.",
                    "category": "engineering",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "W_CATEGORY_ALIAS" in out
    assert "development" in out


def test_strict_promotes_warning_to_failure(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "description": "Long enough description here.",
                    "category": "moonbase",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources), "--strict"])
    captured = capsys.readouterr()
    assert rc == 2
    assert "W_CATEGORY_UNKNOWN" in captured.out


def test_duplicate_keys_across_files_warn(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "path": "skills/demo",
                    "description": "Long enough description here.",
                    "category": "development",
                }
            ],
        },
    )
    _write(
        sources / "anthropic.json",
        {
            "name": "Anthropic",
            "repo": "owner/repo",  # same repo
            "description": "Official",
            "skills": [
                {
                    "name": "demo",
                    "path": "skills/demo",
                    "description": "Same key as community.json above.",
                    "category": "development",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "W_DUPLICATE" in out


def test_short_description_warns(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "description": "tiny",
                    "category": "development",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "W_DESCRIPTION_SHORT" in out


# ---------------------------------------------------------------------------
# Output formats / file selection
# ---------------------------------------------------------------------------


def test_json_output_is_machine_readable(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "bad-format",
                    "description": "Long enough description here.",
                    "category": "development",
                }
            ],
        },
    )
    rc = vs.main(["--sources-dir", str(sources), "--json"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)
    assert rc == 1
    assert payload["files_scanned"] == 1
    assert any(err["code"] == "E_REPO_FORMAT" for err in payload["errors"])


def test_specific_file_argument(vs, sources, capsys):
    _write(
        sources / "community.json",
        {
            "name": "Community",
            "description": "x",
            "skills": [
                {
                    "name": "demo",
                    "repo": "owner/repo",
                    "description": "Long enough description here.",
                    "category": "development",
                }
            ],
        },
    )
    _write(sources / "broken.json", "{not json")
    rc = vs.main(["--sources-dir", str(sources), "community.json"])
    out = capsys.readouterr().out
    assert rc == 0
    # Only community.json was checked, broken.json is untouched.
    assert "broken.json" not in out


def test_missing_sources_dir_returns_error(vs, tmp_path, capsys):
    rc = vs.main(["--sources-dir", str(tmp_path / "nope")])
    err = capsys.readouterr().err
    assert rc == 2
    assert "sources directory not found" in err


def test_no_files_in_sources_dir_is_warning(vs, sources, capsys):
    rc = vs.main(["--sources-dir", str(sources)])
    err = capsys.readouterr().err
    assert rc == 0
    assert "no source files matched" in err
