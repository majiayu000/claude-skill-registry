---
name: txc
description: TXC Corporation MPN encoding patterns, frequency and temperature decoding, and handler guidance. Use when working with TXC timing devices (crystals, oscillators, TCXO, VCXO).
---

# TXC Corporation Manufacturer Skill

## MPN Structure

TXC MPNs follow this general structure:

```
[SERIES]-[FREQUENCY][SUFFIX]
   |         |         |
   |         |         +-- Temperature grade + packaging (e.g., MAAJ-T)
   |         +-- Frequency value (e.g., 12.000M = 12 MHz)
   +-- 2-character series code (7M, 8Y, 9C, 7V, 7X, AX)
```

### Example Decoding

```
7M-12.000MAAJ-T
|    |    || |
|    |    || +-- T = Tape and Reel packaging
|    |    |+-- J = Package variant
|    |    +-- A = Commercial temperature (-20 to +70C)
|    +-- 12.000M = 12 MHz frequency
+-- 7M = Standard crystal series

8Y-16.000MAAE-T
|    |    ||
|    |    |+-- E = Extended temperature (-40 to +85C)
|    |    +-- A = Tolerance code
|    +-- 16.000M = 16 MHz
+-- 8Y = SMD crystal series

9C-25.000MBD-T
|    |    |
|    |    +-- BD = Clock oscillator suffix
|    +-- 25.000M = 25 MHz
+-- 9C = Clock oscillator series
```

---

## Series Codes

### Crystal Series

| Series | Product Type | Package | Notes |
|--------|--------------|---------|-------|
| 7M | Standard crystals | HC49 | Through-hole, general purpose |
| 8Y | SMD crystals | 3.2x2.5mm | Surface mount, common size |
| AX | Automotive crystals | SMD | AEC-Q200 qualified |

### Oscillator Series

| Series | Product Type | Package | Notes |
|--------|--------------|---------|-------|
| 9C | Clock oscillators | SMD | Standard clock output |
| 7V | VCXO | SMD | Voltage Controlled Crystal Oscillator |
| 7X | TCXO | SMD | Temperature Compensated Crystal Oscillator |

---

## Frequency Encoding

Frequency is encoded after the series prefix with a hyphen separator:

| Format | Example | Meaning |
|--------|---------|---------|
| XX.XXXM | 12.000M | 12.000 MHz |
| XX.XXXK | 32.768K | 32.768 kHz |
| XXXM | 25M | 25 MHz (simplified) |

---

## Temperature Grades

| Code | Range | Application |
|------|-------|-------------|
| A | -20 to +70C | Commercial |
| E | -40 to +85C | Extended/Industrial |
| I | -40 to +85C | Industrial (alternate) |
| M | -55 to +125C | Military (rarely used) |

Temperature grade is typically the second character in the options suffix after the frequency.

---

## Package Codes

TXC uses the series prefix to indicate general package type, with additional suffix encoding:

### By Series

| Series | Default Package | Dimensions |
|--------|----------------|------------|
| 7M | HC49 | Through-hole |
| 8Y | SMD ceramic | 3.2x2.5mm |
| 9C | SMD oscillator | Various |
| 7V | SMD VCXO | 5.0x3.2mm typical |
| 7X | SMD TCXO | 3.2x2.5mm typical |
| AX | Automotive SMD | Various |

### Suffix Codes

| Suffix | Meaning |
|--------|---------|
| -T | Tape and Reel |
| -TR | Tape and Reel (alternate) |
| G | Gold finish |
| J | Standard package variant |

---

## Replacement Compatibility

TXC parts are compatible when:
1. **Same series** (7M vs 7M, 8Y vs 8Y)
2. **Same frequency** (12.000M matches 12.000M)
3. **Compatible temperature** (Extended can replace Commercial, not vice versa)

### Temperature Grade Upgrade Path

```
Commercial (A) can be upgraded to Extended (E)
Extended (E) CANNOT be downgraded to Commercial (A)
```

---

## Common Part Numbers

### Standard Crystals (7M)

