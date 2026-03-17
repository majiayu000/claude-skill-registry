---
name: yangjie
description: Yangjie Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Yangjie diodes, transistors, or YangjieHandler.
---

# Yangjie Technology Manufacturer Skill

## Overview

Yangjie Technology is a Chinese semiconductor manufacturer specializing in discrete semiconductors including rectifier diodes, Schottky rectifiers, TVS diodes, and transistors. They are one of China's largest discrete semiconductor manufacturers.

## MPN Structure

Yangjie MPNs follow industry-standard patterns:

### YJ-Prefixed Series (Proprietary)

```
YJ[SERIES][RATING][SUFFIX]
   |        |       |
   |        |       +-- Package code
   |        +-- Voltage/current rating
   +-- YJ = Yangjie proprietary prefix
```

### Standard Industry Parts

```
[SERIES][RATING][SUFFIX]
   |       |       |
   |       |       +-- Package code
   |       +-- Specification code
   +-- Industry standard prefix (1N, MBR, SMBJ, etc.)
```

### Example Decoding

```
YJ1N4007G
| |  |  ||
| |  |  |+-- G = DO-41 package
| |  |  +-- 7 = 1000V rating
| |  +-- 400 = Rectifier series
| +-- 1N = Diode prefix
+-- YJ = Yangjie prefix

MBR1045CT
|  |  |||
|  |  ||+-- T = TO-220 indicator
|  |  |+-- C = Common cathode
|  |  +-- 45 = 45V voltage
|  +-- 10 = 10A current
+-- MBR = Schottky rectifier prefix

SMBJ15A
|  | ||
|  | |+-- A = Unidirectional
|  | +-- 15 = 15V standoff voltage
|  +-- J = SMB package indicator
+-- SMB = TVS diode series
```

---

## Product Lines

### YJ Series Rectifier Diodes

| Pattern | Description | Current |
|---------|-------------|---------|
| YJ1N4001-YJ1N4007 | Standard rectifiers | 1A |
| YJ1N5401-YJ1N5408 | Power rectifiers | 3A |

### MBR Schottky Rectifiers

| Part | Current | Voltage | Package |
|------|---------|---------|---------|
| MBR1045 | 10A | 45V | TO-220 |
| MBR2045 | 20A | 45V | TO-220 |
| MBR3045 | 30A | 45V | TO-247 |
| MBR1545 | 15A | 45V | TO-220 |
| MBR2545 | 25A | 45V | TO-247 |

**Format**: MBR[current][voltage]

### SMBJ TVS Diodes (SMB Package)

| Part | Standoff | Clamping | Type |
|------|----------|----------|------|
| SMBJ5.0A | 5.0V | 9.2V | Unidirectional |
| SMBJ5.0CA | 5.0V | 9.2V | Bidirectional |
| SMBJ15A | 15V | 24.4V | Unidirectional |
| SMBJ24A | 24V | 38.9V | Unidirectional |
| SMBJ33CA | 33V | 53.3V | Bidirectional |

**Suffix**: A = Unidirectional, CA = Bidirectional

### SMAJ TVS Diodes (SMA Package)

| Part | Standoff | Type |
|------|----------|------|
| SMAJ5.0A | 5.0V | Unidirectional |
| SMAJ15A | 15V | Unidirectional |
| SMAJ24CA | 24V | Bidirectional |

### SS Series Schottky Diodes

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SS12 | 20V | 1A | DO-214AC |
| SS14 | 40V | 1A | DO-214AC |
| SS16 | 60V | 1A | DO-214AC |
| SS24 | 40V | 2A | DO-214AC |
| SS34 | 40V | 3A | DO-214AC |
| SS54 | 40V | 5A | DO-214AC |

**Format**: SS[current][voltage_code]

### SK Series Schottky Diodes

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SK34 | 40V | 3A | SMB |
| SK36 | 60V | 3A | SMB |
| SK54 | 40V | 5A | SMB |
| SK56 | 60V | 5A | SMB |

### 2N Series Transistors

| Part | Type | Application |
|------|------|-------------|
| 2N7002 | N-Channel MOSFET | Small signal |
| 2N3904 | NPN | General purpose |
| 2N3906 | PNP | General purpose |

**Note**: 2N7002 is classified as MOSFET, not transistor.

### MMBT Series SMD Transistors

| Part | Type | Equivalent |
|------|------|------------|
| MMBT2222 | NPN | 2N2222 |
| MMBT3904 | NPN | 2N3904 |
| MMBT3906 | PNP | 2N3906 |

### Bridge Rectifiers

| Series | Description | Package |
|--------|-------------|---------|
| YJB | Single-phase bridge | Various |
| YJDB | Single-phase bridge | DIP |

---

## Package Codes

### Diode Packages

| Suffix | Package | Notes |
|--------|---------|-------|
| G | DO-41 | Standard axial |
| S | SMD | Generic SMD |
| FL | SOD-123FL | Flat lead |
| L | SOD-123 | SMD signal |
| A | DO-41 | Axial variant |

### MBR Package Codes

