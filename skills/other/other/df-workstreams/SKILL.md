---
name: df:workstreams
description: |
  Manage parallel workstreams using git worktrees.
  Complex parallel workstream management — use only when explicitly requested.
argument-hint: "setup | status | merge"
disable-model-invocation: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - Task
  - AskUserQuestion
---
<objective>
Manage parallel feature development using git worktrees. Independent objectives execute simultaneously in separate worktrees, each with their own Claude session.

Routes by first argument:
- `setup` — Analyze deps, create worktrees, provision .planning/
- `status` — Check progress across all active workstreams
- `merge` — Squash-merge completed workstreams, reconcile state
</objective>

<execution_context>
@~/.claude/devflow/references/ui-brand.md
</execution_context>

<context>
Subcommand: $ARGUMENTS

@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/config.json
</context>

<process>
Parse $ARGUMENTS to determine subcommand.

**If `setup`:**
Follow @~/.claude/devflow/workflows/workstreams-setup.md

**If `status`:**
Follow @~/.claude/devflow/workflows/workstreams-status.md

**If `merge`:**
Follow @~/.claude/devflow/workflows/workstreams-merge.md

**If no argument or unrecognized:**
Display usage:
```
/df:workstreams setup   — Create parallel worktrees for independent objectives
/df:workstreams status  — Check progress across active workstreams
/df:workstreams merge   — Merge completed workstreams back to main
```
</process>
