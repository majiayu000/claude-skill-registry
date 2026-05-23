---
name: esp32-wifi-tests
description: Include standard WiFi test cases in ESP32 Functional Specification Documents (FSDs). Use when creating or updating any ESP32 project FSD that involves WiFi connectivity, captive portal, MQTT over WiFi, or OTA updates. Triggers on "ESP32 FSD", "functional specification", "WiFi test cases", or when writing test requirements for ESP32 WiFi features.
---

# ESP32 WiFi Test Specification

This skill provides a standard WiFi test suite for ESP32 projects. Tests are conditionally included based on detected project features.

## Feature Detection Workflow

**Before including tests, detect which features the project uses:**

### Step 1: Scan Project for Features

Search the FSD document and/or source code for these indicators:

| Feature | Detection Patterns | If Found, Include |
|---------|-------------------|-------------------|
| **WiFi STA** | `WiFi.begin`, `esp_wifi_connect`, "WiFi station", "STA mode" | WIFI-001 to WIFI-007 |
| **WiFi AP** | `WiFi.softAP`, `esp_wifi_set_mode(WIFI_MODE_AP)`, "captive portal", "AP mode" | AP-001 to AP-006, TC-300 |
| **MQTT** | `PubSubClient`, `esp_mqtt`, `mosquitto`, "MQTT broker", "publish", "subscribe" | WIFI-006, EC-101, EC-118 |
| **OTA** | `ArduinoOTA`, `esp_ota`, `httpUpdate`, "firmware update", "OTA" | TC-301, EC-114, EC-120 |
| **Ethernet** | `W5500`, `ETH.begin`, `esp_eth`, "dual network", "Ethernet" | TEST-001 to TEST-005, EC-100 |
| **Watchdog** | `esp_task_wdt`, `TWDT`, "watchdog", "health check" | EC-116 to EC-120 |
| **NVS Config** | `Preferences`, `nvs_`, "NVS", "stored credentials" | WIFI-002, EC-112 |

### Step 2: Build Test Matrix

Based on detected features, include only relevant tests:

```
Detected: WiFi STA + MQTT + OTA + Watchdog
Include:  WIFI-001 to WIFI-007, TC-301, EC-101, EC-114, EC-116 to EC-120

Detected: WiFi STA + AP (no MQTT)
Include:  WIFI-001 to WIFI-005, AP-001 to AP-006, TC-300
Exclude:  WIFI-006, EC-101, MQTT-related edge cases
```

### Step 3: Customize and Insert

1. Read `references/wifi-test-spec.md` for test details
2. Copy only the tests matching detected features
3. Update project-specific values (see Customization Points below)

## Test Categories

| Category | Test IDs | Required Feature |
|----------|----------|------------------|
| WiFi STA Requirements | WIFI-001 to WIFI-005 | WiFi STA (always if WiFi used) |
| MQTT-specific | WIFI-006, WIFI-007 | MQTT over WiFi |
| AP Requirements | AP-001 to AP-006 | Captive portal |
| Test Mode | TEST-001 to TEST-005 | Ethernet + WiFi |
| Captive Portal Test | TC-300 | AP mode |
| OTA Test | TC-301 | OTA updates |
| Network Disconnect | EC-100, EC-101 | Ethernet or MQTT |
| Signal/Congestion | EC-110, EC-111 | Any WiFi |
| Credential Change | EC-112 | NVS credentials |
| AP+STA Concurrent | EC-113 | AP fallback mode |
| OTA Resilience | EC-114 | OTA updates |
| DHCP | EC-115 | Any WiFi |
| Watchdog Tests | EC-116 to EC-120 | Watchdog enabled |

## Customization Points

Update these project-specific values when copying tests:

| Placeholder | Example | Where Used |
|-------------|---------|------------|
| `PROJECT-{MAC_LAST_4}` | `SENSOR-A1B2` | AP SSID format |
| `192.168.1.1` | `192.168.4.1` | AP gateway IP |
| `192.168.1.50:1883` | Your broker | MQTT broker address |
| `project/#` | `sensor/data/#` | MQTT topic prefix |
| `5 seconds` | `3 seconds` | CONFIG button hold time |
| `60s` | `30s` | Watchdog timeout |

## Reference

Complete test specifications with step-by-step procedures:

- **Full Test Spec**: See [references/wifi-test-spec.md](references/wifi-test-spec.md)

## Quick Reference: Minimal Sets

### WiFi-Only Project (no MQTT, no OTA)

```markdown
| ID | Requirement | Priority |
|----|-------------|----------|
| WIFI-001 | System SHALL connect to configured WiFi network in STA mode | Must |
| WIFI-002 | WiFi credentials SHALL be stored encrypted in NVS | Must |
| WIFI-003 | System SHALL automatically reconnect on WiFi disconnect | Must |
| WIFI-004 | System SHALL log WiFi connection status changes | Should |
| WIFI-005 | System SHALL support WPA2/WPA3 authentication | Must |
```

### WiFi + MQTT Project

Add to above:
```markdown
| WIFI-006 | MQTT client SHALL only use WiFi interface | Must |
| WIFI-007 | System SHALL sync time via NTP over WiFi | Should |
```

Plus edge cases: EC-101, EC-110, EC-111, EC-115

### Full Feature Project (WiFi + MQTT + OTA + Watchdog)

Include all tests from `references/wifi-test-spec.md`
