---
name: ha-mushroom-cards
description: "Create minimalist, mobile-first Home Assistant dashboards using the Mushroom cards ecosystem (13+ card types) with card-mod styling. Use when building modern HA dashboards, creating compact mobile interfaces, styling entity cards, using chips for status indicators, or combining Mushroom with card-mod for custom CSS styling."
---

# Home Assistant Mushroom Cards

Build minimalist, mobile-first Home Assistant dashboards using the Mushroom cards design system.

##Overview

**Installation:** HACS → Frontend → Search "Mushroom"

Mushroom is a complete design system for Home Assistant featuring:
- 13+ specialized card types for entities, controls, and status display
- Minimalist Material Design aesthetic
- Full UI editor support (no YAML required)
- Mobile-first responsive design
- Card-mod integration for advanced styling

## Card Selection Guide

| Card Type | Purpose | Best For |
|-----------|---------|----------|
| `mushroom-entity-card` | General entity display | Sensors, switches, any entity |
| `mushroom-light-card` | Light control | Brightness, color picker |
| `mushroom-climate-card` | HVAC control | Temperature, mode, fan |
| `mushroom-cover-card` | Blinds/garage | Position, tilt control |
| `mushroom-fan-card` | Fan control | Speed, oscillation |
| `mushroom-lock-card` | Lock control | Lock/unlock with confirmation |
| `mushroom-media-player-card` | Media control | Playback, volume, source |
| `mushroom-person-card` | Person tracking | Location, picture |
| `mushroom-chips-card` | Compact status indicators | Quick status/actions |
| `mushroom-template-card` | Custom templating | Jinja2 templates, dynamic content |
| `mushroom-title-card` | Section headers | View organization |

## Quick Start

### Entity Card

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature_living_room
name: Living Room
icon: mdi:thermometer
icon_color: red
tap_action:
  action: more-info
```

### Light Card

```yaml
type: custom:mushroom-light-card
entity: light.bedroom
name: Bedroom Light
show_brightness_control: true
show_color_control: true
use_light_color: true
```

### Climate Card

```yaml
type: custom:mushroom-climate-card
entity: climate.living_room
show_temperature_control: true
collapsible_controls: true
hvac_modes:
  - heat_cool
  - cool
  - heat
  - 'off'
```

## Core Cards

### 1. Entity Card (General Purpose)

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
name: Temperature
icon: mdi:thermometer
icon_color: red
secondary_info: last-changed
tap_action:
  action: more-info
hold_action:
  action: navigate
  navigation_path: /lovelace/climate
```

**Icon Colors:** red, pink, purple, deep-purple, indigo, blue, light-blue, cyan, teal, green, light-green, lime, yellow, amber, orange, deep-orange, brown, grey, blue-grey, white, black, disabled

### 2. Light Card

```yaml
type: custom:mushroom-light-card
entity: light.living_room
name: Living Room
show_brightness_control: true
show_color_control: true
show_color_temp_control: true
use_light_color: true
collapsible_controls: true
tap_action:
  action: toggle
```

### 3. Climate Card

```yaml
type: custom:mushroom-climate-card
entity: climate.snorlug
name: Snorlug AC
show_temperature_control: true
hvac_modes:
  - cool
  - heat
  - heat_cool
  - fan_only
  - dry
  - 'off'
collapsible_controls: true
```

### 4. Cover Card (Blinds/Garage)

```yaml
type: custom:mushroom-cover-card
entity: cover.garage_door
name: Garage Door
show_position_control: true
show_tilt_position_control: false
```

### 5. Fan Card

```yaml
type: custom:mushroom-fan-card
entity: fan.bedroom
name: Bedroom Fan
show_percentage_control: true
show_oscillate_control: true
collapsible_controls: true
```

### 6. Lock Card

```yaml
type: custom:mushroom-lock-card
entity: lock.front_door
name: Front Door
```

### 7. Media Player Card

```yaml
type: custom:mushroom-media-player-card
entity: media_player.living_room_tv
name: Living Room TV
use_media_info: true
show_volume_level: true
collapsible_controls: true
media_controls:
  - play_pause_stop
  - previous
  - next
volume_controls:
  - volume_mute
  - volume_set
```

### 8. Person Card

```yaml
type: custom:mushroom-person-card
entity: person.john
name: John
use_entity_picture: true
icon: mdi:account
```

## Chips Card (Status Indicators)

The chips card displays compact status indicators and quick actions.

### Basic Chips

