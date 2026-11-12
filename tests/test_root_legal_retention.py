"""Regression tests for Apache-2.0 root LICENSE/NOTICE retention (#437).

Apache-2.0 archives must keep upstream LICENSE and NOTICE files when they
exist (keep-when-present, never fail-closed), record their provenance in
license_source_paths, and track the recorded upstream paths during liveness
checks. The fake-aiohttp harness is shared with test_sync_and_download and
the liveness helpers with test_skill_asset_audit.
"""

import asyncio
import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from test_skill_asset_audit import (  # noqa: E402
    FakeLivenessClient,
    liveness,
    make_verified_asset,
)
from test_sync_and_download import (  # noqa: E402
    FakeResponse,
    exact_repo_routes,
    git_blob_entry,
    git_blob_sha,
    install_fake_aiohttp,
    load_module,
)

REPO = "acme/apache-skill"
SOURCE_DIR = "skills/demo"
SOURCE_PATH = f"{SOURCE_DIR}/SKILL.md"
REFERENCE_PATH = f"{SOURCE_DIR}/references/guide.md"
SHA = "a" * 40
SKILL_BODY = (
    b"---\nname: demo\ndescription: Apache retention demo skill.\n---\n"
    b"# Demo\nRead references/guide.md.\n"
)
STANDALONE_BODY = (
    b"---\nname: demo\ndescription: Apache retention demo skill.\n---\n"
    b"# Demo\nStandalone instructions without support files.\n"
)
REFERENCE_BODY = b"# Guide\nKeep the upstream attribution.\n"
ROOT_LICENSE_BODY = b"Apache License\nVersion 2.0, January 2004\n"
ROOT_NOTICE_BODY = b"Demo skill\nCopyright 2026 Demo Authors\n"
LOCAL_LICENSE_BODY = b"Apache License\nVersion 2.0 (skill-directory copy)\n"
LOCAL_NOTICE_BODY = b"Demo skill\nCopyright 2026 Local Authors\n"


def apache_registry_row(**overrides) -> dict:
    row = {
        "name": "demo",
        "repo": REPO,
        "path": SOURCE_PATH,
        "category": "development",
        "description": "Apache retention demo skill.",
        "license": "Apache-2.0",
        "distribution": "compatible",
    }
    row.update(overrides)
    return row


def apache_routes(files: dict, *, pinned: bool, invalid_notice: bool = False) -> dict:
    """Build tree/raw or contents/raw routes for one Apache source revision."""
    ref = SHA if pinned else "main"
    tree = [git_blob_entry(path, body) for path, body in files.items()]
    if pinned and invalid_notice:
        next(entry for entry in tree if entry["path"] == "NOTICE")["mode"] = "120000"
    routes = exact_repo_routes(REPO, "main", SHA, tree) if pinned else {}
    raw_base = f"https://raw.githubusercontent.com/{REPO}/{ref}"
    for path, body in files.items():
        routes[f"{raw_base}/{path}"] = FakeResponse(200, body=body, text=body.decode())
    if not pinned:
        for directory in ("", SOURCE_DIR, f"{SOURCE_DIR}/references"):
            contents = [
                {
                    "type": (
                        "symlink"
                        if invalid_notice and path == "NOTICE"
                        else "file"
                    ),
                    "path": path,
                    "size": len(body),
                    "download_url": f"{raw_base}/{path}",
                }
                for path, body in files.items()
                if path.rpartition("/")[0] == directory
            ]
            if directory == SOURCE_DIR:
                contents.append({"type": "dir", "path": f"{SOURCE_DIR}/references"})
            suffix = f"/{directory}" if directory else ""
            routes[f"https://api.github.com/repos/{REPO}/contents{suffix}?ref=main"] = (
                FakeResponse(200, json_payload=contents)
            )
    return routes


def run_apache_download(tmp_path, monkeypatch, files: dict, *, pinned: bool,
                        invalid_notice: bool = False, row: dict | None = None):
    module = load_module()
    registry_path = tmp_path / "registry.json"
    output_dir = tmp_path / "skills"
    registry_path.write_text(
        json.dumps({"skills": [row or apache_registry_row()]}), encoding="utf-8"
    )
    install_fake_aiohttp(
        monkeypatch, apache_routes(files, pinned=pinned, invalid_notice=invalid_notice)
    )
    stats = asyncio.run(
        module.download_skills(
            registry_path,
            output_dir,
            manifest_path=None,
            cleanup_ci_untracked=False,
            pin_commit_sha=pinned,
        )
    )
    return stats, output_dir


