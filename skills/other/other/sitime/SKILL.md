---
name: sitime
description: SiTime MEMS oscillator MPN encoding patterns, suffix decoding, and handler guidance. Use when working with SiTime timing components or SiTimeHandler.
---

# SiTime Manufacturer Skill

## Overview

SiTime is a leading manufacturer of **MEMS-based silicon timing solutions** including:
- MEMS oscillators (MHz and kHz)
- Super-TCXOs (temperature-compensated)
- Clock generators
- Automotive-qualified timing devices

SiTime's MEMS technology offers advantages over traditional quartz crystals:
- Higher shock/vibration resistance
- Smaller footprint options
- Programmable frequency
- Better reliability in harsh environments

---

## MPN Structure

SiTime MPNs follow this general structure:

```
SiT[FAMILY]-[TEMP/OPTIONS]-[PACKAGE]-[FREQUENCY][OUTPUT]
    │              │            │          │        │
    │              │            │          │        └── Optional output type suffix (X, M, K)
    │              │            │          └── Frequency in MHz or kHz (e.g., 24.000000, 32.768)
    │              │            └── Package size code (e.g., 18E, DCC, 32E)
    │              └── Temperature grade + options (e.g., AI, BI, H4)
    └── Product family (e.g., 1533, 8008, 9121)
```

### Example Decoding

```
SiT1533AI-H4-18E-32.768000X
│   │   │   │   │    │     │
│   │   │   │   │    │     └── X = Output type suffix
│   │   │   │   │    └── 32.768000 = Frequency (32.768 kHz)
│   │   │   │   └── 18E = 1.6x1.2mm package (1612 size)
│   │   │   └── H4 = Voltage/configuration code
│   │   └── AI = Temperature grade A, option I
│   └── 1533 = MHz LVCMOS Oscillator series
└── SiT = SiTime prefix

SiT8021AC-82-33S-24.000000X
│   │    │   │   │    │     │
│   │    │   │   │    │     └── X = Output type suffix
│   │    │   │   │    └── 24.000000 = 24 MHz
│   │    │   │   └── 33S = 3.2x2.5mm SOIC variant
│   │    │   └── 82 = Voltage/configuration
│   │    └── AC = Temperature grade A, variant C
│   └── 8021 = Precision MHz Oscillator
└── SiT = SiTime prefix
```

---

## Product Families

### SiT15xx - MHz LVCMOS Oscillators

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT1533 | 32.768 kHz MEMS Oscillator | Crystal replacement, ultra-low power |
| SiT1534 | 32.768 kHz MEMS Oscillator | Higher accuracy variant |
| SiT1552 | 32.768 kHz with AEC-Q100 | Automotive qualified |

### SiT16xx - Low Power Oscillators

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT1602 | Low Power MHz Oscillator | Battery applications |
| SiT1618 | Ultra Low Power | IoT/wearable focus |

### SiT17xx - Ultra Low Power

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT1701 | Ultra Low Power | Lowest power consumption |

### SiT5xxx/SiT85xx - Super-TCXO

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT5155 | Super-TCXO | +/-0.5 ppm stability |
| SiT5156 | Super-TCXO | Extended temperature range |
| SiT85xx | Super-TCXO alternate naming | Same family |

### SiT80xx - Precision MHz Oscillators

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT8008 | Precision Oscillator | Low jitter, wide freq range |
| SiT8021 | High Precision | Sub-1 ppm stability |

### SiT81xx - Differential Oscillators

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT8148 | LVDS Output | High-speed differential |
| SiT8152 | LVPECL Output | Network/telecom applications |

### SiT86xx - High Performance

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT8621 | High Performance | Data center, 5G applications |

### SiT88xx - Network Sync

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT8814 | Network Sync Oscillator | Telecom synchronization |

### SiT90xx - High Temperature

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT9002 | High Temp Oscillator | -55C to +125C industrial |

### SiT91xx - Automotive AEC-Q100

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT9120 | Automotive Oscillator | AEC-Q100 Grade 1 |
| SiT9121 | Automotive Oscillator | Enhanced automotive |

