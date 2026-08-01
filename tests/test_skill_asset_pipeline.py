"""End-to-end coverage for the three skill-asset audit CLIs.

Network access is stubbed at the `gh` subprocess boundary so the census,
verification, and fetch stages run against real files in tmp_path.
"""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import audit_skill_assets
import fetch_curated_skills
import skill_asset_audit
import verify_upstream_assets


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


@pytest.fixture
def archive(tmp_path):
    root = tmp_path / "data"
    make_skill(
        root, "dev", "with-script",
        "Run scripts/setup.py first.",
        {"stars": 500, "repo": "acme/tools", "path": "skills/with-script/SKILL.md",
         "name": "with-script"},
    )
    make_skill(
        root, "dev", "with-docs",
        "See references/guide.md for details.",
        {"stars": 300, "repo": "acme/docs", "path": "skills/with-docs/SKILL.md",
         "name": "with-docs"},
    )
    make_skill(
        root, "dev", "plain",
        "Just prose, no local files.",
        {"stars": 900, "repo": "acme/plain", "path": "skills/plain/SKILL.md", "name": "plain"},
    )
    make_skill(
        root, "dev", "low-stars",
        "Run scripts/other.py first.",
        {"stars": 3, "repo": "acme/small", "path": "skills/low-stars/SKILL.md",
         "name": "low-stars"},
    )
    return root


class TestFetchRepoTree:
    def test_returns_blob_paths(self, monkeypatch):
        monkeypatch.setattr(
            skill_asset_audit.subprocess, "run",
            lambda *a, **k: FakeCompleted(stdout='["a/SKILL.md", "a/run.py"]'),
        )
        assert skill_asset_audit.fetch_repo_tree("acme/tools") == ["a/SKILL.md", "a/run.py"]

    def test_raises_on_gh_failure(self, monkeypatch):
        monkeypatch.setattr(
            skill_asset_audit.subprocess, "run",
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
        assert rows[0] == {"repo": "acme/tools", "dir": "skills/with-script",
                           "stars": 500, "name": "with-script"}

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


class TestAuditMain:
    def test_census_mode(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "census", str(archive)])
        audit_skill_assets.main()
        assert json.loads(capsys.readouterr().out)["total_skills"] == 4

    def test_targets_mode_with_threshold(self, archive, monkeypatch, capsys):
        monkeypatch.setattr(sys, "argv", ["audit", "targets", str(archive), "1"])
        audit_skill_assets.main()
        assert len(capsys.readouterr().out.splitlines()) == 2

    def test_bad_mode_exits(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["audit", "bogus", "/tmp"])
        with pytest.raises(SystemExit):
            audit_skill_assets.main()


class TestVerifyRepo:
    TREE = [
        "README.md",
        "skills/alpha/SKILL.md",
        "skills/alpha/run.py",
        "skills/beta/SKILL.md",
        "skills/beta/references/guide.md",
        "skills/gamma/SKILL.md",
    ]

    def _patch_tree(self, monkeypatch, tree=None):
        monkeypatch.setattr(
            verify_upstream_assets, "fetch_repo_tree", lambda repo: tree or self.TREE
        )

    def test_classifies_each_verdict(self, monkeypatch):
        self._patch_tree(monkeypatch)
        rows = verify_upstream_assets.verify_repo("acme/tools", [
            {"repo": "acme/tools", "dir": "skills/alpha", "name": "alpha"},
            {"repo": "acme/tools", "dir": "skills/beta", "name": "beta"},
            {"repo": "acme/tools", "dir": "skills/gamma", "name": "gamma"},
        ])
        assert [r["status"] for r in rows] == ["EXEC", "REF_ASSET", "BARE"]
        assert rows[0]["exec"] == 1

    def test_missing_dir_is_not_found(self, monkeypatch):
        self._patch_tree(monkeypatch)
        [row] = verify_upstream_assets.verify_repo(
            "acme/tools", [{"repo": "acme/tools", "dir": "skills/nope", "name": "nope"}]
        )
        assert row["status"] == "not_found"

    def test_root_level_skill_is_ambiguous(self, monkeypatch):
        """A repo whose SKILL.md sits at the root resolves to "", which cannot be
        distinguished from the whole repo, so its siblings must not be classified."""
        self._patch_tree(monkeypatch, ["SKILL.md", "run.py"])
        [row] = verify_upstream_assets.verify_repo(
            "acme/root", [{"repo": "acme/root", "dir": "", "name": ""}]
        )
        assert row["status"] == "root_ambiguous"

    def test_named_target_absent_from_root_repo_is_not_found(self, monkeypatch):
        self._patch_tree(monkeypatch, ["SKILL.md", "run.py"])
        [row] = verify_upstream_assets.verify_repo(
            "acme/root", [{"repo": "acme/root", "dir": "", "name": "root"}]
        )
        assert row["status"] == "not_found"

    def test_tree_failure_marks_every_target(self, monkeypatch):
        def boom(repo):
            raise RuntimeError("gh api tree failed: 404")

        monkeypatch.setattr(verify_upstream_assets, "fetch_repo_tree", boom)
        rows = verify_upstream_assets.verify_repo("acme/gone", [
            {"repo": "acme/gone", "dir": "a", "name": "a"},
            {"repo": "acme/gone", "dir": "b", "name": "b"},
        ])
        assert [r["status"] for r in rows] == ["repo_error", "repo_error"]
        assert "404" in rows[0]["error"]


