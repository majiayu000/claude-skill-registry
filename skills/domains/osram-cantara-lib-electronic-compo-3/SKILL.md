---
name: osram
description: OSRAM Opto Semiconductors MPN encoding patterns, LED color/package decoding, and handler guidance. Use when working with OSRAM LEDs or OSRAMHandler.
---

# OSRAM Opto Semiconductors Manufacturer Skill

## Overview

OSRAM Opto Semiconductors (now part of ams OSRAM) is a leading manufacturer of:
- **Standard LEDs** - Through-hole indicator LEDs
- **SMD LEDs** - Surface mount LEDs in various colors
- **High-Power LEDs** - OSLON, DURIS series for lighting applications
- **RGB/RGBW LEDs** - Multi-color LEDs for dynamic lighting
- **Automotive Lighting** - High-reliability LEDs for vehicle applications
- **Optocouplers** - Although not yet in handler patterns

## MPN Structure

OSRAM LEDs follow a structured naming convention:

### Standard/SMD LEDs (L-prefix)

```
L[COLOR][SERIES][VARIANT][PACKAGE]
│   │      │       │         │
│   │      │       │         └── Package code (G6, G4, T2, CH, MS, P2, CR)
│   │      │       └── Variant/brightness code
│   │      └── Series identifier (1 alphanumeric char)
│   └── Color code (S, W, A, Y, B, R, G)
└── "L" prefix for LED
```

### Color Codes (2nd character)

| Code | Color | Example Series |
|------|-------|----------------|
| S | Standard/Red | LS (standard through-hole) |
| W | White | LW (white SMD) |
| A | Amber | LA (amber SMD) |
| Y | Yellow | LY (yellow SMD) |
| B | Blue | LB (blue SMD) |
| R | Red | LR (red SMD) |
| G | Green | LG (green SMD) |

### High-Power LEDs (Named Series)

```
[SERIES][VARIANT][PACKAGE]
    │       │        │
    │       │        └── Package code (SX, SSL, S5, P3)
    │       └── Variant/specs
    └── Series name: OSLON, DURIS, OSRAM
```

### RGB LEDs (LRTB/LBCW prefix)

```
LRTB[VARIANT][SPEC]  - RGB LEDs
LBCW[VARIANT][SPEC]  - RGBW LEDs (RGB + White)
```

---

## Package Codes

### SMD LED Packages

| Code | Package | Description |
|------|---------|-------------|
| G6 | PLCC-6 | 6-pad PLCC, RGB capable |
| G4 | PLCC-4 | 4-pad PLCC, single color |
| T2 | TOP-LED | Top-emitting SMD |
| CH | Chip-LED | Compact chip package |
| MS | Mini-SIDELED | Side-emitting miniature |
| P2 | Power-TOPLED | Higher power top LED |
| CR | Ceramic | Ceramic substrate LED |

### High-Power LED Packages

| Code | Package | Description |
|------|---------|-------------|
| SX | Square | Standard OSLON Square |
| SSL | Square Lite | Slim OSLON Square |
| S5 | Square 5mm | 5mm OSLON Square |
| P3 | PowerStar | High-power star package |

### Through-Hole

| Prefix | Package | Description |
|--------|---------|-------------|
| LS | THT | Through-hole 3mm/5mm LEDs |

---

## Supported Component Types

From `OSRAMHandler.getSupportedTypes()`:

| ComponentType | Description | Pattern |
|---------------|-------------|---------|
| `LED` | Base LED type | All LED patterns |
| `LED_STANDARD_OSRAM` | Through-hole LEDs | `^LS[A-Z][0-9].*` |
| `LED_SMD_OSRAM` | Surface mount LEDs | `^L[WABYRG][A-Z][0-9].*` |
| `LED_HIGHPOWER_OSRAM` | High-power LEDs | `^(OSLON\|OSRAM\|DURIS).*` |
| `LED_RGB_OSRAM` | RGB/RGBW LEDs | `^(LRTB\|LBCW).*` |

---

## Pattern Matching Details

### Standard LEDs
```regex
^LS[A-Z][0-9].*
```
- Starts with `LS` (Standard LED prefix)
- Followed by letter (series) and digit (variant)
- Example: `LST5678` - Standard LED series T

### SMD LEDs (by color)
```regex
^LW[A-Z][0-9].*  - White
^LA[A-Z][0-9].*  - Amber
^LY[A-Z][0-9].*  - Yellow
^LB[A-Z][0-9].*  - Blue
^LR[A-Z][0-9].*  - Red
^LG[A-Z][0-9].*  - Green
```

### High-Power LEDs
```regex
^OSLON.*   - OSLON series
^OSRAM.*   - OSRAM branded high-power
^DURIS.*   - DURIS general illumination
```

### RGB LEDs
```regex
^LRTB.*    - RGB LEDs
^LBCW.*    - RGBW (RGB + White)
```

---

## Example MPNs with Explanations

### Standard Through-Hole LEDs
```
LST5678
│  │└── Series/variant number
│  └── Series letter
└── Standard LED prefix

Package: THT (through-hole)
Series: LST5 (extracted first 4 chars)
```

### SMD LEDs
```
LWE6SG-G4
│ │││  │
│ │││  └── G4 = PLCC-4 package
│ ││└── Additional variant code
│ │└── Series number
│ └── E = Series letter
└── LW = White SMD LED

Color: White
Package: PLCC-4
Series: LWE6 (first 4 chars)
```

