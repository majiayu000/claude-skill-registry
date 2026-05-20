---
name: abracon
description: Abracon MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Abracon timing devices, crystals, oscillators, RF components, or AbraconHandler.
---

# Abracon Manufacturer Skill

## Manufacturer Overview

Abracon is a leading supplier of timing, frequency control, and RF components. Their product portfolio includes:

- **Crystals**: Standard, low-profile, tuning fork, and automotive-grade quartz crystals
- **Oscillators**: Standard clock oscillators, TCXOs, VCXOs, and OCXOs
- **Resonators**: Ceramic and crystal resonators
- **RF Products**: Antennas, filters, baluns, and diplexers
- **RTC Modules**: Real-time clock modules with integrated crystals
- **Inductors**: Air core, multilayer, and power inductors

---

## MPN Structure

Abracon MPNs follow this general structure:

```
[PREFIX][SIZE][VARIANT]-[FREQUENCY]-[OPTIONS]
   |      |       |          |          |
   |      |       |          |          +-- Stability, tolerance, temp grade
   |      |       |          +-- Frequency in MHz (oscillators) or kHz (crystals)
   |      |       +-- Variant letter/number
   |      +-- Size code (02, 03, 07, 08, 10, etc.)
   +-- Product family (ABM, ABL, ASE, etc.)
```

### Product Family Prefixes

| Prefix | Category | Description |
|--------|----------|-------------|
| **Crystals** | | |
| ABM | Standard Crystal | General-purpose quartz crystals |
| ABL | Low Profile Crystal | Low-height SMD crystals |
| ABT | Tuning Fork Crystal | 32.768 kHz watch crystals |
| ABS | Automotive Crystal | AEC-Q200 qualified crystals |
| ABMM | Ceramic Resonator | 3-terminal ceramic resonators |
| ABRC | Crystal Resonator | Crystal-based resonators |
| **Oscillators** | | |
| ASCO | Standard Oscillator | CMOS/TTL clock oscillators |
| ASFL | Low Power Oscillator | Ultra-low power oscillators |
| ASE | EMI Reduced Oscillator | Low-EMI spread spectrum oscillators |
| ASTX | TCXO | Temperature-compensated crystal oscillator |
| ASVTX | VCTCXO | Voltage-controlled TCXO |
| ASV | VCXO | Voltage-controlled crystal oscillator |
| **RF Products** | | |
| ABA | RF Antenna | Chip antennas for WiFi, BT, GPS, cellular |
| ABF | RF Filter | SAW/BAW filters |
| ABB | RF Balun | Impedance matching baluns |
| ABUN | RF Diplexer | Frequency diplexers |
| **RTC Modules** | | |
| AB-RTC | RTC Module | Real-time clock with integrated crystal |
| ABRTS | RTC with SuperCap | RTC with backup power |
| **Inductors** | | |
| AIAL | Air Core Inductor | High-Q RF inductors |
| AIML | Multilayer Inductor | Chip inductors |
| AIRP | Power Inductor | Shielded/unshielded power inductors |

---

## Example MPN Decoding

### Crystal Example

```
ABM3-8.000MHZ-D2Y-T
|  | |     | | | |
|  | |     | | | +-- T = Tape and Reel packaging
|  | |     | | +-- Y = -40 to +85C temperature range
|  | |     | +-- D2 = +/-20ppm frequency tolerance
|  | |     +-- Operating frequency
|  | +-- 3 = 3.2 x 2.5mm package size
|  +-- M = Standard crystal series
+-- AB = Abracon prefix
```

### Oscillator Example

```
ASFL1-12.000MHZ-EC-T
|   | |       | |  |
|   | |       | |  +-- T = Tape and Reel
|   | |       | +-- C = CMOS output
|   | |       +-- E = 5.0 x 3.2mm package
|   | +-- Operating frequency
|   +-- 1 = Series variant
+-- ASFL = Low Power Oscillator
```

### TCXO Example

```
ASTX-H11-32.768KHZ-T
|    |  |         |
|    |  |         +-- T = Tape and Reel
|    |  +-- 32.768 kHz frequency
|    +-- H11 = High stability variant
+-- ASTX = Temperature-Compensated Crystal Oscillator
```

### Antenna Example

