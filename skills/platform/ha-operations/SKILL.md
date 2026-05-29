---
name: ha-operations
description: |
  Interact with Home Assistant in the network infrastructure setup. Provides guidance for
  API access, health checks, sending notifications, and calling services via REST API.
  Use when working with Home Assistant, checking HA health, sending HA notifications,
  calling HA services, or troubleshooting "Home Assistant returns 405", "HA health check
  failing", "can't access HA API", or "HA notifications not working". Covers the critical
  fact that HA only supports GET requests (HEAD returns 405 which is EXPECTED), HA is an
  external server at 192.168.68.123:8123 (not a Docker container), requires long-lived
  access tokens for API access, and is protected by Cloudflare Access (Google OAuth).
  Works with Home Assistant REST API, curl, and notification services.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# Home Assistant Operations

Interact with Home Assistant in your network infrastructure.

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

## Table of Contents

1. [When to Use This Skill](#1-when-to-use-this-skill)
2. [What This Skill Does](#2-what-this-skill-does)
3. [Instructions](#3-instructions)
   - 3.1 Understanding HA in This Infrastructure
   - 3.2 Health Check (GET, not HEAD)
   - 3.3 API Access with Long-Lived Token
   - 3.4 Sending Notifications
   - 3.5 Calling HA Services
   - 3.6 Reading Entity States
4. [Supporting Files](#4-supporting-files)
5. [Expected Outcomes](#5-expected-outcomes)
6. [Requirements](#6-requirements)
7. [Red Flags to Avoid](#7-red-flags-to-avoid)

## 1. When to Use This Skill

**Explicit Triggers:**
- "Interact with Home Assistant"
- "Call HA service"
- "Send HA notification"
- "Check HA health"
- "Access Home Assistant API"
- "Read HA entity state"

**Implicit Triggers:**
- Setting up infrastructure monitoring with HA integration
- Adding HA alerts to automation scripts
- Verifying HA is accessible via Caddy/Cloudflare
- Checking HA service status

**Debugging Triggers:**
- "Home Assistant returns 405"
- "HA health check failing"
- "Can't access HA API"
- "HA notifications not working"
- "405 Method Not Allowed from HA"

## 2. What This Skill Does

Provides comprehensive guidance for interacting with Home Assistant:

1. **Clarifies HA Architecture** - HA is external server at 192.168.68.123:8123 (not Docker container)
2. **Health Check Guidance** - Use GET requests (HEAD returns expected 405)
3. **API Access** - Long-lived token authentication via REST API
4. **Notification Sending** - Call notify services programmatically
5. **Service Calls** - Trigger HA automations and services
6. **Entity State Reading** - Query sensor/switch/light states

## 3. Instructions

### 3.1 Understanding HA in This Infrastructure

**Critical Facts:**

| Aspect | Detail |
|--------|--------|
| **Location** | External server at 192.168.68.123:8123 |
| **Container Status** | NOT a Docker container (separate HA installation) |
| **Access Paths** | Local: Caddy HTTPS:443 → 192.168.68.123:8123<br>Remote: Cloudflare Tunnel → 192.168.68.123:8123 |
| **Authentication** | Google OAuth (Cloudflare Access) for web UI<br>Long-lived token for API |
| **Domain** | https://ha.temet.ai |
| **HTTP Methods** | Supports GET, POST, not HEAD |

**Architecture Diagram:**

```
┌─────────────────────────────────────────────────────────────────┐
│                    LOCAL ACCESS (Home WiFi)                      │
│                                                                  │
│  Client → Caddy (HTTPS:443) → 192.168.68.123:8123 (HA Server)  │
│                                                                  │
│  ✅ Fast local access                                           │
│  ✅ Let's Encrypt certificate via Caddy                         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   REMOTE ACCESS (Internet)                       │
│                                                                  │
│  Client → Cloudflare → Tunnel → 192.168.68.123:8123 (HA)       │
│                                                                  │
│  ✅ Google OAuth required (Cloudflare Access)                   │
│  ✅ Secure tunnel (no exposed ports)                            │
└─────────────────────────────────────────────────────────────────┘
```

**What HA is NOT:**
- ❌ Not a Docker container in this infrastructure
- ❌ Not managed by docker-compose.yml
- ❌ Not on the same Docker network as Caddy/Pi-hole
- ❌ Not accessible via container name

### 3.2 Health Check (GET, not HEAD)

**The 405 Situation - READ THIS FIRST:**

Home Assistant **does NOT support HEAD requests**. It returns `HTTP 405 Method Not Allowed` for HEAD, which is **EXPECTED and NORMAL behavior**.

**Why this matters:**
- Many health check tools use HEAD requests (curl -I, monitoring systems)
- Seeing 405 does NOT mean HA is broken - it means HA is working correctly
- You MUST use GET requests to verify HA health

**Correct Health Check:**

```bash
# ✅ CORRECT: Use GET and check content
curl -s https://ha.temet.ai/ --max-time 5 | grep "Home Assistant"

# Expected output: HTML containing "Home Assistant"
```

**What NOT to do:**

```bash
# ❌ WRONG: This returns 405, which people misinterpret as failure
curl -I https://ha.temet.ai/

# Output: HTTP/2 405 Method Not Allowed
# Header: Allow: GET
# This is NORMAL - HA only accepts GET!
```

**From monitoring scripts:**

```bash
# This is how infrastructure-monitor.sh correctly checks HA
ha_response=$(curl -s "http://192.168.68.123:8123/" --max-time 5 2>/dev/null | head -1)
if echo "$ha_response" | grep -q "Home Assistant"; then
    echo "✅ Home Assistant: responding"
else
    echo "❌ Home Assistant: not responding"
fi
```

**Local vs Domain Access:**

```bash
# Direct to HA server (bypasses Caddy/Cloudflare)
curl -s "http://192.168.68.123:8123/" | grep "Home Assistant"

# Via Caddy (local network)
curl -s "https://ha.temet.ai/" | grep "Home Assistant"

# Via Cloudflare (requires authentication)
# Use browser or authenticated session
```

### 3.3 API Access with Long-Lived Token

**Create Long-Lived Access Token:**

1. Open Home Assistant web UI:
   - Local: http://192.168.68.123:8123
   - Domain: https://ha.temet.ai (requires Google OAuth)

2. Click your profile (bottom left)

3. Scroll to "Long-Lived Access Tokens"

4. Click "Create Token"

5. Name: "Infrastructure Monitoring" (or descriptive name)

6. Copy the token immediately (you won't see it again!)

**Store Token in .env:**

```bash
# Add to /Users/dawiddutoit/projects/play/network-infrastructure/.env
HA_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Test API Access:**

```bash
source /Users/dawiddutoit/projects/play/network-infrastructure/.env

# Get HA configuration
curl -s "${HA_BASE_URL}/api/config" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" | jq .

# Expected: JSON with HA configuration
```

**Common API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/` | GET | API status |
| `/api/config` | GET | HA configuration |
| `/api/states` | GET | All entity states |
| `/api/states/<entity_id>` | GET | Specific entity state |
| `/api/services/<domain>/<service>` | POST | Call service |
| `/api/events/<event_type>` | POST | Fire event |

### 3.4 Sending Notifications

**Required Environment Variables:**

```bash
# In .env file
HA_NOTIFICATIONS_ENABLED=true
HA_BASE_URL=http://192.168.68.123:8123
HA_ACCESS_TOKEN=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
HA_NOTIFY_SERVICE=notify.mobile_app_your_phone
```

**Find Your Notification Service:**

Open HA: Developer Tools → Services, filter for "notify". Common services:
- `notify.mobile_app_your_phone` - HA Companion mobile app
- `notify.persistent_notification` - HA UI notifications

**Basic Notification:**

```bash
source /Users/dawiddutoit/projects/play/network-infrastructure/.env
SERVICE_NAME="${HA_NOTIFY_SERVICE#*.}"

curl -X POST "${HA_BASE_URL}/api/services/notify/${SERVICE_NAME}" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Infrastructure alert: Tunnel reconnected",
    "title": "Network Infrastructure",
    "data": {"priority": "high", "tag": "infrastructure"}
  }'
```

**See `examples/notification-examples.md` for:**
- Notifications with actions (interactive buttons)
- Priority levels and critical alerts
- Tags for updating existing notifications
- Shell script integration patterns
- Error handling and rate limiting

### 3.5 Calling HA Services

**Basic Service Call Pattern:**

```bash
source /Users/dawiddutoit/projects/play/network-infrastructure/.env

# General pattern
curl -X POST "${HA_BASE_URL}/api/services/<domain>/<service>" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "entity.name"}'

# Example: Trigger automation
curl -X POST "${HA_BASE_URL}/api/services/automation/trigger" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.infrastructure_alert_handler"}'
```

**See `examples/service-call-examples.md` for:**
- Light control (on/off, brightness, color)
- Switch/climate/media player control
- Automation/script execution
- Shell commands and system services
- Bulk operations and error handling

### 3.6 Reading Entity States

**Get Entity State:**

```bash
source /Users/dawiddutoit/projects/play/network-infrastructure/.env

# Specific entity
curl -s "${HA_BASE_URL}/api/states/sensor.temperature" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" | jq .

# All entities
curl -s "${HA_BASE_URL}/api/states" \
  -H "Authorization: Bearer ${HA_ACCESS_TOKEN}" | jq .
```

**See `references/api-endpoints.md` for:**
- Complete endpoint reference
- State filtering with jq
- Event endpoints and error logging
- Response codes and authentication details

## 4. Supporting Files

| File | Purpose |
|------|---------|
| `references/api-endpoints.md` | Complete HA REST API endpoint reference |
| `examples/notification-examples.md` | Notification payload examples with actions |
| `examples/service-call-examples.md` | Common service call patterns |
| `scripts/ha-health-check.sh` | Standalone HA health check script |

## 5. Expected Outcomes

**Success Indicators:**

**Health Check Success:**
```bash
curl -s https://ha.temet.ai/ | grep "Home Assistant"
# Output: <title>Home Assistant</title>
# Exit code: 0
```

**API Access Success:**
```bash
curl -s "${HA_BASE_URL}/api/" -H "Authorization: Bearer ${HA_ACCESS_TOKEN}"
# Output: {"message": "API running."}
# Exit code: 0
```

**Notification Success:**
```bash
curl -X POST "${HA_BASE_URL}/api/services/notify/mobile_app_phone" ...
# Output: [] (empty array means success)
# Exit code: 0
# Phone receives notification within seconds
```

**Service Call Success:**
```bash
curl -X POST "${HA_BASE_URL}/api/services/light/turn_on" ...
# Output: [{"entity_id": "light.living_room", "state": "on", ...}]
# Exit code: 0
# Light turns on
```

**Common Failure Patterns:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| `HTTP 405 Method Not Allowed` | Used HEAD instead of GET | Use GET request for health checks |
| `401 Unauthorized` | Invalid/missing access token | Verify token in .env, recreate if needed |
| `404 Not Found` | Wrong endpoint or entity_id | Check API documentation, verify entity exists |
| `Connection refused` | HA not running | Check HA server status at 192.168.68.123 |
| `Timeout` | Network issues or HA slow | Check network, verify HA responsive |
| No notification received | Wrong service name or token | Verify HA_NOTIFY_SERVICE and HA_ACCESS_TOKEN |

## 6. Requirements

**Environment:**
- Home Assistant running at 192.168.68.123:8123
- Network connectivity to HA server
- Access to .env file with credentials

**Configuration (.env):**
- `HA_BASE_URL=http://192.168.68.123:8123`
- `HA_ACCESS_TOKEN=<long-lived-token>`
- `HA_NOTIFY_SERVICE=notify.<service-name>` (for notifications)
- `HA_NOTIFICATIONS_ENABLED=true` (for monitoring integration)

**Tools:**
- curl (for API requests)
- jq (optional, for JSON parsing)
- grep (for health checks)

**Access:**
- Web UI: https://ha.temet.ai (requires Google OAuth via Cloudflare Access)
- API: Direct to 192.168.68.123:8123 (requires long-lived token)

## 7. Red Flags to Avoid

- [ ] Do not use HEAD requests for HA health checks (always returns 405)
- [ ] Do not assume 405 means HA is broken (it's expected for HEAD)
- [ ] Do not treat HA as a Docker container in this infrastructure
- [ ] Do not try to access HA via Docker network/container name
- [ ] Do not forget to source .env before using environment variables
- [ ] Do not expose access tokens in logs or error messages
- [ ] Do not hardcode tokens in scripts (use .env)
- [ ] Do not skip token creation (API access requires authentication)
- [ ] Do not use wrong service name format (notify.service, not just service)
- [ ] Do not ignore authentication requirements (both OAuth and API token)

## Notes

**Key Takeaways:**
1. **405 is normal** - HA only supports GET, not HEAD
2. **External server** - Not a Docker container, runs separately at 192.168.68.123:8123
3. **Two auth methods** - Google OAuth for web UI, long-lived token for API
4. **Two access paths** - Local via Caddy (fast), remote via Cloudflare Tunnel (secure)
5. **Use GET for health** - Always use GET requests to verify HA is responding

**Integration with Monitoring:**
- `infrastructure-monitor.sh` uses GET to check HA health
- Sends infrastructure alerts to HA via notify service
- Properly handles 405 as expected response

**Related Skills:**
- `infrastructure-health-check` - Uses this skill for HA health verification
- `infrastructure-monitoring-setup` - Configures HA notification integration

**Reference Documentation:**
- Main project CLAUDE.md: `/Users/dawiddutoit/projects/play/network-infrastructure/CLAUDE.md`
- Monitoring setup: `/Users/dawiddutoit/projects/play/network-infrastructure/docs/monitoring-setup.md`
- HA API docs: https://developers.home-assistant.io/docs/api/rest/
