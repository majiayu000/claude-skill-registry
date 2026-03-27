---
name: ln-301-task-creator
description: "Creates implementation, refactoring, and test tasks from templates. Use when an approved task plan needs tasks created in Linear and kanban."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Task Creator

**Type:** L3 Worker
**Category:** 3XX Planning

Standalone-first worker for task creation. It creates tasks from an already approved plan and returns a stable summary contract.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/tools_config_guide.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/template_loading_pattern.md`
- `shared/references/creation_quality_checklist.md`
- `shared/references/destructive_operation_safety.md`

## Inputs

Core inputs:
- `taskType`
- `storyData`
- `idealPlan` or `appendMode + newTaskDescription`
- `teamId`
- `guideLinks`

Optional transport inputs:
- `runId`
- `summaryArtifactPath`

## Output Contract

Always build a structured summary envelope:
- `schema_version`
- `summary_kind=task-plan`
- `run_id`
- `identifier`
- `producer_skill=ln-301`
- `produced_at`
- `payload`

Payload fields:
- `mode`
- `story_id`
- `task_type`
- `tasks_created`
- `tasks_updated`
- `tasks_canceled`
- `task_urls`
- `kanban_updated`
- `dry_warnings_count`
- `warnings`

If `summaryArtifactPath` is provided:
- write the same JSON summary to that path

If `summaryArtifactPath` is not provided:
- return the same summary in structured output only

## Workflow

1. Resolve task provider and template set.
2. Run DRY and destructive-operation checks where applicable.
3. Generate task documents from the selected template.
4. Validate type-specific rules.
5. Show preview and get confirmation if needed.
6. Create tasks in Linear or file mode.
7. Update kanban.
8. Return structured summary.

## Critical Rules

- Remain standalone-capable.
- Do not require coordinator runtime state.
- Keep implementation, refactoring, and test rules separated by `taskType`.
- Write machine-readable summary output every time.

## Definition of Done

- [ ] Templates loaded
- [ ] Task documents generated
- [ ] Type-specific validation passed
- [ ] Tasks created in provider-specific storage
- [ ] kanban updated
- [ ] Structured summary returned
- [ ] Summary artifact written when `summaryArtifactPath` is provided

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
