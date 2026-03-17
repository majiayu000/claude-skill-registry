---
name: gsd-progress
description: Show progress of current GSD execution plan
argument-hint: ""
tags: [orchestration, gsd, progress, status]
user-invocable: true
---

# GSD Progress Report

Read STATE.md and ROADMAP.md to show current execution progress.

## What To Do

1. Read .planning/STATE.md for completion status
2. Read .planning/ROADMAP.md for total phases
3. Calculate % complete
4. Show next pending phase
5. List any blocked or failed phases

## Output Format
```
## GSD Progress: Feature Name
Phases: 5/8 complete (62.5%)
Current wave: 3
Next phase: Phase 6 - Integration Tests
Blocked: None
```