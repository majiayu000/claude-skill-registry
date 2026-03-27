---
name: elixir-idioms
description: "OTP/BEAM patterns and core Elixir idioms — GenServer, Supervisor, Task, Registry, pattern matching, with chains, pipes, error tuples, mix tasks. Load for process design, supervision trees, language idiom refactoring, or BEAM debugging. NOT for Ecto/LiveView/Oban/Phoenix — use dedicated skills."
effort: medium
user-invocable: false
---

# Elixir Idioms

Reference for writing idiomatic Elixir code with BEAM-aware patterns.

## Iron Laws — Never Violate These

1. **NO PROCESS WITHOUT A RUNTIME REASON** — Processes model concurrency, state, isolation—NOT code structure
2. **MESSAGES ARE COPIED** — Keep messages small (except binaries >64 bytes)
3. **GUARDS USE `and`/`or`/`not`** — Never use short-circuit operators in guards (guards require boolean operands)
4. **CHANGESETS FOR EXTERNAL DATA** — Use `cast/4` for user input, `change/2` for internal
5. **RESCUE ONLY FOR EXTERNAL CODE** — Never use rescue for control flow
6. **NO DYNAMIC ATOM CREATION** — `String.to_atom(user_input)` causes memory leak (atoms aren't GC'd)
7. **@external_resource FOR COMPILE-TIME FILES** — Modules reading files at compile time MUST declare `@external_resource`
8. **SUPERVISE ALL LONG-LIVED PROCESSES** — Never bare `GenServer.start_link`/`Agent.start_link` in production. Use supervision trees
9. **WRAP THIRD-PARTY LIBRARY APIs** — Always facade external deps behind a project-owned module. Enables swapping without touching callers

## BEAM Architecture (Why Elixir Works This Way)

- **Processes are cheap (2.6KB)** — Spawn liberally for concurrency/isolation
- **Complete memory isolation** — No shared state, no locks needed
- **Messages are copied** (except binaries >64 bytes) — Keep messages small
- **Per-process GC** — No global GC pauses
- **"Let it crash"** — Supervisors restart to known-good state

## Core Principles

1. **Pattern match over conditionals** — Function heads first, then `case`, then `cond`
2. **Tagged tuples for expected failures** — `{:ok, _}`/`{:error, _}` for expected errors, raise for bugs
3. **Pipe operator for data transformation** — Start with data, never pipe single calls
4. **Let it crash** — Handle expected errors, crash on unexpected ones
5. **Explicit over implicit** — Be clear about intentions

## Quick Decision Trees

### Control Flow

```
Need patterns? → case (or function heads)
Multiple operations? → with
Boolean conditions? → cond (multiple) or if (single)
```

### Error Handling

```
Expected failure? → {:ok, _}/{:error, _} tuples
Unexpected/bug? → raise exception (let supervisor handle)
External library? → rescue (only here!)
```

### OTP

```
Need state?
├─ No → Plain functions
├─ Simple get/update → Agent or ETS
├─ Complex messages/timeouts → GenServer
└─ One-off async → Task
```

## Quick Patterns

```elixir
# Pattern match in function head
def process(%{status: :active} = user), do: activate(user)
def process(%{status: :inactive} = user), do: deactivate(user)

# with for happy path
with {:ok, user} <- get_user(id),
     {:ok, order} <- create_order(user) do
  {:ok, order}
end

# Task for async
Task.Supervisor.async_nolink(TaskSup, fn -> work() end)
|> Task.yield(5000) || Task.shutdown(task)
```

## Common Pitfalls

| Wrong | Right |
|-------|-------|
| `length(list) == 0` | `list == []` or `Enum.empty?(list)` |
| `list ++ [item]` | `[item \| list] \|> Enum.reverse()` |
| `String.to_atom(input)` | `String.to_existing_atom(input)` |
| `spawn(fn -> log(conn) end)` | `ip = conn.ip; spawn(fn -> log(ip) end)` |
| `unless condition` | `if !condition` (unless deprecated in 1.18) |

## References

For detailed patterns, see:

- `${CLAUDE_SKILL_DIR}/references/pattern-matching.md` - Pattern matching, guards, binary matching
- `${CLAUDE_SKILL_DIR}/references/otp-patterns.md` - GenServer, Supervisor, Task, Registry
- `${CLAUDE_SKILL_DIR}/references/error-handling.md` - Tagged tuples, rescue, with
- `${CLAUDE_SKILL_DIR}/references/with-and-pipes.md` - When to use `with` and `|>` (idiomatic patterns)
- `${CLAUDE_SKILL_DIR}/references/troubleshooting.md` - Production BEAM debugging (memory, performance, crashes)
- `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` - Common mistakes and fixes
- `${CLAUDE_SKILL_DIR}/references/mix-tasks.md` - Mix task naming, option parsing, shell output
- `${CLAUDE_SKILL_DIR}/references/elixir-118-features.md` - Duration module, dbg improvements (1.18+)
