---
name: lead-refactor
description: Autonomous comprehensive refactoring. Three-phase pipeline — Phase 1 /refactor (tactical, loops internally to convergence) → Phase 2 loop of /review-arch + /implement-batch until architectural findings converge below a severity floor (default HIGH+) → Phase 3 /refactor (catches tactical issues introduced by restructuring). Auto-approves /review-arch ticket proposals; pulls the andon cord on contested findings, breaking-change proposals, repeated implementation failure, or Phase-2 hard-cap exhaustion (5 architectural iterations).
model: opus
---

# Lead-Refactor — Autonomous Comprehensive Refactoring

Drives a codebase through tactical cleanup, architectural restructuring, and a final tactical cleanup pass — all without operator involvement between startup and termination. The operator states scope, severity floor, constraints, and refactor aggression at startup; the skill then runs a three-phase pipeline that picks up where each previous phase converges.

This skill is the orchestrator-family member that pairs tactical refactoring with architectural review. It is a narrower sibling of `/lead-project` and a peer of `/lead-bug-hunt`. Unlike `/lead-bug-hunt`'s convergence loop, `/lead-refactor` has a fixed three-phase shape: each phase converges internally (via the sub-skills' own loops) rather than via a global loop over the macro phases.

## Philosophy

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template.

### Three phases, each internally convergent

Phase 1 invokes `/refactor`, which loops internally until no more tactical improvements remain. Phase 2 runs `/review-arch` and acts on findings at or above the severity floor via `/implement-batch`, re-running `/review-arch` until it produces no findings above the floor (or the architectural-iteration hard cap of 5 is hit). Phase 3 invokes `/refactor` again to catch any tactical issues introduced by Phase 2's structural changes.

There is no global loop over the macro phases. `/refactor` converging once and then `/review-arch` converging is sufficient — `/refactor`'s tactical scope (DRY, dead code, naming, complexity) does not generate new architectural opportunities, and `/review-arch`'s noun analysis is stable across re-runs. Two `/refactor` invocations and one Phase-2 inner loop is the right shape.

### Auto-approval is delegated to the autonomy discipline

`/review-arch` is advisory; its ticket proposals are auto-approved under `/lead-refactor` per the orchestrator-family contract documented in [`references/autonomy.md`](../../references/autonomy.md) § "Auto-approval of sub-skill ticket proposals". The commander's-intent severity floor (field 2) is applied at the Phase-2 triage step (2b), not at the approval moment. The completion report lists every ticket created.

### Trust the analysis, escalate the disagreement

`/review-arch` produces findings backed by noun-analysis evidence. This skill **trusts findings at or above the severity floor as actionable** — they are real architectural opportunities by `/review-arch`'s contract. The skill does not silently dismiss findings. If the skill genuinely believes a finding is wrong (the proposed restructuring would break a constraint, the finding misreads the domain model), that is an andon trigger ("contested finding"), not a unilateral disregard. No escape hatches.

### Broad authority, narrow gates

The skill may: invoke `/refactor`, `/review-arch`, `/implement-batch`, `/implement`; create tickets via auto-approved `/review-arch` proposals; commit refactoring work via sub-skills; create and modify the working branch.

The skill may NOT without explicit authorization: push or merge to main/master, force-push, propose breaking changes (see `references/autonomy.md` § "No unilateral breaking changes"), invoke other skills outside the bounded repertoire, install dependencies, run irreversible destructive operations.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                    LEAD-REFACTOR WORKFLOW                        │
├──────────────────────────────────────────────────────────────────┤
│  0. Startup                                                      │
│     ├─ 0a. Branch and working-tree check                         │
│     ├─ 0b. Resume existing run or start fresh                    │
│     ├─ 0c. Elicit commander's intent (4 fields)                  │
│     └─ 0d. Seed LEAD_REFACTOR_STATE.md                           │
│                                                                  │
│  1. Phase 1: Tactical refactor                                   │
│     └─ Invoke /refactor (loops internally to convergence)        │
│                                                                  │
│  2. Phase 2: Architectural review loop (max 5 iterations)        │
│     ├─ 2a. Invoke /review-arch (auto-approves ticket proposals)  │
│     ├─ 2b. Triage findings against severity floor                │
│     ├─ 2c. Form batch, invoke /implement-batch                   │
│     ├─ 2d. Verify tests pass                                     │
│     └─ 2e. Convergence check (re-run /review-arch)               │
│                                                                  │
│  3. Phase 3: Final tactical refactor                             │
│     └─ Invoke /refactor (catches tactical issues from Phase 2)   │
│                                                                  │
│  4. Termination                                                  │
│     ├─ 4a. Final verification pass                               │
│     └─ 4b. Completion report                                     │
└──────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 0. Startup

