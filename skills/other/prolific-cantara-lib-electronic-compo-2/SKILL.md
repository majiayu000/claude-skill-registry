---
name: prolific
description: Prolific Technology MPN encoding patterns, variant identification, and handler guidance. Use when working with USB interface ICs or ProlificHandler.
---

# Prolific Technology Manufacturer Skill

## MPN Structure

Prolific MPNs follow this general structure:

```
PL[SERIES][VARIANT][PACKAGE][-REEL]
 |   |       |        |       |
 |   |       |        |       └── Optional: REEL, TUBE, TRAY, TR for packaging
 |   |       |        └── Package code (implicitly determined by variant for PL2303)
 |   |       └── Variant letters (HX, HXA, HXD, TA, GT, GC, GL, RA, SA, etc.)
 |   └── 4-digit series number (23xx, 25xx, 27xx, 38xx)
 └── PL = Prolific prefix
```

### Example Decoding

```
PL2303HXA-SSOP
│  │   │  │
│  │   │  └── SSOP package
│  │   └── HXA = Enhanced HX variant
│  └── 2303 = USB to serial converter
└── PL = Prolific prefix

PL2303GT
│  │   │
│  │   └── GT = QFN package variant
│  └── 2303 = USB to serial converter
└── PL = Prolific prefix
```

---

## Product Series

### PL23xx Series - USB to Serial

| Series | Type | Description |
|--------|------|-------------|
| PL2303 | USB-Serial | USB to RS-232 serial converter (most common) |
| PL2312 | USB-Serial | Enhanced USB to serial |

### PL25xx Series - USB Bridge

| Series | Type | Description |
|--------|------|-------------|
| PL2501 | Bridge | USB 2.0 to ATA/ATAPI bridge |
| PL2571 | Bridge | USB 2.0 to IDE bridge |

### PL27xx Series - USB Hub

| Series | Type | Description |
|--------|------|-------------|
| PL2734 | Hub | USB 2.0 4-port hub controller |
| PL2773 | Hub | USB 3.0 4-port hub controller |

### PL38xx Series - USB to Parallel

| Series | Type | Description |
|--------|------|-------------|
| PL3805 | USB-Parallel | USB to parallel port converter |

---

## PL2303 Variants

The PL2303 series has many variants with different features:

| Variant | Package | Features |
|---------|---------|----------|
| (none) | SOP | Standard, basic version |
| HX | SSOP | Enhanced, higher speed |
| HXA | SSOP | HX with improved GPIO |
| HXD | SSOP | Latest HX generation |
| TA | SSOP-28 | Extended features |
| GT | QFN | Small form factor, GPIO |
| GC | QFN | Compact version |
| GL | QFN | Low power variant |
| RA | SOP | RoHS compliant |
| SA | SOP | Standard alternate |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| S | SOP | Small Outline Package |
| SOP | SOP | Explicit form |
| SS | SSOP | Shrink SOP |
| SSOP | SSOP | Explicit form |
| Q | QFN | Quad Flat No-Lead |
| QFN | QFN | Explicit form |
| TSS | TSSOP | Thin Shrink SOP |
| TSSOP | TSSOP | Explicit form |

---

## USB Version by Series

| Series | USB Version |
|--------|-------------|
| PL2303 | USB 2.0 (Full Speed) |
| PL2312 | USB 2.0 |
| PL2501 | USB 2.0 |
| PL2571 | USB 2.0 |
| PL2734 | USB 2.0 |
| PL2773 | USB 3.0 |
| PL38xx | USB 2.0 |

---

## Handler Implementation Notes

### Pattern Matching

```java
// PL23xx series - USB to serial converters
"^PL23[0-9]{2}[A-Z]*.*"

// PL25xx series - USB bridge ICs
"^PL25[0-9]{2}[A-Z]*.*"

// PL27xx series - USB hub controllers
"^PL27[0-9]{2}[A-Z]*.*"

// PL38xx series - USB to parallel converters
"^PL38[0-9]{2}[A-Z]*.*"
```

### Series Extraction

```java
// Series is "PL" + 4 digits
// PL2303HXA -> PL2303
// PL2773 -> PL2773

if (upperMpn.matches("^PL2303.*")) {
    return "PL2303";
}
// Generic: return first 6 characters
```

### Package Code Extraction

```java
// For PL2303 variants, package is implied by variant:
// HX, HXA, HXD, TA -> SSOP
// GT, GC, GL -> QFN
// RA, SA, S -> SOP

// Explicit package after hyphen:
// PL2303HXA-SSOP -> SSOP
```

### Variant Extraction (PL2303)

```java
// Check variants from longest to shortest:
if (suffix.startsWith("HXD")) return "HXD";
if (suffix.startsWith("HXA")) return "HXA";
if (suffix.startsWith("HX")) return "HX";
if (suffix.startsWith("GT")) return "GT";
if (suffix.startsWith("GL")) return "GL";
if (suffix.startsWith("GC")) return "GC";
if (suffix.startsWith("TA")) return "TA";
if (suffix.startsWith("RA")) return "RA";
if (suffix.startsWith("SA")) return "SA";
```

---

## Replacement Compatibility

### PL2303 Family Compatibility

All PL2303 variants are generally compatible:
- Same USB-to-serial functionality
- Different variants offer additional features (GPIO, speed)
- Software drivers are largely interchangeable

### Hub Controllers

Hub controllers are NOT interchangeable across USB versions:
- PL2734 (USB 2.0) is NOT compatible with PL2773 (USB 3.0)
- Within same USB version, hubs are compatible

---

## Driver Notes

- **PL2303 driver compatibility**: Different OS versions may require different drivers
- **Counterfeit chip detection**: Prolific drivers detect counterfeit chips and refuse to work
- **HXA/HXD variants**: Require newer drivers than original PL2303

---

## Related Files

- Handler: `manufacturers/ProlificHandler.java`
- Component types: `ComponentType.IC`

---

## Learnings & Edge Cases

- **PL2303 is the dominant product**: Most Prolific parts are PL2303 variants
- **Variant determines package**: Unlike other manufacturers, the variant suffix often implies the package type
- **Driver compatibility issues**: PL2303 has complex driver compatibility across variants and OS versions
- **Counterfeit detection**: Prolific implemented counterfeit detection in drivers, causing issues with some legacy parts
- **USB version in series number**: PL27xx uses last digit to hint at USB version (PL2773 = USB 3.0)
- **No manufacturer-specific ComponentTypes**: All parts use generic `ComponentType.IC`

<!-- Add new learnings above this line -->
