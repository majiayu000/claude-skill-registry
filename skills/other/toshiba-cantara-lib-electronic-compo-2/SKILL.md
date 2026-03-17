---
name: toshiba
description: Toshiba Semiconductor MPN encoding patterns, package codes, and handler guidance. Use when working with Toshiba MOSFETs, optocouplers, transistors, motor drivers, or ToshibaHandler.
---

# Toshiba Semiconductor Manufacturer Skill

## MPN Structure

Toshiba uses several distinct naming conventions depending on product family:

### Power MOSFETs (TK, TPC, TPH Series)

#### TK Series (DTMOS Digital Power MOSFETs)

```
TK[CURRENT][CHANNEL][VOLTAGE][SERIES][SUFFIX]
  |    |        |       |        |       |
  |    |        |       |        |       +-- Package: L=DPAK, S=D2PAK, Z=TO-220SIS
  |    |        |       |        +-- Generation: 1, Z1, etc.
  |    |        |       +-- Voltage / 10 (60=600V, 65=650V)
  |    |        +-- N=N-channel, V=Vertical, P=P-channel
  |    +-- On-resistance indicator (024=0.024 Ohm)
  +-- Toshiba K-series prefix
```

Example: `TK024N60Z1` = N-channel, 0.024 Ohm RDS(on), 600V, DTMOS VI gen 1

#### TPC Series (Small Signal Power MOSFETs)

```
TPC[VARIANT][TYPE][SPECS][PACKAGE]
   |    |       |     |      |
   |    |       |     |      +-- Package suffix (U, TU, etc.)
   |    |       |     +-- Specifications
   |    |       +-- Component type (K=MOSFET)
   |    +-- Pin/variant number (8, 6, 4, etc.)
   +-- Toshiba Power Compact
```

Example: `TPC8107` = Small signal power MOSFET, 8-pin variant

#### TPH Series (High Voltage MOSFETs)

```
TPH[CURRENT][CHANNEL][VOLTAGE][SERIES][PKG]
   |    |        |       |        |       |
   |    |        |       |        |       +-- Package: NH=TO-247, etc.
   |    |        |       |        +-- Series: 6, 7, Q, etc.
   |    |        |       +-- Voltage / 10 (60=600V)
   |    |        +-- 0=N-channel
   |    +-- Current/RDS indicator (4R6=4.6A or 0.46mOhm)
   +-- Toshiba Power High-voltage
```

Example: `TPH4R606NH` = N-channel, high-voltage MOSFET, TO-247 package

### Small Signal MOSFETs (SSM Series)

```
SSM[PINS][POLARITY][NUMBER][PACKAGE]
   |   |      |        |       |
   |   |      |        |       +-- Package: TU=UFM, F=S-Mini, FU=USM
   |   |      |        +-- Serial number
   |   |      +-- K=N-channel, J=P-channel
   |   +-- Pin count: 3, 4, 5, 6
   +-- Small Signal MOSFET
```

Example: `SSM3K102TU` = 3-pin, N-channel, UFM package

### Transistors (2SA, 2SC Series - JIS Standard)

```
2S[TYPE][NUMBER][hFE_RANK]
  |   |      |       |
  |   |      |       +-- Optional hFE rank: blank, -O, -P, -Q, -R, -Y
  |   |      +-- 4-digit serial number
  |   +-- A=PNP HF, B=PNP LF, C=NPN HF, D=NPN LF
  +-- 2S = JIS semiconductor prefix
```

| Prefix | Type | Frequency |
|--------|------|-----------|
| 2SA | PNP | High frequency (>3MHz) |
| 2SB | PNP | Low frequency (<3MHz) |
| 2SC | NPN | High frequency (>3MHz) |
| 2SD | NPN | Low frequency (<3MHz) |

Example: `2SC5198` = NPN high-frequency transistor
Example: `2SA1943` = PNP high-frequency transistor (complementary to 2SC5200)

### Digital Transistors (RN, RP Series)

