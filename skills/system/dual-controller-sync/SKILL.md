---
name: dual-controller-sync
description: Debug and synchronize communication between the robocar main controller (Heltec WiFi LoRa 32) and camera module (ESP32-CAM)
---

# Dual-Controller Synchronization Guide

## When to Use This Skill

Apply this skill when the user:
- Has issues with I2C communication between main and camera controllers
- Needs to debug the dual-ESP32 robocar architecture
- Wants to monitor both controllers simultaneously
- Experiences timing or synchronization issues

## Architecture Overview

```
┌─────────────────────┐     I2C      ┌─────────────────────┐
│   Main Controller   │◄────────────►│   Camera Module     │
│  Heltec WiFi LoRa   │              │     ESP32-CAM       │
│                     │              │                     │
│  - AI decisions     │              │  - Image capture    │
│  - Motor control    │              │  - Vision analysis  │
│  - LoRa comms       │              │  - I2C slave        │
└─────────────────────┘              └─────────────────────┘
```

## Build Both Controllers

```bash
# Build main controller
make robocar-build-main

# Build camera module
make robocar-build-cam

# Or build both
make robocar-build-all
```

## Monitor Both Controllers

### Two Terminal Setup

Open two terminals and monitor both:

**Terminal 1 - Main Controller:**
```bash
make robocar-monitor-main PORT=/dev/cu.usbserial-0001
```

**Terminal 2 - Camera Module:**
```bash
make robocar-monitor-cam PORT=/dev/cu.usbserial-0002
```

### Identifying Ports

If unsure which device is which:
```bash
ls -la /dev/cu.usbserial-* /dev/ttyUSB*
```

Look for:
- Device that appears first after connecting main controller
- Device that appears after connecting camera module

## I2C Communication Debugging

### Common I2C Issues

| Symptom | Possible Cause | Solution |
|---------|----------------|----------|
| No response | Wrong address | Verify 7-bit address format |
| Timeout | Missing pull-ups | Add 4.7K resistors on SDA/SCL |
| Corrupted data | Speed too fast | Reduce I2C clock frequency |
| Intermittent | Loose connection | Check wiring |

### I2C Address Configuration

Ensure both controllers use the same address:

**Main controller (master):**
```c
#define CAMERA_I2C_ADDR 0x55  // 7-bit address
```

**Camera module (slave):**
```c
#define I2C_SLAVE_ADDR 0x55   // Must match master
```

### Verify I2C Wiring

```
Main Controller          Camera Module
    SDA (21) ◄──────────► SDA (GPIO)
    SCL (22) ◄──────────► SCL (GPIO)
    GND      ◄──────────► GND
```

Pull-up resistors (4.7K) on SDA and SCL to 3.3V.

## Protocol Debugging

### Expected Communication Pattern

1. Main sends command byte
2. Camera processes command
3. Camera sends response
4. Main reads response

### Debug Logging

Enable verbose I2C logging in both projects:

```c
esp_log_level_set("i2c", ESP_LOG_DEBUG);
```

Look for matching transactions:
- Main: "Sent command 0x01 to 0x55"
- Camera: "Received command 0x01"

### Timing Issues

If commands arrive too fast:

**Add delay between commands:**
```c
i2c_master_cmd_begin(I2C_NUM, cmd, pdMS_TO_TICKS(100));
vTaskDelay(pdMS_TO_TICKS(10));  // Wait for slave to process
```

## Flash Workflow

### Flash Both Controllers

```bash
# Flash main controller first
make robocar-flash-main PORT=/dev/cu.usbserial-0001

# Then flash camera (requires GPIO0 to GND)
# Connect GPIO0 to GND on ESP32-CAM
make robocar-flash-cam PORT=/dev/cu.usbserial-0002
# Disconnect GPIO0 from GND and reset
```

### Development Cycle

For rapid iteration:

1. Make code changes
2. Build: `make robocar-build-all`
3. Flash main: `make robocar-flash-main`
4. Flash camera (GPIO0→GND): `make robocar-flash-cam`
5. Monitor both in separate terminals

## Common Synchronization Issues

### Issue: Camera Not Responding

**Symptoms:**
- Main reports I2C timeout
- Camera not in monitor output

**Debug Steps:**
1. Verify camera is powered and running
2. Check I2C address matches
3. Verify GPIO pins for I2C slave
4. Check clock speed compatibility

### Issue: Corrupted Data

**Symptoms:**
- Data received but values wrong
- Checksum failures

**Debug Steps:**
1. Reduce I2C speed (try 100kHz)
2. Add pull-up resistors
3. Check for noise on long wires
4. Verify endianness of multi-byte data

### Issue: Timing Mismatch

**Symptoms:**
- Works sometimes, fails other times
- Camera not ready when main sends command

**Debug Steps:**
1. Add handshake mechanism
2. Increase timeout values
3. Use interrupt-based I2C on camera
4. Add ready signal GPIO

## Tools and Commands

```bash
# Show system info
make robocar-info

# Check environment
make check-environment

# Clean and rebuild
make robocar-clean
make robocar-build-all

# Full dev cycle for main
make robocar-develop-main PORT=/dev/xxx

# Full dev cycle for camera
make robocar-develop-cam PORT=/dev/xxx
```
