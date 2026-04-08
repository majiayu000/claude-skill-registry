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

## Output Contract

Always build a structured summary envelope:
- `schema_version`
- `summary_kind=story-plan`
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

## Workflow

1. Resolve task provider and Epic context if not already provided.
2. Load the Story template.
3. Generate Story documents with exactly the template sections.
4. Insert standards research into Technical Notes only.
5. Validate INVEST and AC limits before creation.
6. Show preview unless `autoApprove=true`.
7. Create Stories in Linear or file mode.
8. Update kanban.
9. Return structured summary.

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
