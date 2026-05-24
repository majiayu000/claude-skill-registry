---
name: researcher
description: Generates or refreshes research artifacts and RLM evidence for a ticket. Use when research stage should produce or update canonical RLM outputs.
argument-hint: $1 [note...] [--paths path1,path2] [--keywords kw1,kw2] [--note text]
lang: ru
prompt_version: 1.2.34
source_version: 1.2.34
allowed-tools:
  - Read
  - Edit
  - Write
  - Glob
  - "Bash(rg *)"
  - "Bash(sed *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/researcher/runtime/research.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_feature.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/set_active_stage.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasks_derive.py *)"
model: inherit
disable-model-invocation: true
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core`.

## Steps
1. Set active feature and stage `research`.
2. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/researcher/runtime/research.py --ticket <ticket> --auto`.
3. Re-run the same entrypoint with optional overrides (`--paths`, `--keywords`, `--note`) when targeted refresh is needed.
4. Validate RLM outputs (`*-rlm-targets.json`, `*-rlm-manifest.json`, `*-rlm.worklist.pack.json`, optional `*-rlm.pack.json`).
5. Run subagent `feature-dev-aidd:researcher`. First action: read RLM pack/worklist.
6. In `--auto` mode run bounded canonical finalize recovery once (`rlm_finalize --bootstrap-if-missing`) from stage runtime.
7. If RLM is still pending after auto recovery, return deterministic pending reason + explicit next action (`python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py --ticket <ticket>`) and append research handoff via `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-flow-state/runtime/tasks_derive.py --source research --append`.
8. Return the output contract with explicit next step (`/feature-dev-aidd:plan-new <ticket>` when stage handoff is ready).

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/researcher/runtime/research.py`
- When to run: always as canonical researcher pipeline entrypoint.
- Inputs: `--ticket <ticket>` with optional path/keyword/note overrides.
- Outputs: research artifacts, stage status, and RLM readiness/handoff markers (`rlm_status`, `rlm_pack_status`).
- Failure mode: non-zero exit when required inputs/artifacts are missing or RLM artifact generation fails.
- Next action: fix missing inputs/paths, rerun this entrypoint; in auto mode finalize/bridge runs once, then pending outcomes include deterministic `reason_code` + `next_action`.

## Notes
- Planning stage: `AIDD:ACTIONS_LOG: n/a`.

## Migration policy
- Legacy pre-RLM research context/targets artifacts are ignored by runtime/gates.
- For old workspace state, rerun:
  `python3 ${CLAUDE_PLUGIN_ROOT}/skills/researcher/runtime/research.py --ticket <ticket> --auto`.
- If `rlm_status` remains `pending` after bounded auto recovery, hand off to shared owner:
  `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py --ticket <ticket>`.

## Additional resources
- Research template source: [templates/research.template.md](templates/research.template.md) (when: drafting or reviewing `aidd/docs/research/<ticket>.md`; why: keep artifact shape aligned with canonical workspace template).
- Shared RLM owner skill: [../aidd-rlm/SKILL.md](../aidd-rlm/SKILL.md) (when: `rlm_status` is not `ready` or RLM pack is missing; why: run canonical shared RLM API outside stage-local orchestration).
