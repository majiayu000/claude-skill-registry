---
name: ha-automation
description: "Create and debug Home Assistant automations, scripts, blueprints, and Jinja2 templates. Use when working with triggers, conditions, actions, automation YAML, scripts, blueprints, or template expressions. Activates on keywords: automation, trigger, condition, action, blueprint, script, template, jinja2."
---

# Home Assistant Automation Expert

> Master Home Assistant automations, scripts, blueprints, and Jinja2 templating with confidence.

## Before You Start

This skill prevents common automation mistakes including:
1. **Incorrect trigger syntax** - Using deprecated formats or invalid entity IDs
2. **Missing condition operators** - Forgetting `and`/`or`/`not` conjunctions
3. **Jinja2 template errors** - Undefined variables or incorrect filter usage
4. **Blueprint parameterization issues** - Missing `!input` substitutions or misaligned selectors

## Quick Reference: Automation Structure

### Basic Automation Format

```yaml
automation: !include automations.yaml
```

### Single Automation File

```yaml
- alias: "My Automation"
  description: "What this automation does"
  trigger: ...
  condition: ...
  action: ...
  mode: single
```

## Triggers Quick Reference

### State Trigger
```yaml
trigger:
  platform: state
  entity_id: light.bedroom
  from: "off"
  to: "on"
  for:
    minutes: 5
```

### Numeric State Trigger
```yaml
trigger:
  platform: numeric_state
  entity_id: sensor.temperature
  above: 25
  below: 30
```

### Time Trigger
```yaml
trigger:
  platform: time
  at: "10:30:00"
```

### Time Pattern Trigger
```yaml
trigger:
  platform: time_pattern
  hours: "*/2"  # Every 2 hours
  minutes: 0
```

### Device Trigger
```yaml
trigger:
  platform: device
  device_id: abc123...
  domain: light
  type: turned_on
```

### Event Trigger
```yaml
trigger:
  platform: event
  event_type: call_service
  event_data:
    domain: light
```

### MQTT Trigger
```yaml
trigger:
  platform: mqtt
  topic: home/front_door/status
  payload: "opened"
```

### Webhook Trigger
```yaml
trigger:
  platform: webhook
  webhook_id: my_webhook_id
```

### Sun Trigger
```yaml
trigger:
  platform: sun
  event: sunrise
  offset: "-00:30:00"  # 30 min before sunrise
```

### Zone Trigger
```yaml
trigger:
  platform: zone
  entity_id: device_tracker.john
  zone: zone.home
  event: enter
```

### Template Trigger
```yaml
trigger:
  platform: template
  value_template: "{{ state_attr('light.bedroom', 'brightness') > 200 }}"
```

## Conditions Quick Reference

### State Condition
```yaml
condition:
  - condition: state
    entity_id: light.bedroom
    state: "on"
```

### Numeric State Condition
```yaml
condition:
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 20
    below: 25
```

### Time Condition
```yaml
condition:
  - condition: time
    after: "08:00:00"
    before: "20:00:00"
    weekday:
      - mon
      - tue
      - wed
```

### Sun Condition
```yaml
condition:
  - condition: sun
    after: sunrise
    before: sunset
```

### Template Condition
```yaml
condition:
  - condition: template
    value_template: "{{ states('light.bedroom') == 'on' }}"
```

### Combining Conditions
```yaml
condition:
  - condition: and
    conditions:
      - condition: state
        entity_id: light.bedroom
        state: "on"
      - condition: numeric_state
        entity_id: sensor.temperature
        above: 20
```

```yaml
condition:
  - condition: or
    conditions:
      - condition: state
        entity_id: binary_sensor.motion
        state: "on"
      - condition: state
        entity_id: light.bedroom
        state: "on"
```

## Actions Quick Reference

### Call Service Action
```yaml
action:
  - service: light.turn_on
    target:
      entity_id: light.bedroom
    data:
      brightness: 255
      color_temp: 366
```

