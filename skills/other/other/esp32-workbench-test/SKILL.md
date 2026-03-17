---
name: esp32-workbench-test
description: Test automation support — test progress tracking, human interaction requests, and activity log. Triggers on "test progress", "test session", "human interaction", "operator", "activity log", "test tracking".
---

# ESP32 Test Automation

Base URL: `http://192.168.0.87:8080`

## Test Progress Tracking

Test scripts can push live progress updates to the workbench web UI so operators can monitor test execution without a terminal.

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/test/update` | Push session start, step, result, or end |
| GET | `/api/test/progress` | Poll current test session state |

### Session Lifecycle

```bash
# 1. Start a test session
curl -X POST http://192.168.0.87:8080/api/test/update \
  -H 'Content-Type: application/json' \
  -d '{"spec": "iOS-Keyboard v1.0", "phase": "Phase 1", "total": 8}'

# 2. Update current test step
curl -X POST http://192.168.0.87:8080/api/test/update \
  -H 'Content-Type: application/json' \
  -d '{"current": {"id": "TC-001", "name": "WiFi Provisioning", "step": "Joining AP...", "manual": false}}'

# 3. Record a result
curl -X POST http://192.168.0.87:8080/api/test/update \
  -H 'Content-Type: application/json' \
  -d '{"result": {"id": "TC-001", "name": "WiFi Provisioning", "result": "PASS"}}'

# 4. End the session
curl -X POST http://192.168.0.87:8080/api/test/update \
  -H 'Content-Type: application/json' \
  -d '{"end": true}'

# Poll current progress
curl http://192.168.0.87:8080/api/test/progress
```

### Python Driver Methods

```python
wt.test_start("iOS-Keyboard v1.0", "Phase 1", total=8)
wt.test_step("TC-001", "WiFi Provisioning", "Joining AP...", manual=False)
wt.test_result("TC-001", "WiFi Provisioning", "PASS")
wt.test_end()
```

## Human Interaction

Some test steps require physical actions that cannot be automated — pressing a button, connecting a cable, power-cycling a device. The human interaction endpoint lets test scripts block until an operator confirms the action via the web UI.

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/human-interaction` | Block until operator confirms (or timeout) |
| GET | `/api/human/status` | Check if a request is pending |
| POST | `/api/human/done` | Operator confirms action complete |
| POST | `/api/human/cancel` | Operator cancels request |

### Examples

```bash
# Request operator action (blocks until Done/Cancel/timeout)
curl -X POST http://192.168.0.87:8080/api/human-interaction \
  -H 'Content-Type: application/json' \
  -d '{"message": "Connect USB cable to port 2 and click Done", "timeout": 120}'

# Check if a request is pending
curl http://192.168.0.87:8080/api/human/status

# Operator confirms
curl -X POST http://192.168.0.87:8080/api/human/done

# Operator cancels
curl -X POST http://192.168.0.87:8080/api/human/cancel
```

### Responses

| Outcome | Response |
|---------|----------|
| Confirmed | `{"ok": true, "confirmed": true}` |
| Cancelled | `{"ok": true, "confirmed": false}` |
| Timeout | `{"ok": true, "confirmed": false, "timeout": true}` |

Only one request can be pending at a time. A second request while one is active returns `409 Conflict`.

### Python Driver Method

```python
wt.human_interaction("Press the reset button and click Done", timeout=60)
# Returns True if confirmed, False if cancelled or timed out
```

## Activity Log

Timestamped log of all workbench operations — hotplug events, WiFi operations, enter-portal steps, human interactions.

### Endpoints

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/log` | Get activity log entries |

```bash
# Get all entries
curl -s http://192.168.0.87:8080/api/log | jq .

# Get entries since a timestamp
curl -s "http://192.168.0.87:8080/api/log?since=2025-01-01T00:00:00Z" | jq .
```

## Common Workflows

1. **Run automated test suite with progress tracking:**
   - `POST /api/test/update` with `spec`, `phase`, `total` — start session
   - For each test: update step → run test → record result
   - `POST /api/test/update` with `end: true` — end session
   - Operator monitors on web UI (progress bar, results with PASS/FAIL/SKIP badges)

2. **Test requiring physical action:**
   - `POST /api/human-interaction` with instruction message
   - Web UI shows pulsing orange modal with the message
   - Operator performs action, clicks Done
   - Test script continues

3. **Monitor workbench operations:**
   - `GET /api/log?since=<ts>` — poll for new activity entries
   - Useful for debugging enter-portal sequences and tracking what happened

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Human interaction returns 409 | Another request is pending — wait or cancel it |
| Test progress not showing in UI | Ensure a session was started with `spec`, `phase`, `total` |
| Activity log empty | No operations have been performed yet |
