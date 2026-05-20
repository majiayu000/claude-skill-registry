---
name: qa
description: Runs QA-stage validation, report generation, and postflight actions for the current scope. Use when QA stage is ready for loop verification.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.0.39
source_version: 1.0.39
allowed-tools:
  - Read
  - Edit
  - Glob
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/qa/runtime/qa_run.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/qa/runtime/qa.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py *)"
  - "Bash(rg *)"
  - "Bash(npm *)"
  - "Bash(pnpm *)"
  - "Bash(yarn *)"
  - "Bash(pytest *)"
  - "Bash(python *)"
  - "Bash(go *)"
  - "Bash(mvn *)"
  - "Bash(make *)"
  - "Bash(./gradlew *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasks_derive.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/progress_cli.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/status_summary.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py --fix *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core` and `feature-dev-aidd:aidd-loop`.

## Steps
1. Inputs: resolve active `<ticket>/<scope_key>` and validate QA prerequisites from loop/readmap artifacts.
2. Stage-chain policy: execute via canonical stage-chain orchestration through stage runtime entrypoint; internal preflight/postflight are orchestration details and not operator commands.
3. Manual write/create of `stage.qa.result.json` is forbidden; stage-result files are produced only by stage-chain postflight. `[AIDD_LOOP_POLICY:MANUAL_STAGE_RESULT_FORBIDDEN]`
4. Runtime-path safety: use only runtime commands from this skill contracts. If stdout/stderr contains `can't open file .../skills/.../runtime/...`, stop with immediate BLOCKED `runtime_path_missing_or_drift`; one runtime-path error is terminal for current run, do not invent alternate filenames, and do not retry guessed commands.
5. Retry safety: do not rerun the same failing shell command more than once without new evidence/artifacts. For cwd/build mismatches, stop with blocker and handoff instead of looped retries.
6. Read order after stage-chain preflight artifacts: `readmap.md` -> loop pack -> review pack (if exists) -> rolling context pack; do not perform broad repo scan before these artifacts.
7. Run subagent `feature-dev-aidd:qa`.
8. Orchestration: run QA via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/qa/runtime/qa.py`, derive tasks if needed, then Fill actions.json for `aidd/reports/actions/<ticket>/<scope_key>/qa.actions.json` strictly as `aidd.actions.v1` (`schema_version`, `allowed_action_types`, canonical `type` + `params`) with action types only from `{tasklist_ops.set_iteration_done, tasklist_ops.append_progress_log, tasklist_ops.next3_recompute, context_pack_ops.context_pack_update}`, and validate via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/qa/runtime/qa_run.py`.
9. Canonical stage-chain: internal preflight -> stage runtime -> actions_apply.py/postflight -> `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`. `[AIDD_LOOP_POLICY:CANONICAL_STAGE_RESULT_PATH]`
10. Non-canonical stage-result path under `skills/aidd-loop/runtime/` is forbidden (treat as prompt-flow drift). `[AIDD_LOOP_POLICY:NON_CANONICAL_STAGE_RESULT_FORBIDDEN]`
11. Output: return QA status contract with report paths and explicit canonical next action (`/feature-dev-aidd:status <ticket>` or `/feature-dev-aidd:tasks-new <ticket>` when follow-up tasks are required).

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/qa/runtime/qa_run.py`
- When to run: as canonical QA stage runtime before postflight.
- Inputs: ticket, scope/work-item context, QA findings, and actions payload.
- Outputs: validated QA report artifacts and stage status payload.
- Failure mode: non-zero exit when report/actions schema or required stage inputs are invalid.
- Next action: fix QA findings/actions contract issues and rerun runtime validation.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py`
- When to run: mandatory final step in stage-chain postflight after QA actions are validated.
- Inputs: `--actions <path>` and optional `--apply-log <path>`.
- Outputs: applied actions plus progress/stage-result/status-summary artifacts.
- Failure mode: apply failure, progress update failure, or status summary failure.
- Next action: inspect logs, fix blocking contract issues, rerun the stage-chain.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/stage_result.py`
- When to run: stage-chain postflight stage-result emission only (not operator/manual recovery command).
- Inputs: canonical postflight payload (`ticket`, `stage`, `result`, `scope-key`, `work-item-key`, evidence links).
- Outputs: canonical `aidd.stage_result.v1` at `aidd/reports/loops/<ticket>/<scope_key>/stage.qa.result.json`.
- Failure mode: non-zero exit on missing required args or invalid stage-result contract fields.
- Next action: fix postflight payload generation and rerun the stage-chain; do not switch to non-canonical loop runtime paths.

## Notes
- QA stage runs full tests per policy.

## Additional resources
- Contract schema: [CONTRACT.yaml](CONTRACT.yaml) (when: QA action/report requirements are unclear; why: verify mandatory fields before runtime validation and postflight).
