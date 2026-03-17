---
name: esmt
description: ESMT (Elite Semiconductor Memory Technology) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with ESMT DRAM and Flash memory components or ESMTHandler.
---

# ESMT (Elite Semiconductor Memory Technology) Manufacturer Skill

## MPN Structure

ESMT MPNs follow this general structure:

```
[PREFIX][DENSITY][CONFIG][VERSION]-[SPEED][PACKAGE]
   |       |        |       |        |        |
   |       |        |       |        |        +-- Package code (TG, BG, etc.)
   |       |        |       |        +-- Speed grade (6, 5, 2.5, 100, 70)
   |       |        |       +-- Version letter (A, B, etc.)
   |       |        +-- Memory configuration (bus width, banks)
   |       +-- Density in Mbit
   +-- Series prefix (M12L, M14D, F25L, F49L)
```

### Example Decoding

```
M12L128168A-6TG
|  |   |  ||  ||
|  |   |  ||  |+-- TG = TSOP-II package
|  |   |  ||  +-- 6 = 6ns speed grade
|  |   |  |+-- A = version/revision
|  |   |  +-- 8 = 8 banks
|  |   +-- 16 = 16-bit data bus
|  +-- 128 = 128 Mbit density
+-- M12L = SDRAM series

F25L016A-100PAIG
|  |  ||    | ||
|  |  ||    | |+-- IG = Industrial grade
|  |  ||    | +-- PA = SOP package
|  |  ||    +-- 100 = 100MHz speed
|  |  |+-- A = version
|  |  +-- 016 = 16 Mbit
|  +-- 25L = SPI Flash series
+-- F = Flash prefix
```

---

## Series Prefixes

| Prefix | Memory Type | Description |
|--------|-------------|-------------|
| M12L | SDRAM | Synchronous DRAM |
| M14D | DDR SDRAM | DDR1 SDRAM |
| F25L | SPI Flash | Serial SPI NOR Flash |
| F49L | Parallel Flash | Parallel NOR Flash |

---

## Density Codes

### SDRAM (M12L) and DDR (M14D)

| Code | Density | Notes |
|------|---------|-------|
| 16 | 16 Mbit | |
| 32 | 32 Mbit | |
| 64 | 64 Mbit | |
| 128 | 128 Mbit | |
| 256 | 256 Mbit | DDR only |
| 512 | 512 Mbit | DDR only |

### SPI Flash (F25L)

| Code | Density | Notes |
|------|---------|-------|
| 004 | 4 Mbit | Leading zeros |
| 008 | 8 Mbit | Leading zeros |
| 016 | 16 Mbit | Leading zeros |
| 032 | 32 Mbit | Leading zeros |
| 064 | 64 Mbit | Leading zeros |
| 128 | 128 Mbit | |

### Parallel Flash (F49L)

| Code | Density | Notes |
|------|---------|-------|
| 160 | 16 Mbit | Scaled encoding (160 = 16Mb) |
| 320 | 32 Mbit | Scaled encoding |
| 640 | 64 Mbit | Scaled encoding |

---

## Package Codes

| Code | Package | Description |
|------|---------|-------------|
| A | TSOP | Thin Small Outline Package |
| B | BGA | Ball Grid Array |
| TG | TSOP-II | TSOP Type II |
| WG | WBGA | Window BGA |
| BG | BGA | Ball Grid Array |
| PA | SOP | Small Outline Package |
| PAIG | SOP | SOP with Industrial Grade |
| PG | SOP-8 | 8-pin SOP |

---

## Speed Grades

### SDRAM/DDR

| Code | Speed | Access Time |
|------|-------|-------------|
| 5 | 200MHz | 5ns |
| 6 | 166MHz | 6ns |
| 7 | 143MHz | 7ns |
| 2.5 | 400MHz | 2.5ns (DDR) |

### Flash

| Code | Speed | Notes |
|------|-------|-------|
| 70 | 70ns | Parallel Flash |
| 100 | 100MHz | SPI Flash |
| 104 | 104MHz | High-speed SPI |

---

## Product Families

### M12L Series - SDRAM

