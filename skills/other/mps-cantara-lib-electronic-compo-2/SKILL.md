---
name: mps
description: Monolithic Power Systems MPN encoding patterns, suffix decoding, and handler guidance. Use when working with MPS power components or MPSHandler.
---

# Monolithic Power Systems (MPS) Manufacturer Skill

## Manufacturer Overview

MPS (Monolithic Power Systems) specializes in high-performance power management solutions. The company is known for:

- **DC-DC Converters**: Step-down (buck), step-up (boost), and SEPIC converters
- **LED Drivers**: Constant-current drivers for backlighting and general illumination
- **Motor Drivers**: Stepper and brushless DC motor controllers
- **Power Modules**: Integrated solutions with inductor and passives included
- **Automotive-grade variants**: AEC-Q100 qualified parts (MPQ series)

---

## MPN Structure

MPS MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][PACKAGE][-SUFFIX]
   |       |        |        |        |
   |       |        |        |        +-- Optional: LF=Lead-free, Z=RoHS, AEC1=Automotive
   |       |        |        +-- 2-letter package code (EN, DN, GQ, etc.)
   |       |        +-- Optional variant letter
   |       +-- 3-4 digit part number
   +-- MP, MPQ (automotive), or MPM (module)
```

### Prefix Meanings

| Prefix | Category | Pattern | Description |
|--------|----------|---------|-------------|
| MP1 | Step-Down | `MP1xxx` | Entry-level DC-DC converters |
| MP2 | Step-Down/LDO | `MP2xxx` | Buck converters and LDOs |
| MP3 | LED Driver | `MP3xxx` | LED driver ICs |
| MP4 | High-Current | `MP4xxx` | High-current step-down converters |
| MP5 | Step-Up/SEPIC | `MP5xxx` | Boost and SEPIC converters |
| MP6 | Motor Driver | `MP6xxx` | Stepper/BLDC motor drivers |
| MP7 | Power Switch | `MP7xxx` | Load switches and eFuses |
| MP8 | Multi-Channel | `MP8xxx` | PMICs with multiple outputs |
| MP9 | High-Voltage | `MP9xxx` | High-voltage DC-DC converters |
| MPQ | Automotive | `MPQxxxx` | AEC-Q100 qualified versions |
| MPM | Module | `MPMxxxx` | Power modules with inductor |

---

## Example Decoding

```
MP1584EN-LF-Z
|  |   ||  | |
|  |   ||  | +-- Z = RoHS compliant
|  |   ||  +-- LF = Lead-free
|  |   |+-- EN = SOIC-8E package
|  |   +-- (no variant letter)
|  +-- 1584 = 3A step-down converter
+-- MP = Standard MPS prefix

MPQ4560GQ-AEC1-LF-Z
|  |   ||    |
|  |   ||    +-- AEC1-LF-Z = Automotive + Lead-free + RoHS
|  |   |+-- GQ = QFN package
|  |   +-- (no variant)
|  +-- 4560 = 2A step-down converter
+-- MPQ = Automotive-grade prefix

