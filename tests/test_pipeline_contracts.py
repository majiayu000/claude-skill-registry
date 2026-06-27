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
    assert "return await loadSearchIndexUrl(CONFIG.INDEX_URL)" in app_js
    assert "return await loadSearchIndexUrl(CONFIG.LEGACY_INDEX_URL)" in app_js
    assert "in highlighted index" in app_js


def test_readme_links_static_artifact_api_contract():
    readme = read_repo_file("README.md")

    assert "[docs/artifact-api-contract.md](docs/artifact-api-contract.md)" in readme


def test_static_artifact_api_contract_names_public_entrypoints():
    contract = read_repo_file("docs/artifact-api-contract.md")
    expected_paths = [
        "search-index-lite.json",
        "search-index.json",
        "search-index-manifest.json",
        "search-shards/part-000.json",
        "featured.json",
        "plugins.json",
        "stats.json",
        "quality-index.json",
        "quality-index-manifest.json",
        "quality-shards/part-000.json",
        "security-index.json",
        "security-index-manifest.json",
        "security-shards/part-000.json",
        "ranking-index.json",
        "ranking-index-manifest.json",
        "ranking-shards/part-000.json",
        "categories/index.json",
        "categories/<category>.json",
        "categories/<category>/manifest.json",
        "categories/<category>/part-000.json",
        "registry_summary.json",
        "registry.json",
        "registry-manifest.json",
        "registry-shards/00.json",
        "provenance/merge-source.json",
    ]

    for path in expected_paths:
        assert path in contract


def test_static_artifact_api_contract_covers_pointer_and_manifest_fields():
    contract = read_repo_file("docs/artifact-api-contract.md")
    expected_terms = [
        "deprecated_full_payload: true",
        "manifest",
        "replacement",
        "compat_since",
        "compat_until",
        "schema_version",
        "sha256",
        "gzip_path",
        "shards",
        "parts",
        "records",
        "skills",
    ]

    for term in expected_terms:
        assert term in contract


def test_pages_leaderboard_loads_full_data_before_ranking():
    app_js = read_repo_file("docs/js/app.js")
    render_js = read_repo_file("docs/js/app-render.js")

    assert "fullIndex: null" in app_js
    assert "async function loadFullSearchSkills()" in app_js
    assert "loadSearchIndexUrl(CONFIG.LEGACY_INDEX_URL)" in app_js
    assert "async function showLeaderboard" in render_js
    assert "await loadCategorySkills(categoryFilter)" in render_js
    assert "await loadFullSearchSkills()" in render_js


def test_publish_sync_runs_generated_size_guard_after_rebuild():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    rebuild_block = sync_script[sync_script.index('if [[ "$rebuild" -eq 1 ]]') :]

    security_pos = rebuild_block.index("scripts/security_scanner.py")
    rebuild_pos = rebuild_block.index("scripts/build_search_index.py")
    cleanup_pos = rebuild_block.index("rm -f \"$security_report_path\"")
    canonical_pos = rebuild_block.index("scripts/check_canonical_categories.py")
    guard_pos = rebuild_block.index("scripts/check_generated_file_sizes.py")
    category_guard_pos = rebuild_block.index("scripts/check_category_artifacts.py")

    assert category_guard_pos > guard_pos > canonical_pos > cleanup_pos > rebuild_pos > security_pos
    assert 'security_report_path="$(mktemp)"' in sync_script
    assert "--output \"$security_report_path\"" in sync_script
    assert "--security-report \"$security_report_path\"" in sync_script
    assert "--progress-interval 10000" in sync_script
    assert "--output \"$main_dir/docs/security-report.json\"" not in sync_script
    assert "--report-only" in rebuild_block[security_pos:rebuild_pos]
    assert "--allow-missing-security-evidence" not in sync_script
    assert "--include registry.json" in sync_script
    assert "--include registry-shards" in sync_script
    assert "--include docs" in sync_script
    assert "--categories-dir" in sync_script
    assert "--registry-shards" in sync_script


def test_publish_sync_has_observable_steps_and_cache_excludes():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")

    expected_steps = [
        "Sync core -> main (excluding skills and local caches)",
        "Sync data -> main/skills",
        "Rebuild registry shards and category indexes",
        "Build registry summary",
        "Generate required security evidence",
        "Build search and signal indexes",
        "Check published categories are canonical",
        "Check generated artifact sizes",
        "Check category artifacts",
        "Generate third-party notices (advisory full-archive metadata scan)",
    ]
    for label in expected_steps:
        assert f'run_step "{label}"' in sync_script

    for excluded in [
        ".ruff_cache",
        ".pytest_cache",
        "__pycache__",
        "*.pyc",
        "metadata-compliance-report.json",
        "THIRD_PARTY_NOTICES.generated.md",
    ]:
        assert f"--exclude '{excluded}'" in sync_script

    assert "::group::%s" in sync_script
    assert "elapsed=${elapsed}s" in sync_script
    assert "remove_local_artifacts_under()" in sync_script
    assert 'remove_local_artifacts_under "$main_dir"' in sync_script
    assert 'remove_local_artifacts_under "$main_dir/skills"' in sync_script
    assert "--delete-excluded" not in sync_script

    cleanup_block = sync_script[
        sync_script.index("remove_local_artifacts_under()") : sync_script.index(
            "sync_core_to_main()"
        )
    ]
    assert "-delete" not in cleanup_block
    assert "-exec rm -f {} +" in cleanup_block


