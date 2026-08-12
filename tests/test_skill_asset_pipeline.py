"""End-to-end coverage for the skill-asset audit and backfill CLIs.

Network access is stubbed at the `gh` subprocess boundary so the census,
verification, and fetch stages run against real files in tmp_path.
"""

import asyncio
import hashlib
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit_skill_assets
import backfill_skill_assets
import skill_asset_audit
import sync_download_support


class FakeCompleted:
    def __init__(self, returncode=0, stdout="", stderr=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr


def make_skill(root, category, name, body, meta=None):
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    if meta is not None:
        (skill_dir / "metadata.json").write_text(json.dumps(meta), encoding="utf-8")
    return skill_dir


def git_blob_sha(content: bytes) -> str:
    header = f"blob {len(content)}\0".encode("ascii")
    return hashlib.sha1(header + content, usedforsecurity=False).hexdigest()


@pytest.fixture
def archive(tmp_path):
    root = tmp_path / "data"
    make_skill(
        root,
        "dev",
        "with-script",
        "Run scripts/setup.py first.",
        {
            "stars": 500,
            "repo": "acme/tools",
            "path": "skills/with-script/SKILL.md",
            "github_branch": "main",
            "name": "with-script",
            "license": "MIT",
            "distribution": "compatible",
        },
    )
    make_skill(
        root,
        "dev",
        "with-docs",
        "See references/guide.md for details.",
        {
            "stars": 300,
            "repo": "acme/docs",
            "path": "skills/with-docs/SKILL.md",
            "github_branch": "main",
            "name": "with-docs",
            "license": "MIT",
            "distribution": "compatible",
        },
    )
    make_skill(
        root,
        "dev",
        "plain",
        "Just prose, no local files.",
        {
            "stars": 900,
            "repo": "acme/plain",
            "path": "skills/plain/SKILL.md",
            "github_branch": "main",
            "name": "plain",
            "license": "MIT",
            "distribution": "compatible",
        },
    )
    make_skill(
        root,
        "dev",
        "low-stars",
        "Run scripts/other.py first.",
        {
            "stars": 3,
            "repo": "acme/small",
            "path": "skills/low-stars/SKILL.md",
            "github_branch": "main",
            "name": "low-stars",
            "license": "MIT",
            "distribution": "compatible",
        },
    )
    return root


class TestFetchRepoTree:
    def test_returns_blob_paths(self, monkeypatch):
        monkeypatch.setattr(
            skill_asset_audit.subprocess,
            "run",
            lambda *a, **k: FakeCompleted(stdout='["a/SKILL.md", "a/run.py"]'),
        )
        assert skill_asset_audit.fetch_repo_tree("acme/tools") == ["a/SKILL.md", "a/run.py"]

    def test_raises_on_gh_failure(self, monkeypatch):
        monkeypatch.setattr(
            skill_asset_audit.subprocess,
            "run",
            lambda *a, **k: FakeCompleted(returncode=1, stderr="Not Found"),
        )
        with pytest.raises(RuntimeError, match="Not Found"):
            skill_asset_audit.fetch_repo_tree("acme/gone")


class TestCensus:
    def test_counts_every_bucket(self, archive):
        result = audit_skill_assets.run_census(str(archive))
        assert result["total_skills"] == 4
        assert result["buckets"] == {"EXEC": 2, "REF": 1, "BARE": 1}
        assert result["bucket_pct"]["EXEC"] == 50.0
        assert result["median_skill_md_bytes"]["BARE"] > 0

    def test_empty_root_is_an_error(self, tmp_path):
        with pytest.raises(SystemExit):
            audit_skill_assets.run_census(str(tmp_path))


class TestTargets:
    def test_emits_only_exec_candidates_above_threshold(self, archive, capsys):
        audit_skill_assets.run_targets(str(archive), 100)
        rows = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
        assert [r["name"] for r in rows] == ["with-script"]
        assert rows[0] == {
            "repo": "acme/tools",
            "dir": "skills/with-script",
            "stars": 500,
            "name": "with-script",
        }

    def test_lower_threshold_includes_small_repos(self, archive, capsys):
        audit_skill_assets.run_targets(str(archive), 1)
        names = {json.loads(line)["name"] for line in capsys.readouterr().out.splitlines()}
        assert names == {"with-script", "low-stars"}

    def test_dedupes_by_repo_and_dir(self, tmp_path, capsys):
        root = tmp_path / "data"
        meta = {"stars": 500, "repo": "acme/tools", "path": "skills/dup/SKILL.md", "name": "dup"}
        make_skill(root, "a", "dup", "Run scripts/setup.py.", meta)
        make_skill(root, "b", "dup", "Run scripts/setup.py.", meta)
        audit_skill_assets.run_targets(str(root), 100)
        assert len(capsys.readouterr().out.splitlines()) == 1

    def test_skips_entries_without_metadata_or_repo(self, tmp_path, capsys):
        root = tmp_path / "data"
        make_skill(root, "a", "nometa", "Run scripts/setup.py.")
        make_skill(root, "a", "norepo", "Run scripts/setup.py.", {"stars": 500, "name": "x"})
        audit_skill_assets.run_targets(str(root), 100)
        assert capsys.readouterr().out == ""


class TestCurrentStateInventory:
    def test_reports_real_archive_state_and_metadata_drift(self, tmp_path):
        root = tmp_path / "data"
        archived = make_skill(
            root,
            "dev",
            "archived",
            "Run scripts/setup.py first.",
            {
                "stars": 500,
                "repo": "acme/tools",
                "path": "skills/archived/SKILL.md",
                "github_branch": "main",
                "name": "archived",
                "category": "dev",
                "archive_mode": "directory",
                "bundled_files": ["scripts/setup.py"],
                "bundled_file_blobs": {"scripts/setup.py": git_blob_sha(b"print('ok')")},
            },
        )
        (archived / "scripts").mkdir()
        (archived / "scripts" / "setup.py").write_text("print('ok')")
        make_skill(
            root,
            "dev",
            "missing",
            "See references/guide.md.",
            {
                "stars": 300,
                "repo": "acme/docs",
                "path": "skills/missing/SKILL.md",
                "github_branch": "release/v1",
                "name": "missing",
                "category": "dev",
                "archive_mode": "directory",
                "bundled_files": ["references/guide.md"],
                "license": "MIT",
                "distribution": "compatible",
            },
        )
        make_skill(
            root,
            "dev",
            "plain",
            "No local files are required.",
            {
                "stars": 1,
                "repo": "acme/plain",
                "path": "SKILL.md",
                "github_branch": "main",
                "name": "plain",
                "category": "dev",
                "archive_mode": "skill-md",
                "bundled_files": [],
            },
        )

        report = audit_skill_assets.run_current_state(str(root))

        assert report == {
            "schema_version": 1,
            "total_skills": 3,
            "claim_counts": {"EXEC": 1, "REF": 1, "BARE": 1},
            "local_verdict_counts": {"EXEC": 1, "BARE": 2},
            "asset_state_counts": {
                "archived": 1,
                "missing_claimed_assets": 1,
                "no_assets_claimed": 1,
            },
            "archive_mode_counts": {"directory": 1, "skill-md": 2},
            "actual_bundled_file_count": 1,
            "metadata_mismatch_count": 1,
            "source_identity_error_count": 0,
            "source_identity_errors": [],
            "metadata_error_count": 0,
            "metadata_errors": [],
            "ambiguous_stable_key_count": 0,
            "backfill_candidate_count": 1,
        }

    def test_backfill_targets_are_exact_deterministic_and_fail_closed(self, tmp_path):
        root = tmp_path / "data"
        base_meta = {
            "stars": 200,
            "repo": "acme/tools",
            "path": "skills/duplicate/SKILL.md",
            "github_branch": "main",
            "name": "duplicate",
            "category": "dev",
            "license": "MIT",
            "distribution": "compatible",
        }
        make_skill(root, "a", "duplicate", "Run scripts/setup.py.", base_meta)
        make_skill(root, "b", "duplicate", "Run scripts/setup.py.", base_meta)
        make_skill(
            root,
            "dev",
            "ready",
            "Run scripts/build.py.",
            {
                "stars": 500,
                "repo": "acme/ready",
                "path": "skills/ready/SKILL.md",
                "github_branch": "release/v2",
                "name": "ready",
                "category": "dev",
                "license": "MIT",
                "distribution": "compatible",
            },
        )
        rows = audit_skill_assets.build_backfill_targets(str(root), min_stars=100)

        assert rows == [
            {
                "stable_key": "acme/ready:skills/ready/SKILL.md",
                "archive_path": "dev/ready",
                "repo": "acme/ready",
                "source_path": "skills/ready/SKILL.md",
                "github_branch": "release/v2",
                "dir": "skills/ready",
                "name": "ready",
                "category": "dev",
                "stars": 500,
                "claim": "EXEC",
                "license": "MIT",
                "distribution": "compatible",
            }
        ]

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)
        assert report["ambiguous_stable_key_count"] == 1
        assert report["backfill_candidate_count"] == 1

    def test_invalid_candidate_identity_is_reported_and_blocks_targets(self, tmp_path):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "missing-path",
            "Run scripts/build.py.",
            {"stars": 900, "repo": "acme/no-path", "name": "missing-path"},
        )

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)

        assert report["source_identity_error_count"] == 1
        assert report["source_identity_errors"] == [
            {
                "archive_path": "dev/missing-path",
                "error": "missing_source_path",
                "eligible_for_backfill": True,
            }
        ]
        with pytest.raises(ValueError, match="dev/missing-path.*missing_source_path"):
            audit_skill_assets.build_backfill_targets(str(root), min_stars=100)

    def test_unapproved_distribution_is_reported_and_blocks_targets(self, tmp_path):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "restricted",
            "Run scripts/build.py.",
            {
                "stars": 900,
                "repo": "acme/restricted",
                "path": "skills/restricted/SKILL.md",
                "github_branch": "main",
                "name": "restricted",
                "category": "dev",
                "license": "GPL-3.0",
                "distribution": "restricted",
            },
        )

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)

        assert report["metadata_errors"] == [
            {
                "archive_path": "dev/restricted",
                "error": "asset_redistribution_not_approved",
                "eligible_for_backfill": True,
            }
        ]
        with pytest.raises(ValueError, match="asset_redistribution_not_approved"):
            audit_skill_assets.build_backfill_targets(str(root), min_stars=100)

    def test_invalid_candidate_bundle_declaration_blocks_targets(self, tmp_path):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "invalid-bundle",
            "Run scripts/build.py.",
            {
                "stars": 900,
                "repo": "acme/tools",
                "path": "skills/invalid-bundle/SKILL.md",
                "github_branch": "main",
                "bundled_files": ["references/a:b.md"],
            },
        )

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)
        assert report["metadata_errors"] == [
            {
                "archive_path": "dev/invalid-bundle",
                "error": "invalid_bundled_files",
                "eligible_for_backfill": True,
            }
        ]
        with pytest.raises(ValueError, match="dev/invalid-bundle.*invalid_bundled_files"):
            audit_skill_assets.build_backfill_targets(str(root), min_stars=100)

    def test_invalid_identity_and_bundle_declaration_both_block_targets(self, tmp_path):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "invalid-both",
            "Run scripts/build.py.",
            {
                "stars": 900,
                "repo": "acme/tools",
                "bundled_files": ["references/a:b.md"],
            },
        )

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)

        assert report["source_identity_errors"][0]["eligible_for_backfill"] is True
        assert report["metadata_errors"][0]["eligible_for_backfill"] is True
        with pytest.raises(ValueError, match="missing_source_path"):
            audit_skill_assets.build_backfill_targets(str(root), min_stars=100)

    @pytest.mark.parametrize(
        ("repo", "source_path", "error"),
        [
            ("not-a-repo", "skills/a/SKILL.md", "invalid_repo"),
            ("acme/tools", "../outside/SKILL.md", "invalid_source_path"),
            ("acme/tools", "/skills/a/SKILL.md", "absolute_source_path"),
            ("acme/tools", "C:\\skills\\a\\SKILL.md", "absolute_source_path"),
            ("acme/tools", "skills/a", "source_path_not_skill_md"),
        ],
    )
    def test_rejects_non_exact_source_identity(self, repo, source_path, error):
        assert audit_skill_assets.canonical_source_identity(repo, source_path)[2] == error

    def test_canonicalizes_backslashes_and_preserves_root_identity(self):
        assert audit_skill_assets.canonical_source_identity(
            "acme/tools", "skills\\a\\SKILL.md"
        ) == ("acme/tools", "skills/a/SKILL.md", "")
        assert audit_skill_assets.canonical_source_identity("acme/tools", "SKILL.md") == (
            "acme/tools",
            "SKILL.md",
            "",
        )

    def test_accepts_case_insensitive_skill_filename(self):
        assert audit_skill_assets.canonical_source_identity("acme/tools", "skills/a/skill.md") == (
            "acme/tools",
            "skills/a/skill.md",
            "",
        )

    def test_rejects_conflicting_source_path_aliases(self):
        assert (
            audit_skill_assets.canonical_source_identity_from_metadata(
                {
                    "repo": "acme/tools",
                    "path": "skills/old/SKILL.md",
                    "github_path": "skills/new/SKILL.md",
                }
            )[2]
            == "conflicting_source_path_aliases"
        )

    def test_nested_declared_skill_is_counted_only_as_support_file(self, tmp_path):
        root = tmp_path / "data"
        parent = make_skill(
            root,
            "dev",
            "parent",
            "See references/helper/SKILL.md.",
            {
                "repo": "acme/tools",
                "path": "skills/parent/SKILL.md",
                "name": "parent",
                "category": "dev",
                "archive_mode": "directory",
                "bundled_files": ["references/helper/SKILL.md"],
            },
        )
        helper = parent / "references" / "helper"
        helper.mkdir(parents=True)
        (helper / "SKILL.md").write_text("helper")

        report = audit_skill_assets.run_current_state(str(root), min_stars=0)

        assert report["total_skills"] == 1
        assert report["actual_bundled_file_count"] == 1
        assert report["local_verdict_counts"] == {"REF_ASSET": 1}

    def test_nested_skill_is_support_even_when_metadata_is_stale(self, tmp_path):
        root = tmp_path / "data"
        parent = make_skill(
            root,
            "dev",
            "parent",
            "See references/helper/SKILL.md.",
            {
                "repo": "acme/tools",
                "path": "skills/parent/SKILL.md",
                "archive_mode": "directory",
                "bundled_files": [],
            },
        )
        helper = parent / "references" / "helper"
        helper.mkdir(parents=True)
        (helper / "SKILL.md").write_text("helper")

        report = audit_skill_assets.run_current_state(str(root), min_stars=0)

        assert report["total_skills"] == 1
        assert report["actual_bundled_file_count"] == 1
        assert report["metadata_mismatch_count"] == 1

    def test_repository_case_aliases_are_ambiguous(self, tmp_path):
        root = tmp_path / "data"
        for name, repo in (("one", "Acme/Tools"), ("two", "acme/tools")):
            make_skill(
                root,
                "dev",
                name,
                "Run scripts/setup.py.",
                {
                    "repo": repo,
                    "path": "skills/demo/SKILL.md",
                    "stars": 100,
                },
            )

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)

        assert report["ambiguous_stable_key_count"] == 1
        assert report["backfill_candidate_count"] == 0

    @pytest.mark.parametrize(
        "declared",
        [{}, ["scripts/run.py", 7], ["scripts/run.py", "scripts/run.py"]],
    )
    def test_malformed_bundled_files_is_visible_drift(self, tmp_path, declared):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "broken",
            "body",
            {
                "repo": "acme/tools",
                "path": "skills/broken/SKILL.md",
                "archive_mode": "skill-md",
                "bundled_files": declared,
            },
        )

        report = audit_skill_assets.run_current_state(str(root), min_stars=0)

        assert report["metadata_mismatch_count"] == 1

    def test_rejects_symbolic_links(self, tmp_path):
        root = tmp_path / "data"
        skill = make_skill(
            root,
            "dev",
            "linked",
            "Run scripts/setup.py.",
            {"repo": "acme/tools", "path": "skills/linked/SKILL.md"},
        )
        outside = tmp_path / "outside.py"
        outside.write_text("print('outside')")
        (skill / "linked.py").symlink_to(outside)

        with pytest.raises(ValueError, match="symbolic link"):
            audit_skill_assets.run_current_state(str(root))

    def test_rejects_non_portable_existing_asset_paths(self, tmp_path):
        root = tmp_path / "data"
        skill = make_skill(
            root,
            "dev",
            "non-portable",
            "Read references/a:b.md.",
            {"repo": "acme/tools", "path": "skills/non-portable/SKILL.md"},
        )
        (skill / "references").mkdir()
        (skill / "references" / "a:b.md").write_text("body")

        with pytest.raises(ValueError, match="non-portable path"):
            audit_skill_assets.run_current_state(str(root))

    def test_rejects_symlinked_archive_directories(self, tmp_path):
        root = tmp_path / "data"
        make_skill(root, "dev", "valid", "body")
        outside = tmp_path / "outside-category"
        make_skill(outside, "external", "linked", "body")
        (root / "linked-category").symlink_to(outside / "external", target_is_directory=True)

        with pytest.raises(ValueError, match="symbolic link"):
            audit_skill_assets.run_current_state(str(root))

    @pytest.mark.parametrize("metadata_text", ["{broken", "[]"])
    def test_rejects_invalid_metadata(self, tmp_path, metadata_text):
        root = tmp_path / "data"
        skill = make_skill(root, "dev", "broken", "body")
        (skill / "metadata.json").write_text(metadata_text)

        with pytest.raises(ValueError, match="invalid metadata object"):
            audit_skill_assets.run_current_state(str(root))

    @pytest.mark.parametrize("stars", ["many", "100", 100.9, {}, [], -1, True])
    def test_rejects_invalid_stars(self, tmp_path, stars):
        root = tmp_path / "data"
        make_skill(
            root,
            "dev",
            "broken",
            "Run scripts/setup.py.",
            {
                "repo": "acme/tools",
                "path": "skills/broken/SKILL.md",
                "stars": stars,
            },
        )

        with pytest.raises(ValueError, match="invalid stars"):
            audit_skill_assets.run_current_state(str(root))


