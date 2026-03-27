---
name: phx:perf
description: Analyze Elixir/Phoenix code for performance issues — N+1 queries, LiveView memory, query patterns, OTP bottlenecks. Use whenever the user mentions slowness, timeouts, high memory, slow queries, or wants to optimize any part of their Phoenix application. Also use before deploying performance-sensitive features.
effort: high
argument-hint: [page|context|module] [--focus ecto|liveview|otp]
disable-model-invocation: true
---

# Performance Analysis

Analyze code for performance issues across Ecto, LiveView,
and OTP layers. Prioritize findings by impact and effort.

## Usage

```
/phx:perf                           # Analyze full project
/phx:perf lib/my_app/accounts.ex    # Analyze specific module
/phx:perf --focus ecto              # Ecto queries only
/phx:perf --focus liveview          # LiveView memory only
/phx:perf --focus otp               # OTP bottlenecks only
```

## Arguments

`$ARGUMENTS` = Optional module/context path and `--focus` flag.

## Iron Laws

1. **MEASURE BEFORE OPTIMIZING** — Never optimize without evidence of a problem
2. **DATABASE FIRST** — 90% of Elixir performance issues are query-related
3. **ONE CHANGE AT A TIME** — Isolate optimizations to measure impact

## Workflow

### Step 1: Identify Scope

If specific file provided, focus there. Otherwise:

```bash
# Find hot paths: contexts, LiveViews, workers
find lib/ -name "*.ex" | head -50
```

### Step 2: Run Analysis Tracks

Spawn analysis agents in parallel based on focus:

**Ecto Track** (default or `--focus ecto`):

Spawn `elixir-phoenix:elixir-reviewer` with prompt:
"Analyze for N+1 queries, missing preloads, unindexed queries,
and inefficient patterns. Check: `Repo.all` in loops,
`Enum.map` with Repo calls, missing `preload`, queries without
indexes on WHERE/JOIN columns."

**LiveView Track** (default or `--focus liveview`):

Spawn `elixir-phoenix:elixir-reviewer` with prompt:
"Analyze LiveViews for memory issues: large assigns, missing
streams for lists, assigns that grow unbounded, heavy
`handle_info` processing, missing `assign_async` for slow ops."

**OTP Track** (only with `--focus otp`):

Spawn `elixir-phoenix:otp-advisor` with prompt:
"Analyze for OTP bottlenecks: GenServer mailbox growth,
synchronous calls in hot paths, missing Task.async for
parallel work, ETS opportunities for read-heavy state."

### Step 3: Prioritize Findings

Score each finding on a 2x2 matrix:

| | Low Effort | High Effort |
|---|---|---|
| **High Impact** | DO FIRST | PLAN |
| **Low Impact** | QUICK WIN | SKIP |

High impact = affects response time, memory per user, or query count.
Low effort = single file change, no migration needed.

### Step 4: Present Top 5

Present findings sorted by priority:

```markdown
## Performance Analysis: {scope}

### 1. {Finding} — DO FIRST
**Impact**: {what improves}
**Location**: {file}:{line}
**Current**: {problematic pattern}
**Fix**: {optimized pattern}
**Estimated gain**: {e.g., "eliminates N+1, reduces queries from O(n) to O(1)"}

### 2. {Finding} — PLAN
...
```

### Step 5: Offer Next Steps

Always end with actionable next steps — findings without follow-up
get lost. Present options based on severity:

```
How would you like to proceed?

- `/phx:plan` — Create a plan from these findings (recommended for 3+ fixes)
- `/phx:quick` — Apply top priority fix directly (1-2 simple fixes)
- `/phx:investigate` — Deep-dive into a specific finding
```

## Tidewave Integration

If Tidewave MCP is available:

- Use `mcp__tidewave__project_eval` to run `Repo.query!("EXPLAIN ANALYZE ...")` on suspicious queries
- Use `mcp__tidewave__project_eval` to check `Process.info(pid, :message_queue_len)` for GenServer bottlenecks
- Use `mcp__tidewave__execute_sql_query` to check missing indexes

## References

- `${CLAUDE_SKILL_DIR}/references/benchmarking.md` — Benchee patterns, profiling, flame graphs
