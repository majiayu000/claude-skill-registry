---
name: spec-interview
description: Collects missing spec inputs and synchronizes answers into `spec.yaml`. Use when review-spec leaves unresolved specification fields.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.0.15
source_version: 1.0.15
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - AskUserQuestionTool
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(cat *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-interview/runtime/spec_interview.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Set active stage `spec-interview` and active feature.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-interview/runtime/spec_interview.py --ticket <ticket>`.
3. Run subagent `feature-dev-aidd:spec-interview-writer`.
4. Use `AskUserQuestionTool` to gather missing spec details; update `aidd/docs/spec/<ticket>.spec.yaml`.
5. If answers arrive, sync them into the spec and `AIDD:OPEN_QUESTIONS`/`AIDD:DECISIONS` as needed.
6. Return the output contract and next step `/feature-dev-aidd:tasks-new <ticket>`.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/spec-interview/runtime/spec_interview.py`
- When to run: as canonical spec interview entrypoint after review-spec and before tasklist derivation.
- Inputs: `--ticket <ticket>` with current PRD/plan context and optional notes.
- Outputs: updated `spec.yaml`, synchronized open questions/decisions, and stage status.
- Failure mode: non-zero exit when required source artifacts are missing or spec contract is violated.
- Next action: gather missing inputs/answers, then rerun the same command.

## Notes
- Use the aidd-core question format.
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.
- Canonical stage name: `spec-interview` (legacy alias `spec` normalizes to `spec-interview`).

## Additional resources
- Spec template source: [templates/spec.template.yaml](templates/spec.template.yaml) (when: creating or reconciling spec structure; why: keep generated `spec.yaml` aligned with canonical schema).
