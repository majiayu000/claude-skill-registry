---
name: service
description: Manage UnaMentis services via USM API (never via bash kill commands)
---

# /service - Server Service Management

## Purpose

Manages UnaMentis services through the USM (UnaMentis Server Manager) API. This skill enforces the mandate to NEVER use bash commands like `pkill` for service control.

**Critical Rule:** ALWAYS use USM API (port 8787). NEVER use bash kill commands.

> **Note:** A legacy USM app exists at port 8767 but is deprecated. Always use port 8787.

## Usage

```
/service status              # Show status of all services
/service status <service>    # Show status of specific service
/service start <service>     # Start a service
/service stop <service>      # Stop a service
/service restart <service>   # Restart a service
/service restart-all         # Restart all services
/service logs <service>      # View recent logs for a service
```

## Available Services

| Service ID | Description | Port |
|------------|-------------|------|
| `postgresql` | PostgreSQL Database | 5432 |
| `log-server` | Log Server | 8765 |
| `management-api` | Management API | 8766 |
| `web-server` | Operations Console | 3000 |
| `web-client` | Web Client | 3001 |
| `ollama` | Ollama LLM | 11434 |

## Workflow

### 1. Check USM Running
```bash
curl -s http://localhost:8787/api/health
```
If USM is not running, inform user to start the USM menu bar app.

### 2. Execute Service Operation

**Status check:**
```bash
curl -s http://localhost:8787/api/services
curl -s http://localhost:8787/api/services/{service_id}
```

**Start service:**
```bash
curl -X POST http://localhost:8787/api/services/{service_id}/start
```

**Stop service:**
```bash
curl -X POST http://localhost:8787/api/services/{service_id}/stop
```

**Restart service:**
```bash
curl -X POST http://localhost:8787/api/services/{service_id}/restart
```

### 3. Wait for Health
After start/restart, poll health until ready:
```bash
curl -s http://localhost:8787/api/services/{service_id}
```
Wait until status shows "running" (up to 30 seconds).

### 4. Verify Active (for restarts)
After restarting a service with code changes:
- Make an API call to test the endpoint
- Check logs for expected startup messages
- Confirm behavioral changes are active

## Success Criteria

- Service transitions to expected state
- Health check passes
- No error messages in response

## Examples

**Check all services:**
```
User: /service status
Claude: Checking service status via USM API...

Services:
- postgresql: running (port 5432)
- log-server: running (port 8765)
- management-api: running (port 8766)
- web-server: stopped
- web-client: stopped
- ollama: running (port 11434)
```

**Restart management API:**
```
User: /service restart management-api
Claude: Restarting management-api via USM API...

Stop: OK
Start: OK
Health check: PASSED (ready in 2.3s)

management-api is now running on port 8766
```

**Restart with verification:**
```
User: I changed the latency API endpoint, restart the server
Claude: Restarting management-api via USM API...

Stop: OK
Start: OK
Health check: PASSED

Verifying code changes active...
- Testing endpoint: GET /api/latency-tests/status
- Response confirms new field present

Code changes are active and working.
```

## Why USM API?

Using bash commands like `pkill` or `killall`:
- Can leave services in inconsistent states
- Doesn't trigger proper cleanup/shutdown
- Bypasses the service manager's state tracking
- May kill unrelated processes

The USM API provides:
- Clean shutdown sequences
- Proper state management
- Health monitoring
- Dependency handling

## Exception: Restarting USM Itself

The ONE exception to the "never use pkill" rule is restarting the USM (Server Manager) app itself. Since USM cannot restart itself via its own API, you must use:

```bash
pkill -f "USM.app" 2>/dev/null
```

Then relaunch USM manually. This is documented in `server/server-manager/FRESH_SESSION_TASKS.md`.
