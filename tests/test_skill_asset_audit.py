import hashlib
import json
import os
import sys
import urllib.error
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import archive_preflight
import audit_skill_assets
import verify_upstream_assets as liveness
from skill_asset_audit import (
    classify_files,
    classify_skill_text,
    iter_archived_skills,
    verdict_from_counts,
)


class TestClassifySkillText:
    def test_exec_reference(self):
        assert classify_skill_text("Run scripts/setup.py before use.") == "EXEC"

    def test_relative_exec_reference(self):
        assert classify_skill_text("Execute ./tools/build.sh to compile.") == "EXEC"

    def test_doc_reference_only(self):
        assert classify_skill_text("See references/guide.md for details.") == "REF"

    def test_bare(self):
        assert classify_skill_text("Just follow these markdown steps.") == "BARE"

    def test_url_does_not_count_as_exec(self):
        text = "Docs at https://example.com/raw/setup.py explain more."
        assert classify_skill_text(text) == "BARE"


class TestClassifyFiles:
    def test_counts_and_ignores_skill_md(self):
        counts = classify_files(
            [
                "s/SKILL.md",
                "s/metadata.json",
                "s/run.py",
                "s/notes.md",
                "s/logo.png",
            ]
        )
        assert counts == {"exec": 1, "doc": 1, "asset": 1}

    def test_verdicts(self):
        assert verdict_from_counts({"exec": 1, "doc": 0, "asset": 0}) == "EXEC"
        assert verdict_from_counts({"exec": 0, "doc": 2, "asset": 0}) == "REF_ASSET"
        assert verdict_from_counts({"exec": 0, "doc": 0, "asset": 0}) == "BARE"


