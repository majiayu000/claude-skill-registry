---
name: task
description: Quick task creation for MASTER_PLAN.md with auto-generated IDs. This skill should be used when the user wants to add a new task, bug, feature, or inquiry to the project's master plan. Triggers on "/task", "add task", "new task", "create task", "track this", "investigate".
---

# Task Creator

Quickly add new tasks to `docs/MASTER_PLAN.md` with automatic ID generation.

## Workflow

### Step 1: Generate and Announce Task ID (FIRST!)

**CRITICAL**: Before doing ANYTHING else, run the ID generator and tell the user:

```bash
node ./scripts/utils/get-next-task-id.cjs
```

**Immediately output to user:**
```
Using task number: [ID]
```

This must happen BEFORE asking any questions or gathering details.

### Step 2: Gather Task Information

Use `AskUserQuestion` tool to collect task details in a SINGLE question with multiple parts:

**Questions to ask:**

1. **Task Type** (header: "Type")
   - `TASK` - New feature or improvement
   - `BUG` - Bug fix
   - `FEATURE` - Major new feature
   - `INQUIRY` - Investigation to understand behavior, errors, or unexpected results (not a bug fix)

2. **Priority** (header: "Priority")
   - `P0` - Critical/Blocker
   - `P1` - High priority
   - `P2` - Medium priority (Recommended)
   - `P3` - Low priority

Then ask for the task title and optional description via the "Other" free-text option or follow-up.

### Step 3: Add to MASTER_PLAN.md

Read `docs/MASTER_PLAN.md` and insert the new task in the Roadmap table:

```markdown
| **[TYPE]-[ID]** | **[Title]** | **[Priority]** | IN PROGRESS | [Dependencies or -] |
```

**Example:**
```markdown
| **TASK-301** | **Implement Dark Mode Toggle** | **P2** | IN PROGRESS | - |
```

### Step 4: Add Active Work Section (P0/P1 only)

For P0 or P1 tasks, also add under "## Active Work (Summary)":

```markdown
### [TYPE]-[ID]: [Title] (IN PROGRESS)
**Priority**: [Priority]
**Status**: IN PROGRESS (YYYY-MM-DD)

[Description from user]

**Tasks**:
- [ ] [First step]
- [ ] [Additional steps as needed]
```

### Step 5: Confirm

Report to user:
```
Task added to MASTER_PLAN.md:
- ID: [TYPE]-[ID]
- Title: [Title]
- Priority: [Priority]
- Status: IN PROGRESS

Ready to begin work.
```

## Important Rules

- **NEVER reuse existing task IDs** - Always run get-next-task-id.cjs first
- **Use strikethrough** (~~ID~~) only when marking tasks DONE
- **Keep titles concise** - Under 50 characters when possible
- **P0 tasks always need** an Active Work section
