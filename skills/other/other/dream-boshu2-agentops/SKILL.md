---
name: dream
description: 'Private overnight operator mode. Routes interactive Dream requests to the shared `ao overnight` engine for setup, bedtime runs, and morning reports. Triggers: "$dream", "overnight", "bedtime run", "morning report", "dream setup", "dream report", "dream council", "dreamscape".'
---

# Dream Skill

`$dream` is the interactive surface for the same Dream engine used by
`ao overnight`.

## Compounding Loop (v2)

Dream v2 runs a bounded outer loop of `INGEST -> REDUCE -> MEASURE` iterations until a halt condition fires: wall-clock budget exhausted, plateau (K sub-epsilon deltas in a row), regression beyond a per-metric floor, or metadata integrity failure. Each iteration is atomic and checkpointed so any rollback leaves the corpus clean. Dream is strictly knowledge-only.

Anti-goals (hard constraints):

- NEVER mutates source code.
- NEVER invokes `$rpi` or any code-mutating flow.
- NEVER performs git operations (no commits, branches, push, rebase, checkout).
- NEVER creates symlinks anywhere.
- No swarm/gc fan-out inside iterations in the first slice (serial only).

## Execution Steps

### Step 1: Route the request

- `setup` -> `ao overnight setup`
- `start` or `run` -> `ao overnight start`
- `report` -> `ao overnight report`

### Step 2: Setup lane

Use `ao overnight setup` to inspect host constraints, runner availability,
scheduler mode, and keep-awake behavior.

```bash
ao overnight setup
ao overnight setup --apply --runner codex --runner claude --at 01:30
```

Default to preview. Use `--apply` only when the user explicitly wants Dream
config or scheduler artifacts persisted.

### Step 3: Bedtime run lane

Use `ao overnight start` for the actual private local run.

```bash
ao overnight start --goal "close the loop on today's auth work"
ao overnight start --goal "stabilize release follow-ups" --runner codex --runner claude --creative-lane
$dream start --queue=.agents/dream/tonight.md
$dream start --max-iterations=3
$dream start --warn-only=false
```

Expected behavior:

- operates against the real repo-local `.agents` corpus
- writes `summary.json` and `summary.md` (with per-iteration sub-summary entries for each INGEST -> REDUCE -> MEASURE pass)
- degrades honestly when soft-fail steps or keep-awake helpers are unavailable

### Step 4: Morning report lane

Use `ao overnight report` to render the latest Dream result.

```bash
ao overnight report
ao overnight report --from .agents/overnight/latest
```

When rendering a report, answer four questions fast:

1. What state did I wake up to?
2. What ran overnight?
3. What degraded or failed?
4. What should I do first?

## Key Rules

- Keep Dream settings under the shared `dream.*` control plane.
- Do not promise scheduled execution on a sleeping laptop.
- Do not imply tracked source-code edits overnight.
- GitHub nightly is the public proof harness, not the private Dream engine.

## Delineation vs $evolve

| Lane | Runs | Mutates code? | Mutates corpus? | Outer loop? | Budget |
|------|------|---------------|-----------------|-------------|--------|
| `$dream` | nightly, private local | **No** | **Yes (heavy)** | **Yes (convergence)** | wall-clock + plateau |
| `$evolve` | daytime, operator-driven | Yes (via `$rpi`) | Yes (light) | Yes | cycle cap |

Dream owns the knowledge compounding layer; `$evolve` owns the code compounding layer. Both share fitness-measurement substrate via `corpus.Compute` / `ao goals measure`. Run Dream overnight, then start each day with `$evolve` against the freshly-compounded corpus with a clean fitness baseline.

## See Also

- [Dream Run Contract](../../docs/contracts/dream-run-contract.md)
- [Dream Report Contract](../../docs/contracts/dream-report.md)
