---
name: ha-conditional-cards
description: |
  Implements conditional visibility for Home Assistant dashboard cards using state, numeric_state,
  screen, user, time, and/or conditions via Conditional Card wrapper and per-card visibility
  property. Use when asked to "hide card when", "show only if", "user-specific dashboard",
  "mobile vs desktop cards", "conditional visibility", or "show card based on state/time/user".

---

Works with Lovelace YAML dashboards and conditional/visibility card configurations.
# Home Assistant Conditional Cards

Control card visibility dynamically based on states, users, screen size, and complex conditions.

## Overview

Home Assistant provides two approaches for conditional visibility:
- **Conditional Card** (wrapper): Shows/hides entire card based on conditions
- **Per-Card Visibility**: Native `visibility` property on any card

Both support multiple condition types:
- **state**: Entity matches specific state
- **numeric_state**: Sensor value within range
- **screen**: Screen width/media queries
- **user**: Current user matches list
- **time**: Current time within range
- **and/or**: Complex logic combinations

## When to Use This Skill

Use this skill when you need to:
- Show cards only when specific conditions are met (person home, motion detected, temperature threshold)
- Create responsive dashboards with mobile vs desktop layouts
- Build user-specific views with different access levels
- Display time-based cards (daytime vs nighttime controls)
- Combine multiple conditions with AND/OR logic for complex visibility rules

Do NOT use when:
- You need to modify card content based on state (use template cards instead)
- Building static dashboards where all cards are always visible
- Checking entity attributes directly (create template sensor first)

## Quick Start

### Conditional Card (Wrapper)

```yaml
type: conditional
conditions:
  - condition: state
    entity: person.john
    state: home
card:
  type: entities
  entities:
    - light.bedroom
```

### Per-Card Visibility (Native)

```yaml
type: entities
entities:
  - light.bedroom
visibility:
  - condition: state
    entity: person.john
    state: home
```

## Usage

1. **Choose approach**: Use Conditional Card wrapper for complex logic, per-card visibility for simple conditions
2. **Select condition type**: state, numeric_state, screen, user, time, and/or
3. **Apply condition**: Add `conditions` to conditional card or `visibility` to any card
4. **Test in edit mode**: Exit edit mode to test visibility (cards always show when editing)
5. **Verify entity states**: Check Developer Tools → States to debug conditions

See Condition Types Reference below for all available conditions and syntax.

## Condition Types Reference

| Condition | Parameters | Use Case |
|-----------|------------|----------|
| `state` | `entity`, `state` | Show when entity has specific state |
| `numeric_state` | `entity`, `above`, `below` | Show when sensor in range |
| `screen` | `media_query` | Show based on screen width |
| `user` | `users` (list of user IDs) | Show for specific users only |
| `time` | `after`, `before` | Show during specific time window |
| `and` | List of conditions | All conditions must be true |
| `or` | List of conditions | At least one condition must be true |

## State Conditions

### Basic State Match

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.motion_living_room
    state: "on"
card:
  type: camera
  entity: camera.living_room
```

### Multiple State Options

```yaml
visibility:
  - condition: state
    entity: climate.living_room
    state_not:
      - "off"
      - unavailable
```

### State with Attributes (Workaround)

**Note:** Native conditional cards don't support attribute conditions. Create a template sensor instead.

```yaml
# In configuration.yaml
template:
  - sensor:
      - name: "AC Mode Cool"
        state: "{{ state_attr('climate.living_room', 'hvac_mode') == 'cool' }}"

# In dashboard
visibility:
  - condition: state
    entity: sensor.ac_mode_cool
    state: "True"
```

## Numeric State Conditions

### Temperature Range

```yaml
type: entities
entities:
  - climate.bedroom
visibility:
  - condition: numeric_state
    entity: sensor.temperature
    above: 18
    below: 30
```

### Above Threshold

```yaml
visibility:
  - condition: numeric_state
    entity: sensor.battery
    below: 20  # Show when battery < 20%
```

### Between Values

```yaml
visibility:
  - condition: numeric_state
    entity: sensor.humidity
    above: 40
    below: 60  # Show when 40% < humidity < 60%
```

## Screen/Responsive Conditions

### Mobile Only

```yaml
visibility:
  - condition: screen
    media_query: "(max-width: 600px)"
```

### Desktop Only

```yaml
visibility:
  - condition: screen
    media_query: "(min-width: 1280px)"
```

### Tablet Range

```yaml
visibility:
  - condition: screen
    media_query: "(min-width: 601px) and (max-width: 1279px)"
```

### Common Media Queries

```yaml
# Mobile (portrait)
media_query: "(max-width: 600px)"

# Tablet (portrait)
media_query: "(min-width: 601px) and (max-width: 900px)"

