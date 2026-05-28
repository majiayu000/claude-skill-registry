---
name: epson
description: Epson timing devices MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Epson crystals, oscillators, RTCs, or EpsonHandler.
---

# Epson Timing Devices Manufacturer Skill

## Manufacturer Overview

Epson (Seiko Epson Corporation) is a leading manufacturer of **timing devices** including:

- **Crystal Units**: AT-cut crystals, tuning fork crystals, ceramic package crystals
- **Oscillators**: Standard clock oscillators (SPXO), programmable oscillators
- **TCXOs**: Temperature Compensated Crystal Oscillators (high stability)
- **VCXOs**: Voltage Controlled Crystal Oscillators
- **OCXOs**: Oven Controlled Crystal Oscillators (ultra-high stability)
- **RTC Modules**: Real-Time Clock modules with integrated crystals
- **Timing ICs**: Programmable timers, RTC ICs

Epson's timing devices are known for high precision and reliability, widely used in communications, automotive, industrial, and consumer electronics.

---

## MPN Structure

Epson MPNs follow this general structure:

```
[FAMILY][SIZE/MODEL]-[SPEC][FREQUENCY][OPTIONS]
   |        |           |       |         |
   |        |           |       |         +-- Temperature grade, packaging
   |        |           |       +-- Frequency code (MHz or kHz)
   |        |           +-- Specification variant
   |        +-- Size code or model number
   +-- Product family prefix (FA, FC, SG, TG, etc.)
```

### Family Prefixes

| Prefix | Product Type | Description |
|--------|--------------|-------------|
| FA | AT-Cut Crystal | Fundamental and overtone crystals |
| FC | Tuning Fork Crystal | 32.768 kHz crystals for RTC |
| MA | High Frequency Crystal | MHz range crystals |
| MC | Ceramic Package Crystal | Crystals in ceramic packages |
| SG | Standard Oscillator | SPXO (Simple Packaged Crystal Oscillator) |
| TG | TCXO | Temperature Compensated Crystal Oscillator |
| VG | VCXO | Voltage Controlled Crystal Oscillator |
| HG | OCXO | Oven Controlled Crystal Oscillator |
| RX | RTC Module | Real-Time Clock with integrated crystal |
| RA | Programmable Timer | Timer ICs |
| RR | RTC IC | Real-Time Clock ICs |

---

## Example MPN Decoding

### Crystal Example

```
FA-128 32.0000MF10X-K3
|   |   |        |  |
|   |   |        |  +-- K3 = Packaging/tape specification
|   |   |        +-- F10X = Frequency tolerance spec
|   |   +-- 32.0000M = 32 MHz frequency
|   +-- 128 = Size code (1.2 x 1.0mm)
+-- FA = AT-Cut Crystal family
```

### Oscillator Example

```
SG-210STF 24.0000ML0
|    |    |        |
|    |    |        +-- L0 = Operating voltage/stability spec
|    |    +-- 24.0000M = 24 MHz frequency
|    +-- 210 = Size code (2.0 x 1.6mm) + STF variant
+-- SG = Standard Oscillator
```

### RTC Module Example

```
RX-8900CE UA
|    |    |  |
|    |    |  +-- UA = Package variant
|    |    +-- CE = Specific model variant
|    +-- 8900 = High Accuracy RTC series
+-- RX = RTC Module family
```

---

## Supported Component Types

The EpsonHandler supports these ComponentTypes:

| ComponentType | Description | Example Prefixes |
|---------------|-------------|------------------|
| `CRYSTAL` | Generic crystal type | FA, FC, MA, MC |
| `CRYSTAL_EPSON` | Epson-specific crystal | FA, FC, MA, MC |
| `OSCILLATOR` | Generic oscillator type | SG, TG, VG, HG |
| `OSCILLATOR_EPSON` | Epson-specific oscillator | SG |
| `OSCILLATOR_TCXO_EPSON` | Temperature compensated | TG |
| `OSCILLATOR_VCXO_EPSON` | Voltage controlled | VG |
| `OSCILLATOR_OCXO_EPSON` | Oven controlled | HG |
| `RTC_EPSON` | RTC modules | RX |
| `TIMER_EPSON` | Programmable timers | RA |
| `GYRO_SENSOR_EPSON` | Gyroscope sensors | (not in patterns) |

