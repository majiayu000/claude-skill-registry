---
name: ln-500-story-quality-gate
description: "Story-level quality gate with 4-level verdict (PASS/CONCERNS/FAIL/WAIVED) and Quality Score. Use when Story is ready for quality assessment."
license: MIT
---

> **Paths:** File paths (`shared/`, `references/`, `../ln-*`) are relative to skills repo root. If not found at CWD, locate this SKILL.md directory and go up one level for repo root. If `shared/` is missing, fetch files via WebFetch from `https://raw.githubusercontent.com/levnikolaevich/claude-code-skills/master/skills/{path}`.

**Type:** L2 Coordinator
**Category:** 5XX Quality

# Story Quality Gate

Runtime-backed gate coordinator. Owns fast-track routing, quality/test summaries, final Story verdict, and branch finalization.

## Inputs

| Input | Required | Source | Description |
|-------|----------|--------|-------------|
| `storyId` | Yes | args, git branch, kanban, user | Story to process |

**Resolution:** Story Resolution Chain.  
**Status filter:** To Review

## Purpose & Scope

- Invoke `ln-510-quality-coordinator`
- Invoke `ln-520-test-planner` when needed
- Wait deterministically for test-task readiness
- Calculate gate verdict: `PASS | CONCERNS | FAIL | WAIVED`
- Move Story to `Done` only on passing outcomes
- Persist resumable gate runtime in `.hex-skills/story-gate/runtime/`

## Runtime Contract

**MANDATORY READ:** Load `shared/references/environment_state_contract.md`, `shared/references/storage_mode_detection.md`, `shared/references/input_resolution_pattern.md`
**MANDATORY READ:** Load `shared/references/coordinator_runtime_contract.md`, `shared/references/story_gate_runtime_contract.md`, `shared/references/coordinator_summary_contract.md`
**MANDATORY READ:** Load `shared/references/git_worktree_fallback.md`
**MANDATORY READ:** Load `references/minimum_quality_checks.md`

Runtime CLI:

```bash
node shared/scripts/story-gate-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-gate/manifest.json
node shared/scripts/story-gate-runtime/cli.mjs status
node shared/scripts/story-gate-runtime/cli.mjs record-quality --payload '{...}'
node shared/scripts/story-gate-runtime/cli.mjs record-test-status --payload '{...}'
node shared/scripts/story-gate-runtime/cli.mjs record-stage-summary --story {storyId} --payload '{...}'
node shared/scripts/story-gate-runtime/cli.mjs checkpoint --phase PHASE_6_VERDICT --payload '{...}'
node shared/scripts/story-gate-runtime/cli.mjs advance --to PHASE_7_FINALIZATION
```

## 4-Level Gate Model

| Verdict | Meaning | Action |
|---------|---------|--------|
| `PASS` | All checks passed | Story -> `Done` |
| `CONCERNS` | Minor issues, accepted risk | Story -> `Done` with comment |
| `FAIL` | Blocking issues found | Create follow-up tasks; Story does not go to `Done` |
| `WAIVED` | User-approved exception | Story -> `Done` with waiver evidence |

## Workflow

### Phase 0: Config

1. Resolve `storyId` and `task_provider`.
2. Build gate manifest:
   - `story_id`
   - `task_provider`
   - `project_root`
   - `worktree_dir`
   - `branch`
   - `fast_track_policy`
   - `nfr_policy`
   - `test_task_policy`
3. Start runtime and checkpoint `PHASE_0_CONFIG`.

### Phase 1: Discovery

1. Load Story metadata and child task metadata.
2. Detect existing test task and its current status.
3. Capture readiness inputs if available from upstream pipeline.
4. Checkpoint `PHASE_1_DISCOVERY`.

### Phase 2: Fast-Track

1. Determine `fast_track=true` only when readiness explicitly allows it.
2. Checkpoint `PHASE_2_FAST_TRACK` with:
   - `fast_track`
   - gate scope summary

### Phase 3: Quality Checks

1. Compute:
   - `childRunId = {parent_run_id}--ln-510--{storyId}`
   - `childSummaryArtifactPath = .hex-skills/runtime-artifacts/runs/{parent_run_id}/story-quality/{storyId}.json`
2. Materialize child manifest and start child coordinator runtime:
   - `node shared/scripts/quality-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-gate/ln-510--{storyId}_manifest.json --run-id {childRunId}`
3. Checkpoint `PHASE_3_QUALITY_CHECKS` with:
   - `child_run.worker=ln-510`
   - `child_run.run_id={childRunId}`
   - `child_run.summary_artifact_path={childSummaryArtifactPath}`
   - `child_run.phase_context=quality_checks`