| Part Number | Frequency | Package | Notes |
|-------------|-----------|---------|-------|
| 7M-12.000MAAJ-T | 12 MHz | HC49 | Commercial, tape/reel |
| 7M-16.000MAAJ-T | 16 MHz | HC49 | Commercial, tape/reel |
| 7M-8.000MAAJ-T | 8 MHz | HC49 | Commercial, tape/reel |

### SMD Crystals (8Y)

| Part Number | Frequency | Package | Notes |
|-------------|-----------|---------|-------|
| 8Y-12.000MAAE-T | 12 MHz | 3.2x2.5mm | Extended temp |
| 8Y-16.000MAAE-T | 16 MHz | 3.2x2.5mm | Extended temp |
| 8Y-25.000MAAJ-T | 25 MHz | 3.2x2.5mm | Commercial |

### Clock Oscillators (9C)

| Part Number | Frequency | Output | Notes |
|-------------|-----------|--------|-------|
| 9C-12.000MBD-T | 12 MHz | CMOS | Standard output |
| 9C-25.000MBD-T | 25 MHz | CMOS | Standard output |
| 9C-50.000MBD-T | 50 MHz | CMOS | High frequency |

### VCXO (7V)

| Part Number | Frequency | Notes |
|-------------|-----------|-------|
| 7V-12.000MBA-T | 12 MHz | Voltage controlled |
| 7V-25.000MBA-T | 25 MHz | Voltage controlled |

### TCXO (7X)

| Part Number | Frequency | Stability | Notes |
|-------------|-----------|-----------|-------|
| 7X-16.000MBA-T | 16 MHz | +/-2.5ppm | Temperature compensated |
| 7X-26.000MBA-T | 26 MHz | +/-2.5ppm | Temperature compensated |

---

## Handler Implementation Notes

### Series Code Extraction

```java
// Series is first 2 characters
String extractSeriesCode(String mpn) {
    if (mpn == null || mpn.length() < 2) return "";
    String prefix = mpn.substring(0, 2).toUpperCase();
    return switch (prefix) {
        case "7M", "8Y", "9C", "7V", "7X", "AX" -> prefix;
        default -> "";
    };
}
```

### Frequency Extraction

```java
// Frequency is after first hyphen, ends with M or K
String extractFrequency(String mpn) {
    int dashIndex = mpn.indexOf('-');
    if (dashIndex < 0) return "";
    String afterDash = mpn.substring(dashIndex + 1);

    // Find end of frequency (M for MHz, K for kHz)
    for (int i = 0; i < afterDash.length(); i++) {
        char c = afterDash.charAt(i);
        if (c == 'M' || c == 'K') {
            return afterDash.substring(0, i + 1);
        }
    }
    return "";
}
```

### Temperature Grade Detection

```java
// Look for E (Extended) or A (Commercial) in options suffix
String extractTemperatureGrade(String mpn) {
    // Remove trailing -T if present
    String workMpn = mpn.endsWith("-T") ? mpn.substring(0, mpn.length() - 2) : mpn;

    // Find options suffix after frequency
    // E anywhere = Extended, A anywhere = Commercial
    String optionsSuffix = /* extract suffix after frequency */;
    if (optionsSuffix.contains("E")) return "Extended";
    if (optionsSuffix.contains("A")) return "Commercial";
    return "";
}
```

---

## Related Files

- Handler: `manufacturers/TXCHandler.java`
- Component types: `CRYSTAL`, `OSCILLATOR`
- No manufacturer-specific types defined

---

## Learnings & Edge Cases

- **Frequency format**: Always includes decimal for precision (12.000M, not 12M)
- **Temperature in suffix**: The second character in options suffix typically indicates temperature grade
- **Series determines package**: Unlike other manufacturers, TXC uses series prefix to indicate package type
- **VCXO/TCXO distinction**: 7V = voltage controlled, 7X = temperature compensated (different applications)
- **Automotive (AX)**: Requires AEC-Q200 qualification, typically extended temp range

<!-- Add new learnings above this line -->
