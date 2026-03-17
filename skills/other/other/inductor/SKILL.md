---
name: inductor
description: Use when working with inductor components - adding inductor patterns, parsing inductor MPNs, extracting inductance values, current ratings, or package codes from inductor part numbers.
---

# Inductor Component Skill

Guidance for working with inductor components in the lib-electronic-components library.

## Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Murata | `MurataHandler` | `LQG...`, `LQH...`, `LQW...`, `LQM...` | `LQG15HS2N2S02D` |
| TDK | `TDKHandler` | `MLF#...`, `NLV...`, `SDR...` | `MLF2012A100KT000` |
| Bourns | `BournsHandler` | `SRR...`, `SRN...`, `SRP...` | `SRR1208-100M` |

## ComponentTypes

```java
// Base type
ComponentType.INDUCTOR

// Manufacturer-specific types
ComponentType.INDUCTOR_CHIP_MURATA
ComponentType.INDUCTOR_POWER_MURATA
ComponentType.INDUCTOR_CHIP_TDK
ComponentType.INDUCTOR_POWER_TDK
ComponentType.INDUCTOR_CHIP_BOURNS
ComponentType.INDUCTOR_THT_BOURNS
ComponentType.INDUCTOR_CHIP_YAGEO
ComponentType.INDUCTOR_CHIP_COILCRAFT
ComponentType.INDUCTOR_PANASONIC
```

## MPN Structure

### Murata LQG Series (Chip Inductor)
```
LQG 15 HS 2N2 S 02 D
│   │  │  │   │ │  │
│   │  │  │   │ │  └── Packaging (D=180mm Reel)
│   │  │  │   │ └───── Special code
│   │  │  │   └──────── Tolerance (S=±0.3nH)
│   │  │  └──────────── Value (2N2=2.2nH)
│   │  └─────────────── Series (HS=High Frequency)
│   └────────────────── Size (15=0402)
└────────────────────── Family (LQG=Chip)
```

### TDK MLF Series
```
MLF 2012 A 100 K T 000
│   │    │ │   │ │ │
│   │    │ │   │ │ └── Special code
│   │    │ │   │ └──── Packaging (T=Taping)
│   │    │ │   └────── Tolerance (K=±10%)
│   │    │ └────────── Value (100=10µH)
│   │    └──────────── Type (A=Standard)
│   └───────────────── Size (2012=0805)
└────────────────────── Series (MLF=Multilayer)
```

## Inductor Types

| Type | Description | Applications |
|------|-------------|--------------|
| Chip | Multilayer ceramic/ferrite | RF, filtering |
| Power | Shielded/unshielded wound | DC-DC, power |
| Common Mode Choke | Coupled inductors | EMI filtering |
| Ferrite Bead | Lossy inductor | Noise suppression |

## Related ComponentTypes for EMI

```java
ComponentType.FERRITE_BEAD_TDK
ComponentType.FERRITE_BEAD_YAGEO
ComponentType.EMI_FILTER_MURATA
ComponentType.EMI_FILTER_TDK
ComponentType.COMMON_MODE_CHOKE_MURATA
ComponentType.COMMON_MODE_CHOKE_TDK
```

## Adding New Inductor Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.INDUCTOR, "^NEWIND[0-9]{4}.*");
registry.addPattern(ComponentType.INDUCTOR_CHIP_MANUFACTURER, "^NEWIND[0-9]{4}.*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.INDUCTOR);
types.add(ComponentType.INDUCTOR_CHIP_MANUFACTURER);
```

## Value Notation

| Notation | Value |
|----------|-------|
| 2N2 | 2.2 nH |
| 10N | 10 nH |
| R10 | 0.10 µH |
| 100 | 10 µH (10 × 10^0) |
| 101 | 100 µH (10 × 10^1) |
| 102 | 1000 µH (10 × 10^2) |

## Murata Size Codes

| Code | Imperial | Metric |
|------|----------|--------|
| 15 | 0402 | 1005 |
| 18 | 0603 | 1608 |
| 21 | 0805 | 2012 |
| 31 | 1206 | 3216 |
---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
