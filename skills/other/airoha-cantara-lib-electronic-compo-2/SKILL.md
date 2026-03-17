---
name: airoha
description: Airoha Technology (MediaTek subsidiary) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Airoha Bluetooth audio SoCs or AirohaHandler.
---

# Airoha Technology Manufacturer Skill

## Company Overview

Airoha Technology is a MediaTek subsidiary specializing in Bluetooth audio solutions for TWS (True Wireless Stereo) earbuds, ANC (Active Noise Cancellation) headphones, and premium audio applications.

## MPN Structure

Airoha MPNs follow this general structure:

```
[PREFIX][SERIES][MODEL][-PACKAGE]
   |       |       |       |
   |       |       |       +-- Optional: Package code (QFN, BGA, CSP)
   |       |       +-- Model variant (0-9)
   |       +-- Series number (55, 56, 57, 58)
   +-- AB15 prefix (Airoha Bluetooth 15xx)
```

### Example Decoding

```
AB1552
|  |||
|  ||+-- 2 = Model variant (basic TWS)
|  |+-- 5 = TWS earbud series
|  +-- 15 = Bluetooth 1.5 generation
+-- AB = Airoha Bluetooth

AB1562-QFN
|  ||| |
|  ||| +-- QFN = QFN package
|  ||+-- 2 = Model variant
|  |+-- 6 = ANC series
|  +-- 15 = Generation
+-- AB = Airoha Bluetooth

AB1575
|  |||
|  ||+-- 5 = Premium variant
|  |+-- 7 = Premium audio series
|  +-- 15 = Generation
+-- AB = Airoha Bluetooth
```

---

## Series Overview

| Series | Application | Features | Bluetooth |
|--------|-------------|----------|-----------|
| AB155x | TWS Earbuds | Basic TWS, low power | BT 5.0 |
| AB156x | ANC Earbuds | Active Noise Cancellation | BT 5.2 |
| AB157x | Premium Audio | Hi-Fi, low latency | BT 5.2 |
| AB158x | Ultra-Low Power | Extended battery life | BT 5.3 |

---

## Product Families

### AB155x Series - TWS Earbuds

| Part Number | Features | Bluetooth | Application |
|-------------|----------|-----------|-------------|
| AB1552 | Basic TWS | BT 5.0 | Entry-level earbuds |
| AB1558 | Enhanced TWS | BT 5.0 | Mid-range earbuds |

### AB156x Series - ANC Earbuds

| Part Number | Features | Bluetooth | ANC Type |
|-------------|----------|-----------|----------|
| AB1562 | Hybrid ANC | BT 5.2 | Feedforward + Feedback |
| AB1563 | Enhanced ANC | BT 5.2 | Advanced hybrid |
| AB1568 | Premium ANC | BT 5.2 | Multi-mic ANC |

### AB157x Series - Premium Audio

| Part Number | Features | Bluetooth | Audio |
|-------------|----------|-----------|-------|
| AB1570 | Hi-Fi audio | BT 5.2 | High-resolution |
| AB1575 | Premium codec | BT 5.2 | LDAC/aptX HD |

### AB158x Series - Ultra-Low Power

| Part Number | Features | Bluetooth | Power |
|-------------|----------|-----------|-------|
| AB1580 | Ultra-low power | BT 5.3 | Optimized for battery |
| AB1585 | Enhanced ULP | BT 5.3 | Extended standby |

---

## Package Codes

| Code | Package | Description |
|------|---------|-------------|
| QFN | QFN | Quad Flat No-lead |
| BGA | BGA | Ball Grid Array |
| CSP | CSP | Chip Scale Package |
| WLCSP | Wafer Level CSP | Ultra-small footprint |
| FCBGA | Flip-Chip BGA | High-density BGA |

---

## Bluetooth Version by Series

| Series | Default BT Version | LE Audio Support |
|--------|-------------------|------------------|
| AB155x | Bluetooth 5.0 | No |
| AB156x | Bluetooth 5.2 | Yes |
| AB157x | Bluetooth 5.2 | Yes |
| AB158x | Bluetooth 5.3 | Yes |

---

## Feature Comparison

| Feature | AB155x | AB156x | AB157x | AB158x |
|---------|--------|--------|--------|--------|
| TWS Support | Yes | Yes | Yes | Yes |
| ANC | No | Yes | Optional | Optional |
| Hi-Res Audio | No | No | Yes | Yes |
| Low Latency | Basic | Good | Excellent | Good |
| Power Efficiency | Good | Good | Moderate | Excellent |
| LE Audio | No | Yes | Yes | Yes |

---

## Handler Implementation Notes

### Pattern Matching

```java
// AB155x Series - TWS earbuds
"^AB155[0-9].*"

// AB156x Series - ANC earbuds
"^AB156[0-9].*"

// AB157x Series - Premium audio
"^AB157[0-9].*"

// AB158x Series - Ultra-low power
"^AB158[0-9].*"

// Generic pattern for all AB15xx
"^AB15[5-8][0-9].*"
```

### Package Code Extraction

```java
// Check for hyphenated suffix first
String[] parts = upperMpn.split("-");
if (parts.length > 1) {
    String suffix = parts[parts.length - 1];
    // Map: QFN, BGA, CSP, WLCSP, FCBGA
}

// Check for inline package indicators
if (upperMpn.contains("QFN")) return "QFN";
if (upperMpn.contains("BGA")) return "BGA";
```

### Series Extraction

```java
// Extract first 6 characters (e.g., AB1562)
// Validate matches AB15[5-8][0-9] pattern
if (result.matches("^AB15[5-8][0-9].*")) {
    return result.substring(0, 6);
}
```

### Bluetooth Version Inference

```java
// Infer BT version from series
if (mpn.startsWith("AB158")) return "5.3";
if (mpn.startsWith("AB157")) return "5.2";
if (mpn.startsWith("AB156")) return "5.2";
if (mpn.startsWith("AB155")) return "5.0";
```

---

## Replacement Compatibility

### Within-Series Replacements

Higher model numbers within a series can typically replace lower ones:
- AB1558 can replace AB1552 (more features)
- AB1568 can replace AB1562 (better ANC)

### Cross-Series Restrictions

Different series target different applications and are NOT interchangeable:
- AB156x (ANC) should NOT replace AB155x (basic TWS)
- AB157x (premium) should NOT replace AB155x (basic TWS)

### Feature Compatibility Rules

1. If target requires ANC, replacement must support ANC
2. If target requires premium audio, replacement must support it
3. Higher Bluetooth version can replace lower version

---

## Application Guidelines

| Use Case | Recommended Series |
|----------|-------------------|
| Budget TWS earbuds | AB155x |
| Mid-range ANC earbuds | AB156x |
| Premium headphones | AB157x |
| Long-battery earbuds | AB158x |

---

## Related Files

- Handler: `manufacturers/AirohaHandler.java`
- Component types: `IC`

---

## Learnings & Edge Cases

- **MediaTek subsidiary**: Airoha is owned by MediaTek, some parts may have MTK cross-references
- **Series determines features**: AB155x vs AB156x vs AB157x have fundamentally different capabilities
- **Package suffix optional**: Many MPNs don't include package code
- **Bluetooth version tied to series**: Cannot upgrade BT version without changing series
- **ANC compatibility critical**: Never substitute non-ANC for ANC-required applications
- **Model numbering**: Higher model number within series = more features/better performance

<!-- Add new learnings above this line -->