def test_publish_sync_preserves_main_owned_routing_files():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    sync_block = sync_script[
        sync_script.index("sync_core_to_main()") : sync_script.index(
            "sync_data_to_main()"
        )
    ]

    assert "--exclude 'README.md'" in sync_block
    assert "--exclude '.github/ISSUE_TEMPLATE'" in sync_block
    assert "--exclude '.github/ISSUE_TEMPLATE/**'" in sync_block
    assert "--exclude '.github/PULL_REQUEST_TEMPLATE.md'" in sync_block
    assert "--delete-excluded" not in sync_block


def test_publish_sync_metadata_compliance_is_advisory_for_historical_notices():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    notices_block = sync_script[sync_script.index("Generate third-party notices") :]

    assert "scripts/check_metadata_compliance.py" in notices_block
    assert "--notices \"$main_dir/THIRD_PARTY_NOTICES.md\"" in notices_block
    assert "--report-only" in notices_block
    assert "--strict" not in notices_block


def test_build_index_generates_security_report_for_checked_out_data():
    workflow = read_repo_file(".github/workflows/build-index.yml")
    build_steps = workflow[workflow.index("Generate security report for checked-out data") :]

    security_pos = build_steps.index("scripts/security_scanner.py")
    build_pos = build_steps.index("scripts/build_search_index.py")

    assert security_pos < build_pos
    assert "--output \"$RUNNER_TEMP/security-report.json\"" in build_steps
    assert "--security-report \"$RUNNER_TEMP/security-report.json\"" in build_steps
    assert "--output docs/security-report.json" not in build_steps
    assert "unzip -o security-report.zip -d docs || true" not in build_steps
    assert "test -f \"$RUNNER_TEMP/security-report.json\"" in build_steps
    assert "--allow-missing-security-evidence" not in build_steps
    assert "'scripts/build_search_index.py'" in workflow
    assert "'scripts/search_sources.py'" in workflow
    assert "'scripts/security_scanner.py'" in workflow
    assert "'scripts/security_blocklist.py'" in workflow
    assert "'sources/security_blocklist.json'" in workflow
    assert "'schema/skill.schema.json'" in workflow


def test_build_index_runs_generated_size_guard_before_pages_upload():
    workflow = read_repo_file(".github/workflows/build-index.yml")

    guard_pos = workflow.index("scripts/check_generated_file_sizes.py")
    category_guard_pos = workflow.index("scripts/check_category_artifacts.py")
    canonical_pos = workflow.rindex("scripts/check_canonical_categories.py")
    upload_pos = workflow.index("actions/upload-pages-artifact")

    assert guard_pos < category_guard_pos < canonical_pos < upload_pos
    assert "--include docs" in workflow
    assert "--docs-dir docs" in workflow


def test_sync_data_runs_generated_size_guard_after_registry_rebuild():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    rebuild_pos = workflow.index("scripts/rebuild_registry.py")
    canonical_pos = workflow.index("scripts/check_canonical_categories.py --registry-shards")
    guard_pos = workflow.index("scripts/check_generated_file_sizes.py")
    commit_pos = workflow.index("Commit & push data repo changes")

    assert rebuild_pos < canonical_pos < guard_pos < commit_pos
    assert "--include registry.json" in workflow
    assert "--include registry-shards" in workflow
    assert "--include docs" in workflow


def test_sync_data_checks_sources_and_archive_categories():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    validate_pos = workflow.index("scripts/validate_sources.py --sources-dir sources")
    sync_pos = workflow.index("scripts/sync_and_download.py --sync-only")
    archive_gate_pos = workflow.index("scripts/check_canonical_categories.py --skills-dir skills")
    security_pos = workflow.index("Resolve security scope")

    assert validate_pos < sync_pos
    assert sync_pos < archive_gate_pos < security_pos


def test_sync_data_stages_registry_shard_artifacts():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    assert "git add registry.json registry_summary.json registry-manifest.json registry-shards/" in workflow


def test_sync_data_cleans_ci_archive_leftovers_before_discovery():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    cleanup_pos = workflow.index("Clean CI archive leftovers before discovery")
    discovery_pos = workflow.index("Discover new skills from GitHub")
    download_pos = workflow.index("Download skills from registry")

    assert cleanup_pos < discovery_pos < download_pos
    assert "--cleanup-ci-untracked-archive-files-only" in workflow
    assert workflow.count("--skip-ci-untracked-cleanup") == 2


def test_sync_data_discovery_writes_to_archive_root_not_other_category():
    workflow = read_repo_file(".github/workflows/sync-data.yml")

    assert "--output skills/other" not in workflow
    assert workflow.count("--output skills") == 2


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
    assert "scripts/check_taxonomy_governance.py" in workflow
    assert "--override-ini" not in workflow
    assert "scripts/**" in workflow
    assert "taxonomy/**" in workflow
    assert "crawler/**" in workflow
