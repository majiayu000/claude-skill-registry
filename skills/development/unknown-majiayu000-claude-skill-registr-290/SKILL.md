---
name: esphome-config-helper
description: This skill should be used when the user asks to "create an esphome config", "set up an esp32 device", "configure esphome yaml", "add a sensor to esphome", "fix esphome compile error", or mentions "gpio pin assignment", "wifi setup", "ota update", or error messages like "Unknown platform", "GPIO already in use", "Could not compile", or "WiFi connection failed". Provides rapid ESPHome configuration generation, troubleshooting, and validation.
version: 0.1.0
allowed-tools: Read, Write, Edit, Grep, Glob, WebFetch
---

# ESPHome Configuration Helper

Rapid ESPHome configuration generation and troubleshooting skill with ready-to-use templates, GPIO reference guides, and validation utilities.

## Purpose

This skill accelerates ESPHome device configuration by providing:
- Quick-start templates for common device types
- GPIO pinout references to prevent conflicts
- Common sensor configurations with wiring diagrams
- Error message lookup and solutions
- Configuration validation workflow

Use this skill for general ESPHome configuration tasks. For ESP32-S3-BOX-3 specific implementations, use the esphome-box3-builder skill instead.

## When to Use This Skill

Use this skill when:
- Starting a new ESPHome device configuration
- Adding sensors, switches, or displays to existing configs
- Troubleshooting compilation or runtime errors
- Determining safe GPIO pins for components
- Validating configuration before flashing

Delegate to specialized ESPHome agents for:
- Deep technical questions (esphome-core, esphome-components, etc.)
- Complex automation logic (esphome-automations agent)
- Network troubleshooting (esphome-networking agent)
- ESP32-S3-BOX-3 projects (esphome-box3 agent)

## Configuration Templates

### Available Templates

Located in `templates/` directory:

1. **`basic-device.yaml`** - Minimal ESP32 starter
   - ESP32 platform with WiFi and API
   - OTA updates enabled
   - Logger and web server
   - Use as foundation for custom projects

2. **`sensor-node.yaml`** - Temperature/humidity sensor node
   - DHT22 sensor on GPIO4
   - WiFi with fallback AP
   - Home Assistant integration
   - Use for environmental monitoring

3. **`relay-switch.yaml`** - 4-channel relay controller
   - GPIO control for 4 relays (GPIO23, GPIO22, GPIO21, GPIO19)
   - Physical button inputs with interlocks
   - Switch entities for Home Assistant
   - Use for home automation switching

4. **`display-node.yaml`** - Display with sensors
   - SSD1306 OLED display (128x64, I²C)
   - DHT22 temperature/humidity
   - Display lambda showing sensor readings
   - Use for visual sensor displays

### Using Templates

To use a template:
1. Read the appropriate template file
2. Customize device name, WiFi credentials, GPIO pins
3. Add or remove components as needed
4. Validate configuration (see Validation Workflow below)

**Template Workflow:**
```yaml
# 1. Read template
cat .claude/skills/esphome-config-helper/templates/sensor-node.yaml

# 2. Copy to project
cp .claude/skills/esphome-config-helper/templates/sensor-node.yaml my-device.yaml

# 3. Edit with device-specific values
# - Update device name
# - Set WiFi credentials (use secrets.yaml)
# - Adjust GPIO pins if needed
# - Customize sensor names

# 4. Validate (see Validation Workflow)
```

## GPIO Pin Reference

### Quick GPIO Lookup

For detailed GPIO pinouts and safe pin selection, consult:
- **`references/gpio-pinouts.md`** - Complete ESP32 and ESP8266 GPIO reference
  - Safe pins for each platform
  - Strapping pins to avoid
  - I²C/SPI/UART default pins
  - Input-only vs output-capable pins
  - Boot failure pins (GPIO0, GPIO2, GPIO15)

**Quick Safe Pins:**
- **ESP32**: GPIO4, GPIO5, GPIO12, GPIO13, GPIO14, GPIO16, GPIO17, GPIO18, GPIO19, GPIO21, GPIO22, GPIO23, GPIO25-27, GPIO32, GPIO33
- **ESP8266**: GPIO4 (D2), GPIO5 (D1), GPIO12 (D6), GPIO13 (D7), GPIO14 (D5)

