---
name: connectivity-ip
description: IP networking fundamentals for Zephyr RTOS. Covers IoT protocol selection (LwM2M, CoAP, MQTT), IP stack configuration and trimming (IPv4/IPv6, UDP/TCP), and professional SDK integration as Zephyr modules using West manifests. Trigger when building cloud-connected applications, optimizing network memory usage, or integrating external cloud SDKs.
---

# Zephyr Connectivity: IP Networking

Build memory-efficient, cloud-connected applications using Zephyr's modular IP stack and industry-standard IoT protocols.

## Core Workflows

### 1. Protocol Selection
Choose the right protocol (LwM2M, CoAP, MQTT) based on your device's power and management needs.
- **Reference**: **[protocol_selection.md](references/protocol_selection.md)**
- **Key Tools**: `CONFIG_COAP`, `CONFIG_LWM2M`, `CONFIG_MQTT_LIB`.

### 2. IP Stack Configuration
Tune the networking stack to save Flash and RAM while ensuring reliable communication.
- **Reference**: **[ip_stack_config.md](references/ip_stack_config.md)**
- **Key Tools**: `CONFIG_NET_IPV4`, `CONFIG_NET_BUF_RX_COUNT`, DNS resolver.

### 3. SDK & Module Integration
Integrate external cloud SDKs and libraries as first-class Zephyr modules.
- **Reference**: **[sdk_module_integration.md](references/sdk_module_integration.md)**
- **Key Tools**: `west.yml`, `zephyr/module.yml`, `name-allowlist`.

## Quick Start (Kconfig for CoAP)
```kconfig
# Minimal stack for CoAP over UDP
CONFIG_NETWORKING=y
CONFIG_NET_UDP=y
CONFIG_NET_IPV4=y
CONFIG_COAP=y
CONFIG_DNS_RESOLVER=y
```

## Professional Patterns (Cloud Connectivity)
- **Extreme Trimming**: Disable TCP and IPv6 if not strictly required to reclaim 10KB+ of RAM.
- **Manifest Control**: Use an `allow-list` in your `west.yml` to prevent cloning hundreds of megabytes of unused vendor modules.
- **Async DNS**: Use the asynchronous DNS resolver to prevent blocking the main application thread during host lookup.

## Resources

- **[References](references/)**:
  - `protocol_selection.md`: LwM2M vs CoAP vs MQTT.
  - `ip_stack_config.md`: Optimizing buffers and disabling unused protocols.
  - `sdk_module_integration.md`: West manifest management and SDK modules.
