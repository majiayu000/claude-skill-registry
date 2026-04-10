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

**MANDATORY READ:** Load `shared/references/coordinator_summary_contract.md` and `shared/references/task_plan_worker_runtime_contract.md`
**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, `shared/references/template_loading_pattern.md`, and `shared/references/destructive_operation_safety.md`
**MANDATORY READ:** Load `references/replan_algorithm.md`

## Inputs

Core inputs:
- `storyId`
- `taskType`
- `storyData`
- `existingTaskIds`
- `idealPlan`
- `teamId`

Transport inputs:
- standalone: omit `runId` and `summaryArtifactPath`
- managed: pass both `runId` and `summaryArtifactPath`

## Runtime

Runtime family: `task-plan-worker-runtime`

Phase profile:
1. `PHASE_0_CONFIG`
2. `PHASE_1_LOAD_INPUTS`
3. `PHASE_2_LOAD_EXISTING_TASKS`
4. `PHASE_3_NORMALIZE_AND_CLASSIFY`
5. `PHASE_4_CONFIRM_OR_AUTOAPPROVE`
6. `PHASE_5_APPLY_REPLAN`
7. `PHASE_6_UPDATE_KANBAN`
8. `PHASE_7_WRITE_SUMMARY`
9. `PHASE_8_SELF_CHECK`

Summary artifact rules:
- emit `summary_kind=task-plan`
- standalone runs generate their own `run_id` and write the default worker-family artifact path
- managed runs require both `runId` and `summaryArtifactPath` and must write the summary to the exact provided path
- always write the validated summary artifact before terminal outcome

## Output Contract

Always build a structured `task-plan` summary envelope per:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/task_plan_worker_runtime_contract.md`

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

Always write the validated summary before terminal outcome.

## Workflow

1. Resolve Story context if needed.
2. Load existing tasks.
3. Normalize ideal vs existing task structures.
4. Classify `KEEP`, `UPDATE`, `OBSOLETE`, `CREATE`.
5. If classification is empty, emit a verified no-op summary and stop.
6. Show summary if interactive.
7. Execute provider-specific updates.
8. Update kanban only when provider mutations occurred.
9. Return structured summary.

## Critical Rules

- Remain standalone-capable.
- Do not require coordinator runtime state.
- Preserve type-specific rules after replanning.
- Return machine-readable output every time.
- **Fast path for no-op replans:** when no task changes survive normalization, do not mutate provider state or kanban; return a summary with zero changes.
- **STOP before save_issue:** verify all 7 sections present in body: Context, Implementation Plan, Technical Approach, Acceptance Criteria, Affected Components, Existing Code Impact, Definition of Done. PreToolUse hook will BLOCK creation without them.

## Definition of Done

- [ ] Existing tasks loaded and compared
- [ ] Replan operations classified
- [ ] Updates, cancellations, and creations executed
- [ ] kanban updated
- [ ] Structured summary returned
- [ ] Summary artifact written to the managed or standalone runtime path

---
**Version:** 3.0.0
**Last Updated:** 2025-12-23
