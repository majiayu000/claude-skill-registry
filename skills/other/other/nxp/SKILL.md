---
name: nxp
description: NXP Semiconductors MPN encoding patterns, suffix decoding, and handler guidance. Use when working with LPC, Kinetis, i.MX, S32K, MOSFETs, or transistors.
---

# NXP Semiconductors Manufacturer Skill

## MPN Structure Overview

NXP has diverse product lines with different naming conventions:

```
Microcontrollers:   [FAMILY][SERIES][VARIANT][PACKAGE][SUFFIX]
Processors:         MC[IMX][SERIES][VARIANT][PACKAGE][TEMP][REV]
MOSFETs:            [PREFIX][SPEC][PACKAGE]
Transistors:        [BASE][GAIN_GROUP][PACKAGE_SUFFIX]
```

---

## Product Families

### LPC Microcontrollers (ARM Cortex-M)

```
LPC[SERIES][VARIANT][PACKAGE][PIN_COUNT]
 |    |       |        |         |
 |    |       |        |         +-- Pin count (48, 64, 100, 144, 208)
 |    |       |        +-- FBD=LQFP, FET=TFBGA, FHN=QFN
 |    |       +-- Feature variant
 |    +-- Series (1768, 4357, 5500, etc.)
 +-- LPC family prefix
```

#### LPC Series Overview

| Series | Core | Features | Example |
|--------|------|----------|---------|
| **LPC800** | Cortex-M0+ | Low cost | LPC812M101FDH16 |
| **LPC1100** | Cortex-M0 | Entry level | LPC1115FBD48 |
| **LPC1300** | Cortex-M3 | USB | LPC1343FBD48 |
| **LPC1500** | Cortex-M3 | Analog | LPC1549JBD100 |
| **LPC1700** | Cortex-M3 | Feature rich | LPC1768FBD100 |
| **LPC1800** | Cortex-M3 | High performance | LPC1857FET256 |
| **LPC4300** | Cortex-M4/M0 | Dual core | LPC4357FET180 |
| **LPC5500** | Cortex-M33 | TrustZone | LPC55S69JBD100 |

#### LPC Package Codes

| Code | Package | Description |
|------|---------|-------------|
| **FBD** | LQFP | Low-profile Quad Flat Pack |
| **FET** | TFBGA | Thin Fine-pitch Ball Grid Array |
| **FHN** | QFN | Quad Flat No-leads (HVQFN) |
| **JBD** | LQFP | LQFP variant |
| **UK** | WLCSP | Wafer Level Chip Scale Package |

#### Example Decoding

```
LPC1768FBD100
|   |  |   |
|   |  |   +-- 100 pins
|   |  +-- FBD = LQFP package
|   +-- 1768 = Cortex-M3, 512KB Flash, 100MHz
+-- LPC family

LPC55S69JBD100
|   |  ||   |
|   |  ||   +-- 100 pins
|   |  |+-- JBD = LQFP package
|   |  +-- S = Security (TrustZone)
|   +-- 5569 = Cortex-M33, 640KB Flash
+-- LPC family
```

---

### Kinetis Microcontrollers (MK Series)

```
MK[FAMILY][SUBSERIES][FLASH][V][PACKAGE][SPEED]
 |   |        |        |   |     |        |
 |   |        |        |   |     |        +-- Speed grade (5=50MHz, 7=72MHz)
 |   |        |        |   |     +-- Package code
 |   |        |        |   +-- V prefix for package
 |   |        |        +-- Flash size code
 |   |        +-- Features (D=USB, E=Ethernet, W=Wireless)
 |   +-- Family (10, 20, 22, 60, 64, 66, etc.)
 +-- MK = Kinetis MCU
```

#### Kinetis K Series Families

