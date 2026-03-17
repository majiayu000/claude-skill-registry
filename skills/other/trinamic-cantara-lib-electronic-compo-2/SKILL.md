---
name: trinamic
description: Trinamic Motion Control MPN encoding patterns, motor driver series decoding, and handler guidance. Use when working with Trinamic stepper drivers and motion controllers (TMC series).
---

# Trinamic Motion Control Manufacturer Skill

## Overview

Trinamic (now part of Analog Devices) specializes in motor control ICs:
- **TMC21xx**: Basic stepper motor drivers
- **TMC22xx**: Advanced stepper drivers with UART/StallGuard
- **TMC23xx/24xx**: Stepper drivers
- **TMC26xx**: High-power stepper drivers
- **TMC4xxx**: Gate drivers and motion controllers
- **TMC5xxx**: Integrated motion controllers
- **TMC6xxx**: 3-phase BLDC/PMSM drivers
- **TMC7xxx**: Specialized drivers

---

## MPN Structure

```
TMC[FAMILY][SERIES]-[PACKAGE][-SUFFIX]
|     |       |        |        |
|     |       |        |        +-- T = Tape and reel
|     |       |        +-- Package code (LA, TA, WA, BOB)
|     |       +-- 2-digit series within family (00-99)
|     +-- Family digit (2, 4, 5, 6, 7)
+-- TMC prefix (all Trinamic parts)

Example: TMC2209-LA
         |  |  | |
         |  |  | +-- LA = QFN package
         |  |  +-- 09 = Series number
         |  +-- 2 = Stepper driver family
         +-- TMC = Trinamic prefix

Example: TMC5160-TA-T
         |  |  | | |
         |  |  | | +-- T = Tape and reel packaging
         |  |  | +-- TA = TQFP package
         |  |  +-- 60 = Series (motion controller)
         |  +-- 5 = Motion controller family
         +-- TMC = Trinamic prefix
```

---

## Family Codes

| Family | Description | Applications |
|--------|-------------|--------------|
| TMC21xx | Basic stepper drivers | TMC2100, TMC2130, TMC2160 |
| TMC22xx | Advanced stepper drivers | TMC2208, TMC2209, TMC2225, TMC2226 |
| TMC23xx | Stepper drivers | TMC2300 |
| TMC24xx | Stepper drivers | TMC2400 |
| TMC26xx | High-power stepper | TMC2660, TMC2690 |
| TMC4xxx | Gate/motion controllers | TMC4361, TMC4671 |
| TMC5xxx | Integrated motion | TMC5041, TMC5072, TMC5130, TMC5160 |
| TMC6xxx | 3-phase BLDC/PMSM | TMC6100, TMC6140, TMC6200 |
| TMC7xxx | Specialized | Various |

---

## Package Codes

| Code | Package | Description |
|------|---------|-------------|
| LA | QFN | Leadless Array - most common |
| TA | TQFP | Thin Quad Flat Package |
| WA | WQFN | Very thin QFN variant |
| BOB | Breakout Board | Evaluation/development board |

### Package Selection Guide

| Application | Recommended | Notes |
|-------------|-------------|-------|
| Production | LA (QFN) | Smallest footprint, best thermal |
| Prototyping | TA (TQFP) | Easier to hand solder |
| Development | BOB | Plug-and-play evaluation |
| Tight spaces | WA (WQFN) | Ultra-thin profile |

---

## Suffix Codes

| Suffix | Meaning |
|--------|---------|
| -T | Tape and reel packaging |
| -TR | Tape and reel (alternate) |
| (none) | Tube/tray packaging |

---

## Popular Product Series

### TMC21xx - Basic Stepper Drivers

| Part | Features | Max Current |
|------|----------|-------------|
| TMC2100 | Basic driver, stealthChop | 1.2A RMS |
| TMC2130 | SPI interface, StallGuard2 | 1.2A RMS |
| TMC2160 | High power, spreadCycle | 2.5A peak |

### TMC22xx - Advanced Stepper Drivers

| Part | Features | Max Current | Interface |
|------|----------|-------------|-----------|
| TMC2208 | UART, stealthChop | 1.4A RMS | UART |
| TMC2209 | UART, StallGuard4 | 2.0A RMS | UART |
| TMC2225 | Enhanced 2208 | 1.4A RMS | UART |
| TMC2226 | Enhanced 2209 | 2.0A RMS | UART |

### TMC5xxx - Motion Controllers

| Part | Features | Notes |
|------|----------|-------|
| TMC5041 | Dual driver + controller | 2 motors |
| TMC5072 | Dual driver + ramp | 2 motors |
| TMC5130 | Driver + controller | Single motor |
| TMC5160 | High power + controller | 3A RMS |

### TMC6xxx - 3-Phase Drivers

| Part | Application | Voltage |
|------|-------------|---------|
| TMC6100 | BLDC gate driver | 6-25V |
| TMC6140 | BLDC power stage | 6-36V |
| TMC6200 | High voltage BLDC | 8-60V |

---

## Replacement Compatibility

Trinamic parts are compatible when:
1. **Same series number** (TMC2209 vs TMC2209)
2. **Same package** (LA vs LA, TA vs TA)
3. **Different packaging suffix** (-T vs no suffix)

