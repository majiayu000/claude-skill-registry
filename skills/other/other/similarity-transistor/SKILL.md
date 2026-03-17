---
name: similarity-transistor
description: Use when working with transistor similarity calculations - comparing BJT MPNs, understanding NPN/PNP polarity matching, equivalent groups like 2N2222/PN2222, or transistor-specific similarity logic.
---

# Transistor Similarity Calculator Skill

Guidance for working with `TransistorSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `TransistorSimilarityCalculator` compares bipolar junction transistors (BJTs) based on:
- **Equivalent groups** - Known interchangeable parts
- **Polarity** - NPN vs PNP (must match)
- **Family/series** - BC, 2N, PN, etc.

## Applicable Types

```java
ComponentType.TRANSISTOR
ComponentType.TRANSISTOR_NXP
ComponentType.TRANSISTOR_VISHAY
// Any type starting with "TRANSISTOR_"
```

Note: Does NOT apply to MOSFETs - use `MosfetSimilarityCalculator` for those.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Equivalent parts
MEDIUM_SIMILARITY = 0.7; // Same family, compatible
LOW_SIMILARITY = 0.3;    // Same category, different specs or polarity
```

## Equivalent Groups

The calculator knows these equivalent groups:

| Group | Members |
|-------|---------|
| 2N2222 family | 2N2222, 2N2222A, PN2222, PN2222A |
| 2N3904 family | 2N3904, PN3904 |
| 2N3906 family | 2N3906, PN3906 |
| 2N2907 family | 2N2907, 2N2907A, PN2907, PN2907A |
| BC547 family | BC547, BC547A, BC547B, BC547C |
| BC557 family | BC557, BC557A, BC557B, BC557C |

## Polarity Rules

**NPN and PNP transistors always return LOW_SIMILARITY (0.3)**

| Comparison | Result |
|------------|--------|
| 2N2222 (NPN) vs PN2222 (NPN) | 0.9 (equivalent) |
| 2N2222 (NPN) vs 2N2907 (PNP) | 0.3 (different polarity) |
| 2N3904 (NPN) vs 2N3906 (PNP) | 0.3 (complementary pair, different polarity) |

## Suffix Handling

The calculator ignores common suffixes:
- `-T`, `-TR`, `-TA` (tape/reel packaging)
- `A`, `B`, `C` (grade suffixes on BC series)

```java
calculator.calculateSimilarity("2N2222", "2N2222-T", registry);
// Returns 0.9 (same transistor, different packaging)

calculator.calculateSimilarity("2n2222", "2N2222", registry);
// Returns 0.9 (case insensitive)
```

## Test Examples

```java
// Equivalent parts
calculator.calculateSimilarity("2N2222", "PN2222", registry);
// Returns 0.9

// Same part with variant
calculator.calculateSimilarity("2N2222", "2N2222A", registry);
// Returns 0.9

// NPN vs PNP
calculator.calculateSimilarity("2N2222", "2N2907", registry);
// Returns 0.3

// Different families
calculator.calculateSimilarity("2N2222", "BC547", registry);
// Returns 0.3

// Non-transistor parts
calculator.calculateSimilarity("LM358", "MC1458", registry);
// Returns 0.0
```

## Implementation Notes

- Returns 0.0 for non-transistor MPNs
- Returns 0.0 for mixed transistor/non-transistor comparison
- Symmetry: `sim(A,B) == sim(B,A)`

---

## Learnings & Quirks

### Part Number Patterns
- `2N` prefix: JEDEC standard (2N2222, 2N3904, etc.)
- `PN` prefix: Often equivalent to 2N (PN2222 ≈ 2N2222)
- `BC` prefix: European standard (BC547, BC557)
- `MPS` prefix: Motorola/ON Semi (MPS2222A ≈ 2N2222A)

### Complementary Pairs
- 2N3904 (NPN) / 2N3906 (PNP)
- BC547 (NPN) / BC557 (PNP)
- These are designed to work together but are NOT equivalent

<!-- Add new learnings above this line -->
