---
name: df:cleanup
description: |
  Archive accumulated objective directories from completed milestones.
  Destructive operation — archives directories. Use only when explicitly requested.
disable-model-invocation: true
---
<objective>
Archive objective directories from completed milestones into `.planning/milestones/v{X.Y}-objectives/`.

Use when `.planning/objectives/` has accumulated directories from past milestones.
</objective>

<execution_context>
@~/.claude/devflow/workflows/cleanup.md
</execution_context>

<process>
Follow the cleanup workflow at @~/.claude/devflow/workflows/cleanup.md.
Identify completed milestones, show a dry-run summary, and archive on confirmation.
</process>