class TestStrictBackfillInventory:
    @pytest.mark.parametrize("repo", ["../tools", "owner/..", "./repo", "owner/."])
    def test_rejects_dot_segment_repository_components(self, repo):
        assert (
            audit_skill_assets.canonical_source_identity(repo, "skills/demo/SKILL.md")[2]
            == "invalid_repo"
        )

    def test_requires_one_exact_source_branch(self):
        assert audit_skill_assets.canonical_source_branch_from_metadata({}) == (
            "",
            "missing_source_branch",
        )
        assert audit_skill_assets.canonical_source_branch_from_metadata(
            {
                "github_branch": "main",
                "branch": "release",
            }
        ) == ("", "conflicting_source_branch_aliases")
        assert audit_skill_assets.canonical_source_branch_from_metadata(
            {
                "github_branch": " release/v1 ",
                "branch": "release/v1",
            }
        ) == ("release/v1", "")
        pinned_ref = "a" * 40
        assert audit_skill_assets.canonical_source_branch_from_metadata(
            {
                "github_branch": pinned_ref,
            }
        ) == (pinned_ref, "")
        assert audit_skill_assets.canonical_source_branch_from_metadata(
            {
                "github_branch": "@",
            }
        ) == ("@", "")

    @pytest.mark.parametrize(
        "source_ref",
        ["main..evil", "main@{x}", "main.lock", ".hidden", "main/", "-main", "main?"],
    )
    def test_rejects_invalid_git_source_refs(self, source_ref):
        assert audit_skill_assets.canonical_source_branch_from_metadata(
            {
                "github_branch": source_ref,
            }
        ) == ("", "invalid_source_branch")

    def test_rejects_case_colliding_archive_roots(self, tmp_path, monkeypatch):
        root = tmp_path / "data"
        monkeypatch.setattr(
            audit_skill_assets,
            "_iter_canonical_archive_paths",
            lambda _root: iter(["dev/Demo", "dev/demo"]),
        )

        with pytest.raises(ValueError, match="case-conflicting skill roots"):
            list(audit_skill_assets._canonical_archive_rows(root))

    def test_archive_path_preflight_fails_closed_on_walk_error(self, tmp_path, monkeypatch):
        root = tmp_path / "data"

        def failed_walk(_root, *, onerror):
            onerror(PermissionError("denied"))
            yield from ()

        monkeypatch.setattr(audit_skill_assets.os, "walk", failed_walk)

        with pytest.raises(ValueError, match="unable to inspect archive tree.*denied"):
            list(audit_skill_assets._canonical_archive_rows(root))

    def test_archive_preflight_rejects_coexisting_skill_case_variants(
        self, tmp_path, monkeypatch
    ):
        root = tmp_path / "data"
        skill_dir = root / "dev" / "demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Demo", encoding="utf-8")

        monkeypatch.setattr(
            archive_preflight.os,
            "walk",
            lambda _root, *, onerror: iter(
                [(str(skill_dir), [], ["SKILL.md", "skill.md"])]
            ),
        )

        with pytest.raises(ValueError, match="case-conflicting SKILL.md files"):
            list(archive_preflight.iter_canonical_archive_paths(root))

    def test_canonical_archive_rows_reuse_fail_closed_preflight_paths(self, tmp_path, monkeypatch):
        root = tmp_path / "data"
        first = root / "dev" / "one"
        second = root / "dev" / "two"
        first.mkdir(parents=True)
        second.mkdir(parents=True)
        (first / "metadata.json").write_text('{"name":"one"}', encoding="utf-8")
        (second / "metadata.json").write_text('{"name":"two"}', encoding="utf-8")
        calls = 0

        def canonical_paths(_root):
            nonlocal calls
            calls += 1
            yield "dev/one"
            yield "dev/two"

        monkeypatch.setattr(audit_skill_assets, "_iter_canonical_archive_paths", canonical_paths)

        rows = iter(audit_skill_assets._canonical_archive_rows(root))
        assert next(rows) == (str(first), {"name": "one"})
        assert next(rows) == (str(second), {"name": "two"})
        with pytest.raises(StopIteration):
            next(rows)
        assert calls == 1

    @pytest.mark.parametrize(
        ("metadata", "expected_path"),
        [
            ({"repo": "acme/tools", "path": "skills/demo"}, "skills/demo/SKILL.md"),
            ({"repo": "acme/tools", "github_path": "skills/demo"}, "skills/demo/SKILL.md"),
            ({"repo": "acme/tools", "github_path": ""}, "SKILL.md"),
            (
                {
                    "repo": "acme/tools",
                    "path": "skills/demo/SKILL.md",
                    "github_path": "skills/demo",
                },
                "skills/demo/SKILL.md",
            ),
        ],
    )
    def test_normalizes_repository_directory_form_metadata_paths(self, metadata, expected_path):
        assert audit_skill_assets.canonical_source_identity_from_metadata(metadata) == (
            "acme/tools",
            expected_path,
            "",
        )

    def test_direct_canonical_source_still_requires_exact_skill_path(self):
        assert audit_skill_assets.canonical_source_identity("acme/tools", "skills/demo") == (
            "acme/tools",
            "skills/demo",
            "source_path_not_skill_md",
        )

    @pytest.mark.parametrize("field", ["path", "github_path"])
    def test_metadata_file_path_is_not_reinterpreted_as_directory(self, field):
        assert audit_skill_assets.canonical_source_identity_from_metadata(
            {"repo": "acme/tools", field: "README.md"}
        ) == ("acme/tools", "README.md", "source_path_not_skill_md")

    def test_dotted_directory_metadata_path_is_preserved(self):
        assert audit_skill_assets.canonical_source_identity_from_metadata(
            {"repo": "acme/tools", "path": "skills/v1.0"}
        ) == ("acme/tools", "skills/v1.0/SKILL.md", "")

    def test_conflicting_aliases_contribute_every_normalized_identity_key(self):
        keys = audit_skill_assets._identity_keys(
            {
                "repo": "Acme/Tools",
                "path": "skills/one/SKILL.md",
                "github_path": "skills/two/SKILL.md",
            },
            name="demo",
            category="dev",
        )
        assert keys == {
            "acme/tools:skills/one/SKILL.md",
            "acme/tools:skills/two/SKILL.md",
        }

    @pytest.mark.parametrize(
        "paths",
        [
            ["references/Guide.md", "references/guide.md"],
            ["References/one.md", "references/two.md"],
        ],
    )
    def test_detects_case_conflicts_in_files_and_directory_prefixes(self, paths):
        assert audit_skill_assets.has_case_conflicting_paths(paths) is True

    @pytest.mark.parametrize(
        "declared",
        [
            ["references//guide.md"],
            ["C:/scripts/run.py"],
            ["C:scripts/run.py"],
            ["skill.md"],
            ["SKILL.MD"],
            ["Metadata.json"],
            ["references/Guide.md", "references/guide.md"],
            ["References/one.md", "references/two.md"],
        ],
    )
    def test_rejects_non_portable_bundled_file_declarations(self, declared):
        assert audit_skill_assets._declared_bundled_files(
            {
                "bundled_files": declared,
            }
        ) == ([], False)

    def test_nested_metadata_is_a_bundled_asset(self):
        assert audit_skill_assets._local_verdict(["references/metadata.json"]) == "REF_ASSET"

    def test_nested_metadata_keeps_current_state_internally_consistent(self, tmp_path):
        skill = tmp_path / "data" / "dev" / "demo"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("See references/metadata.json.", encoding="utf-8")
        (skill / "references" / "metadata.json").write_text("{}", encoding="utf-8")

        report = audit_skill_assets.run_current_state(str(tmp_path / "data"), min_stars=0)

        assert report["actual_bundled_file_count"] == 1
        assert report["local_verdict_counts"] == {"REF_ASSET": 1}

    def test_support_file_scan_fails_closed_on_walk_error(self, tmp_path, monkeypatch):
        skill = tmp_path / "dev" / "demo"
        skill.mkdir(parents=True)

        def failed_walk(_root, *, onerror):
            onerror(PermissionError("denied"))
            yield from ()

        monkeypatch.setattr(audit_skill_assets.os, "walk", failed_walk)

        with pytest.raises(ValueError, match="unable to inspect archive skill.*denied"):
            audit_skill_assets._actual_bundled_files(str(skill))

    @pytest.mark.parametrize(
        ("category", "name"),
        [("CON", "demo"), ("dev", "demo.")],
    )
    def test_rejects_nonportable_canonical_archive_root(self, tmp_path, category, name):
        root = tmp_path / "data"
        skill = root / category / name
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body", encoding="utf-8")

        with pytest.raises(ValueError, match="non-portable canonical archive path"):
            audit_skill_assets.run_current_state(str(root))

    def test_rejects_miscased_canonical_skill_filename(self, tmp_path):
        root = tmp_path / "data"
        valid = root / "dev" / "valid"
        invalid = root / "dev" / "invalid"
        valid.mkdir(parents=True)
        invalid.mkdir(parents=True)
        (valid / "SKILL.md").write_text("body", encoding="utf-8")
        (invalid / "skill.md").write_text("body", encoding="utf-8")

        with pytest.raises(ValueError, match="canonical SKILL.md has invalid casing"):
            audit_skill_assets.run_current_state(str(root))

    @pytest.mark.parametrize(
        ("filename", "error"),
        [
            ("Metadata.json", "canonical metadata.json has invalid casing"),
            ("METADATA.JSON", "canonical metadata.json has invalid casing"),
        ],
    )
    def test_rejects_miscased_canonical_metadata_filename(
        self, tmp_path, filename, error
    ):
        root = tmp_path / "data"
        skill = root / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body", encoding="utf-8")
        (skill / filename).write_text("{}", encoding="utf-8")

        with pytest.raises(ValueError, match=error):
            audit_skill_assets.run_current_state(str(root))

    def test_rejects_coexisting_canonical_skill_case_variants(
        self, tmp_path, monkeypatch
    ):
        root = tmp_path / "data"
        skill = root / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body", encoding="utf-8")
        monkeypatch.setattr(
            audit_skill_assets.os,
            "walk",
            lambda _root, *, onerror: iter(
                [(str(skill), [], ["SKILL.md", "skill.md"])]
            ),
        )

        with pytest.raises(ValueError, match="case-conflicting SKILL.md files"):
            audit_skill_assets.run_current_state(str(root))

    @pytest.mark.parametrize(
        ("filename", "error"),
        [
            ("SKILL.md", "canonical SKILL.md must be a regular file"),
            ("metadata.json", "canonical metadata.json must be a regular file"),
        ],
    )
    def test_rejects_symlinked_canonical_files(self, tmp_path, filename, error):
        root = tmp_path / "data"
        skill = root / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body", encoding="utf-8")
        target = tmp_path / f"outside-{filename}"
        target.write_text("{}" if filename == "metadata.json" else "body", encoding="utf-8")
        canonical = skill / filename
        canonical.unlink(missing_ok=True)
        canonical.symlink_to(target)

        with pytest.raises(ValueError, match=error):
            audit_skill_assets.run_current_state(str(root))

    def test_conflicting_alias_record_makes_valid_candidate_ambiguous(self, tmp_path):
        root = tmp_path / "data"
        for name, metadata in (
            (
                "valid",
                {
                    "repo": "acme/tools",
                    "path": "skills/one/SKILL.md",
                    "github_branch": "main",
                    "stars": 100,
                },
            ),
            (
                "conflict",
                {
                    "repo": "Acme/Tools",
                    "path": "skills/two/SKILL.md",
                    "github_path": "skills/one/SKILL.md",
                    "github_branch": "main",
                    "stars": 100,
                },
            ),
        ):
            skill = root / "dev" / name
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Run scripts/setup.py.", encoding="utf-8")
            (skill / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

        report = audit_skill_assets.run_current_state(str(root), min_stars=100)

        assert report["ambiguous_stable_key_count"] == 1
        assert report["backfill_candidate_count"] == 0

    def test_backfill_target_preserves_source_branch(self, tmp_path):
        skill = tmp_path / "data" / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Run scripts/setup.py.", encoding="utf-8")
        (skill / "metadata.json").write_text(
            json.dumps(
                {
                    "repo": "acme/tools",
                    "path": "skills/demo/SKILL.md",
                    "github_branch": "release/v1",
                    "stars": 100,
                    "license": "MIT",
                    "distribution": "compatible",
                }
            ),
            encoding="utf-8",
        )

        [target] = audit_skill_assets.build_backfill_targets(str(tmp_path / "data"), min_stars=100)

        assert target["github_branch"] == "release/v1"

    def test_directory_form_path_emits_exact_backfill_identity(self, tmp_path):
        skill = tmp_path / "data" / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("Run scripts/setup.py.", encoding="utf-8")
        (skill / "metadata.json").write_text(
            json.dumps(
                {
                    "repo": "acme/tools",
                    "path": "skills/demo",
                    "github_branch": "main",
                    "stars": 100,
                    "license": "MIT",
                    "distribution": "compatible",
                }
            ),
            encoding="utf-8",
        )

        [target] = audit_skill_assets.build_backfill_targets(str(tmp_path / "data"), min_stars=100)

        assert target["source_path"] == "skills/demo/SKILL.md"
        assert target["stable_key"] == "acme/tools:skills/demo/SKILL.md"

    @pytest.mark.parametrize(
        ("body", "bundled_files"),
        [
            ("No recognizable asset reference.", ["package.json"]),
            ("Run src/widget.jsx before continuing.", None),
        ],
    )
    def test_pipeline_asset_claims_are_backfill_eligible(
        self, tmp_path, body, bundled_files
    ):
        skill = tmp_path / "data" / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(body, encoding="utf-8")
        metadata = {
            "repo": "acme/tools",
            "path": "skills/demo/SKILL.md",
            "github_branch": "main",
            "stars": 100,
            "license": "MIT",
            "distribution": "compatible",
        }
        if bundled_files is not None:
            metadata.update(
                {"archive_mode": "directory", "bundled_files": bundled_files}
            )
        (skill / "metadata.json").write_text(json.dumps(metadata), encoding="utf-8")

        [target] = audit_skill_assets.build_backfill_targets(
            str(tmp_path / "data"), min_stars=100
        )

        assert target["stable_key"] == "acme/tools:skills/demo/SKILL.md"

    def test_remote_asset_url_is_not_a_backfill_claim(self, tmp_path):
        skill = tmp_path / "data" / "dev" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text(
            "Read https://example.com/references/guide.md.", encoding="utf-8"
        )
        (skill / "metadata.json").write_text(
            json.dumps(
                {
                    "repo": "acme/tools",
                    "path": "skills/demo/SKILL.md",
                    "github_branch": "main",
                    "stars": 100,
                }
            ),
            encoding="utf-8",
        )

        assert audit_skill_assets.build_backfill_targets(
            str(tmp_path / "data"), min_stars=100
        ) == []


@pytest.mark.parametrize("path", ["references/CONIN$.md", "references/CONOUT$.txt"])
def test_windows_console_device_names_are_not_portable(path):
    assert audit_skill_assets.is_safe_portable_relative_path(path) is False


class TestIterArchivedSkills:
    def test_yields_skill_dirs_with_metadata(self, tmp_path):
        skill = tmp_path / "cat" / "demo"
        skill.mkdir(parents=True)
        (skill / "SKILL.md").write_text("body")
        (skill / "metadata.json").write_text(json.dumps({"stars": 5}))
        (tmp_path / "cat" / "not-a-skill").mkdir()

        results = list(iter_archived_skills(str(tmp_path)))
        assert len(results) == 1
        dirpath, meta = results[0]
        assert dirpath.endswith("demo")
        assert meta == {"stars": 5}

    def test_bad_metadata_yields_none(self, tmp_path):
        skill = tmp_path / "demo"
        skill.mkdir()
        (skill / "SKILL.md").write_text("body")
        (skill / "metadata.json").write_text("{broken")
        [(_, meta)] = list(iter_archived_skills(str(tmp_path)))
        assert meta is None


def make_verified_asset(
    root: Path,
    name: str,
    *,
    repo: str = "acme/tools",
    branch: str = "main",
    bundled_files: list[str] | None = None,
) -> Path:
    files = bundled_files or ["scripts/run.py"]
    skill_dir = root / "dev" / name
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("Run scripts/run.py", encoding="utf-8")
    for filename in files:
        path = skill_dir / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"asset")
    blob_header = b"blob 5\0"
    blob_sha = hashlib.sha1(blob_header + b"asset", usedforsecurity=False).hexdigest()
    metadata = {
        "name": name,
        "repo": repo,
        "path": f"skills/{name}/SKILL.md",
        "github_branch": branch,
        "github_commit_sha": "a" * 40,
        "assets_verified_at": "2026-08-01T00:00:00Z",
        "archive_mode": "directory",
        "bundled_files": files,
        "bundled_file_blobs": dict.fromkeys(files, blob_sha),
    }
    metadata_path = skill_dir / "metadata.json"
    metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
    return metadata_path


