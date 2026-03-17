---
name: torex
description: Torex Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Torex power management ICs.
---

# Torex Semiconductor Manufacturer Skill

## MPN Structure

Torex MPNs follow this general structure:

```
[PREFIX][SERIES][PACKAGE][VOLTAGE][OPTION][SUFFIX]
   |       |        |        |        |       |
   |       |        |        |        |       +-- MR/TR = Tape/Reel
   |       |        |        |        +-- Optional grade letter
   |       |        |        +-- 2-3 digit voltage code (e.g., 332 = 3.3V)
   |       |        +-- Package letter (P, A, B, N, etc.)
   |       +-- 4-digit series (e.g., 6206, 9265)
   +-- XC = Torex prefix
```

### Example Decoding

```
XC6206P332MR
||  | |  |||
||  | |  ||+-- R = Reel packaging
||  | |  |+-- M = Metal reel / USP package suffix
||  | |  +-- 332 = 3.3V output (3.32V)
||  | +-- P = SOT-23-5 package
||  +-- 6206 = LDO regulator series
|+-- XC = Torex prefix
+-- LDO regulator

XC9265A33AMR
||  | | | ||
||  | | | |+-- R = Reel
||  | | | +-- M = Metal reel
||  | | +-- A = Grade/option
||  | +-- 33 = 3.3V output
||  +-- A = SOT-23 package
|+-- XC = Torex prefix
+-- DC-DC converter series

XC61CN
||  ||
||  |+-- N = SOT-89-5 package (from second letter)
||  +-- C = Type/variant
|+-- XC = Torex prefix
+-- Voltage detector, short format MPN
```

---

## Package Codes

### Standard Package Letters

| Code | Package | Pin Count | Notes |
|------|---------|-----------|-------|
| A | SOT-23 | 3-6 | Standard small outline |
| B | SOT-89 | 3 | Medium power |
| C | SOT-25 | 5 | SOT-23 variant |
| D | DFN | Various | Dual flat no-lead |
| N | SOT-89-5 | 5 | 5-pin SOT-89 |
| P | SOT-23-5 | 5 | 5-pin SOT-23 |
| R | SOT-25 | 5 | SOT-25 variant |
| S | SOT-353 | 5 | Small outline |
| T | TSOT-5 | 5 | Thin SOT |

### Reel/Suffix Codes

| Code | Meaning | Notes |
|------|---------|-------|
| MR | USP + Metal reel | Ultra Small Package |
| TR | Tape and reel | Standard tape/reel |
| NR | SOT-89-5 + Reel | Variant |
| DR | DFN + Reel | DFN package variant |

---

## Product Lines

### XC62xx - LDO Regulators

| Series | Description | Features |
|--------|-------------|----------|
| XC6206 | Ultra-low quiescent LDO | 1uA Iq, 200mA output |
| XC6210 | Low dropout LDO | Higher current |
| XC6220 | High accuracy LDO | Tight regulation |

### XC63xx - High Current LDOs

| Series | Description | Output Current |
|--------|-------------|----------------|
| XC63xx | High current LDO | 500mA+ |

### XC64xx - Low Noise LDOs

| Series | Description | Features |
|--------|-------------|----------|
| XC64xx | Low noise LDO | For sensitive analog |

### XC61xx - Voltage Detectors / Reset ICs

| Series | Description | Function |
|--------|-------------|----------|
| XC6119 | Voltage detector | Reset IC |
| XC61CN | Voltage detector | Short form MPN |
| XC61xx | Supervisor ICs | Power monitoring |

### XC68xx - Battery Chargers

| Series | Description | Chemistry |
|--------|-------------|-----------|
| XC6802 | Li-ion charger | Single cell |
| XC6808 | Li-ion charger | Advanced features |

### XC81xx - Load Switches

| Series | Description | Features |
|--------|-------------|----------|
| XC8107 | High-side load switch | Low Ron |
| XC8109 | Load switch | Over-current protection |

### XC91xx - DC-DC Converters

| Series | Description | Type |
|--------|-------------|------|
| XC9142 | DC-DC converter | Step-down |
| XC91xx | Switching regulators | Various |

