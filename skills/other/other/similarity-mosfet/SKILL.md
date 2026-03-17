---
name: similarity-mosfet
description: Use when working with MOSFET similarity calculations - comparing MOSFET MPNs, understanding N-channel/P-channel matching, equivalent groups like IRF530/STF530, or MOSFET-specific similarity logic.
---

# MOSFET Similarity Calculator Skill

Guidance for working with `MosfetSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `MosfetSimilarityCalculator` compares MOSFETs based on:
- **Equivalent groups** - Cross-manufacturer equivalents
- **Channel type** - N-channel vs P-channel
- **Electrical characteristics** - Voltage, current ratings

## Applicable Types

```java
ComponentType.MOSFET
ComponentType.MOSFET_INFINEON
ComponentType.MOSFET_ST
ComponentType.MOSFET_NXP
// Any type starting with "MOSFET_"
```

Note: Returns `true` for `null` type to handle unrecognized MOSFETs.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Equivalent parts
MEDIUM_SIMILARITY = 0.7; // Similar specs
LOW_SIMILARITY = 0.3;    // Different channel type or specs
```

## Equivalent Groups

The calculator knows these cross-manufacturer equivalents:

| IRF Part | Equivalents |
|----------|-------------|
| IRF530 | STF530, IRF530N, STF530N |
| IRF540 | STF540, IRF540N, STF540N |
| IRF9530 | STF9530, IRF9530N (P-channel) |
| IRF9540 | STF9540, IRF9540N (P-channel) |

## Channel Type Rules

**N-channel and P-channel MOSFETs always return LOW_SIMILARITY (0.3)**

| Part | Channel | Note |
|------|---------|------|
| IRF530 | N-channel | Standard power MOSFET |
| IRF9530 | P-channel | The "9" indicates P-channel |
| IRF540 | N-channel | Higher current than IRF530 |
| IRF9540 | P-channel | Higher current P-channel |

```java
calculator.calculateSimilarity("IRF530", "IRF9530", registry);
// Returns 0.3 (N vs P channel)
```

## Manufacturer Prefix Handling

The calculator normalizes manufacturer prefixes:

| Manufacturer | Prefix | Example |
|--------------|--------|---------|
| International Rectifier | IRF | IRF530 |
| STMicroelectronics | STF | STF530 |
| Vishay | IRF, SIF | SIF530 |
| Infineon | IPD, IPB | IPD530 |

```java
calculator.calculateSimilarity("IRF530", "STF530", registry);
// Returns 0.9 (same part, different manufacturer)
```

## Suffix Handling

Common suffixes that don't affect equivalence:
- `N` - Updated version (IRF530N ≈ IRF530)
- `PBF` - Lead-free
- `L` - Logic level gate

```java
calculator.calculateSimilarity("IRF530", "IRF530N", registry);
// Returns 0.9 (same MOSFET, N is just version)
```

## Test Examples

```java
// Cross-manufacturer equivalent
calculator.calculateSimilarity("IRF530", "STF530", registry);
// Returns 0.9

// N-channel vs P-channel
calculator.calculateSimilarity("IRF530", "IRF9530", registry);
// Returns 0.3

// Different current ratings
calculator.calculateSimilarity("IRF530", "IRF540", registry);
// Returns < 0.9 (14A vs 28A)

// Non-MOSFET parts
calculator.calculateSimilarity("LM358", "LM324", registry);
// Returns 0.0
```

## Implementation Notes

- Returns 0.0 for non-MOSFET MPNs
- The `9` in part number typically indicates P-channel
- Symmetry: `sim(A,B) == sim(B,A)`

---

## Learnings & Quirks

### Part Number Patterns
- IRF5xx/IRF6xx: N-channel power MOSFETs
- IRF95xx/IRF96xx: P-channel equivalents
- The xx number often indicates Vds rating (e.g., 530 ≈ 100V)

### Cross-Manufacturer Equivalence
- STF = ST equivalent to IRF
- Many manufacturers make "drop-in" replacements
- Check Vds, Rds(on), and Id specs for true equivalence

### Package Variants
- TO-220: Standard through-hole
- TO-220F: Isolated tab
- D-PAK: Surface mount
- Same electrical part in different package = HIGH_SIMILARITY

<!-- Add new learnings above this line -->