class TestAuditMain:
    def test_census_mode(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "census", str(archive)])
        audit_skill_assets.main()
        assert json.loads(capsys.readouterr().out)["total_skills"] == 4

    def test_targets_mode_with_threshold(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "targets", str(archive), "1"])
        audit_skill_assets.main()
        assert len(capsys.readouterr().out.splitlines()) == 2

    def test_current_state_mode(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "current-state", str(archive), "100"])
        audit_skill_assets.main()
        report = json.loads(capsys.readouterr().out)
        assert report["total_skills"] == 4
        assert report["backfill_candidate_count"] == 2

    def test_backfill_targets_mode(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "backfill-targets", str(archive), "100"])
        audit_skill_assets.main()
        rows = [json.loads(line) for line in capsys.readouterr().out.splitlines()]
        assert [row["stable_key"] for row in rows] == [
            "acme/docs:skills/with-docs/SKILL.md",
            "acme/tools:skills/with-script/SKILL.md",
        ]

    def test_bad_mode_exits(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["audit", "bogus", "/tmp"])
        with pytest.raises(SystemExit):
            audit_skill_assets.main()


def make_backfill_target(
    root, *, name="demo", repo="acme/tools", source_path="skills/demo/SKILL.md"
):
    skill = make_skill(
        root,
        "dev",
        name,
        "Run scripts/setup.py.",
        {
            "name": name,
            "repo": repo,
            "path": source_path,
            "category": "dev",
            "license": "MIT",
            "distribution": "compatible",
            "downloaded_at": "2026-01-02T00:00:00Z",
            "stars": 500,
            "github_branch": "main",
        },
    )
    target = {
        "stable_key": f"{repo}:{source_path}",
        "archive_path": f"dev/{name}",
        "repo": repo,
        "source_path": source_path,
        "github_branch": "main",
        "name": name,
        "category": "dev",
        "stars": 500,
        "claim": "EXEC",
        "license": "MIT",
        "distribution": "compatible",
    }
    return skill, target


