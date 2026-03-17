---
name: iqd
description: IQD Frequency Products MPN encoding patterns, package decoding, and handler guidance. Use when working with IQD crystals, oscillators, TCXOs, VCXOs, or OCXOs.
---

# IQD Frequency Products Manufacturer Skill

## Manufacturer Overview

IQD (International Quartz Devices) is a UK-based manufacturer specializing in frequency control products. Their product range includes:

- **Crystals**: Low frequency, standard, SMD, and through-hole crystal units
- **Oscillators**: Standard clock oscillators (XO)
- **TCXOs**: Temperature Compensated Crystal Oscillators
- **VCXOs**: Voltage Controlled Crystal Oscillators
- **OCXOs**: Oven Controlled Crystal Oscillators
- **Clock Modules**: Integrated timing solutions
- **RTC Modules**: Real-Time Clock modules
- **Filters**: Crystal filters, SAW filters, resonator bandpass

---

## MPN Structure

IQD MPNs follow product-family-specific structures:

### Crystal Units

```
[PREFIX][SIZE]-[FREQUENCY]-[TOLERANCE]-[LOAD]-[TEMP]
   |      |        |           |        |       |
   |      |        |           |        |       +-- Temperature range
   |      |        |           |        +-- Load capacitance
   |      |        |           +-- Frequency tolerance (PPM)
   |      |        +-- Frequency value
   |      +-- Size code (e.g., 016, 020, 032)
   +-- Series prefix (CFPX, XTALS, XTAL, LFXTAL)
```

### Oscillators (XO, TCXO, VCXO, OCXO)

```
[PREFIX]-[SIZE][SPEC]-[FREQUENCY]-[STABILITY]-[OUTPUT]
   |       |     |         |          |          |
   |       |     |         |          |          +-- Output type
   |       |     |         |          +-- Stability (PPM)
   |       |     |         +-- Frequency value
   |       |     +-- Specification variant (H=High freq, L=Low power)
   |       +-- Package size code (21, 25, 32, 50, 70, 90)
   +-- Family prefix (IQXO, IQTX, IQVCXO, IQOCXO)
```

---

## Example Decoding

### Crystal Examples

```
CFPX-032-16.000MHz-10ppm
|    |      |        |
|    |      |        +-- 10 PPM frequency tolerance
|    |      +-- 16.000 MHz frequency
|    +-- 032 = 3.2 x 2.5mm package
+-- Standard Crystal series

XTALS-020-8.000MHz
|     |      |
|     |      +-- 8.000 MHz frequency
|     +-- 020 = 2.0 x 1.6mm package
+-- SMD Crystal series

LFXTAL-25.000kHz
|        |
|        +-- 25.000 kHz (low frequency)
+-- Low Frequency Crystal series
```

### Oscillator Examples

```
IQXO-32-16.000MHz
|    |     |
|    |     +-- 16.000 MHz output frequency
|    +-- 32 = 3.2 x 2.5mm package
+-- Standard Oscillator

IQXO-L50-1.000MHz
|    ||    |
|    ||    +-- 1.000 MHz frequency
|    |+-- 50 = 5.0 x 3.2mm package
|    +-- L = Low Power variant
+-- Low Power Oscillator

IQTX-H25-10.000MHz-0.5PPM
|    ||     |         |
|    ||     |         +-- 0.5 PPM stability
|    ||     +-- 10.000 MHz frequency
|    |+-- 25 = 2.5 x 2.0mm package
|    +-- H = High Stability variant
+-- High Stability TCXO

IQVCXO-32-100.000MHz
|      |      |
|      |      +-- 100.000 MHz center frequency
|      +-- 32 = 3.2 x 2.5mm package
+-- Voltage Controlled Crystal Oscillator

IQOCXO-H70-10.000MHz-1PPB
|      ||     |        |
|      ||     |        +-- 1 PPB (parts per billion) stability
|      ||     +-- 10.000 MHz frequency
|      |+-- 70 = 7.0 x 5.0mm package
|      +-- H = High Stability variant
+-- High Stability Oven Controlled Crystal Oscillator
```

### Module Examples

```
IQCM-100-25.000MHz
|       |     |
|       |     +-- 25.000 MHz output
|       +-- Series/variant code
+-- Clock Module

IQRTC-32768Hz
|        |
|        +-- 32.768 kHz (standard RTC frequency)
+-- RTC Module

IQXF-455kHz
|      |
|      +-- 455 kHz center frequency
+-- Crystal Filter

IQSPF-100.000MHz
|       |
|       +-- 100.000 MHz center frequency
+-- SAW Filter
```

