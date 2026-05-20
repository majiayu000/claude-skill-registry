---
name: onsemi
description: ON Semiconductor (onsemi) MPN encoding patterns, package codes, and handler guidance. Use when working with onsemi MOSFETs, diodes, transistors, voltage regulators, or OnSemiHandler.
---

# ON Semiconductor (onsemi) Manufacturer Skill

## Company Overview

ON Semiconductor (onsemi) is a major semiconductor manufacturer that acquired Fairchild Semiconductor in 2016. The company inherited multiple part numbering conventions from various acquisitions including Fairchild, Motorola Semiconductor Products Sector, and others.

---

## MPN Structure by Product Family

### MOSFETs - NTD/NTB/NTS Series (ON Semiconductor Native)

```
NT[PKG][VOLTAGE][CURRENT/RDS][CHANNEL][SUFFIX]
 |   |      |         |         |        |
 |   |      |         |         |        +-- L=Logic level, blank=standard
 |   |      |         |         +-- N=N-channel (may be embedded)
 |   |      |         +-- Current capability or RDS identifier
 |   |      +-- Voltage class
 |   +-- Package: D=DPAK, B=D2PAK, S=SO-8, R=SOT-23
 +-- NT = ON Semiconductor power MOSFET
```

**Examples:**
- NTD20N06L = N-channel, DPAK, 60V, 20A, Logic Level
- NTD2955 = P-channel equivalent of 2N2955 in DPAK
- NTD4809N = N-channel, DPAK, 30V, 88A
- NTB60N06 = N-channel, D2PAK, 60V, 60A

### MOSFETs - FQP/FQD/FQB Series (Legacy Fairchild)

```
FQ[PKG][CURRENT][CHANNEL][VOLTAGE][SUFFIX]
 |   |     |        |        |       |
 |   |     |        |        |       +-- L=Logic level, blank=standard
 |   |     |        |        +-- Voltage / 10 (e.g., 06=60V, 20=200V)
 |   |     |        +-- N=N-channel, P=P-channel
 |   |     +-- Current rating (A)
 |   +-- Package: P=TO-220, D=DPAK, B=D2PAK, A=TO-3P
 +-- FQ = Fairchild QFET series
```

**Examples:**
- FQP50N06L = TO-220, 50A, N-channel, 60V, Logic Level
- FQP27P06 = TO-220, 27A, P-channel, 60V
- FQP4N20L = TO-220, 4A, N-channel, 200V, Logic Level
- FQD13N10 = DPAK, 13A, N-channel, 100V

### MOSFETs - FDP/FDB/FDD Series (Legacy Fairchild PowerTrench)

```
FD[PKG][CURRENT/CODE][RDS][VOLTAGE][SUFFIX]
 |   |        |        |      |       |
 |   |        |        |      |       +-- Technology suffix (optional)
 |   |        |        |      +-- Voltage class
 |   |        |        +-- RDS identifier (mOhm related)
 |   |        +-- Device code or current
 |   +-- Package: P=TO-220, B=D2PAK, D=DPAK
 +-- FD = Fairchild PowerTrench MOSFET
```

**Examples:**
- FDP3680 = TO-220, PowerTrench, 100V
- FDD3680 = DPAK, PowerTrench, 100V
- FDB3632 = D2PAK, 100V, 73A

### Transistors - 2N Series (JEDEC Standard)

```
2N[SEQUENCE][SUFFIX]
 |    |        |
 |    |        +-- A/B/C = grade improvement
 |    +-- JEDEC registration number (no encoded meaning)
 +-- 2N = JEDEC transistor prefix
```

**Examples:**
- 2N2222A = NPN general purpose
- 2N3904 = NPN general purpose
- 2N3906 = PNP general purpose
- 2N7000 = N-channel enhancement MOSFET
- 2N7002 = N-channel SMD MOSFET

### Transistors - MMBT Series (Surface Mount)

