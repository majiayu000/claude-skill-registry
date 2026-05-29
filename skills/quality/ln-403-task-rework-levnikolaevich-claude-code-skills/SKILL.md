---
name: ln-403-task-rework
description: Fixes tasks in To Rework and returns them to To Review. Applies reviewer feedback only for the selected task.
---

# Task Rework Executor

Executes rework for a single task marked To Rework and hands it back for review.

## Purpose & Scope
- Load full task, reviewer comments, and parent Story; understand requested changes.
- Apply fixes per feedback, keep KISS/YAGNI, and align with guides/Technical Approach.
- Update only this task: To Rework -> In Progress -> To Review; no other tasks touched.

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Load review notes** | Linear comments | Review section in task file or kanban |
| **Update status** | `update_issue(id, state)` | `Edit` the `**Status:**` line in file |

**File Mode transitions:** To Rework → In Progress → To Review

## Workflow (concise)
1) **Receive task:** Get task ID from orchestrator (ln-400); read task (Linear: get_issue; File: Read task file), review notes, parent Story.
2) **Plan fixes:** Map each comment to an action; confirm no new scope added.
3) **Implement:** Follow task plan/checkboxes; address config/hardcoded issues; update docs/tests noted in Affected Components and Existing Code Impact.
4) **Quality:** Run typecheck/lint (or project equivalents); ensure fixes reflect guides/manuals/ADRs/research.
5) **Handoff:** Set task to To Review (Linear: update_issue; File: Edit status line); move it in kanban; add summary comment referencing resolved feedback.

## Critical Rules
- Single-task only; never bulk update.
- Do not mark Done; only To Review (ln-402 decides Done).
- Keep language (EN/RU) consistent with task.
- No new tests/tasks created here; only update existing tests if impacted.

## Definition of Done
- Task and review feedback fully read; actions mapped.
- Fixes applied; docs/tests updated as required.
- Quality checks passed (typecheck/lint or project standards).
- Status set to To Review; kanban updated; summary comment added referencing fixed items.

## Reference Files
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
