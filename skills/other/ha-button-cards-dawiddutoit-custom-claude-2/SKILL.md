---
name: ha-button-cards
description: |
  Creates and configures Home Assistant button cards with actions (tap, hold, double-tap), service calls,
  navigation, and custom button-card (HACS) with templating and state-based styling.
  Use when asked to "create button card", "add service call button", "configure tap actions",
  or "customize button appearance".
---

Works with Lovelace YAML dashboards and custom button-card integration.
# Home Assistant Button Cards

Create interactive buttons for controlling devices, calling services, and navigating between views in Home Assistant dashboards.

## Overview

This skill covers:
- **Native Button Card**: Simple entity controls with actions
- **Custom Button Card** (HACS): Advanced templating, state-based styling, multiple actions
- **Action Types**: tap, hold, double-tap behaviors
- **Service Calls**: Execute Home Assistant services
- **Navigation**: Move between dashboard views
- **State-Based Styling**: Dynamic colors and icons

## When to Use This Skill

Use this skill when you need to:
- Create interactive buttons for toggling lights, switches, or climate controls
- Add service call buttons to execute automations or scripts
- Configure tap, hold, and double-tap actions for different behaviors
- Build navigation buttons to move between dashboard views
- Implement state-based styling with dynamic colors and icons
- Use custom button-card (HACS) for advanced templating and conditional logic

Do NOT use when:
- You only need to display sensor values without interaction (use entity card instead)
- Building complex multi-entity cards (use entities card or custom layouts)

## Quick Start

### Basic Toggle Button

```yaml
type: button
entity: light.living_room
name: Living Room
show_state: true
icon: mdi:lightbulb
tap_action:
  action: toggle
hold_action:
  action: more-info
```

### Service Call Button

```yaml
type: button
name: Turn Off All Lights
icon: mdi:lightbulb-off
show_state: false
tap_action:
  action: perform-action
  perform_action: light.turn_off
  data:
    entity_id: all
```

### Navigation Button

```yaml
type: button
name: Bedroom
icon: mdi:bed
tap_action:
  action: navigate
  navigation_path: /lovelace/bedroom
```

## Action Types

Home Assistant cards support three action types:

| Action | Trigger | Use Case |
|--------|---------|----------|
| `tap_action` | Single tap/click | Primary action (toggle, navigate, service call) |
| `hold_action` | Press and hold 0.5s+ | Secondary action (more-info, different service) |
| `double_tap_action` | Two quick taps | Tertiary action (navigate, custom service) |

## Available Actions

| Action | Description | Example Use |
|--------|-------------|-------------|
| `none` | Do nothing | Disable interaction |
| `toggle` | Toggle entity on/off | Lights, switches |
| `more-info` | Show entity details dialog | View sensor history |
| `navigate` | Go to another view/dashboard | Room navigation |
| `url` | Open external URL | Documentation, web apps |
| `perform-action` (was `call-service`) | Execute HA service | Scripts, automations, scenes |
| `assist` | Trigger voice assistant | Voice commands |

## Instructions

### Using Native Button Card

The native button card provides basic entity control with action support.

### Entity Toggle Button

```yaml
type: button
entity: light.bedroom
name: Bedroom Light
icon: mdi:ceiling-light
show_name: true
show_icon: true
show_state: true
tap_action:
  action: toggle
hold_action:
  action: more-info
double_tap_action:
  action: none
```

### Climate Control Button

```yaml
type: button
entity: climate.living_room
name: AC
icon: mdi:air-conditioner
show_state: true
tap_action:
  action: toggle
hold_action:
  action: more-info
```

### Scene Activation Button

```yaml
type: button
name: Movie Mode
icon: mdi:movie
tap_action:
  action: perform-action
  perform_action: scene.turn_on
  target:
    entity_id: scene.movie_mode
```

### Script Execution Button

```yaml
type: button
name: Good Night
icon: mdi:sleep
tap_action:
  action: perform-action
  perform_action: script.good_night
hold_action:
  action: none
```

### External URL Button

```yaml
type: button
name: Router Admin
icon: mdi:router-wireless
tap_action:
  action: url
  url_path: http://192.168.1.1
```

### Assist/Voice Button

```yaml
type: button
name: Voice Assistant
icon: mdi:microphone
tap_action:
  action: assist
```

## Service Calls

### Turn Off All Lights

