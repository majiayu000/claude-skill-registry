---
name: tasmota
description: >
  Tasmota firmware management for ESP8266/ESP32 devices. Flash firmware, configure WiFi, MQTT,
  device templates, rules, and automation. Use when working with Tasmota, ESP devices, smart plugs,
  switches, sensors, Sonoff devices, or custom IoT hardware flashing and configuration.
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, WebFetch
---

# Tasmota Skill

Complete guide for flashing and configuring Tasmota firmware on ESP devices.

## Quick Reference

### Common Commands
| Command | Description |
|---------|-------------|
| `Status 0` | Full device status |
| `Status 5` | Network status |
| `Status 6` | MQTT status |
| `Power` | Toggle power |
| `Power ON` | Turn on |
| `Power OFF` | Turn off |
| `Restart 1` | Restart device |
| `Reset 1` | Reset to defaults |

### Web Console Access
```
http://<device-ip>/
http://<device-ip>/cm?cmnd=<command>
```

---

## 1. Flashing Tasmota

### Using Tasmota Web Installer (Easiest)
1. Visit https://tasmota.github.io/install/
2. Connect ESP device via USB
3. Select firmware variant
4. Click "Install"

### Using esptool.py
```bash
# Install esptool
pip install esptool

# Erase flash
esptool.py --port COM3 erase_flash

# Flash Tasmota
esptool.py --port COM3 write_flash -fs 1MB -fm dout 0x0 tasmota.bin

# For ESP32
esptool.py --port COM3 write_flash 0x0 tasmota32.bin
```

### OTA Update
```bash
# Via web console
Upgrade 1

# Via command
OtaUrl http://ota.tasmota.com/tasmota/release/tasmota.bin.gz
Upgrade 1
```

---

## 2. Initial Configuration

### WiFi Setup
```bash
# Connect to Tasmota-XXXX AP
# Browse to 192.168.4.1
# Configure WiFi credentials

# Or via commands
Backlog SSID1 YourWiFi; Password1 YourPassword
```

### MQTT Configuration
```bash
# Set MQTT broker
Backlog MqttHost 192.168.1.10; MqttPort 1883; MqttUser user; MqttPassword pass

# Set topic
Topic living_room_light

# Full topic structure
FullTopic %prefix%/%topic%/
# Results in: cmnd/living_room_light/, stat/living_room_light/, tele/living_room_light/
```

### Device Name
```bash
# Set friendly name
FriendlyName1 Living Room Light

# Set device name
DeviceName Living Room Light

# Set hostname
Hostname living-room-light
```

---

## 3. Device Templates

### Apply Template
```bash
# Set template (example: Sonoff Basic)
Template {"NAME":"Sonoff Basic","GPIO":[17,255,255,255,255,0,0,0,21,56,255,255,0],"FLAG":0,"BASE":1}
Module 0
```

### Common Templates
```bash
# Sonoff Basic
Template {"NAME":"Sonoff Basic","GPIO":[17,255,255,255,255,0,0,0,21,56,255,255,0],"FLAG":0,"BASE":1}

# Sonoff S31
Template {"NAME":"Sonoff S31","GPIO":[17,145,0,146,0,0,0,0,21,56,0,0,0],"FLAG":0,"BASE":41}

# Shelly 1
Template {"NAME":"Shelly 1","GPIO":[0,0,0,0,21,82,0,0,0,0,0,0,0],"FLAG":0,"BASE":46}

# Generic ESP8266 Relay
Template {"NAME":"Generic Relay","GPIO":[0,0,0,0,21,0,0,0,0,0,0,0,0],"FLAG":0,"BASE":18}
```

### GPIO Configuration
```bash
# Set GPIO function
GPIO4 21    # Relay 1
GPIO5 9     # Button 1
GPIO12 17   # Button 2
GPIO13 56   # LED
GPIO14 22   # Relay 2
```

---

## 4. Power Control

### Basic Power Commands
```bash
Power          # Toggle
Power ON       # Turn on
Power OFF      # Turn off
Power 1        # Turn on
Power 0        # Turn off
Power 2        # Toggle
Power1 ON      # Relay 1 on
Power2 OFF     # Relay 2 off
```