@pytest.mark.parametrize("pinned", [False, True])
@pytest.mark.parametrize("legal_case", [
    "root_both", "notice_only", "no_legal_files", "local_license_root_notice",
    "local_notice", "invalid_root_notice", "unapproved_distribution",
])
def test_apache_archive_keeps_root_legal_when_present(tmp_path, monkeypatch, pinned, legal_case):
    files = {SOURCE_PATH: SKILL_BODY, REFERENCE_PATH: REFERENCE_BODY}
    expected_bundled = ["references/guide.md"]
    expected_provenance: dict = {}
    archived_legal: dict = {}
    row = apache_registry_row()
    invalid_notice = False
    if legal_case == "root_both":
        files.update({"LICENSE": ROOT_LICENSE_BODY, "NOTICE": ROOT_NOTICE_BODY})
        expected_bundled = ["LICENSE", "NOTICE", "references/guide.md"]
        expected_provenance = {"LICENSE": "LICENSE", "NOTICE": "NOTICE"}
        archived_legal = {"LICENSE": ROOT_LICENSE_BODY, "NOTICE": ROOT_NOTICE_BODY}
    elif legal_case == "notice_only":
        files["NOTICE"] = ROOT_NOTICE_BODY
        expected_bundled = ["NOTICE", "references/guide.md"]
        expected_provenance = {"NOTICE": "NOTICE"}
        archived_legal = {"NOTICE": ROOT_NOTICE_BODY}
    elif legal_case == "local_license_root_notice":
        files.update({
            f"{SOURCE_DIR}/LICENSE": LOCAL_LICENSE_BODY,
            "LICENSE": ROOT_LICENSE_BODY,
            "NOTICE": ROOT_NOTICE_BODY,
        })
        expected_bundled = ["LICENSE", "NOTICE", "references/guide.md"]
        expected_provenance = {"LICENSE": f"{SOURCE_DIR}/LICENSE", "NOTICE": "NOTICE"}
        archived_legal = {"LICENSE": LOCAL_LICENSE_BODY, "NOTICE": ROOT_NOTICE_BODY}
    elif legal_case == "local_notice":
        files.update({f"{SOURCE_DIR}/NOTICE": LOCAL_NOTICE_BODY, "NOTICE": ROOT_NOTICE_BODY})
        expected_bundled = ["NOTICE", "references/guide.md"]
        expected_provenance = {"NOTICE": f"{SOURCE_DIR}/NOTICE"}
        archived_legal = {"NOTICE": LOCAL_NOTICE_BODY}
    elif legal_case == "invalid_root_notice":
        files.update({"LICENSE": ROOT_LICENSE_BODY, "NOTICE": ROOT_NOTICE_BODY})
        invalid_notice = True
        expected_bundled = ["LICENSE", "references/guide.md"]
        expected_provenance = {"LICENSE": "LICENSE"}
        archived_legal = {"LICENSE": ROOT_LICENSE_BODY}
    elif legal_case == "unapproved_distribution":
        files.update({SOURCE_PATH: STANDALONE_BODY, "LICENSE": ROOT_LICENSE_BODY, "NOTICE": ROOT_NOTICE_BODY})
        expected_bundled = []
        row = apache_registry_row(distribution="restricted")

    stats, output_dir = run_apache_download(
        tmp_path, monkeypatch, files, pinned=pinned, invalid_notice=invalid_notice, row=row
    )

    # Keep-when-present: no legal-file state ever fails the acquisition.
    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    archive = next(output_dir.glob("development/*"))
    metadata = json.loads((archive / "metadata.json").read_text())
    assert metadata["license"] == "Apache-2.0"
    assert metadata["bundled_files"] == expected_bundled
    for name, body in archived_legal.items():
        assert (archive / name).read_bytes() == body
    if legal_case == "local_license_root_notice":
        assert (archive / "LICENSE").read_bytes() == LOCAL_LICENSE_BODY
    if legal_case in {"notice_only", "no_legal_files"}:
        assert not (archive / "LICENSE").exists()
    if legal_case in {"no_legal_files", "invalid_root_notice", "unapproved_distribution"}:
        assert not (archive / "NOTICE").exists()
    if expected_provenance:
        assert metadata["license_source_paths"] == expected_provenance
    else:
        assert "license_source_paths" not in metadata
    if legal_case == "unapproved_distribution":
        assert metadata["archive_mode"] == "skill-md"
        assert not (archive / "references").exists()
    if pinned and expected_bundled:
        assert metadata["github_commit_sha"] == SHA
        assert metadata["bundled_file_blobs"] == {
            name: git_blob_sha(files[expected_provenance.get(name, f"{SOURCE_DIR}/{name}")])
            for name in expected_bundled
        }
    elif pinned:
        assert metadata["github_commit_sha"] == SHA
        assert "bundled_file_blobs" not in metadata


@pytest.mark.parametrize("pinned", [False, True])
@pytest.mark.parametrize("notice_name", ["NOTICE", "NOTICE.md", "NOTICE.txt"])
def test_apache_root_notice_variants_are_retained(tmp_path, monkeypatch, pinned, notice_name):
    files = {
        SOURCE_PATH: SKILL_BODY,
        REFERENCE_PATH: REFERENCE_BODY,
        "LICENSE": ROOT_LICENSE_BODY,
        notice_name: ROOT_NOTICE_BODY,
    }
    stats, output_dir = run_apache_download(tmp_path, monkeypatch, files, pinned=pinned)
    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    archive = next(output_dir.glob("development/*"))
    assert (archive / notice_name).read_bytes() == ROOT_NOTICE_BODY
    assert (archive / "LICENSE").read_bytes() == ROOT_LICENSE_BODY
    metadata = json.loads((archive / "metadata.json").read_text())
    assert metadata["license_source_paths"] == {"LICENSE": "LICENSE", notice_name: notice_name}
    assert metadata["bundled_files"] == ["LICENSE", notice_name, "references/guide.md"]


