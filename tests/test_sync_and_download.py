import importlib.util
import sys
from pathlib import Path

import pytest


def load_module():
    module_path = Path(__file__).resolve().parents[1] / "scripts" / "sync_and_download.py"
    spec = importlib.util.spec_from_file_location("sync_and_download_module", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_should_fail_on_empty_download_only_when_all_attempts_fail():
    module = load_module()

    assert module.should_fail_on_empty_download({"downloaded": 0, "failed": 3}) is True
    assert module.should_fail_on_empty_download({"downloaded": 2, "failed": 3}) is False
    assert module.should_fail_on_empty_download({"downloaded": 0, "failed": 0}) is False
    assert module.should_fail_on_empty_download({"downloaded": 0, "failed": 3, "skipped": 10}) is False


def test_manifest_round_trip(tmp_path):
    module = load_module()
    manifest_path = tmp_path / "acquisition_manifest.json"
    entries = {
        "development:demo-skill": {
            "repo": "acme/demo",
            "branch": "main",
            "relative_path": "skills/demo/SKILL.md",
            "updated_at": "2026-04-10T00:00:00Z",
        }
    }

    module.save_acquisition_manifest(manifest_path, entries)
    loaded = module.load_acquisition_manifest(manifest_path)
    assert loaded == entries


def test_manifest_loader_tolerates_legacy_and_invalid_entries(tmp_path):
    module = load_module()
    manifest_path = tmp_path / "acquisition_manifest.json"
    manifest_path.write_text(
        """
        {
          "legacy_key": {"repo": "acme/demo", "branch": "main", "relative_path": "SKILL.md"},
          "bad_key": {"repo": "acme/demo", "branch": "", "relative_path": ""},
          "bad_type": "oops"
        }
        """,
        encoding="utf-8",
    )

    loaded = module.load_acquisition_manifest(manifest_path)
    assert loaded == {
        "legacy_key": {
            "repo": "acme/demo",
            "branch": "main",
            "relative_path": "SKILL.md",
            "updated_at": "",
        }
    }


def test_probe_order_prefers_manifest_hints():
    module = load_module()
    manifest_entry = {"branch": "release", "relative_path": "custom/path/SKILL.md"}
    preferred = {"acme/demo": "main"}

    branch_order = module.build_branch_probe_order(
        "acme/demo", preferred, manifest_entry, ("main", "master")
    )
    path_order = module.build_relative_probe_order(
        ["skills/demo/SKILL.md", "SKILL.md"], manifest_entry
    )

    assert branch_order == ["release", "main", "master"]
    assert path_order == ["custom/path/SKILL.md", "skills/demo/SKILL.md", "SKILL.md"]


def test_probe_order_removes_duplicates():
    module = load_module()
    manifest_entry = {"branch": "main", "relative_path": "skills/demo/SKILL.md"}
    preferred = {"acme/demo": "main"}

    branch_order = module.build_branch_probe_order(
        "acme/demo", preferred, manifest_entry, ("main", "master")
    )
    path_order = module.build_relative_probe_order(
        ["skills/demo/SKILL.md", "SKILL.md", "SKILL.md"], manifest_entry
    )

    assert branch_order == ["main", "master"]
    assert path_order == ["skills/demo/SKILL.md", "SKILL.md"]


def test_select_shard_skills_is_deterministic():
    module = load_module()
    skills = [
        {"repo": "acme/repo1", "path": "skills/a", "name": "a", "category": "dev"},
        {"repo": "acme/repo2", "path": "skills/b", "name": "b", "category": "dev"},
        {"repo": "acme/repo3", "path": "skills/c", "name": "c", "category": "dev"},
        {"repo": "acme/repo4", "path": "skills/d", "name": "d", "category": "dev"},
    ]
    first = module.select_shard_skills(skills, shard_count=3, shard_index=1)
    second = module.select_shard_skills(skills, shard_count=3, shard_index=1)
    assert first == second


def test_select_shard_skills_partition_has_no_overlap():
    module = load_module()
    skills = [
        {"repo": f"acme/repo{i}", "path": f"skills/{i}", "name": f"s{i}", "category": "dev"}
        for i in range(15)
    ]
    shard_count = 4
    buckets = []
    for idx in range(shard_count):
        bucket = module.select_shard_skills(skills, shard_count=shard_count, shard_index=idx)
        keys = {module.skill_key(item) for item in bucket}
        buckets.append(keys)

    combined = set().union(*buckets)
    original = {module.skill_key(item) for item in skills}

    assert combined == original
    for i in range(shard_count):
        for j in range(i + 1, shard_count):
            assert buckets[i].isdisjoint(buckets[j])


def test_main_exits_when_fail_on_empty_download_is_enabled(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 0, "failed": 2, "skipped": 0, "total": 0}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    with pytest.raises(SystemExit) as exc:
        module.main()

    assert exc.value.code == 1


def test_main_allows_partial_success_with_fail_on_empty_download(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 1, "failed": 2, "total": 1}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    module.main()


def test_main_allows_existing_archive_when_all_pending_fail(monkeypatch):
    module = load_module()

    async def fake_download_skills(*args, **kwargs):
        return {"downloaded": 0, "failed": 2, "skipped": 100, "total": 100}

    monkeypatch.setattr(module, "download_skills", fake_download_skills)
    monkeypatch.setattr(
        sys,
        "argv",
        ["sync_and_download.py", "--download-only", "--fail-on-empty-download"],
    )

    module.main()
