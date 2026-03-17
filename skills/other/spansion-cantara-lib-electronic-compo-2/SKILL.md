---
name: spansion
description: Spansion (now Infineon) MPN encoding patterns for Flash memory and MCUs. Use when working with Spansion components or SpansionHandler.
---

# Spansion Manufacturer Skill

## Company Overview

Spansion was a leading manufacturer of Flash memory and microcontrollers, formed as a joint venture between AMD and Fujitsu in 2003. The company specialized in:

- **NOR Flash Memory** - Parallel and serial NOR Flash for code storage
- **NAND Flash Memory** - SLC and MLC NAND for data storage
- **Microcontrollers** - FM3 and FM4 ARM Cortex-based MCUs

**Acquisition History:**
- 2015: Acquired by Cypress Semiconductor
- 2020: Cypress acquired by Infineon Technologies
- Legacy Spansion parts are now manufactured under Infineon's brand

---

## MPN Structure

Spansion MPNs follow product-family-specific structures:

### NOR Flash Memory (S25, S29)

```
[PREFIX][FAMILY][DENSITY][SPEED][CONFIG][PACKAGE]
   │       │        │       │      │       │
   │       │        │       │      │       └── Package code (F, T, V, S, W, N, L, P)
   │       │        │       │      └── Configuration/feature code
   │       │        │       └── Speed grade
   │       │        └── Memory density (128=128Mbit, 256=256Mbit)
   │       └── Memory family (FL=Serial, GL=Parallel)
   └── S = Spansion prefix
```

### NAND Flash Memory (S34ML, S35ML)

```
[PREFIX][FAMILY][DENSITY][CONFIG][PACKAGE]
   │       │        │       │       │
   │       │        │       │       └── Package code
   │       │        │       └── Configuration
   │       │        └── Density in Gbits
   │       └── ML = Multi-Level/Single-Level NAND
   └── S34/S35 = NAND prefix
```

### Microcontrollers (MB9)

```
[PREFIX][FAMILY][VARIANT][SIZE][PACKAGE]
   │       │       │       │      │
   │       │       │       │      └── Package code
   │       │       │       └── Flash/RAM size indicator
   │       │       └── Feature variant (A, B, etc.)
   │       └── Family letter
   └── MB9 = FM MCU prefix
```

---

## Product Families

### NOR Flash Memory

| Pattern | Family | Description |
|---------|--------|-------------|
| S29AL | Parallel NOR | Low-density parallel NOR |
| S29GL | Parallel NOR | High-density parallel NOR (GL=GLUE Logic) |
| S25FL | Serial NOR | Standard serial NOR (SPI) |
| S25FS | Serial NOR | High-performance serial NOR |

### NAND Flash Memory

| Pattern | Family | Description |
|---------|--------|-------------|
| S34ML | SLC NAND | Single-Level Cell NAND (higher endurance) |
| S35ML | MLC NAND | Multi-Level Cell NAND (higher density) |

### Microcontrollers

| Pattern | Family | Core | Description |
|---------|--------|------|-------------|
| MB9AF | FM3 | ARM Cortex-M3 | General purpose MCU |
| MB9BF | FM4 | ARM Cortex-M4 | High performance MCU |

### Interface ICs

| Pattern | Type | Description |
|---------|------|-------------|
| GL850 | USB Hub | USB 2.0 Hub Controller |
| FL1K | USB Controller | USB Flash Controller |

---

## Package Codes

| Code | Package | Description |
|------|---------|-------------|
| F | FBGA | Fine-pitch Ball Grid Array |
| T | TSOP | Thin Small Outline Package |
| V | VFBGA | Very Fine-pitch BGA |
| S | SO | Small Outline (SOIC) |
| W | WSON | Very thin plastic quad flat no-lead |
| N | PBGA | Plastic Ball Grid Array |
| L | PLCC | Plastic Leaded Chip Carrier |
| P | PDIP | Plastic Dual In-line Package |

