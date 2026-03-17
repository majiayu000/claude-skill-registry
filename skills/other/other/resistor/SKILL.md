---
name: resistor
description: Use when working with resistor components - adding resistor patterns, parsing resistor MPNs, extracting resistance values, tolerance, or package codes from resistor part numbers.
---

# Resistor Component Skill

Guidance for working with resistor components in the lib-electronic-components library.

## Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Vishay | `VishayHandler` | `CRCW####...`, `RCG#...`, `WSL#...` | `CRCW060310K0FKEA` |
| Yageo | `YageoHandler` | `RC####...`, `RT####...`, `RL####...` | `RC0603FR-0710KL` |
| Panasonic | `PanasonicHandler` | `ERJ...`, `ERJP...`, `ERJG...` | `ERJ-3EKF1001V` |
| Bourns | `BournsHandler` | `CR...`, `CRM...`, `CRH...` | `CR0603-FX-1001ELF` |

## ComponentTypes

```java
// Base type
ComponentType.RESISTOR

// Manufacturer-specific types
ComponentType.RESISTOR_CHIP_VISHAY
ComponentType.RESISTOR_THT_VISHAY
ComponentType.RESISTOR_CHIP_YAGEO
ComponentType.RESISTOR_THT_YAGEO
ComponentType.RESISTOR_CHIP_PANASONIC
ComponentType.RESISTOR_CHIP_BOURNS
```

## MPN Structure

### Vishay CRCW Series
```
CRCW 0603 10K0 F K EA
│    │    │    │ │ │
│    │    │    │ │ └── Packaging (EA=Tape & Reel)
│    │    │    │ └──── Termination (K=Standard)
│    │    │    └────── Tolerance (F=1%, J=5%)
│    │    └─────────── Value (10K0 = 10kΩ)
│    └──────────────── Size (0603)
└───────────────────── Series
```

### Yageo RC Series
```
RC 0603 FR -07 10K L
│  │    │   │  │   │
│  │    │   │  │   └── Packaging (L=7" Reel)
│  │    │   │  └────── Value (10K = 10kΩ)
│  │    │   └───────── TCR Code (07=±100ppm)
│  │    └───────────── Tolerance (F=1%, J=5%)
│  └────────────────── Size (0603)
└───────────────────── Series (RC=Thick Film)
```

## Key Handler Methods

### Extract Package Code
```java
// Returns "0603" from "CRCW060310K0FKEA"
handler.extractPackageCode("CRCW060310K0FKEA");

// Returns "0805" from "RC0805JR-0710KL"
handler.extractPackageCode("RC0805JR-0710KL");
```

### Extract Series
```java
// Returns "CRCW" from Vishay
handler.extractSeries("CRCW060310K0FKEA");

// Returns "RC0603" from Yageo (includes size)
handler.extractSeries("RC0603FR-0710KL");
```

## Adding New Resistor Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.RESISTOR, "^NEWPFX[0-9]{4}.*");
registry.addPattern(ComponentType.RESISTOR_CHIP_MANUFACTURER, "^NEWPFX[0-9]{4}.*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.RESISTOR);
types.add(ComponentType.RESISTOR_CHIP_MANUFACTURER);
```

3. Implement `matches()` for direct pattern matching (faster than regex fallback)

## Similarity Calculation

`ResistorSimilarityCalculator` compares:
- Resistance value (extracted from MPN)
- Package size (0402, 0603, 0805, etc.)
- Tolerance class (1%, 5%, etc.)
- Power rating (if determinable)

## Common Package Sizes

| Code | Metric | Size (mm) |
|------|--------|-----------|
| 0402 | 1005 | 1.0 x 0.5 |
| 0603 | 1608 | 1.6 x 0.8 |
| 0805 | 2012 | 2.0 x 1.25 |
| 1206 | 3216 | 3.2 x 1.6 |
| 2512 | 6332 | 6.3 x 3.2 |
---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
