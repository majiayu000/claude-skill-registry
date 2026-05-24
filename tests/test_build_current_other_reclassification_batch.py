from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("build_current_other_reclassification_batch")


def _write_skill(root: Path, rel: str, *, body: str | None = None) -> None:
    skill_dir = root / rel
    skill_dir.mkdir(parents=True)
    payload = {
        "name": Path(rel).name,
        "category": Path(rel).parts[0],
        "dir_name": Path(rel).name,
    }
    (skill_dir / "metadata.json").write_text(
        json.dumps(payload, indent=2),
        encoding="utf-8",
    )
    (skill_dir / "SKILL.md").write_text(
        body or f"---\nname: {Path(rel).name}\n---\n\nUse this skill.",
        encoding="utf-8",
    )


def test_builds_current_other_input_and_manifest(tmp_path):
    builder = _load_module()
    skills_dir = tmp_path / "skills"
    _write_skill(skills_dir, "other/alpha")
    _write_skill(skills_dir, "other/beta")
    _write_skill(skills_dir, "development/gamma")
    output_dir = tmp_path / "batch"

    manifest = builder.build_batch(
        skills_dir=skills_dir,
        output_dir=output_dir,
        batch_id="other-001",
        from_categories={"other"},
        limit=1,
        offset=1,
        content_chars=120,
    )

    rows = [
        json.loads(line)
        for line in (output_dir / "input.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    saved_manifest = json.loads((output_dir / "manifest.json").read_text(encoding="utf-8"))

    assert manifest["batch_id"] == "other-001"
    assert saved_manifest["summary"]["archive_category_counts"] == {
        "development": 1,
        "other": 2,
    }
    assert saved_manifest["summary"]["matching_category_skill_count"] == 2
    assert saved_manifest["summary"]["selected_input_count"] == 1
    assert rows[0]["path"] == "other/beta/SKILL.md"
    assert rows[0]["workset"] == "live_current_category"
    assert rows[0]["source_sha256"]
    assert rows[0]["metadata_sha256"]
    assert rows[0]["semantic_text_sha256"]
    commands = "\n".join(saved_manifest["commands"])
    assert "sample_category_classification_audit.py" in commands
    assert "build_residual_category_worksets.py" in commands
    assert "residual_worksets_report" in saved_manifest["artifacts"]
    assert "residual_worksets_dir" in saved_manifest["artifacts"]
