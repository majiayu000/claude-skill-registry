---
name: oban
description: "Oban job processing — workers, perform/1 (OSS) and process/1 (Pro), queues, cron, retries, unique jobs, idempotency, Oban Pro (Workflow, Batch, Chunk, Smart Engine), Testing. Use when writing Oban workers, queue config, or debugging jobs."
effort: medium
user-invocable: false
paths:
  - "**/workers/**/*.ex"
  - "**/*_worker.ex"
  - "**/*_worker_test.exs"
  - "**/*_job.ex"
---

# Oban Background Jobs Reference

Quick reference for Elixir Oban patterns.

## Oban Pro Detection

**Before applying patterns, check for Oban Pro:**

```bash
grep -E "oban_pro|oban_web" mix.exs
grep -r "use Oban.Pro.Worker" lib/
grep -r "Oban.Pro.Engines.Smart" config/
```

**If Oban Pro detected**, use Pro patterns for ALL new workers:

| Standard Oban | Oban Pro |
|---------------|----------|
| `use Oban.Worker` | `use Oban.Pro.Worker` |
| `def perform(%Job{})` | `def process(%Job{})` |
| `Oban.Testing` | `Oban.Pro.Testing` |
| Advisory lock engine | `Oban.Pro.Engines.Smart` |

**Pro features** (all optional): `args_schema` (typed args), Workflows, Batches, Chunks,
Relay, hooks, encryption, deadlines, chaining, Smart Engine (global concurrency + rate limiting).
Pro plugins (DynamicCron, DynamicLifeline, DynamicPruner) **enhance** OSS equivalents — swap module, don't run both.
See `${CLAUDE_SKILL_DIR}/references/oban-pro-basics.md` for all patterns and migration guide.

---

## Iron Laws — Never Violate These

1. **JOBS MUST BE IDEMPOTENT** — Safe to retry. Use idempotency keys for payments
2. **JOBS MUST STORE IDs, NOT STRUCTS** — JSON serialization. `%{user_id: 1}` not `%{user: %User{}}`
3. **JOBS MUST HANDLE ALL RETURN VALUES** — `:ok`, `{:error, _}`, `{:cancel, _}`, `{:snooze, _}`
4. **ARGS USE STRING KEYS** — Pattern match `%{"user_id" => id}` not `%{user_id: id}`
5. **UNIQUE CONSTRAINTS FOR USER ACTIONS** — Prevent double-click duplicates
6. **NEVER STORE LARGE DATA IN ARGS** — Store references (IDs, paths), not content
7. **SMART ENGINE: NEVER USE `attempt` TO LIMIT SNOOZES** — Snooze rolls back attempt counter. Use `meta["snoozed"]` instead. Causes infinite loops

## Quick Worker Template

```elixir
defmodule MyApp.Workers.ExampleWorker do
  use Oban.Worker,
    queue: :default,
    max_attempts: 5,
    unique: [period: {5, :minutes}, keys: [:entity_id]]

  @impl Oban.Worker
  def perform(%Oban.Job{args: %{"entity_id" => id}}) do
    case process(id) do
      {:ok, _} -> :ok
      {:error, :not_found} -> {:cancel, "Entity not found"}
      {:error, :rate_limited} -> {:snooze, {5, :minutes}}
      {:error, reason} -> {:error, reason}
    end
  end
end
```

## Return Value Meanings

| Return | State | Behavior |
|--------|-------|----------|
| `:ok` | `completed` | Success |
| `{:ok, value}` | `completed` | Success with value |
| `{:error, reason}` | `retryable` | Retry with backoff |
| `{:cancel, reason}` | `cancelled` | Stop permanently |
| `{:snooze, seconds}` | `scheduled` | Delay and retry |

## Quick Decisions

### Which Queue?

- **Critical operations** → High concurrency (20+)
- **Mailers/Webhooks (I/O)** → Medium concurrency (30-50)
- **CPU-intensive** → Low concurrency (3-5)
- **External APIs** → Use `dispatch_cooldown` for rate limiting

### Testing Pattern

```elixir
use Oban.Testing, repo: MyApp.Repo

# Assert enqueued
assert_enqueued worker: MyApp.Worker, args: %{id: 1}

# Execute and verify
assert :ok = perform_job(MyApp.Worker, %{id: 1})
```

## Common Anti-patterns

| Wrong | Right |
|-------|-------|
| `%{user_id: id}` pattern match | `%{"user_id" => id}` (string keys) |
| `%{user: %User{}}` in args | `%{user_id: 1}` (IDs only) |
| No idempotency for payments | Use idempotency keys |
| Ignoring return values | Handle all outcomes explicitly |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/worker-patterns.md` - Worker options, backoff, timeout
- `${CLAUDE_SKILL_DIR}/references/queue-config.md` - Queue design, pool sizing, cron, Smart Engine
- `${CLAUDE_SKILL_DIR}/references/testing-patterns.md` - Testing, assertions, drain (OSS + Pro)
- `${CLAUDE_SKILL_DIR}/references/oban-pro-basics.md` - Pro.Worker, Workflow, Batch, Chunk, Relay, plugins
