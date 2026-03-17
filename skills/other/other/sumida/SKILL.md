---
name: sumida
description: Sumida Corporation MPN encoding patterns, inductance value decoding, and handler guidance. Use when working with Sumida inductors, transformers, or common mode chokes.
---

# Sumida Corporation Manufacturer Skill

## Overview

Sumida Corporation is a leading manufacturer of magnetic components, specializing in:
- **Power Inductors** - SMD and through-hole designs for DC-DC converters
- **Drum Core Inductors** - High current applications
- **Shielded Inductors** - EMI-sensitive designs
- **Chip Inductors** - Compact surface mount applications
- **Common Mode Chokes** - EMI/EMC filtering
- **Edge-Wound Inductors** - High frequency applications

## MPN Structure

Sumida MPNs follow this general structure:

```
[SERIES][SIZE][SUFFIX]-[VALUE][TOLERANCE][TERMINATION]
   |      |      |        |       |          |
   |      |      |        |       |          +-- Termination code (NC, MC, etc.)
   |      |      |        |       +-- Tolerance: M=+/-20%, N=+/-30%, J=+/-5%
   |      |      |        +-- Inductance value (R-notation: 4R7 = 4.7uH)
   |      |      +-- Optional suffix (NP=Non-magnetic, etc.)
   |      +-- Size code (series-dependent encoding)
   +-- Series prefix (CDRH, CDR, CDEP, CR, CLF, etc.)
```

### Example Decoding

```
CDRH6D28NP-4R7NC
|   |  | |  |  |
|   |  | |  |  +-- NC = Non-magnetic terminals
|   |  | |  +-- 4R7 = 4.7uH inductance (R = decimal)
|   |  | +-- NP = Non-magnetic core/shield
|   |  +-- 28 = 2.8mm height
|   +-- 6D = 6mm x 6mm footprint
+-- CDRH = SMD Power Inductor series

CDR125NP-100MC
|  |  | |  |
|  |  | |  +-- MC = Magnetic terminals
|  |  | +-- 100 = 10uH (EIA code: 10 x 10^0)
|  |  +-- NP = Non-magnetic
|  +-- 125 = 12.5mm diameter drum
+-- CDR = Drum Core Inductor series
```

---

## Product Series

### SMD Power Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| CDRH | SMD Power | Standard SMD power inductor | DC-DC converters |
| CDEP | Shielded SMD | Shielded power inductor | EMI-sensitive designs |
| CDEF | High Efficiency | Low DCR, high efficiency | High-efficiency PSUs |
| CLF | Low Profile | Thin power inductor | Height-constrained designs |

### Drum Core Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| CDR | Drum Core | High current drum inductor | High current applications |
| RCH | High Current | Very high saturation current | Power supplies |
| CEP | Edge-Wound | Edge-wound construction | High frequency |

### Chip Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| CR | Chip Inductor | Multilayer chip inductor | General SMD circuits |

### EMI Components

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| CDC | Common Mode Choke | EMI suppression | Power line filtering |

---

## Inductance Value Code

Sumida uses two notation systems for inductance values:

### R-Notation (Primary)

The "R" character represents the decimal point:

| Code | Calculation | Value |
|------|-------------|-------|
| R47 | 0.47 | 0.47 uH |
| 1R5 | 1.5 | 1.5 uH |
| 4R7 | 4.7 | 4.7 uH |
| 10R | 10.0 | 10 uH |
| 22R | 22.0 | 22 uH |
| 47R | 47.0 | 47 uH |

### EIA 3-Digit Code

Standard EIA multiplier format (first two digits x 10^third digit):

| Code | Calculation | Value |
|------|-------------|-------|
| 100 | 10 x 10^0 | 10 uH |
| 220 | 22 x 10^0 | 22 uH |
| 470 | 47 x 10^0 | 47 uH |
| 101 | 10 x 10^1 | 100 uH |
| 221 | 22 x 10^1 | 220 uH |
| 102 | 10 x 10^2 | 1000 uH = 1 mH |

---

## Tolerance Codes

| Code | Tolerance |
|------|-----------|
| J | +/- 5% |
| K | +/- 10% |
| M | +/- 20% |
| N | +/- 30% |

---

## Termination Codes

| Code | Description |
|------|-------------|
| NC | Non-magnetic terminals (tin-plated) |
| MC | Magnetic terminals |
| C | Standard terminals |

---

## Size Code Reference by Series

### CDRH Series Size Codes

CDRH uses format `[L]D[H]` where L=length/width, D=delimiter, H=height:

| Code | Dimensions (L x W x H) | Notes |
|------|------------------------|-------|
| 4D28 | 4.0mm x 4.0mm x 2.8mm | Compact |
| 6D28 | 6.0mm x 6.0mm x 2.8mm | Standard |
| 8D43 | 8.0mm x 8.0mm x 4.3mm | Higher current |
| 10D43 | 10.0mm x 10.0mm x 4.3mm | High current |
| 12D58 | 12.0mm x 12.0mm x 5.8mm | Very high current |

