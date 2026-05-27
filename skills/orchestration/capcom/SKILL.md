---
name: capcom
description: "Check mission status and progress via fresh subagent. Queries Beads for features, tasks, bugs, and recent work activity. Keeps HOUSTON context lean."
---

# /capcom - Status Check

Check current status and progress using Beads. Spawns a fresh subagent to do the heavy lifting, keeping HOUSTON's context lean.

---

## Instructions

When the user runs `/capcom`, spawn a Task agent to gather and format status:

### Step 1: Spawn CAPCOM Subagent

Use the Task tool with subagent_type `general-purpose`:

```
You are a CAPCOM status agent for Space-Agents.

TASK: Query the current state using Beads and return a formatted status report.

Run these Beads commands:

1. Statistics overview:
   bd stats

2. Features (in_progress first, then open):
   bd list -t feature --status in_progress
   bd list -t feature --status open

3. Tasks by status:
   bd list -t task --status in_progress
   bd list -t task --status open

4. Open bugs:
   bd list -t bug --status open

5. Blocked issues:
   bd blocked

6. Dependency tree (full structure):
   bd list --tree

7. Recent work activity (check comments on in_progress issues):
   For each in_progress issue, run: bd comments {issue-id}
   Filter comments containing [ATTEMPT], [PROGRESS], [BLOCKED], or [HANDOVER] titles

FORMAT your response as:

[CAPCOM_REPORT]

STATISTICS
─────────────────
[bd stats summary]

FEATURES
─────────────────
[In Progress]
{list in_progress features with status indicator}

[Open]
{list open features with priority}

TASKS
─────────────────
[In Progress]
{list in_progress tasks}

[Open/Ready]
{list open tasks}

BUGS
─────────────────
{list open bugs by priority}

BLOCKED
─────────────────
{list blocked issues with what blocks them}

DEPENDENCY TREE
─────────────────
{bd list --tree output}

RECENT ACTIVITY
─────────────────
{Recent [ATTEMPT], [PROGRESS], [BLOCKED] comments from active work}

End with [CAPCOM_COMPLETE]
```

### Step 2: Display and Highlight

Display subagent report. Emphasize blocked issues and critical bugs.

---

## Example Output

```
CAPCOM STATUS REPORT
────────────────────
STATISTICS: 25 issues (13 open, 2 in_progress, 5 blocked)

FEATURES [In Progress]
◐ space-agents-1.1: Execution Flow Skills (P1)

TASKS [In Progress]
◐ space-agents-1.1.3: Update /capcom...

BLOCKED
● space-agents-1.3.2 ← space-agents-1.3.1

DEPENDENCY TREE
[bd list --tree output]

RECENT ACTIVITY
[PROGRESS] space-agents-1.1.3 (10m): Updated skill...
────────────────────
HOUSTON standing by.
```

---

## Optional Filters

- `/capcom bugs` - Show only bugs
- `/capcom blocked` - Show only blocked issues
- `/capcom feature {id}` - Show specific feature and its tasks

---

## Error Handling

| Condition | Response |
|-----------|----------|
| Beads not initialized | Prompt `/install` |
| Subagent fails | Fall back to direct `bd stats && bd list --tree` |
| No active work | Suggest `/exploration` or `bd create` |