@pytest.mark.parametrize("pinned", [False, True])
@pytest.mark.parametrize("local_name,root_name", [
    ("NOTICE.md", "NOTICE"), ("LICENSE.md", "LICENSE"),
])
def test_apache_local_legal_precedence_is_per_filename(
    tmp_path, monkeypatch, pinned, local_name, root_name
):
    # A differently named local legal file must not suppress the root file.
    local_body = LOCAL_NOTICE_BODY if local_name.startswith("NOTICE") else LOCAL_LICENSE_BODY
    root_body = ROOT_NOTICE_BODY if root_name == "NOTICE" else ROOT_LICENSE_BODY
    files = {
        SOURCE_PATH: SKILL_BODY,
        REFERENCE_PATH: REFERENCE_BODY,
        f"{SOURCE_DIR}/{local_name}": local_body,
        root_name: root_body,
    }
    stats, output_dir = run_apache_download(tmp_path, monkeypatch, files, pinned=pinned)
    assert stats["downloaded"] == 1
    assert stats["failed"] == 0
    archive = next(output_dir.glob("development/*"))
    assert (archive / local_name).read_bytes() == local_body
    assert (archive / root_name).read_bytes() == root_body
    metadata = json.loads((archive / "metadata.json").read_text())
    assert metadata["license_source_paths"][root_name] == root_name
    assert sorted(metadata["bundled_files"]) == sorted(
        [local_name, root_name, "references/guide.md"]
    )


@pytest.mark.parametrize("notice_name", ["NOTICE", "NOTICE.md", "NOTICE.txt"])
@pytest.mark.parametrize("upstream_has_root_notice", [True, False])
def test_apache_root_notice_liveness_uses_provenance(tmp_path, notice_name, upstream_has_root_notice):
    skills = tmp_path / "skills"
    metadata_path = make_verified_asset(
        skills, "alpha", bundled_files=[notice_name, "scripts/run.py"]
    )
    metadata = json.loads(metadata_path.read_text())
    metadata["license"] = "Apache-2.0"
    metadata["license_source_paths"] = {notice_name: notice_name}
    metadata_path.write_text(json.dumps(metadata))
    targets, errors = liveness.load_targets(skills)
    assert not errors
    # Upstream keeps a skill-directory namesake; only the root copy satisfies
    # the recorded provenance, so its absence must decay to partial.
    paths = {"skills/alpha/SKILL.md", "skills/alpha/scripts/run.py", f"skills/alpha/{notice_name}"}
    if upstream_has_root_notice:
        paths.add(notice_name)
    [row] = liveness.verify_targets(targets, FakeLivenessClient(paths), "now")
    if upstream_has_root_notice:
        assert row["status"] == "live"
        assert row["missing_assets"] == []
    else:
        assert row["status"] == "partial"
        assert row["missing_assets"] == [notice_name]


@pytest.mark.parametrize("upstream_legal", [{"LICENSE", "NOTICE"}, {"NOTICE"}, set()])
def test_apache_root_license_and_notice_liveness(tmp_path, upstream_legal):
    skills = tmp_path / "skills"
    metadata_path = make_verified_asset(
        skills, "alpha", bundled_files=["LICENSE", "NOTICE", "scripts/run.py"]
    )
    metadata = json.loads(metadata_path.read_text())
    metadata["license"] = "Apache-2.0"
    metadata["license_source_paths"] = {"LICENSE": "LICENSE", "NOTICE": "NOTICE"}
    metadata_path.write_text(json.dumps(metadata))
    targets, errors = liveness.load_targets(skills)
    assert not errors
    paths = {"skills/alpha/SKILL.md", "skills/alpha/scripts/run.py", *upstream_legal}
    [row] = liveness.verify_targets(targets, FakeLivenessClient(paths), "now")
    missing = sorted({"LICENSE", "NOTICE"} - upstream_legal)
    assert row["missing_assets"] == missing
    assert row["status"] == ("partial" if missing else "live")


def test_apache_legal_without_provenance_falls_back_to_skill_dir(tmp_path):
    skills = tmp_path / "skills"
    metadata_path = make_verified_asset(
        skills, "alpha", bundled_files=["LICENSE", "scripts/run.py"]
    )
    metadata = json.loads(metadata_path.read_text())
    metadata["license"] = "Apache-2.0"
    metadata_path.write_text(json.dumps(metadata))
    targets, errors = liveness.load_targets(skills)
    assert not errors
    paths = {"skills/alpha/SKILL.md", "skills/alpha/scripts/run.py", "skills/alpha/LICENSE"}
    [row] = liveness.verify_targets(targets, FakeLivenessClient(paths), "now")
    assert row["status"] == "live"
    assert row["missing_assets"] == []
