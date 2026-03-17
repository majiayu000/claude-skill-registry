---
name: similarity-logic
description: Use when working with logic IC similarity calculations - comparing 74xx series, CD4000 CMOS, technology families (LS, HC, HCT), function groups (NAND, NOR, flip-flops), or logic IC-specific similarity logic.
---

# Logic IC Similarity Calculator Skill

Guidance for working with `LogicICSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `LogicICSimilarityCalculator` compares logic ICs based on:
- **Logic function** - NAND, NOR, NOT, AND, OR, flip-flops, etc.
- **Technology family** - LS, ALS, HC, HCT, F, etc.
- **Part number series** - 74xx vs CD4000

## Applicable Types

```java
ComponentType.LOGIC_IC
ComponentType.LOGIC_IC_NEXPERIA
ComponentType.LOGIC_IC_DIODES
ComponentType.IC  // Generic IC type also supported
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Same function, compatible technology
MEDIUM_SIMILARITY = 0.5; // Related parts
LOW_SIMILARITY = 0.3;    // Different functions
```

## 74xx Series

### Technology Families (Interchangeable within groups)
| Family | Speed | Power | Compatible With |
|--------|-------|-------|-----------------|
| LS | Fast | Low | ALS, F, HC, HCT |
| ALS | Faster | Lower | LS, F, HC, HCT |
| F | Fast | Medium | LS, ALS, HC, HCT |
| HC | Fast | Very Low | LS, ALS, F, HCT |
| HCT | Fast | Very Low | LS, ALS, F, HC |

```java
// Compatible technologies = HIGH
calculator.calculateSimilarity("74LS00", "74HC00", registry);
// Returns 0.9

calculator.calculateSimilarity("74LS04", "74ALS04", registry);
// Returns 0.9
```

### Function Groups
| Function | Part Numbers |
|----------|--------------|
| NAND Gates | 00, 10, 20, 30, 40 |
| NOR Gates | 02, 12, 22, 32, 42 |
| Inverters | 04, 14, 24, 34, 44 |
| AND Gates | 08, 18, 28, 38, 48 |
| OR Gates | 32, 42 |
| Flip-Flops | 73, 74, 75, 76, 77, 78 |
| Multiplexers | 151, 153, 157, 158 |
| Decoders | 138, 139, 154, 155 |

```java
// Different functions = LOW
calculator.calculateSimilarity("74LS00", "74LS74", registry);
// Returns 0.3 (NAND vs Flip-Flop)
```

## CD4000 CMOS Series

### Common CD4000 Parts
| Part | Function |
|------|----------|
| CD4001 | Quad 2-input NOR |
| CD4011 | Quad 2-input NAND |
| CD4013 | Dual D flip-flop |
| CD4017 | Decade counter |
| CD4040 | 12-bit binary counter |
| CD4051 | 8-channel mux |
| CD4066 | Quad bilateral switch |

### CD4000 Package Codes
| Suffix | Package |
|--------|---------|
| BE | PDIP (plastic) |
| BM | SOIC |
| UBE | Unbuffered PDIP |
| N, P | DIP variants |
| DG, PW, DR | SMD variants |

```java
// Same CD4000 IC, different package = HIGH
calculator.calculateSimilarity("CD4001BE", "CD4001BM", registry);
// Returns 0.9

// Different CD4000 ICs = LOW
calculator.calculateSimilarity("CD4001BE", "CD4011BE", registry);
// Returns 0.3
```

## Cross-Series Comparison

74xx and CD4000 are generally not interchangeable:

```java
// 74xx vs CD4000 with same function
calculator.calculateSimilarity("74HC00", "CD4011BE", registry);
// Returns LOW (different series, even if same function)
```

## Test Examples

```java
// Same 74xx, compatible technologies
calculator.calculateSimilarity("74LS00", "74HC00", registry);
// Returns 0.9

// Same CD4000 IC, different package
calculator.calculateSimilarity("CD4001BE", "CD4001BM", registry);
// Returns 0.9

// Same function group in 74xx
calculator.calculateSimilarity("74LS04", "74ALS04", registry);
// Returns 0.9

// Different functions
calculator.calculateSimilarity("74LS00", "74LS74", registry);
// Returns 0.3
```

---

## Learnings & Quirks

### 74xx Part Number Structure
```
74 LS 04 N
│  │  │  │
│  │  │  └── Package (N=DIP)
│  │  └───── Function (04=Inverter)
│  └──────── Technology (LS=Low-power Schottky)
└─────────── Series prefix
```

### CD4000 Part Number Structure
```
CD 4001 BE
│  │    │
│  │    └── Package (BE=Plastic DIP)
│  └─────── Function number
└────────── Series prefix
```

## Metadata-Driven Implementation (January 2026)

**Status**: ✅ Converted (PR #119)

The `LogicICSimilarityCalculator` now uses a **metadata-driven approach** with spec-based comparison.

### Specs Compared

| Spec | Importance | Tolerance Rule | Description |
|------|-----------|----------------|-------------|
| **function** | CRITICAL | exactMatch | NAND, NOR, NOT, AND, OR, flip-flop, etc. |
| **series** | HIGH | exactMatch | 74xx vs CD4000 |
| **technology** | MEDIUM | exactMatch | LS, HC, HCT, ALS, F, etc. |
| **package** | LOW | exactMatch | N, D, P, PW, etc. |

### Implementation Pattern

```java
// Short-circuit check for CRITICAL incompatibility
if (!function1.isEmpty() && !function2.isEmpty() && !areSameFunction(mpn1, mpn2)) {
    return LOW_SIMILARITY;
}

// Short-circuit for series incompatibility (74xx vs CD4000)
if (!series1.isEmpty() && !series2.isEmpty() && !series1.equals(series2)) {
    return 0.0;
}

// Extract function from both 74xx and CD4000 series
private String extractFunction(String mpn) {
    if (mpn.matches("^CD4.*")) {
        // CD4001 → "001", CD4011 → "011"
        return cmosPatternMatcher.group(1);
    }
    // 74LS00 → "00", 74HC138 → "138"
    return ttlPatternMatcher.group(3);
}
```

### Behavior Changes

| Comparison | Legacy Result | Metadata Result | Notes |
|-----------|--------------|-----------------|-------|
| 74LS00 vs 74HC00 | 0.9 | 0.88 | Compatible technologies |
| CD4001BE vs CD4001BM | 0.9 | 0.96 | Same IC, different package |
| CD4001 vs CD4011 | 0.3 | 0.3 | Short-circuit on function |
| 74LS00 vs CD4001 | undefined | 0.0 | Short-circuit on series |

**Why more accurate**: Metadata approach correctly handles both 74xx and CD4000 series, with series check preventing false matches.

---

### Technology Compatibility Notes
- HC is CMOS, LS is TTL - but they're voltage compatible at 5V
- HCT is specifically designed for TTL compatibility
- 74LVC series is for 3.3V operation

### Function Group Patterns
- The 2-digit function number after technology code determines function
- Same function number = same function across technologies

<!-- Add new learnings above this line -->
