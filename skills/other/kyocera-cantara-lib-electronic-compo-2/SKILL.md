---
name: kyocera
description: Kyocera Corporation MPN encoding patterns, ceramic resonator and capacitor decoding, and handler guidance. Use when working with Kyocera timing devices, capacitors, or connectors.
---

# Kyocera Corporation Manufacturer Skill

## Overview

Kyocera is a major Japanese manufacturer of electronic components including:
- **CX series**: Ceramic resonators
- **KC/KT series**: Crystal oscillators
- **CT/CM series**: Ceramic capacitors
- **5600/5800 series**: Connectors
- **AVX acquisition products**: Various capacitor lines (acquired 2019)

---

## MPN Structure

### Ceramic Resonators (CX, CXO, CSTS, PBRC)

```
CX-[SIZE][OPTIONS][FREQUENCY]
|    |      |        |
|    |      |        +-- Frequency (if specified separately)
|    |      +-- Package and tolerance options
|    +-- Size code (32 = 3.2x1.5mm, 49 = 4.5x2.0mm)
+-- Series prefix

Example: CX-3215GA
         |  |  ||
         |  |  |+-- A = Tolerance grade
         |  |  +-- G = SMD ceramic package
         |  +-- 3215 = 3.2x1.5mm dimensions
         +-- CX = Ceramic resonator series
```

### Crystal Oscillators (KC, KT)

```
KC[SIZE][VARIANT]-[OPTIONS]
|   |       |        |
|   |       |        +-- Additional options/frequency
|   |       +-- Variant letter (D, B, etc.)
|   +-- 4-digit size code (1612 = 1.6x1.2mm)
+-- Series prefix

Example: KC1612D-C3
         |  |  | ||
         |  |  | |+-- Variant 3
         |  |  | +-- C = Option code
         |  |  +-- D = Differential output
         |  +-- 1612 = 1.6x1.2mm
         +-- KC = Crystal oscillator series
```

### Ceramic Capacitors (CT, CM)

```
CT[SIZE][VALUE][VOLTAGE][DIELECTRIC]
|   |      |       |         |
|   |      |       |         +-- Dielectric type (X7R, X5R, etc.)
|   |      |       +-- Voltage rating
|   |      +-- Capacitance value
|   +-- Size code (31 = 0603, 41 = 0805)
+-- Series prefix
```

### Connectors (5600 series)

```
[SERIES]-[PINCOUNT]-[VARIANT]
   |         |          |
   |         |          +-- Mounting/option variant
   |         +-- Pin count or configuration
   +-- Series number (5600, 5800, etc.)

Example: 5600-050-141
         |    |   |
         |    |   +-- Variant code
         |    +-- 050 = 50 pins (if applicable)
         +-- 5600 = Series
```

---

## Package Size Codes

### Resonator Packages (CX series)

| Size Code | Dimensions | Notes |
|-----------|------------|-------|
| 16 | 1.6x1.0mm | Ultra-small |
| 20 | 2.0x1.2mm | Small |
| 25 | 2.5x2.0mm | Standard small |
| 32 | 3.2x1.5mm | Standard |
| 49 | 4.5x2.0mm | Large |

### Oscillator Packages (KC/KT series)

| Size Code | Dimensions | Common Use |
|-----------|------------|------------|
| 1612 | 1.6x1.2mm | Ultra-miniature |
| 2016 | 2.0x1.6mm | Miniature |
| 2520 | 2.5x2.0mm | Standard small |
| 3215 | 3.2x1.5mm | Standard |
| 3225 | 3.2x2.5mm | Standard |
| 5032 | 5.0x3.2mm | Large |
| 7050 | 7.0x5.0mm | High performance |

### Capacitor Packages (CT/CM series)

| Size Code | Imperial | Metric |
|-----------|----------|--------|
| 01 | 0201 | 0603M |
| 02 | 0402 | 1005M |
| 03 | 0603 | 1608M |
| 05 | 0805 | 2012M |
| 06 | 1206 | 3216M |
| 31 | 0603 | 1608M |
| 41 | 0805 | 2012M |
| 42 | 1206 | 3216M |
| 43 | 1210 | 3225M |
| 45 | 1812 | 4532M |

---

## Series Reference

### Ceramic Resonators

| Series | Description | Typical Frequencies |
|--------|-------------|---------------------|
| CX | Standard ceramic resonator | 400kHz - 70MHz |
| CXO | High-precision ceramic resonator | 1MHz - 50MHz |
| CSTS | 3-terminal ceramic resonator | 400kHz - 20MHz |
| PBRC | Piezoelectric resonator | 400kHz - 4MHz |

### Crystal Oscillators

| Series | Output Type | Features |
|--------|-------------|----------|
| KC | CMOS/TTL | Standard clock |
| KC-B | CMOS | Low power |
| KC-D | Differential | High-speed |
| KT | CMOS | Temperature compensated |