### Upgrade Paths

| Original | Upgrade | Notes |
|----------|---------|-------|
| TMC2208 | TMC2209 | Adds StallGuard4 |
| TMC2100 | TMC2130 | Adds SPI + StallGuard2 |
| TMC5130 | TMC5160 | Higher current |
| TMC2225 | TMC2226 | Higher current |

### NOT Compatible

| Part A | Part B | Reason |
|--------|--------|--------|
| TMC2130 | TMC2209 | Different interface (SPI vs UART) |
| TMC2100 | TMC2208 | Different interface (STEP/DIR vs UART) |
| TMC5xxx | TMC21xx | Different architecture |

---

## Common Applications

### 3D Printers

| Part | Use Case |
|------|----------|
| TMC2209 | X/Y/Z axes, extruder |
| TMC2208 | Older designs |
| TMC5160 | High-current motors |

### CNC Machines

| Part | Use Case |
|------|----------|
| TMC2160 | Light duty spindle |
| TMC5160 | Axis motors |
| TMC6200 | BLDC spindle |

### Robotics

| Part | Use Case |
|------|----------|
| TMC4671 | Servo control |
| TMC6100 | BLDC joints |
| TMC2209 | Small actuators |

---

## Handler Implementation Notes

### Pattern Matching

```java
// All Trinamic parts start with TMC
if (!upperMpn.startsWith("TMC")) {
    return false;
}

// TMC21xx - Basic stepper drivers
"^TMC21[0-9]{2}.*"

// TMC22xx - Advanced stepper drivers
"^TMC22[0-9]{2}.*"

// TMC4xxx - Gate drivers / Motion controllers
"^TMC4[0-9]{3}.*"

// TMC5xxx - Motion controllers
"^TMC5[0-9]{3}.*"

// TMC6xxx - 3-phase drivers
"^TMC6[0-9]{3}.*"
```

### Package Code Extraction

```java
String extractPackageCode(String mpn) {
    String upperMpn = mpn.toUpperCase();

    // Check for breakout board first (longest match)
    if (upperMpn.contains("-BOB") || upperMpn.endsWith("BOB")) {
        return "Breakout Board";
    }

    // Package codes: -LA, -TA, -WA (with optional -T suffix)
    if (upperMpn.contains("-LA") || upperMpn.matches(".*LA(-T)?$")) {
        return "QFN";
    }
    if (upperMpn.contains("-TA") || upperMpn.matches(".*TA(-T)?$")) {
        return "TQFP";
    }
    if (upperMpn.contains("-WA") || upperMpn.matches(".*WA(-T)?$")) {
        return "WQFN";
    }

    // Check without hyphen separator
    if (upperMpn.endsWith("LA") || upperMpn.endsWith("LAT")) return "QFN";
    if (upperMpn.endsWith("TA") || upperMpn.endsWith("TAT")) return "TQFP";
    if (upperMpn.endsWith("WA") || upperMpn.endsWith("WAT")) return "WQFN";

    return "";
}
```

### Series Extraction

```java
String extractSeries(String mpn) {
    String upperMpn = mpn.toUpperCase();

    if (!upperMpn.startsWith("TMC")) {
        return "";
    }

    // Find where series number ends
    int seriesEnd = 3;  // Start after "TMC"
    for (int i = 3; i < upperMpn.length() && i < 7; i++) {
        if (Character.isDigit(upperMpn.charAt(i))) {
            seriesEnd = i + 1;
        } else {
            break;
        }
    }

    return upperMpn.substring(0, seriesEnd);  // e.g., "TMC2209"
}
```

---

## Related Files

- Handler: `manufacturers/TrinamicHandler.java`
- Component types: `MOTOR_DRIVER`, `IC`
- Note: Trinamic was acquired by Analog Devices in 2021

---

## Key Features by Series

### StealthChop

Silent operation through voltage PWM chopping:
- TMC21xx: StealthChop (1st gen)
- TMC22xx: StealthChop2 (improved)
- TMC5xxx: StealthChop2

### StallGuard

Sensorless load detection:
- TMC2130: StallGuard2 (SPI only)
- TMC2209: StallGuard4 (UART)
- TMC5xxx: StallGuard4

### CoolStep

Current reduction based on load:
- TMC2130: Yes
- TMC2209: Yes
- TMC5160: Yes

---

## Learnings & Edge Cases

- **Analog Devices acquisition**: Trinamic was acquired by Analog Devices in 2021, some new parts may use ADI branding
- **BOB = development**: "-BOB" suffix indicates breakout board, NOT a production package
- **UART vs SPI**: TMC2208/2209 use UART, TMC2130 uses SPI - NOT interchangeable without firmware changes
- **StallGuard versions**: StallGuard2 (TMC2130) and StallGuard4 (TMC2209) have different tuning parameters
- **-T suffix**: Tape and reel packaging, functionally identical to tube packaging
- **TMC5xxx dual**: TMC5041/5072 control TWO motors, TMC5130/5160 control ONE motor
- **3-phase vs stepper**: TMC6xxx is for BLDC/PMSM motors, NOT stepper motors

<!-- Add new learnings above this line -->
