---
name: work
description: Find and start the next highest-priority expedition from the kanban board
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Read
argument-hint: "[EXP-XXX]"
---

# Pick Up Work

Find and start work on an expedition. If an expedition ID is provided ($ARGUMENTS), start that one. Otherwise, find the next highest-priority ready item.

## Steps

### 1. Check Current Work

First, check if already working on something:

```bash
yurtle-kanban list --status in_progress
```

If items are in progress, show them and ask if the user wants to continue or pick up new work.

### 2. Find Ready Work

If no specific expedition requested:

```bash
yurtle-kanban list --status ready --limit 5
```

Show the top 5 ready items with their priorities.

### 3. Start Work

Once an expedition is selected (either from $ARGUMENTS or user choice):

```bash
# Move to in_progress
yurtle-kanban move EXP-XXX in_progress

# Create expedition branch from main
git checkout main
git pull origin main
git checkout -b expedition/exp-XXX-short-description
```

**IMPORTANT**: Expedition branches use the `expedition/exp-XXX-name` prefix and are never deleted (permanent memory).

### 4. Load Context

Read the expedition file to understand the work:

```bash
# Find and read the expedition file
cat kanban-work/expeditions/EXP-XXX*.md
```

Summarize:
- What needs to be done (Build Steps)
- Success criteria
- Dependencies
- Current status from Ship's Log

### 5. Ready to Work

Confirm the expedition is loaded and ready to begin implementation.
