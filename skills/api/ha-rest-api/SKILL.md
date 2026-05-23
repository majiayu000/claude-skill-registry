---
name: ha-rest-api
description: "Interact with Home Assistant REST API for entity discovery, state retrieval, and service calls. Use when working with Home Assistant integrations, controlling devices, querying sensor data, or automating Home Assistant operations. Covers authentication, entity patterns, service calls, and state queries."
---

# Home Assistant REST API

Interact with Home Assistant using the REST API to discover entities, retrieve states, and call services.

## Quick Start

All API calls require authentication using a long-lived access token:

```bash
# Token stored in ~/.zshrc as HA_LONG_LIVED_TOKEN
source ~/.zshrc

# Test connection
curl -s "http://192.168.68.123:8123/api/" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" \
  -H "Content-Type: application/json"
```

## Core Operations

### 1. Discover Entities

Get all entities or filter by domain:

```python
import requests
import os

HA_URL = "http://192.168.68.123:8123"
HA_TOKEN = os.environ["HA_LONG_LIVED_TOKEN"]

def get_all_entities():
    """Get all entity states."""
    url = f"{HA_URL}/api/states"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()

def discover_entities(pattern: str) -> dict[str, str]:
    """Discover entity IDs matching a pattern."""
    entities = {}
    for state in get_all_entities():
        entity_id = state["entity_id"]
        if pattern.lower() in entity_id.lower():
            entities[entity_id] = state["state"]
    return entities

# Examples
climate_entities = discover_entities("climate.")
office_sensors = discover_entities("sensor.office")
```

**bash equivalent:**

```bash
# Get all entities
curl -s "$HA_URL/api/states" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq

# Filter to specific domain
curl -s "$HA_URL/api/states" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | \
  jq '.[] | select(.entity_id | startswith("climate."))'
```

### 2. Get Entity State

Retrieve full entity state including attributes:

```python
def get_entity_state(entity_id: str) -> dict:
    """Get full entity state including attributes."""
    url = f"{HA_URL}/api/states/{entity_id}"
    headers = {"Authorization": f"Bearer {HA_TOKEN}"}

    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    return response.json()
    # Returns: {
    #   "entity_id": "sensor.temperature",
    #   "state": "22.5",
    #   "attributes": {"unit_of_measurement": "°C", ...},
    #   "last_changed": "2025-12-14T10:30:00+00:00"
    # }

# Example
temp_state = get_entity_state("sensor.officeht_temperature")
print(f"Temperature: {temp_state['state']}{temp_state['attributes']['unit_of_measurement']}")
```

**bash equivalent:**

```bash
curl -s "$HA_URL/api/states/sensor.officeht_temperature" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq
```

### 3. Call Services

Control devices by calling Home Assistant services:

```python
def call_service(domain: str, service: str, entity_id: str, **kwargs):
    """Call a Home Assistant service."""
    url = f"{HA_URL}/api/services/{domain}/{service}"
    headers = {
        "Authorization": f"Bearer {HA_TOKEN}",
        "Content-Type": "application/json",
    }

    data = {"entity_id": entity_id, **kwargs}
    response = requests.post(url, headers=headers, json=data, timeout=10)
    response.raise_for_status()
    return response.json()

# Examples
# Turn on light with brightness
call_service("light", "turn_on", "light.living_room_dimmer", brightness=150)

# Set AC temperature
call_service("climate", "set_temperature", "climate.snorlug", temperature=22)

# Turn on irrigation zone
call_service("switch", "turn_on", "switch.s01_left_top_patio_lawn_station_enabled")

# Turn off climate
call_service("climate", "turn_off", "climate.mines_of_moria")
```

**bash equivalent:**

```bash
# Turn on light with brightness
curl -X POST "$HA_URL/api/services/light/turn_on" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "light.living_room_dimmer", "brightness": 150}'

# Set AC temperature
curl -X POST "$HA_URL/api/services/climate/set_temperature" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entity_id": "climate.snorlug", "temperature": 22}'
```

### 4. Get Available Services

Discover what services are available:

```bash
curl -s "$HA_URL/api/services" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq
```

### 5. Get Configuration

Retrieve Home Assistant configuration:

```bash
curl -s "$HA_URL/api/config" \
  -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq
```

## Common Patterns

### Monitor Multiple Sensors

```python
def get_environmental_data() -> dict:
    """Get all environmental sensor data."""
    sensors = [
        "sensor.officeht_temperature",
        "sensor.officeht_humidity",
        "sensor.enviro_temperature",
        "sensor.enviro_humidity",
        "sensor.enviro_pressure",
        "sensor.enviro_pm2_5",
    ]

    data = {}
    for sensor in sensors:
        state = get_entity_state(sensor)
        data[sensor] = {
            "value": state["state"],
            "unit": state["attributes"].get("unit_of_measurement"),
            "last_updated": state["last_changed"],
        }
    return data
```

### Batch Service Calls

```python
def turn_off_all_acs():
    """Turn off all air conditioners."""
    acs = ["climate.snorlug", "climate.val_hella_wam", "climate.mines_of_moria"]
    for ac in acs:
        call_service("climate", "turn_off", ac)
```

### Entity State Monitoring

```python
def check_if_entity_changed(entity_id: str, last_check: str) -> bool:
    """Check if entity state changed since last check."""
    state = get_entity_state(entity_id)
    return state["last_changed"] > last_check
```

## Common Service Domains

| Domain | Common Services | Example Entities |
|--------|----------------|------------------|
| `light` | turn_on, turn_off, toggle | light.living_room_dimmer |
| `climate` | turn_on, turn_off, set_temperature, set_hvac_mode | climate.snorlug |
| `switch` | turn_on, turn_off, toggle | switch.s01_* (irrigation) |
| `media_player` | turn_on, turn_off, play_media, volume_set | media_player.* |
| `automation` | trigger, turn_on, turn_off | automation.* |

## Error Handling

```python
def safe_service_call(domain: str, service: str, entity_id: str, **kwargs):
    """Call service with error handling."""
    try:
        result = call_service(domain, service, entity_id, **kwargs)
        return {"success": True, "result": result}
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            return {"success": False, "error": "Entity or service not found"}
        elif e.response.status_code == 401:
            return {"success": False, "error": "Authentication failed"}
        else:
            return {"success": False, "error": f"HTTP {e.response.status_code}"}
    except requests.Timeout:
        return {"success": False, "error": "Request timeout"}
```

## Shell Aliases

Add to ~/.zshrc for quick API access:

```bash
export HA_URL="http://192.168.68.123:8123"

# Quick HA API calls
alias ha-test='curl -s "$HA_URL/api/" -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN"'
alias ha-states='curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq'
alias ha-climate='curl -s "$HA_URL/api/states" -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq ".[] | select(.entity_id | startswith(\"climate.\"))"'
alias ha-config='curl -s "$HA_URL/api/config" -H "Authorization: Bearer $HA_LONG_LIVED_TOKEN" | jq'
```

## Resources

See [references/api_endpoints.md](references/api_endpoints.md) for complete REST API endpoint reference.
