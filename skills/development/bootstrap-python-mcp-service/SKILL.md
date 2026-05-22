---
name: bootstrap-python-mcp-service
description: Bootstrap Python MCP server projects and workspaces on macOS using uv and FastMCP with consistent defaults. Use when creating a new MCP server from scratch, scaffolding a single uv MCP project, scaffolding a uv workspace with package/service members, initializing pytest+ruff+mypy defaults, creating README.md, initializing git, running initial validation checks, or starting from OpenAPI/FastAPI with MCP mapping guidance.
---

# Bootstrap Python MCP Service

Create production-oriented FastMCP starter layouts using shared uv project/workspace scaffolding plus deterministic MCP overlays.

## Workflow

1. Choose mode:
- Project: scaffold one MCP service.
- Workspace: scaffold uv workspace, then convert service members to FastMCP.
2. Run `scripts/init_fastmcp_service.sh` with explicit `--name` and optional `--path`, `--python`, `--force`, `--no-git-init`, `--initial-commit`.
3. For workspace mode, optionally pass `--members` and `--profile-map`.
4. Verify quality checks:
- `uv run pytest`
- `uv run ruff check .`
- `uv run mypy .`
5. If bootstrapping from OpenAPI/FastAPI, run `scripts/assess_api_for_mcp.py` and review mapping report.
6. Return exact next commands.

## Commands

```bash
# Project mode (default)
scripts/init_fastmcp_service.sh --name my-mcp-server

# Project mode with explicit options
scripts/init_fastmcp_service.sh --name my-mcp-server --mode project --python 3.13 --path /tmp/my-mcp-server

# Workspace mode with defaults (core-lib package + api-service service)
scripts/init_fastmcp_service.sh --name platform --mode workspace

# Workspace mode with explicit members and profile mapping
scripts/init_fastmcp_service.sh \
  --name platform \
  --mode workspace \
  --members "core-lib,tools-service,ops-service" \
  --profile-map "core-lib=package,tools-service=service,ops-service=service"

# Allow non-empty target directory
scripts/init_fastmcp_service.sh --name my-mcp-server --force

# Skip git initialization
scripts/init_fastmcp_service.sh --name my-mcp-server --no-git-init

# Create initial commit
scripts/init_fastmcp_service.sh --name my-mcp-server --initial-commit

# Generate MCP mapping guidance from OpenAPI
python3 scripts/assess_api_for_mcp.py --openapi ./openapi.yaml --out ./mcp_mapping_report.md

# Generate MCP mapping guidance from existing FastAPI app
python3 scripts/assess_api_for_mcp.py --fastapi app.main:app --out ./mcp_mapping_report.md
```

## Base UV/FastAPI Guidance

The shared scaffold basis follows uv FastAPI integration style:

```bash
uv add fastapi --extra standard
uv run fastapi dev app/main.py
```

This skill then overlays FastMCP dependencies and server files for MCP service members.

## API Import Guidance

When starting from OpenAPI or FastAPI, bootstrap first, then map endpoints to MCP primitives:

1. Generate mapping report with `scripts/assess_api_for_mcp.py`.
2. Classify endpoints into `Resources`, `Tools`, and `Prompts`.
3. Recommend RouteMaps/Transforms only when they improve usability.
4. Keep bootstrap deterministic; defer heavy custom mapping unless requested.

## FastMCP Docs Lookup

Use the `fastmcp_docs` MCP server for up-to-date framework details.

Suggested queries:

- `FastMCP quickstart server example`
- `FastMCP tools resources prompts best practices`
- `FastMCP RouteMap Transform`
- `FastMCP from OpenAPI`
- `FastMCP from FastAPI`

## Guardrails

- Refuse non-empty target directories unless `--force` is set.
- Require at least one service profile member in workspace mode.
- Require `uv` and `git` (unless `--no-git-init` is set and no initial commit is requested).
- Fail when workspace-only options are used in project mode.
- Fail when `--initial-commit` is used with `--no-git-init`.

## Defaults

