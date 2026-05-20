---
name: sunlord
description: Sunlord Electronics inductor and ferrite bead MPN encoding patterns, value decoding, and handler guidance. Use when working with Sunlord inductors or SunlordHandler.
---

# Sunlord Electronics Manufacturer Skill

## MPN Structure

Sunlord MPNs follow this structure:

```
[SERIES][SIZE][TYPE][VALUE][TOLERANCE][OPTIONS]
   |      |     |      |       |         |
   |      |     |      |       |         +-- Packaging/options
   |      |     |      |       +-- M=20%, K=10%, J=5%
   |      |     |      +-- Inductance code (see below)
   |      |     +-- Type/characteristics code
   |      +-- 4-digit metric size code
   +-- Series prefix (SDCL, SWPA, SDFL, GZ)
```

### Example Decoding

```
SDCL1005C1R0MTDF
|   |   ||  ||||
|   |   ||  |||+-- Additional options
|   |   ||  ||+-- Packaging (T=Tape/Reel)
|   |   ||  |+-- Tolerance (M=+/-20%)
|   |   ||  +-- Inductance (1R0 = 1.0uH)
|   |   |+-- Type code (C)
|   |   +-- Size (1005 = 1.0mm x 0.5mm = 0402 imperial)
|   +-- Series
+-- SDCL = Power Inductor

GZ2012D601TF
| |   ||  ||
| |   ||  |+-- Packaging (F)
| |   ||  +-- Tolerance (T)
| |   |+-- Impedance (601 = 600 ohm at 100MHz)
| |   +-- Type code (D)
| +-- Size (2012 = 2.0mm x 1.2mm = 0805 imperial)
+-- GZ = Ferrite Bead
```

---

## Series Reference

### SDCL - Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Power inductor |
| Pattern | `^SDCL[0-9]{4}.*` |
| Value encoding | Inductance in uH |

### SWPA - Shielded Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Power inductor (shielded) |
| Pattern | `^SWPA[0-9]{4}.*` |
| Value encoding | Inductance in uH |
| S prefix in type | Indicates shielded |

### SDFL - Ferrite Chip Inductors

| Feature | Description |
|---------|-------------|
| Type | Ferrite chip inductor |
| Pattern | `^SDFL[0-9]{4}.*` |
| Value encoding | Inductance in uH |

### GZ - Ferrite Beads

| Feature | Description |
|---------|-------------|
| Type | Ferrite bead |
| Pattern | `^GZ[0-9]{4}.*` |
| Value encoding | Impedance at 100MHz in ohms |

---

## Inductance Encoding

Sunlord uses a 3-character inductance code:

### R-Notation (Decimal Point)

| Code | Value | Calculation |
|------|-------|-------------|
| R47 | 0.47uH | 0.47 |
| R10 | 0.10uH | 0.10 |
| 1R0 | 1.0uH | 1.0 |
| 2R2 | 2.2uH | 2.2 |
| 4R7 | 4.7uH | 4.7 |

### 3-Digit Code (Multiplier)

| Code | Value | Calculation |
|------|-------|-------------|
| 100 | 10uH | 10 x 10^0 |
| 101 | 100uH | 10 x 10^1 |
| 102 | 1000uH (1mH) | 10 x 10^2 |
| 220 | 22uH | 22 x 10^0 |
| 221 | 220uH | 22 x 10^1 |
| 470 | 47uH | 47 x 10^0 |
| 471 | 470uH | 47 x 10^1 |

### Decoding Algorithm

```java
// R at start = sub-1uH value
if (code.startsWith("R")) {
    return Double.parseDouble("0." + code.substring(1));  // R47 -> 0.47
}

// R in middle = decimal point
if (code.contains("R")) {
    return Double.parseDouble(code.replace("R", "."));  // 1R0 -> 1.0
}

// 3-digit code: first 2 digits x 10^(3rd digit)
int mantissa = Integer.parseInt(code.substring(0, 2));
int exponent = Integer.parseInt(code.substring(2, 3));
return mantissa * Math.pow(10, exponent);  // 101 -> 10 x 10^1 = 100
```

---

## Impedance Encoding (Ferrite Beads)

GZ series uses 3-digit impedance code (at 100MHz):

| Code | Impedance | Calculation |
|------|-----------|-------------|
| 601 | 600 ohm | 60 x 10^1 |
| 121 | 120 ohm | 12 x 10^1 |
| 102 | 1000 ohm | 10 x 10^2 |
| 220 | 22 ohm | 22 x 10^0 |

```java
int mantissa = Integer.parseInt(code.substring(0, 2));
int exponent = Integer.parseInt(code.substring(2, 3));
return mantissa * Math.pow(10, exponent);  // 601 -> 60 x 10^1 = 600
```

