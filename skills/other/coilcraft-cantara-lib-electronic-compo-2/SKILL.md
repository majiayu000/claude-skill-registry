---
name: coilcraft
description: Coilcraft MPN encoding patterns, inductance value decoding, and handler guidance. Use when working with Coilcraft inductors, transformers, or RF components.
---

# Coilcraft Manufacturer Skill

## Overview

Coilcraft is a leading manufacturer of magnetic components, specializing in:
- **Power Inductors** - Shielded and unshielded designs for DC-DC converters
- **RF Inductors** - High-Q chip inductors for RF/wireless applications
- **Transformers** - Signal and power transformers
- **Common Mode Chokes** - EMI suppression components

## MPN Structure

Coilcraft MPNs follow this general structure:

```
[SERIES][SIZE][-][VALUE][TOLERANCE][PACKAGING]
   |       |     |    |       |         |
   |       |     |    |       |         +-- E=Embossed tape, B=Bulk
   |       |     |    |       +-- M=+/-20%, L=+/-15%, K=+/-10%
   |       |     |    +-- 3-digit inductance code (or Rxx for sub-uH)
   |       |     +-- Optional hyphen separator
   |       +-- 4-digit size code (e.g., 4020 = 4.0mm x 2.0mm)
   +-- Series prefix (XAL, XEL, XFL, SER, LPS, MSS, DO, MSD, SLC, SLR)
```

### Example Decoding

```
XAL4020-222ME
|  |    |  ||
|  |    |  |+-- E = Embossed tape packaging
|  |    |  +-- M = +/-20% tolerance
|  |    +-- 222 = 2.2uH (see value code section)
|  +-- 4020 = 4.0mm x 2.0mm footprint
+-- XAL = Shielded power inductor series

LPS3015-103MLB
|  |    |  |||
|  |    |  ||+-- B = Bulk packaging
|  |    |  |+-- L = +/-15% tolerance
|  |    |  +-- M = +/-20% (sometimes double suffix for different specs)
|  |    +-- 103 = 10uH
|  +-- 3015 = 3.0mm x 1.5mm footprint
+-- LPS = Low Profile Shielded series
```

---

## Product Series

### Power Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| XAL | Shielded Power | High current, low DCR | DC-DC converters |
| XAT | Shielded Power | XAL variant | Point-of-load regulators |
| XEL | Shielded Low DCR | Ultra-low DC resistance | High efficiency supplies |
| XFL | Low Profile | Thin shielded inductors | Height-constrained designs |
| SER | High Efficiency | Optimized for efficiency | High-frequency switching |
| LPS | Low Profile Shielded | Compact shielded | Mobile devices |
| MSS | Magnetically Shielded | Fully shielded | EMI-sensitive applications |

### Drum Core Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| DO | Drum Core | Unshielded, high current | Cost-sensitive designs |
| MSD | Mid-Size Drum | Medium current | General purpose |

### RF/High-Q Inductors

| Series | Type | Description | Typical Use |
|--------|------|-------------|-------------|
| SLC | High-Q Chip | Ceramic chip, high Q | RF matching |
| SLR | High-Q Chip RF | RF-optimized | Wireless applications |
| 0402HP | High Performance | 0402 size, precision | Compact RF circuits |
| 0603HP | High Performance | 0603 size, precision | RF filter circuits |

---

## Inductance Value Code

Coilcraft uses a 3-digit code for inductance values:

### Standard 3-Digit Code

```
[D1][D2][M]
 |   |   |
 |   |   +-- Multiplier (10^M in nanohenries)
 |   +-- Second significant digit
 +-- First significant digit

Value (nH) = D1D2 x 10^M
Value (uH) = (D1D2 x 10^M) / 1000
```

### Decoding Examples

| Code | Calculation | Value |
|------|-------------|-------|
| 100 | 10 x 10^0 nH | 10 nH = 0.01 uH |
| 101 | 10 x 10^1 nH | 100 nH = 0.1 uH |
| 102 | 10 x 10^2 nH | 1000 nH = 1.0 uH |
| 222 | 22 x 10^2 nH | 2200 nH = 2.2 uH |
| 472 | 47 x 10^2 nH | 4700 nH = 4.7 uH |
| 103 | 10 x 10^3 nH | 10000 nH = 10 uH |
| 334 | 33 x 10^4 nH | 330000 nH = 330 uH |

