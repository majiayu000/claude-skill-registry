---
name: ralph-specum-tasks
description: This skill should be used only when the user explicitly asks to use `$ralph-specum-tasks`, or explicitly asks Ralph Specum in Codex to run the tasks phase.
metadata:
  surface: helper
  action: tasks
---

# Ralph Specum Tasks

Use this for the tasks phase.

## Contract

- Resolve the active spec by explicit path, exact name, or `.current-spec`
- Require `requirements.md` and `design.md`
- Merge state fields only
- Keep the Ralph disk contract unchanged

## Action

1. Resolve the active spec. If none exists, stop.
2. Require `requirements.md` and `design.md`. Read `research.md` when present, `.progress.md`, and current state.
3. Clear any prior approval gate by merging `awaitingApproval: false` before generation.
4. Respect `granularity` from state. Allow `--tasks-size fine|coarse` to override it. In quick mode, default unset granularity to `fine`.
5. Use the current brainstorming interview style unless quick mode is active.
6. Write or rewrite `tasks.md`.
7. Count tasks and merge state with:
   - `phase: "tasks"`
   - `awaitingApproval: true`
   - `taskIndex: first incomplete or totalTasks`
   - `totalTasks: counted tasks`
8. Update `.progress.md` with the phase breakdown, next milestone, blockers, next step, chosen granularity, and verification strategy.
9. If spec commits are enabled, commit only the spec artifacts.
10. In quick mode, review quickly, then continue directly into implementation.

## Output Shape

Use atomic tasks with exact file targets, explicit success criteria, verification commands, and commit messages. Preserve POC-first ordering. Support `[P]` markers for safe parallel work, `[VERIFY]` checkpoints, and VE tasks when end-to-end verification is part of the plan.

## Response Handoff

- After writing `tasks.md`, name `tasks.md` and summarize the task plan briefly.
- End with exactly one explicit choice prompt:
  - `approve current artifact`
  - `request changes`
  - `continue to implementation`
- Treat `continue to implementation` as approval of `tasks.md`.
