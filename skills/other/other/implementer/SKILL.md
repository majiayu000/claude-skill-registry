---
name: implementer
description: Execute feature tasks one by one with live documentation and context logging. Triggers on "Execute FEAT-XXX tasks", "Start implementing FEAT-XXX", "Work on FEAT-XXX", "Continue FEAT-XXX".
globs: ["docs/features/**/tasks.md", "docs/features/**/status.md", "docs/features/**/context/*", "src/**", "tests/**"]
---

# Implementer

Execute feature tasks one by one with live documentation and context updates.

## Triggers

- "Execute FEAT-XXX tasks"
- "Start implementing FEAT-XXX"
- "Work on FEAT-XXX"
- "Continue FEAT-XXX"
- "Resume FEAT-XXX"
- "Next task for FEAT-XXX"

## Prerequisites

- Feature folder exists with completed:
  - `spec.md`
  - `analysis.md`
  - `design.md`
  - `tasks.md`
  - `context/` folder with templates
- Git branch created for feature
- If missing: guide user to complete previous phases

## Purpose

1. **Find next uncompleted task** in tasks.md
2. **Execute task** (write code, create files, etc.)
3. **Update documentation** in real-time
4. **Update context** (session_log, decisions, blockers)
5. **Commit** after each task
6. **Repeat** until all tasks done or blocker hit

## Process

### 1. Read Context

```bash
# Read tasks
cat docs/features/FEAT-XXX/tasks.md

# Read design for reference
cat docs/features/FEAT-XXX/design.md

# Read spec for requirements
cat docs/features/FEAT-XXX/spec.md

# Check current status
cat docs/features/FEAT-XXX/status.md

# Read last session log entries
tail -30 docs/features/FEAT-XXX/context/session_log.md

# Check for active blockers
cat docs/features/FEAT-XXX/context/blockers.md

# Verify git branch
git branch --show-current
```

### 2. Verify Branch

If on main/master:
-> STOP and say: "Create feature branch first: git checkout -b feature/XXX-name"

If on correct feature branch:
-> Continue with implementation

### 3. Find Next Task

Scan tasks.md for first task that is:
- `[ ]` Pending, OR
- `[in progress]` In Progress (resume)

Skip tasks that are:
- `[x]` Complete
- `[skipped]` Skipped
- `[blocked]` Blocked

### 4. Execute Task Loop

For each task:

**A. BEFORE starting:**
1. Update tasks.md: [ ] -> [in progress]
2. Announce: "Starting task: [task description]"

**B. DURING execution:**
1. Write code / create files
2. Follow design.md specifications
3. If unclear -> ask user, don't assume
4. If blocked -> mark [blocked], log to blockers.md, move to next
5. If decision needed -> log to decisions.md

**C. AFTER completing:**
1. Update tasks.md: [in progress] -> [x]
2. Update progress table in tasks.md
3. Commit: git add . && git commit -m "FEAT-XXX: [task]"
4. Announce: "Task complete. Progress: X/Y tasks"

**D. CHECKPOINT (every 30 min or 3 tasks):**
1. Update status.md with progress
2. Update context/session_log.md
3. git push origin [branch]
4. Summary of progress

### 5. Commit Format

```bash
git add [specific files for this task]
git commit -m "FEAT-XXX: [Task description]"
```

**Examples:**
```
FEAT-001: Create User model
FEAT-001: Add user validation schemas
FEAT-001: Implement UserService CRUD methods
FEAT-001: Add POST /users endpoint
FEAT-001: Add unit tests for UserService
```

### 6. Completion

When all tasks done:

```
FEAT-XXX implementation complete!

Summary:
- Total tasks: X
- Completed: X
- Skipped: X
- Blocked: X

Next steps:
1. Push: git push -u origin feature/XXX-name
2. Create PR: /git pr
3. After merge: /wrap-up FEAT-XXX
```