### Ceramic Capacitors

| Series | Class | Application |
|--------|-------|-------------|
| CT | Class II | General purpose |
| CM | Class I | High precision |

---

## Replacement Compatibility

Kyocera parts are compatible when:
1. **Same series** (CX vs CX, KC vs KC)
2. **Same package dimensions** (3.2x1.5mm matches 3.2x1.5mm)
3. **Same frequency** (for resonators/oscillators)

### Upgrade Paths

- Higher stability resonator can replace standard
- AEC-Q200 qualified can replace non-automotive

---

## Common Part Numbers

### Ceramic Resonators

| Part Number | Frequency | Package | Notes |
|-------------|-----------|---------|-------|
| CX-3215GA | 8 MHz | 3.2x1.5mm | SMD ceramic |
| CX-4920GA | 16 MHz | 4.5x2.0mm | SMD ceramic |
| CSTSA-4M00G | 4 MHz | 3.2x1.3mm | 3-terminal |

### Crystal Oscillators

| Part Number | Frequency | Package | Output |
|-------------|-----------|---------|--------|
| KC2520D-C3 | 25 MHz | 2.5x2.0mm | Differential |
| KC3225A | 12 MHz | 3.2x2.5mm | CMOS |
| KC7050B | 50 MHz | 7.0x5.0mm | Low power |

### Connectors

| Part Number | Pins | Pitch | Notes |
|-------------|------|-------|-------|
| 5600-050-141 | 50 | 0.5mm | FPC connector |
| 5800-040-117 | 40 | 0.5mm | FFC connector |

---

## Handler Implementation Notes

### Pattern Matching

```java
// Ceramic resonators - multiple series
Pattern CX_PATTERN = Pattern.compile("^CX[-]?[0-9]{2,4}[A-Z]*.*", Pattern.CASE_INSENSITIVE);
Pattern CSTS_PATTERN = Pattern.compile("^CSTS[A-Z]*[-]?[0-9]+.*", Pattern.CASE_INSENSITIVE);

// Crystal oscillators
Pattern KC_PATTERN = Pattern.compile("^KC[0-9]{4}[A-Z]*[-]?.*", Pattern.CASE_INSENSITIVE);

// Connectors
Pattern CONNECTOR_PATTERN = Pattern.compile("^5[6-9][0-9]{2}[-]?[0-9]+.*", Pattern.CASE_INSENSITIVE);
```

### Package Code Extraction

```java
// CX resonator: size code is positions 2-3 (or 2-4 after normalizing)
String extractResonatorPackage(String mpn) {
    String normalized = mpn.toUpperCase().replace("-", "");
    if (normalized.length() >= 4) {
        String sizeCode = normalized.substring(2, 4);
        return mapResonatorPackage(sizeCode);
    }
    return "";
}

// KC oscillator: size code is 4 digits after KC
String extractOscillatorPackage(String mpn) {
    String normalized = mpn.toUpperCase().replace("-", "");
    if (normalized.length() >= 6) {
        String sizeCode = normalized.substring(2, 6);
        return mapOscillatorPackage(sizeCode);
    }
    return "";
}
```

### Frequency Extraction

```java
// Frequency may be embedded in MPN or in separate suffix
String extractFrequency(String mpn) {
    String upperMpn = mpn.toUpperCase();
    int lastDash = upperMpn.lastIndexOf('-');
    if (lastDash >= 0 && lastDash < upperMpn.length() - 1) {
        String suffix = upperMpn.substring(lastDash + 1);
        if (suffix.matches(".*[0-9]+.*[MK].*") || suffix.matches(".*[0-9]+.*HZ.*")) {
            return suffix;
        }
    }
    return "";
}
```

---

## Related Files

- Handler: `manufacturers/KyoceraHandler.java`
- Component types: `CRYSTAL`, `OSCILLATOR`, `CAPACITOR`, `CONNECTOR`
- Note: Extends `AbstractManufacturerHandler`

---

## AVX Acquisition Notes

Kyocera acquired AVX Corporation in 2019. Some AVX product lines are now branded under Kyocera AVX:
- Tantalum capacitors
- Ceramic capacitors
- Connectors
- Filters

For AVX-branded parts, use the separate AVX handler.

---

## Learnings & Edge Cases

- **Dual branding**: Post-acquisition, some parts may be branded "Kyocera AVX" or "AVX (a Kyocera Company)"
- **Size code normalization**: Remove hyphens before extracting size codes
- **Connector pin count**: May be encoded in second segment of MPN (e.g., 5600-050-xxx where 050 = 50 pins)
- **CSTS 3-terminal**: Different pinout than standard 2-terminal resonators
- **KC-D differential**: Requires differential receiver, not compatible with CMOS inputs

<!-- Add new learnings above this line -->
