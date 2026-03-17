---
name: progress
description: Show progress through EXECUTION_PLAN.md and feature plans. Use to check completion status and identify remaining work.
allowed-tools: Read, Grep, Glob
---

Read EXECUTION_PLAN.md and any feature execution plans to show overall project status.

## Workflow

Copy this checklist and track progress:

```
Progress Report:
- [ ] Step 1: Directory guard check
- [ ] Step 2: Discover all execution plans
- [ ] Step 3: Count checkbox categories
- [ ] Step 4: Calculate completion percentages
- [ ] Step 5: Generate progress report
```

After parsing EXECUTION_PLAN.md, validate that at least one phase and one task were found. If parsing yields zero phases or zero tasks, report a parse error (e.g., "EXECUTION_PLAN.md found but no phases/tasks detected — file may be malformed") and stop.

## Directory Guard (Wrong Directory Check)

Before starting, confirm `EXECUTION_PLAN.md` exists in the current working directory.

- If it does not exist, **STOP** and tell the user to `cd` into their project directory (the one containing `EXECUTION_PLAN.md`) and re-run `/progress`.

## Discover All Execution Plans

Search for execution plans in the project:

```bash
# Main project plan (required)
EXECUTION_PLAN.md

# Feature plans (optional) - check common locations
features/*/EXECUTION_PLAN.md
features/**/EXECUTION_PLAN.md
FEATURES/*/EXECUTION_PLAN.md
```

Build a list of all execution plans found:
1. Main: `./EXECUTION_PLAN.md` (always present)
2. Features: Any `EXECUTION_PLAN.md` files in `features/` subdirectories

## Checkbox Categories

Execution plans contain **4 distinct checkbox categories**. Count them separately:

| Category | Location | Identifier |
|----------|----------|------------|
| **Task Acceptance Criteria** | Under `#### Task X.Y.Z` headers, after `**Acceptance Criteria:**` | Has type tags like `(TEST)`, `(CODE)`, `(BROWSER:*)`, `(MANUAL)`, `(MANUAL:DEFER)` |
| **Phase Checkpoint Criteria** | Under `### Phase N Checkpoint` headers | Sections: "Automated Checks", "Manual Local Verification", "Browser Verification" |
| **Pre-Phase Setup Criteria** | Under `### Pre-Phase Setup` headers | Items with `Verify:` commands |
| **Manual Verification** | Under "Human Required" headers | Items with `Reason:` lines |

**Primary Metric:** Task Acceptance Criteria only (represents actual implementation work).

**Secondary Metrics:** Checkpoint, Setup, and Manual criteria (procedural/verification work).

**How to distinguish categories when counting:**
- **Task criteria**: Found under `#### Task X.Y.Z` headers; lines match `- [ ] .*\((TEST|CODE|BROWSER|MANUAL|MANUAL:DEFER)\)`
- **Checkpoint criteria**: Found under `### Phase N Checkpoint`; in "Automated Checks" or "Manual Verification" subsections
- **Setup criteria**: Found under `### Pre-Phase Setup`; lines contain `Verify:` commands
- **Manual verification**: Under "Human Required" headers; lines have `Reason:` annotations

When in doubt, check the parent header level: `####` = task, `###` = phase-level.

## Progress Report Format

### If Multiple Execution Plans Exist

Show an **Overall Summary** first, then individual plan details:

```
OVERALL PROJECT PROGRESS
========================

  Plan                              Status        Progress
  ─────────────────────────────────────────────────────────
  Main Project                      Complete      45/45 (100%)
  Feature: user-auth                In Progress   12/18 (67%)
  Feature: payments                 Not Started    0/24 (0%)
  ─────────────────────────────────────────────────────────
  TOTAL                                           57/87 (66%)

Next action: Continue with Feature: user-auth Phase 2
```

Then show detailed breakdown for each plan (see Individual Plan Report below).

### If Only Main Execution Plan Exists

Skip the overall summary and show the Individual Plan Report directly.

## Individual Plan Report

For each execution plan, show:

### 1. Overview
- Plan name (Main Project or Feature: {name})
- Total phases, steps, tasks
- Current phase in progress

### 2. Completion Status

For each phase, count **Task Acceptance Criteria only**:
- Total criteria: Count `- [ ]` and `- [x]` lines under `#### Task` sections
- Verified: Count `- [x]` lines that do NOT contain `— Deferred:`
- Deferred: Count `- [x]` lines that contain `— Deferred:` (implemented but pending review)
- Remaining: Count `- [ ]` lines

Calculate percentage complete per phase. Deferred items count toward completion
(they are implemented) but are reported separately for visibility.

**Important:** Do NOT count checkpoint criteria, pre-phase setup items, or phase-level verification checkboxes in the primary progress metric.

### 3. Current Position
- Last completed task (all its acceptance criteria are `[x]`)
- Next task to execute (first task with any `[ ]` criteria)
- Any blocked tasks (marked with `**Status:** BLOCKED`)

### 4. Summary Table

```
| Phase | Status | Task Criteria | Checkpoint Criteria |
|-------|--------|---------------|---------------------|
| Phase 1: {name} | Complete | 12/12 (100%) | 5/5 |
| Phase 2: {name} | In Progress | 5/8 (62%) | 0/4 |
| Phase 3: {name} | Not Started | 0/10 (0%) | 0/6 |
```

Status definitions:
- **Complete**: All task acceptance criteria checked
- **In Progress**: Some task criteria checked, some unchecked
- **Not Started**: No task criteria checked

### 5. Verification Breakdown (optional, if relevant)