class FakeLivenessClient:
    def __init__(self, paths=None, *, repo_error=None, branch_error=None, tree_error=None):
        self.paths = set(paths or [])
        self.repo_error = repo_error
        self.branch_error = branch_error
        self.tree_error = tree_error
        self.calls = []

    def repository(self, repo):
        self.calls.append(("repo", repo))
        if self.repo_error:
            raise self.repo_error
        return {"full_name": repo}

    def branch_sha(self, repo, branch):
        self.calls.append(("branch", repo, branch))
        if self.branch_error:
            raise self.branch_error
        return "b" * 40

    def tree(self, repo, sha):
        self.calls.append(("tree", repo, sha))
        if self.tree_error:
            raise self.tree_error
        return self.paths


class TestAssetLiveness:
    def test_public_legacy_verifier_functions_remain_supported(self, monkeypatch):
        target = {"repo": "acme/tools", "dir": "skills/demo", "name": "demo"}
        monkeypatch.setattr(
            liveness,
            "fetch_repo_tree",
            lambda _repo: ["skills/demo/SKILL.md", "skills/demo/scripts/run.py"],
        )

        assert liveness.resolve_skill_dir(target, ["skills/demo"]) == "skills/demo"
        [row] = liveness.verify_repo("acme/tools", [target])
        assert row["status"] == "EXEC"

    def test_legacy_jsonl_verifier_interface_remains_supported(self, tmp_path, monkeypatch, capsys):
        targets_path = tmp_path / "targets.jsonl"
        output_path = tmp_path / "verified.jsonl"
        targets_path.write_text(
            json.dumps(
                {
                    "repo": "acme/tools",
                    "dir": "skills/demo",
                    "name": "demo",
                    "stars": 100,
                }
            )
            + "\n",
            encoding="utf-8",
        )
        monkeypatch.setattr(
            liveness,
            "fetch_repo_tree",
            lambda _repo: ["skills/demo/SKILL.md", "skills/demo/scripts/run.py"],
        )

        assert liveness.main([str(targets_path), str(output_path)]) == 0

        [row] = [json.loads(line) for line in output_path.read_text().splitlines()]
        assert row["resolved_dir"] == "skills/demo"
        assert row["status"] == "EXEC"
        assert json.loads(capsys.readouterr().err) == {"EXEC": 1}

    def test_skips_ordinary_directory_archives_without_verification_evidence(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "ordinary")
        metadata = json.loads(metadata_path.read_text())
        for field in liveness.VERIFICATION_EVIDENCE_FIELDS:
            metadata.pop(field, None)
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert errors == []

    def test_groups_repository_and_branch_then_applies_live_and_partial(self, tmp_path):
        skills = tmp_path / "skills"
        first = make_verified_asset(skills, "alpha")
        second = make_verified_asset(skills, "beta")
        client = FakeLivenessClient(
            {
                "skills/alpha/SKILL.md",
                "skills/alpha/scripts/run.py",
                "skills/beta/SKILL.md",
            }
        )
        report_path = tmp_path / "report.json"

        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(report_path),
                "--apply",
                "--max-decayed-percent",
                "100",
            ],
            client=client,
        )

        assert result == 0
        assert [call[0] for call in client.calls] == ["repo", "branch", "tree"]
        report = json.loads(report_path.read_text())
        assert report["summary"] == {"live": 1, "partial": 1}
        assert report["repo_count"] == 1
        assert report["applied"] is True
        alpha = json.loads(first.read_text())
        beta = json.loads(second.read_text())
        assert alpha["asset_liveness"] == "live"
        assert beta["asset_liveness"] == "partial"
        assert alpha["github_commit_sha"] == "a" * 40
        assert alpha["assets_liveness_sha"] == "b" * 40
        assert alpha["assets_verified_at"] == "2026-08-01T00:00:00Z"

    def test_api_failure_preserves_previous_verified_state(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        metadata = json.loads(metadata_path.read_text())
        metadata.update(
            {
                "asset_liveness": "live",
                "assets_liveness_checked_at": "2026-08-02T00:00:00Z",
                "assets_liveness_sha": "c" * 40,
            }
        )
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        before = metadata_path.read_bytes()
        client = FakeLivenessClient(repo_error=liveness.GitHubApiError(503, "service unavailable"))

        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(tmp_path / "report.json"),
                "--apply",
                "--max-error-percent",
                "100",
            ],
            client=client,
        )

        assert result == 0
        assert metadata_path.read_bytes() == before
        report = json.loads((tmp_path / "report.json").read_text())
        assert report["summary"] == {"verification_error": 1}

    def test_missing_repo_records_gone_without_deleting_archive(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        metadata = json.loads(metadata_path.read_text())
        metadata["assets_liveness_sha"] = "c" * 40
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        client = FakeLivenessClient(repo_error=liveness.GitHubApiError(404, "not found"))

        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(tmp_path / "report.json"),
                "--apply",
                "--max-decayed-percent",
                "100",
            ],
            client=client,
        )

        assert result == 0
        updated = json.loads(metadata_path.read_text())
        assert updated["asset_liveness"] == "gone"
        assert "assets_liveness_sha" not in updated
        assert (metadata_path.parent / "scripts/run.py").is_file()

    def test_missing_branch_is_moved_and_missing_skill_path_is_moved(self, tmp_path):
        skills = tmp_path / "skills"
        make_verified_asset(skills, "alpha")
        targets, errors = liveness.load_targets(skills)
        assert not errors
        branch_client = FakeLivenessClient(
            branch_error=liveness.GitHubApiError(404, "branch missing")
        )
        [branch_row] = liveness.verify_targets(targets, branch_client, "now")
        assert branch_row["status"] == "moved"
        path_client = FakeLivenessClient({"skills/alpha/scripts/run.py"})
        [path_row] = liveness.verify_targets(targets, path_client, "now")
        assert path_row["status"] == "moved"
        assert path_row["current_source_sha"] == "b" * 40

    def test_tree_failure_preserves_state_as_verification_error(self, tmp_path):
        skills = tmp_path / "skills"
        make_verified_asset(skills, "alpha")
        targets, errors = liveness.load_targets(skills)
        assert not errors
        client = FakeLivenessClient(tree_error=liveness.GitHubApiError(404, "tree unavailable"))
        [row] = liveness.verify_targets(targets, client, "now")
        assert row["status"] == "verification_error"
        assert [call[0] for call in client.calls] == ["repo", "branch", "tree"]

    def test_repository_identity_redirect_is_moved(self, tmp_path):
        skills = tmp_path / "skills"
        make_verified_asset(skills, "alpha")
        targets, _ = liveness.load_targets(skills)
        client = FakeLivenessClient()
        client.repository = lambda _repo: {"full_name": "other/tools"}
        [row] = liveness.verify_targets(targets, client, "now")
        assert row["status"] == "moved"

    def test_local_mismatch_fails_closed_without_api_call(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        (metadata_path.parent / "scripts/run.py").unlink()
        client = FakeLivenessClient()
        before = metadata_path.read_bytes()

        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(tmp_path / "report.json"),
                "--apply",
                "--max-error-percent",
                "100",
            ],
            client=client,
        )

        assert result == 1
        assert client.calls == []
        assert metadata_path.read_bytes() == before
        report = json.loads((tmp_path / "report.json").read_text())
        assert report["summary"] == {"local_error": 1}

    def test_local_blob_mismatch_fails_closed_without_api_call(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        (metadata_path.parent / "scripts/run.py").write_text("tampered", encoding="utf-8")
        client = FakeLivenessClient()

        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(tmp_path / "report.json"),
                "--apply",
                "--max-error-percent",
                "100",
            ],
            client=client,
        )

        assert result == 1
        assert client.calls == []
        report = json.loads((tmp_path / "report.json").read_text())
        assert report["summary"] == {"local_error": 1}
        assert "do not match archived support file bytes" in report["rows"][0]["error"]

    @pytest.mark.parametrize("metadata_state", ["missing", "dangling", "directory"])
    def test_missing_or_nonregular_metadata_is_local_error(self, tmp_path, metadata_state):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        metadata_path.unlink()
        if metadata_state == "dangling":
            metadata_path.symlink_to(tmp_path / "missing.json")
        elif metadata_state == "directory":
            metadata_path.mkdir()

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert errors == [
            {
                "stable_key": "dev/alpha",
                "status": "local_error",
                "error": "metadata.json must be a regular file",
            }
        ]

    @pytest.mark.parametrize(
        "change,error",
        [
            ({"bundled_files": []}, "non-empty"),
            ({"bundled_files": ["../run.py"]}, "invalid or duplicate"),
            ({"bundled_files": ["skill.md"]}, "invalid or duplicate"),
            ({"bundled_files": ["Metadata.json"]}, "invalid or duplicate"),
            ({"bundled_files": ["skill.md/run.py"]}, "invalid or duplicate"),
            ({"bundled_files": ["C:scripts/run.py"]}, "invalid or duplicate"),
            (
                {"bundled_files": ["scripts/Run.py", "scripts/run.py"]},
                "case-conflicting",
            ),
            ({"github_commit_sha": None}, "immutable"),
            ({"github_commit_sha": "not-a-sha"}, "immutable"),
            ({"github_branch": ""}, "github_branch must be a non-empty string"),
            ({"github_branch": "d" * 40}, "raw commit SHA"),
            ({"github_path": "other/SKILL.md"}, "conflicting path"),
            ({"branch": "develop"}, "conflicting github_branch"),
            (
                {"path": "", "github_path": "skills/alpha/SKILL.md"},
                "path must be a non-empty string",
            ),
            ({"github_branch": [], "branch": "main"}, "github_branch must be"),
        ],
    )
    def test_invalid_canonical_metadata_is_a_local_error(self, tmp_path, change, error):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        metadata = json.loads(metadata_path.read_text())
        metadata.update(change)
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        targets, errors = liveness.load_targets(skills)
        assert targets == []
        assert error in errors[0]["error"]

    @pytest.mark.parametrize("level", ["category", "skill"])
    def test_symlinked_archive_parent_is_rejected(self, tmp_path, level):
        external = tmp_path / "external"
        metadata_path = make_verified_asset(external, "alpha")
        skills = tmp_path / "skills"
        skills.mkdir()
        if level == "category":
            (skills / "dev").symlink_to(external / "dev", target_is_directory=True)
        else:
            (skills / "dev").mkdir()
            (skills / "dev" / "alpha").symlink_to(metadata_path.parent, target_is_directory=True)
        targets, errors = liveness.load_targets(skills)
        assert targets == []
        assert "cannot be a symlink" in errors[0]["error"]

    @pytest.mark.parametrize(
        ("category", "name"),
        [("CON", "alpha"), ("dev", "alpha.")],
    )
    def test_nonportable_canonical_roots_are_liveness_errors(
        self, tmp_path, category, name
    ):
        skills = tmp_path / "skills"
        make_verified_asset(skills, name)
        if category != "dev":
            (skills / "dev").rename(skills / category)

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert "non-portable canonical archive path" in errors[0]["error"]

    def test_miscased_canonical_skill_file_is_a_liveness_error(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        skill_path = metadata_path.parent / "SKILL.md"
        miscased_path = metadata_path.parent / "skill.md"
        skill_path.rename(miscased_path)
        if not any(path.name == "skill.md" for path in metadata_path.parent.iterdir()):
            pytest.skip("case-insensitive filesystem cannot represent the fixture")

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert "canonical SKILL.md has invalid casing" in errors[0]["error"]

    def test_symlinked_canonical_skill_file_is_a_liveness_error(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        skill_path = metadata_path.parent / "SKILL.md"
        external = tmp_path / "outside.md"
        external.write_text("# Outside", encoding="utf-8")
        skill_path.unlink()
        skill_path.symlink_to(external)

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert "regular non-symlink file" in errors[0]["error"]

    def test_case_conflicting_skill_roots_are_rejected(self, tmp_path):
        skills = tmp_path / "skills"
        make_verified_asset(skills, "Alpha")
        try:
            make_verified_asset(skills, "alpha")
        except FileExistsError:
            pytest.skip("case-insensitive filesystem cannot represent the fixture")

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert "case-conflicting skill paths" in errors[0]["error"]

    def test_case_conflicting_category_roots_are_rejected(self, tmp_path):
        skills = tmp_path / "skills"
        first = make_verified_asset(skills, "alpha")
        first.parent.parent.rename(skills / "Dev")
        try:
            make_verified_asset(skills, "beta")
        except FileExistsError:
            pytest.skip("case-insensitive filesystem cannot represent the fixture")
        if len(list(skills.iterdir())) < 2:
            pytest.skip("case-insensitive filesystem cannot represent the fixture")

        targets, errors = liveness.load_targets(skills)

        assert targets == []
        assert "case-conflicting category paths" in errors[0]["error"]

    def test_apply_rejects_changed_metadata(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        targets, errors = liveness.load_targets(skills)
        assert not errors
        metadata_path.write_text(metadata_path.read_text() + "\n", encoding="utf-8")
        rows = [
            {"stable_key": targets[0].stable_key, "status": "live", "current_source_sha": "b" * 40}
        ]
        apply_errors = liveness.apply_updates(targets, rows, "now")
        assert "changed after verification" in apply_errors[0]

    def test_gate_recomputes_summary_and_enforces_thresholds(self):
        report = {
            "rows": [
                {"status": "live"},
                {"status": "partial"},
                {"status": "verification_error"},
            ],
            "summary": {"live": 1, "partial": 1, "verification_error": 1},
            "target_count": 3,
        }
        errors = liveness.gate_errors(
            report, max_decayed_percent=20, max_error_percent=20, min_targets=4
        )
        assert len(errors) == 3
        report["summary"] = {"live": 3}
        assert (
            "summary mismatch"
            in liveness.gate_errors(
                report, max_decayed_percent=100, max_error_percent=100, min_targets=1
            )[0]
        )
        malformed = liveness.gate_errors(
            {"rows": None, "summary": {}, "target_count": 0},
            max_decayed_percent=100,
            max_error_percent=100,
            min_targets=1,
        )
        assert malformed == ["report rows or summary is malformed"]

    def test_apply_error_always_fails_even_below_error_threshold(self):
        rows = [{"status": "live"} for _ in range(20)] + [{"status": "apply_error"}]
        report = {
            "rows": rows,
            "summary": liveness.summarize(rows),
            "target_count": 20,
        }
        assert liveness.gate_errors(
            report, max_decayed_percent=100, max_error_percent=10, min_targets=1
        ) == ["metadata apply or rollback failed"]

    def test_main_apply_failure_rolls_back_and_fails_gate(self, tmp_path, monkeypatch):
        skills = tmp_path / "skills"
        first = make_verified_asset(skills, "alpha")
        second = make_verified_asset(skills, "beta")
        originals = {path: path.read_bytes() for path in (first, second)}
        real_write = liveness._write_atomic
        failed = False

        def fail_second_update(path, content):
            nonlocal failed
            if path == second and not failed and b'"asset_liveness"' in content:
                failed = True
                raise OSError("replace failed")
            real_write(path, content)

        monkeypatch.setattr(liveness, "_write_atomic", fail_second_update)
        client = FakeLivenessClient(
            {
                "skills/alpha/SKILL.md",
                "skills/alpha/scripts/run.py",
                "skills/beta/SKILL.md",
                "skills/beta/scripts/run.py",
            }
        )
        report_path = tmp_path / "report.json"
        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(report_path),
                "--apply",
                "--max-error-percent",
                "100",
            ],
            client=client,
        )
        assert result == 1
        assert {path: path.read_bytes() for path in (first, second)} == originals
        report = json.loads(report_path.read_text())
        assert report["summary"]["apply_error"] == 1
        assert report["gate"]["passed"] is False

    def test_main_metadata_drift_fails_gate_without_overwrite(self, tmp_path):
        skills = tmp_path / "skills"
        metadata_path = make_verified_asset(skills, "alpha")
        original = metadata_path.read_bytes()
        client = FakeLivenessClient(
            {
                "skills/alpha/SKILL.md",
                "skills/alpha/scripts/run.py",
            }
        )
        real_tree = client.tree

        def mutate_then_list(repo, sha):
            metadata_path.write_bytes(original + b"\n")
            return real_tree(repo, sha)

        client.tree = mutate_then_list
        report_path = tmp_path / "report.json"
        result = liveness.main(
            [
                "--skills-dir",
                str(skills),
                "--report",
                str(report_path),
                "--apply",
                "--max-error-percent",
                "100",
            ],
            client=client,
        )
        assert result == 1
        assert metadata_path.read_bytes() == original + b"\n"
        report = json.loads(report_path.read_text())
        assert report["summary"]["apply_error"] == 1

    def test_apply_reports_incomplete_rollback(self, tmp_path, monkeypatch):
        skills = tmp_path / "skills"
        first = make_verified_asset(skills, "alpha")
        second = make_verified_asset(skills, "beta")
        targets, errors = liveness.load_targets(skills)
        assert not errors
        originals = {path: path.read_bytes() for path in (first, second)}
        real_write = liveness._write_atomic
        apply_failed = False

        def fail_apply_and_restore(path, content):
            nonlocal apply_failed
            if path == second and not apply_failed and b'"asset_liveness"' in content:
                apply_failed = True
                raise OSError("apply failed")
            if path == first and apply_failed and content == originals[first]:
                raise OSError("restore failed")
            real_write(path, content)

        monkeypatch.setattr(liveness, "_write_atomic", fail_apply_and_restore)
        rows = [
            {"stable_key": target.stable_key, "status": "live", "current_source_sha": "b" * 40}
            for target in targets
        ]
        apply_errors = liveness.apply_updates(targets, rows, "now")
        assert "recovery failed" in apply_errors[0]
        assert json.loads(first.read_text())["asset_liveness"] == "live"
        assert second.read_bytes() == originals[second]

    def test_workflow_runs_full_profile_gate_before_data_commit(self):
        workflow = Path(".github/workflows/sync-data.yml").read_text(encoding="utf-8")
        verify_at = workflow.index("Verify bundled asset liveness")
        commit_at = workflow.index("Commit & push data repo changes")
        assert verify_at < commit_at
        assert "steps.discovery.outputs.profile == 'full'" in workflow[verify_at:commit_at]
        assert "--apply" in workflow[verify_at:commit_at]
        assert "--max-decayed-percent 35" in workflow[verify_at:commit_at]
        assert "Upload bundled asset liveness report" in workflow


class TestGitHubClient:
    class Response:
        def __init__(self, payload):
            self.payload = payload

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self):
            return json.dumps(self.payload).encode()

        def close(self):
            return None

    def test_encodes_branch_and_parses_blob_tree(self, monkeypatch):
        requests = []
        payloads = iter(
            [
                {"name": "feature/assets", "commit": {"sha": "a" * 40}},
                {
                    "truncated": False,
                    "tree": [
                        {"path": "SKILL.md", "type": "blob", "mode": "100644"},
                        {"path": "linked.py", "type": "blob", "mode": "120000"},
                        {"path": "dir", "type": "tree", "mode": "040000"},
                    ],
                },
            ]
        )

        def fake_urlopen(request, timeout):
            requests.append((request, timeout))
            return self.Response(next(payloads))

        monkeypatch.setattr(liveness.urllib.request, "urlopen", fake_urlopen)
        client = liveness.GitHubClient("token")
        assert client.branch_sha("acme/tools", "feature/assets") == "a" * 40
        assert client.tree("acme/tools", "a" * 40) == {"SKILL.md"}
        assert "feature%2Fassets" in requests[0][0].full_url
        assert requests[0][0].get_header("Authorization") == "Bearer token"

    def test_http_and_malformed_tree_fail_explicitly(self, monkeypatch):
        def http_error(_request, timeout):
            assert timeout == 30
            raise urllib.error.HTTPError(
                "url", 404, "missing", {}, self.Response({"message": "missing"})
            )

        monkeypatch.setattr(liveness.urllib.request, "urlopen", http_error)
        with pytest.raises(liveness.GitHubApiError, match="404") as caught:
            liveness.GitHubClient().repository("acme/missing")
        assert caught.value.status == 404

        monkeypatch.setattr(
            liveness.urllib.request,
            "urlopen",
            lambda _request, timeout: self.Response({"truncated": True}),
        )
        with pytest.raises(liveness.GitHubApiError, match="truncated"):
            liveness.GitHubClient().tree("acme/tools", "a" * 40)

        monkeypatch.setattr(
            liveness.urllib.request,
            "urlopen",
            lambda _request, timeout: self.Response({"tree": []}),
        )
        with pytest.raises(liveness.GitHubApiError, match="truncated or malformed"):
            liveness.GitHubClient().tree("acme/tools", "a" * 40)
