---
name: asmedia
description: ASMedia Technology MPN encoding patterns, series identification, and handler guidance. Use when working with USB/Storage controller ICs or ASMediaHandler.
---

# ASMedia Technology Manufacturer Skill

## MPN Structure

ASMedia MPNs follow this general structure:

```
ASM[SERIES][VARIANT][PACKAGE][-REEL]
  |    |       |        |       |
  |    |       |        |       └── Optional: REEL, TRAY, TR for packaging
  |    |       |        └── Package code (QFN, BGA, LQFP, or single letter)
  |    |       └── Revision letter (A, B, etc.)
  |    └── 4-digit series number (1xxx, 2xxx, 3xxx)
  └── ASMedia prefix
```

### Example Decoding

```
ASM1042A-QFN
│  │   │  │
│  │   │  └── QFN package
│  │   └── A revision
│  └── 1042 = PCIe to USB 3.0 host controller
└── ASM = ASMedia prefix

ASM2364-BGA
│  │   │
│  │   └── BGA package
│  └── 2364 = USB 3.2 Gen2x2 to NVMe bridge
└── ASM = ASMedia prefix
```

---

## Product Series

### ASM1xxx Series - USB 3.x Controllers

| Series | Type | Description |
|--------|------|-------------|
| ASM1042 | PCIe Host | USB 3.0 Host Controller |
| ASM1074 | Hub | USB 3.0 Hub Controller |
| ASM1142 | PCIe Host | USB 3.1 Gen2 Host Controller |
| ASM1143 | PCIe Host | USB 3.1 Gen2 Host Controller (variant) |
| ASM1153 | Bridge | USB 3.0 to SATA Bridge (single port) |
| ASM1156 | Bridge | USB 3.0 to SATA Bridge |

### ASM2xxx Series - Storage Controllers

| Series | Type | Description |
|--------|------|-------------|
| ASM2362 | Bridge | PCIe to NVMe/SATA Bridge |
| ASM2364 | Bridge | USB 3.2 Gen2x2 to NVMe Bridge |

### ASM3xxx Series - USB4/Thunderbolt

| Series | Type | Description |
|--------|------|-------------|
| ASM3242 | Controller | USB4 Controller |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFN | QFN | Quad Flat No-Lead |
| Q | QFN | Short form |
| BGA | BGA | Ball Grid Array |
| B | BGA | Short form |
| LQFP | LQFP | Low-profile Quad Flat Package |
| L | LQFP | Short form |

---

## USB Version by Series

| Series | USB Version |
|--------|-------------|
| ASM1042 | USB 3.0 |
| ASM1074 | USB 3.0 |
| ASM1153 | USB 3.0 |
| ASM1156 | USB 3.0 |
| ASM1142 | USB 3.1 Gen2 |
| ASM1143 | USB 3.1 Gen2 |
| ASM10xx | USB 3.0 (general) |
| ASM11xx | USB 3.1 (general) |
| ASM2362 | N/A (PCIe) |
| ASM2364 | USB 3.2 Gen2x2 |
| ASM3242 | USB4 |

---

## Interface Types

| Series | Host Interface | Device Interface |
|--------|----------------|------------------|
| ASM1042 | PCIe | USB |
| ASM1074 | USB | USB Hub |
| ASM1142 | PCIe | USB |
| ASM1153 | USB | SATA |
| ASM1156 | USB | SATA |
| ASM2362 | PCIe | NVMe/SATA |
| ASM2364 | USB | NVMe |
| ASM3242 | USB4 | Thunderbolt |

---

## Handler Implementation Notes

### Pattern Matching

```java
// ASM1xxx series - USB 3.x controllers and bridges
"^ASM1[0-9]{3}[A-Z]*.*"

// ASM2xxx series - SATA controllers
"^ASM2[0-9]{3}[A-Z]*.*"

// ASM3xxx series - USB4/Thunderbolt controllers
"^ASM3[0-9]{3}[A-Z]*.*"

// Generic pattern for all ASM parts
"^ASM[0-9]{4}[A-Z]*.*"
```

### Series Extraction

```java
// Series is always "ASM" + 4 digits
// ASM1042A-QFN -> ASM1042
// ASM2364 -> ASM2364

if (mpn.length() >= 7) {
    return mpn.substring(0, 7);  // Returns "ASM1042"
}
```

### Package Code Extraction

```java
// Check for explicit package suffix after hyphen
// ASM1042-QFN -> QFN
int hyphen = cleanMpn.indexOf('-');
if (hyphen > 0) {
    String suffix = cleanMpn.substring(hyphen + 1);
    // Map to package name
}

// Or extract trailing letter after digits
// ASM1042Q -> QFN (Q maps to QFN)
```

---

## Replacement Compatibility

### USB Generation Upgrades

USB 3.1 Gen2 controllers can replace USB 3.0 (backward compatible):
- ASM1142 can replace ASM1042

### Bridge Family Compatibility

Same-generation bridges are compatible:
- ASM1153 and ASM1156 are interchangeable (USB 3.0 to SATA family)

---

## Related Files

- Handler: `manufacturers/ASMediaHandler.java`
- Component types: `ComponentType.IC`

---

## Learnings & Edge Cases

- **All ASMedia parts use single IC type**: Unlike other manufacturers, ASMedia only produces controller ICs, no discrete components
- **Series numbering scheme**: 1xxx = USB, 2xxx = Storage/NVMe, 3xxx = USB4/Thunderbolt
- **USB generation embedded in series**: ASM10xx = USB 3.0, ASM11xx = USB 3.1
- **Package codes can appear after hyphen or as trailing letter**: Both ASM1042-QFN and ASM1042Q are valid
- **REEL/TRAY/TR suffixes**: Indicate packaging type, should be stripped before package extraction

<!-- Add new learnings above this line -->
