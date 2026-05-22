---
name: qa-workflow
description: Complete QA Validator workflow orchestration. References specialized skills for each validation step. Load at session startup for full protocol.
category: orchestration
---

# QA Validator Workflow

> "Orchestration layer for QA validation - delegate to specialized skills for each step."

---

## Startup Workflow

1. Load `Skill("qa-router")` to understand your skill set

2. Load `Skill("threejs-builder")` to understand your Three.js skill set

3. Load `Skill("qa-validation-workflow")` to understand validation loops

4. **Process pending messages** - **IMPORTANT**: Messages are in the master branch, accessed via relative path like `../agentic-threejs/.claude/session/messages/qa/`. Consolidate all the .json messages requests and delete the files before continue. Update watchdog status.

5. **Read current-task-qa.json** - **IMPORTANT**: State file is in the master branch, accessed via relative path like `../agentic-threejs/.claude/session/current-task-qa.json`. Reason about the message request and define your next action

---

## State File Status Updates

Update `current-task-qa.json` immediately when status changes:

| Event               | Update State File                                               | Send Status Update to Watchdog                                           |
| ------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------ |
| Starting validation | `state.status = "working"` + `state.currentTaskId = "{taskId}"` | `Send-StatusUpdate -From "qa" -Status "working" -CurrentTask "{taskId}"` |
| Validation PASSED   | Include in bug_report message (PM sets passed in prd.json)      | -                                                                        |
| Validation FAILED   | Include bugs in bug_report message (PM updates prd.json)        | -                                                                        |
| Finishing           | `state.status = "idle"`                                         | `Send-StatusUpdate -From "qa" -Status "idle"`                            |

---

## Validation Workflow

**PRE-REQUISITE: You should already be in the correct worktree directory before starting this workflow!**

1. **UPDATE STATE FILE** (MANDATORY - First step)
   - Edit `current-task-qa.json`:
     - `state.status = "working"`
     - `state.currentTaskId = "{taskId}"`
     - `state.lastSeen = "{ISO_TIMESTAMP}"`
   - Send status update to watchdog: `Send-StatusUpdate -From "qa" -Status "working" -CurrentTask "{taskId}"`

2. **RUN VALIDATION FEEDBACK LOOPS**
   - Follow the guidelines of `qa-validation-workflow` and proceed with steps

3. **TEST COVERAGE CHECK**
   - `Skill("qa-test-creation")` - Check if tests exist for modified files
   - If tests missing: MUST invoke `test-creator` sub-agent before proceeding
4. **IF BLOCKED**
   - Update state: `state.status = "awaiting_pm"`
   - Send question to PM using the **Write tool**:

   ```
   Write to: .claude/session/messages/pm/msg-pm-{timestamp}-001.json
   Content:
   {
     "id": "msg-pm-{timestamp}-001",
     "from": "qa",
     "to": "pm",
     "type": "question",
     "priority": "high",
     "payload": {
       "question": "How should I handle X?",
       "context": "Current situation..."
     },
     "timestamp": "{ISO-8601-timestamp}",
     "status": "pending"
   }
   ```

   - Document blocker in task memory
   - Exit and wait

5. **TEST PASS** - Commit everything and merge it to the `master` branch

6. **TEST DO NOT PASS** - Check your skills and decision tree

7. **COMMIT** - At the end of the task, commit all changes to the current branch

8. **SEND TO PM**

- Update state: `state.status = "idle"`, `id = null`
- Send status update to watchdog: `Send-StatusUpdate -From "qa" -Status "idle"`
- Send completion message using the **Write tool**:

9. **EXIT**

## Quick Decision Tree

```

START VALIDATION
│
├─→ Tests missing? ──► Skill("qa-test-creation")
│
├─→ Run tests ─────────► Skill("qa-validation-workflow")
│ │
│ └─→ Tests fail? ──► Analyze (see Test Failure Decision Tree below)
│
├─→ Code quality check ──► Skill("qa-code-review")
│
├─→ Browser testing ────► Skill("qa-browser-testing")
│ └─► Choose sub-agent based on task type
│
└─→ Report result ─────► Skill("qa-reporting-bug-reporting")

```

---

## Test Failure Decision Tree

```

                    TESTS FAIL
                        │
        ┌───────────────┴───────────────┐
        │                               │
    Test Code Issue?              Game Code Issue?
        │ YES                          │ YES
        ▼                               ▼

Fix and Re-run                  Create Bug Report
(QA can edit)                  (Return to Developer)

```

## Exit Conditions

**BEFORE exiting, you MUST:**

2. **IF VALIDATION PASSES:** Merge to main and push
3. **IF VALIDATION FAILS:** Send bug_report to PM (no merge)
4. Update state file with validation results
5. Commit with `[ralph] [qa]` prefix
6. Send result message to PM
7. **MANDATORY:** Run server cleanup (shared-lifecycle)

---
