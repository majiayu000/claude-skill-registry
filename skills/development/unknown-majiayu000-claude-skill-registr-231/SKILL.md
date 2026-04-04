---
name: cyntec
description: Cyntec power inductor MPN encoding patterns, value decoding, and handler guidance. Use when working with Cyntec inductors or CyntecHandler.
---

# Cyntec Corporation Manufacturer Skill

## MPN Structure

Cyntec MPNs follow this structure:

```
[SERIES][SIZE][TYPE]-[VALUE][TOLERANCE][PACK]
   |      |     |      |        |        |
   |      |     |      |        |        +-- Packaging (N=Tape/Reel)
   |      |     |      |        +-- M=20%, K=10%
   |      |     |      +-- Inductance code
   |      |     +-- Type variant (T, S, etc.)
   |      +-- 3-4 digit size code
   +-- Series (PCMC, VCMD, MCPA, CMC)
```

### Example Decoding

```
PCMC063T-1R0MN
|   |  |  |  ||
|   |  |  |  |+-- Packaging (N=Tape/Reel)
|   |  |  |  +-- Tolerance (M=+/-20%)
|   |  |  +-- Inductance (1R0 = 1.0uH)
|   |  +-- Type variant (T)
|   +-- Size (063 = 6.3mm)
+-- PCMC = Power Inductor series

MCPA0504-1R0MN
|   |    |  ||
|   |    |  |+-- Packaging (N=Tape/Reel)
|   |    |  +-- Tolerance (M=+/-20%)
|   |    +-- Inductance (1R0 = 1.0uH)
|   +-- Size (0504 = 5.0mm x 4.0mm)
+-- MCPA = Automotive Power Inductor series

CMC0503-471M
|  |    |  |
|  |    |  +-- Tolerance (M=+/-20%)
|  |    +-- Impedance (471 = 470 ohm)
|  +-- Size (0503 = 5.0mm x 3.0mm)
+-- CMC = Common Mode Choke series
```

---

## Series Reference

### PCMC - Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Power inductor |
| Pattern | `^PCMC[0-9]{3,4}.*` |
| Size format | 3-4 digits |
| Application | General power conversion |

### VCMD - Molded Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Molded power inductor |
| Pattern | `^VCMD[0-9]{3,4}.*` |
| Size format | 3-4 digits |
| Application | High current, shielded |

### MCPA - Automotive Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Automotive-grade power inductor |
| Pattern | `^MCPA[0-9]{4}.*` |
| Size format | 4 digits |
| Application | AEC-Q200 qualified |

### CMC - Common Mode Chokes

| Feature | Description |
|---------|-------------|
| Type | Common mode choke |
| Pattern | `^CMC[0-9]{4}.*` |
| Size format | 4 digits |
| Application | EMI/EMC filtering |

---

## Inductance Encoding

Cyntec uses standard R-notation:

### R-Notation (Decimal Point)

| Code | Value | Notes |
|------|-------|-------|
| R47 | 0.47uH | R at start = sub-1uH |
| R68 | 0.68uH | R at start |
| 1R0 | 1.0uH | R in middle |
| 2R2 | 2.2uH | R in middle |
| 4R7 | 4.7uH | R in middle |
| 6R8 | 6.8uH | R in middle |

### 3-Digit Multiplier Code

| Code | Value | Calculation |
|------|-------|-------------|
| 100 | 10uH | 10 x 10^0 |
| 101 | 100uH | 10 x 10^1 |
| 220 | 22uH | 22 x 10^0 |
| 470 | 47uH | 47 x 10^0 |
| 471 | 470uH | 47 x 10^1 |

### Decoding Algorithm

```java
// R at start (R47, R68)
if (code.startsWith("R")) {
    double value = Double.parseDouble("0." + code.substring(1));
    return formatInductance(value);
}

// R in middle (1R0, 2R2)
if (code.contains("R")) {
    String[] parts = code.split("R");
    double value = Double.parseDouble(parts[0] + "." + parts[1]);
    return formatInductance(value);
}

// 3-digit code
if (code.matches("\\d{3}")) {
    int mantissa = Integer.parseInt(code.substring(0, 2));
    int exponent = Integer.parseInt(code.substring(2, 3));
    double microhenries = mantissa * Math.pow(10, exponent);
    return formatInductance(microhenries);
}
```

---

## Size Code Formats

### 3-Digit Size (PCMC, VCMD)

| Code | Dimension |
|------|-----------|
| 063 | 6.3mm |
| 050 | 5.0mm |
| 040 | 4.0mm |

### 4-Digit Size (MCPA, CMC)