```yaml
type: custom:mushroom-chips-card
chips:
  - type: entity
    entity: sensor.temperature
    icon_color: red
  - type: weather
    entity: weather.home
    show_conditions: true
  - type: action
    icon: mdi:lightbulb
    tap_action:
      action: perform-action
      perform_action: light.turn_off
      data:
        entity_id: all
```

### Chip Types

**Entity Chip:**
```yaml
- type: entity
  entity: sensor.temperature
  icon: mdi:thermometer
  icon_color: red
  content_info: state
```

**Weather Chip:**
```yaml
- type: weather
  entity: weather.home
  show_conditions: true
  show_temperature: true
```

**Action Chip:**
```yaml
- type: action
  icon: mdi:home
  icon_color: blue
  tap_action:
    action: navigate
    navigation_path: /lovelace/home
```

**Menu Chip:**
```yaml
- type: menu
```

**Back Chip:**
```yaml
- type: back
```

**Light Chip:**
```yaml
- type: light
  entity: light.bedroom
  use_light_color: true
  content_info: state
```

**Template Chip:**
```yaml
- type: template
  icon: mdi:lightbulb
  content: "{{ states('sensor.lights_on') }} lights"
  icon_color: >-
    {% if states('sensor.lights_on') | int > 0 %}
      orange
    {% else %}
      grey
    {% endif %}
  tap_action:
    action: navigate
    navigation_path: /lovelace/lights
```

## Template Card (Advanced)

Template cards use Jinja2 for dynamic content.

```yaml
type: custom:mushroom-template-card
primary: "{{ states('sensor.temperature') }}°C"
secondary: "Feels like {{ state_attr('weather.home', 'temperature') }}°C"
icon: mdi:thermometer
icon_color: >-
  {% set temp = states('sensor.temperature') | float %}
  {% if temp < 18 %}
    blue
  {% elif temp < 25 %}
    green
  {% else %}
    red
  {% endif %}
badge_icon: >-
  {% if is_state('binary_sensor.window_open', 'on') %}
    mdi:window-open
  {% endif %}
badge_color: orange
tap_action:
  action: more-info
  entity: sensor.temperature
```

### Template Examples

**Lights On Counter:**
```yaml
type: custom:mushroom-template-card
primary: "{{ states('sensor.lights_on') }} Lights On"
secondary: >-
  {% if states('sensor.lights_on') | int == 0 %}
    All lights off
  {% else %}
    {{ states('sensor.lights_on') }} active
  {% endif %}
icon: mdi:lightbulb
icon_color: >-
  {% if states('sensor.lights_on') | int > 0 %}
    amber
  {% else %}
    grey
  {% endif %}
```

**Battery Status:**
```yaml
type: custom:mushroom-template-card
primary: "{{ state_attr('sensor.phone_battery', 'friendly_name') }}"
secondary: "{{ states('sensor.phone_battery') }}%"
icon: >-
  {% set battery = states('sensor.phone_battery') | int %}
  {% if battery > 80 %}
    mdi:battery
  {% elif battery > 50 %}
    mdi:battery-60
  {% elif battery > 20 %}
    mdi:battery-30
  {% else %}
    mdi:battery-alert
  {% endif %}
icon_color: >-
  {% set battery = states('sensor.phone_battery') | int %}
  {% if battery < 20 %}
    red
  {% elif battery < 50 %}
    orange
  {% else %}
    green
  {% endif %}
```

## Title Card (Section Headers)

```yaml
type: custom:mushroom-title-card
title: Climate Control
subtitle: Temperature and AC settings
alignment: left
```

## Card-Mod Styling

**Installation:** HACS → Frontend → Search "card-mod"

Card-mod injects custom CSS into Mushroom cards for advanced styling.

### Transparent Background

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
card_mod:
  style: |
    ha-card {
      background: rgba(0, 0, 0, 0.3);
      border-radius: 15px;
    }
```

### Large Icon

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
card_mod:
  style: |
    mushroom-shape-icon {
      --icon-size: 80px;
    }
```

### Custom Font Sizes

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
card_mod:
  style: |
    ha-card {
      --card-primary-font-size: 24px;
      --card-secondary-font-size: 16px;
    }
```

### Conditional Styling

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
card_mod:
  style: |
    :host {
      {% if states('sensor.temperature') | float > 25 %}
        --card-mod-icon-color: red;
      {% elif states('sensor.temperature') | float < 18 %}
        --card-mod-icon-color: blue;
      {% else %}
        --card-mod-icon-color: green;
      {% endif %}
    }
```

