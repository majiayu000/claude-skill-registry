---
name: ln-222-story-replanner
description: "Replans Stories by comparing IDEAL vs existing (KEEP/UPDATE/OBSOLETE/CREATE). Use when Epic requirements changed and Stories need realignment."
license: MIT
---

> **Paths:** File paths (`references/`, `../ln-*`) are relative to this skill directory.

# Story Replanner

**Type:** L3 Worker
**Category:** 2XX Planning

Standalone-first worker for Story replanning. It compares ideal Story intent with existing Stories and applies the resulting operations.

## MANDATORY READ

Load these before execution:
- `references/planning_worker_runtime_contract.md`
- `references/coordinator_summary_contract.md`
- `references/environment_state_contract.md`
- `references/storage_mode_detection.md`
- `references/template_loading_pattern.md`
- `references/replan_algorithm_stories.md`

## Inputs

Core inputs:
- `epicData`
- `idealPlan`
- `existingStoryIds`
- `standardsResearch`
- `teamId`
- `autoApprove`

Optional transport inputs:
- `runId`
- `summaryArtifactPath`

The worker must remain fully usable without caller-provided `runId` and without `summaryArtifactPath`. In standalone mode it generates its own `run_id` before emitting the summary envelope.

## Runtime

Runtime family: `planning-worker-runtime`

Identifier:
- `epic-{epicId}`

Phases:
1. `PHASE_0_CONFIG`
2. `PHASE_1_RESOLVE_CONTEXT`
3. `PHASE_2_LOAD_EXISTING_STORIES`
4. `PHASE_3_CLASSIFY_REPLAN`
5. `PHASE_4_CONFIRM_OR_AUTOAPPROVE`
6. `PHASE_5_APPLY_REPLAN`
7. `PHASE_6_UPDATE_KANBAN`
8. `PHASE_7_WRITE_SUMMARY`
9. `PHASE_8_SELF_CHECK`

Managed child-run mode:
- caller starts the runtime with `--run-id` and `--summary-artifact-path`
- runtime writes the final summary artifact directly to the caller-provided path
- parent coordinator records the resulting `story-plan-worker` artifact

Standalone mode:
- runtime generates its own `run_id`
- runtime still returns the same structured summary envelope
- artifact writing is optional unless `summaryArtifactPath` is provided

## Output Contract

Always build a structured summary envelope:
- `schema_version`
- `summary_kind=story-plan-worker`
- `run_id`
- `identifier`
- `producer_skill=ln-222`
- `produced_at`
- `payload`

Payload fields:
- `mode`
- `epic_id`
- `stories_planned`
- `stories_created`
- `stories_updated`
- `stories_canceled`
- `story_urls`
- `warnings`
- `kanban_updated`
- `research_path_used`

If `summaryArtifactPath` is provided:
- write the same JSON summary to that path

If `summaryArtifactPath` is not provided:
- return the same summary in structured output only

Managed artifact path pattern:
- `.hex-skills/runtime-artifacts/runs/{parent_run_id}/story-plan-worker/ln-222--{identifier}.json`

## Workflow

1. Resolve Epic context if not already provided.
2. Load existing Stories one by one.
3. Normalize ideal vs existing Story structures.
4. Run the replan algorithm to classify `KEEP`, `UPDATE`, `OBSOLETE`, `CREATE`.
5. Show operations summary unless `autoApprove=true`.
6. Execute provider-specific updates.
7. Update kanban.
8. Return structured summary.

## Critical Rules

- Prefer conservative updates when matching is ambiguous.
- Preserve finished work when replanning conflicts with completed Stories.
- Keep the worker standalone-capable.
- Never require coordinator runtime state to operate.
- Return machine-readable results, not prose-only outcomes.
- **STOP before tracker createStory/updateBody:** verify all 9 sections present in body: Story, Context, Acceptance Criteria, Implementation Tasks, Test Strategy, Technical Notes, Definition of Done, Dependencies, Assumptions. PreToolUse hook will BLOCK creation without them.

## Definition of Done

- [ ] Existing Stories loaded and normalized
- [ ] Replan algorithm applied
- [ ] Required updates, cancellations, and creations executed
- [ ] kanban updated
- [ ] Structured summary returned
- [ ] Summary artifact written when `summaryArtifactPath` is provided

---

**Version:** 3.0.0
**Last Updated:** 2025-12-23
