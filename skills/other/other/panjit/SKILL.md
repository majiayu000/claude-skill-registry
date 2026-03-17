---
name: panjit
description: Panjit International MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Panjit diodes, transistors, MOSFETs, or PanjitHandler.
---

# Panjit International Manufacturer Skill

## Overview

Panjit International is a Taiwanese semiconductor manufacturer producing discrete semiconductors including diodes, transistors, and MOSFETs. They are known for industry-standard compatible parts as well as their proprietary PJ MOSFET series.

## MPN Structure

Panjit MPNs follow industry-standard patterns with package suffixes:

### Standard Diode Pattern

```
[SERIES][RATING][SUFFIX]
   |       |       |
   |       |       +-- Package code
   |       +-- Voltage/specification
   +-- Series prefix (1N, SS, SK, BAV, etc.)
```

### PJ MOSFET Pattern

```
PJ[SERIES][SUFFIX]
   |        |
   |        +-- Package code
   +-- 4-digit series number
```

### Example Decoding

```
1N4007G
|  |  ||
|  |  |+-- G = DO-41 package
|  |  +-- 7 = 1000V rating
|  +-- 400 = Rectifier series
+-- 1N = Standard diode prefix

MMBT3904LT
|   |  | |
|   |  | +-- LT = SOT-23 package
|   |  +-- NPN transistor number
|   +-- 3904 series
+-- MMBT = SMD transistor prefix

PJ2308N
| |  ||
| |  |+-- N = TO-92 package
| |  +-- Series number
| +-- 23 series
+-- PJ = Panjit proprietary MOSFET
```

---

## Product Lines

### Standard Rectifier Diodes (1N4xxx)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| 1N4001 | 50V | 1A | DO-41 |
| 1N4002 | 100V | 1A | DO-41 |
| 1N4003 | 200V | 1A | DO-41 |
| 1N4004 | 400V | 1A | DO-41 |
| 1N4005 | 600V | 1A | DO-41 |
| 1N4006 | 800V | 1A | DO-41 |
| 1N4007 | 1000V | 1A | DO-41 |

### Signal Diodes

| Part | Description | Package |
|------|-------------|---------|
| 1N4148 | Small signal, 100V | DO-35/SOD-123 |
| 1N914 | Signal diode (equiv. 1N4148) | DO-35 |

### Power Rectifiers (1N5xxx)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| 1N5400 | 50V | 3A | DO-201 |
| 1N5401 | 100V | 3A | DO-201 |
| 1N5402 | 200V | 3A | DO-201 |
| 1N5404 | 400V | 3A | DO-201 |
| 1N5406 | 600V | 3A | DO-201 |
| 1N5408 | 1000V | 3A | DO-201 |
| 1N5817 | 20V | 1A | DO-41 (Schottky) |
| 1N5819 | 40V | 1A | DO-41 (Schottky) |

### Fast Recovery Diodes

| Series | Speed | Examples |
|--------|-------|----------|
| ES | Fast | ES1J, ES2J, ES1D |
| RS | Fast | RS1M, RS2M, RS1G |
| US | Ultra-fast | US1M, US2M |
| UF | Ultra-fast | UF4001-UF4007 |

### Schottky Diodes (SS Series)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SS12 | 20V | 1A | SMA |
| SS14 | 40V | 1A | SMA |
| SS16 | 60V | 1A | SMA |
| SS24 | 40V | 2A | SMA |
| SS34 | 40V | 3A | SMA |

### Schottky Diodes (SK Series)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SK34 | 40V | 3A | SMB |
| SK36 | 60V | 3A | SMB |
| SK52 | 20V | 5A | SMB |
| SK54 | 40V | 5A | SMB |
| SK56 | 60V | 5A | SMB |

### Schottky Barrier (SB Series)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SB140 | 40V | 1A | DO-41 |
| SB160 | 60V | 1A | DO-41 |
| SB360 | 60V | 3A | DO-201 |
| SB560 | 60V | 5A | DO-201 |

### Schottky Barrier (MBR Series)

| Part | Current | Voltage | Package |
|------|---------|---------|---------|
| MBR340 | 3A | 40V | DO-201 |
| MBR360 | 3A | 60V | DO-201 |
| MBR1045 | 10A | 45V | TO-220 |

### Signal Diodes (BAV/BAS/BAT Series)

| Series | Type | Examples |
|--------|------|----------|
| BAV | Small signal | BAV21, BAV70, BAV99 |
| BAS | Switching | BAS16, BAS21 |
| BAT | Schottky barrier | BAT54, BAT54S, BAT54C |