Follow the shared startup protocol in [`references/lead-startup.md`](../../references/lead-startup.md). Skill-specific values:

- **0a. Branch and working-tree check** — branch-name pattern: `lead-refactor/<date>` (e.g., `lead-refactor/2026-05-12`).
- **0b. Resume existing run or start fresh** — state-doc filename: `LEAD_REFACTOR_STATE.md`. "Resume as-is" semantic: re-verify the current phase's state, then continue.
- **0c. Elicit commander's intent** — four fields per the schema in [`references/autonomy.md`](../../references/autonomy.md) § "Commander's-intent schemas per skill / `/lead-refactor`". Push-back examples specific to this skill: "Clean it all up" is not a scope — ask which modules; "Whatever severity" is not a floor — push for HIGH+ as the productive default.
- **0d. Seed `LEAD_REFACTOR_STATE.md`** — include the four pinned intent fields, `Current phase: phase-1`, an empty cycle log, and an empty findings ledger. Gitignore the state doc per the protocol.

### 1. Phase 1: Tactical Refactor

Invoke `/refactor` with:
- **Scope** — from commander's intent field 1.
- **Aggression ceiling** — from commander's intent field 4.

`/refactor` loops internally until no more tactical improvements remain. Suppress `/refactor`'s built-in `/tidy-docs` pass (step 7 in `/refactor`) — `/lead-refactor` does not include a documentation finisher; the operator can run `/tidy-docs` separately if needed.

After `/refactor` concludes:
- Verify tests pass.
- Record outcome in the cycle log: commits made, net diff, batches completed.
- Update state doc: current phase becomes `phase-2`.

If tests fail after Phase 1 — andon cord (regression introduced by tactical refactor).

### 2. Phase 2: Architectural Review Loop

Bounded loop with max 5 architectural iterations. Each iteration has five sub-phases.

#### 2a. Invoke `/review-arch`

Run `/review-arch` with:
- **Scope** — from commander's intent field 1.

When `/review-arch` reaches its ticket-proposal step, auto-approve. Record in the cycle log: ticket IDs proposed, scope of the proposal, and the fact that auto-approval was applied per commander's intent.

#### 2b. Triage findings

For each finding produced by `/review-arch`:

1. **Classify against severity floor:**
   - At or above floor → fix-list (blocks Phase 2 convergence).
   - Below floor → deferred list. Record in `## Deferred findings` with severity and a one-line summary.

