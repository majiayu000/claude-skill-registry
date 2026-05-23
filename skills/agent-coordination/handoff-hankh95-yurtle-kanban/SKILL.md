---
name: handoff
description: Hand off work to another agent with full context
disable-model-invocation: true
allowed-tools: Bash(yurtle-kanban *), Bash(git *), Write, Read
argument-hint: "<EXP-XXX> <agent-a|agent-b|agent-c|agent-d> [notes]"
---

# Hand Off Work

Create a handoff note so the receiving agent has full context when they pick up the work.

## Required Arguments

- `EXP-XXX` - The expedition ID to hand off
- `agent-X` - The target agent (agent-a, agent-b, agent-c, agent-d)
- `[notes]` - Optional additional context

## Steps

### 1. Create Handoffs Directory

```bash
mkdir -p kanban-work/handoffs
```

### 2. Gather Current State

Read the expedition file and check git status:

```bash
# Find expedition file
cat kanban-work/expeditions/EXP-XXX*.md

# Check current branch and uncommitted changes
git status
git log --oneline -5
```

### 3. Create Handoff Note

Create `kanban-work/handoffs/EXP-XXX-to-agent-X-YYYYMMDD.md`:

```markdown
---
expedition: EXP-XXX
from: agent-[current]
to: agent-[target]
created: YYYY-MM-DD HH:MM
status: pending
---

# Handoff: EXP-XXX

**From:** Agent [Current] ([Mac/DGX])
**To:** Agent [Target] ([Mac/DGX])
**Time:** YYYY-MM-DD HH:MM

## Current State

**Branch:** `expedition/exp-XXX-...`
**Last Commit:** [commit message]
**Kanban Status:** [status]

## What's Done

- [x] [Completed item 1]
- [x] [Completed item 2]

## What's Needed

- [ ] [Remaining item 1]
- [ ] [Remaining item 2]

## Key Context

[Important decisions, gotchas, things to watch out for]

## Files to Focus On

- `path/to/important/file.py` - [why it matters]
- `path/to/another/file.py` - [why it matters]

## How to Continue

1. Checkout branch: `git checkout expedition/exp-XXX-...`
2. [Next step]
3. [Next step]
```

### 4. Update Expedition File

Add a Ship's Log entry to the expedition:

```markdown
### YYYY-MM-DD: Handed off to Agent [X]

[Summary of what was done and what remains]
```

### 5. Commit and Push

```bash
git add kanban-work/handoffs/EXP-XXX-*.md
git add kanban-work/expeditions/EXP-XXX*.md
git commit -m "handoff(exp-XXX): Hand off to agent-X

- What was completed
- What remains

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin HEAD
```

### 6. Update Kanban (Optional)

If the work is paused, optionally move to a waiting status:

```bash
# Only if work is blocked waiting for the other agent
yurtle-kanban move EXP-XXX blocked
```

### 7. Confirm Handoff

Show summary:
- Handoff note location
- What the receiving agent should do
- Remind to run `/sync` on next session

## Agent Reference

| Agent | Machine | Focus |
|-------|---------|-------|
| agent-a | DGX | GPU training, heavy compute |
| agent-b | Mac | Architecture, tooling, docs |
| agent-c | DGX | GPU training, heavy compute |
| agent-d | Mac | Architecture, tooling, docs |
