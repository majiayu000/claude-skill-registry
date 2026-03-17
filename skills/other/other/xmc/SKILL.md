---
name: xmc
description: XMC (Wuhan Xinxin Semiconductor) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with XMC SPI NOR Flash memory components or XMCHandler.
---

# XMC (Wuhan Xinxin Semiconductor) Manufacturer Skill

## MPN Structure

XMC MPNs follow this general structure:

```
[PREFIX][DENSITY][PACKAGE]
   |       |        |
   |       |        +-- Package code (A, B, C, D)
   |       +-- Memory density (32, 64, 128, 256, 512)
   +-- Series prefix (XM25QH, XM25QU, XM25LU)
```

### Example Decoding

```
XM25QH64A
|  |  |||
|  |  ||+-- A = SOIC-8 package
|  |  |+-- 64 = 64 Mbit density
|  |  +-- H = Standard 3.3V series
|  +-- 25Q = SPI Flash family
+-- XM = XMC prefix

XM25QU128B
|  |  | ||
|  |  | |+-- B = SOIC-16 package
|  |  | +-- 128 = 128 Mbit density
|  |  +-- U = 1.8V Low Voltage series
|  +-- 25Q = SPI Flash family
+-- XM = XMC prefix

XM25LU256C
|  |  | ||
|  |  | |+-- C = WSON-8 package
|  |  | +-- 256 = 256 Mbit density
|  |  +-- LU = Ultra Low Voltage series
|  +-- 25 = SPI Flash family
+-- XM = XMC prefix
```

---

## Series Prefixes

| Prefix | Voltage Range | Description |
|--------|---------------|-------------|
| XM25QH | 2.7V - 3.6V | Standard 3.3V SPI NOR Flash |
| XM25QU | 1.65V - 2.0V | 1.8V Low Voltage SPI NOR Flash |
| XM25LU | 1.65V - 1.95V | Ultra Low Voltage SPI NOR Flash |

---

## Density Codes

| Code | Density | Size |
|------|---------|------|
| 32 | 32 Mbit | 4 MB |
| 64 | 64 Mbit | 8 MB |
| 128 | 128 Mbit | 16 MB |
| 256 | 256 Mbit | 32 MB |
| 512 | 512 Mbit | 64 MB |

---

## Package Codes

| Code | Package | Pin Count | Body Size |
|------|---------|-----------|-----------|
| A | SOIC-8 | 8 | 208mil |
| B | SOIC-16 | 16 | 300mil |
| C | WSON-8 | 8 | 6x5mm |
| D | USON-8 | 8 | 2x3mm |

---

## Product Families

### XM25QH Series - Standard 3.3V SPI NOR Flash

| Part Number | Density | Voltage | Max Speed | Interface |
|-------------|---------|---------|-----------|-----------|
| XM25QH32A | 32 Mbit | 2.7V-3.6V | 104MHz | SPI/Dual/Quad |
| XM25QH64A | 64 Mbit | 2.7V-3.6V | 104MHz | SPI/Dual/Quad |
| XM25QH128A | 128 Mbit | 2.7V-3.6V | 104MHz | SPI/Dual/Quad |
| XM25QH256B | 256 Mbit | 2.7V-3.6V | 104MHz | SPI/Dual/Quad |
| XM25QH512 | 512 Mbit | 2.7V-3.6V | 104MHz | SPI/Dual/Quad |

### XM25QU Series - 1.8V Low Voltage SPI NOR Flash

| Part Number | Density | Voltage | Max Speed | Interface |
|-------------|---------|---------|-----------|-----------|
| XM25QU64A | 64 Mbit | 1.65V-2.0V | 104MHz | SPI/Dual/Quad |
| XM25QU128B | 128 Mbit | 1.65V-2.0V | 104MHz | SPI/Dual/Quad |
| XM25QU256C | 256 Mbit | 1.65V-2.0V | 104MHz | SPI/Dual/Quad |

### XM25LU Series - Ultra Low Voltage SPI NOR Flash

| Part Number | Density | Voltage | Max Speed | Application |
|-------------|---------|---------|-----------|-------------|
| XM25LU128 | 128 Mbit | 1.65V-1.95V | 104MHz | Ultra-low power |
| XM25LU256 | 256 Mbit | 1.65V-1.95V | 104MHz | Ultra-low power |

---

## Handler Implementation Notes

### Pattern Matching

```java
// XM25QH series - Standard 3.3V
Pattern XM25QH_PATTERN = Pattern.compile("^XM25QH\\d+[A-Z]*.*", Pattern.CASE_INSENSITIVE);

// XM25QU series - 1.8V Low Voltage
Pattern XM25QU_PATTERN = Pattern.compile("^XM25QU\\d+[A-Z]*.*", Pattern.CASE_INSENSITIVE);

// XM25LU series - Ultra Low Voltage
Pattern XM25LU_PATTERN = Pattern.compile("^XM25LU\\d+[A-Z]*.*", Pattern.CASE_INSENSITIVE);
```

### Package Code Extraction

```java
// XMC format: XM25QHxxxY where Y is the package code
// Extract the letter after density digits
Matcher matcher = DENSITY_PATTERN.matcher(upperMpn);
if (matcher.find()) {
    int densityEnd = matcher.end();
    if (densityEnd < upperMpn.length()) {
        String pkgCode = upperMpn.substring(densityEnd, densityEnd + 1);
        // Map to package: A=SOIC-8, B=SOIC-16, C=WSON-8, D=USON-8
    }
}
```

### Voltage Range Extraction

```java
// Determine operating voltage based on series
switch (series) {
    case "XM25QH" -> "2.7V-3.6V";
    case "XM25QU" -> "1.65V-2.0V";
    case "XM25LU" -> "1.65V-1.95V";
}
```

---

## Cross-References

XMC Flash is pin-compatible with other SPI NOR Flash manufacturers:

### 3.3V Standard Series (XM25QH)

| XMC | Winbond | GigaDevice | Macronix |
|-----|---------|------------|----------|
| XM25QH64A | W25Q64JV | GD25Q64C | MX25L6433F |
| XM25QH128A | W25Q128JV | GD25Q128C | MX25L12835F |
| XM25QH256B | W25Q256JV | GD25Q256C | MX25L25645G |

### 1.8V Low Voltage Series (XM25QU)

| XMC | Winbond | GigaDevice | Macronix |
|-----|---------|------------|----------|
| XM25QU64A | W25Q64FW | GD25LQ64C | MX25U6435F |
| XM25QU128B | W25Q128FW | GD25LQ128C | MX25U12835F |

---

## Voltage Selection Guide

| Application | Recommended Series | Voltage |
|-------------|-------------------|---------|
| Legacy 3.3V systems | XM25QH | 2.7V-3.6V |
| Mobile/Battery powered | XM25QU | 1.65V-2.0V |
| Ultra-low power IoT | XM25LU | 1.65V-1.95V |

---

## Related Files

- Handler: `manufacturers/XMCHandler.java`
- Component types: `MEMORY`, `MEMORY_FLASH`, `IC`

---

## Learnings & Edge Cases

- **Series order**: Check XM25QH before XM25QU before XM25LU for proper matching
- **Package code position**: Single letter immediately after density digits
- **Voltage compatibility**: XM25QH (3.3V) and XM25QU (1.8V) are NOT voltage compatible
- **Pin compatibility**: All series are pin-compatible with Winbond 25Q series
- **Density encoding**: Direct numeric encoding (64=64Mbit, 128=128Mbit, etc.)
- **SOIC-16 for high density**: Larger densities (256Mbit+) often use SOIC-16 (package code B)

<!-- Add new learnings above this line -->
