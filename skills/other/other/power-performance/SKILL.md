---
name: power-performance
description: Power management and performance optimization for Zephyr RTOS. Covers system power states (Idle, Suspend, Off), device-level power management, residency hooks, and code/data relocation for speed efficiency. Trigger when optimizing battery life, reducing latency, or managing memory constraints.
---

# Zephyr Power & Performance

Maximize the efficiency of your embedded system by balancing power consumption and computational performance.

## Core Workflows

### 1. Power Management (PM)
Implement system-level and peripheral-specific power saving strategies.
- **Reference**: **[power_management.md](references/power_management.md)**
- **Key Tools**: `pm_device_action_run`, `pm_state_set`, Residency hooks.

### 2. Performance Tuning
Optimize critical code paths and monitor system resources.
- **Reference**: **[performance_tuning.md](references/performance_tuning.md)**
- **Key Tools**: `CONFIG_THREAD_ANALYZER`, Linker Map, Code relocation.

### 3. Memory Optimization
Relocate code and data to utilize the fastest memory available.
- **Reference**: **[performance_tuning.md](references/performance_tuning.md#code--data-relocation)**
- **Key Tools**: `__ramfunc`, Relocation scripts.

## Quick Start (Device Suspend)
```c
#include <zephyr/pm/device.h>

const struct device *spi0 = DEVICE_DT_GET(DT_NODELABEL(spi0));

void sleep_spi(void) {
    pm_device_action_run(spi0, PM_DEVICE_ACTION_SUSPEND);
}
```

## Professional Patterns (Optimization)
- **Aggressive Suspend**: Transition peripherals to low-power states as soon as their transaction is complete.
- **ITCM/DTCM**: Use Tightly Coupled Memory for time-critical control loops to avoid Flash latency.
- **Runtime Monitoring**: Always enable the thread analyzer during development to find the "RAM floor" for your application.
- **Coordinated Sleep**: To coordinate sleep across modules, see **[kernel-services](../kernel-services/SKILL.md)** for Zbus-based event-driven power management.

## Automation Tools
- **[power_budget_estimator.py](scripts/power_budget_estimator.py)**: Estimate average current and battery life from duty-cycle state data.

## Examples & Templates
- **[power_budget_template.csv](assets/power_budget_template.csv)**: Starter power-state budget sheet for battery-life estimation.

## Validation Checklist
- [ ] Target peripherals enter and exit suspend/resume states without functional regressions.
- [ ] Measured idle and active power align with expected optimization deltas.
- [ ] Thread analyzer and map data confirm stack/RAM budgets are within limits.
- [ ] Relocated time-critical functions execute from intended memory region.

## Resources

- **[References](references/)**:
  - `power_management.md`: System states, device PM, and hooks.
  - `performance_tuning.md`: Optimization strategies and relocation.
- **[Scripts](scripts/)**:
  - `power_budget_estimator.py`: Duty-cycle based battery-life estimator.
- **[Assets](assets/)**:
  - `power_budget_template.csv`: Initial state/current budget template.
