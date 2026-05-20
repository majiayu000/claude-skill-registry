---
name: session-start
description: Start a session by loading workspace context and prior state
---

# Session Start

Uses **Orchestrator**. Orchestrator loads context directly — session operations run inline because they need conversation context and judgment. Load workspace context, prior session state, and establish the session goal.

**Prerequisites:** Access to workspace configuration files

---

## Phase 1: Load Context

### Read Workspace Files

Read these files in order:

1. `workspace.config.yaml` — process profile, forge topology, board IDs, AI runtimes, commands
2. `docs/workspace/context.md` — tech stack, domain terms, architecture, key conventions
3. `docs/workspace/goals.md` — durable priorities, milestones, backlog (if exists)
4. `.tmp/workspace/goals.md` — active sprint state, current focus (if exists)

### Check for Prior Sessions

1. List files in `.tmp/sessions/`
2. Read the most recent session handoff artifact (if any)
3. Note any incomplete work or open questions from prior sessions

### Verify Board Status

For any tracked issues carried over from prior sessions or identified in sprint state:

1. Read `workspace.config.yaml` for board field IDs
2. Check current board status for each active issue
3. Flag any stale statuses (e.g., issue still "In Progress" but branch was merged)
4. Correct stale statuses before proceeding

---

## Phase 2: Establish Session

### Summarize Context

1. State the process profile and its implications
2. Note active AI runtimes
3. Identify current priorities from goals.md
4. Flag any carry-over from prior sessions

### State the Goal

1. Confirm the session goal with the user
2. Identify active constraints
3. Acknowledge approval gates

### Output

```markdown
## Context Anchors

- **Issue:** #<number> - <title> (if applicable)
- **Branch:** <active branch> (if applicable)
- **Prior Session:** <session file> (if applicable)

## Session Context

**Process Profile:** <lightweight | standard | regulated>
**AI Runtimes:** <list>
**Active Priorities:**

- <priority 1>
- <priority 2>

## Carry-Over (if any)

- <incomplete item from prior session>
- <open question>

## Session Goal

<Clear statement of what this session aims to accomplish>

## Next Step

<First action toward the goal>

**Approval Required:** Yes
```

### ⛔ CHECKPOINT

**STOP.** Confirm the session goal before proceeding to execution.

---

## Error Handling

| Situation                                 | Recovery                             |
| ----------------------------------------- | ------------------------------------ |
| workspace.config.yaml missing             | Ask user to run setup-workspace      |
| goals.md missing or empty                 | Ask user for current priorities      |
| Prior session file references stale state | Verify current state before acting   |
| Context files are outdated                | Use refresh-context prompt to update |