Height decoding: `28` = 2.8mm, `43` = 4.3mm, `58` = 5.8mm

### CDR Series Size Codes

CDR uses diameter encoding:

| Code | Diameter | Notes |
|------|----------|-------|
| 74 | 7.4mm | Standard |
| 104 | 10.4mm | Higher current |
| 125 | 12.5mm | High current |
| 127 | 12.7mm | Alternative 12.5mm |

### CDEP Series Size Codes

CDEP uses format `[WW][H]` where WW=width, H=height:

| Code | Dimensions (L x W x H) | Notes |
|------|------------------------|-------|
| 104 | 10.0mm x 10.0mm x 4.0mm | Standard |
| 105 | 10.0mm x 10.0mm x 5.0mm | Taller version |
| 126 | 12.0mm x 12.0mm x 6.0mm | Large footprint |

### CR Series Size Codes

CR chip inductors use millimeter encoding:

| Code | Size | EIA Equivalent |
|------|------|----------------|
| 16 | 1.6mm x 0.8mm | 0603 |
| 21 | 2.1mm x 1.2mm | 0805 |
| 32 | 3.2mm x 1.6mm | 1206 |

### CLF Series Size Codes

CLF uses format `[LL][WW][H]` (5 digits):

| Code | Dimensions (L x W x H) | Notes |
|------|------------------------|-------|
| 10040 | 10.0mm x 10.0mm x 4.0mm | Standard low profile |
| 12060 | 12.0mm x 12.0mm x 6.0mm | Large low profile |

---

## Package Code Extraction

The handler extracts and decodes size codes to human-readable dimensions:

| MPN | Extracted Package |
|-----|-------------------|
| CDRH6D28NP-4R7NC | 6x6x2.8mm |
| CDRH4D28NP-1R5NC | 4x4x2.8mm |
| CDRH8D43NP-100MC | 8x8x4.3mm |
| CDR74NP-100MC | 7.4mm |
| CDR125NP-220MC | 12.5mm |
| CDEP104NP-1R5MC | 10x10x4mm |
| CDEP105NP-4R7MC | 10x10x5mm |
| CR21-100JM | 2.1mm |
| CLF10040-470MC | 10x10x4.0mm |

---

## Series Extraction

The handler extracts the series prefix (without size code):

| MPN | Extracted Series |
|-----|------------------|
| CDRH6D28NP-4R7NC | CDRH |
| CDRH4D28NP-1R5NC | CDRH |
| CDR125NP-100MC | CDR |
| CDEP104NP-1R5MC | CDEP |
| CDEF38NP-100MC | CDEF |
| CR21-100JM | CR |
| RCH110NP-1R0MC | RCH |
| CEP105NP-4R7MC | CEP |
| CDC2G2NP-100MC | CDC |
| CLF10040-470MC | CLF |

### Series Extraction Order (Important)

Due to prefix overlap, series must be checked in this order:
1. `CDRH` (before CDR)
2. `CDEP` (before CDE)
3. `CDEF` (before CDE)
4. `CDC`
5. `CDR` (generic CD prefix)
6. `CLF`
7. `CR`
8. `RCH`
9. `CEP`

---

## Supported Component Types

The SumidaHandler supports:
- `ComponentType.INDUCTOR` - Base inductor type

Note: Sumida does not have a manufacturer-specific inductor type (e.g., `INDUCTOR_SUMIDA`) in this codebase.

---

## Example MPNs with Full Decoding

### CDRH6D28NP-4R7NC

```
Series:      CDRH (SMD Power Inductor)
Size:        6D28 (6.0mm x 6.0mm x 2.8mm)
Suffix:      NP = Non-magnetic core
Inductance:  4R7 = 4.7 uH
Tolerance:   N = +/- 30%
Termination: C = Standard

Full Series: CDRH
Package:     6x6x2.8mm
```

### CDR125NP-100MC

```
Series:      CDR (Drum Core Inductor)
Size:        125 (12.5mm diameter)
Suffix:      NP = Non-magnetic core
Inductance:  100 = 10 x 10^0 = 10 uH
Tolerance:   M = +/- 20%
Termination: C = Standard

Full Series: CDR
Package:     12.5mm
```

### CDEP104NP-1R5MC

```
Series:      CDEP (Shielded SMD Power Inductor)
Size:        104 (10.0mm x 10.0mm x 4.0mm)
Suffix:      NP = Non-magnetic core
Inductance:  1R5 = 1.5 uH
Tolerance:   M = +/- 20%
Termination: C = Standard

Full Series: CDEP
Package:     10x10x4mm
```

### CR21-100JM

