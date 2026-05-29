---
name: tasks
description: Extract tasks from input or manage existing tasks. Handles "Extract tasks", "What's on my plate?", "Show my tasks", "Mark [task] as done". Duplicate checking, accountability test, and triage.
user-invocable: true
help:
  purpose: |-
    Task extraction from conversations and task management workflows.
  use_cases:
    - "Extract tasks from this"
    - "What's on my plate?"
    - "Show my tasks"
    - "Mark [task] as done"
  scope: tasks,action-items,commitments
---

# Tasks skill

Extract commitments into actionable tasks, or manage existing tasks with duplicate checking, accountability validation, and intelligent triage.

---

## Mode detection

This skill operates in two modes depending on user intent:

1. **Extract Mode**: User provides input (transcript, email, notes) and requests task extraction
2. **Manage Mode**: User requests task review, prioritization, completion, or backlog pruning

---

## EXTRACT MODE

Convert loose commitments into actionable, accountable tasks with duplicate checking and proper placement.

---

### Step 1: Load replacements (MANDATORY)

Read `reference/replacements.md`. Ensure ALL owners are mapped to canonical names.

---

### Step 2: Extract candidates and filter

Scan input for commitments:
- "I will...", "Can you...", "Let's...", "Action item:", "Need to..."

Apply accountability test. Discard failures:
- NEVER create tasks for "Team" or "We" without a specific lead
- Tasks must have a clear owner
- Tasks must be actionable and specific

---

### Step 3: Resolve metadata

For each passing task:

| Field | Logic |
|-------|-------|
| `due` | Map relative dates to YYYY-MM-DD using date resolution table. Default to `backlog`. |
| `source` | `journal/YYYY-MM/YYYY-MM-DD-slug` (if meeting), `email`, or `direct` |
| `created` | Today's date (YYYY-MM-DD) |
| `initiative` | Extract if related to known initiative |
| `owner` | Canonical name of responsible person |

**Date resolution table:**
- "today" -> YYYY-MM-DD (current date)
- "tomorrow" -> YYYY-MM-DD (current date + 1)
- "next week" -> YYYY-MM-DD (current date + 7)
- "end of month" -> YYYY-MM-DD (last day of current month)
- "next [day]" (e.g., "next Friday") -> YYYY-MM-DD (first occurrence of that day after today)
- No date specified -> `backlog`

---

### Step 4: Check duplicates

Read `reference/integrations.md` Tasks section for provider details. Execute the `list` operation for all configured lists (default: Active, Delegated, Backlog).

Compare by title and owner (from notes field). If a similar task exists for the same owner:
- Skip if identical (already exists)
- Execute the `edit` operation to update if new details or deadline

---

### Step 5: Placement logic

Use these rules to determine destination list:
- Has due date + owner is user -> `Active` list
- Has due date + owner is other -> `Delegated` list
- No due date -> `Backlog` list

---

### Step 6: Create tasks

Create tasks directly via the task integration. Do not ask for permission. Read `reference/integrations.md` Tasks section for the provider-specific command format.

Standard task creation fields:
```
title: "Task description"
list: Active
due: YYYY-MM-DD
notes: |
  source: journal/YYYY-MM/YYYY-MM-DD-slug.md
  created: YYYY-MM-DD
  initiative: [[Initiative Name]]
  owner: Name
```

For EACH task:
1. Execute the `create_reminder` operation
2. Check the tool response. If the response indicates an error or does not confirm creation, add the task to the errors list and continue with the next task.
3. Only count a task as "created" if the tool response confirms success.

---

### Step 7: Verify task creation (MANDATORY)

After all creation attempts, execute `list_reminders` for each list that received new tasks. Confirm each created task appears in the list by matching title.

If any tasks are missing from the list despite a successful creation response:
- Add them to a "creation_unverified" section in the output
- Report the discrepancy to the user

NEVER report a task as "Created" in the output table unless it was confirmed present in the verification query.

---

### Extract mode output

```markdown
---
## Task extraction complete

### Created tasks (X total, Y verified)
| Task | Owner | List | Due | Source | Verified |
|------|-------|------|-----|--------|----------|
| Task description | Name | Active/Delegated/Backlog | YYYY-MM-DD | source | yes/no |

### Creation unverified
| Task | Owner | List | Issue |
|------|-------|------|-------|
| Task description | Name | Active | Not found in list after creation |

### Duplicates skipped
| Task | Owner | Reason |
|------|-------|--------|
| Task description | Name | Already exists as matching task |

### Unactionable items
| Item | Reason |
|------|--------|
| Description | Why it was skipped |
```

---

## MANAGE MODE

Review, prioritize, complete, and prune existing tasks via the task integration.

---

### Step 1: Load task state

Read `reference/integrations.md` Tasks section for provider details. Execute the `list` operation for all configured lists (default: Active, Delegated, Backlog).

---

### Step 2: Present current state

Group tasks by list and display to user:

```markdown
## Current task state

### Active (X tasks)
| Task | Owner | Due |
|------|-------|-----|
| Task description | Name | YYYY-MM-DD |

### Delegated (Y tasks)
| Task | Owner | Due |
|------|-------|-----|
| Task description | Name | YYYY-MM-DD |

### Backlog (Z tasks)
| Task | Owner | Age |
|------|-------|-----|
| Task description | Name | X days old |
```

---

### Step 3: Handle user actions

**For completion:**
- Execute the `complete` operation only AFTER user confirmation
- Record which user marked it complete and timestamp

**For reprioritization:**
- Execute the `edit` operation to update due date or move between lists
- Update the `modified` field in notes

**For backlog pruning:**
- Flag items with `created` date older than 90 days in notes field
- Ask user for confirmation before deleting or archiving
- Suggest moving to archive or backlog-archive list if available

---

### Step 4: Duplicate detection (opportunistic)

While reviewing, note any potential duplicates:
- Same task title, different owners
- Similar descriptions across multiple lists
- Tasks that should be consolidated

Suggest consolidation but allow user to decide.

---

### Manage mode output

```markdown
---
## Task management update

### Completed
| Task | Owner | Status |
|------|-------|--------|
| Task description | Name | Marked done |

### Reprioritized
| Task | Owner | From | To | Change |
|------|-------|------|-----|--------|
| Task description | Name | Backlog | Active | New due date: YYYY-MM-DD |

### Pruning recommendations
| Task | Owner | Age | Recommendation |
|------|-------|-----|-----------------|
| Task description | Name | X days | Archive or delete |

### Current summary
- Active: X tasks
- Delegated: Y tasks
- Backlog: Z tasks (W tasks >90 days old)
```

---

## Context budget

- Tasks: Execute task integration `list` operation for all configured lists
- Reference: `reference/replacements.md` (mandatory)

---

## Absolute constraints

Universal constraints from the core skill apply (date resolution, name normalization, task verification, no deletion without instruction). Additionally:

- NEVER create tasks for "Team" or "We" without a specific lead
- NEVER mark tasks done without user confirmation
- ONLY write to Active, Delegated, Backlog lists (person-named lists are read-only)
