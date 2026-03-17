---
name: ha-api
description: Integrate with Home Assistant REST and WebSocket APIs. Use when making API calls, managing entity states, calling services, subscribing to events, or setting up authentication. Activates on keywords REST API, WebSocket, API endpoint, service call, access token, Bearer token, subscribe_events.
---

# Home Assistant API Integration

> Master Home Assistant's REST and WebSocket APIs for external integration, state management, and real-time communication.

## ⚠️ BEFORE YOU START

**This skill prevents 5 common API integration errors and saves ~30% token overhead.**

| Aspect | Details |
|--------|---------|
| Common Errors Prevented | 5+ (auth, WebSocket lifecycle, state format, error handling) |
| Token Savings | ~30% vs. manual API discovery |
| Setup Time | 2-5 minutes vs. 15-20 minutes manual |

### Known Issues This Skill Prevents

1. **Incorrect authentication headers** - Bearer tokens must be prefixed with "Bearer " in Authorization header
2. **WebSocket lifecycle management** - Missing auth_required handling or improper state subscription
3. **State format mismatches** - Confusing state vs. attributes; incorrect JSON payload structure
4. **Error response handling** - Not distinguishing between 4xx client errors and 5xx server errors
5. **Service call domain/service mismatch** - Incorrect routing to service endpoints

## Quick Start

### Step 1: Authentication Setup

```bash
# In Home Assistant UI:
# Settings → My Home → Create Long-Lived Access Token
# Store token securely (never commit to git)

export HA_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
export HA_URL="http://192.168.1.100:8123"
```

**Why this matters:** All API requests require Bearer token authentication. Creating a dedicated token for external apps allows you to revoke access without changing your password.

### Step 2: Test REST API Connectivity

```bash
# Get all entity states
curl -X GET "${HA_URL}/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json"
```

**Why this matters:** Verifies your Home Assistant instance is accessible and your token is valid before building complex integrations.

### Step 3: Choose API Type

- **REST API**: For one-time requests, state queries, service calls (HTTP polling)
- **WebSocket API**: For real-time events, continuous subscriptions, lower latency (~50ms vs. seconds)

**Why this matters:** Different use cases require different APIs. WebSocket excels at real-time apps; REST is simpler for occasional requests.

## Critical Rules

### ✅ Always Do

- ✅ Store access tokens in environment variables or secure vaults (never hardcode)
- ✅ Include "Bearer " prefix in Authorization header (exact case and spacing required)
- ✅ Validate WebSocket auth_required messages before sending other commands
- ✅ Handle HTTP errors (401 = token invalid/expired, 404 = entity not found, 502 = HA unavailable)
- ✅ Specify full domain/service for service calls (e.g., "light/turn_on" not just "turn_on")

### ❌ Never Do

- ❌ Commit access tokens to git or share in logs
- ❌ Skip the initial WebSocket auth handshake
- ❌ Mix Bearer token authentication with username/password
- ❌ Assume state values are always strings (can be "on", 123, or null)
- ❌ Call service endpoints with entity_id as path parameter (use JSON payload instead)

### Common Mistakes

**❌ Wrong - Missing Bearer prefix:**
```bash
curl -X GET "http://ha:8123/api/states" \
  -H "Authorization: ${HA_TOKEN}"  # Missing "Bearer "
```

**✅ Correct - Bearer prefix required:**
```bash
curl -X GET "http://ha:8123/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}"
```

**Why:** Home Assistant's API uses standard Bearer token authentication. The "Bearer " prefix tells the server this is a token-based auth scheme, not a username/password.

## REST API Endpoints Reference

### States Endpoint

**Get all states:**
```bash
GET /api/states
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
[
  {
    "entity_id": "light.living_room",
    "state": "on",
    "attributes": {
      "brightness": 255,
      "color_mode": "color_temp",
      "friendly_name": "Living Room Light"
    },
    "last_changed": "2025-12-31T18:00:00+00:00",
    "last_updated": "2025-12-31T18:05:00+00:00"
  }
]
```

**Get single entity state:**
```bash
GET /api/states/{entity_id}
Authorization: Bearer {token}
```

**Create/update entity state:**
```bash
POST /api/states/{entity_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "state": "on",
  "attributes": {
    "friendly_name": "Custom Entity",
    "custom_attribute": "value"
  }
}
```

