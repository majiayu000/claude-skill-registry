---
name: ftdi
description: FTDI (Future Technology Devices International) MPN encoding patterns, USB interface chip decoding, and handler guidance. Use when working with FTDI USB bridge ICs or FTDIHandler.
---

# FTDI Manufacturer Skill

## Company Overview

FTDI (Future Technology Devices International) specializes in USB interface ICs and bridge chips. Their products convert USB to various protocols including serial UART, I2C, SPI, and parallel FIFO interfaces. FTDI chips are widely used for USB-to-serial converters, development boards, and embedded systems.

---

## MPN Structure

FTDI MPNs follow this general structure:

```
FT[SERIES][VARIANT][PACKAGE][-QUALIFIER]
│    │       │        │         │
│    │       │        │         └── Optional: REEL=Tape/Reel, TUBE=Tube, TRAY=Tray
│    │       │        └── Package code (see table below)
│    │       └── Variant letter(s) (H=High-speed, D=Device, X=X-series)
│    └── Series number (232, 2232, 4232, 230, etc.)
└── FT prefix (always present)
```

### Example Decoding

```
FT232RL
│  │ ││
│  │ │└── L = SSOP variant (RL = SSOP-28)
│  │ └── R = First generation revision
│  └── 232 = USB to UART bridge series
└── FT = FTDI prefix

FT2232H-REEL
│  │   │  │
│  │   │  └── REEL = Tape and reel packaging
│  │   └── H = High-speed USB 2.0
│  └── 2232 = Dual channel series
└── FT = FTDI prefix

FT230XS-R
│  │  ││ │
│  │  ││ └── R = Tape and reel (shortened)
│  │  │└── S = SSOP package
│  │  └── X = X-series (low-cost, simplified)
│  └── 230 = Basic UART series
└── FT = FTDI prefix
```

---

## Supported Component Types

The FTDIHandler supports a single component type:

| ComponentType | Description |
|---------------|-------------|
| `IC` | All FTDI USB interface ICs |

Note: FTDI products are all ICs - there are no manufacturer-specific component types defined (e.g., no `USB_BRIDGE_FTDI`).

---

## Package Codes

### Single Letter Codes

| Code | Package | Pin Count | Notes |
|------|---------|-----------|-------|
| R | SSOP | 28 | FT232R standard package |
| S | SSOP | 16-28 | Standard SSOP |
| Q | QFN | 20-32 | QFN variant |
| H | LQFP | 48-64 | High-speed devices |
| D | LQFP | 48 | FT2232D |
| X | TSSOP | 20 | Thin profile |
| T | TQFP | 32-48 | Standard TQFP |

### Two Letter Codes

| Code | Package | Pin Count | Notes |
|------|---------|-----------|-------|
| RL | SSOP | 28 | FT232RL (most common) |
| RQ | QFN | 32 | FT232RQ |
| BL | LQFP | 76 | FT600/FT601 LQFP |
| BQ | QFN | 56 | FT600/FT601 QFN |
| XS | TSSOP | 16-20 | X-series TSSOP |
| XQ | QFN | 16-20 | X-series QFN |

### Packaging Suffixes (After Hyphen)

| Suffix | Meaning |
|--------|---------|
| -REEL | Tape and reel |
| -TUBE | Tube packaging |
| -TRAY | Tray packaging |
| -R | Tape and reel (shortened) |

---

## Product Families

### USB to Serial UART

| Series | Channels | USB Speed | Control Lines | Notes |
|--------|----------|-----------|---------------|-------|
| FT232 | 1 | Full-Speed | Full modem | Original, most common |
| FT230X | 1 | Full-Speed | None | Basic, low-cost |
| FT231X | 1 | Full-Speed | RTS/CTS | X-series with handshaking |
| FT234X | 1 | Full-Speed | RTS/CTS/DTR/DSR | X-series full control |
| FT2232 | 2 | High-Speed | Full modem | Dual channel |
| FT4232 | 4 | High-Speed | Partial | Quad channel |

### USB to I2C

| Series | Channels | USB Speed | Notes |
|--------|----------|-----------|-------|
| FT200XD | 1 | Full-Speed | USB to I2C bridge |
| FT201X | 1 | Full-Speed | USB to I2C with GPIO |
| FT260 | 1 | Full-Speed | HID-class I2C/UART |

### USB to SPI

| Series | Channels | USB Speed | Notes |
|--------|----------|-----------|-------|
| FT220X | 1 | Full-Speed | USB to SPI/FT1248 |
| FT221X | 1 | Full-Speed | USB to SPI with GPIO |

### USB to FIFO

| Series | Bus Width | USB Speed | Notes |
|--------|-----------|-----------|-------|
| FT240X | 8-bit | Full-Speed | USB 2.0 FIFO |
| FT600 | 16-bit | Super-Speed | USB 3.0 FIFO |
| FT601 | 32-bit | Super-Speed | USB 3.0 FIFO |

