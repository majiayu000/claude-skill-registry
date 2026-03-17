---
name: ha-error-checking
description: |
  Debugs and validates Home Assistant dashboards by checking system logs, verifying entity IDs,
  validating HACS card installations, and analyzing configuration errors via WebSocket API.

  Use when troubleshooting dashboard errors, validating entity IDs, checking HACS card installations,
  investigating lovelace/frontend issues, or debugging "ApexCharts span error", "entity not found",
  "custom card not loading", or "dashboard not appearing in sidebar".
---

Works with Home Assistant WebSocket API, Python websocket library, and YAML configurations.
# Home Assistant Error Checking and Validation

Debug and validate Home Assistant dashboards, configurations, and entity usage programmatically.

## Quick Start

Use the automation script for fast dashboard validation:

```bash
python ~/.claude/skills/ha-error-checking/scripts/check_dashboard.py climate-control
```

Or use the Quick Start workflow below for custom checks.

### Quick Start Workflow

```python
import json
import websocket
import os

HA_URL = "http://192.168.68.123:8123"
HA_TOKEN = os.environ["HA_LONG_LIVED_TOKEN"]

def check_dashboard_errors(url_path: str):
    """Check for errors in a specific dashboard."""
    ws_url = HA_URL.replace("http://", "ws://") + "/api/websocket"
    ws = websocket.create_connection(ws_url)
    msg_id = 1

    # 1. Auth
    ws.recv()
    ws.send(json.dumps({"type": "auth", "access_token": HA_TOKEN}))
    ws.recv()

    # 2. Check system logs for lovelace errors
    ws.send(json.dumps({"id": msg_id, "type": "system_log/list"}))
    msg_id += 1
    logs = json.loads(ws.recv())

    lovelace_errors = [
        log for log in logs.get("result", [])
        if "lovelace" in log.get("name", "").lower()
        or "frontend" in log.get("name", "").lower()
    ]

    # 3. Validate dashboard config
    ws.send(json.dumps({
        "id": msg_id,
        "type": "lovelace/config",
        "url_path": url_path
    }))
    msg_id += 1
    config_response = json.loads(ws.recv())

    # 4. Get all entity states
    ws.send(json.dumps({"id": msg_id, "type": "get_states"}))
    msg_id += 1
    states_response = json.loads(ws.recv())

    ws.close()

    return {
        "lovelace_errors": lovelace_errors,
        "config": config_response.get("result"),
        "available_entities": [s["entity_id"] for s in states_response.get("result", [])]
    }
```

## Usage

Follow these steps to debug Home Assistant dashboard errors:

1. **Check system logs** for lovelace/frontend errors
2. **Validate dashboard config** exists and is properly formatted
3. **Verify entity IDs** exist in Home Assistant
4. **Check HACS cards** are installed before use
5. **Validate card configurations** for known issues (ApexCharts span, URL paths)

## System Logs - Check for Errors

### Get All System Logs

```python
ws.send(json.dumps({"id": 1, "type": "system_log/list"}))
response = json.loads(ws.recv())

logs = response.get("result", [])
# Structure: [{"name": "homeassistant.components.lovelace", "message": "...", "level": "ERROR", ...}, ...]
```

### Filter for Lovelace/Frontend Errors

```python
lovelace_errors = [
    log for log in logs
    if "lovelace" in log.get("name", "").lower()
    or "frontend" in log.get("name", "").lower()
]

for error in lovelace_errors:
    print(f"[{error['level']}] {error['name']}: {error['message']}")
```

## Dashboard Configuration Validation

### Get Dashboard Config

```python
ws.send(json.dumps({
    "id": 1,
    "type": "lovelace/config",
    "url_path": "climate-control"  # Must contain hyphen
}))
response = json.loads(ws.recv())

config = response.get("result")
# Returns the full dashboard configuration dict
```

### Validate Dashboard Exists

```python
ws.send(json.dumps({"id": 1, "type": "lovelace/dashboards/list"}))
response = json.loads(ws.recv())

dashboards = response.get("result", [])
dashboard_paths = [d["url_path"] for d in dashboards]

if "climate-control" in dashboard_paths:
    print("Dashboard exists")
else:
    print("Dashboard not found")
```

### Check Dashboard URL Path Format

**CRITICAL:** Dashboard URL paths must contain a hyphen.

```python
def validate_url_path(url_path: str) -> tuple[bool, str]:
    """Validate dashboard URL path format.

    Returns:
        (is_valid, error_message)
    """
    if "-" not in url_path:
        return False, f"URL path must contain hyphen: '{url_path}' -> '{url_path}-view'"

    if " " in url_path:
        return False, f"URL path cannot contain spaces: '{url_path}'"

    if not url_path.islower():
        return False, f"URL path must be lowercase: '{url_path}'"

    return True, ""

# Examples
validate_url_path("climate")         # ❌ (False, "URL path must contain hyphen...")
validate_url_path("climate-control") # ✅ (True, "")
validate_url_path("Climate-Control") # ❌ (False, "URL path must be lowercase...")
```

