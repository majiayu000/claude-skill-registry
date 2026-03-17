---
name: similarity-resistor
description: Use when working with resistor similarity calculations - comparing resistor MPNs, understanding value/tolerance/package matching, or implementing resistor-specific similarity logic.
---

# Resistor Similarity Calculator Skill

Guidance for working with `ResistorSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `ResistorSimilarityCalculator` compares resistors based on:
- **Package size** (0.3 weight) - 0402, 0603, 0805, etc.
- **Resistance value** (0.5 weight) - 10K, 100R, 4.7K, etc.

Maximum similarity is 0.8 (not 1.0) since tolerance and other specs aren't always extractable.

## Applicable Types

```java
ComponentType.RESISTOR
ComponentType.RESISTOR_CHIP_VISHAY
ComponentType.RESISTOR_CHIP_YAGEO
ComponentType.RESISTOR_CHIP_PANASONIC
ComponentType.RESISTOR_CHIP_BOURNS
// Any type starting with "RESISTOR_"
```

## Similarity Scoring

| Condition | Score |
|-----------|-------|
| Same value, same package | 0.8 |
| Same value, different package | 0.5 |
| Same package, different value | 0.3 |
| Different value, different package | 0.0 |

## Value Extraction

The calculator extracts resistance values from MPNs:

| MPN | Extracted Value |
|-----|-----------------|
| `CRCW060310K0FKEA` | 10K (10kΩ) |
| `RC0603FR-0710KL` | 10K (10kΩ) |
| `ERJ3GEYJ103V` | 10K (103 = 10×10³) |

## Package Size Extraction

Common package codes in MPNs:

| Pattern | Package |
|---------|---------|
| `0603` | 0603 (1608 metric) |
| `0805` | 0805 (2012 metric) |
| `1206` | 1206 (3216 metric) |

## Cross-Manufacturer Matching

The calculator can match equivalent resistors across manufacturers:

```java
// Vishay 0603 10K vs Yageo 0603 10K
calculator.calculateSimilarity("CRCW060310K0FKEA", "RC0603FR-0710KL", registry);
// Returns >= 0.5 (both are 10K, may have same package)
```

## Test Examples

```java
// Same Vishay resistor - max similarity
calculator.calculateSimilarity("CRCW060310K0FKEA", "CRCW060310K0FKEA", registry);
// Returns 0.8

// Same value, different package
calculator.calculateSimilarity("CRCW060310K0FKEA", "CRCW080510K0FKEA", registry);
// Returns 0.5

// Same package, different value
calculator.calculateSimilarity("CRCW0603100RFKEA", "CRCW060310K0FKEA", registry);
// Returns 0.3 (100R vs 10K)
```

## Implementation Notes

- Returns 0.0 for null MPNs or null registry
- Returns 0.0 for empty strings
- Handles unrecognized formats gracefully (returns 0.0-1.0)

---

## Learnings & Quirks

### Value Notation
- E96 notation: `103` = 10×10³ = 10kΩ, `4R7` = 4.7Ω
- Yageo TCR code `-07` is NOT a separator, it's temperature coefficient

### Package Extraction
- Some MPNs embed package in series name (e.g., `RC0603`)
- Others have separate position (e.g., `CRCW` + `0603`)

<!-- Add new learnings above this line -->