### Call Service (Multiple Targets)
```yaml
action:
  - service: light.turn_on
    target:
      entity_id:
        - light.bedroom
        - light.living_room
      area_id: downstairs
```

### Choose (If/Then/Else)
```yaml
action:
  - choose:
      - conditions:
          - condition: state
            entity_id: light.bedroom
            state: "on"
        sequence:
          - service: light.turn_off
            target:
              entity_id: light.bedroom
      - conditions:
          - condition: state
            entity_id: light.bedroom
            state: "off"
        sequence:
          - service: light.turn_on
            target:
              entity_id: light.bedroom
    default:
      - service: notification.send
        data:
          message: "Unable to determine light state"
```

### Repeat (Loop)
```yaml
action:
  - repeat:
      count: 3
      sequence:
        - service: light.toggle
          target:
            entity_id: light.bedroom
        - delay:
            seconds: 1
```

### Delay
```yaml
action:
  - delay:
      minutes: 5
```

### Wait for Trigger
```yaml
action:
  - wait_for_trigger:
      platform: state
      entity_id: binary_sensor.motion
      to: "off"
    timeout:
      minutes: 30
  - service: light.turn_off
    target:
      entity_id: light.bedroom
```

### Parallel Actions
```yaml
action:
  - parallel:
      - service: light.turn_off
        target:
          entity_id: light.bedroom
      - service: switch.turn_off
        target:
          entity_id: switch.fan
```

## Automation Modes

```yaml
mode: single  # Default - cancel previous run
mode: restart  # Restart on retrigger
mode: queued  # Queue up to 10 retriggered runs
mode: parallel  # Allow multiple simultaneous runs
mode: queued  # with max: 10  # Limit queued runs
```

## Jinja2 Template Cheatsheet

### Common Variables
- `states('entity.id')` - Get entity state
- `state_attr('entity.id', 'attribute')` - Get entity attribute
- `now()` - Current datetime
- `as_timestamp('2024-01-01')` - Convert to timestamp
- `trigger` - Trigger object (if in trigger template)

### Filters
```jinja2
{{ value | float(0) }}  # Convert to float with default
{{ value | int(0) }}  # Convert to int with default
{{ value | round(2) }}  # Round to 2 decimal places
{{ value | timestamp_custom("%Y-%m-%d") }}  # Format timestamp
{{ value | replace("old", "new") }}  # Replace string
{{ value | lower }}  # Lowercase
{{ value | upper }}  # Uppercase
{{ value | length }}  # Get length
{{ list | list }}  # Convert to list
```

### Conditionals
```jinja2
{% if states('light.bedroom') == 'on' %}
  Light is on
{% elif states('light.bedroom') == 'off' %}
  Light is off
{% else %}
  Unknown
{% endif %}
```

### Loops
```jinja2
{% for entity in states.light %}
  {{ entity.name }}: {{ entity.state }}
{% endfor %}
```

### Math Operations
```jinja2
{{ 5 + 3 }}  # Addition
{{ 10 - 4 }}  # Subtraction
{{ 3 * 4 }}  # Multiplication
{{ 20 / 4 }}  # Division
{{ 17 % 5 }}  # Modulo (remainder)
```

### String Operations
```jinja2
{{ "hello " + "world" }}  # Concatenation
{{ value is string }}  # Type checking
{{ value is number }}
{{ value is defined }}  # Check if variable exists
{{ value | default("fallback") }}  # Provide default
```

### Debugging Templates
Use Developer Tools > Template in Home Assistant UI to test templates in real-time.

## Blueprint Creation Basics

### Blueprint Structure
```yaml
blueprint:
  name: "Friendly Name"
  description: "What this blueprint does"
  domain: automation
  source_url: "https://github.com/user/repo/path/to/blueprint.yaml"

  input:
    my_light:
      name: "Light to control"
      description: "The light entity to control"
      selector:
        entity:
          domain: light

    brightness_level:
      name: "Brightness"
      description: "Brightness percentage (0-100)"
      selector:
        number:
          min: 0
          max: 100
          unit_of_measurement: "%"

    duration:
      name: "Duration"
      description: "How long to stay on"
      selector:
        number:
          min: 1
          max: 60
          unit_of_measurement: "minutes"

    my_bool:
      name: "Enable feature"
      selector:
        boolean:

trigger: ...
condition: ...
action:
  - service: light.turn_on
    target:
      entity_id: !input my_light
    data:
      brightness: !input brightness_level
```

