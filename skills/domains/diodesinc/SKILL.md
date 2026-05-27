---
name: diodesinc
description: Diodes Incorporated MPN encoding patterns, package codes, and handler guidance. Use when working with Diodes Inc MOSFETs, diodes, transistors, voltage regulators, or DiodesIncHandler.
---

# Diodes Incorporated Manufacturer Skill

## Company Overview

Diodes Incorporated is a global manufacturer specializing in discrete semiconductors and analog/mixed-signal ICs. The company acquired Zetex Semiconductors (2008) and Pericom Semiconductor (2015), inheriting their product lines and part numbering conventions. Key product families include:

- **Discrete diodes**: Signal, Schottky, Zener, TVS
- **MOSFETs**: N-channel and P-channel in various packages
- **Transistors**: Small signal BJTs and digital transistors
- **Voltage regulators**: Linear regulators, LDOs, DC-DC converters
- **LED drivers**: Constant current drivers
- **Interface ICs**: USB switches, level translators

---

## MPN Structure by Product Family

### MOSFETs - DMN/DMP Series (Diodes Inc Native)

```
DM[CHANNEL][SPECS][PACKAGE]
 |    |       |       |
 |    |       |       +-- Package suffix (U=SOT23, T=SOT223, L=DPAK, F=TO220)
 |    |       +-- Voltage/current specs (encoded in digits)
 |    +-- N=N-channel, P=P-channel
 +-- DM = Diodes Inc MOSFET
```

**Examples:**
- DMN2075U = N-channel, SOT-23, 20V, 7.5A
- DMP3056LDM = P-channel, DPAK, 30V, 5.6A
- DMN6040SSD = N-channel, PowerDI5060, 60V, 4A

### MOSFETs - ZXMN/ZXMP Series (Zetex Legacy)

```
ZXM[CHANNEL][SPECS][SUFFIX]
 |     |       |       |
 |     |       |       +-- Package/variant suffix
 |     |       +-- Voltage/current specifications
 |     +-- N=N-channel, P=P-channel
 +-- ZXM = Zetex MOSFET
```

**Examples:**
- ZXMN2B01FH = N-channel, SOT23, 20V
- ZXMN10A07F = N-channel, SOT23, 100V
- ZXMP3A13DN8 = P-channel, SOIC-8, 30V

---

### Transistors - MMBT Series (Small Signal)

```
MMBT[BASE][SUFFIX]
  |    |      |
  |    |      +-- Grade/packaging suffix (L=low, T1=tape & reel)
  |    +-- Equivalent 2N series number (e.g., 2222, 3904)
  +-- MMBT = Surface mount bipolar transistor (SOT-23)
```

**Examples:**
- MMBT2222A = NPN, SOT-23, equivalent to 2N2222A
- MMBT3904 = NPN, SOT-23, general purpose
- MMBT3906 = PNP, SOT-23, general purpose
- MMBT4401 = NPN, SOT-23, 40V
- MMBT4403 = PNP, SOT-23, 40V

### Transistors - FMMT Series (RF/High Performance)

```
FMMT[CODE][SUFFIX]
  |    |      |
  |    |      +-- Grade/variant suffix
  |    +-- Device code
  +-- FMMT = Fast/Medium power transistor
```

**Examples:**
- FMMT458 = NPN, high voltage, SOT-23
- FMMT491 = PNP, high gain
- FMMT617 = NPN, RF transistor

### Transistors - ZXT/DTA/DTB Series (Digital Transistors)

Digital transistors have built-in base resistors.

```
ZXT[CODE][SUFFIX]    or    DT[TYPE][CODE][SUFFIX]
 |    |      |              |   |     |      |
 |    |      +-- Package    |   |     |      +-- Package
 |    +-- Device code       |   |     +-- Resistance code
 |                          |   +-- A=NPN, B=PNP
 +-- ZXT = Zetex digital    +-- DT = Digital transistor
```

**Examples:**
- ZXT10600E6 = Digital transistor, SC-70
- DTA114ECA = NPN, 10k+10k resistors, SOT-23
- DTB123ECA = PNP, 2.2k+2.2k resistors, SOT-23

---

### Diodes - 1N Series (General Purpose)

```
1N[CODE][SUFFIX]
 |   |      |
 |   |      +-- Grade suffix (A, B, etc.)
 |   +-- JEDEC registration number
 +-- 1N = JEDEC diode prefix
```

**Examples:**
- 1N4148 = High-speed signal diode
- 1N4001 = 50V, 1A rectifier
- 1N4007 = 1000V, 1A rectifier
- 1N5819 = Schottky, 40V, 1A

