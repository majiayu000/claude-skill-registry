---
name: hardware-io
description: Hardware interfacing and peripheral management for Zephyr RTOS. Covers the sensor subsystem (channels, triggers, fetch/get), pin control (Pinctrl) and multiplexing, GPIO management using Devicetree specs, and SoC-level hardware configurations. Trigger when adding new hardware components, configuring pinmux, or developing sensor-based applications.
---

# Zephyr Hardware I/O

Interface with the physical world using Zephyr's standardized driver models and hardware abstraction layers.

## Core Workflows

### 1. Sensor Subsystem
Interact with various sensors using a uniform API for data fetching and decoding.
- **Reference**: **[sensors.md](references/sensors.md)**
- **Key Tools**: `sensor_sample_fetch`, `sensor_channel_get`, `struct sensor_value`.

### 2. Pinctrl & GPIO
Manage pin multiplexing, electrical configuration, and basic digital input/output.
- **Reference**: **[pinctrl_gpio.md](references/pinctrl_gpio.md)**
- **Key Tools**: `pinctrl`, `gpio_dt_spec`, `GPIO_DT_SPEC_GET`.

### 3. SoC Configuration
Tune chip-level parameters and manage hardware across multiple board variants.
- **Reference**: **[soc_config.md](references/soc_config.md)**
- **Key Tools**: `Kconfig`, `soc_common.dtsi`, SoC-level overlays.

## Quick Start (Sensor Polling)
```c
#include <zephyr/drivers/sensor.h>

const struct device *temp_sensor = DEVICE_DT_GET(DT_ALIAS(ambient_temp0));
struct sensor_value val;

void poll_sensor(void) {
    if (sensor_sample_fetch(temp_sensor) == 0) {
        sensor_channel_get(temp_sensor, SENSOR_CHAN_AMBIENT_TEMP, &val);
    }
}
```

## Professional Patterns (Hardware Engineering)
- **Safe GPIO**: Always use `gpio_dt_spec` to ensure polarity and pin number are automatically handled by the driver.
- **Background Sampling**: Never poll sensors in high-priority threads; use a background work queue. See **[Work Queues](../kernel-services/references/settings_workqueue.md)** in the kernel-services skill.
- **Deferred Pinctrl**: Define pin states in a shared `.dtsi` to simplify multi-revision hardware support.

## Resources

- **[References](references/)**:
  - `sensors.md`: Reading data, channels, and triggers.
  - `pinctrl_gpio.md`: Pin multiplexing and GPIO specs.
  - `soc_config.md`: Multi-variant SoC configuration.
