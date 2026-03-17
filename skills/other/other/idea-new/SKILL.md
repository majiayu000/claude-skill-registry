---
name: idea-new
description: Bootstraps a new feature ticket by setting active context, deriving `slug_hint`, and preparing PRD questions. Use when the idea stage starts for a new ticket.
argument-hint: $1 [note...]
lang: ru
prompt_version: 1.3.21
source_version: 1.3.21
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/idea-new/runtime/analyst_check.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Inputs: resolve `<ticket>`, parse `idea_note` from user text, and verify PRD/context artifacts are readable for idea stage.
2. Slug synthesis: generate a short LLM summary from `idea_note`, normalize it into kebab-case token (`[a-z0-9-]`, 2-6 words), and use it as internal `slug_hint`; if `idea_note` is empty, fallback to `<ticket>` token. Do not ask user for `slug_hint`.
3. Preflight: set active stage `idea` and active feature with `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py` and `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py <ticket> --slug-note "<generated-slug>"`.
4. Orchestration: build/update the rolling context pack `aidd/reports/context/<ticket>.pack.md` and run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/idea-new/runtime/analyst_check.py --ticket <ticket>`.
5. Run subagent `feature-dev-aidd:analyst`. First action: read the rolling context pack.
6. Postflight: if answers already exist, rerun `python3 ${CLAUDE_PLUGIN_ROOT}/skills/idea-new/runtime/analyst_check.py --ticket <ticket>` and sync PRD readiness status.
7. Output: return open questions (if any) and explicit next step `/feature-dev-aidd:researcher <ticket>`.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py`
- When to run: once ticket and idea note are parsed, before analyst execution.
- Inputs: `<ticket>` and generated `--slug-note <slug_hint>` derived from `idea_note`.
- Outputs: updated `aidd/docs/.active.json` (`ticket` + internal `slug_hint`) and PRD scaffold.
- Failure mode: non-zero exit when workspace paths/permissions are invalid.
- Next action: fix workspace issue, keep the same generated slug policy, rerun the command.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/idea-new/runtime/analyst_check.py`
- When to run: before/after analyst execution to validate PRD readiness and Q/A synchronization.
- Inputs: `--ticket <ticket>` and active workspace artifacts.
- Outputs: deterministic readiness status for idea-stage gate decisions.
- Failure mode: non-zero exit when required PRD fields or answer alignment are missing.
- Next action: update PRD/QA artifacts, then rerun the same validator.

## Notes
- Use the aidd-core question format.
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.

## Additional resources
- PRD template source: [templates/prd.template.md](templates/prd.template.md) (when: defining or validating required PRD structure; why: keep analyst output aligned with canonical sections).