**Avoid (strapping/boot pins):**
- **ESP32**: GPIO0, GPIO2, GPIO5, GPIO12, GPIO15 (use with caution)
- **ESP8266**: GPIO0, GPIO2, GPIO15

## Common Sensor Configurations

### Sensor Selection Guide

For detailed sensor configurations with wiring diagrams, consult:
- **`references/common-sensors.md`** - Top 20 sensor configurations
  - Temperature/humidity sensors (DHT22, BME280, SHT3x)
  - Motion sensors (PIR, mmWave)
  - Light sensors (BH1750, TSL2561)
  - Distance sensors (HC-SR04, VL53L0X)
  - Gas sensors (MQ-series, SGP30)
  - Complete wiring diagrams and platform selection

**Quick Sensor Recommendations:**
- **Temperature/Humidity**: BME280 (I²C, more reliable than DHT22)
- **Motion**: HC-SR501 PIR (GPIO binary sensor)
- **Light**: BH1750 (I²C, accurate lux measurements)
- **Distance**: HC-SR04 (ultrasonic, 2-400cm range)
- **Air Quality**: BME680 (I²C, temp/humidity/pressure/gas)

### Basic Sensor Patterns

**I²C Sensor** (BME280 example):
```yaml
i2c:
  sda: GPIO21
  scl: GPIO22
  scan: true

sensor:
  - platform: bme280
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    pressure:
      name: "Pressure"
    address: 0x76
    update_interval: 60s
```

**GPIO Sensor** (DHT22 example):
```yaml
sensor:
  - platform: dht
    pin: GPIO4
    model: DHT22
    temperature:
      name: "Temperature"
    humidity:
      name: "Humidity"
    update_interval: 60s
```

**Binary Sensor** (PIR motion):
```yaml
binary_sensor:
  - platform: gpio
    pin: GPIO14
    name: "Motion Sensor"
    device_class: motion
```

## Troubleshooting Guide

### Error Lookup

For complete error message lookup table and solutions, consult:
- **`references/troubleshooting.md`** - Comprehensive error message reference
  - Compilation errors (unknown platform, GPIO conflicts, dependency issues)
  - Runtime errors (WiFi failures, sensor timeouts, OTA problems)
  - Configuration errors (YAML syntax, invalid pins, missing components)
  - Hardware issues (sensor not detected, relay not switching)

**Common Error Quick Reference:**

| Error Message | Quick Fix |
|---------------|-----------|
| "Unknown platform" | Check component name spelling, ensure platform supported |
| "GPIO already in use" | Check GPIO pin assignments, avoid duplicates |
| "Could not compile" | Check YAML syntax, verify indentation (2 spaces) |
| "WiFi connection failed" | Verify SSID/password, check signal strength, use static IP |
| "Sensor not found" | Check I²C address (use scan: true), verify wiring |
| "OTA upload failed" | Check device reachable, verify OTA password, restart device |

### Troubleshooting Workflow

When encountering errors:

1. **Check YAML syntax**: Verify indentation (2 spaces, no tabs)
2. **Validate GPIO pins**: Ensure no conflicts, use safe pins
3. **Check component platform**: Verify platform name and configuration
4. **Review logs**: Use `esphome logs device.yaml` to see runtime errors
5. **Consult references**: Check `references/troubleshooting.md` for specific error
6. **Validate config**: Run validation workflow (see below)

## Validation Workflow

### Using the Validation Script

The validation utility provides quick configuration checks:

**Script**: `scripts/validate-config.sh`

**Usage:**
```bash
# Validate configuration
./.claude/skills/esphome-config-helper/scripts/validate-config.sh my-device.yaml

# The script runs:
# 1. esphome config my-device.yaml  (syntax check)
# 2. esphome compile my-device.yaml (compilation test)
```

**Validation Steps:**

1. **Syntax validation**: `esphome config my-device.yaml`
   - Checks YAML syntax
   - Validates component configuration
   - Reports missing requirements
   - Shows final configuration

2. **Compilation test**: `esphome compile my-device.yaml`
   - Downloads required libraries
   - Compiles firmware
   - Reports errors and warnings
   - Confirms configuration works

3. **Fix errors**: If validation fails:
   - Review error messages
   - Check GPIO conflicts
   - Verify component platforms
   - Consult `references/troubleshooting.md`
   - Re-validate after fixes

### Pre-Flash Checklist