```
ABA-25.5-0000E
|   |   |    |
|   |   |    +-- E = Extended variant
|   |   +-- Version/variant code
|   +-- 25.5 = 2.4/5GHz band
+-- ABA = RF Antenna series
```

---

## Package Size Codes

### Crystal Packages (ABM/ABL Series)

| Code | Dimensions | Imperial | Typical Use |
|------|------------|----------|-------------|
| 02 | 2.0 x 1.6mm | - | Ultra-compact designs |
| 03 | 3.2 x 2.5mm | HC49/US | Standard SMD |
| 07 | 7.0 x 5.0mm | HC49SMD | Standard SMD |
| 08 | 8.0 x 4.5mm | HC49S | Through-hole compatible |
| 10 | 10.0 x 4.5mm | HC49/4H | High-power |
| 11 | 11.4 x 4.7mm | HC49/U | Standard through-hole |
| 13 | 13.0 x 4.9mm | HC49 | Large through-hole |

### Oscillator Packages

| Code | Dimensions | Notes |
|------|------------|-------|
| B | 2.0 x 1.6mm | Ultra-miniature |
| C | 2.5 x 2.0mm | Compact |
| D | 3.2 x 2.5mm | Standard small |
| E | 5.0 x 3.2mm | Standard medium |
| F | 7.0 x 5.0mm | Standard large |

### Inductor Packages (AIAL/AIML Series)

| Code | Package Size | Notes |
|------|--------------|-------|
| 02 | 0201 | 0.6 x 0.3mm |
| 03 | 0302 | 0.8 x 0.5mm |
| 05 | 0503 | 1.2 x 0.8mm |
| 10 | 1005 | 2.5 x 1.2mm |
| 15 | 1508 | 4.0 x 2.0mm |
| 20 | 2010 | 5.0 x 2.5mm |

---

## Supported ComponentTypes

The AbraconHandler supports these component types:

| ComponentType | Pattern Examples |
|---------------|------------------|
| CRYSTAL | ABM3-*, ABL5-*, ABT1-*, ABS07-* |
| CRYSTAL_ABRACON | ABM*, ABL*, ABT*, ABS* |
| OSCILLATOR | ASCO*, ASFL*, ASE*, ASTX*, ASV* |
| OSCILLATOR_ABRACON | ASCO*, ASFL*, ASE* |
| OSCILLATOR_TCXO_ABRACON | ASTX*, ASVTX* |
| OSCILLATOR_VCXO_ABRACON | ASXV* |
| OSCILLATOR_OCXO_ABRACON | (declared but no patterns) |
| CLOCK_ABRACON | (declared but no patterns) |
| ANTENNA_ABRACON | (declared but no patterns) |
| RF_FILTER_ABRACON | (declared but no patterns) |
| IC | AB*RTC*, ABRTS*, ABA*, ABF*, ABB*, ABUN* |
| INDUCTOR | AIAL*, AIML*, AIRP* |

**Note**: Some types are declared in `getSupportedTypes()` but may not have corresponding patterns registered in `initializePatterns()`.

---

## Handler Implementation Details

### Package Code Extraction

```java
// Crystals: Extract size code at positions 3-4 after prefix
// ABM03-... -> "03" -> "3.2 x 2.5mm"
String sizeCode = upperMpn.substring(3, 5);

// Oscillators: Package code comes after dash
// ASCO-12.000MHZ-E-T -> "E" -> "5.0 x 3.2mm"
int dashIndex = upperMpn.indexOf('-');
String pkgCode = upperMpn.substring(dashIndex + 1, dashIndex + 3);

// Inductors: Size code at positions 4-5
// AIAL02-... -> "02" -> "0201"
String sizeCode = upperMpn.substring(4, 6);
```

### Series Extraction

The handler returns human-readable series names:

| Prefix | Returned Series |
|--------|-----------------|
| ABM | "Standard Crystal" |
| ABL | "Low Profile Crystal" |
| ABT | "Tuning Fork Crystal" |
| ABS | "Automotive Crystal" |
| ASCO | "Standard Oscillator" |
| ASFL | "Low Power Oscillator" |
| ASE | "EMI Reduced Oscillator" |
| ASTX | "TCXO" |
| ASVTX | "VCTCXO" |
| ASV | "VCXO" |
| ABA | "RF Antenna" |
| ABF | "RF Filter" |
| ABB | "RF Balun" |
| ABUN | "RF Diplexer" |
| AIAL | "Air Core Inductor" |
| AIML | "Multilayer Inductor" |
| AIRP | "Power Inductor" |

