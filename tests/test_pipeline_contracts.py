import gzip
import hashlib
import json
import os
import shutil
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


def build_valid_handoff(
    tmp_path: Path, full_scan: str = "false", full_cycle_complete: str = ""
) -> tuple[Path, bytes, dict]:
    step = workflow_step("sync", "Build immutable publish handoff")
    env = {
        "RUN_ID": "1234",
        "CORE_REPO": "Owner/Core",
        "CORE_SHA": "a" * 40,
        "DATA_REPO": "Owner/Data",
        "DATA_SHA": "b" * 40,
        "REGISTRY_MAIN_REPO": "Owner/Main",
        "FULL_SCAN": full_scan,
        "FULL_CYCLE_COMPLETE": full_cycle_complete,
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
    static_pages_pos = rebuild_block.index("scripts/build_static_skill_pages.py")
    cleanup_pos = rebuild_block.index("rm -f \"$security_report_path\"")
    canonical_pos = rebuild_block.index("scripts/check_canonical_categories.py")
    guard_pos = rebuild_block.index("scripts/check_generated_file_sizes.py")
    category_guard_pos = rebuild_block.index("scripts/check_category_artifacts.py")
    artifact_api_pos = rebuild_block.index("scripts/check_artifact_api.py")

    assert artifact_api_pos > category_guard_pos > guard_pos > canonical_pos > cleanup_pos > static_pages_pos > rebuild_pos > security_pos
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
        "Build static featured skill pages",
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


@pytest.mark.parametrize("shell", ["bash", "/bin/bash"])
@pytest.mark.parametrize("mirror_skills", [0, 1])
def test_publish_static_pages_receives_catalog_archive_and_output_together(mirror_skills, shell):
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    command = sync_script[sync_script.index('if [[ "$rebuild" -eq 1 ]]') :]
    command = command.split('\n  run_step "Remove temporary guide catalog"', 1)[0] + '\nfi'
    result = subprocess.run(
        [
            shell,
            "-eu",
            "-c",
            'main_dir=/tmp/publish\narchive_dir=/tmp/publish/skills\nrebuild=1\n'
            f'mirror_skills={mirror_skills}\n'
            'mktemp() { :; }\nmkdir() { :; }\n'
            'run_step() { if [[ "$1" == "Build static featured skill pages" ]]; then '
            'printf "%s\\n" "$@"; fi; }\n' + command,
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.stdout.splitlines() == [
        "Build static featured skill pages",
        "python",
        "/tmp/publish/scripts/build_static_skill_pages.py",
        "--catalog",
        "/tmp/publish/docs/page-catalog.json",
        *(["--archive", "/tmp/publish/skills"] if mirror_skills else []),
        "--output",
        "/tmp/publish/docs",
    ]


@pytest.mark.parametrize("mirror_skills", [0, 1])
def test_publish_static_pages_preserves_data_checkout(tmp_path, mirror_skills):
    """Run the real page generator through the publish shell's rebuild wiring."""
    data = tmp_path / "data source"
    main = tmp_path / "publish target"
    for category in ("development", "design"):
        skill_dir = data / category / "demo"
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("# Original archived skill\n", encoding="utf-8")
        (skill_dir / "metadata.json").write_text('{"name":"demo"}\n', encoding="utf-8")
    (data / "development/README.md").write_text("# Maintained category notes\n", encoding="utf-8")

    def snapshot():
        return {path.relative_to(data): path.read_bytes() for path in data.rglob("*") if path.is_file()}

    before = snapshot()
    archive = data
    if mirror_skills:
        archive = main / "skills"
        shutil.copytree(data, archive)
    (main / "scripts").mkdir(parents=True)
    shutil.copy2(ROOT / "scripts/build_static_skill_pages.py", main / "scripts")
    docs = main / "docs"
    docs.mkdir()
    (docs / "page-catalog.json").write_text(json.dumps({"skills": [{
        "id": "demo", "name": "demo", "repo": "owner/repo", "category": "development",
        "description": "A useful skill with a substantive description for publishing.",
        "security_status": "passed", "install_status": "known_good", "quality_score": 80,
    }]}), encoding="utf-8")
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    rebuild_block = sync_script[sync_script.index('if [[ "$rebuild" -eq 1 ]]') :]
    rebuild_block = rebuild_block.split('\nrun_step "Generate third-party notices', 1)[0]
    command = '''set -euo pipefail
rebuild=1
run_step() {
  local label="$1"
  shift
  if [[ "$label" == "Build static featured skill pages" ]]; then
    "$@"
  fi
}
''' + rebuild_block

    for _ in range(2):
        result = subprocess.run(
            ["bash", "-c", command], capture_output=True, text=True, check=False,
            env={**os.environ, "main_dir": str(main), "archive_dir": str(archive),
                 "mirror_skills": str(mirror_skills),
                 "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}"},
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert "Generated 1 static skill pages" in result.stdout
        assert snapshot() == before
        assert (docs / "skills/index.html").is_file()
        assert len(list((docs / "skills").glob("*/index.html"))) == 1
        assert (docs / "sitemap.xml").is_file()
        if mirror_skills:
            for category in ("development", "design"):
                assert "Browse [skill guides" in (archive / category / "README.md").read_text()
        else:
            assert not (main / "skills").exists()


def test_publish_sync_rebuild_steps_read_the_selected_archive_dir():
    sync_script = read_repo_file("scripts/sync_main_repo.sh")
    rebuild_block = sync_script[sync_script.index('if [[ "$rebuild" -eq 1 ]]') :]

    assert '"$main_dir/skills"' not in rebuild_block
    assert rebuild_block.count('"$archive_dir"') == 6
    selection = sync_script[
        sync_script.index('if [[ "$mirror_skills" -eq 1 ]]') : sync_script.index(
            'if [[ "$rebuild" -eq 1 ]]'
        )
    ]
    assert 'run_step "Sync data -> main/skills" sync_data_to_main' in selection
    assert 'archive_dir="$main_dir/skills"' in selection
    assert 'archive_dir="$data_dir"' in selection


@pytest.mark.parametrize("shell", ["bash", "/bin/bash"])
def test_publish_sync_without_skills_mirror_builds_from_data_dir(tmp_path, shell):
    core, data, main = (tmp_path / name for name in ("core", "data", "main"))
    for path in (core, data, main):
        path.mkdir()
    for directory in ("scripts", "schema", "taxonomy"):
        shutil.copytree(ROOT / directory, core / directory)
    skill = data / "design/legal-example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# legal example\n", encoding="utf-8")
    (skill / "metadata.json").write_text(
        json.dumps(
            {
                "name": "legal-example",
                "repo": "owner/repo",
                "category": "design",
                "dir_name": "legal-example",
                "author": "Owner",
                "license": "MIT",
                "copyright": "Copyright 2026 Owner",
                "distribution": "compatible",
                "source_url": "https://github.com/owner/repo/blob/main/SKILL.md",
                "permission_note": "Preserve the copyright and permission notice.",
            }
        ),
        encoding="utf-8",
    )

    stale_skill = main / "skills/design/stale-skill/SKILL.md"
    stale_skill.parent.mkdir(parents=True)
    stale_skill.write_text("# Previous publishing mirror\n", encoding="utf-8")
    archive_before = {
        path.relative_to(data): path.read_bytes()
        for path in data.rglob("*") if path.is_file()
    }

    result = subprocess.run(
        [
            shell, str(core / "scripts/sync_main_repo.sh"),
            "--core", str(core), "--data", str(data), "--main", str(main),
            "--no-rebuild", "--no-skills-mirror",
        ],
        cwd=main,
        env={
            **os.environ,
            "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
        },
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Skipping data -> main/skills mirror" in result.stdout
    assert "START: Sync data -> main/skills" not in result.stdout
    assert not (main / "skills").exists()
    assert (skill / "SKILL.md").is_file()
    assert {
        path.relative_to(data): path.read_bytes()
        for path in data.rglob("*") if path.is_file()
    } == archive_before
    assert "Copyright 2026 Owner" in (main / "THIRD_PARTY_NOTICES.d/part-00001.md").read_text(
        encoding="utf-8"
    )


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


def test_publish_sync_preserves_main_owned_tests_during_repeated_sync(tmp_path):
    core = tmp_path / "core"
    data = tmp_path / "data"
    main = tmp_path / "main"
    for path in (core, data, main):
        path.mkdir()
    for directory in ("scripts", "schema", "taxonomy"):
        shutil.copytree(ROOT / directory, core / directory)

    (core / "tests").mkdir()
    (main / "tests").mkdir()
    owned = main / "tests/test_publish_from_core_workflow.py"
    owned.write_text("# main-owned workflow security tests\n", encoding="utf-8")
    expected_owned = owned.read_bytes()
    mirrored = "tests/test_pipeline_contracts.py"
    (core / mirrored).write_text("# current core tests\n", encoding="utf-8")
    (main / mirrored).write_text("# previous core tests\n", encoding="utf-8")
    stale = main / "tests/test_obsolete_core.py"
    stale.write_text("# obsolete core tests\n", encoding="utf-8")
    workflow = main / ".github/workflows/publish-from-core.yml"
    workflow.parent.mkdir(parents=True)
    workflow.write_text("# main-owned publish workflow\n", encoding="utf-8")
    (data / "archived-skill.md").write_text("# archive fixture\n", encoding="utf-8")

    for revision in ("first", "second"):
        (core / mirrored).write_text(f"# {revision} core tests\n", encoding="utf-8")
        result = subprocess.run(
            [
                "bash", str(core / "scripts/sync_main_repo.sh"),
                "--core", str(core), "--data", str(data), "--main", str(main),
                "--no-rebuild",
            ],
            cwd=main,
            env={
                **os.environ,
                "PATH": f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}",
            },
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stdout + result.stderr
        assert owned.is_file(), result.stdout + result.stderr
        assert owned.read_bytes() == expected_owned
        assert (main / mirrored).read_bytes() == (core / mirrored).read_bytes()
        assert not stale.exists()
        assert workflow.read_text(encoding="utf-8") == "# main-owned publish workflow\n"
        assert (main / "skills/archived-skill.md").is_file()


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
    assert "'scripts/build_static_skill_pages.py'" in workflow
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


def test_build_index_runs_generated_guards_without_deploying_pages():
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
    static_pages_pos = names.index("Build static featured skill pages")
    assert rebuild_pos < search_pos < static_pages_pos < guard_pos < category_guard_pos < canonical_pos < artifact_api_pos
    validator_step = steps[artifact_api_pos]
    assert validator_step["run"] == "python scripts/check_artifact_api.py --root . --docs-dir docs"
    assert "continue-on-error" not in validator_step
    assert "scripts/check_artifact_api.py" in workflow_text
    assert "scripts/check_registry_shard_placement.py" in workflow_text
    assert "--include docs" in workflow_text
    assert "--docs-dir docs" in workflow_text
    assert "actions/configure-pages" not in workflow_text
    assert "actions/upload-pages-artifact" not in workflow_text
    assert "actions/deploy-pages" not in workflow_text


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


@pytest.mark.parametrize("oversized_docs_artifact", [False, True])
def test_sync_data_keeps_large_raw_security_report_outside_publish_artifacts(
    tmp_path, oversized_docs_artifact,
):
    steps = yaml.safe_load(read_repo_file(".github/workflows/sync-data.yml"))["jobs"]["sync"]["steps"]
    names = [step.get("name") for step in steps]
    upload = steps[names.index("Upload security report")]
    assert upload["with"]["path"] == "security-report.json"
    assert "--security-report security-report.json" in steps[
        names.index("Validate sync pipeline health")
    ]["run"]

    (tmp_path / "docs").mkdir()
    (tmp_path / "scripts").mkdir()
    shutil.copyfile(ROOT / "scripts/check_generated_file_sizes.py",
                    tmp_path / "scripts/check_generated_file_sizes.py")
    raw_report = tmp_path / "security-report.json"
    with raw_report.open("wb") as handle:
        handle.truncate(266250501)
    if oversized_docs_artifact:
        with (tmp_path / "docs/unrelated.json").open("wb") as handle:
            handle.truncate(266250501)

    for step in steps[names.index("Upload bundled asset liveness report") + 1:
                      names.index("Rebuild registry.json from archive")]:
        if "run" in step:
            subprocess.run(["bash", "-e", "-c", step["run"]], cwd=tmp_path, check=True)
    result = subprocess.run(
        ["bash", "-e", "-c", steps[names.index("Check generated artifact sizes")]["run"]],
        cwd=tmp_path,
        env={**os.environ, "PATH": f"{Path(sys.executable).parent}:{os.environ['PATH']}"},
        capture_output=True, text=True, check=False,
    )
    assert result.returncode == (1 if oversized_docs_artifact else 0), result.stdout + result.stderr
    assert raw_report.stat().st_size == 266250501
    assert not (tmp_path / "docs/security-report.json").exists()
    if oversized_docs_artifact:
        assert "failure 253.92 MiB docs/unrelated.json" in result.stdout


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


@pytest.mark.parametrize("security_mode,archive_change", [
    ("full", "unchanged"), ("full", "added"), ("full", "removed"), ("incremental", "added"),
])
def test_sync_data_security_scan_uses_snapshot_and_rejects_full_archive_drift(
    tmp_path, security_mode, archive_change
):
    skills = tmp_path / "skills"
    original = skills / "development/demo/SKILL.md"
    original.parent.mkdir(parents=True)
    original.write_text("---\nname: demo\ndescription: Demo.\n---\n", encoding="utf-8")
    for directory in ("scripts", "schema", "sources"):
        (tmp_path / directory).symlink_to(ROOT / directory, target_is_directory=True)
    env = dict(os.environ, PATH=f"{Path(sys.executable).parent}{os.pathsep}{os.environ['PATH']}")
    targets = tmp_path / "targets.bin"
    subprocess.run(
        [sys.executable, str(ROOT / "scripts/resolve_security_scope.py"),
         "--skills-dir", str(skills), "--mode", "full", "--output", str(targets)],
        check=True, capture_output=True, text=True,
    )
    if archive_change == "added":
        added = skills / "development/new/SKILL.md"
        added.parent.mkdir()
        added.write_text("---\nname: new\ndescription: New.\n---\n", encoding="utf-8")
    elif archive_change == "removed":
        original.unlink()

    step_name = "Security scan (skills full)" if security_mode == "full" else (
        "Security scan (skills daily incremental)"
    )
    scan = workflow_step("sync", step_name)["run"].replace(
        "${{ steps.security_scope.outputs.file_list }}", str(targets)
    )
    result = subprocess.run(
        ["bash", "-eo", "pipefail", "-c", scan], cwd=tmp_path, env=env,
        capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((tmp_path / "security-report.json").read_text())
    assert {skill["path"] for skill in report["skills"]} == (
        set() if archive_change == "removed" else {"development/demo/SKILL.md"}
    )

    health_env = dict(
        env, PROFILE="full" if security_mode == "full" else "daily-bounded",
        DISCOVER_FULL_OUTCOME="success", DOWNLOAD_FULL_OUTCOME="success",
        DISCOVER_DAILY_OUTCOME="success", DOWNLOAD_DAILY_OUTCOME="success",
        SECURITY_MODE=security_mode, SECURITY_FULL_OUTCOME="success",
        SECURITY_DAILY_OUTCOME="success", SECURITY_TARGET_LIST=str(targets),
    )
    health = subprocess.run(
        ["bash", "-eo", "pipefail", "-c",
         workflow_step("sync", "Validate sync pipeline health")["run"]],
        cwd=tmp_path, env=health_env, capture_output=True, text=True,
    )
    if archive_change == "unchanged" or security_mode == "incremental":
        assert health.returncode == 0, health.stdout + health.stderr
    else:
        assert health.returncode != 0
        assert "security archive path drift:" in health.stdout
        drift_path = "development/new/SKILL.md" if archive_change == "added" else "development/demo/SKILL.md"
        assert drift_path in health.stdout


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


@pytest.mark.parametrize("step_id", ["discover_full", "discover_daily"])
def test_sync_data_discovery_failure_stops_sync(step_id):
    workflow = read_workflow(".github/workflows/sync-data.yml")
    step = next(step for step in workflow["jobs"]["sync"]["steps"]
                if step.get("id") == step_id)

    assert not step.get("continue-on-error", False)


@pytest.mark.parametrize("step_id", ["discover_full", "discover_daily"])
def test_sync_data_discovery_owns_step_process_and_preserves_exit_code(tmp_path, step_id):
    workflow = read_workflow(".github/workflows/sync-data.yml")
    step = next(step for step in workflow["jobs"]["sync"]["steps"]
                if step.get("id") == step_id)
    scripts = tmp_path / "scripts"
    scripts.mkdir()
    (scripts / "discover_by_topic.py").write_text(
        "import os\nprint(f'discovery pid={os.getpid()}')\nraise SystemExit(23)\n",
        encoding="utf-8",
    )
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    (bin_dir / "python").symlink_to(sys.executable)
    env = dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}")

    with subprocess.Popen(
        ["bash", "--noprofile", "--norc", "-eo", "pipefail", "-c", step["run"]],
        cwd=tmp_path, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    ) as process:
        stdout, stderr = process.communicate(timeout=10)

    assert process.returncode == 23, stderr
    assert f"discovery pid={process.pid}" in stdout


@pytest.mark.parametrize("cursor,schedule,skip,expected", [
    (None, "0 0 * * *", False, "daily-bounded"),
    (1, "0 0 * * *", False, "full"),
    (2, "0 0 * * *", False, "daily-bounded"),
    (1, "30 2 * * 0", False, "full"),
    (2, "30 2 * * 0", False, "full"),
    (1, "", True, "manual-sources-only"),
])
def test_sync_profile_resumes_pending_cycle(tmp_path, cursor, schedule, skip, expected):
    progress = tmp_path / "progress.json"
    if cursor is not None:
        progress.write_text(json.dumps({"repos": ["acme/a", "acme/b"], "next_repo": cursor}))
    output = tmp_path / "output"
    step = workflow_step("sync", "Resolve discovery profile")
    result = subprocess.run(
        ["bash", "-e", "-c", step["run"]], cwd=tmp_path, capture_output=True, text=True,
        env=dict(os.environ, EVENT_NAME="workflow_dispatch" if skip else "schedule",
                 EVENT_SCHEDULE=schedule, INPUT_FULL_SCAN="false",
                 INPUT_SKIP_DISCOVERY=str(skip).lower(), FULL_DISCOVERY_PROGRESS=str(progress),
                 GITHUB_OUTPUT=str(output)),
    )
    assert result.returncode == 0, result.stderr
    assert f"profile={expected}\n" == output.read_text()


@pytest.mark.parametrize("cursor,complete", [(1, "false"), (2, "true")])
def test_sync_progress_reports_batch_separately_from_cycle(tmp_path, cursor, complete):
    progress = tmp_path / "progress.json"
    progress.write_text(json.dumps({
        "repos": ["acme/a", "acme/b"], "next_repo": cursor, "started_at": "2026-09-29",
    }))
    output, summary = tmp_path / "output", tmp_path / "summary"
    result = subprocess.run(
        ["bash", "-e", "-c", workflow_step("sync", "Report full discovery progress")["run"]],
        cwd=tmp_path, capture_output=True, text=True,
        env=dict(os.environ, FULL_DISCOVERY_PROGRESS=str(progress), GITHUB_OUTPUT=str(output),
                 GITHUB_STEP_SUMMARY=str(summary)),
    )
    assert result.returncode == 0, result.stderr
    assert output.read_text() == f"complete={complete}\n"
    assert f"{cursor}/2 repositories finished" in summary.read_text()


ALERT_PROGRESS = {
    # Finished after the open alert was last raised (issue created 2026-10-04).
    "done-new": {"started_at": "2026-10-03T16:05:00Z", "repos": ["a/b", "c/d"], "next_repo": 2,
                 "completed_at": "2026-10-05T04:36:22Z"},
    # Finished before the open alert was raised.
    "done-old": {"started_at": "2026-09-27T02:30:00Z", "repos": ["a/b", "c/d"], "next_repo": 2,
                 "completed_at": "2026-09-30T00:00:00Z"},
    # A cycle that is still advancing; started_at is filled in relative to now.
    "running": {"started_at": None, "repos": ["a/b", "c/d"], "next_repo": 1, "completed_at": None},
}


def stage_alert_workspace(tmp_path: Path, progress: str, published_progress: str = None) -> None:
    """Stage the pinned helper, latest cursor, and published cursor checkouts."""
    (tmp_path / "scripts").mkdir(exist_ok=True)
    shutil.copy(ROOT / "scripts" / "sync_alert_decision.py", tmp_path / "scripts")
    for checkout, value in (
        ("latest-progress", progress),
        ("published-progress", published_progress if published_progress is not None else progress),
    ):
        if value == "absent":
            continue
        state = dict(ALERT_PROGRESS[value])
        if state["started_at"] is None:
            from datetime import datetime, timedelta, timezone
            state["started_at"] = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
        target = tmp_path / checkout / "sources" / "learning" / "full-discovery-progress.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(state), encoding="utf-8")


@pytest.mark.parametrize("skip_discovery,progress,attempt,origin,action", [
    pytest.param("false", "done-old", "2", "body", "close", id="originating-failure-recovery"),
    pytest.param("false", "done-old", "2", "comment", "close", id="latest-bot-failure-recovery"),
    pytest.param("false", "done-old", "2", "other-run", None, id="newer-other-run"),
    pytest.param("false", "done-old", "2", "unknown", None, id="unconfirmed-origin"),
    pytest.param("false", "done-old", "2", "human", None, id="human-url-is-not-an-alert"),
    pytest.param("false", "done-old", "1", "body", None, id="first-attempt-is-not-recovery"),
    pytest.param("true", "done-new", "1", "body", None, id="skip-discovery"),
    pytest.param("true", "done-new", "2", "body", None, id="skip-discovery-replay"),
])
def test_sync_alert_closure_correlates_failure_and_discovery_profile(
    tmp_path, skip_discovery, progress, attempt, origin, action
):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$2" = "list" ]; then
  echo 323
elif [ "$1" = "api" ]; then
  case "$*" in
    *created_at*)
      if [ "$2" = "repos/Owner/Core/issues/323" ]; then
        if [ "$ALERT_ORIGIN" = "unknown" ] || [ "$ALERT_ORIGIN" = "human" ]; then
          echo '["2026-10-04T00:00:00Z", "Unknown originating run"]'
        else
          printf '["2026-10-04T00:00:00Z","Failed run: %s"]\\n' "$RUN_URL"
        fi
      elif [ "$ALERT_ORIGIN" = "comment" ]; then
        printf '["2026-10-05T00:00:00Z","The scheduled weekly full sync failed again: %s"]\\n' "$RUN_URL"
      elif [ "$ALERT_ORIGIN" = "other-run" ]; then
        echo '["2026-10-05T00:00:00Z", "The scheduled weekly full sync failed again: https://github.com/Owner/Core/actions/runs/5678"]'
      elif [ "$ALERT_ORIGIN" = "human" ] && [[ "$*" != *'.user.login == "github-actions[bot]"'* ]]; then
        printf '["2026-10-05T00:00:00Z","Failed run: %s"]\\n' "$RUN_URL"
      fi
      exit 0 ;;
  esac
  case "$2" in
    */issues/323) echo "Failed run: $RUN_URL" ;;
    */issues/323/comments) ;;
    *) exit 24 ;;
  esac