### Power State on Boot
```bash
PowerOnState 0    # OFF after power up
PowerOnState 1    # ON after power up
PowerOnState 2    # Toggle from last state
PowerOnState 3    # Last saved state
PowerOnState 4    # ON and disable further control
PowerOnState 5    # Inverted PowerOnState 0
```

### Pulse Mode (Auto-off)
```bash
# Turn off after 5 seconds
PulseTime1 50    # 50 = 5 seconds (value * 0.1)

# Disable pulse
PulseTime1 0
```

---

## 5. Sensors

### Temperature/Humidity (DHT, BME280, etc.)
```bash
# Status
Status 10

# Set temperature offset
TempOffset -2.5

# Set humidity offset
HumOffset 3

# Set resolution
TempRes 1    # 1 decimal place
```

### Power Monitoring (S31, POW, etc.)
```bash
# Get readings
Status 8

# Calibration
PowerSet 60.0      # Set known wattage
VoltageSet 120.0   # Set known voltage
CurrentSet 0.5     # Set known current

# Energy reset
EnergyReset1 0     # Reset yesterday
EnergyReset2 0     # Reset today
EnergyReset3 0     # Reset total
```

### DS18B20 Temperature
```bash
# Multiple sensors addressed by index
DS18Alias 1,Kitchen
DS18Alias 2,Garage

# Resolution
DS18B20Resolution 12    # 9-12 bits
```

---

## 6. Rules

### Rule Syntax
```bash
Rule1 ON <trigger> DO <command> ENDON
Rule1 1    # Enable rule
Rule1 0    # Disable rule
```

### Example Rules
```bash
# Turn off after 10 minutes
Rule1 ON Power1#state=1 DO RuleTimer1 600 ENDON ON Rules#Timer=1 DO Power1 OFF ENDON
Rule1 1

# Motion sensor triggers light
Rule1 ON Switch1#state=1 DO Power1 ON ENDON ON Switch1#state=0 DO Power1 OFF ENDON
Rule1 1

# Temperature threshold
Rule1 ON Tele-DS18B20#Temperature>25 DO Power1 ON ENDON ON Tele-DS18B20#Temperature<23 DO Power1 OFF ENDON
Rule1 1

# Button double-press
Rule1 ON Button1#state=3 DO Power2 TOGGLE ENDON
Rule1 1

# Time-based automation
Rule1 ON Time#Minute=480 DO Power1 ON ENDON ON Time#Minute=1320 DO Power1 OFF ENDON
Rule1 1
```

### Variables in Rules
```bash
# Set variable
Var1 100

# Use variable
Rule1 ON Power1#state=1 DO Var1 %value% ENDON

# Math operations
Add1 10      # Var1 = Var1 + 10
Sub1 5       # Var1 = Var1 - 5
Mult1 2      # Var1 = Var1 * 2
Scale1 0,100,0,255    # Scale Var1
```

### Chained Rules
```bash
Rule1 ON System#Boot DO Var1 0 ENDON
Rule2 ON Power1#state=1 DO Add1 1 ENDON ON Var1#state>5 DO Power1 OFF ENDON
Rule1 1
Rule2 1
```

---

## 7. Timers

### Set Timer
```bash
# Timer syntax
Timer<x> {"Enable":1,"Mode":0,"Time":"06:00","Window":0,"Days":"1111111","Repeat":1,"Output":1,"Action":1}

# Timer 1: Turn on at 6:00 AM daily
Timer1 {"Enable":1,"Mode":0,"Time":"06:00","Window":0,"Days":"1111111","Repeat":1,"Output":1,"Action":1}

# Timer 2: Turn off at 10:00 PM daily
Timer2 {"Enable":1,"Mode":0,"Time":"22:00","Window":0,"Days":"1111111","Repeat":1,"Output":1,"Action":0}
```

