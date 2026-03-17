---
name: wch
description: WCH (Nanjing Qinheng Microelectronics) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with WCH RISC-V MCUs, USB interface chips, or WCHHandler.
---

# WCH (Nanjing Qinheng) Manufacturer Skill

## MPN Structure

WCH has two main product categories with different structures:

### RISC-V and ARM MCUs (CH32 Series)

```
CH32[CORE][SERIES][PIN][FLASH][PKG][TEMP]
│     │      │     │     │     │     │
│     │      │     │     │     │     └── Temperature (6=industrial)
│     │      │     │     │     └── Package type (T=LQFP, U=QFN)
│     │      │     │     └── Flash size (4=16KB, 8=64KB, B=128KB, C=256KB)
│     │      │     └── Pin code (C=48, R=64, V=100)
│     │      └── Series (003=entry, 103=standard, 203=enhanced, 30x=high-perf)
│     └── Core (V=RISC-V, F=ARM Cortex-M3)
└── CH32 prefix
```

### USB Interface Chips (CH34x Series)

```
CH[SERIES][VARIANT]
│    │       │
│    │       └── Package variant (G=SOP-16, C=SOP-16 w/crystal, K=ESSOP-10)
│    └── Series (340=USB-UART, 341=USB-Multi, 9340=Enhanced)
└── CH prefix
```

### Example Decoding

```
CH32V103C8T6
│   │  │ │││
│   │  │ ││└── Temp 6 (industrial)
│   │  │ │└── Package T (LQFP)
│   │  │ └── Flash 8 (64KB)
│   │  └── Pin C (48-pin)
│   └── Series 103 (QingKe V3A core)
└── Core V (RISC-V)

CH340G
│  │ │
│  │ └── Package G (SOP-16)
│  └── Series 340 (USB to UART)
└── CH prefix
```

---

## Package Codes

### MCU Pin Codes

| Code | Package | Pin Count |
|------|---------|-----------|
| A | QFN-28 | 28 |
| C | LQFP-48 | 48 |
| F | TSSOP-20 | 20 |
| G | QFN-20 | 20 |
| J | SOP-20 | 20 |
| K | ESSOP-20 | 20 |
| N | SOP-8 | 8 |
| R | LQFP-64 | 64 |
| U | QFN-20 | 20 |
| V | LQFP-100 | 100 |
| W | QFN-28 | 28 |

### USB Interface Chip Packages

| Suffix | Package |
|--------|---------|
| G | SOP-16 |
| C | SOP-16 (integrated crystal) |
| K | ESSOP-10 |
| N | SOP-8 |
| E | MSOP-10 |
| X | ESSOP-10 |
| T | SSOP-20 |
| A | SOP-28 |
| B | SSOP-28 |
| S | SOP-28 |
| H | SOP-28 |
| L | LQFP-48 |

---

## Product Families

### RISC-V MCUs (CH32Vxxx)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| CH32V003 | QingKe V2A | 48MHz | Entry-level, 2KB SRAM |
| CH32V103 | QingKe V3A | 80MHz | Standard, 20KB SRAM |
| CH32V203 | QingKe V4B | 144MHz | Enhanced, 64KB SRAM |
| CH32V208 | QingKe V4C | 144MHz | Bluetooth LE support |
| CH32V303 | QingKe V4F | 144MHz | High-performance |
| CH32V305 | QingKe V4F | 144MHz | USB HS, Ethernet |
| CH32V307 | QingKe V4F | 144MHz | USB HS, Ethernet, CAN |

### ARM Cortex-M3 MCUs (CH32Fxxx)

| Series | Core | Clock | Features |
|--------|------|-------|----------|
| CH32F103 | Cortex-M3 | 72MHz | STM32F103 compatible |
| CH32F203 | Cortex-M3 | 144MHz | Enhanced peripherals |

### USB Interface Chips