```
MMBT[BASE][SUFFIX]
  |    |      |
  |    |      +-- Grade suffix (L=low, T1=tape & reel)
  |    +-- Equivalent 2N or base number
  +-- MMBT = Motorola Miniature Bipolar Transistor (SOT-23)
```

**Examples:**
- MMBT2222A = SMD equivalent of 2N2222A (SOT-23)
- MMBT3904 = SMD equivalent of 2N3904 (SOT-23)
- MMBT3906 = SMD equivalent of 2N3906 (SOT-23)
- MMBT4401 = NPN 40V transistor (SOT-23)
- MMBT4403 = PNP 40V transistor (SOT-23)

### Transistors - MPS/MPSA Series

```
MPS[A][CODE]
 |   |   |
 |   |   +-- Device code
 |   +-- A = variant designation
 +-- MPS = Motorola Plastic Small (signal transistor)
```

**Examples:**
- MPSA42 = NPN high voltage (300V)
- MPSA92 = PNP high voltage (300V)
- MPS2222A = Plastic equivalent of 2N2222A

### Voltage Regulators - MC78xx/MC79xx Series

```
MC78[VOLTAGE][GRADE][PACKAGE]
  |     |       |       |
  |     |       |       +-- Package suffix (CT=TO-220, CD=DPAK, etc.)
  |     |       +-- Grade: blank=std, A/B/C=improved
  |     +-- Output voltage (05=5V, 12=12V, 15=15V, etc.)
  +-- MC78 = Motorola positive regulator / MC79 = negative regulator
```

**Examples:**
- MC7805CT = +5V, 1A, TO-220
- MC7812ACT = +12V, 1A, improved, TO-220
- MC78L05ACP = +5V, 100mA, plastic
- MC7905CT = -5V, 1A, TO-220
- MC79M12CT = -12V, 500mA, TO-220

### Voltage Regulators - MC33xx Series (Switching)

```
MC33[CODE][VARIANT][PACKAGE]
  |    |      |        |
  |    |      |        +-- Package designator
  |    |      +-- Variant/feature code
  |    +-- Device code
  +-- MC33 = Motorola switching regulator family
```

**Examples:**
- MC33063AD = DC-DC converter, SOIC
- MC34063A = 1.5A switching regulator
- MC33167T = 5A switching regulator, TO-220

### Voltage Regulators - NCP Series (Newer ON Semi)

```
NCP[CODE][VARIANT][PACKAGE]
  |   |      |        |
  |   |      |        +-- Package designator
  |   |      +-- Feature/variant code
  |   +-- Device family code
  +-- NCP = ON Semiconductor power IC
```

**Examples:**
- NCP1117ST33T3G = 3.3V LDO, SOT-223, tape & reel
- NCP1117DT33G = 3.3V LDO, DPAK
- NCP5500 = Ultra-low Iq LDO

### Diodes - RL Series (Standard Rectifiers)

```
RL20[VOLTAGE CODE]
  |        |
  |        +-- 1=50V, 2=100V, 3=200V, 4=400V, 5=600V, 6=800V, 7=1000V
  +-- RL20 = 2A standard recovery rectifier series
```

**Examples:**
- RL201 = 50V, 2A rectifier (DO-41)
- RL204 = 400V, 2A rectifier (DO-41)
- RL207 = 1000V, 2A rectifier (DO-41)

### Diodes - MUR Series (Ultra-Fast Recovery)

```
MUR[CURRENT][VOLTAGE]
  |     |       |
  |     |       +-- Voltage rating / 10 (e.g., 20=200V)
  |     +-- Current rating in Amps
  +-- MUR = Motorola Ultra-fast Recovery
```

**Examples:**
- MUR120 = 1A, 200V ultra-fast
- MUR460 = 4A, 600V ultra-fast
- MUR1520 = 15A, 200V ultra-fast

### Diodes - MBR/MBRS Series (Schottky)

