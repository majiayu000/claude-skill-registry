"""Regression tests for intake-reviewed commit pins (#436).

Community rows whose source_url cites a specific GitHub commit must be
archived at that reviewed commit rather than the probed branch head.
The fake-aiohttp harness is shared with test_sync_and_download.
"""

import asyncio
import importlib.util
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from test_sync_and_download import (  # noqa: E402
    FakeResponse,
    exact_repo_routes,
    git_blob_entry,
    git_blob_sha,
    install_fake_aiohttp,
    load_module,
)


def load_download_support_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    module_path = scripts_dir / "sync_download_support.py"
    spec = importlib.util.spec_from_file_location("sync_download_support_module", module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class RecordingRoutes(dict):
    """Route table that records every URL requested through the fake session."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requested_urls = []

    def get(self, url, default=None):
        self.requested_urls.append(url)
        return super().get(url, default)


REVIEWED_PIN_SHA = "62c6f18cd67e96a80985583ecb42324c2f74c355"


@pytest.mark.parametrize(
    ("skill", "repo", "expected"),
    [
        ({"source_url": f"https://github.com/acme/demo/blob/{REVIEWED_PIN_SHA}/skills/demo/SKILL.md"}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": f"https://github.com/acme/demo/tree/{REVIEWED_PIN_SHA}/skills/demo"}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": f"https://github.com/acme/demo/tree/{REVIEWED_PIN_SHA}"}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": f"https://github.com/acme/demo/blob/{REVIEWED_PIN_SHA.upper()}/SKILL.md"}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": f"https://github.com/ACME/Demo/blob/{REVIEWED_PIN_SHA}/SKILL.md"}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": f"https://github.com/acme/demo/blob/{REVIEWED_PIN_SHA}/SKILL.md"}, "ACME/DEMO", REVIEWED_PIN_SHA),
        ({"source_url": f"  https://github.com/acme/demo/blob/{REVIEWED_PIN_SHA}/SKILL.md  "}, "acme/demo", REVIEWED_PIN_SHA),
        ({"source_url": "https://github.com/acme/demo/blob/main/SKILL.md"}, "acme/demo", ""),
        ({"source_url": f"https://github.com/other/repo/blob/{REVIEWED_PIN_SHA}/SKILL.md"}, "acme/demo", ""),
        ({"source_url": f"https://gitlab.com/acme/demo/blob/{REVIEWED_PIN_SHA}/SKILL.md"}, "acme/demo", ""),
        ({"source_url": f"https://github.com/acme/demo/blob/{REVIEWED_PIN_SHA[:7]}/SKILL.md"}, "acme/demo", ""),
        ({"source_url": f"https://github.com/acme/demo/commit/{REVIEWED_PIN_SHA}"}, "acme/demo", ""),
        ({"source_url": ""}, "acme/demo", ""),
        ({"source_url": None}, "acme/demo", ""),
        ({}, "acme/demo", ""),
    ],
)
def test_reviewed_pin_helper_parses_github_commit_urls(skill, repo, expected):
    support = load_download_support_module()
    assert support.reviewed_commit_pin(skill, repo) == expected


def reviewed_pin_registry_row(repo, skill_path, source_url):
    return {
        "name": "demo",
        "repo": repo,
        "path": skill_path,
        "category": "development",
        "description": "A reviewed demo skill.",
        "source_url": source_url,
        "license": "MIT",
        "distribution": "compatible",
    }


def test_reviewed_pin_archives_reviewed_commit_after_upstream_moves(tmp_path, monkeypatch):
    module = load_module()
    repo = "acme/demo"
    reviewed_sha = REVIEWED_PIN_SHA
    moved_head_sha = "b" * 40
    skill_path = "skills/demo/SKILL.md"
    source_url = f"https://github.com/{repo}/blob/{reviewed_sha}/{skill_path}"
    skill_body = (
        b"---\nname: demo\ndescription: A reviewed demo skill.\n---\n"
        b"# Demo\nReviewed revision; run scripts/setup.py.\n"
    )
    script_body = b"print('reviewed')\n"
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    registry_path.write_text(
        json.dumps({"skills": [reviewed_pin_registry_row(repo, skill_path, source_url)]}),
        encoding="utf-8",
    )
    # Upstream main has moved past the reviewed commit; only the reviewed
    # commit's tree and raw routes exist, so archiving the head cannot succeed.
    routes = RecordingRoutes({
        f"https://api.github.com/repos/{repo}": FakeResponse(200, json_payload={"full_name": repo}),
        f"https://api.github.com/repos/{repo}/branches/main": FakeResponse(
            200, json_payload={"name": "main", "commit": {"sha": moved_head_sha}}
        ),
        f"https://api.github.com/repos/{repo}/commits/{reviewed_sha}": FakeResponse(
            200, json_payload={"sha": reviewed_sha}
        ),
        f"https://api.github.com/repos/{repo}/git/trees/{reviewed_sha}?recursive=1": FakeResponse(
            200,
            json_payload={
                "truncated": False,
                "tree": [
                    git_blob_entry(skill_path, skill_body),
                    git_blob_entry("skills/demo/scripts/setup.py", script_body),
                ],
            },
        ),
        f"https://raw.githubusercontent.com/{repo}/{reviewed_sha}/{skill_path}": FakeResponse(
            200, body=skill_body
        ),
        f"https://raw.githubusercontent.com/{repo}/{reviewed_sha}/skills/demo/scripts/setup.py": (
            FakeResponse(200, body=script_body)
        ),
    })
    install_fake_aiohttp(monkeypatch, routes)

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=None,
            cleanup_ci_untracked=False,
            pin_commit_sha=True,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    assert (skill_dir / "SKILL.md").read_bytes() == skill_body
    assert (skill_dir / "scripts/setup.py").read_bytes() == script_body
    metadata = json.loads((skill_dir / "metadata.json").read_text())
    assert metadata["github_commit_sha"] == reviewed_sha
    assert metadata["github_branch"] == "main"
    assert metadata["source_url"] == source_url
    assert metadata["bundled_file_blobs"] == {"scripts/setup.py": git_blob_sha(script_body)}
    assert (
        f"https://raw.githubusercontent.com/{repo}/{reviewed_sha}/{skill_path}"
        in routes.requested_urls
    )
    assert (
        f"https://api.github.com/repos/{repo}/git/trees/{reviewed_sha}?recursive=1"
        in routes.requested_urls
    )
    assert not any(moved_head_sha in url for url in routes.requested_urls)


def test_reviewed_pin_fails_closed_when_commit_gone(tmp_path, monkeypatch):
    module = load_module()
    repo = "acme/demo"
    reviewed_sha = REVIEWED_PIN_SHA
    skill_path = "skills/demo/SKILL.md"
    source_url = f"https://github.com/{repo}/blob/{reviewed_sha}/{skill_path}"
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    failure_report_path = tmp_path / "failure_report.json"
    registry_path.write_text(
        json.dumps({"skills": [reviewed_pin_registry_row(repo, skill_path, source_url)]}),
        encoding="utf-8",
    )
    routes = RecordingRoutes({
        f"https://api.github.com/repos/{repo}": FakeResponse(200, json_payload={"full_name": repo}),
        f"https://api.github.com/repos/{repo}/branches/main": FakeResponse(
            200, json_payload={"name": "main", "commit": {"sha": "b" * 40}}
        ),
        f"https://api.github.com/repos/{repo}/commits/{reviewed_sha}": FakeResponse(404),
    })
    install_fake_aiohttp(monkeypatch, routes)

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            failure_report_path=failure_report_path,
            manifest_path=None,
            cleanup_ci_untracked=False,
            pin_commit_sha=True,
        )
    )

    assert stats["downloaded"] == 0
    assert stats["failed"] == 1
    assert not list(output_dir.rglob("SKILL.md"))
    assert not list(output_dir.rglob("metadata.json"))
    failure_report = json.loads(failure_report_path.read_text(encoding="utf-8"))
    assert failure_report["failure_reasons"]["commit_resolution_failed"] == 1
    assert not any(url.startswith("https://raw.githubusercontent.com/") for url in routes.requested_urls)


@pytest.mark.parametrize("source_url_kind", ["branch_url", "foreign_repo", "missing"])
def test_reviewed_pin_absent_for_branch_or_foreign_repo_urls(tmp_path, monkeypatch, source_url_kind):
    module = load_module()
    repo = "acme/demo"
    head_sha = "b" * 40
    skill_path = "skills/demo/SKILL.md"
    source_url = {
        "branch_url": f"https://github.com/{repo}/blob/main/{skill_path}",
        "foreign_repo": f"https://github.com/other/repo/blob/{REVIEWED_PIN_SHA}/{skill_path}",
        "missing": "",
    }[source_url_kind]
    skill_body = (
        b"---\nname: demo\ndescription: A reviewed demo skill.\n---\n"
        b"# Demo\nCurrent branch head; run scripts/setup.py.\n"
    )
    script_body = b"print('head')\n"
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    registry_path.write_text(
        json.dumps({"skills": [reviewed_pin_registry_row(repo, skill_path, source_url)]}),
        encoding="utf-8",
    )
    routes = RecordingRoutes({
        **exact_repo_routes(
            repo,
            "main",
            head_sha,
            [
                git_blob_entry(skill_path, skill_body),
                git_blob_entry("skills/demo/scripts/setup.py", script_body),
            ],
        ),
        f"https://raw.githubusercontent.com/{repo}/{head_sha}/{skill_path}": FakeResponse(
            200, body=skill_body
        ),
        f"https://raw.githubusercontent.com/{repo}/{head_sha}/skills/demo/scripts/setup.py": (
            FakeResponse(200, body=script_body)
        ),
    })
    install_fake_aiohttp(monkeypatch, routes)

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=None,
            cleanup_ci_untracked=False,
            pin_commit_sha=True,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    assert (skill_dir / "SKILL.md").read_bytes() == skill_body
    metadata = json.loads((skill_dir / "metadata.json").read_text())
    assert metadata["github_commit_sha"] == head_sha
    assert metadata["github_branch"] == "main"
    assert not any("/commits/" in url for url in routes.requested_urls)
    assert not any(REVIEWED_PIN_SHA in url for url in routes.requested_urls)


def test_reviewed_pin_ignored_in_exact_mode(tmp_path, monkeypatch):
    module = load_module()
    repo = "acme/demo"
    head_sha = "b" * 40
    skill_path = "skills/demo/SKILL.md"
    source_url = f"https://github.com/{repo}/blob/{REVIEWED_PIN_SHA}/{skill_path}"
    skill_body = (
        b"---\nname: demo\ndescription: A reviewed demo skill.\n---\n"
        b"# Demo\nBackfilled branch head; run scripts/setup.py.\n"
    )
    script_body = b"print('backfill')\n"
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    row = reviewed_pin_registry_row(repo, skill_path, source_url)
    row["github_branch"] = "main"
    registry_path.write_text(json.dumps({"skills": [row]}), encoding="utf-8")
    # Exact/backfill mode keeps its recorded-branch semantics: only the branch
    # head's tree and raw routes exist, and the reviewed pin is never resolved.
    routes = RecordingRoutes({
        **exact_repo_routes(
            repo,
            "main",
            head_sha,
            [
                git_blob_entry(skill_path, skill_body),
                git_blob_entry("skills/demo/scripts/setup.py", script_body),
            ],
        ),
        f"https://raw.githubusercontent.com/{repo}/{head_sha}/{skill_path}": FakeResponse(
            200, body=skill_body
        ),
        f"https://raw.githubusercontent.com/{repo}/{head_sha}/skills/demo/scripts/setup.py": (
            FakeResponse(200, body=script_body)
        ),
    })
    install_fake_aiohttp(monkeypatch, routes)

    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=None,
            cleanup_ci_untracked=False,
            exact_paths_only=True,
            pin_commit_sha=True,
        )
    )

    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    skill_dir = next(output_dir.glob("development/*"))
    assert (skill_dir / "SKILL.md").read_bytes() == skill_body
    metadata = json.loads((skill_dir / "metadata.json").read_text())
    assert metadata["github_commit_sha"] == head_sha
    assert metadata["github_branch"] == "main"
    assert not any("/commits/" in url for url in routes.requested_urls)
    assert not any(REVIEWED_PIN_SHA in url for url in routes.requested_urls)
