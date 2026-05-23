---
name: session-resume
description: Cold-start resume — load all memory and project state to continue any interrupted project
triggers: [resume, continue, new session, where were we, restart project, pick up, interrupted, cold start]
context_cost: medium
---

# Session Resume Skill

## Goal
Allow ANY agent at ANY time to load the complete project state and continue as if they were there from the beginning. Zero knowledge loss between sessions. Always run integrity-check before continuing to verify current state.

## Steps

1. **Load PROJECT_STATE.md** (primary state file)
   - Read: `agents/memory/PROJECT_STATE.md`
   - Determine: current SDLC phase (S01-S10)
   - Note: last checkpoint, last completed milestone, current blockers

2. **Load CONTINUITY.md** (past failures — CRITICAL, read before doing anything)
   - Read: `agents/memory/CONTINUITY.md`
   - Identify: any past failed approaches relevant to current work
   - Note: libraries that caused conflicts, patterns that didn't work, decisions reversed

3. **Load AUDIT_LOG.md** (recent history)
   - Read last 50 entries from: `agents/memory/AUDIT_LOG.md`
   - Understand: recent decisions, what was completed, what was blocked

4. **Load latest SESSION_SNAPSHOT** (working context)
   - Find the most recent file in: `agents/memory/episodic/SESSION_SNAPSHOT/`
   - Read the snapshot for the current SDLC phase
   - Restore: task context, open questions, implementation decisions

5. **Load semantic knowledge** (crystallized facts)
   - Read: `agents/memory/semantic/PROJECT_KNOWLEDGE_TEMPLATE.md`
   - Note: verified library APIs, confirmed architecture decisions, known constraints

6. **Read current project/tasks.md**
   - Identify: all TODO tasks, IN_PROGRESS tasks, BLOCKED tasks
   - Note: any tasks that are blocked and what's blocking them

7. **Run integrity-check.skill** (before starting any new work)
   - Verify current codebase matches the state recorded in memory
   - Catch: any changes made outside of agent sessions, merge conflicts, etc.
   - If integrity fails: investigate before proceeding

8. **Produce Resume Report** (present to human before continuing)
   ```markdown
   ## Project Resume Report

   ### Project State
   - Current SDLC phase: [S0X — Phase Name]
   - Last checkpoint: [date] at [phase]
   - Overall progress: [X/10 phases complete]

   ### What Was Completed (last session)
   - [list of completed tasks/phases]

   ### What Was In Progress
   - [task name] — [where it was left, what remains]

   ### Blocked Items
   - [task] blocked by: [reason / pending human decision]

   ### Open Human Decisions Pending
   - [question 1 still waiting for answer]

   ### Known Issues / Constraints (from CONTINUITY.md)
   - [any relevant past failures to avoid repeating]

   ### Integrity Check Result
   - [PASS/FAIL — details if fail]

   ### Recommended Next Action
   [What I will do next, starting from: task X in project/tasks.md]

   Ready to continue? Please confirm or direct me to a different task.
   ```

9. **Wait for human confirmation** before starting work
   - Human may redirect to different priority
   - Human may resolve pending decisions listed in report

10. **Continue from next pending task**
    - Pick up from the first TODO or IN_PROGRESS task in project/tasks.md
    - Apply RARV cycle (loki/RARV_CYCLE.md)

## Memory Loading Order (critical — load in this sequence)

```
1. PROJECT_STATE.md    → SDLC phase, last checkpoint
2. CONTINUITY.md       → past failures (MOST IMPORTANT — read before anything)
3. AUDIT_LOG.md        → last 50 entries (recent decisions)
4. SESSION_SNAPSHOT/   → latest milestone snapshot
5. semantic/           → crystallized project knowledge
6. project/tasks.md            → current task status
7. integrity-check     → verify state is consistent
```

## Constraints
- NEVER start new work without first completing all 7 loading steps
- NEVER skip the integrity check — it catches silent state corruption
- If CONTINUITY.md mentions a failed approach: do NOT repeat it
- If human decisions are pending in AUDIT_LOG: surface them before starting new work

## Output Format
Resume Report (presented to human) + confirmation of which task will be worked on next.