| Suffix | Package | Notes |
|--------|---------|-------|
| CT | TO-220 | Common cathode |
| PT | TO-247 | High power |
| FCT | TO-220F | Isolated tab |
| S | DO-214AB (SMC) | Surface mount |
| D | DPAK | Medium power SMD |
| DP | D2PAK | High power SMD |

### TVS Package Mapping

| Prefix | Package |
|--------|---------|
| SMBJ | SMB (DO-214AA) |
| SMAJ | SMA (DO-214AC) |

### Transistor Packages

| Series | Default Package |
|--------|-----------------|
| 2N | TO-92 |
| MMBT | SOT-23 |

### Bridge Rectifier Packages

| Pattern | Package |
|---------|---------|
| YJB with S | MBS (mini bridge SMD) |
| YJB/YJDB | DIP-4 |

---

## Standard 1N Series Voltage Ratings

### 1N400x (1A Rectifiers)

| Part | Voltage |
|------|---------|
| 1N4001 | 50V |
| 1N4002 | 100V |
| 1N4003 | 200V |
| 1N4004 | 400V |
| 1N4005 | 600V |
| 1N4006 | 800V |
| 1N4007 | 1000V |

### 1N540x (3A Rectifiers)

| Part | Voltage |
|------|---------|
| 1N5401 | 100V |
| 1N5402 | 200V |
| 1N5403 | 200V |
| 1N5404 | 400V |
| 1N5405 | 500V |
| 1N5406 | 600V |
| 1N5407 | 800V |
| 1N5408 | 1000V |

---

## Handler Implementation Notes

### Pattern Matching

```java
// YJ prefixed rectifiers
"^YJ1N[0-9]{4}.*"

// MBR Schottky rectifiers
"^MBR[0-9]{4}.*"

// TVS diodes
"^SMBJ[0-9]+\\.?[0-9]*[AC]?.*"
"^SMAJ[0-9]+\\.?[0-9]*[AC]?.*"

// Schottky diodes
"^SS[0-9]{2}.*"
"^SK[0-9]{2}.*"

// Transistors
"^2N[0-9]{4}.*"
"^MMBT[0-9]{4}.*"

// MOSFETs
"^2N7002.*"

// Bridge rectifiers
"^YJB[0-9]+.*"
"^YJDB[0-9]+.*"

// Standard diodes
"^1N[0-9]{4}.*"
```

### Series Extraction

```java
// YJ prefix removed for series
"YJ1N4007G" -> "YJ"

// MBR base
"MBR1045CT" -> "MBR"

// TVS voltage
"SMBJ15A" -> "SMBJ"
"SMAJ24CA" -> "SMAJ"

// Schottky
"SS14" -> "SS"
"SK34" -> "SK"

// Transistors - specific series
"2N7002" -> "2N7002"  // MOSFET
"2N3904" -> "2N"

// MMBT
"MMBT3904" -> "MMBT"

// Signal diodes
"1N4148" -> "1N4148"
"1N914" -> "1N914"

// Rectifier series
"1N4007" -> "1N4xxx"
"1N5408" -> "1N5xxx"
```

### Replacement Logic

```java
// Rectifier voltage upgrade
"1N4007" can replace "1N4001-1N4007"

// MBR: same ratings, different package
"MBR1045CT" == "MBR1045S" (electrically)

// TVS: bidirectional can replace unidirectional
"SMBJ15CA" can replace "SMBJ15A"
// (But A cannot replace CA in AC applications)

// SS Schottky: same rating comparison
"SS14" vs "SS24" - same voltage, different current

// Transistor series
"MMBT3904" == "2N3904" (different package)
```

---

## Component Types

| Pattern | ComponentType |
|---------|---------------|
| YJ1N*, MBR*, SMBJ*, SMAJ*, SS*, SK*, YJB*, YJDB*, 1N* | DIODE |
| 2N* (except 2N7002), MMBT* | TRANSISTOR |
| 2N7002 | MOSFET |

---

## Related Files

- Handler: `manufacturers/YangjieHandler.java`
- Component types: `ComponentType.DIODE`, `ComponentType.TRANSISTOR`, `ComponentType.MOSFET`

---

## Learnings & Edge Cases

- **2N7002 is a MOSFET**: Despite the 2N prefix (usually transistors), 2N7002 is an N-channel MOSFET. Handler returns MOSFET type.
- **YJ prefix**: Yangjie uses YJ prefix for their branded versions of industry standard parts (YJ1N4007 = 1N4007).
- **MBR naming**: Format is MBR[current][voltage]. MBR1045 = 10A, 45V. MBR2545 = 25A, 45V.
- **TVS polarity**: A suffix = unidirectional, CA suffix = bidirectional. Critical distinction for circuit protection.
- **SS/SK current**: First digit is current (1-5A). SS14 = 1A/40V, SS34 = 3A/40V.
- **Check suffix ordering**: When extracting packages from SS/SK, check longer suffixes (FL) before shorter (L).
- **Bridge rectifier series**: YJB and YJDB are similar bridge rectifiers. YJDB typically in DIP package.
- **1N series signal vs rectifier**: 1N4148 is a signal diode (different from 1N4xxx rectifiers). Check specific pattern first.

<!-- Add new learnings above this line -->