```
RN[NUMBER][SUFFIX]  or  RP[NUMBER][SUFFIX]
  |    |       |          |    |       |
  |    |       +-- Package: E=EMT3, etc.
  |    +-- Serial number
  +-- RN=NPN, RP=PNP (with built-in bias resistors)
```

### Optocouplers (TLP Series)

```
TLP[NUMBER][VARIANT]([OPTIONS])
   |    |       |        |
   |    |       |        +-- Packaging options: GB, GR, TP, SE
   |    |       +-- Output type variant: A, B, C (CTR grade)
   |    +-- 3-4 digit model number
   +-- Toshiba Light/Photocoupler
```

Example: `TLP291(GB-TP,SE)` = Photocoupler, CTR grade GB, Tape/reel, RoHS

#### Option Suffixes

| Suffix | Meaning |
|--------|---------|
| TP | Tape and reel |
| SE | RoHS compatible |
| T | Thailand manufacture |
| C | China manufacture |
| (blank) | Japan manufacture |

#### CTR (Current Transfer Ratio) Grades

| Grade | CTR Range | Applications |
|-------|-----------|--------------|
| A, GR | 50-100% | Low current |
| B, GB | 100-200% | Standard |
| C, GC | 200-400% | High sensitivity |
| D | 300-600% | Very high sensitivity |

### Motor Drivers (TB Series)

```
TB[NUMBER][VARIANT][PACKAGE]
  |    |       |       |
  |    |       |       +-- Package: FNG=SSOP24, AFG=QFN, etc.
  |    |       +-- Feature variant
  |    +-- Series/model number (6612, 67S, etc.)
  +-- Toshiba Brushed/Brushless motor driver
```

Example: `TB6612FNG` = Dual H-bridge motor driver, SSOP24

### Gate Drivers (TPD Series)

```
TPD[NUMBER][VARIANT][PACKAGE]
   |    |       |       |
   |    |       |       +-- Package suffix
   |    |       +-- Feature/variant
   |    +-- Series number
   +-- Toshiba Power Driver
```

### Voltage Regulators (TAR Series)

```
TAR[NUMBER][VOLTAGE]
   |    |       |
   |    |       +-- Output voltage (5 = 5V, 33 = 3.3V)
   |    +-- Series number
   +-- Toshiba Adjustable Regulator
```

### Microcontrollers (TMP Series)

```
TMP[CORE][GROUP][VARIANT]-[PKG][PINS]
   |   |     |       |       |     |
   |   |     |       |       |     +-- Pin count
   |   |     |       |       +-- Package: F=QFP, Q=QFN, etc.
   |   |     |       +-- Feature variant
   |   |     +-- Product group (H, K, G, E, P)
   |   +-- M=ARM Cortex-M, V=RISC-V
   +-- Toshiba Microprocessor
```

#### Core Identifiers

| Code | Core | Notes |
|------|------|-------|
| M3 | ARM Cortex-M3 | TXZ03 family |
| M4 | ARM Cortex-M4 | TXZ04 family |
| M0 | ARM Cortex-M0 | TXZ00 family |
| V | RISC-V | Newer products |

#### Product Groups

| Group | Application |
|-------|-------------|
| H | General-purpose/Consumer |
| K | Motor/Inverter control |
| G | OA/Digital equipment |
| E | Robotics, precision instruments |
| P | Healthcare/Battery equipment |

#### Package Codes

| Code | Package |
|------|---------|
| F, FG | LQFP |
| FY | LQFP (specific variant) |
| Q, QG | QFN |
| MG | SOP |
| NG | SDIP |
| XBG | BGA |
| WBG | WCSP |

Example: `TMPM370FYFG` = ARM Cortex-M3, Group G, 370 series, LQFP

### IGBTs (GT, MG Series)