class TestBackfillTargets:
    @pytest.mark.parametrize(
        ("metadata", "approved"),
        [
            ({"license": "MIT", "distribution": "compatible"}, True),
            ({"license": "MIT", "distribution": "restricted"}, False),
            ({"license": "GPL-3.0", "distribution": "compatible"}, False),
            ({}, False),
        ],
    )
    def test_ordinary_asset_redistribution_requires_explicit_approval(
        self, metadata, approved
    ):
        assert sync_download_support.asset_redistribution_approved(metadata) is approved

    @pytest.mark.parametrize(
        "entry",
        [
            {
                "type": "file",
                "path": "scripts/tool.py",
                "size": 0,
                "submodule_git_url": "https://github.com/acme/tool.git",
            },
            {
                "type": "file",
                "path": "scripts/huge.py",
                "size": sync_download_support.MAX_BUNDLED_FILE_BYTES + 1,
            },
        ],
    )
    def test_ordinary_collection_reports_support_scope_omissions(self, entry):
        async def listing_fetcher(_session, _repo, _branch, _directory):
            return [entry]

        entries, incomplete = asyncio.run(
            sync_download_support.collect_contents_bundled_file_entries(
                object(),
                "acme/tools",
                "main",
                "SKILL.md",
                listing_fetcher=listing_fetcher,
            )
        )

        assert entries == []
        assert incomplete is True

    def test_required_ordinary_bundle_rejects_empty_listing(self, tmp_path):
        async def empty_collector(*_args):
            return [], False

        result = asyncio.run(
            sync_download_support.download_bundled_files_to_directory(
                object(),
                "acme/tools",
                "main",
                "SKILL.md",
                tmp_path,
                True,
                pin_commit_sha=False,
                timeout=None,
                tree_cache={},
                contents_collector=empty_collector,
            )
        )

        assert result[1] == ["required bundled archive contains no eligible support files"]
        assert result[2] == "bundled_listing_incomplete"

    @pytest.mark.parametrize(
        "paths",
        [
            ["references/Guide.md", "references/guide.md"],
            ["References/one.md", "references/two.md"],
        ],
    )
    def test_download_selection_rejects_case_conflicts(self, paths):
        entries = [{"relative_path": path, "size": 1} for path in paths]

        with pytest.raises(sync_download_support.BundledListingError, match="case-conflicting"):
            sync_download_support.select_bundled_file_entries(entries)

    def test_loads_exact_target_and_preserves_existing_metadata(self, tmp_path):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")

        [loaded] = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

        assert loaded["stable_key"] == target["stable_key"]
        assert loaded["destination"] == archive_root / "dev" / "demo"
        assert loaded["skill"]["license"] == "MIT"
        assert loaded["skill"]["github_branch"] == target["github_branch"]

    @pytest.mark.parametrize(
        ("license_name", "distribution"),
        [("NOASSERTION", "restricted"), ("GPL-3.0", "restricted"), ("Vendor EULA", "compatible")],
    )
    def test_rejects_unapproved_asset_redistribution(self, tmp_path, license_name, distribution):
        archive_root = tmp_path / "archive"
        skill, target = make_backfill_target(archive_root)
        metadata_path = skill / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata.update({"license": license_name, "distribution": distribution})
        metadata_path.write_text(json.dumps(metadata))
        target.update({"license": license_name, "distribution": distribution})
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")

        with pytest.raises(ValueError, match="does not approve asset redistribution"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    @pytest.mark.parametrize(
        "branch_update",
        [
            None,
            {"github_branch": ""},
            {"github_branch": "bad branch"},
            {"github_branch": "release/v2"},
        ],
    )
    def test_rejects_missing_invalid_or_mismatched_target_branch(self, tmp_path, branch_update):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        target_payload = dict(target)
        if branch_update is None:
            target_payload.pop("github_branch")
        else:
            target_payload.update(branch_update)
        targets_path.write_text(json.dumps(target_payload) + "\n")

        with pytest.raises(ValueError, match="exact source branch|does not match"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    def test_accepts_matching_commit_pinned_target_ref(self, tmp_path):
        archive_root = tmp_path / "archive"
        skill, target = make_backfill_target(archive_root)
        pinned_ref = "a" * 40
        target["github_branch"] = pinned_ref
        metadata_path = skill / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["github_branch"] = pinned_ref
        metadata_path.write_text(json.dumps(metadata))
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")

        [loaded] = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

        assert loaded["skill"]["github_branch"] == pinned_ref

    def test_rejects_identity_mismatch_and_archive_traversal(self, tmp_path):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps({**target, "stable_key": "wrong"}) + "\n")
        with pytest.raises(ValueError, match="stable_key"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

        targets_path.write_text(json.dumps({**target, "archive_path": "../escape"}) + "\n")
        with pytest.raises(ValueError, match="archive_path"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    def test_rejects_duplicate_targets(self, tmp_path):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n" + json.dumps(target) + "\n")
        with pytest.raises(ValueError, match="duplicate backfill stable_key"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    def test_rejects_duplicate_destinations(self, tmp_path):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        second = {
            **target,
            "stable_key": "acme/other:skills/other/SKILL.md",
            "repo": "acme/other",
            "source_path": "skills/other/SKILL.md",
        }
        targets_path.write_text(json.dumps(target) + "\n" + json.dumps(second) + "\n")
        with pytest.raises(ValueError, match="duplicate backfill destination"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    def test_rejects_target_metadata_drift(self, tmp_path):
        archive_root = tmp_path / "archive"
        _skill, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps({**target, "category": "other"}) + "\n")
        with pytest.raises(ValueError, match="category does not match"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    @pytest.mark.parametrize(
        "alias_update",
        [
            {"github_path": "skills/other/SKILL.md"},
            {"branch": "develop"},
        ],
    )
    def test_rejects_conflicting_source_aliases(self, tmp_path, alias_update):
        archive_root = tmp_path / "archive"
        skill, target = make_backfill_target(archive_root)
        metadata_path = skill / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata.update(alias_update)
        metadata_path.write_text(json.dumps(metadata))
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")

        with pytest.raises(ValueError, match="identity mismatch|exact source branch"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)

    def test_rejects_symlinked_archive_parent(self, tmp_path):
        archive_root = tmp_path / "archive"
        real_category = archive_root / "real"
        _skill, target = make_backfill_target(real_category.parent, name="demo")
        (archive_root / "dev").rename(real_category)
        (archive_root / "dev").symlink_to(real_category, target_is_directory=True)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")

        with pytest.raises(ValueError, match="symbolic link"):
            backfill_skill_assets.load_backfill_targets(targets_path, archive_root)


class TestApplyStagedArchives:
    def _stage(self, stage_root, target, body="new"):
        staged = make_skill(
            stage_root,
            "dev",
            target["name"],
            body,
            {
                "name": target["name"],
                "repo": target["repo"],
                "path": target["source_path"],
                "category": "dev",
                "github_commit_sha": "a" * 40,
                "assets_verified_at": "2026-08-11T00:00:00Z",
                "github_branch": "main",
                "archive_mode": "directory",
                "bundled_files": ["scripts/setup.py"],
                "bundled_file_blobs": {"scripts/setup.py": git_blob_sha(b"print('ok')")},
            },
        )
        (staged / "scripts").mkdir()
        (staged / "scripts" / "setup.py").write_text("print('ok')")
        return staged

    def _allow_clean_scan(self, monkeypatch):
        monkeypatch.setattr(
            backfill_skill_assets,
            "_scan_archives_with_clamav",
            lambda archives, _binary: {
                key: backfill_skill_assets._archive_snapshot(path) for key, path in archives.items()
            },
        )

    def test_archive_snapshot_is_unambiguous_for_nul_content(self, tmp_path):
        single = tmp_path / "single"
        split = tmp_path / "split"
        single.mkdir()
        split.mkdir()
        (single / "a").write_bytes(b"x\0z\0")
        (split / "a").write_bytes(b"x")
        (split / "z").write_bytes(b"")

        assert backfill_skill_assets._archive_snapshot(single) != (
            backfill_skill_assets._archive_snapshot(split)
        )

    def test_archive_snapshot_includes_executable_mode(self, tmp_path):
        first = tmp_path / "first"
        second = tmp_path / "second"
        first.mkdir()
        second.mkdir()
        (first / "run.sh").write_text("exit 0")
        (second / "run.sh").write_text("exit 0")
        (first / "run.sh").chmod(0o644)
        (second / "run.sh").chmod(0o755)

        assert backfill_skill_assets._archive_snapshot(first) != (
            backfill_skill_assets._archive_snapshot(second)
        )

    def test_applies_complete_staged_archive(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        self._stage(stage_root, target)
        self._allow_clean_scan(monkeypatch)

        backfill_skill_assets.apply_staged_archives(loaded, stage_root)

        assert (destination / "SKILL.md").read_text() == "new"
        assert (destination / "scripts" / "setup.py").is_file()
        metadata = json.loads((destination / "metadata.json").read_text())
        assert metadata["dir_name"] == "demo"
        assert metadata["downloaded_at"] == "2026-01-02T00:00:00Z"

    def test_restores_original_when_atomic_swap_fails(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        self._stage(stage_root, target)
        self._allow_clean_scan(monkeypatch)
        real_replace = backfill_skill_assets.os.replace
        failed = False

        def fail_candidate_once(source, target_path, *args, **kwargs):
            nonlocal failed
            if ".backfill-" in str(source) and not failed:
                failed = True
                raise OSError("swap failed")
            return real_replace(source, target_path, *args, **kwargs)

        monkeypatch.setattr(backfill_skill_assets.os, "replace", fail_candidate_once)

        with pytest.raises(OSError, match="swap failed"):
            backfill_skill_assets.apply_staged_archives(loaded, stage_root)
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."

    def test_rolls_back_candidate_mutated_during_swap(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        self._stage(stage_root, target)
        self._allow_clean_scan(monkeypatch)
        real_replace = backfill_skill_assets.os.replace
        mutated = False

        def mutate_after_backup(source, target_path, *args, **kwargs):
            nonlocal mutated
            result = real_replace(source, target_path, *args, **kwargs)
            if source == destination.name and ".backup-" in str(target_path) and not mutated:
                candidate = next(destination.parent.glob(".demo.backfill-*"))
                (candidate / "scripts" / "setup.py").write_text("print('tampered')")
                mutated = True
            return result

        monkeypatch.setattr(backfill_skill_assets.os, "replace", mutate_after_backup)

        with pytest.raises(ValueError, match="differs from ClamAV scan"):
            backfill_skill_assets.apply_staged_archives(loaded, stage_root)
        assert mutated is True
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."
        assert not (destination / "scripts").exists()

    def test_rejects_non_hex_sha_and_unexpected_identity(self, tmp_path):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        staged = self._stage(stage_root, target)
        metadata_path = staged / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["github_commit_sha"] = "z" * 40
        metadata_path.write_text(json.dumps(metadata))
        with pytest.raises(ValueError, match="immutable commit SHA"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

        metadata["github_commit_sha"] = "a" * 40
        metadata["repo"] = "acme/unexpected"
        metadata_path.write_text(json.dumps(metadata))
        with pytest.raises(ValueError, match="staged identity mismatch"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

    def test_rejects_staged_archive_without_bundled_assets(self, tmp_path):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        staged = self._stage(stage_root, target)
        (staged / "scripts" / "setup.py").unlink()
        metadata_path = staged / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["bundled_files"] = []
        metadata_path.write_text(json.dumps(metadata))

        with pytest.raises(ValueError, match="contains no bundled files"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

    def test_rejects_case_conflicting_staged_declaration(self, tmp_path):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        staged = self._stage(stage_root, target)
        metadata_path = staged / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["bundled_files"] = ["scripts/Setup.py", "scripts/setup.py"]
        metadata_path.write_text(json.dumps(metadata))

        with pytest.raises(ValueError, match="case conflicts"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

    def test_rejects_drive_relative_staged_declaration(self, tmp_path):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        staged = self._stage(stage_root, target)
        metadata_path = staged / "metadata.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["bundled_files"] = ["C:scripts/setup.py"]
        metadata_path.write_text(json.dumps(metadata))

        with pytest.raises(ValueError, match="bundled_files is malformed"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

    def test_rejects_staged_asset_that_no_longer_matches_pinned_blob(self, tmp_path):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        staged = self._stage(stage_root, target)
        (staged / "scripts" / "setup.py").write_text("print('tampered')")

        with pytest.raises(ValueError, match="blob mismatch"):
            backfill_skill_assets.validate_staged_archives(loaded, stage_root)

    def test_descriptor_relative_replace_rejects_changed_parent(self, tmp_path):
        source = tmp_path / "source"
        source.mkdir()
        with pytest.raises(ValueError, match="parent changed"):
            backfill_skill_assets._replace_in_verified_directory(
                tmp_path,
                (-1, -1),
                source.name,
                "destination",
            )
        assert source.is_dir()

    def test_clamav_scans_final_merged_candidate(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        self._stage(stage_root, target)
        scanned_metadata = []

        def scan_final(archives, _binary):
            for path in archives.values():
                scanned_metadata.append(json.loads((path / "metadata.json").read_text()))
            return {
                key: backfill_skill_assets._archive_snapshot(path) for key, path in archives.items()
            }

        monkeypatch.setattr(backfill_skill_assets, "_scan_archives_with_clamav", scan_final)
        backfill_skill_assets.apply_staged_archives(loaded, stage_root)

        assert scanned_metadata[0]["downloaded_at"] == "2026-01-02T00:00:00Z"
        assert (destination / "metadata.json").is_file()

    def test_rollback_continues_after_one_restore_fails(self, tmp_path, monkeypatch):
        first = tmp_path / "first"
        second = tmp_path / "second"
        first_backup = tmp_path / "first-backup"
        second_backup = tmp_path / "second-backup"
        for path, body in (
            (first, "first-new"),
            (second, "second-new"),
            (first_backup, "first-old"),
            (second_backup, "second-old"),
        ):
            path.mkdir()
            (path / "value").write_text(body)
        real_replace = backfill_skill_assets.os.replace
        failed = False

        def fail_second_restore_once(source, target_path, *args, **kwargs):
            nonlocal failed
            if source == second_backup.name and not failed:
                failed = True
                raise OSError("restore failed")
            return real_replace(source, target_path, *args, **kwargs)

        monkeypatch.setattr(backfill_skill_assets.os, "replace", fail_second_restore_once)
        parent_identity = backfill_skill_assets._directory_identity(tmp_path)
        errors = backfill_skill_assets._rollback_applied_archives(
            [
                (first, first_backup, parent_identity),
                (second, second_backup, parent_identity),
            ]
        )

        assert errors and "restore failed" in errors[0]
        assert (first / "value").read_text() == "first-old"
        assert (second / "value").read_text() == "second-new"

    def test_rejects_destination_changed_after_target_load(self, tmp_path):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        loaded = backfill_skill_assets.load_backfill_targets(targets_path, archive_root)
        stage_root = tmp_path / "stage"
        self._stage(stage_root, target)
        (destination / "new-asset.py").write_text("print('changed')")

        with pytest.raises(ValueError, match="already contains support files"):
            backfill_skill_assets.apply_staged_archives(loaded, stage_root)
        assert (destination / "new-asset.py").is_file()


class TestRunBackfill:
    def test_rejects_report_path_inside_archive_before_download(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        original_metadata = (destination / "metadata.json").read_bytes()
        downloaded = False

        async def unexpected_download(*_args, **_kwargs):
            nonlocal downloaded
            downloaded = True

        monkeypatch.setattr(backfill_skill_assets, "download_skills", unexpected_download)
        with pytest.raises(ValueError, match="cannot overlap archive root"):
            asyncio.run(
                backfill_skill_assets.run_backfill(
                    targets_path,
                    archive_root,
                    destination / "metadata.json",
                    apply=True,
                )
            )

        assert not downloaded
        assert (destination / "metadata.json").read_bytes() == original_metadata

    def test_validates_in_staging_without_mutating_archive(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        report_path = tmp_path / "report.json"

        async def fake_download(registry_path, stage_root, *args, **kwargs):
            registry = json.loads(registry_path.read_text())
            skill = registry["skills"][0]
            staged = make_skill(
                stage_root,
                "dev",
                "demo",
                "new",
                {
                    **skill,
                    "github_commit_sha": "a" * 40,
                    "assets_verified_at": "2026-08-11T00:00:00Z",
                    "archive_mode": "directory",
                    "bundled_files": ["scripts/setup.py"],
                    "bundled_file_blobs": {"scripts/setup.py": git_blob_sha(b"print('ok')")},
                },
            )
            (staged / "scripts").mkdir()
            (staged / "scripts" / "setup.py").write_text("print('ok')")
            return {"downloaded": 1, "failed": 0}

        monkeypatch.setattr(backfill_skill_assets, "download_skills", fake_download)
        result = asyncio.run(
            backfill_skill_assets.run_backfill(targets_path, archive_root, report_path, apply=False)
        )

        assert result == 0
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."
        assert json.loads(report_path.read_text())["status"] == "validated"

    def test_reports_download_failure_without_mutating_archive(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        report_path = tmp_path / "report.json"

        async def failed_download(_registry_path, _stage_root, *_args, **kwargs):
            kwargs["failure_report_path"].write_text(
                json.dumps({"failures": [{"reason": "commit_resolution_failed"}]})
            )
            return {"downloaded": 0, "failed": 1}

        monkeypatch.setattr(backfill_skill_assets, "download_skills", failed_download)
        result = asyncio.run(
            backfill_skill_assets.run_backfill(targets_path, archive_root, report_path, apply=True)
        )

        report = json.loads(report_path.read_text())
        assert result == 1
        assert report["status"] == "failed"
        assert report["failure_report"]["failures"][0]["reason"] == "commit_resolution_failed"
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."

    def test_reports_validation_failure_without_mutating_archive(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        report_path = tmp_path / "report.json"

        async def empty_bundle_download(registry_path, stage_root, *_args, **_kwargs):
            skill = json.loads(registry_path.read_text())["skills"][0]
            make_skill(
                stage_root,
                "dev",
                "demo",
                "new",
                {
                    **skill,
                    "github_commit_sha": "a" * 40,
                    "assets_verified_at": "2026-08-11T00:00:00Z",
                    "archive_mode": "skill-md",
                    "bundled_files": [],
                },
            )
            return {"downloaded": 1, "failed": 0}

        monkeypatch.setattr(backfill_skill_assets, "download_skills", empty_bundle_download)
        result = asyncio.run(
            backfill_skill_assets.run_backfill(targets_path, archive_root, report_path, apply=True)
        )

        report = json.loads(report_path.read_text())
        assert result == 1
        assert report["status"] == "failed"
        assert "contains no bundled files" in report["error"]
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."

    def test_reports_apply_exception_as_failure(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        _destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        report_path = tmp_path / "report.json"

        async def successful_download(*_args, **_kwargs):
            return {"downloaded": 1, "failed": 0}

        monkeypatch.setattr(backfill_skill_assets, "download_skills", successful_download)
        monkeypatch.setattr(backfill_skill_assets, "validate_staged_archives", lambda *_args: {})
        monkeypatch.setattr(
            backfill_skill_assets,
            "scan_staged_archives_with_clamav",
            lambda *_args: None,
        )
        monkeypatch.setattr(
            backfill_skill_assets,
            "apply_staged_archives",
            lambda *_args: (_ for _ in ()).throw(OSError("apply failed")),
        )
        result = asyncio.run(
            backfill_skill_assets.run_backfill(targets_path, archive_root, report_path, apply=True)
        )

        report = json.loads(report_path.read_text())
        assert result == 1
        assert report["status"] == "failed"
        assert report["error"] == "OSError: apply failed"

    def test_clamav_failure_blocks_apply(self, tmp_path, monkeypatch):
        archive_root = tmp_path / "archive"
        destination, target = make_backfill_target(archive_root)
        targets_path = tmp_path / "targets.jsonl"
        targets_path.write_text(json.dumps(target) + "\n")
        report_path = tmp_path / "report.json"

        async def successful_download(registry_path, stage_root, *_args, **_kwargs):
            skill = json.loads(registry_path.read_text())["skills"][0]
            staged = make_skill(
                stage_root,
                "dev",
                "demo",
                "new",
                {
                    **skill,
                    "github_commit_sha": "a" * 40,
                    "assets_verified_at": "2026-08-11T00:00:00Z",
                    "archive_mode": "directory",
                    "bundled_files": ["scripts/setup.py"],
                    "bundled_file_blobs": {"scripts/setup.py": git_blob_sha(b"print('ok')")},
                },
            )
            (staged / "scripts").mkdir()
            (staged / "scripts" / "setup.py").write_text("print('ok')")
            return {"downloaded": 1, "failed": 0}

        monkeypatch.setattr(backfill_skill_assets, "download_skills", successful_download)
        monkeypatch.setattr(
            backfill_skill_assets,
            "_scan_archives_with_clamav",
            lambda *_args: (_ for _ in ()).throw(RuntimeError("ClamAV infected")),
        )
        result = asyncio.run(
            backfill_skill_assets.run_backfill(targets_path, archive_root, report_path, apply=True)
        )

        assert result == 1
        assert json.loads(report_path.read_text())["error"] == "RuntimeError: ClamAV infected"
        assert (destination / "SKILL.md").read_text() == "Run scripts/setup.py."

    @pytest.mark.parametrize("returncode", [1, 2])
    def test_clamav_nonzero_exit_is_fail_closed(self, tmp_path, monkeypatch, returncode):
        stage_root = tmp_path / "stage"
        stage_root.mkdir()
        monkeypatch.setattr(
            backfill_skill_assets.subprocess,
            "run",
            lambda *args, **kwargs: FakeCompleted(
                returncode=returncode, stdout="infected" if returncode == 1 else "", stderr="error"
            ),
        )

        with pytest.raises(RuntimeError, match="ClamAV rejected"):
            backfill_skill_assets.scan_staged_archives_with_clamav(stage_root)

    def test_missing_clamav_is_fail_closed(self, tmp_path, monkeypatch):
        stage_root = tmp_path / "stage"
        stage_root.mkdir()
        monkeypatch.setattr(
            backfill_skill_assets.subprocess,
            "run",
            lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError("clamscan")),
        )

        with pytest.raises(RuntimeError, match="unable to execute ClamAV"):
            backfill_skill_assets.scan_staged_archives_with_clamav(stage_root)