| Family | Core | Frequency | Example |
|--------|------|-----------|---------|
| **MK10** | Cortex-M4 | 50-150 MHz | MK10DN128VLH5 |
| **MK20** | Cortex-M4 | 50-120 MHz | MK20DX256VLH7 |
| **MK22** | Cortex-M4F | 120 MHz | MK22FN512VLH12 |
| **MK60** | Cortex-M4 | 100 MHz | MK60DN512VLQ10 |
| **MK64** | Cortex-M4F | 120 MHz | MK64FN1M0VLL12 |
| **MK66** | Cortex-M4F | 180 MHz | MK66FN2M0VMD18 |

#### Kinetis L Series (Low Power)

| Family | Core | Features | Example |
|--------|------|----------|---------|
| **MKL02** | Cortex-M0+ | Ultra low power | MKL02Z32VFM4 |
| **MKL25** | Cortex-M0+ | USB | MKL25Z128VLK4 |
| **MKL26** | Cortex-M0+ | USB, LCD | MKL26Z256VLH4 |

#### Kinetis Package Codes (after V)

| Code | Package | Pins |
|------|---------|------|
| **VFM** | QFN | 32 |
| **VFT** | QFN | 48 |
| **VLH** | LQFP | 64 |
| **VLK** | LQFP | 80 |
| **VLL** | LQFP | 100 |
| **VLQ** | LQFP | 144 |
| **VMD** | BGA | 144 |

#### Speed Grade Suffix

| Suffix | Frequency |
|--------|-----------|
| 4 | 48 MHz |
| 5 | 50 MHz |
| 7 | 72 MHz |
| 10 | 100 MHz |
| 12 | 120 MHz |
| 18 | 180 MHz |

---

### i.MX Applications Processors

```
MCIMX[SERIES][VARIANT][PACKAGE][TEMP][REV]
  |     |       |        |      |     |
  |     |       |        |      |     +-- Silicon revision (A, B, C, D)
  |     |       |        |      +-- Temperature (C=Commercial, I=Industrial)
  |     |       |        +-- Package code
  |     |       +-- Feature/core variant
  |     +-- Series (6D=Dual, 6Q=Quad, 6S=Solo, 8)
  +-- MCIMX = i.MX processor prefix
```

#### i.MX 6 Series Variants

| Code | Cores | Description |
|------|-------|-------------|
| **6S** | 1x Cortex-A9 | Solo |
| **6D** | 2x Cortex-A9 | Dual |
| **6Q** | 4x Cortex-A9 | Quad |
| **6SX** | Cortex-A9 + M4 | Hybrid |
| **6UL** | 1x Cortex-A7 | Ultra Lite |

#### i.MX 8 Series

| Code | Cores | Description |
|------|-------|-------------|
| **8M** | Cortex-A53 + M4 | Mini |
| **8MM** | Cortex-A53 + M4 | Mini Mini |
| **8MN** | Cortex-A53 + M7 | Mini Nano |
| **8QM** | A72 + A53 + M4 | QuadMax |
| **8QX** | A35 + M4 | QuadXPlus |

#### Example Decoding

```
MCIMX6Q5EYM10AC
  |   |||| | | ||
  |   |||| | | |+-- Silicon rev C
  |   |||| | | +-- A = Automotive/Extended temp
  |   |||| | +-- 10 = 1.0 GHz
  |   |||| +-- M = BGA package
  |   |||+-- Y = specific variant
  |   ||+-- E = features (VPU, GPU)
  |   |+-- 5 = variant code
  |   +-- Q = Quad core
  +-- IMX6 = i.MX 6 series
```

---

### S32K Automotive MCUs

```
S32K[SERIES][VARIANT]
    |   |       |
    |   |       +-- Feature suffix (see below)
    |   +-- Model (116, 118, 142, 144, 146, 148, 3xx)
    +-- S32K = Automotive MCU family
```

#### S32K1 Series (Cortex-M0+/M4F)