### SiT93xx - Clock Generators

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT9367 | Multi-output Clock Gen | Multiple frequencies |

### SiT95xx - High Performance Clock

| Series | Description | Key Features |
|--------|-------------|--------------|
| SiT9501 | High Performance | Ultra-low jitter |

---

## Package Codes

### Numeric Size Codes

| Code | Physical Size | Industry Name | Notes |
|------|---------------|---------------|-------|
| 18E / 18 | 1.6 x 1.2 mm | 1612 | Ultra-small |
| 21E / 21 | 2.0 x 1.6 mm | 2016 | Very small |
| 25E / 25 | 2.5 x 2.0 mm | 2520 | Small |
| 32E / 32 | 3.2 x 2.5 mm | 3225 | Standard |
| 50E / 50 | 5.0 x 3.2 mm | 5032 | Medium |
| 70E / 70 | 7.0 x 5.0 mm | 7050 | Large |

### Chip-Scale Packages

| Code | Physical Size | Notes |
|------|---------------|-------|
| DCC | 1.5 x 0.8 mm | Chip-Scale Package (CSP) |
| DCS | 1.2 x 1.0 mm | Ultra-small CSP |

### Other Packages

| Code | Package Type | Notes |
|------|--------------|-------|
| SOT | SOT23-5 | 5-pin small outline |
| QFN | QFN | Quad Flat No-lead |

---

## Temperature Grades

Temperature grades are typically indicated in the first segment after the family number:

| Grade Letter | Range | Application |
|--------------|-------|-------------|
| A | Standard | Commercial (0C to +70C) |
| B | Extended | Industrial (-40C to +85C) |
| C | Automotive | Automotive (-40C to +105C) |
| E | Extreme | Extended industrial (-40C to +125C) |

**Examples**:
- `SiT1533AI` - Grade A, Industrial option
- `SiT8021BC` - Grade B, Extended

---

## Voltage/Configuration Codes

The second segment (after temperature) often contains voltage and configuration info:

| Code | Typical Meaning |
|------|-----------------|
| H4 | High voltage config |
| 71 | 1.8V supply |
| 82 | 2.5V/3.3V supply |
| 33S | 3.3V SOIC variant |

**Note**: These codes vary by product family - consult SiTime datasheets for specific mappings.

---

## Frequency Encoding

Frequency appears as the last numeric segment before any output type suffix:

| Format | Meaning | Example |
|--------|---------|---------|
| `32.768` | 32.768 kHz | RTC applications |
| `24.000000` | 24 MHz | Standard MHz oscillator |
| `25.000000` | 25 MHz | Ethernet applications |
| `48.000000` | 48 MHz | USB applications |
| `100.000000` | 100 MHz | High-speed applications |

### Common Frequencies

| Frequency | Application |
|-----------|-------------|
| 32.768 kHz | RTC, low power |
| 10 MHz | Reference oscillator |
| 12 MHz | USB full speed |
| 24 MHz | Microcontroller clock |
| 25 MHz | Ethernet PHY |
| 48 MHz | USB high speed |
| 100 MHz | High-speed logic |
| 125 MHz | Gigabit Ethernet |

---

## Output Type Suffixes

| Suffix | Output Type | Notes |
|--------|-------------|-------|
| X | LVCMOS | Standard push-pull |
| M | LVDS | Differential |
| K | Clipped sine | Low EMI |
| (none) | Default for series | Check datasheet |

---

## Component Types in Handler

The SiTimeHandler supports:

| ComponentType | Description | Pattern |
|---------------|-------------|---------|
| OSCILLATOR | Primary type | `^SIT[0-9]{4}.*` |
| CRYSTAL | 32.768 kHz parts | `^SIT1[567][0-9]{2}.*-32\.768.*` |
| IC | Generic IC type | `^SIT[0-9]{4}.*` |

**Note**: 32.768 kHz MEMS oscillators can serve as drop-in replacements for quartz crystals, hence the CRYSTAL type registration for those frequencies.

---

## Handler Implementation Notes

### Series Extraction

