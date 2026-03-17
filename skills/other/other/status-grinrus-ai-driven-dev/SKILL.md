---
name: status
description: Generates consolidated ticket status summary and key artifact pointers. Use when checking current stage state or handoff readiness.
argument-hint: [$1]
lang: ru
prompt_version: 1.0.8
source_version: 1.0.8
allowed-tools:
  - Read
  - "Bash(rg *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/status/runtime/status.py *)"
  - "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/skills/status/runtime/index_sync.py *)"
model: inherit
disable-model-invocation: false
user-invocable: true
---

Follow `feature-dev-aidd:aidd-core` and `feature-dev-aidd:aidd-loop`.

## Steps
1. Run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/status/runtime/status.py --ticket <ticket>` for the canonical stage entrypoint.
2. If index data is missing or stale, run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/status/runtime/index_sync.py --ticket <ticket>`.
3. Return the output contract and the status summary.

## Command contracts
### `python3 ${CLAUDE_PLUGIN_ROOT}/skills/status/runtime/status.py`
- When to run: canonical status command for read-only ticket summary.
- Inputs: optional `--ticket <ticket>` (falls back to active ticket when available).
- Outputs: consolidated stage/status snapshot and artifact pointers.
- Failure mode: non-zero exit when ticket resolution or index/report reads fail.
- Next action: refresh index or fix missing ticket context, then rerun status runtime.

## Notes
- Loop stage: set `AIDD:ACTIONS_LOG` to the most recent `*.actions.json` under `aidd/reports/actions/<ticket>/...` (use `rg` if needed).

## Additional resources
- Runtime implementation: [runtime/status.py](runtime/status.py) (when: status aggregation behavior needs debugging; why: verify ticket resolution and output fields).