### Diodes - BAV/BAS Series (Signal Diodes)

```
BA[V/S][CODE][SUFFIX]
 |  |    |      |
 |  |    |      +-- Variant suffix
 |  |    +-- Device code
 |  +-- V=general signal, S=small signal
 +-- BA = European signal diode prefix
```

**Examples:**
- BAV19 = High-speed switching diode
- BAV20 = High-speed switching diode
- BAV21 = High-speed switching diode
- BAS16 = High-speed switching diode, SOT-23
- BAS21 = High-speed switching diode, SOT-23

### Diodes - SBR Series (Schottky Rectifiers)

```
SBR[CURRENT][VOLTAGE][SUFFIX]
 |     |        |        |
 |     |        |        +-- Package/variant
 |     |        +-- Voltage / 10 (e.g., 04=40V)
 |     +-- Current rating in Amps
 +-- SBR = Schottky Barrier Rectifier
```

**Examples:**
- SBR10U40CT = 10A, 40V, TO-220
- SBR20A100CT = 20A, 100V, TO-220
- SBR3U30LP = 3A, 30V, TO-277

### Diodes - BZX Series (Zener Diodes)

```
BZX[POWER][C][VOLTAGE][SUFFIX]
 |    |    |     |        |
 |    |    |     |        +-- Voltage variant
 |    |    |     +-- Zener voltage code
 |    |    +-- C = precision
 |    +-- Power code (84=500mW, 79=500mW)
 +-- BZX = European Zener prefix
```

**Examples:**
- BZX84C5V1 = 5.1V Zener, 300mW, SOT-23
- BZX84C12 = 12V Zener, 300mW, SOT-23
- BZX79C6V2 = 6.2V Zener, 500mW, DO-35

### Diodes - MMSZ Series (Surface Mount Zener)

```
MMSZ[VOLTAGE][SUFFIX]
  |     |        |
  |     |        +-- Package variant (T1=SOD-123)
  |     +-- Zener voltage (e.g., 5V1 = 5.1V)
  +-- MMSZ = Miniature Melf Surface Mount Zener
```

**Examples:**
- MMSZ5231B = 5.1V Zener, SOD-123
- MMSZ5242B = 12V Zener, SOD-123
- MMSZ4689 = 5.1V Zener (1N series numbering)

### Diodes - DMXX Series (Dual/Surface Mount)

```
DMX[X][CODE][SUFFIX]
  |  |   |      |
  |  |   |      +-- Package variant
  |  |   +-- Device code
  |  +-- X variant
  +-- DMX = Diodes Inc surface mount dual diodes
```

**Examples:**
- DMXX = Dual surface mount diode series

### Diodes - MMBD Series (Dual Diodes)

```
MMBD[CODE][SUFFIX]
  |    |      |
  |    |      +-- Package variant
  |    +-- Device configuration code
  +-- MMBD = Surface mount dual diode
```

**Examples:**
- MMBD4148 = Dual 1N4148 equivalent, SOT-23
- MMBD914 = Dual 1N914 equivalent, SOT-23

---

### Voltage Regulators - AP Series (Linear Regulators)

```
AP[CODE][VARIANT][PACKAGE]
 |   |      |        |
 |   |      |        +-- Package suffix
 |   |      +-- Variant/voltage code
 |   +-- Device family code
 +-- AP = Analog Products (voltage regulator)
```

**Examples:**
- AP1117 = 1A LDO regulator series
- AP2112K-3.3 = 600mA LDO, 3.3V output
- AP7333 = 300mA LDO, low quiescent current

### Voltage Regulators - AZ Series (LDO Regulators)

```
AZ[CODE][VARIANT][PACKAGE]
 |   |      |        |
 |   |      |        +-- Package suffix
 |   |      +-- Variant code
 |   +-- Device family code
 +-- AZ = Advanced Zener/LDO regulators
```

**Examples:**
- AZ1117CH-3.3TRG1 = 800mA LDO, 3.3V, SOT-223, tape & reel
- AZ1084D2-3.3 = 5A LDO, 3.3V, TO-263

### Voltage Regulators - PAM Series (DC-DC Converters)

```
PAM[CODE][VARIANT][PACKAGE]
 |    |      |        |
 |    |      |        +-- Package suffix
 |    |      +-- Feature variant
 |    +-- Device code
 +-- PAM = Power Analog Module
```