| Code | Dimensions |
|------|------------|
| 0504 | 5.0mm x 4.0mm |
| 0403 | 4.0mm x 3.0mm |
| 0503 | 5.0mm x 3.0mm |

---

## Tolerance Codes

| Code | Tolerance |
|------|-----------|
| K | +/- 10% |
| M | +/- 20% |

---

## Package Type by Series

| Series | Package Type |
|--------|--------------|
| PCMC | Power Inductor |
| VCMD | Molded Power Inductor |
| MCPA | Automotive Power Inductor |
| CMC | Common Mode Choke |

---

## Handler Implementation Notes

### Series Extraction

```java
// Returns series + size + type as the full identifier
// PCMC063T-1R0MN -> "PCMC063T"
// MCPA0504-1R0MN -> "MCPA0504"

Matcher m = PCMC_PATTERN.matcher(upperMpn);
if (m.matches()) {
    String type = m.group(3);
    return m.group(1) + m.group(2) + (type != null ? type : "");
}

m = VCMD_PATTERN.matcher(upperMpn);
if (m.matches()) {
    String type = m.group(3);
    return m.group(1) + m.group(2) + (type != null ? type : "");
}

// MCPA and CMC don't have type suffix
m = MCPA_PATTERN.matcher(upperMpn);
if (m.matches()) {
    return m.group(1) + m.group(2);
}
```

### Package Code Extraction

```java
// Returns the package type description based on series
String series = extractSeriesPrefix(mpn);
return SERIES_PACKAGE_MAP.get(series);
// Returns: "Power Inductor", "Molded Power Inductor", etc.
```

### Value Extraction

```java
// Value code position varies by series
// PCMC/VCMD: group(4) after type
// MCPA/CMC: group(3) directly after size

Matcher m = PCMC_PATTERN.matcher(mpn);
if (m.matches()) {
    String valueCode = m.group(4);
    return parseInductanceCode(valueCode);
}

m = MCPA_PATTERN.matcher(mpn);
if (m.matches()) {
    String valueCode = m.group(3);
    return parseInductanceCode(valueCode);
}
```

---

## Pattern Details

### PCMC Pattern

```java
Pattern.compile(
    "^(PCMC)(\\d{3,4})([A-Z]?)[-]?([0-9R]+)([A-Z]*)$"
);
// Groups: (1)series (2)size (3)type (4)value (5)tolerance+options
```

### VCMD Pattern

```java
Pattern.compile(
    "^(VCMD)(\\d{3,4})([A-Z]?)[-]?([0-9R]+)([A-Z]*)$"
);
// Same structure as PCMC
```

### MCPA Pattern

```java
Pattern.compile(
    "^(MCPA)(\\d{4})[-]?([0-9R]+)([A-Z]*)$"
);
// No type field, 4-digit size only
```

### CMC Pattern

```java
Pattern.compile(
    "^(CMC)(\\d{4})[-]?([0-9]+)([A-Z]*)$"
);
// Numeric-only value (impedance), no R-notation
```

---

## Component Types

Cyntec products map to:
- `INDUCTOR` - All inductor and choke products
- `IC` - Also registered for pattern matching compatibility

---

## CMC Impedance Encoding

Common mode chokes use 3-digit impedance code (like ferrite beads):

| Code | Impedance |
|------|-----------|
| 471 | 470 ohm |
| 102 | 1000 ohm |
| 222 | 2200 ohm |

---

## Common Part Numbers

| MPN | Description |
|-----|-------------|
| PCMC063T-1R0MN | 1.0uH power inductor, 6.3mm |
| VCMD063T-2R2MN | 2.2uH molded inductor, 6.3mm |
| MCPA0504-1R0MN | 1.0uH automotive inductor |
| CMC0503-471M | 470 ohm common mode choke |

---

## Related Files

- Handler: `manufacturers/CyntecHandler.java`
- Supported types: `INDUCTOR`, `IC`
- No manufacturer-specific ComponentType enum entries

---

## Learnings & Edge Cases

- **Variable size digit count**: PCMC/VCMD can have 3 OR 4 digit size codes (063 vs 0504). MCPA/CMC always have 4.
- **Type field presence**: PCMC/VCMD have optional type letter (T, S). MCPA/CMC don't have this field.
- **CMC uses impedance**: Common mode chokes encode impedance, not inductance. No R-notation allowed.
- **Series included in package code**: Unlike other handlers, Cyntec returns the package TYPE name (e.g., "Power Inductor") not size.
- **Dash is optional**: The dash before value code may be present or absent.
- **N suffix = tape and reel**: Standard packaging suffix.

<!-- Add new learnings above this line -->
