---
name: tasks-router
description: Routes task operations to tasks-file or tasks-beads based on project state. Use when a skill needs to create, triage, or update tasks and must choose the system.
---

# Tasks Router Skill

## Overview

Use this skill to select the correct task system for the current repository and then follow the chosen skill.

## Routing Logic

- If `.beads/` exists at repo root, use `tasks-beads`.
- Otherwise, use `tasks-file`.
- If `.beads/` exists but `br` is not available, fall back to `tasks-file` and note the mismatch.

## Procedure

1. Check for Beads workspace:
   ```bash
   test -d .beads
   ```
2. If `.beads/` exists, verify `br` is installed:
   ```bash
   command -v br
   ```
3. State the selected skill explicitly:
   - "Using tasks-beads" or "Using tasks-file"
4. Follow the chosen skill's workflow.

## Examples

**Beads project:**
```bash
test -d .beads
command -v br
# Using tasks-beads
br create --title="..." --type=bug --priority=2 --description="..." --json
```

**File-based project:**
```bash
test -d .beads || echo "no beads"
# Using tasks-file
create tasks/001-pending-p2-short-title.md using the tasks-file workflow
```
