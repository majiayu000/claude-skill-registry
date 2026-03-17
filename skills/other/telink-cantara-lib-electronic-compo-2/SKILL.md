---
name: telink
description: Telink Semiconductor MPN encoding patterns, BLE/Zigbee SoC decoding, and handler guidance. Use when working with Telink wireless components or TelinkHandler.
---

# Telink Semiconductor Manufacturer Skill

## MPN Structure

Telink uses two naming conventions for their BLE and Zigbee SoCs:

### Legacy TLSR Naming
```
TLSR[SERIES][VARIANT][FEATURES][PACKAGE]
   |    |       |        |        |
   |    |       |        |        +-- Package code (ET32, ET48, Q)
   |    |       |        +-- Feature/flash suffix (F512, F1M)
   |    |       +-- Variant letter (A, B, etc.)
   |    +-- Series number (8251, 8258, 9218)
   +-- Telink Low-power Semiconductor Radio
```

### Newer B-Series Naming
```
B[SERIES][VARIANT]
  |   |      |
  |   |      +-- Variant (M for module, etc.)
  |   +-- Series number (85, 87, 91, 92)
  +-- B-series (BLE-focused)
```

### Example Decoding

```
TLSR8258F512ET32
|    |   |    |
|    |   |    +-- ET32 = QFN-32 package
|    |   +-- F512 = 512KB Flash
|    +-- 8258 = BLE 5.0 series
+-- TLSR = Telink Low-power Semiconductor Radio

B91M
| ||
| |+-- M = Module variant
| +-- 91 = RISC-V BLE 5.2 series
+-- B-series naming
```

---

## Product Families

### TLSR82xx Series (BLE 5.0)

| Part | Description | Flash | Packages |
|------|-------------|-------|----------|
| TLSR8251 | BLE 5.0 SoC, entry-level | 512KB | QFN-32 |
| TLSR8253 | BLE 5.0 SoC, mid-range | 512KB | QFN-32 |
| TLSR8258 | BLE 5.0 SoC, feature-rich | 512KB/1MB | QFN-32, QFN-48 |
| TLSR8261 | BLE 5.0/Mesh SoC | 512KB | QFN-32 |
| TLSR8269 | BLE 5.0 high-end | 1MB | QFN-48 |

### TLSR825x Series (Zigbee 3.0)

| Part | Description | Protocol |
|------|-------------|----------|
| TLSR8258 | Zigbee 3.0 + BLE dual-mode | Zigbee 3.0/BLE 5.0 |
| TLSR8278 | Matter-ready SoC | Zigbee/Thread/BLE |

### TLSR92xx Series (BLE 5.2)

| Part | Description | Features |
|------|-------------|----------|
| TLSR9218 | BLE 5.2 SoC | LE Audio, Direction Finding |

### B-Series (Newer Naming)

| Part | Description | Core |
|------|-------------|------|
| B85 | BLE 5.0 | ARM Cortex-M0 |
| B87 | BLE 5.0+ | ARM Cortex-M0 |
| B91 | BLE 5.2 RISC-V | RISC-V |
| B92 | BLE 5.3 RISC-V | RISC-V |

---

## Package Codes

| Code/Suffix | Package | Pin Count |
|-------------|---------|-----------|
| ET32 | QFN | 32 |
| ET48 | QFN | 48 |
| ET24 | QFN | 24 |
| Q32, QFN32 | QFN | 32 |
| Q48, QFN48 | QFN | 48 |
| Q | QFN | Various |

### Package Code Extraction

The handler looks for package codes in these locations:
1. After hyphen: `TLSR8258-Q32`
2. Embedded in suffix: `TLSR8258ET32`
3. Trailing digits: `TLSR8258F51232` (32 = pin count)

---

## Feature Suffixes

| Suffix | Meaning |
|--------|---------|
| F512 | 512KB Flash |
| F1M | 1MB Flash |
| A, B | Silicon revision |
| M | Module variant |

---

## Series Compatibility

### Upgrade Paths

```
TLSR8251 -> TLSR8258 (more features, pin-compatible)
TLSR8258 -> TLSR8269 (more Flash/features)
B85 -> B87 (improved BLE 5.0)
TLSR82xx -> TLSR92xx (BLE 5.0 to 5.2 upgrade)
```

### Handler `isOfficialReplacement()` Logic

```java
// Compatible upgrades:
TLSR8258 can replace TLSR8251
TLSR8269 can replace TLSR8258
B87 can replace B85
TLSR92xx can replace TLSR82xx
```

---

## Handler Implementation Notes

### Series Extraction

```java
// TLSR series: extract first 8 alphanumeric characters
// TLSR8258F512ET32 -> TLSR8258

// B-series: extract B + 2 digits
// B91M -> B91
```

### Package Code Extraction

```java
// Check for explicit package suffix patterns
// Format: TLSR8258F512ET32 where last digits indicate package

// Common patterns: ET32 (QFN-32), ET48 (QFN-48), ET24 (QFN-24)
if (upperMpn.matches(".*ET32.*") || upperMpn.endsWith("32")) {
    return "QFN-32";
}
```

### Matching Logic

Both `IC` and `MICROCONTROLLER` component types are supported:
- TLSR series: `^TLSR[0-9]{4}.*`
- B-series: `^B[0-9]{2}[A-Z]*.*`

---

## Related Files

- Handler: `manufacturers/TelinkHandler.java`
- Component types: `ComponentType.IC`, `ComponentType.MICROCONTROLLER`

---

## Common MPNs

| MPN | Description | Package |
|-----|-------------|---------|
| TLSR8251F512ET32 | BLE 5.0, 512KB, QFN-32 | QFN-32 |
| TLSR8258F512ET32 | BLE 5.0, 512KB, QFN-32 | QFN-32 |
| TLSR8258F1MET48 | BLE 5.0, 1MB, QFN-48 | QFN-48 |
| TLSR8269F1M | BLE 5.0 high-end, 1MB | Various |
| TLSR9218 | BLE 5.2 | Various |
| B91 | RISC-V BLE 5.2 | Various |

---

## Applications

- Bluetooth Low Energy (BLE) devices
- Zigbee 3.0 smart home devices
- Thread/Matter IoT devices
- BLE beacons and sensors
- Wireless keyboards/mice
- Audio devices (TWS earbuds)

---

## Learnings & Edge Cases

- **Dual naming convention**: Telink transitioned from TLSR to B-series naming. Both are still in use.
- **BLE/Zigbee dual-mode**: Some chips like TLSR8258 support both BLE and Zigbee protocols.
- **Flash size in MPN**: F512 = 512KB, F1M = 1MB - important for firmware sizing.
- **Package in trailing digits**: If MPN ends with 32/48/24, it indicates QFN pin count.
- **B91 is RISC-V**: Unlike older TLSR chips (ARM Cortex-M0), B91 uses RISC-V core.

<!-- Add new learnings above this line -->
