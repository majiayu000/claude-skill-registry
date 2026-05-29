---
name: ablic
description: ABLIC (formerly Seiko Instruments) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with ABLIC power management and memory ICs.
---

# ABLIC Manufacturer Skill

## MPN Structure

ABLIC MPNs follow this general structure:

```
[S-][SERIES][VARIANT][VOLTAGE][PACKAGE][-SUFFIX]
 |     |        |        |        |        |
 |     |        |        |        |        +-- Grade/options (e.g., I6T1U)
 |     |        |        |        +-- Package letter (A, B, U, N)
 |     |        |        +-- 2-3 digit voltage code
 |     |        +-- Variant letter
 |     +-- Series number (1xxx, 80xxx, 35xxx, 82xx, 24C, 93C)
 +-- S- prefix (always present)
```

### Example Decoding

```
S-1167B33A-I6T1U
| |  | | |  |
| |  | | |  +-- I6T1U = Industrial grade, options
| |  | | +-- A = SOT-23 package
| |  | +-- 33 = 3.3V output
| |  +-- B = Variant within series
| +-- 1167 = LDO regulator series
+-- S- = ABLIC prefix

S-80740CNNB-G6T1U
| |   | | |  |
| |   | | |  +-- G6T1U = Grade/options
| |   | | +-- B = SOT-89 package
| |   | +-- NN = Variant/options
| |   +-- C = Type indicator
| +-- 80740 = Voltage detector series
+-- S- = ABLIC prefix

S-35390A-T8T1G
| |   | |  |
| |   | |  +-- T8T1G = Grade/options
| |   | +-- T = TSSOP package
| |   +-- A = Variant
| +-- 35390 = Real-Time Clock series
+-- S- = ABLIC prefix

S-24C02A
| |  | |
| |  | +-- A = SOT-23 package
| |  +-- 02 = 2Kbit density
| +-- 24C = I2C EEPROM series
+-- S- = ABLIC prefix
```

---

## Package Codes

### Standard Package Letters

| Code | Package | Notes |
|------|---------|-------|
| A | SOT-23 | Standard SOT-23 |
| B | SOT-89 | Medium power |
| U | USP | Ultra Small Package |
| N | SON | Small outline no-lead |
| C | CSP | Chip scale package |
| T | TSSOP | Thin shrink SOP |
| S | SOP | Standard SOP |
| F | WLCSP | Wafer-level CSP |

---

## Product Lines

### S-1xxx - LDO Voltage Regulators

| Series | Description | Features |
|--------|-------------|----------|
| S-1167 | Ultra-low Iq LDO | <1uA quiescent |
| S-1206 | Low dropout LDO | Standard regulator |
| S-1312 | LDO with enable | On/off control |
| S-1313 | LDO regulator | Various outputs |
| S-1318 | LDO regulator | High accuracy |

### S-80xxx / S-807xx / S-809xx - Voltage Detectors

| Series | Description | Function |
|--------|-------------|----------|
| S-80740 | Voltage detector | Reset IC |
| S-80945 | Voltage detector | Supervisory IC |
| S-807xx | Detector series | Power monitoring |
| S-809xx | Detector series | Reset generation |

### S-35xxx - Real-Time Clocks

| Series | Description | Interface |
|--------|-------------|-----------|
| S-35390A | RTC with I2C | 2-wire interface |
| S-35198 | RTC | Low power |

### S-82xx / S-8xxx - Battery Management ICs

| Series | Description | Function |
|--------|-------------|----------|
| S-8261 | Battery protection | Over-voltage/under-voltage |
| S-8254 | Battery fuel gauge | State of charge |

### S-24Cxx - I2C EEPROM

| Series | Description | Density |
|--------|-------------|---------|
| S-24C01 | I2C EEPROM | 1Kbit |
| S-24C02 | I2C EEPROM | 2Kbit |
| S-24C04 | I2C EEPROM | 4Kbit |
| S-24C08 | I2C EEPROM | 8Kbit |
| S-24C16 | I2C EEPROM | 16Kbit |

### S-93Cxx - Microwire EEPROM

| Series | Description | Density |
|--------|-------------|---------|
| S-93C46 | Microwire EEPROM | 1Kbit |
| S-93C56 | Microwire EEPROM | 2Kbit |
| S-93C66 | Microwire EEPROM | 4Kbit |
| S-93C76 | Microwire EEPROM | 8Kbit |
| S-93C86 | Microwire EEPROM | 16Kbit |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// ABLIC package codes are single letters
// Position varies by product type
// For LDOs: S-1167B33A -> A after voltage code
// For EEPROM: S-24C02A -> A after density

