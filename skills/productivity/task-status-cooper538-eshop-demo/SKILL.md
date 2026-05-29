---
name: task-status
description: Show task status overview. Use when user asks "jaký je stav tasků", "co je hotové", "co mě blokuje", or runs /task-status.
allowed-tools: Bash, Read
---

# Task Status Overview

Display current status of tasks with visual indicators, blocking information, and progress tracking.

## Usage

```
/task-status              # Current phase (or all if not in branch)
/task-status phase-02     # Specific phase
/task-status --all        # All phases
```

## Current Status

!.claude/scripts/task-status.sh

## Process

### Step 1: Run Status Script

Execute the task status script:

```bash
.claude/scripts/task-status.sh [phase-XX|--all]
```

### Step 2: Present Results

The script outputs:
- List of tasks with status icons (✅ completed, 🔵 in_progress, ⚪ pending)
- "YOU ARE HERE" marker for current task
- Blocking dependencies for pending tasks
- Progress percentage
- Next available task

## Arguments

- `$1` - Phase filter:
  - `phase-XX` or just `XX` - specific phase
  - `--all` - all phases
  - (none) - current phase from branch, or all if on main

## Status Icons

| Icon | Status | Description |
|------|--------|-------------|
| ⚪ | pending | Not started, may be blocked |
| 🔵 | in_progress | Currently being worked on |
| ✅ | completed | Done and merged |

## Output Example

```
Phase 01: Foundation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ task-01 Solution Setup
🔵 task-02 Shared Kernel                    ← YOU ARE HERE
⚪ task-03 Contracts                        (blocked by: task-02)
⚪ task-04 gRPC                             (blocked by: task-02, task-03)

Progress: 1/6 (16%)
Next available: task-02 (in progress)
```

## Integration

This skill integrates with:
- `/start-task` - to begin working on available tasks
- `/finish-task` - to complete current task
- `/sort-tasks` - for topological ordering