### Timer Parameters
| Parameter | Values | Description |
|-----------|--------|-------------|
| Enable | 0/1 | Enable timer |
| Mode | 0=time, 1=sunrise, 2=sunset | Trigger mode |
| Time | HH:MM | Time of day |
| Window | 0-15 | Random window (minutes) |
| Days | SMTWTFS | Days of week |
| Repeat | 0/1 | Repeat daily |
| Output | 1-16 | Relay number |
| Action | 0=off, 1=on, 2=toggle, 3=rule | Action |

### Sunrise/Sunset
```bash
# Set location
Latitude 40.7128
Longitude -74.0060

# Sunrise timer
Timer1 {"Enable":1,"Mode":1,"Time":"00:00","Window":0,"Days":"1111111","Repeat":1,"Output":1,"Action":0}

# Sunset + 30 minutes
Timer2 {"Enable":1,"Mode":2,"Time":"00:30","Window":0,"Days":"1111111","Repeat":1,"Output":1,"Action":1}
```

---

## 8. MQTT Integration

### Topic Structure
```
cmnd/<topic>/<command>   # Commands
stat/<topic>/<response>  # Status responses
tele/<topic>/<telemetry> # Periodic telemetry
```

### Subscribe to Status
```bash
mosquitto_sub -t "stat/living_room_light/#"
mosquitto_sub -t "tele/living_room_light/#"
```

### Send Commands
```bash
# Power control
mosquitto_pub -t "cmnd/living_room_light/Power" -m "ON"
mosquitto_pub -t "cmnd/living_room_light/Power" -m "TOGGLE"

# Get status
mosquitto_pub -t "cmnd/living_room_light/Status" -m "0"

# Dimmer
mosquitto_pub -t "cmnd/living_room_light/Dimmer" -m "50"
```

### Home Assistant Auto-Discovery
```bash
# Enable discovery
SetOption19 1

# Discovery prefix (default: homeassistant)
SetOption19 1
```

---

## 9. Advanced Configuration

### Backlog (Multiple Commands)
```bash
Backlog SSID1 MyWiFi; Password1 MyPass; MqttHost 192.168.1.10; Topic mydevice; Restart 1
```

### Save Settings
```bash
SaveData 1    # Save every hour
SaveData 0    # Save on change only
Restart 1     # Restart to apply
```

### Disable Features
```bash
SetOption0 0     # Disable save on power toggle
SetOption1 1     # Disable button restriction
SetOption3 1     # Disable MQTT
SetOption36 0    # Disable boot loop protection
```

### Web Interface
```bash
WebServer 1      # Enable web server
WebServer 0      # Disable web server
WebPassword pass # Set password
```

### Serial/Console
```bash
SerialLog 0      # Disable serial logging
WebLog 2         # Set web log level
MqttLog 0        # Disable MQTT logging
```

---

## 10. Troubleshooting

### Common Issues

**Device not connecting to WiFi:**
```bash
# Reset WiFi settings
Reset 1

# Or via button
# Hold button 40+ seconds
```

**MQTT not connecting:**
```bash
Status 6         # Check MQTT status
MqttHost <ip>    # Verify broker IP
MqttPort 1883    # Verify port
MqttUser user    # Verify credentials
```

**Device keeps restarting:**
```bash
# Check restart reason
Status 1

# Disable boot loop protection
SetOption36 0
```

**GPIO not working:**
```bash
# Check template
Template         # View current template
Module 0         # Apply template
GPIOs            # List GPIO assignments
```

### Debug Commands
```bash
Status 0     # Full status
Status 1     # Device parameters
Status 2     # Firmware info
Status 4     # Memory info
Status 5     # Network info
Status 6     # MQTT info
Status 7     # Time info
```

### Factory Reset
```bash
# Via command
Reset 1

# Via button
# Hold for 40+ seconds (4 short blinks)
```

---

## Best Practices

1. **Backup settings** before updates: Configuration > Backup Configuration
2. **Use templates** from https://templates.blakadder.com/
3. **Set static IP** for critical devices: `IPAddress1 192.168.1.100`
4. **Enable watchdog**: `SetOption65 1`
5. **Use rules** instead of external automation when possible
6. **Label devices** with Topic name for easy identification
7. **Group devices** with consistent naming: `room_device_type`
