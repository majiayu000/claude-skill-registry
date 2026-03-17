---
name: millmax
description: Mill-Max precision connectors MPN encoding patterns, series decoding, and handler guidance. Use when working with Mill-Max components or MillMaxHandler.
---

# Mill-Max Manufacturing Manufacturer Skill

## MPN Structure

Mill-Max MPNs follow a dash-separated numeric structure:

```
[SERIES]-[FIELD1]-[FIELD2]-[FIELD3]-[FIELD4][-FIELD5][-FIELD6][-FIELD7]
   |        |        |        |        |
   |        |        |        |        +-- Additional specification fields
   |        |        |        +-- Specification field
   |        |        +-- Specification field (often pin count)
   |        +-- Specification field
   +-- 3-4 digit series number
```

### Example Decoding

```
0906-0-15-20-75-14-11-0
|    | |  |  |  |  |  |
|    | |  |  |  |  |  +-- Plating option
|    | |  |  |  |  +-- Contact material
|    | |  |  |  +-- Force specification
|    | |  |  +-- Stroke specification
|    | |  +-- Force specification
|    | +-- Travel specification
|    +-- Type variant
+-- 0906 = Spring-loaded contact series

310-93-108-41-001000
|   |  |   |  |
|   |  |   |  +-- Additional options
|   |  |   +-- Row configuration
|   |  +-- Pin count (108 pins)
|   +-- Profile specification
+-- 310 = Header series
```

---

## Series Families

### Spring-Loaded Contacts (Pogo Pins)

| Series | Mounting | Application | Pattern |
|--------|----------|-------------|---------|
| 0906 | THT | Test/Programming | `^0906-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]$` |
| 0907 | SMT | Test/Programming | `^0907-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]$` |
| 0908 | THT | Test/Programming | `^0908-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]$` |
| 0965 | SMT | Battery Contact | `^096[0-9]-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]$` |
| 0985 | SMT | Board-to-Board Spring | `^098[0-9]-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]+-[0-9]$` |

### IC Sockets

| Series | Mounting | Application | Pattern |
|--------|----------|-------------|---------|
| 110 | THT | DIP IC Socket | `^110-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 510 | SMT | PLCC Socket | `^510-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 610 | THT | PGA Socket | `^610-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |

### Board-to-Board Connectors

| Series | Mounting | Application | Pattern |
|--------|----------|-------------|---------|
| 850 | THT | High Density B2B | `^850-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 851 | SMT | High Density B2B SMT | `^851-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 852 | THT | High Density B2B | `^852-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |

### Headers

| Series | Mounting | Type | Pattern |
|--------|----------|------|---------|
| 300 | THT | Pin Header | `^300-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 310 | THT | Pin Header | `^310-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 311 | SMT | Pin Header | `^311-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 315 | SMT | SMT Header | `^315-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 316 | SMT | SMT Header | `^316-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |

### Receptacles

| Series | Mounting | Type | Pattern |
|--------|----------|------|---------|
| 800 | THT | Pin Receptacle | `^800-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |
| 801 | SMT | Pin Receptacle SMT | `^801-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |

### Single Row Sockets

| Series | Mounting | Type | Pattern |
|--------|----------|------|---------|
| 350 | THT | Single Row Socket | `^350-[0-9]+-[0-9]+-[0-9]+-[0-9]+$` |

---

## Mounting Type Detection

```
THT Series: 0906, 0908, 110, 610, 850, 852, 300, 310, 800, 350
SMT Series: 0907, 0965, 0985, 510, 851, 311, 315, 316, 801
```

Mill-Max uses the series number to indicate mounting type. This is different from most other manufacturers where mounting is encoded as a suffix.

---

## Pin Count Extraction

For headers and receptacles, pin count is typically in the third field:

```java
// Example: 310-93-108-41-001000
// Pin count = 108 (third field after series)

String[] parts = mpn.split("-");
if (parts.length >= 3) {
    int pinCount = Integer.parseInt(parts[2]);
}
```

---

## Spring Pin Compatibility

Spring pins are compatible replacements when:
1. Same series number (e.g., both 0906)
2. Same travel specification (group 3)
3. Same force specification (groups 4-5)
4. Same stroke specification

```
0906-0-15-20-75-14-11-0  vs  0906-0-15-20-75-14-11-1
     ^  ^  ^               ^  ^  ^
     Same travel/force/stroke = Compatible (different plating)
```

---

## Handler Implementation Notes

### Series Extraction

```java
// Mill-Max series is always the first field before the dash
// Example: 0906-0-15-20-75-14-11-0 -> series = "0906"

int firstDash = mpn.indexOf('-');
if (firstDash > 0) {
    String series = mpn.substring(0, firstDash);
    // Validate: should be 3-4 digits
    if (series.matches("[0-9]{3,4}")) {
        return series;
    }
}
```

### Package Code Extraction

```java
// For Mill-Max, "package code" is effectively the mounting type
// Determined by series number, not a suffix

String series = extractSeries(mpn);
if (SERIES_MOUNTING.containsKey(series)) {
    return SERIES_MOUNTING.get(series);  // Returns "THT" or "SMT"
}
```

### Generic Pattern Matching

```java
// Mill-Max MPNs are ALL numeric with dashes
// General pattern: 3-4 digit series, followed by dash-separated numbers
Pattern GENERIC_PATTERN = Pattern.compile(
    "^([0-9]{3,4})-[0-9]+-[0-9]+-[0-9]+-[0-9]+.*$"
);
```

---

## Component Types

Mill-Max products map to these ComponentTypes:
- `CONNECTOR` - All header, receptacle, B2B, spring pin products
- `IC` - IC socket products (110, 510, 610 series)

Note: IC sockets register under BOTH `CONNECTOR` and `IC` types.

---

## Related Files

- Handler: `manufacturers/MillMaxHandler.java`
- Supported types: `CONNECTOR`, `IC`
- No manufacturer-specific ComponentType enum entries

---

## Learnings & Edge Cases

- **Numeric-only MPNs**: Unlike most manufacturers, Mill-Max MPNs are entirely numeric with dashes. No letters.
- **Series determines mounting**: The series number indicates THT vs SMT, not a suffix code.
- **IC sockets are dual-typed**: 110/510/610 series register as both CONNECTOR and IC types.
- **8-field spring pins**: Spring-loaded pins have the most complex structure with 8 dash-separated fields.
- **Pin count location varies**: For spring pins, pin count is not directly extractable. For headers, it's the third field.
- **No package code suffix**: Mill-Max does not use package code suffixes like other manufacturers.

<!-- Add new learnings above this line -->