```
MBR[S][CURRENT][VOLTAGE]
  |  |     |       |
  |  |     |       +-- Voltage rating / 10
  |  |     +-- Current rating
  |  +-- S = Surface mount version
  +-- MBR = Motorola Barrier Rectifier (Schottky)
```

**Examples:**
- MBR1045 = 10A, 45V Schottky (TO-220)
- MBR2045CT = 20A, 45V dual Schottky (TO-220)
- MBRS340 = 3A, 40V SMD Schottky (SMC)

### Diodes - 1N47xx/1N52xx Series (Zener)

```
1N[SERIES][CODE][SUFFIX]
 |    |      |      |
 |    |      |      +-- Grade suffix (A, B, C, etc.)
 |    |      +-- Voltage code within series
 |    +-- 47=1W Zener, 52=0.5W Zener
 +-- 1N = JEDEC diode prefix
```

**Examples:**
- 1N4733A = 5.1V Zener, 1W
- 1N4742A = 12V Zener, 1W
- 1N5231B = 5.1V Zener, 0.5W
- 1N5242B = 12V Zener, 0.5W

### Op-Amps - MC Series

```
MC[BASE][VARIANT][PACKAGE]
 |   |      |        |
 |   |      |        +-- Package code
 |   |      +-- Grade variant
 |   +-- Device base number
 +-- MC = Motorola integrated circuit
```

**Examples:**
- MC1458 = Dual op-amp (equivalent to LM1458)
- MC324 = Quad op-amp (equivalent to LM324)
- MC741 = Single op-amp (equivalent to LM741)

---

## Package Codes

### Through-Hole Packages

| Code | Package | Current | Notes |
|------|---------|---------|-------|
| CT | TO-220 | 1A+ | Standard power |
| T | TO-220 | 1A+ | Alternate code |
| ACP | TO-92 | 100mA | Plastic small |
| P | DIP | - | Dual in-line |
| N | DIP | - | Alternate for DIP |

### Surface Mount Packages

| Code | Package | Notes |
|------|---------|-------|
| D | SOIC | Standard SOIC-8/14/16 |
| DT | DPAK (TO-252) | Power SMD |
| BD | D2PAK (TO-263) | High power SMD |
| DW | SOIC-Wide | Wide body |
| PW | TSSOP | Thin shrink SOP |
| DGK | MSOP | Mini SOP |
| DBV | SOT-23 | Small outline |
| T3G | SOT-23 Tape | SOT-23 with T&R |

### Diode Packages

| Code | Package | Notes |
|------|---------|-------|
| RL | DO-41 | Standard axial |
| G | DO-35 | Small signal |
| T | TO-220 | Power diode |
| FP | TO-220F | Fully isolated |
| SMB | DO-214AA | Surface mount |
| SMC | DO-214AB | Larger SMD |

---

## Temperature Grades & Prefixes

### Automotive Prefix (NCV)

```
NCV[BASE PART NUMBER]
  |
  +-- Automotive grade, AEC-Q100/Q101 qualified
      Temperature: -40C to +125C
      PPAP capable
```

**Examples:**
- NCV7805 = Automotive version of MC7805
- NCV8402 = Automotive power MOSFET

### Temperature Suffixes

| Suffix | Range | Application |
|--------|-------|-------------|
| (none) | 0C to +70C | Commercial |
| I | -40C to +85C | Industrial |
| E | -40C to +125C | Extended |

### Grade Suffixes

| Suffix | Meaning |
|--------|---------|
| A | Improved tolerance/specs |
| B | Further improved |
| C | Premium grade |
| L | Logic level (MOSFETs) |
| G | Green/RoHS compliant |
| T1 | Tape & reel (SOT-23) |
| T3G | Tape & reel + Green |

---

## Common Series Reference

### Popular MOSFETs

