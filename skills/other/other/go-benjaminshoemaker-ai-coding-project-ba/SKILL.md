---
name: go
description: Resume execution from wherever you left off. Detects current state and runs the appropriate next command, or reports what's blocking progress. Use at the start of any session to pick up where you left off.
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

Determine where execution stands and either continue or report blockers.

## Workflow

Copy this checklist and track progress:

```
Go Progress:
- [ ] Detect context (project root vs feature directory)
- [ ] Check for execution plan
- [ ] Read phase state
- [ ] Determine next action
- [ ] Execute or report blockers
```

## Context Detection

Determine working context:

1. If current working directory matches pattern `*/features/*`:
   - PROJECT_ROOT = parent of parent of CWD (e.g., `/project/features/foo` → `/project`)
   - FEATURE_DIR = CWD
   - MODE = "feature"

2. Otherwise:
   - PROJECT_ROOT = current working directory
   - MODE = "greenfield"

## Step 1: Check for Execution Plan

Check if `EXECUTION_PLAN.md` exists in the current working directory (or FEATURE_DIR if feature mode).

**If no EXECUTION_PLAN.md:**

Check if this is the toolkit repo (e.g., `GENERATOR_PROMPT.md` exists or `.claude/skills/go/SKILL.md` exists in CWD):

```
NO EXECUTION PLAN
=================

You're in the toolkit repo, not a project directory.

To start a new project:
  1. /generate-plan <project-path>    (greenfield project)
  2. cd <project-path>
  3. /go

To add a feature to an existing project:
  1. /feature-plan <feature-name>     (from the project directory)
  2. cd features/<feature-name>
  3. /go
```

If NOT in the toolkit repo:

```
NO EXECUTION PLAN
=================

No EXECUTION_PLAN.md found in this directory.

Options:
  - If you have specs ready: Run /generate-plan from the toolkit repo
  - If this is a feature: cd features/<name> and try again
  - If you need specs first: Run /product-spec then /technical-spec
```

**Stop here** if no execution plan found.

## Step 2: Read Phase State

Read `.claude/phase-state.json` from PROJECT_ROOT (or FEATURE_DIR if feature mode).

Also read `EXECUTION_PLAN.md` to determine total phase count and current checkbox state.

### Parse Phase Count

Count the number of `## Phase N:` headers in EXECUTION_PLAN.md to determine TOTAL_PHASES.

### Parse State

If `phase-state.json` exists and is valid JSON with a `main` key:
- CURRENT_PHASE = `main.current_phase`
- PHASE_STATUS = status of the current phase from `main.phases[]`
- Check for in-progress tasks, blocked tasks, and failure counts

If `phase-state.json` does not exist or is invalid:
- STATE_EXISTS = false

## Step 3: Determine Next Action

Walk through these conditions **in order**. Take the FIRST match:

### Case A: No Phase State — First Run

**Condition:** `phase-state.json` doesn't exist or is invalid.

**Action:** Invoke `/fresh-start` using the Skill tool.

```
STARTING EXECUTION
==================
No prior state found. Running /fresh-start...
```

### Case B: Phase In Progress — Tasks Remaining

**Condition:** State exists. Current phase status is `IN_PROGRESS`. There are tasks in EXECUTION_PLAN.md for that phase with unchecked `- [ ]` acceptance criteria.

**Action:** Invoke `/phase-start {CURRENT_PHASE}` using the Skill tool. Phase-start handles resumption — it skips already-completed tasks.

```
RESUMING EXECUTION
==================
Phase {CURRENT_PHASE} in progress. Resuming...
{If a specific task was IN_PROGRESS in state: "Continuing from Task {id}"}
```

### Case C: Phase Tasks Complete — Needs Checkpoint

**Condition:** State exists. Current phase status is `IN_PROGRESS` or `COMPLETE`. ALL task acceptance criteria for the current phase are checked `[x]` in EXECUTION_PLAN.md. But phase status is NOT `CHECKPOINTED`.

**Action:** Invoke `/phase-checkpoint {CURRENT_PHASE}` using the Skill tool.

```
RUNNING CHECKPOINT
==================
All Phase {CURRENT_PHASE} tasks complete. Running quality gates...
```

### Case D: Phase Checkpointed — More Phases Exist