# Desktop
media_query: "(min-width: 1280px)"

# Landscape orientation
media_query: "(orientation: landscape)"

# Portrait orientation
media_query: "(orientation: portrait)"
```

## User Conditions

### Single User

```yaml
visibility:
  - condition: user
    users:
      - 1234567890abcdef  # User ID (not username)
```

### Multiple Users (Admin Access)

```yaml
type: entities
entities:
  - switch.advanced_settings
visibility:
  - condition: user
    users:
      - 1234567890abcdef  # Admin user 1
      - fedcba0987654321  # Admin user 2
```

**Finding User IDs:**
1. Go to Settings → People
2. Click on user
3. User ID is in the URL: `/config/person/USER_ID_HERE`

## Time Conditions

### During Daytime

```yaml
visibility:
  - condition: time
    after: "06:00:00"
    before: "22:00:00"
```

### Night Mode Cards

```yaml
visibility:
  - condition: time
    after: "22:00:00"
    before: "06:00:00"
```

### Business Hours

```yaml
visibility:
  - condition: time
    after: "09:00:00"
    before: "17:00:00"
    weekday:
      - mon
      - tue
      - wed
      - thu
      - fri
```

## Complex Logic (AND/OR)

### AND Condition (All Must Be True)

```yaml
visibility:
  - condition: and
    conditions:
      - condition: state
        entity: person.john
        state: home
      - condition: numeric_state
        entity: sensor.temperature
        below: 18
      - condition: time
        after: "06:00:00"
        before: "23:00:00"
```

### OR Condition (At Least One Must Be True)

```yaml
visibility:
  - condition: or
    conditions:
      - condition: state
        entity: person.john
        state: home
      - condition: state
        entity: person.jane
        state: home
```

### Nested Logic

```yaml
visibility:
  - condition: and
    conditions:
      # Show during daytime...
      - condition: time
        after: "06:00:00"
        before: "22:00:00"
      # ...AND (someone is home OR security is armed)
      - condition: or
        conditions:
          - condition: state
            entity: person.john
            state: home
          - condition: state
            entity: alarm_control_panel.home
            state: armed_away
```

## Real-World Patterns

### Show Camera When Motion Detected

```yaml
type: conditional
conditions:
  - condition: state
    entity: binary_sensor.motion_living_room
    state: "on"
card:
  type: camera
  entity: camera.living_room
```

### Mobile vs Desktop Layout

```yaml
# Mobile: Compact view
type: custom:mushroom-chips-card
visibility:
  - condition: screen
    media_query: "(max-width: 600px)"

# Desktop: Detailed view
type: grid
columns: 3
visibility:
  - condition: screen
    media_query: "(min-width: 1280px)"
```

### User-Specific Controls

```yaml
type: entities
entities:
  - switch.developer_mode
visibility:
  - condition: user
    users:
      - 1234567890abcdef  # Admin user ID (Settings → People → URL)
```

For more patterns (low battery alerts, temperature warnings, occupied rooms, time-based controls), see `references/advanced-patterns.md`.

## Best Practices

1. **Combine approaches**: Use conditional card for complex logic, per-card visibility for simple conditions
2. **Test in edit mode**: Exit edit mode to test visibility (cards always visible when editing)
3. **Use helper entities**: Create template sensors for attribute-based or complex conditions
4. **Add buffer zones**: Use hysteresis for numeric conditions to prevent flapping
5. **Document user IDs**: Keep reference of user IDs for maintenance
6. **Screen conditions**: Use media queries for responsive mobile/desktop layouts

## Limitations

**Cannot check attributes directly** - Create template sensor to expose attribute as entity state.

**No template conditions** - Create template binary sensor instead.

**Always visible in edit mode** - Must exit edit mode to test visibility behavior.

For detailed workarounds, see `references/advanced-patterns.md`.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Card not hiding | Exit edit mode, check entity state, verify YAML indentation |
| User condition fails | Use user ID (not username), find in Settings → People → URL |
| Time condition fails | Use 24-hour format `"23:00:00"`, check HA timezone |
| Numeric condition fails | Verify sensor has numeric state (not "unknown") |
| Screen condition fails | Test on actual device (not browser resize) |

For detailed troubleshooting, see `references/advanced-patterns.md`.

## Supporting Files

- **references/advanced-patterns.md** - Complex logic patterns, real-world use cases, workarounds, detailed troubleshooting, best practices, common media queries

## Official Documentation

- [Conditional card - Home Assistant](https://www.home-assistant.io/dashboards/conditional/)
- [Card Visibility - Home Assistant](https://www.home-assistant.io/dashboards/cards/#card-visibility)
- [Template Sensors - Home Assistant](https://www.home-assistant.io/integrations/template/)
