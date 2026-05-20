---
name: ess
description: ESS Technology MPN encoding patterns, high-end audio DAC decoding, and handler guidance. Use when working with ESS Sabre DACs or ESSHandler.
---

# ESS Technology Manufacturer Skill

## MPN Structure

ESS Technology specializes in high-performance audio DACs (Sabre series).

```
ES[SERIES][VARIANT]-[PACKAGE]-[PINCOUNT]
   |   |      |        |         |
   |   |      |        |         +-- Pin count (optional)
   |   |      |        +-- Package code (QFN, TQFP, etc.)
   |   |      +-- Variant (PRO, Q2M, K2M, P, S)
   |   +-- Series (9038, 9028, 9018, 92xx)
   +-- ES = ESS Technology prefix
```

### Example Decoding

```
ES9038PRO
|  |   |
|  |   +-- PRO = 8-channel flagship variant
|  +-- 9038 = Flagship Sabre series
+-- ES = ESS Technology

ES9218P-QFNR-48
|  |  | |    |
|  |  | |    +-- 48 = 48-pin
|  |  | +-- QFNR = QFN package, Tape and Reel
|  |  +-- P = Portable variant with headphone amp
|  +-- 9218 = Portable DAC series
+-- ES = ESS Technology
```

---

## Product Families

### ES9038 Series - Flagship Sabre DACs

The ultimate performance audio DACs.

| Part | Channels | Features |
|------|----------|----------|
| ES9038PRO | 8 | Flagship, -140dB THD+N |
| ES9038Q2M | 2 | Mobile/portable optimized |

### ES9028 Series - High-End Sabre DACs

| Part | Channels | Features |
|------|----------|----------|
| ES9028PRO | 8 | High performance |
| ES9028Q2M | 2 | Mobile version |

### ES9018 Series - Classic Sabre DACs

| Part | Channels | Features |
|------|----------|----------|
| ES9018S | 8 | Reference stereo |
| ES9018K2M | 2 | Mobile 2-channel |

### ES901x/902x Series - Mid-Range DACs

| Part | Description |
|------|-------------|
| ES9010 | Entry-level DAC |
| ES9016 | Mid-range DAC |
| ES9023 | Popular 24-bit DAC |

### ES92xx Series - Portable DACs with Headphone Amps

Integrated DAC + headphone amplifier for mobile devices.

| Part | Features |
|------|----------|
| ES9218P | Portable HiFi, headphone amp |
| ES9219 | Latest portable DAC/amp |
| ES9219C | ES9219 variant |
| ES9281 | USB DAC |

---

## Variant Suffixes

| Suffix | Meaning |
|--------|---------|
| PRO | Professional 8-channel flagship |
| Q2M | 2-channel mobile/battery optimized |
| K2M | 2-channel compact variant |
| S | Stereo version |
| P | Portable with headphone amp |
| C | Grade/revision variant |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFN | QFN | Most common for audio DACs |
| QFNR | QFN, Tape & Reel | QFN with packaging |
| TQFP | TQFP | Larger pin count parts |
| WLCSP | WLCSP | Compact mobile parts |
| LQFP | LQFP | Low-profile quad flat |

---

## Handler Implementation Notes

### Series Extraction

```java
// Extract ES + 4 digits for the series
// ES9038PRO -> ES9038
// ES9218P -> ES9218

if (upperMpn.length() >= 6) {
    String digits = upperMpn.substring(2, 6);
    if (digits.chars().allMatch(Character::isDigit)) {
        return "ES" + digits;
    }
}
```

### Package Code Extraction

```java
// Check for hyphenated suffix with package info
// ES9218P-QFNR-48 -> QFN

// Check for embedded package code without hyphen
// ESxxxxQFN -> QFN
```

### Base Part Number Extraction

```java
// Remove package suffixes to get base part
// ES9038PRO-QFN -> ES9038PRO
// ES9218P-QFNR-48 -> ES9218P

// Remove trailing package codes
result = upper
    .replaceAll("QFN.*$", "")
    .replaceAll("TQFP.*$", "")
    .replaceAll("WLCSP.*$", "")
    .replaceAll("LQFP.*$", "");
```

---

## Replacement Rules

### Same Part, Different Package

Parts with the same base number but different packages are replacements:
- ES9038PRO-QFN = ES9038PRO-TQFP (same part, different package)
- ES9218P = ES9218P-QFNR-48 (same part with package suffix)

### NOT Replacements (Different Channel Count)

Parts in the same series with different channel counts are NOT direct replacements:
- ES9038PRO (8-channel) != ES9038Q2M (2-channel)
- ES9028PRO (8-channel) != ES9028Q2M (2-channel)

---

## Related Files

- Handler: `manufacturers/ESSHandler.java`
- Component types: `ComponentType.IC`

---

## Common MPNs

| MPN | Description | Application |
|-----|-------------|-------------|
| ES9038PRO | 8-ch flagship DAC | High-end audio |
| ES9038Q2M | 2-ch mobile DAC | Portable HiFi |
| ES9028PRO | 8-ch high-end | Audio equipment |
| ES9018K2M | 2-ch classic | DAPs, headphone amps |
| ES9218P | Portable DAC/amp | Smartphones |
| ES9219 | Latest portable | USB-C audio |
| ES9023 | Entry 24-bit | DIY audio |

---

## Audio Specifications

### ES9038PRO Performance

| Spec | Value |
|------|-------|
| THD+N | -140 dB |
| DNR | 140 dB |
| Channels | 8 |
| Resolution | 32-bit |
| Sample Rate | Up to 768 kHz |

### ES9218P Performance

| Spec | Value |
|------|-------|
| THD+N | -118 dB |
| SNR | 129 dB |
| Output | 2 Vrms |
| Features | HiFi DAC + headphone amp |

---

## Applications

- High-end audio equipment
- Digital Audio Players (DAPs)
- Headphone amplifiers
- USB DACs
- Smartphone HiFi
- Professional audio systems
- Home theater preamps
- Audiophile equipment

---

## Learnings & Edge Cases

- **PRO vs Q2M naming**: PRO = 8-channel professional, Q2M = 2-channel mobile - NOT interchangeable.
- **Channel count determines compatibility**: 8-channel and 2-channel parts are functionally different.
- **ES92xx includes headphone amp**: These are integrated DAC + amp solutions, not standalone DACs.
- **Package rarely changes function**: Same base part in different packages are true replacements.
- **ESS Sabre branding**: All modern ESS DACs use "Sabre" technology branding.
- **K2M vs Q2M**: Both are 2-channel, but K2M is earlier generation, Q2M is optimized for mobile.
- **High-end audio market**: ESS dominates portable HiFi - found in most premium DAPs and USB DACs.

<!-- Add new learnings above this line -->