## Entity Validation

### Get All Available Entities

```python
ws.send(json.dumps({"id": 1, "type": "get_states"}))
response = json.loads(ws.recv())

entities = response.get("result", [])
entity_ids = [e["entity_id"] for e in entities]

# Group by domain
from collections import defaultdict
by_domain = defaultdict(list)
for entity_id in entity_ids:
    domain = entity_id.split(".")[0]
    by_domain[domain].append(entity_id)

print(f"Total entities: {len(entity_ids)}")
print(f"Sensors: {len(by_domain['sensor'])}")
print(f"Climate: {len(by_domain['climate'])}")
```

See `examples/examples.md` for entity extraction from dashboard configs and pattern matching.

## HACS Card Installation Validation

### Check if Card is Installed

```python
def check_hacs_card_installed(ws, repository_id: int) -> bool:
    """Check if a HACS card is installed by repository ID."""
    ws.send(json.dumps({
        "id": 1,
        "type": "hacs/repositories/list"
    }))
    response = json.loads(ws.recv())

    repositories = response.get("result", [])
    installed = [r for r in repositories if r.get("id") == repository_id]

    return len(installed) > 0

# Known repository IDs
HACS_CARDS = {
    "mini-graph-card": 151280062,
    "bubble-card": 680112919,
    "modern-circular-gauge": 871730343,
    "lovelace-mushroom": 444350375,
    "apexcharts-card": 331701152,
}

# Check installation
if check_hacs_card_installed(ws, HACS_CARDS["apexcharts-card"]):
    print("ApexCharts card is installed")
else:
    print("ApexCharts card NOT installed - install via HACS first")
```

See `examples/examples.md` for programmatic HACS card installation.

## Card Configuration Validation

### Validate ApexCharts Span Configuration

**CRITICAL:** `span.end` must be one of: "minute", "hour", "day", "week", "month", "year", "isoWeek"

```python
VALID_SPAN_END_VALUES = ["minute", "hour", "day", "week", "month", "year", "isoWeek"]

def validate_apexcharts_span(card_config: dict) -> tuple[bool, str]:
    """Validate ApexCharts span configuration.

    Returns:
        (is_valid, error_message)
    """
    if "span" not in card_config:
        return True, ""  # span is optional

    span = card_config["span"]
    if "end" not in span:
        return True, ""  # end is optional within span

    end_value = span["end"]
    if end_value not in VALID_SPAN_END_VALUES:
        return False, f"Invalid span.end: '{end_value}'. Must be one of: {VALID_SPAN_END_VALUES}"

    return True, ""

# Usage
apexcharts_card = {
    "type": "custom:apexcharts-card",
    "span": {"end": "now"}  # ❌ Invalid
}

is_valid, error = validate_apexcharts_span(apexcharts_card)
if not is_valid:
    print(f"Error: {error}")
    # Fix it
    apexcharts_card["span"]["end"] = "hour"  # ✅ Valid
```

## Supporting Files

- **examples/examples.md** - Comprehensive workflows (complete dashboard validation, entity extraction, pattern matching, HACS installation, custom card validation)
- **references/reference.md** - Error patterns, known entity IDs, troubleshooting solutions, best practices
- **scripts/check_dashboard.py** - Automated dashboard validation script

## Common Error Patterns

### 1. ApexCharts Span Error

**Error:** `"Invalid value for span.end: now"`

**Solution:**
```python
# WRONG
card = {
    "type": "custom:apexcharts-card",
    "span": {"end": "now"}  # ❌
}

# CORRECT
card = {
    "type": "custom:apexcharts-card",
    "span": {"end": "hour"}  # ✅
}
```

### 2. Dashboard URL Path Missing Hyphen

**Error:** Dashboard doesn't appear in sidebar

**Solution:**
```python
# WRONG
url_path = "climate"  # ❌

# CORRECT
url_path = "climate-control"  # ✅
```

### 3. Entity Not Found

**Error:** `"Entity not found: sensor.temperature"`

**Solution:**
```python
# Check entity exists
all_entities = get_all_entity_ids(ws)
if "sensor.temperature" not in all_entities:
    print("Entity not found - check spelling in Developer Tools → States")

    # Find similar entities
    similar = [e for e in all_entities if "temperature" in e]
    print(f"Did you mean: {similar}")
```

See `references/reference.md` for complete error patterns, browser debugging steps, best practices, and troubleshooting checklist.

## Notes

- Dashboard URL paths MUST contain a hyphen (e.g., "climate-control" not "climate")
- ApexCharts `span.end` only accepts: minute, hour, day, week, month, year, isoWeek
- HACS repository IDs: mini-graph-card (151280062), apexcharts-card (331701152)
- Check system logs after every dashboard update for errors
- Use Developer Tools → States to verify entity IDs before use