**Examples:**
- PAM2305AAB120 = DC-DC step-down, 1A, 1.2V
- PAM8403 = Audio amplifier IC
- PAM8610 = Class-D audio amplifier

---

### LED Drivers - AL Series

```
AL[CODE][VARIANT][PACKAGE]
 |   |      |        |
 |   |      |        +-- Package suffix
 |   |      +-- Feature variant
 |   +-- Device code
 +-- AL = Analog LED driver
```

**Examples:**
- AL8805 = Buck LED driver, 40V, 1A
- AL8807 = Buck LED driver, 36V, 500mA

### Interface ICs - PI Series

```
PI[CODE][VARIANT][PACKAGE]
 |   |      |        |
 |   |      |        +-- Package suffix
 |   |      +-- Feature variant
 |   +-- Device code
 +-- PI = Pericom Interface IC
```

**Examples:**
- PI3USB30532 = USB 3.0 switch
- PI3EQX = PCIe/USB ReDriver ICs

---

## Package Codes

### MOSFET Package Extraction (from handler)

| Suffix | Package | Notes |
|--------|---------|-------|
| U | SOT-23 | Small outline |
| T | SOT-223 | Power small outline |
| L | TO-252 (DPAK) | Medium power SMD |
| F | TO-220 | Through-hole power |

### Common Packages

| Package | Description | Typical Use |
|---------|-------------|-------------|
| SOT-23 | 3-pin small outline | Signal transistors, small MOSFETs |
| SOT-223 | 4-pin power SOT | Medium current regulators |
| TO-252 (DPAK) | Power SMD | MOSFETs, regulators |
| TO-220 | 3-pin through-hole | Power MOSFETs, regulators |
| SOD-123 | Small outline diode | SMD Zener/signal diodes |
| DO-35 | Axial glass | Small signal diodes |
| DO-41 | Axial | Standard rectifiers |

---

## Supported Component Types

From `DiodesIncHandler.getSupportedTypes()`:

| Component Type | Description |
|----------------|-------------|
| MOSFET | General MOSFETs |
| MOSFET_DIODES | Diodes Inc branded MOSFETs |
| VOLTAGE_REGULATOR | General voltage regulators |
| VOLTAGE_REGULATOR_DIODES | Diodes Inc branded regulators |
| LED_DRIVER_DIODES | Diodes Inc LED drivers |
| LOGIC_IC_DIODES | Diodes Inc logic ICs |
| HALL_SENSOR_DIODES | Diodes Inc Hall effect sensors |

**Note**: Handler declares types for Hall sensors, LED drivers, Logic ICs but currently only registers patterns for DIODE, MOSFET, TRANSISTOR, VOLTAGE_REGULATOR, and IC component types.

---

## Series Extraction

The handler extracts series based on prefix matching:

| Prefix | Returns | Component Type |
|--------|---------|----------------|
| DMN | "DMN Series" | N-channel MOSFET |
| DMP | "DMP Series" | P-channel MOSFET |
| ZXMN | "ZXMN Series" | N-channel MOSFET (Zetex) |
| ZXMP | "ZXMP Series" | P-channel MOSFET (Zetex) |
| MMBT | "MMBT Series" | SMD transistor |
| FMMT | "FMMT Series" | RF/fast transistor |
| ZXT | "ZXT Series" | Digital transistor |
| DTA | "DTA Series" | NPN digital transistor |
| DTB | "DTB Series" | PNP digital transistor |
| BAV | "BAV Series" | Signal diode |
| BAS | "BAS Series" | Small signal diode |
| SBR | "SBR Series" | Schottky rectifier |
| BZX | "BZX Series" | Zener diode |
| AP | "AP Series" | Linear regulator |
| AZ | "AZ Series" | LDO regulator |
| PAM | "PAM Series" | DC-DC converter |
| AL | "AL Series" | LED driver |
| PI | "PI Series" | Interface IC |

---

## Official Replacement Cross-References

The handler defines these replacement pairs:

| Part | Replacement | Notes |
|------|-------------|-------|
| BAV19 | BAV20 | Compatible signal diodes |
| ZXMN | DMN | Zetex to Diodes Inc migration |
| ZXMP | DMP | Zetex to Diodes Inc migration |

---

## Handler Implementation Notes

### Current Issues in DiodesIncHandler

