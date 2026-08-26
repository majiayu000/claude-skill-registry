import gzip
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def build_index_workflow_step(name: str) -> dict:
    workflow = yaml.safe_load(read_repo_file(".github/workflows/build-index.yml"))
    return next(
        step for step in workflow["jobs"]["build-index"]["steps"] if step.get("name") == name
    )


def write_fake_security_scanner(sandbox: Path) -> None:
    script_path = sandbox / "scripts" / "security_scanner.py"
    script_path.parent.mkdir(parents=True)
    script_path.write_text(
        """import json
import os
import sys
from pathlib import Path

mode = os.environ["FAKE_SCANNER_MODE"]
output_path = Path(sys.argv[sys.argv.index("--output") + 1])
if mode == "missing":
    raise SystemExit(0)
if mode == "invalid":
    output_path.write_text("not-json", encoding="utf-8")
    raise SystemExit(0)

sentinel = os.environ["SENTINEL_SECRET_MARKER"]
failed = mode in {"scanner_nonzero", "failed_exit_zero"}
require_metadata = mode != "metadata_disabled"
skill = {
    "path": "development/private-source/SKILL.md",
    "safe": not failed,
    "security_decision": {
        "status": "failed" if failed or mode == "decision_mismatch" else "passed",
        "policy": {"require_metadata": require_metadata},
    },
    "issues": ([{
        "severity": "error",
        "type": "hardcoded_credential",
        "message": f"credential marker: {sentinel}",
        "code": f"Authorization: Bearer {sentinel}",
        "file": f"/private/archive/{sentinel}/SKILL.md",
    }] if failed else []),
}
if mode == "missing_decision":
    skill.pop("security_decision")
report = {
    "scanner": {
        "name": "claude-skill-registry-security-scanner",
        "version": "1.1.2",
        "ruleset_sha256": "a" * 64,
    },
    "scan_policy": {"require_metadata": require_metadata},
    "total": 2 if mode == "count_mismatch" else 1,
    "passed": 0 if failed else 1,
    "failed": 1 if failed else 0,
    "skills": [skill],
}
output_path.write_text(json.dumps(report), encoding="utf-8")
raise SystemExit(1 if mode == "scanner_nonzero" else 0)
""",
        encoding="utf-8",
    )


def run_security_generation(tmp_path: Path, mode: str) -> dict:
    sandbox = tmp_path / mode
    sandbox.mkdir()
    write_fake_security_scanner(sandbox)
    (sandbox / "skills").mkdir()
    report_path = sandbox / "security-report.json"
    evidence_path = sandbox / "security-evidence.json"
    output_path = sandbox / "github-output.txt"
    summary_path = sandbox / "github-summary.md"
    output_path.touch()
    summary_path.touch()
    env = {
        **os.environ,
        "FAKE_SCANNER_MODE": mode,
        "SENTINEL_SECRET_MARKER": "SENTINEL_DO_NOT_UPLOAD_12345",
        "SECURITY_REPORT": str(report_path),
        "SECURITY_EVIDENCE": str(evidence_path),
        "GITHUB_OUTPUT": str(output_path),
        "GITHUB_STEP_SUMMARY": str(summary_path),
    }
    result = subprocess.run(
        ["bash", "-c", "set -euo pipefail\n" + build_index_workflow_step(
            "Generate security report for checked-out data"
        )["run"]],
        cwd=sandbox,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )
    outputs = {}
    for line in output_path.read_text(encoding="utf-8").splitlines():
        key, value = line.split("=", 1)
        outputs[key] = value
    return {
        "result": result,
        "env": env,
        "outputs": outputs,
        "report": report_path,
        "evidence": evidence_path,
        "archive": Path(f"{evidence_path}.gz"),
        "summary": summary_path,
    }


def run_security_enforcement(generation: dict, upload_outcome: str = "success"):
    outputs = generation["outputs"]
    env = {
        **generation["env"],
        "SCAN_EXIT": outputs.get("exit_code", ""),
        "REPORT_PRESENT": outputs.get("report_present", ""),
        "REPORT_VALID": outputs.get("report_valid", ""),
        "EVIDENCE_PRESENT": outputs.get("evidence_present", ""),
        "EVIDENCE_ARCHIVE_PRESENT": outputs.get("evidence_archive_present", ""),
        "FAILED_COUNT": outputs.get("failed_count", ""),
        "EVIDENCE_UPLOAD_OUTCOME": upload_outcome,
    }
    return subprocess.run(
        ["bash", "-c", "set -euo pipefail\n" + build_index_workflow_step(
            "Enforce archive security scan"
        )["run"]],
        cwd=generation["report"].parent,
        env=env,
        check=False,
        capture_output=True,
        text=True,
    )