| Part Number | Type | Vds | Id | Package |
|-------------|------|-----|-----|---------|
| FQP50N06L | N-ch Logic | 60V | 50A | TO-220 |
| FQP27P06 | P-ch | 60V | 27A | TO-220 |
| NTD20N06L | N-ch Logic | 60V | 20A | DPAK |
| NTD2955 | P-ch | 60V | 12A | DPAK |
| 2N7000 | N-ch | 60V | 200mA | TO-92 |
| 2N7002 | N-ch | 60V | 115mA | SOT-23 |
| FDB3632 | N-ch | 100V | 73A | D2PAK |

### Popular Transistors

| Part Number | Type | Vceo | Ic | Package |
|-------------|------|------|-----|---------|
| 2N2222A | NPN | 40V | 600mA | TO-18/TO-92 |
| 2N3904 | NPN | 40V | 200mA | TO-92 |
| 2N3906 | PNP | 40V | 200mA | TO-92 |
| MMBT2222A | NPN | 40V | 600mA | SOT-23 |
| MMBT3904 | NPN | 40V | 200mA | SOT-23 |
| MMBT3906 | PNP | 40V | 200mA | SOT-23 |
| MPSA42 | NPN | 300V | 500mA | TO-92 |

### Popular Regulators

| Part Number | Output | Current | Package |
|-------------|--------|---------|---------|
| MC7805CT | +5V | 1A | TO-220 |
| MC7812CT | +12V | 1A | TO-220 |
| MC78L05ACP | +5V | 100mA | TO-92 |
| MC7905CT | -5V | 1A | TO-220 |
| NCP1117ST33T3G | +3.3V | 1A | SOT-223 |
| MC33063AD | Variable | 1.5A | SOIC-8 |

### Popular Diodes

| Part Number | Type | Vrrm | If | Package |
|-------------|------|------|-----|---------|
| RL207 | Rectifier | 1000V | 2A | DO-41 |
| MUR460 | Ultra-fast | 600V | 4A | TO-220 |
| MBR1045 | Schottky | 45V | 10A | TO-220 |
| MBRS340 | Schottky | 40V | 3A | SMC |
| 1N4733A | Zener | 5.1V | 1W | DO-41 |
| 1N4742A | Zener | 12V | 1W | DO-41 |

---

## Handler Implementation Notes

### Issues Found in Current OnSemiHandler

1. **HashSet usage** (line 39): Uses mutable `HashSet` instead of `Set.of()` or `EnumSet` for immutability
2. **Limited MOSFET patterns**: No patterns for NTD, FQP, FDP series MOSFETs
3. **Limited transistor patterns**: No patterns for 2N, MMBT, MPSA series transistors
4. **Missing NCP regulator patterns**: Only covers MC78xx/MC79xx, missing NCP series
5. **Package extraction logic**: Only handles diode packages, missing MOSFET/transistor package codes
6. **Series extraction incomplete**: Does not extract series for MOSFETs or transistors

### Recommended Pattern Additions

```java
// MOSFETs - ON Semi native
registry.addPattern(ComponentType.MOSFET, "^NT[DBSR][0-9]+.*");
registry.addPattern(ComponentType.MOSFET_ONSEMI, "^NT[DBSR][0-9]+.*");

// MOSFETs - Fairchild legacy
registry.addPattern(ComponentType.MOSFET, "^FQ[PDBA][0-9]+.*");
registry.addPattern(ComponentType.MOSFET_ONSEMI, "^FQ[PDBA][0-9]+.*");
registry.addPattern(ComponentType.MOSFET, "^FD[PDB][0-9]+.*");
registry.addPattern(ComponentType.MOSFET_ONSEMI, "^FD[PDB][0-9]+.*");

// Small signal MOSFETs
registry.addPattern(ComponentType.MOSFET, "^2N7[0-9]{3}.*");
registry.addPattern(ComponentType.MOSFET_ONSEMI, "^2N7[0-9]{3}.*");
registry.addPattern(ComponentType.MOSFET, "^BSS[0-9]+.*");
registry.addPattern(ComponentType.MOSFET_ONSEMI, "^BSS[0-9]+.*");

// Transistors
registry.addPattern(ComponentType.TRANSISTOR, "^2N[0-9]{4}.*");
registry.addPattern(ComponentType.TRANSISTOR, "^MMBT[0-9]+.*");
registry.addPattern(ComponentType.TRANSISTOR, "^MPS[A]?[0-9]+.*");
registry.addPattern(ComponentType.TRANSISTOR, "^BC[0-9]{3}.*");

// NCP voltage regulators
registry.addPattern(ComponentType.VOLTAGE_REGULATOR, "^NCP[0-9]+.*");
registry.addPattern(ComponentType.VOLTAGE_REGULATOR_LINEAR_ON, "^NCP[0-9]+.*");
```

