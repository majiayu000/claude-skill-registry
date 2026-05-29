---
name: logicic
description: Use when working with 74xx and CD4xxx series logic ICs - standard TTL/CMOS logic gates, flip-flops, counters, decoders, multiplexers. Includes technology families (LS, HC, HCT, AC, AHC) and LogicICHandler guidance.
---

# Logic IC Manufacturer Skill

## Overview

Logic ICs are standardized digital integrated circuits implementing basic logic functions. The two main families are:

1. **74xx Series** - TTL-based logic (originally Texas Instruments, now multi-source)
2. **CD4xxx Series** - CMOS-based logic (originally RCA, now multi-source)

These parts are produced by multiple manufacturers (TI, ON Semi, Nexperia, Diodes Inc, STMicroelectronics) with identical pinouts and functions.

---

## MPN Structure

### 74xx Series

```
[PREFIX][FAMILY][SERIES][FUNCTION][PACKAGE]
   |       |       |        |         |
   |       |       |        |         +-- Package code (N, D, PW, etc.)
   |       |       |        +-- Function number (00, 04, 74, 138, etc.)
   |       |       +-- Fixed: "74" (commercial) or "54" (military temp)
   |       +-- Technology family (LS, HC, HCT, AC, AHC, etc.)
   +-- Optional manufacturer prefix (SN for TI)
```

#### Example Decoding

```
SN74HC595N
|  |  |  ||
|  |  |  |+-- N = DIP package
|  |  |  +-- 595 = 8-bit shift register function
|  |  +-- 74 = Commercial temperature range
|  +-- HC = High-speed CMOS family
+-- SN = Texas Instruments prefix

74LS04D
  |  ||
  |  |+-- D = SOIC package
  |  +-- 04 = Hex inverter function
  +-- LS = Low-power Schottky TTL family
```

### CD4xxx Series

```
CD[FUNCTION][PACKAGE]
|     |         |
|     |         +-- Package suffix (BE, BM, UBE, etc.)
|     +-- Function number (4001, 4017, 4051, etc.)
+-- CD = CMOS Digital prefix
```

#### Example Decoding

```
CD4017BE
|  |   ||
|  |   |+-- E = Economy grade
|  |   +-- B = Buffered output
|  +-- 4017 = Decade counter/divider function
+-- CD = CMOS Digital prefix

CD4001UBE
|  |   |||
|  |   ||+-- E = Economy grade
|  |   |+-- B = Buffered
|  |   +-- U = Unbuffered variant
|  +-- 4001 = Quad 2-input NOR gate
+-- CD = CMOS Digital prefix
```

---

## Technology Families (74xx Series)

### Original TTL Technologies

| Family | Name | Speed | Power | Supply | Notes |
|--------|------|-------|-------|--------|-------|
| (none) | Standard TTL | Slow | High | 5V | Original, obsolete |
| L | Low-power TTL | Slow | Low | 5V | Obsolete |
| S | Schottky TTL | Fast | High | 5V | Obsolete |
| LS | Low-power Schottky | Fast | Low | 5V | Still common |
| ALS | Advanced LS | Faster | Lower | 5V | Improved LS |
| F | Fast TTL | Very Fast | Medium | 5V | High-speed apps |
| AS | Advanced Schottky | Very Fast | High | 5V | Maximum speed |

### CMOS Technologies (Modern)

| Family | Name | Speed | Power | Supply | Notes |
|--------|------|-------|-------|--------|-------|
| C | CMOS | Slow | Very Low | 3-15V | Wide voltage range |
| HC | High-speed CMOS | Fast | Very Low | 2-6V | Most common today |
| HCT | HC TTL-compatible | Fast | Very Low | 4.5-5.5V | 5V TTL I/O levels |
| AC | Advanced CMOS | Very Fast | Low | 2-6V | High-speed CMOS |
| ACT | AC TTL-compatible | Very Fast | Low | 4.5-5.5V | Fast + TTL levels |
| AHC | Advanced HC | Faster | Very Low | 2-5.5V | Improved HC |
| AHCT | AHC TTL-compatible | Faster | Very Low | 4.5-5.5V | Improved HCT |

