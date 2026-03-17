---
name: ndk
description: NDK (Nihon Dempa Kogyo) timing devices MPN encoding patterns, suffix decoding, and handler guidance. Use when working with NDK crystals, oscillators, TCXOs, VCXOs, OCXOs, VCSOs, or SAW devices.
---

# NDK (Nihon Dempa Kogyo) Manufacturer Skill

## Manufacturer Overview

NDK (Nihon Dempa Kogyo Co., Ltd.) is a leading Japanese manufacturer of **timing devices and frequency control products** including:

- **Crystal Units**: Standard crystals (NX), tuning fork crystals (NT), high frequency crystals (NH), automotive grade (NAT)
- **Clock Oscillators**: Standard oscillators (NZ), programmable oscillators (NP), low jitter oscillators (NV)
- **TCXOs**: Temperature Compensated Crystal Oscillators (NT, NTW)
- **VCXOs**: Voltage Controlled Crystal Oscillators (NV, NVW)
- **OCXOs**: Oven Controlled Crystal Oscillators (NO, NH)
- **VCSOs**: Voltage Controlled SAW Oscillators (VS, VSW)
- **SAW Devices**: SAW filters (SF), SAW resonators (SR), SAW duplexers (SD)

NDK is known for high-precision timing components used in telecommunications, networking, automotive, and industrial applications.

---

## MPN Structure

NDK MPNs follow this general structure:

```
[PREFIX][SIZE][VARIANT]-[FREQUENCY][OPTIONS]
   |       |      |          |         |
   |       |      |          |         +-- Temperature grade, packaging
   |       |      |          +-- Frequency code (MHz or kHz)
   |       |      +-- Variant/specification letter
   |       +-- Size code (2 digits indicating package dimensions)
   +-- Product family prefix (NX, NT, NZ, NV, etc.)
```

### Family Prefixes

| Prefix | Product Type | Description |
|--------|--------------|-------------|
| NX | Standard Crystal | AT-cut MHz range crystals |
| NT | Tuning Fork Crystal / TCXO | 32.768 kHz crystals or TCXOs |
| NH | High Frequency Crystal | High frequency AT-cut crystals |
| NAT | Automotive Crystal | AEC-Q200 qualified crystals |
| NZ | Standard Oscillator | SPXO (Simple Packaged Crystal Oscillator) |
| NP | Programmable Oscillator | User-programmable frequency |
| NV | VCXO / Low Jitter | Voltage controlled or low jitter oscillators |
| NTW | Wide Temp TCXO | Extended temperature range TCXO |
| NVW | Wide Pull VCXO | Extended pull range VCXO |
| NO | OCXO | Oven Controlled Crystal Oscillator |
| VS | VCSO | Voltage Controlled SAW Oscillator |
| VSW | Wide Pull VCSO | Extended pull range VCSO |
| SF | SAW Filter | Surface Acoustic Wave filter |
| SR | SAW Resonator | Surface Acoustic Wave resonator |
| SD | SAW Duplexer | Surface Acoustic Wave duplexer |

---

## Example MPN Decoding

### Crystal Example

```
NX3225SA-24.000M
|  |  | |     |
|  |  | |     +-- 24.000M = 24 MHz frequency
|  |  | +-- - = Separator
|  |  +-- SA = Series/specification variant
|  +-- 32 25 = 3.2 x 2.5mm package
+-- NX = Standard Crystal family
```

### Oscillator Example

```
NZ2520SDA-20.000M
|  |  |  |     |
|  |  |  |     +-- 20.000M = 20 MHz frequency
|  |  |  +-- - = Separator
|  |  +-- SDA = Series/specification variant
|  +-- 25 20 = 2.5 x 2.0mm package (note: size code is first 2 digits after prefix)
+-- NZ = Standard Oscillator family
```

### Automotive Crystal Example

