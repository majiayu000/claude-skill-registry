---
name: artery
description: Artery Technology MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Artery AT32 MCUs (STM32-compatible ARM Cortex-M4) or ArteryHandler.
---

# Artery Technology Manufacturer Skill

## MPN Structure

Artery MCUs follow a structure similar to STM32:

```
AT32[FAMILY][SERIES][VARIANT][PIN][FLASH][PKG][TEMP]
│      │       │       │       │     │      │     │
│      │       │       │       │     │      │     └── Temperature (6/7)
│      │       │       │       │     │      └── Package (T=LQFP, U=QFN, H=BGA)
│      │       │       │       │     └── Flash size (4=16KB...M=4096KB)
│      │       │       │       └── Pin code (C=48, R=64, V=100, Z=144)
│      │       │       └── Optional variant (A, etc.)
│      │       └── Series number (403, 413, 415, 421, 435, etc.)
│      └── Family (F=MCU, WB=Wireless)
└── AT32 prefix
```

### Example Decoding

```
AT32F403AVCT7
│   │  │ ││││
│   │  │ │││└── Temp 7 (industrial extended, -40 to +105C)
│   │  │ ││└── Package T (LQFP)
│   │  │ │└── Flash C (256KB)
│   │  │ └── Pin V (100-pin)
│   │  └── Variant A
│   └── Series 403 (high performance)
└── F = MCU family

AT32WB415CCU6
│     │  │││
│     │  ││└── Temp 6 (industrial, -40 to +85C)
│     │  │└── Package U (QFN)
│     │  └── Flash C (256KB)
│     └── Pin C (48-pin)
└── WB415 = Wireless (Bluetooth LE)
```

---

## Package Codes

### Package Type (2nd from last character)

| Code | Package |
|------|---------|
| T | LQFP |
| U | QFN |
| H | BGA |

### Pin Count (4th from last character)

| Code | Pin Count |
|------|-----------|
| K | 32 |
| T | 36 |
| C | 48 |
| R | 64 |
| V | 100 |
| Z | 144 |
| I | 176 |

---

## Flash Size Encoding (3rd from last character)

| Code | Flash Size |
|------|------------|
| 4 | 16KB |
| 6 | 32KB |
| 8 | 64KB |
| B | 128KB |
| C | 256KB |
| D | 384KB |
| E | 512KB |
| G | 1024KB |
| M | 4096KB |

---

## Temperature Grades (last character)

| Code | Range | Description |
|------|-------|-------------|
| 6 | -40 to +85C | Industrial |
| 7 | -40 to +105C | Industrial Extended |

---

## Product Series

### High Performance (AT32F403, AT32F407)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| AT32F403 | Cortex-M4 | 240MHz | High performance, up to 1MB Flash |
| AT32F403A | Cortex-M4 | 240MHz | Enhanced AT32F403 |
| AT32F407 | Cortex-M4 | 240MHz | Ethernet + CAN |

### Mainstream (AT32F413, AT32F415)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| AT32F413 | Cortex-M4 | 200MHz | Mainstream, cost-effective |
| AT32F415 | Cortex-M4 | 150MHz | USB OTG support |

### Value Line (AT32F421, AT32F423, AT32F425)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| AT32F421 | Cortex-M4 | 120MHz | Entry-level |
| AT32F423 | Cortex-M4 | 150MHz | Enhanced value |
| AT32F425 | Cortex-M4 | 96MHz | USB device |

### High-Performance Plus (AT32F435, AT32F437)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| AT32F435 | Cortex-M4 | 288MHz | High-perf, up to 4MB Flash |
| AT32F437 | Cortex-M4 | 288MHz | High-perf + Ethernet |

### Wireless (AT32WB415)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| AT32WB415 | Cortex-M4 | 150MHz | Bluetooth LE 5.0 |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Package type is 2nd from last character
// AT32F403AVCT7 -> T = LQFP
char packageChar = upperMpn.charAt(upperMpn.length() - 2);
String packageType = MCU_PACKAGE_CODES.get(packageChar);

// Combine with pin count for full package name
int pinCount = extractMCUPinCount(upperMpn);
return packageType + pinCount;  // e.g., "LQFP100"
```

### Pin Count Extraction

```java
// Pin code is 4th from last character
// AT32F403AVCT7 -> V = 100 pins
char pinCode = upperMpn.charAt(upperMpn.length() - 4);
Integer pinCount = MCU_PIN_COUNTS.get(pinCode);
```

### Flash Size Extraction

```java
// Flash code is 3rd from last character
// AT32F403AVCT7 -> C = 256KB
char flashCode = upperMpn.charAt(upperMpn.length() - 3);
Integer flashSize = MCU_FLASH_SIZES.get(flashCode);
```

### Series Extraction

```java
// AT32WB must be checked before AT32F
if (upperMpn.startsWith("AT32WB415")) return "AT32WB415";

// Standard series extraction
if (upperMpn.startsWith("AT32F403")) return "AT32F403";
if (upperMpn.startsWith("AT32F407")) return "AT32F407";
// etc.
```

### Official Replacement Logic

```java
// Same series AND same pin count = valid replacement
// Flash size, package type, and temperature can differ

String series1 = extractSeries(mpn1);
String series2 = extractSeries(mpn2);
if (!series1.equals(series2)) return false;

int pins1 = extractMCUPinCount(mpn1);
int pins2 = extractMCUPinCount(mpn2);
return pins1 == pins2;
```

---

## Related Files

- Handler: `manufacturers/ArteryHandler.java`
- Component types: `MICROCONTROLLER`, `IC`

---

## STM32 Compatibility

Artery AT32 MCUs are designed as enhanced STM32-compatible alternatives:

| AT32 Series | STM32 Equivalent | Advantages |
|-------------|------------------|------------|
| AT32F403A | STM32F103 | Higher clock (240 vs 72MHz) |
| AT32F407 | STM32F107 | Higher clock, more Flash |
| AT32F413 | STM32F103 | Better price/performance |
| AT32F415 | STM32F105 | USB OTG compatible |
| AT32F421 | STM32F030 | Cortex-M4 vs M0 |
| AT32F435/437 | STM32F4xx | Up to 4MB Flash |

**Important**: While register-compatible for most peripherals, always verify critical functionality when migrating from STM32.

---

## Variant Suffixes

Some series have variant letters after the series number:

| Variant | Meaning |
|---------|---------|
| A | Enhanced version (e.g., AT32F403A) |
| (none) | Standard version |

---

## Learnings & Edge Cases

- **Position-based extraction**: Package at -2, flash at -3, pin at -4 from end
- **4MB Flash**: AT32F435/437 support M=4096KB, larger than most STM32
- **AT32WB prefix**: Wireless series uses WB instead of F in family position
- **240MHz+ clocks**: Artery MCUs often have higher clock speeds than equivalent STM32
- **Variant letter optional**: AT32F403 and AT32F403A are different series
- **Temperature 7 is extended**: Goes to +105C vs standard industrial +85C
- **STM32 migration**: Pin-compatible but verify peripheral registers for critical functions

<!-- Add new learnings above this line -->
