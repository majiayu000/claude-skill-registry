from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path


def _load_module():
    scripts_dir = Path(__file__).resolve().parents[1] / "scripts"
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    return importlib.import_module("plan_stable_key_duplicate_cleanup")


def _write_skill(
    root: Path,
    rel: str,
    *,
    body: str,
    name: str = "duplicate",
    repo: str = "owner/repo",
    path: str = ".claude/skills/duplicate/SKILL.md",
    downloaded_at: str | None = "2026-01-01T00:00:00Z",
) -> None:
    skill_dir = root / rel
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    metadata = {
        "name": name,
        "repo": repo,
        "path": path,
        "category": Path(rel).parts[0],
        "dir_name": Path(rel).name,
    }
    if downloaded_at is not None:
        metadata["downloaded_at"] = downloaded_at
    (skill_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8",
    )


def _sha(path: Path) -> str:
    cleanup = _load_module()
    return cleanup.file_sha256(path)


def _detail(
    root: Path,
    *,
    source_path: str,
    target_path: str,
    skill_content_equal: bool = True,
    metadata_identity_equal: bool = True,
    target_exists: bool = True,
) -> dict:
    return {
        "source_path": source_path,
        "source_skill": f"{source_path}/SKILL.md",
        "target_path": target_path,
        "target_skill": f"{target_path}/SKILL.md",
        "target_exists": target_exists,
        "target_category": target_path.split("/", 1)[0],
        "target_status": "active",
        "classification_name": "duplicate",
        "confidence": 0.95,
        "key": "owner/repo:.claude/skills/duplicate/SKILL.md",
        "source_skill_sha256": _sha(root / source_path / "SKILL.md"),
        "target_skill_sha256": _sha(root / target_path / "SKILL.md")
        if target_exists
        else "",
        "metadata_identity_equal": metadata_identity_equal,
        "skill_content_equal": skill_content_equal,
    }


def _write_report(root: Path, report_path: Path, details: list[dict]) -> None:
    report_path.write_text(
        json.dumps(
            {
                "skills_dir": str(root),
                "details": {"stable_key_conflicts": details},
            },
            indent=2,
        ),
        encoding="utf-8",
    )


def test_plan_filters_to_exact_duplicates(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/exact", body="same")
    _write_skill(root, "development/exact", body="same")
    _write_skill(root, "other/content-drift", body="source")
    _write_skill(root, "development/content-drift", body="target")
    _write_skill(root, "other/meta-drift", body="same")
    _write_skill(root, "development/meta-drift", body="same")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(root, source_path="other/exact", target_path="development/exact"),
            _detail(
                root,
                source_path="other/content-drift",
                target_path="development/content-drift",
                skill_content_equal=False,
            ),
            _detail(
                root,
                source_path="other/meta-drift",
                target_path="development/meta-drift",
                metadata_identity_equal=False,
            ),
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        from_categories={"other"},
    )

    assert plan["summary"]["planned_remove_count"] == 1
    assert plan["removals"][0]["source_path"] == "other/exact"
    assert plan["summary"]["skipped_reasons"] == {
        "SKILL content differs": 1,
        "metadata identity differs": 1,
    }


def test_apply_removes_only_verified_duplicate(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/exact", body="same")
    _write_skill(root, "development/exact", body="same")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [_detail(root, source_path="other/exact", target_path="development/exact")],
    )
    plan = cleanup.build_cleanup_plan(residual_report=report_path)

    cleanup.apply_cleanup_plan(root, plan)

    assert not (root / "other" / "exact").exists()
    assert (root / "development" / "exact" / "SKILL.md").exists()


def test_apply_fails_closed_when_source_hash_changes(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/exact", body="same")
    _write_skill(root, "development/exact", body="same")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [_detail(root, source_path="other/exact", target_path="development/exact")],
    )
    plan = cleanup.build_cleanup_plan(residual_report=report_path)
    (root / "other" / "exact" / "SKILL.md").write_text("changed", encoding="utf-8")

    try:
        cleanup.apply_cleanup_plan(root, plan)
    except ValueError as exc:
        assert "source SKILL hash changed" in str(exc)
    else:
        raise AssertionError("expected stale cleanup plan to fail closed")

    assert (root / "other" / "exact" / "SKILL.md").exists()


def test_plan_can_allow_metadata_identity_drift_after_review(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/meta-drift", body="same")
    _write_skill(root, "development/meta-drift", body="same")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/meta-drift",
                target_path="development/meta-drift",
                metadata_identity_equal=False,
            )
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        require_metadata_identity=False,
    )

    assert plan["summary"]["planned_remove_count"] == 1


