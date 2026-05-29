---
name: nuvoton
description: Nuvoton Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Nuvoton MCUs, audio codecs, TPM chips, or NuvotonHandler.
---

# Nuvoton Technology Manufacturer Skill

## MPN Structure

Nuvoton has multiple product families with different MPN structures:

### ARM Cortex-M MCUs (NUC, M-series)

```
NUC[SERIES][LINE][PIN][FLASH][PKG][TEMP][VER]
│     │      │    │     │      │    │     │
│     │      │    │     │      │    │     └── Version (0, 1, etc.)
│     │      │    │     │      │    └── Temperature (N=normal, A=automotive)
│     │      │    │     │      └── Package type (A=QFN, etc.)
│     │      │    │     └── Flash size code
│     │      │    └── Pin code (LD=48, SD=64, VD=100, ZD=144)
│     │      └── Line number (23, 40, etc.)
│     └── Series (1=Cortex-M0, 2=Cortex-M0)
└── NuMicro prefix

M[LINE][PIN][FLASH][PKG]
│  │    │     │      │
│  │    │     │      └── Package code (AE=LQFP-48)
│  │    │     └── Flash size code
│  │    └── Pin code (LD=48, SD=64, LG=100, KI=128)
│  └── Line number (031=entry, 451=motor, 480=high-perf)
└── M-series prefix
```

### Example Decoding

```
NUC123LD4AN0
│  │  │ │││││
│  │  │ ││││└── Version 0
│  │  │ │││└── Temperature N (normal)
│  │  │ ││└── Package A (QFN)
│  │  │ │└── Flash 4 (64KB)
│  │  │ └── Pin LD (LQFP-48)
│  │  └── Line 23
│  └── Series 1 (Cortex-M0)
└── NUC prefix

M451LG6AE
│  │ │ ││
│  │ │ │└── Package E (LQFP variant)
│  │ │ └── Package A (LQFP)
│  │ └── Flash 6 (512KB)
│  └── Pin LG (LQFP-100)
└── M451 series (Cortex-M4 motor control)
```

---

## Package Codes

### NUC Series Pin Codes

| Code | Package | Pin Count |
|------|---------|-----------|
| LD | LQFP-48 | 48 |
| LE | LQFP-48 | 48 |
| SD | LQFP-64 | 64 |
| SE | LQFP-64 | 64 |
| VD | LQFP-100 | 100 |
| VE | LQFP-100 | 100 |
| ZD | LQFP-144 | 144 |
| AN | QFN-33 | 33 |

### M-Series Pin Codes

| Code | Package | Pin Count |
|------|---------|-----------|
| LD | LQFP-48 | 48 |
| LC | LQFP-48 | 48 |
| SD | LQFP-64 | 64 |
| SC | LQFP-64 | 64 |
| LG | LQFP-100 | 100 |
| VG | LQFP-100 | 100 |
| KI | LQFP-128 | 128 |
| ZG | LQFP-144 | 144 |
| ZI | LQFP-144 | 144 |

### 8051 MCU Package Codes

| Code | Package |
|------|---------|
| AT | TSSOP-20 |
| AS | SOP-20 |
| AQ | QFN-20 |
| FB | TSSOP-20 |
| DA | TSSOP-16 |
| BA | TSSOP-8 |
| AE | LQFP-48 |

### Audio Codec Package Codes

| Code | Package |
|------|---------|
| YG | QFN-32 |
| YGB | QFN-32 |
| LG | WLCSP |
| G | QFN-48 |

---

## Product Families

### ARM Cortex-M MCUs

| Series | Core | Features | Max Clock |
|--------|------|----------|-----------|
| NUC1xx | Cortex-M0 | General purpose | 50MHz |
| NUC2xx | Cortex-M0 | Enhanced peripherals | 72MHz |
| M031 | Cortex-M0 | Entry-level | 48MHz |
| M451 | Cortex-M4 | Motor control | 72MHz |
| M480 | Cortex-M4 | High performance | 192MHz |

### 8051-Based MCUs

| Series | Core | Features |
|--------|------|----------|
| N76E003 | 8051 | Low-cost, small footprint |
| MS51 | Enhanced 8051 | More peripherals |

### Audio Codecs

| Series | Type | Features |
|--------|------|----------|
| NAU8810 | Mono Codec | Single input/output |
| NAU8822 | Stereo Codec | Dual input/output |
| NAU88L25 | Low Power Codec | Battery applications |

### Security ICs

| Series | Type | Features |
|--------|------|----------|
| NPCT6xx | TPM 2.0 | Trusted Platform Module |

---

## Flash Size Encoding

### NUC Series

| Code | Flash Size |
|------|------------|
| 2 | 16KB |
| 3 | 32KB |
| 4 | 64KB |
| 5 | 128KB |
| 6 | 256KB |

### M-Series (Numeric)

| Code | Flash Size |
|------|------------|
| 2 | 32KB |
| 3 | 64KB |
| 4 | 128KB |
| 5 | 256KB |
| 6 | 512KB |

### M480 Series (Letter)

| Code | Flash Size |
|------|------------|
| A | 128KB |
| B | 256KB |
| C | 384KB |
| D | 512KB |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// NUC series: Pin code is after line number
// NUC123LD4AN0 -> LD determines package

// M-series: Pin code is after series number
// M451LG6AE -> LG determines package

// N76E series: Package code is 2-letter prefix of pin count
// N76E003AT20 -> AT = TSSOP, 20 = pins
```

### Series Extraction

```java
// NUC1xx and NUC2xx return generic series
if (upperMpn.matches("^NUC1\\d{2}.*")) return "NUC1xx";
if (upperMpn.matches("^NUC2\\d{2}.*")) return "NUC2xx";

// M-series returns exact line number
if (upperMpn.startsWith("M031")) return "M031";
if (upperMpn.startsWith("M451")) return "M451";
if (upperMpn.startsWith("M480")) return "M480";

// NAU88L must be checked before NAU88
if (upperMpn.matches("^NAU88L\\d{2}.*")) return "NAU88L";
```

### Official Replacement Logic

```java
// MCUs: Same series AND same pin count are replacements
// Audio Codecs: Same series are replacements (package variants OK)
```

---

## Related Files

- Handler: `manufacturers/NuvotonHandler.java`
- Component types: `MICROCONTROLLER`, `IC`

---

## Learnings & Edge Cases

- **NUC vs M naming**: NUC series uses full format (NUC123LD4AN0), M-series is shorter (M451LG6AE)
- **N76E003 popularity**: Most popular Nuvoton 8051 MCU due to low cost and Arduino compatibility
- **NAU88L prefix**: NAU88L25 must match before generic NAU88xx pattern
- **M480 flash encoding**: Uses letters (A-D) instead of numbers for flash size
- **Pin code position varies**: NUC at position 6, M-series at position 4, N76E at end of MPN
- **TPM chips**: NPCT6xx series are security ICs, not MCUs

<!-- Add new learnings above this line -->
