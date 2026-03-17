---
name: sitronix
description: Sitronix Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Sitronix display controllers or SitronixHandler.
---

# Sitronix Technology Manufacturer Skill

## MPN Structure

Sitronix MPNs follow this general structure:

```
[PREFIX][SERIES][MODEL][VARIANT][PACKAGE]
   |       |       |       |        |
   |       |       |       |        +-- Package suffix (S=SOP, V=LQFP, R=QFN)
   |       |       |       +-- Optional variant letter or revision
   |       |       +-- Model number (65, 89, 20, etc.)
   |       +-- Series digits (75, 77, 79, 16)
   +-- ST prefix (all Sitronix products)
```

### Example Decoding

```
ST7735S
|  |  ||
|  |  |+-- S = SOP package
|  |  +-- (no variant)
|  +-- 7735 = TFT display driver model
+-- ST = Sitronix prefix

ST7920-0B
|  |   |||
|  |   ||+-- B = COG package
|  |   |+-- 0 = revision/option
|  |   +-- hyphen separator
|  +-- 7920 = Graphic LCD controller
+-- ST = Sitronix prefix
```

---

## Product Families

### ST75xx Series - TFT LCD Controllers

| Part Number | Description | Resolution |
|-------------|-------------|------------|
| ST7565 | COG LCD controller | 128x64 |
| ST7567 | COG LCD controller | 128x64 |
| ST7571 | TFT LCD controller | 132x64 |
| ST7580 | TFT LCD controller | Variable |

### ST77xx Series - TFT Display Drivers

| Part Number | Description | Resolution |
|-------------|-------------|------------|
| ST7735 | 1.8" TFT driver | 128x160 |
| ST7735S | 1.8" TFT driver (SOP) | 128x160 |
| ST7789 | 2.0-2.4" TFT driver | 240x320 |
| ST7789V | ST7789 in LQFP | 240x320 |
| ST7796 | 3.5"+ TFT driver | 320x480 |

### ST79xx Series - Graphic LCD Controllers

| Part Number | Description | Features |
|-------------|-------------|----------|
| ST7920 | Graphic LCD controller | Chinese font ROM |
| ST7920-0B | ST7920 COG variant | Built-in fonts |

### ST16xx Series - LED Drivers

| Part Number | Description | Channels |
|-------------|-------------|----------|
| ST1628 | LED driver | Segment display |
| ST1633 | LED driver | Matrix display |

---

## Package Codes

### Single-Letter Suffixes

| Code | Package | Notes |
|------|---------|-------|
| S | SOP | Small outline package |
| V | LQFP | Low-profile QFP |
| R | QFN | Quad flat no-lead |
| B | COG | Chip-on-glass |

### Multi-Letter Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFP | QFP | Quad flat package |
| LQFP | LQFP | Low-profile QFP |
| COG | COG | Chip-on-glass |
| COF | COF | Chip-on-film |
| QFN | QFN | Quad flat no-lead |
| SOP | SOP | Small outline package |
| SSOP | SSOP | Shrink SOP |
| TSSOP | TSSOP | Thin shrink SOP |
| TQFP | TQFP | Thin QFP |
| BGA | BGA | Ball grid array |

---

## Naming Pattern Conflicts

### ST vs STMicroelectronics

**IMPORTANT**: Both Sitronix (Taiwan) and STMicroelectronics (Europe) use the "ST" prefix!

**Sitronix patterns**: ST followed by 2-digit series + 2-digit model
- ST75xx, ST77xx, ST79xx (display controllers)
- ST16xx (LED drivers)

**STMicroelectronics patterns**: STM prefix or different number patterns
- STM32Fxxx (microcontrollers)
- STM8xxx (8-bit MCUs)
- L78xx (voltage regulators)

**How to distinguish**:
```java
// Sitronix: ST + specific series numbers
"^ST(75|77|79|16)[0-9]{2}[A-Z0-9-]*$"

// STMicroelectronics: STM prefix or different patterns
"^STM[0-9].*"  // MCUs
"^L78[0-9]{2}.*"  // Regulators
```

---

## Handler Implementation Notes

### Pattern Matching

```java
// ST75xx - TFT LCD controllers
"^ST75[0-9]{2}[A-Z0-9-]*$"

// ST77xx - TFT display drivers
"^ST77[0-9]{2}[A-Z0-9-]*$"

// ST79xx - Graphic LCD controllers (includes ST7920)
"^ST79[0-9]{2}[A-Z0-9-]*$"

// ST16xx - LED drivers
"^ST16[0-9]{2}[A-Z0-9-]*$"
```

### Package Code Extraction

```java
// Step 1: Handle hyphenated suffixes (ST7920-0B)
int hyphen = mpn.indexOf('-');
String basePart = hyphen >= 0 ? mpn.substring(0, hyphen) : mpn;

// Step 2: Extract suffix from ST[0-9]{4}[letters]
Pattern packagePattern = Pattern.compile("^ST[0-9]{4}([A-Z]+)$");

// Step 3: Map single-letter codes
switch (code) {
    case "S": return "SOP";
    case "V": return "LQFP";
    case "R": return "QFN";
    case "B": return "COG";
}
```

### Series Extraction

Returns the first 4 characters (ST + 2 digits):
- ST7735S -> "ST77"
- ST7920 -> "ST79"
- ST1628 -> "ST16"

---

## Related Files

- Handler: `manufacturers/SitronixHandler.java`
- Component types: `IC`, `LED_DRIVER`

---

## Common Use Cases

### Embedded Display Projects

Sitronix controllers are widely used in:
- Arduino/Raspberry Pi displays: ST7735 (1.8" TFT), ST7789 (2.0" TFT)
- Character LCDs: ST7920 (128x64 with Chinese fonts)
- LED segment displays: ST1628

### Popular Development Modules

| Module | Controller | Resolution | Interface |
|--------|------------|------------|-----------|
| 1.8" TFT | ST7735 | 128x160 | SPI |
| 2.0" TFT | ST7789 | 240x320 | SPI |
| 2.4" TFT | ST7789V | 240x320 | SPI |
| 12864 LCD | ST7920 | 128x64 | Parallel/SPI |

---

## Learnings & Edge Cases

- **ST7735 vs ST7735S**: The "S" is the package code (SOP), not part of the model number.
- **ST7920 variants**: ST7920-0B has hyphenated option code; the "0" is a revision, "B" is COG package.
- **Sitronix vs STMicro**: Always check the number pattern - Sitronix uses ST[75|77|79|16]xx while STMicro uses STM[8|32] or other prefixes.
- **Display resolution**: The model number sometimes hints at resolution capability, but datasheet verification is required.
- **COG/COF packages**: These are bare die packages for direct bonding, common in display applications.

<!-- Add new learnings above this line -->