else
  echo "$2" >> "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    stage_alert_workspace(tmp_path, progress)
    actions = tmp_path / "actions"
    result = run_workflow_script(
        workflow_step("alert", "Open, update or close the sync alert issue"), tmp_path,
        dict(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", GH_REPO="Owner/Core",
             EVENT_NAME="workflow_dispatch" if skip_discovery == "true" else "schedule",
             IS_FULL="false" if skip_discovery == "true" else "true",
             SKIP_DISCOVERY=skip_discovery, PREFLIGHT_RESULT="success",
             SYNC_RESULT="skipped" if attempt == "2" else "success", PUBLISH_RESULT="success",
             RUN_ATTEMPT=attempt, RUN_NUMBER="10",
             RUN_URL="https://github.com/Owner/Core/actions/runs/1234", MAX_CYCLE_DAYS="",
             WEEKLY_TITLE="[sync-data] Weekly full sync failed", ALERT_ORIGIN=origin,
             ALERT_ACTIONS=str(actions)),
    )
    assert result.returncode == 0, result.stderr
    assert (actions.read_text().strip() if actions.exists() else None) == action


@pytest.mark.parametrize("event,is_full,progress,preflight,sync,publish,attempt,failed_number,action", [
    # Unfinished cycles that keep advancing no longer comment on the weekly alert (#323).
    ("schedule", "true", "running", "success", "success", "success", "1", "", None),
    ("schedule", "true", "running", "success", "skipped", "success", "2", "", None),
    ("schedule", "true", "absent", "success", "skipped", "success", "2", "", None),
    ("schedule", "true", "done-new", "success", "success", "success", "1", "", "close"),
    ("schedule", "true", "done-new", "success", "success", "skipped", "1", "", None),
    ("schedule", "true", "done-new", "success", "success", "failure", "1", "", "comment"),
    ("schedule", "false", "done-old", "success", "success", "success", "1", "", "close"),
    ("schedule", "false", "done-old", "success", "skipped", "success", "2", "", "close"),
    ("schedule", "true", "done-new", "success", "skipped", "success", "2", "", "close"),
    ("schedule", "false", "done-old", "success", "skipped", "success", "1", "", None),
    ("schedule", "true", "done-new", "success", "skipped", "failure", "2", "", "comment"),
    ("schedule", "false", "done-old", "failure", "skipped", "skipped", "2", "", "comment"),
    ("schedule", "false", "done-old", "cancelled", "skipped", "skipped", "2", "", None),
    ("schedule", "false", "done-old", "success", "skipped", "success", "2", "11", None),
    ("schedule", "true", "done-new", "success", "skipped", "success", "2", "11", None),
    ("schedule", "false", "done-old", "success", "success", "success", "2", "11", None),
    ("schedule", "true", "done-new", "success", "success", "success", "2", "11", None),
    ("schedule", "false", "done-old", "success", "skipped", "success", "2", "9", "close"),
    ("schedule", "true", "done-new", "success", "skipped", "success", "2", "9", "close"),
    # A daily-bounded run after the cycle finished resolves the weekly alert.
    ("schedule", "false", "done-new", "success", "success", "success", "1", "", "close"),
    # Manual runs resolve a completed cycle but never open or comment on alerts.
    ("workflow_dispatch", "true", "done-new", "success", "success", "success", "1", "", "close"),
    ("workflow_dispatch", "false", "done-new", "success", "success", "success", "1", "", "close"),
    ("workflow_dispatch", "false", "done-old", "success", "success", "success", "1", "", None),
    ("workflow_dispatch", "true", "running", "success", "success", "success", "1", "", None),
    ("workflow_dispatch", "true", "done-new", "success", "failure", "skipped", "1", "", None),
])
def test_sync_alert_closes_only_after_complete_success(
    tmp_path, event, is_full, progress, preflight, sync, publish, attempt, failed_number, action
):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$1" = "api" ]; then
  case "$*" in
    *created_at*)
      case "$2" in
        */issues/323) echo '["2026-10-04T00:00:00Z", ""]' ;;
        */issues/323/comments) ;;
        *) exit 25 ;;
      esac
      exit 0 ;;
  esac
  case "$2" in
    */issues/323) echo "Failed run: $RUN_URL" ;;
    */issues/323/comments)
      if [ -n "$FAILED_RUN_NUMBER" ]; then
        echo "The scheduled sync failed again: https://github.com/Owner/Core/actions/runs/5678"
      fi ;;
    */actions/runs/5678)
      if [ "$FAILED_RUN_NUMBER" -gt "$RUN_NUMBER" ]; then echo true; else echo false; fi ;;
    *) exit 23 ;;
  esac
