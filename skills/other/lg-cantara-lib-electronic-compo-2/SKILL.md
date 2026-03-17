---
name: lg
description: LG Innotek MPN encoding patterns, LED suffix decoding, and handler guidance. Use when working with LG LEDs, camera modules, automotive components, or LGHandler.
---

# LG Innotek Manufacturer Skill

## Manufacturer Overview

LG Innotek is a subsidiary of LG Corporation and a major manufacturer of electronic components, specializing in:

- **LEDs** - Standard, high-brightness, automotive, and display backlighting LEDs
- **Camera Modules** - Smartphone camera modules, automotive cameras, iris recognition
- **Automotive Components** - LED headlights, sensors, communication modules
- **Display Components** - Backlight units (BLUs), touch windows
- **Substrate Materials** - FC-BGA substrates, HDI boards

LG Innotek is particularly known for their high-quality LED products used in automotive lighting, display backlighting, and general illumination applications.

---

## MPN Structure

LG Innotek LED MPNs follow this general structure:

```
LG [SERIES][VARIANT][-SUFFIX]
|   |       |         |
|   |       |         +-- Package/variant suffix (KN, etc.)
|   |       +-- Variant code (color, specs)
|   +-- Series identifier (R971 = LED series)
+-- LG manufacturer prefix (note: space after LG)
```

### Key Pattern Characteristics

- **Space separator**: LG MPNs typically have a space after "LG" prefix
- **R-series LEDs**: Common format is `LG R####` where # are digits
- **Optional suffix**: Package codes follow a hyphen (e.g., `-KN`)

---

## Example Decoding

```
LG R971-KN
|  |    |
|  |    +-- KN = Package/variant suffix
|  +-- R971 = LED series number
+-- LG = Manufacturer prefix

LG R971
|  |
|  +-- R971 = LED series number (base part)
+-- LG = Manufacturer prefix
```

---

## Supported Component Types

From `LGHandler.getSupportedTypes()`:

| ComponentType | Description |
|---------------|-------------|
| `LED` | All LED products (standard, SMD, high-brightness, automotive) |

**Note**: The handler currently only supports the `LED` component type. LG Innotek also manufactures camera modules and other components, but these are not yet implemented in the handler.

---

## Package Code Extraction Rules

The handler extracts package codes from the suffix after a hyphen:

```java
// Format: LG [SERIES]-[PACKAGE]
// Example: LG R971-KN -> Package code: KN

// Rules:
// 1. Find the hyphen in the MPN
// 2. Extract everything after the hyphen
// 3. Return empty string if no hyphen present
```

### Common Package Suffixes

| Suffix | Likely Package | Notes |
|--------|----------------|-------|
| KN | SMD package | Common LED package variant |
| (none) | Standard | Base part without package specifier |

**Note**: LG Innotek's full package code documentation is not publicly detailed in the handler. The current implementation extracts whatever follows the hyphen as the package code.

---

## Series Extraction Rules

The handler extracts series from the base part before any suffix:

```java
// Format: LG [SERIES][-SUFFIX]
// Example: LG R971-KN -> Series: LG R971
// Example: LG R971 -> Series: LG R971

// Rules:
// 1. Split MPN by whitespace
// 2. Take the second part (after "LG")
// 3. Remove any hyphenated suffix
// 4. Prepend "LG " to form full series name
```

### Series Pattern

| Pattern | Example | Series Extracted |
|---------|---------|------------------|
| `LG RXXXX` | LG R971 | LG R971 |
| `LG RXXXX-XX` | LG R971-KN | LG R971 |

---

## Example MPNs with Explanations

### Standard LED

```
LG R971
  - Manufacturer: LG Innotek
  - Type: LED
  - Series: LG R971
  - Package: (not specified - base part)

LG R971-KN
  - Manufacturer: LG Innotek
  - Type: LED
  - Series: LG R971
  - Package: KN variant
```

### Replacement Logic

Parts with the same series but different or no suffix are considered replacements:

```
LG R971 and LG R971-KN
  - Same series: LG R971
  - isOfficialReplacement() returns: TRUE

LG R971-KN and LG R972-KN
  - Different series: LG R971 vs LG R972
  - isOfficialReplacement() returns: FALSE
```

---

## Handler Implementation Notes

### Pattern Matching

