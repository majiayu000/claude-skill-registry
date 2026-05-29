---
name: executing-plans-review
description: Verification, drift detection, and snapshot logic for executing-plans
user-invocable: false
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Edit
  - Write
  - Task
  - AskUserQuestion
  - mcp__plugin_mermaid-collab_mermaid__*
---

# Verification and Review Phase Details

This document contains detailed verification, drift detection, and snapshot logic for the executing-plans skill.

## Snapshot Saving

Save context snapshots to enable recovery after compaction events. This preserves the executing-plans skill's state and progress across context compaction.

### When to Save

Call `saveSnapshot()` at these critical points:
- After each wave of tasks completes
- After full test suite passes (post-wave verification)
- After each individual task completes (per-task verification)
- Before asking for user feedback
- At major milestones (all tasks complete)

### Save Function

```javascript
FUNCTION saveSnapshot():
  session = current session name

  // Read current state via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
  Args: { "project": "<cwd>", "session": session }
  Returns: state = { "phase": "...", "completedTasks": [...], "pendingTasks": [...], ... }

  // Save snapshot via MCP
  Tool: mcp__plugin_mermaid-collab_mermaid__save_snapshot
  Args: {
    "project": "<cwd>",
    "session": session,
    "activeSkill": "executing-plans",
    "currentStep": "implementation",
    "inProgressItem": null,
    "pendingQuestion": null,
    "recentContext": [
      {
        "type": "progress",
        "content": "Completed tasks: {state.completedTasks}. Pending: {state.pendingTasks}. Last wave: {wave number}"
      }
    ]
  }
  // Note: version and timestamp are automatically added

  // Update collab state to mark snapshot exists
  Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
  Args: {
    "project": "<cwd>",
    "session": session,
    "hasSnapshot": true,
    "lastSnapshot": "<current-ISO-timestamp>"
  }
```

### Save Points with Examples

**After wave completes with test suite passing:**
```
[Wave N tasks all complete]
-> Run full test suite: npm run test:ci
-> If tests FAIL: Stop, report failure (don't save)
-> If tests PASS:
   - saveSnapshot()
   - Update task diagram (all Wave N tasks -> "completed")
   - Show wave completion report
   - Proceed to next wave
```

Example snapshot after Wave 1:
```json
{
  "version": 1,
  "timestamp": "2026-01-21T14:35:22Z",
  "activeSkill": "executing-plans",
  "currentStep": "implementation",
  "completedTasks": ["task-planning-skill", "gather-goals-types", "brainstorming-cleanup"],
  "pendingTasks": ["collab-routing", "executing-plans-tdd-skip", "pre-compact-script"],
  "recentContext": [
    {
      "type": "progress",
      "content": "Completed tasks: task-planning-skill, gather-goals-types, brainstorming-cleanup. Pending: 3 tasks. Last wave: 1"
    }
  ]
}
```

**After each task completes (per-task verification):**
```
[Task execution completes]
-> Compare implementation against design doc
-> Check for drift
-> If verification PASSES:
   - saveSnapshot() with updated completedTasks list
   - Unlock dependent tasks
   - Proceed to next ready task
-> If verification FAILS:
   - Keep task as in_progress
   - Request fixes before saving
```

**Before batch completion report:**
```
[All ready tasks complete, about to report to user]
-> saveSnapshot()
-> Show progress report with completed tasks
-> Show which tasks are ready next
-> Wait for user feedback
```

**At final completion:**
```
[All tasks complete and verified]
-> saveSnapshot()
-> Show implementation summary
-> Invoke finishing-a-development-branch skill
-> (After finishing-a-development-branch completes: cleanup collab session)
```

## Step 2.5: Per-Task Verification (Collab Workflow)

When within a collab workflow, run verification after each task completes:

**Verification Steps:**
1. After task completion, trigger `verify-phase` hook (if available)
2. Compare task output against design doc specification
3. Check for drift:
   - Are implemented interfaces matching design?
   - Any undocumented additions?
   - Missing components?

**On Verification Success:**
- Mark task as verified
- Update `collab-state.json`: move task from `pendingTasks` to `completedTasks`
- Update `lastActivity` timestamp
- Unlock dependent tasks
- Proceed to next ready tasks

```javascript
FUNCTION markTaskComplete(taskId):
  session = current session name

  // 1. Read current state
  Tool: mcp__plugin_mermaid-collab_mermaid__get_session_state
  Args: { "project": "<cwd>", "session": session }
  Returns: state = { "completedTasks": [...], "pendingTasks": [...], ... }

  // 2. Move task from pending to completed
  newCompleted = [...state.completedTasks, taskId]
  newPending = state.pendingTasks.filter(t => t !== taskId)

  // 3. Update session state via MCP (updates progress bar)
  Tool: mcp__plugin_mermaid-collab_mermaid__update_session_state
  Args: {
    "project": "<cwd>",
    "session": session,
    "completedTasks": newCompleted,
    "pendingTasks": newPending
  }

  // 4. Update task execution diagram (visual progress)
  // Change from executing (blue) to completed (green)
  Tool: mcp__plugin_mermaid-collab_mermaid__patch_diagram
  Args: {
    "project": "<cwd>",
    "session": session,
    "id": "task-execution",
    "old_string": "style {taskId} fill:#bbdefb,stroke:#1976d2,stroke-width:3px",  // executing
    "new_string": "style {taskId} fill:#c8e6c9,stroke:#2e7d32"                    // completed
  }
  // If patch fails (task wasn't marked executing), try from waiting state:
  // old_string: "style {taskId} fill:#e0e0e0,stroke:#9e9e9e"  // waiting
```