1. **HashSet usage** (line 64): Uses mutable `HashSet` instead of `Set.of()` for immutability
2. **Type declaration mismatch**: Declares HALL_SENSOR_DIODES, LED_DRIVER_DIODES, LOGIC_IC_DIODES in `getSupportedTypes()` but does not register patterns for corresponding base types
3. **Missing DIODE in getSupportedTypes()**: Registers many DIODE patterns but doesn't include base DIODE type in supported types
4. **Missing TRANSISTOR in getSupportedTypes()**: Registers transistor patterns but doesn't include TRANSISTOR type
5. **Limited package extraction**: Only handles DMN/DMP and ZX prefixes, missing other series

### Missing Patterns

The handler does not currently register patterns for:
- Hall effect sensors (no AH series patterns)
- Logic ICs (only PI series for interface ICs)
- Additional LED driver patterns beyond AL series

### Recommended Fixes

```java
// 1. Change getSupportedTypes() to use Set.of()
@Override
public Set<ComponentType> getSupportedTypes() {
    return Set.of(
        ComponentType.DIODE,
        ComponentType.MOSFET,
        ComponentType.MOSFET_DIODES,
        ComponentType.TRANSISTOR,
        ComponentType.VOLTAGE_REGULATOR,
        ComponentType.VOLTAGE_REGULATOR_DIODES,
        ComponentType.LED_DRIVER_DIODES,
        ComponentType.LOGIC_IC_DIODES,
        ComponentType.HALL_SENSOR_DIODES,
        ComponentType.IC
    );
}

// 2. Add Hall sensor patterns
registry.addPattern(ComponentType.HALL_SENSOR, "^AH[0-9].*");  // Hall sensors
registry.addPattern(ComponentType.HALL_SENSOR_DIODES, "^AH[0-9].*");

// 3. Improve package extraction for more series
if (upperMpn.startsWith("MMBT")) return "SOT-23";
if (upperMpn.startsWith("BZX84")) return "SOT-23";
if (upperMpn.startsWith("MMSZ")) return "SOD-123";
if (upperMpn.startsWith("1N")) return "DO-41";
```

---

## Example MPNs with Full Decoding

### DMN2075U (N-channel MOSFET)
```
DMN2075U
│  │   │
│  │   └── U = SOT-23 package
│  └── 2075 = 20V, 7.5A specs
└── DMN = Diodes Inc N-channel MOSFET
```

### MMBT3904LT1G (NPN Transistor)
```
MMBT3904LT1G
│     │  │││
│     │  ││└── G = Green/RoHS
│     │  │└── T1 = Tape & reel
│     │  └── L = Low saturation variant
│     └── 3904 = equivalent to 2N3904
└── MMBT = Surface mount bipolar transistor (SOT-23)
```

### BZX84C5V1-7-F (Zener Diode)
```
BZX84C5V1-7-F
│  │ ││  │ │
│  │ ││  │ └── F = Automotive grade
│  │ ││  └── 7 = Tape orientation code
│  │ │└── 5V1 = 5.1V Zener voltage
│  │ └── C = Precision grade
│  └── 84 = 300mW power rating
└── BZX = European Zener diode prefix
```

### AP2112K-3.3TRG1 (LDO Regulator)
```
AP2112K-3.3TRG1
│  │   │ │  │││
│  │   │ │  ││└── G1 = Lead-free version
│  │   │ │  │└── R = Tape & reel
│  │   │ │  └── T = SOT-23-5 package
│  │   │ └── 3.3 = 3.3V output voltage
│  │   └── K = Version with enable pin
│  └── 2112 = 600mA LDO series
└── AP = Analog Products (voltage regulator)
```

---

## Related Files

- Handler: `manufacturers/DiodesIncHandler.java`
- Component types: `MOSFET_DIODES`, `VOLTAGE_REGULATOR_DIODES`, `LED_DRIVER_DIODES`, `LOGIC_IC_DIODES`, `HALL_SENSOR_DIODES`

---

## Learnings & Edge Cases

- **Zetex acquisition**: Diodes Inc acquired Zetex in 2008, inheriting ZXMN/ZXMP MOSFET nomenclature
- **Pericom acquisition**: Diodes Inc acquired Pericom in 2015, inheriting PI interface IC series
- **JEDEC standards**: 1N prefix and 2N prefix follow JEDEC numbering (no encoded specs in number)
- **European prefixes**: BA, BZ prefixes follow European Pro Electron naming conventions
- **Package suffix position**: For DMN/DMP series, package code comes after last digit; for ZETEX parts, it varies
- **BAV19/BAV20 interchangeability**: These are considered compatible signal diodes by the handler
- **ZXMN to DMN migration**: Handler recognizes Zetex ZXMN series as equivalent to Diodes Inc DMN series

<!-- Add new learnings above this line -->
