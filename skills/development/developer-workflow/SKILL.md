---
name: developer-workflow
description: Complete Developer workflow orchestration - task research sequence, implementation flow, validation gates, PRD synchronization, exit conditions.
category: workflow
---

# Developer Workflow

> "This skill orchestrates the development workflow sequence. For detailed implementation guidance."

---

## Startup Workflow

1. Load `Skill("dev-router")` to understand your skill set

2. Load `Skill("threejs-builder")` to understand your Three.js skill set

3. Load `Skill("shared-validation-feedback-loops")` to understand validation loops

4. **Process pending messages** - **IMPORTANT**: Messages are in the master branch, accessed via relative path like `../agentic-threejs/.claude/session/messages/developer/`. Consolidate all the .json messages requests and delete the files before continue. Update watchdog status.

5. **Read current-task-developer.json** - **IMPORTANT**: State file is in the master branch, accessed via relative path like `../agentic-threejs/.claude/session/current-task-developer.json`. Reason about the message request and define your next action

---

## Dashboard Status Update - **CRITICAL: Before starting ANY work action, update your status in current-task-developer.json:**

| Action                      | Update State File Like This                                                           | Send Status Update to Watchdog                                                  |
| --------------------------- | ------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Starting work on task**   | `state.status = "working"` + `id = "{taskId}"` + `state.lastSeen = "{ISO_TIMESTAMP}"` | `Send-StatusUpdate -From "developer" -Status "working" -CurrentTask "{taskId}"` |
| **Blocked by question**     | `state.status = "awaiting_pm"` + `state.lastSeen = "{ISO_TIMESTAMP}"`                 | `Send-StatusUpdate -From "developer" -Status "waiting"`                         |
| **Sending to QA**           | `state.status = "idle"` + `id = null` + `state.lastSeen = "{ISO_TIMESTAMP}"`          | `Send-StatusUpdate -From "developer" -Status "idle"`                            |
| **Self-reporting progress** | `state.lastSeen = "{ISO_TIMESTAMP}"`                                                  | -                                                                               |

---

## Implementation Workflow

**PRE-REQUISITE: You should already be in your worktree directory (`../developer-worktree`) before starting this workflow!**

1. **UPDATE STATE FILE** (MANDATORY - First step)
   - Edit `current-task-developer.json`:
     - `state.status = "working"`
     - `state.currentTaskId = "{taskId}"`
     - `state.lastSeen = "{ISO_TIMESTAMP}"`
   - Send status update to watchdog: `Send-StatusUpdate -From "developer" -Status "working" -CurrentTask "{taskId}"`

2. **Task Research** (MANDATORY Before Coding new tasks)
   - Step 1: GDD Reading (Bugs can skip it)

     ```
     Skill("dev-research-gdd-reading")
     ```

     - Read `docs/design/gdd/index.md` for overview
     - Read feature-specific GDD files
     - Check decision log and open questions

   - Step 2: Codebase Exploration

     ```
     Task({
     subagent_type: "developer-code-research",
     description: "Research patterns for {feature}",
     prompt: "Research existing codebase patterns for implementing {feature}",
     timeout: 300000
     })
     ```

3. **IMPLEMENTATION**
   - Create/modify files following researched patterns

4. **TEST COVERAGE CHECK** (MANDATORY - CANNOT SKIP)
   - `Skill("qa-test-creation")` - Check if tests exist for modified files
   - If tests missing: MUST invoke `test-creator` sub-agent before proceeding
   - Files changed without tests = BLOCKING - cannot proceed to step 8

   **⚠️ NON-BYPASSABLE GATE:**
   - NO exceptions for "bug fixes", "refactorings", or "non-visual changes"
   - Even trivial changes need test coverage (unit test minimum)
   - ONLY PM can approve skipping tests via explicit message

5. **IF BLOCKED**
   - Update state: `state.status = "awaiting_pm"`
   - Send question to PM using the **Write tool**:

   ```
   Write to: .claude/session/messages/pm/msg-pm-{timestamp}-001.json
   Content:
   {
     "id": "msg-pm-{timestamp}-001",
     "from": "developer",
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

6. **FEEDBACK LOOPS**

7. **COMMIT** - At the end of the task, commit all changes to your branch

8. **SEND TO QA**

- Update state: `state.status = "idle"`, `id = null`
- Send status update to watchdog: `Send-StatusUpdate -From "developer" -Status "idle"`
- Send completion using the **Write tool**:

  ```
  Write to: .claude/session/messages/pm/msg-pm-{timestamp}-001.json
  Content:
  {
    "id": "msg-pm-{timestamp}-001",
    "from": "developer",
    "to": "pm",
    "type": "task_complete",
    "priority": "normal",
    "payload": {
      "taskId": "{taskId}",
      "success": true,
      "summary": "Implementation complete"
    },
    "timestamp": "{ISO-8601-timestamp}",
    "status": "pending"
  }
  ```

9. **EXIT**

---