### Low-Voltage Technologies

| Family | Name | Speed | Supply | Notes |
|--------|------|-------|--------|-------|
| LV | Low Voltage | Medium | 2-5.5V | General low-voltage |
| LVC | LV CMOS | Fast | 1.65-5.5V | Common in 3.3V systems |
| LVT | LV TTL | Fast | 2.7-3.6V | 3.3V optimized |
| ALVC | Advanced LVC | Very Fast | 1.65-3.6V | High-speed 3.3V |
| AUC | Advanced ULP | Fast | 0.8-2.7V | Ultra-low voltage |
| AUP | Advanced ULP | Medium | 0.8-3.6V | Ultra-low power |

### Technology Selection Guide

| Use Case | Recommended Family |
|----------|-------------------|
| New 5V design | HC or HCT |
| Replacing old TTL | HCT (input compatible) |
| 3.3V systems | LVC |
| Mixed 3.3V/5V | LVC (5V tolerant) |
| Low power battery | AUP, HC |
| High speed | AC, AHC, ALVC |
| Wide voltage range | CD4000 series |

---

## Function Number Reference

### Gates (2-digit)

| Number | Function | Gates/Package |
|--------|----------|---------------|
| 00 | Quad 2-input NAND | 4 |
| 02 | Quad 2-input NOR | 4 |
| 04 | Hex inverter | 6 |
| 08 | Quad 2-input AND | 4 |
| 10 | Triple 3-input NAND | 3 |
| 11 | Triple 3-input AND | 3 |
| 20 | Dual 4-input NAND | 2 |
| 21 | Dual 4-input AND | 2 |
| 27 | Triple 3-input NOR | 3 |
| 30 | 8-input NAND | 1 |
| 32 | Quad 2-input OR | 4 |
| 86 | Quad 2-input XOR | 4 |
| 125 | Quad bus buffer (tri-state) | 4 |
| 126 | Quad bus buffer (tri-state) | 4 |

### Flip-Flops

| Number | Function | Flip-Flops/Package |
|--------|----------|-------------------|
| 73 | Dual J-K flip-flop (clear) | 2 |
| 74 | Dual D flip-flop (preset/clear) | 2 |
| 75 | Quad bistable latch | 4 |
| 76 | Dual J-K flip-flop (preset/clear) | 2 |
| 109 | Dual J-K flip-flop (positive edge) | 2 |
| 112 | Dual J-K flip-flop (negative edge) | 2 |
| 174 | Hex D flip-flop (common clear) | 6 |
| 175 | Quad D flip-flop (common clear) | 4 |
| 273 | Octal D flip-flop (common clear) | 8 |
| 374 | Octal D flip-flop (tri-state) | 8 |
| 574 | Octal D flip-flop (tri-state, edge) | 8 |

### Counters

| Number | Function |
|--------|----------|
| 90 | Decade counter |
| 93 | 4-bit binary counter |
| 160 | Sync decade counter (async clear) |
| 161 | Sync 4-bit counter (async clear) |
| 163 | Sync 4-bit counter (sync clear) |
| 190 | Sync decade up/down counter |
| 191 | Sync binary up/down counter |
| 393 | Dual 4-bit binary counter |
| 4017 | CD4017 decade counter/divider |
| 4040 | CD4040 12-bit binary counter |

### Shift Registers

| Number | Function | Bits |
|--------|----------|------|
| 164 | 8-bit serial-in parallel-out | 8 |
| 165 | 8-bit parallel-in serial-out | 8 |
| 166 | 8-bit parallel-in serial-out | 8 |
| 595 | 8-bit serial-in parallel-out (latch) | 8 |
| 597 | 8-bit serial-in parallel-out (latch) | 8 |
| 4015 | CD4015 dual 4-bit shift register | 2x4 |
| 4094 | CD4094 8-bit shift register | 8 |

