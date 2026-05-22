---
name: refactor-deep
description: Comprehensive refactoring workflow that pairs tactical refactoring with architectural review. Runs /refactor (tactical cleanup), then /review-arch (advisory architectural analysis, with the option to cut tickets for the recommended work). All user input gathered upfront, except for ticket review at the end of Phase 2.
model: opus
---

# Refactor-Deep — Tactical Cleanup + Architectural Review

Convenience workflow that pairs `/refactor` with `/review-arch`. The tactical pass cleans up the codebase; the architectural pass analyzes structure and (optionally) converts its recommendations into tickets the operator can pick up later. Gathers all user input upfront and runs Phase 1 autonomously; pauses once in Phase 2 for ticket review when applicable.

## Philosophy

**Tactical cleanup first, then architectural read-out.** The `/refactor` pass clears noise so `/review-arch` can focus on real structural opportunities. The architectural pass is **advisory** as of `/review-arch`'s v8.0.0 transformation (see the "Advisory aspiration" section of [`references/autonomy.md`](../../references/autonomy.md)) — it surfaces a plan but does not implement. `/review-arch` offers to cut tickets so the recommended work is captured for later implementation by `/refactor`, `/implement`, or `/implement-batch`.

**Ask once, then execute — with one ticket-review interruption.** All major user decisions are gathered in a single upfront conversation. The workflow then runs Phase 1 autonomously. In Phase 2, if the operator opted in to ticket creation, the skill pauses once for the operator to review and approve the ticket set before any tickets are created in the tracker. Ticket review is the only mid-run user touchpoint; the andon cord remains the only unplanned escalation path.

This skill implements the autonomy discipline documented in [`references/autonomy.md`](../../references/autonomy.md). Its upfront-input gathering is the skill's commander's intent (six fields: scope, aggression ceiling, QA instructions, ticket-creation preference, constraints, non-goals).

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│              REFACTOR-DEEP WORKFLOW                  │
├─────────────────────────────────────────────────────┤
│  0. Branch safety check                             │
│  1. Gather all user input                           │
│     ├─ Scope                                        │
│     ├─ Refactor aggression ceiling                  │
│     ├─ QA instructions                              │
│     └─ Ticket-creation preference (Phase 2)         │
│  2. Phase 1: /refactor (tactical cleanup)           │
│  3. Phase 2: /review-arch (advisory; may cut tickets)│
│  4. /tidy-docs (once, at the end)                  │
│  5. Completion summary                              │
└─────────────────────────────────────────────────────┘
```

The former third phase (a second `/refactor` after `/review-arch` implemented changes) is removed. `/review-arch` no longer implements changes (see the "Advisory aspiration" section of [`references/autonomy.md`](../../references/autonomy.md)), so there is nothing for a post-restructuring tactical cleanup to do. Any work `/review-arch` surfaces is captured as tickets (operator-approved) and picked up by separate skill invocations afterwards.

## Workflow Details

### 0. Branch Safety Check

Before gathering any input, verify the current git branch.

**If on `main` or `master`:**
- Ask the user for confirmation: "You're on `<branch>`. This workflow will make many commits. Create a new branch, or proceed on `<branch>`?"
- If the user wants a new branch: create `refactor-deep/<date>` (e.g., `refactor-deep/2026-04-02`) and check it out.
- If the user explicitly confirms proceeding on main/master: continue.

**If on any other branch:** Proceed without asking.

### 1. Gather All User Input

Collect everything upfront in a single conversation. After this step, the only further user interaction is the ticket-review pause in Phase 2 (and only if ticket creation is opted in).

#### 1a. Scope

**Default:** Entire codebase.

**If user specifies scope:** Respect that scope. Pass it to both phases.

#### 1b. Refactor Aggression Ceiling

**Ask the user:** "How aggressive should the tactical refactoring pass be?"

Present these options:
- **Maximum**: Attempt all improvements, including aggressive changes (removing legacy code with unclear purpose, consolidating similar-but-not-identical behavior)
- **High**: Go up to MODERATE changes (cross-module DRY, removing abstraction layers, splitting files into focused modules) but skip aggressive changes
- **Low**: Only SAFEST and SAFE changes (formatters, linters, dead code, simple DRY, pruning single-use indirection, reducing stutter)
- **Let's discuss**: Talk through the situation to determine the right level

This ceiling applies to the Phase 1 `/refactor` pass.

#### 1c. QA Instructions

**Ask the user:** "Are there any special verification steps for the QA agent? For example: visual checks, manual testing commands, specific scenarios to validate."

**If provided:** Pass these instructions to the Phase 1 QA agent.

**If none provided:** QA agents run standard verification (test suite, linters, formatters).

#### 1d. Ticket-Creation Preference

**Ask the user:** "After Phase 2's architectural analysis, would you like to cut tickets for the recommended work?"

Present these options:
- **Yes (default)**: After `/review-arch` finalizes the plan, pause for the operator to review the proposed ticket set, then create the tickets in the tracker. This is the only mid-run user touchpoint.
- **No**: Skip ticket creation. The architectural analysis surfaces in the completion summary as advisory recommendations only.
- **Preview-then-decide**: Run the analysis, show the proposed ticket set when it's ready, and ask interactively whether to create them. Same effective outcome as "Yes" but gives a clearer escape hatch.

The choice is passed through to `/review-arch` in Phase 2.

### 2. Phase 1: Tactical Refactoring

Run the `/refactor` workflow with:
- **Scope:** As specified in step 1a
- **Aggression ceiling:** As specified in step 1b
- **QA instructions:** As specified in step 1c

**Override:** Suppress `/refactor`'s built-in `/tidy-docs` pass (step 7 in `/refactor`). Documentation will be updated once at the end.

### 3. Phase 2: Architectural Review (Advisory)

Run the `/review-arch` workflow. It will offer to cut tickets after presenting the analysis; the operator's upfront ticket-creation preference (from step 1d) determines how the offer is handled. `/review-arch` is advisory as of v8.0.0 — it does not implement changes.

| `/review-arch` Step                     | Behavior in `/refactor-deep` Phase 2                                                                                                                                                                                                                                                       |
|-----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Step 1** (scope)                      | Scope: from step 1a.                                                                                                                                                                                                                                                                       |
| **Step 2** (analyze)                    | Normal operation.                                                                                                                                                                                                                                                                          |
| **Step 3** (present analysis to user)   | The operator participates. This is one of the mid-run user touchpoints.                                                                                                                                                                                                                    |
| **Step 4** (iterate on plan with user)  | The operator participates. They shape the plan.                                                                                                                                                                                                                                            |
| **Step 5** (offer to cut tickets)       | Behavior depends on the ticket-creation preference from step 1d:<br>**Yes** — `/review-arch` proceeds with its standard preview-and-approve ticket flow.<br>**Preview-then-decide** — same as Yes; the operator decides at the preview step.<br>**No** — pass through; `/review-arch` skips its ticket-creation offer and produces only the advisory report. |
| **Step 6** (completion summary)         | `/review-arch` returns its summary (tickets created, or advisory analysis); `/refactor-deep` captures it for the final summary.                                                                                                                                                            |

### 4. Update Documentation

Run the `/tidy-docs` workflow once. Phase 1's tactical changes may have renamed functions or moved code; documentation is updated to reflect the new state.

### 5. Completion Summary

Present a consolidated summary across both phases:

```
## Refactor-Deep Complete

