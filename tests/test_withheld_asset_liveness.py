"""License withholding removes obsolete bundle evidence, not verifier safeguards."""

import json
import sys
from pathlib import Path

import pytest
from test_skill_asset_audit import FakeLivenessClient, make_verified_asset

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import verify_upstream_assets as liveness  # noqa: E402
import withheld_archives  # noqa: E402

LIVENESS = {
    "asset_liveness": "live",
    "assets_liveness_checked_at": "2026-11-12T09:58:40Z",
    "assets_liveness_sha": "b" * 40,
}


def update_metadata(path, **changes):
    metadata = json.loads(path.read_text())
    metadata.update(changes)
    path.write_text(json.dumps(metadata))
    return metadata


@pytest.mark.parametrize("existing_body", [True, False])
@pytest.mark.parametrize("license_name", ["NOASSERTION", "Proprietary", "CC-BY-NC-4.0"])
def test_withholding_clears_liveness_for_new_and_existing_listings(tmp_path, existing_body, license_name):
    skills = tmp_path / "skills"
    healthy = make_verified_asset(skills, "healthy")
    update_metadata(healthy, license="MIT")
    metadata_path = make_verified_asset(skills, "withheld")
    original = update_metadata(
        metadata_path, license=license_name, distribution="restricted",
        content_fingerprint="c" * 64, description="Preserved description", **LIVENESS,
    )
    if not existing_body:
        (metadata_path.parent / "SKILL.md").unlink()
        (metadata_path.parent / "scripts/run.py").unlink()
        (metadata_path.parent / "scripts").rmdir()
        original = update_metadata(metadata_path, archive_mode="skill-md", bundled_files=[])
        original.pop("bundled_file_blobs")
        metadata_path.write_text(json.dumps(original))

    before = metadata_path.read_bytes()
    assert withheld_archives.main(["--skills-dir", str(skills)]) == 0
    assert metadata_path.read_bytes() == before
    assert withheld_archives.main(["--skills-dir", str(skills), "--check"]) == 1
    assert withheld_archives.main(["--skills-dir", str(skills), "--apply"]) == 0
    assert withheld_archives.main(["--skills-dir", str(skills), "--check"]) == 0

    updated = json.loads(metadata_path.read_text())
    assert not set(LIVENESS) & updated.keys()
    assert updated["license"] == license_name
    assert updated["repo"] == original["repo"]
    assert updated["github_commit_sha"] == original["github_commit_sha"]
    assert updated["description"] == original["description"]
    if not existing_body:
        assert updated["content_fingerprint"] == original["content_fingerprint"]
    assert sorted(p.name for p in metadata_path.parent.iterdir()) == ["metadata.json"]
    assert (healthy.parent / "SKILL.md").is_file()

    after = metadata_path.read_bytes()
    assert withheld_archives.main(["--skills-dir", str(skills), "--apply"]) == 0
    assert metadata_path.read_bytes() == after
    client = FakeLivenessClient({"skills/healthy/SKILL.md", "skills/healthy/scripts/run.py"})
    report = tmp_path / "report.json"
    assert liveness.main(["--skills-dir", str(skills), "--report", str(report)], client=client) == 0
    assert json.loads(report.read_text())["summary"] == {"live": 1}


@pytest.mark.parametrize("damage", ["missing_body", "empty_bundle", "modified_asset"])
def test_withholding_preserves_corrupt_open_source_bundle_errors(tmp_path, damage):
    skills = tmp_path / "skills"
    path = make_verified_asset(skills, "damaged")
    update_metadata(path, license="MIT", **LIVENESS)
    if damage == "missing_body":
        (path.parent / "SKILL.md").unlink()
    elif damage == "empty_bundle":
        (path.parent / "scripts/run.py").unlink()
    else:
        (path.parent / "scripts/run.py").write_text("tampered")
    before = path.read_bytes()
    assert withheld_archives.main(["--skills-dir", str(skills), "--apply"]) == 0
    assert path.read_bytes() == before
    targets, errors = liveness.load_targets(skills)
    assert not targets
    assert len(errors) == 1 and errors[0]["status"] == "local_error"


def test_metadata_only_cleanup_has_distinct_report_count(tmp_path):
    skills = tmp_path / "skills"
    directory = skills / "development" / "listed"
    directory.mkdir(parents=True)
    (directory / "metadata.json").write_text(json.dumps({
        "repo": "RS42-AI/scout-ai-lite", "path": "SKILL.md", "license": "NOASSERTION",
        "archive_mode": "skill-md", "bundled_files": [], **LIVENESS,
    }))
    report = tmp_path / "withheld.json"
    assert withheld_archives.main([
        "--skills-dir", str(skills), "--apply", "--report", str(report),
    ]) == 0
    summary = json.loads(report.read_text())
    assert summary["withheld_with_content"] == 0
    assert summary["withheld_metadata_needing_cleanup"] == 1

    assert summary["metadata_cleanup_examples"] == ["development/listed"]