def read_workflow(path: str) -> dict:
    return yaml.safe_load(read_repo_file(path))


def workflow_step(job_name: str, step_name: str) -> dict:
    workflow = read_workflow(".github/workflows/sync-data.yml")
    return next(step for step in workflow["jobs"][job_name]["steps"] if step["name"] == step_name)


def install_fake_curl(tmp_path: Path) -> Path:
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(exist_ok=True)
    fake_curl = bin_dir / "curl"
    fake_curl.write_text(
        """#!/usr/bin/env python3
import json
import os
from pathlib import Path
import sys

mode = os.environ.get("FAKE_CURL_MODE", "repo")
if mode == "fail":
    raise SystemExit(22)
if mode == "mark":
    Path(os.environ["FAKE_CURL_MARKER"]).write_text("called", encoding="utf-8")
    raise SystemExit(0)

args = sys.argv[1:]
output = args[args.index("--output") + 1]
url = next(arg for arg in args if arg.startswith("https://api.github.com/repos/"))
repo = url.split("/repos/", 1)[1]
response = {
    "full_name": repo,
    "default_branch": os.environ.get("FAKE_DEFAULT_BRANCH", "main"),
    "permissions": {"push": os.environ.get("FAKE_PUSH", "true") == "true"},
}
Path(output).write_text(json.dumps(response), encoding="utf-8")
""",
        encoding="utf-8",
    )
    fake_curl.chmod(0o755)
    return bin_dir


def run_workflow_script(
    step: dict,
    tmp_path: Path,
    env: dict[str, str] | None = None,
    fake_curl: bool = False,
) -> subprocess.CompletedProcess[str]:
    runtime_env = os.environ.copy()
    runtime_env.update(
        {
            "RUNNER_TEMP": str(tmp_path / "runner-temp"),
            "GITHUB_OUTPUT": str(tmp_path / "github-output"),
            "GITHUB_STEP_SUMMARY": str(tmp_path / "github-summary"),
        }
    )
    (tmp_path / "runner-temp").mkdir(exist_ok=True)
    if env:
        runtime_env.update(env)
    if fake_curl:
        bin_dir = install_fake_curl(tmp_path)
        runtime_env["PATH"] = f"{bin_dir}:{runtime_env['PATH']}"
    return subprocess.run(
        ["bash", "-c", step["run"]],
        cwd=tmp_path,
        env=runtime_env,
        text=True,
        capture_output=True,
        check=False,
    )


def valid_sync_env() -> dict[str, str]:
    return {
        "CORE_REPO": "Owner/Core",
        "REGISTRY_DATA_REPO": "Owner/Data",
        "DATA_REPO_TOKEN": "data-test-token",
        "REGISTRY_MAIN_REPO": "Owner/Main",
        "MAIN_REPO_TOKEN": "main-test-token",
    }


def build_valid_handoff(tmp_path: Path) -> tuple[Path, bytes, dict]:
    step = workflow_step("sync", "Build immutable publish handoff")
    env = {
        "RUN_ID": "1234",
        "CORE_REPO": "Owner/Core",
        "CORE_SHA": "a" * 40,
        "DATA_REPO": "Owner/Data",
        "DATA_SHA": "b" * 40,
        "REGISTRY_MAIN_REPO": "Owner/Main",
    }
    result = run_workflow_script(step, tmp_path, env)
    assert result.returncode == 0, result.stderr
    root = tmp_path / "sync-publish-handoff"
    payload_bytes = (root / "publish-dispatch-payload.json").read_bytes()
    evidence = json.loads((root / "publish-dispatch-evidence.json").read_text())
    return root, payload_bytes, evidence


def test_pages_app_keeps_full_index_behind_explicit_action():
    app_js = read_repo_file("docs/js/app.js")
    artifact_api_js = read_repo_file("docs/js/artifact-api.js")
    index_html = read_repo_file("docs/index.html")

    assert "INDEX_URL: 'search-index-lite.json'" in app_js
    assert "LEGACY_INDEX_URL: 'search-index.json'" in app_js
    assert "function normalizeSearchIndex" in artifact_api_js
    assert "function loadSearchIndex" in app_js
    assert "function activateFullSearch" in app_js
    assert 'id="search-all-btn"' in index_html
    assert index_html.index('src="js/artifact-api.js"') < index_html.index('src="js/app.js"')
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
        "static-artifact-api-v1",
        "static-artifact-api-v2",
        "Same-set Count Groups",
    ]

    for term in expected_terms:
        assert term in contract


def test_pages_leaderboard_uses_bounded_sources():
    app_js = read_repo_file("docs/js/app.js")
    render_js = read_repo_file("docs/js/app-render.js")

    assert "fullIndex: null" in app_js
    assert "async function loadCategoryLeaderboardSkills" in app_js
    assert "async function showLeaderboard" in render_js
    assert "await loadCategoryLeaderboardSkills(categoryFilter)" in render_js
    assert "state.featured.map(normalizeSkillRecord)" in render_js


