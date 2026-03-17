---
name: gsd:execute-phase
description: Execute phase tasks using wave-based parallel execution
version: 1.0.0
triggers: [execute phase, run phase]
tools: [Bash, Glob, Grep, Write]
---

# GSD Execute Phase

Executes phase tasks using wave-based parallel execution with gsd-executor agent.

## When to Use

- Running a planned phase
- Executing tasks in parallel waves
- Following structured development workflow

## Process

1. Load phase-plan.md for task list
2. Identify independent tasks for parallel execution
3. Execute tasks in waves (parallel where possible)
4. Create atomic commits per task
5. Handle deviations automatically (bugs, missing functionality, blocking)
6. Request checkpoint verification between waves

## Wave Execution Rules

- Independent tasks execute in parallel
- Dependent tasks wait for dependencies
- Deviations are handled per deviation rules
- Checkpoints occur between waves

## Deviation Handling

- BUG: Fix immediately in same context
- MISSING: Implement if under 5 minutes
- BLOCKING: Defer to backlog

## Success Criteria

All phase tasks completed with atomic commits.

## Related Skills

@skills/gsd/agents/executor - Agent that executes tasks
@skills/gsd/commands/plan-phase - Creates phase plans