### Blueprint Selectors
```yaml
# Entity selector
selector:
  entity:
    domain: light

# Device selector
selector:
  device:
    integration: zwave
    manufacturer: Philips

# Area selector
selector:
  area:

# Number selector
selector:
  number:
    min: 0
    max: 100
    step: 5
    unit_of_measurement: "%"

# Text selector
selector:
  text:
    multiline: true

# Boolean selector
selector:
  boolean:

# Select (dropdown)
selector:
  select:
    options:
      - label: "Option 1"
        value: "value1"
      - label: "Option 2"
        value: "value2"
```

## Common Mistakes to Avoid

### ❌ Don't: Use old trigger format
```yaml
trigger:
  - platform: state
    entity_id: light.bedroom
```

### ✅ Do: Use nested structure
```yaml
trigger:
  - platform: state
    entity_id: light.bedroom
    to: "on"
```

### ❌ Don't: Mix trigger and condition logic
```yaml
trigger:
  - platform: state
    entity_id: light.bedroom
    to: "on"
condition:
  - condition: state
    entity_id: light.bedroom
    to: "on"  # Redundant!
```

### ✅ Do: Use trigger for change detection, condition for state verification
```yaml
trigger:
  - platform: state
    entity_id: light.bedroom
condition:
  - condition: numeric_state
    entity_id: sensor.temperature
    above: 20  # Additional check
```

### ❌ Don't: Forget entity_id in service calls
```yaml
action:
  - service: light.turn_on
    data:
      brightness: 255
```

### ✅ Do: Specify target entity
```yaml
action:
  - service: light.turn_on
    target:
      entity_id: light.bedroom
    data:
      brightness: 255
```

## Best Practices

1. **Use descriptive alias names** - Make automation purposes clear
2. **Add descriptions** - Explain why the automation exists
3. **Test with Developer Tools** - Verify templates before deployment
4. **Use choose for complex logic** - More readable than multiple automations
5. **Organize by room or function** - Use `!include` to split large files
6. **Set appropriate mode** - Choose single/restart/queued based on use case
7. **Add for: condition** - Prevent false triggers from brief state changes
8. **Use templates for flexibility** - Enable parameter passing in blueprints

## Troubleshooting

### Template Shows "Error"
- Check template in Developer Tools > Template
- Verify entity IDs exist: `homeassistant.entity_ids`
- Use `| default("value")` filter for optional attributes

### Automation Doesn't Trigger
- Verify entity IDs and state values (case-sensitive)
- Check trigger.yaml syntax with YAML validator
- Review automation logs in Settings > Developer Tools > Logs

### Blueprint Input Not Working
- Verify `!input variable_name` syntax (YAML 1.2 tag)
- Check selector type matches input type
- Ensure blueprint is in correct folder: `config/blueprints/automation/`

### Jinja2 Syntax Error
- Check for undefined variables - use `| default()`
- Verify filter syntax: `value | filter_name(arg)`
- Don't use quotes inside quotes without escaping

## Official Resources

- [Home Assistant Automation Docs](https://www.home-assistant.io/docs/automation/)
- [Home Assistant Scripts](https://www.home-assistant.io/docs/scripts/)
- [Jinja2 Templating Guide](https://www.home-assistant.io/docs/automation/templating/)
- [Blueprint Documentation](https://www.home-assistant.io/docs/blueprint/)
- [Condition Types](https://www.home-assistant.io/docs/automation/condition/)
- [Trigger Types](https://www.home-assistant.io/docs/automation/trigger/)
- [Template Integration](https://www.home-assistant.io/integrations/template/)