elif [ "$2" = "list" ]; then
  echo 323
else
  echo "$2" >> "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    stage_alert_workspace(tmp_path, progress)
    actions = tmp_path / "actions"
    step = workflow_step("alert", "Open, update or close the sync alert issue")
    result = subprocess.run(
        ["bash", "-e", "-c", step["run"]], cwd=tmp_path, capture_output=True, text=True,
        env=dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}",
                 EVENT_NAME=event, IS_FULL=is_full, SKIP_DISCOVERY="false", PREFLIGHT_RESULT=preflight,
                 SYNC_RESULT=sync, PUBLISH_RESULT=publish, RUN_ATTEMPT=attempt, RUN_NUMBER="10",
                 RUN_URL="https://github.com/Owner/Core/actions/runs/1234", GH_REPO="Owner/Core",
                 FAILED_RUN_NUMBER=failed_number, MAX_CYCLE_DAYS="",
                 WEEKLY_TITLE="[sync-data] Weekly full sync failed",
                 ALERT_ACTIONS=str(actions)),
    )
    assert result.returncode == 0, result.stderr
    assert (actions.read_text().strip() if actions.exists() else None) == action


@pytest.mark.parametrize("issue_exists,action", [(False, "create"), (True, None)])
def test_sync_alert_flags_overdue_cycle_once(tmp_path, issue_exists, action):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$1" = "api" ]; then
  case "$*" in *created_at*) echo '["2026-09-01T00:00:00Z", ""]'; exit 0 ;; esac
  exit 23