```
NAT3225SBTC-25.000M
|   |   |     |
|   |   |     +-- 25.000M = 25 MHz frequency
|   |   +-- SBTC = Automotive specification variant
|   +-- 32 25 = 3.2 x 2.5mm package
+-- NAT = Automotive grade Crystal
```

---

## Supported Component Types

The NDKHandler supports these ComponentTypes:

| ComponentType | Description | Example Prefixes |
|---------------|-------------|------------------|
| `CRYSTAL` | Generic crystal type | NX, NT, NH, NAT |
| `CRYSTAL_NDK` | NDK-specific crystal | NX, NT, NH, NAT |
| `OSCILLATOR` | Generic oscillator type | NZ, NP, NV, NT, NTW, NVW, NO, NH, VS, VSW |
| `OSCILLATOR_NDK` | NDK-specific oscillator | NZ, NP, NV |
| `OSCILLATOR_TCXO_NDK` | Temperature compensated | NT, NTW |
| `OSCILLATOR_VCXO_NDK` | Voltage controlled | NV, NVW |
| `OSCILLATOR_OCXO_NDK` | Oven controlled | NO, NH |
| `SAW_FILTER_NDK` | SAW filter devices | SF |
| `SAW_RESONATOR_NDK` | SAW resonator devices | SR |

**Note**: SAW devices (SF, SR, SD) are registered under `ComponentType.IC` in patterns but `SAW_FILTER_NDK` and `SAW_RESONATOR_NDK` are listed in `getSupportedTypes()`.

---

## Package Code Extraction

The handler extracts package dimensions from the size code in the MPN. The size code is positions 3-4 (0-indexed) after the prefix.

### Crystal Packages (NX, NT, NH, NAT)

| Size Code | Package Dimensions |
|-----------|-------------------|
| 12 | 1.2 x 1.0mm |
| 16 | 1.6 x 1.2mm |
| 20 | 2.0 x 1.6mm |
| 25 | 2.5 x 2.0mm |
| 32 | 3.2 x 2.5mm |
| 50 | 5.0 x 3.2mm |
| 80 | 8.0 x 4.5mm |

**Extraction Logic:**
```java
// For crystals: extract characters at positions 3-4 (after NX, NT, NH, or NAT prefix)
// Example: NX3225SA → position 3 is "3", position 4 is "2" → "32" → 3.2 x 2.5mm
String sizeCode = upperMpn.substring(3, 5);  // Gets "32" from "NX3225..."
```

### Oscillator Packages (NZ, NP, NV, NO)

| Size Code | Package Dimensions |
|-----------|-------------------|
| 21 | 2.0 x 1.6mm |
| 25 | 2.5 x 2.0mm |
| 32 | 3.2 x 2.5mm |
| 50 | 5.0 x 3.2mm |
| 70 | 7.0 x 5.0mm |
| 98 | 9.8 x 7.5mm |

**Extraction Logic:**
```java
// For oscillators: extract characters at positions 3-4
// Example: NZ2520SDA → "25" → 2.5 x 2.0mm
String sizeCode = upperMpn.substring(3, 5);
```

---

## Series Extraction

The handler returns descriptive series names based on the MPN prefix:

### Crystal Series

| Prefix | Series Name |
|--------|-------------|
| NX | Standard Crystal |
| NT | Tuning Fork Crystal |
| NH | High Frequency Crystal |
| NAT | Automotive Crystal |

### Oscillator Series

| Prefix | Variant Check | Series Name |
|--------|---------------|-------------|
| NZ | - | Standard Oscillator |
| NP | - | Programmable Oscillator |
| NV | char[2] == 'W' | Wide Pull VCXO |
| NV | (other) | VCXO |
| NT | char[2] == 'W' | Wide Temp TCXO |
| NT | (other) | TCXO |
| NO | - | OCXO |
| NH | (not crystal pattern) | High Stability OCXO |

### VCSO Series

| Prefix | Series Name |
|--------|-------------|
| VS | VCSO |
| VSW | Wide Pull VCSO |

### SAW Device Series