---

## Package Codes

### Crystal Packages (CFPX, XTALS series)

Size codes appear after a dash and indicate package dimensions:

| Code | Package Size | Common Use |
|------|--------------|------------|
| 016 | 1.6 x 1.2mm | Ultra-small SMD |
| 020 | 2.0 x 1.6mm | Small SMD |
| 025 | 2.5 x 2.0mm | Standard SMD |
| 032 | 3.2 x 2.5mm | Standard SMD (most common) |
| 050 | 5.0 x 3.2mm | Larger SMD |
| 070 | 7.0 x 5.0mm | Large SMD |

### Oscillator Packages (IQXO, IQTX, IQVCXO, IQOCXO series)

Size codes appear after the dash (or after H/L modifier):

| Code | Package Size | Common Use |
|------|--------------|------------|
| 21 | 2.0 x 1.6mm | Ultra-compact oscillators |
| 25 | 2.5 x 2.0mm | Compact oscillators |
| 32 | 3.2 x 2.5mm | Standard oscillators |
| 50 | 5.0 x 3.2mm | Standard/high stability |
| 70 | 7.0 x 5.0mm | High stability / OCXO |
| 90 | 9.0 x 7.0mm | High stability OCXO |

---

## Component Type Prefixes

### Crystal Prefixes

| Prefix | Component Type | Description |
|--------|----------------|-------------|
| LFXTAL | Low Frequency Crystal | 32.768 kHz and other low frequencies |
| CFPX | Standard Crystal | General purpose SMD crystals |
| XTALS | SMD Crystal | Surface mount crystal units |
| XTAL | Through-hole Crystal | Leaded crystal units (HC-49, etc.) |

### Oscillator Prefixes

| Prefix | Component Type | Description |
|--------|----------------|-------------|
| IQXO | Standard Oscillator | Basic clock oscillator (XO) |
| IQXO-H | High Frequency Oscillator | Higher frequency range XO |
| IQXO-L | Low Power Oscillator | Reduced power consumption XO |
| IQTX | TCXO | Temperature Compensated Crystal Oscillator |
| IQTX-H | High Stability TCXO | Tighter frequency stability |
| IQTX-L | Low Power TCXO | Reduced power consumption |
| IQVCXO | VCXO | Voltage Controlled Crystal Oscillator |
| IQVCXO-H | High Stability VCXO | Tighter frequency stability |
| IQOCXO | OCXO | Oven Controlled Crystal Oscillator |
| IQOCXO-H | High Stability OCXO | Ultra-stable (PPB range) |

### Module and Filter Prefixes

| Prefix | Component Type | Description |
|--------|----------------|-------------|
| IQCM | Clock Module | Integrated clock/timing module |
| IQRTC | RTC Module | Real-Time Clock module |
| IQXF | Crystal Filter | Crystal-based bandpass filter |
| IQSPF | SAW Filter | Surface Acoustic Wave filter |
| IQRB | Resonator Bandpass | Resonator-based bandpass filter |

---

## Supported Component Types

The IQDHandler supports these component types:

| ComponentType | Description |
|---------------|-------------|
| CRYSTAL | Base crystal type |
| CRYSTAL_IQD | IQD-specific crystal |
| OSCILLATOR | Base oscillator type |
| OSCILLATOR_IQD | IQD standard oscillator |
| OSCILLATOR_TCXO_IQD | IQD TCXO |
| OSCILLATOR_VCXO_IQD | IQD VCXO |
| OSCILLATOR_OCXO_IQD | IQD OCXO |
| CRYSTAL_FILTER_IQD | IQD crystal filter |
| RTC_MODULE_IQD | IQD RTC module |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// For crystals (CFPX, XTALS), size code is 3 digits after dash
// CFPX-032-16.000MHz → dashIndex=4, extract positions 5-7 → "032"
int dashIndex = upperMpn.indexOf('-');
if (dashIndex > 0 && dashIndex + 4 <= upperMpn.length()) {
    String sizeCode = upperMpn.substring(dashIndex + 1, dashIndex + 4);
    // Map to readable format
}

// For oscillators (IQXO, IQTX, etc.), size code is 2 digits
// Split by dash, take first 2 chars of second part
// IQXO-32-16.000MHz → parts[1]="32..." → pkgCode="32"
String[] parts = upperMpn.split("-");
if (parts.length >= 2) {
    String pkgCode = parts[1].substring(0, 2);
    // Map to readable format
}
```

### Series Extraction

```java
// Series extraction uses prefix matching with variant detection
// More specific variants (H, L) checked before base prefix

