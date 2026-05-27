---
name: chilisin
description: Chilisin Electronics inductor MPN encoding patterns, value decoding, and handler guidance. Use when working with Chilisin inductors or ChilisinHandler.
---

# Chilisin Electronics Manufacturer Skill

## MPN Structure

Chilisin MPNs follow this structure:

```
[SERIES][SIZE][HEIGHT][TYPE]-[VALUE][TOLERANCE]-[PACK]
   |      |     |       |      |        |         |
   |      |     |       |      |        |         +-- Packaging code
   |      |     |       |      |        +-- M=20%, K=10%, J=5%
   |      |     |       |      +-- Inductance code
   |      |     |       +-- Type/shield code
   |      |     +-- Height code (SQC only)
   |      +-- 4-digit size code
   +-- Series (SQC, MHCI, MHCC, CS)
```

### Example Decoding

```
SQC453226T-100M-N
|  |  | |  |  | |
|  |  | |  |  | +-- Packaging (N=Tape/Reel)
|  |  | |  |  +-- Tolerance (M=+/-20%)
|  |  | |  +-- Inductance (100 = 10uH)
|  |  | +-- Type code (T=Shield type)
|  |  +-- Height (26 = 2.6mm)
|  +-- Size (4532 = 4.5mm x 3.2mm)
+-- SQC = Chip Inductor series

MHCI0504-1R0M-R8
|   |    |  | ||
|   |    |  | |+-- Reel option (8)
|   |    |  | +-- Reel marker (R)
|   |    |  +-- Tolerance (M=+/-20%)
|   |    +-- Inductance (1R0 = 1.0uH)
|   +-- Size (0504 = 5.0mm x 4.0mm)
+-- MHCI = Power Inductor series
```

---

## Series Reference

### SQC - Chip Inductors

| Feature | Description |
|---------|-------------|
| Type | Multilayer chip inductor |
| Pattern | `^SQC[0-9]{4}[0-9]{2}[A-Z]?-?[0-9R]+[A-Z]-?.*` |
| Unique | Includes height code after size |

### MHCI - Power Inductors

| Feature | Description |
|---------|-------------|
| Type | Power inductor |
| Pattern | `^MHCI[0-9]{4}-?[0-9R]+[A-Z]-?.*` |
| Application | High current, low DCR |

### MHCC - Coupled Inductors

| Feature | Description |
|---------|-------------|
| Type | Coupled/dual winding inductor |
| Pattern | `^MHCC[0-9]{4}-?[0-9R]+?[A-Z]?-?.*` |
| Application | DC-DC converters |

### CS - Ferrite Chip Inductors

| Feature | Description |
|---------|-------------|
| Type | Ferrite chip inductor |
| Pattern | `^CS[0-9]{4}-?[0-9R]+?[A-Z]?-?.*` |
| Application | EMI filtering |

---

## Inductance Encoding

Chilisin uses standard EIA encoding:

### R-Notation (Decimal Point)

| Code | Value | Notes |
|------|-------|-------|
| R10 | 0.10uH (100nH) | R at start |
| R22 | 0.22uH (220nH) | R at start |
| R47 | 0.47uH (470nH) | R at start |
| 1R0 | 1.0uH | R in middle |
| 2R2 | 2.2uH | R in middle |
| 4R7 | 4.7uH | R in middle |

### 3-Digit Multiplier Code

| Code | Value | Calculation |
|------|-------|-------------|
| 100 | 10uH | 10 x 10^0 |
| 101 | 100uH | 10 x 10^1 |
| 102 | 1mH | 10 x 10^2 |
| 220 | 22uH | 22 x 10^0 |
| 221 | 220uH | 22 x 10^1 |
| 470 | 47uH | 47 x 10^0 |
| 471 | 470uH | 47 x 10^1 |

### Decoding Algorithm

```java
// R at start (R10, R22, R47)
if (code.startsWith("R") && !code.substring(1).contains("R")) {
    String digits = code.substring(1);
    double value = Double.parseDouble("0." + digits);
    return formatInductance(value);  // Returns "100nH" etc.
}

// R in middle (1R0, 2R2)
if (code.contains("R")) {
    String normalized = code.replace("R", ".");
    double value = Double.parseDouble(normalized);
    return formatInductance(value);  // Returns "1.0uH" etc.
}

// 3-digit code
if (code.length() >= 3 && code.matches("\\d{3}")) {
    int mantissa = Integer.parseInt(code.substring(0, 2));
    int exponent = Integer.parseInt(code.substring(2, 3));
    double microhenries = mantissa * Math.pow(10, exponent);
    return formatInductance(microhenries);
}
```

---

## Package Size Codes

### Size Code to Dimensions