| Prefix | Series Name |
|--------|-------------|
| SF | SAW Filter |
| SR | SAW Resonator |
| SD | SAW Duplexer |

---

## Frequency Code Patterns

NDK MPNs include frequency specifications after the hyphen:

| Format | Meaning | Example |
|--------|---------|---------|
| `XX.XXXM` | Megahertz | 24.000M, 48.000M |
| `XX.XXXXM` | Megahertz (4 decimal) | 24.0000M |
| `32.768K` | 32.768 kHz | Tuning fork crystal frequency |

**Extraction Logic:**
```java
private String extractFrequencyCode(String mpn) {
    // Extract everything after the last hyphen
    int lastDash = mpn.lastIndexOf('-');
    if (lastDash >= 0 && lastDash < mpn.length() - 1) {
        return mpn.substring(lastDash + 1);
    }
    return "";
}
```

---

## Common Example MPNs

### Standard Crystals (NX)

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| NX3225SA-24.000M | Standard | 3.2 x 2.5mm | 24 MHz |
| NX2520SA-16.000M | Standard | 2.5 x 2.0mm | 16 MHz |
| NX2016SA-32.000M | Standard | 2.0 x 1.6mm | 32 MHz |
| NX5032GA-8.000M | Standard | 5.0 x 3.2mm | 8 MHz |

### Tuning Fork Crystals (NT)

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| NT2012SA-32.768K | Tuning Fork | 2.0 x 1.2mm | 32.768 kHz |
| NT1612SA-32.768K | Tuning Fork | 1.6 x 1.2mm | 32.768 kHz |

### Automotive Crystals (NAT)

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| NAT3225SBTC-25.000M | Automotive | 3.2 x 2.5mm | 25 MHz |
| NAT2520SBTA-20.000M | Automotive | 2.5 x 2.0mm | 20 MHz |

### Standard Oscillators (NZ)

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| NZ2520SDA-20.000M | Standard | 2.5 x 2.0mm | 20 MHz |
| NZ3225SDA-24.000M | Standard | 3.2 x 2.5mm | 24 MHz |
| NZ5032SDA-50.000M | Standard | 5.0 x 3.2mm | 50 MHz |

### TCXOs (NT oscillator)

| MPN | Type | Size | Stability |
|-----|------|------|-----------|
| NT2520SD-26.000M | TCXO | 2.5 x 2.0mm | Standard |
| NTW3225CC-26.000M | Wide Temp TCXO | 3.2 x 2.5mm | Extended temp |

### VCXOs (NV)

| MPN | Type | Size | Pull Range |
|-----|------|------|------------|
| NV2520SA-100.000M | VCXO | 2.5 x 2.0mm | Standard |
| NVW3225SD-155.520M | Wide Pull VCXO | 3.2 x 2.5mm | Extended |

### OCXOs (NO)

| MPN | Type | Size | Stability |
|-----|------|------|-----------|
| NO5032SD-10.000M | OCXO | 5.0 x 3.2mm | High |
| NO7050SD-10.000M | OCXO | 7.0 x 5.0mm | Very High |

---

## Handler Implementation Notes

### Pattern Registration

The handler registers patterns for both base types and NDK-specific types:

```java
// Crystal patterns - register for BOTH generic and manufacturer-specific types
registry.addPattern(ComponentType.CRYSTAL, "^NX[0-9].*");
registry.addPattern(ComponentType.CRYSTAL_NDK, "^NX[0-9].*");
```

### Prefix Overlap Issues

**NT Prefix Conflict**: The `NT` prefix is used for BOTH:
- Tuning fork crystals (when followed by size code like NT1612, NT2012)
- TCXOs (Temperature Compensated Crystal Oscillators)

The handler's `extractSeries()` method has overlapping checks:
```java
// This check comes first, returning "Tuning Fork Crystal"
if (upperMpn.startsWith("NT")) return "Tuning Fork Crystal";

// This check is never reached because the first one matches
if (upperMpn.startsWith("NT") && upperMpn.length() > 3) {
    // TCXO logic
}
```

