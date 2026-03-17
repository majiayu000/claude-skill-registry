---
name: harting
description: Harting industrial connector MPN encoding patterns, series decoding, and handler guidance. Use when working with Harting Han, M12, M8, har-bus, or har-flex connectors.
---

# Harting Manufacturer Skill

## Manufacturer Overview

Harting is a German manufacturer specializing in **industrial connectors** for harsh environments. Key product families include:

- **Han Series** - Heavy-duty industrial connectors (rectangular)
- **M12/M8** - Circular connectors for sensors and Ethernet
- **har-bus HM** - High-speed backplane connectors
- **har-link** - High-speed data connectors
- **har-flex** - Flexible PCB connectors

Harting connectors are widely used in factory automation, transportation, energy, and telecommunications.

---

## MPN Structure

Harting MPNs follow a structured **11-digit numeric format** with optional separators:

```
[SS] [VV] [PPP] [CCCC]
 |    |    |     |
 |    |    |     +-- Configuration code (4 digits): plating, orientation, etc.
 |    |    +-- Position/Pin code (3 digits): pin count or variant
 |    +-- Sub-series (2 digits): specific variant within series
 +-- Series (2 digits): product family identifier
```

### Format Variations

Harting MPNs can appear in several formats:

| Format | Example | Notes |
|--------|---------|-------|
| Spaced | `09 20 010 2611` | Official Harting format |
| Compact | `09200102611` | No separators |
| Hyphenated | `09-20-010-2611` | Alternative separator |

**All formats are equivalent and handled by the handler.**

---

## Series Codes

### Series Code Reference (First 4 Digits)

| Code | Series | Description | Typical Current |
|------|--------|-------------|-----------------|
| `0920` | Han A | Standard industrial signal | 16A |
| `0933` | Han E | Enhanced industrial signal | 16A |
| `0930` | Han B | High current industrial | 40A |
| `0921` | Han D | Compact industrial | 10A |
| `0938` | Han K | High power distribution | 200A |
| `0916` | Han K | High power (variant) | 200A |
| `0914` | Han-Modular | Modular connector system | 10A |
| `0902` | Han-Yellock | Push-pull circular | 10A |
| `0901` | har-link | High-speed data | 3A |
| `14xx` | har-flex | Flexible PCB | 1.5A |
| `15xx` | har-flex | Flexible PCB (variant) | 1.5A |
| `2103` | M12 | Industrial circular (sensor/Ethernet) | 4A |
| `2102` | M8 | Miniature circular (sensor) | 3A |
| `0200` | har-bus HM | High-speed backplane | 1A |
| `0201` | har-bus HM | Backplane (variant) | 1A |

---

## Example Decoding

### Han A/E Connector

```
09 20 010 2611
|  |  |   |
|  |  |   +-- 2611 = Configuration (gold plating, straight)
|  |  +-- 010 = 10-pin connector
|  +-- 20 = Han A series
+-- 09 = Han product family

Series: Han A
Pin Count: 10
Application: Industrial Signal
IP Rating: IP65
Current: 16A
```

### Han B High Current

```
09 30 016 0301
|  |  |   |
|  |  |   +-- 0301 = Configuration code
|  |  +-- 016 = 16-pin connector
|  +-- 30 = Han B series (high current)
+-- 09 = Han product family

Series: Han B
Pin Count: 16
Application: High Current Industrial
IP Rating: IP65
Current: 40A
```

### M12 Circular

```
21 03 311 1305
|  |  |   |
|  |  |   +-- 1305 = Configuration code
|  |  +-- 311 = Position/variant code (3-pin inferred)
|  +-- 03 = M12 series
+-- 21 = Circular connector family

Series: M12
Application: Industrial Sensor/Ethernet
IP Rating: IP67
Current: 4A
```

### har-bus HM Backplane

```
02 00 120 1101
|  |  |   |
|  |  |   +-- 1101 = Configuration code
|  |  +-- 120 = Position count (120 positions)
|  +-- 00 = har-bus HM series
+-- 02 = har-bus product family

Series: har-bus HM
Application: High-Speed Backplane
IP Rating: IP20 (indoor only)
Current: 1A
```

---

## Supported Component Types

The HartingHandler supports:

| ComponentType | Description |
|---------------|-------------|
| `CONNECTOR` | Primary type for all Harting products |
| `IC` | Secondary type (for cross-handler compatibility) |

---

## Configuration Code (Last 4 Digits)

The final 4 digits encode connector configuration details:

| Position | Meaning | Examples |
|----------|---------|----------|
| 1st digit | Plating type | Gold, silver, tin |
| 2nd digit | Contact orientation | Straight, angled |
| 3rd-4th digits | Variant/options | Gender, termination |

**Note**: Harting does not publish a complete public mapping of configuration codes. Use the configuration code primarily for exact part matching, not for extracting specifications.

---

## Helper Methods

The HartingHandler provides several utility methods:

### Series Detection

```java
handler.extractSeries("09 20 010 2611")  // Returns "Han A"
handler.extractSeries("09 33 024 2701")  // Returns "Han E"
handler.extractSeries("21 03 311 1305")  // Returns "M12"
```

### Classification Methods

