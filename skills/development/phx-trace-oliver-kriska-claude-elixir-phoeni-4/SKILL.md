---
name: phx-trace
description: Trace Elixir call trees from entry points via mix xref. Use when debugging
  data flow, planning signature changes, or understanding how a bug reaches code.
---

# Call Tracing

Build call trees showing how functions are reached from entry points.

## Iron Laws - Never Violate These

1. **Always use `mix xref callers` first** - It's authoritative; grep is fallback only
2. **Stop at entry points** - Controllers, LiveView callbacks, Oban workers, GenServer callbacks
3. **Track visited MFAs** - Prevent infinite loops from circular calls
4. **Extract argument patterns** - Just knowing "who calls" isn't enough; HOW they call matters
5. **Max depth 10** - Deeper trees indicate architectural issues, not useful traces

## When to Build Call Tree (Use Proactively)

| Condition | Why Call Tree Helps |
|-----------|---------------------|
| Unexpected nil/value at runtime | Trace where the value originates |
| Bug can't reproduce locally | See all entry points that reach the code |
| Changing function signature | Find all callers and their argument patterns |
| Incomplete stack trace | Get full path context |
| "Where does X come from?" | Visual answer to data flow question |

## Quick Trace

Run the caller query first, then inspect another function in the chain as needed:

```bash
mix xref callers MyApp.Accounts.update_user/2
mix xref callers MyApp.Accounts.get_user/1
```

Read the reported locations to see argument patterns.

## Entry Points (Stop Here)

| Pattern | Type |
|---------|------|
| `def mount/3`, `def handle_event/3` | LiveView |
| `def index/2`, `def show/2`, `def create/2` | Controller |
| `def perform(%Oban.Job{})` | Oban Worker |
| `def handle_call/3`, `def handle_cast/2` | GenServer |

## Full Recursive Trace

Trace controller, LiveView, worker, and internal entry-point categories in this
session, starting each category with `mix xref callers`. Native generic workers
may handle independent categories in parallel when the runtime provides them,
but the same-session sequential path is fully supported and must produce the
same call tree. Do not require a named custom agent or Claude-specific spawn
configuration.

## Output Location

`.claude/plans/{slug}/research/call-tree-{function}.md`

## References

For detailed patterns:

- `references/mix-xref-usage.md` - Full mix xref commands and options
- `references/entry-points.md` - All Phoenix/OTP entry point patterns
- `references/argument-extraction.md` - AST parsing for argument patterns
