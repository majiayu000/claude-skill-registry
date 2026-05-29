---
name: task-status-sync
description: Enforce atomic task status updates through task-tracker commands only. Prevent manual edits to NOTES.md and tasks.md that break synchronization. Auto-trigger when detecting Edit/Write attempts to task files, task completion mentions, or status update discussions. Auto-convert manual edit attempts to equivalent task-tracker commands. Validate task-tracker usage and auto-fix common mistakes.
---

<objective>
Maintain atomic synchronization between tasks.md checkboxes and NOTES.md completion markers by enforcing task-tracker command usage and preventing manual file edits that cause data inconsistencies.
</objective>

<quick_start>
<enforcement_model>
**Intercept and convert manual edits to task-tracker commands:**

1. **Detect attempt**: Monitor for Edit/Write tool usage on NOTES.md or tasks.md
2. **Extract intent**: Parse what change the user/Claude wants to make
3. **Convert to command**: Generate equivalent task-tracker command
4. **Execute atomically**: Run task-tracker to update both files simultaneously
5. **Provide feedback**: Explain the conversion and show the result

**Example workflow:**
```
User: "Mark T001 as completed"

❌ BLOCKED: Direct edit to tasks.md
✅ AUTO-CONVERTED: .spec-flow/scripts/bash/task-tracker.sh mark-done-with-notes -TaskId T001

Result:
- tasks.md: - [X] T001 Create database schema
- NOTES.md: ✅ T001: Create database schema - est (2025-11-19 10:30)
```
</enforcement_model>

<allowed_operations>
**✅ Permitted (read-only):**
- Read NOTES.md to understand progress
- Read tasks.md to see task list
- Read error-log.md to diagnose failures

**✅ Permitted (through task-tracker):**
- Mark tasks complete: `mark-done-with-notes`
- Mark tasks in progress: `mark-in-progress`
- Mark tasks failed: `mark-failed`
- Sync status: `sync-status`
- Get next task: `next`
- Get summary: `summary`
- Validate: `validate`

**❌ Blocked (auto-converted):**
- Direct Edit/Write to tasks.md
- Direct Edit/Write to NOTES.md
- Manual checkbox changes ([ ] → [X])
- Manual completion markers (✅ T001)
</allowed_operations>

<task_tracker_commands>
**Available task-tracker.sh / task-tracker.ps1 actions:**

```bash
# Get current status
.spec-flow/scripts/bash/task-tracker.sh status -Json

# Mark task completed with full details
.spec-flow/scripts/bash/task-tracker.sh mark-done-with-notes \
  -TaskId T001 \
  -Notes "Created Message model with validation" \
  -Evidence "pytest: 25/25 passing" \
  -Coverage "92% (+8%)" \
  -CommitHash "abc123" \
  -Duration "15min"

# Mark task in progress
.spec-flow/scripts/bash/task-tracker.sh mark-in-progress -TaskId T002

# Mark task failed
.spec-flow/scripts/bash/task-tracker.sh mark-failed \
  -TaskId T003 \
  -ErrorMessage "Tests failing: ImportError on MessageService"

# Sync tasks.md to NOTES.md (migration utility)
.spec-flow/scripts/bash/task-tracker.sh sync-status

# Get next available task
.spec-flow/scripts/bash/task-tracker.sh next -Json

# Get phase-wise summary
.spec-flow/scripts/bash/task-tracker.sh summary -Json

# Validate task file structure
.spec-flow/scripts/bash/task-tracker.sh validate -Json
```

See [references/task-tracker-api.md](references/task-tracker-api.md) for complete API reference.
</task_tracker_commands>
</quick_start>

<workflow>
<detection_phase>
**1. Monitor Tool Usage**

Watch for these patterns that indicate task status updates:

**Direct file edits:**
- `Edit(file_path: "*/tasks.md", ...)`
- `Edit(file_path: "*/NOTES.md", ...)`
- `Write(file_path: "*/tasks.md", ...)`
- `Write(file_path: "*/NOTES.md", ...)`

**Verbal indicators:**
- "Mark T001 as complete"
- "Update task status for T002"
- "Task T003 is done"
- "Completed T004"
- "T005 failed"

