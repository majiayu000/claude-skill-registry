from __future__ import annotations

import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import check_coverage_ratchet as ratchet  # noqa: E402

MODULES = ["scripts/discover_plugins.py", "scripts/plugin_index.py"]
CRITICAL = {
    "scripts/discover_plugins.py": [
        "_run_command",
        "_load_json",
        "npm_search",
        "npm_view",
        "inspect_repo_structure",
        "get_install_command",
        "load_existing_plugins",
        "_load_registry_repos",
        "discover_from_registry",
        "derive_status",
        "run_discovery",
        "write_discovery_report",
        "main",
    ],
    "scripts/plugin_index.py": ["_validate_plugins"],
}


def _summary(line=100.0, branch=100.0):
    return {
        "percent_statements_covered": line,
        "percent_branches_covered": branch,
    }


def _baseline(global_line=66.0):
    return {
        "schema_version": 1,
        "recorded_commit": "a" * 40,
        "global_line_percent": global_line,
        "module_line_minimums": dict.fromkeys(MODULES, 80.0),
        "critical_functions": deepcopy(CRITICAL),
    }


def _coverage(global_line=90.0):
    files = {}
    for path in MODULES:
        files[path] = {
            "summary": _summary(90.0, 90.0),
            "functions": {name: {"summary": _summary()} for name in CRITICAL[path]},
        }
    return {
        "totals": {"percent_statements_covered": global_line},
        "files": files,
    }


def _config(*, sources=None, run=None, report=None):
    run_config = {"branch": True, "source": sources or ["scripts", "crawler"]}
    run_config.update(run or {})
    return {
        "tool": {
            "pytest": {
                "ini_options": {
                    "addopts": "--cov=scripts --cov=crawler --cov-report=term-missing"
                }
            },
            "coverage": {
                "run": run_config,
                "report": report
                or {
                    "exclude_lines": [
                        "pragma: no cover",
                        "if __name__ == .__main__.:",
                        "raise NotImplementedError",
                    ]
                },
            }
        }
    }


def _policy_coverage(*files):
    return {
        "meta": {"branch_coverage": True},
        "files": {path: {} for path in files},
    }


def test_validate_coverage_accepts_all_gates():
    assert ratchet.validate_coverage(_coverage(), _baseline()) == []


def test_validate_coverage_reports_global_regression():
    errors = ratchet.validate_coverage(_coverage(global_line=65.9), _baseline(global_line=66.0))
    assert any("global line coverage" in error for error in errors)


def test_validate_coverage_reports_module_below_target():
    coverage = _coverage()
    coverage["files"][MODULES[0]]["summary"]["percent_statements_covered"] = 79.9
    errors = ratchet.validate_coverage(coverage, _baseline())
    assert any(MODULES[0] in error and "below" in error for error in errors)


@pytest.mark.parametrize(("key", "value"), [("percent_statements_covered", 99.0), ("percent_branches_covered", 99.0)])
def test_validate_coverage_reports_critical_function_gap(key, value):
    coverage = _coverage()
    function = coverage["files"][MODULES[0]]["functions"][CRITICAL[MODULES[0]][0]]
    function["summary"][key] = value
    errors = ratchet.validate_coverage(coverage, _baseline())
    assert any("critical function" in error for error in errors)


def test_validate_coverage_reports_missing_module_and_function():
    coverage = _coverage()
    del coverage["files"][MODULES[0]]
    del coverage["files"][MODULES[1]]["functions"][CRITICAL[MODULES[1]][0]]
    errors = ratchet.validate_coverage(coverage, _baseline())
    assert any("missing module" in error for error in errors)
    assert any("missing critical function" in error for error in errors)


def test_validate_coverage_rejects_baseline_lowering():
    current = _baseline(global_line=65.0)
    current["module_line_minimums"][MODULES[0]] = 80.0
    current["critical_functions"][MODULES[0]] = current["critical_functions"][MODULES[0]][:1]
    previous = _baseline(global_line=66.0)
    previous["module_line_minimums"][MODULES[0]] = 85.0
    errors = ratchet.validate_coverage(
        _coverage(), current, previous_baseline=previous
    )
    assert any("baseline cannot decrease" in error for error in errors)
    assert any("module coverage minimum cannot decrease" in error for error in errors)
    assert any("critical function coverage set cannot shrink" in error for error in errors)


@pytest.mark.parametrize(
    "mutation",
    [
        lambda baseline: baseline.update(schema_version=2),
        lambda baseline: baseline.update(recorded_commit="short"),
        lambda baseline: baseline.update(recorded_commit="z" * 40),
        lambda baseline: baseline.update(global_line_percent="high"),
        lambda baseline: baseline.update(module_line_minimums={}),
        lambda baseline: baseline.update(critical_functions={}),
        lambda baseline: baseline["module_line_minimums"].update({MODULES[0]: 79.0}),
    ],
)
def test_validate_baseline_rejects_invalid_contract(mutation):
    baseline = _baseline()
    mutation(baseline)
    with pytest.raises(ratchet.CoverageRatchetError):
        ratchet.validate_baseline(baseline)


def test_load_json_object_rejects_malformed_and_nonobject(tmp_path):
    path = tmp_path / "data.json"
    path.write_text("{", encoding="utf-8")
    with pytest.raises(ratchet.CoverageRatchetError):
        ratchet.load_json_object(path)
    path.write_text("[]", encoding="utf-8")
    with pytest.raises(ratchet.CoverageRatchetError):
        ratchet.load_json_object(path)


