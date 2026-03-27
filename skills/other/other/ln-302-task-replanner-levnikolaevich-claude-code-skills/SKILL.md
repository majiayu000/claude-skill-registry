---
name: ln-302-task-replanner
description: "Compares ideal plan vs existing tasks and applies KEEP/UPDATE/OBSOLETE/CREATE changes. Use when Story tasks need re-sync with updated requirements."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Task Replanner

**Type:** L3 Worker
**Category:** 3XX Planning

Standalone-first worker for task replanning. It compares the ideal task plan with existing tasks and applies the required operations.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/tools_config_guide.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/template_loading_pattern.md`
- `shared/references/destructive_operation_safety.md`
- `references/replan_algorithm.md`

## Inputs

Core inputs:
- `storyId`
- `taskType`
- `storyData`
- `existingTaskIds`
- `idealPlan`
- `teamId`

Optional transport inputs:
- `runId`
- `summaryArtifactPath`

## Output Contract

Always build a structured summary envelope:
- `schema_version`
- `summary_kind=task-plan`
- `run_id`
- `identifier`
- `producer_skill=ln-302`
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

1. Resolve Story context if needed.
2. Load existing tasks.
3. Normalize ideal vs existing task structures.
4. Classify `KEEP`, `UPDATE`, `OBSOLETE`, `CREATE`.
5. Show summary if interactive.
6. Execute provider-specific updates.
7. Update kanban.
8. Return structured summary.

## Critical Rules

- Remain standalone-capable.
- Do not require coordinator runtime state.
- Preserve type-specific rules after replanning.
- Return machine-readable output every time.

## Definition of Done

- [ ] Existing tasks loaded and compared
- [ ] Replan operations classified
- [ ] Updates, cancellations, and creations executed
- [ ] kanban updated
- [ ] Structured summary returned
- [ ] Summary artifact written when `summaryArtifactPath` is provided

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