def test_plan_can_replace_target_with_newer_source_content_after_review(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(
        root,
        "other/content-drift",
        body="new source",
        downloaded_at="2026-01-03T00:00:00Z",
    )
    _write_skill(
        root,
        "development/content-drift",
        body="old target",
        downloaded_at="2026-01-02T00:00:00Z",
    )
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/content-drift",
                target_path="development/content-drift",
                skill_content_equal=False,
            )
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        content_drift_strategy=cleanup.CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
    )

    assert plan["summary"]["planned_remove_count"] == 1
    assert plan["removals"][0]["operation"] == "replace_target_remove_source"
    assert plan["removals"][0]["reason"] == "source downloaded_at is newer than target"

    cleanup.apply_cleanup_plan(root, plan)

    assert not (root / "other" / "content-drift").exists()
    assert (root / "development" / "content-drift" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "new source"
    metadata = json.loads(
        (root / "development" / "content-drift" / "metadata.json").read_text(
            encoding="utf-8"
        )
    )
    assert metadata["category"] == "development"
    assert metadata["dir_name"] == "content-drift"


def test_plan_removes_source_when_target_is_newer_after_review(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(
        root,
        "other/content-drift",
        body="old source",
        downloaded_at="2026-01-01T00:00:00Z",
    )
    _write_skill(
        root,
        "development/content-drift",
        body="new target",
        downloaded_at="2026-01-02T00:00:00Z",
    )
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/content-drift",
                target_path="development/content-drift",
                skill_content_equal=False,
            )
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        content_drift_strategy=cleanup.CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
    )

    assert plan["removals"][0]["operation"] == "remove_source_keep_target"
    cleanup.apply_cleanup_plan(root, plan)
    assert not (root / "other" / "content-drift").exists()
    assert (root / "development" / "content-drift" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "new target"


def test_content_drift_without_downloaded_at_fails_closed(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/content-drift", body="source", downloaded_at=None)
    _write_skill(root, "development/content-drift", body="target")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/content-drift",
                target_path="development/content-drift",
                skill_content_equal=False,
            )
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        content_drift_strategy=cleanup.CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
    )

    assert plan["summary"]["planned_remove_count"] == 0
    assert plan["summary"]["skipped_reasons"] == {
        "downloaded_at unavailable for content drift": 1
    }


def test_content_drift_can_keep_target_when_downloaded_at_is_missing_after_review(
    tmp_path,
):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(root, "other/content-drift", body="source", downloaded_at=None)
    _write_skill(root, "development/content-drift", body="target")
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/content-drift",
                target_path="development/content-drift",
                skill_content_equal=False,
            )
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        content_drift_strategy=cleanup.CONTENT_DRIFT_PREFER_NEWER_OR_KEEP_TARGET,
    )

    assert plan["summary"]["planned_remove_count"] == 1
    assert plan["removals"][0]["operation"] == "remove_source_keep_target"
    assert (
        plan["removals"][0]["reason"]
        == "target retained because downloaded_at is unavailable"
    )
    cleanup.apply_cleanup_plan(root, plan)
    assert not (root / "other" / "content-drift").exists()
    assert (root / "development" / "content-drift" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "target"


def test_only_newest_source_replaces_shared_target(tmp_path):
    cleanup = _load_module()
    root = tmp_path / "skills"
    _write_skill(
        root,
        "other/content-drift-newer",
        body="newer source",
        downloaded_at="2026-01-03T00:00:00Z",
    )
    _write_skill(
        root,
        "other/content-drift-newest",
        body="newest source",
        downloaded_at="2026-01-04T00:00:00Z",
    )
    _write_skill(
        root,
        "development/content-drift",
        body="old target",
        downloaded_at="2026-01-02T00:00:00Z",
    )
    report_path = tmp_path / "report.json"
    _write_report(
        root,
        report_path,
        [
            _detail(
                root,
                source_path="other/content-drift-newer",
                target_path="development/content-drift",
                skill_content_equal=False,
            ),
            _detail(
                root,
                source_path="other/content-drift-newest",
                target_path="development/content-drift",
                skill_content_equal=False,
            ),
        ],
    )

    plan = cleanup.build_cleanup_plan(
        residual_report=report_path,
        content_drift_strategy=cleanup.CONTENT_DRIFT_PREFER_NEWER_DOWNLOADED_AT,
    )

    assert [removal["operation"] for removal in plan["removals"]] == [
        "remove_source_keep_target",
        "replace_target_remove_source",
    ]
    cleanup.apply_cleanup_plan(root, plan)
    assert not (root / "other" / "content-drift-newer").exists()
    assert not (root / "other" / "content-drift-newest").exists()
    assert (root / "development" / "content-drift" / "SKILL.md").read_text(
        encoding="utf-8"
    ) == "newest source"
