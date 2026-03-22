---
name: recce-mcp-dev
description: Use when modifying recce/mcp_server.py, MCP tool handlers, error classification, or MCP-related tests. Also use when adding new MCP tools or changing tool response formats.
---

# Recce MCP Server Development

## Architecture

`RecceMCPServer` registers `list_tools`/`call_tool` handlers via MCP SDK `Server`. `call_tool` dispatches to `_tool_*` methods, classifies errors, logs/emits metrics, re-raises.

Entry point `run_mcp_server()` pops `single_env` before passing kwargs to `load_context()`.

## Key Patterns

**Error classification** — Shared indicator lists defined in `recce/tasks/rowcount.py`. Priority order (`PERMISSION_DENIED` > `TABLE_NOT_FOUND` > `SYNTAX_ERROR`) enforced by `_classify_db_error()` in `mcp_server.py` and `_query_row_count()` in `rowcount.py`. Classified → `logger.warning()` + `sentry_metrics.count()` (when sentry_sdk available). Unclassified → `logger.error()` + traceback.

**MCP SDK quirk** — Handler must **raise** for SDK to set `isError=True`.

**Response contracts** — See CLAUDE.md. Additive `_meta` only. `summary.py`: guard with `is None`, not `dict.get(key, 0)`. N/A display includes reason: `"N/A (table_not_found)"`.

**Single-env** — `_maybe_add_single_env_warning()` adds `_warning` to diff results. Descriptions get conditional note.

## Testing (Three Layers)

| Layer | File | Data Source | Runs In | Purpose |
|-------|------|-------------|---------|---------|
| Unit | `tests/test_mcp_server.py` | Mock `RecceContext` | CI (`pytest`) | Logic correctness — tool handlers, error classification, response format |
| Integration | `tests/test_mcp_e2e.py` | `DbtTestHelper` + DuckDB (fixed data) | CI (`pytest`) | MCP protocol works end-to-end via anyio memory streams |
| Smoke (E2E) | `/recce-mcp-e2e` skill | User's real dbt project + real database | Manual | All 8 tools return valid results against real data |

Each new MCP feature or behavior change should be covered at all three layers.

## Test Coverage Gap Analysis

After completing a round of MCP changes (see E2E Gate below for definition), proactively scan for missing test coverage across the three layers before asking about E2E verification.

**How to check:**
1. Identify what changed — new tool handler? new error path? new response field?
2. For each change, verify coverage exists at each layer:
   - **Unit**: Does `tests/test_mcp_server.py` have a test case for the new behavior? (happy path + error path)
   - **Integration**: Does `tests/test_mcp_e2e.py` exercise the new tool/feature via MCP protocol?
   - **Smoke**: Will `/recce-mcp-e2e` template cover the new tool? (If a new tool was added, the template may need updating)

**If gaps are found**, report them to the user before the E2E gate prompt:

> Test coverage gaps found:
> - Unit: missing test for `_tool_foo` error path when table not found
> - Integration: `test_mcp_e2e.py` does not exercise `foo` tool
> - Smoke: `/recce-mcp-e2e` template does not include `foo` tool
>
> Want to fill these gaps before running E2E?

**Do NOT scan** after: test-only changes, comment/doc edits, import reordering.

## E2E Verification Gate

After each meaningful round of MCP changes, you MUST ask the user:

> MCP changes complete for this round. Run `/recce-mcp-e2e` to verify?

If the user says yes, invoke `/recce-mcp-e2e`. If a dbt project path was used earlier in this session, reuse it automatically; otherwise ask.

**What counts as "a round":**
- A tool handler added or modified + its unit tests pass
- Error classification logic changed + tests pass
- Single-env or response format changed + tests pass

**Do NOT ask** after: test-only changes, comment/doc edits, import reordering.

**This is separate from `tests/test_mcp_e2e.py`** — that file tests with DbtTestHelper + DuckDB in CI. `/recce-mcp-e2e` verifies all 8 tools against a real dbt project with a real database.

## Pitfalls

- `sentry_sdk` import: `# pragma: no cover` on except (CI always has it)
- Python 3.9: `Union[X, Y]` not `X | Y`
- Pre-commit: black/isort may reformat — re-stage and commit
- `run.py` `schema_diff_should_be_approved()` try/except is intentional (ensures check creation)

## File Map

`recce/mcp_server.py` (server + handlers), `recce/tasks/rowcount.py` (error indicators, RowCountStatus), `recce/run.py` (CLI preset), `recce/summary.py` (display logic), `recce/event/__init__.py` (Sentry)
