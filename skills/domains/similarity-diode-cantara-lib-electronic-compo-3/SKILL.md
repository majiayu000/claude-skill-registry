---
name: similarity-diode
description: Use when working with diode similarity calculations - comparing signal/rectifier/zener/Schottky diode MPNs, understanding equivalent groups like 1N4148/1N914, or diode-specific similarity logic.
---

# Diode Similarity Calculator Skill

Guidance for working with `DiodeSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `DiodeSimilarityCalculator` compares diodes based on:
- **Diode type** - Signal, rectifier, zener, Schottky
- **Equivalent groups** - Known interchangeable parts
- **Voltage ratings** - For rectifier and zener diodes

## Applicable Types

```java
ComponentType.DIODE
// Any type starting with "DIODE_"
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Equivalent parts
MEDIUM_SIMILARITY = 0.7; // Same family, compatible
LOW_SIMILARITY = 0.3;    // Same type, different specs
```

## Signal Diode Equivalents

| Group | Members | Notes |
|-------|---------|-------|
| 1N4148/1N914 | 1N4148, 1N914 | Classic signal diodes, equivalent |

```java
calculator.calculateSimilarity("1N4148", "1N914", registry);
// Returns 0.9 (equivalent signal diodes)
```

## Rectifier Diode Equivalents

### 1N400x Series (1A Rectifiers)
| Part | Voltage | Equivalent |
|------|---------|------------|
| 1N4001 | 50V | RL201 |
| 1N4002 | 100V | RL202 |
| 1N4003 | 200V | RL203 |
| 1N4004 | 400V | RL204 |
| 1N4005 | 600V | RL205 |
| 1N4006 | 800V | RL206 |
| 1N4007 | 1000V | RL207 |

```java
// Same voltage equivalents
calculator.calculateSimilarity("1N4007", "RL207", registry);
// Returns 0.9 (both 1000V rectifiers)

// Same family, different voltage
calculator.calculateSimilarity("1N4001", "1N4007", registry);
// Returns 0.9 (same family, all rectifiers)

calculator.calculateSimilarity("1N4001", "1N4004", registry);
// Returns >= 0.7 (same family)
```

## Zener Diode Rules

Zener diodes are compared by voltage rating:

| Part | Voltage |
|------|---------|
| 1N4728 | 3.3V |
| 1N4733 | 5.1V |
| 1N4742 | 12V |
| 1N4744 | 15V |

```java
// Same voltage zener
calculator.calculateSimilarity("1N4733", "1N4733", registry);
// Returns 0.9

// Different voltage zeners
calculator.calculateSimilarity("1N4733", "1N4742", registry);
// Returns 0.3 (5.1V vs 12V - not interchangeable)
```

## Schottky Diode Equivalents

| Group | Members |
|-------|---------|
| BAT54 | BAT54, BAT54S (series dual) |

```java
calculator.calculateSimilarity("BAT54", "BAT54S", registry);
// Returns 0.9 (same Schottky, different configuration)
```

## Test Examples

```java
// Equivalent signal diodes
calculator.calculateSimilarity("1N4148", "1N914", registry);
// Returns 0.9

// Same rectifier diode
calculator.calculateSimilarity("1N4007", "1N4007", registry);
// Returns 0.9

// Cross-manufacturer rectifier
calculator.calculateSimilarity("1N4007", "RL207", registry);
// Returns 0.9

// Same zener voltage
calculator.calculateSimilarity("1N4733", "1N4733", registry);
// Returns 0.9

// Different zener voltage
calculator.calculateSimilarity("1N4733", "1N4742", registry);
// Returns 0.3

// Non-diode parts
calculator.calculateSimilarity("LM358", "LM324", registry);
// Returns 0.0
```

---

## Learnings & Quirks

### 1N400x Series Pattern
- 1N = JEDEC prefix
- 400x = 1A rectifier series
- x = voltage code (1=50V through 7=1000V)

### Zener Voltage Codes
- 1N47xx series: xx roughly indicates voltage
- Need lookup table for exact voltage

### Schottky Configurations
- BAT54 = Single diode
- BAT54S = Series dual (2 diodes in series)
- BAT54A = Common anode
- BAT54C = Common cathode
- These are same diode, different configurations

### Signal vs Rectifier
- Signal diodes (1N4148): Fast switching, low current
- Rectifier diodes (1N4007): Higher current, slower

<!-- Add new learnings above this line -->