```
Series:      CR (Chip Inductor)
Size:        21 (2.1mm x 1.2mm, ~0805)
Inductance:  100 = 10 uH
Tolerance:   J = +/- 5%
Suffix:      M = (variant)

Full Series: CR
Package:     2.1mm
```

### CLF10040-470MC

```
Series:      CLF (Low Profile Power Inductor)
Size:        10040 (10.0mm x 10.0mm x 4.0mm)
Inductance:  470 = 47 x 10^0 = 47 uH
Tolerance:   M = +/- 20%
Termination: C = Standard

Full Series: CLF
Package:     10x10x4.0mm
```

### CDC2G2NP-100MC

```
Series:      CDC (Common Mode Choke)
Size:        2G2 (variant designation)
Suffix:      NP = Non-magnetic core
Inductance:  100 = 10 uH
Tolerance:   M = +/- 20%
Termination: C = Standard

Full Series: CDC
Package:     2G2
```

---

## Handler Implementation Notes

### Pattern Matching

```java
// Sumida patterns have series-specific structures:
// CDRH series: CDRH + size code (nDnn format) + optional suffix + hyphen + value
"^CDRH[0-9]+[A-Z]?[0-9]*[A-Z]*-?[0-9R]+[A-Z]*$"

// CDR drum core: CDR + size code (2-3 digits) + optional suffix + hyphen + value
"^CDR[0-9]+[A-Z]*-?[0-9R]+[A-Z]*$"

// CR chip: CR + size (2 digits) + hyphen + value
"^CR[0-9]+[A-Z]*-?[0-9R]+[A-Z]*$"

// Combined pattern for quick Sumida detection:
"^(CDRH|CDR|CDEP|CDEF|CR|RCH|CEP|CDC|CLF)[0-9A-Z]+-?[0-9R]*[A-Z]*$"
```

### Inductance Value Extraction

The handler includes `extractInductanceValue()` method that:
1. Finds the value portion after the hyphen
2. Parses R-notation (4R7 = 4.7uH, R47 = 0.47uH, 10R = 10uH)
3. Parses EIA 3-digit code (100 = 10uH, 101 = 100uH)
4. Returns formatted string (e.g., "4.7uH", "10uH")

### Official Replacement Check

Two Sumida parts are considered official replacements if:
1. Same series (e.g., both CDRH)
2. Same inductance value (e.g., both 4.7uH)

Different size codes, tolerances, or termination options are NOT automatic replacements because they affect electrical performance and footprint compatibility.

### Utility Methods

The handler provides additional helper methods:

```java
// Check if MPN is a Sumida inductor
boolean isSumidaInductor(String mpn)

// Get human-readable inductor type description
String getInductorTypeDescription(String mpn)
// Returns: "SMD Power Inductor", "Drum Core Inductor", etc.
```

---

## Related Files

- Handler: `manufacturers/SumidaHandler.java`
- Component types: `ComponentType.INDUCTOR`
- Tests: Check for `SumidaHandlerTest.java` in handlers package

---

## Learnings & Edge Cases

- **Hyphen is optional**: MPNs may appear as `CDRH6D28NP-4R7NC` or `CDRH6D28NP4R7NC`
- **R-notation ambiguity**: `10R` means 10uH (R as terminator), but `1R0` also means 1.0uH (R as decimal)
- **NP suffix common**: Most Sumida inductors use NP (non-magnetic) suffix before the value separator
- **CDC series alphanumeric**: CDC series uses alphanumeric size codes (e.g., CDC2G2) unlike numeric-only codes in other series
- **CDRH vs CDR prefix**: CDRH is the SMD variant, CDR is drum core - pattern matching must check CDRH first to avoid false CDR match
- **Series check order matters**: Due to prefix overlaps (CDRH/CDR, CDEP/CDEF/CDC), check longer prefixes before shorter ones
- **Height encoding varies**: CDRH uses 2-digit encoding (28=2.8mm), CDEP uses 1-digit (4=4mm), CLF uses 2-digit different format
- **getSupportedTypes() uses Set.of()**: Handler correctly uses immutable Set.of() pattern (not HashSet)
- **No manufacturer-specific type**: Unlike some handlers, Sumida only uses base `INDUCTOR` type, not `INDUCTOR_SUMIDA`

### Common MPN Variants

```
CDRH6D28NP-4R7NC   - Standard shielded SMD
CDRH6D28NP-4R7MC   - Magnetic terminals
CDRH6D28-4R7NC    - No NP suffix
CDRH6D284R7NC     - No hyphen separator
```

### Size Code Decoding Edge Cases

The size code decoding assumes specific formats:
- CDRH: `[L]D[HH]` - Letter D is always delimiter, not "10" like "10D43"
- CDR: Pure numeric diameter
- CDEP: `[WW][H]` - First 2 digits are width, last is height
- CLF: `[LL][WW][H]` - Format may vary for different sizes

When decoding produces unexpected results, verify against datasheet.

<!-- Add new learnings above this line -->
