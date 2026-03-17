---
name: ln-401-task-executor
description: Executes implementation tasks (Todo -> In Progress -> To Review). Follows KISS/YAGNI, guides, quality checks. Not for test tasks.
---

# Implementation Task Executor

Executes a single implementation (or refactor) task from Todo to To Review using the task description and linked guides.

## Purpose & Scope
- Handle one selected task only; never touch other tasks.
- Follow task Technical Approach/plan/AC; apply KISS/YAGNI and guide patterns.
- Update Linear/kanban for this task: Todo -> In Progress -> To Review.
- Run typecheck/lint; update docs/tests/config per task instructions.
- Not for test tasks (label "tests" goes to ln-404-test-executor).

## Task Storage Mode

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Load task** | `get_issue(task_id)` | `Read("docs/tasks/epics/.../tasks/T{NNN}-*.md")` |
| **Update status** | `update_issue(id, state)` | `Edit` the `**Status:**` line in file |
| **Kanban** | Updated by Linear sync | Must update `kanban_board.md` manually |

**File Mode status format:**
```markdown
## Status
**Status:** In Progress | **Priority:** High | **Estimate:** 4h
```

## Mode Detection

Detect operating mode at startup:

**Plan Mode Active:**
- Steps 1-2: Load task context (read-only, OK in plan mode)
- Generate EXECUTION PLAN (files to create/modify, approach) → write to plan file
- Call ExitPlanMode → STOP. Do NOT implement.
- Steps 3-6: After approval → execute implementation

**Normal Mode:**
- Steps 1-6: Standard workflow without stopping

## Progress Tracking with TodoWrite

When operating in any mode, skill MUST create detailed todo checklist tracking ALL steps.

**Rules:**
1. Create todos IMMEDIATELY before Step 1
2. Each workflow step = separate todo item; implementation step gets sub-items
3. Mark `in_progress` before starting step, `completed` after finishing

**Todo Template (10 items):**

```
Step 1: Load Context
  - Fetch full task description + linked guides/manuals/ADRs

Step 2: Receive Task
  - Get task ID from orchestrator, load full description

Step 3: Start Work
  - Set task to In Progress, update kanban

Step 4: Implement
  - Follow task plan/AC, apply KISS/YAGNI
  - Update docs and existing tests if impacted

Step 5: Quality
  - Run typecheck and lint (or project equivalents)

Step 6: Finish
  - Set task to To Review, update kanban
  - Add summary comment (changes, tests, docs)
```

## Workflow (concise)
1) **Load context:** Fetch full task description (Linear: get_issue; File: Read task file); read linked guides/manuals/ADRs/research; auto-discover team/config if needed.
2) **Receive task:** Get task ID from orchestrator (ln-400); load full task description.
3) **Start work:** Update this task to In Progress (Linear: update_issue; File: Edit status line); move it in kanban (keep Epic/Story indent).
4) **Implement:** Follow checkboxes/plan; keep it simple; avoid hardcoded values; reuse existing components; add Task ID comment (`// See PROJ-123`) to new code blocks; update docs noted in Affected Components; update existing tests if impacted (no new tests here).
5) **Quality:** Run typecheck and lint (or project equivalents); ensure instructions in Existing Code Impact are addressed.
6) **Finish:** Mark task To Review (Linear: update_issue; File: Edit status line); update kanban to To Review; add summary comment (what changed, tests run, docs touched).

## Critical Rules
- Single-task updates only; no bulk status changes.
- Keep language of the task (EN/RU) in edits/comments.
- No code snippets in the description; code lives in repo, not in Linear.
- No new test creation; only update existing tests if required.
- Preserve Foundation-First ordering from orchestrator; do not reorder tasks.
- Add Task ID comments to new code blocks for traceability (`// See PROJ-123` or `# See PROJ-123`).
- **Do NOT commit.** Leave all changes uncommitted — ln-402 reviews and commits with task ID reference.

## Definition of Done
- Task selected and set to In Progress; kanban updated accordingly.
- Guides/manuals/ADRs/research read; approach aligned with task Technical Approach.
- Implementation completed per plan/AC; docs and impacted tests updated.
- Typecheck and lint passed (or project quality commands) with evidence in comment.
- Task set to To Review; kanban moved to To Review; summary comment added.

## Reference Files
- Guides/manuals/ADRs/research: `docs/guides/`, `docs/manuals/`, `docs/adrs/`, `docs/research/`
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
