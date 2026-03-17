---
name: gsd-quick
description: Quick single-phase GSD execution without full planning
argument-hint: "<task-description>"
tags: [orchestration, gsd, quick, productivity]
user-invocable: true
---

# GSD Quick -- Single-Phase Execution

Execute a simple task in a fresh sub-agent context without full planning overhead.

## What To Do

1. Parse the task description
2. Spawn ONE fresh Task agent with the task
3. Verify the result
4. No STATE.md or ROADMAP.md needed (too lightweight)

Use this for tasks completable in a single agent session (< 30 tool calls).
For multi-phase tasks, use /gsd-plan instead.

## Arguments
- `<task-description>`: What to do (natural language)