4. Invoke `ln-510-quality-coordinator` with managed transport inputs:
   - full mode: `Skill(skill: "ln-510-quality-coordinator", args: "{storyId} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")`
   - fast-track: `Skill(skill: "ln-510-quality-coordinator", args: "{storyId} --fast-track --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")`
5. Read child `story-quality` artifact only, then `record-quality`.
6. Checkpoint `PHASE_3_QUALITY_CHECKS` with the recorded quality summary.
7. If the quality summary already implies hard FAIL, you may jump directly to `PHASE_6_VERDICT`.

### Phase 4: Test Planning

1. Decide whether planning is needed:
   - no test task -> invoke `ln-520`
   - fast-track -> invoke simplified `ln-520`
   - test task already exists and is terminal (`Done | SKIPPED | VERIFIED`) -> checkpoint as reused
2. When invoking `ln-520`, compute:
   - `childRunId = {parent_run_id}--ln-520--{storyId}`
   - `childSummaryArtifactPath = .hex-skills/runtime-artifacts/runs/{parent_run_id}/story-tests/{storyId}.json`
3. Materialize child manifest and start child coordinator runtime:
   - `node shared/scripts/test-planning-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-gate/ln-520--{storyId}_manifest.json --run-id {childRunId}`
4. Checkpoint `PHASE_4_TEST_PLANNING` with:
   - `child_run.worker=ln-520`
   - `child_run.run_id={childRunId}`
   - `child_run.summary_artifact_path={childSummaryArtifactPath}`
   - `child_run.phase_context=test_planning`
5. Invoke `ln-520-test-planner` with managed transport inputs:
   - normal mode: `Skill(skill: "ln-520-test-planner", args: "{storyId} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")`
   - simplified mode: `Skill(skill: "ln-520-test-planner", args: "{storyId} --simplified --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")`
6. Read child `story-tests` artifact only, then `record-test-status`.
7. Checkpoint `PHASE_4_TEST_PLANNING`.

### Phase 5: Test Verification

1. If test task exists but is not `Done`, pause runtime:
   - `phase = PAUSED`
   - `resume_action = wait for test task completion`
2. When resumed, verify:
   - test task terminal status is `Done`, `SKIPPED`, or `VERIFIED`
   - coverage summary exists
   - planned scenarios and Story AC coverage are machine-readable
3. Checkpoint `PHASE_5_TEST_VERIFICATION` with:
   - `test_task_status`
   - verification result

### Phase 6: Verdict

1. Calculate `quality_score`.
2. Evaluate NFR validation:
   - full gate: security, performance, reliability, maintainability
   - fast-track: security mandatory, others may downgrade to concerns-only scope
3. **End-to-End Scenario Completeness Walkthrough:** For each AC where an actor (user, bot, scheduler, handler, pipeline) must invoke or consume a mechanism, trace all 5 segments of the interaction path:
   - **(1) Actor trigger** — what initiates the scenario (user sends message, timer fires, webhook arrives, event is enqueued)
   - **(2) Entry point** — the named mechanism (MCP tool, API endpoint, CLI command, UI component, chat handler, config file, cron handler)
   - **(3) Discovery** — how the actor's system finds/loads the mechanism at runtime (config registration, route mounting, plugin loading, system prompt, environment variable)
   - **(4) Usage context** — what the actor's system needs to correctly invoke the mechanism (instructions, prompts, schemas, type hints, documentation, parameter guidance)
   - **(5) Observable outcome** — the verifiable result (response message, state change, log entry, notification)
   If any segment is missing, create an `AC-` prefixed issue. Common failures: infrastructure exists but nothing exposes it (missing segment 2), mechanism exists but the actor's system can't find it (missing segment 3), mechanism is discoverable but the actor's system doesn't know when or how to use it (missing segment 4). If any `AC-` issue is found: verdict MUST be `FAIL`; create fix tasks for the missing segments.
4. Determine final verdict.
5. For `FAIL`:
   - create follow-up tasks
   - keep Story out of `Done`
6. Checkpoint `PHASE_6_VERDICT` with:
   - `final_result`
   - `quality_score`
   - `nfr_validation`
   - `fix_tasks_created`

### Phase 7: Finalization

For `PASS | CONCERNS | WAIVED`:

1. Commit and push verified branch if needed.
2. Move Story to `Done`.
3. Post gate comment.
4. Cleanup worktree when caller does not own it.

For `FAIL`:

1. Do not finalize branch as accepted.
2. Checkpoint `PHASE_7_FINALIZATION` with `status=skipped_by_verdict`.
3. Record resulting Story status and follow-up task IDs.

After finalization, write a Stage 3 coordinator artifact with:
- `summary_kind=pipeline-stage`
- `stage=3`
- `story_id`
- `status=completed`
- `final_result`
- `story_status`
- `verdict`
- `quality_score`
- `warnings`

