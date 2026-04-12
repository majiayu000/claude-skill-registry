---
name: dream
description: >
  Private overnight operator mode. Routes interactive Dream requests to the
  shared `ao overnight` engine for setup, bedtime runs, and morning reports.
  Use when the user wants to bootstrap Dream, run an overnight compounding
  pass, inspect Dream Council or DreamScape output, or review the latest
  morning report. Triggers: "dream", "overnight", "bedtime run",
  "morning report", "dream setup", "dream report", "dream council",
  "dreamscape".
skill_api_version: 1
user-invocable: true
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [TASK]
  intel_scope: topic
metadata:
  tier: session
  stability: experimental
output_contract: "Dream report artifacts at .agents/overnight/*/summary.{json,md}, per-iteration cycle history at .agents/overnight/*/<runID>/iterations/iter-<N>.json (resumed runs rehydrate from disk), and optional scheduler assistance under .agentops/generated/dream/"
---

# Dream - Private Overnight Operator Mode

`/dream` is the interactive face of the Dream system. It should drive the same
engine as `ao overnight`; do not invent a parallel workflow.

## Purpose

Use Dream to:

- preview or persist Dream setup and scheduler assistance
- run a bounded private overnight compounding pass against the real `.agents/`
  corpus
- render and interpret the latest morning report, including Dream Council and
  DreamScape sections
- explain the difference between the private local Dream lane and the public
  nightly proof harness

## Routing

Map user intent to one of three lanes:

| Intent | Command | Notes |
|--------|---------|-------|
| bootstrap, install, configure Dream | `ao overnight setup` | Default to preview. Use `--apply` only when the user explicitly wants config or scheduler artifacts persisted. |
| run Dream now | `ao overnight start` | Include `--goal` when the user provides one. Use `--runner` and `--creative-lane` only when the user asks for multimodel or wildcard analysis. |
| inspect a prior run | `ao overnight report` | Use `--from <dir-or-summary.json>` for non-default report paths. |

## Compounding Loop (v2)

Dream v2 runs a bounded outer loop of `INGEST -> REDUCE -> MEASURE` iterations until a halt condition fires: wall-clock budget exhausted, plateau (K sub-epsilon deltas in a row), regression beyond a per-metric floor, or metadata integrity failure. Each iteration is atomic and checkpointed so any rollback leaves the corpus clean. Dream is strictly knowledge-only.

Anti-goals (hard constraints):

- NEVER mutates source code.
- NEVER invokes `/rpi` or any code-mutating flow.
- NEVER performs git operations (no commits, branches, push, rebase, checkout).
- NEVER creates symlinks anywhere.
- No swarm/gc fan-out inside iterations in the first slice (serial only).

## Key Rules

- Keep the shared control plane authoritative. Dream settings live under
  `dream.*`; do not duplicate config logic inside the skill.
- Keep platform semantics honest. Never promise scheduled execution on a
  sleeping laptop.
- Keep the first slice bounded. Dream is for close-loop, defrag preview,
  metrics, retrieval proof, optional briefing, and optional artifact-mediated
  council synthesis.
- Do not imply tracked source-code edits overnight unless the runtime actually
  supports them.
- GitHub nightly is the public proof harness. Dream is the private local
  engine.

## Execution Steps

### Step 1: Resolve the operator lane

Interpret the request as `setup`, `start`, or `report`.

Examples:

```bash
/dream setup
/dream setup --apply --runner codex --runner claude --at 01:30
/dream start "close the loop on today's auth work"
/dream report
/dream report --from .agents/overnight/latest
```

### Step 2: Setup lane

Use `ao overnight setup` to inspect the host, available runtimes, scheduler
mode, and keep-awake behavior.

```bash
ao overnight setup
ao overnight setup --apply --runner codex --runner claude --at 01:30
```

Default behavior:

- Preview first when the user asks how Dream would work on this machine.
- Persist with `--apply` only when the user explicitly asks to save config or
  generate scheduler artifacts.

Expected outputs:

- a config preview in terminal, JSON, or YAML
- optional generated scheduler assistance under `.agentops/generated/dream/`

### Step 3: Bedtime run lane

Use `ao overnight start` for the actual local run.

```bash
ao overnight start --goal "close the loop on today's auth work"
ao overnight start --goal "stabilize release follow-ups" --runner codex --runner claude --creative-lane
/dream start --queue=.agents/dream/tonight.md
/dream start --max-iterations=3
/dream start --warn-only=false
```

Expected behavior:

- operates against the real repo-local `.agents` corpus
- writes `summary.json` and `summary.md`
- degrades honestly when soft-fail steps or keep-awake helpers are unavailable

### Step 4: Morning report lane

Use `ao overnight report` to render the latest Dream result.

```bash
ao overnight report
ao overnight report --from .agents/overnight/latest
ao overnight report --from .agents/overnight/latest/summary.json
```

Focus the response on four questions:

1. What state did I wake up to?
2. What ran overnight?
3. What degraded or failed?
4. What should I do first?

## Output

- Dream setup preview or persisted `dream.*` config with optional scheduler
  assistance artifacts
- Dream morning report artifacts:
  - `.agents/overnight/<run>/summary.json`
  - `.agents/overnight/<run>/summary.md`
- A concise operator summary with degraded items and the single highest-signal
  next action
- v2 morning reports also include per-iteration sub-summaries, composite
  `fitness_delta`, and `plateau_reason` / `regression_reason` when applicable

## Examples

```text
Help me get Dream working on this Mac without pretending launchd survives sleep.
```

```text
Run Dream tonight with Codex and Claude, goal: stabilize the Homebrew release follow-up.
```

```text
Read the latest Dream report and tell me the first move.
```

## Reference Documents

- [Dream Run Contract](../../docs/contracts/dream-run-contract.md)
- [Dream Report Contract](../../docs/contracts/dream-report.md)
- [How It Works](../../docs/how-it-works.md)
- [CLI Reference](../../cli/docs/COMMANDS.md)

## Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| `ao overnight setup` suggests `manual` scheduler mode | Host scheduler semantics are ambiguous or unsupported | Keep the run operator-armed, or use generated assistance only after reviewing the host behavior |
| Dream report shows degraded keep-awake | `caffeinate` or the platform helper is unavailable | Continue with the degraded report; do not claim the machine will stay awake |
| No morning report exists | Dream has not been run yet or the output dir is different | Run `ao overnight start`, or point `ao overnight report --from` at the correct directory |
| User expects GitHub nightly to replace local Dream | CI proof harness and local Dream are different surfaces | Explain that nightly proves the contract, while Dream operates on the private local corpus |

## Delineation vs /evolve

| Lane | Runs | Mutates code? | Mutates corpus? | Outer loop? | Budget |
|------|------|---------------|-----------------|-------------|--------|
| `/dream` | nightly, private local | **No** | **Yes (heavy)** | **Yes (convergence)** | wall-clock + plateau |
| `/evolve` | daytime, operator-driven | Yes (via `/rpi`) | Yes (light) | Yes | cycle cap |

Dream owns the knowledge compounding layer; `/evolve` owns the code compounding layer. Both share fitness-measurement substrate via `corpus.Compute` / `ao goals measure`. Run Dream overnight, then start each day with `/evolve` against the freshly-compounded corpus with a clean fitness baseline.

## See Also

- `/handoff` - capture explicit session closeout before bedtime
- `/status` - inspect the current repo state before deciding whether to run Dream
- `/compile` - compile the knowledge corpus when the morning report points at corpus hygiene work
- `/rpi` - run the daytime delivery flow before handing work off to Dream