---

## Package Code Extraction

### Crystal Packages (FA, FC)

The handler extracts package size from the model number after the hyphen:

| Size Code | Package Dimensions |
|-----------|-------------------|
| 128 | 1.2 x 1.0mm |
| 135 | 1.6 x 1.2mm |
| 238 | 2.0 x 1.6mm |
| 328 | 3.2 x 2.5mm |
| 405 | 4.0 x 2.5mm |
| 506 | 5.0 x 3.2mm |

**Extraction Logic:**
```java
// Extract 3 characters after the first hyphen
String sizeCode = mpn.substring(mpn.indexOf('-') + 1, mpn.indexOf('-') + 4);
// Map to actual dimensions
```

### Oscillator Packages (SG, TG, VG, HG)

The handler extracts package size from the model number:

| Model Code | Package Dimensions |
|------------|-------------------|
| 210 | 2.0 x 1.6mm |
| 310 | 2.5 x 2.0mm |
| 510 | 3.2 x 2.5mm |
| 531 | 5.0 x 3.2mm |
| 7050 | 7.0 x 5.0mm |
| 8002 | 8.0 x 4.5mm |

**Extraction Logic:**
```java
// Extract up to 4 characters after the first hyphen
String modelNum = mpn.substring(mpn.indexOf('-') + 1, mpn.indexOf('-') + 5);
// Map to actual dimensions
```

---

## Series Extraction

The handler extracts series names based on prefix and model variants:

### Crystal Series

| Prefix | Contains | Series Name |
|--------|----------|-------------|
| FA | - | AT-Cut Crystal |
| FC | - | Tuning Fork Crystal |
| MA | - | High Frequency Crystal |
| MC | - | Ceramic Package Crystal |

### Oscillator Series

| Prefix | Contains | Series Name |
|--------|----------|-------------|
| SG | 210 | Programmable Oscillator |
| SG | (other) | Standard Oscillator |
| TG | 3541 | High Stability TCXO |
| TG | (other) | TCXO |
| VG | 4513 | High Stability VCXO |
| VG | (other) | VCXO |
| HG | - | OCXO |

### RTC Series

| Prefix | Contains | Series Name |
|--------|----------|-------------|
| RX | 4571 | Low Power RTC |
| RX | 8900 | High Accuracy RTC |
| RX | (other) | RTC Module |

### Timing IC Series

| Prefix | Series Name |
|--------|-------------|
| RA | Programmable Timer |
| RR | RTC IC |

---

## Frequency Code Patterns

Epson MPNs often include frequency specifications:

| Format | Meaning | Example |
|--------|---------|---------|
| `XX.XXXXMHZ` | Megahertz | 24.0000MHZ |
| `XX.XXXXM` | Megahertz (short) | 24.0000M |
| `32.768K` | Kilohertz | 32.768K (standard RTC frequency) |

---

## Common Example MPNs

### Crystals

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| FA-128 8.0000MF20X-K3 | AT-Cut | 1.2 x 1.0mm | 8 MHz |
| FA-238 16.0000MB-W3 | AT-Cut | 2.0 x 1.6mm | 16 MHz |
| FC-135 32.7680KA-A3 | Tuning Fork | 1.6 x 1.2mm | 32.768 kHz |
| MC-306 32.7680KA-A0 | Ceramic | 3.2 x 1.5mm | 32.768 kHz |

### Oscillators