elif [ "$2" = "list" ]; then
  [ "$ISSUE_EXISTS" = "true" ] && echo 323
  exit 0
else
  echo "$2" >> "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    stage_alert_workspace(tmp_path, "absent")
    target = tmp_path / "latest-progress" / "sources" / "learning" / "full-discovery-progress.json"
    target.parent.mkdir(parents=True)
    target.write_text(json.dumps({"started_at": "2026-01-01T00:00:00Z", "repos": ["a/b", "c/d"],
                                  "next_repo": 1, "completed_at": None}), encoding="utf-8")
    actions = tmp_path / "actions"
    result = run_workflow_script(
        workflow_step("alert", "Open, update or close the sync alert issue"), tmp_path,
        dict(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", GH_REPO="Owner/Core",
             EVENT_NAME="schedule", IS_FULL="true", SKIP_DISCOVERY="false", PREFLIGHT_RESULT="success",
             SYNC_RESULT="success", PUBLISH_RESULT="success", RUN_ATTEMPT="1", RUN_NUMBER="10",
             RUN_URL="https://github.com/Owner/Core/actions/runs/1234", MAX_CYCLE_DAYS="",
             WEEKLY_TITLE="[sync-data] Weekly full sync failed",
             ISSUE_EXISTS=str(issue_exists).lower(), ALERT_ACTIONS=str(actions)),
    )
    assert result.returncode == 0, result.stderr
    assert (actions.read_text().strip() if actions.exists() else None) == action


