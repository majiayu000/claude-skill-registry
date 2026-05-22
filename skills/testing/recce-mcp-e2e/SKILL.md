---
name: recce-mcp-e2e
description: Use when MCP server code is modified and needs full E2E verification against a real dbt project. Triggers after changes to recce/mcp_server.py, MCP tool handlers, single-env logic, or error classification. Also use before merging MCP PRs.
---

# MCP E2E Verification

Full-stack verification of all 8 MCP tools against a real dbt project.

## When to Use

- After modifying `recce/mcp_server.py` or `_tool_*` handlers
- After changing single-env logic or error classification
- Before merging any MCP-related PR
- **Not for**: unit test changes only, frontend-only changes, docs-only changes

## Usage

Invoke as `/recce-mcp-e2e` or `/recce-mcp-e2e <project_path>`.

- **With argument**: use the given path as the dbt project directory
- **Without argument**: ask the user for the dbt project path

The project directory must contain `target/manifest.json` and `target-base/manifest.json`.

## Process

1. **Resolve project path** from argument or user input
2. **Validate** `target/` and `target-base/` exist with `manifest.json`
3. **Detect recce source** — find the repo root containing `recce/mcp_server.py`. If `recce-nightly` is also installed (`pip show recce recce-nightly`), set `PYTHONPATH=<RECCE_REPO_ROOT>:$PYTHONPATH`
4. **Generate** `test_mcp_e2e.py` in the project directory from `test_mcp_e2e_template.py` (in this skill directory). Replace `PROJECT_DIR_PLACEHOLDER` with the resolved absolute path.
5. **Execute** with appropriate PYTHONPATH prefix
6. **Report** results — all 13 checks must show PASS. Expected output:
   ```
   === FULL MODE (8 tools) ===
     PASS lineage_diff: PASS
     ...
   === SINGLE-ENV MODE ===
     PASS row_count_diff (_warning): PASS
     ...
   ALL PASS
   ```
7. **Clean up** — delete `test_mcp_e2e.py`

## Quick Reference

| Test Suite | Checks | What's Verified |
|-----------|--------|----------------|
| Full mode (8 tools) | lineage_diff, schema_diff, row_count_diff, query, query_diff, profile_diff, list_checks, run_check | Non-empty results from each tool |
| Single-env _warning (3) | row_count_diff, query_diff, profile_diff | `_warning` field present with `SINGLE_ENV_WARNING` |
| Single-env no _warning (2) | lineage_diff, schema_diff | `_warning` field NOT present |

**Additional manual checks** (not in script):

| Check | Command/Action |
|-------|---------------|
| --help | `recce mcp-server --help` shows Prerequisites section |
| Server modes | Non-server mode: `list_tools` returns only lineage_diff + schema_diff |

## Common Mistakes

| Problem | Fix |
|---------|-----|
| `ImportError: cannot import name 'SINGLE_ENV_WARNING'` | recce-nightly conflict — use `PYTHONPATH=<RECCE_REPO_ROOT>:$PYTHONPATH` |
| lineage_diff returns empty | Use `view_mode="all"` (default `changed_models` filters out unchanged) |
| list_checks returns empty | Preset checks from `recce.yml` must be loaded via `load_preset_checks()` — script handles this |
| `portalocker` FileNotFoundError on exit | Cosmetic thread error in event collector — does not affect results |
| Single-env test uses target-base | By design — `load_context` needs both, `single_env=True` flag simulates the mode |
