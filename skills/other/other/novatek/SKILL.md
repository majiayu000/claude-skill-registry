---
name: novatek
description: Novatek Microelectronics MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Novatek display driver components or NovatekHandler.
---

# Novatek Microelectronics Manufacturer Skill

## MPN Structure

Novatek MPNs follow this general structure:

```
[PREFIX][SERIES][MODEL][VARIANT][PACKAGE][-OPTION]
   |       |       |       |        |        |
   |       |       |       |        |        +-- Optional: additional options
   |       |       |       |        +-- Package: H=COG, C=COF, A=AMOLED, D=Display
   |       |       |       +-- Variant letter for revisions
   |       |       +-- Model number (3 digits)
   |       +-- Series digits (35, 36, 37, 38, 39, 50, 51, 66, 67)
   +-- NT prefix (all Novatek products)
```

### Example Decoding

```
NT35510H
|  |   ||
|  |   |+-- H = COG package
|  |   +-- (no variant)
|  +-- 35510 = TFT LCD driver model
+-- NT = Novatek prefix

NT36672A-DP
|  |    | ||
|  |    | |+-- P = additional option
|  |    | +-- D = Display driver type
|  |    +-- A = AMOLED variant
|  +-- 36672 = AMOLED driver model
+-- NT = Novatek prefix
```

---

## Product Families

### NT35xxx Series - TFT LCD Drivers

| Part Number | Description | Resolution |
|-------------|-------------|------------|
| NT35510 | TFT LCD driver | 480x800 |
| NT35516 | TFT LCD driver | 540x960 |
| NT35596 | TFT LCD driver | 1080x1920 |

### NT36xxx Series - AMOLED Drivers

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT36672 | AMOLED driver | FHD+ |
| NT36672A | AMOLED driver | Improved A variant |
| NT36675 | AMOLED driver | Premium panel |

### NT37xxx/NT38xxx Series - Display Drivers

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT37xxx | OLED drivers | General OLED |
| NT38xxx | Display drivers | Various panels |

### NT39xxx Series - Advanced Display Controllers

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT39016 | Advanced display | Multi-interface |
| NT39xxx | Advanced display | Special applications |

### NT50xxx Series - Timing Controllers (TCON)

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT50xxx | Timing controller | Panel timing |

### NT51xxx Series - LED Backlight Drivers

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT51xxx | LED backlight | Backlight control |

### NT66xxx/NT67xxx Series - Touch Controllers

| Part Number | Description | Features |
|-------------|-------------|----------|
| NT66xxx | Touch controller | Capacitive touch |
| NT67xxx | Touch controller | Advanced touch |

---

## Package Codes

### Single-Letter Package Indicators

| Code | Package/Type | Notes |
|------|--------------|-------|
| H | COG | Chip-on-glass |
| C | COF | Chip-on-film |
| A | AMOLED | AMOLED variant |
| D | Display Driver | General display type |

### Multi-Letter Package Codes

| Code | Package | Notes |
|------|---------|-------|
| COG | Chip-on-Glass | Direct glass bonding |
| COF | Chip-on-Film | Flexible film bonding |
| BGA | BGA | Ball grid array |
| QFP | QFP | Quad flat package |
| WLCSP | WLCSP | Wafer level CSP |
| TFBGA | Thin Fine-pitch BGA | Thin BGA |
| FBGA | Fine-pitch BGA | Fine-pitch BGA |

---

## Display Technology Detection

```java
public String getDisplayTechnology(String mpn) {
    if (mpn.matches("^NT35[0-9]{3}.*")) return "TFT LCD";
    if (mpn.matches("^NT36[0-9]{3}.*")) return "AMOLED";
    if (mpn.matches("^NT37[0-9]{3}.*") || mpn.matches("^NT38[0-9]{3}.*")) return "OLED";
    if (mpn.matches("^NT39[0-9]{3}.*")) return "Advanced Display";
    if (mpn.matches("^NT50[0-9]{3}.*")) return "Timing Controller";
    if (mpn.matches("^NT51[0-9]{3}.*")) return "LED Backlight";
    if (mpn.matches("^NT66[0-9]{3}.*") || mpn.matches("^NT67[0-9]{3}.*")) return "Touch Controller";
    return "";
}
```