@pytest.mark.parametrize("lookup_failure", ["created", "body", "comments", "run"])
def test_sync_alert_replay_lookup_failure_does_not_close(tmp_path, lookup_failure):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$2" = "list" ]; then
  echo 323
elif [ "$1" = "api" ]; then
  case "$*" in
    *created_at*)
      if [ "$LOOKUP_FAILURE" = "created" ] && [ "$2" = "repos/Owner/Core/issues/323" ]; then
        exit 23
      fi
      echo '["2026-10-04T00:00:00Z", ""]'; exit 0 ;;
  esac
  case "$2" in
    */issues/323)
      [ "$LOOKUP_FAILURE" != "body" ] || exit 23
      echo "Failed run: https://github.com/Owner/Core/actions/runs/5678" ;;
    */issues/323/comments)
      [ "$LOOKUP_FAILURE" != "comments" ] || exit 23 ;;
    */actions/runs/5678)
      [ "$LOOKUP_FAILURE" != "run" ] || exit 23
      echo false ;;
    *) exit 24 ;;
  esac
else
  touch "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    stage_alert_workspace(tmp_path, "done-old")
    actions = tmp_path / "actions"
    result = run_workflow_script(
        workflow_step("alert", "Open, update or close the sync alert issue"), tmp_path,
        dict(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", GH_REPO="Owner/Core",
             EVENT_NAME="schedule", IS_FULL="false", SKIP_DISCOVERY="false", PREFLIGHT_RESULT="success",
             SYNC_RESULT="skipped", PUBLISH_RESULT="success", RUN_ATTEMPT="2", RUN_NUMBER="10",
             RUN_URL="https://github.com/Owner/Core/actions/runs/1234", ALERT_ACTIONS=str(actions),
             MAX_CYCLE_DAYS="", WEEKLY_TITLE="[sync-data] Weekly full sync failed",
             LOOKUP_FAILURE=lookup_failure),
    )
    assert result.returncode == 23, result.stderr
    assert not actions.exists()


