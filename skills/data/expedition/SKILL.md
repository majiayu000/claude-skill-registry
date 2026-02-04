---
name: expedition
description: Create a new expedition with proper ID allocation and template
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Write, Read
argument-hint: "<title>"
---

# Create New Expedition

Create a new expedition with properly allocated ID to prevent conflicts between agents.

## Steps

### 1. Allocate ID

**CRITICAL**: Always allocate the ID first to prevent duplicates:

```bash
yurtle-kanban next-id EXP --json
```

This atomically allocates the next available ID (e.g., EXP-720).

### 2. Create Expedition File

Create `kanban-work/expeditions/EXP-XXX-Title.md` with this template:

```yaml
---
yurtle: v1.3
id: EXP-XXX
type: expedition
title: "EXP-XXX: $ARGUMENTS"
status: ready
priority: MEDIUM
created: YYYY-MM-DD
assignee: TBD
tags: []
depends_on: []
---

# EXP-XXX: $ARGUMENTS

## Problem Statement

[What problem does this solve?]

## Solution

[High-level approach]

## Build Steps

### Phase 1: [Name]

[Steps to implement]

## Success Criteria

- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Files to Modify

| File | Action | Description |
|------|--------|-------------|
| path/to/file | Create/Modify | What changes |

## Ship's Log

### YYYY-MM-DD: Expedition Created

[Initial context and decision]

## Related

- [Related doc](path)
```

### 3. IMMEDIATELY Commit and Push

**CRITICAL**: Push the expedition file immediately to prevent conflicts:

```bash
git add kanban-work/expeditions/EXP-XXX-*.md
git commit -m "feat(kanban): create EXP-XXX expedition"
git push
```

The `next-id` command only reserves the ID. If you don't push the file, other agents won't see it and may create conflicting work.

### 4. Update Kanban Status

Explicitly set the kanban status so other agents can see it:

```bash
yurtle-kanban move EXP-XXX ready
```

### 5. Confirm Creation

Show the created expedition and suggest next steps:
- Review and fill in details
- Set priority and assignee
- Add dependencies if any
- Run `/work EXP-XXX` to start working on it