def test_load_previous_baseline_missing_and_valid(monkeypatch):
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1, "", "missing"),
    )
    assert ratchet.load_previous_baseline("origin/main", Path("coverage-baseline.json")) is None

    payload = _baseline()
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, json.dumps(payload), ""),
    )
    assert ratchet.load_previous_baseline("origin/main", Path("coverage-baseline.json")) == payload


def test_validate_recorded_commit_pass_and_fail(monkeypatch):
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 0, "", ""),
    )
    assert ratchet.validate_recorded_commit(_baseline(), "origin/main") == []
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1, "", ""),
    )
    assert "not an ancestor" in ratchet.validate_recorded_commit(
        _baseline(), "origin/main"
    )[0]


def test_validate_coverage_policy_accepts_complete_unchanged_scope(tmp_path):
    for path in [tmp_path / "scripts" / "a.py", tmp_path / "crawler" / "b.py"]:
        path.parent.mkdir(exist_ok=True)
        path.write_text("value = 1\n", encoding="utf-8")
    config = _config()
    coverage = _policy_coverage("scripts/a.py", "crawler/b.py")

    assert ratchet.validate_coverage_policy(
        coverage,
        config,
        deepcopy(config),
        repo_root=tmp_path,
    ) == []


@pytest.mark.parametrize(
    ("mutate", "expected"),
    [
        (
            lambda config: config["tool"]["coverage"]["run"].update(source=["scripts"]),
            "source scope cannot narrow",
        ),
        (
            lambda config: config["tool"]["coverage"]["run"].update(omit=["scripts/risky.py"]),
            "omit patterns cannot expand",
        ),
        (
            lambda config: config["tool"]["coverage"]["report"]["exclude_lines"].append(
                "def risky"
            ),
            "exclude_lines patterns cannot expand",
        ),
        (
            lambda config: config["tool"]["coverage"]["report"].update(
                exclude_also=["raise SecurityError"]
            ),
            "exclude_also patterns cannot expand",
        ),
        (
            lambda config: config["tool"]["coverage"]["run"].update(
                include=["scripts/safe.py"]
            ),
            "include scope cannot change",
        ),
        (
            lambda config: config["tool"]["coverage"]["run"].update(branch=False),
            "branch measurement must remain enabled",
        ),
        (
            lambda config: config["tool"]["pytest"]["ini_options"].update(
                addopts="--cov=scripts --cov-report=term-missing"
            ),
            "pytest coverage source arguments cannot narrow",
        ),
        (
            lambda config: config["tool"]["pytest"]["ini_options"].update(
                addopts="--cov=scripts --cov=crawler --cov-config=unsafe.ini"
            ),
            "cannot override the audited coverage configuration",
        ),
    ],
)
def test_validate_coverage_policy_rejects_bypass_config(tmp_path, mutate, expected):
    for path in [tmp_path / "scripts" / "a.py", tmp_path / "crawler" / "b.py"]:
        path.parent.mkdir(exist_ok=True)
        path.write_text("value = 1\n", encoding="utf-8")
    recorded = _config()
    current = deepcopy(recorded)
    mutate(current)

    errors = ratchet.validate_coverage_policy(
        _policy_coverage("scripts/a.py", "crawler/b.py"),
        current,
        recorded,
        repo_root=tmp_path,
    )

    assert any(expected in error for error in errors)


def test_validate_coverage_policy_rejects_narrowed_evidence(tmp_path):
    for path in [tmp_path / "scripts" / "a.py", tmp_path / "crawler" / "b.py"]:
        path.parent.mkdir(exist_ok=True)
        path.write_text("value = 1\n", encoding="utf-8")

    errors = ratchet.validate_coverage_policy(
        _policy_coverage("scripts/a.py"),
        _config(),
        _config(),
        repo_root=tmp_path,
    )

    assert any("narrowed source files" in error and "crawler/b.py" in error for error in errors)


def test_validate_coverage_policy_requires_branch_evidence(tmp_path):
    (tmp_path / "scripts").mkdir()
    (tmp_path / "crawler").mkdir()
    coverage = _policy_coverage()
    coverage["meta"]["branch_coverage"] = False

    errors = ratchet.validate_coverage_policy(
        coverage,
        _config(),
        _config(),
        repo_root=tmp_path,
    )

    assert "coverage evidence must include branch measurement" in errors


def test_validate_no_new_coverage_pragmas_rejects_added_annotation(monkeypatch):
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0],
            0,
            "diff --git a/scripts/a.py b/scripts/a.py\n+value = 1  # pragma: no cover\n",
            "",
        ),
    )

    assert ratchet.validate_no_new_coverage_pragmas("a" * 40, ["scripts"]) == [
        "new pragma: no cover annotations are forbidden in measured source"
    ]


def test_validate_no_new_coverage_pragmas_accepts_context_only(monkeypatch):
    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(
            args[0],
            0,
            " value = 1  # pragma: no cover\n+value = 2\n",
            "",
        ),
    )
    assert ratchet.validate_no_new_coverage_pragmas("a" * 40, ["scripts"]) == []


def test_load_toml_object_and_git_toml_fail_closed(monkeypatch, tmp_path):
    path = tmp_path / "pyproject.toml"
    path.write_text("[tool.coverage.run]\nbranch = true\n", encoding="utf-8")
    assert ratchet.load_toml_object(path)["tool"]["coverage"]["run"]["branch"] is True

    path.write_text("[", encoding="utf-8")
    with pytest.raises(ratchet.CoverageRatchetError):
        ratchet.load_toml_object(path)

    monkeypatch.setattr(
        ratchet.subprocess,
        "run",
        lambda *args, **kwargs: subprocess.CompletedProcess(args[0], 1, "", "missing"),
    )
    with pytest.raises(ratchet.CoverageRatchetError):
        ratchet.load_git_toml("a" * 40, Path("pyproject.toml"))