// LDO pattern: S-[0-9]+[variant][voltage]([package])
Pattern packagePattern = Pattern.compile("^S-[0-9]+[A-Z]*[0-9]{2,3}([ABUNCTSF]).*$");

// EEPROM pattern: S-[0-9]+C[0-9]+([package])
Pattern eepromPattern = Pattern.compile("^S-[0-9]+C[0-9]+([A-Z]).*$");
```

### Series Extraction

```java
// Different series have different length numbers
// S-1xxx (4 digits), S-80xxx (5 digits), S-35xxx (5 digits)
// S-82xx/S-82xxx (4-5 digits), S-24C/S-93C (prefix only)

if (upperMpn.matches("^S-1[0-9]{3}.*")) {
    return upperMpn.substring(0, 6);  // S-1167, S-1206
}
if (upperMpn.matches("^S-80[0-9]{3}.*")) {
    return upperMpn.substring(0, 7);  // S-80740, S-80945
}
if (upperMpn.matches("^S-35[0-9]{3}.*")) {
    return upperMpn.substring(0, 7);  // S-35390, S-35198
}
if (upperMpn.matches("^S-24C[0-9]+.*")) {
    return "S-24C";  // I2C EEPROM series
}
if (upperMpn.matches("^S-93C[0-9]+.*")) {
    return "S-93C";  // Microwire EEPROM series
}
```

### Product Type Detection

```java
public boolean isLDORegulator(String mpn) {
    return mpn.matches("^S-1[0-9]{3}[A-Z0-9-]*$");
}

public boolean isVoltageDetector(String mpn) {
    return mpn.matches("^S-80[0-9]{3}[A-Z0-9-]*$") ||
           mpn.matches("^S-8[07]9[0-9]{2}[A-Z0-9-]*$");
}

public boolean isRTC(String mpn) {
    return mpn.matches("^S-35[0-9]{3}[A-Z0-9-]*$");
}

public boolean isBatteryManagement(String mpn) {
    return mpn.matches("^S-82[0-9]{2,3}[A-Z0-9-]*$");
}

public boolean isEEPROM(String mpn) {
    return mpn.matches("^S-24C[0-9]+.*") ||
           mpn.matches("^S-93C[0-9]+.*");
}

public boolean isI2CEEPROM(String mpn) {
    return mpn.matches("^S-24C[0-9]+[A-Z0-9-]*$");
}

public boolean isMicrowireEEPROM(String mpn) {
    return mpn.matches("^S-93C[0-9]+[A-Z0-9-]*$");
}
```

### Supported Component Types

```java
// ABLIC handler supports:
// - IC (all parts)
// - VOLTAGE_REGULATOR (S-1xxx LDOs, S-80xxx detectors)
// - MEMORY (S-24Cxx, S-93Cxx EEPROMs)
// - MEMORY_EEPROM (S-24Cxx, S-93Cxx EEPROMs)

// Note: RTC (S-35xxx) and Battery Management (S-82xx) are classified as IC only
```

---

## Related Files

- Handler: `manufacturers/ABLICHandler.java`
- Component types: `IC`, `VOLTAGE_REGULATOR`, `MEMORY`, `MEMORY_EEPROM`
- Test file: `handlers/ABLICHandlerTest.java`

---

## Learnings & Edge Cases

- **S- prefix is mandatory**: All ABLIC parts start with "S-" - don't confuse with other S-prefixed manufacturers
- **Formerly Seiko Instruments (SII)**: ABLIC was spun off from SII in 2016, legacy parts may have SII branding
- **Ultra-low power focus**: ABLIC specializes in battery-powered and IoT applications
- **Voltage detectors as regulators**: S-80xxx voltage detectors are classified as VOLTAGE_REGULATOR
- **EEPROM interface types**: S-24Cxx uses I2C, S-93Cxx uses Microwire (3-wire SPI-like)
- **Complex suffix structure**: Suffixes like "-I6T1U" encode grade, tape/reel, and package options
- **Package code position varies**: For LDOs it's after voltage code, for EEPROM it's after density
- **Real-Time Clocks not in VOLTAGE_REGULATOR**: S-35xxx RTCs are IC type only
- **Battery management ICs**: S-82xx parts are for Li-ion protection/fuel gauge, classified as IC

<!-- Add new learnings above this line -->
