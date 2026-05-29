---
name: similarity-capacitor
description: Use when working with capacitor similarity calculations - comparing ceramic/electrolytic/film capacitor MPNs, understanding value/voltage/dielectric matching, or capacitor-specific similarity logic.
---

# Capacitor Similarity Calculator Skill

Guidance for working with `CapacitorSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `CapacitorSimilarityCalculator` compares capacitors based on:
- **Capacitance value** - Must match for high similarity
- **Package size** - 0402, 0603, 0805, etc.
- **Voltage rating** - Should be compatible
- **Dielectric type** - X5R, X7R, C0G, etc.

## Applicable Types

```java
ComponentType.CAPACITOR
ComponentType.CAPACITOR_CERAMIC_MURATA
ComponentType.CAPACITOR_CERAMIC_TDK
ComponentType.CAPACITOR_CERAMIC_SAMSUNG
ComponentType.CAPACITOR_CERAMIC_YAGEO
ComponentType.CAPACITOR_ELECTROLYTIC_NICHICON
// Any type starting with "CAPACITOR_"
```

Returns `false` for `null` type.

## Similarity Scoring

| Condition | Score |
|-----------|-------|
| Same value, same package, same voltage | ~0.8+ |
| Same value, different package | ~0.5-0.7 |
| Same package, different value | ~0.3 |
| Different everything | ~0.0-0.3 |

## Capacitance Value Extraction

| MPN Pattern | Value |
|-------------|-------|
| `104` in MPN | 100nF (10×10⁴ pF) |
| `103` in MPN | 10nF (10×10³ pF) |
| `100N` | 100nF |
| `10U` | 10µF |

## Common Manufacturers & Patterns

### Murata GRM Series
```
GRM 188 R 71 H 104 K A01 D
│   │   │  │  │ │   │ │   │
│   │   │  │  │ │   │ │   └── Packaging
│   │   │  │  │ │   │ └────── Termination
│   │   │  │  │ │   └──────── Tolerance (K=10%)
│   │   │  │  │ └──────────── Value (104=100nF)
│   │   │  │  └────────────── Voltage (H=50V)
│   │   │  └───────────────── Dielectric (71=X7R)
│   │   └──────────────────── Thickness
│   └──────────────────────── Size (188=0603)
└──────────────────────────── Series
```

### Samsung CL Series
```
CL 10 B 104 K B8 NNNC
│  │  │ │   │ │  │
│  │  │ │   │ │  └── Packaging
│  │  │ │   │ └───── Voltage (B8=25V)
│  │  │ │   └─────── Tolerance (K=10%)
│  │  │ └─────────── Value (104=100nF)
│  │  └────────────── Dielectric (B=X7R)
│  └───────────────── Size (10=0603)
└──────────────────── Series
```

### Yageo CC Series
```
CC 0603 KRX 7R 9 BB 104
│  │    │   │  │ │  │
│  │    │   │  │ │  └── Value (104=100nF)
│  │    │   │  │ └───── Voltage (BB=50V)
│  │    │   │  └─────── TCC code
│  │    │   └────────── Dielectric (7R=X7R)
│  │    └──────────────  Tolerance (K=10%)
│  └───────────────────  Size (0603)
└──────────────────────  Series
```

## Cross-Manufacturer Matching

```java
// Murata vs Samsung same value/size
calculator.calculateSimilarity("GRM188R71H104KA01D", "CL10B104KB8NNNC", registry);
// Returns >= 0.5 (both 100nF, 0603)
```

## Dielectric Types

| Type | Characteristics | Temp Range |
|------|-----------------|------------|
| C0G/NP0 | Stable, low loss | -55 to +125°C |
| X5R | Higher capacity | -55 to +85°C |
| X7R | General purpose | -55 to +125°C |
| Y5V | High capacity, variable | -30 to +85°C |

## Test Examples

```java
// Same Murata capacitor
calculator.calculateSimilarity("GRM188R71H104KA01D", "GRM188R71H104KA01D", registry);
// Returns ~0.8

// Same value, different package
calculator.calculateSimilarity("GRM188R71H104KA01D", "GRM21BR71H104KA01D", registry);
// Returns ~0.5-0.7

// Different values
calculator.calculateSimilarity("GRM188R71H104KA01D", "GRM188R71H103KA01D", registry);
// Returns ~0.3 (100nF vs 10nF)

// Cross-manufacturer
calculator.calculateSimilarity("GRM188R71H104KA01D", "CL10B104KB8NNNC", registry);
// Returns >= 0.5
```

---

## Learnings & Quirks

### Value Notation
- E-series notation: `104` = 10×10⁴ pF = 100nF
- Last digit is multiplier (power of 10)
- `473` = 47×10³ pF = 47nF

### Package Size Mapping
| Imperial | Metric | Murata Code |
|----------|--------|-------------|
| 0402 | 1005 | 155 |
| 0603 | 1608 | 188 |
| 0805 | 2012 | 21 |
| 1206 | 3216 | 31 |

### Voltage Code Variations
- Different manufacturers use different voltage codes
- Murata: H=50V, Samsung: B8=25V
- Always verify voltage compatibility

### Dielectric Compatibility
- X7R and X5R are often interchangeable for general use
- C0G is preferred for precision applications

### Unicode Gotcha: Micro Sign (Milestone 2, January 2026)
**Critical Bug**: The micro sign µ (U+00B5) becomes Greek capital MU Μ (U+039C) when uppercased:
```java
"0.1µF".toUpperCase() // Returns "0.1ΜF" NOT "0.1µF"!
```

**Impact**: If parseCapacitanceValue() uses toUpperCase() before checking for "µF", the check fails silently, returning null. This causes capacitance comparison to be skipped, reducing similarity from ~1.0 to ~0.33 (package match only).

**Solution**: Replace µ→u and Μ→u before normalizing:
```java
String normalized = value.replace("µ", "u").replace("Μ", "u");
normalized = normalizeValue(normalized); // Now safe to toUpperCase
if (normalized.contains("UF")) { // Matches both µF and plain UF
```

**Lesson**: Always handle Greek-origin SI prefixes (µ, Ω) carefully in string normalization logic.

<!-- Add new learnings above this line -->
