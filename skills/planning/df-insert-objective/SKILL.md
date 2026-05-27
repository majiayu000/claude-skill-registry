---
name: df:insert-objective
description: |
  Insert urgent work as decimal objective (e.g., 72.1) between existing objectives.
  Structural roadmap change — use only when explicitly requested.
argument-hint: <after> <description>
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
---

<objective>
Insert a decimal objective for urgent work discovered mid-milestone that must be completed between existing integer objectives.

Uses decimal numbering (72.1, 72.2, etc.) to preserve the logical sequence of planned objectives while accommodating urgent insertions.

Purpose: Handle urgent work discovered during execution without renumbering entire roadmap.
</objective>

<execution_context>
@~/.claude/devflow/workflows/insert-objective.md
</execution_context>

<context>
Arguments: $ARGUMENTS (format: <after-phase-number> <description>)

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
Execute the insert-objective workflow from @~/.claude/devflow/workflows/insert-objective.md end-to-end.
Preserve all validation gates (argument parsing, objective verification, decimal calculation, roadmap updates).
</process>