If checkpoint or setup criteria exist, show:
```
Additional Criteria:
- Pre-Phase Setup: X/Y completed
- Phase Checkpoints: X/Y completed
- Manual Verification: X/Y confirmed
```

### 6. Deferred Review Queue (if items exist)

Read `.claude/deferred-reviews.json` and count unreviewed items:

```
Deferred Review Queue:
- Pending review: {N} items across {P} phases
- Use /review-deferred to review them
```

Only show this section if the queue file exists and has unreviewed items.

If `.claude/deferred-reviews.json` exists but fails to parse (invalid JSON), treat as empty and note: "Deferred review queue file is corrupt — treating as empty."

## Next Action Recommendation

Based on overall status, recommend what to do next:

**If main project incomplete:**
- Continue with task X.Y.Z
- Run /phase-checkpoint N (if all tasks in phase complete)
- Run /phase-prep N for next phase

**If main project complete but features incomplete:**
- Continue with Feature: {name} task X.Y.Z
- Note: `cd features/{name}` to work on that feature

**If everything complete:**
```
All execution plans complete!

Main Project: 100% (45/45 criteria)
Features: 100% (42/42 criteria)

Consider:
- Run final /phase-checkpoint on each plan
- Review for any deferred items in DEFERRED.md
- Check .claude/deferred-reviews.json for pending verification reviews (/review-deferred)
- Check TODOS.md for follow-up work
```

## Error Handling

**If EXECUTION_PLAN.md exists but is empty:**
- Report: "EXECUTION_PLAN.md exists but contains no content"
- Suggest running `/generate-plan` to populate it

**If EXECUTION_PLAN.md has unexpected format:**
- Attempt to parse what exists
- Report any sections that couldn't be parsed
- Show raw checkbox counts as fallback: "Found X checkboxes (Y checked)"

**If feature plan directory exists but EXECUTION_PLAN.md is missing:**
- Report the feature directory was found but has no execution plan
- List: "Feature directory without plan: features/{name}/"
- Suggest: "Run /feature-plan to generate the missing plan"

**If checkbox parsing yields zero items:**
- Report: "No task acceptance criteria found in EXECUTION_PLAN.md"
- Check if the file uses non-standard checkbox format
- Suggest verifying the plan was generated correctly

**If file read permissions fail:**
- Report which file couldn't be read
- Continue with other files if possible
- Suggest checking file permissions

## Feature Plan Discovery Details

When scanning for feature plans:

1. **Directory patterns to check:**
   - `features/*/EXECUTION_PLAN.md`
   - `FEATURES/*/EXECUTION_PLAN.md`
   - `feature/*/EXECUTION_PLAN.md`

2. **Extract feature name from path:**
   - `features/user-auth/EXECUTION_PLAN.md` → "user-auth"
   - `features/payments/EXECUTION_PLAN.md` → "payments"

3. **Skip non-feature plans:**
   - Don't include the main `EXECUTION_PLAN.md` twice
   - Don't include template or example files

## Output Examples

### Single Plan (Main Only)

```
PROJECT PROGRESS
================

Main Project: EXECUTION_PLAN.md
Phases: 4 | Steps: 12 | Tasks: 28

| Phase | Status | Task Criteria | Checkpoint |
|-------|--------|---------------|------------|
| Phase 1: Setup | Complete | 8/8 (100%) | 3/3 |
| Phase 2: Core API | In Progress | 5/12 (42%) | 0/4 |
| Phase 3: Frontend | Not Started | 0/6 (0%) | 0/3 |
| Phase 4: Deploy | Not Started | 0/2 (0%) | 0/2 |

Current: Task 2.2.A - Implement user endpoints
Next: Complete Task 2.2.A, then Task 2.2.B

Overall: 13/28 criteria (46%)
```

### Multiple Plans (Main + Features)

```
OVERALL PROJECT PROGRESS
========================

  Plan                              Status        Progress
  ─────────────────────────────────────────────────────────
  Main Project                      Complete      45/45 (100%)
  Feature: user-auth                In Progress   12/18 (67%)
  Feature: payments                 Not Started    0/24 (0%)
  ─────────────────────────────────────────────────────────
  TOTAL                                           57/87 (66%)

─────────────────────────────────────────────────────────────

MAIN PROJECT (Complete)
=======================
All 4 phases complete. 45/45 task criteria satisfied.

─────────────────────────────────────────────────────────────

FEATURE: user-auth (In Progress)
================================
Location: features/user-auth/EXECUTION_PLAN.md

| Phase | Status | Task Criteria | Checkpoint |
|-------|--------|---------------|------------|
| Phase 1: OAuth Setup | Complete | 6/6 (100%) | 2/2 |
| Phase 2: Session Mgmt | In Progress | 6/12 (50%) | 0/3 |

Current: Task 2.1.B - Add session refresh logic
Next: Complete Task 2.1.B, then Task 2.1.C

─────────────────────────────────────────────────────────────

FEATURE: payments (Not Started)
===============================
Location: features/payments/EXECUTION_PLAN.md

| Phase | Status | Task Criteria | Checkpoint |
|-------|--------|---------------|------------|
| Phase 1: Stripe Setup | Not Started | 0/8 (0%) | 0/2 |
| Phase 2: Checkout | Not Started | 0/10 (0%) | 0/3 |
| Phase 3: Webhooks | Not Started | 0/6 (0%) | 0/2 |

─────────────────────────────────────────────────────────────

NEXT ACTION
===========
Continue with Feature: user-auth
  cd features/user-auth
  /phase-start 2  (or continue Task 2.1.B)
```