| Part Number | Density | Configuration | Speed |
|-------------|---------|---------------|-------|
| M12L128168A-6TG | 128 Mbit | 8M x 16 x 8 banks | 166MHz |
| M12L64164A-5TG | 64 Mbit | 4M x 16 x 4 banks | 200MHz |
| M12L32164A-6TG | 32 Mbit | 2M x 16 x 4 banks | 166MHz |

### M14D Series - DDR SDRAM

| Part Number | Density | Configuration | Speed |
|-------------|---------|---------------|-------|
| M14D5121632A-2.5BG | 512 Mbit | 32M x 16 x 2 | 400MHz |
| M14D2561616A-2.5BG | 256 Mbit | 16M x 16 x 1 | 400MHz |
| M14D1281616A-2.5BG | 128 Mbit | 8M x 16 x 1 | 400MHz |

### F25L Series - SPI Flash

| Part Number | Density | Interface | Speed |
|-------------|---------|-----------|-------|
| F25L004A-100PAIG | 4 Mbit | SPI | 100MHz |
| F25L008A-100PAIG | 8 Mbit | SPI | 100MHz |
| F25L016A-100PAIG | 16 Mbit | SPI | 100MHz |

### F49L Series - Parallel Flash

| Part Number | Density | Interface | Speed |
|-------------|---------|-----------|-------|
| F49L160UA-70TG | 16 Mbit | Parallel | 70ns |
| F49L320UA-70TG | 32 Mbit | Parallel | 70ns |

---

## Configuration Encoding (SDRAM/DDR)

The configuration digits after the density encode:

```
M12L128168A
       |||
       ||+-- Banks (4 or 8)
       |+-- Data bus width (16-bit = 16)
       +-- First digit varies
```

| Config Code | Meaning |
|-------------|---------|
| 168 | 16-bit bus, 8 banks |
| 164 | 16-bit bus, 4 banks |
| 1616 | 16-bit bus, 16Mbit config |

---

## Handler Implementation Notes

### Pattern Matching

```java
// SDRAM - M12L series
"^M12L\\d+.*"

// DDR SDRAM - M14D series
"^M14D\\d+.*"

// SPI Flash - F25L series (also MEMORY_FLASH type)
"^F25L\\d+.*"

// Parallel Flash - F49L series (also MEMORY_FLASH type)
"^F49L\\d+.*"
```

### Package Code Extraction

```java
// Handle hyphenated MPNs - get part after last hyphen
int lastHyphen = upperMpn.lastIndexOf('-');
if (lastHyphen > 0) {
    String suffix = upperMpn.substring(lastHyphen + 1);
    // Strip leading speed grade digits/dots
    String pkgCode = suffix.replaceAll("^[0-9.]+", "");
    // Check PACKAGE_CODES map
}
```

### Density Extraction Complexities

```java
// SPI Flash uses leading zeros: 004, 008, 016
// Parallel Flash uses scaled encoding: 160=16Mbit

// F25L004A -> "4" (strip leading zeros)
// F49L160UA -> "16" (scale down by 10)
```

---

## Cross-References

### SDRAM Equivalents

| ESMT | Samsung | Micron | ISSI |
|------|---------|--------|------|
| M12L128168A | K4S641632N | MT48LC8M16 | IS42S16800 |
| M12L64164A | K4S281632I | MT48LC4M16 | IS42S16400 |

### SPI Flash Equivalents

| ESMT | Winbond | Macronix | SST |
|------|---------|----------|-----|
| F25L016A | W25Q16 | MX25L1606E | SST25VF016B |
| F25L008A | W25Q80 | MX25L8006E | SST25VF080B |

---

## Related Files

- Handler: `manufacturers/ESMTHandler.java`
- Component types: `MEMORY`, `MEMORY_FLASH`, `IC`

---

## Learnings & Edge Cases

- **Leading zeros in F25L**: SPI Flash density codes have leading zeros (004, 008, 016)
- **Scaled encoding in F49L**: Parallel Flash uses 160=16Mbit, 320=32Mbit encoding
- **Configuration encoding**: SDRAM part numbers encode bus width and bank count
- **Speed grade in suffix**: Speed appears before package code after hyphen (e.g., -6TG = 6ns + TSOP-II)
- **Industrial grade suffix**: PAIG = SOP package with Industrial Grade indicator
- **Version letters**: A, B, C indicate silicon revisions, not always form/fit/function compatible

<!-- Add new learnings above this line -->