### Decoders/Demultiplexers

| Number | Function |
|--------|----------|
| 42 | BCD to decimal decoder |
| 138 | 3-to-8 line decoder |
| 139 | Dual 2-to-4 line decoder |
| 154 | 4-to-16 line decoder |
| 155 | Dual 2-to-4 decoder/demux |
| 238 | 3-to-8 line decoder (active high) |
| 4028 | CD4028 BCD to decimal decoder |
| 4514 | CD4514 4-to-16 line decoder (latch) |

### Multiplexers

| Number | Function |
|--------|----------|
| 151 | 8-to-1 multiplexer |
| 153 | Dual 4-to-1 multiplexer |
| 157 | Quad 2-to-1 multiplexer |
| 158 | Quad 2-to-1 multiplexer (inverted) |
| 251 | 8-to-1 multiplexer (tri-state) |
| 253 | Dual 4-to-1 multiplexer (tri-state) |
| 257 | Quad 2-to-1 multiplexer (tri-state) |
| 4051 | CD4051 8-channel analog mux |
| 4052 | CD4052 Dual 4-channel analog mux |
| 4053 | CD4053 Triple 2-channel analog mux |

### Buffers/Drivers

| Number | Function |
|--------|----------|
| 07 | Hex buffer (open-collector) |
| 17 | Hex buffer (open-collector) |
| 125 | Quad buffer (tri-state) |
| 126 | Quad buffer (tri-state) |
| 240 | Octal buffer (inverting, tri-state) |
| 241 | Octal buffer (non-inverting, tri-state) |
| 244 | Octal buffer (non-inverting, tri-state) |
| 245 | Octal bus transceiver (tri-state) |
| 4049 | CD4049 Hex inverting buffer |
| 4050 | CD4050 Hex non-inverting buffer |

---

## Package Codes

### 74xx Series Package Codes

| Code | Package | Pins | Notes |
|------|---------|------|-------|
| N | PDIP | 14-20 | Through-hole, prototyping |
| D | SOIC | 14-20 | Surface mount, 1.27mm pitch |
| DW | SOIC-Wide | 16-28 | Wide body SOIC |
| PW | TSSOP | 14-24 | Thin profile, 0.65mm pitch |
| DB | SSOP | 14-28 | Shrink SOIC |
| DBV | SOT-23 | 5-6 | Very small, single gate |
| DGV | VSSOP | 8 | Mini SOIC |
| RGY | QFN | 16-24 | No-lead package |
| NS | SO | 14-20 | Small outline |
| M | SOIC | 14-20 | Alternative SOIC code |
| T | TSSOP | 14-24 | Alternative TSSOP code |
| P | DIP | 14-20 | Plastic DIP (alternate) |

### CD4xxx Series Package Codes

| Code | Package | Notes |
|------|---------|-------|
| BE | PDIP | Standard plastic DIP, buffered |
| B | PDIP | Standard buffered output |
| E | PDIP | Economy grade |
| UBE | PDIP | Unbuffered output |
| BC | CERDIP | Ceramic DIP (high reliability) |
| BM | SOIC | Surface mount, buffered |
| BT | TSSOP | Thin package, buffered |
| BD | SOIC | Alternative SOIC code |
| PWR | TSSOP | Tape and reel |
| N | DIP | Generic DIP |
| P | DIP | Plastic DIP |
| NSR | SOIC | SOIC tape and reel |

---

## Handler Implementation

### Supported Component Types

```java
ComponentType.IC         // Base type
ComponentType.LOGIC_IC   // Specific logic IC type
```

### Pattern Recognition

```java
// 74xx series pattern (includes 54xx military)
"^(?:74|54)[LSAHCTTF]{0,4}[0-9]{2,4}.*"

// CD4xxx series pattern
"^CD4[0-9]{3}.*"
```

### Series Extraction Rules

