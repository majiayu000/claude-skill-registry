---
name: df:health
description: |
  Diagnose planning directory health and optionally repair issues.
  Use when the user wants to check project integrity or troubleshoot DevFlow state.
  Triggers on: "is the project healthy?", "check project health", "any issues?", "something seems wrong with planning"
argument-hint: [--repair]
allowed-tools:
  - Read
  - Bash
  - Write
  - AskUserQuestion
---
<objective>
Validate `.planning/` directory integrity and report actionable issues. Checks for missing files, invalid configurations, inconsistent state, and orphaned jobs.
</objective>

<execution_context>
@~/.claude/devflow/workflows/health.md
</execution_context>

<process>
Execute the health workflow from @~/.claude/devflow/workflows/health.md end-to-end.
Parse --repair flag from arguments and pass to workflow.
</process>