---

## Example MPNs with Decoding

### Serial NOR Flash

```
S25FL128SAGMFI00
│  │  │   │ │ │ │
│  │  │   │ │ │ └── 00 = Ordering code
│  │  │   │ │ └── I = Industrial temperature (-40 to +85C)
│  │  │   │ └── F = FBGA package
│  │  │   └── SAGM = Product variant (Speed/Config)
│  │  └── 128 = 128 Mbit density
│  └── FL = Serial Flash family
└── S25 = Spansion serial NOR prefix
```

### Parallel NOR Flash

```
S29GL128P90TFI01
│  │  │   │ │ │ │
│  │  │   │ │ │ └── 01 = Ordering variant
│  │  │   │ │ └── I = Industrial temperature
│  │  │   │ └── TF = TSOP/FBGA package variant
│  │  │   └── 90 = 90ns access time
│  │  └── 128P = 128 Mbit, P variant
│  └── GL = Parallel (GLUE Logic) Flash family
└── S29 = Spansion parallel NOR prefix
```

### SLC NAND Flash

```
S34ML01G200TFI00
│  │  │    │ │ │
│  │  │    │ │ └── 00 = Ordering code
│  │  │    │ └── TFI = Package + temperature
│  │  │    └── 200 = Page size variant
│  │  └── 01G = 1 Gbit density
│  └── ML = SLC NAND
└── S34 = Spansion NAND prefix
```

### FM3 Microcontroller

```
MB9AF314NPMC
│  │ │  │ │ │
│  │ │  │ │ └── C = Variant
│  │ │  │ └── PM = Package code
│  │ │  └── N = Configuration
│  │ └── 314 = Series number
│  └── AF = FM3 ARM Cortex-M3 family
└── MB9 = Spansion MCU prefix
```

---

## Series Extraction Rules

The handler extracts series based on prefix patterns:

| Prefix | Series Extraction | Example |
|--------|-------------------|---------|
| S29xxx | First 4 characters | S29GL128P → "S29G" |
| S25xxx | First 4 characters | S25FL128S → "S25F" |
| S34xxx | First 5 characters | S34ML01G → "S34ML" |
| S35xxx | First 5 characters | S35ML02G → "S35ML" |
| MB9xxx | MB9 + following letters | MB9AF314 → "MB9AF" |

---

## Replacement Compatibility

The handler implements `isOfficialReplacement()` to determine if two parts are compatible replacements:

### Flash Memory Replacement Logic

Two Flash parts are considered replacements if:
1. Same series (e.g., both S25FL)
2. Same density (e.g., both 128Mbit)
3. Same or compatible speed grade

```java
// Example: S25FL128SAGMFI00 ≈ S25FL128LAGMFI01
// Both are 128Mbit S25FL, different variant letters
```

### MCU Replacement Logic

Two MCUs are considered replacements if:
1. Same series (e.g., both MB9AF)
2. Same variant code (letter after series number)

---

## Handler Implementation Notes

### Supported ComponentTypes

```java
getSupportedTypes() returns:
  - ComponentType.MEMORY         // Base memory type
  - ComponentType.MEMORY_FLASH   // Flash-specific type
  - ComponentType.MICROCONTROLLER // FM3/FM4 MCUs
```

**Note**: The handler also registers patterns for `ComponentType.IC` (USB controllers) but does not include it in `getSupportedTypes()`. This is a known inconsistency.

### Pattern Registry

