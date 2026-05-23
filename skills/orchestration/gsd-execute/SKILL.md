---
name: gsd-execute
description: Execute a planned phase in a fresh agent context
argument-hint: "<phase-number>"
tags: [orchestration, execution, gsd, context-engineering]
user-invocable: true
---

# GSD Execute -- Fresh-Context Phase Execution

Execute a specific phase from the plan in a fresh agent context to prevent context rot.

## What To Do

1. **Read the plan**: Load ROADMAP.md and find the specified phase.
2. **Read current state**: Load STATE.md for decisions from previous phases.
3. **Spawn a fresh agent** using Task tool with clean 200K context.
4. **Agent executes tasks**: Follow XML task structure, run verification, create atomic commits.
5. **Update STATE.md** with completion status, decisions, and files modified.

## Wave execution
Launch multiple Task agents simultaneously for independent phases in the same wave.

## Arguments
- `<phase-number>`: Which phase to execute
- `--wave`: Execute all tasks in current wave in parallel
- `--dry-run`: Show what would be executed without changes