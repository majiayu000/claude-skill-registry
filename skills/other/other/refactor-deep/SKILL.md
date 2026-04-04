---
name: refactor-deep
description: Comprehensive refactoring workflow that combines tactical and architectural passes. Runs /refactor (tactical cleanup), /review-arch (architectural restructuring), then /refactor again (cleanup after restructuring). All user input gathered upfront; fully autonomous after that.
model: opus
---

# Refactor-Deep - Tactical + Architectural Refactoring

Convenience workflow that runs a full tactical-then-architectural-then-tactical refactoring cycle. Gathers all user input upfront, then executes autonomously.

## Philosophy

**Tactical cleanup first, then structural improvement, then tactical cleanup again.** The first `/refactor` pass clears noise so `/review-arch` can focus on real structural issues. The architectural pass restructures the codebase. The final `/refactor` pass cleans up anything the restructuring introduced.

**Ask once, then execute.** All user decisions are gathered in a single upfront conversation. After that, the workflow runs to completion without interruption. The andon cord is the only escalation path.

## Workflow Overview

```
┌─────────────────────────────────────────────────────┐
│              REFACTOR-DEEP WORKFLOW                  │
├─────────────────────────────────────────────────────┤
│  0. Branch safety check                             │
│  1. Gather all user input                           │
│     ├─ Scope                                        │
│     ├─ Refactor aggression ceiling                  │
│     ├─ Arch review boldness                         │
│     └─ QA instructions                              │
│  2. Phase 1: /refactor (tactical cleanup)           │
│  3. Phase 2: /review-arch (architectural)           │
│  4. Phase 3: /refactor (post-restructuring cleanup) │
│  5. /review-doc (once, at the end)                  │
│  6. Completion summary                              │
└─────────────────────────────────────────────────────┘
```

## Workflow Details

### 0. Branch Safety Check

Before gathering any input, verify the current git branch.

**If on `main` or `master`:**
- Ask the user for confirmation: "You're on `<branch>`. This workflow will make many commits. Create a new branch, or proceed on `<branch>`?"
- If the user wants a new branch: create `refactor-deep/<date>` (e.g., `refactor-deep/2026-04-02`) and check it out.
- If the user explicitly confirms proceeding on main/master: continue.

**If on any other branch:** Proceed without asking.

### 1. Gather All User Input

Collect everything upfront in a single conversation. After this step, no further user interaction occurs (except andon cord).

#### 1a. Scope

**Default:** Entire codebase.

**If user specifies scope:** Respect that scope. Pass it to all three phases.

#### 1b. Refactor Aggression Ceiling

**Ask the user:** "How aggressive should the tactical refactoring passes be?"

Present these options:
- **Maximum**: Attempt all improvements, including aggressive changes (removing legacy code with unclear purpose, consolidating similar-but-not-identical behavior)
- **High**: Go up to MODERATE changes (cross-module DRY, removing abstraction layers, splitting files into focused modules) but skip aggressive changes
- **Low**: Only SAFEST and SAFE changes (formatters, linters, dead code, simple DRY, pruning single-use indirection, reducing stutter)
- **Let's discuss**: Talk through the situation to determine the right level

This ceiling applies to both `/refactor` passes (phases 2 and 4).

#### 1c. Arch Review Boldness

**Ask the user:** "How bold should the architectural restructuring be?"

Present these options:
- **Aggressive**: Implement all recommended changes — dissolutions, new modules, major restructuring. Use `/deliberate` for genuinely ambiguous trade-offs.
- **Moderate**: Implement clearly beneficial changes (dead code, renames, obvious function moves). Use `/deliberate` for high-impact items (module dissolution, new modules). Defer anything that seems uncertain.
- **Conservative**: Only implement low-risk architectural changes — dead code removal, renames, stutter fixes. Defer restructuring items to the completion summary as recommendations.

#### 1d. QA Instructions

**Ask the user:** "Are there any special verification steps for the QA agent? For example: visual checks, manual testing commands, specific scenarios to validate."

**If provided:** Pass these instructions to QA agents across all three phases.

**If none provided:** QA agents run standard verification (test suite, linters, formatters).

### 2. Phase 1: Tactical Refactoring

Run the `/refactor` workflow with:
- **Scope:** As specified in step 1a
- **Aggression ceiling:** As specified in step 1b
- **QA instructions:** As specified in step 1d

**Override:** Suppress `/refactor`'s built-in `/review-doc` pass (step 7 in `/refactor`). Documentation will be updated once at the end.

### 3. Phase 2: Architectural Review

Run the `/review-arch` workflow with autonomous overrides:

| `/review-arch` Step                 | Autonomous Override                                                        |
|--------------------------------------|----------------------------------------------------------------------------|
| **Step 1** (scope)                   | As specified in step 1a                                                    |
| **Step 2** (QA instructions)         | As specified in step 1d                                                    |
| **Step 3** (analyze)                 | Normal operation                                                           |
| **Step 4** (present analysis)        | **Orchestrator reviews the analysis.** Do not present to user.             |
| **Step 5** (iterate on plan)         | **Orchestrator decides based on boldness level (step 1c).** See below.     |
| **Step 6** (how to proceed)          | Proceed with implementation of approved items                              |
| **Steps 7-9** (implement + summary)  | Normal operation                                                           |
| **Step 10** (review-doc)             | **Suppressed.** Documentation updated once at the end.                     |

**Boldness-driven decision-making for step 5:**

- **Aggressive:** Approve all recommended items. Use `/deliberate` only when the analysis contains genuinely contradictory recommendations or unclear trade-offs.
- **Moderate:** Approve clearly beneficial items (dead code removal, naming improvements, obvious function ownership fixes). For high-impact items (module dissolution, major restructuring, new module creation), use `/deliberate` to reason through trade-offs. Defer items that seem uncertain — note them in the final summary as recommendations.
- **Conservative:** Approve only low-risk items (dead code removal, renames, stutter fixes). Defer all restructuring items to the final summary as recommendations for the user to consider.

### 4. Phase 3: Tactical Refactoring (Again)

Run the `/refactor` workflow again with identical parameters to phase 1:
- **Scope:** As specified in step 1a
- **Aggression ceiling:** As specified in step 1b
- **QA instructions:** As specified in step 1d

**Override:** Suppress `/refactor`'s built-in `/review-doc` pass. Documentation will be updated once at the end.

This pass cleans up anything the architectural restructuring introduced — new DRY opportunities from function moves, dead code exposed by dissolutions, naming inconsistencies from module renames.

### 5. Update Documentation

Run the `/review-doc` workflow once. This is the single documentation pass for the entire workflow. All three phases may have renamed functions, moved code, changed APIs, and restructured modules — documentation is updated to reflect the final state.

### 6. Completion Summary

Present a consolidated summary across all three phases:

```
## Refactor-Deep Complete

### Phase 1: Tactical Refactoring
- Commits: N
- Net lines changed: -XXX
- Batches completed: N / aborted: N

### Phase 2: Architectural Review
- Commits: N
- Net lines changed: -XXX
- Blueprint items completed: N / skipped: N

### Phase 3: Tactical Refactoring (Post-Restructuring)
- Commits: N
- Net lines changed: -XXX
- Batches completed: N / aborted: N

### Documentation
- Files updated: N

### Totals
- Total commits: N
- Total net lines changed: -XXX

### Deferred Architectural Items (if any)
[Items the orchestrator chose not to implement, with rationale.
 These are recommendations for the user to consider.]

### Aborted/Skipped Items (if any)
- [Description]: [reason for failure]
```

## Andon Cord Protocol

**This protocol applies throughout the entire workflow.** The andon cord is the escape valve for problems that cannot be resolved autonomously.

**Before pulling the andon cord:**
1. Attempt autonomous resolution first
2. For judgment calls, run `/deliberate` to reason through options
3. Only escalate if autonomous resolution has failed or is clearly futile

**When the andon cord is pulled:**
1. **Stop all work immediately**
2. Present to user:
   - Current phase and step
   - What was attempted and what went wrong
   - What autonomous resolution was tried (including any `/deliberate` results)
   - Recommended path forward (if you have one)
3. Wait for user guidance before resuming

**Andon cord triggers:**
- Phase workflow encounters an unrecoverable error
- Git repository in unclean state that can't be resolved
- Critical system error

## Abort Conditions

**Phase-level failures do NOT abort the workflow.** If phase 1 finds nothing to refactor, proceed to phase 2. If phase 2 finds no architectural improvements, proceed to phase 3. Only abort the entire workflow on andon cord triggers.

**Agent failures within phases:** Handled by the sub-workflow's own retry/abort logic (3 failures per batch/item, then skip).

## Integration with Other Skills

**This skill is a composition of:**
- `/refactor` — tactical code quality improvements within existing architecture
- `/review-arch` — strategic architectural analysis and restructuring
- `/review-doc` — documentation audit and updates

**Relationship to `/implement-project`:**
- `/implement-project` includes a similar quality pipeline (refactor → arch → refactor) as steps 7a-7c
- `/refactor-deep` extracts that pipeline as a standalone workflow for use outside of project implementation
- Use `/refactor-deep` when you want comprehensive refactoring without a ticket-driven implementation phase

**Relationship to individual skills:**
- Use `/refactor` alone for quick tactical cleanup
- Use `/review-arch` alone for interactive architectural analysis with user collaboration
- Use `/refactor-deep` when you want the full cycle, autonomous, in one shot
