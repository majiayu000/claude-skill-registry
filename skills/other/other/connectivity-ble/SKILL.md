---
name: connectivity-ble
description: Bluetooth Low Energy (BLE) integration for Zephyr RTOS. Covers GATT Services/Characteristics, GAP advertising, connection parameters, power optimization strategies, and the professional Send-When-Idle design pattern. Trigger when adding BLE connectivity, optimizing battery life for wireless devices, or implementing custom GATT profiles.
---

# Zephyr Connectivity: BLE

Implement robust, low-power Bluetooth Low Energy applications using Zephyr's industry-standard BLE stack.

## Core Workflows

### 1. BLE Fundamentals
Set up advertising, define GATT services, and manage connections.
- **Reference**: **[ble_fundamentals.md](references/ble_fundamentals.md)**
- **Key Tools**: `BT_GATT_SERVICE_DEFINE`, `bt_le_adv_start`, `BT_CONN_CB_DEFINE`.

### 2. Send-When-Idle Pattern
Optimize radio usage by bundling data and transmitting only during idle periods.
- **Reference**: **[send_when_idle.md](references/send_when_idle.md)**
- **Key Tools**: `k_work_delayable`, Workqueues, SMF integration.

### 3. Power Optimization
Fine-tune intervals and connection parameters for maximum battery life.
- **Reference**: **[power_optimization.md](references/power_optimization.md)**
- **Key Tools**: `bt_le_conn_param`, Advertising intervals, PHY selection.

## Quick Start (Advertising)
```kconfig
CONFIG_BT=y
CONFIG_BT_PERIPHERAL=y
```
```c
#include <zephyr/bluetooth/bluetooth.h>

void start_simple_adv(void) {
    bt_enable(NULL);
    bt_le_adv_start(BT_LE_ADV_CONN_NAME, NULL, 0, NULL, 0);
}
```

## Professional Patterns (Wireless Design)
- **Aggressive Latency**: Increase peripheral latency to allow the radio to stay off longer during quiet periods.
- **Decoupled Messaging**: Use Zbus to feed data into the BLE module, keeping the radio logic separate from the application logic.
- **Idle Bundling**: Use the "Send-When-Idle" pattern specifically to reduce the number of wake-ups for the radio controller.

## Resources

- **[References](references/)**:
  - `ble_fundamentals.md`: GATT, GAP, and connection basics.
  - `send_when_idle.md`: Implementing the idle-bundle pattern.
  - `power_optimization.md`: Parameter tuning and power-saving Kconfigs.
