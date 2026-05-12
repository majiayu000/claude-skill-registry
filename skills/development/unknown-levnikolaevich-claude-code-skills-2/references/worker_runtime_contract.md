<!-- SOURCE-OF-TRUTH: shared/references/worker_runtime_contract.md. Edit ONLY here; run `node tools/marketplace/shared.mjs sync` -->

# Worker Runtime Contract

Small deterministic runtime contract for stateful L3 workers.

## Runtime Files

Every stateful worker runtime uses:
- `manifest.json` for immutable invocation inputs
- `state.json` for mutable execution snapshot
- `checkpoints.json` for latest checkpoint per phase plus history
- `history.jsonl` for append-only runtime events

Terminal phases: `DONE`, `PAUSED`.

## Required Fields

`run_id`, `skill`, `identifier`, `phase`, `complete`, `paused_reason`, `pending_decision`, `final_result`, `resume_action`.

`resume_action` must be derived from `state.json` and checkpoints only, never from chat memory.

## Artifact Contract

Coordinator-invoked workers must receive `runId` and `summaryArtifactPath`, then write a validated summary artifact before `DONE`. Standalone workers may generate a run id and write the summary to the family-specific run-scoped path. Coordinators consume worker artifacts, not worker prose.

## Independence and Guards

- Workers depend only on shared contracts and their own domain inputs.
- Workers must not encode `Parent`, `Coordinator`, caller hierarchy, or upward orchestration state.
- No transition without a checkpoint for the current phase.
- No `DONE` before self-checks pass and the summary artifact is written.
- Public outputs and runtime artifacts stay separate.

## Family Contracts

Load the matching family contract only when it applies: environment worker, audit worker, task worker, quality worker, test planning, task planning, or planning worker.

---
**Version:** 1.0.0
**Last Updated:** 2026-04-06