Before flashing device:
- [ ] Configuration validates without errors
- [ ] WiFi credentials correct (use secrets.yaml)
- [ ] Device name unique on network
- [ ] GPIO pins verified safe
- [ ] OTA password set (for future updates)
- [ ] API encryption key configured (2026.1.0+)

## Configuration Best Practices

### YAML Structure

Organize configuration in logical sections:
```yaml
# 1. Core platform
esphome:
  name: device-name
  friendly_name: Device Name

esp32:
  board: esp32dev
  framework:
    type: arduino

# 2. Network
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password

api:
  encryption:
    key: !secret api_encryption_key

ota:
  - platform: esphome
    password: !secret ota_password

# 3. Logging
logger:
web_server:

# 4. Components (sensors, switches, etc.)
sensor:
  # ...

binary_sensor:
  # ...
```

### Secrets Management

Use `secrets.yaml` for sensitive data:

**secrets.yaml:**
```yaml
wifi_ssid: "MyNetwork"
wifi_password: "MyPassword123"
api_encryption_key: "base64-generated-key"
ota_password: "SecureOTAPassword"
```

**Reference in config:**
```yaml
wifi:
  ssid: !secret wifi_ssid
  password: !secret wifi_password
```

### Naming Conventions

Follow consistent naming:
- **Device names**: lowercase-with-hyphens (e.g., `bedroom-sensor`)
- **Entity names**: Title Case with Spaces (e.g., `"Bedroom Temperature"`)
- **IDs**: lowercase_with_underscores (e.g., `temp_sensor`)

**Example:**
```yaml
sensor:
  - platform: dht
    pin: GPIO4
    temperature:
      name: "Living Room Temperature"
      id: living_room_temp
    humidity:
      name: "Living Room Humidity"
      id: living_room_humidity
```

## Integration with Other Skills and Agents

### When to Use Other Resources

- **ESP32-S3-BOX-3 projects**: Use esphome-box3-builder skill
  - Audio pipeline (I²S, ES7210, ES8311)
  - Display lambda rendering (ILI9xxx)
  - Touch interaction (GT911)
  - Voice assistant integration

- **Deep technical questions**: Delegate to ESPHome agents
  - Core concepts → esphome-core agent
  - Component selection → esphome-components agent
  - Automation logic → esphome-automations agent
  - Network issues → esphome-networking agent
  - HA integration → esphome-homeassistant agent

- **Complex projects**: Combine resources
  - Start with template (this skill)
  - Customize with agent guidance
  - Validate with scripts (this skill)
  - Deploy and troubleshoot (this skill + agents)

## Additional Resources

### Reference Files

For detailed information, consult:
- **`references/gpio-pinouts.md`** - Complete ESP32/ESP8266 GPIO reference with safe pins, strapping pins, and pin capabilities
- **`references/common-sensors.md`** - Top 20 sensor configurations with wiring diagrams, platform selection, and usage examples
- **`references/troubleshooting.md`** - Comprehensive error message lookup table with solutions for compilation, runtime, and hardware issues

### Template Files

Working configuration examples in `templates/`:
- **`basic-device.yaml`** - Minimal ESP32 foundation
- **`sensor-node.yaml`** - DHT22 temperature/humidity node
- **`relay-switch.yaml`** - 4-channel relay controller
- **`display-node.yaml`** - OLED display with sensors

### Utility Scripts

Validation and testing tools in `scripts/`:
- **`validate-config.sh`** - ESPHome configuration validation wrapper

## Quick Start Workflow

For new ESPHome device:

1. **Select template** based on device type (sensor, switch, display, or basic)
2. **Copy template** to project directory
3. **Customize configuration**:
   - Update device name
   - Set WiFi credentials in secrets.yaml
   - Adjust GPIO pins using `references/gpio-pinouts.md`
   - Add/remove components as needed
4. **Validate configuration** using `scripts/validate-config.sh`
5. **Fix any errors** using `references/troubleshooting.md`
6. **Flash device** with validated configuration
7. **Monitor logs** and troubleshoot if needed

For adding to existing config:
1. **Consult references** for component configuration
2. **Check GPIO availability** in `references/gpio-pinouts.md`
3. **Add component** to configuration
4. **Validate** before flashing
5. **Update and monitor**

This skill provides rapid configuration generation for common ESPHome use cases. For specialized hardware (ESP32-S3-BOX-3) or deep technical questions, use the appropriate specialist skills and agents.
