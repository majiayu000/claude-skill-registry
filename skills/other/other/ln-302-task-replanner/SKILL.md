---
name: ln-302-task-replanner
description: Updates ALL task types (implementation/refactoring/test). Compares IDEAL plan vs existing tasks, categorizes KEEP/UPDATE/OBSOLETE/CREATE, applies changes in Linear and kanban.
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Universal Task Replanner

Worker that re-syncs existing tasks to the latest requirements for any task type.

## Purpose & Scope
- Load full existing task descriptions from Linear
- Compare them with orchestrator-provided IDEAL plan (implementation/refactoring/test)
- Decide operations (KEEP/UPDATE/OBSOLETE/CREATE) and execute
- Drop NFR items; only functional scope remains
- Update Linear issues and kanban_board.md accordingly

## Task Storage Mode

**MANDATORY READ:** Load `shared/references/tools_config_guide.md`, `shared/references/storage_mode_detection.md`, and `shared/references/input_resolution_pattern.md`

Extract: `task_provider` = Task Management → Provider (`linear` | `file`).

## Invocation (who/when)
- **ln-300-task-coordinator:** REPLAN mode when implementation tasks already exist.
- **Orchestrators (other groups):** Replan refactoring or test tasks as needed.
- **Standalone:** User invokes directly with storyId (resolved via Input Resolution Chain).

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story whose tasks to replan |

**Resolution:** Story Resolution Chain.
**Status filter:** In Progress, To Review

**Additional inputs (from orchestrator or Story context):**
- Common: `taskType`, teamId, Story data (id/title/description with AC, Technical Notes, Context), existingTaskIds.
- Implementation: idealPlan (1-8 tasks), guideLinks.
- Refactoring: codeQualityIssues, refactoringPlan, affectedComponents.
- Test: manualTestResults, testPlan (Priority ≥15, Usefulness Criteria), infra/doc/cleanup items.

## Template Loading

**MANDATORY READ:** Load `shared/references/template_loading_pattern.md` for template copy workflow. Load `shared/references/destructive_operation_safety.md` for destructive operation keywords and severity classification.

**Template Selection by taskType:**
- `implementation` → `task_template_implementation.md`
- `refactoring` → `refactoring_task_template.md`
- `test` → `test_task_template.md`

**Local copies:** `docs/templates/*.md` (in target project)

## Workflow (concise)
1) **Resolve storyId:** Run Story Resolution Chain per guide (status filter: [In Progress, To Review]).
2) Load templates per taskType (see Template Loading) and fetch full existing task descriptions.
3) Normalize both sides (IDEAL vs existing sections) and run replan algorithm to classify KEEP/UPDATE/OBSOLETE/CREATE.
   - **Inherited Assumptions (UPDATE):** Preserve Inherited Assumptions from parent Story. If parent Story Assumptions changed, update Inherited Assumptions in affected tasks to match current Story registry (ID + text sync).
   - **Inherited Assumptions (CREATE):** For new tasks, extract relevant assumptions from parent Story Assumptions table, add to Context > Inherited Assumptions using `A{N} ({CATEGORY})` format.
   - **Destructive Op Detection (UPDATE):** After updating Implementation Plan, re-scan for keywords from destructive_operation_safety.md (loaded above). IF detected AND "Destructive Operation Safety" section missing → add section from shared reference template. IF section already present → preserve it.
   - **Destructive Op Detection (CREATE):** For new tasks, scan Implementation Plan for keywords from destructive_operation_safety.md (loaded above). IF detected → include "Destructive Operation Safety" section from shared reference template (MANDATORY). Fill all 5 fields + severity.
4) Present summary (counts, titles, key diffs). Confirmation required if running interactively.
5) Execute operations in Linear: update descriptions, cancel obsolete, **create missing with state="Backlog"**, preserve parentId for updates.
6) Update kanban_board.md: remove canceled, add new tasks under Story in Backlog.
7) Return operations summary with URLs and warnings.

## Type Rules (must hold after update)
| taskType | Hard rule | What to enforce |
|----------|-----------|-----------------|
| implementation | No new test creation | Updated/created tasks must not introduce test creation text |
| refactoring | Regression strategy required | Issues + severity, 3-phase plan, regression strategy, preserve functionality |
| test | Risk-based limits | Priority ≥15 scenarios covered; each test passes Usefulness Criteria; no framework/library/DB tests |

## Critical Notes
- **MANDATORY:** Always pass `state: "Backlog"` when creating new tasks (CREATE operation). Linear defaults to team's default status (often "Postponed") if not specified.
- **Destructive Op Detection:** Use keyword list from destructive_operation_safety.md (loaded above). If found after update/create → include Destructive Operation Safety section as MANDATORY.
- Foundation-First ordering from IDEAL plan is preserved; do not reorder.
- Language preservation: keep existing task language (EN/RU).
- No code snippets; keep to approach/steps/AC/components.
- If Story reality differs (component exists, column exists), propose Story correction to orchestrator.

## Definition of Done
- [ ] Existing tasks loaded and parsed with correct template.
- [ ] IDEAL plan vs existing compared; operations classified.
- [ ] Type validation passed for all updated/created tasks.
- [ ] Operations executed in Linear (updates, cancels, creations) with parentId intact.
- [ ] kanban_board.md updated (Backlog) with correct Epic/Story/indentation.
- [ ] Summary returned (KEEP/UPDATE/OBSOLETE/CREATE counts, URLs, warnings).

## Reference Files
- **Tools config:** `shared/references/tools_config_guide.md`
- **Storage mode operations:** `shared/references/storage_mode_detection.md`
- **Kanban update algorithm:** `shared/references/kanban_update_algorithm.md`
- **Template loading:** `shared/references/template_loading_pattern.md`
- **Linear creation workflow:** `shared/references/linear_creation_workflow.md`
- **Replan algorithm (universal):** `shared/references/replan_algorithm.md`
- **Task-specific replan algorithm:** `references/replan_algorithm.md` (5 scenarios, comparison logic)
- Templates (centralized): `shared/templates/task_template_implementation.md`, `shared/templates/refactoring_task_template.md`, `shared/templates/test_task_template.md`
- Local copies: `docs/templates/*.md` (in target project)
- Kanban format: `docs/tasks/kanban_board.md`

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
