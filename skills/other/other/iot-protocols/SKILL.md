---
name: iot-protocols
description: Integration of advanced IoT protocols for Zephyr RTOS. Covers OpenThread mesh networking, Matter-over-Thread device development, Golioth Cloud SDK patterns, and LoRaWAN basics. Trigger when building smart home devices, wide-area sensor networks, or cloud-integrated hardware fleets.
---

# Zephyr IoT Protocols

Implement production-ready IoT communication using industry-standard mesh, wide-area, and cloud protocols.

## Core Workflows

### 1. OpenThread Mesh
Build robust, low-power mesh networks using the integrated OpenThread stack.
- **Reference**: **[openthread_integration.md](references/openthread_integration.md)**
- **Key Tools**: `CONFIG_NET_L2_OPENTHREAD`, `otInstance`, Thread Shell.

### 2. Matter-over-Thread
Create interoperable smart home devices using the Matter standard.
- **Reference**: **[matter_devices.md](references/matter_devices.md)**
- **Key Tools**: Matter Clusters, BLE Commissioning, ZAP tool.

### 3. Golioth Cloud SDK
Connect your fleet to the cloud for real-time state sync, telemetry, and OTA.
- **Reference**: **[golioth_sdk.md](references/golioth_sdk.md)**
- **Key Tools**: LightDB, `golioth_system_client`, remote logging.

### 4. LoRaWAN Basics
Deploy long-range, low-power sensor networks.
- **Reference**: **[lorawan_basics.md](references/lorawan_basics.md)**
- **Key Tools**: `CONFIG_LORA`, LoRa PHY, Adaptive Data Rate (ADR).

## Quick Start (OpenThread Shell)
```kconfig
# Enable OpenThread with Shell
CONFIG_NET_L2_OPENTHREAD=y
CONFIG_OPENTHREAD_SHELL=y
```
```bash
# Join a network via Shell
ot dataset init new
ot dataset commit active
ot thread start
```

## Professional Patterns (Ecosystem Design)
- **Commissioning via BLE**: Use the `connectivity-ble` skill patterns to handle Matter or Thread commissioning for a seamless user experience.
- **Cloud-Mesh Gateways**: Implement Thread Border Routers to bridge local mesh traffic to Golioth or other cloud backends.
- **Battery Optimization**: Use Sleepy End Device (SED) modes for Thread/LoRaWAN nodes to achieve multi-year battery life.

## Resources

- **[References](references/)**:
  - `openthread_integration.md`: Thread networking and Zephyr APIs.
  - `matter_devices.md`: Smart home integration with Matter.
  - `golioth_sdk.md`: Fleet management and real-time state sync.
  - `lorawan_basics.md`: Long-range sensor networking.