### Specialized Products

| Series | Type | Notes |
|--------|------|-------|
| FT51A | USB MCU | 8051-based USB programmable MCU |
| FT311D | Android AOA | USB Android Open Accessory host |
| FT312D | Android AOA | USB Android Open Accessory device |
| FT800/FT81x | EVE | Embedded Video Engine (display controller) |

---

## USB Speed Reference

| Category | USB Speed | Bandwidth | Devices |
|----------|-----------|-----------|---------|
| Full-Speed | USB 2.0 FS | 12 Mbps | FT232, FT23xX, FT2xxX, FT260 |
| High-Speed | USB 2.0 HS | 480 Mbps | FT2232H, FT4232H |
| Super-Speed | USB 3.0 SS | 5 Gbps | FT600, FT601 |

---

## Series Extraction Rules

The handler extracts series using these patterns:

```java
// FT232 family - returns "FT232"
if (mpn.matches("^FT232[A-Z]{0,2}.*")) return "FT232";

// FT2232/FT4232 - returns "FT2232" or "FT4232"
if (mpn.matches("^FT2232[A-Z]?.*")) return "FT2232";
if (mpn.matches("^FT4232[A-Z]?.*")) return "FT4232";

// X-series - returns "FT230X", "FT231X", etc.
if (mpn.matches("^FT230X.*")) return "FT230X";
if (mpn.matches("^FT231X.*")) return "FT231X";
if (mpn.matches("^FT234X.*")) return "FT234X";

// USB 3.0 - returns "FT600" or "FT601"
if (mpn.matches("^FT600.*")) return "FT600";
if (mpn.matches("^FT601.*")) return "FT601";

// EVE series - returns "FT800" or "FT810", "FT811", etc.
if (mpn.matches("^FT800.*")) return "FT800";
if (mpn.matches("^FT81[0-9].*")) return mpn.substring(0, 5);  // FT810, FT811, etc.
```

---

## Package Code Extraction Rules

The handler uses a priority system for package extraction:

1. **Remove packaging suffixes first**: Strip `-REEL`, `-TUBE`, `-TRAY`
2. **Match specific patterns**:
   - `FT232[A-Z]{1,2}$` - Extract suffix after "FT232" (e.g., RL, RQ)
   - `FT[24]232[A-Z]$` - Extract last character (e.g., H, D)
   - `FT2[0-4][0-9]X[A-Z]?` - Extract character after X (e.g., S, Q)
   - `FT260[A-Z]` - Extract character after "FT260"
   - `FT60[0-1][A-Z]{1,2}` - Extract suffix after "FT60x" (e.g., BL, BQ)
3. **Resolve to package name**: Use PACKAGE_CODES map

```java
// Example: FT232RL-REEL
// Step 1: Remove -REEL -> FT232RL
// Step 2: Match FT232[A-Z]{1,2}$ -> suffix = "RL"
// Step 3: PACKAGE_CODES.get("RL") -> "SSOP"
```

---

## Replacement Compatibility

The handler implements `isOfficialReplacement()` with these rules:

### Same Series (Always Compatible)
Parts in the same series with different packages are always replacement-compatible:
- FT232RL <==> FT232RQ (same chip, different package)
- FT2232H <==> FT2232D (same functionality)

### X-Series UART Upgrade Path
X-series variants can replace each other in one direction (more pins = superset):
```
FT230X (0 control lines) <-- FT231X (2: RTS/CTS) <-- FT234X (4: +DTR/DSR)
```
- FT234X can replace FT231X or FT230X (superset)
- FT231X can replace FT230X
- Downgrade is NOT valid (FT230X cannot replace FT231X)

### NOT Compatible
- FT2232 vs FT4232 - Different channel count
- FT600 vs FT601 - Different bus width (16-bit vs 32-bit)
- FT232 vs FT2232 - Different channel count

---

## Helper Methods (FTDI-Specific)

The FTDIHandler provides additional helper methods:

### getInterfaceType(mpn)
Returns the USB interface type:
| Return Value | Series |
|--------------|--------|
| "UART" | FT232, FT2232, FT4232, FT23xX |
| "I2C" | FT200X, FT201X |
| "SPI" | FT220X, FT221X |
| "FIFO" | FT240X, FT600, FT601 |
| "I2C/UART" | FT260 |
| "USB MCU" | FT51A |
| "Android AOA" | FT311D, FT312D |
| "EVE" | FT8xx |

### getChannelCount(mpn)
Returns number of channels (1, 2, or 4):
- FT232, FT23xX, FT2xxX, FT260 -> 1
- FT2232, FT600 -> 2
- FT4232 -> 4

