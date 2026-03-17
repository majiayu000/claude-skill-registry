---
name: ln-302-task-replanner
description: Updates ALL task types (implementation/refactoring/test). Compares IDEAL plan vs existing tasks, categorizes KEEP/UPDATE/OBSOLETE/CREATE, applies changes in Linear and kanban.
---

# Universal Task Replanner

Worker that re-syncs existing tasks to the latest requirements for any task type.

## Purpose & Scope
- Load full existing task descriptions from Linear
- Compare them with orchestrator-provided IDEAL plan (implementation/refactoring/test)
- Decide operations (KEEP/UPDATE/OBSOLETE/CREATE) and execute
- Drop NFR items; only functional scope remains
- Update Linear issues and kanban_board.md accordingly

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/storage_mode_detection.md` for Linear vs File mode operations.

## Invocation (who/when)
- **ln-300-task-coordinator:** REPLAN mode when implementation tasks already exist.
- **Orchestrators (other groups):** Replan refactoring or test tasks as needed.
- Not user-invoked directly.

## Inputs
- Common: `taskType`, teamId, Story data (id/title/description with AC, Technical Notes, Context), existingTaskIds.
- Implementation: idealPlan (1-6 tasks), guideLinks.
- Refactoring: codeQualityIssues, refactoringPlan, affectedComponents.
- Test: manualTestResults, testPlan (E2E 2-5, Integration 0-8, Unit 0-15, Priority ≤15), infra/doc/cleanup items.

## Template Loading

**MANDATORY READ:** Load `shared/references/template_loading_pattern.md` for template copy workflow.

**Template Selection by taskType:**
- `implementation` → `task_template_implementation.md`
- `refactoring` → `refactoring_task_template.md`
- `test` → `test_task_template.md`

**Local copies:** `docs/templates/*.md` (in target project)

## Workflow (concise)
1) Load templates per taskType (see Template Loading) and fetch full existing task descriptions.
2) Normalize both sides (IDEAL vs existing sections) and run replan algorithm to classify KEEP/UPDATE/OBSOLETE/CREATE.
3) Present summary (counts, titles, key diffs). Confirmation required if running interactively.
4) Execute operations in Linear: update descriptions, cancel obsolete, **create missing with state="Backlog"**, preserve parentId for updates.
5) Update kanban_board.md: remove canceled, add new tasks under Story in Backlog.
6) Return operations summary with URLs and warnings.

## Type Rules (must hold after update)
| taskType | Hard rule | What to enforce |
|----------|-----------|-----------------|
| implementation | No new test creation | Updated/created tasks must not introduce test creation text |
| refactoring | Regression strategy required | Issues + severity, 3-phase plan, regression strategy, preserve functionality |
| test | Risk-based limits | Priority ≤15 scenarios; E2E 2-5, Integration 0-8, Unit 0-15, Total 10-28; no framework/library/DB tests |

## Critical Notes
- **MANDATORY:** Always pass `state: "Backlog"` when creating new tasks (CREATE operation). Linear defaults to team's default status (often "Postponed") if not specified.
- Foundation-First ordering from IDEAL plan is preserved; do not reorder.
- Language preservation: keep existing task language (EN/RU).
- No code snippets; keep to approach/steps/AC/components.
- If Story reality differs (component exists, column exists), propose Story correction to orchestrator.

## Definition of Done
- Existing tasks loaded and parsed with correct template.
- IDEAL plan vs existing compared; operations classified.
- Type validation passed for all updated/created tasks.
- Operations executed in Linear (updates, cancels, creations) with parentId intact.
- kanban_board.md updated (Backlog) with correct Epic/Story/indentation.
- Summary returned (KEEP/UPDATE/OBSOLETE/CREATE counts, URLs, warnings).

## Reference Files
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Template loading:** `shared/references/template_loading_pattern.md`
- **Linear creation workflow:** `shared/references/linear_creation_workflow.md`
- **Replan algorithm (universal):** `shared/references/replan_algorithm.md`
- **Task-specific replan algorithm:** `references/replan_algorithm.md` (5 scenarios, comparison logic)
- **Storage mode detection:** `shared/references/storage_mode_detection.md`
- Templates (centralized): `shared/templates/task_template_implementation.md`, `shared/templates/refactoring_task_template.md`, `shared/templates/test_task_template.md`
- Local copies: `docs/templates/*.md` (in target project)
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