```java
// NOR Flash
registry.addPattern(ComponentType.MEMORY, "^S29[A-Z][A-Z].*");   // Parallel NOR
registry.addPattern(ComponentType.MEMORY, "^S25FL.*");           // Serial NOR
registry.addPattern(ComponentType.MEMORY, "^S25FS.*");           // High-perf Serial

// NAND Flash
registry.addPattern(ComponentType.MEMORY, "^S34ML.*");           // SLC NAND
registry.addPattern(ComponentType.MEMORY, "^S35ML.*");           // MLC NAND

// Microcontrollers
registry.addPattern(ComponentType.MICROCONTROLLER, "^MB9[A-Z].*"); // FM3
registry.addPattern(ComponentType.MICROCONTROLLER, "^MB9B.*");     // FM4

// Interface ICs
registry.addPattern(ComponentType.IC, "^GL850.*");                // USB Hub
registry.addPattern(ComponentType.IC, "^FL1K.*");                 // USB Flash
```

### Package Code Extraction

```java
// Extracts suffix after alphanumeric base
String suffix = mpn.replaceAll("^[A-Z0-9]+", "");

// Maps single letter to package name
switch (suffix) {
    case "F" -> "FBGA";
    case "T" -> "TSOP";
    case "V" -> "VFBGA";
    case "S" -> "SO";
    case "W" -> "WSON";
    case "N" -> "PBGA";
    case "L" -> "PLCC";
    case "P" -> "PDIP";
    default -> suffix;  // Return as-is if unknown
}
```

**Known Issue**: The regex `^[A-Z0-9]+` removes all leading alphanumerics, which may not correctly isolate the package suffix in complex MPNs like "S25FL128SAGMFI00" where "00" is returned, not the package code embedded in the middle.

---

## Memory Density Reference

### Common NOR Flash Densities

| Part Number | Density | Bytes |
|-------------|---------|-------|
| S25FL016 | 16 Mbit | 2 MB |
| S25FL032 | 32 Mbit | 4 MB |
| S25FL064 | 64 Mbit | 8 MB |
| S25FL128 | 128 Mbit | 16 MB |
| S25FL256 | 256 Mbit | 32 MB |
| S25FL512 | 512 Mbit | 64 MB |

### Common NAND Flash Densities

| Part Number | Density | Bytes |
|-------------|---------|-------|
| S34ML01G | 1 Gbit | 128 MB |
| S34ML02G | 2 Gbit | 256 MB |
| S34ML04G | 4 Gbit | 512 MB |

---

## Cross-Reference with Current Parts

Since Spansion is now part of Infineon, many parts have Infineon equivalents:

| Spansion Part | Infineon Equivalent | Notes |
|---------------|---------------------|-------|
| S25FL128S | S25FL128SAGMFIG03 | Same part, different suffix |
| MB9AF314N | - | Obsolete, no direct replacement |
| S34ML01G2 | - | End of life |

---

## Related Files

- Handler: `manufacturers/SpansionHandler.java`
- Component types: `MEMORY`, `MEMORY_FLASH`, `MICROCONTROLLER`
- Pattern conflicts: May conflict with generic memory patterns

---

## Learnings & Quirks

- **Acquisition chain**: Spansion -> Cypress -> Infineon. Legacy Spansion MPNs still use original numbering.
- **MB9 MCUs**: These are from the FM3/FM4 family, based on ARM Cortex-M3/M4 cores. They are largely obsolete now.
- **Interface ICs (GL850, FL1K)**: These patterns are registered under `ComponentType.IC` but IC is not in `getSupportedTypes()` - this is a handler bug.
- **Package extraction bug**: The `extractPackageCode()` method uses a regex that strips too much, returning incorrect suffixes for complex MPNs.
- **HashSet in getSupportedTypes()**: The handler uses mutable `HashSet` instead of immutable `Set.of()` - should be fixed for consistency with other handlers.
- **Serial vs Parallel Flash**: S25xx = Serial (SPI interface), S29xx = Parallel (address/data bus interface).
- **SLC vs MLC NAND**: S34ML = SLC (Single-Level Cell, higher endurance, ~100K cycles), S35ML = MLC (Multi-Level Cell, higher density, ~10K cycles).
- **Speed grade extraction**: The handler extracts speed grade for Flash memory but the method may return incorrect values for some MPN formats.

<!-- Add new learnings above this line -->