**Checkbox change patterns:**
- `old_string: "- [ ] T001"` → `new_string: "- [X] T001"`
- Adding ✅ markers to NOTES.md manually
</detection_phase>

<interception_phase>
**2. Intercept and Block Manual Edits**

When Edit/Write detected on tasks.md or NOTES.md:

```
⛔ MANUAL EDIT BLOCKED

File: specs/001-feature/tasks.md
Attempted change: Mark T001 as [X] completed

❌ Reason: Manual edits break atomic sync between tasks.md and NOTES.md

✅ Solution: Use task-tracker command instead

Auto-converting to:
  .spec-flow/scripts/bash/task-tracker.sh mark-done-with-notes -TaskId T001

This atomically updates:
  - tasks.md checkbox: - [X] T001
  - NOTES.md marker: ✅ T001: ... - est (2025-11-19 10:30)
  - Progress summary in tasks.md (if update-tasks-summary.ps1 exists)
```

Do NOT execute the manual edit. Instead, proceed to conversion phase.
</interception_phase>

<conversion_phase>
**3. Convert Manual Edit to Task-Tracker Command**

**Parse the intended change:**

Extract from Edit/Write tool parameters:
- `TaskId`: T### from checkbox pattern or ✅ marker
- `NewStatus`: Infer from checkbox ([X] = completed, [~] = in-progress, [ ] = pending)
- `Notes`: Extract from NOTES.md addition or Edit context
- `ErrorMessage`: Extract if marking failed

**Generate equivalent command:**

```javascript
// Pseudo-logic
if (newStatus === 'X' || intent === 'mark complete') {
  command = 'mark-done-with-notes'
  params = {
    TaskId: extractedTaskId,
    Notes: extractedNotes || "",
    Duration: "est"  // Default if not specified
  }
}
else if (newStatus === '~' || intent === 'mark in progress') {
  command = 'mark-in-progress'
  params = { TaskId: extractedTaskId }
}
else if (intent === 'mark failed' || errorMessage present) {
  command = 'mark-failed'
  params = {
    TaskId: extractedTaskId,
    ErrorMessage: extractedErrorMessage
  }
}
```

**Validation before execution:**

Check that:
- TaskId exists in tasks.md
- Status transition is valid (pending → in-progress → completed)
- Required fields present (e.g., ErrorMessage for mark-failed)

If validation fails, auto-fix where possible:
- Missing TaskId → Extract from context or ask user
- Invalid transition → Warn and suggest correct flow
- Missing ErrorMessage → Prompt for details

See [references/conversion-logic.md](references/conversion-logic.md) for detailed conversion rules.
</conversion_phase>

<execution_phase>
**4. Execute Task-Tracker Command**

```bash
# Platform detection
if (platform === 'win32') {
  script = '.spec-flow/scripts/bash/task-tracker.sh'  # Uses WSL or delegates to PS
} else if (platform === 'linux' || platform === 'darwin') {
  script = '.spec-flow/scripts/bash/task-tracker.sh'
}

# Execute with Bash tool
Bash(`${script} ${command} -TaskId ${TaskId} [additional params] -Json`)
```

**Parse JSON output:**

```json
{
  "Success": true,
  "TaskId": "T001",
  "Message": "Task T001 marked complete in both tasks.md and NOTES.md",
  "TasksFile": "specs/001-feature/tasks.md",
  "NotesFile": "specs/001-feature/NOTES.md",
  "PhaseMarker": "[RED]"
}
```

**Provide feedback:**

```
✅ TASK STATUS UPDATED ATOMICALLY

Task T001 marked complete:
  - tasks.md: Updated checkbox to [X]
  - NOTES.md: Added completion marker
  - Phase: [RED] (TDD red phase)

Files synchronized:
  - specs/001-feature/tasks.md
  - specs/001-feature/NOTES.md

Next steps:
  - Run: task-tracker.sh next
  - Continue with T002
```
</execution_phase>

<validation_phase>
**5. Validate Task-Tracker Usage**

**Common mistakes to auto-fix:**

