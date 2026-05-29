---
name: similarity-led
description: Use when working with LED similarity calculations - comparing LED MPNs, understanding color bins, brightness bins, families, or LED-specific similarity logic.
---

# LED Similarity Calculator Skill

Guidance for working with `LEDSimilarityCalculator` in the lib-electronic-components library.

## Overview

The `LEDSimilarityCalculator` compares LEDs based on:
- **LED family** - Same manufacturer series
- **Bin codes** - Brightness and color temperature bins
- **Color temperature** - Must match for high similarity

## Applicable Types

```java
ComponentType.LED
// Any type starting with "LED_"
// Uses getBaseType() == ComponentType.LED
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Same LED, same color temp
MEDIUM_SIMILARITY = 0.7; // Different families but valid LEDs
LOW_SIMILARITY = 0.3;    // Different color temperatures
```

## LED Equivalent Groups

### TI High-Power LED Series
| Group | Members |
|-------|---------|
| TLHR5400 (Red) | TLHR5400, TLHR5401, TLHR5402, TLHR5403 |
| TLHG5800 (Green) | TLHG5800, TLHG5801, TLHG5802, TLHG5803 |
| TLHB5800 (Blue) | TLHB5800, TLHB5801, TLHB5802, TLHB5803 |

### LG LED Series
| Group | Members |
|-------|---------|
| LG R971 (Red) | LG R971, LG R971-KN, LG R971-PK |
| LG B971 (Blue) | LG B971, LG B971-KN, LG B971-PK |
| LG G971 (Green) | LG G971, LG G971-KN, LG G971-PK |

### Samsung LM Series
| Group | Members |
|-------|---------|
| LM301B | LM301B, LM301B-K, LM301B-V2 |
| LM281B | LM281B, LM281B-K, LM281B-V2 |

### Nichia NCS Series
| Group | Members |
|-------|---------|
| NCSW (White) | NCSW170, NCSW170T, NCSW170AT |
| NCSR (Red) | NCSR170, NCSR170T, NCSR170AT |

## Bin Code Handling

LEDs use bin codes for brightness and color sorting:

### Brightness Bins (Typical)
- `K`, `L`, `M`, `N` - Brightness grades

### Color Temperature Bins (Cree)
- `FK*` - One color temperature
- `FC*` - Different color temperature

```java
// Same color temperature = HIGH
calculator.calculateSimilarity("XPERED-L1-FKA", "XPERED-L1-FKB", registry);
// Returns 0.9

// Different color temperatures = LOW
calculator.calculateSimilarity("XPERED-L1-FKA", "XPERED-L1-FCA", registry);
// Returns 0.3
```

## Family Detection

| Prefix | Manufacturer | Family |
|--------|--------------|--------|
| TLHR | TI | Red LED |
| TLHG | TI | Green LED |
| TLHB | TI | Blue LED |
| TLW | TI | White LED |
| LG R/B/G | LG | Color LEDs |
| LW, LR, LS | Osram | Standard LEDs |
| XP, XB, XQ | Cree | High-power LEDs |
| L130, L135 | Lumileds | LUXEON series |
| LM | Samsung | LM series |
| NCS | Nichia | Standard series |

## Package Compatibility

| Package Type | Compatible Packages |
|--------------|---------------------|
| SMD | SMD, PLCC, 3528, 5050, 2835, 3030, 5630, 0603, 0805, 1206 |
| Through-Hole | TH, DIP, 5MM, 3MM, 8MM, 10MM, T-1, T-1¾ |
| High-Power | STAR, MCE, XPE, XPG, XML, LUXEON, REBEL |

## Test Examples

```java
// Same LED
calculator.calculateSimilarity("TLHR5400", "TLHR5400", registry);
// Returns 0.9

// Same family, different bin
calculator.calculateSimilarity("TLHR5400", "TLHR5401", registry);
// Returns 0.9

// LG variants with suffix
calculator.calculateSimilarity("LG R971", "LG R971-KN", registry);
// Returns 0.9

// Different color temps
calculator.calculateSimilarity("XPERED-L1-FKA", "XPERED-L1-FCA", registry);
// Returns 0.3
```

---

## Metadata-Driven Implementation (January 2026)

**Status**: ✅ Converted (PR #118)

The `LEDSimilarityCalculator` now uses a **metadata-driven approach** with spec-based comparison.

### Specs Compared

| Spec | Importance | Tolerance Rule | Description |
|------|-----------|----------------|-------------|
| **color** | CRITICAL | exactMatch | Red, Green, Blue, White, etc. |
| **family** | HIGH | exactMatch | TLHR, LG R, LM301, XP-E, etc. |
| **brightness** | HIGH | exactMatch | Brightness bin code |
| **package** | LOW | exactMatch | 0603, 0805, 5mm, SMD, etc. |

### Implementation Pattern

```java
// Short-circuit check for CRITICAL incompatibility
if (!color1.isEmpty() && !color2.isEmpty() && !color1.equals(color2)) {
    return LOW_SIMILARITY;
}

// Weighted spec scoring
// color: CRITICAL (1.0 weight)
// family: HIGH (0.7 weight)
// brightness: HIGH (0.7 weight)
// package: LOW (0.2 weight)

// Family boost for known equivalent groups
if (areSameFamily(mpn1, mpn2)) {
    similarity = Math.max(similarity, HIGH_SIMILARITY);
}
```

### Behavior Changes

| Comparison | Legacy Result | Metadata Result | Notes |
|-----------|--------------|-----------------|-------|
| TLHR5400 vs TLHR5401 | 0.9 | 0.96 | Same family, different bins |
| LG R971 vs LG R971-KN | 0.9 | 1.0 | Exact family + color match |
| TLHR5400 vs LCW E6SF | 0.7 | 0.66 | Different families, same color |
| XPERED-L1-FKA vs XPERED-L1-FCA | 0.3 | 0.3 | Short-circuit on color temp |

**Why more accurate**: Metadata approach prioritizes color matching (CRITICAL) and separates family from brightness considerations.

---

## Learnings & Quirks

### Color Temperature Codes
- Cree uses `FK`/`FC` in bin codes to indicate color temp
- Same base LED with different color temps are NOT equivalent

### Brightness Bin Codes
- Adjacent brightness bins (K vs L) are usually interchangeable
- Large gaps in brightness bins may not be suitable substitutes

### LG LED Format
- Format: `LG R971-KN` where `-KN` is the suffix variant
- All suffix variants of same base part are equivalent

### Package Suffixes
- `-RL`, `-RT` = Tape and reel packaging
- `-TUBE` = Tube packaging
- These don't affect LED equivalence

<!-- Add new learnings above this line -->