if (upperMpn.startsWith("IQXO")) {
    if (upperMpn.startsWith("IQXO-H")) return "High Frequency Oscillator";
    if (upperMpn.startsWith("IQXO-L")) return "Low Power Oscillator";
    return "Standard Oscillator";  // Base case last
}

if (upperMpn.startsWith("IQTX")) {
    if (upperMpn.startsWith("IQTX-H")) return "High Stability TCXO";
    if (upperMpn.startsWith("IQTX-L")) return "Low Power TCXO";
    return "Standard TCXO";
}
```

### Replacement Compatibility Logic

```java
// IQDHandler implements sophisticated replacement logic:
// 1. Same series required (or compatible upgrade)
// 2. Same package size required
// 3. Same frequency required
// 4. Better or equal stability allowed

// Compatible upgrades:
// - High Stability can replace Standard (e.g., IQTX-H → IQTX)
// - Low Power variants may be compatible with Standard

// Stability comparison:
// Lower PPM value = better stability
// A 0.5 PPM part can replace a 2.5 PPM part
```

---

## Stability Grades

Frequency stability is a key specification for timing products:

| Grade | Typical PPM | Application |
|-------|-------------|-------------|
| Standard | +/- 20-100 | General purpose |
| Medium | +/- 2.5-10 | Precision timing |
| High | +/- 0.5-2.5 | High accuracy |
| Ultra | +/- 0.1-0.5 | Precision instruments |
| OCXO | PPB range | Ultra-stable references |

---

## Common Frequency Values

### Standard Crystal Frequencies

| Frequency | Common Application |
|-----------|-------------------|
| 32.768 kHz | RTC, watch crystals |
| 4.000 MHz | General purpose |
| 8.000 MHz | Microcontrollers |
| 12.000 MHz | USB (12 Mbps) |
| 16.000 MHz | Microcontrollers |
| 20.000 MHz | General purpose |
| 25.000 MHz | Ethernet PHY |
| 48.000 MHz | USB (480 Mbps) |

### Standard Oscillator Frequencies

| Frequency | Common Application |
|-----------|-------------------|
| 1.000 MHz | Low frequency reference |
| 10.000 MHz | Reference standard |
| 12.288 MHz | Audio (48 kHz * 256) |
| 19.200 MHz | Telecom reference |
| 24.576 MHz | Audio (96 kHz * 256) |
| 100.000 MHz | High-speed systems |

---

## Related Files

- Handler: `manufacturers/IQDHandler.java`
- Component types: `CRYSTAL`, `CRYSTAL_IQD`, `OSCILLATOR`, `OSCILLATOR_IQD`, `OSCILLATOR_TCXO_IQD`, `OSCILLATOR_VCXO_IQD`, `OSCILLATOR_OCXO_IQD`, `CRYSTAL_FILTER_IQD`, `RTC_MODULE_IQD`

---

## Known Issues (Technical Debt)

The IQDHandler has these documented issues:

1. **HashSet in getSupportedTypes()** - Should use `Set.of()` for immutability
2. **Missing IC type** - Handler registers patterns for `ComponentType.IC` (clock modules, RTC, filters) but does not include `IC` in `getSupportedTypes()`
3. **No handler tests** - Listed in handlers without tests in CLAUDE.md

---

## Learnings & Quirks

- **Variant modifiers (H, L)**: Appear between prefix and size code (e.g., IQXO-H32 vs IQXO-32). The handler correctly checks for these before falling back to base series.
- **Package extraction differs by product type**: Crystals use 3-digit codes after dash, oscillators use 2-digit codes. The handler splits logic based on prefix.
- **Replacement compatibility**: IQD handler includes sophisticated replacement logic that considers stability grades - better stability parts can replace worse ones but not vice versa.
- **PPM vs PPB**: OCXOs use parts-per-billion (PPB) while other products use parts-per-million (PPM). Both are extracted as stability grades.
- **IQTX vs IQXO**: Easy to confuse - IQTX is TCXO (Temperature Compensated), IQXO is standard XO (crystal oscillator).
- **Missing IC in getSupportedTypes()**: Clock modules (IQCM), RTC modules (IQRTC), and filters (IQXF, IQSPF, IQRB) are registered under `ComponentType.IC` but IC is not in the supported types set.

<!-- Add new learnings above this line -->
