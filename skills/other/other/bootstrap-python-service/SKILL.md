---
name: bootstrap-python-service
description: Bootstrap Python FastAPI services on macOS using uv with consistent project and workspace scaffolds. Use when creating a new backend/API service from scratch, scaffolding a single uv service project, scaffolding a uv workspace with package/service members, initializing pytest+ruff+mypy defaults, creating README.md, initializing git, and running initial validation commands.
---

# Bootstrap Python Service

Create production-oriented FastAPI starter layouts using shared uv project/workspace scaffolding.

## Workflow

1. Choose mode:
- Project: single FastAPI service scaffold.
- Workspace: multi-member uv workspace scaffold.
2. Run `scripts/init_python_service.sh` with explicit `--name` and optional `--path`, `--python`, `--force`, `--no-git-init`, `--initial-commit`.
3. For workspace mode, optionally pass `--members` and `--profile-map`.
4. Verify quality checks:
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy .`
5. Return exact next run/test commands.

## Commands

```bash
# Project mode (default)
scripts/init_python_service.sh --name my-service

# Project mode with explicit options
scripts/init_python_service.sh --name my-service --mode project --python 3.13 --path /tmp/my-service

# Workspace mode with defaults (core-lib package + api-service service)
scripts/init_python_service.sh --name platform --mode workspace

# Workspace mode with explicit members and profile mapping
scripts/init_python_service.sh \
  --name platform \
  --mode workspace \
  --members "core-lib,billing-service,orders-service" \
  --profile-map "core-lib=package,billing-service=service,orders-service=service"

# Allow non-empty target directory
scripts/init_python_service.sh --name my-service --force

# Skip git initialization
scripts/init_python_service.sh --name my-service --no-git-init

# Create initial commit
scripts/init_python_service.sh --name my-service --initial-commit
```

## FastAPI Guidance

Use uv FastAPI integration style as primary guidance:

```bash
uv add fastapi --extra standard
uv run fastapi dev app/main.py
# optional production-style local run
uv run fastapi run app/main.py
```

## Guardrails

- Refuse non-empty target directories unless `--force` is set.
- Require `uv` and `git` (unless `--no-git-init` is set and no initial commit is requested).
- Fail when workspace-only options are used in project mode.
- Fail when `--initial-commit` is used with `--no-git-init`.

## Defaults

- Mode: `project`
- Python version: `3.13`
- Quality tooling: `pytest`, `ruff`, `mypy`
- Workspace defaults (when mode is `workspace`):
- Members: `core-lib,api-service`
- Profiles: first member `package`, remaining members `service`

## Automation Suitability

- Codex App automation: Medium. Useful for recurring FastAPI scaffold smoke checks and regression checks.
- Codex CLI automation: High. Strong fit for CI or scheduled scaffolder reliability checks.

## Codex App Automation Prompt Template

```markdown
Use $bootstrap-python-service.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Create or validate scaffold output only in <TARGET_PATH>.
- Limit activity to scaffolding and verification; no unrelated refactors.

Task:
1. If <MODE:PROJECT|WORKSPACE> is PROJECT, run:
   `scripts/init_python_service.sh --name <SERVICE_NAME> --mode project --path <TARGET_PATH> --python <PYTHON_VERSION> <FORCE_FLAG> <GIT_INIT_MODE>`
2. If <MODE:PROJECT|WORKSPACE> is WORKSPACE, run:
   `scripts/init_python_service.sh --name <SERVICE_NAME> --mode workspace --path <TARGET_PATH> --python <PYTHON_VERSION> --members "<MEMBERS_CSV>" --profile-map "<PROFILE_MAP>" <FORCE_FLAG> <GIT_INIT_MODE>`
3. Validate generated checks:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`
4. If mode is PROJECT, also validate generated run commands:
   - `uv run fastapi dev app/main.py`
   - `uv run fastapi run app/main.py`

Output contract:
1. STATUS: PASS or FAIL
2. GENERATED_PATH: final output path
3. COMMANDS: exact commands executed
4. RESULTS: concise check outputs
5. If FAIL: short root-cause summary and minimal remediation steps
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

Optional machine-readable variant:

```bash
codex exec --json --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $bootstrap-python-service.
Scope is scaffolding plus verification only in <TARGET_PATH> under <REPO_PATH>.
Run the scaffold command for <MODE:PROJECT|WORKSPACE>, then run pytest, ruff, and mypy.
If project mode, confirm FastAPI dev/run commands are valid.
Return STATUS, generated path, exact command transcript, and minimal remediation on failure.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<SERVICE_NAME>`
- `<MODE:PROJECT|WORKSPACE>`
- `<TARGET_PATH>`
- `<PYTHON_VERSION>`
- `<MEMBERS_CSV>`
- `<PROFILE_MAP>`
- `<FORCE_FLAG>`
- `<GIT_INIT_MODE>`

## Resources

### scripts/

- `init_python_service.sh`: thin orchestrator that delegates to `bootstrap-uv-python-workspace` scripts.

### references/

- `conventions.md`: runtime, dependency, and quality defaults.

### assets/

- `README.md.tmpl`: README template for service-focused output.