| Part | Core | Flash | Pins |
|------|------|-------|------|
| **S32K116** | M0+ | 128KB | 48 LQFP |
| **S32K118** | M0+ | 256KB | 48 LQFP |
| **S32K142** | M4F | 256KB | 100 LQFP |
| **S32K144** | M4F | 512KB | 100 LQFP |
| **S32K146** | M4F | 1MB | 144 LQFP |
| **S32K148** | M4F | 2MB | 176 LQFP |

#### S32K3 Series (Cortex-M7)

| Part | Safety | Cores | Flash |
|------|--------|-------|-------|
| **S32K322** | ASIL B | Dual | 2MB |
| **S32K344** | ASIL D | Lockstep | 4MB |
| **S32K358** | ASIL D | Lockstep+1 | 8MB |

#### S32K1 Feature Suffixes

| Suffix | Features |
|--------|----------|
| **R** | RAM max |
| **F** | CAN FD & FlexIO |
| **S** | Security |
| **A** | CAN FD, FlexIO & Security |
| **E** | Ethernet & Audio |
| **J** | All features |

---

## MOSFETs

### PSMN Series (Power MOSFETs)

```
PSMN[VOLTAGE][RESISTANCE][PACKAGE]
    |     |         |         |
    |     |         |         +-- Package suffix
    |     |         +-- On-resistance (e.g., 9R2 = 9.2 mohm)
    |     +-- Voltage rating (e.g., 040 = 40V)
    +-- PSMN = Power MOSFET N-channel
```

### BUK Series (Automotive MOSFETs)

```
BUK[LEVEL][PACKAGE][TECH][VOLTAGE][RESISTANCE]
    |        |       |       |         |
    |        |       |       |         +-- Resistance code
    |        |       |       +-- Voltage rating
    |        |       +-- Technology generation
    |        +-- Package code
    +-- Level: 7=Standard, 9=Logic
```

#### BUK Package Codes

| Code | Package |
|------|---------|
| **Y** | LFPAK56 |
| **K** | LFPAK56D (Dual) |
| **M** | LFPAK33 |
| **2** | DPAK |
| **6** | D2PAK |
| **5** | TO-220 |
| **E** | I2PAK |

#### BUK Technology Codes

| Code | Generation |
|------|------------|
| **E** | Trench 6 |
| **C** | Trench 4 |
| **B** | Trench 3 |
| **A** | Trench 2 |

### PMV/BSS Series (Small Signal MOSFETs)

| Prefix | Type | Package |
|--------|------|---------|
| **PMV** | Small signal | SOT-23, SOT-323 |
| **BSS** | Small signal | SOT-23, SOT-323 |

---

## Transistors

### BC847/BC857 Series

```
BC847[GAIN][PACKAGE_SUFFIX]
  |    |        |
  |    |        +-- Package: (none)=SOT-23, W=SOT-323, MB=DFN
  |    +-- Gain group: A, B, C (hFE ranges)
  +-- BC847 = NPN (BC857 = PNP complement)
```

#### Transistor Gain Groups

| Suffix | hFE Range |
|--------|-----------|
| **A** | 110-220 |
| **B** | 200-450 |
| **C** | 420-800 |

#### Package Variants

| Suffix | Package | Size |
|--------|---------|------|
| (none) | SOT-23 | TO-236AB |
| **W** | SOT-323 | SC-70 |
| **MB** | DFN | SOT883B |

### PN Series (2N Equivalents)

| NXP Part | Equivalent | Type |
|----------|------------|------|
| **PN2222** | 2N2222 | NPN |
| **PN2907** | 2N2907 | PNP |
| **PN3904** | 2N3904 | NPN |
| **PN3906** | 2N3906 | PNP |
| **PN4401** | 2N4401 | NPN |
| **PN4403** | 2N4403 | PNP |

---

## Temperature Grades

| Grade | Range | Suffix |
|-------|-------|--------|
| Commercial | 0C to +70C | (none) or C |
| Industrial | -40C to +85C | I |
| Extended | -40C to +105C | E |
| Automotive | -40C to +125C | A |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// LPC: Extract from FBD, FET, FHN, JBD, UK patterns
if (upperMpn.startsWith("LPC")) {
    // LPC1768FBD100 -> FBD100
    // Find where letters after digits start
    int numEnd = findLastDigit(mpn, "LPC".length()) + 1;
    if (numEnd < mpn.length()) {
        return mpn.substring(numEnd);
    }
}

