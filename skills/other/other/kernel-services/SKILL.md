---
name: kernel-services
description: Advanced Zephyr RTOS kernel services. Covers inter-thread communication using Zbus (pub/sub), behavioral management with the State Machine Framework (SMF), background processing via work queues, and persistent configuration with the Settings subsystem. Trigger when building modular application architectures, complex state-driven logic, or requiring persistent data storage.
---

# Zephyr Kernel Services

Move beyond basic threading and logging to build modular, event-driven, and robust Zephyr applications.

## Core Workflows

### 1. Event-Driven Communication (Zbus)
Decouple your modules using a lightweight publish-and-subscribe bus.
- **Reference**: **[zbus.md](references/zbus.md)**
- **Key Tools**: `ZBUS_CHAN_DEFINE`, `ZBUS_SUBSCRIBER_DEFINE`, `zbus_chan_pub`.

### 2. Behavioral Logic (SMF)
Manage complex system states and transitions using the State Machine Framework.
- **Reference**: **[smf.md](references/smf.md)**
- **Key Tools**: `smf_set_state`, `SMF_CREATE_STATE`, Hierarchical states.

### 3. Background Processing (Work Queues)
Defer long-running or non-critical tasks to prevent blocking interrupts or high-priority threads.
- **Reference**: **[settings_workqueue.md](references/settings_workqueue.md)**
- **Key Tools**: `k_work_submit`, `k_work_delayable`, Custom work queues.

### 4. Persistence (Settings)
Save and restore configuration data and state across reboots.
- **Reference**: **[settings_workqueue.md](references/settings_workqueue.md#settings-subsystem)**
- **Key Tools**: `settings_load`, `settings_save_one`, NVS backends.

## Quick Start (Zbus)
```c
// Define a channel for sensor data
ZBUS_CHAN_DEFINE(sensor_data_chan, struct sensor_msg, NULL, NULL, ZBUS_OBSERVERS_EMPTY, ZBUS_CHAN_DEFAULTS);

// Publish from a thread
zbus_chan_pub(&sensor_data_chan, &msg, K_NO_WAIT);
```

## Professional Patterns (Asset Tracker Style)
- **Modularity**: Use Zbus as the backbone for inter-module communication.
- **Predictability**: Use SMF to define clear lifecycle states for each module (e.g., Uninitialized -> Ready -> Active -> Error).
- **Responsiveness**: Use custom work queues for sensor data ingestion to keep the main thread responsive for cloud communication.
- **Sensor Integration**: For sensor data ingestion patterns, see the **[hardware-io](../hardware-io/SKILL.md)** skill.

## Resources

- **[References](references/)**:
  - `zbus.md`: Publish/Subscribe patterns and subscriber types.
  - `smf.md`: Finite and Hierarchical state machine implementation.
  - `settings_workqueue.md`: Background work and persistent storage.
