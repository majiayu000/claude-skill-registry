---
name: goodark
description: Good-Ark Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Good-Ark diodes, transistors, or GoodArkHandler.
---

# Good-Ark Semiconductor Manufacturer Skill

## Overview

Good-Ark Semiconductor is a Chinese manufacturer specializing in discrete semiconductors including diodes, rectifiers, and transistors. They produce both proprietary series and industry-standard compatible devices.

## MPN Structure

Good-Ark MPNs follow industry-standard patterns with package suffixes:

### Diode Pattern

```
[SERIES][VARIANT][-SUFFIX]
   |        |        |
   |        |        +-- Package/lead-free indicator
   |        +-- Voltage/rating code
   +-- Series prefix (1N, SS, SK, BAV, etc.)
```

### Transistor Pattern

```
[SERIES][NUMBER][VARIANT][SUFFIX]
   |       |        |        |
   |       |        |        +-- Package code
   |       |        +-- Optional variant (A, B)
   |       +-- Part number
   +-- Prefix (2N, MMBT, BC, etc.)
```

### Example Decoding

```
1N4007G
|  |  ||
|  |  |+-- G = DO-41 package
|  |  +-- 7 = 1000V voltage rating
|  +-- 400 = Rectifier series
+-- 1N = Standard diode prefix

MMBT3904LT1
|   |  | ||
|   |  | |+-- 1 = Variant
|   |  | +-- T = SOT package indicator
|   |  +-- L = SOT-23 package
|   +-- 3904 = NPN low power transistor
+-- MMBT = SMD transistor prefix
```

---

## Product Lines

### Standard Rectifier Diodes (1N400x)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| 1N4001 | 50V | 1A | DO-41 |
| 1N4002 | 100V | 1A | DO-41 |
| 1N4003 | 200V | 1A | DO-41 |
| 1N4004 | 400V | 1A | DO-41 |
| 1N4005 | 600V | 1A | DO-41 |
| 1N4006 | 800V | 1A | DO-41 |
| 1N4007 | 1000V | 1A | DO-41 |

### Power Rectifiers (1N540x)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| 1N5400 | 50V | 3A | DO-201AD |
| 1N5401 | 100V | 3A | DO-201AD |
| 1N5402 | 200V | 3A | DO-201AD |
| 1N5404 | 400V | 3A | DO-201AD |
| 1N5406 | 600V | 3A | DO-201AD |
| 1N5408 | 800V | 3A | DO-201AD |

### Signal Diodes

| Part | Description | Package |
|------|-------------|---------|
| 1N4148 | Small signal, 100V | DO-35/SOD-123 |
| 1N4448 | High-speed signal, 100V | DO-35 |
| 1N914 | Signal diode (equiv. 1N4148) | DO-35 |

### Schottky Diodes (SS Series)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SS12 | 20V | 1A | SMA |
| SS14 | 40V | 1A | SMA |
| SS16 | 60V | 1A | SMA |
| SS24 | 40V | 2A | SMA |
| SS34 | 40V | 3A | SMA |
| SS54 | 40V | 5A | SMA |

### Schottky Diodes (SK Series)

| Part | Voltage | Current | Package |
|------|---------|---------|---------|
| SK34 | 40V | 3A | SMB |
| SK36 | 60V | 3A | SMB |
| SK54 | 40V | 5A | SMB |
| SK56 | 60V | 5A | SMB |

### Fast Recovery Diodes (ES/US Series)

| Series | Speed | Applications |
|--------|-------|--------------|
| ES1x | Fast | ES1J, ES1D, ES2D |
| US1x | Ultra-fast | US1M, US1G, US2G |
| UF | Ultra-fast | UF4001-UF4007 |

### Signal Diodes (BAV/BAT Series)

| Series | Type | Examples |
|--------|------|----------|
| BAV | Small signal | BAV21, BAV70, BAV99 |
| BAT | Schottky barrier | BAT54, BAT85, BAT46 |

