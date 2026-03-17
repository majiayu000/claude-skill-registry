---
name: vicor
description: Vicor Corporation MPN encoding patterns for high-performance power modules, DC-DC converters, and ZVS regulators. Use when working with Vicor power components or VicorHandler.
---

# Vicor Corporation Manufacturer Skill

## Company Overview

Vicor Corporation is a leading manufacturer of high-performance modular power components. Their products are used in demanding applications including data centers, electric vehicles, aerospace, and industrial automation.

**Key Product Families:**
- **DCM** - DC-DC Converter Modules (isolated converters)
- **BCM** - Bus Converter Modules (fixed-ratio converters)
- **PRM** - PRM Regulator Modules (factorized power architecture)
- **VTM** - Voltage Transformation Modules (current multipliers)
- **NBM** - NBM Converter Modules (bidirectional converters)
- **PI33xx** - ZVS Buck Regulators
- **PI35xx** - Cool-Power ZVS Regulators

---

## MPN Structure

### Power Modules (DCM, BCM, PRM, VTM, NBM)

```
[PREFIX][SPEC][PACKAGE][RATINGS][OPTIONS]
   |      |      |        |        |
   |      |      |        |        +-- Options code (00, 01, etc.)
   |      |      |        +-- Current/power rating
   |      |      +-- Package type (T=ChiP, S=SiP, A=Advanced)
   |      +-- Voltage specification (input/output config)
   +-- Product family (DCM, BCM, PRM, VTM, NBM)
```

### PI Series (ZVS Regulators)

```
[PI][SERIES][VARIANT]-[OPTIONS]-[PACKAGE]
 |     |        |         |         |
 |     |        |         |         +-- Package code (LGIZ, QGIZ, etc.)
 |     |        |         +-- Options (00, 01, etc.)
 |     |        +-- Variant (01, 02, 23, etc.)
 |     +-- Series (33 or 35)
 +-- Prefix

```

---

## Example MPN Decoding

### DCM Series (DC-DC Converter Modules)

```
DCM3623T50D40A4T
|  |   | |  |  ||
|  |   | |  |  |+-- T = ChiP package variant
|  |   | |  |  +-- 4 = Revision/option
|  |   | |  +-- A = Package option
|  |   | +-- D40 = Output spec (40V DC)
|  |   +-- T50 = Transfer ratio/spec
|  +-- 3623 = Input/output voltage configuration
+-- DCM = DC-DC Converter Module
```

### BCM Series (Bus Converter Modules)

```
BCM48BT120T300A00
|  | || |  |   |
|  | || |  |   +-- 00 = Base options
|  | || |  +-- A = Revision
|  | || +-- T300 = Current spec (300A peak)
|  | |+-- T = Transfer ratio code
|  | +-- B = Version
|  +-- 48 = Input voltage (48V)
+-- BCM = Bus Converter Module
```

### PRM Series (PRM Regulator Modules)

```
PRM48BH480T200A00
|  | ||  ||   |
|  | ||  ||   +-- 00 = Options
|  | ||  |+-- A = Version
|  | ||  +-- T200 = Current spec
|  | |+-- 480 = Power rating code
|  | +-- H = High efficiency variant
|  +-- 48 = Input voltage (48V)
+-- PRM = PRM Regulator Module
```

### VTM Series (Voltage Transformation Modules)

```
VTM48EH040T025A00
|  | ||  ||   |
|  | ||  ||   +-- 00 = Options
|  | ||  |+-- A = Version
|  | ||  +-- T025 = Current multiplier spec
|  | |+-- 040 = Output voltage code
|  | +-- H = High efficiency
|  +-- 48 = Input voltage (48V)
+-- VTM = Voltage Transformation Module
```

### NBM Series (NBM Converter Modules)

```
NBM2317S54E1560T00
|  |   | || |   |
|  |   | || |   +-- 00 = Options
|  |   | || +-- T = Package type
|  |   | |+-- 1560 = Power/current spec
|  |   | +-- E = Efficiency/version
|  |   +-- S54 = Specification code
|  +-- 2317 = Model/configuration
+-- NBM = NBM Converter Module
```

### PI33xx Series (ZVS Buck Regulators)

```
PI3301-00-LGIZ
|  | | |   |
|  | | |   +-- LGIZ = LGA package, industrial temp, Z suffix
|  | | +-- 00 = Base variant (no options)
|  | +-- 01 = Specific model variant
|  +-- 33 = Series (ZVS Buck)
+-- PI = Vicor Power IC prefix
```

### PI35xx Series (Cool-Power ZVS Regulators)

```
PI3523-00-LGIZ
|  | | |   |
|  | | |   +-- LGIZ = LGA package, industrial temp, Z suffix
|  | | +-- 00 = Base variant
|  | +-- 23 = Model variant
|  +-- 35 = Series (Cool-Power ZVS)
+-- PI = Vicor Power IC prefix
```

---

## Package Codes

### Power Module Packages

| Indicator | Package | Description |
|-----------|---------|-------------|
| T | ChiP | Vicor Converter housed in Package |
| S | SiP | System in Package |
| A | ChiP-A | Advanced ChiP package |
| M | MCM | Multi-Chip Module |

### PI Series Package Codes

| Code | Package | Description |
|------|---------|-------------|
| LG | LGA | Land Grid Array |
| LGIZ | LGA | LGA, Industrial temp, RoHS |
| QG | QFN | Quad Flat No-Lead |
| QGIZ | QFN | QFN, Industrial temp, RoHS |
| BG | BGA | Ball Grid Array |

---

## Supported Component Types

From `VicorHandler.getSupportedTypes()`:

| ComponentType | Description |
|---------------|-------------|
| `VOLTAGE_REGULATOR` | Primary type for all Vicor power modules |
| `IC` | Generic IC type for power ICs |

---

## Series Extraction Rules

The handler extracts series prefixes as follows:

| MPN Prefix | Extracted Series | Product Family |
|------------|------------------|----------------|
| `DCM*` | `DCM` | DC-DC Converter Modules |
| `BCM*` | `BCM` | Bus Converter Modules |
| `PRM*` | `PRM` | PRM Regulator Modules |
| `VTM*` | `VTM` | Voltage Transformation Modules |
| `NBM*` | `NBM` | NBM Converter Modules |
| `PI33xx*` | `PI33` | ZVS Buck Regulators |
| `PI35xx*` | `PI35` | Cool-Power ZVS Regulators |

---

## Package Code Extraction Rules

### PI Series

1. Look for hyphenated suffix pattern: `-[PACKAGE][IZ]?$`
2. Map package codes:
   - `LG` or `LGIZ` -> `LGA`
   - `QG` or `QGIZ` -> `QFN`
   - `BG` -> `BGA`
3. If no hyphen found, return empty (no package suffix)

### Power Modules (DCM, BCM, PRM, VTM, NBM)

1. Look for suffix pattern at end of MPN
2. First character of suffix indicates package family:
   - `T` -> `ChiP`
   - `S` -> `SiP`
   - `A` -> `ChiP-A`
   - `M` -> `MCM`
3. Default to `ChiP` for power modules without clear suffix

---

## Replacement Logic

The handler's `isOfficialReplacement()` method uses these rules:

1. **Same series required**: Parts must be from the same product family (DCM, BCM, etc.)
2. **Power modules**: Compare core specification (voltage/current configuration)
   - DCM/NBM: First 4 digits after prefix (e.g., `DCM3623` core spec is `3623`)
   - BCM/PRM/VTM: Voltage + suffix + rating (e.g., `48BT120`)
3. **PI series**: Compare base part number (everything before first hyphen)
   - `PI3301-00-LGIZ` base is `PI3301`
   - Same base = compatible (may differ in package/options)

---

## Pattern Reference

### Regex Patterns from Handler

| Series | Pattern | Example Match |
|--------|---------|---------------|
| DCM | `^DCM[0-9]{4}[A-Z0-9]+$` | DCM3623T50D40A4T |
| BCM | `^BCM[0-9]{2,3}[A-Z]{2}[0-9]+[A-Z0-9]*$` | BCM48BT120T300A00 |
| PRM | `^PRM[0-9]{2}[A-Z]{2}[0-9]+[A-Z0-9]*$` | PRM48BH480T200A00 |
| VTM | `^VTM[0-9]{2}[A-Z]{2}[0-9]+[A-Z0-9]*$` | VTM48EH040T025A00 |
| NBM | `^NBM[0-9]{4}[A-Z][0-9]+[A-Z0-9]*$` | NBM2317S54E1560T00 |
| PI33xx | `^PI33[0-9]{2}(-[A-Z0-9]+)*$` | PI3301-00-LGIZ |
| PI35xx | `^PI35[0-9]{2}(-[A-Z0-9]+)*$` | PI3523-00-LGIZ |

---

## Common MPN Examples

### DC-DC Converter Modules (DCM)

| MPN | Input | Output | Notes |
|-----|-------|--------|-------|
| DCM3623T50D40A4T | 36V-75V | 40V | Isolated DC-DC |
| DCM3714T40D40A4T | 36V-75V | 40V | Different config |

### Bus Converter Modules (BCM)

| MPN | Input | Notes |
|-----|-------|-------|
| BCM48BT120T300A00 | 48V | 1/4 ratio bus converter |
| BCM384BT120T300A00 | 384V | High voltage input |

### ZVS Regulators (PI Series)

| MPN | Series | Package | Notes |
|-----|--------|---------|-------|
| PI3301-00-LGIZ | PI33xx | LGA | ZVS Buck, industrial |
| PI3523-00-LGIZ | PI35xx | LGA | Cool-Power ZVS |
| PI3523-00-QGIZ | PI35xx | QFN | Same part, QFN package |

---

## Related Files

- Handler: `manufacturers/VicorHandler.java`
- Component types: `VOLTAGE_REGULATOR`, `IC`

---

## Learnings & Edge Cases

- **ChiP package default**: Power modules without a clear package indicator default to `ChiP` (Converter housed in Package), Vicor's signature dense power module package
- **BCM voltage range**: BCM modules support input voltages from 2-3 digits (48V to 384V), reflected in the pattern `BCM[0-9]{2,3}`
- **PI series hyphenation**: PI series MPNs can have multiple hyphen-separated segments (e.g., `PI3301-00-LGIZ`), handled by `(-[A-Z0-9]+)*` pattern
- **No manufacturer-specific ComponentTypes**: Unlike handlers for TI or STM, VicorHandler uses only generic types (`VOLTAGE_REGULATOR`, `IC`), not Vicor-specific types like `VOLTAGE_REGULATOR_VICOR`
- **Core spec extraction complexity**: Different product families have different core specification formats:
  - DCM/NBM: 4 digits after prefix
  - BCM/PRM/VTM: voltage + 2 letters + 3 digits (e.g., `48BT120`)
- **Package suffix detection**: For power modules, the handler looks for pattern `[A-Z]([0-9]{2,3})[A-Z]([0-9]{2})$` to find where suffix begins
- **Empty package for bare PI series**: PI series parts without hyphens (if they exist) return empty string for package code

<!-- Add new learnings above this line -->