def test_publish_sync_runs_generated_size_guard_after_rebuild():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    rebuild_block = sync_script[sync_script.index('if [[ "$rebuild" -eq 1 ]]') :]

    security_pos = rebuild_block.index("scripts/security_scanner.py")
    rebuild_pos = rebuild_block.index("scripts/build_search_index.py")
    cleanup_pos = rebuild_block.index("rm -f \"$security_report_path\"")
    canonical_pos = rebuild_block.index("scripts/check_canonical_categories.py")
    guard_pos = rebuild_block.index("scripts/check_generated_file_sizes.py")
    category_guard_pos = rebuild_block.index("scripts/check_category_artifacts.py")
    artifact_api_pos = rebuild_block.index("scripts/check_artifact_api.py")

    assert artifact_api_pos > category_guard_pos > guard_pos > canonical_pos > cleanup_pos > rebuild_pos > security_pos
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
    assert '--root "$main_dir"' in sync_script
    assert '--docs-dir "$main_dir/docs"' in sync_script


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
        "Validate static artifact API v1",
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
    upload_pos = build_steps.index("Upload security scan evidence")
    enforce_pos = build_steps.index("Enforce archive security scan")
    build_pos = build_steps.index("scripts/build_search_index.py")
    security_block = build_steps[security_pos:upload_pos]
    upload_block = build_steps[upload_pos:enforce_pos]
    enforce_block = build_steps[enforce_pos:build_pos]

    assert security_pos < upload_pos < enforce_pos < build_pos
    assert "--output \"$SECURITY_REPORT\"" in security_block
    assert "--security-report \"$RUNNER_TEMP/security-report.json\"" in build_steps
    assert "--output docs/security-report.json" not in build_steps
    assert "unzip -o security-report.zip -d docs || true" not in build_steps
    assert "--require-metadata" in security_block
    assert "--report-only" not in security_block
    assert "continue-on-error" not in security_block
    assert "|| true" not in security_block
    assert "scan_exit=$?" in security_block
    assert "GITHUB_STEP_SUMMARY" in security_block
    assert "Error taxonomy" in security_block
    assert "gzip -c \"$SECURITY_EVIDENCE\"" in security_block
    assert "failed_skill_ids" in security_block
    assert "error_type_counts" in security_block
    assert "message" not in upload_block
    assert "if: always()" in upload_block
    assert "actions/upload-artifact@v7" in upload_block
    assert "security-evidence.json.gz" in upload_block
    assert "SECURITY_REPORT" not in upload_block
    assert "security-report.json.gz" not in build_steps
    assert "if: always()" in enforce_block
    assert "steps.security_scan.outputs.exit_code" in enforce_block
    assert "steps.security_scan.outputs.report_present" in enforce_block
    assert "steps.security_scan.outputs.report_valid" in enforce_block
    assert "steps.security_scan.outputs.evidence_present" in enforce_block
    assert "steps.security_scan.outputs.evidence_archive_present" in enforce_block
    assert "steps.security_scan.outputs.failed_count" in enforce_block
    assert "steps.security_evidence.outcome" in enforce_block
    assert "exit 1" in enforce_block
    assert "test -s \"$SECURITY_REPORT\"" in enforce_block
    assert "--allow-missing-security-evidence" not in build_steps
    assert "'scripts/build_search_index.py'" in workflow
    assert "'scripts/search_sources.py'" in workflow
    assert "'scripts/security_scanner.py'" in workflow
    assert "'scripts/security_rules.py'" in workflow
    assert "'scripts/security_blocklist.py'" in workflow
    assert "'scripts/utils.py'" in workflow
    assert "'sources/security_blocklist.json'" in workflow
    assert "'schema/skill.schema.json'" in workflow


@pytest.mark.parametrize(
    "mode",
    [
        "scanner_nonzero",
        "missing",
        "invalid",
        "count_mismatch",
        "missing_decision",
        "decision_mismatch",
        "metadata_disabled",
    ],
)
def test_build_index_actual_security_gate_blocks_invalid_scanner_evidence(tmp_path, mode):
    generation = run_security_generation(tmp_path, mode)

    assert generation["result"].returncode == 0
    assert run_security_enforcement(generation).returncode != 0


def test_build_index_actual_security_gate_accepts_valid_sanitized_evidence(tmp_path):
    generation = run_security_generation(tmp_path, "valid")

    assert generation["result"].returncode == 0
    assert generation["outputs"] == {
        "exit_code": "0",
        "report_present": "true",
        "report_valid": "true",
        "evidence_present": "true",
        "evidence_archive_present": "true",
        "failed_count": "0",
    }
    assert run_security_enforcement(generation).returncode == 0


