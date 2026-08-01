---
name: ca-sprint
description: Autonomous sprint — one interactive spec gate, then plan-to-PR execution with every auto-decision SMARTS-scored and logged. Hard gates remain true stops.
argument-hint: "[goal] [--farm]"
---

# /ca-sprint — autonomous sprint

The autonomy mode. Brainstorm a sprint spec with the user — the one interactive gate — then execute
the approved plan end-to-end without per-batch checkpoints, deciding "as the user" via SMARTS on
every non-hard-gate point. Every auto-decision lands in `.codearbiter/sprint-log.md` (append-only)
with a confidence flag; the `low`-confidence entries are exactly what the user reviews afterward.
Nothing is hidden behind autonomy.

## Flow

Load and follow `<plugin-root>/SPRINT.md` — it is the procedure. In brief:

1. **Sprint spec (STOP)** — `brainstorming` scoped to a sprint, then `writing-plans`. Explicit user
   approval of spec AND plan before autonomy begins.
2. **Autonomous execution (BLOCK)** — `subagent-driven-development` runs the plan; test-first via
   `tdd`, two-pass reviewed, fresh-run verified. SMARTS decides non-hard-gate points; everything logs.
3. **Land & summarize (BLOCK)** — `commit-gate`, then `finishing-a-development-branch`, which
   auto-selects open-PR. `/ca-sprint` never merges and never discards; the merge decision is the user's.

Hard gates — `security-controls`, crypto/secrets/auth, irreversible ops, `/override`, an
unresolvable `[CONFIRM-NN]`, merge-to-default — are NEVER auto-decided. They halt and surface.

## Arguments

- **`"goal"`** — seed for the sprint-spec brainstorm.
- **`--farm`** — cost-arbitrage backend: cheap workers implement under the same gates; Claude still
  authors spec, failing tests, plan, and reviews everything. Pre-flights `FARM_API_KEY`.

## Routes to

`<plugin-root>/SPRINT.md` (mode body), which routes through `brainstorming`,
`writing-plans`, `subagent-driven-development`, `commit-gate`, `finishing-a-development-branch`.

## When NOT to use

- A single feature with human checkpoints → `/ca-feature`.
- Work whose spec cannot be made concrete up front — the one interactive gate is load-bearing;
  a thin spec makes hard-gate stops frequent instead of rare.