```yaml
type: button
name: All Lights Off
icon: mdi:lightbulb-off
tap_action:
  action: perform-action
  perform_action: light.turn_off
  data:
    entity_id: all
```

### Set Climate Temperature

```yaml
type: button
name: Set Temp 22°C
icon: mdi:thermostat
tap_action:
  action: perform-action
  perform_action: climate.set_temperature
  target:
    entity_id: climate.living_room
  data:
    temperature: 22
```

### Turn On Light with Brightness

```yaml
type: button
name: Dim Lights
icon: mdi:lightbulb-on-50
tap_action:
  action: perform-action
  perform_action: light.turn_on
  target:
    entity_id: light.living_room_dimmer
  data:
    brightness: 150
```

### Run Automation

```yaml
type: button
name: Trigger Automation
icon: mdi:home-automation
tap_action:
  action: perform-action
  perform_action: automation.trigger
  target:
    entity_id: automation.motion_lights
```

## Navigation Patterns

### Simple Navigation

```yaml
type: button
name: Go to Bedroom
icon: mdi:bed
tap_action:
  action: navigate
  navigation_path: /lovelace/bedroom
```

### Room Navigation Grid

```yaml
type: grid
columns: 2
cards:
  - type: button
    name: Living Room
    icon: mdi:sofa
    tap_action:
      action: navigate
      navigation_path: /lovelace/living-room

  - type: button
    name: Bedroom
    icon: mdi:bed
    tap_action:
      action: navigate
      navigation_path: /lovelace/bedroom

  - type: button
    name: Kitchen
    icon: mdi:fridge
    tap_action:
      action: navigate
      navigation_path: /lovelace/kitchen

  - type: button
    name: Outdoors
    icon: mdi:tree
    tap_action:
      action: navigate
      navigation_path: /lovelace/outdoors
```

### Back to Home Button

```yaml
type: button
name: Home
icon: mdi:home
tap_action:
  action: navigate
  navigation_path: /lovelace/home
```

## Custom Button Card (HACS)

**Installation:** HACS → Frontend → Search "button-card"

The custom button-card provides extensive templating, state-based styling, and advanced action configurations. For complete template examples and advanced patterns, see [references/custom-button-card-templates.md](references/custom-button-card-templates.md).

### Basic Custom Button

```yaml
type: custom:button-card
entity: light.bedroom
name: Bedroom Light
show_state: true
icon: mdi:ceiling-light
tap_action:
  action: toggle
hold_action:
  action: more-info
```

### State-Based Styling

```yaml
type: custom:button-card
entity: light.bedroom
name: Bedroom Light
show_state: true
icon: mdi:ceiling-light
color: auto
state:
  - value: "on"
    color: rgb(255, 200, 100)  # Warm white when on
    icon: mdi:ceiling-light-on
  - value: "off"
    color: rgb(100, 100, 100)  # Gray when off
    icon: mdi:ceiling-light-off
tap_action:
  action: toggle
```


See [references/custom-button-card-templates.md](references/custom-button-card-templates.md) for advanced examples including temperature thresholds, multiple service calls, and icon-specific tap actions.

## Troubleshooting

### Button Not Responding

- Check entity exists in HA (Developer Tools → States)
- Verify service name is correct (`perform-action` not `call-service` in newer HA)
- Check browser console for errors (F12)

### Service Call Fails

- Test service in Developer Tools → Services first
- Verify entity_id or target format
- Check service data syntax (YAML indentation)

### Navigation Not Working

- Ensure view path is defined (e.g., `path: bedroom`)
- Use full navigation path: `/lovelace/bedroom`
- Check for typos in navigation_path

### Custom Button Card Not Loading

- Verify HACS installation (Frontend category)
- Clear browser cache (Ctrl+Shift+R)
- Check Lovelace resources (Settings → Dashboards → Resources)

## References

For advanced configurations, see:

- [references/action-reference.md](references/action-reference.md) - Complete action type documentation
- [references/service-calls.md](references/service-calls.md) - Common service call patterns
- [references/custom-button-card-templates.md](references/custom-button-card-templates.md) - Reusable button templates

## Official Documentation

- [Button card - Home Assistant](https://www.home-assistant.io/dashboards/button/)
- [Actions - Home Assistant](https://www.home-assistant.io/dashboards/actions/)
- [Custom Button Card GitHub](https://github.com/custom-cards/button-card)