def test_build_index_actual_security_gate_blocks_failed_decision_with_zero_exit(tmp_path):
    generation = run_security_generation(tmp_path, "failed_exit_zero")

    assert generation["result"].returncode == 0
    assert generation["outputs"]["exit_code"] == "0"
    assert generation["outputs"]["report_valid"] == "true"
    assert generation["outputs"]["failed_count"] == "1"
    assert run_security_enforcement(generation).returncode != 0


@pytest.mark.parametrize("missing_output", ["evidence", "archive"])
def test_build_index_actual_security_gate_blocks_missing_sanitized_output(
    tmp_path, missing_output
):
    generation = run_security_generation(tmp_path, "valid")
    generation[missing_output].unlink()

    assert run_security_enforcement(generation).returncode != 0


def test_build_index_actual_security_gate_blocks_failed_evidence_upload(tmp_path):
    generation = run_security_generation(tmp_path, "valid")

    assert run_security_enforcement(generation, upload_outcome="failure").returncode != 0


def test_uploaded_security_evidence_excludes_raw_secret_markers(tmp_path):
    generation = run_security_generation(tmp_path, "scanner_nonzero")
    sentinel = generation["env"]["SENTINEL_SECRET_MARKER"]
    evidence_text = generation["evidence"].read_text(encoding="utf-8")
    archived_text = gzip.decompress(generation["archive"].read_bytes()).decode("utf-8")
    summary_text = generation["summary"].read_text(encoding="utf-8")
    evidence = json.loads(evidence_text)

    assert evidence_text == archived_text
    assert sentinel not in evidence_text
    assert sentinel not in summary_text
    assert set(evidence) == {
        "schema_version",
        "scanner",
        "scan_policy",
        "counts",
        "failed_skill_ids",
        "error_type_counts",
    }
    assert evidence["error_type_counts"] == {"hardcoded_credential": 1}
    assert len(evidence["failed_skill_ids"]) == 1
    assert len(evidence["failed_skill_ids"][0]) == 64
    assert "issues" not in evidence_text
    assert "/private/" not in evidence_text


def test_build_index_runs_generated_size_guard_before_pages_upload():
    workflow_text = read_repo_file(".github/workflows/build-index.yml")
    workflow = yaml.safe_load(workflow_text)
    steps = workflow["jobs"]["build-index"]["steps"]
    names = [step.get("name") for step in steps]

    guard_pos = names.index("Check generated artifact sizes")
    category_guard_pos = names.index("Check category artifacts remain sharded")
    canonical_pos = names.index("Check published categories are canonical")
    artifact_api_pos = names.index("Validate static artifact API v1")
    rebuild_pos = names.index("Rebuild root registry artifacts")
    search_pos = names.index("Build search index")
    setup_pos = names.index("Setup Pages")
    upload_pos = names.index("Upload Pages artifact")

    assert rebuild_pos < search_pos < guard_pos < category_guard_pos < canonical_pos < artifact_api_pos < setup_pos < upload_pos
    validator_step = steps[artifact_api_pos]
    assert validator_step["run"] == "python scripts/check_artifact_api.py --root . --docs-dir docs"
    assert "continue-on-error" not in validator_step
    assert "scripts/check_artifact_api.py" in workflow_text
    assert "scripts/check_registry_shard_placement.py" in workflow_text
    assert "--include docs" in workflow_text
    assert "--docs-dir docs" in workflow_text


