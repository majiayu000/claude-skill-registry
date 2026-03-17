---
name: uv-pytest-unit-testing
description: Set up and run unit tests for Python uv projects and uv workspaces with pytest. Use when creating or updating pytest configuration in pyproject.toml, installing pytest dev dependencies with uv, running tests in a workspace member package via `uv run --package`, organizing tests with fixtures/markers/parametrize, or troubleshooting test discovery and import failures.
---

# Uv Pytest Unit Testing

## Overview

Use this skill to standardize pytest setup and execution for uv-managed Python repositories, including single-project repos and uv workspaces.

## Workflow

1. Detect repository mode.
- Treat repo as workspace when `pyproject.toml` defines `[tool.uv.workspace]`.
- Treat repo as single project otherwise.

2. Bootstrap pytest dependencies and baseline config.
- Run `scripts/bootstrap_pytest_uv.sh --workspace-root <repo>`.
- Add `--package <member-name>` for workspace member package setup.
- Add `--with-cov` when `pytest-cov` should be installed and baseline coverage flags added.
- Add `--dry-run` to preview all actions without mutating files.

3. Run tests with uv.
- Run `scripts/run_pytest_uv.sh --workspace-root <repo>` for root-project execution.
- Run `scripts/run_pytest_uv.sh --workspace-root <repo> --package <member-name>` for workspace member execution.
- Pass through pytest selectors/options after `--`, for example:
  - `scripts/run_pytest_uv.sh --workspace-root <repo> -- --maxfail=1 -q`
  - `scripts/run_pytest_uv.sh --workspace-root <repo> --package api --path tests/unit -- -k auth -m "not slow"`

4. Apply balanced quality gates.
- Require passing test runs before concluding work.
- Recommend coverage reporting as guidance, not a hard threshold, unless user explicitly requests enforced minimum coverage.

5. Troubleshoot failures in this order.
- Confirm command context: root vs `--package` run target.
- Confirm test discovery layout: `tests/`, `test_*.py`, `*_test.py`.
- Confirm marker registration in `tool.pytest.ini_options.markers` when custom markers are used.
- Confirm import path assumptions (package install mode, working directory, and module names).

## Test Authoring Guidance

- Keep fast unit tests under `tests/unit` and integration-heavy tests under `tests/integration` when repo size warrants separation.
- Use fixtures for setup reuse, and keep fixture scope minimal (`function` by default).
- Use `@pytest.mark.parametrize` for matrix-style cases instead of hand-written loops.
- Use `monkeypatch` for environment variables and runtime dependency replacement.
- Register custom marks in config to avoid marker warnings.

## Automation Suitability

- Codex App automation: High. Strong recurring fit for test health checks, failure triage, and drift detection.
- Codex CLI automation: High. Strong fit for non-interactive test setup and targeted test sweeps.

## Codex App Automation Prompt Template

```markdown
Use $uv-pytest-unit-testing.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Operate only on pytest setup and test execution tasks.
- Do not perform unrelated code refactors.

Task:
1. Detect repository mode from <WORKSPACE_ROOT>/pyproject.toml.
2. If <DRY_RUN_BOOTSTRAP:TRUE|FALSE> is TRUE, run:
   `scripts/bootstrap_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <WITH_COV_FLAG> --dry-run`
3. If <DRY_RUN_BOOTSTRAP:TRUE|FALSE> is FALSE, run:
   `scripts/bootstrap_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <WITH_COV_FLAG>`
4. Run tests with:
   `scripts/run_pytest_uv.sh --workspace-root <WORKSPACE_ROOT> <PACKAGE_FLAG> <TEST_PATH_FLAG> -- <PYTEST_ARGS>`
5. Keep package-targeted runs explicit when <PACKAGE_NAME_OR_EMPTY> is set.

Output contract:
1. STATUS: PASS or FAIL
2. SETUP: what bootstrap actions ran
3. TEST_RESULTS: concise pass/fail summary
4. FAILURES: grouped likely causes
5. NEXT_STEPS: minimal remediation actions
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $uv-pytest-unit-testing.
Limit scope to pytest setup and execution in <WORKSPACE_ROOT>.
Run bootstrap in dry-run or real mode based on <DRY_RUN_BOOTSTRAP:TRUE|FALSE>.
Run tests with explicit package targeting when <PACKAGE_NAME_OR_EMPTY> is set.
Return STATUS, setup actions, concise test summary, grouped likely causes for failures, and minimal next steps.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<WORKSPACE_ROOT>`
- `<PACKAGE_NAME_OR_EMPTY>`
- `<PACKAGE_FLAG>`
- `<TEST_PATH_OR_EMPTY>`
- `<TEST_PATH_FLAG>`
- `<PYTEST_ARGS>`
- `<WITH_COV_FLAG:--with-cov|EMPTY>`
- `<DRY_RUN_BOOTSTRAP:TRUE|FALSE>`

## References

- Use [`references/pytest-workflow.md`](references/pytest-workflow.md) for pytest conventions, config keys, fixtures, markers, and troubleshooting.
- Use [`references/uv-workspace-testing.md`](references/uv-workspace-testing.md) for uv workspace execution patterns (`uv run`, `uv run --package`, package-targeted test runs).

## Resources

### scripts/

- `scripts/bootstrap_pytest_uv.sh`: Install pytest dev dependencies and append baseline `tool.pytest.ini_options` when missing.
- `scripts/run_pytest_uv.sh`: Run pytest via uv for root project or workspace member package, with passthrough args.

### references/

- `references/pytest-workflow.md`: Practical pytest setup and usage guidance.
- `references/uv-workspace-testing.md`: uv execution guidance for single-project and workspace repositories.
