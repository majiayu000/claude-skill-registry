---
name: similarity-mcu
description: Use when working with MCU/microcontroller similarity calculations - comparing microcontroller MPNs, understanding family/series/feature matching, or MCU-specific similarity logic.
---

# MCU Similarity Calculator Skill

Guidance for working with MCU similarity calculators in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

There are two MCU-related calculators:

### MCUSimilarityCalculator (Simple Interface)
- Implements `SimilarityCalculator`
- Uses pattern matching for family/series/features
- No PatternRegistry required

### MicrocontrollerSimilarityCalculator (Component Interface)
- Implements `ComponentSimilarityCalculator`
- Uses manufacturer handlers for extraction
- Requires PatternRegistry

## Applicable Types (MicrocontrollerSimilarityCalculator)

```java
ComponentType.MICROCONTROLLER
ComponentType.MICROCONTROLLER_ATMEL
ComponentType.MICROCONTROLLER_INFINEON
ComponentType.MICROCONTROLLER_ST
ComponentType.MCU_ATMEL
```

## Similarity Weights (MCUSimilarityCalculator)

```java
familySimilarity * 0.5   // Family is most important
seriesSimilarity * 0.3   // Series number
featureSimilarity * 0.2  // Feature codes (F, L, U, etc.)
```

## MCU Families

### Family Groups
| Group | Members |
|-------|---------|
| PIC | PIC16, PIC18, PIC24, PIC32 |
| STM | STM8, STM32 |
| ATM | ATMEGA, ATTINY, ATXMEGA |
| MSP | MSP430, MSP432 |

```java
// Same family = 1.0 family similarity
calculator.calculateSimilarity("STM32F103", "STM32F407");
// High similarity (same STM32 family)

// Related family = 0.8 family similarity
calculator.calculateSimilarity("PIC16F877", "PIC18F4550");
// Good similarity (both PIC family)
```

## Feature Codes

| Code | Meaning |
|------|---------|
| F | Flash memory |
| L | Low power |
| U | USB capable |
| W | Wireless |
| R | ROM version |
| T | Extended temperature |

```java
// Same feature codes contribute to similarity
calculator.calculateSimilarity("STM32F103", "STM32F407");
// Both have F (Flash) feature
```

## Series Similarity

Series numbers are compared numerically:
- Same series = 1.0
- Close numbers (within 100) = partial similarity
- Far numbers = lower similarity

```java
// Same series
calculator.calculateSimilarity("ATMEGA328", "ATMEGA328P");
// Very high similarity

// Close series
calculator.calculateSimilarity("ATMEGA328", "ATMEGA329");
// High similarity

// Far series
calculator.calculateSimilarity("ATMEGA328", "ATMEGA2560");
// Lower similarity
```

## MicrocontrollerSimilarityCalculator Scoring

| Condition | Score |
|-----------|-------|
| Same manufacturer, same series, same package | 1.0 |
| Same manufacturer, same series, different package | 0.9 |
| Official replacement parts | 0.8 |
| Same series across manufacturers | 0.7 |
| Both microcontrollers, different series | 0.5 |

## Test Examples

### MCUSimilarityCalculator
```java
// Identical MCU
calculator.calculateSimilarity("ATMEGA328P", "ATMEGA328P");
// Returns 1.0

// Same family, different series
calculator.calculateSimilarity("STM32F103", "STM32F407");
// Returns > 0.5

// Different families
calculator.calculateSimilarity("STM32F103", "ATMEGA328");
// Returns lower similarity
```

### MicrocontrollerSimilarityCalculator
```java
// Same part, different package
calculator.calculateSimilarity("ATMEGA328P-AU", "ATMEGA328P-PU", registry);
// Returns >= 0.5

// Different MCUs
calculator.calculateSimilarity("ATMEGA328P", "STM32F103C8T6", registry);
// Returns 0.5 (base MCU similarity)
```

## Common MCU Patterns

### Atmel/Microchip AVR
```
ATMEGA 328 P -AU
│      │   │  │
│      │   │  └── Package (AU=TQFP)
│      │   └───── Variant (P=Picopower)
│      └───────── Series number
└──────────────── Family
```

### STMicroelectronics STM32
```
STM32 F 103 C8 T6
│     │ │   │  │
│     │ │   │  └── Package (T6=LQFP48)
│     │ │   └───── Memory/pins
│     │ └───────── Series
│     └─────────── Type (F=Foundation)
└───────────────── Family
```

### Microchip PIC
```
PIC16 F 877 A
│     │ │   │
│     │ │   └── Variant
│     │ └────── Series
│     └──────── Memory type (F=Flash)
└────────────── Family
```

---

## Learnings & Quirks

### Family Detection
- Regex `^([A-Z]+)\d+` extracts family prefix
- Empty family = 0.0 family similarity

### Series Number Extraction
- Extracts first numeric sequence
- Compared as integers for proximity

### Feature Code Position
- Usually at end of part number
- Regex `[A-Z]+$` extracts trailing letters

### Package Codes
- Vary significantly by manufacturer
- Don't affect core part equivalence
- Same MCU in different package = HIGH similarity

### Cross-Family Comparison
- Different families get Levenshtein similarity
- Never returns > 0.8 for different families

<!-- Add new learnings above this line -->
