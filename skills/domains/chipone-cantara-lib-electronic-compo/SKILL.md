---
name: chipone
description: Chipone Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Chipone LED driver components or ChiponeHandler.
---

# Chipone Technology Manufacturer Skill

## MPN Structure

Chipone MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][PACKAGE]
   |        |        |        |
   |        |        |        +-- Package suffix (SS=SSOP, S=SOP, Q=QFN)
   |        |        +-- Variant letter (B, C for improved versions)
   |        +-- Series number (2024, 2053, 2110, etc.)
   +-- Prefix: ICN or ICND (improved series)
```

### Example Decoding

```
ICN2053SS
|   |   ||
|   |   |+-- SS = SSOP package
|   |   +-- (no variant letter)
|   +-- 2053 = 16-channel LED driver with S-PWM
+-- ICN = Constant current LED driver prefix

ICND2110-S
|    |   ||
|    |   |+-- S = SOP package
|    |   +-- (hyphen separator)
|    +-- 2110 = 16-channel improved LED driver
+-- ICND = Improved series prefix
```

---

## Product Families

### ICN2xxx Series - Constant Current LED Drivers

| Part Number | Channels | Features |
|-------------|----------|----------|
| ICN2012 | 12 | Basic LED driver |
| ICN2018 | 18 | Basic LED driver |
| ICN2024 | 24 | 24-channel constant current |
| ICN2026 | 26 | 26-channel constant current |
| ICN2038 | 38 | 38-channel constant current |
| ICN2053 | 16 | S-PWM for high grayscale |
| ICN2065 | 16 | High refresh rate support |

### ICND2xxx Series - Improved LED Drivers

| Part Number | Channels | Features |
|-------------|----------|----------|
| ICND2025 | 24 | Improved ICN2024 replacement |
| ICND2053 | 16 | Improved ICN2053 replacement |
| ICND2110 | 16 | Enhanced 16-channel driver |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| SS | SSOP | Small outline shrink package |
| S | SOP | Small outline package |
| SOP | SOP | Explicit SOP |
| SSOP | SSOP | Explicit SSOP |
| Q | QFN | Quad flat no-lead |
| QFN | QFN | Explicit QFN |
| T | TSSOP | Thin shrink small outline |
| TSSOP | TSSOP | Explicit TSSOP |

### Package Suffix Positioning

Package codes appear in two ways:
1. **Inline**: Directly after the part number (ICN2053SS)
2. **Hyphenated**: After a hyphen (ICND2110-S)

---

## Variant Letters

| Letter | Meaning |
|--------|---------|
| B | Second revision |
| C | Third revision |
| (none) | Original revision |

Single letters like B, C after the part number typically indicate variant revisions, NOT packages.

**Example**: `ICN2065B` = ICN2065 revision B

---

## Official Replacements

The ICND2xxx series are drop-in replacements for the corresponding ICN2xxx parts:

| Original | Replacement | Notes |
|----------|-------------|-------|
| ICN2053 | ICND2053 | Pin-compatible, improved performance |
| ICN2024 | ICND2025 | Similar functionality |

Parts with the same base number in ICN vs ICND series are typically compatible.

---

## Handler Implementation Notes

### Pattern Matching

```java
// ICN2xxx patterns
"^ICN2[0-9]{3}[A-Z0-9-]*$"

// ICND2xxx patterns (improved series)
"^ICND2[0-9]{3}[A-Z0-9-]*$"
```

### Package Code Extraction

```java
// Step 1: Check for hyphenated suffix first
// ICND2110-S -> S -> SOP

// Step 2: Check for inline suffix
// ICN2053SS -> SS -> SSOP

// Step 3: Skip single variant letters
// ICN2065B -> B is variant, not package -> return ""
```

### Series Extraction

```java
// ICND2xxx -> "ICND2"
// ICN2xxx -> "ICN2"
```

---

## Related Files

- Handler: `manufacturers/ChiponeHandler.java`
- Component types: `IC`, `LED_DRIVER`

---

## Common Use Cases

### LED Display Panels

Chipone drivers are commonly used in LED display panels and signage:
- Indoor LED screens: ICN2053, ICND2053 (high grayscale)
- Outdoor LED screens: ICN2024, ICN2038 (high channel count)
- High refresh displays: ICN2065 (high refresh rate)

### BOM Matching

When matching BOMs, consider these equivalents:
```
ICN2053 == ICND2053 (drop-in replacement)
ICN2053SS == ICN2053-SSOP (same package, different notation)
```

---

## Learnings & Edge Cases

- **Variant vs Package**: Single letters after the part number (B, C) are variants, not packages. Multi-letter suffixes (SS, QFN) are packages.
- **ICND prefix**: The "D" in ICND stands for an improved/digital version, not a package code.
- **Channel count from part number**: The last 2-3 digits sometimes indicate channel count (2024 = 24ch, 2012 = 12ch), but this is not universal.
- **Tape and reel**: -TR suffix indicates tape and reel packaging, should be stripped before package extraction.

<!-- Add new learnings above this line -->