### R-Notation (Sub-Microhenry)

For values less than 1 uH, the "R" notation indicates decimal placement:

| Code | Value |
|------|-------|
| R10 | 0.10 uH |
| R22 | 0.22 uH |
| R33 | 0.33 uH |
| R47 | 0.47 uH |
| R68 | 0.68 uH |

---

## Tolerance Codes

| Code | Tolerance |
|------|-----------|
| K | +/- 10% |
| L | +/- 15% |
| M | +/- 20% |

---

## Packaging Codes

| Code | Description |
|------|-------------|
| E | Embossed tape (pick-and-place ready) |
| B | Bulk packaging |
| R | Tape and reel (sometimes used instead of E) |

---

## Size Code Reference

The 4-digit size code encodes physical dimensions:

```
XXYY
||++-- Height in 0.1mm (YY x 0.1mm)
++---- Length/Width in 0.1mm (XX x 0.1mm)
```

### Common Size Codes

| Code | Dimensions (L x W x H) | Notes |
|------|------------------------|-------|
| 2006 | 2.0mm x 2.0mm x 0.6mm | Ultra-low profile |
| 3012 | 3.0mm x 3.0mm x 1.2mm | Low profile |
| 3015 | 3.0mm x 3.0mm x 1.5mm | Low profile |
| 4018 | 4.0mm x 4.0mm x 1.8mm | Standard |
| 4020 | 4.0mm x 4.0mm x 2.0mm | Standard |
| 4030 | 4.0mm x 4.0mm x 3.0mm | Higher current |
| 5030 | 5.0mm x 5.0mm x 3.0mm | High current |
| 1038 | 10.0mm x 10.0mm x 3.8mm | Large footprint |
| 1048 | 10.0mm x 10.0mm x 4.8mm | Large footprint |

---

## Package Code Extraction

The handler maps series prefixes to package types:

| Series | Extracted Package Type |
|--------|------------------------|
| XAL | Shielded Power |
| XAT | Shielded Power |
| XEL | Shielded Low DCR |
| XFL | Low Profile |
| SER | High Efficiency |
| LPS | Low Profile Shielded |
| MSS | Magnetically Shielded |
| DO | Drum Core |
| MSD | Mid-Size Drum |
| SLC | High Q Chip |
| SLR | High Q Chip RF |
| 0402HP | 0402 High Performance |
| 0603HP | 0603 High Performance |

---

## Series Extraction

The handler extracts series + size code as the full series identifier:

| MPN | Extracted Series |
|-----|------------------|
| XAL4020-222ME | XAL4020 |
| XFL3012-102MEB | XFL3012 |
| LPS4018-473MLB | LPS4018 |
| DO3316P-472 | DO3316P |
| 0402HP-R47 | 0402HP |

### DO Series Special Case

The DO series may include an optional suffix letter before the value code:

```
DO3316P-472
    |  |
    |  +-- P = Variant suffix (C=Standard, P=Power, T=alternate)
    +-- 3316 = Size code
```

---

## Supported Component Types

The CoilcraftHandler supports:
- `ComponentType.INDUCTOR` - Base inductor type
- `ComponentType.INDUCTOR_CHIP_COILCRAFT` - Coilcraft-specific inductor type

---

## Example MPNs with Full Decoding

### XAL4020-222ME

```
Series:      XAL (Shielded Power Inductor)
Size:        4020 (4.0mm x 4.0mm x 2.0mm)
Inductance:  222 = 22 x 10^2 nH = 2.2 uH
Tolerance:   M = +/- 20%
Packaging:   E = Embossed tape

Full Series: XAL4020
Package:     Shielded Power
```

### XEL4030-102MRB

```
Series:      XEL (Shielded Low DCR)
Size:        4030 (4.0mm x 4.0mm x 3.0mm)
Inductance:  102 = 10 x 10^2 nH = 1.0 uH
Tolerance:   M = +/- 20%
Options:     R = Tape, B = (possibly bulk variant)

Full Series: XEL4030
Package:     Shielded Low DCR
```

