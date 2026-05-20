---
name: aidd-docio
description: Owns shared DocIO runtime for markdown slicing/patching, actions validation/apply, and context-map expansion. Use when stage skills need canonical DocIO operations.
lang: en
model: inherit
user-invocable: false
---

## Scope
- This skill owns shared DocIO runtime entrypoints.
- Stage skills consume these APIs for preflight/postflight and deterministic document updates.
- Flow-state orchestration remains in `feature-dev-aidd:aidd-core` and `feature-dev-aidd:aidd-loop`.

## Canonical shared Python entrypoints
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/md_slice.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/md_patch.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_validate.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/context_map_validate.py`
- `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/context_expand.py`

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/md_slice.py`
- When to run: when stage or subagent needs bounded section reads instead of full-file scans.
- Inputs: source markdown path with heading/line selectors.
- Outputs: deterministic excerpt payload for pack-first evidence workflows.
- Failure mode: non-zero exit on missing file, invalid selectors, or malformed markdown boundaries.
- Next action: fix selectors/source path and rerun the same slice command.

### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/aidd-docio/runtime/actions_apply.py`
- When to run: stage-chain postflight after validated `*.actions.json` is available.
- Inputs: `--actions <path>` with optional apply-log paths and stage context.
- Outputs: applied updates, progress synchronization, and downstream stage artifacts.
- Failure mode: non-zero exit on schema violations, write failures, or boundary guard blocks.
- Next action: inspect apply log, fix action payload/root cause, then rerun stage-chain postflight.

## Ownership guard
- DocIO-facing runtime modules must be implemented under `skills/aidd-docio/runtime/*`.
- Consumers should reference `skills/aidd-docio/runtime/*` as canonical paths.

## Additional resources
- [references/read-write-maps.md](references/read-write-maps.md) (when: readmap/writemap behavior is in question; why: align map validation and expansion semantics).
- [references/actions-flow.md](references/actions-flow.md) (when: actions schema/apply behavior is unclear; why: follow validator-to-apply lifecycle).