```java
// Series is extracted as "SiT" + first 2 digits of 4-digit family
// Example: SiT1533AI-H4-18E-32.768000X -> "SiT15"
// Example: SiT8021AC-82-33S-24.000000X -> "SiT80"

// Special case: SiT5xxx Super-TCXO series
// SiT5155 -> "SiT5" (not "SiT51")
if (upperMpn.startsWith("SIT5") && Character.isDigit(upperMpn.charAt(4))) {
    return "SiT5";
}
```

### Package Extraction

```java
// Package code is typically the third hyphen-separated segment
// SiT1533AI-H4-18E-32.768000X
//              ^^^
// Pattern: -([0-9]{2}[A-Z]|[A-Z]{2,3})-
```

### Frequency Extraction

```java
// Frequency is the last segment after the final hyphen
// SiT1533AI-H4-18E-32.768000X
//                  ^^^^^^^^^^
// Pattern: ([0-9]+(?:\.[0-9]+)?)[MKX]?$
```

### Official Replacement Logic

Two SiTime parts can be replacements if:
1. Same series (e.g., both SiT15)
2. Same frequency

They may differ in:
- Temperature grade
- Package size
- Voltage configuration

---

## Example MPNs

| MPN | Series | Package | Frequency | Description |
|-----|--------|---------|-----------|-------------|
| SiT1533AI-H4-18E-32.768000X | SiT15 | 1.6x1.2mm | 32.768 kHz | LVCMOS 32.768kHz oscillator |
| SiT1552BC-H4-DCC-32.768000 | SiT15 | 1.5x0.8mm CSP | 32.768 kHz | Automotive 32.768kHz |
| SiT8008BI-82-33E-24.000000X | SiT80 | 3.2x2.5mm | 24 MHz | Precision oscillator |
| SiT8021AC-82-33S-24.000000X | SiT80 | 3.2x2.5mm | 24 MHz | High precision oscillator |
| SiT9121AI-2C1-25E-48.000000 | SiT91 | 2.5x2.0mm | 48 MHz | AEC-Q100 automotive |
| SiT5156AI-H4-DCC-25.000000M | SiT5 | 1.5x0.8mm CSP | 25 MHz | Super-TCXO with LVDS |
| SiT9367AI-JW-25E | SiT93 | 2.5x2.0mm | Programmable | Clock generator |

---

## Crystal Replacement Use Case

SiTime 32.768 kHz oscillators are often used as drop-in replacements for traditional quartz crystals in RTC applications:

**Traditional Crystal Circuit**:
```
[MCU] --XTAL1-- [Crystal] --XTAL2-- [MCU]
                   |
                 [Caps]
```

**SiTime MEMS Replacement**:
```
[MCU] --OSC_IN-- [SiT1533] --VDD-- [Power]
                     |
                   [GND]
```

**Advantages of MEMS replacement**:
- No external load capacitors needed
- Better shock/vibration resistance
- Faster startup time
- More consistent frequency across temperature

---

## Related Files

- Handler: `manufacturers/SiTimeHandler.java`
- Component types: `OSCILLATOR`, `CRYSTAL`, `IC`
- Series descriptions: Available via `getSeriesDescription(mpn)` helper method

---

## Learnings & Edge Cases

- **SiT5 vs SiT85**: Both refer to Super-TCXO family. `SiT5xxx` and `SiT85xx` patterns are both registered.
- **Frequency parsing**: Frequency appears after the last hyphen, before optional output suffix (X, M, K).
- **32.768 kHz special case**: These parts are registered as both OSCILLATOR and CRYSTAL types since they can replace quartz crystals.
- **Package code position**: The package code is in the third hyphen-separated segment, not a suffix like many other manufacturers.
- **No manufacturer-specific ComponentTypes**: SiTimeHandler uses generic types (OSCILLATOR, CRYSTAL, IC) rather than SiTime-specific types.
- **Case insensitivity**: Handler converts MPNs to uppercase before pattern matching (`SiT` = `SIT` = `sit`).
- **Series extraction returns 2-digit**: Unlike some handlers that return full part numbers, SiTime series extraction returns abbreviated form (e.g., "SiT15" not "SiT1533").

<!-- Add new learnings above this line -->