### LPS3015-103MLB

```
Series:      LPS (Low Profile Shielded)
Size:        3015 (3.0mm x 3.0mm x 1.5mm)
Inductance:  103 = 10 x 10^3 nH = 10 uH
Tolerance:   L = +/- 15%
Packaging:   B = Bulk

Full Series: LPS3015
Package:     Low Profile Shielded
```

### 0402HP-R47KB

```
Series:      0402HP (0402 High Performance)
Inductance:  R47 = 0.47 uH
Tolerance:   K = +/- 10%
Packaging:   B = Bulk

Full Series: 0402HP
Package:     0402 High Performance
```

### DO3316P-472MLB

```
Series:      DO (Drum Core)
Size:        3316 (3.3mm x 3.3mm x 1.6mm)
Variant:     P = Power variant
Inductance:  472 = 47 x 10^2 nH = 4.7 uH
Tolerance:   L = +/- 15%
Packaging:   B = Bulk

Full Series: DO3316P
Package:     Drum Core
```

---

## Handler Implementation Notes

### Pattern Matching

```java
// Coilcraft patterns have consistent structure:
// - 2-3 letter series prefix
// - 4-digit size code
// - Optional hyphen
// - 3-digit value code (or Rxx)
// - Optional tolerance + packaging suffix

// Example pattern for XAL/XEL series:
"^(XA[LT]|XEL)(\\d{4})[-]?(\\d{3}|R\\d{2})([A-Z]*)$"
//  |          |       |    |              |
//  |          |       |    |              +-- Suffix group (tolerance+pkg)
//  |          |       |    +-- Value group (222 or R47)
//  |          |       +-- Optional hyphen
//  |          +-- Size code group (4 digits)
//  +-- Series group
```

### Inductance Value Extraction

The handler includes `extractInductanceValue()` method that:
1. Matches the MPN against series patterns
2. Extracts the 3-digit value code
3. Parses using standard EIA notation or R-notation
4. Returns formatted string (e.g., "2.2uH", "470nH")

### Official Replacement Check

Two Coilcraft parts are considered official replacements if:
1. Same series (including size) - e.g., both XAL4020
2. Same inductance value - e.g., both 2.2uH

Different tolerance or packaging options are compatible replacements.

---

## Related Files

- Handler: `manufacturers/CoilcraftHandler.java`
- Component types: `INDUCTOR`, `INDUCTOR_CHIP_COILCRAFT`
- Tests: Check for `CoilcraftHandlerTest.java` in handlers package

---

## Learnings & Edge Cases

- **Hyphen is optional**: MPNs may appear as `XAL4020-222ME` or `XAL4020222ME`
- **Suffix variations**: Tolerance + packaging may appear in various orders (ME, MEB, MRB)
- **DO series variant suffix**: The C/P/T letter after the size code indicates design variant, not tolerance
- **HP series different structure**: 0402HP and 0603HP don't have a separate size code - the size IS the series prefix
- **R-notation case sensitivity**: While the handler is case-insensitive, R-notation typically appears uppercase
- **Value code group extraction**: For DO pattern, the value code is in group 4 (not group 3) due to the extra variant suffix group
- **Series includes size for uniqueness**: `extractSeries()` returns "XAL4020" not just "XAL" because different sizes have different current ratings

### Pattern Group Numbering

Different series have different regex group structures:

```
XAL/XEL/XFL/SER/LPS/MSS/MSD/SLC/SLR patterns:
  Group 1: Series prefix (XAL)
  Group 2: Size code (4020)
  Group 3: Value code (222)
  Group 4: Suffix (ME)

DO pattern (has extra variant group):
  Group 1: Series prefix (DO)
  Group 2: Size code (3316)
  Group 3: Variant suffix (P)
  Group 4: Value code (472)
  Group 5: Suffix (MLB)

HP pattern (no separate size):
  Group 1: Series+size (0402HP)
  Group 2: Value code (R47)
  Group 3: Suffix (KB)
```

<!-- Add new learnings above this line -->
