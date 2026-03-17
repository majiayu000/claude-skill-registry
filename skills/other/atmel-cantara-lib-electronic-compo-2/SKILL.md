---
name: atmel
description: Atmel/Microchip AVR MPN encoding patterns, suffix decoding, and handler guidance. Use when working with ATmega, ATtiny, SAM, or other Atmel components.
---

# Atmel (now Microchip) Manufacturer Skill

## MPN Structure

Atmel MPNs follow this general structure:

```
[FAMILY][SERIES][VARIANT]-[PACKAGE][TEMP]
   │       │        │         │      │
   │       │        │         │      └── Optional temperature grade
   │       │        │         └── Package code (after hyphen)
   │       │        └── Feature variant (P=picopower, A=automotive, etc.)
   │       └── Series number (flash size, pin count encoded)
   └── Product family (ATMEGA, ATTINY, ATSAM, etc.)
```

### Example Decoding

```
ATMEGA328P-PU
│     │  │  ││
│     │  │  │└── (no temp suffix = commercial)
│     │  │  └── U in PU = standard grade
│     │  └── P = picoPower technology
│     └── 328 = 32KB flash, 8-bit
└── ATMEGA = AVR 8-bit megaAVR family

ATSAM3X8E-AU
│    │ ││  ││
│    │ ││  │└── U = standard grade
│    │ ││  └── A = TQFP package
│    │ │└── E = Ethernet variant
│    │ └── 8 = 512KB flash
│    └── 3X = Cortex-M3 SAM3X series
└── ATSAM = ARM-based SAM family
```

---

## Package Codes (After Hyphen)

| Code | Package | Description |
|------|---------|-------------|
| **PU** | PDIP | Plastic Dual In-line Package (through-hole) |
| **AU** | TQFP | Thin Quad Flat Pack (surface mount) |
| **MU** | QFN/MLF | Quad Flat No-leads / Micro Lead Frame |
| **SU** | SOIC | Small Outline IC |
| **XU** | TSSOP | Thin Shrink Small Outline Package |
| **TU** | QFP | Quad Flat Pack (larger than TQFP) |
| **CU** | WLCSP/UCSP | Wafer Level / Ultra Chip Scale Package |
| **SS** | SSOP | Shrink Small Outline Package |

### Package Code Pattern

```
[PACKAGE_TYPE][GRADE]
      │          │
      │          └── U = Standard, C = Commercial, I = Industrial
      └── P=PDIP, A=TQFP, M=QFN, S=SOIC, X=TSSOP, T=QFP, C=WLCSP
```

---

## Product Families

### 8-bit AVR Microcontrollers

| Family | Description | Example |
|--------|-------------|---------|
| **ATmega** | Feature-rich 8-bit | ATMEGA328P, ATMEGA2560 |
| **ATtiny** | Small footprint 8-bit | ATTINY85, ATTINY13A |
| **AT90** | USB/CAN enabled | AT90USB162, AT90CAN128 |
| **ATxmega** | Extended 8/16-bit | ATXMEGA128A1U |

### 32-bit ARM Microcontrollers

| Family | Core | Example |
|--------|------|---------|
| **ATSAM3** | Cortex-M3 | ATSAM3X8E (Arduino Due) |
| **ATSAM4** | Cortex-M4 | ATSAM4S16B |
| **ATSAMD** | Cortex-M0+ | ATSAMD21G18A |
| **ATSAME** | Cortex-M7 | ATSAME70Q21 |

### Memory Products

| Family | Type | Example |
|--------|------|---------|
| **AT24C** | I2C EEPROM | AT24C256-PU (256Kbit) |
| **AT25** | SPI EEPROM/Flash | AT25SF041 (4Mbit Flash) |
| **AT45DB** | DataFlash | AT45DB321E |

### Security/Touch Products

| Family | Type | Example |
|--------|------|---------|
| **ATECC** | Crypto Authentication | ATECC608A |
| **ATSHA** | SHA Authentication | ATSHA204A |
| **AT42QT** | QTouch Controller | AT42QT1010 |
| **ATMXT** | maXTouch Controller | ATMXT336S |

---

## Series Number Encoding

### ATmega Series Numbers

The number encodes flash size and sometimes pin count:

| Series | Flash | SRAM | EEPROM | Notes |
|--------|-------|------|--------|-------|
| ATMEGA8 | 8KB | 1KB | 512B | Original |
| ATMEGA88 | 8KB | 1KB | 512B | Improved |
| ATMEGA168 | 16KB | 1KB | 512B | Pin-compatible with 88 |
| ATMEGA328 | 32KB | 2KB | 1KB | Arduino Uno |
| ATMEGA1284 | 128KB | 16KB | 4KB | High memory |
| ATMEGA2560 | 256KB | 8KB | 4KB | Arduino Mega |

### ATtiny Series Numbers

| Series | Flash | Pins | Notes |
|--------|-------|------|-------|
| ATTINY13 | 1KB | 8 | Smallest |
| ATTINY25 | 2KB | 8 | |
| ATTINY45 | 4KB | 8 | |
| ATTINY85 | 8KB | 8 | Popular small MCU |
| ATTINY84 | 8KB | 14 | More I/O |
| ATTINY2313 | 2KB | 20 | UART included |

---

## Variant Suffixes (Before Hyphen)

