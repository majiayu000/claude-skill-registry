---
name: lelon
description: Lelon Electronics MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Lelon aluminum electrolytic capacitors.
---

# Lelon Electronics Manufacturer Skill

## MPN Structure

Lelon MPNs follow this general structure:

```
[SERIES]-[CAP_CODE][TOLERANCE][VOLTAGE][TR][PACKAGE]
   |         |         |         |      |      |
   |         |         |         |      |      +-- Package code (0605=6.3x5mm)
   |         |         |         |      +-- TR=Tape and Reel
   |         |         |         +-- Voltage code (1C=16V, 1E=25V)
   |         |         +-- Tolerance (M=20%, K=10%, J=5%)
   |         +-- 3-digit capacitance code (101=100uF)
   +-- Series prefix (VE, VR, VZ, REA, REB, REC, OVZ, OVR)
```

### Example Decoding

```
VE-101M1CTR-0605
|  |  | | |   |
|  |  | | |   +-- Package: 6.3x5mm
|  |  | | +-- TR = Tape and Reel
|  |  | +-- 1C = 16V
|  |  +-- M = +/-20% tolerance
|  +-- 101 = 100uF (10 x 10^1)
+-- VE = Low Impedance series

REA221M1CTR-0810
|  |  | | |   |
|  |  | | |   +-- Package: 8x10mm
|  |  | | +-- TR = Tape and Reel
|  |  | +-- 1C = 16V
|  |  +-- M = +/-20% tolerance
|  +-- 221 = 220uF (22 x 10^1)
+-- REA = Radial Lead series (no hyphen after prefix)
```

---

## Series Reference

### V-Series (with hyphen)

| Series | Description | Application |
|--------|-------------|-------------|
| VE | Low Impedance | Power supply filtering, high ripple current |
| VR | Standard | General purpose applications |
| VZ | High Temperature | Automotive, harsh environments |

### RE-Series (radial lead, no hyphen)

| Series | Description | Application |
|--------|-------------|-------------|
| REA | Radial Lead Type A | Through-hole general purpose |
| REB | Radial Lead Type B | Through-hole standard |
| REC | Radial Lead Type C | Through-hole compact |

### OV-Series (polymer, with hyphen)

| Series | Description | Application |
|--------|-------------|-------------|
| OVZ | Conductive Polymer Z | Long life, high reliability |
| OVR | Conductive Polymer R | High ripple current |

---

## Voltage Codes

Voltage codes appear after capacitance and tolerance codes.

| Code | Voltage | Code | Voltage |
|------|---------|------|---------|
| 0G | 4V | 1H | 50V |
| 0J | 6.3V | 1J | 63V |
| 1A | 10V | 2A | 100V |
| 1C | 16V | 2C | 160V |
| 1E | 25V | 2D | 200V |
| 1V | 35V | 2E | 250V |
| | | 2G | 400V |
| | | 2W | 450V |

---

## Capacitance Codes

Uses 3-digit EIA code for electrolytic capacitors (value in uF):

| Code | Value | Calculation |
|------|-------|-------------|
| 100 | 10uF | 10 x 10^0 |
| 101 | 100uF | 10 x 10^1 |
| 221 | 220uF | 22 x 10^1 |
| 470 | 47uF | 47 x 10^0 |
| 471 | 470uF | 47 x 10^1 |
| 102 | 1000uF | 10 x 10^2 |

---

## Package Codes

Package codes are 4 digits indicating diameter x height in mm (DDLL format):

| Code | Dimensions | Code | Dimensions |
|------|------------|------|------------|
| 0405 | 4x5mm | 1012 | 10x12mm |
| 0505 | 5x5mm | 1016 | 10x16mm |
| 0605 | 6.3x5mm | 1225 | 12.5x25mm |
| 0607 | 6.3x7mm | 1315 | 13x15mm |
| 0810 | 8x10mm | 1620 | 16x20mm |
| 0811 | 8x11mm | 1825 | 18x25mm |

---

## Handler Implementation Notes

### Pattern Recognition

```java
// V-series with hyphen: VE-, VR-, VZ-
"^VE-[0-9]+.*"  // Low impedance
"^VR-[0-9]+.*"  // Standard
"^VZ-[0-9]+.*"  // High temperature

// RE-series without hyphen: REA, REB, REC
"^REA[0-9]+.*"  // Radial lead A
"^REB[0-9]+.*"  // Radial lead B
"^REC[0-9]+.*"  // Radial lead C

// OV-series with hyphen: OVZ-, OVR-
"^OVZ-[0-9]+.*"  // Polymer Z
"^OVR-[0-9]+.*"  // Polymer R
```

### Package Code Extraction

```java
// Package code is the last 4 digits
// VE-101M1CTR-0605 -> 0605 -> 6.3x5mm

// Steps:
// 1. Check last 4 chars for numeric pattern
// 2. Map DDLL to diameter x height
String lastFour = mpn.substring(mpn.length() - 4);
if (lastFour.matches("[0-9]{4}")) {
    // Decode: 06 = 6.3mm diameter, 05 = 5mm height
}
```

### Series Extraction

```java
// Check prefix to determine series type
if (mpn.startsWith("VE-")) return "VE Low Impedance";
if (mpn.startsWith("VR-")) return "VR Standard";
if (mpn.startsWith("VZ-")) return "VZ High Temperature";
if (mpn.startsWith("REA")) return "REA Radial Lead";  // No hyphen
// etc.
```

---

## Replacement Rules

The handler supports these replacement scenarios:

1. **VE can replace VR**: Low impedance can replace standard (better performance)
2. **VZ can replace VR/VE**: High temp can replace standard (wider temp range)
3. **OVZ/OVR can replace VR**: Polymer can replace standard (longer life)

Package dimensions must match for any replacement.

---

## Related Files

- Handler: `manufacturers/LelonHandler.java`
- Component types: `CAPACITOR`
- Supported types: CAPACITOR, IC

---

## Learnings & Edge Cases

- **Hyphen placement**: V-series and OV-series use hyphen after prefix (VE-), but RE-series does not (REA)
- **Package code position**: Always the last 4 digits of the MPN
- **Voltage code position**: After capacitance (3 digits) and tolerance (1 letter)
- **Tolerance codes**: M=20% (most common), K=10%, J=5%
- **TR suffix**: Indicates tape and reel packaging

<!-- Add new learnings above this line -->
