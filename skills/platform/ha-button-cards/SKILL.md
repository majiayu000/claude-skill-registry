---
name: ha-button-cards
description: "Create and configure Home Assistant button cards with actions (tap, hold, double-tap), service calls, navigation, and custom button-card (HACS) with templating and state-based styling. Use when creating interactive buttons, service call triggers, navigation controls, or custom buttons with conditional styling and multiple actions."
---

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

## Native Button Card

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

The custom button-card provides extensive templating, state-based styling, and advanced action configurations.

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

### Temperature Color Thresholds

```yaml
type: custom:button-card
entity: sensor.temperature
name: Temperature
show_state: true
icon: mdi:thermometer
color: auto
state:
  - value: 0
    operator: "<"
    color: rgb(0, 102, 255)  # Blue (cold)
  - value: 18
    operator: ">="
    color: rgb(46, 204, 113)  # Green (comfortable)
  - value: 26
    operator: ">="
    color: rgb(241, 196, 15)  # Yellow (warm)
  - value: 30
    operator: ">="
    color: rgb(231, 76, 60)  # Red (hot)
tap_action:
  action: more-info
```

### Multiple Service Calls (via Script)

```yaml
type: custom:button-card
name: Movie Mode
icon: mdi:movie
tap_action:
  action: call-service
  service: script.movie_mode
  service_data:
    lights: "dim"
    blinds: "close"
    tv: "on"
```

### Icon-Specific Tap Action

```yaml
type: custom:button-card
entity: climate.bedroom
name: Bedroom AC
tap_action:
  action: more-info
custom_fields:
  icon:
    tap_action:
      action: perform-action
      perform_action: climate.turn_off
      target:
        entity_id: climate.bedroom
```

### Double-Tap Action

```yaml
type: custom:button-card
entity: light.bedroom
name: Bedroom Light
tap_action:
  action: toggle
hold_action:
  action: perform-action
  perform_action: scene.turn_on
  data:
    entity_id: scene.bedtime
double_tap_action:
  action: more-info
icon: mdi:ceiling-light
color: auto
```

### Templated Name and Icon

```yaml
type: custom:button-card
entity: sensor.lights_on
name: |
  [[[
    return `${states['sensor.lights_on'].state} Lights On`;
  ]]]
icon: mdi:lightbulb
color: |
  [[[
    if (states['sensor.lights_on'].state > 0) return 'rgb(255, 200, 100)';
    return 'rgb(100, 100, 100)';
  ]]]
tap_action:
  action: navigate
  navigation_path: /lovelace/lights
```

### Confirmation Dialog

```yaml
type: custom:button-card
name: Restart Home Assistant
icon: mdi:restart
confirmation:
  text: "Are you sure you want to restart?"
tap_action:
  action: perform-action
  perform_action: homeassistant.restart
```

### Custom Styles

```yaml
type: custom:button-card
entity: light.living_room
name: Living Room
icon: mdi:lightbulb
styles:
  card:
    - height: 100px
    - border-radius: 15px
  name:
    - font-size: 18px
    - font-weight: bold
  icon:
    - width: 50px
    - height: 50px
tap_action:
  action: toggle
```

### Show Last Changed

```yaml
type: custom:button-card
entity: binary_sensor.motion_living_room
name: Living Room Motion
show_last_changed: true
icon: mdi:motion-sensor
color: auto
state:
  - value: "on"
    color: orange
  - value: "off"
    color: gray
```

## Real-World Patterns

### Climate Control Panel

```yaml
type: grid
columns: 2
cards:
  # Turn on ACs
  - type: custom:button-card
    name: All ACs On
    icon: mdi:air-conditioner
    tap_action:
      action: perform-action
      perform_action: climate.turn_on
      target:
        entity_id: all

  # Turn off ACs
  - type: custom:button-card
    name: All ACs Off
    icon: mdi:air-conditioner-off
    tap_action:
      action: perform-action
      perform_action: climate.turn_off
      target:
        entity_id: all

  # Set temp 22°C
  - type: custom:button-card
    name: Set 22°C
    icon: mdi:thermometer
    tap_action:
      action: perform-action
      perform_action: climate.set_temperature
      target:
        entity_id:
          - climate.snorlug
          - climate.mines_of_moria
      data:
        temperature: 22

  # Set temp 24°C
  - type: custom:button-card
    name: Set 24°C
    icon: mdi:thermometer
    tap_action:
      action: perform-action
      perform_action: climate.set_temperature
      target:
        entity_id:
          - climate.snorlug
          - climate.mines_of_moria
      data:
        temperature: 24
```

