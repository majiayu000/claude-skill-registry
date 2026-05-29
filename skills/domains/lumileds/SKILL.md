---
name: lumileds
description: Lumileds MPN encoding patterns for LUXEON LEDs, automotive LEDs, and handler guidance. Use when working with Lumileds LED components or LumiledsHandler.
---

# Lumileds Manufacturer Skill

## Company Overview

Lumileds is a global leader in LED technology, best known for the **LUXEON** brand of high-power LEDs. Originally part of Philips Lighting, Lumileds specializes in:

- **High-power LEDs** for general illumination
- **Automotive LEDs** for headlights, taillights, and interior lighting
- **Mid-power LEDs** for industrial and commercial applications
- **Color LEDs** for architectural and entertainment lighting
- **UV and IR LEDs** for specialized applications

## MPN Structure

Lumileds MPNs follow different patterns depending on the product line:

### Classic LUXEON Format (LXxx)

```
LX[SERIES][VARIANT][-COLOR][-OPTION]
│  │       │        │       │
│  │       │        │       └── Options: PW=Power, ES=Emitter, etc.
│  │       │        └── Color code after dash
│  │       └── Variant identifier
│  └── Series code (ML=Rebel, HL=III, Z1=Z, CL=C, etc.)
└── LX = LUXEON prefix
```

### New Format (L1xx, L2xx)

```
L[GEN][SERIES][VARIANT][-COLOR][-OPTION]
│ │    │       │        │       │
│ │    │       │        │       └── Options: package/application
│ │    │       │        └── Color code after dash
│ │    │       └── Variant code
│ │    └── Series (T2=TX, M1=M, V0=V)
│ └── Generation (1=current, 2=next)
└── L = Lumileds prefix
```

### Mid-Power Format (L1xx)

```
L1[SIZE][VARIANT][-COLOR]
│  │     │        │
│  │     │        └── Color code
│  │     └── Variant identifier
│  └── Package size (30=3030, 35=3535, 50=5050)
└── L1 = Mid-power series prefix
```

---

## LUXEON Series Overview

### High-Power LEDs

| Series | Prefix | Description | Typical Application |
|--------|--------|-------------|---------------------|
| LUXEON TX | L1T2 | High flux density | General lighting |
| LUXEON M | L1M1 | High power die | Directional lighting |
| LUXEON V | L1V0 | High voltage | Street lighting |
| LUXEON Rebel | LXML | Industry standard | Retrofits, modules |
| LUXEON III | LXHL | Legacy high power | Replacement parts |

### Color LEDs

| Series | Prefix | Description | Colors Available |
|--------|--------|-------------|------------------|
| LUXEON Z | LXZ1 | Compact color | R, G, B, A, PC |
| LUXEON C | LXCL | Color mixing | Full spectrum |

### RGB & Multi-Die LEDs

| Series | Prefix | Description | Die Configuration |
|--------|--------|-------------|-------------------|
| LUXEON Altilon | LXI8 | High-power multi-chip | 4-die |
| LUXEON RGB | LXA7 | Full RGB | 3-die RGB |

### Mid-Power LEDs

| Series | Prefix | Package Size | Typical Power |
|--------|--------|--------------|---------------|
| LUXEON 3030 | L130 | 3.0 x 3.0mm | 0.5-1W |
| LUXEON 3535 | L135 | 3.5 x 3.5mm | 1-2W |
| LUXEON 5050 | L150 | 5.0 x 5.0mm | 2-5W |

### Low-Power LEDs

| Series | Prefix | Description |
|--------|--------|-------------|
| LUXEON Low-Power | LW Q18 | Low power applications |

### Automotive LEDs

| Series | Prefix | Description | Application |
|--------|--------|-------------|-------------|
| LUXEON Altilon Automotive | LXA2 | High-power automotive | Headlights |
| LUXEON F | LXA3 | Automotive-grade | Front lighting |

---

## Example MPNs with Decoding

### High-Power Examples

