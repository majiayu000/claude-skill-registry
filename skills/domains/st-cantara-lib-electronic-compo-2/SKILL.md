---
name: st
description: STMicroelectronics MPN encoding patterns, suffix decoding, and handler guidance. Use when working with STM32, STM8, ST MOSFETs, or L78/L79 regulators.
---

# STMicroelectronics (ST) Manufacturer Skill

## Product Families

STMicroelectronics produces a wide range of components:
- **STM32** - 32-bit ARM Cortex-M microcontrollers
- **STM8** - 8-bit microcontrollers
- **ST MOSFETs** - Power transistors (STF, STP, STD, STB, STW)
- **L78/L79** - Linear voltage regulators
- **Op-amps** - Various analog ICs

---

## STM32 Microcontroller Naming

### MPN Structure

```
STM32 F 1 03 C 8 T 6
  │   │ │  │ │ │ │ │
  │   │ │  │ │ │ │ └── Temperature range (6 = -40 to 85°C)
  │   │ │  │ │ │ └── Package (T = LQFP)
  │   │ │  │ │ └── Flash size (8 = 64KB)
  │   │ │  │ └── Pin count (C = 48 pins)
  │   │ │  └── Line (03 = access line)
  │   │ └── Core (1 = Cortex-M3)
  │   └── Type (F = Mainstream)
  └── Family (STM32)
```

### Type Letters (after STM32)

| Letter | Type | Description |
|--------|------|-------------|
| F | Mainstream | General purpose, good balance |
| L | Low-power | Ultra-low-power modes |
| H | High-performance | High clock speeds, more features |
| G | General-purpose | Newer mainstream series |
| W | Wireless | Integrated radio (BLE, LoRa) |
| U | Ultra-low-power | Next-gen low-power |

### Core Digit

| Digit | Core | Notes |
|-------|------|-------|
| 0 | Cortex-M0/M0+ | Entry level |
| 1 | Cortex-M3 | Mainstream |
| 2 | Cortex-M3 | Performance |
| 3 | Cortex-M4 | DSP instructions |
| 4 | Cortex-M4 | With FPU |
| 7 | Cortex-M7 | High performance |

### Pin Count Codes

| Code | Pins | Notes |
|------|------|-------|
| F | 20 | Smallest |
| G | 28 | |
| K | 32 | |
| T | 36 | |
| S | 44 | |
| C | 48 | Common |
| R | 64-66 | Popular |
| V | 100 | |
| Z | 144 | |
| I | 176 | Largest |

### Flash Size Codes

| Code | Size | Notes |
|------|------|-------|
| 4 | 16 KB | |
| 6 | 32 KB | |
| 8 | 64 KB | Common |
| B | 128 KB | |
| C | 256 KB | |
| D | 384 KB | |
| E | 512 KB | |
| F | 768 KB | |
| G | 1024 KB | |
| H | 1536 KB | |
| I | 2048 KB | Largest |

### Package Codes

| Code | Package | Description |
|------|---------|-------------|
| T | LQFP | Low-profile Quad Flat Pack |
| H | BGA | Ball Grid Array |
| U | VFQFPN | Very thin Fine-pitch QFN |
| Y | WLCSP | Wafer Level Chip Scale |
| P | TSSOP | Thin Shrink SOP |

### Temperature Range

| Code | Range | Application |
|------|-------|-------------|
| 6 | -40 to +85°C | Industrial |
| 7 | -40 to +105°C | Extended |

### Example Decoding

```
STM32F103C8T6
│     │  │││││
│     │  ││││└── 6 = -40 to +85°C
│     │  │││└── T = LQFP package
│     │  ││└── 8 = 64KB Flash
│     │  │└── C = 48 pins
│     │  └── 03 = Access line (medium density)
│     └── F1 = Mainstream Cortex-M3
└── STM32 family

Result: Mainstream M3 MCU, 48-pin LQFP, 64KB Flash, Industrial temp
Common Name: "Blue Pill" MCU
```

---

## STM8 Microcontroller Naming

### Structure