### Lighting Scenes

```yaml
type: horizontal-stack
cards:
  - type: custom:button-card
    name: Bright
    icon: mdi:lightbulb-on
    tap_action:
      action: perform-action
      perform_action: scene.turn_on
      target:
        entity_id: scene.bright_lights

  - type: custom:button-card
    name: Dim
    icon: mdi:lightbulb-on-50
    tap_action:
      action: perform-action
      perform_action: scene.turn_on
      target:
        entity_id: scene.dim_lights

  - type: custom:button-card
    name: Off
    icon: mdi:lightbulb-off
    tap_action:
      action: perform-action
      perform_action: light.turn_off
      data:
        entity_id: all
```

### Irrigation Manual Controls

```yaml
type: vertical-stack
cards:
  - type: markdown
    content: "## Irrigation Manual Controls"

  - type: grid
    columns: 2
    cards:
      # Zone 1
      - type: custom:button-card
        entity: switch.s01_left_top_patio_lawn_station_enabled
        name: Zone 1
        icon: mdi:sprinkler
        show_state: true
        tap_action:
          action: toggle

      # Zone 2
      - type: custom:button-card
        entity: switch.s02_right_top_patio_lawn_station_enabled
        name: Zone 2
        icon: mdi:sprinkler
        show_state: true
        tap_action:
          action: toggle

      # All zones off
      - type: custom:button-card
        name: Stop All Zones
        icon: mdi:stop
        tap_action:
          action: perform-action
          perform_action: switch.turn_off
          target:
            entity_id:
              - switch.s01_left_top_patio_lawn_station_enabled
              - switch.s02_right_top_patio_lawn_station_enabled
        styles:
          card:
            - background-color: rgb(231, 76, 60)
```

### Device Status with Navigation

```yaml
type: custom:button-card
entity: sensor.motion_sensor_living_room_battery
name: Living Room Motion
icon: mdi:motion-sensor
show_state: true
color: |
  [[[
    const battery = states['sensor.motion_sensor_living_room_battery'].state;
    if (battery < 20) return 'red';
    if (battery < 50) return 'orange';
    return 'green';
  ]]]
tap_action:
  action: more-info
hold_action:
  action: navigate
  navigation_path: /lovelace/sensors
```

## Best Practices

### 1. Use Descriptive Names

```yaml
# Good
type: button
name: Turn Off All Lights
icon: mdi:lightbulb-off

# Bad
type: button
name: Off
icon: mdi:lightbulb-off
```

### 2. Disable Unused Actions

```yaml
type: button
entity: light.bedroom
tap_action:
  action: toggle
hold_action:
  action: none  # Disable hold if not needed
double_tap_action:
  action: none  # Disable double-tap if not needed
```

### 3. Show State for Toggles

```yaml
type: button
entity: light.living_room
show_state: true  # User sees on/off state
tap_action:
  action: toggle
```

### 4. Use Icons Consistently

- `mdi:lightbulb` for lights
- `mdi:air-conditioner` for climate
- `mdi:sprinkler` for irrigation
- `mdi:home` for home/back navigation
- `mdi:bed` for bedroom
- `mdi:sofa` for living room

### 5. Group Related Actions

```yaml
type: grid
columns: 3
cards:
  # Group all light controls together
  - type: button
    entity: light.all_lights
  - type: button
    name: Bright
    tap_action:
      action: perform-action
      perform_action: scene.turn_on
      target:
        entity_id: scene.bright
  - type: button
    name: Dim
    tap_action:
      action: perform-action
      perform_action: scene.turn_on
      target:
        entity_id: scene.dim
```

### 6. Use Confirmation for Destructive Actions

```yaml
type: custom:button-card
name: Restart HA
icon: mdi:restart
confirmation:
  text: "Are you sure?"
tap_action:
  action: perform-action
  perform_action: homeassistant.restart
```

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
