---
name: rubycon
description: Rubycon Corporation MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Rubycon aluminum electrolytic capacitors.
---

# Rubycon Corporation Manufacturer Skill

## MPN Structure

Rubycon uses multiple MPN formats depending on the series:

### Format 1: Letter-prefix series (ZLH, YXF, MCZ)
```
[SERIES][VOLTAGE]V[SUFFIX][CAP_CODE][TOL][PACKAGE]
   |       |         |        |      |      |
   |       |         |        |      |      +-- Dimensions (08X12=8x12mm)
   |       |         |        |      +-- Tolerance (M=20%)
   |       |         |        +-- 3-digit capacitance code
   |       |         +-- Optional suffix (B, etc.)
   |       +-- Voltage in V
   +-- Series code (ZLH, YXF, YXG, MCZ, etc.)
```

### Format 2: Voltage-prefix series (PK, PL)
```
[VOLTAGE][SERIES][CAP][TOL][SUFFIX][PACKAGE]
    |        |     |    |     |        |
    |        |     |    |     |        +-- Dimensions (10X20)
    |        |     |    |     +-- Suffix (EFC, etc.)
    |        |     |    +-- Tolerance (M=20%)
    |        |     +-- Capacitance value (direct or code)
    |        +-- Series (PK, PL)
    +-- Voltage in V
```

### Example Decoding

```
ZLH35VB221M08X12
|  | |  |  | |
|  | |  |  | +-- Package: 8x12mm
|  | |  |  +-- M = +/-20% tolerance
|  | |  +-- 221 = 220uF (22 x 10^1)
|  | +-- B suffix
|  +-- 35V
+-- ZLH = Low Impedance series

16PK1000MEFC10X20
| |   |  |   |
| |   |  |   +-- Package: 10x20mm
| |   |  +-- EFC suffix
| |   +-- M = +/-20% tolerance
| +-- PK = Small Size series
|     1000 = 1000uF (direct value)
+-- 16V

MCZ1V471MNN08F12
|  | |  |  |
|  | |  |  +-- Package: 8x12mm (F separator)
|  | |  +-- MNN suffix
|  | +-- 471 = 470uF (47 x 10^1)
|  +-- 1V = 35V (voltage code)
+-- MCZ = Polymer Hybrid series
```

---

## Series Reference

### Low Impedance Series

| Series | Full Name | Description |
|--------|-----------|-------------|
| ZLH | ZLH Low Impedance | High ripple current, low impedance |
| ZL | ZL Standard | Standard low impedance |
| YXH | YXH Low ESR Miniature | Miniature low ESR |

### Miniature Series

| Series | Full Name | Description |
|--------|-----------|-------------|
| YXF | YXF Miniature | Standard miniature |
| YXG | YXG Miniature Wide Temp | Wide temperature range (-55C to +105C) |
| YXA | YXA High Temperature | High temperature endurance |
| YXJ | YXJ Standard Miniature | Standard miniature |
| YXL | YXL Long Life Miniature | Long life miniature |

### Polymer Series

| Series | Full Name | Description |
|--------|-----------|-------------|
| MCZ | MCZ Polymer Hybrid | Conductive polymer hybrid aluminum |
| MBZ | MBZ Polymer Solid | Conductive polymer solid |
| USP | USP Ultra-Small SMD Polymer | Ultra-small SMD polymer |

### Small Size Series

| Series | Full Name | Description |
|--------|-----------|-------------|
| PK | PK Small Size | Compact aluminum electrolytic |
| PL | PL Small Size Long Life | Compact long life |

### Ultra-Small SMD Series

| Series | Full Name | Description |
|--------|-----------|-------------|
| USR | USR Ultra-Small SMD | Ultra-small SMD standard |
| UST | UST Ultra-Small SMD High Temp | Ultra-small SMD high temperature |

---

## Voltage Codes

### Standard Format (letter-prefix series)

Voltage appears directly after series code: `ZLH35VB` = 35V

### EIA Voltage Codes (MCZ, MBZ series)