@pytest.mark.parametrize("attempt,sync", [("1", "success"), ("2", "skipped")])
def test_sync_alert_old_replay_preserves_newer_unfinished_cycle(tmp_path, attempt, sync):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$1" = "api" ]; then
  case "$*" in *created_at*) echo '["2026-10-04T00:00:00Z", ""]'; exit 0 ;; esac
  case "$2" in
    */issues/323) echo "Failed run: https://github.com/Owner/Core/actions/runs/1234" ;;
    */issues/323/comments) ;;
    */actions/runs/5678) echo true ;;
    *) exit 24 ;;
  esac
elif [ "$2" = "list" ]; then
  echo 323
else
  echo "$2" >> "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    # Main already holds the newer run's unfinished cycle when the old run is replayed.
    stage_alert_workspace(tmp_path, "running")
    actions = tmp_path / "actions"
    step = workflow_step("alert", "Open, update or close the sync alert issue")
    env = dict(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", GH_REPO="Owner/Core",
               EVENT_NAME="schedule", IS_FULL="true", SKIP_DISCOVERY="false", PREFLIGHT_RESULT="success",
               PUBLISH_RESULT="success", MAX_CYCLE_DAYS="",
               WEEKLY_TITLE="[sync-data] Weekly full sync failed", ALERT_ACTIONS=str(actions))
    unfinished = run_workflow_script(
        step, tmp_path, dict(env, SYNC_RESULT=sync, RUN_ATTEMPT=attempt, RUN_NUMBER="11",
                             RUN_URL="https://github.com/Owner/Core/actions/runs/5678"),
    )
    assert unfinished.returncode == 0, unfinished.stderr
    replay = run_workflow_script(
        step, tmp_path, dict(env, SYNC_RESULT="skipped", RUN_ATTEMPT="2", RUN_NUMBER="10",
                             RUN_URL="https://github.com/Owner/Core/actions/runs/1234"),
    )
    assert replay.returncode == 0, replay.stderr
    assert not actions.exists(), actions.read_text() if actions.exists() else ""