```
STM8 S 003 F 3 P 6
  │  │  │  │ │ │ │
  │  │  │  │ │ │ └── Temperature range
  │  │  │  │ │ └── Package
  │  │  │  │ └── Flash size
  │  │  │  └── Pin count
  │  │  └── Line
  │  └── Type (S=Standard, L=Low-power, A=Automotive)
  └── STM8 family
```

---

## ST Power MOSFET Naming

### Package Prefix

| Prefix | Package | Notes |
|--------|---------|-------|
| STF | TO-220FP | Isolated tab |
| STP | TO-220 | Standard |
| STD | DPAK (TO-252) | Surface mount |
| STB | D²PAK (TO-263) | High power SMD |
| STW | TO-247 | High power through-hole |
| VN | Various | N-channel series |
| VP | Various | P-channel series |

### Naming Pattern

```
ST [Package] [Current] [Channel] [Voltage] [Suffix]
│     │         │         │         │         │
│     │         │         │         │         └── Technology (F, L, etc.)
│     │         │         │         └── Voltage class (20=200V, 25=250V)
│     │         │         └── Channel (N=N-ch, P=P-ch)
│     │         └── Current rating (amps)
│     └── Package code (F, P, D, B, W)
└── ST prefix
```

### Example Decoding

```
STF5N52U
│││ │ ││
│││ │ │└── U = technology suffix
│││ │ └── 52 = 520V class
│││ └── N = N-channel
││└── 5 = ~5A rating
│└── F = TO-220FP package
└── ST prefix
```

---

## L78/L79 Voltage Regulator Naming

### Structure

```
L 78 [Voltage] [Grade] [Package]
│  │     │        │        │
│  │     │        │        └── Package suffix
│  │     │        └── Temperature grade (optional)
│  │     └── Output voltage (05=5V, 12=12V, etc.)
│  └── 78=Positive, 79=Negative
└── L prefix (ST designation)
```

### Package Suffixes

| Suffix | Package | Description |
|--------|---------|-------------|
| CV | TO-220 | Standard through-hole |
| V | TO-220 | Alternate |
| CP | TO-220FP | Isolated tab |
| P | TO-220FP | Alternate |
| CD2T | D²PAK | High power SMD |
| D2T | D²PAK | Alternate |
| CDT | DPAK | SMD |
| DT | DPAK | Alternate |

### Grade Codes

| Grade | Temperature | Notes |
|-------|-------------|-------|
| (none) | 0 to +125°C | Standard |
| C | 0 to +125°C | Commercial |
| A | -40 to +125°C | Extended |
| AB | -40 to +125°C | Extended |
| AC | 0 to +125°C | Standard |

### Example Decoding

```
L7805CV
│ ││ ││
│ ││ │└── V = through-hole variant
│ ││ └── C = Commercial grade
│ │└── 05 = 5V output
│ └── 78 = Positive regulator
└── L prefix

L7912ACD2T
│ ││ │ │ │
│ ││ │ │ └── T = tape packaging
│ ││ │ └── D2 = D²PAK
│ ││ └── AC = standard temp grade
│ │└── 12 = -12V output
│ └── 79 = Negative regulator
└── L prefix
```

---

## Handler Implementation Notes

### STM32 Package Extraction (CRITICAL BUG)

Current STHandler has a bug in `extractPackageCode()`:
```java
// WRONG - Tries to match last 2 chars as package+temp
String lastTwo = upperMpn.substring(upperMpn.length() - 2);
// For STM32F103C8T6: lastTwo = "T6"
// Then validates: "TUVRY".indexOf('T') >= 0 && isDigit('6')
// This passes but returns "T6" instead of just "T" (LQFP)
```

**Correct approach:**
```java
// STM32F103C8T6 → Package is second-to-last char: "T"
if (upperMpn.startsWith("STM32") && upperMpn.length() >= 2) {
    char packageChar = upperMpn.charAt(upperMpn.length() - 2);
    return switch (packageChar) {
        case 'T' -> "LQFP";
        case 'H' -> "BGA";
        case 'U' -> "VFQFPN";
        case 'Y' -> "WLCSP";
        case 'P' -> "TSSOP";
        default -> String.valueOf(packageChar);
    };
}
```