| Series | Type | Features |
|--------|------|----------|
| CH340 | USB-UART | Most popular, no crystal needed (CH340C) |
| CH341 | USB-Multi | UART/I2C/SPI/Parallel |
| CH9340 | USB-UART | Enhanced CH340 |
| CH342-CH348 | USB-UART | Various channel counts |

### Other Interface Chips

| Series | Type | Features |
|--------|------|----------|
| CH395 | Ethernet | 10/100M Ethernet controller |
| CH9121 | ETH-UART | Ethernet to serial |
| CH9141 | BLE-UART | Bluetooth LE module |
| CH9143 | BLE-UART | Bluetooth LE module |
| CH334 | USB Hub | USB hub controller |
| CH224 | USB PD | Power Delivery controller |
| CH552/554/559 | 8051 USB | 8051-based USB MCUs |

---

## Flash Size Encoding

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

---

## Handler Implementation Notes

### MCU Package Code Extraction

```java
// MCU format: CH32V103C8T6
// Position:   01234567890123
//                    ^-- position 8 is pin code 'C'
char pinCode = mpn.charAt(8);
String packageType = MCU_PACKAGE_CODES.get(pinCode);

// Pin count also at position 8
Integer pinCount = MCU_PIN_COUNTS.get(pinCode);
```

### USB Interface Package Extraction

```java
// CH340G -> G = SOP-16
// Last character is package code
String suffix = mpn.substring(mpn.length() - 1);
String pkg = USB_PACKAGE_CODES.get(suffix);

// CH340 without suffix defaults to SOP-16
if (mpn.matches("^CH(340|341|9340)$")) {
    return "SOP-16";  // Default package
}
```

### Core Type Detection

The handler provides `getCoreType()` for MCUs:

| Series | Core Type |
|--------|-----------|
| CH32V003 | RISC-V QingKe V2A |
| CH32V103 | RISC-V QingKe V3A |
| CH32V203/208 | RISC-V QingKe V4B |
| CH32V303/305/307 | RISC-V QingKe V4F |
| CH32F103/203 | ARM Cortex-M3 |
| CH552/554/559 | 8051 Enhanced |

### Interface Type Detection

The handler provides `getInterfaceType()` for interface chips:

| Series | Interface Type |
|--------|---------------|
| CH340, CH9340 | USB to UART |
| CH341 | USB to UART/I2C/SPI/Parallel |
| CH348 | USB to 8x UART |
| CH395 | Ethernet Controller |
| CH9121 | Ethernet to UART |
| CH9141/9143 | BLE to UART |
| CH334 | USB Hub Controller |
| CH224 | USB PD Controller |

---

## Related Files

- Handler: `manufacturers/WCHHandler.java`
- Component types: `MICROCONTROLLER`, `IC`

---

## CH340 vs CH340C

The CH340C has an integrated crystal oscillator:
- **CH340G**: Requires external 12MHz crystal
- **CH340C**: No external crystal needed (recommended for new designs)

Both are SOP-16 package and pin-compatible.

---

## STM32 Compatibility

CH32F103 series is designed as a drop-in replacement for STM32F103:
- Same pinout and package options
- Same peripheral registers
- Lower cost alternative
- **Note**: Not 100% register-compatible, test thoroughly

---

## Learnings & Edge Cases

- **QingKe cores**: WCH's proprietary RISC-V core implementations (V2A, V3A, V4B, V4C, V4F)
- **CH32V003 popularity**: Entry-level RISC-V MCU, extremely low cost (~$0.10)
- **CH340 dominance**: Most common USB-UART chip in Arduino clones and hobbyist boards
- **Position-based extraction**: MCU pin code at position 8, flash at position 9
- **Flash code reuse**: Same encoding as STM32 (8=64KB, B=128KB, C=256KB)
- **CH32F vs STM32F**: Pin-compatible but register differences exist, verify before migration
- **Temperature code**: 6 = industrial (-40 to +85C) is standard for all CH32 MCUs

<!-- Add new learnings above this line -->
