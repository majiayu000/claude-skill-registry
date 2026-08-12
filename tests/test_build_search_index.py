"""Tests for build_search_index.py scoring of root-mounted SKILL.md entries.

Background: many community catalog entries (sources/community.json) describe
skills whose SKILL.md lives at the repo root, encoded as path="". Treating an
empty path as "no install location" under-scored these skills on install
status, quality, and trust, dropping them below the visibility threshold even
though their install URL (repo) was fully resolvable.

These tests pin the behavior that path="" and path="." are equivalent to a
real subdirectory path for scoring purposes whenever a repo is present.
"""

import hashlib
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import archive_preflight  # noqa: E402
from build_search_index import (  # noqa: E402
    build_search_index,
    has_install_location,
    infer_install_status,
    score_skill_quality,
    score_skill_trust,
)
from rebuild_registry import scan_skills as scan_registry_skills  # noqa: E402
from search_sources import (  # noqa: E402
    asset_ranking_penalty,
    is_root_mounted_path,
    load_from_registry,
    scan_skills_v2,
    verified_asset_fields,
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


def _verified_asset_evidence(liveness=None):
    evidence = {
        "asset_state": "verified",
        "bundled_file_count": 1,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }
    if liveness is not None:
        evidence.update(
            {
                "asset_liveness": liveness,
                "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
            }
        )
        if liveness in {"live", "partial", "moved"}:
            evidence["assets_liveness_sha"] = "b" * 40
    return evidence


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


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

    root_status = infer_install_status(root_skill["repo"], root_skill["path"], root_skill["repo"])
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


def test_build_search_index_consumes_security_decision_evidence(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    output_dir.joinpath("security-report.json").write_text(
        json.dumps(
            {
                "scanner": {
                    "name": "claude-skill-registry-security-scanner",
                    "version": "1.1.0",
                    "ruleset_sha256": "abc123",
                },
                "generated_at": "2026-05-24T00:00:00Z",
                "total": 1,
                "passed": 1,
                "failed": 0,
                "skills": [
                    {
                        "path": "development/demo/SKILL.md",
                        "safe": True,
                        "security_decision": {
                            "id": "decision123",
                            "status": "passed",
                            "reason": "no_errors",
                            "scanner": {
                                "name": "claude-skill-registry-security-scanner",
                                "version": "1.1.0",
                                "ruleset_sha256": "abc123",
                            },
                            "provenance": {
                                "content_sha256": "def456",
                                "scanned_at": "2026-05-24T00:00:00Z",
                            },
                        },
                        "issues": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    build_search_index(
        [
            _skill(
                path="skills/demo",
                install="acme/example/skills/demo",
                archive_path="development/demo/SKILL.md",
            )
        ],
        output_dir,
        require_security_evidence=True,
    )

    manifest = json.loads((output_dir / "security-index-manifest.json").read_text())
    shard = json.loads((output_dir / manifest["shards"][0]["path"]).read_text())
    record = shard["records"][0]
    assert record["security_status"] == "passed"
    assert record["security_decision"]["id"] == "decision123"


def test_build_search_index_consumes_external_security_report_without_publishing_raw(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    security_report_path = tmp_path / "security-report.json"
    security_report_path.write_text(
        json.dumps(
            {
                "total": 1,
                "passed": 1,
                "failed": 0,
                "skills": [
                    {
                        "path": "development/demo/SKILL.md",
                        "security_decision": {
                            "status": "passed",
                            "scanner": {
                                "name": "claude-skill-registry-security-scanner",
                                "version": "1.1.0",
                                "ruleset_sha256": "abc123",
                            },
                            "provenance": {
                                "content_sha256": "def456",
                                "scanned_at": "2026-05-24T00:00:00Z",
                            },
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    build_search_index(
        [
            _skill(
                path="skills/demo",
                install="acme/example/skills/demo",
                archive_path="development/demo/SKILL.md",
            )
        ],
        output_dir,
        require_security_evidence=True,
        security_report_path=security_report_path,
    )

    stats = json.loads((output_dir / "stats.json").read_text())
    assert stats["security_scan"] == {"total": 1, "passed": 1, "failed": 0}
    assert not output_dir.joinpath("security-report.json").exists()


def test_build_search_index_fails_when_required_security_report_is_missing(tmp_path):
    with pytest.raises(FileNotFoundError, match="Required security evidence is missing"):
        build_search_index(
            [_skill(path="skills/demo", install="acme/example/skills/demo")],
            tmp_path / "docs",
            require_security_evidence=True,
        )


def test_build_search_index_skips_missing_security_decision_when_optional(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    output_dir.joinpath("security-report.json").write_text(
        json.dumps(
            {
                "total": 1,
                "passed": 1,
                "failed": 0,
                "skills": [
                    {
                        "path": "development/demo/SKILL.md",
                        "safe": True,
                        "issues": [],
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    build_search_index(
        [
            _skill(
                path="skills/demo",
                install="acme/example/skills/demo",
                archive_path="development/demo/SKILL.md",
            )
        ],
        output_dir,
        require_security_evidence=False,
    )

    manifest = json.loads((output_dir / "security-index-manifest.json").read_text())
    shard = json.loads((output_dir / manifest["shards"][0]["path"]).read_text())
    record = shard["records"][0]
    assert record["security_status"] == "unknown"
    assert "security_decision" not in record


def test_build_search_index_requires_security_decision_when_required(tmp_path):
    output_dir = tmp_path / "docs"
    output_dir.mkdir()
    output_dir.joinpath("security-report.json").write_text(
        json.dumps(
            {
                "total": 1,
                "passed": 1,
                "failed": 0,
                "skills": [{"path": "development/demo/SKILL.md", "safe": True}],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="Missing security_decision"):
        build_search_index(
            [
                _skill(
                    path="skills/demo",
                    install="acme/example/skills/demo",
                    archive_path="development/demo/SKILL.md",
                )
            ],
            output_dir,
            require_security_evidence=True,
        )


def test_build_emits_complete_category_taxonomy_sidecar(tmp_path):
    output_dir = tmp_path / "docs"
    build_search_index([], output_dir)

    sidecar = json.loads((output_dir / "category-taxonomy.json").read_text())
    assert sidecar["schema_version"] == 1
    assert sidecar["taxonomy_schema_version"] == 2
    assert sidecar["category_count"] == 40
    assert sidecar["default_category"] == "other"
    assert sidecar["default_code"] == "oth"
    assert len({item["slug"] for item in sidecar["categories"]}) == 40
    assert len({item["code"] for item in sidecar["categories"]}) == 40
    assert len([item for item in sidecar["categories"] if not item["parent"]]) == 12


def test_registry_and_search_publish_only_locally_validated_asset_facets(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "asset-demo"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Asset demo", encoding="utf-8")
    support_file = skill_dir / "scripts" / "run.py"
    support_file.write_text("print('ok')", encoding="utf-8")
    metadata = {
        "name": "asset-demo",
        "repo": "acme/assets",
        "path": "skills/asset-demo/SKILL.md",
        "github_branch": "main",
        "category": "development",
        "archive_mode": "directory",
        "bundled_files": ["scripts/run.py"],
        "bundled_file_blobs": {"scripts/run.py": git_blob_sha(b"print('ok')")},
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
        "asset_liveness": "live",
        "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
        "assets_liveness_sha": "b" * 40,
    }
    (skill_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)
    expected = {
        "asset_state": "verified",
        "asset_liveness": "live",
        "bundled_file_count": 1,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
        "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
        "assets_liveness_sha": "b" * 40,
    }
    assert {key: search_record[key] for key in expected} == expected
    assert {key: registry_record[key] for key in expected} == expected

    support_file.unlink()
    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)
    for record in (search_record, registry_record):
        assert "asset_state" not in record
        assert "asset_liveness" not in record

    support_file.write_text("print('tampered')", encoding="utf-8")
    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)
    for record in (search_record, registry_record):
        assert "asset_state" not in record


def test_registry_and_search_bind_verified_assets_to_canonical_source_identity(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "identity-demo"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Identity demo", encoding="utf-8")
    support_file = skill_dir / "scripts" / "run.py"
    support_file.write_text("asset", encoding="utf-8")
    metadata = {
        "name": "identity-demo",
        "repo": " acme/assets ",
        "path": " skills\\identity-demo\\SKILL.md ",
        "github_branch": " release/v2 ",
        "category": "development",
        "archive_mode": "directory",
        "bundled_files": ["scripts/run.py"],
        "bundled_file_blobs": {"scripts/run.py": git_blob_sha(b"asset")},
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }
    (skill_dir / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)

    for record in (search_record, registry_record):
        assert record["repo"] == "acme/assets"
        assert record["path"] == "skills/identity-demo/SKILL.md"
        assert record["branch"] == "release/v2"
        assert record["asset_state"] == "verified"
    assert search_record["install"] == "acme/assets/skills/identity-demo/SKILL.md"


def test_registry_and_search_keep_legacy_github_path_install_identity(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "identity-demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Identity demo", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "identity-demo",
                "repo": "acme/identity",
                "github_path": "legacy/location/SKILL.md",
                "path": "new/location/SKILL.md",
                "github_branch": "main",
                "category": "development",
            }
        ),
        encoding="utf-8",
    )

    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)

    assert search_record["path"] == "legacy/location/SKILL.md"
    assert search_record["install"] == "acme/identity/legacy/location/SKILL.md"
    assert registry_record["path"] == "legacy/location/SKILL.md"


def test_live_asset_facets_win_equal_search_ranks_by_downranking_only(tmp_path):
    plain = _skill(
        name="plain",
        repo="acme/plain",
        path="skills/demo/SKILL.md",
        install="acme/plain/skills/demo/SKILL.md",
        branch="main",
        stars=10,
    )
    verified_live = _skill(
        name="verified-live",
        repo="acme/live",
        path="skills/demo/SKILL.md",
        install="acme/live/skills/demo/SKILL.md",
        branch="main",
        stars=10,
        asset_state="verified",
        asset_liveness="live",
        bundled_file_count=1,
        github_commit_sha="a" * 40,
        assets_verified_at="2026-08-01T00:00:00Z",
        assets_liveness_checked_at="2026-08-11T00:00:00Z",
        assets_liveness_sha="b" * 40,
    )
    output_dir = tmp_path / "docs"
    stats = build_search_index([plain, verified_live], output_dir)

    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert [skill["name"] for skill in lite["skills"]] == ["verified-live", "plain"]
    assert lite["skills"][0]["asset_state"] == "verified"
    assert lite["skills"][0]["asset_liveness"] == "live"
    assert "asset_state" not in lite["skills"][1]

    search_manifest = json.loads((output_dir / "search-index-manifest.json").read_text())
    search_shard = json.loads((output_dir / search_manifest["shards"][0]["path"]).read_text())
    assert search_shard["s"][0]["a"] == "verified"
    assert search_shard["s"][0]["l"] == "live"
    assert "a" not in search_shard["s"][1]

    ranking_manifest = json.loads((output_dir / "ranking-index-manifest.json").read_text())
    ranking_shard = json.loads((output_dir / ranking_manifest["shards"][0]["path"]).read_text())
    by_install = {record["install"]: record for record in ranking_shard["records"]}
    live_rank = by_install[verified_live["install"]]
    plain_rank = by_install[plain["install"]]
    assert live_rank["asset_ranking_penalty"] == 0
    assert plain_rank["asset_ranking_penalty"] == 0.1
    assert live_rank["recommended_score"] == plain_rank["recommended_score"]
    assert stats["asset_state_counts"] == {"verified": 1}
    assert stats["asset_liveness_counts"] == {"live": 1}
    featured = json.loads((output_dir / "featured.json").read_text())
    assert [skill["name"] for skill in featured["skills"]] == ["verified-live", "plain"]


def test_asset_evidence_never_overrides_existing_non_equal_ranks(tmp_path):
    live = _skill(
        name="live-one-star",
        repo="acme/live",
        install="acme/live/SKILL.md",
        branch="main",
        stars=1,
        **_verified_asset_evidence("live"),
    )
    gone = _skill(
        name="gone-two-stars",
        repo="acme/gone",
        install="acme/gone/SKILL.md",
        branch="main",
        stars=2,
        **_verified_asset_evidence("gone"),
    )
    output_dir = tmp_path / "docs"

    build_search_index([live, gone], output_dir)

    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert [skill["name"] for skill in lite["skills"]] == [
        "gone-two-stars",
        "live-one-star",
    ]
    ranking_manifest = json.loads((output_dir / "ranking-index-manifest.json").read_text())
    ranking_shard = json.loads((output_dir / ranking_manifest["shards"][0]["path"]).read_text())
    assert [record["install"] for record in ranking_shard["records"]] == [
        gone["install"],
        live["install"],
    ]
    assert (
        ranking_shard["records"][0]["recommended_score"]
        > (ranking_shard["records"][1]["recommended_score"])
    )


def test_asset_evidence_does_not_override_existing_dedupe_winner(tmp_path):
    plain = _skill(
        name="plain-short",
        description="short",
        repo="acme/shared",
        install="acme/shared/SKILL.md",
        branch="main",
        stars=10,
    )
    gone = _skill(
        name="gone-long",
        description="a much longer description that won before asset facets existed",
        repo="acme/shared",
        install="acme/shared/SKILL.md",
        branch="main",
        stars=10,
        **_verified_asset_evidence("gone"),
    )
    output_dir = tmp_path / "docs"

    build_search_index([plain, gone], output_dir)

    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert [skill["name"] for skill in lite["skills"]] == ["gone-long"]


def test_asset_fields_do_not_change_legacy_final_dedupe_tie(tmp_path):
    common = {
        "name": "same",
        "description": "same description",
        "repo": "acme/shared",
        "path": "SKILL.md",
        "install": "acme/shared/SKILL.md",
        "branch": "main",
        "stars": 10,
    }
    plain = _skill(**common)
    same_penalty_verified = _skill(**common, **_verified_asset_evidence())
    output_dir = tmp_path / "docs"

    build_search_index([plain, same_penalty_verified], output_dir)

    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert len(lite["skills"]) == 1
    assert "asset_state" not in lite["skills"][0]

    reverse_output_dir = tmp_path / "reverse-docs"
    build_search_index([same_penalty_verified, plain], reverse_output_dir)
    reverse_lite = json.loads((reverse_output_dir / "search-index-lite.json").read_text())
    assert reverse_lite["skills"] == lite["skills"]


def test_asset_ranking_penalties_are_downrank_only():
    assert asset_ranking_penalty({"asset_state": "verified", "asset_liveness": "live"}) == 0
    assert asset_ranking_penalty({"asset_state": "verified"}) == 0.1
    assert asset_ranking_penalty({"asset_state": "verified", "asset_liveness": "partial"}) == 0.25
    assert asset_ranking_penalty({"asset_state": "verified", "asset_liveness": "moved"}) == 0.5
    assert asset_ranking_penalty({"asset_state": "verified", "asset_liveness": "gone"}) == 0.75
    assert asset_ranking_penalty({}) == 0.1


def test_verified_asset_fields_omit_malformed_claims_and_incomplete_liveness(tmp_path):
    skill_dir = tmp_path / "dev" / "skill"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("body", encoding="utf-8")
    (skill_dir / "scripts/run.py").write_text("asset", encoding="utf-8")
    base = {
        "repo": "acme/tools",
        "path": "skills/demo/SKILL.md",
        "github_branch": "main",
        "archive_mode": "directory",
        "bundled_files": ["scripts/run.py"],
        "bundled_file_blobs": {"scripts/run.py": git_blob_sha(b"asset")},
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }
    invalid_changes = [
        {"archive_mode": "skill-md"},
        {"bundled_files": []},
        {"bundled_files": [" scripts/run.py"]},
        {"bundled_files": ["scripts\\run.py"]},
        {"bundled_files": ["../run.py"]},
        {"bundled_files": ["/run.py"]},
        {"bundled_files": ["C:scripts/run.py"]},
        {"bundled_files": ["SKILL.md"]},
        {"bundled_files": ["skill.md"]},
        {"bundled_files": ["Metadata.json"]},
        {"bundled_files": ["scripts/run.py", "scripts/run.py"]},
        {
            "bundled_files": ["scripts/run.py", "Scripts/run.py"],
            "bundled_file_blobs": {
                "scripts/run.py": git_blob_sha(b"asset"),
                "Scripts/run.py": git_blob_sha(b"asset"),
            },
        },
        {"github_commit_sha": "bad"},
        {"assets_verified_at": ""},
        {"assets_verified_at": "not-a-date"},
        {"bundled_file_blobs": {"scripts/run.py": "a" * 40}},
    ]
    for change in invalid_changes:
        assert verified_asset_fields({**base, **change}, skill_dir, tmp_path) == {}

    for missing_field in ("repo", "path", "github_branch"):
        incomplete = dict(base)
        incomplete.pop(missing_field)
        assert verified_asset_fields(incomplete, skill_dir, tmp_path) == {}
    for conflict in (
        {"github_path": "skills/other/SKILL.md"},
        {"branch": "develop"},
    ):
        assert verified_asset_fields({**base, **conflict}, skill_dir, tmp_path) == {}

    verified = verified_asset_fields({**base, "asset_liveness": "live"}, skill_dir, tmp_path)
    assert verified["asset_state"] == "verified"
    assert "asset_liveness" not in verified
    verified = verified_asset_fields(
        {
            **base,
            "asset_liveness": "gone",
            "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
        },
        skill_dir,
        tmp_path,
    )
    assert verified["asset_liveness"] == "gone"
    assert "assets_liveness_sha" not in verified
    invalid_gone = verified_asset_fields(
        {
            **base,
            "asset_liveness": "gone",
            "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
            "assets_liveness_sha": "b" * 40,
        },
        skill_dir,
        tmp_path,
    )
    assert "asset_liveness" not in invalid_gone
    invalid_timestamp = verified_asset_fields(
        {
            **base,
            "asset_liveness": "live",
            "assets_liveness_checked_at": "not-a-date",
            "assets_liveness_sha": "b" * 40,
        },
        skill_dir,
        tmp_path,
    )
    assert "asset_liveness" not in invalid_timestamp
    verified = verified_asset_fields(
        {
            **base,
            "asset_liveness": "live",
            "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
            "assets_liveness_sha": "bad",
        },
        skill_dir,
        tmp_path,
    )
    assert "asset_liveness" not in verified


def test_verified_asset_fields_reject_symlinks(tmp_path):
    skill_dir = tmp_path / "dev" / "skill"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("body", encoding="utf-8")
    external = tmp_path / "external.py"
    external.write_text("asset", encoding="utf-8")
    (skill_dir / "run.py").symlink_to(external)
    metadata = {
        "repo": "acme/tools",
        "path": "skills/demo/SKILL.md",
        "github_branch": "main",
        "archive_mode": "directory",
        "bundled_files": ["run.py"],
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }
    assert verified_asset_fields(metadata, skill_dir, tmp_path) == {}

    external_skill = tmp_path / "external-skill"
    external_skill.mkdir()
    (external_skill / "SKILL.md").write_text("body", encoding="utf-8")
    (external_skill / "run.py").write_text("asset", encoding="utf-8")
    linked_skill = tmp_path / "linked-skill"
    linked_skill.symlink_to(external_skill, target_is_directory=True)
    assert verified_asset_fields(metadata, linked_skill, tmp_path) == {}
    linked_root = tmp_path / "linked-root"
    linked_root.symlink_to(tmp_path, target_is_directory=True)
    assert verified_asset_fields(metadata, linked_root / "skill", linked_root) == {}


def test_verified_asset_fields_reject_reserved_bundle_root(tmp_path):
    skill_dir = tmp_path / "dev" / "skill"
    reserved_dir = skill_dir / "Metadata.json"
    reserved_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("body", encoding="utf-8")
    asset = reserved_dir / "run.py"
    asset.write_text("asset", encoding="utf-8")
    metadata = {
        "repo": "acme/tools",
        "path": "skills/demo/SKILL.md",
        "github_branch": "main",
        "archive_mode": "directory",
        "bundled_files": ["Metadata.json/run.py"],
        "bundled_file_blobs": {"Metadata.json/run.py": git_blob_sha(b"asset")},
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }

    assert verified_asset_fields(metadata, skill_dir, tmp_path) == {}


@pytest.mark.parametrize("scanner", [scan_skills_v2, scan_registry_skills])
@pytest.mark.parametrize(
    ("relative_path", "error"),
    [
        (Path("CON/demo/SKILL.md"), "non-portable canonical archive path"),
        (Path("dev/demo/skill.md"), "canonical SKILL.md has invalid casing"),
    ],
)
def test_registry_scanners_fail_closed_on_invalid_canonical_archive(
    tmp_path, scanner, relative_path, error
):
    skills_dir = tmp_path / "skills"
    skill_md = skills_dir / relative_path
    skill_md.parent.mkdir(parents=True)
    skill_md.write_text("# Invalid", encoding="utf-8")

    with pytest.raises(ValueError, match=error):
        scanner(skills_dir)


@pytest.mark.parametrize("scanner", [scan_skills_v2, scan_registry_skills])
def test_registry_scanners_reject_symlinked_canonical_skill(tmp_path, scanner):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "dev" / "demo"
    skill_dir.mkdir(parents=True)
    external = tmp_path / "outside.md"
    external.write_text("# Outside", encoding="utf-8")
    (skill_dir / "SKILL.md").symlink_to(external)

    with pytest.raises(ValueError, match="regular non-symlink file"):
        scanner(skills_dir)


@pytest.mark.parametrize("scanner", [scan_skills_v2, scan_registry_skills])
@pytest.mark.parametrize("metadata_kind", ["symlink", "directory"])
def test_registry_scanners_reject_nonregular_canonical_metadata(tmp_path, scanner, metadata_kind):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "dev" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Demo", encoding="utf-8")
    metadata_path = skill_dir / "metadata.json"
    if metadata_kind == "symlink":
        external = tmp_path / "outside.json"
        external.write_text(json.dumps({"repo": "attacker/repo"}), encoding="utf-8")
        metadata_path.symlink_to(external)
    else:
        metadata_path.mkdir()

    with pytest.raises(ValueError, match="canonical metadata.json must be a regular file"):
        scanner(skills_dir)


@pytest.mark.parametrize("scanner", [scan_skills_v2, scan_registry_skills])
@pytest.mark.parametrize(
    ("first_relative", "second_relative", "error"),
    [
        (Path("Dev/demo"), Path("dev/other"), "case-conflicting category paths"),
        (Path("dev/Demo"), Path("dev/demo"), "case-conflicting skill paths"),
    ],
)
def test_registry_scanners_reject_case_conflicting_canonical_roots(
    tmp_path, scanner, first_relative, second_relative, error
):
    skills_dir = tmp_path / "skills"
    first = skills_dir / first_relative
    second = skills_dir / second_relative
    first.mkdir(parents=True)
    second.mkdir(parents=True, exist_ok=True)
    first_category = skills_dir / first_relative.parts[0]
    second_category = skills_dir / second_relative.parts[0]
    if first.samefile(second) or (
        first_category != second_category and first_category.samefile(second_category)
    ):
        pytest.skip("case-insensitive filesystem cannot represent conflicting roots")
    (first / "SKILL.md").write_text("# First", encoding="utf-8")
    (second / "SKILL.md").write_text("# Second", encoding="utf-8")

    with pytest.raises(ValueError, match=error):
        scanner(skills_dir)


@pytest.mark.parametrize("scanner", [scan_skills_v2, scan_registry_skills])
def test_registry_scanners_reject_coexisting_skill_case_variants(tmp_path, monkeypatch, scanner):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "dev" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Demo", encoding="utf-8")
    monkeypatch.setattr(
        archive_preflight.os,
        "walk",
        lambda _root, *, onerror: iter([(str(skill_dir), [], ["SKILL.md", "skill.md"])]),
    )

    with pytest.raises(ValueError, match="case-conflicting SKILL.md files"):
        scanner(skills_dir)


def test_registry_and_search_omit_verified_state_without_source_identity(tmp_path):
    skills_dir = tmp_path / "skills"
    skill_dir = skills_dir / "development" / "asset-demo"
    (skill_dir / "scripts").mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Asset demo", encoding="utf-8")
    (skill_dir / "scripts" / "run.py").write_text("print('ok')", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps(
            {
                "name": "asset-demo",
                "category": "development",
                "archive_mode": "directory",
                "bundled_files": ["scripts/run.py"],
                "github_commit_sha": "a" * 40,
                "assets_verified_at": "2026-08-01T00:00:00Z",
            }
        ),
        encoding="utf-8",
    )

    [search_record] = scan_skills_v2(skills_dir)
    [registry_record] = scan_registry_skills(skills_dir)

    assert "asset_state" not in search_record
    assert "asset_state" not in registry_record


def test_registry_fallback_preserves_validated_asset_fields(tmp_path):
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(
        json.dumps(
            {
                "skills": [
                    {
                        "name": "verified-live",
                        "repo": "acme/live",
                        "path": "skills/demo/SKILL.md",
                        "branch": "main",
                        "category": "development",
                        "asset_state": "verified",
                        "asset_liveness": "live",
                        "bundled_file_count": 1,
                        "github_commit_sha": "a" * 40,
                        "assets_verified_at": "2026-08-01T00:00:00Z",
                        "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
                        "assets_liveness_sha": "b" * 40,
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    [loaded] = load_from_registry(registry_path)
    assert loaded["asset_state"] == "verified"
    assert loaded["asset_liveness"] == "live"

    output_dir = tmp_path / "docs"
    build_search_index([loaded], output_dir)
    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert lite["skills"][0]["asset_state"] == "verified"
    manifest = json.loads((output_dir / "search-index-manifest.json").read_text())
    shard = json.loads((output_dir / manifest["shards"][0]["path"]).read_text())
    assert shard["s"][0]["a"] == "verified"


@pytest.mark.parametrize("missing_field", ["repo", "path", "branch"])
def test_registry_fallback_requires_complete_source_identity_for_assets(tmp_path, missing_field):
    record = {
        "name": "invalid-source",
        "repo": "acme/source",
        "path": "skills/demo/SKILL.md",
        "branch": "main",
        "asset_state": "verified",
        "asset_liveness": "live",
        "bundled_file_count": 1,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
        "assets_liveness_checked_at": "2026-08-11T00:00:00Z",
        "assets_liveness_sha": "b" * 40,
    }
    record.pop(missing_field)
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps({"skills": [record]}), encoding="utf-8")

    [loaded] = load_from_registry(registry_path)

    assert "asset_state" not in loaded
    assert "asset_liveness" not in loaded


@pytest.mark.parametrize(
    "conflict",
    [
        {"github_path": "skills/other/SKILL.md"},
        {"github_branch": "release/v2"},
    ],
)
def test_registry_fallback_rejects_conflicting_source_aliases(tmp_path, conflict):
    record = {
        "name": "conflicting-source",
        "repo": "acme/source",
        "path": "skills/demo/SKILL.md",
        "branch": "main",
        "asset_state": "verified",
        "bundled_file_count": 1,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
        **conflict,
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps({"skills": [record]}), encoding="utf-8")

    [loaded] = load_from_registry(registry_path)

    assert "asset_state" not in loaded


def test_registry_fallback_canonicalizes_alias_only_asset_source(tmp_path):
    record = {
        "name": "alias-source",
        "repo": " acme/source ",
        "github_path": " skills/demo ",
        "github_branch": " release/v2 ",
        "asset_state": "verified",
        "bundled_file_count": 1,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps({"skills": [record]}), encoding="utf-8")

    [loaded] = load_from_registry(registry_path)

    assert loaded["asset_state"] == "verified"
    assert loaded["repo"] == "acme/source"
    assert loaded["path"] == "skills/demo/SKILL.md"
    assert loaded["branch"] == "release/v2"
    assert loaded["install"] == "acme/source/skills/demo/SKILL.md"


def test_unvalidated_asset_claims_are_removed_from_registry_fallback_and_build(tmp_path):
    invalid_claim = {
        "name": "unvalidated",
        "repo": "acme/unvalidated",
        "path": "SKILL.md",
        "branch": "main",
        "category": "development",
        "asset_state": "verified",
        "asset_liveness": "live",
    }
    registry_path = tmp_path / "registry.json"
    registry_path.write_text(json.dumps({"skills": [invalid_claim]}), encoding="utf-8")

    [loaded] = load_from_registry(registry_path)
    assert "asset_state" not in loaded
    assert "asset_liveness" not in loaded

    output_dir = tmp_path / "docs"
    build_search_index([invalid_claim], output_dir)
    lite = json.loads((output_dir / "search-index-lite.json").read_text())
    assert "asset_state" not in lite["skills"][0]
    assert "asset_liveness" not in lite["skills"][0]
    manifest = json.loads((output_dir / "search-index-manifest.json").read_text())
    shard = json.loads((output_dir / manifest["shards"][0]["path"]).read_text())
    assert "a" not in shard["s"][0]
    assert "l" not in shard["s"][0]