@pytest.mark.parametrize("event", ["schedule", "workflow_dispatch"])
def test_sync_alert_old_incomplete_handoff_does_not_close_new_main_completion(tmp_path, event):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    fake_gh = bin_dir / "gh"
    fake_gh.write_text(
        """#!/bin/bash
if [ "$2" = "list" ]; then
  echo 323
elif [ "$1" = "api" ]; then
  case "$*" in *created_at*) echo '["2026-10-04T00:00:00Z", ""]'; exit 0 ;; esac
  exit 24
else
  touch "$ALERT_ACTIONS"
fi
"""
    )
    fake_gh.chmod(0o755)
    stage_alert_workspace(tmp_path, "done-new", published_progress="running")
    actions = tmp_path / "actions"
    result = run_workflow_script(
        workflow_step("alert", "Open, update or close the sync alert issue"), tmp_path,
        dict(PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}", GH_REPO="Owner/Core",
             EVENT_NAME=event, IS_FULL="true", SKIP_DISCOVERY="false", PREFLIGHT_RESULT="success",
             SYNC_RESULT="skipped", PUBLISH_RESULT="success", RUN_ATTEMPT="2", RUN_NUMBER="10",
             RUN_URL="https://github.com/Owner/Core/actions/runs/1234", MAX_CYCLE_DAYS="",
             WEEKLY_TITLE="[sync-data] Weekly full sync failed", ALERT_ACTIONS=str(actions)),
    )
    assert result.returncode == 0, result.stderr
    assert not actions.exists()


def test_sync_alert_keeps_trigger_helper_when_main_advances(tmp_path):
    alert = read_workflow(".github/workflows/sync-data.yml")["jobs"]["alert"]
    checkout = next(
        step for step in alert["steps"]
        if "scripts/sync_alert_decision.py" in step.get("with", {}).get("sparse-checkout", "")
    )
    source = tmp_path / "source"
    source.mkdir()
    subprocess.run(["git", "init", "-b", "main"], cwd=source, check=True, capture_output=True)
    (source / "scripts").mkdir()
    helper = source / "scripts" / "sync_alert_decision.py"
    shutil.copy(ROOT / "scripts" / "sync_alert_decision.py", helper)
    for message in ("trigger", "advance main"):
        if message == "advance main":
            helper.write_text('raise SystemExit("incompatible newer helper")\n', encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=source, check=True, capture_output=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com",
             "commit", "-m", message], cwd=source, check=True, capture_output=True,
        )
        if message == "trigger":
            trigger_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=source, text=True).strip()
    ref = checkout["with"]["ref"].replace("${{ github.sha }}", trigger_sha)
    checked_out_helper = tmp_path / "sync_alert_decision.py"
    checked_out_helper.write_bytes(subprocess.check_output(
        ["git", "show", f"{ref}:scripts/sync_alert_decision.py"], cwd=source,
    ))
    result = subprocess.run(
        [sys.executable, str(checked_out_helper), "--event-name", "workflow_dispatch",
         "--is-full", "false"], capture_output=True, text=True,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["action"] == "none"


def test_sync_alert_reads_latest_and_published_progress_on_every_trigger():
    alert = read_workflow(".github/workflows/sync-data.yml")["jobs"]["alert"]
    assert alert["if"] == "${{ always() }}"
    helper, latest, published = alert["steps"][:3]
    assert helper["with"]["ref"] == "${{ github.sha }}"
    assert helper["with"]["sparse-checkout"] == "scripts/sync_alert_decision.py"
    for checkout in (latest, published):
        assert checkout["uses"].startswith("actions/checkout@")
        assert checkout["with"]["sparse-checkout"] == "sources/learning/full-discovery-progress.json"
    assert latest["with"]["ref"] == "main"
    assert latest["with"]["path"] == "latest-progress"
    assert published["with"]["ref"] == "${{ needs.publish.outputs.core_sha }}"
    assert published["with"]["path"] == "published-progress"
    assert published["if"] == "needs.publish.result == 'success'"
    step = workflow_step("alert", "Open, update or close the sync alert issue")
    assert step["env"]["MAX_CYCLE_DAYS"] == "${{ vars.FULL_DISCOVERY_MAX_CYCLE_DAYS }}"
    assert step["env"]["EVENT_NAME"] == "${{ github.event_name }}"
    assert step["env"]["SKIP_DISCOVERY"] == (
        "${{ github.event_name == 'workflow_dispatch' && github.event.inputs.skip_discovery == 'true' }}"
    )


def test_full_discovery_cursor_commits_after_archive_and_health_gates():
    workflow = read_repo_file(".github/workflows/sync-data.yml")
    sync = read_workflow(".github/workflows/sync-data.yml")["jobs"]["sync"]
    assert sync["env"]["FULL_DISCOVERY_PROGRESS"].startswith("sources/learning/")
    discover = workflow_step("sync", "Discover new skills from GitHub (full)")
    assert '--progress "$FULL_DISCOVERY_PROGRESS"' in discover["run"]
    assert "--time-budget-seconds 6000" in discover["run"]
    assert discover["timeout-minutes"] * 60 > 6000
    assert sync["outputs"]["full_cycle_complete"] == "${{ steps.full_progress.outputs.complete }}"
    assert "needs.sync.outputs.full_scan" in workflow_step(
        "alert", "Open, update or close the sync alert issue"
    )["env"]["IS_FULL"]
    assert "sources/" in workflow_step("sync", "Commit & push core metadata changes")["run"]
    assert workflow.index("Validate sync pipeline health") < workflow.index(
        "Commit & push data repo changes"
    ) < workflow.index("Commit & push core metadata changes")


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
        "full_scan": "false",
        "full_cycle_complete": "",
    }
    assert sorted(path.name for path in root.iterdir()) == [
        "publish-dispatch-evidence.json",
        "publish-dispatch-evidence.sha256",
        "publish-dispatch-payload.json",
    ]
    assert (root / "publish-dispatch-evidence.sha256").read_text().strip() == hashlib.sha256(
        (root / "publish-dispatch-evidence.json").read_bytes()
    ).hexdigest()


