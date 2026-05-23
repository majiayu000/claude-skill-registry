---
name: df:pause-work
description: |
  Create context handoff when pausing work mid-objective.
  Use when the user needs to stop working and wants to save context for later resumption.
  Triggers on: "I need to stop", "save context", "pausing for now", "let's pause", "I'm done for today", "save my progress"
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Create `.continue-here.md` handoff file to preserve complete work state across sessions.

Routes to the pause-work workflow which handles:
- Current objective detection from recent files
- Complete state gathering (position, completed work, remaining work, decisions, blockers)
- Handoff file creation with all context sections
- Git commit as WIP
- Resume instructions
</objective>

<execution_context>
@.planning/STATE.md
@~/.claude/devflow/workflows/pause-work.md
</execution_context>

<process>
**Follow the pause-work workflow** from `@~/.claude/devflow/workflows/pause-work.md`.

The workflow handles all logic including:
1. Objective directory detection
2. State gathering with user clarifications
3. Handoff file writing with timestamp
4. Git commit
5. Confirmation with resume instructions
</process>