```
LXML-PWC1-0100
│    │    │
│    │    └── 0100 = Flux bin code
│    └── PWC1 = Cool white, power grade
└── LXML = LUXEON Rebel series

LXHL-PW09
│    │
│    └── PW09 = Power white, bin 09
└── LXHL = LUXEON III series

L1T2-3070000000000
│    │
│    └── 3070000000000 = Full part specification
└── L1T2 = LUXEON TX series
```

### Color LED Examples

```
LXZ1-PB01
│    │
│    └── PB01 = Blue, bin 01
└── LXZ1 = LUXEON Z series

LXCL-PR01
│    │
│    └── PR01 = Red, bin 01
└── LXCL = LUXEON C series
```

### Mid-Power Examples

```
L130-5780003000W21
│    │           │
│    │           └── W21 = White bin variant
│    └── 5780003000 = Flux/CCT specification
└── L130 = LUXEON 3030 (3.0x3.0mm package)

L135-2780003000W01
│    │
│    └── 2780003000W01 = Full specification
└── L135 = LUXEON 3535 (3.5x3.5mm package)
```

### Automotive Examples

```
LXA2-PW00
│    │
│    └── PW00 = Power white, automotive grade
└── LXA2 = LUXEON Altilon Automotive

LXA3-PW12
│    │
│    └── PW12 = Power white, bin 12
└── LXA3 = LUXEON F (automotive front lighting)
```

---

## Package Codes

### Package Extraction Rules

The handler extracts package codes based on series prefix:

| Series Prefix | Package Code | Physical Size | Notes |
|---------------|--------------|---------------|-------|
| LXZ1 | Z2 | 2.2 x 1.4mm | LUXEON Z compact package |
| LXML | Rebel | 4.4 x 4.4mm | Industry-standard Rebel |
| L130 | 3030 | 3.0 x 3.0mm | Mid-power standard |
| L135 | 3535 | 3.5 x 3.5mm | Mid-power standard |
| L150 | 5050 | 5.0 x 5.0mm | High-power mid-power |

### Suffix-Based Package Codes

| Suffix | Package Type | Description |
|--------|--------------|-------------|
| PW | Power | High-power package variant |
| ES | Emitter | Bare emitter (no lens) |
| DS | DomeLED | Dome lens package |
| UV | UV | UV wavelength package |
| IR | IR | Infrared package |
| RGB | RGB | RGB multi-die package |
| RGBW | RGBW | RGBW multi-die package |

---

## Series Extraction Rules

### LX-Prefix Series (Classic LUXEON)

For MPNs starting with `LX`, extract the first 4 alphanumeric characters:

```java
// LXML-PWC1-0100 → LXML
// LXHL-PW09 → LXHL
// LXZ1-PB01 → LXZ1
// LXA2-PW00 → LXA2

for (int i = 0; i < mpn.length() && i < 4; i++) {
    if (Character.isLetterOrDigit(mpn.charAt(i))) {
        series.append(mpn.charAt(i));
    }
}
```

### L1/L2-Prefix Series (Newer Products)

For MPNs starting with `L1` or `L2`, extract the first 4 characters:

```java
// L1T2-3070000000000 → L1T2
// L1M1-xxx → L1M1
// L1V0-xxx → L1V0

return mpn.substring(0, 4);
```

### Numbered Series (Mid-Power)

For MPNs starting with `L` followed by digits, extract until non-alphanumeric:

```java
// L130-5780003000W21 → L130
// L135-xxx → L135
// L150-xxx → L150

for (char c : mpn.toCharArray()) {
    if (Character.isLetterOrDigit(c)) {
        series.append(c);
    } else {
        break;
    }
}
```

---

## Color Code Extraction

Color codes are typically found after a dash in the MPN:

### For LUXEON Z and Rebel (LXZ1, LXML)

Color code is the first character after the dash:

```java
// LXZ1-PB01 → P (Power) or B (Blue) depending on interpretation
// Extract position dash+1

int dashIndex = mpn.indexOf('-');
if (dashIndex > 0 && dashIndex + 2 <= mpn.length()) {
    return mpn.substring(dashIndex + 1, dashIndex + 2);
}
```

