---
name: semiconductor
description: Use when working with discrete semiconductor components - diodes, transistors, MOSFETs, IGBTs. Includes adding patterns, parsing MPNs, extracting voltage/current ratings, and package codes.
---

# Semiconductor Component Skill

Guidance for working with discrete semiconductor components (diodes, transistors, MOSFETs) in the lib-electronic-components library.

## Diodes

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Vishay | `VishayHandler` | `1N4###`, `1N5###`, `BAT#`, `BZX#` | `1N4007`, `BAT54S` |
| ON Semi | `OnSemiHandler` | `1N47##`, `MUR###` | `1N4742A` |
| Diodes Inc | `DiodesIncHandler` | `1N#`, `BAV#`, `BAS#` | `1N4148W` |
| Nexperia | `NexteriaHandler` | `BZX#`, `BAT#`, `BAV#` | `BZX84C5V1` |

### ComponentTypes

```java
ComponentType.DIODE
ComponentType.DIODE_VISHAY
ComponentType.DIODE_ON
ComponentType.DIODE_ROHM
```

### Common Diode Series

| Series | Type | Typical Specs |
|--------|------|---------------|
| 1N400x | Rectifier | 1A, 50-1000V |
| 1N5400 | Rectifier | 3A, 50-1000V |
| 1N4148 | Signal | 100mA, 75V |
| 1N47xx | Zener | Various voltages |
| BAT54 | Schottky | 200mA, 30V |
| BZX84 | Zener SMD | Various voltages |

## Transistors

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Vishay | `VishayHandler` | `2N####`, `BC###` | `2N2222A`, `BC547B` |
| ON Semi | `OnSemiHandler` | `2N####`, `BC###`, `MMBT#` | `MMBT3904` |
| Nexperia | `NexteriaHandler` | `PMBT#`, `PBSS#` | `PMBT2222A` |

### ComponentTypes

```java
ComponentType.TRANSISTOR
ComponentType.TRANSISTOR_VISHAY
ComponentType.TRANSISTOR_NXP
ComponentType.BIPOLAR_TRANSISTOR_NEXPERIA
```

### Common Transistor Series

| Series | Type | Typical Use |
|--------|------|-------------|
| 2N2222 | NPN | General purpose |
| 2N3904 | NPN | Low power |
| 2N3906 | PNP | Low power |
| BC547 | NPN | General purpose SMD |
| MMBT3904 | NPN | SMD version of 2N3904 |

## MOSFETs

### Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Infineon | `InfineonHandler` | `IRF#`, `IRL#`, `IRFP#`, `IRFB#` | `IRF540N`, `IRL3803` |
| Vishay | `VishayHandler` | `SI#`, `SIS#`, `SIR#` | `SI2302CDS` |
| ON Semi | `OnSemiHandler` | `FQP#`, `NTD#` | `FQP30N06L` |
| ST | `STHandler` | `STF#`, `STP#`, `STD#` | `STP55NF06` |
| Nexperia | `NexteriaHandler` | `PMV#`, `PSMN#` | `PMV45EN` |
| Toshiba | `ToshibaHandler` | `TPC#`, `TPN#` | `TPC8107` |
| ROHM | `RohmHandler` | `RQ#`, `RGT#` | `RQ5E050AJ` |

### ComponentTypes

```java
ComponentType.MOSFET
ComponentType.MOSFET_INFINEON
ComponentType.MOSFET_VISHAY
ComponentType.MOSFET_ONSEMI
ComponentType.MOSFET_ST
ComponentType.MOSFET_NEXPERIA
ComponentType.MOSFET_TOSHIBA
ComponentType.MOSFET_ROHM
ComponentType.MOSFET_NXP
ComponentType.MOSFET_DIODES
```

### MPN Structure - Infineon IRF Series
```
IRF 540 N
│   │   │
│   │   └── Package (N=TO-220, S=D2PAK, L=TO-262)
│   └────── Part number (voltage/current encoding)
└────────── Series (IRF=Standard, IRL=Logic Level)
```

### MOSFET Key Parameters

| Parameter | Description |
|-----------|-------------|
| Vds | Drain-Source Voltage |
| Rds(on) | On-Resistance |
| Id | Continuous Drain Current |
| Qg | Total Gate Charge |

## IGBTs

### ComponentTypes

```java
ComponentType.IGBT_INFINEON
ComponentType.IGBT_ONSEMI
ComponentType.IGBT_TOSHIBA
```

### Patterns
- Infineon: `IKP#`, `IKW#`
- Toshiba: `GT#`

## Adding New Semiconductor Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.MOSFET, "^NEWMOS[0-9].*");
registry.addPattern(ComponentType.MOSFET_MANUFACTURER, "^NEWMOS[0-9].*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.MOSFET);
types.add(ComponentType.MOSFET_MANUFACTURER);
```

## Similarity Calculators

- `DiodeSimilarityCalculator` - Compares voltage, current, type (rectifier/Schottky/Zener)
- `TransistorSimilarityCalculator` - Compares hFE, Vce, Ic
- `MosfetSimilarityCalculator` - Compares Vds, Rds(on), Id, package

## Common Packages

| Package | Description |
|---------|-------------|
| TO-220 | Through-hole power |
| TO-247 | High power |
| D2PAK | SMD power |
| SOT-23 | Small SMD |
| SOT-223 | Medium SMD |
| DPAK | SMD power |

---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