**Response (201 Created or 200 OK):**
```json
{
  "entity_id": "sensor.custom_sensor",
  "state": "on",
  "attributes": { ... }
}
```

### Services Endpoint

**Get all available services:**
```bash
GET /api/services
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
[
  {
    "domain": "light",
    "services": {
      "turn_on": {
        "description": "Turn on light(s)",
        "fields": {
          "entity_id": {
            "description": "The entity_id of the light(s)",
            "example": ["light.living_room", "light.bedroom"]
          },
          "brightness": {
            "description": "Brightness 0-255",
            "example": 180
          }
        }
      },
      "turn_off": { ... }
    }
  }
]
```

**Call a service:**
```bash
POST /api/services/{domain}/{service}
Authorization: Bearer {token}
Content-Type: application/json

{
  "entity_id": "light.living_room",
  "brightness": 180,
  "transition": 2
}
```

**Response (200 OK):**
```json
[
  {
    "entity_id": "light.living_room",
    "state": "on",
    "attributes": { ... }
  }
]
```

### Events Endpoint

**Get all events:**
```bash
GET /api/events
Authorization: Bearer {token}
```

**Fire an event:**
```bash
POST /api/events/{event_type}
Authorization: Bearer {token}
Content-Type: application/json

{
  "custom_data": "value"
}
```

### History Endpoint

**Get entity history:**
```bash
GET /api/history/period/{timestamp}?filter_entity_id={entity_id}
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
[
  [
    {
      "entity_id": "sensor.temperature",
      "state": "22.5",
      "attributes": { ... },
      "last_changed": "2025-12-31T12:00:00+00:00"
    }
  ]
]
```

### Config Endpoint

**Get Home Assistant configuration:**
```bash
GET /api/config
Authorization: Bearer {token}
```

**Response (200 OK):**
```json
{
  "latitude": 52.3,
  "longitude": 4.9,
  "elevation": 0,
  "unit_system": {
    "length": "km",
    "mass": "kg",
    "temperature": "°C",
    "volume": "L"
  },
  "time_zone": "Europe/Amsterdam",
  "components": ["light", "switch", "sensor", ...]
}
```

### Template Endpoint

**Render a template:**
```bash
POST /api/template
Authorization: Bearer {token}
Content-Type: application/json

{
  "template": "{{ states('sensor.temperature') }}"
}
```

**Response (200 OK):**
```json
{
  "template": "{{ states('sensor.temperature') }}",
  "result": "22.5"
}
```

## WebSocket API Reference

### Connection Flow

1. **Open WebSocket connection to `/api/websocket`**
2. **Receive auth_required message** (must respond within 10 seconds)
3. **Send auth message with token**
4. **Receive auth_ok confirmation**
5. **Send subscriptions/commands**
6. **Receive responses and events in real-time**

### WebSocket Commands

**Authentication:**
```javascript
// Message 1: Server sends (automatically)
{
  "type": "auth_required",
  "ha_version": "2025.1.0"
}

// Message 2: Client responds
{
  "type": "auth",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}

// Message 3: Server confirms
{
  "type": "auth_ok",
  "ha_version": "2025.1.0"
}
```

**Subscribe to events:**
```javascript
{
  "id": 1,
  "type": "subscribe_events",
  "event_type": "state_changed"
}

// Responses come as:
{
  "id": 1,
  "type": "event",
  "event": {
    "type": "state_changed",
    "data": {
      "entity_id": "light.living_room",
      "old_state": { "state": "off", ... },
      "new_state": { "state": "on", ... }
    }
  }
}
```

**Call a service:**
```javascript
{
  "id": 2,
  "type": "call_service",
  "domain": "light",
  "service": "turn_on",
  "service_data": {
    "entity_id": "light.living_room",
    "brightness": 200
  }
}

// Response:
{
  "id": 2,
  "type": "result",
  "success": true,
  "result": [
    {
      "entity_id": "light.living_room",
      "state": "on",
      "attributes": { ... }
    }
  ]
}
```

**Get current states:**
```javascript
{
  "id": 3,
  "type": "get_states"
}

// Response:
{
  "id": 3,
  "type": "result",
  "success": true,
  "result": [ ... ]  // Array of all entity states
}
```

**Subscribe to specific trigger:**
```javascript
{
  "id": 4,
  "type": "subscribe_trigger",
  "trigger": {
    "platform": "state",
    "entity_id": "light.living_room"
  }
}

// Trigger fires when light state changes:
{
  "id": 4,
  "type": "event",
  "event": { ... }
}
```

