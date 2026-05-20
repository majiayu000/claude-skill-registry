---
name: silergy
description: Silergy Corp MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Silergy power management ICs.
---

# Silergy Corp Manufacturer Skill

## MPN Structure

Silergy MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][PACKAGE]
   |       |        |        |
   |       |        |        +-- Package code (2-5 letters): AAC, QNC, DFN
   |       |        +-- Single digit variant (0-9)
   |       +-- 3-4 digit series (e.g., 808, 720, 628)
   +-- SY or SYX (extended line)
```

### Example Decoding

```
SY8088AAC
|| |  |||
|| |  ||+-- C = Part of QFN suffix
|| |  |+-- A = Part of QFN suffix
|| |  +-- A = Package code start
|| +-- 8 = Variant within SY808 series
|+-- SY808 = DC-DC buck converter series
+-- Silergy prefix

SY7208QNC
|| |  |||
|| |  ||+-- C = Part of QFN suffix
|| |  |+-- N = QFN variant
|| |  +-- Q = Package start
|| +-- 8 = Variant within SY720 series
|+-- SY720 = DC-DC boost converter series
+-- Silergy prefix

SYX196
||| ||
||| |+-- 6 = Variant
||| +-- 19 = Part of series number
||+-- X = Extended product line indicator
|+-- SY = Silergy prefix
+-- Extended line part
```

---

## Package Codes

### QFN Packages

| Code | Package | Notes |
|------|---------|-------|
| AAC | QFN | Common QFN variant |
| QNC | QFN | QFN with N variant |
| QFN | QFN | Standard designation |

### DFN Packages

| Code | Package | Notes |
|------|---------|-------|
| DFN | DFN | Standard DFN |

### SOT Packages

| Code | Package | Notes |
|------|---------|-------|
| SOT | SOT-23 | Standard SOT-23 |
| TSOT | TSOT-23 | Thin SOT-23 |

### CSP Packages

| Code | Package | Notes |
|------|---------|-------|
| WLCSP | WLCSP | Wafer-level chip scale |
| CSP | CSP | Chip scale package |

### SOIC/SOP Packages

| Code | Package | Notes |
|------|---------|-------|
| SOIC | SOIC-8 | 8-pin SOIC |
| SOP | SOP-8 | 8-pin SOP |

---

## Product Lines

### SY808x - DC-DC Buck Converters (Low Voltage Input)

| Series | Description | Input Voltage |
|--------|-------------|---------------|
| SY8088 | Synchronous buck | 2.5V-5.5V |
| SY8089 | Synchronous buck | 2.5V-5.5V |

### SY809x - DC-DC Buck Converters

| Series | Description | Features |
|--------|-------------|----------|
| SY8090 | Buck converter | Standard efficiency |
| SY809x | Buck converters | Various output currents |

### SY811x - DC-DC Buck Converters

| Series | Description | Features |
|--------|-------------|----------|
| SY8113 | Buck converter | High efficiency |
| SY811x | Buck converters | Various packages |

### SY720x - DC-DC Boost Converters / LED Drivers

| Series | Type | Notes |
|--------|------|-------|
| SY7200 | LED driver | White LED driver |
| SY7201-SY7209 | Boost converters | Step-up converters |

### SY800x - LDO Regulators

| Series | Description | Output Current |
|--------|-------------|----------------|
| SY8009 | LDO | Low current |
| SY800x | LDO series | Various ratings |

### SY628x - LDO Regulators (High Current)

| Series | Description | Output Current |
|--------|-------------|----------------|
| SY6288 | High current LDO | Higher current capability |
| SY628x | LDO series | Load switch features |

### SY698x - Battery Chargers

| Series | Description | Chemistry |
|--------|-------------|-----------|
| SY6981 | Li-ion charger | Single cell |
| SY6982 | Li-ion charger | With power path |

### SYXxxx - Extended Product Line

| Series | Description | Notes |
|--------|-------------|-------|
| SYX196 | Extended line | Various functions |
| SYXxxx | Mixed products | Newer designs |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Silergy package codes are 2-5 letters after the part number
// Pattern: SY[X]?[0-9]{3,4}[PACKAGE]
// Examples: SY8088AAC -> AAC -> QFN
//           SY6288DFN -> DFN -> DFN

Pattern packagePattern = Pattern.compile("^SY[X]?[0-9]{3,4}([A-Z]{2,5}).*$");
```

### Series Extraction

```java
// SYX series returns "SYX"
// Standard SY[0-9]{4} returns first 5 chars (e.g., SY808, SY720)
if (upperMpn.matches("^SYX[0-9]{3}.*")) {
    return "SYX";
}
if (upperMpn.matches("^SY[0-9]{4}.*")) {
    return upperMpn.substring(0, 5);  // SY808, SY720, SY628, etc.
}
```

### LED Driver Detection

```java
// Only SY7200 is an LED driver in the SY720x series
// SY7201-SY7209 are boost converters
private boolean isLEDDriver(String mpn) {
    return mpn.matches("^SY7200[A-Z0-9]*$");
}
```

### Product Category Determination

```java
public String getProductCategory(String mpn) {
    String upper = mpn.toUpperCase();

    // Buck converters
    if (upper.matches("^SY808[0-9].*") ||
        upper.matches("^SY809[0-9].*") ||
        upper.matches("^SY811[0-9].*")) {
        return "DC-DC Buck Converter";
    }
    // Boost converters (not SY7200)
    if (upper.matches("^SY720[1-9].*")) {
        return "DC-DC Boost Converter";
    }
    // LED driver
    if (upper.matches("^SY7200.*")) {
        return "LED Driver";
    }
    // LDOs
    if (upper.matches("^SY800[0-9].*") ||
        upper.matches("^SY628[0-9].*")) {
        return "LDO Regulator";
    }
    // Battery chargers
    if (upper.matches("^SY698[0-9].*")) {
        return "Battery Charger";
    }
    return "";
}
```

---

## Related Files

- Handler: `manufacturers/SilergyHandler.java`
- Component types: `IC`, `VOLTAGE_REGULATOR`, `LED_DRIVER`
- Test file: `handlers/SilergyHandlerTest.java`

---

## Learnings & Edge Cases

- **SY7200 vs SY720x**: SY7200 is specifically an LED driver, while SY7201-SY7209 are boost converters
- **SYX extended line**: SYX parts are newer designs with 3-digit numbers (e.g., SYX196)
- **Package code length varies**: Silergy uses 2-5 letter package codes (AAC, QNC, DFN, WLCSP)
- **Series numbering**: SY followed by 4 digits, where first 3 digits identify the product family
- **High current LDOs (SY628x)**: These often include load switch functionality
- **Battery chargers (SY698x)**: Include power path management for Li-ion/Li-polymer cells
- **No automotive prefix**: Unlike Richtek, Silergy doesn't use a separate prefix for automotive parts

<!-- Add new learnings above this line -->