### Zener Diodes (BZX Series)

| Series | Package | Examples |
|--------|---------|----------|
| BZX84 | SOT-23 | BZX84C5V1, BZX84C3V3 |
| BZX55 | DO-35 | BZX55C3V3, BZX55C5V1 |

### TVS Diodes

| Series | Package | Examples |
|--------|---------|----------|
| SMBJ | SMB | SMBJ5.0A, SMBJ15A |
| SMAJ | SMA | SMAJ5.0A, SMAJ15A |

### SMD Transistors (MMBT Series)

| Part | Type | Equivalent | Package |
|------|------|------------|---------|
| MMBT2222 | NPN | 2N2222 | SOT-23 |
| MMBT2907 | PNP | 2N2907 | SOT-23 |
| MMBT3904 | NPN | 2N3904 | SOT-23 |
| MMBT3906 | PNP | 2N3906 | SOT-23 |

### MPSA Series Transistors

| Part | Type | Application |
|------|------|-------------|
| MPSA42 | NPN | High voltage |
| MPSA92 | PNP | High voltage |
| MPSA06 | NPN | General purpose |

### 2N Series Transistors

| Part | Type | Package |
|------|------|---------|
| 2N2222 | NPN | TO-92 |
| 2N2907 | PNP | TO-92 |
| 2N3904 | NPN | TO-92 |
| 2N3906 | PNP | TO-92 |
| 2N7002 | N-Ch MOSFET | SOT-23 |

### BC Series Transistors

| Part | Type | Package |
|------|------|---------|
| BC847 | NPN | SOT-23 |
| BC857 | PNP | SOT-23 |
| BC337 | NPN | TO-92 |

### PN Series Transistors

| Part | Type | Equivalent |
|------|------|------------|
| PN2222 | NPN | 2N2222 |
| PN2907 | PNP | 2N2907 |

### MOSFETs (BSS Series)

| Part | Type | Package |
|------|------|---------|
| BSS138 | N-Channel | SOT-23 |
| BSS84 | P-Channel | SOT-23 |

### MOSFETs (PJ Series - Panjit Proprietary)

| Part | Type | Package |
|------|------|---------|
| PJ2308 | N-Channel | Various |
| PJ3415 | N-Channel | Various |
| PJ4435 | P-Channel | Various |

### MOSFETs (SI/AO Series)

| Part | Type | Package |
|------|------|---------|
| SI2301 | P-Channel | SOT-23 |
| SI2302 | N-Channel | SOT-23 |
| AO3400 | N-Channel | SOT-23 |
| AO3401 | P-Channel | SOT-23 |

---

## Package Codes

### Comprehensive Package Suffix Table

| Code | Package | Notes |
|------|---------|-------|
| G | DO-41 | Standard axial |
| GP | DO-41 | Axial variant |
| W | SOD-123 | Small SMD |
| WS | SOD-323 | Very small SMD |
| A | SOT-23 | SMD transistor |
| LT | SOT-23 | SOT-23 variant |
| WT | SOT-23 | SOT-23 variant |
| F | SMAF | Flat SMA |
| S | SMA | Standard SMD |
| B | SMB | Medium SMD |
| C | SMC | Large SMD |
| FL | SOD-123FL | Flat lead |
| T | TO-220 | Power through-hole |
| TP | TO-220F | Isolated tab |
| N | TO-92 | Small through-hole |
| NL | TO-92 | TO-92 variant |

### Default Packages by Series

| Series | Default Package |
|--------|-----------------|
| MMBT | SOT-23 |
| BC | SOT-23 |
| 2N7002 | SOT-23 |
| BSS | SOT-23 |
| 2N (other) | TO-92 |
| ES/RS/US | SMA |
| SS | DO-214AC (SMA) |
| SK | SMB |
| BAV/BAS/BAT | SOT-23 |
| 1N4xxx | DO-41 |

---

## Handler Implementation Notes

### Pattern Matching

