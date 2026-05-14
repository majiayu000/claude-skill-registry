# /lead-refactor — Autonomous Comprehensive Refactoring

## Overview

The `/lead-refactor` skill drives a codebase through tactical cleanup, architectural restructuring, and a final tactical cleanup pass — all without operator involvement between startup and termination. The operator states **scope, severity floor, constraints, and refactor aggression** at startup; the skill then runs a three-phase pipeline:

1. **Phase 1 — `/refactor`** (tactical, loops internally to convergence)
2. **Phase 2 — `/review-arch` + `/implement-batch` loop** (bounded to 5 iterations; converges when `/review-arch` produces no findings above the severity floor)
3. **Phase 3 — `/refactor` again** (catches tactical issues introduced by Phase 2's restructuring)

This skill is a member of the **orchestrator family** and implements the autonomy discipline documented in [`references/autonomy.md`](../../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template.

`/lead-refactor` is the successor to `/refactor-deep`. The v10 rename moves the skill into the `/lead-*` namespace where its autonomy-axis identity is explicit; the redesign adds a Phase-2 convergence loop (acting on HIGH+ architectural findings via `/implement-batch` until clean) and restores the Phase-3 final-refactor pass that was dropped when `/review-arch` became advisory in v8.

**Key benefits:**
- Unattended comprehensive refactoring — kick it off and walk away
- Three phases, each internally convergent — no global loop needed
- Mechanical triage against a stated severity floor — no rationalization
- Auto-approves `/review-arch` ticket proposals per the orchestrator-family contract
- `LEAD_REFACTOR_STATE.md` as persistent state across sessions
- Phase 3 catches tactical issues that Phase 2's restructuring introduces — without it, refactors that move code around can leave dead imports, redundant guards, and stale naming

## When to Use

**Use `/lead-refactor` for:**
- Comprehensive cleanup sweeps where you want both tactical hygiene and architectural restructuring
- Long-lived codebases that have accumulated structural debt
- Post-feature-burst cleanup, where rapid feature work left tactical and structural drift
- Any time you'd otherwise run `/refactor` → `/review-arch` → `/implement-batch` → `/refactor` by hand

**Don't use `/lead-refactor` for:**
- Tactical-only cleanup (use `/refactor` directly)
- Architectural read-out without implementation (use `/review-arch` directly)
- Mixed work that includes feature implementation, bug elimination, or doc cleanup (use `/lead-project`)
- Bug elimination (use `/lead-bug-hunt`)

**Rule of thumb:** if you find yourself repeatedly running `/refactor`, accepting `/review-arch`'s proposed tickets, implementing them via `/implement-batch`, and re-running `/refactor` to clean up afterwards, `/lead-refactor` is the right abstraction.

## Relationship to `/refactor` and `/review-arch`

| Dimension                | `/refactor`                                                   | `/review-arch`                                              | `/lead-refactor`                                                                |
|--------------------------|---------------------------------------------------------------|-------------------------------------------------------------|---------------------------------------------------------------------------------|
| Mode                     | Autonomous tactical loop                                      | Advisory architectural read-out                             | Autonomous three-phase pipeline                                                 |
| Output                   | Committed tactical cleanups                                   | Target blueprint + proposed tickets                         | Committed tactical + architectural changes                                      |
| Ticket approval          | N/A (no tickets)                                              | Operator-approved at end of pass                            | Auto-approved per commander's intent                                            |
| Architectural changes    | Out of scope                                                  | Proposed only                                               | Implemented via `/implement-batch` until convergence                            |
| Termination              | End of internal loop (no improvements remain)                 | End of single pass                                          | Phase 3 completion + final verification                                         |
| Duration                 | Bounded by tactical findings                                  | Roughly predictable                                         | Open-ended (Phase 2 capped at 5 iterations)                                     |

## Relationship to `/lead-project`

| Dimension                | `/lead-project`                                            | `/lead-refactor`                                                                |
|--------------------------|-------------------------------------------------------------|---------------------------------------------------------------------------------|
| Input                    | Five-field commander's intent (broad)                       | Four-field commander's intent (narrow, refactor-specific)                       |
| Loop shape               | OODA, open-ended action space                               | Fixed: Phase 1 → Phase 2 loop → Phase 3                                          |
| Sub-skill repertoire     | All implement/refactor/review/think/bug skills              | Only `/refactor`, `/review-arch`, `/implement-batch`, `/implement`               |
| Termination              | Mechanical end-state conditions + quiescence                | Phase 3 completion + final verification pass                                    |
| Hard cap                 | 50 OODA cycles                                              | 5 Phase-2 architectural iterations                                              |
| Use when                 | Refactoring is one of several concerns                      | Comprehensive refactoring is the sole objective                                 |

`/lead-project` may invoke `/lead-refactor` as a sub-skill when its Decide phase identifies a refactor sweep as the next move.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /lead-refactor Workflow                                         │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  0. STARTUP                                  │
 │  ────────────────────────────────────────    │
 │  0a. Branch and working-tree check           │
 │  0b. Resume existing run or start fresh      │
 │  0c. Elicit commander's intent (4 fields)    │
 │  0d. Seed LEAD_REFACTOR_STATE.md             │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  1. PHASE 1 — Tactical refactor              │
 │  ────────────────────────────────────────    │
 │  Invoke /refactor (aggression from intent)   │
 │  /refactor loops internally to convergence   │
 │  Suppress /refactor's /tidy-docs step        │
 │  Verify tests pass                           │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  2. PHASE 2 — Architectural loop (max 5)     │
 │  ────────────────────────────────────────    │
 │  2a. /review-arch (auto-approve proposals)   │
 │  2b. Triage findings against severity floor  │
 │      - at/above floor → fix-list             │
 │      - below floor → deferred                │
 │      - contested → andon cord                │
 │      - breaking → andon cord                 │
 │  2c. Form batch | escalate | converged       │
 │  2d. /implement-batch + verify               │
 │  2e. Convergence check (increment counter)   │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  3. PHASE 3 — Final tactical refactor        │
 │  ────────────────────────────────────────    │
 │  Invoke /refactor again, same aggression     │
 │  Catches tactical issues from Phase 2        │
 │  Suppress /refactor's /tidy-docs step        │
 │  Verify tests pass                           │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  4. TERMINATION                              │
 │  ────────────────────────────────────────    │
 │  4a. Final verification pass                 │
 │  4b. Completion report                       │
 └──────────────────────────────────────────────┘
```

## Commander's Intent

Elicited interactively at startup, frozen for the duration of the run. Four fields:

### Scope

What the pipeline covers. Same shape as `/refactor`'s and `/review-arch`'s scope.

Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session`."
- "All production code, with extra attention to `pkg/legacy`."

### Severity floor

The lowest `/review-arch` severity that gates Phase 2 convergence.

| Floor              | Effect                                                                                                       |
|--------------------|--------------------------------------------------------------------------------------------------------------|
| CRITICAL only      | Fastest convergence; ships with HIGH+MEDIUM+LOW deferred. "Fix only the worst" mode.                          |
| HIGH+              | **Default.** Acts on HIGH and CRITICAL; defers MEDIUM and LOW.                                                |
| MEDIUM+            | Acts on MEDIUM and above. Phase 2 may not converge in 5 iterations on large repos.                            |
| All severities     | Not recommended. `/review-arch` finds LOW-severity opportunities indefinitely; unlikely to converge.          |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes).

Examples:
- "Do not modify the public API of package `auth`."
- "Do not touch `pkg/legacy`."
- "Must remain Go 1.22 compatible."

### Refactor aggression

Aggression ceiling for both `/refactor` passes (Phase 1 and Phase 3).

| Setting       | Effect                                                                                                          |
|---------------|-----------------------------------------------------------------------------------------------------------------|
| conservative  | Only SAFEST and SAFE categories — dead code, formatters, simple DRY, single-use indirection.                     |
| moderate      | **Default.** Adds cross-module DRY, splitting files, removing abstraction layers.                                |
| aggressive    | Adds removal of legacy code with unclear purpose, consolidating similar-but-not-identical behavior.              |

## The Three Phases

### Phase 1 — Tactical refactor

`/refactor` is invoked with the elicited scope and aggression. It loops internally to convergence — when no more tactical improvements remain, it returns. `/refactor`'s built-in `/tidy-docs` step is suppressed (`/lead-refactor` does not include a documentation finisher).

Verification: full test suite passes after Phase 1. If not — andon cord.

### Phase 2 — Architectural review loop (bounded to 5 iterations)

Five sub-phases per iteration:

1. **`/review-arch`** — auto-answer scope from commander's intent. Auto-approve any ticket proposals.
2. **Triage** — classify findings against the severity floor. Above floor → fix-list. Below floor → deferred. Contested or breaking-change → andon cord.
3. **Decide** — form batch (proceed to 2d), escalate (andon cord), or converged (proceed to Phase 3).
4. **Act** — `/implement-batch` (or `/implement` for single-ticket batches). Verify tests pass.
5. **Convergence check** — increment iteration counter. If 5 hit without convergence → andon cord.

Phase 2 ends when `/review-arch` produces no findings above the floor on the most recent run.

### Phase 3 — Final tactical refactor

`/refactor` again, same scope and aggression. This phase exists because Phase 2's architectural changes can introduce tactical issues — moved functions leave dead imports, consolidated modules leave redundant code paths, renamed types leave stale comments. `/refactor` cleans those up.

Verification: full test suite passes after Phase 3. If not — andon cord.

### Termination

Final verification pass (tests, build, lint, constraints), then a completion report ordered by review priority. See SKILL.md § 4b for the full template.

## The Andon Cord

The only planned escalation path. See `references/autonomy.md` § "Shared handoff template" for the canonical structure.

### Triggers

- **Contested finding.** The skill believes a `/review-arch` finding is wrong on substance.
- **Breaking-change required.** A `/review-arch` recommendation requires a breaking change.
- **Regression introduced.** A `/refactor` or `/implement-batch` invocation made the test suite fail.
- **Sub-skill cord cascaded up.** `/refactor`, `/review-arch`, `/implement-batch`, or `/implement` pulled its own cord.
- **Phase 2 hard cap hit.** 5 architectural iterations elapsed without convergence.
- **Repeated batch failure.** `/implement-batch` fails on the same finding 3 times.
- **Resume-time HEAD divergence.** Recorded branch SHA does not match current HEAD.

### Skill-specific handoff extensions

- **Title** — `## Andon Cord — /lead-refactor — Phase N`
- **Current state** additionally includes current phase, Phase 2 iteration counter (if applicable), findings-ledger summary, and state-doc pointer.

After pulling the cord: stop. Do not attempt additional phases. Wait for operator input.

## State Management

`LEAD_REFACTOR_STATE.md` lives at the repo root, is gitignored, and survives across invocations. See SKILL.md § "State Management" for the full structure. Key sections:

- Pinned commander's intent
- Cycle log (per phase: Phase 1, Phase 2 iterations 1-5, Phase 3)
- Findings ledger (fixed, deferred, contested, breaking-change-required)
- Andon cord history (full handoff text for each pull)

Update at every phase transition and every Phase 2 iteration.

## Hard Caps

- **Phase 2: 5 architectural iterations** — each is one `/review-arch` + one batch-implementation. If 5 is hit, the architectural shape is not converging; andon cord.
- **3 consecutive failed batches** — if `/implement-batch` fails on the same finding 3 times with different approaches, andon cord.

No file-touch or dependency-change budgets, per the autonomy discipline.

## Available Sub-Skills

The bounded repertoire:

| Skill              | When used                                                                                  |
|--------------------|--------------------------------------------------------------------------------------------|
| `/refactor`        | Phase 1 and Phase 3 — tactical cleanup, loops internally to convergence.                   |
| `/review-arch`     | Phase 2 every iteration — architectural read-out. Ticket proposals auto-approved.          |
| `/implement-batch` | Phase 2 every iteration's Act step — fixes batches of `/review-arch` tickets.              |
| `/implement`       | Phase 2 Act step when a single-ticket batch would make `/implement-batch` ceremony.         |

Skills explicitly **not** in the repertoire (out-of-axis):
- Other `/review-*` skills, `/scope-project`, `/test-mutation`, `/tidy-docs`, `/tidy-git`, `/bug-*` — adjacent concerns.

If you need these alongside refactoring, use `/lead-project`.

## Examples

### Example 1: Pre-release comprehensive refactor

```
User: /lead-refactor

Starting commander's intent elicitation.

Scope — what does this refactor cover?
> Entire production codebase. Exclude vendor/, gen/, and pkg/legacy
  (slated for removal next quarter).

Severity floor — lowest /review-arch severity that gates Phase 2?
> HIGH+. We have time for HIGH but want to ship soon.

Constraints — hard limits beyond breaking changes and main/master?
> Don't modify the public API of pkg/auth.
  Must remain Go 1.22 compatible.

Refactor aggression — how aggressive should /refactor be?
> Moderate. Don't want to delete code with unclear purpose right now.

Read back:
[four-field intent]

Confirm?
> Yes

Creating branch: lead-refactor/2026-05-12
Seeding LEAD_REFACTOR_STATE.md

[Phase 1 — Tactical refactor]
/refactor with moderate aggression, scoped per intent ...
  Loops internally — 4 internal cycles, 23 commits, net -412/+187 lines
  Tests pass ✓

[Phase 2 — Iteration 1]
/review-arch: 6 findings
  - 2 HIGH: pkg/payment domain leakage into pkg/order, utility grab-bag in pkg/util
  - 3 MEDIUM: (deferred)
  - 1 LOW: (deferred)
  3 tickets proposed (#440-#442), auto-approved per commander's intent
Triage: 2 above floor, 4 below (deferred). No contested. No breaking.
Decide: form batch (2 tickets)
Act: /implement-batch ... 2 tickets closed, 18 commits
Verify: tests pass, lint clean

[Phase 2 — Iteration 2]
/review-arch: 2 findings
  - 1 HIGH: pkg/order still has shared mutable state across goroutines
  - 1 LOW: (deferred)
  1 ticket proposed (#443), auto-approved
Triage: 1 above floor, 1 below
Decide: form batch (1 ticket)
Act: /implement ... ticket closed, 4 commits
Verify: tests pass

[Phase 2 — Iteration 3]
/review-arch: 0 findings above floor (2 LOW surfaced)
Triage: 0 above floor, 2 below
Decide: CONVERGED (fix-list empty)

[Phase 3 — Final tactical refactor]
/refactor with moderate aggression ...
  Loops internally — catches dead imports left from Phase 2 moves,
  redundant nil-checks after pkg/order consolidation
  2 internal cycles, 11 commits, net -167/+42 lines
  Tests pass ✓

[Final verification]
- go test ./... → exit 0 ✓
- No constraint violations (pkg/legacy untouched, auth API unchanged) ✓

## Lead-Refactor Complete

### Commander's intent
[Verbatim]

### Outcome
Pipeline completed cleanly. Phase 2 converged in 3 iterations.
3 tickets fixed (3 HIGH-severity architectural findings).
6 deferred findings (4 MEDIUM, 2 LOW) — operator may run another
iteration with floor=MEDIUM+ to address them.

### Phase summary
- Phase 1: 23 commits, net -412/+187 lines
- Phase 2: 3 iterations, 3 tickets fixed, 6 deferred
- Phase 3: 11 commits, net -167/+42 lines

### Tickets created and fixed (Phase 2)
- [#440] Move payment-domain types out of pkg/order
        — fix SHA abc1234 — domain leakage
- [#441] Dissolve pkg/util grab-bag (split into pkg/strutil, pkg/timeutil)
        — fix SHA def5678 — utility consolidation
- [#443] Eliminate shared mutable state in pkg/order
        — fix SHA ghi9012 — concurrency

### Deferred findings (below severity floor)
- [Medium | iter 1] pkg/session module boundary is fuzzy
- [Medium | iter 1] pkg/auth/handlers has overlapping responsibilities
- [Medium | iter 1] (...)
- [Low | iter 1] (...)
- [Low | iter 3] (...)
- [Low | iter 3] (...)

### Constraint adherence
No commits to pkg/legacy. Public API of pkg/auth preserved.
Go 1.22 compatibility maintained.

### Changes summary
- Branch: lead-refactor/2026-05-12
- Commits on branch: 56 (Phase 1: 23 + Phase 2: 22 + Phase 3: 11)
- Net lines: -579 / +229

### Run metadata
- Phase 2 iterations: 3 of 5
- Andon-cord pulls: 0
```

## Tips

**Pick your severity floor honestly.** "All severities" almost never converges — `/review-arch` always finds LOW-severity opportunities. Default to HIGH+; lower the floor for follow-up iterations once the higher severities are clean.

**Run on a feature branch, never main.** The skill enforces this, but worth internalizing. Many commits will be produced.

**Resume is cheap.** Interrupting the skill (Ctrl-C, session end) is safe — the state doc captures enough to resume. Just re-invoke `/lead-refactor` and choose "Resume" when prompted.

**Andon cords are not failures.** Hitting a contested finding or a breaking-change requirement is the skill doing its job — surfacing decisions that need operator judgment.

**Pair with `/tidy-docs` separately if needed.** Phase 2's structural changes commonly invalidate inline docs, code examples, and module references. Run `/tidy-docs` after `/lead-refactor` if doc drift is a concern.

**Pair with `/review-test` separately if test scaffolding is a concern.** Structural changes can break test setup helpers and shared fixtures; `/review-test` catches quality drift.

## Integration with Other Skills

**`/refactor`:** the workhorse for Phases 1 and 3. Loops internally to convergence each time.

**`/review-arch`:** the architectural advisor for Phase 2. Ticket proposals auto-approved per the orchestrator-family contract. Use `/review-arch` directly when you want a one-shot advisory read-out without implementation.

**`/implement-batch` and `/implement`:** the fix arms in Phase 2. Sub-skill escalations cascade up per the autonomy discipline.

**`/lead-project`:** the broader sibling. Use `/lead-project` when refactoring is one of several concerns; use `/lead-refactor` when comprehensive refactoring is the sole objective. `/lead-project` may invoke `/lead-refactor` from its Decide phase.

**`/lead-bug-hunt`:** sibling orchestrator with a different outcome. Same shape philosophy (4-field intent, severity floor, auto-approval of sub-skill ticket proposals, andon protocol), different domain.

## Agent Coordination

**Sequential execution.** One phase at a time. One sub-skill invocation per Phase 2 iteration's Act step. No parallel phases.

**Context discipline.** The skill is a thin coordinator. Implementation work is delegated to sub-skills. Summary-level state lives in the skill's context; `LEAD_REFACTOR_STATE.md` holds durable memory.

**Sub-skill invocation.** Invoke via the Skill tool with autonomous overrides where supported. Interactive prompts from sub-skills are answered using engineering judgment anchored to commander's intent.

## Abort Conditions

**Do NOT abort for:**
- Phase 1 finding nothing to refactor (proceed to Phase 2).
- Phase 2 first iteration finding nothing above floor (Phase 2 converges immediately; proceed to Phase 3).
- Phase 3 finding nothing to refactor (proceed to termination).
- Findings the skill thinks are exaggerated (apply severity floor mechanically).

**Pull the andon cord for:**
- Triggers listed under "The Andon Cord" above.

**Abort the entire workflow for:**
- Operator interrupts.
- Critical system error (repository corrupted, git state unrecoverable).
- Operator declines to confirm commander's intent at startup.
