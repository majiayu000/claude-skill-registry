---
name: status
description: "Check task status in the tracker and local artifacts. Use when the user invokes /status or asks for project/task status."
---

# Status Command

Follow `CLAUDE.md`, `conventions.md`, and `ARCHITECTURE.md`.

## Task

Show task status from tracker and related local artifacts.

## Algorithm

1. If no argument: show overall project status.
2. If argument provided: show specific task status.

### Mode 1: Project Overview (no argument)

Use `beads` skill to get:
- List open tasks
- List ready tasks (not blocked)
- List blocked tasks
- List in-progress tasks

Output:
```
Project Status
==============

Stats:
- Open tasks: <count>
- Ready to work: <count>
- Blocked: <count>
- In progress: <count>

Ready Tasks (can start now):
- <id1> - <title> (P<priority>)
- <id2> - <title> (P<priority>)

Blocked Tasks:
- <id3> - <title>
  Blocked by: <blocker-id> (<blocker-status>)

In Progress:
- <id5> - <title>
```

### Mode 2: Specific Task (with argument)

Use `beads` to get task details and dependency tree.

Also check local artifacts:
- `docs/drafts/BRIEF_*<name>*.md`
- `docs/drafts/TASK_*<name>*.md`
- `docs/reviews/REVIEW_*<name>*.md`

Output:
```
Task: <id> - <title>
Status: <status>
Type: <type>
Priority: <priority>

Description:
<description>

Dependency Tree:
<tree output>

Local Artifacts:
- Brief: <exists/none>
- Spec: <exists/none>
- Review: <exists/none>

Next step:
[What needs to be done based on current stage]
```

## Next Step Suggestions

Based on task status, suggest:
- `open` + no blocker -> `/implement <id>`
- `in_progress` -> continue implementation
- `in_progress` + code done -> `/review <id>`
- `needs_work` -> `/fix <id>`