// Kinetis: Package is between V and speed digit
// MK64FN1M0VLL12 -> VLL (LQFP100)
if (upperMpn.startsWith("MK")) {
    int vPos = upperMpn.indexOf('V');
    if (vPos > 0) {
        // Extract 3-letter package code after V
        return upperMpn.substring(vPos, Math.min(vPos + 4, upperMpn.length()));
    }
}

// i.MX: Complex - after variant letters
// MCIMX6Q5EYM10AC -> M (BGA)
```

### Series Extraction

```java
// LPC: Family is LPC + series digits
// LPC1768FBD100 -> LPC1768
// LPC55S69JBD100 -> LPC55S69

// Kinetis: MK + family + subseries
// MK64FN1M0VLL12 -> MK64
// MKL25Z128VLK4 -> MKL25

// S32K: Full model number
// S32K144 -> S32K144
```

### Known Issues in Current Handler

1. **HashSet usage**: Line 80 uses `new HashSet<>()` - should use `Set.of()` for immutability
2. **Op-amp attribution error**: LM358, LM324, LM741 are Texas Instruments parts, NOT NXP
3. **QorIQ pattern too broad**: `^P[0-9]+.*` may match unrelated parts
4. **Missing patterns**: PMV and BSS MOSFETs in matches() but not initializePatterns()
5. **Package extraction incomplete**: Only handles LPC and MCIMX, missing Kinetis, S32K, MOSFETs

### Pattern Recommendations

```java
// LPC - more specific
"^LPC[0-9]{3,4}[A-Z]?[A-Z]{2,3}[0-9]{2,3}.*"

// Kinetis K series
"^MK[0-9]{2}[A-Z]{0,2}[0-9]+V[A-Z]{2,3}[0-9]+$"

// Kinetis L series
"^MKL[0-9]{2}[A-Z][0-9]+V[A-Z]{2,3}[0-9]+$"

// S32K with optional suffix
"^S32K[0-9]{3}[A-Z]?.*"

// i.MX - starts with MCIMX or MIMX
"^(?:MC)?IMX[0-9][A-Z0-9]+.*"
```

---

## Related Files

- Handler: `manufacturers/NXPHandler.java`
- Component types: `MICROCONTROLLER_NXP`, `MCU_NXP`, `KINETIS_MCU`, `LPC_MCU`, `IMX_PROCESSOR`, `MOSFET_NXP`, `TRANSISTOR_NXP`

---

## External References

- [NXP Product Numbering Information (BRORDERINFO.pdf)](https://www.nxp.com/docs/en/product-numbering-scheme/BRORDERINFO.pdf)
- [LPC Microcontrollers Selector Guide](https://www.nxp.com/docs/en/product-selector-guide/LPCMICROLNCD.pdf)
- [Kinetis K Series Selector Guide](https://www.nxp.com/docs/en/product-selector-guide/KINETISKMCUSELGD.pdf)
- [NXP Community - Part Number Naming](https://community.nxp.com/t5/8-bit-Microcontrollers/Part-Number-Naming-Conventions/td-p/1346059)

---

## Learnings & Edge Cases

- **Nexperia spin-off**: BC847/BC857 transistors and some MOSFETs are now Nexperia (spun off from NXP in 2017)
- **LPC55 security**: The "S" in LPC55S69 indicates TrustZone security support
- **i.MX ordering**: MCIMX prefix is for ordering, datasheets often use just IMX
- **Kinetis F vs no-F**: "F" in MK64F indicates floating-point unit (Cortex-M4F vs M4)
- **Package number is pin count**: In LPC, FBD100 means LQFP with 100 pins

<!-- Add new learnings above this line -->