---

## Package Size Codes

### Metric to Imperial Conversion

| Metric (mm) | Imperial | Notes |
|-------------|----------|-------|
| 1005 | 0402 | 1.0 x 0.5mm |
| 1608 | 0603 | 1.6 x 0.8mm |
| 2012 | 0805 | 2.0 x 1.2mm |
| 3216 | 1206 | 3.2 x 1.6mm |
| 3225 | 1210 | 3.2 x 2.5mm |
| 4516 | 1806 | 4.5 x 1.6mm |
| 4520 | 1808 | 4.5 x 2.0mm |
| 4532 | 1812 | 4.5 x 3.2mm |
| 5025 | 2010 | 5.0 x 2.5mm |
| 6332 | 2512 | 6.3 x 3.2mm |

### Power Inductor Sizes (Stay Metric)

| Size | Dimensions |
|------|------------|
| 2520 | 2.5 x 2.0mm |
| 3015 | 3.0 x 1.5mm |
| 4020 | 4.0 x 2.0mm |
| 4030 | 4.0 x 3.0mm |
| 5020 | 5.0 x 2.0mm |
| 5030 | 5.0 x 3.0mm |
| 6020 | 6.0 x 2.0mm |
| 6030 | 6.0 x 3.0mm |

---

## Tolerance Codes

| Code | Tolerance |
|------|-----------|
| J | +/- 5% |
| K | +/- 10% |
| M | +/- 20% |

---

## Handler Implementation Notes

### Series Extraction

```java
// Returns series + size as the full series identifier
// Example: SDCL1005C1R0MTDF -> "SDCL1005"

if (mpn.startsWith("SDCL")) {
    return "SDCL" + mpn.substring(4, 8);  // SDCL + 4-digit size
}
if (mpn.startsWith("SWPA")) {
    return "SWPA" + mpn.substring(4, 8);
}
if (mpn.startsWith("SDFL")) {
    return "SDFL" + mpn.substring(4, 8);
}
if (mpn.startsWith("GZ")) {
    return "GZ" + mpn.substring(2, 6);  // GZ only has 2-letter prefix
}
```

### Package Code Extraction

```java
// Extract 4-digit size code and convert to imperial
String sizeCode = extractSizeCode(mpn);  // e.g., "1005"
String imperial = SIZE_TO_IMPERIAL_MAP.get(sizeCode);  // e.g., "0402"
return imperial != null ? imperial : sizeCode;
```

### Value Extraction

```java
// For inductors (SDCL, SWPA, SDFL) - extract inductance
public String extractInductanceValue(String mpn) {
    // Match pattern and extract value code from group 4
    Matcher m = SDCL_PATTERN.matcher(mpn);
    if (m.matches()) {
        return parseInductanceCode(m.group(4));
    }
    // ... similar for SWPA, SDFL
}

// For ferrite beads (GZ) - extract impedance
public String extractImpedanceValue(String mpn) {
    Matcher m = GZ_PATTERN.matcher(mpn);
    if (m.matches()) {
        return parseImpedanceCode(m.group(4));
    }
}
```

---

## Component Types

Sunlord products map to:
- `INDUCTOR` - All inductor products
- `IC` - Also registered under IC for pattern matching compatibility

Note: Handler registers both types for each pattern.

---

## Common Part Numbers

| MPN | Description |
|-----|-------------|
| SDCL1005C1R0MTDF | 1.0uH power inductor, 0402, 20% |
| SWPA4020S100MT | 10uH shielded power inductor, 4020 |
| SDFL2012T1R0M3B | 1.0uH ferrite chip inductor, 0805 |
| GZ2012D601TF | 600 ohm ferrite bead, 0805 |

---

## Related Files

- Handler: `manufacturers/SunlordHandler.java`
- Supported types: `INDUCTOR`, `IC`
- No manufacturer-specific ComponentType enum entries

---

## Learnings & Edge Cases

- **GZ series prefix length**: GZ has only 2 letters before size code, unlike SDCL/SWPA/SDFL which have 4.
- **Value position varies**: In SDCL/SWPA/SDFL the value follows an optional type code. Pattern matching must be flexible.
- **Imperial conversion**: Standard chip sizes convert to imperial. Power inductor sizes stay metric (4020 stays 4020).
- **Type code is optional**: The single letter between size and value may be empty in some MPNs.
- **Ferrite beads vs inductors**: GZ series stores impedance, not inductance. Different extraction method needed.
- **Tolerance position**: Tolerance (M/K/J) appears immediately after the value code.

<!-- Add new learnings above this line -->
