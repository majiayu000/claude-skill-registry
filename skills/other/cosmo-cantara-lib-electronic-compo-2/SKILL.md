---
name: cosmo
description: Cosmo Electronics MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Cosmo optocouplers or CosmoHandler.
---

# Cosmo Electronics Manufacturer Skill

## Overview

Cosmo Electronics is a Taiwanese manufacturer specializing in optocouplers and photo interrupters. Their product lines use the "KP" prefix family.

## MPN Structure

Cosmo MPNs follow these general patterns:

### KP Series (Phototransistor Optocouplers)

```
KP[SERIES][VARIANT][-SUFFIX]
   |         |         |
   |         |         +-- Optional: -1=DIP-4, C/S=SMD
   |         +-- Variant letter (optional)
   +-- 4-digit series (e.g., 1010, 2010, 4010)
```

### KPC Series (High Isolation)

```
KPC[SERIES][CTR-GRADE][PKG-IND][-SUFFIX]
    |         |          |        |
    |         |          |        +-- Optional suffix
    |         |          +-- Package indicator (S/G=SMD, T=SOP)
    |         +-- CTR Grade: A/B/C/D
    +-- 3-digit series (e.g., 817, 357)
```

### Example Decoding

```
KP1010-1
|  |   |
|  |   +-- -1 = DIP-4 package
|  +-- 1010 = Single channel phototransistor
+-- KP = Phototransistor optocoupler series

KPC817C-1
|  |  | |
|  |  | +-- -1 = DIP-4 package
|  |  +-- C = CTR grade (200-400%)
|  +-- 817 = General purpose high isolation
+-- KPC = High isolation optocoupler

KPH121S
|  |  |
|  |  +-- S = SMD package
|  +-- 121 = High speed single channel
+-- KPH = High speed optocoupler
```

---

## Product Lines

### KP Series - Phototransistor Optocouplers

| Series | Description | Channels |
|--------|-------------|----------|
| KP1010 | Single channel phototransistor | 1 |
| KP1020 | Single channel (variant) | 1 |
| KP2010 | Dual channel phototransistor | 2 |
| KP4010 | Quad channel phototransistor | 4 |

### KPC Series - High Isolation Optocouplers

| Series | Description | Output |
|--------|-------------|--------|
| KPC817 | General purpose, high isolation | Phototransistor |
| KPC357 | Darlington output | Darlington |

**Note**: KPC817 is functionally equivalent to Sharp PC817.

### KPH Series - High Speed Optocouplers

| Series | Description | Channels |
|--------|-------------|----------|
| KPH121 | High speed single channel | 1 |
| KPH141 | High speed dual channel | 2 |

### KPS Series - SMD Optocouplers

| Series | Description | Package |
|--------|-------------|---------|
| KPS1010 | SMD version of KP1010 | SMD |
| KPS2010 | SMD version of KP2010 | SMD |

### KPTR Series - Reflective Sensors

| Series | Description | Type |
|--------|-------------|------|
| KPTR1200 | Reflective photo interrupter | Sensor |
| KPTR1201 | Reflective photo interrupter | Sensor |

---

## CTR (Current Transfer Ratio) Grades

For KPC817 series:

| Grade | CTR Range | Application |
|-------|-----------|-------------|
| A | 80-160% | Highest gain |
| B | 130-260% | High gain |
| C | 200-400% | Medium gain |
| D | 300-600% | Wide range |

---

## Package Codes

### Suffix-Based Packages

| Suffix | Package | Notes |
|--------|---------|-------|
| -1 | DIP-4 | Standard 4-pin DIP |
| C | SMD | Compact SMD variant |
| S | SMD | Surface mount |
| G | SMD | SMD variant |
| T | SOP | Thin SOP variant |
| -F | Lead-free | RoHS compliant |
| -TR | Tape and reel | Packaging option |

### Default Packages by Series

| Prefix | Default Package |
|--------|-----------------|
| KP | DIP-4 |
| KPC | DIP-4 |
| KPH | DIP |
| KPS | SMD (always) |
| KPTR | SMD (always) |

---

## Channel Count by Series

| Series Pattern | Channels |
|----------------|----------|
| 1010, 1020, 817, 357, 121, 1200, 1201 | 1 |
| 2010, 141 | 2 |
| 4010 | 4 |

---

## Handler Implementation Notes

### Pattern Matching

```java
// KP series: 4-digit series number
"^KP\\d{4}.*"        // KP1010, KP2010, KP4010

// KPC series: 3-digit series number
"^KPC\\d{3}.*"       // KPC817, KPC357

// KPH series: 3-digit series number
"^KPH\\d{3}.*"       // KPH121, KPH141

// KPS series: 4-digit series number
"^KPS\\d{4}.*"       // KPS1010, KPS2010

// KPTR series: 4-digit series number
"^KPTR\\d{4}.*"      // KPTR1200, KPTR1201
```

### Series Extraction

```java
// Returns prefix + series number
"KP1010-1" -> "KP1010"
"KPC817C" -> "KPC817"
"KPH121S" -> "KPH121"
"KPS2010C" -> "KPS2010"
"KPTR1200" -> "KPTR1200"
```

### Package Extraction Logic

```java
// Check for -1 suffix first
"KPC817C-1" -> "DIP-4"

// KPS series is always SMD
"KPS1010" -> "SMD"

// KPTR series is always SMD
"KPTR1200" -> "SMD"

// Check package indicators for KPC
"KPC817CS" -> "SMD"  // S = SMD
"KPC817CT" -> "SOP"  // T = SOP thin

// Check variant letter for KP/KPH
"KP1010C" -> "SMD"
"KPH121S" -> "SMD"

// Default packages
"KP1010" -> "DIP-4"
"KPC817C" -> "DIP-4"
"KPH121" -> "DIP"
```

### CTR Grade Extraction

```java
// KPC series: letter after 3-digit number
"KPC817A" -> "A"
"KPC817B-1" -> "B"
"KPC817CS" -> "C"  // C is CTR, S is package
```

---

## Component Types

The handler maps to these ComponentTypes:

| Prefix | ComponentTypes |
|--------|----------------|
| KP, KPC, KPH, KPS | IC, OPTOCOUPLER_TOSHIBA |
| KPTR | IC, SENSOR |

**Note**: Uses `OPTOCOUPLER_TOSHIBA` as the generic optocoupler type (historical naming).

---

## Cross-Reference / Equivalents

| Cosmo | Equivalent | Notes |
|-------|------------|-------|
| KPC817 | Sharp PC817 | Pin-compatible |
| KPC817 | Toshiba TLP817 | Pin-compatible |
| KPC357 | Sharp PC357 | Darlington output |

---

## Related Files

- Handler: `manufacturers/CosmoHandler.java`
- Component types: `ComponentType.IC`, `ComponentType.OPTOCOUPLER_TOSHIBA`, `ComponentType.SENSOR`

---

## Learnings & Edge Cases

- **CTR grade vs package indicator**: For KPC series, the first letter after digits is CTR grade (A-D), subsequent letters may be package indicators (S/G/T). Order matters.
- **KPS always SMD**: The KPS prefix indicates SMD package regardless of any suffix.
- **KPTR is a sensor**: KPTR series are reflective sensors, not optocouplers. They map to SENSOR type.
- **Channel count from series**: 1010/1020 = single, 2010 = dual, 4010 = quad. The first digit often indicates channel count.
- **Replacement compatibility**: Same series with different packages (DIP vs SMD) are not direct replacements due to footprint differences.

<!-- Add new learnings above this line -->
