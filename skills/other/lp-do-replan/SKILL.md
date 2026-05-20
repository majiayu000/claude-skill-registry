---
name: lp-do-replan
description: Thin orchestrator for resolving low-confidence plan tasks with evidence, explicit precursor tasks, stable task IDs, and checkpoint-aware reassessment.
---

# Re-Plan Orchestrator

`/lp-do-replan` updates an existing plan by converting uncertainty into evidence-backed task updates.

This orchestrator owns:
1. task selection and mode detection,
2. canonical replan gates,
3. module routing,
4. structured plan delta updates,
5. sequencing handoff,
6. decision-oriented completion output.

## Global Invariants

### Operating mode

**RE-PLANNING ONLY**

### Allowed actions

- Read/search files and docs.
- Run read-only commands needed for evidence (for example targeted tests, type checks, grep/ripgrep, static analysis commands).
- Update plan and replan notes docs.

### Prohibited actions

- Production implementation/refactor/migration changes.
- Destructive shell/git commands.
- Writing throwaway probe code in this skill.

If an assumption requires executable probe code, create a SPIKE precursor task instead of writing probes in `/lp-do-replan`.

## Inputs

- Existing plan: `docs/plans/<feature-slug>/plan.md` (legacy fallback allowed)
- Optional task IDs to target
- Optional fact-find brief

If plan is missing, route to `/lp-do-plan` (or create initial plan from fact-find then return).

## Invocation Modes

- `standard`: low-confidence/missing-contract replanning
- `checkpoint`: mid-build reassessment when `/lp-do-build` hits CHECKPOINT

Load checkpoint module only in checkpoint mode.

## Replan Gates (Canonical)

Evaluate and record these gates for each affected task:

1. **Promotion Gate**
- `<80 -> >=80` requires E2+ evidence or explicit precursor chain.

2. **Validation Gate**
- Runnable tasks require complete validation contracts before Ready status (task-type appropriate).

3. **Precursor Gate**
- Unresolved unknowns become formal precursor tasks (`INVESTIGATE` or `SPIKE`).
- No inline "needs spike" notes.

4. **Sequencing Gate**
- If topology changed (tasks added/split/removed/dependencies updated), run `/lp-do-sequence` in stable-ID mode (no renumbering).

5. **Escalation Gate**
- Ask user only when decision intent cannot be inferred after evidence review.

Shared doctrine sources:
- `../_shared/confidence-protocol.md`
- `../_shared/evidence-ladder.md`
- `../_shared/fail-first-biz.md`
- `../_shared/validation-contracts.md`
- `../_shared/replan-update-format.md`
- `../_shared/precursor-doctrine.md`

## Phase 1: Select Scope

Target explicit IDs when provided; otherwise include:
- all `IMPLEMENT` tasks below 80,
- all `SPIKE` tasks below 80,
- all `INVESTIGATE` tasks below 60,
- runnable tasks with missing/incomplete validation contracts,
- direct dependents affected by those tasks.

## Phase 2: Classify Track and Route

Determine per task:
- `Execution-Track`: `code | business-artifact | mixed`

Route modules:
- code -> `modules/replan-code.md`
- business-artifact -> `modules/replan-biz.md`
- mixed -> both modules + `modules/replan-validation.md`
- missing/weak validation contracts -> `modules/replan-validation.md`
- checkpoint invocation -> add `modules/replan-checkpoint.md`

## Phase 3: Apply Deltas to Plan

Use compact delta format from:
- `../_shared/replan-update-format.md`

Keep in-plan updates concise; put detailed evidence in:
- `docs/plans/<feature-slug>/replan-notes.md` when needed.

ID policy:
- Preserve existing TASK-IDs.
- New tasks get next available TASK-ID and remain stable.
- Dependencies reference stable TASK-IDs.

## Phase 3.5: Walkthrough Refresh Gate

If the replan changes process topology or operating-model behavior — branch triggers, CI/deploy lanes, approval paths, lifecycle states, handoffs, or multi-app orchestration — refresh the plan's `## Delivered Processes` section, not just the task tables.

Rules:
- Re-walk only the affected areas, but keep the full end-state flow internally consistent.
- Update unresolved seams or known issues when task splits, new precursor tasks, or dependency changes alter the delivered process.
- If the refreshed walkthrough exposes a new blocking seam, convert it into an explicit precursor task or lower readiness.

## Phase 4: Sequencing

When topology changed, run `/lp-do-sequence` with stable IDs preserved.

Expected sequence behavior for replan flows:
- reorder tasks,
- refresh `Depends on` / `Blocks` consistency,
- refresh Parallelism Guide,
- **do not renumber task IDs**.

## Replan Depth Gate

Track the replan round count in `docs/plans/<feature-slug>/replan-notes.md` using a frontmatter field `Replan-round: N`. Increment on each invocation.

If any task has been below its type threshold across 3+ consecutive replan rounds without new evidence or a viable new precursor path:
- Declare that task `Infeasible` in the plan with a one-line kill rationale.
- If all tasks that were the target of this replan are now `Infeasible` and no other runnable tasks remain: set plan `Status: Infeasible` in frontmatter, write a `## Kill Rationale` block, surface to user, and stop. Do not route to `/lp-do-build`.

## Phase 5: Readiness Decision

- `Ready`: runnable tasks meet type thresholds (`IMPLEMENT/SPIKE >=80`, `INVESTIGATE >=60`) and have complete validation contracts.
- `Partially ready`: precursor chain created; blocked tasks remain below type threshold. Build precursor tasks first.
- `Blocked (pending-decision)`: a DECISION task requires user input to proceed. Surface the specific question; build cannot continue until resolved.
- `Blocked (low-confidence)`: tasks remain below threshold with no viable precursor path and have not yet hit the 3-round depth limit. Escalate to user for scope clarification.
- `Infeasible`: tasks declared infeasible after hitting the replan depth gate. Pipeline ends.

## Completion Messages

Ready:

> Re-plan complete. Updated `docs/plans/<feature-slug>/plan.md`. Stable task IDs preserved. Eligible tasks are ready for `/lp-do-build`. If invoked from a CHECKPOINT in an active build pipeline: automatically resume `/lp-do-build <feature-slug>` without waiting for manual invocation.

Partially ready:

> Re-plan complete. Added precursor chain(s) and updated dependencies with stable task IDs. Build precursor tasks first, then re-run `/lp-do-replan` for blocked tasks.

Blocked (pending-decision):

> Re-plan blocked. DECISION required: [specific question]. Build cannot continue until resolved. See `docs/plans/<feature-slug>/replan-notes.md`.

Blocked (low-confidence):

> Re-plan complete but confidence floor not reached. No viable precursor path found. Escalating to user — scope clarification required before proceeding.

Infeasible:

> Re-plan terminated. Task(s) [IDs] declared infeasible after [N] replan rounds with no viable path. Plan `Status: Infeasible`. See `## Kill Rationale` in plan. Pipeline ends here.

## Quick Checklist

- [ ] Evidence-based confidence adjustments only
- [ ] Unknowns converted to formal precursor tasks
- [ ] Validation contracts complete for runnable tasks
- [ ] Stable task IDs preserved
- [ ] `## Delivered Processes` refreshed when the replan changed operating-model behavior
- [ ] `/lp-do-sequence` run after topology changes (no renumber)
