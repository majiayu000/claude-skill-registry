---
name: aidd-stage-research
description: Defines stage-specific research contract for subagent evidence reading and handoff behavior. Use when researcher subagent stage rules are needed.
lang: en
model: inherit
user-invocable: false
---

## Scope
- Preload-only reference for `feature-dev-aidd:researcher` subagent.
- Defines stage behavior for research content work in the RLM-only pipeline.
- Keeps stage rules separate from the user-invocable `researcher` command skill.

## Stage contract
- `skills/researcher/SKILL.md` owns orchestration only (state sync, pipeline run, explicit subagent call, handoff).
- `agents/researcher.md` owns content updates (`aidd/docs/research/<ticket>.md`) based on existing evidence.
- Subagent must not run shared RLM owner internals directly (`rlm_nodes_build.py`, `rlm_links_build.py`, `rlm_finalize.py`).
- Stage runtime may run bounded canonical finalize recovery once in `--auto` mode; manual recovery paths remain outside subagent scope.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py`
- When to run: for bounded evidence lookup during researcher subagent analysis.
- Inputs: ticket/query tuple for targeted code-artifact context extraction.
- Outputs: slice evidence blocks suitable for research document updates.
- Failure mode: non-zero exit on missing pack/worklist artifacts or invalid query.
- Next action: surface blocker and handoff to RLM owner flow, then rerun slice when artifacts are ready.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py`
- When to run: handoff-only path when stage runtime reports pending RLM readiness after bounded auto recovery.
- Inputs: `--ticket <ticket>` from deterministic pending output.
- Outputs: finalized RLM readiness state (`ready` or pending with reason code).
- Failure mode: non-zero exit when upstream targets/manifest/worklist integrity is broken.
- Next action: resolve upstream integrity issues and rerun finalize via shared owner flow.

## Evidence policy
- Read pack-first: `aidd/reports/research/<ticket>-rlm.pack.json`.
- If pack is missing, read `*-rlm.worklist.pack.json` and return BLOCKED with explicit handoff.
- Use slice for targeted evidence only:
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_slice.py --ticket <ticket> --query "<token>"`.
- Avoid full JSONL scans unless pack/worklist is insufficient.

## Handoff policy
- When `rlm_status` is not ready, return BLOCKED with deterministic next action:
  - `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-rlm/runtime/rlm_finalize.py --ticket <ticket>`.
- Pending output must include deterministic `reason_code` + `next_action` and append research handoff tasks.
- When evidence is ready, update research document and return READY with next stage command hint.

## Additional resources
- Stage command owner: [../researcher/SKILL.md](../researcher/SKILL.md) (when: researcher stage orchestration order is unclear; why: keep stage entrypoint behavior aligned with no-fork command contract).
- Shared RLM owner: [../aidd-rlm/SKILL.md](../aidd-rlm/SKILL.md) (when: pending/finalize ownership boundaries are unclear; why: enforce explicit handoff from stage to shared RLM runtime owner).
