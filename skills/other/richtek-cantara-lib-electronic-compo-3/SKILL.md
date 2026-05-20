---
name: richtek
description: Richtek Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Richtek power management ICs.
---

# Richtek Technology Manufacturer Skill

## MPN Structure

Richtek MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][PACKAGE][SUFFIX]
   |       |        |        |       |
   |       |        |        |       +-- Optional: -TR (Tape/Reel), -E (RoHS)
   |       |        |        +-- Package code (2-3 letters): GQW, GSP, GB
   |       |        +-- Optional variant or voltage code
   |       +-- 4-digit series number (e.g., 8059, 9013)
   +-- RT or RTQ (automotive grade)
```

### Example Decoding

```
RT8059GQW
||  | |||
||  | ||+-- W = Part of QFN suffix
||  | |+-- Q = QFN package indicator
||  | +-- G = Package code start
||  +-- 8059 = DC-DC converter series
|+-- RT = Richtek prefix
+-- Standard industrial grade

RT9013-33GB
||  | || ||
||  | || |+-- B = SOT-23-5 package suffix
||  | || +-- G = Package code start
||  | |+-- 33 = 3.3V voltage code
||  | +-- Hyphen separates voltage
||  +-- 9013 = LDO series
|+-- RT = Richtek prefix
+-- Standard grade

RTQ2106GQW
|||  | |||
|||  | ||+-- W = Part of QFN suffix
|||  | |+-- Q = QFN indicator
|||  | +-- G = Package start
|||  +-- 2106 = Part number
||+-- Q = Automotive grade (AEC-Q100)
|+-- RT = Richtek
+-- Automotive qualified
```

---

## Package Codes

### QFN Packages

| Code | Package | Notes |
|------|---------|-------|
| GQW | QFN | Standard QFN |
| PQW | QFN | QFN variant |
| GQ | QFN | Compact QFN |
| GW | QFN | QFN variant |

### WLCSP Packages

| Code | Package | Notes |
|------|---------|-------|
| GSP | WLCSP | Wafer-level chip scale |
| GS | WLCSP | WLCSP variant |

### SOT-23 Packages

| Code | Package | Notes |
|------|---------|-------|
| GB | SOT-23-5 | 5-pin SOT-23 |
| GE | SOT-23-6 | 6-pin SOT-23 |
| GT | SOT-23-3 | 3-pin SOT-23 |

### DFN Packages

| Code | Package | Notes |
|------|---------|-------|
| GD | DFN | Standard DFN |
| GF | DFN | DFN variant |

### SOP/SOIC Packages

| Code | Package | Notes |
|------|---------|-------|
| SP | SOP-8 | 8-pin SOP |
| SA | SOIC-8 | 8-pin SOIC |
| SE | SOIC-8 | SOIC variant |

### TSSOP Packages

| Code | Package | Notes |
|------|---------|-------|
| TP | TSSOP | Standard TSSOP |
| TS | TSSOP | TSSOP variant |

### MSOP Packages

| Code | Package | Notes |
|------|---------|-------|
| MS | MSOP | Standard MSOP |
| MF | MSOP-8 | 8-pin MSOP |

---

## Product Lines

### RT4xxx - LED Drivers / Backlight Controllers

| Series | Description | Application |
|--------|-------------|-------------|
| RT4831 | LED Backlight Driver | LCD panel backlighting |
| RT4801 | LED Driver | Display backlighting |
| RT4xxx | General LED drivers | LED lighting control |

### RT5xxx - DC-DC Converters

| Series | Description | Output |
|--------|-------------|--------|
| RT5785 | Step-down DC-DC | Various |
| RT5749 | Buck converter | Various |

### RT6xxx - High-Efficiency DC-DC Converters

| Series | Description | Efficiency |
|--------|-------------|------------|
| RT6150 | High-efficiency buck | >90% |
| RT6160 | Synchronous buck | High efficiency |

### RT8xxx - DC-DC Converters / LED Drivers

| Subseries | Type | Notes |
|-----------|------|-------|
| RT80xx-RT83xx | DC-DC converters | Step-down |
| RT84xx | LED drivers | Backlight |
| RT85xx | LED drivers | Display |
| RT86xx-RT89xx | DC-DC converters | Various |

### RT9xxx - LDO / Linear Regulators

| Series | Description | Features |
|--------|-------------|----------|
| RT9013 | 500mA LDO | Ultra-low noise |
| RT9193 | 300mA LDO | Low dropout |
| RT9058 | LDO | General purpose |
| RT945x | Battery chargers | Li-ion/Li-Po |
| RT946x | Battery chargers | Fast charging |

### RTQ Series - Automotive Grade

| Series | Description | Qualification |
|--------|-------------|---------------|
| RTQxxxx | Automotive versions | AEC-Q100 qualified |
| RTQ2106 | Automotive DC-DC | Extended temp |
| RTQ6360 | Automotive buck | -40C to +125C |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Richtek package codes are typically 2-3 letters after the part number
// Pattern: RT[Q]?[0-9]{4}[package-letters]...
// Examples: RT8059GQW -> GQW -> QFN
//           RT9013-33GB -> GB -> SOT-23-5

// Handle voltage code in middle (e.g., RT9013-33GB)
// Pattern: RT[0-9]{4}-[0-9]{2}[package]
Pattern voltagePattern = Pattern.compile("^RT[0-9]{4}-[0-9]{2}([A-Z]{2,3})$");
```

