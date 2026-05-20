---
name: df:remove-objective
description: |
  Remove a future objective from roadmap and renumber subsequent objectives.
  Destructive operation — permanently removes objective and renumbers.
argument-hint: <phase-number>
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
---
<objective>
Remove an unstarted future objective from the roadmap and renumber all subsequent objectives to maintain a clean, linear sequence.

Purpose: Clean removal of work you've decided not to do, without polluting context with cancelled/deferred markers.
Output: Objective deleted, all subsequent objectives renumbered, git commit as historical record.
</objective>

<execution_context>
@~/.claude/devflow/workflows/remove-objective.md
</execution_context>

<context>
Objective: $ARGUMENTS

@.planning/ROADMAP.md
@.planning/STATE.md
</context>

<process>
Execute the remove-objective workflow from @~/.claude/devflow/workflows/remove-objective.md end-to-end.
Preserve all validation gates (future objective check, work check), renumbering logic, and commit.
</process>
