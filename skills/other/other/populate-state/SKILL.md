---
name: populate-state
description: Generate `.claude/phase-state.json` from `EXECUTION_PLAN.md` and git history. Use to recover phase state after context loss or when joining an existing project.
allowed-tools: Bash, Read, Write, Edit, Glob, Grep, AskUserQuestion
---

# Populate Phase State

Generate `.claude/phase-state.json` from existing EXECUTION_PLAN.md and git history.

Use this command when:
- Starting to use the orchestrator on an existing project
- phase-state.json is missing or corrupted
- State has drifted from actual progress

## Workflow

Copy this checklist and track progress:

```
Populate State Progress:
- [ ] Directory guard (verify EXECUTION_PLAN.md exists)
- [ ] Ensure .claude directory exists
- [ ] Parse EXECUTION_PLAN.md (phases, tasks, criteria)
- [ ] Parse git history (commits, branches, timestamps)
- [ ] Detect features (features/*/EXECUTION_PLAN.md)
- [ ] Identify blockers (BLOCKED markers, stale tasks)
- [ ] Generate .claude/phase-state.json
- [ ] Determine task and phase statuses
- [ ] Output summary report
```

## Directory Guard (Wrong Directory Check)

Before starting:
- If the current directory appears to be the toolkit repo (e.g., `GENERATOR_PROMPT.md` exists), **STOP** and tell the user to run `/populate-state` from their project directory instead.
- Confirm `EXECUTION_PLAN.md` exists in the current working directory. If it does not exist, **STOP** and tell the user to `cd` into the directory containing `EXECUTION_PLAN.md` and re-run `/populate-state`.

## Instructions

1. **Ensure directory exists**
   ```bash
   mkdir -p .claude
   ```

2. **Parse EXECUTION_PLAN.md** to extract:
   - Total phases (count `## Phase N` headers)
   - Tasks per phase (count `#### Task X.Y.Z` headers)
   - Completion status per task (count `- [x]` vs `- [ ]` in acceptance criteria)
   - A task is COMPLETE if ALL its acceptance criteria are `[x]`

3. **Parse git history** to extract:
   - Task completion timestamps (from commits matching `task(X.Y.Z):`)
   - Phase branches (from branches matching `phase-N`)
   - Last activity date per phase

4. **Detect features** by scanning for:
   - `features/*/EXECUTION_PLAN.md` files
   - Parse each feature's execution plan the same way

5. **Identify blockers** by scanning EXECUTION_PLAN.md for:
   - Tasks with `**Status:** BLOCKED` marker
   - Tasks with incomplete criteria that have no recent git activity (7+ days)
   - Mark these as potentially blocked

6. **Generate `.claude/phase-state.json`** with this structure:

```json
{
  "schema_version": "1.0",
  "project_name": "{from directory name}",
  "last_updated": "{ISO timestamp}",
  "generated_by": "populate-state",

  "main": {
    "current_phase": 2,
    "total_phases": 6,
    "status": "IN_PROGRESS",
    "phases": [
      {
        "number": 1,
        "name": "Foundation",
        "status": "COMPLETE",
        "tasks_total": 8,
        "tasks_complete": 8,
        "completed_at": "2026-01-10T14:22:00Z"
      },
      {
        "number": 2,
        "name": "Core Features",
        "status": "IN_PROGRESS",
        "tasks_total": 12,
        "tasks_complete": 5,
        "started_at": "2026-01-11T09:00:00Z",
        "tasks": {
          "2.1.A": {"status": "COMPLETE", "completed_at": "..."},
          "2.1.B": {"status": "COMPLETE", "completed_at": "..."},
          "2.2.A": {"status": "IN_PROGRESS", "failures": {"consecutive": 0, "verification_attempts": {}, "last_errors": []}},
          "2.2.B": {"status": "NOT_STARTED"},
          "2.3.A": {"status": "BLOCKED", "blocker": "Needs API key", "since": "...", "failures": {"consecutive": 1, "verification_attempts": {"V-003": 3}, "last_errors": ["timeout connecting to API"]}}
        }
      }
    ]
  },

  "features": {
    "improved_metrics": {
      "path": "features/improved_metrics",
      "current_phase": 2,
      "total_phases": 4,
      "status": "IN_PROGRESS",
      "phases": [...]
    }
  }
}
```

7. **Determine task status** using this logic:
   - `COMPLETE`: All acceptance criteria are `[x]` AND git commit exists for task
   - `IN_PROGRESS`: Some criteria are `[x]` OR git commit exists but not all criteria done
   - `BLOCKED`: Has `**Status:** BLOCKED` marker OR stale (7+ days, incomplete)
   - `NOT_STARTED`: No criteria are `[x]` AND no git commit for task

8. **Determine phase status** using this logic:
   - `COMPLETE`: All tasks are COMPLETE
   - `IN_PROGRESS`: At least one task is IN_PROGRESS or COMPLETE, but not all COMPLETE
   - `BLOCKED`: Current task is BLOCKED
   - `NOT_STARTED`: No tasks have any progress

9. **Output summary** after generation:

```
Phase State Generated: .claude/phase-state.json

Main Project: Phase 2 of 6 (IN_PROGRESS)
  - Phase 1: COMPLETE (8/8 tasks)
  - Phase 2: IN_PROGRESS (5/12 tasks, 1 blocked)

Features:
  - improved_metrics: Phase 2 of 4 (IN_PROGRESS)
  - github_oauth: Phase 3 of 4 (IN_PROGRESS)

Blockers Found: 2
  - Task 2.3.A: Needs API key (blocked 3 days)
  - Feature improved_metrics Task 2.1.C: Test failures (blocked 1 day)
```

## Notes

- This command is **read-only** for EXECUTION_PLAN.md - it only generates state
- If phase-state.json exists, it will be **overwritten**
- Run this after manually updating EXECUTION_PLAN.md checkboxes
- The orchestrator can trigger this command on projects missing phase-state.json
