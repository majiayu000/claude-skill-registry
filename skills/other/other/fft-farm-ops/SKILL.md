---
name: fft-farm-ops
description: Operate the farm bridge through ledger reads and IPC action requests, using main-chat-only control flows and safety guardrails.
---

# FFT Farm Ops

Use this skill for farm state awareness and operational actions routed through the FFT_nano farm bridge.

## Guardrails

- Never run destructive git commands unless explicitly requested.
- Preserve unrelated worktree changes.
- Keep write operations main-chat-only.
- Use main/admin chat only for any operational control action.
- Never run destructive shell commands against hosts, containers, or Home Assistant.

## Read Farm State

- Primary status file: `/workspace/farm-state/current.json`
- Alert snapshot: `/workspace/farm-state/alerts.json`
- Device inventory: `/workspace/farm-state/devices.json`
- Calendar snapshot: `/workspace/farm-state/calendar.json`
- Time series: `/workspace/farm-state/telemetry.ndjson`

Read `current.json` first. Treat `stale: true` as degraded connectivity and avoid risky recommendations.

## Submit Actions

Write request files into `/workspace/ipc/actions/` with unique names like:

- `act_<unix_ts>_<rand>.json`

Request format:

```json
{
  "type": "farm_action",
  "action": "ha_call_service",
  "params": {
    "domain": "switch",
    "service": "turn_on",
    "data": { "entity_id": "switch.irrigation_north" }
  },
  "requestId": "act_1707830400_abc"
}
```

## Poll Action Results

Read `/workspace/ipc/action_results/<requestId>.json` until available.

Result format:

```json
{
  "requestId": "act_1707830400_abc",
  "status": "success",
  "result": {},
  "executedAt": "2026-02-13T10:30:01Z"
}
```

If `status` is `error`, surface the exact error and propose the safest next step.

## Action Allowlist

Only use allowlisted actions:

- `ha_get_status`
- `ha_call_service`
- `ha_set_entity`
- `ha_restart`
- `ha_apply_dashboard`
- `ha_capture_screenshot`
- `farm_state_refresh`

## Alert Interpretation

- Critical alerts: prioritize immediate stabilization actions and ask for confirmation before control changes.
- Warning alerts: recommend monitored corrective actions.
- Normal state: suggest optimization and preventative maintenance.
- Always include context from `timeOfDay`, `season`, and weather-related states.
