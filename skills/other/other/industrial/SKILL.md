---
name: industrial
description: Industrial communication protocols for Zephyr RTOS. Covers Modbus RTU (serial), Modbus TCP (Ethernet/Wi-Fi), and CANopen basics. Trigger when building factory automation controllers, industrial sensors, or medical equipment interfaces.
---

# Zephyr Industrial Protocols

Build robust, industry-standard communication systems using Zephyr's modular industrial protocol stacks.

## Core Workflows

### 1. Modbus RTU (Serial)
Implement serial-based industrial communication for meters, PLCs, and sensors.
- **Reference**: **[modbus_rtu.md](references/modbus_rtu.md)**
- **Key Tools**: `CONFIG_MODBUS`, RS-485 DE/RE handling, Register Mapping.

### 2. Modbus TCP
Bridge industrial data over standard Ethernet or Wi-Fi networks.
- **Reference**: **[modbus_tcp.md](references/modbus_tcp.md)**
- **Key Tools**: Port 502, TCP/IP networking, Client/Server patterns.

### 3. CANopen Basics
Integrate with complex automation networks using the CANopenNode stack.
- **Reference**: **[canopen_basics.md](references/canopen_basics.md)**
- **Key Tools**: Object Dictionary (OD), PDO/SDO, Network Management (NMT).

## Quick Start (Modbus RTU Server)
```kconfig
# prj.conf
CONFIG_MODBUS=y
CONFIG_MODBUS_SERIAL=y
```
```c
// Initialize a server on a serial device
const struct device *dev = DEVICE_DT_GET(DT_CHOSEN(zephyr_modbus_serial));
struct modbus_iface_param param = {
    .mode = MODBUS_MODE_RTU,
    .server = { .node_addr = 1, .cb = &my_callbacks },
    .serial = { .baud = 115200, .parity = UART_CFG_PARITY_NONE },
};
modbus_init_server(dev, param);
```

## Professional Patterns (Reliability & Safety)
- **RS-485 Hardware Handling**: Always use the devicetree `uart-rs485` property to handle transceiver direction signals automatically at the driver level.
- **Isolated Communication**: Use galvanically isolated transceivers for both serial and CAN lines in factory environments to prevent damage from ground loops.
- **Watchdog Integration**: In industrial control, always pair your communication loops with the **watchdog_reliability** pattern (see **specialized** skill) to ensure the system enters a fail-safe state on protocol lockup.

## Resources

- **[References](references/)**:
  - `modbus_rtu.md`: Serial Modbus master/slave setup.
  - `modbus_tcp.md`: Ethernet Modbus client/server patterns.
  - `canopen_basics.md`: Object Dictionary and PDO mapping.
