---
name: platformio
description: |
  Builds and deploys ESP32 firmware with PlatformIO for the VanDaemon LED dimmer hardware.
  Use when: Building, uploading, or debugging ESP32 firmware in hw/LEDDimmer/
allowed-tools: Read, Edit, Write, Glob, Grep, Bash
---

# PlatformIO Skill

PlatformIO manages the ESP32 firmware for VanDaemon's 8-channel PWM LED dimmer. The firmware handles MQTT communication, WiFi provisioning via captive portal, and NVS state persistence. All firmware lives in `hw/LEDDimmer/firmware/`.

## Quick Start

### Build and Upload

```bash
cd hw/LEDDimmer/firmware

# Build for 8-channel variant (default)
pio run -e 8ch

# Upload via USB
pio run -e 8ch -t upload

# Build 4-channel variant
pio run -e 4ch -t upload
```

### Monitor Serial Output

```bash
# Start serial monitor at 115200 baud
pio device monitor -e 8ch

# Monitor with timestamp
pio device monitor -e 8ch --filter time
```

## Key Concepts

| Concept | Usage | Example |
|---------|-------|---------|
| Environment | Build target variant | `-e 8ch`, `-e 4ch`, `-e 8ch-ota` |
| Upload | Flash firmware to device | `pio run -e 8ch -t upload` |
| Monitor | Serial debugging | `pio device monitor` |
| Clean | Remove build artifacts | `pio run -t clean` |
| OTA | Over-the-air updates | `-e 8ch-ota` environment |

## Common Patterns

### Full Development Cycle

**When:** Making firmware changes

```bash
# Clean, build, upload, then monitor
pio run -e 8ch -t clean && pio run -e 8ch -t upload && pio device monitor -e 8ch
```

### OTA Update

**When:** Device deployed and accessible via WiFi

```bash
# Build and upload via OTA (requires device IP in platformio.ini)
pio run -e 8ch-ota -t upload
```

### Upload Filesystem

**When:** Updating SPIFFS/LittleFS data

```bash
pio run -e 8ch -t uploadfs
```

## Pin Configuration

```cpp
// PWM Outputs (8 channels)
GPIO 25, 26, 27, 14, 4, 5, 18, 19

// Status LED (WS2812)
GPIO 16

// Buttons
GPIO 32 (Button 1), GPIO 33 (Button 2)
```

## MQTT Integration

The firmware publishes to topics under `vandaemon/leddimmer/{deviceId}/`:
- `status` - online/offline
- `config` - device configuration JSON
- `channel/{N}/state` - current brightness (0-255)

Subscribes to `channel/{N}/set` for brightness commands.

See the **mqttnet** skill for backend MQTT handling.

## See Also

- [patterns](references/patterns.md) - Build configurations and debugging
- [workflows](references/workflows.md) - Development and deployment workflows

## Related Skills

- **kicad** - PCB design for the LED dimmer hardware
- **mqttnet** - Backend MQTT communication with the dimmer
- **docker** - Running MQTT broker for testing