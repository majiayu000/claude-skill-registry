---
name: multi-session-orchestrator
description: "Orchestrate multi-session workflows that span multiple sessions or require state persistence. Use when tasks span multiple sessions. Not for single-session tasks or simple scripts."
---

# Multi-Session Orchestration

Test TaskList persistence across multiple Claude Code sessions.

## Multi-Session Workflow

**Session 1** (Initial Session):

1. Create TaskList with migration phases:
   - database-migration - Migrate database schema
   - application-migration - Migrate application code
   - data-validation - Validate migrated data
2. Mark database-migration as IN_PROGRESS
3. Execute database migration
4. Mark database-migration as COMPLETE
5. **CRITICAL**: Report TaskList ID for session continuation
   - This ID is required to resume in Session 2

**Session 2** (Resume Session):

1. Load existing TaskList by ID
2. Verify database-migration status is preserved (COMPLETE)
3. Mark application-migration as IN_PROGRESS
4. Execute application migration
5. Mark application-migration as COMPLETE
6. Mark data-validation as IN_PROGRESS
7. Execute data validation
8. Mark data-validation as COMPLETE
9. Report: Session 2 complete, migration finished

## Execution Workflow

**Execute autonomously:**

**For Session 1**:

1. Create TaskList with three migration tasks
2. Execute database-migration task
3. Report: TaskList ID for resumption

**For Session 2** (simulated continuation):

1. Verify TaskList state persisted
2. Continue execution from where Session 1 ended
3. Complete remaining tasks
4. Report: Cross-session continuation successful

## Expected Output

**Session 1 Output:**

```
Multi-Session Orchestration: SESSION 1
TaskList Created: [task-list-id]
[task-id] database-migration: IN_PROGRESS -> COMPLETE
[task-id] application-migration: PENDING
[task-id] data-validation: PENDING

SESSION 1 COMPLETE
TaskList ID: [id] - Save this for Session 2
```

**Session 2 Output (simulated):**

```
Multi-Session Orchestration: SESSION 2
TaskList Loaded: [task-list-id]
[task-id] database-migration: COMPLETE (status preserved)
[task-id] application-migration: IN_PROGRESS -> COMPLETE
[task-id] data-validation: IN_PROGRESS -> COMPLETE

SESSION 2 COMPLETE
Cross-Session Continuation: SUCCESS
Task State Persistence: VERIFIED
```

**Contrast:**

```
Good: TaskList ID saved and used to resume
Good: Status preserved across sessions
Good: Continuation seamless from previous state
Bad: TaskList recreated in Session 2
Bad: Previous state lost
```

**Validation criteria:**

- TaskList ID continuity
- Status preservation
- Seamless continuation

**Binary check:** "Proper cross-session persistence?" → All three criteria must pass.

---

<critical_constraint>
MANDATORY: Report TaskList ID for session continuation
MANDATORY: Verify state is preserved before proceeding
MANDATORY: Never lose TaskList ID between sessions
No exceptions. Cross-session continuity requires explicit ID management.
</critical_constraint>

---

## Genetic Code

This component carries essential Seed System principles for context: fork isolation:

<critical_constraint>
MANDATORY: All components MUST be self-contained (zero .claude/rules dependency)
MANDATORY: Achieve 80-95% autonomy (0-5 AskUserQuestion rounds per session)
MANDATORY: Description MUST use What-When-Not format in third person
MANDATORY: No component references another component by name in description
MANDATORY: Progressive disclosure - references/ for detailed content
MANDATORY: Use XML for control (mission_control, critical_constraint), Markdown for data
No exceptions. Portability invariant must be maintained.
</critical_constraint>

**Delta Standard**: Good Component = Expert Knowledge − What Claude Already Knows

**Recognition Questions**:

- "Would Claude know this without being told?" → Delete (zero delta)
- "Can this work standalone?" → Fix if no (non-self-sufficient)
- "Did I read the actual file, or just see it in grep?" → Verify before claiming

---
