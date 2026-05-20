---
name: aidd-rlm
description: Owns shared RLM evidence workflow for subagents (slice, build, verify, finalize, pack). Use when preload roles require canonical RLM evidence operations.
lang: en
allowed-tools:
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_nodes_build.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_verify.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_links_build.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_jsonl_compact.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/reports_pack.py *)"
model: inherit
user-invocable: false
---

## Scope
- This skill is preload-only for subagents.
- Use it to keep RLM behavior consistent across agents without duplicating long instructions.
- Preload matrix v2 roles: `analyst`, `planner`, `plan-reviewer`, `prd-reviewer`, `researcher`, `reviewer`, `spec-interview-writer`, `tasklist-refiner`, `validator`.
- Do not preload for `implementer` or `qa`.

## Canonical command paths
- Slice (shared): `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py`
- RLM runtime entrypoints:
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_nodes_build.py`
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_verify.py`
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_links_build.py`
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_jsonl_compact.py`
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py`
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/reports_pack.py`

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py`
- When to run: when agent needs targeted evidence from existing RLM artifacts without full JSONL scans.
- Inputs: `--ticket <ticket>` with one or more `--query` tokens.
- Outputs: compact slice payload suitable for pack-first reasoning.
- Failure mode: non-zero exit when source artifacts are missing or query context is invalid.
- Next action: generate/repair missing RLM artifacts, then rerun slice query.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py`
- When to run: handoff/finalization path when `rlm_status` remains pending after stage-local bounded recovery.
- Inputs: `--ticket <ticket>` and optional bootstrap/recovery flags.
- Outputs: finalized RLM nodes/links/pack status with deterministic readiness metadata.
- Failure mode: non-zero exit on unresolved manifest/worklist integrity issues.
- Next action: fix upstream targets/worklist inconsistencies and rerun finalize.

## Fallback paths
- Use canonical Python runtime entrypoints only for new prompts/integrations.

## Evidence policy
- Read pack-first: `aidd/reports/research/<ticket>-rlm.pack.json`.
- Use slice queries for targeted context extraction.
- Avoid full JSONL reads unless pack/slice is insufficient.

## Additional resources
- Runtime finalize reference: [runtime/rlm_finalize.py](runtime/rlm_finalize.py) (when: finalize/handoff behavior is unclear; why: confirm canonical finalize flags and pending/ready transitions).
- Cross-skill stage contract: [../aidd-stage-research/SKILL.md](../aidd-stage-research/SKILL.md) (when: researcher stage orchestration and RLM ownership boundary needs clarification; why: keep shared/runtime and stage responsibilities split).
