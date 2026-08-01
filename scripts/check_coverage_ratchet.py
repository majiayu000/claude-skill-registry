#!/usr/bin/env python3
"""Fail closed on global, module, and critical-function coverage regressions."""

from __future__ import annotations

import argparse
import json
import shlex
import string
import subprocess
from pathlib import Path
from typing import Any, Sequence

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility for this CI-only tool.
    import tomli as tomllib


class CoverageRatchetError(ValueError):
    """Invalid baseline or coverage evidence."""


def load_json_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise CoverageRatchetError(f"unable to read JSON object {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CoverageRatchetError(f"expected JSON object: {path}")
    return payload


def load_toml_object(path: Path) -> dict[str, Any]:
    try:
        payload = tomllib.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise CoverageRatchetError(f"unable to read TOML object {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CoverageRatchetError(f"expected TOML object: {path}")
    return payload


def load_git_toml(ref: str, path: Path) -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{ref}:{path.as_posix()}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise CoverageRatchetError(f"unable to read {path} at {ref}")
    try:
        payload = tomllib.loads(result.stdout)
    except tomllib.TOMLDecodeError as exc:
        raise CoverageRatchetError(f"malformed {path} at {ref}: {exc}") from exc
    if not isinstance(payload, dict):
        raise CoverageRatchetError(f"expected TOML object at {ref}:{path}")
    return payload


def _coverage_config(config: dict[str, Any], context: str) -> dict[str, Any]:
    tool = config.get("tool")
    coverage = tool.get("coverage") if isinstance(tool, dict) else None
    if not isinstance(coverage, dict):
        raise CoverageRatchetError(f"{context} must define tool.coverage")
    return coverage


def _string_list(section: dict[str, Any], key: str, context: str) -> list[str]:
    value = section.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise CoverageRatchetError(f"{context}.{key} must be a string list")
    return value


def _pytest_addopts(config: dict[str, Any], context: str) -> list[str]:
    tool = config.get("tool")
    pytest_config = tool.get("pytest") if isinstance(tool, dict) else None
    ini_options = pytest_config.get("ini_options") if isinstance(pytest_config, dict) else None
    addopts = ini_options.get("addopts", "") if isinstance(ini_options, dict) else ""
    if not isinstance(addopts, str):
        raise CoverageRatchetError(f"{context} pytest addopts must be a string")
    return shlex.split(addopts)


def validate_coverage_policy(
    coverage: dict[str, Any],
    current_config: dict[str, Any],
    recorded_config: dict[str, Any],
    *,
    repo_root: Path,
) -> list[str]:
    """Reject configuration and evidence changes that can inflate coverage."""
    errors: list[str] = []
    current_coverage = _coverage_config(current_config, "current pyproject")
    recorded_coverage = _coverage_config(recorded_config, "recorded pyproject")
    current_run = current_coverage.get("run")
    recorded_run = recorded_coverage.get("run")
    if not isinstance(current_run, dict) or not isinstance(recorded_run, dict):
        raise CoverageRatchetError("tool.coverage.run must be an object")
    if current_run.get("branch") is not True:
        errors.append("coverage branch measurement must remain enabled")

    current_sources = _string_list(current_run, "source", "current tool.coverage.run")
    recorded_sources = _string_list(recorded_run, "source", "recorded tool.coverage.run")
    missing_sources = sorted(set(recorded_sources) - set(current_sources))
    if missing_sources:
        errors.append(f"coverage source scope cannot narrow: {', '.join(missing_sources)}")

    current_addopts = _pytest_addopts(current_config, "current pyproject")
    recorded_addopts = _pytest_addopts(recorded_config, "recorded pyproject")
    current_cov_targets = {option for option in current_addopts if option.startswith("--cov=")}
    recorded_cov_targets = {option for option in recorded_addopts if option.startswith("--cov=")}
    if not recorded_cov_targets.issubset(current_cov_targets):
        errors.append("pytest coverage source arguments cannot narrow")
    if any(option.startswith("--cov-config") for option in current_addopts):
        errors.append("pytest cannot override the audited coverage configuration")

    section_names = set(recorded_coverage) | set(current_coverage)
    for section_name in sorted(section_names):
        current_section = current_coverage.get(section_name, {})
        recorded_section = recorded_coverage.get(section_name, {})
        if not isinstance(current_section, dict) or not isinstance(recorded_section, dict):
            raise CoverageRatchetError(f"tool.coverage.{section_name} must be an object")
        for key in ("omit", "exclude_lines", "exclude_also"):
            current_values = _string_list(
                current_section,
                key,
                f"current tool.coverage.{section_name}",
            )
            recorded_values = _string_list(
                recorded_section,
                key,
                f"recorded tool.coverage.{section_name}",
            )
            added = sorted(set(current_values) - set(recorded_values))
            if added:
                errors.append(
                    f"coverage {key} patterns cannot expand in {section_name}: "
                    + ", ".join(added)
                )
        current_include = _string_list(
            current_section,
            "include",
            f"current tool.coverage.{section_name}",
        )
        recorded_include = _string_list(
            recorded_section,
            "include",
            f"recorded tool.coverage.{section_name}",
        )
        if current_include != recorded_include:
            errors.append(f"coverage include scope cannot change in {section_name}")

    meta = coverage.get("meta")
    files = coverage.get("files")
    if not isinstance(meta, dict) or meta.get("branch_coverage") is not True:
        errors.append("coverage evidence must include branch measurement")
    if not isinstance(files, dict):
        raise CoverageRatchetError("coverage JSON files must be an object")
    required_files: set[str] = set()
    for source in current_sources:
        source_path = repo_root / source
        if not source_path.is_dir():
            errors.append(f"coverage source root does not exist: {source}")
            continue
        required_files.update(
            path.relative_to(repo_root).as_posix()
            for path in source_path.rglob("*.py")
            if "__pycache__" not in path.parts
        )
    missing_files = sorted(required_files - set(files))
    if missing_files:
        preview = ", ".join(missing_files[:5])
        suffix = f" (+{len(missing_files) - 5} more)" if len(missing_files) > 5 else ""
        errors.append(f"coverage evidence has narrowed source files: {preview}{suffix}")
    return errors


def validate_no_new_coverage_pragmas(
    recorded_commit: str,
    source_roots: Sequence[str],
) -> list[str]:
    forbidden_annotation = "pragma:" + " no cover"
    result = subprocess.run(
        [
            "git",
            "diff",
            "--unified=0",
            "--no-ext-diff",
            recorded_commit,
            "--",
            *source_roots,
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise CoverageRatchetError("unable to inspect source diff for coverage pragmas")
    added_pragmas = [
        line
        for line in result.stdout.splitlines()
        if line.startswith("+")
        and not line.startswith("+++")
        and forbidden_annotation in line.lower()
    ]
    if added_pragmas:
        return [f"new {forbidden_annotation} annotations are forbidden in measured source"]
    return []


def _number(payload: dict[str, Any], key: str, context: str) -> float:
    value = payload.get(key)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise CoverageRatchetError(f"{context}.{key} must be numeric")
    return float(value)


def validate_baseline(baseline: dict[str, Any]) -> None:
    if baseline.get("schema_version") != 1:
        raise CoverageRatchetError("coverage baseline schema_version must be 1")
    commit = baseline.get("recorded_commit")
    if (
        not isinstance(commit, str)
        or len(commit) != 40
        or any(character not in string.hexdigits for character in commit)
    ):
        raise CoverageRatchetError("coverage baseline recorded_commit must be a full SHA")
    _number(baseline, "global_line_percent", "baseline")
    module_minimums = baseline.get("module_line_minimums")
    critical_functions = baseline.get("critical_functions")
    if not isinstance(module_minimums, dict) or not module_minimums:
        raise CoverageRatchetError("coverage baseline module_line_minimums must be an object")
    if not isinstance(critical_functions, dict) or not critical_functions:
        raise CoverageRatchetError("coverage baseline critical_functions must be an object")
    for path, minimum in module_minimums.items():
        if not isinstance(path, str) or isinstance(minimum, bool) or not isinstance(
            minimum, (int, float)
        ):
            raise CoverageRatchetError("invalid module coverage minimum")
        if float(minimum) < 80.0:
            raise CoverageRatchetError(f"module minimum cannot be below 80: {path}")
    for path, functions in critical_functions.items():
        if not isinstance(path, str) or not isinstance(functions, list) or not functions:
            raise CoverageRatchetError("invalid critical function mapping")
        if any(not isinstance(function, str) or not function for function in functions):
            raise CoverageRatchetError(f"invalid critical function name: {path}")


def validate_coverage(
    coverage: dict[str, Any],
    baseline: dict[str, Any],
    *,
    previous_baseline: dict[str, Any] | None = None,
) -> list[str]:
    validate_baseline(baseline)
    errors: list[str] = []
    totals = coverage.get("totals")
    files = coverage.get("files")
    if not isinstance(totals, dict) or not isinstance(files, dict):
        raise CoverageRatchetError("coverage JSON must contain totals and files objects")

    current_global = _number(totals, "percent_statements_covered", "coverage.totals")
    required_global = _number(baseline, "global_line_percent", "baseline")
    if current_global + 1e-9 < required_global:
        errors.append(
            f"global line coverage {current_global:.6f}% is below baseline "
            f"{required_global:.6f}%"
        )

    module_minimums = baseline["module_line_minimums"]
    for path, minimum in module_minimums.items():
        file_data = files.get(path)
        if not isinstance(file_data, dict) or not isinstance(file_data.get("summary"), dict):
            errors.append(f"coverage evidence is missing module: {path}")
            continue
        current = _number(file_data["summary"], "percent_statements_covered", path)
        if current + 1e-9 < float(minimum):
            errors.append(f"{path} line coverage {current:.6f}% is below {float(minimum):.6f}%")

    for path, function_names in baseline["critical_functions"].items():
        file_data = files.get(path)
        functions = file_data.get("functions") if isinstance(file_data, dict) else None
        if not isinstance(functions, dict):
            errors.append(f"coverage evidence is missing function data: {path}")
            continue
        for function_name in function_names:
            function = functions.get(function_name)
            if not isinstance(function, dict) or not isinstance(function.get("summary"), dict):
                errors.append(f"coverage evidence is missing critical function: {path}:{function_name}")
                continue
            summary = function["summary"]
            line_percent = _number(
                summary,
                "percent_statements_covered",
                f"{path}:{function_name}",
            )
            branch_percent = _number(
                summary,
                "percent_branches_covered",
                f"{path}:{function_name}",
            )
            if line_percent < 100.0 or branch_percent < 100.0:
                errors.append(
                    f"critical function {path}:{function_name} must have 100% line/branch "
                    f"coverage (line={line_percent:.6f}%, branch={branch_percent:.6f}%)"
                )

    if previous_baseline is not None:
        validate_baseline(previous_baseline)
        previous_global = _number(previous_baseline, "global_line_percent", "previous baseline")
        if required_global + 1e-9 < previous_global:
            errors.append(
                f"coverage baseline cannot decrease ({required_global:.6f}% < "
                f"{previous_global:.6f}%)"
            )
        for path, previous_minimum in previous_baseline["module_line_minimums"].items():
            current_minimum = module_minimums.get(path)
            if not isinstance(current_minimum, (int, float)) or float(current_minimum) < float(
                previous_minimum
            ):
                errors.append(f"module coverage minimum cannot decrease: {path}")
        for path, previous_functions in previous_baseline["critical_functions"].items():
            current_functions = baseline["critical_functions"].get(path)
            if not isinstance(current_functions, list) or not set(previous_functions).issubset(
                current_functions
            ):
                errors.append(f"critical function coverage set cannot shrink: {path}")
    return errors


def load_previous_baseline(compare_ref: str, baseline_path: Path) -> dict[str, Any] | None:
    result = subprocess.run(
        ["git", "show", f"{compare_ref}:{baseline_path.as_posix()}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        return None
    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise CoverageRatchetError("previous coverage baseline is malformed") from exc
    if not isinstance(payload, dict):
        raise CoverageRatchetError("previous coverage baseline must be an object")
    return payload


def validate_recorded_commit(baseline: dict[str, Any], compare_ref: str) -> list[str]:
    commit = baseline["recorded_commit"]
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", commit, compare_ref],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode == 0:
        return []
    return [f"baseline recorded_commit {commit} is not an ancestor of {compare_ref}"]


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--coverage", type=Path, default=Path("coverage.json"))
    parser.add_argument("--baseline", type=Path, default=Path("coverage-baseline.json"))
    parser.add_argument("--pyproject", type=Path, default=Path("pyproject.toml"))
    parser.add_argument("--compare-ref", default="origin/main")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        coverage = load_json_object(args.coverage)
        baseline = load_json_object(args.baseline)
        previous = load_previous_baseline(args.compare_ref, args.baseline)
        errors = validate_coverage(coverage, baseline, previous_baseline=previous)
        errors.extend(validate_recorded_commit(baseline, args.compare_ref))
        current_config = load_toml_object(args.pyproject)
        recorded_config = load_git_toml(baseline["recorded_commit"], args.pyproject)
        errors.extend(
            validate_coverage_policy(
                coverage,
                current_config,
                recorded_config,
                repo_root=Path.cwd(),
            )
        )
        current_coverage = _coverage_config(current_config, "current pyproject")
        current_run = current_coverage.get("run")
        if not isinstance(current_run, dict):
            raise CoverageRatchetError("tool.coverage.run must be an object")
        source_roots = _string_list(
            current_run,
            "source",
            "current tool.coverage.run",
        )
        errors.extend(
            validate_no_new_coverage_pragmas(
                baseline["recorded_commit"],
                source_roots,
            )
        )
    except CoverageRatchetError as exc:
        print(f"Coverage ratchet failed: {exc}")
        return 1
    if errors:
        print("Coverage ratchet failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Coverage ratchet passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