### Replacement Compatibility

The `isOfficialReplacement()` method checks:
1. Same series (e.g., both "Standard Crystal")
2. Same package size
3. Same frequency
4. Compatible stability grade (lower PPM can replace higher PPM)

```java
// Stability compatibility: lower PPM (tighter tolerance) can replace higher
// Example: 10PPM crystal can replace 20PPM crystal
int ppm1 = Integer.parseInt(stability1.replace("PPM", ""));
int ppm2 = Integer.parseInt(stability2.replace("PPM", ""));
return ppm1 <= ppm2;  // Lower is better, can replace higher
```

---

## Frequency and Stability Codes

### Common Crystal Frequencies

| Frequency | Application |
|-----------|-------------|
| 32.768 kHz | RTC, watch crystals |
| 8.000 MHz | MCU clocks |
| 12.000 MHz | USB full-speed |
| 16.000 MHz | MCU clocks |
| 20.000 MHz | General timing |
| 24.000 MHz | USB high-speed |
| 25.000 MHz | Ethernet PHY |
| 48.000 MHz | USB full-speed |

### Stability/Tolerance Codes

| Code | Tolerance | Application |
|------|-----------|-------------|
| D1 | +/-10ppm | Precision |
| D2 | +/-20ppm | Standard |
| D3 | +/-30ppm | General purpose |
| D5 | +/-50ppm | Cost-sensitive |

### Temperature Grade Codes

| Code | Range | Application |
|------|-------|-------------|
| Y | -40 to +85C | Industrial |
| E | -20 to +70C | Commercial |
| T | -40 to +105C | Extended |
| A | -40 to +125C | Automotive |

---

## Related Files

- Handler: `manufacturers/AbraconHandler.java`
- Component types: `CRYSTAL`, `CRYSTAL_ABRACON`, `OSCILLATOR`, `OSCILLATOR_ABRACON`, `OSCILLATOR_TCXO_ABRACON`, `OSCILLATOR_VCXO_ABRACON`, `OSCILLATOR_OCXO_ABRACON`

---

## Learnings & Quirks

### Handler Issues (Known)

1. **HashSet in getSupportedTypes()**: Uses mutable `HashSet` instead of `Set.of()`. Should be modernized.

2. **Type/Pattern Mismatch**: `getSupportedTypes()` declares these types that have NO patterns registered:
   - `OSCILLATOR_OCXO_ABRACON` - no OCXO patterns
   - `CLOCK_ABRACON` - no clock patterns
   - `ANTENNA_ABRACON` - no antenna patterns (but ABA* registered as IC)
   - `RF_FILTER_ABRACON` - no filter patterns (but ABF* registered as IC)

3. **RF Products Registered as IC**: Antennas (ABA), filters (ABF), baluns (ABB), and diplexers (ABUN) are registered under `ComponentType.IC` instead of their specific types.

4. **VCXO Pattern Mismatch**: The pattern for OSCILLATOR_VCXO_ABRACON uses `^ASXV[0-9].*` but the base OSCILLATOR type uses `^ASV[0-9].*` (note ASXV vs ASV).

### MPN Pattern Notes

- All Abracon crystal/oscillator MPNs start with "AB" or "AS"
- Frequency is typically after the first dash
- Size code position varies by product family:
  - Crystals (ABM/ABL): positions 3-4
  - Inductors (AIAL/AIML): positions 4-5
  - Oscillators: after dash in options section

### Replacement Part Guidance

- Crystals with tighter tolerance (lower PPM) can replace looser tolerance parts
- Must match: frequency, package size, load capacitance
- Consider: temperature grade (automotive needs AEC-Q200)

### Testing Notes

- No existing test file for AbraconHandler (listed in "Handlers Without Tests")
- When creating tests, use package `no.cantara.electronic.component.lib.handlers` (NOT `manufacturers`)
- Test frequency extraction, package code mapping, and series identification

<!-- Add new learnings above this line -->
