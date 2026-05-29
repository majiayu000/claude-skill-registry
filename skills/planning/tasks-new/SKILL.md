---
name: tasks-new
description: Derives or refines tasklist items from PRD, plan, and spec artifacts. Use when tasklist stage prepares implementation-ready work items.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.1.23
source_version: 1.1.23
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(cat *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/tasks-new/runtime/tasks_new.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Inputs: resolve active feature and verify PRD/plan/spec artifacts needed for tasklist generation.
2. Preflight: set active stage `tasklist` and active feature.
3. Orchestration: run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/tasks-new/runtime/tasks_new.py --ticket <ticket>`, then gate PRD readiness with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py`.
4. Use the existing rolling context pack as input evidence; do not invoke standalone context-pack builder scripts from this stage.
5. Run subagent `feature-dev-aidd:tasklist-refiner` (internal orchestration role). First action: read the rolling context pack.
6. Postflight: validate via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasklist_check.py` and update `aidd/docs/tasklist/<ticket>.md` when needed.
7. Output: return the output contract and explicit next step `/feature-dev-aidd:implement <ticket>`.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/tasks-new/runtime/tasks_new.py`
- When to run: as canonical tasklist stage entrypoint before implement phase.
- Inputs: `--ticket <ticket>` and current PRD/plan/spec artifacts.
- Outputs: normalized tasklist structure and stage readiness signal.
- Failure mode: non-zero exit when required artifacts are missing or tasklist contract checks fail.
- Next action: fix source artifacts/tasklist issues and rerun tasklist orchestration.

## Notes
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.

## Additional resources
- Tasklist template source: [templates/tasklist.template.md](templates/tasklist.template.md) (when: generating or normalizing tasklist sections; why: keep iteration/handoff structure aligned with canonical template).