| MPN | Type | Size | Frequency |
|-----|------|------|-----------|
| SG-210STF 24.0000ML0 | Standard | 2.0 x 1.6mm | 24 MHz |
| SG-310STF 48.0000MB0 | Standard | 2.5 x 2.0mm | 48 MHz |
| TG-3541CE 10.0000MC-C | TCXO | 5.0 x 3.2mm | 10 MHz |
| VG-4513CA 25.0000M | VCXO | 5.0 x 3.2mm | 25 MHz |

### RTC Modules

| MPN | Type | Features |
|-----|------|----------|
| RX-4571LC | Low Power RTC | Ultra-low power |
| RX-8900CE UA | High Accuracy | Temperature compensation |
| RX-8010SJ | Standard RTC | I2C interface |

---

## Handler Implementation Notes

### Pattern Registration

The handler registers patterns for both base and manufacturer-specific types:

```java
// Crystal patterns - register for BOTH types
registry.addPattern(ComponentType.CRYSTAL, "^FA-?[0-9].*");
registry.addPattern(ComponentType.CRYSTAL_EPSON, "^FA-?[0-9].*");
```

### Replacement Compatibility

The `isOfficialReplacement()` method considers:

1. **Same series** - Different series are never replacements
2. **Same package** - Package must match for physical compatibility
3. **High stability upgrade** - High stability versions can replace standard
4. **Same frequency** - Frequency code must match

```java
// High stability can replace standard
if (series1.contains("High Stability") &&
    series2.replace("High Stability ", "").equals(series1.replace("High Stability ", ""))) {
    return true;
}
```

### Frequency Extraction

The handler extracts frequency from the suffix after the last hyphen:

```java
private String extractFrequencyCode(String mpn) {
    int freqStart = mpn.lastIndexOf('-');
    if (freqStart >= 0 && freqStart < mpn.length() - 1) {
        return mpn.substring(freqStart + 1);
    }
    return "";
}
```

---

## Related Files

- Handler: `manufacturers/EpsonHandler.java`
- Component types: `CRYSTAL`, `CRYSTAL_EPSON`, `OSCILLATOR`, `OSCILLATOR_EPSON`, `OSCILLATOR_TCXO_EPSON`, `OSCILLATOR_VCXO_EPSON`, `OSCILLATOR_OCXO_EPSON`, `RTC_EPSON`, `TIMER_EPSON`, `GYRO_SENSOR_EPSON`

---

## Learnings & Quirks

### Handler Issues (Identified)

- **HashSet in getSupportedTypes()**: Should use `Set.of()` for immutability
- **Missing IC type**: RTC and timer patterns are registered under `ComponentType.IC` but `IC` is not in `getSupportedTypes()`
- **Package extraction edge case**: If MPN has no hyphen, `indexOf('-')` returns -1, causing `StringIndexOutOfBoundsException` (handler catches this)
- **Model number length varies**: Package extraction assumes 3-4 character model numbers, but some products may differ

### MPN Format Variations

- **With hyphen**: `FA-128`, `SG-210STF` (standard format)
- **Without hyphen**: `FA128`, `SG210` (some datasheets omit hyphen)
- **Pattern handles both**: `^FA-?[0-9].*` uses `-?` for optional hyphen

### Oscillator Type Hierarchy

| Type | Stability | Use Case |
|------|-----------|----------|
| SPXO (SG) | Standard | General timing |
| TCXO (TG) | High | Mobile, GPS |
| VCXO (VG) | Medium, tunable | PLL, clock recovery |
| OCXO (HG) | Ultra-high | Telecom, instrumentation |

### RTC Module Selection

| Series | Power | Accuracy | Interface |
|--------|-------|----------|-----------|
| RX-4571 | Ultra-low | Standard | I2C |
| RX-8900 | Low | High | I2C/SPI |
| RX-8010 | Standard | Standard | I2C |

### Competing Products

| Epson | NDK | TXC | Kyocera |
|-------|-----|-----|---------|
| FA-xxx | NX series | 7A series | KC series |
| SG-xxx | NT series | 8Z series | KT series |
| TG-xxx | NT series | 8P series | KT series |

<!-- Add new learnings above this line -->