The handler uses two patterns for LED detection:

```java
// Basic LED pattern with optional suffix
"^LG\\s+R\\d+.*"

// LED pattern with explicit optional suffix group
"^LG\\s+R\\d+(-[A-Z]+)?$"
```

**Pattern Breakdown:**
- `^LG\\s+` - Must start with "LG" followed by whitespace
- `R\\d+` - "R" followed by one or more digits
- `.*` or `(-[A-Z]+)?` - Optional suffix (with or without hyphen)

### Package Code Extraction

```java
public String extractPackageCode(String mpn) {
    // Returns everything after the first hyphen
    // "LG R971-KN" -> "KN"
    // "LG R971" -> ""
    int dashIndex = mpn.indexOf('-');
    if (dashIndex > 0 && dashIndex < mpn.length() - 1) {
        return mpn.substring(dashIndex + 1);
    }
    return "";
}
```

### Series Extraction

```java
public String extractSeries(String mpn) {
    // Split by whitespace, take part after "LG"
    // Remove any hyphenated suffix
    String[] parts = mpn.split("\\s+");
    if (parts.length > 1) {
        String basePart = parts[1];
        int dashIndex = basePart.indexOf('-');
        if (dashIndex > 0) {
            return "LG " + basePart.substring(0, dashIndex);
        }
        return "LG " + basePart;
    }
    return "";
}
```

### Replacement Detection

```java
public boolean isOfficialReplacement(String mpn1, String mpn2) {
    // Same series = official replacement
    String series1 = extractSeries(mpn1);
    String series2 = extractSeries(mpn2);
    return !series1.isEmpty() && series1.equals(series2);
}
```

---

## Related Files

- Handler: `manufacturers/LGHandler.java`
- Component types: `LED`
- Test file: `handlers/LGHandlerTest.java` (to be created)

---

## Known Handler Limitations

The current `LGHandler` has several limitations that may need addressing:

| Issue | Severity | Description |
|-------|----------|-------------|
| HashSet in getSupportedTypes() | MEDIUM | Uses mutable HashSet instead of Set.of() |
| Limited pattern support | LOW | Only covers `LG R####` LED pattern |
| No camera module support | LOW | LG Innotek camera modules not implemented |
| No automotive component support | LOW | Automotive LEDs/sensors not implemented |
| Basic package extraction | LOW | Does not decode package codes to standard names |

### Recommended Improvements

1. **Change to Set.of()**: Replace `HashSet` with immutable `Set.of(ComponentType.LED)`
2. **Add more LED patterns**: Support additional LG LED series beyond R-series
3. **Add camera module support**: LG Innotek is a major camera module manufacturer
4. **Decode package codes**: Map suffixes like `-KN` to standard package names

---

## Learnings & Quirks

### MPN Format

- **Space is significant**: LG MPNs use a space between "LG" and the series (not a hyphen or underscore)
- **R-prefix LEDs**: The R-prefix indicates LED products in LG Innotek's naming scheme
- **Simple pattern**: LG Innotek uses relatively simple MPN structures compared to other manufacturers
- **Hyphen separator**: Package/variant codes are separated by hyphen from base part number

### Pattern Matching

- **Whitespace handling**: Pattern uses `\\s+` to handle variable whitespace
- **Case sensitivity**: Handler currently assumes uppercase MPNs in patterns
- **Suffix optionality**: Both patterns allow for missing suffix (base part number)

### Replacement Logic

- **Series-based matching**: Two parts are replacements if they share the same series
- **Suffix ignored for replacement**: Different package variants of same series are considered interchangeable
- **Empty series handling**: Returns false if series extraction fails for either part

### Handler Architecture

- **No manufacturer-specific types**: Unlike TI or ST, LG handler uses generic `LED` type
- **getManufacturerTypes() empty**: Returns empty set, no LG-specific component types defined
- **Simple implementation**: Handler is minimal compared to other manufacturers

### Testing Considerations

- **Test with space**: Remember to include space in test MPNs: `"LG R971"` not `"LGR971"`
- **Test empty suffix**: Both `"LG R971"` and `"LG R971-KN"` should extract same series
- **Test replacement symmetry**: `isOfficialReplacement(a, b)` should equal `isOfficialReplacement(b, a)`

<!-- Add new learnings above this line -->