### TVS Diodes

| Series | Package | Examples |
|--------|---------|----------|
| SMBJ | SMB | SMBJ5.0A, SMBJ15A |
| SMAJ | SMA | SMAJ5.0A, SMAJ15CA |
| P4KE | DO-41 | P4KE6.8A, P4KE15A |
| P6KE | DO-41 | P6KE6.8A, P6KE15A |

### Transistors (2N Series)

| Part | Type | Package |
|------|------|---------|
| 2N2222 | NPN | TO-92 |
| 2N2907 | PNP | TO-92 |
| 2N3904 | NPN low power | TO-92 |
| 2N3906 | PNP low power | TO-92 |
| 2N4401 | NPN high gain | TO-92 |
| 2N4403 | PNP high gain | TO-92 |
| 2N5401 | PNP high voltage | TO-92 |
| 2N5551 | NPN high voltage | TO-92 |

### SMD Transistors (MMBT Series)

| Part | Equivalent | Package |
|------|------------|---------|
| MMBT2222 | 2N2222 | SOT-23 |
| MMBT2907 | 2N2907 | SOT-23 |
| MMBT3904 | 2N3904 | SOT-23 |
| MMBT3906 | 2N3906 | SOT-23 |
| MMBT4401 | 2N4401 | SOT-23 |
| MMBT4403 | 2N4403 | SOT-23 |
| MMBT5401 | 2N5401 | SOT-23 |
| MMBT5551 | 2N5551 | SOT-23 |

### European Transistors (BC Series)

| Part | Type | Package |
|------|------|---------|
| BC547 | NPN | TO-92/SOT-23 |
| BC557 | PNP | TO-92/SOT-23 |
| BC337 | NPN | TO-92 |
| BC327 | PNP | TO-92 |

### Asia-Market Transistors (S Series)

| Part | Type | Application |
|------|------|-------------|
| S8050 | NPN | General purpose |
| S8550 | PNP | General purpose |
| S9012 | PNP | Low noise |
| S9013 | NPN | Low noise |
| S9014 | NPN | Low noise |
| S9015 | PNP | Low noise |
| S9018 | NPN | High frequency |

---

## Package Codes

### Through-Hole Diode Packages

| Code | Package | Notes |
|------|---------|-------|
| A | DO-41 | Standard axial |
| B | DO-15 | Medium current |
| G | DO-35 | Small signal |
| RL | DO-201AD | Power rectifier |
| TAP | DO-41 | Tape and ammo pack |

### SMD Diode Packages

| Code | Package | Notes |
|------|---------|-------|
| S | DO-214AA (SMB) | Medium power SMD |
| F | DO-214AB (SMC) | Large SMD |
| FA | DO-214AC (SMA) | Standard SMD |
| FL | SOD-123FL | Flat lead |
| W | SOD-123 | Small signal SMD |

### Transistor Packages

| Code | Package | Notes |
|------|---------|-------|
| TO | TO-92 | Standard through-hole |
| TA | TO-92 | Alternate suffix |
| TF | TO-92F | Flat package |
| LT | SOT-23 | SMD 3-pin |
| LT1 | SOT-23 | SMD 3-pin |
| G3 | SOT-323 | Small SMD |
| K | SOT-23 | Alternative marking |

### Power Packages

| Code | Package | Notes |
|------|---------|-------|
| CT | TO-220 | Through-hole power |
| TU | TO-220F | Isolated tab |
| D | TO-252 | DPAK |
| D2 | TO-263 | D2PAK |
| D3 | TO-268 | D3PAK |

---

## Handler Implementation Notes

### Pattern Matching