### Package Extraction Improvements

```java
// MOSFET package extraction
if (upperMpn.startsWith("FQP") || upperMpn.endsWith("CT")) return "TO-220";
if (upperMpn.startsWith("FQD") || upperMpn.matches(".*DT$")) return "DPAK";
if (upperMpn.startsWith("FQB") || upperMpn.matches(".*BD$")) return "D2PAK";
if (upperMpn.startsWith("NTD")) return "DPAK";
if (upperMpn.startsWith("NTB")) return "D2PAK";

// Transistor package extraction
if (upperMpn.startsWith("MMBT") || upperMpn.matches(".*T1$")) return "SOT-23";
if (upperMpn.startsWith("2N") && !upperMpn.startsWith("2N7")) return "TO-92";
if (upperMpn.startsWith("MPS")) return "TO-92";
```

### Series Extraction Improvements

```java
// MOSFET series
if (mpn.matches("(?i)^NTD.*")) return "NTD";
if (mpn.matches("(?i)^NTB.*")) return "NTB";
if (mpn.matches("(?i)^FQP.*")) return "FQP";
if (mpn.matches("(?i)^FQD.*")) return "FQD";
if (mpn.matches("(?i)^FDP.*")) return "FDP";
if (mpn.matches("(?i)^FDD.*")) return "FDD";
if (mpn.matches("(?i)^FDB.*")) return "FDB";

// Transistor series
if (mpn.matches("(?i)^MMBT.*")) return "MMBT";
if (mpn.matches("(?i)^2N[0-9]+.*")) return "2N";
if (mpn.matches("(?i)^MPS[A]?.*")) return "MPS";

// Regulator series
if (mpn.matches("(?i)^NCP[0-9]+.*")) return "NCP";
```

---

## Related Files

- Handler: `manufacturers/OnSemiHandler.java`
- Component types: `MOSFET_ONSEMI`, `IGBT_ONSEMI`, `VOLTAGE_REGULATOR_LINEAR_ON`, `VOLTAGE_REGULATOR_SWITCHING_ON`, `LED_DRIVER_ONSEMI`, `MOTOR_DRIVER_ONSEMI`, `OPAMP_ON`, `DIODE_ON`

---

## Learnings & Edge Cases

- **Fairchild acquisition**: ON Semiconductor acquired Fairchild in 2016, inheriting FQP/FDP/FDD nomenclature
- **Motorola heritage**: MC78xx, MC79xx, MUR, MBR series come from Motorola semiconductor division
- **JEDEC standards**: 2N and 1N prefixes follow JEDEC numbering (no encoded specs in number)
- **Logic level**: "L" suffix indicates logic-level gate threshold (~2.5V Vgs max)
- **Automotive grade**: NCV prefix indicates AEC-Q100/Q101 qualified automotive parts
- **Cross-reference needed**: Many parts have equivalents across ON Semi, Fairchild, and other sources
- **Package suffix variations**: CT vs T both mean TO-220; DT means DPAK

<!-- Add new learnings above this line -->
