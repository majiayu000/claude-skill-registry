---
name: puya
description: Puya Semiconductor MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Puya SPI NOR Flash memory components or PuyaHandler.
---

# Puya Semiconductor Manufacturer Skill

## MPN Structure

Puya MPNs follow this general structure:

```
[PREFIX][DENSITY][PACKAGE][-SUFFIX]
   |       |        |        |
   |       |        |        +-- Optional: Grade/Temperature (SSH, SUH)
   |       |        +-- Package code (H, U, SH, SU)
   |       +-- Memory density (80=8Mbit, 16, 32, 64, 128)
   +-- Series prefix (P25Q, P25D, PY25Q)
```

### Example Decoding

```
P25Q80H
|  | ||
|  | |+-- H = SOIC-8 package
|  | +-- 80 = 8 Mbit density
|  +-- Q = Standard series
+-- P25 = Puya SPI Flash prefix

P25Q16H-SSH
|  |  | | |
|  |  | | +-- SSH = SOIC-8 (hyphenated suffix)
|  |  | +-- H = base package indicator
|  |  +-- 16 = 16 Mbit density
|  +-- Q = Standard series
+-- P25 = Puya SPI Flash prefix

PY25Q128HA
| | |  ||
| | |  |+-- A = Grade code (Automotive)
| | |  +-- H = SOIC-8 package
| | +-- 128 = 128 Mbit density
| +-- Y25Q = Automotive grade series
+-- P = Puya prefix
```

---

## Series Prefixes

| Prefix | Category | Description |
|--------|----------|-------------|
| P25Q | Standard SPI NOR Flash | 3.3V operation, general purpose |
| P25D | Low Power SPI NOR Flash | Reduced power consumption |
| PY25Q | Automotive Grade SPI NOR Flash | AEC-Q100 qualified, extended temperature |

---

## Density Codes

| Code | Density | Size |
|------|---------|------|
| 80 | 8 Mbit | 1 MB |
| 16 | 16 Mbit | 2 MB |
| 32 | 32 Mbit | 4 MB |
| 64 | 64 Mbit | 8 MB |
| 128 | 128 Mbit | 16 MB |

**Note**: Density code 80 represents 8 Mbit (not 80 Mbit).

---

## Package Codes

### Base Package Codes

| Code | Package | Notes |
|------|---------|-------|
| H | SOIC-8 | Standard 208mil body |
| U | USON-8 | Ultra thin 2x3mm |
| SH | SOIC-8-WIDE | Wide body 300mil |
| SU | WSON-8 | 6x5mm leadless |

### Hyphenated Suffix Codes

| Suffix | Package | Notes |
|--------|---------|-------|
| -SSH | SOIC-8 | Standard SOIC-8 with grade indicator |
| -SUH | WSON-8 | WSON-8 with grade indicator |

---

## Product Families

### P25Q Series - Standard SPI NOR Flash

| Part Number | Density | Interface | Voltage | Speed |
|-------------|---------|-----------|---------|-------|
| P25Q80H | 8 Mbit | SPI/Dual/Quad | 2.3V-3.6V | 104MHz |
| P25Q16H | 16 Mbit | SPI/Dual/Quad | 2.3V-3.6V | 104MHz |
| P25Q32H | 32 Mbit | SPI/Dual/Quad | 2.3V-3.6V | 104MHz |
| P25Q64H | 64 Mbit | SPI/Dual/Quad | 2.3V-3.6V | 104MHz |
| P25Q128H | 128 Mbit | SPI/Dual/Quad | 2.3V-3.6V | 104MHz |

### P25D Series - Low Power SPI NOR Flash

| Part Number | Density | Interface | Voltage | Power Mode |
|-------------|---------|-----------|---------|------------|
| P25D80H | 8 Mbit | SPI/Dual/Quad | 1.65V-3.6V | Ultra Low Power |

### PY25Q Series - Automotive Grade SPI NOR Flash

| Part Number | Density | Temperature | Qualification |
|-------------|---------|-------------|---------------|
| PY25Q128HA | 128 Mbit | -40C to +125C | AEC-Q100 |

---

## Handler Implementation Notes

### Pattern Matching

```java
// P25Q series - Standard SPI NOR Flash
"^P25Q\\d+.*"

// P25D series - Low Power SPI NOR Flash
"^P25D\\d+.*"

// PY25Q series - Automotive Grade (check first as more specific)
"^PY25Q\\d+.*"
```

### Package Code Extraction

```java
// Handle hyphenated suffixes first
int hyphenIndex = upperMpn.indexOf('-');
if (hyphenIndex > 0) {
    String suffix = upperMpn.substring(hyphenIndex + 1);
    // Check against PACKAGE_CODES map
}

// Then extract trailing package code after density
// P25Q80H -> H (SOIC-8)
// Check longer suffixes before shorter ones (SU before U, SH before H)
```

### Density Extraction

```java
// Special case: 80 = 8Mbit, not 80Mbit
switch (densityCode) {
    case "80" -> "8";
    default -> densityCode;
}
```

### Grade Extraction

```java
// Check prefix to determine grade
if (upperMpn.startsWith("PY25Q")) return "Automotive";
if (upperMpn.startsWith("P25D")) return "Low Power";
if (upperMpn.startsWith("P25Q")) return "Standard";
```

---

## Cross-References

Puya Flash is pin-compatible with other SPI NOR Flash manufacturers:

| Puya | Winbond | GigaDevice | Macronix |
|------|---------|------------|----------|
| P25Q80H | W25Q80 | GD25Q80 | MX25L8006E |
| P25Q16H | W25Q16 | GD25Q16 | MX25L1606E |
| P25Q32H | W25Q32 | GD25Q32 | MX25L3206E |
| P25Q64H | W25Q64 | GD25Q64 | MX25L6406E |
| P25Q128H | W25Q128 | GD25Q128 | MX25L12835F |

---

## Related Files

- Handler: `manufacturers/PuyaHandler.java`
- Component types: `MEMORY`, `MEMORY_FLASH`, `IC`

---

## Learnings & Edge Cases

- **Density code 80**: Represents 8 Mbit, not 80 Mbit - special handling required
- **PY vs P prefix**: PY25Q is automotive grade, must check before P25Q pattern
- **Hyphenated suffixes**: Some MPNs have package code after hyphen (P25Q16H-SSH)
- **Grade indicators**: Trailing 'A' often indicates automotive grade
- **Pin compatibility**: Puya Flash is generally pin-compatible with Winbond, GigaDevice, and Macronix equivalents

<!-- Add new learnings above this line -->