---

## Handler Implementation Notes

### Pattern Matching

```java
// NT35xxx - TFT LCD drivers
"^NT35[0-9]{3}[A-Z0-9-]*$"

// NT36xxx - AMOLED drivers
"^NT36[0-9]{3}[A-Z0-9-]*$"

// NT37xxx, NT38xxx - Display drivers
"^NT37[0-9]{3}[A-Z0-9-]*$"
"^NT38[0-9]{3}[A-Z0-9-]*$"

// NT39xxx - Advanced display controllers
"^NT39[0-9]{3}[A-Z0-9-]*$"

// NT50xxx - Timing controllers
"^NT50[0-9]{3}[A-Z0-9-]*$"

// NT51xxx - LED backlight drivers
"^NT51[0-9]{3}[A-Z0-9-]*$"

// NT66xxx, NT67xxx - Touch controllers
"^NT66[0-9]{3}[A-Z0-9-]*$"
"^NT67[0-9]{3}[A-Z0-9-]*$"
```

### Package Code Extraction

```java
// Method 1: Check hyphenated suffix (NT35510-COG)
int hyphenIndex = mpn.indexOf('-');
if (hyphenIndex > 0) {
    String suffix = mpn.substring(hyphenIndex + 1);
    // Extract first part if multiple hyphens
    int nextHyphen = suffix.indexOf('-');
    if (nextHyphen > 0) suffix = suffix.substring(0, nextHyphen);
    // Map to package
}

// Method 2: Extract single-letter after NTxxxxx
// NT[0-9]{5}[A-Z]...
Pattern packagePattern = Pattern.compile("^NT[0-9]{5}([A-Z]).*$");
```

### Series Extraction

Returns first 4 characters (NT + 2 digits):
- NT35510 -> "NT35"
- NT36672 -> "NT36"
- NT66xxx -> "NT66"

---

## Related Files

- Handler: `manufacturers/NovatekHandler.java`
- Component types: `IC`, `LED_DRIVER`

---

## Common Use Cases

### Smartphone Display Drivers

Novatek is a leading supplier for smartphone display drivers:
- **NT35510**: Entry-level smartphone LCDs (480x800)
- **NT35596**: FHD smartphone LCDs (1080x1920)
- **NT36672**: AMOLED smartphone displays

### Display Technology Migration

| Upgrade Path | From | To |
|--------------|------|-----|
| LCD to AMOLED | NT35xxx | NT36xxx |
| Low-res to High-res | NT35510 | NT35596 |

---

## Replacement Considerations

### Family Compatibility

Parts within the same NTxx000 family (differing in last digit) may be revision variants:
- NT35510, NT35511 - possibly compatible
- Always verify pinout and register set compatibility

### Same Base Part

Same NTxxxxx with different package codes are NOT direct replacements (different physical form):
- NT35510H (COG) vs NT35510C (COF)

---

## Learnings & Edge Cases

- **5-digit model numbers**: Novatek uses NTxxxxx (5 digits after NT), unlike some competitors with 4 digits.
- **Suffix complexity**: Some parts have multi-part suffixes like NT36672A-DP where A=variant, D=type, P=option.
- **NT51xxx dual registration**: These are registered as both IC and LED_DRIVER since they're LED backlight controllers.
- **Touch vs Display**: NT66/NT67 series are touch controllers only; display is NT35/36/37/38/39.
- **TCON role**: NT50xxx timing controllers don't drive pixels - they control panel timing signals.
- **Family revisions**: Parts like NT35510 and NT35511 may be within the same family but check datasheets for differences.

<!-- Add new learnings above this line -->