### Phase 8: Self-Check

Build final checklist from runtime state:

- [ ] Config, discovery, and fast-track checkpoints exist
- [ ] Quality summary recorded from `ln-510`
- [ ] Test-planning and test-verification state are deterministic
- [ ] Final verdict checkpoint exists
- [ ] Story final status recorded
- [ ] Branch finalization recorded or skipped by verdict
- [ ] Stage 3 coordinator artifact recorded

Checkpoint `PHASE_8_SELF_CHECK` with `pass=true|false`.
Complete runtime only after `pass=true`.

## Coordinator Invocation (MANDATORY)

| Phase | Worker | Purpose |
|-------|--------|---------|
| 3 | `ln-510-quality-coordinator` | Code quality, agent review, regression, log analysis |
| 4 | `ln-520-test-planner` | Research/manual/auto test planning |

```javascript
childRunId = "{parent_run_id}--ln-510--{storyId}"
childSummaryArtifactPath = ".hex-skills/runtime-artifacts/runs/{parent_run_id}/story-quality/{storyId}.json"
node shared/scripts/quality-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-gate/ln-510--{storyId}_manifest.json --run-id {childRunId}
node shared/scripts/story-gate-runtime/cli.mjs checkpoint --phase PHASE_3_QUALITY_CHECKS --payload '{"child_run":{"worker":"ln-510","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}","phase_context":"quality_checks"}}'
Skill(skill: "ln-510-quality-coordinator", args: "{storyId} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")

childRunId = "{parent_run_id}--ln-520--{storyId}"
childSummaryArtifactPath = ".hex-skills/runtime-artifacts/runs/{parent_run_id}/story-tests/{storyId}.json"
node shared/scripts/test-planning-runtime/cli.mjs start --story {storyId} --manifest-file .hex-skills/story-gate/ln-520--{storyId}_manifest.json --run-id {childRunId}
node shared/scripts/story-gate-runtime/cli.mjs checkpoint --phase PHASE_4_TEST_PLANNING --payload '{"child_run":{"worker":"ln-520","run_id":"{childRunId}","summary_artifact_path":"{childSummaryArtifactPath}","phase_context":"test_planning"}}'
Skill(skill: "ln-520-test-planner", args: "{storyId} --run-id {childRunId} --summary-artifact-path {childSummaryArtifactPath}")
```

## TodoWrite format (mandatory)

```
- Start ln-500 runtime (pending)
- Load Story/test-task metadata (pending)
- Decide fast-track mode (pending)
- Start ln-510 child runtime, checkpoint child_run, and record quality summary (pending)
- Start or reuse ln-520 child runtime, checkpoint child_run, and record test-planning summary (pending)
- Verify test task readiness (pending)
- Calculate final verdict (pending)
- Finalize Story/branch state and Stage 3 artifact (pending)
- Run runtime self-check and complete (pending)
```

## Critical Rules

- Runtime state is the gate orchestration SSOT.
- `ln-510` and `ln-520` are consumed only through summary JSON artifacts.
- Child coordinator runtime status is resume-only metadata; phase completion still depends on the recorded child artifact.
- Test-task waiting is a deterministic pause, not an implicit stop.
- `FAIL` is a valid terminal gate result if follow-up actions are recorded correctly.
- `ln-1000` consumes the Stage 3 coordinator artifact, not free-text stage output.
- Story may go to `Done` only on `PASS`, `CONCERNS`, or `WAIVED`.

## Definition of Done

- [ ] Runtime started and config/discovery checkpoints recorded
- [ ] Fast-track decision checkpointed
- [ ] `ln-510` summary recorded in runtime
- [ ] `ln-520` summary recorded or reused deterministically
- [ ] Test verification reached terminal state or deterministic pause
- [ ] Final verdict checkpointed with quality score and NFR results
- [ ] Story moved to `Done` only for passing outcomes, or follow-up tasks created for `FAIL`
- [ ] Stage 3 coordinator artifact recorded before completion
- [ ] Self-check passed and runtime completed

## Phase 9: Meta-Analysis

**MANDATORY READ:** Load `shared/references/meta_analysis_protocol.md`

Skill type: `execution-orchestrator`. Run after phases complete. Output to chat using the `execution-orchestrator` format.

## Reference Files

- `shared/references/coordinator_runtime_contract.md`
- `shared/references/story_gate_runtime_contract.md`
- `shared/references/coordinator_summary_contract.md`
- `references/minimum_quality_checks.md`
- `../ln-510-quality-coordinator/SKILL.md`
- `../ln-520-test-planner/SKILL.md`

---
**Version:** 7.0.0
**Last Updated:** 2026-02-09
