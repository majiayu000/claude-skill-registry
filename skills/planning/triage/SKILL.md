---
name: triage
description: Triage and categorize findings for the task system
---

## Arguments
[findings list or source type]

- Use tasks-router to select the task system
- Read pending tasks from tasks/ (tasks-file) or `br list --status=open --json` (tasks-beads)

Present all findings, decisions, or issues here one by one for triage. The goal is to go through each item and decide whether to add it to the CLI task system.

**IMPORTANT: DO NOT CODE ANYTHING DURING TRIAGE!**

This command is for:

- Triaging code review findings
- Processing security audit results
- Reviewing performance analysis
- Handling any other categorized findings that need tracking

## Workflow

### Step 0: Select Task System

Use the tasks-router skill to decide whether this repo uses tasks-file or tasks-beads. Follow the corresponding instructions below.

### Step 1: Present Each Finding

For each finding, present in this format:

```
---
Issue #X: [Brief Title]

Severity: 🔴 P1 (CRITICAL) / 🟡 P2 (IMPORTANT) / 🔵 P3 (NICE-TO-HAVE)

Category: [Security/Performance/Architecture/Bug/Feature/etc.]

Description:
[Detailed explanation of the issue or improvement]

Location: [file_path:line_number]

Problem Scenario:
[Step by step what's wrong or could happen]

Proposed Solution:
[How to fix it]

Estimated Effort: [Small (< 2 hours) / Medium (2-8 hours) / Large (> 8 hours)]

---
Do you want to add this to the task list?
1. yes - create task file
2. next - skip this item
3. custom - modify before creating
```

### Step 2: Handle User Decision

**When user says "yes":**

First, use tasks-router to select tasks-file or tasks-beads.

**If tasks-beads:**

1. If task already exists:
   - Update priority and add labels: `br update <id> --priority=P1 --add-label "ready" --add-label "<category>" --json`
   - Update type if needed: `br update <id> --type=bug|feature|docs|question|epic|task --json`
   - Add recommended action to notes: `br update <id> --notes "## Recommended Action\n..." --json`
   - Update acceptance criteria: `br update <id> --acceptance-criteria "- [ ] ..." --json`
   - Set effort estimate if known: `br update <id> --estimate=120 --json`
2. If creating a new task:
   - Create issue: `br create --title="..." --type=... --priority=P1 --description="Problem statement" --json`
   - Add design (solutions/technical): `br update <id> --design "## Proposed Solutions\n..." --json`
   - Add notes (findings/resources): `br update <id> --notes "## Findings\n..." --json`
   - Add acceptance criteria: `br update <id> --acceptance-criteria "- [ ] ..." --json`
3. Add triage approval comment:
   - `br comments add <id> --message "Approved during triage. Ready for work." --json`
4. Confirm approval: "✅ Approved: Issue #<id> - Status: **open** (label: ready)"

Field mapping: `description`=problem, `design`=solutions/technical, `notes`=findings/resources/recommended action, `acceptance_criteria`=done criteria

Priority mapping for tasks-beads:

- 🔴 P1 (CRITICAL) -> `P1`
- 🟡 P2 (IMPORTANT) -> `P2`
- 🔵 P3 (NICE-TO-HAVE) -> `P3`

**If tasks-file:**

1. **Update existing task file** (if it exists) or **Create new filename:**

   If task already exists (from code review):

   - Rename file from `{id}-pending-{priority}-{desc}.md` → `{id}-ready-{priority}-{desc}.md`
   - Update YAML frontmatter: `status: pending` → `status: ready`
   - Keep issue_id, priority, and description unchanged

   If creating new task:

   ```
   {next_id}-ready-{priority}-{brief-description}.md
   ```

   Priority mapping:

   - 🔴 P1 (CRITICAL) → `p1`
   - 🟡 P2 (IMPORTANT) → `p2`
   - 🔵 P3 (NICE-TO-HAVE) → `p3`

   Example: `042-ready-p1-transaction-boundaries.md`

2. **Update YAML frontmatter:**

   ```yaml
   ---
   status: ready # IMPORTANT: Change from "pending" to "ready"
   priority: p1 # or p2, p3 based on severity
   issue_id: "042"
   tags: [category, relevant-tags]
   dependencies: []
   ---
   ```

3. **Populate or update the file:**

   ```yaml
   # [Issue Title]

   ## Problem Statement
   [Description from finding]

   ## Findings
   - [Key discoveries]
   - Location: [file_path:line_number]
   - [Scenario details]

   ## Proposed Solutions

   ### Option 1: [Primary solution]
   - **Pros**: [Benefits]
   - **Cons**: [Drawbacks if any]
   - **Effort**: [Small/Medium/Large]
   - **Risk**: [Low/Medium/High]

   ## Recommended Action
   [Filled during triage - specific action plan]

   ## Technical Details
   - **Affected Files**: [List files]
   - **Related Components**: [Components affected]
   - **Database Changes**: [Yes/No - describe if yes]

   ## Resources
   - Original finding: [Source of this issue]
   - Related issues: [If any]

   ## Acceptance Criteria
   - [ ] [Specific success criteria]
   - [ ] Tests pass
   - [ ] Code reviewed

   ## Work Log

   ### {date} - Approved for Work
   **By:** Claude Triage System
   **Actions:**
   - Issue approved during triage session
   - Status changed from pending → ready
   - Ready to be picked up and worked on

   **Learnings:**
   - [Context and insights]

   ## Notes
   Source: Triage session on {date}
   ```

