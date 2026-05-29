---
name: kds
description: KDS (Daishinku Corporation) MPN encoding patterns, crystal and oscillator decoding, and handler guidance. Use when working with KDS timing devices (DSX, DST, DSO, DSB series).
---

# KDS (Daishinku Corporation) Manufacturer Skill

## Overview

KDS (Daishinku Corporation) is a major Japanese manufacturer of frequency control products:
- **DSX series**: SMD crystals
- **DST series**: Tuning fork crystals (32.768kHz typical)
- **DSO series**: Clock oscillators
- **DSB series**: SAW filters and resonators
- **1N series**: Through-hole crystal units
- **DX/SM series**: Standard and surface mount crystals

---

## MPN Structure

### DSX Series (SMD Crystals)

```
DSX[SIZE][PACKAGE][OPTIONS]-[FREQUENCY]
|    |      |        |          |
|    |      |        |          +-- Optional frequency suffix
|    |      |        +-- GA = AEC-Q200, G = standard ceramic
|    |      +-- Package suffix
|    +-- 3-digit size code (321 = 3.2x1.3mm)
+-- DSX = SMD crystal series

Example: DSX321G-12.000M
         |  | ||    |
         |  | ||    +-- 12 MHz frequency
         |  | |+-- (SMD ceramic)
         |  | +-- G = SMD ceramic package
         |  +-- 321 = 3.2x1.3mm
         +-- DSX = SMD crystal

Example: DSX530GA
         |  |  ||
         |  |  |+-- A = AEC-Q200 automotive grade
         |  |  +-- G = SMD ceramic
         |  +-- 530 = 5.0x3.2mm
         +-- DSX = SMD crystal
```

### DST Series (Tuning Fork Crystals)

```
DST[SIZE][PACKAGE]
|    |      |
|    |      +-- S = SMD, other variants
|    +-- 3-digit size code (310 = 3.1x1.5mm)
+-- DST = Tuning fork crystal series

Example: DST310S
         |  | |
         |  | +-- S = SMD package
         |  +-- 310 = 3.1x1.5mm
         +-- DST = Tuning fork (32.768kHz typical)
```

### DSO Series (Clock Oscillators)

```
DSO[SIZE][PACKAGE][OPTIONS]
|    |      |        |
|    |      |        +-- SDH = high stability, R = tape reel
|    |      +-- S = SMD
|    +-- 3-digit size code
+-- DSO = Clock oscillator series

Example: DSO321SR
         |  | ||
         |  | |+-- R = Tape and reel
         |  | +-- S = SMD package
         |  +-- 321 = 3.2x2.5mm
         +-- DSO = Clock oscillator
```

### DSB Series (SAW Filters/Resonators)

```
DSB[SIZE][PACKAGE][OPTIONS]
|    |      |        |
|    |      |        +-- SDA = automotive, other options
|    |      +-- S = SMD
|    +-- 3-digit size code
+-- DSB = SAW filter/resonator

Example: DSB321SDA
         |  |  ||
         |  |  |+-- A = AEC-Q200 automotive
         |  |  +-- SD = SMD automotive
         |  +-- 321 = 3.2x1.3mm
         +-- DSB = SAW device
```

### 1N Series (Through-Hole Crystals)

```
1N-[FREQUENCY]
|      |
|      +-- Frequency in MHz (26.000 = 26 MHz)
+-- 1N = Through-hole crystal unit

Example: 1N-26.000
         |    |
         |    +-- 26.000 MHz
         +-- 1N series, HC-49U package
```

---

## Size Codes

### DSX Series (SMD Crystals)

| Size Code | Dimensions | Common Frequencies |
|-----------|------------|-------------------|
| 211 | 2.0x1.2mm | 16-50 MHz |
| 221 | 2.0x1.2mm | 16-50 MHz |
| 321 | 3.2x1.3mm | 8-50 MHz |
| 320 | 3.2x2.0mm | 8-40 MHz |
| 530 | 5.0x3.2mm | 4-50 MHz |
| 531 | 5.0x3.2mm | 4-50 MHz |
| 750 | 7.0x5.0mm | 1-40 MHz |
| 840 | 8.0x4.5mm | 1-25 MHz |
| 860 | 8.6x3.7mm | 1-25 MHz |

### DST Series (Tuning Fork)

| Size Code | Dimensions | Typical Frequency |
|-----------|------------|-------------------|
| 210 | 2.0x1.2mm | 32.768 kHz |
| 310 | 3.1x1.5mm | 32.768 kHz |
| 410 | 4.1x1.5mm | 32.768 kHz |
| 520 | 5.0x2.0mm | 32.768 kHz |

### DSO Series (Oscillators)

| Size Code | Dimensions | Output Type |
|-----------|------------|-------------|
| 211 | 2.0x1.6mm | CMOS |
| 221 | 2.0x1.6mm | CMOS |
| 321 | 3.2x2.5mm | CMOS |
| 531 | 5.0x3.2mm | CMOS |
| 750 | 7.0x5.0mm | CMOS/LVDS |

---

## Package Suffix Codes

| Suffix | Meaning | Notes |
|--------|---------|-------|
| G | SMD ceramic | Standard ceramic package |
| GA | SMD ceramic AEC-Q200 | Automotive qualified |
| S | SMD | General SMD |
| SR | SMD tape reel | Tape and reel packaging |
| R | Tape reel | Tape and reel (any package) |
| SDH | SMD high stability | Enhanced frequency stability |
| SDA | SMD automotive | AEC-Q200 qualified |

