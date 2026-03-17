# Sensor Management Skill

Home Assistant sensor configuration and analytics patterns.

## Activation Triggers

- Working with sensor entities
- Creating template sensors
- Setting up presence detection
- Configuring security sensors
- Sensor analytics

## Core Patterns

### Temperature Sensors

```yaml
# Average temperature
template:
  - sensor:
      - name: "House Average Temperature"
        unit_of_measurement: "°F"
        device_class: temperature
        state: >
          {% set temps = [
            states('sensor.living_room_temp'),
            states('sensor.bedroom_temp'),
            states('sensor.kitchen_temp')
          ] | map('float', 0) | reject('equalto', 0) | list %}
          {{ (temps | sum / temps | count) | round(1) if temps else 'unavailable' }}

      - name: "Feels Like"
        unit_of_measurement: "°F"
        state: >
          {% set t = states('sensor.outdoor_temp') | float %}
          {% set h = states('sensor.outdoor_humidity') | float %}
          {{ (0.5 * (t + 61 + ((t-68)*1.2) + (h*0.094))) | round(1) }}
```

### Motion and Presence

```yaml
# Combined presence
template:
  - binary_sensor:
      - name: "Room Occupied"
        device_class: occupancy
        state: >
          {{ is_state('binary_sensor.motion', 'on') or
             is_state('binary_sensor.mmwave', 'on') }}
        delay_off:
          minutes: 5

# Room presence sensor
  - sensor:
      - name: "Occupied Rooms"
        state: >
          {% set rooms = [
            ('Living', is_state('binary_sensor.living_occupied', 'on')),
            ('Bedroom', is_state('binary_sensor.bedroom_occupied', 'on')),
            ('Office', is_state('binary_sensor.office_occupied', 'on'))
          ] %}
          {{ rooms | selectattr('1') | map(attribute='0') | join(', ') or 'None' }}
```

### Door/Window Sensors

```yaml
# Security group
template:
  - binary_sensor:
      - name: "Any Door Open"
        device_class: door
        state: >
          {{ expand('group.all_doors') |
             selectattr('state', 'eq', 'on') | list | count > 0 }}

      - name: "House Secure"
        device_class: safety
        state: >
          {{ is_state('binary_sensor.any_door_open', 'off') and
             is_state('binary_sensor.any_window_open', 'off') and
             is_state('lock.front_door', 'locked') }}

# Door list sensor
  - sensor:
      - name: "Open Doors"
        state: >
          {% set doors = expand('group.all_doors') |
             selectattr('state', 'eq', 'on') |
             map(attribute='attributes.friendly_name') | list %}
          {{ doors | join(', ') if doors else 'All Closed' }}
```

### Air Quality

```yaml
template:
  - sensor:
      - name: "Air Quality Index"
        state: >
          {% set co2 = states('sensor.co2') | float(400) %}
          {% set pm25 = states('sensor.pm25') | float(0) %}
          {% set co2_score = 100 - ((co2 - 400) / 10) %}
          {% set pm25_score = 100 - (pm25 * 4) %}
          {{ ((co2_score + pm25_score) / 2) | round(0) | max(0) | min(100) }}

      - name: "Air Quality Status"
        state: >
          {% set aqi = states('sensor.air_quality_index') | float(50) %}
          {% if aqi >= 80 %}Excellent
          {% elif aqi >= 60 %}Good
          {% elif aqi >= 40 %}Fair
          {% else %}Poor{% endif %}
```

### Water Leak Detection

```yaml
automation:
  - alias: "Water Leak Alert"
    trigger:
      - platform: state
        entity_id:
          - binary_sensor.kitchen_leak
          - binary_sensor.bathroom_leak
        to: "on"
    action:
      - service: notify.mobile_app
        data:
          title: "WATER LEAK!"
          message: "Leak at {{ trigger.to_state.attributes.friendly_name }}"
          data:
            push:
              sound:
                critical: 1
                volume: 1.0
      - service: valve.close
        entity_id: valve.main_water
```

### Sensor Groups

```yaml
group:
  all_doors:
    name: All Doors
    entities:
      - binary_sensor.front_door
      - binary_sensor.back_door
      - binary_sensor.garage_door

  all_windows:
    name: All Windows
    entities:
      - binary_sensor.living_window
      - binary_sensor.bedroom_window

  motion_sensors:
    name: Motion Sensors
    entities:
      - binary_sensor.living_motion
      - binary_sensor.kitchen_motion
      - binary_sensor.hallway_motion
```

### Calibration

```yaml
# Calibrated sensor
template:
  - sensor:
      - name: "Temperature Calibrated"
        unit_of_measurement: "°F"
        state: >
          {% set raw = states('sensor.temp_raw') | float %}
          {% set offset = -2.5 %}
          {{ (raw + offset) | round(1) }}
```

## Dashboard Cards

```yaml
# Sensor overview
type: custom:mini-graph-card
name: Room Temperatures
entities:
  - sensor.living_room_temp
  - sensor.bedroom_temp
hours_to_show: 24

# Security glance
type: glance
title: Security
entities:
  - binary_sensor.front_door
  - binary_sensor.back_door
  - lock.front_door
  - binary_sensor.house_secure
```

## Sensor Types Reference

| Type | Device Class | Unit |
|------|-------------|------|
| Temperature | temperature | °F/°C |
| Humidity | humidity | % |
| Motion | motion | on/off |
| Door | door | on/off |
| Window | window | on/off |
| CO2 | carbon_dioxide | ppm |
| PM2.5 | pm25 | µg/m³ |
| Power | power | W |
| Energy | energy | kWh |
