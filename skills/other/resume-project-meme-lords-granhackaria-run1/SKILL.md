---
name: gsd:workflow:resume-project
description: Workflow for resuming a paused project
version: 1.0.0
triggers: [resume, continue, restore]
tools: [Bash, Glob, Grep, Write]
---

# GSD Resume Project Workflow

Workflow for resuming a paused or interrupted project.

## When to Use

- Continuing after pause
- Restoring project state
- Picking up where left off

## Phases

1. Load saved state
2. Restore progress
3. Verify readiness
4. Continue work

## Success Criteria

Project resumed from saved state.
