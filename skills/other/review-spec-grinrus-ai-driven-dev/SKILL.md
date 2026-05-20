---
name: review-spec
description: Reviews plan and PRD, then gates readiness for implementation. Use when plan and PRD artifacts are ready for spec approval.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.0.25
source_version: 1.0.25
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/progress_cli.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-core/runtime/prd_review.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Set active stage `review-plan`, then `review-prd`; keep active feature in sync via canonical active-state runtime commands only.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-core/runtime/prd_review.py --ticket <ticket>` to refresh structured PRD report payload.
3. Gate PRD readiness with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/prd_check.py`; block on failure.
4. Use the existing rolling context pack as review input; do not invoke standalone context-pack builder scripts from this stage.
5. Run subagent `feature-dev-aidd:plan-reviewer`, then run subagent `feature-dev-aidd:prd-reviewer`.
6. Persist PRD review report with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-core/runtime/prd_review.py --ticket <ticket> --report aidd/reports/prd/<ticket>.json --require-ready` for READY-path validation.
7. Review-stage RLM policy: if RLM links are empty, the runtime performs bounded auto-heal (`rlm_links_build`, then finalize probe) and returns WARN attribution with evidence instead of terminal block when review can continue.
8. Report payload (`aidd/reports/prd/<ticket>.json|.pack.json`) is the source of truth for final verdict: READY is allowed only when `recommended_status=ready`; otherwise return WARN/BLOCKED with canonical next action (`/feature-dev-aidd:spec-interview <ticket>`).

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-core/runtime/prd_review.py`
- When to run: as canonical review-spec stage entrypoint before PRD approval decisions.
- Inputs: `--ticket <ticket>` plus active PRD/plan artifacts.
- Outputs: normalized PRD review report payload; verdict decisions use report payload (`recommended_status`) as source of truth.
- Failure mode: non-zero exit when review inputs are incomplete or report validation fails; RLM links-empty path is handled as bounded auto-heal then WARN attribution.
- Next action: fix missing artifacts/review findings or unresolved RLM prerequisites and rerun the CLI.

## Notes
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.

## Additional resources
- PRD review runtime: [../aidd-core/runtime/prd_review.py](../aidd-core/runtime/prd_review.py) (when: review-spec gate behavior is unclear; why: confirm report contract and status mapping).
