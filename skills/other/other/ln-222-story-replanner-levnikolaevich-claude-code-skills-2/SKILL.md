---
name: ln-222-story-replanner
description: "Replans Stories by comparing IDEAL vs existing (KEEP/UPDATE/OBSOLETE/CREATE). Use when Epic requirements changed and Stories need realignment."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root.

# Story Replanner

**Type:** L3 Worker
**Category:** 2XX Planning

Standalone-first worker for Story replanning. It compares ideal Story intent with existing Stories and applies the resulting operations.

## MANDATORY READ

Load these before execution:
- `shared/references/coordinator_summary_contract.md`
- `shared/references/environment_state_contract.md`
- `shared/references/storage_mode_detection.md`
- `shared/references/template_loading_pattern.md`
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

## Output Contract

Always build a structured summary envelope:
- `schema_version`
- `summary_kind=story-plan`
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
- **STOP before save_issue:** verify all 9 sections present in body: Story, Context, Acceptance Criteria, Implementation Tasks, Test Strategy, Technical Notes, Definition of Done, Dependencies, Assumptions. PreToolUse hook will BLOCK creation without them.

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
