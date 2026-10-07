"""Main-owned security contracts for the main-owned publish workflow."""

import json
import os
import subprocess
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def read_repo_file(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def run_workflow_script(step: dict, tmp_path: Path, env: dict[str, str]):
    (tmp_path / "runner-temp").mkdir()
    output = tmp_path / "github-output"
    output.touch()
    return subprocess.run(
        ["bash", "-c", step["run"]],
        cwd=tmp_path,
        env={
            **os.environ,
            **env,
            "RUNNER_TEMP": str(tmp_path / "runner-temp"),
            "GITHUB_OUTPUT": str(output),
        },
        capture_output=True,
        text=True,
        check=False,
    )


def load_workflow(path: str) -> dict:
    return yaml.safe_load(read_repo_file(path))


def publish_from_core_step(step_name: str) -> dict:
    workflow = load_workflow(".github/workflows/publish-from-core.yml")
    return next(step for step in workflow["jobs"]["publish"]["steps"] if step["name"] == step_name)


def parse_github_output(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    outputs: dict[str, str] = {}
    lines = text.splitlines()
    index = 0
    while index < len(lines):
        line = lines[index]
        if "<<" in line:
            name, delim = line.split("<<", 1)
            index += 1
            chunks: list[str] = []
            while index < len(lines) and lines[index] != delim:
                chunks.append(lines[index])
                index += 1
            assert index < len(lines), f"unterminated multiline output for {name}"
            outputs[name] = "\n".join(chunks)
            index += 1
            continue
        if "=" in line:
            name, value = line.split("=", 1)
            outputs[name] = value
        index += 1
    return outputs


def valid_publish_ref_env() -> dict[str, str]:
    return {
        "PAYLOAD_CORE_REPO": "",
        "PAYLOAD_CORE_SHA": "",
        "PAYLOAD_DATA_REPO": "",
        "PAYLOAD_DATA_SHA": "",
        "INPUT_CORE_REPO": "majiayu000/claude-skill-registry-core",
        "INPUT_CORE_SHA": "a" * 40,
        "INPUT_DATA_REPO": "majiayu000/claude-skill-registry-data",
        "INPUT_DATA_SHA": "b" * 40,
        "DEFAULT_DATA_REPO": "majiayu000/claude-skill-registry-data",
        "ALLOWED_CORE_REPO": "majiayu000/claude-skill-registry-core",
        "ALLOWED_DATA_REPO": "majiayu000/claude-skill-registry-data",
    }


def test_publish_from_core_checks_out_current_main_and_pinned_sources():
    # A queued dispatch may carry an old event SHA after main has advanced.
    main = publish_from_core_step("Checkout main")
    assert main["with"]["ref"] == "main"
    # History is not needed: provenance comes from the checked-out file and the
    # push step fetches newer main commits before retrying.
    assert main["with"]["fetch-depth"] == 1

    for source in ("core", "data"):
        pinned = publish_from_core_step(f"Checkout pinned {source}")
        assert pinned["with"]["ref"] == "${{ steps.refs.outputs." + source + "_sha }}"


def test_publish_from_core_workflow_parses_and_hardens_publish_refs():
    workflow_text = read_repo_file(".github/workflows/publish-from-core.yml")
    workflow = yaml.safe_load(workflow_text)
    resolve = publish_from_core_step("Resolve publish refs")
    provenance = publish_from_core_step("Write provenance manifest")

    assert workflow["name"] == "Publish Merged Artifact (From Core)"
    assert resolve["env"]["ALLOWED_CORE_REPO"] == "majiayu000/claude-skill-registry-core"
    assert resolve["env"]["ALLOWED_DATA_REPO"] == "majiayu000/claude-skill-registry-data"
    assert "^[0-9a-f]{40}$" in resolve["run"]
    assert 'printf \'%s<<%s\\n\' "$name" "$delim"' in resolve["run"]
    assert 'echo "core_repo=$core_repo" >> "$GITHUB_OUTPUT"' not in resolve["run"]
    assert provenance["env"]["CORE_REPO"] == "${{ steps.refs.outputs.core_repo }}"
    assert "python3 - <<'PY'" in provenance["run"]
    assert "json.dumps(payload" in provenance["run"]
    assert "cat > provenance/merge-source.json <<EOF" not in provenance["run"]
    assert '"core_repo": "${{ steps.refs.outputs.core_repo }}"' not in provenance["run"]


@pytest.mark.parametrize("source", ["INPUT", "PAYLOAD"])
@pytest.mark.parametrize(
    ("updates", "expected_error"),
    [
        (
            {"INPUT_CORE_REPO": 'evil/repo; touch "$RUNNER_TEMP/pwned"'},
            "Rejected core_repo (not allowlisted)",
        ),
        (
            {"INPUT_DATA_REPO": "majiayu000/claude-skill-registry-core"},
            "Rejected data_repo (not allowlisted)",
        ),
        (
            {"INPUT_CORE_SHA": "deadbeef"},
            "Invalid core_sha (want 40-char lowercase hex)",
        ),
        (
            {"INPUT_DATA_SHA": "A" * 40},
            "Invalid data_sha (want 40-char lowercase hex)",
        ),
        (
            {"INPUT_CORE_SHA": "a" * 39 + "g"},
            "Invalid core_sha (want 40-char lowercase hex)",
        ),
        (
            {
                "INPUT_CORE_REPO": "majiayu000/claude-skill-registry-core\ninjected=1",
                "INPUT_CORE_SHA": "a" * 40,
            },
            "Rejected core_repo (not allowlisted)",
        ),
        (
            {
                "INPUT_CORE_SHA": "a" * 40 + '; $(touch "$RUNNER_TEMP/pwned")',
            },
            "Invalid core_sha (want 40-char lowercase hex)",
        ),
    ],
)
def test_publish_from_core_resolve_refs_rejects_malicious_inputs(
    tmp_path, source, updates, expected_error
):
    step = publish_from_core_step("Resolve publish refs")
    env = valid_publish_ref_env()
    env.update({key.replace("INPUT_", f"{source}_"): value for key, value in updates.items()})

    result = run_workflow_script(step, tmp_path, env)

    assert result.returncode != 0
    assert expected_error in result.stdout + result.stderr
    assert not (tmp_path / "runner-temp" / "pwned").exists()
    assert (tmp_path / "github-output").read_text(encoding="utf-8") == ""


@pytest.mark.parametrize("source", ["INPUT", "PAYLOAD"])
def test_publish_from_core_resolve_refs_accepts_allowlisted_refs_with_safe_output(tmp_path, source):
    step = publish_from_core_step("Resolve publish refs")
    env = {
        key.replace("INPUT_", f"{source}_"): value for key, value in valid_publish_ref_env().items()
    }

    result = run_workflow_script(step, tmp_path, env)
    outputs = parse_github_output(tmp_path / "github-output")

    assert result.returncode == 0, result.stdout + result.stderr
    assert outputs == {
        "core_repo": "majiayu000/claude-skill-registry-core",
        "core_sha": "a" * 40,
        "data_repo": "majiayu000/claude-skill-registry-data",
        "data_sha": "b" * 40,
    }
    raw = (tmp_path / "github-output").read_text(encoding="utf-8")
    assert "core_repo<<" in raw
    assert "core_sha<<" in raw


def test_publish_from_core_provenance_write_is_non_interpolating(tmp_path):
    step = publish_from_core_step("Write provenance manifest")
    env = {
        "CORE_REPO": "majiayu000/claude-skill-registry-core",
        "CORE_SHA": "a" * 40,
        "DATA_REPO": 'majiayu000/claude-skill-registry-data$(touch "$RUNNER_TEMP/pwned")',
        "DATA_SHA": "b" * 40,
    }

    result = run_workflow_script(step, tmp_path, env)
    provenance = json.loads((tmp_path / "provenance" / "merge-source.json").read_text())

    assert result.returncode == 0, result.stdout + result.stderr
    assert provenance["core_repo"] == env["CORE_REPO"]
    assert provenance["core_sha"] == env["CORE_SHA"]
    assert provenance["data_repo"] == env["DATA_REPO"]
    assert provenance["data_sha"] == env["DATA_SHA"]
    assert not (tmp_path / "runner-temp" / "pwned").exists()
    assert "<<EOF" not in step["run"]
    assert "<<'PY'" in step["run"]


def test_publish_builds_from_data_checkout_without_skills_mirror():
    rebuild = publish_from_core_step("Rebuild main from pinned refs")
    canary = publish_from_core_step("Validate canary artifact and write publish status")
    commit = publish_from_core_step("Commit and push publish result")

    assert "--no-skills-mirror" in rebuild["run"]
    assert canary["env"]["ARCHIVE_DIR"] == "${{ steps.srcpaths.outputs.data_dir }}"
    assert "main still tracks a skills/ mirror" in canary["run"]
    assert "git add -f" not in commit["run"]


def test_publish_deploys_pages_from_publish_workspace_after_push():
    workflow = load_workflow(".github/workflows/publish-from-core.yml")
    steps = [step["name"] for step in workflow["jobs"]["publish"]["steps"]]
    upload = publish_from_core_step("Upload Pages artifact from the publish workspace")

    assert steps.index("Upload Pages artifact from the publish workspace") > steps.index(
        "Commit and push publish result"
    )
    assert upload["uses"].startswith("actions/upload-pages-artifact@")
    assert upload["with"]["path"] == "docs"
    assert "if" not in upload

    deploy = workflow["jobs"]["deploy-site"]
    assert deploy["needs"] == "publish"
    assert deploy["permissions"] == {"pages": "write", "id-token": "write"}
    assert deploy["environment"]["name"] == "github-pages"
    assert deploy["concurrency"]["group"] == "github-pages"
    assert [step["uses"].split("@")[0] for step in deploy["steps"]] == ["actions/deploy-pages"]
    assert "gh workflow run" not in read_repo_file(".github/workflows/publish-from-core.yml")


def test_deploy_pages_workflow_never_publishes_an_incomplete_checkout():
    workflow = load_workflow(".github/workflows/deploy-pages.yml")
    triggers = workflow[True] if True in workflow else workflow["on"]
    steps = [step["name"] for step in workflow["jobs"]["deploy"]["steps"]]

    assert set(triggers) == {"workflow_dispatch"}
    assert steps.index("Refuse to deploy an incomplete site") < steps.index("Upload Pages artifact")


@pytest.mark.parametrize(
    ("path", "ignored"),
    [
        ("skills/development/example/SKILL.md", True),
        ("docs/security-shards/part-000.json", True),
        ("docs/quality-shards/part-000.json.gz", True),
        ("docs/ranking-index-manifest.json", True),
        ("docs/skill-detail-shards/a.json", True),
        ("docs/skills/example/index.html", True),
        ("docs/search-index-lite.json.gz", True),
        ("registry.json", False),
        ("registry-manifest.json", False),
        ("registry-shards/00.json.gz", False),
        ("docs/featured.json", False),
        ("docs/categories/index.json", False),
        ("docs/categories/agent/part-000.json.gz", False),
        ("docs/search-index.json", False),
        ("docs/search-index.json.gz", False),
        ("docs/search-index-manifest.json", False),
        ("docs/search-shards/part-000.json", False),
        ("docs/index.html", False),
        ("docs/js/app.js", False),
        ("provenance/merge-source.json", False),
    ],
)
def test_gitignore_keeps_raw_consumer_paths_and_drops_pages_only_artifacts(path, ignored):
    result = subprocess.run(
        ["git", "check-ignore", "--no-index", "-q", path],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode in (0, 1), result.stderr
    assert (result.returncode == 0) is ignored


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True
    ).stdout.strip()


def _commit_file(repo: Path, name: str, content: str, message: str) -> None:
    (repo / name).write_text(content, encoding="utf-8")
    _git(repo, "add", name)
    _git(repo, "-c", "user.email=t@example.com", "-c", "user.name=t", "commit", "-qm", message)


def _push_race_fixture(tmp_path: Path, concurrent_file: str) -> Path:
    remote = tmp_path / "remote.git"
    seed = tmp_path / "seed"
    _git(tmp_path, "init", "-q", "--bare", "-b", "main", str(remote))
    _git(tmp_path, "clone", "-q", str(remote), str(seed))
    _commit_file(seed, "registry.json", "old\n", "seed")
    _commit_file(seed, "README.md", "readme\n", "seed readme")
    _git(seed, "push", "-q", "origin", "HEAD:main")

    work = tmp_path / "work"
    _git(tmp_path, "clone", "-q", "--depth=1", f"file://{remote}", str(work))
    (work / "registry.json").write_text("published\n", encoding="utf-8")

    _commit_file(seed, concurrent_file, "concurrent\n", "concurrent main change")
    _git(seed, "push", "-q", "origin", "HEAD:main")
    return work


def _run_commit_step(tmp_path: Path, work: Path):
    step = publish_from_core_step("Commit and push publish result")
    runner_temp = tmp_path / "runner-temp"
    runner_temp.mkdir()
    (runner_temp / "publish-commit-message.txt").write_text("chore: publish\n", encoding="utf-8")
    stub_bin = tmp_path / "bin"
    stub_bin.mkdir()
    sleep = stub_bin / "sleep"
    sleep.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
    sleep.chmod(0o755)
    return subprocess.run(
        ["bash", "-c", step["run"]],
        cwd=work,
        env={
            **os.environ,
            "PATH": f"{stub_bin}{os.pathsep}{os.environ['PATH']}",
            "RUNNER_TEMP": str(runner_temp),
            "CORE_SHA": "a" * 40,
            "DATA_SHA": "b" * 40,
        },
        capture_output=True,
        text=True,
        check=False,
    )


def test_publish_push_rebases_onto_concurrent_main_change(tmp_path):
    work = _push_race_fixture(tmp_path, "CHANGELOG.md")

    result = _run_commit_step(tmp_path, work)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Push succeeded on attempt 2" in result.stdout
    remote = tmp_path / "remote.git"
    assert _git(remote, "log", "-1", "--format=%s", "main") == "chore: publish"
    assert _git(remote, "log", "-1", "--format=%s", "main~1") == "concurrent main change"
    assert _git(remote, "show", "main:registry.json") == "published"


def test_publish_push_fails_closed_on_conflicting_concurrent_change(tmp_path):
    work = _push_race_fixture(tmp_path, "registry.json")

    result = _run_commit_step(tmp_path, work)

    assert result.returncode == 1
    assert "rerun the publish" in result.stdout
    assert _git(tmp_path / "remote.git", "show", "main:registry.json") == "concurrent"
    assert not (work / ".git" / "rebase-merge").exists()
