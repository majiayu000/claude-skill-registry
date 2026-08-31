---
name: dispatching-parallel-agents
description: "The parallel fan-out primitive. Routed to by any skill or command that splits work across independent units and dispatches an agent per unit — subagent-driven-development, /sprint, parallel /review. It owns the dispatch/collect/funnel discipline: bound concurrency, isolate units, collect every result, dedupe overlap, and funnel through finding-triage then checkpoint-aggregator. Raw agent output is never consumed before the funnel runs; an agent that errors drops its unit without corrupting the batch."
disable-model-invocation: true
---

# dispatching-parallel-agents

Fan out, collect everything, funnel before consuming. Plumbing other skills dispatch through — it owns the parallel discipline, not domain logic.

## Pre-flight

The caller supplies the work. Confirm it, or STOP and surface the gap — never invent units or pick an agent on a hunch:

- **The unit list** — N discrete, independently-completable units of work, each with its scope and target paths.
- **The agent kind** — which agent kind to dispatch per unit (e.g. `backend-author`, `frontend-author`, `scout`, `security-reviewer` at [agents/<name>.md](../../agents/<name>.md)). One kind per batch.
- **The completion contract** — what each agent must return: a structured result, its unit ID, and a pass/fail/error status. Self-reports are claims, not evidence (see Phase 4).

## Phase 1 — Partition · gate: BLOCK

Split the work into units that do not collide. A unit owns a distinct file or path set; two units in one batch MUST NOT mutate the same path.

- **Independent paths** — units touch disjoint files. Dispatch directly. This is the common, fast case.
- **Shared paths unavoidable** — units must mutate the same file or tree. Do NOT dispatch into the conflict. Route to `using-git-worktrees` ([routines/using-git-worktrees/SKILL.md](../using-git-worktrees/SKILL.md)) to give each unit an isolated working tree, or serialize the colliding units into one sequential unit. A shared-path collision in a parallel batch is a corruption, not a merge.

Tag each unit with its ID, scope, target paths, and the agent kind. Read-only batches (review, scout) skip the collision check — they mutate nothing.

Gate: every unit has a disjoint path set, or its overlap is resolved by worktree isolation or serialization. An unresolved collision does not pass.

## Phase 2 — Dispatch · gate: BLOCK

Dispatch one agent per unit, bounded.

- **Concurrency bound** — dispatch in waves of at most a fixed width (default 4 concurrent agents; the caller MAY override). Do not fan out unbounded; a hundred agents at once starves the batch and corrupts nothing useful.
- **Fresh and isolated** — each agent gets only its own unit's scope and the completion contract. No agent sees another's working state. No shared mutable context between units in flight.
- **Hard-stop propagation** — a `tdd` BLOCK, a `commit-gate` failure, a security CRITICAL, or a `[CONFIRM-NN]` inside any unit halts that unit and surfaces immediately; it does not get silently swallowed by the batch.

Gate: every unit is dispatched or explicitly deferred. No unit is dropped silently at dispatch.

## Phase 3 — Collect · gate: BLOCK

Wait for the full wave, then the next, until every unit has terminated. Record each unit's terminal state: `DONE` (returned a result), `ERRORED` (the agent failed), or `DEFERRED` (a hard-stop surfaced).

An `ERRORED` unit drops its own work — its partial output is discarded, never half-applied — and is logged against its unit ID. **One errored unit MUST NOT corrupt or discard the batch.** The remaining units' results stand. Record the error for the funnel; do not retry blindly inside this phase.

Gate: every unit has a terminal state and `DONE` results are captured intact. A still-running or unaccounted unit blocks Phase 4 — partial collection does not pass.

## Phase 4 — Dedupe · gate: BLOCK

Parallel agents over adjacent units produce overlapping findings — the same issue reported by two units, the same fix proposed twice. Collapse them before anything downstream sees the batch.

- Merge findings that name the same defect at the same location into one, keeping the highest severity reported.
- Reconcile contradictory results across units (two units that disagree on the same fact) into a single surfaced conflict, not a silent pick.
- Verify any "done" claim that gates real work: re-run the proving command fresh and read its output and exit code. A subagent's self-report is a claim — never trust it as evidence of completion.

Gate: the result set is deduped, contradictions surfaced, and completion claims verified by fresh evidence. Raw, un-deduped agent output MUST NOT reach Phase 5.

## Phase 5 — Funnel · gate: STOP

The batch is consumed only here, through the fixed funnel — never directly by the caller.

1. Dispatch `finding-triage` ([agents/finding-triage.md](../../agents/finding-triage.md)) over the deduped result set: it classifies severity, marks out-of-scope items with an inline `[NEEDS-TRIAGE]` marker, and discards noise.
2. Hand the triaged set to `checkpoint-aggregator` ([agents/checkpoint-aggregator.md](../../agents/checkpoint-aggregator.md)): it aggregates into the single batch verdict the caller consumes — pass, or a blocking finding list.

The errored and deferred units from Phase 3 ride through the funnel as findings — an `ERRORED` unit is a finding the caller must see, not a silent gap.

Gate: the caller receives only the aggregated verdict. Bypassing the funnel — consuming raw or merely-deduped agent output — is a gate violation. STOP and return the verdict.

## Hard rules

- MUST NOT dispatch two units that mutate the same path in one batch; isolate via `using-git-worktrees` or serialize.
- MUST NOT fan out unbounded; dispatch within the concurrency bound.
- MUST NOT let one `ERRORED` unit discard or corrupt the rest of the batch.
- MUST NOT consume agent output before the `finding-triage` → `checkpoint-aggregator` funnel runs.
- MUST NOT trust a subagent's self-reported completion; verify with a fresh proving command.
- MUST NOT silently drop a unit — every unit terminates with a recorded state that rides through the funnel.