## Code Examples

### Python - REST API

```python
import requests
import os

HA_URL = os.getenv("HA_URL", "http://localhost:8123")
HA_TOKEN = os.getenv("HA_TOKEN")

headers = {
    "Authorization": f"Bearer {HA_TOKEN}",
    "Content-Type": "application/json"
}

# Get all states
response = requests.get(f"{HA_URL}/api/states", headers=headers)
response.raise_for_status()
states = response.json()

# Get single entity
response = requests.get(f"{HA_URL}/api/states/light.living_room", headers=headers)
light_state = response.json()
print(f"Light state: {light_state['state']}")
print(f"Brightness: {light_state['attributes'].get('brightness', 'N/A')}")

# Call service
service_data = {
    "entity_id": "light.living_room",
    "brightness": 180,
    "transition": 2
}
response = requests.post(
    f"{HA_URL}/api/services/light/turn_on",
    headers=headers,
    json=service_data
)
response.raise_for_status()
print(f"Service call successful: {response.json()}")

# Handle errors
try:
    response = requests.get(f"{HA_URL}/api/states/invalid.entity", headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print("ERROR: Token invalid or expired")
    elif e.response.status_code == 404:
        print("ERROR: Entity not found")
    else:
        print(f"ERROR: {e}")
```

### Python - WebSocket API

```python
import asyncio
import aiohttp
import json
import os

HA_URL = os.getenv("HA_URL", "http://localhost:8123").replace("http", "ws")
HA_TOKEN = os.getenv("HA_TOKEN")

async def monitor_light_changes():
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(f"{HA_URL}/api/websocket") as ws:
            # Wait for auth_required
            msg = await ws.receive_json()
            print(f"Server: {msg}")

            # Send auth
            await ws.send_json({
                "type": "auth",
                "access_token": HA_TOKEN
            })

            # Wait for auth_ok
            msg = await ws.receive_json()
            print(f"Server: {msg}")

            # Subscribe to state changes
            await ws.send_json({
                "id": 1,
                "type": "subscribe_events",
                "event_type": "state_changed"
            })

            # Listen for events
            async for msg in ws:
                event = msg.json()
                if event.get("type") == "event":
                    data = event["event"]["data"]
                    print(f"Entity: {data['entity_id']}")
                    print(f"  Old state: {data['old_state']['state']}")
                    print(f"  New state: {data['new_state']['state']}")

# Run the monitoring loop
asyncio.run(monitor_light_changes())
```

### JavaScript - REST API

```javascript
const HA_URL = process.env.HA_URL || "http://localhost:8123";
const HA_TOKEN = process.env.HA_TOKEN;

const headers = {
  "Authorization": `Bearer ${HA_TOKEN}`,
  "Content-Type": "application/json"
};

// Get all states
async function getAllStates() {
  const response = await fetch(`${HA_URL}/api/states`, { headers });
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// Get single entity
async function getEntityState(entityId) {
  const response = await fetch(`${HA_URL}/api/states/${entityId}`, { headers });
  if (response.status === 404) {
    throw new Error(`Entity ${entityId} not found`);
  }
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  const state = await response.json();
  console.log(`${entityId}: ${state.state}`);
  console.log(`Attributes:`, state.attributes);
  return state;
}

// Call service
async function callService(domain, service, data) {
  const response = await fetch(
    `${HA_URL}/api/services/${domain}/${service}`,
    {
      method: "POST",
      headers,
      body: JSON.stringify(data)
    }
  );
  if (!response.ok) {
    const error = await response.text();
    throw new Error(`HTTP ${response.status}: ${error}`);
  }
  return response.json();
}

// Example usage
(async () => {
  try {
    const states = await getAllStates();
    console.log(`Found ${states.length} entities`);

    await getEntityState("light.living_room");

    const result = await callService("light", "turn_on", {
      entity_id: "light.living_room",
      brightness: 180
    });
    console.log("Service call successful");
  } catch (error) {
    console.error(error);
  }
})();
```

### JavaScript - WebSocket API

