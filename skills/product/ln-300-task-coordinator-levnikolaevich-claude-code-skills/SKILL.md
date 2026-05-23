---
name: ln-300-task-coordinator
description: Orchestrates task operations. Analyzes Story, builds optimal plan (1-6 implementation tasks), delegates to ln-301-task-creator (CREATE/ADD) or ln-302-task-replanner (REPLAN). Auto-discovers team ID.
---

# Linear Task Planner (Orchestrator)

Coordinates creation or replanning of implementation tasks for a Story. Builds the ideal plan first, then routes to workers.

## Purpose & Scope
- Auto-discover Team ID, load Story context (AC, Technical Notes, Context)
- Build optimal implementation task plan (1-6 implementation tasks; NO test/refactoring tasks) in Foundation-First order
- Detect mode and delegate: CREATE/ADD -> ln-301-task-creator, REPLAN -> ln-302-task-replanner
- Strip any Non-Functional Requirements; only functional scope becomes tasks
- Never creates/updates Linear or kanban directly (workers do)

## Task Storage Mode

This orchestrator supports dual-mode task storage:

| Aspect | Linear Mode | File Mode |
|--------|-------------|-----------|
| **Detection** | Default (MCP Linear available) | `docs/tasks/epics/` directory exists |
| **Check existing** | `list_issues(parentId=Story.id)` | `Glob("docs/tasks/epics/*/stories/{slug}/tasks/*.md")` |
| **Delegate to** | ln-301/ln-302 (same workers) | ln-301/ln-302 (same workers) |

**Auto-detection:** Check if `docs/tasks/epics/` exists → File Mode, otherwise Linear Mode.

Workers (ln-301, ln-302) handle the actual Linear/File operations based on detected mode.

## When to Use
- Need tasks for a Story with clear AC/Technical Notes
- Story requirements changed and existing tasks must be updated
- NOT for test tasks or refactoring tasks (created by other orchestrators)

## Workflow (concise)
- **Phase 1 Discovery:** Auto-discover Team ID (docs/tasks/kanban_board.md); parse Story ID from request.
- **Phase 2 Decompose (always):** Load Story (AC, Technical Notes, Context), assess complexity, build IDEAL plan (1-6 implementation tasks only), apply Foundation-First execution order, extract guide links.
- **Phase 3 Check & Detect Mode:** Query Linear for existing tasks (metadata only). Detect mode by count + user keywords (add/replan).
- **Phase 4 Delegate:** Call the right worker with Story data, IDEAL plan/append request, guide links, existing task IDs if any; autoApprove=true.
- **Phase 5 Verify:** Ensure worker returns URLs/summary and updated kanban_board.md; report result.

## Mode Matrix
| Condition | Mode | Delegate | Payload |
|-----------|------|----------|---------|
| Count = 0 | CREATE | ln-301-task-creator | taskType=implementation, Story data, IDEAL plan, guideLinks |
| Count > 0 AND "add"/"append" | ADD | ln-301-task-creator | taskType=implementation, appendMode=true, newTaskDescription, guideLinks |
| Count > 0 AND replan keywords | REPLAN | ln-302-task-replanner | taskType=implementation, Story data, IDEAL plan, guideLinks, existingTaskIds |
| Count > 0 AND ambiguous | ASK | Clarify with user | — |

## Plan Mode Behavior
When invoked in Plan Mode (read-only):
- Execute Phases 1-3 normally (Discovery, Decompose, Check Existing)
- Phase 4: DO NOT delegate to workers — instead show IDEAL plan preview:
  - Task titles, goals, estimates, Foundation-First order
  - Mode detected (CREATE/ADD/REPLAN)
  - What worker WOULD be invoked (ln-301 or ln-302)
- Phase 5: Write plan summary to plan file (not Linear)
- NO Linear API calls, NO kanban updates, NO worker invocations

**TodoWrite format (mandatory):**
Add phases to todos before starting:
```
- Phase 1: Discovery (in_progress)
- Phase 2: Decompose & Build IDEAL Plan (pending)
- Phase 3: Check Existing & Detect Mode (pending)
- Phase 4: Delegate to ln-301/ln-302 (pending)
- Phase 5: Verify worker result (pending)
```
Mark each as in_progress when starting, completed when done.

## Critical Rules
- Decompose-first: always build IDEAL plan before looking at existing tasks.
- Foundation-First execution order: DB -> Repository -> Service -> API -> Frontend.
- Task limits: 1-6 implementation tasks, 3-5h each; cap total at 6. Test task created later by test planner.
- Linear creation must be sequential: create one task, confirm success, then create the next (no bulk) to catch errors early.
- **HARD CONSTRAINT:** This skill creates ONLY implementation tasks (taskType=implementation). NEVER include test tasks, manual testing tasks, or refactoring tasks in the plan. Test tasks are created LATER by test planner (after manual testing passes). Refactoring tasks are created by quality gate when code quality issues found.
- No code snippets in descriptions; workers own task documents and Linear/kanban updates.
- Language preservation: keep Story language (EN/RU) in any generated content by workers.

## Definition of Done (orchestrator)
- Team ID discovered; Story ID parsed.
- Story loaded; IDEAL plan built (1-6 implementation tasks only) with Foundation-First order and guide links.
- **NO test or refactoring tasks** in IDEAL plan (only taskType=implementation).
- Existing tasks counted; mode selected (CREATE/ADD/REPLAN or ask).
- Worker invoked with correct payload and autoApprove=true.
- Worker summary received (Linear URLs/operations) and kanban update confirmed.
- Next steps returned (ln-310-story-validator, then orchestrator continues).

## Reference Files
- Templates (centralized): `shared/templates/task_template_implementation.md`
- Local copies: `docs/templates/task_template_implementation.md` (in target project, created by workers)
- Replan algorithm details: `ln-302-task-replanner/references/replan_algorithm.md`
- Auto-discovery notes: `CLAUDE.md`, `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
