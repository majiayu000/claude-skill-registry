---
name: lead-bug-hunt
description: Autonomous bug-elimination loop. Iteratively invokes /bug-hunt and /implement-batch until findings converge below an operator-specified severity floor. At termination, runs /review-test scoped to the run's new reproducing tests and fixes quality issues above the floor. Auto-approves /bug-hunt and /review-test ticket proposals; pulls the andon cord on contested findings, repeated implementation failure, hard-cap exhaustion, or breaking-change proposals. Optional /refactor finisher.
model: opus
---

# Lead-Bug-Hunt — Autonomous Bug Elimination

Drives a codebase toward "no bugs above severity floor" without operator involvement between startup and termination. The operator states scope, severity floor, constraints, and finisher preference at startup; the skill then loops `/bug-hunt` → triage → `/implement-batch` until two consecutive hunt passes produce no findings above the floor, or until a hard cap or andon cord halts the run.

This skill is a narrower sibling of `/lead-project`. `/lead-project` takes open-ended commander's intent and decides which skills to invoke from a broad repertoire. `/lead-bug-hunt` has a fixed loop shape (hunt → fix → re-hunt) and a bounded sub-skill repertoire. It exists because "iterate until bugs converge" is a recurring workflow worth canonizing.

## Philosophy

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template. Skill-specific shape (the hunt-cycle structure, convergence criteria, severity-floor triage) is layered on top.

### The loop converges on a floor, not on zero

Bugs below a stated severity floor do not block termination. They are recorded as deferred items in the completion report. The operator chooses the floor at startup; defaults to **High** (fix Critical and High; defer Medium and below).

This is the dominant judgment call this skill exposes. Setting the floor too low produces a loop that never converges (`/bug-hunt` always finds *something* at Low). Setting it too high produces a run that ships with real bugs unaddressed. The floor is elicited explicitly so the operator owns this trade-off.

### Reproducing tests are durable artifacts

`/bug-hunt` commits reproducing tests as it works. Those tests outlive the run — they become permanent regression tests in the suite. Their quality matters more than typical test code because they will catch regressions for years and bias future test authors who read them as examples.

This skill therefore treats test review as part of its core contract, not as adjacent cleanup. At termination (after convergence, after any `/refactor` finisher), the skill invokes `/review-test` scoped to the test files modified during this run, auto-approves any quality-finding ticket proposals at or above the severity floor, and fixes them via `/implement-batch`. Findings below the floor are deferred to the completion report.

### Trust the reproducing test, escalate the disagreement

`/bug-hunt` produces findings backed by reproducing tests. This skill **trusts findings with passing reproducing tests against current HEAD** — they are real bugs by `/bug-hunt`'s evidence contract. The skill does not silently dismiss findings. If the skill genuinely believes a finding is wrong (the reproducing test asserts wrong behavior, the "bug" is intentional), that is an andon trigger ("contested finding"), not a unilateral disregard.

No escape hatches: the skill cannot rationalize bugs away to make the loop converge.

### Auto-approval is delegated to the autonomy discipline

`/bug-hunt` and `/review-test` are advisory; their ticket proposals are auto-approved under `/lead-bug-hunt` per the orchestrator-family contract documented in [`references/autonomy.md`](../../references/autonomy.md) § "Auto-approval of sub-skill ticket proposals". The commander's-intent severity floor (field 2) is applied at the triage step (1b), not at the approval moment. The completion report lists every ticket created.

### Broad authority, narrow gates