MPM3610GQV-Z
|  |   |  |
|  |   |  +-- Z = RoHS
|  |   +-- GQV = QFN variant package
|  +-- 3610 = 1.2A power module
+-- MPM = Power module prefix
```

---

## Package Codes

### QFN Variants

| Code | Package | Notes |
|------|---------|-------|
| GQ | QFN | Standard QFN |
| GL | QFN | QFN variant |
| GR | QFN | QFN variant |
| GS | QFN-EP | QFN with exposed pad |
| GT | QFN | QFN variant |
| GU | QFN | QFN variant |
| GV | QFN | QFN variant |
| GN | QFN | QFN variant |

### WLCSP (Wafer-Level Chip Scale Package)

| Code | Package | Notes |
|------|---------|-------|
| GF | WLCSP | Ultra-small form factor |
| GW | WLCSP | WLCSP variant |

### SOIC/SOP Variants

| Code | Package | Notes |
|------|---------|-------|
| EN | SOIC-8E | Extended SOIC-8 |
| DN | SO-8 | Standard SOIC-8 |
| EC | SOIC-8 | SOIC-8 variant |
| EF | SOIC-8 | SOIC-8 variant |
| EG | TSSOP-8 | Thin profile |
| EH | TSSOP-16 | 16-pin TSSOP |
| EJ | SOP-8 | SOP-8 variant |
| EK | MSOP-8 | Mini SOIC-8 |
| EL | MSOP-10 | Mini SOIC-10 |

### SOT Variants

| Code | Package | Notes |
|------|---------|-------|
| DF | TSOT-23 | Thin SOT-23 |
| DG | TSOT-23-5 | 5-pin thin SOT |
| DH | SOT-23-8 | 8-pin SOT-23 |

### DFN Variants

| Code | Package | Notes |
|------|---------|-------|
| DJ | DFN | Standard DFN |
| DK | DFN-10 | 10-pin DFN |
| DL | DFN-12 | 12-pin DFN |

### Module Packages

| Code | Package | Notes |
|------|---------|-------|
| MN | QFN-Module | Module with QFN footprint |
| MF | Module-BGA | BGA module package |

### Power Packages

| Code | Package | Notes |
|------|---------|-------|
| HF | TO-263 | D2PAK power package |
| HN | TO-220 | Through-hole power |

---

## Component Type Mapping

The MPSHandler supports these ComponentTypes:

| MPN Pattern | ComponentType | Description |
|-------------|---------------|-------------|
| `MP1xxx`, `MP2xxx`, `MP4xxx`, `MP5xxx`, `MP7xxx`, `MP8xxx`, `MP9xxx` | VOLTAGE_REGULATOR | DC-DC converters and regulators |
| `MPQxxxx` (except 3xxx/6xxx) | VOLTAGE_REGULATOR | Automotive DC-DC converters |
| `MPMxxxx` | VOLTAGE_REGULATOR | Power modules |
| `MP3xxx` | LED_DRIVER | LED driver ICs |
| `MPQ3xxx` | LED_DRIVER | Automotive LED drivers |
| `MP6xxx` | MOTOR_DRIVER | Motor controller ICs |
| `MPQ6xxx` | MOTOR_DRIVER | Automotive motor drivers |
| All MPS parts | IC | Base IC type for all parts |

---

## Series Extraction Rules

The handler extracts series as follows:

```java
// MPM series: returns "MPM"
"MPM3610GQV-Z" -> "MPM"

// MPQ series: returns "MPQ"
"MPQ4560GQ-AEC1-LF-Z" -> "MPQ"

// Standard MP[1-9]xxx: returns first 3 characters
"MP1584EN-LF-Z" -> "MP1"
"MP2307DN-LF-Z" -> "MP2"
"MP6500HF" -> "MP6"
```

### Series Descriptions

| Series | Category |
|--------|----------|
| MP1 | Step-Down Converters |
| MP2 | Step-Down/LDO Converters |
| MP3 | LED Drivers |
| MP4 | High-Current Step-Down |
| MP5 | Step-Up/SEPIC Converters |
| MP6 | Motor Drivers |
| MP7 | Power Switches |
| MP8 | Multi-Channel PMIC |
| MP9 | High-Voltage Converters |
| MPQ | Automotive Grade |
| MPM | Power Modules |

---

## Package Code Extraction Rules

The handler extracts package codes with this logic:

1. Remove common suffixes: `-LF-Z`, `-Z`, `-LF`, `-AEC1`, etc.
2. Match pattern: `MP[A-Z]?[0-9]{3,4}([A-Z]{2}).*`
3. Look up the 2-letter code in the PACKAGE_CODES map
4. Return the mapped package name or the raw code

```java
// Example extraction:
"MP1584EN-LF-Z"
  -> Remove suffix: "MP1584EN"
  -> Match: group(1) = "EN"
  -> Lookup: PACKAGE_CODES.get("EN") = "SOIC-8E"

"MPQ4560GQ-AEC1-LF-Z"
  -> Remove suffix: "MPQ4560GQ"
  -> Match: group(1) = "GQ"
  -> Lookup: PACKAGE_CODES.get("GQ") = "QFN"
```

---

## Official Replacement Logic

The handler identifies official replacements in two scenarios:

### Same Base Part, Different Package
```
MP1584EN <-> MP1584DN   // Same part, different package (SOIC-8E vs SO-8)
```

### Automotive Equivalents (MPQ vs MP)
```
MP4560GQ <-> MPQ4560GQ  // Consumer vs automotive grade
```

The `isOfficialReplacement()` method checks:
1. Automotive equivalents (MPQ ↔ MP with same 4-digit number)
2. Same series and same base part number

---

## Automotive Detection

MPS uses two indicators for automotive-grade parts:

```java
// Method: isAutomotiveGrade(String mpn)