### MOSFET Package Extraction

```java
// Extract from prefix: STF = TO-220FP, STP = TO-220, STD = DPAK
if (upperMpn.startsWith("STF")) return "TO-220FP";
if (upperMpn.startsWith("STP")) return "TO-220";
if (upperMpn.startsWith("STD")) return "DPAK";
if (upperMpn.startsWith("STB")) return "D2PAK";
if (upperMpn.startsWith("STW")) return "TO-247";
```

### Series Extraction

```java
// STM32F103C8T6 → Series: STM32F103 (or STM32F1)
// For STM32: Extract up to and including line number
if (upperMpn.startsWith("STM32")) {
    // STM32 + Type + Core + Line = STM32F103
    // Match pattern: STM32[A-Z][0-9]{1,3}
    Pattern p = Pattern.compile("^(STM32[A-Z][0-9]{1,3})");
    Matcher m = p.matcher(upperMpn);
    if (m.find()) return m.group(1);
}
```

---

## Related Files

- Handler: `manufacturers/STHandler.java`
- Component types: `MICROCONTROLLER_ST`, `MCU_ST`, `MOSFET_ST`, `VOLTAGE_REGULATOR_LINEAR_ST`
- Test: `handlers/STHandlerTest.java` (72 tests)

---

## Handler Implementation Learnings (PR #81)

### Fixed Issues

All issues discovered during analysis have been fixed:

1. ~~HashSet in getSupportedTypes()~~ - Changed to `Set.of()`
2. ~~Debug println statements~~ - Removed
3. ~~Package extraction bug~~ - Now returns "LQFP" for STM32, "TO-220" for MOSFETs, etc.
4. ~~Voltage regulator regex broken~~ - Fixed with proper prefix matching

### Package Code Extraction (Fixed)

```java
// STM32/STM8: Package is second-to-last character
if (upperMpn.startsWith("STM32") || upperMpn.startsWith("STM8")) {
    char packageChar = upperMpn.charAt(upperMpn.length() - 2);
    return switch (packageChar) {
        case 'T' -> "LQFP";
        case 'H' -> "BGA";
        case 'U' -> "VFQFPN";
        // ...
    };
}

// MOSFETs: Package is in prefix
if (upperMpn.startsWith("STF")) return "TO-220FP";
if (upperMpn.startsWith("STP")) return "TO-220";
// ...

// Voltage regulators: Strip prefix and grade, then match suffix
String suffix = upperMpn.replaceFirst("^[LM]C?7[89]\\d{2}", "")
                       .replaceFirst("^[A-C]{1,2}", "");
// CV → TO-220, D2T → D2PAK, etc.
```

### Cross-Handler Pattern Matching Bug

When handler A's `matches()` falls through to `patterns.matches(mpn, type)`, it can accidentally match patterns registered by handler B.

**Fix in AtmelHandler**: Don't fall through to pattern matching for base `MICROCONTROLLER` type - return false if prefix check fails. This prevents AtmelHandler from matching STM32 MPNs.

---

## Learnings & Edge Cases

- **STM32 package code is NOT last 2 chars** - It's the second-to-last char only
- **Temperature is the last digit** - 6 or 7, not part of package
- **MOSFET package is in PREFIX** - Unlike most components where it's suffix
- **L78/L79 have multiple suffix styles** - CV, V, D2T, DT, etc.
- **STM32F4 naming differs slightly** - Some devices don't follow standard pattern
- **Pattern registry is shared across handlers** - Must use explicit prefix checks for base types to avoid cross-matching

---

## Sources

- [Understanding STM32 Naming Conventions - DigiKey](https://www.digikey.com/en/maker/tutorials/2020/understanding-stm32-naming-conventions)
- [STM32 Naming Scheme - Ziutek](https://ziutek.github.io/2018/05/07/stm32_naming_scheme.html)
- [L78 Datasheet - STMicroelectronics](https://www.st.com/resource/en/datasheet/l78.pdf)
- [Power MOSFETs - STMicroelectronics](https://www.st.com/en/power-transistors/power-mosfets.html)

<!-- Add new learnings above this line -->
