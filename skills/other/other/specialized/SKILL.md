---
name: specialized
description: Specialized hardware interfaces and system reliability for Zephyr RTOS. Covers LVGL GUI development, Audio I2S/Codecs, Watchdog timers, and Fault Injection. Trigger when building human-machine interfaces (HMI), audio devices, or high-reliability mission-critical systems.
---

# Zephyr Specialized Hardware & Reliability

Integrate complex peripherals and build resilient systems that recover gracefully from unexpected failures.

## Core Workflows

### 1. LVGL GUI Development
Build sophisticated graphical user interfaces for LCD and TFT displays.
- **Reference**: **[lvgl_gui.md](references/lvgl_gui.md)**
- **Key Tools**: Widgets, Styles, Double Buffering, `native_sim` simulator.

### 2. Audio I2S & Codecs
Implement high-quality digital audio streaming and codec management.
- **Reference**: **[audio_i2s.md](references/audio_i2s.md)**
- **Key Tools**: `CONFIG_I2S`, DMA streaming, Ping-pong buffering.

### 3. Watchdog & Reliability
Ensure your system never hangs in the field using hardware watchdog timers.
- **Reference**: **[watchdog_reliability.md](references/watchdog_reliability.md)**
- **Key Tools**: `wdt_feed()`, Windowed watchdog, Health checks.

### 4. Fault Injection & Resilience
Test your system's ability to recover from unexpected software and hardware errors.
- **Reference**: **[fault_injection.md](references/fault_injection.md)**
- **Key Tools**: Chaos testing, `k_oops()`, Reset reason diagnostics.

## Quick Start (Watchdog Feed)
```kconfig
# Enable watchdog support
CONFIG_WATCHDOG=y
```
```c
// Feed the dog in your main loop
while (1) {
    // Perform application work
    wdt_feed(wdt_dev, wdt_channel);
    k_sleep(K_MSEC(1000));
}
```

## Professional Patterns (Reliability & UX)
- **Safe Boot Animation**: Use a simple, non-interactive LVGL screen to show system status while critical subsystems (e.g., cloud connectivity) are initializing.
- **Zero-Pop Audio**: Always use volume ramping when starting or stopping I2S streams to protect hardware and improve user experience.
- **Bitmask Health Monitoring**: Use a bitmask to track the health of all background threads; the watchdog monitor only feeds the timer if ALL bits are set periodically.

## Resources

- **[References](references/)**:
  - `lvgl_gui.md`: GUI widgets and performance tuning.
  - `audio_i2s.md`: Audio streaming and DMA patterns.
  - `watchdog_reliability.md`: Watchdog setup and health checks.
  - `fault_injection.md`: System resilience and chaos testing.
