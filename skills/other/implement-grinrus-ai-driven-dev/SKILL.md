---
name: implement
description: Executes implement-stage loop workflow for the next scoped work item through stage-chain orchestration. Use when implement stage enters loop mode.
argument-hint: $1 [note...] [test=fast|targeted|full|none] [tests=<filters>] [tasks=<task1,task2>]
lang: ru
prompt_version: 1.1.49
source_version: 1.1.49
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/implement/runtime/implement_run.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py *)"
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(cat *)"
  - "Bash(xargs *)"
  - "Bash(npm *)"
  - "Bash(pnpm *)"
  - "Bash(yarn *)"
  - "Bash(pytest *)"
  - "Bash(python *)"
  - "Bash(go *)"
  - "Bash(mvn *)"
  - "Bash(make *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-loop/runtime/loop_pack.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-core/runtime/diff_boundary_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(${CLAUDE_PLUGIN_ROOT}/hooks/format-and-test.sh *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/progress_cli.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/status_summary.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py --fix *)"
  - "Bash(git status *)"
  - "Bash(git diff *)"
  - "Bash(git log *)"
  - "Bash(git show *)"
  - "Bash(git rev-parse *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core` and `feature-dev-aidd:aidd-loop`.

## Steps
1. Inputs: resolve active `<ticket>/<scope_key>` and confirm loop artifacts are present for implement stage.
2. Stage-chain policy: execute via canonical stage-chain orchestration through stage runtime entrypoint; internal preflight/postflight are orchestration details and not operator commands.
3. Manual write/create of `stage.implement.result.json` is forbidden; stage-result files are produced only by stage-chain postflight. `[AIDD_LOOP_POLICY:MANUAL_STAGE_RESULT_FORBIDDEN]`
4. Runtime-path safety: use only runtime commands from this skill contracts. If stdout/stderr contains `can't open file .../skills/.../runtime/...`, stop with immediate BLOCKED `runtime_path_missing_or_drift`; one runtime-path error is terminal for current run, do not invent alternate filenames, and do not retry guessed commands.
5. Retry safety: do not rerun the same failing shell command more than once without new evidence/artifacts. For cwd/build mismatches, stop with blocker and handoff instead of looped retries.
6. Read order after stage-chain preflight artifacts: `readmap.md` -> loop pack -> review pack (if exists) -> rolling context pack; do not perform broad repo scan before these artifacts.
7. Run subagent `feature-dev-aidd:implementer`.
8. Orchestration: use the existing rolling context pack (do not regenerate it), Fill actions.json (v1) at `aidd/reports/actions/<ticket>/<scope_key>/implement.actions.json`, keep action types strictly in `{tasklist_ops.set_iteration_done, tasklist_ops.append_progress_log, tasklist_ops.next3_recompute, context_pack_ops.context_pack_update}`, and validate schema via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/implement/runtime/implement_run.py`.
9. Canonical stage-chain: internal preflight -> stage runtime -> actions_apply.py/postflight -> `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`; it must produce `aidd/reports/loops/<ticket>/<scope_key>/stage.implement.result.json`. `[AIDD_LOOP_POLICY:CANONICAL_STAGE_RESULT_PATH]`
10. Non-canonical stage-result path under `skills/aidd-loop/runtime/` is forbidden (treat as prompt-flow drift). `[AIDD_LOOP_POLICY:NON_CANONICAL_STAGE_RESULT_FORBIDDEN]`
11. Output: return stage contract + updated artifacts with explicit handoff/next action.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/implement/runtime/implement_run.py`
- When to run: as canonical implement stage runtime before postflight.
- Inputs: ticket, scope/work-item context, and validated actions payload.
- Outputs: stage validation artifacts and status payload for downstream postflight.
- Failure mode: non-zero exit for invalid actions schema or missing stage prerequisites.
- Next action: fix actions/preconditions and rerun runtime validation before postflight.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py`
- When to run: mandatory final step in stage-chain postflight after actions validation.
- Inputs: `--actions <path>` and optional `--apply-log <path>`.
- Outputs: applied actions, progress/status artifacts, and apply logs.
- Failure mode: DocOps apply failure, boundary guard failure, or status-summary failure.
- Next action: inspect action/apply logs, fix root cause, rerun the stage-chain, and verify canonical stage result exists (`aidd/reports/loops/<ticket>/<scope_key>/stage.implement.result.json`).

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`
- When to run: stage-chain postflight stage-result emission only (not operator/manual recovery command).
- Inputs: canonical postflight payload (`ticket`, `stage`, `result`, `scope-key`, `work-item-key`, evidence links).
- Outputs: canonical `aidd.stage_result.v1` at `aidd/reports/loops/<ticket>/<scope_key>/stage.implement.result.json`.
- Failure mode: non-zero exit on missing required args or invalid stage-result contract fields.
- Next action: fix postflight payload generation and rerun the stage-chain; do not switch to non-canonical loop runtime paths.

## Notes
- Implement stage does not run ad-hoc test loops; format-only is allowed and test orchestration is delegated to hook policy.

## Additional resources
- Contract schema: [CONTRACT.yaml](CONTRACT.yaml) (when: preflight/postflight or actions contract is unclear; why: validate required fields and artifact expectations before rerun).