**Condition:** State exists. Current phase status is `CHECKPOINTED`. CURRENT_PHASE < TOTAL_PHASES.

**Action:** Invoke `/phase-prep {CURRENT_PHASE + 1}` using the Skill tool.

```
ADVANCING TO NEXT PHASE
========================
Phase {CURRENT_PHASE} checkpointed. Preparing Phase {CURRENT_PHASE + 1}...
```

### Case E: All Phases Complete

**Condition:** State exists. CURRENT_PHASE >= TOTAL_PHASES. Current phase status is `CHECKPOINTED` or `COMPLETE`.

**Action:** Check deferred review queue, then report completion.

1. Read `.claude/deferred-reviews.json`
2. Read `autoAdvance.drainOnCompletion` from `.claude/settings.local.json` (default: true)
3. If queue is non-empty (has `reviewed: false` items) AND `drainOnCompletion` is true:

```
PROJECT COMPLETE — DEFERRED REVIEW
===================================
All {TOTAL_PHASES} phases finished.

{N} items were deferred during execution.
These are non-blocking items that need human review:

Phase 1:
- [ ] "{criterion}" (Task {id})
  Context: {file}:{line} — {summary}

Phase 3:
- [ ] "{criterion}" (Task {id})
  Context: {file}:{line} — {summary}
```

Use AskUserQuestion:
- "All look good" → Clear queue (set all `reviewed: true`, remove reviewed items, update `last_drained`/`last_drain_reason`)
- "Review individually" → Invoke `/review-deferred`
- "Skip for now" → Keep queue, note in session

4. If queue is non-empty but `drainOnCompletion` is false:

```
EXECUTION COMPLETE
==================
All {TOTAL_PHASES} phases finished.

Note: {N} deferred review items remain in queue.
Use /review-deferred to review them when ready.

Summary:
- Phases completed: {TOTAL_PHASES}/{TOTAL_PHASES}
- Total tasks: {count from EXECUTION_PLAN.md}
- Deferred items: {N} pending review
```

5. If queue is empty or file doesn't exist:

```
EXECUTION COMPLETE
==================
All {TOTAL_PHASES} phases finished. All criteria verified. No deferred items.

Summary:
- Phases completed: {TOTAL_PHASES}/{TOTAL_PHASES}
- Total tasks: {count from EXECUTION_PLAN.md}

Consider:
- /progress              — Full completion report
- Review DEFERRED.md     — Any deferred requirements
- Review TODOS.md        — Follow-up work
```

### Case F: Blocked

**Condition:** State exists. Current phase has a task with status `BLOCKED`, or the phase itself is `BLOCKED`.

Check failure tracking in phase-state.json for blocked tasks.

Also check `.claude/deferred-reviews.json` — if the deferred queue has items and
`autoAdvance.drainOnBlocker` is true, present them: "While you're here, {N} deferred
items are pending review."

```
EXECUTION BLOCKED
=================
Phase {CURRENT_PHASE} is blocked.

{For each blocked task:}
Task {id}: {task subject from EXECUTION_PLAN.md}
  Consecutive failures: {count}
  Last errors:
    - {error 1}
    - {error 2}

{If deferred queue has items:}
While you're here, {N} deferred review items are pending:
- "{criterion}" (Task {id}) — {reason}
Use /review-deferred to review them now.
{/If}

Options:
  1. Fix the issue and run /go again
  2. /phase-start {CURRENT_PHASE}     — Retry from current task
  3. Edit EXECUTION_PLAN.md           — Modify blocked criteria
```

### Case G: Ambiguous State

**Condition:** None of the above cases matched (e.g., state file is partially written, phases array is empty, status is unrecognized).

**Action:** Offer to rebuild state.

```
STATE UNCLEAR
=============
phase-state.json exists but state is ambiguous.

Options:
  1. /populate-state      — Rebuild state from EXECUTION_PLAN.md + git history
  2. /fresh-start         — Start fresh (preserves git history)
  3. /progress            — Check EXECUTION_PLAN.md checkboxes directly
```

Use AskUserQuestion to let the user choose.

## Error Handling

- If EXECUTION_PLAN.md exists but is empty → report and suggest `/generate-plan`
- If phase-state.json has parse errors → treat as Case A (no state) with a note about the corrupt file
- If a delegated skill fails → report the failure, don't retry automatically
