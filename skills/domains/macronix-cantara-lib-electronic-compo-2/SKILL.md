---
name: macronix
description: Macronix International MPN encoding patterns, density decoding, and handler guidance. Use when working with Macronix Flash memory components or MacronixHandler.
---

# Macronix International Manufacturer Skill

## Overview

Macronix International Co., Ltd. is a Taiwan-based manufacturer specializing in Flash memory ICs. The company produces:

- **Serial NOR Flash** (MX25L, MX25U, MX25R, MX25V, MX66L series)
- **Parallel NOR Flash** (MX29GL, MX29LV series)
- **SLC NAND Flash** (MX30LF series)
- **ROM ICs**

Macronix is known for high-reliability Flash memory used in embedded systems, IoT devices, automotive, and industrial applications.

---

## MPN Structure

Macronix MPNs follow this general structure:

### Serial NOR Flash (MX25L/U/R/V, MX66L)

```
MX25 L 6433 F MI - 08 G
│    │ │    │ │    │  │
│    │ │    │ │    │  └── Grade: G=Green/RoHS
│    │ │    │ │    └───── Speed: 08=80MHz, 10=104MHz
│    │ │    │ └────────── Package code (see table below)
│    │ │    └──────────── Feature: F=Fast Read, E=Extended Temp
│    │ └───────────────── Density code (see density decoding)
│    └─────────────────── Series: L=Standard, U=Ultra Low Power, R=Wide Voltage, V=Very Low Voltage
└──────────────────────── Family prefix
```

### Parallel NOR Flash (MX29GL, MX29LV)

```
MX29 GL 256 F HT 2 I - 90 Q
│    │  │   │ │  │ │   │  │
│    │  │   │ │  │ │   │  └── Qualifier
│    │  │   │ │  │ │   └───── Speed: 90=90ns
│    │  │   │ │  │ └───────── Temperature: I=Industrial
│    │  │   │ │  └─────────── Version: 2=Version 2
│    │  │   │ └────────────── Package: HT=TSOP-48
│    │  │   └──────────────── Feature: F=Fast
│    │  └──────────────────── Density: 256=256Mbit
│    └─────────────────────── Series: GL=High Density, LV=Low Voltage
└──────────────────────────── Family prefix
```

### SLC NAND Flash (MX30LF)

```
MX30 LF 1G 18 AC
│    │  │  │  │
│    │  │  │  └── Package: AC=TSOP-48
│    │  │  └───── Bus width: 18=x8
│    │  └──────── Density: 1G=1Gbit, 2G=2Gbit
│    └─────────── Series: LF=SLC NAND Flash
└──────────────── Family prefix
```

---

## Series Reference

### Serial NOR Flash

| Series | Description | Voltage Range | Features |
|--------|-------------|---------------|----------|
| MX25L | Standard Serial NOR | 2.7V-3.6V | SPI/QSPI, standard power |
| MX25U | Ultra Low Power | 1.65V-1.95V | SPI/QSPI, low power mode |
| MX25R | Wide Voltage Range | 1.65V-3.6V | Flexible voltage operation |
| MX25V | Very Low Voltage | 2.3V-3.6V | Optimized for low voltage |
| MX66L | High Performance | 2.7V-3.6V | High speed, large density |

### Parallel NOR Flash

| Series | Description | Voltage | Features |
|--------|-------------|---------|----------|
| MX29GL | High Density | 3.3V | Large capacity, burst read |
| MX29LV | Low Voltage | 3.0V | Low power consumption |

### NAND Flash

| Series | Description | Technology |
|--------|-------------|------------|
| MX30LF | SLC NAND | Single-Level Cell, high endurance |

---

## Density Decoding

### Serial NOR Flash Density Codes

Macronix serial flash uses a special encoding where the first 2-4 digits represent density:

| Code | Density | Bytes |
|------|---------|-------|
| 6433, 6435 | 64 Mbit | 8 MB |
| 12833, 12835 | 128 Mbit | 16 MB |
| 25635, 25645 | 256 Mbit | 32 MB |
| 51235, 51245 | 512 Mbit | 64 MB |
| 1G | 1 Gbit | 128 MB |
| 2G | 2 Gbit | 256 MB |

### Parallel NOR Flash Density Codes

| Raw Code | Actual Density | Notes |
|----------|----------------|-------|
| 256 | 256 Mbit | Direct encoding (MX29GL) |
| 128 | 128 Mbit | Direct encoding (MX29GL) |
| 640 | 64 Mbit | Scaled encoding (MX29LV) |
| 320 | 32 Mbit | Scaled encoding (MX29LV) |
| 160 | 16 Mbit | Scaled encoding (MX29LV) |
| 800 | 8 Mbit | Scaled encoding (MX29LV) |

**Important**: MX29LV series uses scaled encoding (multiply by 0.1 for Mbits), while MX29GL uses direct encoding.

---

## Package Codes

| Code | Package | Pin Count | Notes |
|------|---------|-----------|-------|
| MI | SOP-8 | 8 | Standard SOIC, 150mil body |
| MN | DFN-8 | 8 | Dual Flat No-lead |
| ZI | WSON-8 | 8 | Very thin package |
| SI | SOIC-8 | 8 | Standard SOIC |
| SS | SOIC-8 | 8 | SOIC variant |
| DI | SOIC-16 | 16 | Wide body SOIC |
| TI | TSOP-8 | 8 | Thin Small Outline |
| BH | BGA | Various | Ball Grid Array |
| FH | FBGA | Various | Fine-pitch BGA |
| HT | TSOP-48 | 48 | Parallel flash standard |
| AC | TSOP-48 | 48 | NAND standard package |
| ZB | WSON-8 | 8 | WSON variant |
| EB | BGA | Various | BGA variant |
| LI | WLCSP | Various | Wafer-Level CSP |