```
LR E6SP-G4
│  │  │ │
│  │  │ └── PLCC-4 package
│  │  └── Brightness code
│  └── Series identifier
└── LR = Red SMD LED

Color: Red
Package: PLCC-4
```

### High-Power LEDs
```
OSLON SSL 80
│      │   │
│      │   └── Power class
│      └── SSL = Square Lite package
└── OSLON series

Package: Square Lite
Series: OSLON
```

```
DURIS E5
│     │
│     └── Variant identifier
└── DURIS general illumination series

Package: (extracted from suffix)
Series: DURIS
```

### RGB LEDs
```
LRTB G6SG
│     │
│     └── G6 = PLCC-6 package (needed for RGB)
└── LRTB = RGB LED

Package: PLCC-6
Series: LRTB
```

```
LBCW AYBZ
│    │
│    └── Variant/spec codes
└── LBCW = RGBW LED (RGB + White die)

Series: LBCW
```

---

## Series Extraction Logic

The handler extracts series using these rules:

1. **Standard/SMD LEDs** (LS, LW, LA, LY, LB, LR, LG prefix):
   - Extract first 3-4 alphanumeric characters
   - Example: `LWE6SG-G4` -> `LWE6`

2. **High-Power LEDs** (OSLON, DURIS):
   - Extract up to first space
   - Example: `OSLON SSL 80` -> `OSLON`
   - Example: `DURIS E5` -> `DURIS`

3. **RGB LEDs** (LRTB, LBCW):
   - Extract first 4 characters
   - Example: `LRTB G6SG` -> `LRTB`

---

## Package Code Extraction Logic

The handler extracts package codes based on prefix:

1. **LS prefix** (Standard): Returns `THT`

2. **SMD LEDs** (LW, LA, LY, LB, LR, LG):
   - Strips leading alphanumerics to find suffix
   - Maps suffix to package name using switch statement

3. **High-Power LEDs** (OSLON, DURIS):
   - Strips series name to find suffix
   - Maps to package (SX, SSL, S5, P3)

---

## Replacement Logic

`isOfficialReplacement()` returns true when:

1. **Same series** - Both MPNs have the same extracted series
2. **Color LEDs** - Same color code (second character matches for L-prefix)
3. **OSLON/DURIS** - Same series family

```java
// Same color, same series = replacement
"LR E6SP-G4"  vs  "LR E6SP-G6"   // Both red, same series -> true
"LW E6SG-G4"  vs  "LR E6SG-G4"   // Different colors -> false

// High-power same family
"OSLON SSL 80" vs "OSLON SSL 150" // Both OSLON SSL -> true
```

---

## Related LED Families

### OSRAM LED Series Comparison

| Series | Application | Features |
|--------|-------------|----------|
| LS | Indicators | Through-hole, low power |
| LW/LR/LG/etc. | SMD indicators | Various packages |
| OSLON | Automotive, general | High efficiency |
| DURIS | General illumination | Mid-power |
| TOPLED | SMD indicators | Top-emitting |

### Cross-Manufacturer Equivalents

| OSRAM Series | Similar Products |
|--------------|------------------|
| OSLON | Cree XP, Lumileds LUXEON |
| DURIS | Samsung LM series |
| TOPLED | Vishay VLMX, Lite-On LTL |

---

## Handler Implementation Notes

### Known Bugs/Limitations

1. **HashSet in getSupportedTypes()**: Uses mutable HashSet instead of Set.of()
   - Should be fixed to use `Set.of()` for immutability

2. **Package extraction for high-power LEDs**:
   - Uses `replaceAll("^[A-Z0-9]+", "")` which may not correctly isolate suffix
   - Works for named series (OSLON, DURIS) but may need refinement

3. **No optocoupler patterns**:
   - OSRAM makes optocouplers but handler only covers LEDs
   - Could add patterns like `SFH.*` for optocouplers

4. **Color temperature not extracted**:
   - White LEDs (LW) have CCT variants not currently parsed

### Package Code Extraction Quirk

For SMD LEDs, the regex `^[A-Z0-9]+` is used to strip the prefix:
```java
String suffix = mpn.replaceAll("^[A-Z0-9]+", "");
```
This removes ALL leading alphanumerics, leaving only the package suffix if separated by a hyphen or if it starts with a non-alphanumeric. For MPNs like `LWE6SG-G4`, the hyphen separates the suffix properly.

---

## Related Files

- Handler: `manufacturers/OSRAMHandler.java`
- Component types: `LED`, `LED_STANDARD_OSRAM`, `LED_SMD_OSRAM`, `LED_HIGHPOWER_OSRAM`, `LED_RGB_OSRAM`
- Similarity: See `LEDSimilarityCalculator` for LED comparison logic

---

## Learnings & Quirks

### MPN Format Variations
- Some OSRAM MPNs include spaces (e.g., `OSLON SSL 80`, `LR E6SP`)
- Handler uses space-aware extraction for series names

### Color Code Position
- Second character of L-prefix MPNs indicates color
- Same position used for replacement compatibility check

### Package Code Dependencies
- PLCC-6 (G6) typically used for RGB LEDs (needs 6 pads for R, G, B + common)
- PLCC-4 (G4) for single-color SMD LEDs

### ams OSRAM Merger
- OSRAM Opto Semiconductors merged with ams in 2021
- Legacy OSRAM part numbers remain valid
- New products may use different naming conventions

### No Automotive-Specific Patterns
- Handler doesn't distinguish automotive-grade LEDs
- OSRAM has significant automotive LED portfolio (OSLON Black, Synios)

<!-- Add new learnings above this line -->
