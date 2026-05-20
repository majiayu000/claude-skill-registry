---
name: similarity-memory
description: Use when working with memory IC similarity calculations - comparing EEPROM/Flash MPNs, understanding I2C/SPI interface matching, equivalent groups across manufacturers, or memory-specific similarity logic.
---

# Memory Similarity Calculator Skill

Guidance for working with `MemorySimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `MemorySimilarityCalculator` compares memory ICs based on:
- **Equivalent groups** - Cross-manufacturer equivalents
- **Memory type** - EEPROM, Flash, etc.
- **Interface** - I2C, SPI
- **Capacity** - Must match for high similarity
- **Voltage range** - Operating voltage compatibility

## Applicable Types

```java
ComponentType.MEMORY
// Any type starting with "MEMORY_"
// Returns true for null to handle unrecognized memory devices
```

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Equivalent parts
MEDIUM_SIMILARITY = 0.7; // Same type/interface, close specs
LOW_SIMILARITY = 0.3;    // Different capacity or interface
```

## I2C EEPROM Equivalents

| Capacity | Equivalent Parts |
|----------|------------------|
| 256Kbit | 24LC256, AT24C256, M24C256, CAT24C256 |
| 512Kbit | 24LC512, AT24C512, M24C512, CAT24C512 |
| 1Mbit | 24LC1024, AT24C1024, M24C1024 |

```java
calculator.calculateSimilarity("24LC256", "AT24C256", registry);
// Returns >= 0.7 (equivalent I2C EEPROMs)
```

## SPI EEPROM Equivalents

| Capacity | Equivalent Parts |
|----------|------------------|
| 256Kbit | 25LC256, 25AA256, AT25256, M95256 |
| 512Kbit | 25LC512, 25AA512, AT25512, M95512 |

## SPI Flash Equivalents

| Capacity | Equivalent Parts |
|----------|------------------|
| 32Mbit | W25Q32JV, W25Q32FW, MX25L3233F, S25FL032P, IS25LP032 |
| 64Mbit | W25Q64JV, W25Q64FW, MX25L6433F, S25FL064P, IS25LP064 |
| 128Mbit | W25Q128JV, W25Q128FW, MX25L12833F, S25FL128, IS25LP128 |

```java
calculator.calculateSimilarity("W25Q32JV", "MX25L3233F", registry);
// Returns >= 0.3 (same capacity SPI Flash)
```

## Interface Rules

**I2C and SPI memory have lower similarity due to different interfaces:**

```java
calculator.calculateSimilarity("24LC256", "25LC256", registry);
// Returns <= 0.7 (same capacity, different interface)
```

## Capacity Rules

**Different capacities return LOW_SIMILARITY:**

```java
calculator.calculateSimilarity("W25Q32JV", "W25Q128JV", registry);
// Returns 0.3 (same family, different size)
```

## Package Handling

Package codes don't significantly affect similarity for memory:
- Same memory, different package = HIGH_SIMILARITY (0.9)
- Same memory, compatible package = HIGH_SIMILARITY (0.9)
- Same memory, different package type = ~0.8

## Manufacturer Prefixes

| Prefix | Manufacturer | Type |
|--------|--------------|------|
| 24LC | Microchip | I2C EEPROM |
| AT24C | Atmel/Microchip | I2C EEPROM |
| M24C | ST | I2C EEPROM |
| CAT24C | ON Semi | I2C EEPROM |
| 25LC/25AA | Microchip | SPI EEPROM |
| AT25 | Atmel/Microchip | SPI EEPROM |
| M95 | ST | SPI EEPROM |
| W25Q | Winbond | SPI Flash |
| MX25L | Macronix | SPI Flash |
| S25FL | Spansion/Cypress | SPI Flash |
| IS25LP | ISSI | SPI Flash |

## Test Examples

```java
// Same I2C EEPROM
calculator.calculateSimilarity("24LC256", "24LC256", registry);
// Returns 1.0

// Cross-manufacturer I2C EEPROM
calculator.calculateSimilarity("24LC256", "AT24C256", registry);
// Returns >= 0.7

// Same Flash, different manufacturer
calculator.calculateSimilarity("W25Q64JV", "MX25L6433F", registry);
// Returns >= 0.3

// Different capacity
calculator.calculateSimilarity("24LC256", "24LC512", registry);
// Returns 0.3
```

---

## Metadata-Driven Implementation (January 2026)

**Status**: ✅ Converted (PR #117)

The `MemorySimilarityCalculator` now uses a **metadata-driven approach** with spec-based comparison.

### Specs Compared

| Spec | Importance | Tolerance Rule | Description |
|------|-----------|----------------|-------------|
| **memoryType** | CRITICAL | exactMatch | EEPROM, Flash, SRAM, etc. |
| **capacity** | CRITICAL | exactMatch | 256Kbit, 512Kbit, 1Mbit, etc. |
| **interface** | HIGH | exactMatch | I2C, SPI, Parallel |
| **package** | LOW | exactMatch | SOIC, DIP, TSSOP, etc. |

### Implementation Pattern

```java
// Short-circuit check for CRITICAL incompatibility
if (!memoryType1.isEmpty() && !memoryType2.isEmpty() && !memoryType1.equals(memoryType2)) {
    return LOW_SIMILARITY;
}
if (!capacity1.isEmpty() && !capacity2.isEmpty() && !capacity1.equals(capacity2)) {
    return LOW_SIMILARITY;
}

// Weighted spec scoring
// memoryType: CRITICAL (1.0 weight)
// capacity: CRITICAL (1.0 weight)
// interface: HIGH (0.7 weight)
// package: LOW (0.2 weight)
```

### Behavior Changes

| Comparison | Legacy Result | Metadata Result | Notes |
|-----------|--------------|-----------------|-------|
| 24LC256 vs 24LC256 | 1.0 | 1.0 | Identical |
| 24LC256 vs AT24C256 | 0.7+ | 0.85 | Equivalent I2C EEPROM |
| W25Q32JV vs MX25L3233F | 0.3+ | 0.61 | Same capacity Flash |
| 24LC256 vs 24LC512 | 0.3 | 0.3 | Short-circuit on capacity |
| W25Q32JVSSIQ vs W25Q32JVSFIQ | 0.7+ | 0.93 | Same Flash, different package |

**Why more accurate**: Metadata approach prioritizes capacity and type matching, with interface as secondary concern.

---

## Learnings & Quirks

### Part Number Patterns
- `24xx` = I2C interface, `25xx` = SPI interface
- `C` often indicates CMOS
- Capacity in Kbits: 256 = 32KB, 512 = 64KB, 1024 = 128KB

### Revision Suffixes
- `JV`, `FW`, `JW` on Winbond = package/voltage variants
- `A`, `B`, `C` suffixes = revisions (usually compatible)

### Voltage Compatibility
- Standard: 2.7V-5.5V
- Low voltage: 1.7V-3.6V (check compatibility)

<!-- Add new learnings above this line -->
