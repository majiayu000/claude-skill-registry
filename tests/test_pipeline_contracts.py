from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_pages_app_prefers_lite_index_with_full_index_fallback():
    app_js = read_repo_file("docs/js/app.js")

    assert "INDEX_URL: 'search-index-lite.json'" in app_js
    assert "LEGACY_INDEX_URL: 'search-index.json'" in app_js
    assert "function normalizeSearchIndex" in app_js
    assert "function loadSearchIndex" in app_js
    assert "in highlighted index" in app_js


def test_publish_sync_runs_generated_size_guard_after_rebuild():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")

    rebuild_pos = sync_script.index("scripts/build_search_index.py")
    guard_pos = sync_script.index("scripts/check_generated_file_sizes.py")

    assert guard_pos > rebuild_pos
    assert "--include registry.json" in sync_script
    assert "--include registry-shards" in sync_script
    assert "--include docs" in sync_script


def test_build_index_fails_closed_when_security_report_is_missing():
    workflow = read_repo_file(".github/workflows/build-index.yml")

    assert "allow_missing_security_report" in workflow
    assert "core.setFailed(message)" in workflow
    assert "security-report-missing.allowed" in workflow
    assert "unzip -o security-report.zip -d docs || true" not in workflow
    assert "test -f docs/security-report.json" in workflow


def test_build_index_runs_generated_size_guard_before_pages_upload():
    workflow = read_repo_file(".github/workflows/build-index.yml")

    guard_pos = workflow.index("scripts/check_generated_file_sizes.py")
    upload_pos = workflow.index("actions/upload-pages-artifact")

    assert guard_pos < upload_pos
    assert "--include docs" in workflow


def test_sync_data_runs_generated_size_guard_after_registry_rebuild():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    rebuild_pos = workflow.index("scripts/rebuild_registry.py")
    guard_pos = workflow.index("scripts/check_generated_file_sizes.py")
    commit_pos = workflow.index("Commit & push data repo changes")

    assert rebuild_pos < guard_pos < commit_pos
    assert "--include registry.json" in workflow
    assert "--include registry-shards" in workflow
    assert "--include docs" in workflow


def test_metadata_compliance_refuses_unexpected_zero_target_scan():
    workflow = read_repo_file(".github/workflows/metadata-compliance.yml")

    assert "allow_missing_data_repo" in workflow
    assert "metadata-advisory-zero-targets" in workflow
    assert "refusing to run metadata compliance with zero targets" in workflow
    assert "exit 1" in workflow


def test_python_tests_workflow_runs_full_suite_with_coverage_gate():
    workflow = read_repo_file(".github/workflows/python-tests.yml")

    assert "name: Python Test Health" in workflow
    assert "python -m pytest -q --cov-fail-under=50" in workflow
    assert "--override-ini" not in workflow
    assert "scripts/**" in workflow
    assert "crawler/**" in workflow