### For Mid-Power (L130, L135)

Color code is positions 4-5 (after series prefix):

```java
// L130-5780003000W21 → positions 4-5 after prefix
if (mpn.length() >= 6) {
    return mpn.substring(4, 6);
}
```

---

## Compatible Series (Replacement Logic)

The handler recognizes these cross-series compatibilities:

| Series 1 | Series 2 | Compatibility Notes |
|----------|----------|---------------------|
| LXML (Rebel) | LXZ1 (Z) | Similar flux, different footprint |
| L130 (3030) | L135 (3535) | Same technology, different size |

**Note**: Cross-series compatibility indicates similar electrical characteristics but may require PCB redesign due to different footprints.

---

## Supported Component Types

The handler supports these ComponentType values:

| Type | Description |
|------|-------------|
| `LED` | Generic LED type |
| `LED_HIGHPOWER_LUMILEDS` | Lumileds-specific high-power LED |

---

## Handler Implementation Notes

### Pattern Registration

All patterns are registered for both `LED` (base type) and `LED_HIGHPOWER_LUMILEDS` (manufacturer-specific type):

```java
// Each series is registered twice
registry.addPattern(ComponentType.LED, "^L1T2.*");
registry.addPattern(ComponentType.LED_HIGHPOWER_LUMILEDS, "^L1T2.*");
```

### getSupportedTypes() Issue

**Known Bug**: The handler uses `HashSet` instead of `Set.of()`:

```java
// Current (mutable, non-deterministic order)
Set<ComponentType> types = new HashSet<>();
types.add(ComponentType.LED);
types.add(ComponentType.LED_HIGHPOWER_LUMILEDS);

// Should be (immutable, deterministic)
return Set.of(ComponentType.LED, ComponentType.LED_HIGHPOWER_LUMILEDS);
```

### Package Code Extraction Notes

1. Series-based extraction takes precedence over suffix extraction
2. If no series match, suffix is extracted via regex `^[A-Z0-9]+`
3. Unknown suffixes are returned as-is (no default)

---

## Related Files

- Handler: `manufacturers/LumiledsHandler.java`
- Component types: `LED`, `LED_HIGHPOWER_LUMILEDS`
- Similarity calculator: `LEDSimilarityCalculator.java`

---

## Learnings & Quirks

### MPN Format Variability

- LUXEON MPNs have varying levels of detail after the dash
- Some MPNs include flux bins, CCT values, and packaging codes
- The same LED may have many MPN variants for different bins/CCT

### Low-Power Series Pattern

The `LW Q18` pattern includes a space, which is unusual:
```java
registry.addPattern(ComponentType.LED, "^LW Q18.*");
```
This may cause issues with MPN normalization that removes spaces.

### Color Bin vs CCT

- Color LEDs use color codes (R, G, B, A=Amber, PC=PhotonConversion)
- White LEDs use CCT bins in the MPN (2700K, 4000K, 5000K, etc.)
- The handler's `extractColorCode()` method handles both patterns

### Automotive Qualification

- LXA2 and LXA3 series are AEC-Q102 qualified
- Automotive MPNs may have additional suffixes for qualification level

### Handler Test Coverage

As of January 2026, LumiledsHandler does not have dedicated tests. When adding tests:

1. Place tests in `handlers` package, NOT `manufacturers` package
2. Use `MPNUtils.getManufacturerHandler("LXML-PWC1")` for handler access
3. Test all series prefixes: L1T2, L1M1, L1V0, LXML, LXHL, LXZ1, LXCL, LXI8, LXA7, L130, L135, L150, LW Q18, LXA2, LXA3

### Cross-Manufacturer Equivalents

LUXEON LEDs compete with:
- Cree XP-E, XP-G series
- OSRAM OSLON series
- Nichia 757 series
- Samsung LM301 series

These are NOT direct replacements due to different footprints and optical characteristics.

<!-- Add new learnings above this line -->
