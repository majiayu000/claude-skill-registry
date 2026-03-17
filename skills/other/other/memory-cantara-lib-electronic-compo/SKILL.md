---
name: memory
description: Use when working with memory components - Flash, EEPROM, SRAM, DRAM. Includes adding patterns, parsing memory MPNs, extracting capacity, interface type, and speed information.
---

# Memory Component Skill

Guidance for working with memory components in the lib-electronic-components library.

## Supported Manufacturers & Patterns

| Manufacturer | Handler | MPN Patterns | Example |
|--------------|---------|--------------|---------|
| Winbond | `WinbondHandler` | `W25Q#`, `W25X#`, `W##` | `W25Q128JVSIQ` |
| Micron | `MicronHandler` | `MT#`, `N25Q#`, `M25P#` | `MT25QL128ABA` |
| ISSI | `ISSIHandler` | `IS#`, `IS25LP#`, `IS25WP#` | `IS25LP128F` |
| Microchip | `MicrochipHandler` | `AT24C#`, `AT25#`, `SST26#` | `AT24C256` |
| Macronix | Various | `MX25#` | `MX25L12835F` |
| Cypress/Infineon | `CypressHandler` | `S25FL#`, `FM24#` | `S25FL128S` |

## ComponentTypes

```java
// Base types
ComponentType.MEMORY
ComponentType.MEMORY_FLASH
ComponentType.MEMORY_EEPROM

// Manufacturer-specific types
ComponentType.MEMORY_FLASH_WINBOND
ComponentType.MEMORY_EEPROM_WINBOND
ComponentType.MEMORY_MICRON
ComponentType.MEMORY_ISSI
ComponentType.MEMORY_MICROCHIP
ComponentType.MEMORY_ATMEL
ComponentType.MEMORY_INFINEON
ComponentType.MEMORY_NXP
ComponentType.MEMORY_ST
ComponentType.MEMORY_RENESAS
ComponentType.MEMORY_MAXIM
```

## Flash Memory

### Winbond W25Q Series (SPI NOR Flash)

```
W25Q 128 JV SIQ
│    │   │  │
│    │   │  └── Package (SIQ=SOIC-8 150mil)
│    │   └───── Voltage/Grade (JV=3.3V, FV=1.8V)
│    └───────── Density (128=128Mbit)
└────────────── Series
```

### Common Densities

| Code | Size |
|------|------|
| 32 | 32Mbit (4MB) |
| 64 | 64Mbit (8MB) |
| 128 | 128Mbit (16MB) |
| 256 | 256Mbit (32MB) |
| 512 | 512Mbit (64MB) |

### Interfaces

| Type | Description | Speed |
|------|-------------|-------|
| SPI | Serial Peripheral Interface | 50-133MHz |
| QSPI | Quad SPI | 104-133MHz |
| DSPI | Dual SPI | 80-104MHz |
| Parallel | Parallel interface | Various |

## EEPROM

### Microchip AT24C Series (I2C EEPROM)

```
AT24C 256 C
│     │   │
│     │   └── Temperature range (C=Commercial)
│     └────── Density (256=256Kbit)
└──────────── Series (I2C EEPROM)
```

### Common EEPROM Series

| Series | Interface | Organization |
|--------|-----------|--------------|
| AT24C | I2C | x8 |
| AT25 | SPI | x8 |
| 93C | Microwire | x8/x16 |

## SRAM

### Patterns

| Manufacturer | Pattern | Example |
|--------------|---------|---------|
| ISSI | `IS61#`, `IS62#` | `IS62WV12816BLL` |
| Cypress | `CY62#`, `CY7C#` | `CY62256NLL` |

## Adding New Memory Patterns

1. In the manufacturer handler's `initializePatterns()`:
```java
registry.addPattern(ComponentType.MEMORY, "^NEWMEM[0-9].*");
registry.addPattern(ComponentType.MEMORY_FLASH, "^NEWMEM[0-9].*");
registry.addPattern(ComponentType.MEMORY_MANUFACTURER, "^NEWMEM[0-9].*");
```

2. Add to `getSupportedTypes()`:
```java
types.add(ComponentType.MEMORY);
types.add(ComponentType.MEMORY_FLASH);
types.add(ComponentType.MEMORY_MANUFACTURER);
```

## Similarity Calculation

`MemorySimilarityCalculator` compares:
- Memory type (Flash, EEPROM, SRAM)
- Density/capacity
- Interface (SPI, I2C, parallel)
- Voltage range
- Speed grade
- Package

## Package Codes

| Code | Package |
|------|---------|
| SIQ | SOIC-8 150mil |
| SIG | SOIC-8 208mil |
| DIQ | DFN-8 |
| CIQ | WSON-8 |
| BIQ | BGA |
| PIQ | PDIP-8 |

## Memory Type Detection

The library can detect memory types from MPN patterns:

```java
// Detect flash memory
ComponentType type = ComponentType.fromMPN("W25Q128JVSIQ");
// Returns MEMORY_FLASH_WINBOND

// Detect EEPROM
ComponentType type = ComponentType.fromMPN("AT24C256");
// Returns MEMORY_EEPROM or MEMORY_ATMEL
```

---

## Learnings & Quirks

<!-- Record component-specific discoveries, edge cases, and quirks here -->