@pytest.mark.parametrize(
    "corruption",
    ["missing", "invalid_json", "hash_mismatch", "extra_key", "field_mismatch", "missing_cycle_state", "cycle_state_flip", "missing_evidence_hash"],
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
    elif corruption == "missing_cycle_state":
        evidence.pop("full_scan")
        evidence.pop("full_cycle_complete")
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    elif corruption == "cycle_state_flip":
        evidence["full_scan"] = "true"
        evidence["full_cycle_complete"] = "true"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    elif corruption == "missing_evidence_hash":
        (root / "publish-dispatch-evidence.sha256").unlink(missing_ok=True)
    else:
        payload = json.loads(payload_bytes)
        payload["client_payload"]["core_sha"] = "c" * 40
        changed_bytes = (json.dumps(payload, separators=(",", ":")) + "\n").encode()
        payload_path.write_bytes(changed_bytes)
        evidence["payload_sha256"] = hashlib.sha256(changed_bytes).hexdigest()
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    if corruption in {"invalid_json", "extra_key", "field_mismatch", "missing_cycle_state"}:
        (root / "publish-dispatch-evidence.sha256").write_text(
            hashlib.sha256(evidence_path.read_bytes()).hexdigest() + "\n", encoding="utf-8"
        )

    step = workflow_step(job_name, step_name)
    env = {
        "EXPECTED_RUN_ID": "1234",
        "EXPECTED_CORE_REPO": "Owner/Core",
        "EXPECTED_DATA_REPO": "Owner/Data",
        "EXPECTED_TARGET_REPO": "Owner/Main",
    }
    result = run_workflow_script(step, tmp_path, env)

    assert result.returncode != 0


@pytest.mark.parametrize("full_scan,complete", [
    ("false", ""), ("true", "false"), ("true", "true"),
])
def test_sync_data_preflight_replay_validator_executes_and_accepts_valid_handoff(
    tmp_path, full_scan, complete
):
    root, _, _ = build_valid_handoff(tmp_path, full_scan, complete)
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


@pytest.mark.parametrize("full_scan,complete", [
    ("false", ""), ("true", "false"), ("true", "true"),
])
def test_sync_data_handoff_validator_executes_and_exports_verified_fields(
    tmp_path, full_scan, complete
):
    _, _, evidence = build_valid_handoff(tmp_path, full_scan, complete)
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
        for key in ("target_repo", "core_sha", "data_sha", "payload_sha256", "full_scan", "full_cycle_complete")
    }

    publish = read_workflow(".github/workflows/sync-data.yml")["jobs"]["publish"]
    assert publish["outputs"] == {
        key: "${{ steps.handoff.outputs." + key + " }}"
        for key in ("core_sha", "full_scan", "full_cycle_complete")
    }
    handoff = workflow_step("sync", "Build immutable publish handoff")
    assert handoff["env"]["FULL_SCAN"] == "${{ steps.discovery.outputs.profile == 'full' }}"
    assert handoff["env"]["FULL_CYCLE_COMPLETE"] == "${{ steps.full_progress.outputs.complete }}"
    alert = workflow_step("alert", "Open, update or close the sync alert issue")
    assert alert["env"]["IS_FULL"] == (
        "${{ needs.sync.outputs.full_scan == 'true' || needs.publish.outputs.full_scan == 'true' "
        "|| github.event.schedule == '30 2 * * 0' }}"
    )
    assert alert["env"]["RUN_ATTEMPT"] == "${{ github.run_attempt }}"
    assert alert["env"]["RUN_NUMBER"] == "${{ github.run_number }}"


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