4. **Confirm approval:** "✅ Approved: `{new_filename}` (Issue #{issue_id}) - Status: **ready** → Ready to work on"

**When user says "next":**

- If tasks-file: delete the task file from tasks/ directory
- If tasks-beads: close the issue with a reason, for example `br close <id> --reason="Not pursuing" --json`
- Skip to the next item
- Track skipped items for summary

**When user says "custom":**

- Ask what to modify (priority, description, details)
- Update the information
- Present revised version
- Ask again: yes/next/custom

### Step 3: Continue Until All Processed

- Process all items one by one
- Track using TodoWrite for visibility
- Don't wait for approval between items - keep moving

### Step 4: Final Summary

After all items processed:

````markdown
## Triage Complete

**Total Items:** [X] **Tasks Approved (ready):** [Y] **Skipped:** [Z]

### Approved Tasks (Ready for Work):

- `042-ready-p1-transaction-boundaries.md` - Transaction boundary issue (tasks-file)
- Issue #42 - Transaction boundary issue (tasks-beads)

### Skipped Items (Deleted):

- Item #5: [reason] - Removed from tasks/ (tasks-file)
- Item #12: [reason] - Closed issue (tasks-beads)

### Summary of Changes Made:

During triage, the following status updates occurred:

- **Pending → Ready (tasks-file):** Filenames and frontmatter updated to reflect approved status
- **Open + ready label (tasks-beads):** Issues labeled ready with updated notes and acceptance criteria
- **Deleted/Closed:** Task files removed (tasks-file) or issues closed (tasks-beads)

### Next Steps:

1. View approved tasks ready for work:
   ```bash
   ls tasks/*-ready-*.md          # tasks-file
   br ready --json                # tasks-beads
   ```
````

2. Start work on approved items:

   ```bash
   /resolve_task_parallel  # Work on multiple approved items efficiently
   ```

3. Or pick individual items to work on

4. As you work, update task status:
   - If tasks-file: rename `ready → complete`, update frontmatter
   - If tasks-beads: claim before starting: `br update <id> --claim --json`, then close when done: `br close <id> --reason="Completed" --json`

```

## Example Response Format

```

---

Issue #5: Missing Transaction Boundaries for Multi-Step Operations

Severity: 🔴 P1 (CRITICAL)

Category: Data Integrity / Security

Description: The google_oauth2_connected callback in GoogleOauthCallbacks concern performs multiple database operations without transaction protection. If any step fails midway, the database is left in an inconsistent state.

Location: app/controllers/concerns/google_oauth_callbacks.rb:13-50

Problem Scenario:

1. User.update succeeds (email changed)
2. Account.save! fails (validation error)
3. Result: User has changed email but no associated Account
4. Next login attempt fails completely

Operations Without Transaction:

- User confirmation (line 13)
- Waitlist removal (line 14)
- User profile update (line 21-23)
- Account creation (line 28-37)
- Avatar attachment (line 39-45)
- Journey creation (line 47)

Proposed Solution: Wrap all operations in ApplicationRecord.transaction do ... end block

Estimated Effort: Small (30 minutes)

---

Do you want to add this to the task list?

1. yes - create task file
2. next - skip this item
3. custom - modify before creating

```

## Important Implementation Details

### Status Transitions During Triage

**When "yes" is selected:**
1. Rename file: `{id}-pending-{priority}-{desc}.md` → `{id}-ready-{priority}-{desc}.md`
2. Update YAML frontmatter: `status: pending` → `status: ready`
3. Update Work Log with triage approval entry
4. Confirm: "✅ Approved: `{filename}` (Issue #{issue_id}) - Status: **ready**"

**When "next" is selected:**
1. Delete the task file from tasks/ directory
2. Skip to next item
3. No file remains in the system

**When using tasks-beads:**
1. Approve: `br update <id> --add-label "ready" --priority=P1 --json`
2. Add recommended action: `br update <id> --notes "## Recommended Action\n..." --json`
3. Work log: `br comments add <id> --message "Approved during triage. Ready for work." --json`
4. Skip: `br close <id> --reason="Not pursuing" --json`

### Progress Tracking

Every time you present a task as a header, include:
- **Progress:** X/Y completed (e.g., "3/10 completed")
- **Estimated time remaining:** Based on how quickly you're progressing
- **Pacing:** Monitor time per finding and adjust estimate accordingly

Example:
```

Progress: 3/10 completed | Estimated time: ~2 minutes remaining

```

### Do Not Code During Triage

- ✅ Present findings
- ✅ Make yes/next/custom decisions
- ✅ Update task files (rename, frontmatter, work log)
- ❌ Do NOT implement fixes or write code
- ❌ Do NOT add detailed implementation details
- ❌ That's for /resolve_task_parallel phase
```

When done give these options

```markdown
What would you like to do next?

1. run /resolve_task_parallel to resolve the tasks
2. commit the tasks
3. nothing, go chill
```
