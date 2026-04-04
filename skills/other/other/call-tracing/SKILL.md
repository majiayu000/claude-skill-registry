---
name: phx:trace
description: Trace Elixir call trees from entry points via mix xref. Use when debugging data flow, planning signature changes, or understanding how a bug reaches code.
effort: medium
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

Run `mix xref callers MyApp.Accounts.update_user/2` to find all callers. Then read the reported locations to see argument patterns.

## Entry Points (Stop Here)

| Pattern | Type |
|---------|------|
| `def mount/3`, `def handle_event/3` | LiveView |
| `def index/2`, `def show/2`, `def create/2` | Controller |
| `def perform(%Oban.Job{})` | Oban Worker |
| `def handle_call/3`, `def handle_cast/2` | GenServer |

## Delegate to call-tracer Agent

For full recursive tree with argument extraction and **parallel category tracing**:

```
Agent(subagent_type: "call-tracer", prompt: "Build call tree for MyApp.Accounts.update_user/2")
```

The call-tracer agent uses **parallel subagents** for each entry point category:

- Controllers subagent (HTTP paths)
- LiveView subagent (WebSocket paths)
- Workers subagent (Background jobs)
- Internal subagent (Cross-context calls)

Each gets fresh 200k context for deep exploration.

## Output Location

`.claude/plans/{slug}/research/call-tree-{function}.md`

## References

For detailed patterns:

- `${CLAUDE_SKILL_DIR}/references/mix-xref-usage.md` - Full mix xref commands and options
- `${CLAUDE_SKILL_DIR}/references/entry-points.md` - All Phoenix/OTP entry point patterns
- `${CLAUDE_SKILL_DIR}/references/argument-extraction.md` - AST parsing for argument patterns