```java
handler.isHanSeries("09 20 010 2611")       // true
handler.isCircularConnector("21 03 311 1305") // true (M12)
handler.isCircularConnector("21 02 151 0405") // true (M8)
handler.isHighSpeedConnector("02 00 120 1101") // true (har-bus HM)
handler.isPowerConnector("09 30 016 0301")     // true (Han B)
handler.isModularSystem("09 14 008 3001")      // true (Han-Modular)
```

### Specification Extraction

```java
handler.extractPinCount("09 20 010 2611")     // 10
handler.extractPackageCode("09 20 010 2611")  // "2611"
handler.getSeriesCode("09 20 010 2611")       // "0920"
handler.getFamily("09 20 010 2611")           // "Han A/E"
handler.getRatedCurrent("09 30 016 0301")     // 40.0 (Amperes)
handler.getIPRating("21 03 311 1305")         // "IP67"
handler.getApplicationType("09 30 016 0301")  // "High Current Industrial"
```

---

## Pin Count Extraction

The third group of 3 digits typically encodes the pin count:

| Position Code | Pin Count | Notes |
|---------------|-----------|-------|
| `010` | 10 | Direct mapping |
| `024` | 24 | Direct mapping |
| `016` | 16 | Direct mapping |
| `006` | 6 | Direct mapping |
| `003` | 3 | Direct mapping |
| `311` | 31 | First 2 digits (M12 variant) |

**Algorithm**: For codes < 100, the code equals pin count. For codes >= 100, divide by 10 to get approximate pin count.

---

## IP Ratings by Series

| Series | IP Rating | Environment |
|--------|-----------|-------------|
| Han A/E/B/D/K | IP65 | Industrial, splash-proof |
| Han-Modular | IP65 | Industrial, splash-proof |
| Han-Yellock | IP67 | Washdown, submersible |
| M12, M8 | IP67 | Washdown, submersible |
| har-bus HM | IP20 | Indoor/enclosure only |
| har-link | IP20 | Indoor/enclosure only |
| har-flex | IP20 | Indoor/enclosure only |

---

## Application Types

| Series | Application |
|--------|-------------|
| Han A, Han E | Industrial Signal |
| Han B | High Current Industrial |
| Han D | Compact Industrial |
| Han K | Power Distribution |
| Han-Modular | Modular Industrial |
| Han-Yellock | Push-Pull Circular |
| har-flex | Flexible PCB |
| M12 | Industrial Sensor/Ethernet |
| M8 | Miniature Sensor |
| har-bus HM | High-Speed Backplane |
| har-link | High-Speed Data Link |

---

## Replacement Logic

Two Harting connectors are considered compatible replacements when:

1. **Same series** (e.g., both Han A, or both M12)
2. **Same pin count** (third group of digits must match or infer same count)

```java
// Compatible - same series, same pins, different config
handler.isOfficialReplacement("09 20 010 2611", "09 20 010 2801")  // true

// Incompatible - different series
handler.isOfficialReplacement("09 20 010 2611", "09 33 010 2701")  // false (Han A vs Han E)

// Incompatible - different pin count
handler.isOfficialReplacement("09 20 010 2611", "09 20 016 2611")  // false (10-pin vs 16-pin)
```

---

## Related Files

- **Handler**: `manufacturers/HartingHandler.java`
- **Test**: `handlers/HartingHandlerTest.java`
- **Component Types**: `CONNECTOR`, `IC`

---

## Learnings & Edge Cases

### MPN Format Handling

- **Format tolerance**: Handler accepts spaces, hyphens, or no separators between digit groups
- **Normalization**: MPNs are uppercased and trimmed before processing
- **Pattern matching**: All 11 series-specific patterns are checked explicitly in `matches()`

### Han A vs Han E Distinction

```
0920 → Han A (first/original Han series)
0933 → Han E (enhanced version)
```

Both return "Han A/E" from `getFamily()` but return distinct series from `extractSeries()`.

### har-flex Special Case

har-flex connectors have a **9-digit format** instead of 11 digits:

```
14 010 1201   (9 digits, no sub-series)
15 020 1301   (9 digits, variant prefix)
```

The pattern `^(14|15)[- ]?([0-9]{3})[- ]?([0-9]{4})$` handles this shorter format.

### Pin Count Edge Cases

For M12/M8 circular connectors, the position code may encode variant information rather than direct pin count:

```
21 03 311 1305 → Position code 311 does NOT mean 311 pins
               → Algorithm: 311 / 10 = 31 pins (approximate)
```

For more accurate pin count on circular connectors, consult the datasheet.

### Configuration Code Not Decoded

Unlike some manufacturers, Harting's configuration code (last 4 digits) is **not publicly documented** in full detail. The handler extracts it for exact matching but does not decode plating, gender, or termination type.

### IC Type Support

The handler supports `ComponentType.IC` in addition to `CONNECTOR`. This is for **cross-handler compatibility** in generic searches, not because Harting makes ICs. All Harting products are connectors.

### Test Location

Tests are in `handlers/HartingHandlerTest.java` (not `manufacturers/` package) to avoid classpath shadowing issues described in CLAUDE.md.

<!-- Add new learnings above this line -->
