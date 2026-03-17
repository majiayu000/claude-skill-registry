---
name: vialabs
description: VIA Labs (ViaLabs) MPN encoding patterns, series identification, and handler guidance. Use when working with USB hub/PD controller ICs or ViaLabsHandler.
---

# VIA Labs Manufacturer Skill

## MPN Structure

VIA Labs MPNs follow this general structure:

```
VL[SERIES][VARIANT][PACKAGE][-REEL]
 |   |       |        |       |
 |   |       |        |       └── Optional: REEL, TR, TUBE, TRAY for packaging
 |   |       |        └── Package code (Q, L, B, T, or explicit QFN/LQFP)
 |   |       └── Variant letter (optional)
 |   └── 3-digit series number (7xx, 8xx, 82x, 10x)
 └── VL = VIA Labs prefix
```

### Example Decoding

```
VL817-Q7
│  │  │
│  │  └── Q7 = QFN package variant
│  └── 817 = USB 3.0 hub controller
└── VL = VIA Labs prefix

VL822
│  │
│  └── 822 = USB 3.2 hub controller
└── VL = VIA Labs prefix
```

---

## Product Series

### VL7xx Series - USB 2.0 Hub Controllers

| Series | Ports | Description |
|--------|-------|-------------|
| VL750 | 4 | USB 2.0 4-port hub |
| VL751 | 4 | USB 2.0 4-port hub (variant) |
| VL752 | 7 | USB 2.0 7-port hub |

### VL8xx Series - USB 3.0 Hub Controllers

| Series | Ports | Description |
|--------|-------|-------------|
| VL812 | 4 | USB 3.0 4-port hub (1st gen) |
| VL813 | 4 | USB 3.0 4-port hub (2nd gen) |
| VL815 | 4 | USB 3.0 4-port hub (3rd gen) |
| VL817 | 4 | USB 3.0 4-port hub (latest) |

### VL82x Series - USB 3.2 Hub Controllers

| Series | Ports | Description |
|--------|-------|-------------|
| VL820 | 4 | USB 3.2 4-port hub |
| VL822 | 4 | USB 3.2 4-port hub (2nd gen) |
| VL823 | 4 | USB 3.2 4-port hub (latest) |

### VL10x Series - USB Power Delivery Controllers

| Series | Type | Description |
|--------|------|-------------|
| VL100 | PD | USB Power Delivery controller |
| VL102 | PD | USB PD controller (variant) |
| VL103 | PD | USB PD controller (latest) |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| Q | QFN | Quad Flat No-Lead |
| QFN | QFN | Explicit form |
| L | LQFP | Low-profile Quad Flat Package |
| LQFP | LQFP | Explicit form |
| B | BGA | Ball Grid Array |
| T | TQFP | Thin Quad Flat Package |

---

## USB Version by Series

| Series | USB Version |
|--------|-------------|
| VL750 | USB 2.0 |
| VL751 | USB 2.0 |
| VL752 | USB 2.0 |
| VL812 | USB 3.0 |
| VL813 | USB 3.0 |
| VL815 | USB 3.0 |
| VL817 | USB 3.0 |
| VL820 | USB 3.2 |
| VL822 | USB 3.2 |
| VL823 | USB 3.2 |
| VL10x | USB PD |

---

## Generation/Evolution

### USB 3.0 Hub Evolution

```
VL812 (Gen 1) -> VL813 (Gen 2) -> VL815 (Gen 3) -> VL817 (Gen 4 - Latest)
```

### USB 3.2 Hub Evolution

```
VL820 (Gen 1) -> VL822 (Gen 2) -> VL823 (Gen 3 - Latest)
```

---

## Handler Implementation Notes

### Pattern Matching

```java
// VL7xx series - USB 2.0 hub controllers
"^VL7[0-9]{2}[A-Z]*.*"

// VL8xx series - USB 3.0 hub controllers
"^VL8[0-9]{2}[A-Z]*.*"

// VL82x series - USB 3.2 hub controllers (more specific)
"^VL82[0-9][A-Z]*.*"

// VL10x series - USB Power Delivery controllers
"^VL10[0-9][A-Z]*.*"
```

### Series Extraction

```java
// Series is always "VL" + 3 digits = 5 characters
// VL817-Q7 -> VL817
// VL822 -> VL822

if (upperMpn.matches("^VL8[0-9]{2}.*")) {
    return upperMpn.substring(0, 5);
}
```

### Package Code Extraction

```java
// Handle suffix after hyphen
// VL817-Q7 -> Q -> QFN

// Handle trailing suffix without hyphen
// VL817Q -> Q -> QFN
```

---

## Replacement Compatibility

### USB 2.0 Hub Family

All VL7xx series are generally interchangeable:
- VL750, VL751 (4-port)
- VL752 is NOT interchangeable (7-port)

### USB 3.0 Hub Upgrade Path

Newer generations can replace older:
- VL817 can replace VL815, VL813, VL812
- VL815 can replace VL813, VL812
- VL813 can replace VL812

### USB 3.2 Hub Upgrade Path

Newer generations can replace older:
- VL823 can replace VL822, VL820
- VL822 can replace VL820

### Cross-Version Compatibility

**NOT compatible across USB versions:**
- VL7xx (USB 2.0) NOT compatible with VL8xx (USB 3.0)
- VL8xx (USB 3.0) NOT compatible with VL82x (USB 3.2)
- Different USB versions have different electrical requirements

---

## Port Count Reference

| Series | Downstream Ports |
|--------|------------------|
| VL750 | 4 |
| VL751 | 4 |
| VL752 | 7 |
| VL812-VL817 | 4 |
| VL820-VL823 | 4 |

---

## Common Applications

| Product Type | Typical Series |
|--------------|----------------|
| Basic USB 2.0 hub | VL750, VL751 |
| 7-port USB 2.0 hub | VL752 |
| USB 3.0 hub | VL817 (current), VL815 |
| USB 3.2 hub | VL823 (current), VL822 |
| USB-C PD controller | VL100, VL102, VL103 |

---

## Related Files

- Handler: `manufacturers/ViaLabsHandler.java`
- Component types: `ComponentType.IC`

---

## Learnings & Edge Cases

- **VL prefix for all parts**: Unlike VIA Technologies (VT prefix), VIA Labs uses VL prefix
- **3-digit numbering scheme**: 7xx = USB 2.0, 8xx = USB 3.0, 82x = USB 3.2, 10x = PD
- **Generation within series**: Higher second digit = newer generation (812 < 813 < 815 < 817)
- **USB 3.2 overlaps with 8xx**: VL82x is technically VL8xx but specifically USB 3.2
- **4-port is standard**: Most VIA Labs hubs are 4-port; VL752 is exception with 7 ports
- **Package suffix format varies**: Can be hyphenated (VL817-Q7) or appended (VL817Q)

<!-- Add new learnings above this line -->