The skill may: invoke `/bug-hunt`, `/implement-batch`, `/implement`, `/bug-fix`, `/think-diagnose`, `/refactor`, `/review-test` (at termination, scoped to the run's new tests); create tickets via auto-approved proposals; commit fix work via sub-skills; create and modify the working branch.

The skill may NOT without explicit authorization: push or merge to main/master, force-push, propose breaking changes (see `references/autonomy.md` § "No unilateral breaking changes"), invoke `/review-*` skills other than the scoped `/review-test` at termination (out-of-axis — use `/lead-project` if you want broader review-driven work), install dependencies, run irreversible destructive operations.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                  LEAD-BUG-HUNT WORKFLOW                          │
├──────────────────────────────────────────────────────────────────┤
│  0. Startup                                                      │
│     ├─ 0a. Branch and working-tree check                         │
│     ├─ 0b. Resume existing run or start fresh                    │
│     ├─ 0c. Elicit commander's intent (4 fields)                  │
│     └─ 0d. Seed LEAD_BUG_HUNT_STATE.md                           │
│                                                                  │
│  1. Hunt cycle (repeat until convergence or andon cord)          │
│     ├─ 1a. Hunt — invoke /bug-hunt, gather findings              │
│     ├─ 1b. Triage — apply severity floor, screen for contests    │
│     ├─ 1c. Decide — form batch, escalate, or terminate           │
│     ├─ 1d. Act — invoke /implement-batch (or /implement, etc.)   │
│     ├─ 1e. Verify — tests pass, reproducing tests now pass       │
│     └─ 1f. Convergence check                                     │
│                                                                  │
│  2. Termination                                                  │
│     ├─ 2a. Optional /refactor finisher (if opted in)             │
│     ├─ 2b. /review-test on new reproducing tests                 │
│     │       (auto-approved, fix above-floor findings)            │
│     ├─ 2c. Final verification pass                               │
│     └─ 2d. Completion report                                     │
└──────────────────────────────────────────────────────────────────┘
```

## Workflow Details

### 0. Startup

Follow the shared startup protocol in [`references/lead-startup.md`](../../references/lead-startup.md). Skill-specific values:

- **0a. Branch and working-tree check** — branch-name pattern: `lead-bug-hunt/<date>` (e.g., `lead-bug-hunt/2026-05-12`).
- **0b. Resume existing run or start fresh** — state-doc filename: `LEAD_BUG_HUNT_STATE.md`. "Resume as-is" semantic: re-run a hunt before forming the next batch.
- **0c. Elicit commander's intent** — four fields per the schema in [`references/autonomy.md`](../../references/autonomy.md) § "Commander's-intent schemas per skill / `/lead-bug-hunt`". Push-back examples specific to this skill: "Find all the bugs" is not a scope — ask which modules; "Whatever severity" is not a floor — push for Critical+High at minimum, or ask why broader makes sense.
- **0d. Seed `LEAD_BUG_HUNT_STATE.md`** — include the four pinned intent fields, an empty cycle log, and an empty findings ledger. Gitignore the state doc per the protocol.

### 1. Hunt Cycle

Repeat until convergence (1f), andon cord, or hard cap (10 hunt-cycles).

Each cycle has six phases. Keep phase transitions visible in the state doc.

#### 1a. Hunt

Invoke `/bug-hunt` with auto-answered prompts:

- **Scope** — answer from commander's intent field 1.
- **Areas of concern** — on cycle 1, none specified unless the operator listed them in field 1. On subsequent cycles, include any areas the previous cycle's hunters flagged but ran out of time on.
- **Exclusions** — answer from commander's intent field 1.

When `/bug-hunt` reaches its ticket-proposal step, auto-approve. Record in the cycle log: ticket IDs proposed, scope of the proposal, and the fact that auto-approval was applied per commander's intent.

`/bug-hunt` also commits its reproducing tests. Confirm those commits exist in the cycle log.

#### 1b. Triage

For each finding produced by the hunt:

1. **Confirm reproducing test passes against current HEAD.** If yes, the finding is real per `/bug-hunt`'s contract — proceed to classification. If no (the test does not actually fail on current code), the finding is stale or wrong — log it in `## Contested findings` in the state doc and pull the andon cord.

2. **Classify against severity floor:**
   - **At or above floor** — fix-list. These block convergence.
   - **Below floor** — deferred list. These do not block convergence. Record in `## Deferred findings` with severity and a one-line summary.

3. **Screen for contested findings.** If the skill believes a finding is wrong on substance (the reproducing test asserts wrong behavior, the "bug" is documented intentional behavior, the finding contradicts a constraint in commander's intent), do not silently dismiss it. Record in `## Contested findings` and proceed to andon cord at the end of triage (see § "Andon Cord Protocol").

4. **Screen for breaking-change implications.** If fixing a finding would require a breaking change (per `references/autonomy.md` § "No unilateral breaking changes"), record in `## Breaking-change findings` and proceed to andon cord. Do not auto-fix.

#### 1c. Decide

Three possible outcomes:

- **Form a batch and proceed to 1d** — fix-list is non-empty, no contested or breaking-change findings.
- **Escalate and pull the andon cord** — contested findings or breaking-change findings exist (see § "Andon Cord Protocol").
- **Skip to convergence check (1f)** — fix-list is empty (no findings above floor this cycle).

Batch formation: tickets created by `/bug-hunt` this cycle are the batch. Do not co-mingle with prior cycles' tickets — each cycle handles its own batch, so the verification loop is tight.

Record the chosen outcome and rationale in the cycle log.

#### 1d. Act

Execute the batch. Sub-skill choice:

- **`/implement-batch`** — default for any batch with 2+ tickets, or single tickets with bounded scope.
- **`/implement`** — single ticket only, used when `/implement-batch` would be ceremony.
- **`/bug-fix`** — finding has a reproducing test but root cause is unclear and needs diagnosis-first work. Used when `/implement` from the ticket alone would be cargo-culting toward a fix.
- **`/think-diagnose`** — pre-fix, when bug cause is genuinely unclear and `/bug-fix`'s diagnosis phase would benefit from structured reasoning.

When invoking a sub-skill that supports autonomous mode, use it. When a sub-skill requires interactive input, answer using engineering judgment anchored to commander's intent.

Sub-skill escalations cascade up per `references/autonomy.md` § "Cascade rule." `/implement-batch`'s andon-cord pulls become this skill's responsibility to either resolve (next cycle's diagnosis) or escalate further (pull this skill's own andon cord).

#### 1e. Verify

After the batch completes:

- Full test suite passes. If not, the fix introduced a regression — record as andon trigger (see § "Andon Cord Protocol", "regression introduced").
- Each reproducing test from the batch's findings now passes — these are the acceptance criteria.
- Build/typecheck/lint clean.
- No constraint violations in the new commits.

Update the findings ledger: tickets fixed this cycle move from "fix-list" to "resolved" with commit SHAs.

#### 1f. Convergence check

Convergence: **two consecutive cycles produce no findings above the severity floor.**

- **Cycle's fix-list was empty (no findings above floor):** increment the empty-pass counter.
- **Cycle's fix-list was non-empty:** reset the empty-pass counter to zero.

If empty-pass counter reaches 2 → proceed to termination (step 2).
Otherwise → return to 1a for the next cycle.

**Caveat on convergence.** `/bug-hunt` is non-deterministic — different hunters may explore different paths each pass. Two empty passes is a strong signal (the assessor's hotspot list is reasonably stable across passes), but not a proof. The completion report makes this caveat explicit to the operator.

### 2. Termination

#### 2a. Optional `/refactor` finisher

If commander's intent field 4 specified a finisher aggression:

- Invoke `/refactor` with the specified aggression ceiling, scoped to the bug-hunt scope (field 1).
- Verify tests still pass after the refactor.
- Record refactor outcome in the cycle log.

If field 4 was "no finisher": skip this step.

The finisher is opt-in because it is not the core action of this skill. Bug-elimination is the contract; cleanup is adjacent and may be a separate concern for the operator.

#### 2b. `/review-test` on new reproducing tests

Always runs (not opt-in). The reproducing tests committed by `/bug-hunt` during the run are durable regression artifacts; their quality matters.

1. **Determine the test scope** — collect the set of test files modified on the working branch since the base SHA. Use `git diff --name-only <base SHA>..HEAD` filtered to test files. If the set is empty (no new tests this run, which would be unusual), skip this step and log it in the cycle log.

2. **Invoke `/review-test`** with scope set to that file list. Auto-answer `/review-test`'s scope prompt with "specific files" + the collected list. The skill's other prompts answered using engineering judgment anchored to commander's intent.

3. **Triage the proposed tickets.** Use the same severity floor from commander's intent field 2.
   - At or above floor → fix-list (block termination until resolved).
   - Below floor → deferred list, recorded in state doc and completion report.
   - **Contested test-quality finding** (the skill believes the proposed change is wrong on substance, e.g., the finding suggests deleting a test that is genuinely load-bearing) → andon cord, do not silently dismiss.
   - **Breaking-test-change required** (a quality fix would alter test signatures/imports in ways that affect external consumers — rare for test files, but possible for shared test helpers exported by the project) → andon cord per `references/autonomy.md` § "No unilateral breaking changes."

4. **Fix the fix-list** via `/implement-batch` (or `/implement` for single tickets). Sub-skill escalations cascade up per `references/autonomy.md` § "Cascade rule."

5. **Verify after fixing.** Full test suite still passes. The reproducing tests that were the original acceptance criteria still pass after any rewrites. If a fix invalidates a reproducing test (e.g., a SIMPLIFY suggestion accidentally weakens the assertion), pull the andon cord ("regression in reproducing test").

Record outcome in the state doc under `## Test review` section.

**Why this is always-on:** the reproducing tests are this skill's unique durable output. Bug fixes are valuable but transient (the bug is gone either way); the tests stay forever. Treating their quality as adjacent rather than core would be inconsistent with the skill's framing.

**Why no re-hunt after this step:** if the test-review's fixes have changed behavior enough to introduce new bugs above the floor, the test suite catches it during the verify step. Otherwise we'd be susceptible to an infinite loop (re-hunt → find → fix → re-review → re-hunt …).

#### 2c. Final verification pass

Before declaring done:

- Full test suite passes.
- All reproducing tests committed during the run pass.
- No constraint violations in commits on this branch.
- Build/typecheck/lint clean.

If any check fails, treat as a blocker — return to the loop (cycle counter does not increment).

#### 2d. Completion report

```
## Lead-Bug-Hunt Complete

### Commander's intent
[All four fields, verbatim]

### Outcome
[One paragraph: did the loop converge? At what cycle? Did the finisher run?
 Any caveats the operator should know about — non-determinism of /bug-hunt,
 deferred findings below floor, etc.]

### Convergence evidence
- Cycles run: N of 10
- Final two passes: <findings count per pass, all below floor>
- Reproducing tests in tree: N
- Total tickets fixed: N

### Top things to scrutinize
[Three to five items where the skill's judgment is most likely to need
 review. Each item: one sentence + artifact (SHA, ticket ID, file:line).
 Examples: triage calls on borderline findings, batches with multiple
 attempts, the finisher's net diff, areas the hunters flagged as
 uncertain.]

### Tickets created and fixed
- [#N] <title> — fix SHA <short> — reproducing test <file:line>
- [#N+1] <title> — fix SHA <short> — reproducing test <file:line>
- ...

### Test review outcome
- Tests reviewed: <list of test files reviewed in step 2b>
- Quality tickets created: N (list IDs)
- Quality tickets fixed: N
- Deferred quality findings (below floor): N — see Deferred section
- Contested or breaking quality findings: N — see Andon section (if any)

### Deferred findings (below severity floor)
[Findings not gated by the floor. Operator may run another iteration
 with a lower floor to address them.]
- [Low | cycle 3 | /bug-hunt] <description> — see finding artifact
- [Low | cycle 5 | /bug-hunt] <description>
- [Low | termination 2b | /review-test] <description> — test quality
- ...

### Contested or breaking-change findings (if any escalated)
[Findings that were escalated rather than auto-fixed.]
- [contested | cycle 4] <description> — andon-cord SHA <short> in state doc
- ...

### Constraint adherence
[Confirm no violations. If any close calls, name them with commit SHAs.]

### Changes summary
- Branch: <branch name> (SHA <short>)
- Base: <base branch> (SHA <short>)
- Commits on branch: N
- Net lines: +X/-Y
- Finisher: <none | conservative | moderate | aggressive>

### Run metadata
- Hunt cycles: N of 10
- Empty passes at termination: 2 consecutive
- Andon-cord pulls during run: N (each with handoff in state doc)
- Duration (wall-clock, approximate)
```

The operator decides whether to merge, run another iteration (e.g., with a lower severity floor), or pause.

## Commander's Intent — Field Reference

### Scope

Same shape as `/bug-hunt`'s scope question. Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session` — recent rewrite, want focused coverage."
- "All production code, with extra attention to `pkg/payments` and `pkg/billing` (high-stakes areas)."

### Severity floor

The lowest severity that gates termination. Options:

| Floor              | Effect                                                                                                                    |
|--------------------|---------------------------------------------------------------------------------------------------------------------------|
| Critical only      | Loops only on Critical findings. Fastest convergence; ships with High+Medium+Low deferred. Use for emergency sweeps.      |
| Critical + High    | Default. Loops on real-impact findings; defers polish and edge-case opportunities to follow-up.                           |
| Critical+High+Med  | Loops longer; addresses moderate-severity issues. May not converge in 10 cycles for large codebases.                      |
| All severities     | Not recommended. `/bug-hunt` tends to find Low-severity opportunities indefinitely; convergence is unlikely.              |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes). Examples:
- "Do not modify the public API of package `auth`."
- "Do not touch generated code under `gen/`."
- "Must remain Go 1.22 compatible."

### Refactor finisher

Aggression ceiling for the optional finisher. Options (matching `/refactor`'s vocabulary):

| Setting       | Effect                                                                                                          |
|---------------|-----------------------------------------------------------------------------------------------------------------|
| no finisher   | Default. Bug fixes ship as-is. Operator may run `/refactor` separately.                                         |
| conservative  | Cleanup of obviously-redundant code introduced by fixes. Low diff.                                              |
| moderate      | Standard `/refactor` aggression. Moderate diff.                                                                 |
| aggressive    | Maximum aggression — significant restructuring permitted. High diff. The "MAXIMUM aggression" the ad-hoc want. |

## Severity & Triage

Triage is mechanical, not judgment-based. The severity floor is the only knob.

- **Floor and above** → fix-list, blocks convergence until resolved.
- **Below floor** → deferred list, recorded in state doc and completion report, does not block convergence.
- **Contested on substance** → andon cord, not silent dismissal.
- **Breaking change required** → andon cord, not auto-fix.

The skill does NOT:
- Re-rank `/bug-hunt`'s severity classifications. The hunter's judgment stands.
- Bargain findings down to make convergence easier.
- Dismiss findings because "the test seems wrong" — that's the contested-finding path.

## Andon Cord Protocol

Follow the shared handoff template and per-skill extension protocol in [`references/autonomy.md`](../../references/autonomy.md) § "Shared handoff template" and § "Per-skill handoff extensions". Skill-specific values:

- **Title format** — `## Andon Cord — /lead-bug-hunt — Cycle N`
- **Current-state additions:**
  - `Empty-pass counter: <N>`
  - `Findings ledger: <K fixed, M deferred, L contested>`
  - `State doc pointer: see LEAD_BUG_HUNT_STATE.md cycles N-2 through N`

### Andon cord triggers

Pull the cord when:

- **Contested finding.** The skill believes a `/bug-hunt` finding is wrong on substance — the reproducing test asserts wrong behavior, the "bug" is documented intentional behavior, or the finding contradicts a constraint in commander's intent. Surface the finding, the reproducing test, and the disagreement.
- **Breaking-change required.** Fixing a finding requires a breaking change (per `references/autonomy.md` § "No unilateral breaking changes"). List the finding, the breaking-change option, and the non-breaking alternative (if any).
- **Regression introduced.** A batch fix made the test suite fail in ways unrelated to the targeted bug. Record the failing tests, the cycle, and the batch SHAs.
- **Sub-skill cord cascaded up.** `/implement-batch`, `/implement`, or `/bug-fix` pulled its own cord for a reason this skill cannot resolve.
- **Reproducing test stale at triage.** A `/bug-hunt` finding's reproducing test does not actually fail on current HEAD. This indicates either the hunter was wrong or the test exercises the wrong path. Worth operator review before continuing.
- **Contested test-quality finding.** During termination step 2b, `/review-test` proposed a change the skill believes is wrong on substance (e.g., delete a test that is genuinely load-bearing, rewrite an assertion in a way that weakens coverage).
- **Breaking test change required.** A `/review-test` quality fix would alter test signatures or imports in ways that affect external consumers — rare for test files but possible for shared test helpers.
- **Regression in reproducing test.** A test-quality fix during step 2b invalidated a reproducing test that was the acceptance criterion for an earlier-cycle bug fix. The fix may need to be revisited or the quality change reverted.
- **Hunt produces no actionable findings but has high uncertainty.** `/bug-hunt`'s assessment surfaced high-risk hotspots but hunters could not produce confirmed findings. The skill should not declare convergence in this case; operator should decide whether to deepen the hunt or accept the uncertainty.
- **Hard cap hit.** 10 hunt-cycles elapsed without convergence. Something is likely structurally wrong (severity floor set too low, codebase has a class of recurring bug the hunters keep finding, etc.).
- **Resume-time HEAD divergence.** On resume, recorded branch SHA does not match current HEAD.

## State Management

### `LEAD_BUG_HUNT_STATE.md`

Maintained at the repo root. Gitignored. Survives across invocations.

**Structure:**

```markdown
# Lead-Bug-Hunt State

Started: <timestamp>
Branch: <branch-name>
Branch SHA at startup: <short SHA>
Base branch: <main-branch>
Base SHA at startup: <short SHA>
Last cycle HEAD: <short SHA>
Cycle: N
Empty-pass counter: <0 | 1 | 2>
Status: <active | paused-on-andon | complete>

## Commander's Intent

### Scope
<verbatim>

### Severity floor
<Critical only | Critical+High | Critical+High+Medium | All>

### Constraints
- <constraint 1>

### Refactor finisher
<no finisher | conservative | moderate | aggressive>

## Cycle log

### Cycle N — <timestamp> — HEAD <short SHA>
- Hunt: <findings count by severity>, tickets proposed <#N..#M>
- Triage: <count above floor | below floor | contested | breaking>
- Decide: <form batch | escalate | skip to convergence check>
- Act: <skill invoked, outcome, fix SHAs>
- Verify: <tests pass / fail, repro tests passing>
- Convergence: <empty-pass counter after this cycle>

## Findings ledger

### Fixed
- [cycle 2 | ticket #14] <description> — fix SHA <short> — repro test passing
- ...

### Deferred (below floor)
- [Low | cycle 3] <description>
- [Medium | cycle 4] <description> — (if floor is Critical+High)
- ...

### Contested
- [cycle 4] <description> — andon cord pulled, see § Andon Cord history

### Breaking-change-required
- [cycle 5] <description> — andon cord pulled, see § Andon Cord history

## Test review (termination 2b)

Scope: <test files reviewed, from `git diff --name-only <base SHA>..HEAD`>
Findings above floor: N — tickets <#N..#M>, fixed at SHAs <short>..<short>
Findings below floor: N — see § Findings ledger / Deferred
Contested findings: N — see § Andon cord history (if any)
Outcome: <clean | fixes applied | andon cord pulled>

## Andon cord history

### Cycle N pull
<full handoff text, pasted>

## Open questions

- <question>
```

**Update at every phase transition.** The state doc is the durable orientation — losing it means losing the agent's memory.

### `.gitignore`

Ensure `LEAD_BUG_HUNT_STATE.md` is ignored. Commit the `.gitignore` change on the working branch at startup if needed.

## Hard Caps

- **10 hunt-cycles** — each cycle is one full `/bug-hunt` + one batch-implementation. Heavier than `/lead-project`'s OODA cycles, so the cap is lower. Hitting it pulls the andon cord.
- **3 consecutive failed batches** — if `/implement-batch` (or `/implement` / `/bug-fix`) fails on the same finding 3 times across different attempts, pull the andon cord.
- **No file-touch or dependency-change budgets** — explicitly excluded per `references/autonomy.md` § "Risk budgets."

## Integration with Other Skills

**Relationship to `/bug-hunt`:**

`/lead-bug-hunt` invokes `/bug-hunt` as its workhorse. `/bug-hunt` remains advisory in its native contract — it produces ticket proposals and commits reproducing tests, but does not implement fixes. `/lead-bug-hunt` auto-approves the ticket proposals (per the autonomy contract) and chains `/implement-batch` to do the fix work. Run `/bug-hunt` directly when you want a single advisory pass with operator-approved tickets; run `/lead-bug-hunt` when you want the full hunt → fix → re-hunt loop unattended.

**Relationship to `/lead-project`:**

`/lead-project` is the open-ended orchestrator — it takes broad commander's intent and decides which skills to invoke. `/lead-bug-hunt` is a fixed-shape loop for one specific outcome. Use `/lead-project` when bug-hunting is one of several concerns; use `/lead-bug-hunt` when bug elimination is the sole objective. `/lead-project` may invoke `/lead-bug-hunt` as a sub-skill when its Decide phase identifies a bug-sweep as the next move.

**Relationship to `/refactor` and `/lead-refactor`:**

The optional finisher invokes `/refactor` (not `/lead-refactor`) — bug-fix cleanup does not benefit from `/lead-refactor`'s architectural-review loop. If you want comprehensive cleanup after bug elimination, run `/lead-refactor` separately after `/lead-bug-hunt` completes.

**Relationship to `/review-test`:**

Invoked once at termination, scoped to the test files modified during this run. `/review-test`'s ticket proposals are auto-approved (same contract shift as `/bug-hunt`). Findings above the severity floor are fixed via `/implement-batch`; below-floor findings are deferred. Contested findings or breaking test changes pull the andon cord. `/review-test` remains a directly-invokable advisory skill — use it outside `/lead-bug-hunt` for broader test-suite reviews.

**Out-of-axis skills:**

Other `/review-*` skills, `/scope-project`, `/test-mutation`, `/tidy-docs`, `/tidy-git` are not in this skill's repertoire. If your goal is "review → refactor → test → ship," use `/lead-project` instead. `/lead-bug-hunt` is deliberately narrower.
