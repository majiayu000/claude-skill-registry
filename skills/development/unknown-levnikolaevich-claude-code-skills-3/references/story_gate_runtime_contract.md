<!-- SOURCE-OF-TRUTH: shared/references/story_gate_runtime_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Story Gate Runtime Contract

Deterministic runtime for `ln-500-story-quality-gate`.

Canonical phase/status names: `references/runtime_status_catalog.md`

## Runtime Location

```text
.hex-skills/story-gate/runtime/
  active/ln-500/{story_id}.json
  runs/{run_id}/manifest.json
  runs/{run_id}/state.json
  runs/{run_id}/checkpoints.json
  runs/{run_id}/history.jsonl
```

## Commands

```bash
node references/scripts/story-gate-runtime/cli.mjs start --story PROJ-123 --manifest-file <file>
node references/scripts/story-gate-runtime/cli.mjs status --story PROJ-123
node references/scripts/story-gate-runtime/cli.mjs record-quality --payload '{...}'
node references/scripts/story-gate-runtime/cli.mjs record-test-status --payload '{...}'
node references/scripts/story-gate-runtime/cli.mjs record-stage-summary --story PROJ-123 --payload '{...}'
node references/scripts/story-gate-runtime/cli.mjs checkpoint --phase PHASE_6_VERDICT --payload '{...}'
node references/scripts/story-gate-runtime/cli.mjs advance --to PHASE_7_FINALIZATION
node references/scripts/story-gate-runtime/cli.mjs pause --reason "..."
node references/scripts/story-gate-runtime/cli.mjs complete
```

## Phase Graph

- `PHASE_0_CONFIG`
- `PHASE_1_DISCOVERY`
- `PHASE_2_FAST_TRACK`
- `PHASE_3_QUALITY_CHECKS`
- `PHASE_4_TEST_PLANNING`
- `PHASE_5_TEST_VERIFICATION`
- `PHASE_6_VERDICT`
- `PHASE_7_FINALIZATION`
- `PHASE_8_SELF_CHECK`
- `DONE`
- `PAUSED`

## Required State Fields

- `fast_track`
- `quality_summary`
- `child_runs`
- `test_task_id`
- `test_task_status`
- `test_planner_invoked`
- `quality_score`
- `nfr_validation`
- `fix_tasks_created`
- `branch_finalized`
- `story_final_status`
- `final_result`
- `stage_summary`

## Guard Rules

- no transition past `PHASE_3_QUALITY_CHECKS` without recorded `ln-510` summary
- no transition past `PHASE_4_TEST_PLANNING` without recorded `ln-520` summary unless a reused test task is already terminal
- no transition past `PHASE_5_TEST_VERIFICATION` while test task is still pending
- `PHASE_6_VERDICT` must record terminal gate result before finalization
- FAIL still passes through `PHASE_7_FINALIZATION`, but as `skipped_by_verdict`
- child runtime status is resume-only metadata; gate completion still depends on recorded child artifacts
- `DONE` requires `PHASE_8_SELF_CHECK` with `pass=true`, final story state recorded, and Stage 3 coordinator artifact recorded

## Canonical Status Sets

- gate verdicts: `PASS`, `CONCERNS`, `WAIVED`, `FAIL`
- completed test-task statuses: `Done`, `SKIPPED`, `VERIFIED`
- finalization shortcut status: `skipped_by_verdict`

These names are canonical for the runtime. Do not replace them with free-form alternatives in checkpoints or examples.

## Downstream Summary Contract

`ln-510` and `ln-520` must write summaries per `references/coordinator_summary_contract.md`.

## Managed Delegation Sequence

1. compute deterministic child `run_id = {parent_run_id}--{worker}--{story_id}`
2. compute exact child summary artifact path
3. start the child coordinator runtime (`quality-runtime` or `test-planning-runtime`)
4. checkpoint `child_run` metadata in `story-gate-runtime`
5. invoke child coordinator with both `runId` and `summaryArtifactPath`
6. read only the resulting child coordinator artifact
7. record only the artifact payload in `story-gate-runtime`
8. advance Stage 3 only from recorded child artifacts

`child_runs` entries keep:
- `worker`
- `run_id`
- `summary_artifact_path`
- `phase_context`

## Coordinator Stage Summary

After `PHASE_7_FINALIZATION`, `ln-500` writes a `pipeline-stage` coordinator summary for Stage 3.

Minimum semantics:
- `stage = 3`
- `story_id`
- `status = completed`
- `final_result`
- `story_status`
- `verdict`
- `quality_score`

`ln-1000` consumes this artifact as the machine-readable completion signal for Stage 3.