### Series Extraction

```java
// RTQ series returns "RTQ"
// Standard RT[4-9]xxx returns "RT4", "RT5", "RT6", "RT8", "RT9"
if (upperMpn.startsWith("RTQ")) {
    return "RTQ";
}
if (upperMpn.matches("^RT[4-9][0-9]{3}.*")) {
    return upperMpn.substring(0, 3);  // RT4, RT5, RT6, RT8, RT9
}
```

### LED Driver vs Voltage Regulator Detection

```java
// LED Drivers: RT4xxx, RT84xx, RT85xx
// Voltage Regulators: RT5xxx, RT6xxx, RT8[0-367-9]xx, RT9xxx

private boolean isLEDDriver(String mpn) {
    return mpn.matches("^RT4[0-9]{3}.*") ||      // RT4xxx
           mpn.matches("^RT8[45][0-9]{2}.*") ||   // RT84xx, RT85xx
           mpn.matches("^RTQ4[0-9]{3}.*") ||      // RTQ4xxx
           mpn.matches("^RTQ8[45][0-9]{2}.*");    // RTQ84xx, RTQ85xx
}
```

### Automotive Grade Detection

```java
// RTQ prefix indicates AEC-Q100 automotive qualification
// Also check for -AEC suffix
public boolean isAutomotiveGrade(String mpn) {
    String upper = mpn.toUpperCase();
    return upper.startsWith("RTQ") || upper.contains("-AEC");
}
```

### Automotive Equivalents

```java
// RTQ6150 is automotive version of RT6150
// Check for equivalent parts with/without Q
private boolean areEquivalentParts(String mpn1, String mpn2) {
    // RTQ6150 <-> RT6150
    if (mpn1.startsWith("RTQ") && mpn2.startsWith("RT") && !mpn2.startsWith("RTQ")) {
        String num1 = mpn1.substring(3, 7);  // 4-digit from RTQxxxx
        String num2 = mpn2.substring(2, 6);  // 4-digit from RTxxxx
        return num1.equals(num2);
    }
}
```

---

## Related Files

- Handler: `manufacturers/RichtekHandler.java`
- Component types: `IC`, `VOLTAGE_REGULATOR`, `LED_DRIVER`
- Test file: `handlers/RichtekHandlerTest.java`

---

## Learnings & Edge Cases

- **RT84xx/RT85xx are LED drivers**, not DC-DC converters like other RT8xxx parts
- **RTQ prefix indicates AEC-Q100 automotive qualification** - same part number with RTQ vs RT are equivalent except for temperature rating
- **Voltage code in MPN**: Parts like RT9013-33GB have voltage (33=3.3V) embedded between part number and package
- **Battery chargers**: RT945x and RT946x are battery charger ICs, classified as voltage regulators
- **Package suffix structure**: Package codes start with G, P, S, M, T followed by package-specific letters
- **Tape and reel suffixes**: -TR, -E, -RL, -REEL should be stripped before package extraction

<!-- Add new learnings above this line -->
