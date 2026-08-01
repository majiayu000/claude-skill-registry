---
name: crew
description: Use when dispatching two or more concurrent subagents whose work could touch overlapping files, or when concurrent delegated work needs a live answer to "who is running and what do they own".
---

Coordinate concurrent agents through the `crew` CLI in this skill's directory.

- Learn commands on demand, never from memory: `node crew.mjs help`, then `help <command>`.
- First use on a machine: `node crew.mjs selftest` must pass.

## Dispatching (router)

1. Decompose into nodes with disjoint scopes; encode known dependencies as blocked-by edges. A task whose scope overlaps everything (sync, codegen, formatting) gets a blocking edge, not a lease.
2. `add` each node before spawning; pass the printed id into the agent's prompt as `CREW_ID`, with the worker rules below.
3. Dispatch the `ready` frontier in parallel; re-dispatch as edges clear. Cap concurrency at 4–6 agents.
4. Observe with `roster` and `tree`; redirect only on conflict or stall.
5. Verify against the claim log: edits outside any lease, or a forced claim, fail verification.
6. Research fan-out: no file scopes — put each agent's assigned angle in its node's task text; never assign the same angle twice.

## Working (embed in every spawned prompt)

- Prefix every command with `CREW_FILE` and your `CREW_ID`.
- `start` then `me` on entry. `claim` before any edit; on conflict, work an unclaimed part first and retry — never `--force`. `release` after each edit. Decompose big work under your own id with `add --parent`. `done` on exit.
- To block on a contended file, use `claim <glob> --wait [--timeout SEC]` — never a hand-rolled `if ! claim; then sleep` loop (a shell loop cannot tell exit 3, a real conflict, from exit 127, a command that never ran).
- Invoke crew inline on every call (`node <abs>/crew.mjs ...`). Never store `node <path>` in a shell variable and call `$VAR` — zsh will not word-split it, so the command never runs (exit 127).
- Never edit outside your leases.
- Spawning your own sub-agent? Mint it a node first and set the child's `CREW_ID` to that new id — env vars inherit, and a child acting under your identity corrupts ownership.
