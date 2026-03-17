---
name: ha-dashboard-create
description: |
  Creates and updates Home Assistant Lovelace dashboards programmatically via WebSocket API
  with dashboard structure, view configuration, and entity validation. Use when asked to
  "create HA dashboard", "automate dashboard creation", "WebSocket dashboard API", "programmatic
  Lovelace", or "validate dashboard entities".

---

Works with Python websocket-client, WebSocket API authentication, and Lovelace configuration.
# Home Assistant Dashboard Creation

Create and update Lovelace dashboards programmatically using the WebSocket API.

## CRITICAL: Dashboard URL Path Requirements

**Home Assistant requires dashboard URL paths to contain a hyphen:**

- ✅ CORRECT: "climate-control", "mobile-app", "energy-monitor"
- ❌ WRONG: "climate", "mobile", "energy"

**Rule:** Always use kebab-case with at least one hyphen in the `url_path` field.

## When to Use This Skill

Use this skill when you need to:
- Create Home Assistant dashboards programmatically via WebSocket API
- Automate dashboard creation and updates for multiple environments
- Build dashboard generators for dynamic card configurations
- Validate dashboard entities before deployment
- Manage dashboards as code with version control
- Programmatically update existing dashboard configurations

Do NOT use when:
- You can use the Home Assistant UI dashboard editor (simpler for manual changes)
- Building simple static dashboards (UI editor is more intuitive)
- You haven't created a long-lived access token for API authentication

## Usage

1. **Connect to WebSocket**: Authenticate with long-lived access token
2. **Check if exists**: Query existing dashboards with `lovelace/dashboards/list`
3. **Create dashboard**: Use `lovelace/dashboards/create` with url_path containing hyphen
4. **Save configuration**: Update config with `lovelace/config/save`
5. **Verify**: Check HA UI and system logs for errors

## Quick Start

```python
import json
import websocket

HA_URL = "http://192.168.68.123:8123"
HA_TOKEN = os.environ["HA_LONG_LIVED_TOKEN"]

def create_dashboard(url_path: str, title: str, config: dict):
    """Create or update a dashboard.

    Args:
        url_path: Dashboard URL path (must contain hyphen, e.g., "climate-control")
        title: Dashboard display title
        config: Dashboard configuration dict
    """
    # Validate url_path contains hyphen
    if "-" not in url_path:
        raise ValueError(f"url_path must contain hyphen: '{url_path}' -> '{url_path}-view'")

    ws_url = HA_URL.replace("http://", "ws://") + "/api/websocket"
    ws = websocket.create_connection(ws_url)
    msg_id = 1

    # 1. Receive auth_required
    ws.recv()

    # 2. Send auth
    ws.send(json.dumps({"type": "auth", "access_token": HA_TOKEN}))
    ws.recv()  # auth_ok

    # 3. Check if dashboard exists
    ws.send(json.dumps({"id": msg_id, "type": "lovelace/dashboards/list"}))
    msg_id += 1
    response = json.loads(ws.recv())
    exists = any(d["url_path"] == url_path for d in response.get("result", []))

    # 4. Create if doesn't exist
    if not exists:
        ws.send(json.dumps({
            "id": msg_id,
            "type": "lovelace/dashboards/create",
            "url_path": url_path,  # Must contain hyphen!
            "title": title,
            "icon": "mdi:view-dashboard",
            "show_in_sidebar": True,
        }))
        msg_id += 1
        ws.recv()

    # 5. Save configuration
    ws.send(json.dumps({
        "id": msg_id,
        "type": "lovelace/config/save",
        "url_path": url_path,
        "config": config,
    }))
    ws.recv()
    ws.close()
```

## WebSocket Message Types

| Type | Purpose |
|------|---------|
| `lovelace/dashboards/list` | List all dashboards |
| `lovelace/dashboards/create` | Create new dashboard |
| `lovelace/dashboards/delete` | Delete dashboard |
| `lovelace/config/save` | Save dashboard config |
| `lovelace/config` | Get dashboard config |
| `system_log/list` | Check for lovelace errors |

See [references/card-types.md](references/card-types.md) for dashboard configuration structure and common card types.

## Error Checking

### Validate Dashboard Configuration

```python
# 1. Check system logs for lovelace errors
ws.send(json.dumps({"id": 1, "type": "system_log/list"}))
logs = json.loads(ws.recv())
# Filter for 'lovelace' or 'frontend' errors

# 2. Validate dashboard configuration
ws.send(json.dumps({
    "id": 2,
    "type": "lovelace/config",
    "url_path": "climate-control"  # Must contain hyphen
}))
config = json.loads(ws.recv())

# 3. Validate entity IDs exist
ws.send(json.dumps({"id": 3, "type": "get_states"}))
states = json.loads(ws.recv())
entity_ids = [s["entity_id"] for s in states["result"]]

# 4. Check if entities used in dashboard exist
for card in dashboard_config["views"][0]["cards"]:
    if "entity" in card:
        if card["entity"] not in entity_ids:
            print(f"Warning: Entity {card['entity']} not found")
```

### Common Error Patterns

1. **URL path missing hyphen**: `"url_path": "climate"` → Add hyphen: `"climate-control"`
2. **Entity doesn't exist**: Check entity ID in Developer Tools → States
3. **Custom card not installed**: Install via HACS first
4. **JavaScript errors**: Check browser console (F12) for configuration errors

## Entity Validation

Verify entity IDs exist before using them in dashboards.

See [references/entity-patterns.md](references/entity-patterns.md) for entity validation functions and common entity patterns.

## Supporting Files

- **scripts/create_dashboard.py** - Complete working example with entity validation
- **references/card-types.md** - Dashboard configuration structure and card types
- **references/entity-patterns.md** - Entity validation and common patterns

## Workflow

1. **Design dashboard** - Plan views and card layout
2. **Validate entities** - Check all entity IDs exist
3. **Connect to WebSocket** - Authenticate with HA
4. **Check if exists** - Query existing dashboards
5. **Create dashboard** - Create if new (ensure url_path has hyphen!)
6. **Save configuration** - Update dashboard config
7. **Verify** - Check in HA UI and system logs for errors

## URL Path Examples

| Dashboard Type | Bad URL Path | Good URL Path |
|----------------|--------------|---------------|
| Climate monitoring | "climate" | "climate-control" |
| Mobile view | "mobile" | "mobile-app" |
| Energy tracking | "energy" | "energy-monitor" |
| Air quality | "air" | "air-quality" |
| Irrigation | "irrigation" | "irrigation-control" |

## Troubleshooting

### Dashboard not appearing in sidebar

1. Check `show_in_sidebar: True` in dashboard creation
2. Verify `url_path` contains hyphen
3. Refresh browser (Ctrl+Shift+R)
4. Check HA logs for errors

### Configuration not saving

1. Verify WebSocket authentication succeeded
2. Check `url_path` matches existing dashboard
3. Validate JSON structure (no syntax errors)
4. Check system logs via `system_log/list`

### Entity not found errors

1. Get all entities: `{"type": "get_states"}`
2. Compare with entities used in dashboard
3. Fix entity IDs or remove missing entities
4. Ensure entity has proper `state_class` for sensors

## Official Documentation

- [Lovelace Dashboards - Home Assistant](https://www.home-assistant.io/dashboards/)
- [WebSocket API - Home Assistant](https://developers.home-assistant.io/docs/api/websocket)