class TestVerifyMain:
    def test_writes_rows_and_summary(self, tmp_path, monkeypatch, capsys):
        targets = tmp_path / "targets.jsonl"
        targets.write_text(
            json.dumps({"repo": "acme/tools", "dir": "skills/alpha", "name": "alpha"}) + "\n"
            + json.dumps({"repo": "acme/gone", "dir": "skills/x", "name": "x"}) + "\n",
            encoding="utf-8",
        )
        out = tmp_path / "verified.jsonl"

        def fake_tree(repo):
            if repo == "acme/gone":
                raise RuntimeError("404")
            return ["skills/alpha/SKILL.md", "skills/alpha/run.py"]

        monkeypatch.setattr(verify_upstream_assets, "fetch_repo_tree", fake_tree)
        monkeypatch.setattr(sys, "argv", ["verify", str(targets), str(out)])
        verify_upstream_assets.main()

        rows = [json.loads(line) for line in out.read_text().splitlines()]
        assert {r["status"] for r in rows} == {"EXEC", "repo_error"}
        summary = json.loads(capsys.readouterr().err)
        assert summary == {"EXEC": 1, "repo_error": 1}

    def test_wrong_arity_exits(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["verify", "only-one"])
        with pytest.raises(SystemExit):
            verify_upstream_assets.main()


class TestFetchFile:
    def test_writes_bytes(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            fetch_curated_skills.subprocess, "run",
            lambda *a, **k: FakeCompleted(stdout=b"print('hi')"),
        )
        local = tmp_path / "nested" / "run.py"
        fetch_curated_skills.fetch_file("acme/tools", "skills/a/run.py", str(local))
        assert local.read_bytes() == b"print('hi')"

    def test_raises_on_gh_failure(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            fetch_curated_skills.subprocess, "run",
            lambda *a, **k: FakeCompleted(returncode=1, stderr=b"Not Found"),
        )
        with pytest.raises(RuntimeError, match="Not Found"):
            fetch_curated_skills.fetch_file("acme/x", "p", str(tmp_path / "f"))


class TestFetchSkill:
    TARGET = {"repo": "acme/tools", "resolved_dir": "skills/alpha", "stars": 500,
              "status": "EXEC", "_tree": ["skills/alpha/SKILL.md", "skills/alpha/run.py"]}

    def test_fetches_files_and_writes_provenance(self, tmp_path, monkeypatch):
        monkeypatch.setattr(
            fetch_curated_skills, "fetch_file",
            lambda repo, path, local: (os.makedirs(os.path.dirname(local), exist_ok=True),
                                       open(local, "wb").write(b"x")),
        )
        row = fetch_curated_skills.fetch_skill("acme/tools", dict(self.TARGET), str(tmp_path))
        assert row["fetch"] == "ok"
        assert row["files_fetched"] == 2
        assert "_tree" not in row
        provenance = json.loads(
            (tmp_path / "acme__tools" / "alpha" / "_provenance.json").read_text()
        )
        assert provenance["source"].endswith("skills/alpha")
        assert provenance["errors"] == []

    def test_partial_fetch_records_errors(self, tmp_path, monkeypatch):
        def flaky(repo, path, local):
            if path.endswith("run.py"):
                raise RuntimeError("timeout")
            os.makedirs(os.path.dirname(local), exist_ok=True)
            open(local, "wb").write(b"x")

        monkeypatch.setattr(fetch_curated_skills, "fetch_file", flaky)
        row = fetch_curated_skills.fetch_skill("acme/tools", dict(self.TARGET), str(tmp_path))
        assert row["fetch"] == "partial"
        assert row["files_failed"] == 1

    def test_empty_upstream_dir_is_gone(self, tmp_path):
        target = {**self.TARGET, "_tree": ["other/file.md"]}
        row = fetch_curated_skills.fetch_skill("acme/tools", target, str(tmp_path))
        assert row["fetch"] == "gone"


class TestFetchMain:
    def test_skips_unverified_rows_and_writes_report(self, tmp_path, monkeypatch):
        verified = tmp_path / "verified.jsonl"
        verified.write_text("\n".join(json.dumps(r) for r in [
            {"repo": "acme/tools", "resolved_dir": "skills/alpha", "status": "EXEC"},
            {"repo": "acme/tools", "resolved_dir": "skills/beta", "status": "BARE"},
            {"repo": "acme/gone", "resolved_dir": "skills/x", "status": "REF_ASSET"},
        ]) + "\n", encoding="utf-8")
        report_path = tmp_path / "report.json"

        def fake_tree(repo):
            if repo == "acme/gone":
                raise RuntimeError("404")
            return ["skills/alpha/SKILL.md"]

        monkeypatch.setattr(fetch_curated_skills, "fetch_repo_tree", fake_tree)
        monkeypatch.setattr(
            fetch_curated_skills, "fetch_file",
            lambda repo, path, local: (os.makedirs(os.path.dirname(local), exist_ok=True),
                                       open(local, "wb").write(b"x")),
        )
        monkeypatch.setattr(
            sys, "argv", ["fetch", str(verified), str(tmp_path / "out"), str(report_path)]
        )
        fetch_curated_skills.main()

        report = json.loads(report_path.read_text())
        assert {r["fetch"] for r in report} == {"ok", "repo_error"}
        assert len(report) == 2

    def test_wrong_arity_exits(self, monkeypatch):
        monkeypatch.setattr(sys, "argv", ["fetch", "a", "b"])
        with pytest.raises(SystemExit):
            fetch_curated_skills.main()


def test_fetch_file_timeout_propagates(tmp_path, monkeypatch):
    def timeout(*args, **kwargs):
        raise subprocess.TimeoutExpired(cmd="gh", timeout=120)

    monkeypatch.setattr(fetch_curated_skills.subprocess, "run", timeout)
    with pytest.raises(subprocess.TimeoutExpired):
        fetch_curated_skills.fetch_file("acme/x", "p", str(tmp_path / "f"))
