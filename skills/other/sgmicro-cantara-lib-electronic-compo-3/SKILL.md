---
name: sgmicro
description: SG Micro Corp MPN encoding patterns, suffix decoding, and handler guidance. Use when working with SG Micro analog ICs.
---

# SG Micro Corp Manufacturer Skill

## MPN Structure

SG Micro MPNs follow this general structure:

```
[SGM][SERIES][VARIANT][-VOLTAGE][PACKAGE][G][/TR]
  |     |        |        |         |     |   |
  |     |        |        |         |     |   +-- /TR = Tape and Reel
  |     |        |        |         |     +-- G = Green/RoHS
  |     |        |        |         +-- Package code (YN5, XN, YS8, etc.)
  |     |        |        +-- Optional voltage (e.g., -3.3)
  |     |        +-- Variant letter (A, B, etc.)
  |     +-- 4-5 digit series (2xxx, 4xxx, 58xxx, 6xxx, 8xxx)
  +-- SGM = SG Micro prefix
```

### Example Decoding

```
SGM2019-3.3YN5G/TR
|  |   |   |  | |
|  |   |   |  | +-- /TR = Tape and reel
|  |   |   |  +-- G = RoHS/Green
|  |   |   +-- YN5 = SOT-23-5 package
|  |   +-- 3.3 = 3.3V output voltage
|  +-- 2019 = LDO regulator series
+-- SGM = SG Micro prefix

SGM8051XN5G/TR
|  |  | | | |
|  |  | | | +-- /TR = Tape and reel
|  |  | | +-- G = RoHS
|  |  | +-- XN5 = SC70-5 package
|  |  +-- 1 = Variant (single op-amp)
|  +-- 805 = Op-amp series
+-- SGM = SG Micro prefix

SGM6603AYTD6G/TR
|  |  | |   | |
|  |  | |   | +-- /TR = Tape and reel
|  |  | |   +-- G = RoHS
|  |  | +-- YTD6 = DFN-6 package
|  |  +-- A = Variant
|  +-- 6603 = DC-DC converter series
+-- SGM = SG Micro prefix
```

---

## Package Codes

### SOT-23 Family (Y prefix)

| Code | Package | Pin Count |
|------|---------|-----------|
| YN | SOT-23 | 3 |
| YN5 | SOT-23-5 | 5 |
| YN6 | SOT-23-6 | 6 |
| YN8 | SOT-23-8 | 8 |

### SC70 Family (X prefix)

| Code | Package | Pin Count |
|------|---------|-----------|
| XN | SC70 | 3 |
| XN5 | SC70-5 | 5 |
| XN6 | SC70-6 | 6 |

### SOIC Family (YS)

| Code | Package | Pin Count |
|------|---------|-----------|
| YS | SOIC-8 | 8 |
| YS8 | SOIC-8 | 8 |
| YS14 | SOIC-14 | 14 |
| YS16 | SOIC-16 | 16 |

### MSOP Family (XS)

| Code | Package | Pin Count |
|------|---------|-----------|
| XS | MSOP-8 | 8 |
| XS8 | MSOP-8 | 8 |
| XS10 | MSOP-10 | 10 |

### DFN Family (YTD/XTD)

| Code | Package | Pin Count |
|------|---------|-----------|
| YTD | DFN | Various |
| YTD6 | DFN-6 | 6 |
| YTD8 | DFN-8 | 8 |
| XTD | DFN | Various |

### QFN Family (YQN)

| Code | Package | Pin Count |
|------|---------|-----------|
| YQN | QFN | Various |
| YQN16 | QFN-16 | 16 |
| YQN20 | QFN-20 | 20 |

### WLCSP (UTD/UFC)

| Code | Package | Notes |
|------|---------|-------|
| UTD | WLCSP | Wafer-level CSP |
| UFC | WLCSP | WLCSP variant |

---

## Product Lines

### SGM2xxx - LDO Regulators

| Series | Description | Features |
|--------|-------------|----------|
| SGM2019 | Ultra-low Iq LDO | 1.7uA quiescent |
| SGM2036 | 300mA LDO | Low noise |
| SGM2040 | 300mA LDO | Fast transient |

### SGM4xxx - ADCs/DACs/Analog Switches

| Series | Description | Type |
|--------|-------------|------|
| SGM4567 | Analog switch | SPDT |
| SGM4xxx | Mixed signal | Various functions |

### SGM58xxx - High-Precision ADCs

