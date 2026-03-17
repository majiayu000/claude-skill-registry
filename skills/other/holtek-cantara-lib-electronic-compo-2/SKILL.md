---
name: holtek
description: Holtek Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Holtek MCUs, touch controllers, LCD drivers, or HoltekHandler.
---

# Holtek Semiconductor Manufacturer Skill

## MPN Structure

Holtek has two main naming conventions:

### HT Series (MCUs, Audio, USB, LCD)

```
HT[FAMILY][TYPE][PRODUCT]-[PACKAGE]
│    │      │      │          │
│    │      │      │          └── Package suffix (-1=SOP, -2=SOP, -3=SSOP)
│    │      │      └── Product number within series
│    │      └── Type (F=Flash MCU, V=Voice, B=Bridge)
│    └── Family (66/67/68=Flash MCU, 45=Touch, 82=Voice, 42=USB, 16=LCD)
└── Holtek prefix

Example: HT66F0185 = Flash MCU, general purpose
Example: HT42B534-1 = USB to UART Bridge, SOP package
```

### BS Series (Body Sensor/Touch)

```
BS83[LINE][KEYS][VARIANT]-[PACKAGE]
│    │     │      │           │
│    │     │      │           └── Package suffix
│    │     │      └── Variant letter (A, B)
│    │     └── Number of touch keys
│    └── Series 83 (capacitive touch)
└── Body Sensor prefix

Example: BS83B16A-3 = Touch MCU, 16 keys, variant A, SSOP package
```

### Example Decoding

```
HT66F0185
│  │ │  │
│  │ │  └── Product number 0185
│  │ └── F = Flash MCU
│  └── 66 = General purpose Flash MCU family
└── HT = Holtek prefix

BS83B16A-3
│   │ │ │ │
│   │ │ │ └── -3 = SSOP package
│   │ │ └── A = Variant
│   │ └── 16 = 16 touch keys
│   └── B = Enhanced series
└── BS83 = Body Sensor capacitive touch
```

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| -1 | SOP | Standard SOP |
| -2 | SOP | SOP variant |
| -3 | SSOP | Shrink SOP |
| SS | SSOP | Inline suffix |
| SOP | SOP | Inline suffix |
| NS | NSOP | Narrow SOP |
| QF | QFP | Quad Flat Package |
| DIP | DIP | Through-hole |

---

## Product Families

### Flash MCUs (HT66F, HT67F, HT68F)

| Series | Type | Key Features |
|--------|------|--------------|
| HT66F | General Flash MCU | General purpose, up to 64KB Flash |
| HT67F | LCD Flash MCU | Built-in LCD driver |
| HT68F | Enhanced I/O MCU | More GPIO pins |

### Touch MCUs (HT45F, BS83)

| Series | Type | Key Features |
|--------|------|--------------|
| HT45F | Touch Key MCU | Capacitive touch sensing |
| BS83A | Touch MCU | Basic capacitive touch |
| BS83B | Enhanced Touch MCU | More touch channels |

### Voice/Audio ICs (HT82V)

| Series | Type | Key Features |
|--------|------|--------------|
| HT82V739 | Voice Synthesis | OTP voice IC |

### USB Interface (HT42B)

| Series | Type | Key Features |
|--------|------|--------------|
| HT42B534 | USB-UART Bridge | USB to serial converter |

### LCD Drivers (HT16xx)

| Series | Type | Key Features |
|--------|------|--------------|
| HT1621 | LCD Controller | 32x4 segment LCD |
| HT1621B | LCD Controller | Enhanced HT1621 |
| HT1628 | LED/LCD Controller | Combined LED and LCD |

---

## Handler Implementation Notes

### Component Type Detection

```java
// Flash MCUs: HT66F, HT67F, HT68F patterns
boolean isFlashMCU = upperMpn.matches("^HT6[678]F\\d+.*");

// Touch MCUs: HT45F and BS83 patterns
boolean isTouchMCU = upperMpn.startsWith("HT45F") ||
                     upperMpn.startsWith("BS83");

// All HT and BS parts are ICs
boolean isIC = upperMpn.startsWith("HT") || upperMpn.startsWith("BS");
```

### Package Code Extraction

```java
// Check suffix-based codes first (-1, -2, -3)
if (upperMpn.endsWith("-3")) return "SSOP";
if (upperMpn.endsWith("-1") || upperMpn.endsWith("-2")) return "SOP";

// Then check inline codes (SS, SOP, NS, QF)
// Must verify position > 4 to avoid false matches
```

### Series Extraction

```java
// HT series extracts family + type
if (upperMpn.startsWith("HT66F")) return "HT66F";
if (upperMpn.startsWith("HT67F")) return "HT67F";
if (upperMpn.startsWith("HT68F")) return "HT68F";

// BS series preserves variant letter
if (upperMpn.startsWith("BS83B")) return "BS83B";
if (upperMpn.startsWith("BS83A")) return "BS83A";
if (upperMpn.startsWith("BS83")) return "BS83";  // Generic fallback

// LCD drivers include full 4-digit series
if (upperMpn.startsWith("HT1621")) return "HT1621";
if (upperMpn.startsWith("HT1628")) return "HT1628";
```

### Product Code Extraction

The handler provides `extractProductCode()` for getting the full alphanumeric product identifier:

```java
// HT66F0185 -> HT66F0185
// BS83B16A-3 -> BS83B16A (strips package suffix)
// HT1621B -> HT1621B
```

---

## Related Files

- Handler: `manufacturers/HoltekHandler.java`
- Component types: `MICROCONTROLLER`, `IC`

---

## Helper Methods

The handler provides convenience methods for categorization:

| Method | Purpose |
|--------|---------|
| `isTouchMCU(mpn)` | Returns true for HT45F and BS83 series |
| `isFlashMCU(mpn)` | Returns true for HT66F, HT67F, HT68F |
| `isLCDDriver(mpn)` | Returns true for HT16xx series |
| `isVoiceIC(mpn)` | Returns true for HT82V series |
| `isUSBIC(mpn)` | Returns true for HT42B series |

---

## Learnings & Edge Cases

- **BS prefix exception**: BS83 is Holtek despite different prefix (Body Sensor)
- **HT16xx LCD drivers**: These are NOT MCUs, just LCD controller drivers
- **Touch key count**: BS83B16A has 16 keys encoded in part number
- **Package suffix variants**: -1 and -2 both mean SOP (different internal variants)
- **HT67F LCD MCU**: Has built-in LCD driver, different from HT1621 standalone driver
- **Voice ICs are OTP**: HT82V series uses One-Time Programmable memory, not Flash

<!-- Add new learnings above this line -->
