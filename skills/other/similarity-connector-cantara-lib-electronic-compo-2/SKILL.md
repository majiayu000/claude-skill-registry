---
name: similarity-connector
description: Use when working with connector similarity calculations - comparing connector MPNs, understanding pin count/pitch/family matching, or connector-specific similarity logic.
---

# Connector Similarity Calculator Skill

Guidance for working with `ConnectorSimilarityCalculator` in the lib-electronic-components library.

---

**For metadata-driven similarity architecture**, see `/similarity-metadata`:
- SpecImportance levels (CRITICAL, HIGH, MEDIUM, LOW, OPTIONAL)
- ToleranceRule types (exactMatch, percentageTolerance, minimumRequired, etc.)
- SimilarityProfile contexts (DESIGN_PHASE, REPLACEMENT, COST_OPTIMIZATION, etc.)
- Calculator integration patterns and gotchas

---

## Overview

The `ConnectorSimilarityCalculator` compares connectors based on:
- **Family** - Connector type/series (must match)
- **Pin count** - Number of contacts (must match for high similarity)
- **Pitch** - Contact spacing
- **Mounting type** - Through-hole vs SMD
- **Series compatibility** - Within TE, Molex, etc.

## Applicable Types

```java
ComponentType.CONNECTOR
ComponentType.CONNECTOR_MOLEX
ComponentType.CONNECTOR_TE
ComponentType.CONNECTOR_JST
ComponentType.CONNECTOR_HIROSE
ComponentType.CONNECTOR_AMPHENOL
ComponentType.CONNECTOR_HARWIN
// Any type starting with "CONNECTOR_"
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Same series, same pin count
MEDIUM_SIMILARITY = 0.5; // Compatible but different
LOW_SIMILARITY = 0.3;    // Different pin counts
```

## Key Rules

### Family Must Match
Different connector families always return 0.0:

```java
// Different families = incompatible
calculator.calculateSimilarity("TE-connector", "Molex-connector", registry);
// Returns 0.0
```

### Pin Count Rules
```java
// Same pin count required for high similarity
calculator.calculateSimilarity("10-pin", "10-pin-variant", registry);
// Returns HIGH

// Different pin counts = LOW
calculator.calculateSimilarity("10-pin", "20-pin", registry);
// Returns 0.3
```

## TE Connectivity Connectors

### Part Number Format
```
1-292161-0
│ │      │
│ │      └── Configuration/variant
│ └─────────  Series number
└───────────  Prefix
```

```java
// Same TE series
calculator.calculateSimilarity("1-292161-0", "1-292161-2", registry);
// Returns 0.9 (same series)
```

## Würth Headers (WR-PHD)

```java
// Compatible header variants
calculator.calculateSimilarity("61300411121", "61300411021", registry);
// Returns 0.9 if same pin count
```

## Similarity Building Blocks

When connectors aren't direct variants, similarity is built from:
- **Same pin count**: +0.2
- **Same pitch**: +0.2
- **Same mounting type**: +0.1

```java
// Compatible characteristics
// Same pin count (+0.2) + Same pitch (+0.2) + Same mount (+0.1) = 0.5
```

## Connector Handlers

The calculator uses specialized handlers:
- `TEConnectorHandler`
- `MolexConnectorHandler`
- `JSTConnectorHandler`
- etc.

These extract:
- `getPinCount(mpn)` - Number of contacts
- `getPitch(mpn)` - Contact spacing (mm)
- `getMountingType(mpn)` - THT/SMD
- `getFamily()` - Connector family name
- `getVariant(mpn)` - Specific variant
- `areCompatible(mpn1, mpn2)` - Direct compatibility check

## Test Examples

```java
// Same TE connector
calculator.calculateSimilarity("1-292161-0", "1-292161-0", registry);
// Returns 1.0

// Same TE series, different variant
calculator.calculateSimilarity("1-292161-0", "1-292161-2", registry);
// Returns 0.9

// Different families
calculator.calculateSimilarity("TE-part", "Molex-part", registry);
// Returns 0.0

// Null handling
calculator.calculateSimilarity(null, "1-292161-0", registry);
// Returns 0.0
```

---

## Learnings & Quirks

### TE Part Numbers
- Format often: `X-XXXXXX-X` or `XXXXXXXX`
- Series number is key to compatibility
- Last digits often indicate configuration

### Molex Part Numbers
- Often 10+ digits
- Series embedded in part number
- Configuration codes vary by series

## Metadata-Driven Implementation (January 2026)

**Status**: ✅ Converted (pre-existing)

The `ConnectorSimilarityCalculator` uses a **metadata-driven approach** with `ConnectorHandler` integration.

### Specs Compared

| Spec | Importance | Tolerance Rule | Description |
|------|-----------|----------------|-------------|
| **pinCount** | CRITICAL | exactMatch | Number of pins (MUST match) |
| **pitch** | CRITICAL | exactMatch | Pin spacing (2.54mm, 1.27mm, etc.) |
| **family** | HIGH | exactMatch | Connector series/family |
| **mountingType** | HIGH | exactMatch | THT, SMD, Press-fit |

### Implementation Pattern

```java
// Different families return 0.0 immediately
if (!handler1.getFamily().equals(handler2.getFamily())) {
    return 0.0;
}

// Extract specs using ConnectorHandler
int pinCount1 = handler1.getPinCount(mpn1);
int pinCount2 = handler2.getPinCount(mpn2);
double pitch1 = handler1.getPitch(mpn1);
double pitch2 = handler2.getPitch(mpn2);

// Weighted spec scoring
// pinCount: CRITICAL (1.0 weight)
// pitch: CRITICAL (1.0 weight)
// family: HIGH (0.7 weight)
// mountingType: HIGH (0.7 weight)
```

### Key Feature: Handler-Based Extraction

Unlike other calculators that use regex patterns, `ConnectorSimilarityCalculator` uses `ConnectorHandler` implementations for accurate spec extraction.

**Why more accurate**: Connectors have complex MPN formats that vary by manufacturer. Using handlers ensures correct extraction of pin count and pitch.

---

### Pin Count Extraction
- Critical for compatibility
- Different manufacturers encode differently
- Some require handler-specific logic

### Pitch Variations
- 2.54mm (0.1") - Standard through-hole
- 2.00mm - Common header pitch
- 1.27mm (0.05") - Fine pitch
- 0.5mm - FPC connectors

### Mounting Types
- THT (Through-Hole Technology)
- SMT/SMD (Surface Mount)
- Press-fit
- Wire-to-board

<!-- Add new learnings above this line -->