---

## Replacement Compatibility

KDS parts are compatible when:
1. **Same base series** (DSX vs DSX, DST vs DST)
2. **Same package dimensions** (321 matches 321)
3. **Same or higher grade** (AEC-Q200 can replace standard)

### Upgrade Paths

| Original | Replacement | Notes |
|----------|-------------|-------|
| DSX321G | DSX321GA | AEC-Q200 upgrade |
| DSO321S | DSO321SDH | High stability upgrade |
| DSX530G | DSX530GA | Automotive upgrade |

---

## Common Part Numbers

### DSX SMD Crystals

| Part Number | Size | Frequency | Grade |
|-------------|------|-----------|-------|
| DSX321G | 3.2x1.3mm | Various | Standard |
| DSX321GA | 3.2x1.3mm | Various | AEC-Q200 |
| DSX530G | 5.0x3.2mm | Various | Standard |
| DSX530GA | 5.0x3.2mm | Various | AEC-Q200 |
| DSX840GA | 8.0x4.5mm | Low freq | AEC-Q200 |

### DST Tuning Fork Crystals

| Part Number | Size | Frequency | Notes |
|-------------|------|-----------|-------|
| DST310S | 3.1x1.5mm | 32.768 kHz | Standard |
| DST410S | 4.1x1.5mm | 32.768 kHz | Standard |
| DST520S | 5.0x2.0mm | 32.768 kHz | Large |

### DSO Clock Oscillators

| Part Number | Size | Output | Notes |
|-------------|------|--------|-------|
| DSO321SR | 3.2x2.5mm | CMOS | Tape/reel |
| DSO531SDH | 5.0x3.2mm | CMOS | High stability |
| DSO750S | 7.0x5.0mm | CMOS | Large |

### 1N Through-Hole Crystals

| Part Number | Frequency | Package |
|-------------|-----------|---------|
| 1N-8.000 | 8 MHz | HC-49U |
| 1N-12.000 | 12 MHz | HC-49U |
| 1N-16.000 | 16 MHz | HC-49U |
| 1N-26.000 | 26 MHz | HC-49U |

---

## Handler Implementation Notes

### Pattern Matching

```java
// DSX series - SMD crystals
"^DSX[0-9].*"
"^DSX[0-9]{3}G.*"  // With package suffix

// DST series - Tuning fork
"^DST[0-9].*"

// DSO series - Oscillators
"^DSO[0-9].*"
"^DSO[0-9]{3}S.*"  // SMD variant

// DSB series - SAW devices
"^DSB[0-9].*"

// 1N series - Through-hole
"^1N-[0-9].*"
"^1N[0-9].*"
```

### Package Code Extraction

```java
String extractPackageCode(String mpn) {
    String upperMpn = mpn.toUpperCase();

    // DSX series: DSX321G -> 3.2x1.3mm
    if (upperMpn.startsWith("DSX")) {
        String sizeCode = upperMpn.substring(3, 6);  // e.g., "321"
        String packageSuffix = "";
        int idx = 6;
        while (idx < upperMpn.length() && Character.isLetter(upperMpn.charAt(idx))) {
            idx++;
        }
        packageSuffix = upperMpn.substring(6, idx);  // e.g., "G", "GA"
        return mapSizeCodeToPackage(sizeCode, packageSuffix);
    }

    // 1N series: always HC-49U
    if (upperMpn.startsWith("1N")) {
        return "HC-49U";
    }

    return "";
}
```

### Frequency Extraction

```java
String extractFrequencyCode(String mpn) {
    String upperMpn = mpn.toUpperCase();

    // 1N series: 1N-26.000 -> 26.000
    if (upperMpn.startsWith("1N-")) {
        return upperMpn.substring(3);  // Everything after "1N-"
    }

    // DSX/DST/DSO: look for frequency suffix after last dash
    int lastDash = upperMpn.lastIndexOf('-');
    if (lastDash >= 0 && lastDash < upperMpn.length() - 1) {
        String freqPart = upperMpn.substring(lastDash + 1);
        if (freqPart.matches(".*\\d.*")) {
            return freqPart;
        }
    }

    return "";
}
```

---

## Related Files

- Handler: `manufacturers/KDSHandler.java`
- Component types: `CRYSTAL`, `OSCILLATOR`, `IC` (for SAW filters)
- No manufacturer-specific types defined

---

## Learnings & Edge Cases

- **DST always 32.768kHz**: The DST (tuning fork) series is almost exclusively for 32.768 kHz RTC crystals
- **1N frequency in MPN**: The 1N series explicitly includes frequency in the part number (1N-26.000)
- **GA vs G**: GA suffix indicates AEC-Q200 automotive qualification, can replace G but not vice versa
- **SDH high stability**: DSO oscillators with SDH suffix have enhanced frequency stability, suitable for precision applications
- **SAW devices (DSB)**: Registered under IC type as they perform signal filtering, not simple oscillation
- **Size code interpretation**: First 2 digits = length in 0.1mm, third digit = width in 0.1mm (e.g., 321 = 3.2x1.3mm, but varies by series)

<!-- Add new learnings above this line -->