### Phase 1: Tactical Refactoring
- Commits: N
- Net lines changed: -XXX
- Batches completed: N / aborted: N

### Phase 2: Architectural Review (Advisory)
- Blueprint items proposed: N
- Items finalized for ticket creation: N (or "ticket creation declined")
- Tickets created: [list of #N references]
  (or: "No tickets — analysis was advisory-only.")

### Documentation
- Files updated: N

### Totals
- Total commits: N
- Total net lines changed: -XXX

### Recommended next steps
[If tickets were created: brief paragraph naming the natural follow-up,
 e.g. "Tickets are labeled `arch`; consider `/implement-batch` to work
 through them as a cohesive unit."
 If no tickets were created: the architectural analysis stands as a
 planning artifact; the operator can revisit later by running
 /review-arch standalone.]

### Aborted/Skipped Items (if any)
- [Description]: [reason for failure]
```

## Andon Cord Protocol

**This protocol applies throughout the entire workflow.** The andon cord is the escape valve for problems that cannot be resolved autonomously. Ticket review in Phase 2 is a planned interactive touchpoint, not an andon-cord pull.

**Before pulling the andon cord:**
1. Attempt autonomous resolution first.
2. For judgment calls, run `/think-deliberate` to reason through options.
3. Only escalate if autonomous resolution has failed or is clearly futile.

**When the andon cord is pulled:**
1. **Stop all work immediately.**
2. Produce a handoff using the **shared handoff template** in [`references/autonomy.md`](../../references/autonomy.md). The escalation must include pre-loaded options (2–3 named choices), an explicit recommendation, the one tradeoff that would flip the recommendation, and a pre-rebutted counterargument. Include the skill-specific state: current phase, what `/refactor` or `/review-arch` was doing at the time, and any `/think-deliberate` verdicts already considered.
3. Wait for user guidance before resuming.

**Andon cord triggers (skill-specific):**
- Phase workflow encounters an unrecoverable error.
- Git repository in unclean state that can't be resolved.
- Tracker is unavailable when the operator approved ticket creation (Phase 2) — surface the proposed ticket set in the handoff so the operator can either retry tracker setup or create tickets manually.
- Critical system error.

## Abort Conditions

**Phase-level failures do NOT abort the workflow.** If Phase 1 finds nothing to refactor, proceed to Phase 2. If Phase 2 finds no architectural improvements, proceed to documentation update. Only abort the entire workflow on andon-cord triggers.

**Agent failures within phases:** Handled by the sub-workflow's own retry/abort logic (3 failures per batch/item, then skip).

**Ticket creation declined or fails mid-Phase-2:** Not an abort condition. The architectural analysis still stands as advisory output and surfaces in the completion summary. The operator can run `/review-arch` standalone later to revisit.

## Integration with Other Skills

**This skill is a composition of:**
- `/refactor` — tactical code quality improvements within existing architecture
- `/review-arch` — advisory architectural analysis (offers to cut tickets)
- `/tidy-docs` — documentation audit and updates

**`/refactor-deep` vs the parts:** Use `/refactor` alone for quick tactical cleanup; use `/review-arch` alone for an architectural read-out; use `/refactor-deep` when you want both — tactical pass first, then architectural analysis with ticket review.

**`/refactor-deep` vs `/implement-project`:** Both run `/refactor` and `/review-arch` as part of their pipelines. Use `/refactor-deep` when you want comprehensive cleanup with the option to capture architectural follow-ups as tickets; use `/implement-project` when you have a known ticket batch and want a once-through pipeline.
