---
name: Home Assistant Automation
description: Automate smart home devices and create intelligent home automation workflows with Home Assistant
version: 1.0.0
author: Claude Office Skills
category: smart-home
tags:
  - home-assistant
  - iot
  - smart-home
  - automation
  - devices
department: operations
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: homeassistant-mcp
  tools:
    - ha_service_call
    - ha_state_get
    - ha_automation
    - ha_scene
capabilities:
  - Device control
  - Automation creation
  - Scene management
  - State monitoring
input:
  - Device commands
  - Automation triggers
  - Scene configurations
  - Sensor data
output:
  - Device states
  - Automation status
  - Scene activations
  - Event logs
languages:
  - en
related_skills:
  - calendar-automation
  - slack-workflows
---

# Home Assistant Automation

Automate smart home devices and create intelligent automation workflows.

## Core Capabilities

### Device Control
```yaml
device_commands:
  lights:
    - turn_on:
        entity_id: light.living_room
        brightness_pct: 80
        color_temp: 350
    - turn_off:
        entity_id: light.all_lights
        
  climate:
    - set_temperature:
        entity_id: climate.main_thermostat
        temperature: 72
        hvac_mode: heat
        
  media:
    - media_play_pause:
        entity_id: media_player.living_room_tv
    - volume_set:
        entity_id: media_player.sonos
        volume_level: 0.5
```

### Automation Templates
```yaml
automations:
  morning_routine:
    trigger:
      - platform: time
        at: "06:30:00"
      - platform: state
        entity_id: binary_sensor.alarm
        to: "off"
    condition:
      - condition: state
        entity_id: person.owner
        state: "home"
    action:
      - service: light.turn_on
        target:
          entity_id: light.bedroom
        data:
          brightness_pct: 30
          transition: 300
      - service: climate.set_temperature
        data:
          temperature: 72
      - delay: "00:05:00"
      - service: media_player.play_media
        data:
          media_content_type: music
          media_content_id: "news_briefing"

  away_mode:
    trigger:
      platform: state
      entity_id: group.family
      to: "not_home"
      for: "00:10:00"
    action:
      - service: climate.set_preset_mode
        data:
          preset_mode: away
      - service: light.turn_off
        target:
          entity_id: all
      - service: lock.lock
        target:
          entity_id: lock.front_door
```

### Scenes
```yaml
scenes:
  movie_night:
    entities:
      light.living_room:
        state: on
        brightness: 20
        color_temp: 500
      light.tv_backlight:
        state: on
        rgb_color: [0, 0, 255]
      media_player.soundbar:
        state: on
        source: "TV"
      cover.blinds:
        state: closed
        
  good_night:
    entities:
      light.all_lights:
        state: off
      lock.all_locks:
        state: locked
      alarm_control_panel.home:
        state: armed_night
      climate.thermostat:
        temperature: 68
```

### Voice Commands
```yaml
voice_intents:
  - intent: "Turn on the lights"
    action: light.turn_on
    entity: light.all_lights
    
  - intent: "Set temperature to {temp}"
    action: climate.set_temperature
    entity: climate.thermostat
    data:
      temperature: "{{ temp }}"
      
  - intent: "I'm leaving"
    action: script.away_mode
```

## Integration Examples

### Energy Monitoring
```yaml
energy_dashboard:
  sensors:
    - sensor.electricity_usage
    - sensor.solar_production
    - sensor.battery_level
  automations:
    - name: "Off-peak charging"
      trigger:
        platform: time
        at: "00:00:00"
      action:
        service: switch.turn_on
        entity_id: switch.ev_charger
```

### Security System
```yaml
security:
  motion_detection:
    trigger:
      platform: state
      entity_id: binary_sensor.motion_front
      to: "on"
    condition:
      - condition: state
        entity_id: alarm_control_panel.home
        state: armed_away
    action:
      - service: camera.snapshot
        entity_id: camera.front_door
      - service: notify.mobile_app
        data:
          message: "Motion detected at front door"
          data:
            image: "/local/snapshots/front_door.jpg"
```

## Best Practices

1. **Entity Naming**: Use consistent naming conventions
2. **Groups**: Organize devices logically
3. **Conditions**: Always add appropriate conditions
4. **Notifications**: Don't over-notify
5. **Testing**: Test automations thoroughly
6. **Backup**: Regular configuration backups