```
GT[POWER][VOLTAGE][VARIANT]
  |    |       |       |
  |    |       |       +-- Variant/generation
  |    |       +-- Voltage class
  |    +-- Power/current class
  +-- Gate Turn-off (IGBT module prefix)

MG[CONFIG][VOLTAGE][POWER]
  |    |       |       |
  |    |       |       +-- Current rating
  |    |       +-- Voltage class (J=600V, K=1200V)
  |    +-- Module configuration
  +-- IGBT Module
```

---

## Package Codes

### MOSFET/Power Transistor Packages

| Code | Package | Thermal | Notes |
|------|---------|---------|-------|
| U | DPAK (TO-252) | Medium | SMD power |
| S | D2PAK (TO-263) | High | SMD high power |
| L | TO-220SIS | Excellent | Isolated |
| Z | TO-220SIS | Excellent | Full pack |
| NH | TO-247 | Superior | High power |
| TU | UFM | Low | Ultra-thin flat mini |
| F | S-Mini | Low | Compact |
| FU | USM | Low | Ultra small mold |
| LQ | LFPAK | Good | Low-profile |

### Optocoupler Packages

| Code | Package | Pins | Notes |
|------|---------|------|-------|
| (blank) | DIP4 | 4 | Standard through-hole |
| S | SO-4 | 4 | Surface mount |
| SO6L | SO-6 | 6 | Thin SO package |

### Motor Driver Packages

| Code | Package | Pins |
|------|---------|------|
| FNG | SSOP24 | 24 |
| AFG | QFN | Various |
| PG | HTSSOP | Various |
| NG | SDIP | Various |

### Microcontroller Packages

| Code | Package | Description |
|------|---------|-------------|
| FG | LQFP | Quad flat package |
| QG | QFN | Quad flat no-lead |
| MG | SOP | Small outline package |
| NG | SDIP | Shrink DIP |

---

## Temperature Grades

| Suffix | Range | Application |
|--------|-------|-------------|
| (none) | -40C to +85C | Industrial |
| -C | 0C to +70C | Commercial |
| -A | -40C to +125C | Automotive |
| -M | -55C to +150C | Military |

---

## RoHS and Packaging Suffixes

| Suffix | Meaning |
|--------|---------|
| L | Tape and Reel (2500pcs) |
| L1 | Tape and Reel (1000pcs) |
| L3 | Tape and Reel (3000pcs) |
| F | Lead-free package |
| Q | Lead-free terminals |
| X | RoHS compatible |
| V | Halogen-free |

---

## Product Family Prefixes Summary

### MOSFETs

| Prefix | Technology | Application |
|--------|------------|-------------|
| TK | DTMOS | Digital power, high efficiency |
| TPC | Compact MOSFET | Small signal power |
| TPH | High voltage | Power applications |
| SSM | Small signal | Signal switching |
| 2SK | JIS N-channel | Legacy/compatibility |

### Transistors

| Prefix | Type | Notes |
|--------|------|-------|
| 2SA | PNP HF | High frequency |
| 2SB | PNP LF | Low frequency, power |
| 2SC | NPN HF | High frequency |
| 2SD | NPN LF | Low frequency, power |
| RN | NPN Digital | Built-in resistors |
| RP | PNP Digital | Built-in resistors |

### Optocouplers

| Prefix | Output Type | Application |
|--------|-------------|-------------|
| TLP1xx | Transistor output | General isolation |
| TLP2xx | High-speed transistor | Data communication |
| TLP3xxx | Photo-relay | Solid state switching |
| TLP5xx | IGBT driver | High-power gate drive |

### Motor Drivers

| Prefix | Type | Features |
|--------|------|----------|
| TB66xx | Brushed DC | H-bridge drivers |
| TB67xx | Brushless DC | Three-phase drivers |
| TB9xxx | Automotive | AEC-Q100 qualified |

---

## Common Series Reference

### Popular MOSFETs