| Mistake | Detection | Auto-fix |
|---------|-----------|----------|
| Wrong TaskId format (T1 instead of T001) | Regex: `^T\d{1,2}$` | Pad with zeros: T001 |
| Invalid status transition (pending → completed) | Check current status | Insert mark-in-progress first |
| Missing duration | Duration field empty | Default to "est" |
| Missing notes on completion | Notes empty for mark-done-with-notes | Prompt: "Add implementation summary" |
| TaskId doesn't exist | Not found in Parse-TasksFile | List available task IDs |
| Marking already-completed task | IsCompleted = true | Warn: "Already complete, skip or force?" |

**TDD validation:**

Check if test task completed before implementation:
- If marking T002 (implement) complete but T001 (test) is pending → warn
- Recommendation: "Complete T001 (test) before T002 (implement) for TDD"

**Parallel safety:**

- If more than 2 tasks in-progress → warn: "Exceeds parallel limit (2)"
- If file path conflicts detected → block: "T002 and T003 both modify `app.py`"

See [references/validation-rules.md](references/validation-rules.md) for complete validation logic.
</validation_phase>
</workflow>

<anti_patterns>
**Avoid these mistakes that break sync:**

**1. Manual checkbox edits**
```markdown
❌ BAD (manual edit to tasks.md):
- [X] T001 Create database schema

✅ GOOD (task-tracker command):
task-tracker.sh mark-done-with-notes -TaskId T001 -Notes "Created schema"
```

**2. Adding NOTES.md markers manually**
```markdown
❌ BAD (manual edit to NOTES.md):
✅ T001: Created database schema

✅ GOOD (task-tracker handles NOTES.md):
task-tracker.sh mark-done-with-notes -TaskId T001
# Atomically updates both files
```

**3. Inconsistent states**
```markdown
❌ BAD (tasks.md says pending, NOTES.md says complete):
tasks.md: - [ ] T001 Create schema
NOTES.md: ✅ T001: Created schema

✅ GOOD (atomic update ensures consistency):
Both files updated simultaneously via task-tracker
```

**4. Skipping in-progress marker**
```markdown
❌ BAD (pending → completed without in-progress):
Can lose tracking of what's actively being worked on

✅ GOOD (mark in-progress first):
1. task-tracker.sh mark-in-progress -TaskId T001
2. [implement task]
3. task-tracker.sh mark-done-with-notes -TaskId T001
```

**5. Missing task completion evidence**
```markdown
❌ BAD (no evidence of completion):
✅ T001 - est (timestamp)

✅ GOOD (include evidence, coverage, commit):
✅ T001: Created Message model - 15min (2025-11-19 10:30)
  - Evidence: pytest: 25/25 passing
  - Coverage: 92% (+8%)
  - Committed: abc123
```
</anti_patterns>

<success_criteria>
**Task status sync is working correctly when:**

- ✓ All task completions use task-tracker commands
- ✓ tasks.md checkboxes and NOTES.md markers are always synchronized
- ✓ No manual edits to tasks.md or NOTES.md occur
- ✓ Attempted manual edits are auto-converted to task-tracker commands
- ✓ Task-tracker validation catches and fixes common mistakes
- ✓ TDD flow is enforced (tests before implementation)
- ✓ Parallel task limit (2) is respected
- ✓ File path conflicts are detected and prevented
- ✓ Error log entries are created for failed tasks
- ✓ Progress summary stays updated with velocity metrics

**Detection working when:**
- Edit/Write attempts to tasks.md are intercepted
- Verbal task completion mentions are recognized
- Checkbox change patterns are detected
- Auto-conversion generates correct task-tracker commands

**Validation working when:**
- Invalid task IDs are caught and corrected
- Invalid status transitions are prevented or guided
- TDD violations are warned
- Parallel safety limits are enforced
</success_criteria>

<reference_guides>
For detailed implementation and troubleshooting:

- **[references/task-tracker-api.md](references/task-tracker-api.md)** - Complete task-tracker command reference with examples
- **[references/conversion-logic.md](references/conversion-logic.md)** - Manual edit → task-tracker command conversion rules
- **[references/validation-rules.md](references/validation-rules.md)** - Task status validation and auto-fix logic
- **[references/file-formats.md](references/file-formats.md)** - tasks.md and NOTES.md structure and patterns
</reference_guides>