### XC92xx - DC-DC Converters (Step-down/Step-up)

| Series | Description | Type |
|--------|-------------|------|
| XC9265 | Step-down DC-DC | Buck converter |
| XC9235 | Synchronous buck | High efficiency |

### XC93xx - High Efficiency DC-DC Converters

| Series | Description | Efficiency |
|--------|-------------|------------|
| XC93xx | High efficiency | >90% typical |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Torex package code is the SINGLE LETTER immediately after 4-digit part number
// Pattern: XC[0-9]{4}[PACKAGE-LETTER][VOLTAGE][OPTIONS][SUFFIX]
// Example: XC6206P332MR -> P -> SOT-23-5

// MR/TR at end are tape/reel indicators, NOT package codes
Pattern standardPattern = Pattern.compile("^XC[0-9]{4}([A-Z]).*$");

// Short form like XC61CN - second letter may be package
Pattern shortPattern = Pattern.compile("^XC6[0-9]([A-Z]{2}).*$");
```

### Voltage Code Extraction

```java
// Voltage code is 2-3 digits after package letter
// 332 = 3.32V, 33 = 3.3V, 25 = 2.5V
Pattern voltagePattern = Pattern.compile("^XC[0-9]{4}[A-Z]([0-9]{2,3})[A-Z]?.*$");

public String extractVoltageCode(String mpn) {
    // XC6206P332MR -> 332 -> 3.3V
    Matcher matcher = voltagePattern.matcher(mpn);
    if (matcher.matches()) {
        return matcher.group(1);
    }
    return "";
}
```

### Series Extraction

```java
// Standard format: XC[0-9]{4} -> first 4 chars after XC
// Returns XC62, XC91, XC92, XC61, etc.
if (upperMpn.matches("^XC[0-9]{4}.*")) {
    return upperMpn.substring(0, 4);  // XC62, XC91, etc.
}

// Short format: XC6[0-9][A-Z]{2} -> first 4 chars
if (upperMpn.matches("^XC6[0-9][A-Z]{2}.*")) {
    return upperMpn.substring(0, 4);
}
```

### Product Type Detection

```java
public boolean isLDO(String mpn) {
    return mpn.matches("^XC6[234][0-9]{2}.*");  // XC62xx, XC63xx, XC64xx
}

public boolean isDCDCConverter(String mpn) {
    return mpn.matches("^XC9[123][0-9]{2}.*");  // XC91xx, XC92xx, XC93xx
}

public boolean isVoltageDetector(String mpn) {
    return mpn.matches("^XC61[0-9]{2}.*") ||    // XC61xx
           mpn.matches("^XC61[A-Z]{2}.*");      // XC61CN short form
}

public boolean isBatteryCharger(String mpn) {
    return mpn.matches("^XC68[0-9]{2}.*");      // XC68xx
}

public boolean isLoadSwitch(String mpn) {
    return mpn.matches("^XC81[0-9]{2}.*");      // XC81xx
}
```

---

## Related Files

- Handler: `manufacturers/TorexHandler.java`
- Component types: `IC`, `VOLTAGE_REGULATOR`
- Test file: `handlers/TorexHandlerTest.java`

---

## Learnings & Edge Cases

- **Ultra-low quiescent current**: XC6206 is famous for 1uA Iq, popular in battery applications
- **Package letter is SINGLE character**: P, A, B, N etc. immediately after 4-digit series number
- **Voltage code encoding**: 332 = 3.32V, 30 = 3.0V, 25 = 2.5V (first 2 digits are major.minor)
- **Short form MPNs**: XC61CN uses letter codes instead of numeric series (CN = variant+package)
- **MR suffix confusion**: MR means Metal Reel + USP package, not just tape/reel
- **Voltage detectors (XC61xx)**: These are reset ICs/supervisors, classified as voltage regulators
- **Load switches (XC81xx)**: Power distribution switches with protection features
- **No LED driver support**: Unlike other PMIC vendors, Torex handler doesn't include LED drivers

<!-- Add new learnings above this line -->
