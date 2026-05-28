---
name: raydium
description: Raydium Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Raydium display/touch controller components or RaydiumHandler.
---

# Raydium Semiconductor Manufacturer Skill

## MPN Structure

Raydium MPNs follow this general structure:

```
[PREFIX][SERIES][MODEL][PACKAGE]
   |       |       |       |
   |       |       |       +-- Package: COG, COF, BGA, QFN, WLCSP
   |       |       +-- Model number (3 digits: 120, 091, etc.)
   |       +-- Series digits (68, 69, 31, 35)
   +-- RM prefix (all Raydium products)
```

### Example Decoding

```
RM68120
|  |  |
|  |  +-- 120 = Model number
|  +-- 68 = TFT LCD driver series
+-- RM = Raydium prefix

RM69091-COG
|  |    |
|  |    +-- COG = Chip-on-glass package
|  +-- 69091 = AMOLED driver model
+-- RM = Raydium prefix

RM31100BGA
|  |    |
|  |    +-- BGA = Ball grid array package
|  +-- 31100 = Touch controller model
+-- RM = Raydium prefix
```

---

## Product Families

### RM68xxx Series - TFT LCD Drivers

| Part Number | Description | Resolution |
|-------------|-------------|------------|
| RM68120 | TFT LCD driver | 320x480 |
| RM68140 | TFT LCD driver | Variable |
| RM68172 | TFT LCD driver | Variable |

### RM69xxx Series - AMOLED Display Drivers

| Part Number | Description | Features |
|-------------|-------------|----------|
| RM69032 | AMOLED driver | Small panel |
| RM69080 | AMOLED driver | Mid-size panel |
| RM69091 | AMOLED driver | Wearable display |
| RM69299 | AMOLED driver | Premium panel |

### RM31xxx Series - Touch Controllers

| Part Number | Description | Features |
|-------------|-------------|----------|
| RM31100 | Touch controller | Capacitive touch |
| RM31080 | Touch controller | Multi-touch |

### RM35xxx Series - Touch + Display Controllers

| Part Number | Description | Features |
|-------------|-------------|----------|
| RM35xxx | Integrated touch+display | Combined controller |

---

## Package Codes

| Code | Package | Description |
|------|---------|-------------|
| COG | Chip-on-Glass | Direct bonding to glass substrate |
| COF | Chip-on-Film | Flexible film bonding |
| BGA | Ball Grid Array | Standard BGA |
| QFN | Quad Flat No-leads | Leadless package |
| WLCSP | Wafer Level CSP | Ultra-compact package |

### Package Notation

Raydium uses two package notation styles:
1. **Hyphenated**: RM69091-COG
2. **Concatenated**: RM31100BGA

---

## Handler Implementation Notes

### Pattern Matching

```java
// RM68xxx - TFT LCD drivers
"^RM68[0-9]{3}[A-Z0-9-]*$"

// RM69xxx - AMOLED display drivers
"^RM69[0-9]{3}[A-Z0-9-]*$"

// RM31xxx - Touch controllers
"^RM31[0-9]{3}[A-Z0-9-]*$"

// RM35xxx - Touch + display integrated
"^RM35[0-9]{3}[A-Z0-9-]*$"
```

### Package Code Extraction

```java
// Method 1: Check for hyphenated package (RM69091-COG)
int hyphenIndex = mpn.indexOf('-');
if (hyphenIndex > 0) {
    String suffix = mpn.substring(hyphenIndex + 1);
    if (PACKAGE_CODES.containsKey(suffix)) {
        return PACKAGE_CODES.get(suffix);
    }
}

// Method 2: Check for concatenated package (RM31100BGA)
// Base part is RMxxyyy (7 chars), package follows
if (mpn.length() > 7 && mpn.matches("^RM[0-9]{5}[A-Z]+.*$")) {
    String suffix = mpn.substring(7);
    for (String pkg : PACKAGE_CODES.keySet()) {
        if (suffix.startsWith(pkg)) {
            return PACKAGE_CODES.get(pkg);
        }
    }
}
```

### Series Extraction

Returns the first 4 characters (RM + 2 digits):
- RM68120 -> "RM68"
- RM69091 -> "RM69"
- RM31100 -> "RM31"
- RM35xxx -> "RM35"

---

## Product Type Determination

```java
public String getProductType(String mpn) {
    String series = extractSeries(mpn);
    return switch (series) {
        case "RM68" -> "TFT LCD Driver";
        case "RM69" -> "AMOLED Display Driver";
        case "RM31" -> "Touch Controller";
        case "RM35" -> "Touch + Display Controller";
        default -> "";
    };
}
```

---

## Related Files

- Handler: `manufacturers/RaydiumHandler.java`
- Component types: `IC`

---

## Common Use Cases

### Display Technology Selection

| Application | Recommended Series | Notes |
|-------------|-------------------|-------|
| TFT LCD panels | RM68xxx | Traditional LCD |
| AMOLED displays | RM69xxx | Premium OLED |
| Touchscreens | RM31xxx | Capacitive touch |
| Integrated touch display | RM35xxx | Combined solution |

### Smartphone/Wearable Displays

Raydium is a major supplier for smartphone and wearable display drivers:
- **RM69091**: Popular in smartwatch AMOLED displays
- **RM68120**: Used in smartphone TFT LCD modules
- **RM31100**: Touch controller for smartphone screens

---

## Replacement Considerations

### Same Base Part Replacements

Parts with the same model number but different packages are typically interchangeable from a functionality perspective (but require different PCB footprints):
- RM69091-COG == RM69091BGA (same driver, different package)

### Within-Series Compatibility

Parts within the same series (e.g., RM69xxx) are NOT necessarily compatible - they support different panel resolutions and specifications.

---

## Learnings & Edge Cases

- **COG/COF packages**: These are bare die packages designed for direct bonding to display panels. They require specialized assembly.
- **7-character base**: Raydium base part numbers are always RMxxxxx (7 characters) - RM + 5 digits.
- **No variant letters**: Unlike some manufacturers, Raydium typically doesn't use variant letters; differences are in the model number itself.
- **Display-specific**: Different RM69xxx parts support different panel resolutions - always verify against the target display panel datasheet.
- **Touch vs Display**: RM31 is touch only, RM35 is integrated touch+display, RM68/69 is display only.

<!-- Add new learnings above this line -->