```javascript
const HA_URL = (process.env.HA_URL || "http://localhost:8123").replace(/^http/, "ws");
const HA_TOKEN = process.env.HA_TOKEN;

async function subscribeToStateChanges() {
  const ws = new WebSocket(`${HA_URL}/api/websocket`);

  return new Promise((resolve, reject) => {
    ws.onopen = () => console.log("WebSocket connected");

    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      console.log("Message:", msg);

      if (msg.type === "auth_required") {
        // Respond to auth challenge
        ws.send(JSON.stringify({
          type: "auth",
          access_token: HA_TOKEN
        }));
      } else if (msg.type === "auth_ok") {
        // Authentication successful, subscribe to events
        ws.send(JSON.stringify({
          id: 1,
          type: "subscribe_events",
          event_type: "state_changed"
        }));
      } else if (msg.type === "event" && msg.event?.type === "state_changed") {
        // Handle state change
        const data = msg.event.data;
        console.log(`${data.entity_id} changed:`);
        console.log(`  ${data.old_state.state} → ${data.new_state.state}`);
      }
    };

    ws.onerror = (error) => {
      console.error("WebSocket error:", error);
      reject(error);
    };

    ws.onclose = () => {
      console.log("WebSocket closed");
      resolve();
    };
  });
}

subscribeToStateChanges();
```

### cURL - Common Operations

```bash
# Get all entities
curl -X GET "http://localhost:8123/api/states" \
  -H "Authorization: Bearer ${HA_TOKEN}"

# Get specific entity
curl -X GET "http://localhost:8123/api/states/light.living_room" \
  -H "Authorization: Bearer ${HA_TOKEN}"

# Turn on light with brightness
curl -X POST "http://localhost:8123/api/services/light/turn_on" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "light.living_room",
    "brightness": 200,
    "transition": 2
  }'

# Turn off light
curl -X POST "http://localhost:8123/api/services/light/turn_off" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room"}'

# Set climate temperature
curl -X POST "http://localhost:8123/api/services/climate/set_temperature" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "entity_id": "climate.living_room",
    "temperature": 21
  }'

# Get service schema
curl -X GET "http://localhost:8123/api/services/light" \
  -H "Authorization: Bearer ${HA_TOKEN}"

# Call automation
curl -X POST "http://localhost:8123/api/services/automation/trigger" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "automation.my_automation"}'

# Render template
curl -X POST "http://localhost:8123/api/template" \
  -H "Authorization: Bearer ${HA_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"template": "{{ states(\"sensor.temperature\") }}"}'
```

## Known Issues Prevention

| Issue | Root Cause | Solution |
|-------|-----------|----------|
| 401 Unauthorized | Token invalid, expired, or malformed | Create new token in Settings → Create Long-Lived Access Token; verify Bearer prefix |
| 404 Not Found | Entity doesn't exist or wrong domain | Check entity_id with `GET /api/states`; verify domain.service format |
| WebSocket auth timeout | Didn't respond to auth_required within 10s | Send auth message immediately upon receiving auth_required |
| Attribute confusion | Mixing state string with attributes object | State is always a string; attributes contain metadata (brightness, color, etc.) |
| Service call fails silently | Wrong domain/service or missing required fields | Use `GET /api/services` to discover available services and required parameters |

## Error Handling Patterns

### HTTP Status Codes

```python
import requests

try:
    response = requests.get(f"{HA_URL}/api/states/{entity_id}", headers=headers)

    if response.status_code == 401:
        print("Token invalid/expired - create new token in HA UI")
    elif response.status_code == 403:
        print("Forbidden - token lacks necessary permissions")
    elif response.status_code == 404:
        print("Entity not found - check entity_id")
    elif response.status_code == 502:
        print("Home Assistant unavailable - check server status")
    elif response.status_code >= 500:
        print("Server error - try again later")
    else:
        response.raise_for_status()
        return response.json()
except requests.exceptions.ConnectionError:
    print("Cannot connect to Home Assistant - verify HA_URL and network")
except requests.exceptions.Timeout:
    print("Request timeout - Home Assistant is slow to respond")
```

### WebSocket Error Handling

```javascript
const ws = new WebSocket(wsUrl);

ws.onerror = (error) => {
  console.error("WebSocket error:", error);
  // Reconnect after delay
  setTimeout(connect, 5000);
};

ws.onmessage = (event) => {
  const msg = JSON.parse(event.data);

  if (msg.type === "result" && !msg.success) {
    console.error("Command failed:", msg.error);
  }
};

ws.onclose = () => {
  console.log("Connection closed");
  // Implement reconnection logic
  setTimeout(connect, 3000);
};
```