def test_build_index_root_rebuild_commands_are_executable(tmp_path):
    skill_dir = tmp_path / "skills" / "development" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# Demo\n\nGenerated fixture.\n", encoding="utf-8")
    (skill_dir / "metadata.json").write_text(
        json.dumps({"name": "demo", "repo": "owner/demo", "path": "development/demo/SKILL.md", "branch": "main", "category": "development"}),
        encoding="utf-8",
    )
    registry = tmp_path / "registry.json"
    manifest = tmp_path / "registry-manifest.json"
    shards = tmp_path / "registry-shards"
    summary = tmp_path / "registry_summary.json"
    subprocess.run(
        [
            sys.executable, str(ROOT / "scripts/rebuild_registry.py"),
            "--skills-dir", str(tmp_path / "skills"), "--registry", str(registry),
            "--manifest", str(manifest), "--shards-dir", str(shards),
            "--skip-categories", "--compat-manifest-pointer",
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [
            sys.executable, str(ROOT / "scripts/build_registry_summary.py"),
            "--registry", str(registry), "--plugins", str(ROOT / "sources/plugins.json"),
            "--output", str(summary),
        ],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert json.loads(registry.read_text())["manifest"] == "registry-manifest.json"
    assert json.loads(manifest.read_text())["total_count"] == 1
    assert json.loads(summary.read_text())["total_count"] == 1


def test_pages_reader_rejects_unknown_artifact_shapes_without_empty_fallbacks():
    artifact_api_js = read_repo_file("docs/js/artifact-api.js")
    app_js = read_repo_file("docs/js/app.js")
    full_loader = app_js[
        app_js.index("async function loadFullSearchIndex") : app_js.index(
            "async function getFilterBaseSkills"
        )
    ]

    assert "requireExactFields" in artifact_api_js
    assert "validateSearchPointer" in full_loader
    assert "validateSearchManifest" in full_loader
    assert "validateSearchShardEntry" in full_loader
    assert "validateSearchShardPayload" in full_loader
    assert "|| []" not in full_loader
    assert "manifest.v || pointer.v" not in full_loader


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
    gitignore = read_repo_file(".gitignore")

    assert "git add registry.json registry_summary.json registry-manifest.json registry-shards/" in workflow
    assert "registry-shards/*.json.gz" in gitignore
    assert "git rm -f --cached --ignore-unmatch registry-shards/*.json.gz" in workflow


def test_sync_data_security_scope_fails_closed_on_git_errors():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    start = workflow.index("Resolve security scope")
    end = workflow.index("Security scan (skills full)")
    scope = workflow[start:end]

    assert "git -C skills diff --name-only --diff-filter=AM || true" not in scope
    assert "git -C skills ls-files --others --exclude-standard || true" not in scope
    assert "--expected-security-paths" in workflow
    assert "security-scan-targets.txt" in scope


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


def test_sync_data_preflight_is_main_only_and_precedes_repository_checkout():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    parsed = read_workflow(".github/workflows/sync-data.yml")
    preflight = parsed["jobs"]["preflight"]

    assert parsed["concurrency"] == {
        "group": "sync-data-pipeline",
        "cancel-in-progress": False,
    }
    assert preflight["steps"][0]["name"] == "Require main branch authority"
    assert "refs/heads/main" in preflight["steps"][0]["run"]
    assert all("actions/checkout" not in step.get("uses", "") for step in preflight["steps"])

    branch_guard_pos = workflow.index("Require main branch authority")
    config_guard_pos = workflow.index("Validate target repositories and write permissions")
    checkout_pos = workflow.index("Checkout core")
    discovery_pos = workflow.index("Resolve discovery profile")
    push_pos = workflow.index("Commit & push data repo changes")
    assert branch_guard_pos < config_guard_pos < checkout_pos < discovery_pos < push_pos


def test_sync_data_preflight_fails_closed_on_invalid_targets_or_permissions():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    preflight = read_workflow(".github/workflows/sync-data.yml")["jobs"]["preflight"]
    config_step = next(
        step
        for step in preflight["steps"]
        if step["name"] == "Validate target repositories and write permissions"
    )
    config = config_step["run"]

    for name in (
        "REGISTRY_DATA_REPO",
        "DATA_REPO_TOKEN",
        "REGISTRY_MAIN_REPO",
        "MAIN_REPO_TOKEN",
    ):
        assert name in config_step["env"]
        assert name in config
    assert "^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$" in config
    assert 'response.get("default_branch") != "main"' in config
    assert 'response.get("permissions", {}).get("push") is not True' in config
    assert "Core, data, and main repositories must be distinct" in config
    assert "ready=false" not in workflow
    assert "skipping main publish dispatch" not in workflow


def test_sync_data_uses_explicit_main_checkouts_rebases_and_pushes():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    sync = read_workflow(".github/workflows/sync-data.yml")["jobs"]["sync"]
    checkouts = [step for step in sync["steps"] if step.get("uses") == "actions/checkout@v6"]

    assert len(checkouts) == 2
    assert all(step["with"]["ref"] == "main" for step in checkouts)
    assert workflow.count("git fetch origin main") == 2
    assert workflow.count("git rebase origin/main") == 2
    assert workflow.count("git push origin HEAD:main") == 2
    assert "if git push; then" not in workflow


def test_sync_data_handoff_is_immutable_secret_free_and_precedes_dispatch():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    sync = read_workflow(".github/workflows/sync-data.yml")["jobs"]["sync"]
    handoff = next(
        step for step in sync["steps"] if step["name"] == "Build immutable publish handoff"
    )
    upload = next(
        step for step in sync["steps"] if step["name"] == "Upload immutable publish handoff"
    )

    data_push_pos = workflow.index("Commit & push data repo changes")
    core_push_pos = workflow.index("Commit & push core metadata changes")
    capture_pos = workflow.index("Capture source SHAs")
    handoff_pos = workflow.index("Build immutable publish handoff")
    upload_pos = workflow.index("Upload immutable publish handoff")
    dispatch_pos = workflow.index("Dispatch main publish workflow from immutable handoff")
    build_index_pos = workflow.index("Dispatch build-index to refresh Pages")
    assert data_push_pos < core_push_pos < capture_pos < handoff_pos < upload_pos < dispatch_pos
    assert dispatch_pos < build_index_pos

    assert upload["with"]["name"] == "sync-publish-handoff"
    assert upload["with"]["if-no-files-found"] == "error"
    assert upload["with"]["retention-days"] == 30
    for field in (
        '"schema_version": 1',
        '"run_id": os.environ["RUN_ID"]',
        '"run_attempt": 1',
        '"target_repo": os.environ["REGISTRY_MAIN_REPO"]',
        '"event_type": "publish_from_core"',
        '"payload_sha256": hashlib.sha256(payload_bytes).hexdigest()',
    ):
        assert field in handoff["run"]
    assert "TOKEN" not in handoff["env"]
    assert "token" not in handoff["run"].lower()


def test_sync_data_reruns_skip_mutation_and_require_valid_original_handoff():
    parsed = read_workflow(".github/workflows/sync-data.yml")
    preflight = parsed["jobs"]["preflight"]
    sync = parsed["jobs"]["sync"]
    publish = parsed["jobs"]["publish"]

    assert sync["needs"] == "preflight"
    assert sync["if"] == "github.run_attempt == 1"
    assert publish["needs"] == ["preflight", "sync"]
    assert "github.run_attempt > 1" in publish["if"]
    assert "needs.sync.result == 'skipped'" in publish["if"]

    replay_download = next(
        step for step in preflight["steps"] if step["name"] == "Download replay handoff"
    )
    replay_validate = next(
        step
        for step in preflight["steps"]
        if step["name"] == "Validate replay handoff before mutation boundary"
    )
    assert replay_download["if"] == "github.run_attempt > 1"
    assert replay_validate["if"] == "github.run_attempt > 1"
    assert replay_download["with"]["name"] == "sync-publish-handoff"
    assert "run-id" not in replay_download["with"]
    assert "repository" not in replay_download["with"]
    for contract in (
        "set(payload) != payload_keys",
        "set(evidence) != evidence_keys",
        '"run_attempt": 1',
        "Replay payload/evidence mismatch",
        "Replay payload hash mismatch",
    ):
        assert contract in replay_validate["run"]


def test_sync_data_publish_sends_exact_payload_and_fails_with_safe_replay_evidence():
    publish = read_workflow(".github/workflows/sync-data.yml")["jobs"]["publish"]
    download = next(
        step for step in publish["steps"] if step["name"] == "Download immutable publish handoff"
    )
    validate = next(
        step for step in publish["steps"] if step["name"] == "Validate immutable publish handoff"
    )
    dispatch = next(
        step
        for step in publish["steps"]
        if step["name"] == "Dispatch main publish workflow from immutable handoff"
    )
    build_index = next(
        step
        for step in publish["steps"]
        if step["name"] == "Dispatch build-index to refresh Pages"
    )

    for contract in (
        "set(payload) != payload_keys",
        "set(evidence) != evidence_keys",
        "Publish payload/evidence mismatch",
        "Publish payload hash mismatch",
    ):
        assert contract in validate["run"]
    assert download["with"]["name"] == "sync-publish-handoff"
    assert "run-id" not in download["with"]
    assert "repository" not in download["with"]
    assert "if ! curl --fail-with-body -X POST" in dispatch["run"]
    assert '--data-binary "@$PAYLOAD_FILE"' in dispatch["run"]
    assert "GITHUB_STEP_SUMMARY" in dispatch["run"]
    assert "target=$TARGET_REPO core=$CORE_SHA data=$DATA_SHA hash=$PAYLOAD_SHA256" in dispatch["run"]
    assert "exit 1" in dispatch["run"]
    assert "actions/workflows/build-index.yml/dispatches" in build_index["run"]


def test_sync_data_branch_guard_executes_and_rejects_non_main(tmp_path):
    step = workflow_step("preflight", "Require main branch authority")

    rejected = run_workflow_script(step, tmp_path, {"GITHUB_REF_VALUE": "refs/heads/feature"})
    accepted = run_workflow_script(step, tmp_path, {"GITHUB_REF_VALUE": "refs/heads/main"})

    assert rejected.returncode != 0
    assert "only run from refs/heads/main" in rejected.stdout
    assert accepted.returncode == 0


@pytest.mark.parametrize(
    ("updates", "expected_error"),
    [
        ({"DATA_REPO_TOKEN": ""}, "Missing required sync-data configuration"),
        ({"REGISTRY_DATA_REPO": "not-a-repo"}, "Invalid owner/name repository"),
        (
            {"CORE_REPO": "Owner/Core", "REGISTRY_DATA_REPO": "owner/core"},
            "Core, data, and main repositories must be distinct",
        ),
        ({"FAKE_PUSH": "false"}, "does not have push permission"),
        ({"FAKE_DEFAULT_BRANCH": "develop"}, "default branch must be main"),
    ],
)
def test_sync_data_config_preflight_executes_and_fails_closed(
    tmp_path, updates, expected_error
):
    step = workflow_step("preflight", "Validate target repositories and write permissions")
    env = valid_sync_env()
    env.update(updates)

    result = run_workflow_script(step, tmp_path, env, fake_curl=True)

    assert result.returncode != 0
    assert expected_error in result.stdout + result.stderr


def test_sync_data_config_preflight_executes_with_valid_distinct_targets(tmp_path):
    step = workflow_step("preflight", "Validate target repositories and write permissions")

    result = run_workflow_script(step, tmp_path, valid_sync_env(), fake_curl=True)

    assert result.returncode == 0, result.stdout + result.stderr


def test_sync_data_handoff_generator_executes_with_exact_payload_bytes_and_hash(tmp_path):
    root, payload_bytes, evidence = build_valid_handoff(tmp_path)
    expected = (
        b'{"event_type":"publish_from_core","client_payload":'
        b'{"core_repo":"Owner/Core","core_sha":"' + b"a" * 40
        + b'","data_repo":"Owner/Data","data_sha":"' + b"b" * 40
        + b'"}}\n'
    )

    assert payload_bytes == expected
    assert evidence == {
        "schema_version": 1,
        "run_id": "1234",
        "run_attempt": 1,
        "target_repo": "Owner/Main",
        "core_repo": "Owner/Core",
        "core_sha": "a" * 40,
        "data_repo": "Owner/Data",
        "data_sha": "b" * 40,
        "event_type": "publish_from_core",
        "payload_sha256": hashlib.sha256(expected).hexdigest(),
    }
    assert sorted(path.name for path in root.iterdir()) == [
        "publish-dispatch-evidence.json",
        "publish-dispatch-payload.json",
    ]


@pytest.mark.parametrize(
    "corruption",
    ["missing", "invalid_json", "hash_mismatch", "extra_key", "field_mismatch"],
)
@pytest.mark.parametrize(
    ("job_name", "step_name", "handoff_dir"),
    [
        (
            "preflight",
            "Validate replay handoff before mutation boundary",
            "replay-handoff",
        ),
        ("publish", "Validate immutable publish handoff", "sync-publish-handoff"),
    ],
)
def test_sync_data_handoff_validators_execute_and_reject_corruption(
    tmp_path, corruption, job_name, step_name, handoff_dir
):
    root, payload_bytes, evidence = build_valid_handoff(tmp_path)
    if root.name != handoff_dir:
        root = root.rename(tmp_path / handoff_dir)
    payload_path = root / "publish-dispatch-payload.json"
    evidence_path = root / "publish-dispatch-evidence.json"
    if corruption == "missing":
        evidence_path.unlink()
    elif corruption == "invalid_json":
        evidence_path.write_text("{", encoding="utf-8")
    elif corruption == "hash_mismatch":
        payload_path.write_bytes(payload_bytes + b" ")
    elif corruption == "extra_key":
        evidence["unexpected"] = "rejected"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    else:
        payload = json.loads(payload_bytes)
        payload["client_payload"]["core_sha"] = "c" * 40
        changed_bytes = (json.dumps(payload, separators=(",", ":")) + "\n").encode()
        payload_path.write_bytes(changed_bytes)
        evidence["payload_sha256"] = hashlib.sha256(changed_bytes).hexdigest()
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    step = workflow_step(job_name, step_name)
    env = {
        "EXPECTED_RUN_ID": "1234",
        "EXPECTED_CORE_REPO": "Owner/Core",
        "EXPECTED_DATA_REPO": "Owner/Data",
        "EXPECTED_TARGET_REPO": "Owner/Main",
    }
    result = run_workflow_script(step, tmp_path, env)

    assert result.returncode != 0


def test_sync_data_preflight_replay_validator_executes_and_accepts_valid_handoff(tmp_path):
    root, _, _ = build_valid_handoff(tmp_path)
    root.rename(tmp_path / "replay-handoff")
    preflight = read_workflow(".github/workflows/sync-data.yml")["jobs"]["preflight"]
    step = workflow_step("preflight", "Validate replay handoff before mutation boundary")
    env = {
        "EXPECTED_RUN_ID": "1234",
        "EXPECTED_CORE_REPO": "Owner/Core",
        "EXPECTED_DATA_REPO": "Owner/Data",
        "EXPECTED_TARGET_REPO": "Owner/Main",
    }

    result = run_workflow_script(step, tmp_path, env)

    assert result.returncode == 0, result.stderr
    assert all("actions/checkout" not in candidate.get("uses", "") for candidate in preflight["steps"])
    assert preflight["steps"].index(step) > preflight["steps"].index(
        next(candidate for candidate in preflight["steps"] if candidate["name"] == "Download replay handoff")
    )


def test_sync_data_handoff_validator_executes_and_exports_verified_fields(tmp_path):
    _, _, evidence = build_valid_handoff(tmp_path)
    step = workflow_step("publish", "Validate immutable publish handoff")
    env = {
        "EXPECTED_RUN_ID": "1234",
        "EXPECTED_CORE_REPO": "Owner/Core",
        "EXPECTED_DATA_REPO": "Owner/Data",
        "EXPECTED_TARGET_REPO": "Owner/Main",
    }

    result = run_workflow_script(step, tmp_path, env)
    outputs = dict(
        line.split("=", 1)
        for line in (tmp_path / "github-output").read_text(encoding="utf-8").splitlines()
    )

    assert result.returncode == 0, result.stderr
    assert outputs == {
        key: str(evidence[key])
        for key in ("target_repo", "core_sha", "data_sha", "payload_sha256")
    }


def test_sync_data_dispatch_non_2xx_fails_and_suppresses_build_index(tmp_path):
    _, _, evidence = build_valid_handoff(tmp_path)
    publish = read_workflow(".github/workflows/sync-data.yml")["jobs"]["publish"]
    dispatch = workflow_step("publish", "Dispatch main publish workflow from immutable handoff")
    build_index = workflow_step("publish", "Dispatch build-index to refresh Pages")
    env = {
        "MAIN_REPO_TOKEN": "main-test-token",
        "TARGET_REPO": evidence["target_repo"],
        "CORE_SHA": evidence["core_sha"],
        "DATA_SHA": evidence["data_sha"],
        "PAYLOAD_SHA256": evidence["payload_sha256"],
        "FAKE_CURL_MODE": "fail",
    }

    dispatch_result = run_workflow_script(dispatch, tmp_path, env, fake_curl=True)
    build_index_executed = False
    if dispatch_result.returncode == 0:
        build_index_executed = True
        run_workflow_script(build_index, tmp_path, env, fake_curl=True)

    assert dispatch_result.returncode != 0
    assert build_index.get("if") is None
    assert not build_index_executed
    summary = (tmp_path / "github-summary").read_text(encoding="utf-8")
    assert evidence["target_repo"] in summary
    assert evidence["core_sha"] in summary
    assert evidence["data_sha"] in summary
    assert evidence["payload_sha256"] in summary
    assert publish["steps"].index(dispatch) < publish["steps"].index(build_index)


def test_metadata_compliance_refuses_unexpected_zero_target_scan():
    workflow = read_repo_file(".github/workflows/metadata-compliance.yml")

    assert "allow_missing_data_repo" in workflow
    assert "metadata-advisory-zero-targets" in workflow
    assert "refusing to run metadata compliance with zero targets" in workflow
    assert "exit 1" in workflow


def test_python_tests_workflow_runs_full_suite_with_coverage_gate():
    workflow = read_repo_file(".github/workflows/python-tests.yml")
    pyproject = read_repo_file("pyproject.toml")
    pull_request_paths = workflow[workflow.index("pull_request:") : workflow.index("  push:")]
    push_paths = workflow[workflow.index("  push:") : workflow.index("  workflow_dispatch:")]

    assert "name: Python Test Health" in workflow
    assert "fetch-depth: 0" in workflow
    assert "python -m pytest -q --cov-report=xml:coverage.xml --cov-report=json:coverage.json" in workflow
    assert "scripts/check_coverage_ratchet.py" in workflow
    assert "--baseline coverage-baseline.json" in workflow
    assert "--compare-ref origin/main" in workflow
    assert "diff-cover coverage.xml --compare-branch=origin/main --fail-under=80" in workflow
    assert "--cov=" not in workflow
    assert "--cov-config" not in workflow
    assert "--cov-fail-under=50" not in workflow
    assert "scripts/check_taxonomy_governance.py" in workflow
    assert "--override-ini" not in workflow
    assert "scripts/**" in workflow
    assert "taxonomy/**" in workflow
    assert "crawler/**" in workflow
    assert "coverage-baseline.json" in pull_request_paths
    assert "coverage-baseline.json" in push_paths
    assert 'source = ["scripts", "crawler"]' in pyproject
    assert "branch = true" in pyproject
    assert "omit =" not in pyproject
    assert "exclude_also =" not in pyproject
