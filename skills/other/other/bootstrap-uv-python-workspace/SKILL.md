---
name: bootstrap-uv-python-workspace
description: Bootstrap new Python projects and multi-package workspaces with uv on macOS using deterministic scripts and consistent defaults. Use when creating a new uv Python project, scaffolding a uv monorepo/workspace, setting up package or service profiles, initializing dev tooling (pytest, ruff, mypy), creating README scaffolds, or initializing git with an optional first commit.
---

# Bootstrap UV Python Workspace

Create repeatable uv-based scaffolds for both single projects and workspaces.
Use this skill as the shared scaffolding basis for other Python bootstrap skills that need consistent uv project/workspace defaults.

## Workflow

1. Choose bootstrap mode:
- Single project: `scripts/init_uv_python_project.sh`
- Workspace: `scripts/init_uv_python_workspace.sh`
2. Select profile(s):
- `package`: library/package layout
- `service`: FastAPI service layout
3. Run scaffold script with explicit `--name` and optional `--path`, `--python`, and `--initial-commit`.
4. Verify generated environment with built-in checks run by the scripts.
5. Return exact next commands to run locally.

## Commands

```bash
# Package project
scripts/init_uv_python_project.sh --name my-lib --profile package

# Service project
scripts/init_uv_python_project.sh --name my-service --profile service --python 3.13

# Workspace with defaults (core-lib package + api-service service)
scripts/init_uv_python_workspace.sh --name my-workspace

# Workspace with explicit members and profile mapping
scripts/init_uv_python_workspace.sh \
  --name platform \
  --members "core-lib,billing-service,orders-service" \
  --profile-map "core-lib=package,billing-service=service,orders-service=service"

# Allow non-empty target directory
scripts/init_uv_python_project.sh --name my-lib --force

# Skip git initialization
scripts/init_uv_python_workspace.sh --name platform --no-git-init

# Create initial commit after successful scaffold
scripts/init_uv_python_project.sh --name my-service --profile service --initial-commit
```

## Guardrails

- Refuse non-empty target directories unless `--force` is set.
- Refuse to overwrite an existing `pyproject.toml`.
- Require `uv` and `git` (when git initialization is enabled).
- Exit non-zero with actionable error text for invalid arguments or missing prerequisites.

## Defaults

- Python version: `3.13` (override with `--python`).
- Quality tooling: `pytest`, `ruff`, `mypy`.
- Git initialization: enabled by default (disable via `--no-git-init`).
- Workspace defaults:
- Members: `core-lib,api-service`
- Profiles: first member `package`, remaining members `service`
- Local linking: services depend on the first package member using uv workspace sources.

## Automation Suitability

- Codex App automation: Medium. Best for scheduled scaffold health checks, not day-to-day product delivery.
- Codex CLI automation: High. Strong fit for CI or scheduled scaffold validation.

## Codex App Automation Prompt Template

```markdown
Use $bootstrap-uv-python-workspace.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Create temporary scaffolds only under <SCRATCH_ROOT>/<NAME>-<STAMP>.
- Do not modify unrelated files outside the temporary scaffold path.

Task:
1. If <MODE:PROJECT|WORKSPACE> is PROJECT, run:
   `scripts/init_uv_python_project.sh --name <NAME> --profile <PROFILE:PACKAGE|SERVICE> --python <PYTHON_VERSION> --path <SCRATCH_ROOT>/<NAME>-<STAMP> <FORCE_FLAG> <GIT_INIT_MODE>`
2. If <MODE:PROJECT|WORKSPACE> is WORKSPACE, run:
   `scripts/init_uv_python_workspace.sh --name <NAME> --python <PYTHON_VERSION> --path <SCRATCH_ROOT>/<NAME>-<STAMP> --members "<MEMBERS_CSV>" --profile-map "<PROFILE_MAP>" <FORCE_FLAG> <GIT_INIT_MODE>`
3. Run validation checks in the scaffold root:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
4. If <KEEP_OR_CLEANUP_ARTIFACTS:KEEP|CLEANUP> is CLEANUP, remove the scaffold directory after reporting results.

Output contract:
1. STATUS: PASS or FAIL
2. COMMANDS: exact commands executed, in order
3. RESULTS: concise check outcomes
4. If FAIL: include a short stderr summary and minimal fix recommendation
5. If PASS with no findings: include "safe to archive"
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $bootstrap-uv-python-workspace.
Stay strictly within <REPO_PATH>. Create temporary artifacts only under <SCRATCH_ROOT>/<NAME>-<STAMP>.
Run scaffold generation for <MODE:PROJECT|WORKSPACE>, then run:
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy .`
Return STATUS, exact commands, and concise results only. If failures occur, provide only the minimal remediation needed.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<SCRATCH_ROOT>`
- `<NAME>`
- `<STAMP>`
- `<MODE:PROJECT|WORKSPACE>`
- `<PROFILE:PACKAGE|SERVICE>`
- `<MEMBERS_CSV>`
- `<PROFILE_MAP>`
- `<PYTHON_VERSION>`
- `<FORCE_FLAG>`
- `<GIT_INIT_MODE>`
- `<KEEP_OR_CLEANUP_ARTIFACTS:KEEP|CLEANUP>`

## References

Use [references/uv-command-recipes.md](references/uv-command-recipes.md) for concise uv command patterns.

## Resources

### scripts/

- `init_uv_python_project.sh`: bootstrap a single uv project (`package` or `service`).
- `init_uv_python_workspace.sh`: bootstrap a uv workspace with multiple members.

### references/

- `uv-command-recipes.md`: short recipes for init/add/run/sync/workspace operations.

### assets/

- `README.md.tmpl`: shared template consumed by both scripts.
