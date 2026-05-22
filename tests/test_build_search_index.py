"""Tests for build_search_index.py scoring of root-mounted SKILL.md entries.

Background: many community catalog entries (sources/community.json) describe
skills whose SKILL.md lives at the repo root, encoded as path="". Treating an
empty path as "no install location" under-scored these skills on install
status, quality, and trust, dropping them below the visibility threshold even
though their install URL (repo) was fully resolvable.

These tests pin the behavior that path="" and path="." are equivalent to a
real subdirectory path for scoring purposes whenever a repo is present.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from build_search_index import (  # noqa: E402
    has_install_location,
    infer_install_status,
    is_root_mounted_path,
    score_skill_quality,
    score_skill_trust,
)


def _skill(**overrides):
    base = {
        "name": "example",
        "description": "x" * 100,
        "repo": "acme/example",
        "path": "",
        "tags": ["a", "b", "c"],
        "stars": 0,
    }
    base.update(overrides)
    return base


def test_is_root_mounted_path_recognizes_empty_and_dot():
    assert is_root_mounted_path("") is True
    assert is_root_mounted_path(".") is True
    assert is_root_mounted_path(None) is True
    assert is_root_mounted_path("   ") is True


def test_is_root_mounted_path_rejects_real_subdirs():
    assert is_root_mounted_path("skills/foo") is False
    assert is_root_mounted_path("plugins/getterdone") is False
    assert is_root_mounted_path("./skills/foo") is False


def test_has_install_location_true_for_root_and_subdir():
    assert has_install_location("") is True
    assert has_install_location(".") is True
    assert has_install_location("skills/foo") is True


def test_infer_install_status_known_good_for_root_mounted_repo():
    # Root-mounted (path="") with a real repo is now known_good.
    assert infer_install_status("acme/example", "", "acme/example") == "known_good"
    assert infer_install_status("acme/example", ".", "acme/example") == "known_good"


def test_infer_install_status_known_good_for_subdir():
    # Existing behavior preserved: subdir path is still known_good.
    assert (
        infer_install_status("acme/example", "skills/foo", "acme/example/skills/foo")
        == "known_good"
    )


def test_infer_install_status_unchanged_for_broken_and_local_and_risky():
    # Empty install is still broken.
    assert infer_install_status("acme/example", "", "") == "broken"
    # local/ prefix is still unknown regardless of path.
    assert infer_install_status("acme/example", "", "local/foo") == "unknown"
    assert infer_install_status("acme/example", "skills/foo", "local/foo") == "unknown"
    # No repo, no install → risky.
    assert infer_install_status("", "", "something-else") == "risky"


def test_quality_score_root_mounted_matches_subdir():
    """Empty path with a repo must produce the same quality components as a real subdir."""
    root_skill = _skill(path="")
    subdir_skill = _skill(path="skills/foo")

    root_status = infer_install_status(
        root_skill["repo"], root_skill["path"], root_skill["repo"]
    )
    subdir_status = infer_install_status(
        subdir_skill["repo"],
        subdir_skill["path"],
        f"{subdir_skill['repo']}/{subdir_skill['path']}",
    )

    root_quality = score_skill_quality(root_skill, root_status, "unknown")
    subdir_quality = score_skill_quality(subdir_skill, subdir_status, "unknown")

    assert root_quality["score_inputs"]["path"] == 15
    assert root_quality["score_inputs"]["install"] == 20
    assert root_quality["quality_score"] == subdir_quality["quality_score"]


def test_quality_score_dot_path_matches_empty_path():
    empty_skill = _skill(path="")
    dot_skill = _skill(path=".")

    empty_status = infer_install_status(empty_skill["repo"], "", empty_skill["repo"])
    dot_status = infer_install_status(dot_skill["repo"], ".", dot_skill["repo"])

    assert empty_status == dot_status == "known_good"
    assert (
        score_skill_quality(empty_skill, empty_status, "unknown")["quality_score"]
        == score_skill_quality(dot_skill, dot_status, "unknown")["quality_score"]
    )


def test_quality_score_clears_visibility_threshold_for_root_mounted_skill():
    """Realistic getterdone-shaped entry should score >= 70 (the A-grade gate)."""
    skill = _skill(
        description=(
            "AI agents hire human gig workers for real-world and specialized "
            "digital tasks via USD bounty with photo/text proof."
        ),
        repo="getterdoneinc/skill",
        path="",
        tags=["agents", "human-in-the-loop", "gig-economy", "real-world", "bounty", "mcp"],
        stars=0,
    )
    status = infer_install_status(skill["repo"], skill["path"], skill["repo"])
    quality = score_skill_quality(skill, status, "unknown")

    assert status == "known_good"
    assert quality["quality_score"] >= 70
    assert quality["quality_grade"] in {"A", "S"}


def test_quality_security_component_only_rewards_passed_security():
    skill = _skill()
    install_status = infer_install_status(skill["repo"], skill["path"], skill["repo"])

    passed = score_skill_quality(skill, install_status, "passed")
    unknown = score_skill_quality(skill, install_status, "unknown")
    failed = score_skill_quality(skill, install_status, "failed")

    assert passed["score_inputs"]["security"] == 10
    assert unknown["score_inputs"]["security"] == 0
    assert failed["score_inputs"]["security"] == 0


def test_trust_score_only_rewards_passed_security():
    skill = _skill(stars=5)
    install_status = infer_install_status(skill["repo"], skill["path"], skill["repo"])

    passed = score_skill_trust(
        skill["repo"], skill["path"], install_status, "passed", skill["stars"]
    )
    unknown = score_skill_trust(
        skill["repo"], skill["path"], install_status, "unknown", skill["stars"]
    )
    failed = score_skill_trust(
        skill["repo"], skill["path"], install_status, "failed", skill["stars"]
    )

    assert passed == unknown + 15
    assert unknown == failed