| Part Number | Type | Vds | Rds(on) | Package |
|-------------|------|-----|---------|---------|
| TK024N60Z1 | N-ch | 600V | 24mOhm | TO-220SIS |
| TK057V60Z1 | N-ch | 600V | 57mOhm | TO-220SIS |
| TK170V65Z | N-ch | 650V | 170mOhm | DPAK |
| TPH4R606NH | N-ch | 60V | 4.6mOhm | TO-247 |
| TPC8107 | N-ch | 30V | 15mOhm | SOP-8 |
| SSM3K102TU | N-ch | 30V | 500mOhm | UFM |

### Popular Transistors

| Part Number | Type | Vceo | Ic | Package |
|-------------|------|------|-----|---------|
| 2SC5198 | NPN | 140V | 10A | TO-3P |
| 2SA1943 | PNP | 230V | 15A | TO-3P |
| 2SC5200 | NPN | 230V | 15A | TO-3P |
| 2SC1815 | NPN | 50V | 150mA | TO-92 |
| 2SA1015 | PNP | 50V | 150mA | TO-92 |

### Popular Optocouplers

| Part Number | Type | CTR | Speed | Package |
|-------------|------|-----|-------|---------|
| TLP127 | Darlington | 1000% | Low | DIP-4 |
| TLP185 | Transistor | 50-300% | 3.75kV | SOP-4 |
| TLP291 | Transistor | 50-600% | High | SOP-4 |
| TLP3910 | Photo-relay | N/A | Fast | SO-6 |
| TLP350 | IGBT driver | N/A | Fast | DIP-8 |

### Popular Motor Drivers

| Part Number | Type | Voltage | Current | Package |
|-------------|------|---------|---------|---------|
| TB6612FNG | Dual H-bridge | 15V | 1.2A avg | SSOP24 |
| TB67H450FNG | Brushed DC | 50V | 3.5A | HSOP8 |
| TB67S109AFTG | Stepper | 50V | 1.9A | QFN48 |

### Popular MCUs

| Part Number | Core | Flash | Speed | Package |
|-------------|------|-------|-------|---------|
| TMPM370FYFG | CM3 | 256KB | 80MHz | LQFP100 |
| TMPM382FSFG | CM3 | 128KB | 80MHz | LQFP64 |
| TMPM4G9F15FG | CM4 | 2MB | 200MHz | LQFP144 |

---

## Handler Implementation Notes

### Issues Found in Current Handler

1. **HashSet usage** (line 61): Should use `Set.of()` or `EnumSet` for immutability
2. **Missing TRANSISTOR in getSupportedTypes()**: Patterns exist for 2SC/2SA but type not in supported set
3. **Missing base IC type in getSupportedTypes()**: Patterns for IC (IGBTs, motor drivers, optocouplers) exist but base IC not declared
4. **Package extraction incomplete**: Only handles TPC/TPH/TMP, missing TK, TLP, SSM, TB, 2SC/2SA series
5. **Series extraction incomplete**: Missing TLP, 2SC, 2SA, TB series extraction
6. **extractSeries returns empty for optocouplers**: TLP series not handled

### Package Extraction Fix

```java
// Add TK series package extraction
if (upperMpn.startsWith("TK")) {
    // TK024N60Z1 - package in suffix after generation
    if (upperMpn.contains("Z")) return "TO-220SIS";
    if (upperMpn.endsWith("L") || upperMpn.endsWith("LQ")) return "DPAK";
    if (upperMpn.endsWith("S")) return "D2PAK";
}

// Add TLP optocoupler package extraction
if (upperMpn.startsWith("TLP")) {
    if (upperMpn.contains("SO6L") || upperMpn.contains("S06L")) return "SO-6";
    if (upperMpn.matches(".*\\(.*\\).*")) {
        // Has parentheses - likely SOP variant
        return "SOP-4";
    }
    return "DIP-4"; // Default for TLP
}

// Add SSM small signal package extraction
if (upperMpn.startsWith("SSM")) {
    if (upperMpn.endsWith("TU")) return "UFM";
    if (upperMpn.endsWith("F")) return "S-Mini";
    if (upperMpn.endsWith("FU")) return "USM";
}

// Add TB motor driver package extraction
if (upperMpn.startsWith("TB")) {
    if (upperMpn.contains("FNG")) return "SSOP24";
    if (upperMpn.contains("AFG")) return "QFN";
    if (upperMpn.contains("PG")) return "HTSSOP";
}
```