**NH Prefix Conflict**: The `NH` prefix is used for BOTH:
- High frequency crystals
- High stability OCXOs

### Replacement Compatibility

The `isOfficialReplacement()` method checks:

1. **Series compatibility** - Same series or compatible upgrade path
2. **Package match** - Same physical dimensions required
3. **Frequency match** - Identical frequency code required

```java
// Compatible series: Wide temp/stability can replace standard
if (series1.startsWith("Wide Temp") &&
    series2.equals(series1.replace("Wide Temp ", ""))) return true;
if (series1.startsWith("High Stability") &&
    series2.equals(series1.replace("High Stability ", ""))) return true;
```

---

## Related Files

- Handler: `manufacturers/NDKHandler.java`
- Component types: `CRYSTAL`, `CRYSTAL_NDK`, `OSCILLATOR`, `OSCILLATOR_NDK`, `OSCILLATOR_TCXO_NDK`, `OSCILLATOR_VCXO_NDK`, `OSCILLATOR_OCXO_NDK`, `SAW_FILTER_NDK`, `SAW_RESONATOR_NDK`

---

## Learnings & Quirks

### Handler Issues (Identified)

- **HashSet in getSupportedTypes()**: Uses mutable `HashSet`, should use `Set.of()` for immutability (see CLAUDE.md "Handlers Without Tests" section)
- **Missing IC type in getSupportedTypes()**: SAW devices (SF, SR, SD) register patterns under `ComponentType.IC` but `IC` is not in `getSupportedTypes()`
- **NT prefix ambiguity**: Same prefix used for tuning fork crystals AND TCXOs; series extraction logic has unreachable code
- **NH prefix ambiguity**: Same prefix used for high frequency crystals AND high stability OCXOs
- **Package extraction position**: Uses fixed positions 3-4 which assumes 2-letter prefix; NAT (3-letter) will extract wrong characters ("T3" from "NAT3225...")

### Size Code Mapping

NDK uses a unique size code system where digits represent dimensions:
- First digit = first dimension (mm), second digit = second dimension
- "32" = 3.2mm x 2.5mm (but "25" in oscillators = 2.5mm x 2.0mm)
- The mapping is not always intuitive; always verify against datasheet

### Oscillator Type Hierarchy

| Type | Stability | Temperature Range | Use Case |
|------|-----------|-------------------|----------|
| SPXO (NZ) | ±25-50 ppm | -20 to +70°C | General timing |
| TCXO (NT) | ±0.5-2 ppm | -30 to +85°C | Cellular, GPS, IoT |
| VCXO (NV) | ±25-50 ppm | -20 to +70°C | PLL, clock recovery |
| OCXO (NO) | ±0.01-0.1 ppm | -40 to +85°C | Telecom, instrumentation |

### SAW Device Applications

| Type | Application |
|------|-------------|
| SF (Filter) | RF filtering in mobile phones, base stations |
| SR (Resonator) | Timing reference for RF circuits |
| SD (Duplexer) | Simultaneous TX/RX in wireless devices |

### Competing Products

| NDK | Epson | TXC | Kyocera/AVX | Murata |
|-----|-------|-----|-------------|--------|
| NX series | FA series | 7A series | KC series | - |
| NZ series | SG series | 8Z series | KT series | - |
| NT (TCXO) | TG series | 8P series | - | - |
| SF/SR/SD | - | - | - | SAW devices |

### Temperature Grade Suffixes

Common temperature grade indicators in NDK MPNs:
- No suffix: Commercial (0°C to +70°C)
- T or TC: Industrial (-40°C to +85°C)
- A or AC: Automotive (-40°C to +125°C)

### Packaging/Tape Options

| Suffix | Meaning |
|--------|---------|
| -K or K3 | Tape and reel packaging |
| (no suffix) | Tray packaging |

<!-- Add new learnings above this line -->