| Suffix | Meaning |
|--------|---------|
| **P** | picoPower - Ultra low power modes |
| **A** | Revision A / Automotive grade |
| **V** | Low voltage operation (1.8V-5.5V) |
| **PA** | picoPower + Automotive |
| **PB** | picoPower revision B |
| **U** | USB capable |
| **L** | Low voltage (1.8V-3.6V only) |

### Example Variants

```
ATMEGA328    → Original
ATMEGA328P   → picoPower (lower sleep current)
ATMEGA328PB  → picoPower revision B (more features)
ATMEGA328PA  → Automotive grade picoPower
```

---

## Temperature Grades

| Grade | Range | Suffix Position |
|-------|-------|-----------------|
| Commercial | 0°C to +70°C | (no suffix) |
| Industrial | -40°C to +85°C | Often implicit |
| Automotive | -40°C to +125°C | A in variant or separate |

---

## Common Arduino Mappings

| Arduino Board | MCU | Full MPN |
|---------------|-----|----------|
| Uno | ATmega328P | ATMEGA328P-PU |
| Nano | ATmega328P | ATMEGA328P-AU |
| Mega 2560 | ATmega2560 | ATMEGA2560-16AU |
| Leonardo | ATmega32U4 | ATMEGA32U4-AU |
| Due | ATSAM3X8E | ATSAM3X8E-AU |
| Zero | ATSAMD21G18A | ATSAMD21G18A-AU |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Atmel package codes are AFTER the hyphen
// ATMEGA328P-PU → package = "PU"

String[] parts = mpn.split("-");
if (parts.length > 1) {
    String suffix = parts[parts.length - 1];
    return switch (suffix) {
        case "PU" -> "PDIP";
        case "AU" -> "TQFP";
        case "MU" -> "QFN/MLF";
        case "SU" -> "SOIC";
        case "XU" -> "TSSOP";
        case "TU" -> "QFP";
        case "CU" -> "WLCSP";
        default -> suffix;
    };
}
```

### Series Extraction

```java
// Extract family + number, stop at variant letter or hyphen
// ATMEGA328P-PU → series = "ATMEGA328"
// ATTINY85-20PU → series = "ATTINY85"

if (mpn.startsWith("ATMEGA")) {
    // Find end of digits after "ATMEGA"
    int end = "ATMEGA".length();
    while (end < mpn.length() && Character.isDigit(mpn.charAt(end))) {
        end++;
    }
    return mpn.substring(0, end);
}
```

### Pattern Matching

```java
// ATmega: ATMEGA + digits + optional letter variant + optional -package
"^ATMEGA[0-9]+[A-Z]?(?:-[A-Z]{2,4})?$"

// ATtiny: ATTINY + digits + optional variant + optional -package
"^ATTINY[0-9]+[A-Z]?(?:-[A-Z]{2,4})?$"

// SAM: ATSAM + series + variant + -package
"^ATSAM[A-Z0-9]+(?:-[A-Z]{2,4})?$"
```

---

## Pin Compatibility Groups

### 28-pin PDIP/TQFP Compatible

- ATMEGA8 / ATMEGA88 / ATMEGA168 / ATMEGA328
- Direct drop-in replacements (different flash sizes)

### 8-pin DIP/SOIC Compatible

- ATTINY13 / ATTINY25 / ATTINY45 / ATTINY85
- Increasing flash sizes, same pinout

### 44-pin TQFP Compatible

- ATMEGA16 / ATMEGA32 / ATMEGA644 / ATMEGA1284

---

## Related Files

- Handler: `manufacturers/AtmelHandler.java`
- Component types: `MICROCONTROLLER_ATMEL`, `MCU_ATMEL`, `MEMORY_ATMEL`, `TOUCH_ATMEL`, `CRYPTO_ATMEL`
- Package registry: `PackageCodeRegistry.java` (Atmel-specific codes: PU, AU, MU, SU, XU, CU)

---

## Learnings & Edge Cases

- **Microchip acquisition**: Atmel was acquired by Microchip in 2016. New parts may have Microchip branding but same MPN structure
- **Speed grades**: Some parts have speed suffix before package (e.g., ATMEGA328P-20AU = 20MHz max)
- **PU vs AU**: Same chip, different package. PU=DIP for prototyping, AU=TQFP for production
- **P suffix importance**: ATMEGA328 and ATMEGA328P are different! The P version has lower power consumption
- **Memory in name**: ATmega328 has 32KB flash (32), ATtiny85 has 8KB (8), but encoding isn't always consistent

## Handler Cleanup Notes (TODO)

AtmelHandler needs the same cleanup as TIHandler (PR #77):
- [ ] Replace `HashSet` with `Set.of()` in `getSupportedTypes()`
- [ ] Handler doesn't use `PackageCodeRegistry` - has local switch statement
- [ ] Pattern may not handle speed grades like `-20AU` (20MHz before package)
- [ ] Case sensitivity - some methods use `mpn.startsWith()` without `toUpperCase()`

## Test Notes

When creating AtmelHandlerTest:
- Put in `no.cantara.electronic.component.lib.handlers` package (NOT `manufacturers`)
- Use `@BeforeAll` with `MPNUtils.getManufacturerHandler("ATMEGA328P")`
- Test categories: ATmega, ATtiny, AT90, XMEGA, SAM, Memory (AT24C, AT25), Touch (AT42QT), Crypto (ATECC, ATSHA)

<!-- Add new learnings above this line -->