### Series Extraction Fix

```java
// Add TLP optocoupler series
if (upperMpn.startsWith("TLP")) return "TLP Series";

// Add transistor series
if (upperMpn.startsWith("2SC")) return "2SC Series";
if (upperMpn.startsWith("2SA")) return "2SA Series";
if (upperMpn.startsWith("2SB")) return "2SB Series";
if (upperMpn.startsWith("2SD")) return "2SD Series";

// Add digital transistor series
if (upperMpn.startsWith("RN")) return "RN Series";
if (upperMpn.startsWith("RP")) return "RP Series";

// Add voltage regulator series
if (upperMpn.startsWith("TAR")) return "TAR Series";
```

### Missing Pattern Registration

```java
// 2SK JIS N-channel MOSFETs (legacy series, still common)
registry.addPattern(ComponentType.MOSFET, "^2SK[0-9].*");
registry.addPattern(ComponentType.MOSFET_TOSHIBA, "^2SK[0-9].*");

// Missing digital transistors
registry.addPattern(ComponentType.TRANSISTOR, "^RN[0-9].*[A-Z]?$");
registry.addPattern(ComponentType.TRANSISTOR, "^RP[0-9].*[A-Z]?$");
```

### getSupportedTypes Fix

```java
@Override
public Set<ComponentType> getSupportedTypes() {
    // Use Set.of() for immutability
    return Set.of(
        ComponentType.MOSFET,
        ComponentType.MOSFET_TOSHIBA,
        ComponentType.TRANSISTOR,           // ADD - patterns exist
        ComponentType.IC,                   // ADD - patterns exist
        ComponentType.IGBT_TOSHIBA,
        ComponentType.MOTOR_DRIVER_TOSHIBA,
        ComponentType.GATE_DRIVER_TOSHIBA,
        ComponentType.OPTOCOUPLER_TOSHIBA,
        ComponentType.VOLTAGE_REGULATOR,
        ComponentType.VOLTAGE_REGULATOR_TOSHIBA,
        ComponentType.MICROCONTROLLER,
        ComponentType.MICROCONTROLLER_TOSHIBA
    );
}
```

---

## Related Files

- Handler: `manufacturers/ToshibaHandler.java`
- Component types: `MOSFET_TOSHIBA`, `IGBT_TOSHIBA`, `MOTOR_DRIVER_TOSHIBA`, `GATE_DRIVER_TOSHIBA`, `OPTOCOUPLER_TOSHIBA`, `VOLTAGE_REGULATOR_TOSHIBA`, `MICROCONTROLLER_TOSHIBA`

---

## Learnings and Edge Cases

- **JIS naming**: 2SA/2SB/2SC/2SD follow Japanese Industrial Standard for transistors
- **Complementary pairs**: 2SC5200/2SA1943 are matched PNP/NPN pairs for audio amplifiers
- **DTMOS**: Digital Trench MOS technology for improved switching efficiency
- **TLP numbering**: 3-digit (TLP127) typically older, 4-digit (TLP3910) typically newer products
- **hFE ranks**: Transistors sorted by gain (O, P, Q, R, Y grades) - same base part, different gain bins
- **Tape suffix variations**: L, L1, L3 indicate different reel quantities
- **Photocoupler variants**: Same base number with different CTR grades (A, B, C, D, GB, GR, GC)
- **Motor driver generations**: TB66xx (older) vs TB67xx (newer brushed DC) vs TB9xxx (automotive)
- **ARM MCU naming**: TXZ family uses TMP prefix with core indicator (M for ARM, V for RISC-V)

<!-- Add new learnings above this line -->