| Code | Voltage | Code | Voltage |
|------|---------|------|---------|
| 0E | 2.5V | 1H | 50V |
| 0G | 4V | 1J | 63V |
| 0J | 6.3V | 2A | 100V |
| 1A | 10V | 2C | 160V |
| 1C | 16V | 2D | 200V |
| 1E | 25V | 2E | 250V |
| 1V | 35V | 2G | 400V |
| | | 2W | 450V |

### Prefix Format (PK, PL series)

Voltage is the number prefix: `16PK` = 16V, `25PL` = 25V

---

## Capacitance Codes

Uses standard EIA 3-digit code followed by tolerance letter:

| Code | Value | Calculation |
|------|-------|-------------|
| 100M | 10uF | 10 x 10^0, +/-20% |
| 101M | 100uF | 10 x 10^1, +/-20% |
| 221M | 220uF | 22 x 10^1, +/-20% |
| 471M | 470uF | 47 x 10^1, +/-20% |
| 102M | 1000uF | 10 x 10^2, +/-20% |

### Tolerance Codes

| Code | Tolerance |
|------|-----------|
| M | +/-20% |
| K | +/-10% |
| J | +/-5% |

---

## Package Codes

Rubycon uses dimension notation: `DDxHH` or `DDXHH` format.

| Notation | Dimensions |
|----------|------------|
| 05X11 | 5x11mm |
| 06X07 | 6x7mm |
| 08X12 | 8x12mm |
| 10X16 | 10x16mm |
| 10X20 | 10x20mm |
| 12X20 | 12x20mm |

Some polymer series use F separator: `08F12` = 8x12mm

---

## Handler Implementation Notes

### Pattern Recognition

```java
// ZLH/ZL series - voltage follows series code
"^ZLH[0-9]+.*"   // ZLH35VB...
"^ZL[0-9]+.*"    // ZL25V... (not ZLH)

// YX- series - letter after YX indicates type
"^YX[FG][0-9]+.*"   // YXF, YXG
"^YX[AHJL][0-9]+.*" // YXA, YXH, YXJ, YXL

// MCZ/MBZ series - voltage code after series
"^MCZ[0-9][A-Z].*"  // MCZ1V...
"^MBZ[0-9][A-Z].*"  // MBZ0J...

// PK/PL series - voltage prefix
"^[0-9]+P[KL][0-9]+.*"  // 16PK1000...

// US- series - ultra small SMD
"^US[RTP][0-9]+.*"  // USR, UST, USP
```

### Voltage Extraction

```java
// ZLH/YX series: extract digits between series and V
// ZLH35VB -> 35V
Pattern.compile("^(?:ZLH|ZL|YX[FGAHJL])([0-9]+)V");

// MCZ/MBZ series: decode voltage code
// MCZ1V -> 35V (1V code)
Pattern.compile("^(?:MCZ|MBZ)([0-9])([A-Z])");

// PK/PL series: extract prefix voltage
// 16PK -> 16V
Pattern.compile("^([0-9]+)P[KL]");
```

### Package Extraction

```java
// Dimension pattern at end of MPN
// 08X12 or 08F12 format
Pattern.compile("([0-9]{2})X([0-9]{2})$");
Pattern.compile("([0-9]{2})F([0-9]{2})$");
```

---

## Replacement Rules

The handler supports these replacement scenarios:

1. **YXG can replace YXF**: Wide temp can replace standard temp (same specs)
2. **PL can replace PK**: Long life can replace standard (same specs)
3. **ZLH can replace ZL**: Low impedance ZLH is higher grade than ZL

All replacements require matching voltage, capacitance, and package.

---

## Related Files

- Handler: `manufacturers/RubyconHandler.java`
- Component types: `CAPACITOR`
- Supported types: CAPACITOR, IC

---

## Learnings & Edge Cases

- **Voltage format varies by series**: ZLH/YX use direct voltage (35V), MCZ uses code (1V=35V), PK uses prefix (16PK)
- **Series detection order**: Check ZLH before ZL (ZLH starts with ZL)
- **Package separator**: Most use X (08X12), polymer may use F (08F12)
- **PK/PL direct values**: May use direct uF value (1000) instead of code (102)
- **YX series differentiation**: Single letter after YX determines series (F, G, A, H, J, L)

<!-- Add new learnings above this line -->