// 1. MPQ prefix indicates automotive
"MPQ4560GQ-LF-Z" -> true

// 2. -AEC suffix indicates automotive qualification
"MP4560GQ-AEC1-LF-Z" -> true

// Standard consumer parts
"MP4560GQ-LF-Z" -> false
```

---

## Common Part Examples

### Step-Down Converters (Buck)

| MPN | Description | Key Specs |
|-----|-------------|-----------|
| MP1584EN-LF-Z | 3A step-down | 4.5-28V input, SOT-8E |
| MP2307DN-LF-Z | 3A step-down | 4.75-23V input, SO-8 |
| MP2359DJ-LF-Z | 1.2A step-down | 4.5-24V input, DFN |
| MP4560DN-LF-Z | 2A step-down | 4.5-55V input, SO-8 |

### LED Drivers

| MPN | Description | Key Specs |
|-----|-------------|-----------|
| MP3302DJ-LF-Z | LED driver | 2.7-6V input, DFN |
| MP3394GS-Z | 4-channel LED | QFN-EP |

### Motor Drivers

| MPN | Description | Key Specs |
|-----|-------------|-----------|
| MP6500HF | Stepper driver | 2.5A, TO-263 |
| MP6513GQ-Z | 3-phase BLDC | QFN |

### Power Modules

| MPN | Description | Key Specs |
|-----|-------------|-----------|
| MPM3610GQV-Z | 1.2A module | Integrated inductor |
| MPM3833GQV-Z | 3.3A module | Integrated inductor |

---

## Handler Implementation Notes

### Supported Types Declaration

The handler uses `Set.of()` for immutable type set:

```java
public Set<ComponentType> getSupportedTypes() {
    return Set.of(
            ComponentType.IC,
            ComponentType.VOLTAGE_REGULATOR,
            ComponentType.LED_DRIVER,
            ComponentType.MOTOR_DRIVER
    );
}
```

### Pattern Registration

Patterns are registered for both specific and base types:

```java
// MP3xxx registered for both LED_DRIVER and IC
registry.addPattern(ComponentType.LED_DRIVER, "^MP3[0-9]{3}[A-Z0-9-]*$");
registry.addPattern(ComponentType.IC, "^MP3[0-9]{3}[A-Z0-9-]*$");
```

### matches() Implementation

The handler overrides `matches()` for efficient direct pattern checking:

```java
// Direct pattern checks by type for performance
switch (type) {
    case VOLTAGE_REGULATOR:
        return isVoltageRegulator(upperMpn);
    case LED_DRIVER:
        return isLEDDriver(upperMpn);
    case MOTOR_DRIVER:
        return isMotorDriver(upperMpn);
    case IC:
        return isMPSPart(upperMpn);
}
```

---

## Related Files

- Handler: `manufacturers/MPSHandler.java`
- Component types: `VOLTAGE_REGULATOR`, `LED_DRIVER`, `MOTOR_DRIVER`, `IC`
- Test file: `handlers/MPSHandlerTest.java` (if exists)

---

## Learnings & Edge Cases

- **MPQ vs MP**: The automotive variant MPQ has a 4-digit part number (MPQ4560) while standard MP uses 4 digits after the prefix character (MP4560). This is a 1-character offset when extracting the numeric part.
- **AEC suffix**: Parts can be automotive without MPQ prefix if they have `-AEC1` suffix. Always check both.
- **Package code position**: Package codes come immediately after the part number digits, before any hyphens. The handler strips `-LF-Z` and similar suffixes before extraction.
- **Module prefix MPM**: Power modules have their own prefix and are different from standard MP parts - they include an integrated inductor.
- **Series overlap**: MP6xxx (motor drivers) and MPQ6xxx are the same - both are motor drivers. Same for MP3xxx/MPQ3xxx (LED drivers). The MPQ prefix only adds automotive qualification.
- **getSupportedTypes() uses Set.of()**: The handler correctly uses immutable Set.of() instead of HashSet.
- **No manufacturer-specific types**: Unlike some handlers, MPS doesn't define manufacturer-specific ComponentTypes like `VOLTAGE_REGULATOR_MPS`. It uses the base types directly.

<!-- Add new learnings above this line -->