### getUsbVersion(mpn)
Returns USB version string:
- "USB 2.0 Full-Speed" - Most single-channel devices
- "USB 2.0 High-Speed" - FT2232H, FT4232H
- "USB 3.0 Super-Speed" - FT600, FT601

---

## Example MPNs

| MPN | Series | Package | Interface | Channels | USB Speed |
|-----|--------|---------|-----------|----------|-----------|
| FT232RL | FT232 | SSOP | UART | 1 | Full-Speed |
| FT232RQ-REEL | FT232 | QFN | UART | 1 | Full-Speed |
| FT2232H | FT2232 | LQFP | UART | 2 | High-Speed |
| FT4232H-REEL | FT4232 | LQFP | UART | 4 | High-Speed |
| FT230XS | FT230X | SSOP | UART | 1 | Full-Speed |
| FT231XQ-R | FT231X | QFN | UART | 1 | Full-Speed |
| FT234XD | FT234X | LQFP | UART | 1 | Full-Speed |
| FT201XS | FT201X | SSOP | I2C | 1 | Full-Speed |
| FT220XQ | FT220X | QFN | SPI | 1 | Full-Speed |
| FT240XS | FT240X | SSOP | FIFO | 1 | Full-Speed |
| FT260S | FT260 | SSOP | I2C/UART | 1 | Full-Speed |
| FT600BQ | FT600 | QFN | FIFO | 2 | Super-Speed |
| FT601BL-REEL | FT601 | LQFP | FIFO | 1 | Super-Speed |
| FT51AQ | FT51A | QFN | USB MCU | 1 | Full-Speed |
| FT812Q | FT812 | QFN | EVE | - | - |

---

## Handler Implementation Notes

### Pattern Matching Order

The handler defines explicit pattern checks in `matches()` for each family:

```java
// Pattern order in matches():
1. FT232 series:   "^FT232[A-Z]{0,2}.*"
2. FT2232 series:  "^FT2232[A-Z]?.*"
3. FT4232 series:  "^FT4232[A-Z]?.*"
4. X-series UART:  "^FT23[0-9]X[A-Z]?.*"
5. USB to I2C:     "^FT20[0-1]X[A-Z]?.*"
6. USB to SPI:     "^FT22[0-1]X[A-Z]?.*"
7. FT240X FIFO:    "^FT240X[A-Z]?.*"
8. FT260:          "^FT260[A-Z]?.*"
9. USB 3.0:        "^FT60[0-1][A-Z]?.*"
10. FT51A MCU:     "^FT51[A-Z].*"
11. Android AOA:   "^FT31[1-2]D.*"
12. FT120:         "^FT12[0-2].*"
13. EVE:           "^FT8[0-1][0-9].*"
```

### Handler Characteristics

- Uses `Set.of()` for `getSupportedTypes()` (correct, immutable)
- Overrides `matches()` with explicit pattern checks (avoids cross-handler issues)
- Returns empty set for `getManufacturerTypes()` (no manufacturer-specific types defined)
- Uses `Map.ofEntries()` for PACKAGE_CODES (correct, immutable)

---

## Related Files

- Handler: `manufacturers/FTDIHandler.java`
- Component types: Only `ComponentType.IC` (no FTDI-specific types)
- Tests: Should be in `handlers/FTDIHandlerTest.java` (not `manufacturers` package)

---

## Learnings & Edge Cases

- **Single ComponentType**: FTDI only supports `IC` - there are no manufacturer-specific types like `USB_BRIDGE_FTDI`. All FTDI products are ICs.
- **X in series name**: The "X" in FT230X/FT231X/etc. is part of the series name, not a package suffix. Package code comes AFTER the X.
- **Package suffix after X**: For X-series devices, the package code is the letter immediately following "X" (e.g., FT230X**S** = SSOP).
- **Two-letter package codes**: Some package codes are two letters (RL, RQ, BL, BQ). Check longer codes before shorter ones.
- **-R suffix ambiguity**: "-R" at the end typically means tape and reel (shortened from -REEL), but should be stripped before package extraction.
- **FT600 vs FT601**: Different bus widths (16-bit vs 32-bit), NOT interchangeable despite similar names.
- **FT8xx series**: These are EVE (Embedded Video Engine) display controllers, NOT USB bridge chips. Different product category entirely.
- **HID-class FT260**: The FT260 is unique - it's a HID-class device (no driver needed on most OS), supporting both I2C and UART.
- **H suffix meaning**: "H" after series number typically means High-Speed USB 2.0 (480 Mbps), e.g., FT2232**H**, FT4232**H**.
- **USB 3.0 devices (FT600/FT601)**: Use BL/BQ package suffixes, not the standard single-letter codes.

<!-- Add new learnings above this line -->
