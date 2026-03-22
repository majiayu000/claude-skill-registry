---
name: platform-port
description: Guide porting FastLED to new MCU platforms, including int.h types, clockless drivers, SPI implementations, and platform detection. Use when adding support for a new microcontroller family or board.
argument-hint: <target platform name, e.g., "STM32H7", "RP2040", "nRF52840">
context: fork
agent: platform-port-agent
---

Guide the process of porting FastLED to a new microcontroller platform.

$ARGUMENTS

## What This Skill Covers

### Platform Detection Setup
- Create platform detection headers (`is_<platform>.h`)
- Define `FL_IS_<PLATFORM>` macros following naming convention
- Wire into existing detection chain (`src/platforms/`)

### Integer Type Definitions
- Create platform-specific `int.h` with correct primitive type mappings
- Register in the `src/platforms/int.h` dispatcher

### LED Output Drivers
- Clockless (bit-bang) driver implementation
- SPI hardware driver if platform supports it
- RMT/I2S/PARLIO drivers for ESP32 variants
- GPIO register access patterns for the target MCU

### Build System Integration
- PlatformIO board definition
- Meson build configuration
- Compiler flags and linker scripts

## How To Use

```
/platform-port STM32H7
/platform-port RP2040
/platform-port nRF52840
/platform-port I need to add support for the ESP32-P4
```

## What You'll Get

- Step-by-step porting checklist with file locations
- Platform detection header template
- Integer type mapping research and implementation
- Clockless driver skeleton based on platform GPIO speed
- Build system configuration guidance
- Testing strategy for the new platform