```java
// 1N series diodes
"^1N400[1-7].*"       // Standard rectifiers
"^1N4148.*"           // Signal diode
"^1N914.*"            // Signal diode equivalent
"^1N47[0-9]{2}.*"     // Zener diodes
"^1N540[0-8].*"       // Power rectifiers
"^1N58[0-9]{2}.*"     // Schottky rectifiers

// Schottky diodes
"^SS[1-5][0-9].*"     // SS series
"^SK[1-5][0-9].*"     // SK series
"^SB[1-5][0-9]{2}.*"  // SB series

// Signal diodes
"^BAV[0-9]+.*"        // BAV series
"^BAT[0-9]+.*"        // BAT series

// Fast recovery
"^ES[12][A-Z].*"      // ES series
"^US[12][A-Z].*"      // US series
"^UF[0-9]+.*"         // UF series

// TVS diodes
"^SMBJ[0-9]+.*"       // SMB package
"^SMAJ[0-9]+.*"       // SMA package
"^P[46]KE[0-9]+.*"    // P4KE/P6KE

// Transistors
"^2N[0-9]{3,4}.*"     // 2N series
"^MMBT[A]?[0-9]+.*"   // MMBT/MMBTA series
"^PN[0-9]{4}.*"       // PN series
"^MPSA[0-9]+.*"       // MPSA series
"^BC[0-9]{3}.*"       // BC series
"^S8[05][0-9]{2}.*"   // S80xx series
"^S90[0-9]{2}.*"      // S90xx series
```

### Series Extraction

```java
// Signal diodes (specific before generic)
"1N4148W" -> "1N4148"
"1N914" -> "1N914"

// Rectifiers
"1N4007G" -> "1N400x"
"1N5408RL" -> "1N540x"

// Schottky
"SS14" -> "SS14"
"SK34" -> "SK34"
"SB160" -> "SB160"

// Fast recovery
"ES1J" -> "ES1"
"US1M" -> "US1"

// Transistors
"MMBT3904LT1" -> "MMBT3904"
"2N2222A" -> "2N2222"
"BC547B" -> "BC547"
```

### Replacement Logic

```java
// 1N400x: higher voltage can replace lower
"1N4007" can replace "1N4001" through "1N4007"

// MMBT equivalent to 2N
"MMBT2222" == "2N2222"
"MMBT3904" == "2N3904"

// Signal diode equivalents
"1N4148" == "1N914"

// SS series: higher current can replace lower
"SS34" can replace "SS14" (same voltage, higher current)
```

---

## Component Types

| Pattern | ComponentType |
|---------|---------------|
| 1N*, SS*, SK*, SB*, BAV*, BAT*, ES*, US*, SMBJ*, SMAJ*, P4KE*, P6KE*, MB*S | DIODE |
| 2N*, MMBT*, MMBTA*, PN*, MPSA*, BC*, BF*, S80*, S90* | TRANSISTOR |

---

## Related Files

- Handler: `manufacturers/GoodArkHandler.java`
- Component types: `ComponentType.DIODE`, `ComponentType.TRANSISTOR`

---

## Learnings & Edge Cases

- **1N400x voltage order**: 1N4001=50V, 1N4002=100V, ..., 1N4007=1000V. The digit maps to voltage rating.
- **1N540x voltage order**: 1N5400=50V, 1N5401=100V, ..., 1N5408=800V. Similar pattern but different mapping.
- **MMBT vs 2N**: MMBT is the SMD (SOT-23) equivalent of 2N through-hole transistors. Same electrical specs, different package.
- **PN vs 2N**: PN series (PN2222) is plastic-packaged version of 2N series. Generally interchangeable with 2N.
- **1N4148 vs 1N914**: These are electrically equivalent signal diodes. Can be used interchangeably.
- **SS current rating**: First digit indicates current (SS14=1A, SS34=3A). Higher current can replace lower.
- **S80xx/S90xx series**: Common in Asian markets. S8050/S8550 are general purpose NPN/PNP pairs.
- **BAV70/BAV99**: Dual diode packages (SOT-23). BAV70 = common cathode, BAV99 = series pair.

<!-- Add new learnings above this line -->
