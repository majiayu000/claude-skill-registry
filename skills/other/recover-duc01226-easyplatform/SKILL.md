---
name: recover
version: 1.0.0
description: '[Utilities] Restore workflow context from checkpoint after session loss'
activation: user-invoked
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Restore workflow state and todo items from checkpoint files after context loss or session interruption.

**Workflow:**

1. **Find Checkpoint** — Locate latest `memory-checkpoint-*.md` in reports directory
2. **Read Metadata** — Extract JSON block with session ID, active plan, current step, pending todos
3. **Restore Todos** — Immediately call TaskCreate with pending items from checkpoint
4. **Resume Workflow** — Continue from the interrupted step using restored context

**Key Rules:**

- Always restore TaskCreate items before resuming any work
- Check both `plans/reports/` and plan-specific report directories
- Use timestamp to find the checkpoint closest to the interruption

# Recover Workflow Context

Restore workflow state and todo items from checkpoint files after context compaction or session loss.

## Usage

Use this command when:

- Context was compacted and you've lost track of the workflow
- Session was interrupted and needs to resume
- Todo items need to be restored from a checkpoint
- The automatic recovery didn't trigger

## Recovery Process

### Step 1: Find Latest Checkpoint

Look for checkpoint files in the reports directory:

```bash
ls -la plans/reports/memory-checkpoint-*.md | tail -5
```

Or search for all recent checkpoints:

```bash
find plans -name "memory-checkpoint-*.md" -mmin -60 | head -5
```

### Step 2: Read Checkpoint File

Read the most recent checkpoint to understand the saved state:

```
Read the checkpoint file at: plans/reports/memory-checkpoint-YYMMDD-HHMMSS.md
```

### Step 3: Extract Recovery Metadata

The checkpoint file contains a JSON metadata block at the end:

```json
{
  "sessionId": "...",
  "activePlan": "plans/YYMMDD-slug/",
  "workflowType": "feature",
  "currentStep": "cook",
  "remainingSteps": ["test", "code-review"],
  "pendingTodos": [...]
}
```

### Step 4: Restore Todo Items

**IMMEDIATELY call TaskCreate** with the pending todos from the checkpoint:

```json
[
    { "content": "[Workflow] /cook - Implement", "status": "in_progress", "activeForm": "Executing /cook" },
    { "content": "[Workflow] /test - Run tests", "status": "pending", "activeForm": "Executing /test" },
    { "content": "[Workflow] /code-review - Review code", "status": "pending", "activeForm": "Executing /code-review" }
]
```

### Step 5: Read Active Plan (if exists)

If `activePlan` is set in the metadata, read the plan file:

```
Read: {activePlan}/plan.md
```

### Step 6: Continue Workflow

Resume from the `currentStep` identified in the metadata. Execute the remaining workflow steps in order.

## Recovery Checklist

- [ ] Located most recent checkpoint file
- [ ] Read checkpoint content
- [ ] Extracted recovery metadata JSON
- [ ] Restored todo items via TaskCreate
- [ ] Read active plan (if applicable)
- [ ] Identified current workflow step
- [ ] Ready to continue from interrupted step

## Automatic vs Manual Recovery

| Scenario                      | Recovery Type | Trigger                          |
| ----------------------------- | ------------- | -------------------------------- |
| Session resume after compact  | Automatic     | `post-compact-recovery.cjs` hook |
| New session in same directory | Manual        | This `/recover` command          |
| Explicit user request         | Manual        | This `/recover` command          |
| No workflow state found       | Manual        | This `/recover` command          |

## Checkpoint Locations

Checkpoints are saved to different locations based on context:

1. **Active plan exists:** `{plan-path}/reports/memory-checkpoint-*.md`
2. **No active plan:** `plans/reports/memory-checkpoint-*.md`

## Tips

1. **Check multiple locations** - Plans may have their own reports directories
2. **Use timestamp** - Checkpoints are timestamped, find the one closest to when you were working
3. **Verify todo status** - Compare checkpoint todos with current TaskCreate state
4. **Read incrementally** - Don't try to restore everything at once

## Related Commands

- `/checkpoint` - Create a manual checkpoint (before expected loss)
- `/compact` - Manually trigger context compaction
- `/context` - Load project context
- `/watzup` - Generate progress summary

## Example Recovery Flow

```
User: /recover

Claude: Let me find and restore your workflow context.

1. Finding latest checkpoint...
   Found: plans/reports/memory-checkpoint-260110-143025.md

2. Reading checkpoint metadata...
   - Workflow: feature
   - Current step: /cook
   - Remaining: /test, /code-review
   - Active plan: plans/260110-1430-new-feature/

3. Restoring TaskCreate items...
   [Calling TaskCreate with 3 pending items]

4. Reading active plan...
   [Reading plans/260110-1430-new-feature/plan.md]

5. Ready to continue from /cook step.
   Shall I proceed with the implementation?
```

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
