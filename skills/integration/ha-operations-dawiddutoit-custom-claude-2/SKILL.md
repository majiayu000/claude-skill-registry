---
name: ha-operations
description: |
  Interacts with Home Assistant via REST API for health checks, notifications, and service calls.
  Provides guidance for API access with long-lived tokens, sending notifications, calling services,
  and troubleshooting common issues. Use when checking HA health, sending HA notifications, calling
  HA services, or troubleshooting "Home Assistant returns 405", "HA health check failing", "can't
  access HA API", or "HA notifications not working".
Works with Home Assistant REST API, curl, long-lived access tokens, and notification services.
  Critical: HA only supports GET requests (HEAD returns 405 which is EXPECTED behavior).
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Home Assistant Operations

## Quick Start

Check if Home Assistant is healthy:

```bash
# ✅ CORRECT: Use GET request
curl -s https://ha.temet.ai/ | grep "Home Assistant"

# ❌ WRONG: HEAD returns 405 (but this is expected behavior, not an error!)
curl -I https://ha.temet.ai/
# Returns: HTTP/2 405 Method Not Allowed - THIS IS NORMAL
```

Send a notification:

```bash
source /Users/dawiddutoit/projects/play/network-infrastructure/.env

curl -X POST "${HA_BASE_URL}/api/services/notify/${HA_NOTIFY_SERVICE#*.}" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Test from infrastructure monitoring",
    "title": "Infrastructure Alert"
  }'
```

## When to Use

**Triggers:**
- "Interact with Home Assistant"
- "Call HA service"  
- "Send HA notification"
- "Check HA health"
- "Home Assistant returns 405"
- "HA health check failing"

## Key Concepts

### The 405 Situation

Home Assistant does NOT support HEAD requests. It returns `HTTP 405 Method Not Allowed` for HEAD, which is **EXPECTED and NORMAL behavior**.

**Correct Health Check:**
```bash
# ✅ Use GET and check content
curl -s https://ha.temet.ai/ --max-time 5 | grep "Home Assistant"
```

## Operations

### API Access

Create long-lived token in HA UI → Profile → Long-Lived Access Tokens

Store in .env:
```bash
HA_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
HA_BASE_URL=http://192.168.68.123:8123
HA_NOTIFY_SERVICE=notify.mobile_app_your_phone
```

### Send Notifications

```bash
curl -X POST "${HA_BASE_URL}/api/services/notify/${HA_NOTIFY_SERVICE#*.}" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Alert text", "title": "Title"}'
```

### Call Services

```bash
# General pattern
curl -X POST "${HA_BASE_URL}/api/services/<domain>/<service>" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "entity.name"}'

# Trigger automation
curl -X POST "${HA_BASE_URL}/api/services/automation/trigger" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.infrastructure_alert_handler"}'
```

### Read Entity States

```bash
# Specific entity
curl -s "${HA_BASE_URL}/api/states/sensor.temperature" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" | jq .

# All entities
curl -s "${HA_BASE_URL}/api/states" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" | jq .
```

## Supporting Files

| File | Purpose |
|------|---------|
| `references/api-endpoints.md` | Complete HA REST API endpoint reference |

## Requirements

- Home Assistant running at 192.168.68.123:8123
- Long-lived access token
- Environment variables: HA_BASE_URL, HA_ACCESS_TOKEN, HA_NOTIFY_SERVICE
- Tools: curl, jq (optional)

## Red Flags

- [ ] Do not use HEAD requests (always returns 405)
- [ ] Do not assume 405 means HA is broken
- [ ] Do not expose access tokens in logs
- [ ] Do not hardcode tokens in scripts (use .env)
- [ ] Do not skip token creation

## Common Issues

| Symptom | Cause | Fix |
|---------|-------|-----|
| HTTP 405 | Used HEAD instead of GET | Use GET |
| 401 Unauthorized | Invalid token | Verify token, recreate |
| 404 Not Found | Wrong entity_id | Check entity exists |
| Connection refused | HA not running | Check HA server |
| No notification | Wrong service name | Verify HA_NOTIFY_SERVICE |