The handler extracts the base series by:

1. **74xx**: Extracts digits after technology code until non-digit
   - `SN74HC595N` -> `595`
   - `74LS04D` -> `04`

2. **CD4xxx**: Extracts `CD4` + 3-digit function
   - `CD4017BE` -> `CD4017`
   - `CD4001UBE` -> `CD4001`

### Package Code Extraction Rules

**CD4xxx:**
- Check longest suffixes first: `UBE`, `BE`, `BC`
- Then shorter: `B`, `E`

**74xx:**
- Single letter suffix: `N`, `D`, `P`, `M`, `T`
- Pattern: `.*?([NDPMT])$`

---

## Similarity Calculation

The `LogicICSimilarityCalculator` uses these rules:

### Same Function, Compatible Technology = HIGH (0.9)

```java
// These are highly similar (same function)
"74LS00" vs "74HC00"    // 0.9 - Same NAND function
"74LS04" vs "74ALS04"   // 0.9 - Same inverter function
"CD4001BE" vs "CD4001BM" // 0.9 - Same NOR gate, different package
```

### Different Functions = LOW (0.3)

```java
// These have low similarity (different functions)
"74LS00" vs "74LS04"    // 0.3 - NAND vs Inverter
"74HC595" vs "74HC138"  // 0.3 - Shift register vs Decoder
"CD4017" vs "CD4001"    // 0.3 - Counter vs NOR gate
```

### Compatible Technology Groups

These 74xx families are considered compatible:
- `LS`, `ALS`, `F`, `HC`, `HCT`

Parts with the same function and compatible families score HIGH similarity.

### Function Groups

Parts in the same function group may have increased similarity:

| Group | Function Numbers |
|-------|-----------------|
| NAND | 00, 10, 20, 30, 40 |
| NOR | 02, 12, 22, 32, 42 |
| NOT | 04, 14, 24, 34, 44 |
| AND | 08, 18, 28, 38, 48 |
| OR | 32, 42 |
| Flip-Flops | 73, 74, 75, 76, 77, 78 |
| Multiplexers | 151, 153, 157, 158 |
| Decoders | 138, 139, 154, 155 |

---

## Example MPNs

### Texas Instruments (SN prefix)

| MPN | Description |
|-----|-------------|
| SN74HC595N | 8-bit shift register, HC CMOS, DIP |
| SN74LS04D | Hex inverter, LS TTL, SOIC |
| SN74AHC1G04DCKR | Single inverter, AHC, SC70, tape/reel |
| SN74LVC245APW | Octal bus transceiver, LVC, TSSOP |
| SN74HC138D | 3-to-8 decoder, HC CMOS, SOIC |

### Nexperia (74 prefix without SN)

| MPN | Description |
|-----|-------------|
| 74HC595D | 8-bit shift register, HC, SOIC |
| 74LVC1G04GW | Single inverter, LVC, SC70 |
| 74AHCT125D | Quad buffer, AHCT, SOIC |
| 74HCT245D | Octal bus transceiver, HCT, SOIC |

### ON Semiconductor (MC74 prefix)

| MPN | Description |
|-----|-------------|
| MC74HC595ADG | 8-bit shift register, HC, SOIC |
| MC74AC04DG | Hex inverter, AC, SOIC |
| MC74VHC1GT04DTT1G | Single inverter, VHC, SC70 |

### CD4000 Series (Multi-source)

| MPN | Description |
|-----|-------------|
| CD4001BE | Quad 2-input NOR, buffered, DIP |
| CD4017BM | Decade counter, buffered, SOIC |
| CD4051BE | 8-channel mux, buffered, DIP |
| CD4066BM | Quad bilateral switch, buffered, SOIC |
| CD4093BE | Quad Schmitt NAND, buffered, DIP |

---

## Multi-Sourcing Guide

Logic ICs are second-sourced by many manufacturers. These are direct replacements:

| Function | TI | Nexperia | ON Semi | STMicro |
|----------|----|---------:|---------|---------|
| 74HC595 | SN74HC595 | 74HC595 | MC74HC595A | M74HC595 |
| 74LS04 | SN74LS04 | 74LS04 | MC74LS04A | - |
| 74HC138 | SN74HC138 | 74HC138 | MC74HC138A | M74HC138 |
| CD4001 | CD4001B | HEF4001B | MC14001B | HCF4001 |
| CD4017 | CD4017B | HEF4017B | MC14017B | HCF4017 |

**Note:** Nexperia uses `HEF` prefix for CD4000 series (e.g., `HEF4001BT`).
STMicro uses `HCF` prefix (e.g., `HCF4017BE`).
ON Semiconductor uses `MC14` prefix (e.g., `MC14001BCP`).

---

## Related Files

- **Handler**: `manufacturers/LogicICHandler.java`
- **Similarity Calculator**: `componentsimilaritycalculators/LogicICSimilarityCalculator.java`
- **Component Types**: `ComponentType.LOGIC_IC`, `ComponentType.LOGIC_IC_NEXPERIA`, `ComponentType.LOGIC_IC_DIODES`
- **Similarity Skill**: `.claude/skills/similarity-logic/SKILL.md`

---

## Learnings & Quirks

### Handler Patterns

- **Pattern uses character class**: `[LSAHCTTF]{0,4}` captures technology but has duplicates (TT). Works but could be cleaner.
- **54xx military parts**: Pattern includes 54xx prefix for military temperature range variants. Same function as 74xx.
- **No manufacturer prefix required**: Pattern matches both `SN74HC595` (TI) and `74HC595` (generic).

### Series Extraction Gotcha

- The `extractSeries()` method uses regex `replaceAll("([0-9]{2,4}).*$", "$1")` which captures the function number.
- For `74LS04D`, this extracts `04` (correct).
- For `74HC595N`, this extracts `595` (correct).
- **Note**: Technology prefix (LS, HC) is NOT included in extracted series.

### Package Code Order Matters

```java
// CORRECT - Check longer suffixes first
if (mpn.endsWith("UBE")) return "UBE";  // 3 chars first
if (mpn.endsWith("BE")) return "BE";    // 2 chars second
if (mpn.endsWith("B")) return "B";      // 1 char last

// WRONG - Would never match UBE or BE
if (mpn.endsWith("E")) return "E";      // Matches first!
```

### CD4000 Buffered vs Unbuffered

- **B suffix**: Buffered output (higher drive, lower speed)
- **UB suffix**: Unbuffered output (faster, lower drive)
- Most modern designs use buffered versions.

### 74xx vs CD4000 Comparison

| Aspect | 74xx (CMOS) | CD4000 |
|--------|-------------|--------|
| Supply Voltage | 2-6V (HC) | 3-15V |
| Speed | Faster | Slower |
| Power | Low | Very Low |
| Output Drive | Higher | Lower |
| ESD Tolerance | Lower | Higher |
| Noise Immunity | Good | Excellent |

### Technology Selection for Mixed Voltage

| Source Logic | Target Logic | Use Family |
|--------------|--------------|------------|
| 5V TTL | 3.3V CMOS | LVC (5V tolerant inputs) |
| 3.3V CMOS | 5V TTL | HCT (TTL output levels) |
| 3.3V to 5V bidirectional | - | 74LVC245 (transceiver) |

### Debug Statements in Calculator

The `LogicICSimilarityCalculator` contains `System.out.println` debug statements (lines 43, 47, 51, 59, 67, 78, 92, 113-123). These should be removed or replaced with SLF4J logging in production.

### Cross-Handler Considerations

- LogicICHandler handles generic logic ICs (74xx, CD4xxx).
- Manufacturer-specific handlers (TI, Nexperia, etc.) may also match these parts.
- Handler ordering in `ManufacturerHandlerFactory` affects which handler processes the part first.

<!-- Add new learnings above this line -->
