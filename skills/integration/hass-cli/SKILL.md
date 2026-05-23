---
name: home-assistant
description: Control Home Assistant devices and automations via hass-cli. Use when controlling smart home devices, lights, switches, sensors, climate, media players, or running automations/scripts. Requires HASS_SERVER and HASS_TOKEN environment variables.
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["hass-cli"]},"install":[{"id":"brew","kind":"brew","formula":"homeassistant-cli","bins":["hass-cli"],"label":"Install hass-cli (brew)"}]}}
---

# Home Assistant CLI

Control Home Assistant via `hass-cli`.

## Install

```bash
# macOS (Homebrew)
brew install homeassistant-cli

# pip (any platform)
pip install homeassistant-cli

# Verify
hass-cli --version
```

## Setup

### 1. Find Your Home Assistant URL

Common URLs (try in order):
- `http://homeassistant.local:8123` — Default mDNS hostname
- `http://homeassistant:8123` — If using Docker/hostname
- `http://<IP-ADDRESS>:8123` — Direct IP (e.g., `http://192.168.1.100:8123`)
- `https://your-instance.ui.nabu.casa` — If using Nabu Casa cloud

Test it: open the URL in a browser — you should see the HA login page.

### 2. Create a Long-Lived Access Token

1. Open Home Assistant in your browser
2. Click your **profile** (bottom-left of the sidebar, your name/icon)
3. Scroll down to **Long-Lived Access Tokens**
4. Click **Create Token**
5. Give it a name (e.g., "Clawdbot" or "CLI")
6. **Copy the token immediately** — you won't see it again!

The token looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3...`

### 3. Configure Environment Variables

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):
```bash
export HASS_SERVER="http://homeassistant.local:8123"
export HASS_TOKEN="your-token-here"
```

Or for Clawdbot, store credentials in TOOLS.md:
```markdown
## Home Assistant
- **URL:** `http://homeassistant.local:8123`
- **Token:** `eyJ...your-token...`
```

Then reference TOOLS.md before making calls.

## Quick Reference

```bash
# List all entities
hass-cli state list

# Filter entities (pipe to grep)
hass-cli state list | grep -i kitchen

# Get specific entity state
hass-cli state get light.kitchen

# Turn on/off
hass-cli service call switch.turn_on --arguments entity_id=switch.fireplace
hass-cli service call switch.turn_off --arguments entity_id=switch.fireplace
hass-cli service call light.turn_on --arguments entity_id=light.kitchen
hass-cli service call light.turn_off --arguments entity_id=light.kitchen

# Light brightness (0-255)
hass-cli service call light.turn_on --arguments entity_id=light.kitchen,brightness=128

# Toggle
hass-cli service call switch.toggle --arguments entity_id=switch.fireplace

# Climate
hass-cli service call climate.set_temperature --arguments entity_id=climate.thermostat,temperature=72

# Run automation/script
hass-cli service call automation.trigger --arguments entity_id=automation.evening_lights
hass-cli service call script.turn_on --arguments entity_id=script.movie_mode
```

## Entity Naming Patterns

- `light.*` — Lights
- `switch.*` — Switches, plugs, relays
- `sensor.*` — Temperature, humidity, power, etc.
- `binary_sensor.*` — Motion, door/window, presence
- `climate.*` — Thermostats, HVAC
- `cover.*` — Blinds, garage doors
- `media_player.*` — TVs, speakers
- `automation.*` — Automations
- `script.*` — Scripts
- `scene.*` — Scenes

## Discovery Tips

```bash
# Find all lights
hass-cli state list | grep "^light\."

# Find devices by room name
hass-cli state list | grep -i bedroom

# Find all "on" devices
hass-cli state list | grep -E "\s+on\s+"

# Get entity attributes (JSON)
hass-cli --format json state get light.kitchen
```

## Notes

- Empty `[]` response from service calls = success
- Use exact entity_id from `state list`
- Multiple arguments: comma-separated (no spaces)
- If hass-cli unavailable, use REST API as fallback:
  ```bash
  curl -s -H "Authorization: Bearer $HASS_TOKEN" "$HASS_SERVER/api/states" | jq
  ```
