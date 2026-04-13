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
