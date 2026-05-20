---
name: ln-221-story-creator
description: "Creates Story documents with 9-section structure and INVEST validation in Linear. Use when Epic has an IDEAL plan ready for Story generation."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Creator

**Type:** L3 Worker
**Category:** 2XX Planning

Standalone-first worker for Story creation. It may be called directly or as part of a coordinator flow, but its public contract is the same in both cases.

## MANDATORY READ

Load these before execution:
- `shared/references/planning_worker_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_state_contract.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/creation_quality_checklist.md`
- `shared/references/template_loading_pattern.md`

## Inputs

Core inputs:
- `epicData`
- `idealPlan` or `appendMode + newStoryDescription`
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
3. `PHASE_2_LOAD_TEMPLATE`
4. `PHASE_3_GENERATE_STORIES`
5. `PHASE_4_VALIDATE_STORIES`
6. `PHASE_5_CONFIRM_OR_AUTOAPPROVE`
7. `PHASE_6_APPLY_CREATE`
8. `PHASE_7_UPDATE_KANBAN`
9. `PHASE_8_WRITE_SUMMARY`
10. `PHASE_9_SELF_CHECK`

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
- `producer_skill=ln-221`
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
- `.hex-skills/runtime-artifacts/runs/{parent_run_id}/story-plan-worker/ln-221--{identifier}.json`

## Workflow

1. Resolve task provider and Epic context if not already provided.
2. Load the Story template.
3. Generate Story documents with exactly the template sections.
4. Insert standards research into Technical Notes only.
5. Validate INVEST and AC limits before creation.
6. Show preview unless `autoApprove=true`.
7. Create Stories in Linear or file mode.
8. Update kanban.
9. Write `story-plan-worker` summary.
10. Return structured summary.

## Critical Rules

- Keep exactly the template-defined Story structure.
- Insert standards research into Technical Notes, not into ACs.
- Reject Stories that fail INVEST or exceed AC limits.
- **STOP before save_issue:** verify all 9 sections present in body: Story, Context, Acceptance Criteria, Implementation Tasks, Test Strategy, Technical Notes, Definition of Done, Dependencies, Assumptions. PreToolUse hook will BLOCK creation without them.
- Remain standalone-capable.
- Never require coordinator runtime state to operate.

## Definition of Done

- [ ] Story template loaded and respected
- [ ] Story documents generated
- [ ] INVEST validation passed
- [ ] Stories created in provider-specific storage
- [ ] kanban updated
- [ ] Structured summary returned
- [ ] Summary artifact written when `summaryArtifactPath` is provided

---

**Version:** 3.0.0
**Last Updated:** 2025-12-23