---

## Supported Component Types

The `MacronixHandler` supports:

```java
ComponentType.MEMORY
ComponentType.MEMORY_FLASH
```

Note: Unlike some handlers, MacronixHandler does not define manufacturer-specific types like `MEMORY_FLASH_MACRONIX`. Both patterns register to `MEMORY` and `MEMORY_FLASH` base types.

---

## Handler Implementation Notes

### Package Code Extraction

The handler extracts package codes differently based on the flash family:

**Serial NOR (MX25L/U/R/V, MX66L)**:
1. Find position of 'F' or 'E' (feature letter)
2. Extract 2 characters after the feature letter
3. Map to package name if known, otherwise return empty

```java
// Example: MX25L6433FMI-08G
// F is at index 10, MI is at 11-12
// Returns "SOP-8"
```

**Parallel NOR (MX29GL, MX29LV)**:
1. Use regex pattern to find 2-letter code after density
2. Map to package name

```java
// Example: MX29GL256FHT2I-90Q
// HT follows density and F
// Returns "TSOP-48"
```

**NAND (MX30LF)**:
1. Extract last 2 characters before hyphen
2. Map to package or return raw suffix

```java
// Example: MX30LF1G18AC
// AC is the suffix
// Returns "TSOP-48"
```

### Series Extraction

Returns the family prefix including the series letter:

| MPN | Series |
|-----|--------|
| MX25L6433FMI-08G | MX25L |
| MX25U12835FMI-10G | MX25U |
| MX66L1G45GMI-10G | MX66L |
| MX29GL256FHT2I-90Q | MX29GL |
| MX29LV640EBTI-70Q | MX29LV |
| MX30LF1G18AC | MX30LF |

### Density Extraction

The `extractDensity()` method (Macronix-specific helper) returns the decoded density:

| MPN | Extracted Density |
|-----|-------------------|
| MX25L6433F | 64 |
| MX25L12835F | 128 |
| MX29GL256 | 256 |
| MX29LV640 | 64 |
| MX30LF1G18AC | 1G |

### Replacement Logic

`isOfficialReplacement()` returns true when:
1. Both parts are in the same series (e.g., both MX25L)
2. Both parts have the same density

Package and speed differences are acceptable for replacements.

---

## Example MPNs with Full Decoding

### MX25L6433FMI-08G

| Field | Value | Meaning |
|-------|-------|---------|
| Family | MX25 | Serial NOR Flash |
| Series | L | Standard voltage (2.7V-3.6V) |
| Density | 6433 | 64 Mbit |
| Feature | F | Fast Read supported |
| Package | MI | SOP-8 |
| Speed | 08 | 80 MHz |
| Grade | G | RoHS compliant |

### MX25L12835FMI-10G

| Field | Value | Meaning |
|-------|-------|---------|
| Family | MX25 | Serial NOR Flash |
| Series | L | Standard voltage |
| Density | 12835 | 128 Mbit |
| Feature | F | Fast Read |
| Package | MI | SOP-8 |
| Speed | 10 | 104 MHz |
| Grade | G | RoHS compliant |

### MX29GL256FHT2I-90Q

| Field | Value | Meaning |
|-------|-------|---------|
| Family | MX29 | Parallel NOR Flash |
| Series | GL | High density 3.3V |
| Density | 256 | 256 Mbit |
| Feature | F | Fast |
| Package | HT | TSOP-48 |
| Version | 2 | Version 2 |
| Temp | I | Industrial (-40 to +85C) |
| Speed | 90 | 90ns access time |

### MX30LF1G18AC

| Field | Value | Meaning |
|-------|-------|---------|
| Family | MX30 | NAND Flash |
| Series | LF | SLC NAND |
| Density | 1G | 1 Gbit |
| Bus | 18 | x8 data bus |
| Package | AC | TSOP-48 |

---

## Related Files

- Handler: `manufacturers/MacronixHandler.java`
- Memory skill: `.claude/skills/memory/SKILL.md`
- Winbond handler (similar memory manufacturer): `manufacturers/WinbondHandler.java`
- Component types: `MEMORY`, `MEMORY_FLASH`

---

## Learnings & Edge Cases

### Density Code Complexity
- Serial NOR uses complex density encoding (6433 = 64Mb, not 6.4Gb)
- Parallel NOR LV series uses scaled encoding (640 = 64Mb, 160 = 16Mb)
- NAND uses explicit Gbit notation (1G, 2G)

### Package Code Position Varies
- Serial NOR: Package comes after feature letter (F or E)
- Parallel NOR: Package is part of the middle segment
- NAND: Package is the last 2 characters before hyphen

### No Manufacturer-Specific Types
- Unlike TI (OPAMP_TI) or Winbond (MEMORY_FLASH_WINBOND), Macronix does not have manufacturer-specific ComponentTypes
- All patterns map to base `MEMORY` and `MEMORY_FLASH` types
- This simplifies matching but loses manufacturer specificity

### Speed Grades
- Serial NOR: -08 = 80MHz, -10 = 104MHz, -12 = 120MHz
- Parallel NOR: -55 = 55ns, -70 = 70ns, -90 = 90ns

### Voltage Series Selection Guide
- MX25L: Standard applications, 2.7V-3.6V
- MX25U: Battery-powered, ultra-low power
- MX25R: Designs needing voltage flexibility
- MX25V: Legacy 3.3V systems needing lower threshold
- MX66L: High-performance, large storage needs

### Cross-Manufacturer Equivalents
- MX25L series competes with Winbond W25Q series
- MX30LF NAND competes with Micron MT29F series
- Serial NOR from different manufacturers often pin-compatible

<!-- Add new learnings above this line -->
