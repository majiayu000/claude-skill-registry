---
name: aidd-flow-state
description: Owns shared flow/state runtime for stage state, progress/tasklist, and stage-result lifecycle. Use when orchestration needs canonical active-stage, progress, tasklist, or stage-result commands.
lang: en
model: inherit
user-invocable: false
---

## Scope
- This skill owns shared flow/state runtime entrypoints.
- Stage skills call these commands for active stage/feature state, progress checks, tasklist normalization, and stage-result/status lifecycle.
- DocIO and loop orchestration ownership remains in `feature-dev-aidd:aidd-docio` and `feature-dev-aidd:aidd-loop`.

## Canonical shared Python entrypoints
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/progress.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/progress_cli.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasks_derive.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/status_summary.py`

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py`
- When to run: at stage entry before stage-local orchestration begins.
- Inputs: stage identifier (canonical positional argument; compatibility alias `--stage` is accepted) and optional ticket/feature context.
- Outputs: normalized active-stage state in workspace metadata.
- Failure mode: non-zero exit when stage value is invalid or active workspace metadata is unreadable.
- Next action: fix stage/context input and rerun stage activation.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`
- When to run: stage-chain postflight only after stage runtime + actions apply complete.
- Inputs: canonical stage-result payload (ticket, stage, result, scope/work-item keys, evidence links).
- Outputs: deterministic `aidd.stage_result.v1` artifact under `aidd/reports/loops/<ticket>/<scope_key>/`.
- Failure mode: non-zero exit on missing required payload fields or invalid contract values.
- Next action: fix postflight payload generation and rerun stage-chain; do not switch to non-canonical runtime paths.

## Ownership guard
- Flow/state command runtime modules must live under `skills/aidd-flow-state/runtime/*`.
- Consumers should use `skills/aidd-flow-state/runtime/*` as canonical command paths.

## Additional resources
- [references/progress-tasklist.md](references/progress-tasklist.md) (when: progress/tasklist checks are unclear; why: align check/normalize and logging semantics).
- [references/stage-lifecycle.md](references/stage-lifecycle.md) (when: stage result/status flow is unclear; why: keep stage-result and summary updates deterministic).