2. **Screen for contested findings.** If the skill believes a finding is wrong on substance (the proposed restructuring contradicts a constraint in commander's intent, the finding misreads the domain model), do not silently dismiss it. Record in `## Contested findings` and pull the andon cord.

3. **Screen for breaking-change implications.** If a finding's proposed restructuring would require a breaking change (per `references/autonomy.md` § "No unilateral breaking changes"), record in `## Breaking-change findings` and pull the andon cord. Do not auto-fix.

#### 2c. Decide

Three possible outcomes:

- **Form a batch and proceed to 2d** — fix-list non-empty, no contested or breaking-change findings.
- **Escalate and pull the andon cord** — contested findings or breaking-change findings exist.
- **Phase 2 converged, proceed to Phase 3** — fix-list empty (no findings above floor this iteration).

Batches are per-iteration. Don't co-mingle with prior iterations' tickets — verification stays tight.

Record the chosen outcome and rationale in the cycle log.

#### 2d. Act

Execute the batch via `/implement-batch` (or `/implement` for single-ticket batches when `/implement-batch` would be ceremony).

After the batch completes:
- Verify the full test suite still passes.
- Build/typecheck/lint clean.
- No constraint violations in the new commits.

If tests fail — andon cord (regression introduced by architectural change).

Sub-skill escalations cascade up per `references/autonomy.md` § "Cascade rule."

#### 2e. Convergence check

- Iteration counter increments by 1.
- If iteration counter reaches 5 → andon cord (Phase 2 hard cap; the architectural loop is not converging — operator should review).
- Otherwise → return to 2a.

Phase 2 ends when 2c determines the fix-list is empty (no findings above floor on the most recent `/review-arch` run). Update state doc: current phase becomes `phase-3`.

### 3. Phase 3: Final Tactical Refactor

Invoke `/refactor` again with the same scope and aggression as Phase 1. This catches tactical issues introduced by Phase 2's restructuring (renamed-but-not-cleaned modules, redundant code paths after consolidation, dead imports left from moves).

`/refactor` loops internally to convergence. Suppress its built-in `/tidy-docs` pass.

After `/refactor` concludes:
- Verify tests pass.
- Record outcome in the cycle log.
- Update state doc: current phase becomes `termination`.

If tests fail — andon cord.

### 4. Termination

#### 4a. Final verification pass

Before declaring done:

- Full test suite passes.
- No constraint violations in commits on this branch.
- Build/typecheck/lint clean.

If any check fails, treat as a blocker — return to Phase 3 to address.

#### 4b. Completion report

```
## Lead-Refactor Complete

### Commander's intent
[All four fields, verbatim]

### Outcome
[One paragraph: did the pipeline complete cleanly? Did Phase 2 converge
 within the 5-iteration cap? Were there contested or breaking-change
 findings that surfaced? Note any caveats.]

### Phase summary
- Phase 1 (tactical): N commits, net -X/+Y lines
- Phase 2 (architectural): N iterations, K tickets fixed, M tickets deferred
- Phase 3 (tactical cleanup): N commits, net -X/+Y lines

### Top things to scrutinize
[Three to five items where the skill's judgment is most likely to need
 review. Each item: one sentence + artifact (SHA, ticket ID, file:line).
 Examples: aggressive triage calls in Phase 2, batches with multiple
 attempts, areas where /review-arch findings were close-to-floor.]

### Tickets created and fixed (Phase 2)
- [#N] <title> — fix SHA <short> — /review-arch finding type
- [#N+1] <title> — fix SHA <short>
- ...

### Deferred findings (below severity floor)
[/review-arch findings not gated by the floor. Operator may run another
 iteration with a lower floor to address them.]
- [Medium | iteration 1] <description>
- [Low | iteration 2] <description>
- ...

### Contested or breaking-change findings (if any escalated)
- [contested | iteration 3] <description> — andon-cord SHA <short> in state doc
- ...

### Constraint adherence
[Confirm no violations. If any close calls, name them with commit SHAs.]

### Changes summary
- Branch: <branch name> (SHA <short>)
- Base: <base branch> (SHA <short>)
- Commits on branch: N (Phase 1: P1 + Phase 2 fixes: P2 + Phase 3: P3)
- Net lines: +X/-Y

### Run metadata
- Phase 2 iterations: N of 5
- Andon-cord pulls during run: N (each with handoff in state doc)
- Duration (wall-clock, approximate)
```

The operator decides whether to merge, run another iteration (e.g., with a lower severity floor), or pause.

## Commander's Intent — Field Reference

### Scope

Same shape as `/refactor`'s and `/review-arch`'s scope questions. Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session` — recent rewrite, want comprehensive cleanup."
- "All production code, with extra attention to `pkg/legacy` (slated for restructuring)."

### Severity floor

The lowest `/review-arch` severity that gates Phase 2 convergence.

| Floor              | Effect                                                                                                       |
|--------------------|--------------------------------------------------------------------------------------------------------------|
| CRITICAL only      | Loops only on CRITICAL findings. Ships with HIGH+MEDIUM+LOW deferred. Use for "fix only the worst" sweeps.   |
| HIGH+              | **Default.** Acts on HIGH and CRITICAL architectural findings; defers MEDIUM and LOW.                        |
| MEDIUM+            | Acts on MEDIUM and above. Phase 2 may not converge in 5 iterations on large codebases.                       |
| All severities     | Not recommended. `/review-arch` tends to find LOW-severity opportunities indefinitely; unlikely to converge. |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes).

Examples:
- "Do not modify the public API of package `auth`."
- "Do not touch `pkg/legacy` (slated for removal next quarter)."
- "Must remain Go 1.22 compatible."

### Refactor aggression

Aggression ceiling for both `/refactor` passes (Phase 1 and Phase 3). Mirrors `/refactor`'s vocabulary.

| Setting       | Effect                                                                                                                |
|---------------|-----------------------------------------------------------------------------------------------------------------------|
| conservative  | Only SAFEST and SAFE categories — dead code, formatters, simple DRY, single-use indirection.                           |
| moderate      | **Default.** Adds cross-module DRY, splitting files, removing abstraction layers.                                      |
| aggressive    | Adds removal of legacy code with unclear purpose, consolidating similar-but-not-identical behavior.                    |

## Severity & Triage

Triage is mechanical, not judgment-based. The severity floor is the only knob.

- **Floor and above** → fix-list, blocks Phase 2 convergence until resolved via `/implement-batch`.
- **Below floor** → deferred list, recorded in state doc and completion report, does not block.
- **Contested on substance** → andon cord, not silent dismissal.
- **Breaking change required** → andon cord, not auto-fix.

The skill does NOT:
- Re-rank `/review-arch`'s severity classifications. The reviewer's judgment stands.
- Bargain findings down to make convergence easier.
- Dismiss findings because "the analysis seems wrong" — that's the contested-finding path.

## Andon Cord Protocol

Follow the shared handoff template and per-skill extension protocol in [`references/autonomy.md`](../../references/autonomy.md) § "Shared handoff template" and § "Per-skill handoff extensions". Skill-specific values:

- **Title format** — `## Andon Cord — /lead-refactor — Phase N` (the phase is load-bearing).
- **Current-state additions:**
  - `Current phase: <phase-1 | phase-2 | phase-3 | termination>`
  - `Phase 2 iteration counter: <N>` (if currently in Phase 2)
  - `Findings ledger: <K fixed, M deferred, L contested>` (if currently in Phase 2)
  - `State doc pointer: see LEAD_REFACTOR_STATE.md`

### Andon cord triggers

Pull the cord when:

- **Contested finding.** The skill believes a `/review-arch` finding is wrong on substance — the proposed restructuring contradicts a constraint in commander's intent, or the finding misreads the domain model.
- **Breaking-change required.** A `/review-arch` recommendation requires a breaking change (per `references/autonomy.md` § "No unilateral breaking changes").
- **Regression introduced.** A `/refactor` or `/implement-batch` invocation made the test suite fail in ways unrelated to the targeted change.
- **Sub-skill cord cascaded up.** `/refactor`, `/review-arch`, `/implement-batch`, or `/implement` pulled its own cord for a reason this skill cannot resolve.
- **Phase 2 hard cap hit.** 5 architectural iterations elapsed without convergence. Something is likely structurally wrong (severity floor set too low, or the codebase has a recurring architectural pattern the reviewer keeps flagging).
- **Repeated batch failure.** `/implement-batch` fails on the same finding 3 times across different approaches.
- **Resume-time HEAD divergence.** On resume, recorded branch SHA does not match current HEAD.

## State Management

### `LEAD_REFACTOR_STATE.md`

Maintained at the repo root. Gitignored. Survives across invocations.

**Structure:**

```markdown
# Lead-Refactor State

Started: <timestamp>
Branch: <branch-name>
Branch SHA at startup: <short SHA>
Base branch: <main-branch>
Base SHA at startup: <short SHA>
Last cycle HEAD: <short SHA>
Current phase: <phase-1 | phase-2 | phase-3 | termination>
Phase 2 iteration: N (if applicable)
Status: <active | paused-on-andon | complete>

## Commander's Intent

### Scope
<verbatim>

### Severity floor
<CRITICAL only | HIGH+ | MEDIUM+ | All>

### Constraints
- <constraint 1>

### Refactor aggression
<conservative | moderate | aggressive>

## Cycle log

### Phase 1 — <timestamp> — HEAD <short SHA>
- /refactor invoked with aggression <X>, scope <Y>
- Outcome: N commits, net -X/+Y lines, tests pass

### Phase 2 — Iteration 1 — <timestamp> — HEAD <short SHA>
- /review-arch: <findings count by severity>, tickets proposed <#N..#M>
- Triage: <count above floor | below floor | contested | breaking>
- Decide: <form batch | escalate | converged>
- Act: /implement-batch outcome, fix SHAs
- Verify: tests pass / fail

### Phase 2 — Iteration 2 ...

### Phase 3 — <timestamp> — HEAD <short SHA>
- /refactor invoked, outcome: ...

## Findings ledger

### Fixed (Phase 2)
- [iteration 1 | ticket #14] <description> — fix SHA <short>
- ...

### Deferred (below floor)
- [Medium | iteration 1] <description>
- ...

### Contested
- [iteration 3] <description> — andon cord pulled, see § Andon Cord history

### Breaking-change-required
- [iteration 2] <description> — andon cord pulled, see § Andon Cord history

## Andon cord history

### Phase 2 iteration 3 pull
<full handoff text, pasted>

## Open questions

- <question>
```

**Update at every phase transition and every Phase 2 iteration.** The state doc is the durable orientation — losing it means losing the agent's memory.

### `.gitignore`

Ensure `LEAD_REFACTOR_STATE.md` is ignored. Commit the `.gitignore` change on the working branch at startup if needed.

## Hard Caps

- **Phase 2: 5 architectural iterations** — each iteration is one full `/review-arch` + one batch-implementation. If the loop hits 5 without convergence, the architectural shape is not stable under the current severity floor or scope; pull the andon cord.
- **3 consecutive failed batches** — if `/implement-batch` fails on the same finding 3 times across different approaches, pull the andon cord.
- **No file-touch or dependency-change budgets** — explicitly excluded per `references/autonomy.md` § "Risk budgets."

## Integration with Other Skills

**Relationship to `/refactor`:**

`/lead-refactor` invokes `/refactor` twice — once in Phase 1 (clear tactical noise before architectural analysis) and once in Phase 3 (catch tactical issues introduced by Phase 2's restructuring). Run `/refactor` directly when you want only tactical cleanup; run `/lead-refactor` when you want the full tactical + architectural + tactical pipeline.

**Relationship to `/review-arch`:**

`/lead-refactor`'s Phase 2 invokes `/review-arch` repeatedly until findings converge below the severity floor. `/review-arch`'s ticket proposals are auto-approved per the orchestrator-family contract. Run `/review-arch` directly when you want an advisory architectural read-out without implementation.

**Relationship to `/lead-project`:**

`/lead-project` is the open-ended orchestrator — it takes broad commander's intent and decides which skills to invoke. `/lead-refactor` is a fixed-shape three-phase pipeline for one specific outcome. Use `/lead-project` when refactoring is one of several concerns; use `/lead-refactor` when comprehensive refactoring is the sole objective. `/lead-project` may invoke `/lead-refactor` as a sub-skill when its Decide phase identifies a refactor sweep as the next move.

**Relationship to `/lead-bug-hunt`:**

Sibling orchestrator-family skill with a different outcome contract. `/lead-bug-hunt` eliminates bugs above a severity floor; `/lead-refactor` cleans up code structure above a severity floor. Both use the same auto-approval contract for sub-skill ticket proposals and the same 4-field commander's intent shape (scope, severity floor, constraints, aggression-or-finisher).

**Out-of-axis skills:**

`/review-*` skills other than `/review-arch`, `/scope-project`, `/test-mutation`, `/tidy-docs`, `/tidy-git`, `/bug-*` are not in this skill's repertoire. If your goal mixes refactoring with bug elimination, security review, doc tidying, or test surveying, use `/lead-project` instead. `/lead-refactor` is deliberately narrower.

If you want doc cleanup after refactoring, run `/tidy-docs` separately after `/lead-refactor` completes — structural changes in Phase 2 commonly invalidate inline docs and code examples.
