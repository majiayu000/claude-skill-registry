---
name: elna
description: Elna Company MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Elna audio-grade aluminum electrolytic capacitors and supercapacitors.
---

# Elna Company Manufacturer Skill

## MPN Structure

Elna MPNs follow this general structure for capacitors:

```
[SERIES]-[VOLTAGE]V[CAP_CODE][TOL][PACKAGE]#[SUFFIX]
   |         |        |       |      |        |
   |         |        |       |      |        +-- Optional suffix (P, etc.)
   |         |        |       |      +-- Package code (H3, F5, etc.)
   |         |        |       +-- Tolerance (M=20%)
   |         |        +-- Capacitance code (101=100uF or R notation)
   |         +-- Voltage rating
   +-- Series prefix (RFS, ROA, RE3, etc.)
```

### Example Decoding

```
RFS-25V101MH3#P
|   | |  | | |
|   | |  | | +-- P suffix (packaging option)
|   | |  | +-- H3 = 5x11mm package
|   | |  +-- M = +/-20% tolerance
|   | +-- 101 = 100uF (10 x 10^1)
|   +-- 25V
+-- RFS = Silmic II (premium audio grade)

ROA-50V4R7MF3#
|   | |  | |
|   | |  | +-- F3 = 5x7mm package
|   | |  +-- M = +/-20% tolerance
|   | +-- 4R7 = 4.7uF (R notation)
|   +-- 50V
+-- ROA = TONEREX Type A (audio grade)

DB-5R5D105T
|  | | |  |
|  | | |  +-- T = Radial THT package
|  | | +-- 105 = 1F (10 x 10^5 = 1,000,000uF = 1F)
|  | +-- D suffix (EDLC type)
|  +-- 5R5 = 5.5V (R notation)
+-- DB = Dynacap Standard (supercapacitor/EDLC)
```

---

## Series Reference

### Audio Grade Series

| Series | Name | Description |
|--------|------|-------------|
| RFS | Silmic II | Premium audio-grade, silk fiber separator |
| ROA | TONEREX Type A | High-quality audio capacitor |
| ROB | TONEREX Type B | High-quality audio capacitor |
| CE-BP | CE-BP Audio Crossover | Bi-polar for speaker crossovers |

### Standard Aluminum Electrolytic

| Series | Name | Description |
|--------|------|-------------|
| RE3 | RE3 Standard | General purpose aluminum electrolytic |
| RJ3 | RJ3 Standard | Standard aluminum electrolytic |
| RJH | RJH High Temp | High temperature (105C) |

### Specialized Series

| Series | Name | Description |
|--------|------|-------------|
| RBD | RBD Bi-Polar | Non-polar electrolytic |
| RBI | RBI Bi-Polar | Non-polar electrolytic |
| RSE | RSE Super Low ESR | Ultra-low ESR |
| RVD | RVD Low Leakage | Low leakage current |
| RVE | RVE Low Leakage | Low leakage current |

### Dynacap (EDLC/Supercapacitors)

| Series | Name | Description |
|--------|------|-------------|
| DB | Dynacap Standard | Standard EDLC |
| DX | Dynacap Low Profile | Low profile EDLC |
| DZ | Dynacap Ultra-Low Profile | Ultra-low profile EDLC |

### Legacy/STARGET Series

| Series | Name | Description |
|--------|------|-------------|
| LAO | STARGET Audio | Legacy audio series |
| LAS | STARGET Standard | Legacy standard series |

---

## Capacitance Codes

### EIA 3-Digit Code

| Code | Value | Calculation |
|------|-------|-------------|
| 100 | 10uF | 10 x 10^0 |
| 101 | 100uF | 10 x 10^1 |
| 221 | 220uF | 22 x 10^1 |
| 471 | 470uF | 47 x 10^1 |
| 102 | 1000uF | 10 x 10^2 |

### R Notation (decimal placement)

| Code | Value |
|------|-------|
| 1R0 | 1.0uF |
| 2R2 | 2.2uF |
| 4R7 | 4.7uF |
| 10R | 10uF |
| R47 | 0.47uF |

### Dynacap (high values)

| Code | Value |
|------|-------|
| 105 | 1F (10 x 10^5 uF) |
| 225 | 2.2F |
| 475 | 4.7F |
| 106 | 10F |

---

## Package Codes

### Dimension Codes (R-series)

First letter indicates diameter range, digit indicates height:

| Code | Dimensions | Notes |
|------|------------|-------|
| H3 | 5x11mm | Small radial |
| H5 | 6.3x11mm | Standard radial |
| H7 | 8x11.5mm | Medium radial |
| F3 | 5x7mm | Low profile |
| F5 | 6.3x7mm | Low profile |
| L5 | 10x12.5mm | Large radial |
| L7 | 10x16mm | Large radial tall |
| M5 | 12.5x15mm | Extra large |
| M8 | 12.5x20mm | Extra large tall |
| P5 | 16x25mm | Power |
| P8 | 16x31.5mm | Power tall |
| Q5 | 18x25mm | High power |
| R5 | 22x25mm | Very high power |

### Dynacap Package Suffixes

| Suffix | Package Type |
|--------|-------------|
| T | Radial THT |
| V | Vertical SMD |
| H | Horizontal SMD |
| C | Coin Cell |

---

## Handler Implementation Notes

### Pattern Recognition

```java
// Silmic II series
"^RFS-[0-9]+V[0-9A-Z]+.*"

// TONEREX series
"^RO[AB]-[0-9]+V[0-9A-Z]+.*"

// Standard R-series (RE3, RJ3, RJH, RBD, RBI, RSE, RVD, RVE)
"^R[A-Z]{2}-[0-9]+V.*"

// Dynacap series
"^D[BXZ]-[0-9]+R[0-9]+[A-Z][0-9]+.*"  // With R voltage notation
"^D[BXZ][0-9]+.*"                      // Alternative format

// Legacy STARGET series
"^LA[OS][0-9]+.*"

// CE-BP bi-polar
"^CE-BP.*"
```

### Voltage Extraction

```java
// R-series: extract digits between hyphen and V
// RFS-25V101MH3#P -> 25
int dashIdx = mpn.indexOf('-');
String afterDash = mpn.substring(dashIdx + 1);
int vIdx = afterDash.indexOf('V');
String voltage = afterDash.substring(0, vIdx);  // "25"

// Dynacap: R notation for voltage
// DB-5R5D105T -> 5.5V (5R5)
```

### Capacitance Extraction

```java
// After V, before M (tolerance)
// RFS-25V101MH3#P -> 101 (100uF)
// ROA-50V4R7MF3# -> 4R7 (4.7uF)
int vIdx = mpn.indexOf('V');
String afterV = mpn.substring(vIdx + 1);
int mIdx = afterV.indexOf('M');
String capCode = afterV.substring(0, mIdx);  // "101" or "4R7"
```

### Package Code Extraction

```java
// R-series: 2-char code after M and before #
// RFS-25V101MH3#P -> H3
int mIdx = mpn.indexOf('M');
String suffix = mpn.substring(mIdx + 1);
int hashIdx = suffix.indexOf('#');
String packagePart = hashIdx > 0 ? suffix.substring(0, hashIdx) : suffix;
String packageCode = packagePart.substring(0, 2);  // "H3"
```

---

## Replacement Rules

The handler supports these replacement scenarios:

1. **Silmic II can replace TONEREX**: Higher grade audio capacitor
2. **TONEREX Type A and Type B**: Interchangeable within same specs
3. **Same series**: Compatible if voltage and capacitance match

All replacements require matching voltage and capacitance.

---

## Related Files

- Handler: `manufacturers/ElnaHandler.java`
- Component types: `CAPACITOR`
- Supported types: CAPACITOR, IC

---

## Audio Capacitor Notes

Elna is renowned for audio-grade capacitors. Key characteristics:

1. **Silmic II (RFS)**: Uses silk fiber separator, lowest distortion
2. **TONEREX (ROA/ROB)**: Good balance of performance and cost
3. **CE-BP**: Bi-polar design for speaker crossover networks

Audio capacitors are often specified by:
- Low ESR (Equivalent Series Resistance)
- Low distortion characteristics
- High-quality dielectric materials

---

## Learnings & Edge Cases

- **Hash suffix**: Many Elna MPNs end with `#` or `#P` for packaging options
- **R notation**: Used for decimal values (4R7=4.7, 5R5=5.5)
- **Series pattern**: All R-series use `R[A-Z]{2}-` format
- **Dynacap voltage**: Uses R notation (5R5=5.5V) not standard format
- **Audio grade priority**: Silmic II > TONEREX > Standard for audio quality
- **Bi-polar types**: RBD, RBI, CE-BP are non-polar (no polarity requirement)

<!-- Add new learnings above this line -->