**IMPORTANT:** You MUST call `markTaskComplete(taskId)` after each task passes verification. This:
1. Updates the progress bar in the UI (completedTasks/pendingTasks)
2. Updates the task execution diagram (visual green checkmark)

**On Verification Failure:**
- Keep task as `in_progress` (not completed)
- Show drift report with pros/cons
- Ask user: accept drift, reject and fix, or review each
- If drift accepted: update design doc, then unlock dependents
- If drift rejected: fix implementation before proceeding

**Unlocking Dependents:**
```
for each task T where T.depends-on includes completed_task:
  if all(T.depends-on) are completed:
    move T from pending to ready
```

## Step 2.6: Drift Detection

After implementer reports completion, check for drift:

### Step 1: Read design doc and implementation

1. Read design doc:
   Tool: mcp__plugin_mermaid-collab_mermaid__get_document
   Args: { "project": "<cwd>", "session": "<session>", "id": "design" }

2. Read implemented files (from task's file list)

### Step 2: Compare implementation to design

FOR each function/type in the task's Interface section:
  Compare:
    - Function name matches?
    - Parameter names and types match?
    - Return type matches?
    - Logic follows Pseudocode steps?

  IF mismatch found:
    ADD to drift_list: {
      type: "signature" | "logic" | "scope" | "missing",
      design_says: <from design doc>,
      implementation_has: <from code>,
      file: <file path>,
      line: <line number if applicable>
    }

### Step 3: If drift detected, analyze and present

IF drift_list is not empty:
  FOR each drift in drift_list:

    Analyze:
      severity = assess_severity(drift)  // contract vs detail
      intent = assess_intent(drift)      // improvement vs misunderstanding
      precedent = assess_precedent(drift) // will this encourage more drift?
      reversibility = assess_reversibility(drift)

    Generate pros:
      - [benefit of keeping this change]
      - [another benefit if applicable]

    Generate cons:
      - [drawback of keeping this change]
      - [another drawback if applicable]

    Determine recommendation:
      IF drift.type == "signature": recommend = "REJECT"
      ELSE IF drift.type == "logic" AND same_result: recommend = "ACCEPT"
      ELSE IF drift.type == "scope": recommend = "REJECT"
      ELSE IF drift.type == "missing": recommend = "REJECT"

    Present to user:
      ```
      DRIFT DETECTED in task [task-id]:

      ## What Changed
      | Type | Design Says | Implementation Has |
      |------|-------------|-------------------|
      | {drift.type} | {drift.design_says} | {drift.implementation_has} |

      ## Analysis

      **Pros of keeping this change:**
      - {pro1}
      - {pro2}

      **Cons of keeping this change:**
      - {con1}
      - {con2}

      **Suggested choice:** {recommend}
      **Reasoning:** {explanation based on severity, intent, precedent, reversibility}

      ## Your Decision
      1. Reject - revert and re-implement per design
      2. Accept - update design doc to include this change
      3. Discuss - need more context before deciding
      ```

### Step 4: Handle user decision

IF user chooses "Reject":
  - Do NOT mark task as complete
  - Tell implementer to re-implement per design
  - Return to Step 2 (re-execute task)

IF user chooses "Accept":
  - Read current design doc
  - Update relevant section to match implementation
  - Write updated design doc via MCP
  - Log decision in Decision Log section
  - Mark task as complete
  - Proceed to next task

IF user chooses "Discuss":
  - Pause execution
  - Gather more context from user
  - Re-present options after discussion

### Step 5: No drift case

IF drift_list is empty:
  - Mark task as complete
  - Proceed to next task

## Proposing Design Doc Changes

When drift is detected and requires a design doc update, use the proposed tag:

**For section-level changes:**
```markdown
<!-- status: proposed: <drift-description> -->
<new-section-content>
```

**For inline changes:**
```markdown
<!-- propose-start: <drift-description> --><new-text><!-- propose-end -->
```

**Process:**
1. Identify the unique text at the insertion point
2. Use patch to insert proposed content:
   ```
   Tool: mcp__plugin_mermaid-collab_mermaid__patch_document
   Args: {
     "project": "<cwd>",
     "session": "<session>",
     "id": "design",
     "old_string": "<unique text at insertion point>",
     "new_string": "<unique text><!-- propose-start: description --><content><!-- propose-end -->"
   }
   ```
3. If patch fails (not unique), fall back to full update:
   `mcp__plugin_mermaid-collab_mermaid__update_document({ "id": "design", "content": <updated> })`
4. Notify user: "Proposed change visible in design doc (cyan). Accept/reject in mermaid-collab UI."
5. Wait for user decision before proceeding

**After user decision:**
- If accepted: proposed marker removed, content remains -> continue execution
- If rejected: content removed -> address the drift differently or stop