| Code | Dimensions | Notes |
|------|------------|-------|
| 0504 | 5.0 x 4.0mm | Power inductor |
| 0403 | 4.0 x 3.0mm | Power inductor |
| 0302 | 3.0 x 2.0mm | Power inductor |
| 4532 | 4.5 x 3.2mm | Chip inductor |
| 3225 | 3.2 x 2.5mm | Chip inductor |
| 2520 | 2.5 x 2.0mm | Chip inductor |
| 2016 | 2.0 x 1.6mm | Chip inductor |
| 1608 | 1.6 x 0.8mm | Chip inductor |
| 1005 | 1.0 x 0.5mm | Chip inductor |
| 0603 | 0603 imperial | Small chip |
| 0402 | 0402 imperial | Very small |
| 0201 | 0201 imperial | Ultra small |

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
// Returns series + size as the full identifier
// SQC453226T-100M-N -> "SQC4532"
// MHCI0504-1R0M-R8 -> "MHCI0504"

Matcher m = SQC_PATTERN.matcher(upperMpn);
if (m.matches()) {
    return m.group(1) + m.group(2);  // SQC + size
}

m = MHCI_PATTERN.matcher(upperMpn);
if (m.matches()) {
    return m.group(1) + m.group(2);  // MHCI + size
}
// Similar for MHCC, CS
```

### Package Code Extraction

```java
// Extract size code and map to dimensions
String sizeCode = extractSizeCode(mpn);
if (SIZE_CODE_MAP.containsKey(sizeCode)) {
    return SIZE_CODE_MAP.get(sizeCode);  // e.g., "4.5x3.2mm"
}
return sizeCode;  // Return raw code if no mapping
```

### SQC Height Code

SQC series uniquely includes a 2-digit height code:

```java
// SQC453226T -> 4532 (size) + 26 (height = 2.6mm) + T (type)
Matcher m = SQC_PATTERN.matcher(mpn);
if (m.matches()) {
    String size = m.group(2);    // "4532"
    String height = m.group(3);  // "26" = 2.6mm
    String type = m.group(4);    // "T"
}
```

---

## Pattern Details

### SQC Pattern

```java
Pattern.compile(
    "^(SQC)(\\d{4})(\\d{2})([A-Z])?[-]?([0-9R]+)([A-Z])[-]?([A-Z0-9]*)$"
);
// Groups: (1)series (2)size (3)height (4)type (5)value (6)tolerance (7)packaging
```

### MHCI Pattern

```java
Pattern.compile(
    "^(MHCI)(\\d{4})[-]?([0-9R]+)([A-Z])[-]?([A-Z0-9]*)$"
);
// Groups: (1)series (2)size (3)value (4)tolerance (5)packaging
```

### MHCC Pattern

```java
Pattern.compile(
    "^(MHCC)(\\d{4})[-]?([0-9R]+)?([A-Z])?[-]?([A-Z0-9]*)$"
);
// Optional value for coupled inductors
```

### CS Pattern

```java
Pattern.compile(
    "^(CS)(\\d{4})[-]?([0-9R]+)?([A-Z])?[-]?([A-Z0-9]*)$"
);
// CS has only 2-letter prefix
```

---

## Component Types

Chilisin products map to:
- `INDUCTOR` - All inductor products
- `IC` - Also registered for pattern matching compatibility

---

## Common Part Numbers

| MPN | Description |
|-----|-------------|
| SQC453226T-100M-N | 10uH chip inductor, 4.5x3.2mm, 2.6mm height |
| MHCI0504-1R0M-R8 | 1.0uH power inductor, 5.0x4.0mm |
| MHCC0504-2R2M | 2.2uH coupled inductor, 5.0x4.0mm |
| CS0402-R10M | 0.1uH ferrite chip, 0402 |

---

## Related Files

- Handler: `manufacturers/ChilisinHandler.java`
- Supported types: `INDUCTOR`, `IC`
- No manufacturer-specific ComponentType enum entries

---

## Learnings & Edge Cases

- **SQC height code**: Unique to SQC series. The 2 digits after size encode height in 0.1mm units (26 = 2.6mm).
- **CS prefix is short**: Only 2 letters (CS), unlike others with 3-4 letters (SQC, MHCI, MHCC).
- **Dashes are optional**: MPNs may or may not include dashes between fields. Patterns must handle both.
- **MHCC value optional**: Coupled inductors may not include a value code in the MPN.
- **R at start vs middle**: R10 = 0.10uH, 1R0 = 1.0uH. Different parsing logic needed.
- **Package code returns dimensions**: Unlike other handlers, Chilisin handler returns "4.5x3.2mm" format, not imperial code.

<!-- Add new learnings above this line -->
