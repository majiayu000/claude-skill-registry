---
name: plan-new
description: Drafts implementation plan from ready PRD and research artifacts. Use when PRD and research gates pass and plan stage should start.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.1.16
source_version: 1.1.16
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/plan-new/runtime/research_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Set active stage `plan` and active feature.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/plan-new/runtime/research_check.py --ticket <ticket>`.
3. Gate readiness with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py` and `python3 ${CLAUDE_PLUGIN_ROOT}/skills/plan-new/runtime/research_check.py`; block if either fails.
4. Use the existing rolling context pack as input evidence; do not invoke standalone context-pack builder scripts from this stage.
5. Run subagent `feature-dev-aidd:planner`, then run subagent `feature-dev-aidd:validator`; keep updates within plan artifacts and canonical stage outputs.
6. Update `aidd/docs/plan/<ticket>.md` and return the output contract.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/plan-new/runtime/research_check.py`
- When to run: before planning to enforce research-readiness gate.
- Inputs: `--ticket <ticket>` and current PRD/research artifacts.
- Outputs: deterministic readiness verdict for plan stage.
- Failure mode: non-zero exit if research status/artifacts do not satisfy gate policy.
- Next action: resolve research blockers and rerun the gate check.

## Notes
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.

## Additional resources
- Plan template source: [templates/plan.template.md](templates/plan.template.md) (when: generating or normalizing plan structure; why: ensure planner/validator outputs follow canonical sections).
