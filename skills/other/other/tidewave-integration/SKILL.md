---
name: tidewave-integration
description: "Tidewave MCP runtime tools for Phoenix development. Load when evaluating Elixir code in a running app, inspecting live process state, checking application logs, querying the dev database via SQL, introspecting Ecto schemas at runtime, or looking up exact-version hex library docs. Enables runtime debugging, smoke testing, and live state inspection."
effort: low
user-invocable: false
---

# Tidewave MCP Integration

Runtime intelligence for Phoenix apps via MCP. Prefer Tidewave tools over Bash when available.

## Iron Laws — Never Violate These

1. **DEV ONLY** — Never use Tidewave tools in production contexts. Avoid on shared dev servers with production data copies
2. **PREFER TIDEWAVE OVER BASH** — `mcp__tidewave__get_docs` > `web_fetch`, `execute_sql_query` > `psql`
3. **CHECK AVAILABILITY FIRST** — Use `/mcp` command or detect `mcp__tidewave__` tools
4. **SQL IS READ-HEAVY** — Use `execute_sql_query` for SELECT, be careful with mutations
5. **EXACT VERSIONS** — `get_docs` returns docs for YOUR mix.lock versions, not latest

## Quick Reference

| Task | Tidewave Tool | Fallback |
|------|---------------|----------|
| Get docs | `mcp__tidewave__get_docs Module.func/3` | `web_fetch hexdocs.pm/...` |
| Run code | `mcp__tidewave__project_eval` | `mix run -e "code"` |
| SQL query | `mcp__tidewave__execute_sql_query` | `psql $DATABASE_URL` |
| Find source | `mcp__tidewave__get_source_location` | `grep -rn "defmodule"` |
| Inspect DOM | `mcp__Tidewave-Web__browser_eval` | Manual browser inspection |
| List schemas | `mcp__tidewave__get_ecto_schemas` | Read `lib/*/schemas/` |
| Read logs | `mcp__tidewave__get_logs level: :error` | `tail -f log/dev.log` |

## Detection

```bash
# Check endpoint
curl -s http://localhost:4000/tidewave/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"ping"}'
```

Or use `/mcp` in Claude Code to see connected servers.

## Essential Patterns

### Test Function Immediately

```elixir
# mcp__tidewave__project_eval
MyApp.Accounts.create_user(%{email: "test@example.com"})
```

### Verify Migration

```sql
-- mcp__tidewave__execute_sql_query
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name = 'users';
```

### Debug LiveView (with PID from browser)

```elixir
# mcp__tidewave__project_eval
pid = pid("0.1234.0")
:sys.get_state(pid) |> Map.get(:socket) |> Map.get(:assigns) |> Map.keys()
```

## Setup Requirements

```elixir
# mix.exs
{:tidewave, "~> 0.1", only: :dev}

# endpoint.ex (in dev block)
plug Tidewave

# config/dev.exs (for LiveView source mapping)
config :phoenix_live_view,
  debug_heex_annotations: true,
  debug_attributes: true
```

## Proactive Runtime Checks

Don't just use Tidewave reactively. **Query runtime state at
workflow checkpoints** automatically:

- **After code edits**: `get_logs level: :error` (catch runtime crashes)
- **After features complete**: `project_eval` smoke test (behavioral check)
- **Before planning**: `get_ecto_schemas` + routes eval (concrete context)
- **When investigating**: Auto-capture errors before asking user
- **LiveView UI bugs**: `browser_eval` to inspect DOM state before editing components

See `${CLAUDE_SKILL_DIR}/references/proactive-patterns.md` for full integration points.

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/proactive-patterns.md` - Push-like runtime patterns at workflow checkpoints
- `${CLAUDE_SKILL_DIR}/references/tool-examples.md` - Complete tool usage examples
- `${CLAUDE_SKILL_DIR}/references/validation-checklist.md` - Runtime validation patterns