```java
// Standard rectifiers
"^1N4[0-9]{3}.*"        // 1N4001-1N4007
"^1N5[0-9]{3}.*"        // 1N5xxx series

// Signal diodes
"^1N4148.*"
"^1N914.*"

// Fast recovery
"^ES[1-3][A-Z].*"
"^RS[1-3][A-Z].*"
"^US[1-3][A-Z].*"
"^UF[0-9]{4}.*"

// Schottky
"^SS[1-3][0-9].*"
"^SK[3-5][0-9].*"
"^SB[1-5][0-9]{2}.*"
"^MBR[0-9]{3,4}.*"

// Signal diodes
"^BAV[0-9]{2}.*"
"^BAS[0-9]{2}.*"
"^BAT[0-9]{2}.*"

// Zener
"^BZX[0-9]{2}.*"

// TVS
"^SMB[AJ][0-9].*"
"^SMA[J][0-9].*"

// Transistors (exclude 2N7002)
"^MMBT[0-9]{3,4}.*"
"^MPSA[0-9]{2}.*"
"^2N[0-9]{4}.*"         // But NOT 2N7002
"^BC[0-9]{3}.*"
"^PN[0-9]{4}.*"

// MOSFETs
"^2N7002.*"
"^BSS[0-9]{2,3}.*"
"^PJ[0-9]{4}.*"
"^SI[0-9]{4}.*"
"^AO[0-9]{4}.*"
```

### Series Extraction

```java
// Signal diodes (specific before generic)
"1N4148W" -> "1N4148"
"1N914" -> "1N914"

// Rectifiers
"1N4007G" -> "1N4000"
"1N5408" -> "1N5400"
"1N5819" -> "1N5800"  // Schottky series

// Fast recovery
"ES1J" -> "ES"
"RS1M" -> "RS"
"US1M" -> "US"
"UF4007" -> "UF"

// Schottky
"SS14" -> "SS"
"SK34" -> "SK"
"SB160" -> "SB"
"MBR1045" -> "MBR"

// Signal
"BAV99" -> "BAV"
"BAS16" -> "BAS"
"BAT54S" -> "BAT"

// Zener
"BZX84C5V1" -> "BZX"

// TVS
"SMBJ15A" -> "SMBJ"
"SMAJ24CA" -> "SMAJ"

// Transistors
"MMBT3904" -> "MMBT"
"MPSA42" -> "MPSA"
"2N3904" -> "2N"
"BC547B" -> "BC"
"PN2222A" -> "PN"

// MOSFETs
"BSS138" -> "BSS"
"PJ2308" -> "PJ"
"SI2301" -> "SI"
"AO3400" -> "AO"
```

### Replacement Logic

```java
// 1N400x: higher voltage can replace lower
"1N4007" can replace "1N4001" through "1N4006"

// 1N540x: higher voltage can replace lower
"1N5408" can replace "1N5400" through "1N5407"

// SS series: higher current can replace lower
"SS34" can replace "SS14" (same voltage, higher current)

// Signal diode equivalents
"1N4148" == "1N914"

// MMBT equivalent to 2N
"MMBT3904" == "2N3904" (different package)

// Transistor base number match
"MMBT2222" base = "2222"
"2N2222" base = "2222"
"PN2222" base = "2222"
// All three are equivalent electrically
```

---

## Component Types

| Pattern | ComponentType |
|---------|---------------|
| 1N*, SS*, SK*, SB*, MBR*, BAV*, BAS*, BAT*, BZX*, SMBJ*, SMAJ*, ES*, RS*, US*, UF* | DIODE |
| MMBT* (not 2N7002), MPSA*, 2N* (not 2N7002), BC*, PN* | TRANSISTOR |
| 2N7002, BSS*, PJ*, SI*, AO* | MOSFET |

---

## Related Files

- Handler: `manufacturers/PanjitHandler.java`
- Component types: `ComponentType.DIODE`, `ComponentType.TRANSISTOR`, `ComponentType.MOSFET`

---

## Learnings & Edge Cases

- **2N7002 is MOSFET**: The 2N prefix usually indicates transistors, but 2N7002 is specifically an N-channel MOSFET. Handler explicitly excludes it from TRANSISTOR type.
- **PJ series proprietary**: PJ series MOSFETs are Panjit's proprietary line. Package code typically follows 4-digit series number.
- **1N4148 vs 1N914**: These are equivalent signal diodes. Handler returns true for isOfficialReplacement().
- **1N5817-1N5819 are Schottky**: Unlike 1N5400-1N5408 which are standard rectifiers, 1N58xx in this range are Schottky diodes with lower forward voltage.
- **Package suffix order matters**: Check longer suffixes (WS, GP, FL, NL, TP, LT, WT) before shorter (W, G, F, N, T, L). Otherwise "WS" matches "S" first.
- **MMBT base extraction**: Extract base number for equivalence: MMBT2222A -> "2222", 2N2222A -> "2222". Both are electrically equivalent.
- **SS/SK current encoding**: First digit is current (1-5A), second is voltage code. SS14 = 1A/40V.
- **BAT54 variants**: BAT54S = series pair, BAT54C = common cathode. Different pinouts, not interchangeable.

<!-- Add new learnings above this line -->
