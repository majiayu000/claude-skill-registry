# /lead-bug-hunt — Autonomous Bug Elimination

## Overview

The `/lead-bug-hunt` skill drives a codebase toward "no bugs above a stated severity floor" without operator involvement between startup and termination. The operator states **scope, severity floor, constraints, and finisher preference** at startup; the skill then loops `/bug-hunt` → triage → `/implement-batch` until two consecutive hunt passes produce no findings above the floor, or until a hard cap or andon cord halts the run.

This skill is a narrower sibling of `/lead-project`. `/lead-project` takes open-ended commander's intent and decides which skills to invoke from a broad repertoire. `/lead-bug-hunt` has a fixed loop shape (hunt → fix → re-hunt) and a bounded sub-skill repertoire. It exists because "iterate until bugs converge" is a recurring workflow worth canonizing.

This skill is a member of the **orchestrator family** and implements the autonomy discipline documented in [`references/autonomy.md`](../../../references/autonomy.md). The shared discipline governs the five levers (altitude rule, pre-loaded options, pre-rebutted recommendation, commander's intent, risk budgets), the cascade rule, the no-unilateral-breaking-changes guardrail, and the shared handoff template.

**Key benefits:**
- Unattended bug elimination — kick it off and walk away
- Reproducing tests as durable acceptance criteria (committed by `/bug-hunt`)
- Mechanical triage against a stated severity floor — no rationalization
- Convergence on a fixed-point (no findings above floor), not on a ticket list
- `LEAD_BUG_HUNT_STATE.md` as persistent state across sessions
- Optional `/refactor` finisher to clean up defensive code introduced by fixes
- Always-on `/review-test` at termination — reproducing tests are durable regression artifacts and get the same quality care as fixes

## When to Use

**Use `/lead-bug-hunt` for:**
- Pre-release bug sweeps where the goal is "ship with no known Critical/High bugs"
- Periodic hygiene runs on long-lived codebases
- Post-incident or post-bug-bash work where you want comprehensive coverage
- Any time you'd otherwise run `/bug-hunt` → fix tickets → `/bug-hunt` → fix tickets by hand

**Don't use `/lead-bug-hunt` for:**
- A single bug with a known cause (use `/bug-fix`)
- A one-shot proactive scan (use `/bug-hunt` directly)
- Mixed work that includes feature implementation, review, or refactor (use `/lead-project`)
- Exploratory diagnosis where the bug isn't yet characterized (use `/think-diagnose` or `/bug-fix`)

**Rule of thumb:** if you find yourself repeatedly running `/bug-hunt`, accepting the proposed tickets, running `/implement-batch`, and running `/bug-hunt` again, `/lead-bug-hunt` is the right abstraction.

## Relationship to `/bug-hunt`

| Dimension                | `/bug-hunt`                                              | `/lead-bug-hunt`                                                |
|--------------------------|----------------------------------------------------------|-----------------------------------------------------------------|
| Mode                     | Advisory (one pass)                                      | Autonomous loop (many passes until convergence)                 |
| Output                   | Findings + reproducing tests + ticket proposals          | Fixed bugs + reproducing tests in tree + completion report      |
| Ticket approval          | Operator-approved at end of pass                         | Auto-approved per commander's intent                            |
| Fixes                    | Not in scope                                             | Performed by `/implement-batch` (or `/implement`, `/bug-fix`)   |
| Termination              | End of single pass                                       | Convergence (2 empty passes above floor) or andon cord          |
| Duration                 | Roughly predictable                                      | Open-ended (capped at 10 hunt-cycles)                           |

`/lead-bug-hunt` invokes `/bug-hunt` as its workhorse. `/bug-hunt` remains advisory in its native contract — use it directly when you want a single pass with operator approval at the end.

## Relationship to `/lead-project`

| Dimension                | `/lead-project`                                       | `/lead-bug-hunt`                                                 |
|--------------------------|-------------------------------------------------------|------------------------------------------------------------------|
| Input                    | Five-field commander's intent (broad)                 | Four-field commander's intent (narrow, bug-specific)             |
| Loop shape               | OODA, open-ended action space                         | Fixed: hunt → triage → batch-fix → verify → repeat               |
| Sub-skill repertoire     | All implement/refactor/review/think/bug skills        | `/bug-hunt`, `/implement-batch`, `/implement`, `/bug-fix`, `/think-diagnose`, `/refactor` (optional finisher), `/review-test` (termination, scoped to new tests) |
| Termination              | Mechanical end-state conditions + quiescence          | 2 consecutive empty passes above severity floor                  |
| Hard cap                 | 50 cycles                                             | 10 hunt-cycles                                                   |
| Use when                 | Bug-hunting is one of several concerns                | Bug elimination is the sole objective                            |

`/lead-project` may invoke `/lead-bug-hunt` as a sub-skill when its Decide phase identifies a bug-sweep as the next move.

## Workflow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│ /lead-bug-hunt Workflow                                         │
└─────────────────────────────────────────────────────────────────┘

 ┌──────────────────────────────────────────────┐
 │  0. STARTUP                                  │
 │  ────────────────────────────────────────    │
 │  0a. Branch and working-tree check           │
 │  0b. Resume existing run or start fresh      │
 │  0c. Elicit commander's intent (4 fields)    │
 │  0d. Seed LEAD_BUG_HUNT_STATE.md             │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  1. HUNT CYCLE (repeat until convergence)    │
 │  ────────────────────────────────────────    │
 │  1a. Hunt — invoke /bug-hunt                 │
 │      - auto-answers from commander's intent  │
 │      - auto-approves ticket proposals        │
 │  1b. Triage                                  │
 │      - confirm reproducing tests pass        │
 │      - apply severity floor                  │
 │      - screen for contested / breaking       │
 │  1c. Decide                                  │
 │      - form batch | escalate | skip          │
 │  1d. Act                                     │
 │      - /implement-batch (typical)            │
 │      - /implement | /bug-fix | /think-diag.  │
 │  1e. Verify                                  │
 │      - tests pass, repro tests now pass      │
 │  1f. Convergence check                       │
 │      - empty-pass counter: 0 → 1 → 2 → done  │
 └──────────────────────────────────────────────┘
                      │
                      ▼
 ┌──────────────────────────────────────────────┐
 │  2. TERMINATION                              │
 │  ────────────────────────────────────────    │
 │  2a. Optional /refactor finisher             │
 │  2b. /review-test on new reproducing tests   │
 │      - auto-approved, scoped to run's tests  │
 │      - fix above-floor findings              │
 │  2c. Final verification pass                 │
 │  2d. Completion report                       │
 └──────────────────────────────────────────────┘
```

## Commander's Intent

Elicited interactively at startup, frozen for the duration of the run. Four fields:

### Scope

What the hunt covers. Same shape as `/bug-hunt`'s scope question.

Examples:
- "Entire codebase, excluding `vendor/` and `gen/`."
- "Just `pkg/auth` and `pkg/session`."
- "All production code, with extra attention to `pkg/payments` (high-stakes)."

### Severity floor

The lowest severity that gates termination. The dominant judgment call this skill exposes.

| Floor              | Effect                                                                                            |
|--------------------|---------------------------------------------------------------------------------------------------|
| Critical only      | Fastest convergence. Ships with High/Medium/Low deferred. Emergency-sweep mode.                  |
| Critical + High    | **Default.** Loops on real-impact findings; defers polish and edge-case opportunities.            |
| Critical+High+Med  | Loops longer; addresses moderate-severity issues. May not converge in 10 cycles on large repos.   |
| All severities     | Not recommended. `/bug-hunt` finds Low-severity opportunities indefinitely; unlikely to converge. |

### Constraints

Hard limits beyond the always-on guardrails (no breaking changes, no main/master writes).

Examples:
- "Do not modify the public API of package `auth`."
- "Do not touch generated code under `gen/`."
- "Must remain Go 1.22 compatible."

### Refactor finisher

Aggression ceiling for the optional post-convergence `/refactor` pass.

| Setting       | Effect                                                                                          |
|---------------|-------------------------------------------------------------------------------------------------|
| no finisher   | **Default.** Bug fixes ship as-is. Operator may run `/refactor` separately.                     |
| conservative  | Cleanup of obviously-redundant code introduced by fixes. Low diff.                              |
| moderate      | Standard `/refactor` aggression. Moderate diff.                                                 |
| aggressive    | Maximum aggression. Significant restructuring permitted. High diff.                             |

## The Hunt Cycle

Each cycle has six phases. The cycle is OODA-shaped but with bug-specific actions baked into each phase.

### 1a. Hunt (Observe)

Invoke `/bug-hunt` with auto-answered prompts (scope and exclusions from commander's intent). Auto-approve `/bug-hunt`'s ticket proposals at the end of the pass. Record proposed ticket IDs and the auto-approval fact in the cycle log.

`/bug-hunt` commits reproducing tests automatically — confirm those commits exist.

### 1b. Triage (Orient)

For each finding:

1. **Confirm reproducing test passes against current HEAD.** If yes, the finding is real per `/bug-hunt`'s contract. If no, pull the andon cord (stale or wrong reproducing test).
2. **Classify against severity floor:**
   - At or above floor → fix-list (blocks convergence)
   - Below floor → deferred list (does not block; recorded in state doc)
3. **Screen for contested findings.** If the skill believes a finding is wrong on substance, record and pull the andon cord. **Do not silently dismiss.**
4. **Screen for breaking-change implications.** If a fix requires a breaking change, pull the andon cord per `references/autonomy.md` § "No unilateral breaking changes."

### 1c. Decide

- Fix-list non-empty, no contested/breaking findings → form a batch (this cycle's tickets), proceed to 1d.
- Contested or breaking findings exist → pull the andon cord.
- Fix-list empty (no findings above floor this cycle) → skip to convergence check (1f).

Batches are per-cycle. Don't co-mingle this cycle's tickets with prior cycles' — verification stays tight.

### 1d. Act

Execute the batch. Sub-skill choice:

- **`/implement-batch`** — default for any batch with 2+ tickets.
- **`/implement`** — single ticket only, used when `/implement-batch` is ceremony.
- **`/bug-fix`** — root cause unclear; diagnosis-first work needed before fix.
- **`/think-diagnose`** — pre-fix, when bug cause is genuinely unclear.

Sub-skill escalations cascade up per `references/autonomy.md` § "Cascade rule."

### 1e. Verify

- Full test suite passes.
- Each batch's reproducing tests now pass (acceptance criteria met).
- Build/typecheck/lint clean.
- No constraint violations.

If any check fails, treat as a regression → andon cord ("regression introduced").

### 1f. Convergence check

- **Cycle's fix-list was empty:** empty-pass counter += 1.
- **Cycle's fix-list was non-empty:** empty-pass counter = 0.

When the empty-pass counter reaches **2** → proceed to termination.
Otherwise → return to 1a.

**Convergence caveat.** `/bug-hunt` is non-deterministic — different hunters may explore different paths each pass. Two consecutive empty passes is a strong signal (the assessor's hotspot list is reasonably stable across passes), but not a proof. The completion report makes this caveat explicit to the operator.

## Termination

### Optional `/refactor` finisher

If commander's intent specified a finisher aggression: invoke `/refactor` with the specified aggression ceiling, scoped to the bug-hunt scope. Verify tests still pass after. Record outcome.

If "no finisher": skip.

### `/review-test` on new reproducing tests

Always runs (not opt-in). The reproducing tests committed by `/bug-hunt` become permanent regression tests — their quality matters more than typical test code.

1. Collect test files modified on this branch since base SHA (`git diff --name-only`).
2. Invoke `/review-test` with scope = those files. Auto-answer the skill's prompts using engineering judgment anchored to commander's intent.
3. Triage proposed quality tickets against the same severity floor used for bug findings:
   - At/above floor → fix-list (blocks termination).
   - Below floor → deferred to completion report.
   - Contested findings (skill believes the proposed change is wrong on substance, e.g., would delete a load-bearing test) → andon cord.
   - Breaking test changes (alters test helper signatures depended on externally — rare) → andon cord.
4. Fix the fix-list via `/implement-batch` (or `/implement`).
5. Verify the test suite still passes and that no reproducing test from earlier cycles was invalidated by a quality fix.

If the test-review finds nothing above the floor, the step is a near-no-op and the run proceeds to final verification.

**Why always-on (not opt-in like the refactor finisher):** the reproducing tests are this skill's unique durable output. Bug fixes are valuable but transient; the tests stay forever and bias future test authors who read them as examples. Treating their quality as adjacent rather than core would be inconsistent.

**Why no re-hunt after this step:** if test-review's fixes have changed behavior enough to introduce new bugs above the floor, the test suite catches it during verify. Otherwise we'd be susceptible to an infinite loop (re-hunt → find → fix → re-review → re-hunt …).

### Final verification pass

- Full test suite passes.
- All reproducing tests committed during the run pass.
- No constraint violations in commits on this branch.
- Build/typecheck/lint clean.

Any failure → blocker, return to the loop.

### Completion report

The report is ordered by review priority — sections most likely to need operator scrutiny come first. See SKILL.md § 2c for the full template. Key sections:

- Convergence evidence (cycles run, final-pass findings counts, reproducing tests in tree, tickets fixed)
- Top things to scrutinize (3-5 items with artifacts)
- Tickets created and fixed (ticket IDs, fix SHAs, reproducing-test file:line)
- Deferred findings below floor
- Contested or breaking-change findings (if any escalated)
- Constraint adherence
- Changes summary and run metadata

## The Andon Cord

The only planned escalation path. See `references/autonomy.md` § "Shared handoff template" for the canonical structure.

### Triggers

- **Contested finding.** The skill believes a `/bug-hunt` finding is wrong on substance.
- **Breaking-change required.** Fixing a finding requires a breaking change.
- **Regression introduced.** A batch fix made the test suite fail in unrelated ways.
- **Sub-skill cord cascaded up.** `/implement-batch`, `/implement`, `/bug-fix` pulled their own cord.
- **Reproducing test stale at triage.** A `/bug-hunt` finding's reproducing test does not actually fail on current HEAD.
- **Hunt produces no actionable findings but has high uncertainty.** Assessment surfaced hotspots, hunters could not confirm — operator should decide whether to deepen.
- **Hard cap hit.** 10 hunt-cycles elapsed without convergence.
- **Resume-time HEAD divergence.** Recorded branch SHA does not match current HEAD.

### Skill-specific handoff extensions

- **Title** — `## Andon Cord — /lead-bug-hunt — Cycle N`
- **Current state** additionally includes empty-pass counter, findings-ledger summary, and state-doc pointer.

After pulling the cord: stop. Do not attempt additional cycles. Wait for operator input.

## State Management

`LEAD_BUG_HUNT_STATE.md` lives at the repo root, is gitignored, and survives across invocations. See SKILL.md § "State Management" for the full structure. Key sections:

- Pinned commander's intent
- Cycle log (per-cycle: hunt, triage, decide, act, verify, convergence)
- Findings ledger (fixed, deferred, contested, breaking-change-required)
- Andon cord history (full handoff text for each pull)

The state doc is the durable orientation. Update at every phase transition. Losing it means losing the agent's memory.

## Hard Caps

- **10 hunt-cycles** — heavier than `/lead-project`'s OODA cycles, so the cap is lower. Hitting it pulls the andon cord.
- **3 consecutive failed batches** — if `/implement-batch` fails on the same finding 3 times with different approaches, pull the cord.

No file-touch or dependency-change budgets — explicitly excluded per the autonomy discipline.

## Available Sub-Skills

The bounded repertoire:

| Skill              | When used                                                                                          |
|--------------------|----------------------------------------------------------------------------------------------------|
| `/bug-hunt`        | Every cycle's 1a — the workhorse. Ticket proposals auto-approved.                                 |
| `/implement-batch` | Default action in 1d for any batch with 2+ tickets.                                                |
| `/implement`       | 1d for single-ticket batches when `/implement-batch` would be ceremony.                            |
| `/bug-fix`         | 1d when a finding's root cause is unclear and `/implement` from the ticket alone is cargo-culting. |
| `/think-diagnose`  | Pre-fix in 1d when bug cause needs structured reasoning before `/bug-fix`.                         |
| `/refactor`        | Termination 2a, if finisher was opted in.                                                          |
| `/review-test`     | Termination 2b. Always runs, scoped to test files modified on this branch. Ticket proposals auto-approved; above-floor fixes routed through `/implement-batch`. |

Skills explicitly **not** in the repertoire (out-of-axis):
- Other `/review-*` skills (`/review-arch`, `/review-security`, etc.) — broader review work is `/lead-project` territory.
- `/scope-project`, `/test-mutation`, `/tidy-docs`, `/tidy-git` — adjacent concerns.

If you need these alongside bug elimination, use `/lead-project`.

## Examples

### Example 1: Pre-release bug sweep

```
User: /lead-bug-hunt

Starting commander's intent elicitation.

Scope — what does this hunt cover?
> Entire production codebase. Exclude vendor/, gen/, and the
  integration test fixtures under test/fixtures/.

Severity floor — lowest severity that gates termination?
> Critical+High. We have a release in two days.

Constraints — hard limits beyond breaking changes and main/master?
> Don't touch pkg/legacy (slated for removal next quarter).
  Must remain Go 1.22 compatible.

Refactor finisher — clean up after fixes?
> Moderate. The bug fixes tend to leave defensive code I'd rather
  not ship.

Read back:
[four-field intent]

Confirm?
> Yes

Creating branch: lead-bug-hunt/2026-05-12
Seeding LEAD_BUG_HUNT_STATE.md

[Cycle 1]
Hunt: /bug-hunt scoped per intent ... 7 findings (2 Critical, 3 High, 2 Low)
      4 reproducing tests committed, 5 tickets proposed (#412-#416)
      auto-approved per commander's intent
Triage: 5 above floor, 2 below (deferred). No contested. No breaking-change.
Decide: form batch (5 tickets)
Act: /implement-batch ... 5 tickets closed, 14 commits
Verify: tests pass, all 5 reproducing tests now pass, lint clean
Convergence: empty-pass counter 0 → 0 (non-empty cycle)

[Cycle 2]
Hunt: /bug-hunt ... 3 findings (1 High, 2 Low)
      1 ticket proposed (#417), auto-approved
Triage: 1 above floor, 2 below. No contested. No breaking.
Decide: form batch (1 ticket)
Act: /implement ... ticket closed, 3 commits
Verify: tests pass, reproducing test passes
Convergence: 0 → 0

[Cycle 3]
Hunt: /bug-hunt ... 1 finding (Low)
Triage: 0 above floor, 1 below (deferred)
Decide: skip to convergence check
Convergence: 0 → 1

[Cycle 4]
Hunt: /bug-hunt ... 0 findings above floor (2 Low surfaced)
Triage: 0 above floor, 2 below (deferred)
Decide: skip to convergence check
Convergence: 1 → 2 → CONVERGED

[Termination — /refactor finisher]
/refactor with moderate aggression, scoped to production code ...
  18 commits, 412 lines net change, tests pass

[Termination — /review-test on new reproducing tests]
Test files modified this run (via git diff): 6 files
Invoking /review-test scoped to those files ...
  Phase 5 (test quality) findings: 3
    - 1 High: reproducing test for #413 asserts on internal state
      instead of observable behavior (brittle)
    - 1 Low: docstring missing on test for #412
    - 1 Low: redundant setup helper in test for #415
  1 ticket proposed above floor (#418), auto-approved
  2 findings below floor — deferred
Triage: 1 above floor, 0 contested, 0 breaking
Fixing via /implement: ticket #418 — rewrote assertion to observe
  the externally-visible cache miss, SHA p9q0r1s
Verify: tests pass, reproducing test still fails on the pre-fix
  state and passes on current HEAD ✓

[Final verification]
- go test ./... → exit 0 ✓
- 6 reproducing tests in tree, all pass ✓
- No constraint violations (pkg/legacy untouched) ✓

## Lead-Bug-Hunt Complete

### Commander's intent
[Verbatim]

### Outcome
Converged in 4 hunt-cycles. 6 bug-fix tickets fixed (2 Critical, 4 High).
Moderate refactor finisher made 18 commits cleaning up defensive
guards introduced during fixes. /review-test on the run's 6 new
reproducing tests surfaced 1 above-floor quality issue (brittle
assertion in test for #413), fixed via ticket #418. 8 findings below
floor (6 from /bug-hunt, 2 from /review-test) deferred to the report
— operator may run another iteration with a lower floor to address them.

### Convergence evidence
- Cycles run: 4 of 10
- Final two passes: cycle 3 (1 Low), cycle 4 (2 Low) — both below floor
- Reproducing tests in tree: 6
- Total tickets fixed: 6

### Tickets created and fixed
- [#412] Null deref in session.Validate when token expired in flight
        — fix SHA a1b2c3d — reproducing test session/session_test.go:142
- [#413] Race condition in cache.Set under concurrent invalidation
        — fix SHA d4e5f6a — reproducing test cache/cache_test.go:88
- ...
- [#418] (test quality) Rewrite reproducing test for #413 to observe
        externally-visible cache miss instead of internal state
        — fix SHA p9q0r1s — test file cache/cache_test.go:88

### Test review outcome
- Tests reviewed: 6 files (modified on this branch)
- Quality tickets created: 1 (#418)
- Quality tickets fixed: 1
- Deferred quality findings (below floor): 2 — see Deferred section

### Deferred findings (below severity floor)
- [Low | cycle 1 | /bug-hunt] Unchecked error in logger.Flush
- [Low | cycle 1 | /bug-hunt] Magic number in retry backoff (3000ms)
- [Low | termination 2b | /review-test] Docstring missing on test for #412
- [Low | termination 2b | /review-test] Redundant setup helper in test for #415
- ...

### Constraint adherence
No commits to pkg/legacy. Go 1.22 compatibility preserved.

### Changes summary
- Branch: lead-bug-hunt/2026-05-12 (SHA xyz)
- Commits on branch: 43 (24 bug fixes + 18 refactor + 1 test quality)
- Tickets fixed: 7 (6 bugs + 1 test quality)
- Finisher: moderate

### Run metadata
- Hunt cycles: 4 of 10
- Empty passes at termination: 2 consecutive
- Andon-cord pulls: 0
```

## Tips

**Pick your severity floor honestly.** "All severities" almost never converges — `/bug-hunt` always finds Low-severity opportunities. Default to Critical+High; lower the floor for follow-up iterations once the higher severities are clean.

**Run on a feature branch, never main.** The skill enforces this, but worth internalizing. Many commits will be produced.

**Resume is cheap.** Interrupting the skill (Ctrl-C, session end) is safe — the state doc captures enough to resume. Just re-invoke `/lead-bug-hunt` and choose "Resume" when prompted.

**The reproducing tests are durable.** Even if the skill pulls the andon cord mid-run, the reproducing tests `/bug-hunt` committed remain in the tree as durable acceptance criteria. The fixes either pass them or they don't.

**Andon cords are not failures.** Hitting a contested finding or a breaking-change requirement is the skill doing its job — surfacing decisions that need operator judgment. The cost of asking is much smaller than the cost of a silently bad fix.

**Pair with `/lead-refactor` separately if you want comprehensive cleanup.** The optional finisher is a tactical `/refactor`, not the architectural-review loop. For deep cleanup, run `/lead-refactor` after `/lead-bug-hunt` completes.

## Integration with Other Skills

**`/bug-hunt`:** the workhorse. `/lead-bug-hunt` auto-approves its ticket proposals — a contract shift authorized by the operator's commander's intent at startup. The completion report lists every ticket created so the operator can audit.

**`/implement-batch` and `/implement`:** the fix arms. Sub-skill escalations cascade up per the autonomy discipline; this skill either resolves them or pulls its own andon cord at a higher altitude.

**`/review-test`:** the test-quality gate at termination, scoped to the run's new reproducing tests. Same auto-approval contract shift as `/bug-hunt`. Use `/review-test` directly when you want a broader test-suite review unrelated to this skill.

**`/lead-project`:** the broader sibling. Use `/lead-project` when bug-hunting is one of several concerns; use `/lead-bug-hunt` when bug elimination is the sole objective. `/lead-project` may invoke `/lead-bug-hunt` from its Decide phase.

**`/refactor`:** the optional finisher. Not `/lead-refactor` — the architectural-review loop adds scope that isn't on this skill's axis.

## Agent Coordination

**Sequential execution.** One cycle at a time. One sub-skill invocation per cycle's Act phase. No parallel hunt-cycles.

**Context discipline.** The skill is a thin coordinator. Implementation work is delegated to sub-skills. Summary-level state lives in the skill's context; `LEAD_BUG_HUNT_STATE.md` holds durable memory.

**Sub-skill invocation.** Invoke via the Skill tool with autonomous overrides where supported. Interactive prompts from sub-skills are answered using engineering judgment anchored to commander's intent.

## Abort Conditions

**Do NOT abort for:**
- Individual cycle failures (try a different approach in the next cycle).
- Findings the skill thinks are exaggerated (apply severity floor mechanically; if it survives the floor, address it).
- Slow convergence (use the 10-cycle cap as the signal, not impatience).

**Pull the andon cord for:**
- Triggers listed under "The Andon Cord" above.

**Abort the entire workflow for:**
- Operator interrupts.
- Critical system error (repository corrupted, git state unrecoverable).
- Operator declines to confirm commander's intent at startup.
