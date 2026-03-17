---
name: similarity-regulator
description: Use when working with voltage regulator similarity calculations - comparing 78xx/79xx fixed regulators, LM317/LM337 adjustable regulators, or voltage regulator-specific similarity logic.
---

# Voltage Regulator Similarity Calculator Skill

Guidance for working with `VoltageRegulatorSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `VoltageRegulatorSimilarityCalculator` compares voltage regulators based on:
- **Regulator type** - Fixed (78xx/79xx) vs Adjustable (LM317/LM337)
- **Output voltage** - Must match for fixed regulators
- **Polarity** - Positive vs negative
- **Compatible families** - LM317/LM338/LM350 are compatible

## Applicable Types

```java
ComponentType.VOLTAGE_REGULATOR
// Any type starting with "VOLTAGE_REGULATOR"
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Same voltage/compatible adjustable
MEDIUM_SIMILARITY = 0.7; // Related but different specs
LOW_SIMILARITY = 0.3;    // Different voltage or polarity
```

## Fixed Voltage Regulators (78xx/79xx)

### Positive Regulators (78xx)
| Part | Output Voltage |
|------|----------------|
| 7805 | +5V |
| 7809 | +9V |
| 7812 | +12V |
| 7815 | +15V |
| 7824 | +24V |

### Negative Regulators (79xx)
| Part | Output Voltage |
|------|----------------|
| 7905 | -5V |
| 7912 | -12V |
| 7915 | -15V |
| 7924 | -24V |

### Fixed Regulator Rules

```java
// Same voltage, different manufacturer = HIGH
calculator.calculateSimilarity("LM7805", "MC7805", registry);
// Returns 0.9

// Different voltage = LOW
calculator.calculateSimilarity("LM7805", "LM7812", registry);
// Returns 0.3

// Positive vs Negative = LOW
calculator.calculateSimilarity("LM7805", "LM7905", registry);
// Returns 0.3
```

## Adjustable Voltage Regulators

### Positive Adjustable (Compatible Family)
| Part | Current | Equivalent |
|------|---------|------------|
| LM317 | 1.5A | LM317T, LM317K, LM317H |
| LM338 | 5A | Compatible with LM317 |
| LM350 | 3A | Compatible with LM317 |

### Negative Adjustable
| Part | Current | Note |
|------|---------|------|
| LM337 | 1.5A | Negative equivalent of LM317 |

### Adjustable Regulator Rules

```java
// Same adjustable regulator, different package = HIGH
calculator.calculateSimilarity("LM317T", "LM317K", registry);
// Returns 0.9

// Compatible positive adjustable regulators = HIGH
calculator.calculateSimilarity("LM317", "LM350", registry);
// Returns 0.9

// Positive vs Negative adjustable = LOW
calculator.calculateSimilarity("LM317", "LM337", registry);
// Returns 0.3
```

## Package Code Handling

Common package suffixes:
| Code | Package |
|------|---------|
| T | TO-220 |
| CT | TO-220 (different pinout) |
| K | TO-3 |
| KC | TO-3 |
| KV | TO-3 |
| H | TO-39 |
| S | SOT-223 |
| MP | SOT-223 |
| DT | TO-252 |

```java
// Same regulator, different packages = HIGH
calculator.calculateSimilarity("LM7805CT", "LM7805T", registry);
// Returns 0.9
```

## Manufacturer Prefixes

| Prefix | Manufacturer |
|--------|--------------|
| LM | National/TI |
| MC | Motorola/ON Semi |
| UA | Fairchild |
| L78 | ST |
| KA78 | Fairchild |

## Test Examples

```java
// Same voltage, different manufacturer
calculator.calculateSimilarity("LM7805", "MC7805", registry);
// Returns 0.9

// Same adjustable, different package
calculator.calculateSimilarity("LM317T", "LM317K", registry);
// Returns 0.9

// Compatible adjustable family
calculator.calculateSimilarity("LM317", "LM338", registry);
// Returns 0.9

// Different voltage
calculator.calculateSimilarity("LM7805", "LM7812", registry);
// Returns 0.3

// Positive vs negative
calculator.calculateSimilarity("LM317", "LM337", registry);
// Returns 0.3

// Non-regulator parts
calculator.calculateSimilarity("LM358", "LM324", registry);
// Returns 0.0
```

---

## Learnings & Quirks

### Voltage Detection
- The `xx` in 78xx/79xx indicates voltage (05=5V, 12=12V)
- Pattern: `7[89](\d{2})` extracts the voltage code

### Adjustable Detection
- LM317, LM337, LM338, LM350 are detected by prefix
- Package suffixes (T, K, H) come after the number

### Cross-Manufacturer Equivalence
- LM7805 ≈ MC7805 ≈ UA7805 ≈ L7805
- All major manufacturers make compatible 78xx parts

### Current Rating
- 78Lxx = 100mA (low power)
- 78Mxx = 500mA (medium power)
- 78xx = 1A (standard)
- 78Hxx = 5A (high power)

<!-- Add new learnings above this line -->