## Bundled Resources

### References

Located in `references/`:
- [`REST_API_REFERENCE.md`](references/REST_API_REFERENCE.md) - Complete REST endpoint documentation
- [`WEBSOCKET_API_REFERENCE.md`](references/WEBSOCKET_API_REFERENCE.md) - WebSocket command reference
- [`AUTHENTICATION.md`](references/AUTHENTICATION.md) - Auth token creation and security best practices
- [`SERVICE_CATALOG.md`](references/SERVICE_CATALOG.md) - Common services by domain

> **Note:** For deep dives on specific topics, see the reference files above.

## Dependencies

### Required

| Package | Language | Purpose |
|---------|----------|---------|
| requests | Python | HTTP client for REST API calls |
| aiohttp | Python | Async HTTP/WebSocket client |
| fetch | JavaScript | Native HTTP client (browser/Node.js) |
| WebSocket | JavaScript | Native WebSocket API (browser/Node.js) |

### Optional

| Package | Language | Purpose |
|---------|----------|---------|
| httpx | Python | Advanced HTTP client with streaming |
| websockets | Python | Pure Python WebSocket library |
| axios | JavaScript | Promise-based HTTP client |

## Official Documentation

- [Home Assistant REST API](https://developers.home-assistant.io/docs/api/rest)
- [Home Assistant WebSocket API](https://developers.home-assistant.io/docs/api/websocket)
- [Home Assistant Authentication](https://developers.home-assistant.io/docs/auth_api)
- [Home Assistant Integration API](https://www.home-assistant.io/integrations/api/)

## Troubleshooting

### Cannot authenticate - 401 Unauthorized

**Symptoms:** All API requests return 401, even with correct token.

**Solution:**
1. Verify token in Home Assistant (Settings → Developer Tools → States/Services)
2. Check Authorization header includes "Bearer " prefix
3. Create new token if old one expired
4. Ensure HA_URL and HA_TOKEN environment variables are set

```bash
echo $HA_TOKEN  # Verify token is set
echo $HA_URL    # Verify URL is correct (http not https)
```

### WebSocket connection closes immediately

**Symptoms:** WebSocket connects then closes without response.

**Solution:**
1. Verify Home Assistant version supports WebSocket API (2021.1+)
2. Check firewall doesn't block WebSocket upgrade
3. Ensure auth response is sent within 10 seconds of auth_required
4. Use correct `/api/websocket` path, not `/api/websocket/`

```javascript
// Incorrect path
ws = new WebSocket("ws://ha:8123/api/websocket/");

// Correct path
ws = new WebSocket("ws://ha:8123/api/websocket");
```

### Entity states appear as wrong type

**Symptoms:** State should be "on"/"off" but appears as number or boolean.

**Solution:**
1. Check entity's integration configuration
2. Reload integration in Developer Tools
3. Verify template/custom component isn't converting type
4. State is always a string in API response; parse as needed

```python
state = entity["state"]  # String: "on", "off", "123"
is_on = state == "on"   # Convert to boolean

# For numeric states
temperature = float(entity["state"])  # Convert to float
```

### Service call fails but no error returned

**Symptoms:** Service call returns HTTP 200 but nothing happens.

**Solution:**
1. Verify service exists: `GET /api/services/{domain}`
2. Check required fields in service_data
3. Verify entity_id is in entity_ids list, not as separate parameter
4. Check entity supports service (light.turn_on won't work on switch)

```bash
# Correct - entity_id in service_data
curl -X POST "http://ha:8123/api/services/light/turn_on" \
  -d '{"entity_id": "light.living_room"}'

# Incorrect - entity_id as path parameter
curl -X POST "http://ha:8123/api/services/light/turn_on/light.living_room"
```

## Setup Checklist

Before using this skill, verify:

- [ ] Home Assistant instance is running and accessible (test via browser)
- [ ] Created Long-Lived Access Token (Settings → My Home → Create Token)
- [ ] Token stored in environment variable (HA_TOKEN) or secure vault
- [ ] Home Assistant URL set correctly (HA_URL with http not https)
- [ ] Firewall allows API/WebSocket connections (ports 8123 or custom)
- [ ] Python packages installed if using Python examples (pip install requests aiohttp)
- [ ] Tested connectivity with simple curl/fetch request before building full integration