| Series | Description | Resolution |
|--------|-------------|------------|
| SGM58031 | Precision ADC | 16-bit |
| SGM58xxx | High-resolution ADCs | Various |

### SGM6xxx - DC-DC Converters

| Series | Description | Type |
|--------|-------------|------|
| SGM6132 | Synchronous buck | Step-down |
| SGM6603 | Buck converter | High efficiency |

### SGM8xxx - Op-Amps/Comparators

| Subseries | Type | Description |
|-----------|------|-------------|
| SGM80xx-SGM85xx | Op-amps | Various configurations |
| SGM8051 | Single op-amp | Rail-to-rail |
| SGM8262 | Dual op-amp | Low noise |
| SGM8521 | Single op-amp | High precision |
| SGM87xx-SGM89xx | Comparators | Fast/precision |
| SGM8711 | Comparator | Open-drain output |
| SGM8722 | Dual comparator | Push-pull output |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// SG Micro package codes start with Y, X, or U
// Pattern: SGM[0-9]{4,5}[-.]?[voltage]?[package-code]G?(/TR)?
// Extract 2-4 uppercase letters optionally followed by digits

// Remove G and /TR suffixes first
String baseMpn = upperMpn.replaceAll("G?(/TR)?$", "");

// Find package code pattern
Pattern packagePattern = Pattern.compile(".*?([XYUQ][A-Z]*[0-9]*)(?:G?(/TR)?)?$");
```

### Series Extraction

```java
// SGM58xxx is special (5 digits)
// Other series are 4 digits: SGM2xxx, SGM4xxx, SGM6xxx, SGM8xxx

if (upperMpn.startsWith("SGM58") && upperMpn.length() >= 8) {
    return "SGM58";  // High-precision ADC series
}
if (upperMpn.matches("^SGM[0-9][0-9]{3}.*")) {
    return upperMpn.substring(0, 4);  // SGM2, SGM4, SGM6, SGM8
}
```

### Op-Amp vs Comparator Detection

```java
// Op-amps: SGM80xx through SGM85xx
private boolean isOpAmp(String mpn) {
    return mpn.matches("^SGM8[0-5][0-9]{2}[A-Z0-9./-]*$");
}

// Comparators: SGM87xx and higher
private boolean isComparator(String mpn) {
    return mpn.matches("^SGM8[7-9][0-9]{2}[A-Z0-9./-]*$");
}
```

### Voltage in MPN

```java
// Voltage can appear as -3.3 or -3.0 in the MPN
// SGM2019-3.3YN5G/TR -> 3.3V output
// The handler allows dots in MPN patterns: [A-Z0-9./-]*
```

### Product Type Detection

```java
public boolean isLDOPart(String mpn) {
    return mpn.matches("^SGM2[0-9]{3}[A-Z0-9./-]*$");
}

public boolean isDCDCPart(String mpn) {
    return mpn.matches("^SGM6[0-9]{3}[A-Z0-9./-]*$");
}

public boolean isOpAmpPart(String mpn) {
    return mpn.matches("^SGM8[0-5][0-9]{2}[A-Z0-9./-]*$");
}

public boolean isComparatorPart(String mpn) {
    return mpn.matches("^SGM8[7-9][0-9]{2}[A-Z0-9./-]*$");
}
```

---

## Related Files

- Handler: `manufacturers/SGMicroHandler.java`
- Component types: `IC`, `VOLTAGE_REGULATOR`, `OPAMP`
- Test file: `handlers/SGMicroHandlerTest.java`

---

## Learnings & Edge Cases

- **Voltage in MPN**: LDO parts often include output voltage in the MPN (e.g., SGM2019-3.3)
- **Dot character in MPN**: Pattern must allow dots for voltage codes (3.3V, 1.8V, etc.)
- **Package code prefix**: Y = SOT/SOIC, X = SC70/MSOP, U = WLCSP
- **G suffix**: Indicates RoHS/Green compliance, not part of package code
- **Op-amp numbering**: SGM8051 = single, SGM8262 = dual (similar to industry standard)
- **SGM8xxx split**: 80-85xx are op-amps, 87-89xx are comparators
- **ADC series**: SGM58xxx has 5 digits (unlike other 4-digit series)
- **Trailing /TR**: Common tape and reel suffix, strip before package extraction
- **No slash in patterns**: Despite /TR suffix, base patterns use [A-Z0-9./-] to handle it

<!-- Add new learnings above this line -->