### Grid Spanning

```yaml
type: custom:mushroom-entity-card
entity: sensor.temperature
card_mod:
  style:
    .: |
      :host {
        grid-column: span 2;  # Take 2 columns
        grid-row: span 1;     # Take 1 row
      }
```

### Animated Cards

```yaml
type: custom:mushroom-chips-card
chips:
  - type: template
    icon: mdi:lightbulb
    content: "{{ states('sensor.lights_on') }}"
card_mod:
  style: |
    ha-card {
      animation: pulse 2s ease-in-out infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.7; }
    }
```

## Real-World Examples

### Climate Control Panel

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Climate
    subtitle: All AC units

  - type: grid
    columns: 2
    cards:
      - type: custom:mushroom-climate-card
        entity: climate.snorlug
        show_temperature_control: true
        collapsible_controls: true

      - type: custom:mushroom-climate-card
        entity: climate.mines_of_moria
        show_temperature_control: true
        collapsible_controls: true
```

### Status Chips Bar

```yaml
type: custom:mushroom-chips-card
chips:
  - type: weather
    entity: weather.home
    show_conditions: true

  - type: template
    icon: mdi:lightbulb
    content: "{{ states('sensor.lights_on') }}"
    icon_color: >-
      {% if states('sensor.lights_on') | int > 0 %}
        amber
      {% else %}
        grey
      {% endif %}
    tap_action:
      action: navigate
      navigation_path: /lovelace/lights

  - type: template
    icon: mdi:window-open
    content: "{{ states('sensor.windows_open') }}"
    icon_color: >-
      {% if states('sensor.windows_open') | int > 0 %}
        orange
      {% else %}
        grey
      {% endif %}

  - type: entity
    entity: sensor.temperature
    icon_color: red
```

### Irrigation Control

```yaml
type: vertical-stack
cards:
  - type: custom:mushroom-title-card
    title: Irrigation
    subtitle: Manual zone control

  - type: grid
    columns: 2
    cards:
      - type: custom:mushroom-entity-card
        entity: switch.s01_left_top_patio_lawn_station_enabled
        name: Zone 1
        icon: mdi:sprinkler
        tap_action:
          action: toggle

      - type: custom:mushroom-entity-card
        entity: switch.s02_right_top_patio_lawn_station_enabled
        name: Zone 2
        icon: mdi:sprinkler
        tap_action:
          action: toggle
```

## Best Practices

### 1. Use Collapsible Controls

```yaml
type: custom:mushroom-climate-card
entity: climate.living_room
collapsible_controls: true  # Hides controls until tapped (mobile-friendly)
```

### 2. Combine with Chips for Status

```yaml
# Put chips at top of view for quick status
- type: custom:mushroom-chips-card
  chips:
    - type: weather
    - type: template (lights count)
    - type: template (windows open)
```

### 3. Use Title Cards for Sections

```yaml
- type: custom:mushroom-title-card
  title: Section Name

- type: grid
  columns: 2
  cards: [...]
```

### 4. Enable use_light_color

```yaml
type: custom:mushroom-light-card
entity: light.bedroom
use_light_color: true  # Shows actual light color
```

### 5. Template for Dynamic Content

```yaml
# Use template cards for counts, calculations, conditional text
type: custom:mushroom-template-card
primary: "{{ states('sensor.lights_on') }} Lights"
```

## Troubleshooting

### Card Not Loading

- Verify HACS installation (Frontend category)
- Clear browser cache (Ctrl+Shift+R)
- Check Lovelace resources (Settings → Dashboards → Resources)

### Icons Not Showing

- Use valid MDI icon names (`mdi:icon-name`)
- Check icon name at [https://pictogrammers.com/library/mdi/](https://pictogrammers.com/library/mdi/)

### Card-Mod Not Working

- Ensure card-mod is installed as a Frontend module
- Verify CSS syntax using browser DevTools (F12)
- Check for conflicting card-mod styles

### Templates Not Updating

- Verify Jinja2 syntax
- Test templates in Developer Tools → Template
- Check entity_id exists in HA

## Official Documentation

- [Mushroom Cards GitHub](https://github.com/piitaya/lovelace-mushroom)
- [Card-Mod GitHub](https://github.com/thomasloven/lovelace-card-mod)
- [Mushroom Styling Guide (Community)](https://community.home-assistant.io/t/mushroom-cards-card-mod-styling-config-guide/600472)