- Mode: `project`
- Python version: `3.13`
- Quality tooling: `pytest`, `ruff`, `mypy`
- Workspace defaults:
- Members: `core-lib,api-service`
- Profiles: first member `package`, remaining members `service`

## Automation Suitability

- Codex App automation: Medium. Useful for recurring FastMCP scaffold checks and mapping-assessment checks.
- Codex CLI automation: High. Strong fit for CI-style scaffold validation.

## Codex App Automation Prompt Template

```markdown
Use $bootstrap-python-mcp-service.

Scope boundaries:
- Work only inside <REPO_PATH>.
- Create or validate scaffold output only in <TARGET_PATH>.
- Restrict work to scaffold generation, optional mapping report generation, and verification.

Task:
1. If <MODE:PROJECT|WORKSPACE> is PROJECT, run:
   `scripts/init_fastmcp_service.sh --name <MCP_SERVICE_NAME> --mode project --path <TARGET_PATH> --python <PYTHON_VERSION> <FORCE_FLAG> <GIT_INIT_MODE>`
2. If <MODE:PROJECT|WORKSPACE> is WORKSPACE, run:
   `scripts/init_fastmcp_service.sh --name <MCP_SERVICE_NAME> --mode workspace --path <TARGET_PATH> --python <PYTHON_VERSION> --members "<MEMBERS_CSV>" --profile-map "<PROFILE_MAP>" <FORCE_FLAG> <GIT_INIT_MODE>`
3. If <GENERATE_MAPPING_REPORT:TRUE|FALSE> is TRUE:
   - If <MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT> is OPENAPI, run:
     `python3 scripts/assess_api_for_mcp.py --openapi <MAPPING_INPUT_PATH> --out <TARGET_PATH>/mcp_mapping_report.md`
   - If <MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT> is FASTAPI_IMPORT, run:
     `python3 scripts/assess_api_for_mcp.py --fastapi <MAPPING_INPUT_PATH> --out <TARGET_PATH>/mcp_mapping_report.md`
4. Run verification checks in <TARGET_PATH>:
   - `uv run pytest`
   - `uv run ruff check .`
   - `uv run mypy .`

Output contract:
1. STATUS: PASS or FAIL
2. COMMANDS: exact commands executed
3. RESULTS: concise outcomes for scaffold and checks
4. If report generated: include report path
5. If FAIL: provide likely root cause and minimal remediation
```

## Codex CLI Automation Prompt Template

```bash
codex exec --full-auto --sandbox workspace-write --cd "<REPO_PATH>" "<PROMPT_BODY>"
```

`<PROMPT_BODY>` template:

```markdown
Use $bootstrap-python-mcp-service.
Scope is limited to scaffold generation in <TARGET_PATH>, optional mapping report generation, and verification checks.
Run only commands needed for this flow, then return STATUS, exact command transcript, concise results, and minimal remediation if failures occur.
```

## Customization Placeholders

- `<REPO_PATH>`
- `<MCP_SERVICE_NAME>`
- `<MODE:PROJECT|WORKSPACE>`
- `<TARGET_PATH>`
- `<PYTHON_VERSION>`
- `<MEMBERS_CSV>`
- `<PROFILE_MAP>`
- `<FORCE_FLAG>`
- `<GIT_INIT_MODE>`
- `<MAPPING_INPUT_MODE:NONE|OPENAPI|FASTAPI_IMPORT>`
- `<MAPPING_INPUT_PATH>`
- `<GENERATE_MAPPING_REPORT:TRUE|FALSE>`

## Resources

### scripts/

- `init_fastmcp_service.sh`: thin orchestrator that delegates to uv workspace bootstrap then overlays FastMCP files/dependencies.
- `assess_api_for_mcp.py`: endpoint-to-MCP mapping analyzer.

### references/

- `mcp-mapping-guidelines.md`: practical heuristics for MCP primitives, route maps, transforms, and workspace mapping boundaries.
- `fastmcp-docs-lookup.md`: curated `fastmcp_docs` search patterns.

### assets/

- `README.md.tmpl`: README template for MCP project output.
