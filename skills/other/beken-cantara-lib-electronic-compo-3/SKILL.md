---
name: beken
description: Beken Corporation MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Beken WiFi and BLE SoC components or BekenHandler.
---

# Beken Corporation Manufacturer Skill

## Company Overview

Beken Corporation specializes in WiFi and Bluetooth Low Energy (BLE) System-on-Chip (SoC) solutions, primarily targeting IoT applications including smart home, audio, and wearable devices.

## MPN Structure

Beken MPNs follow this general structure:

```
[PREFIX][SERIES][-PACKAGE]
   |       |        |
   |       |        +-- Optional: Package code (QFN-32, QFN-40)
   |       +-- Series number (7231, 3431, etc.)
   +-- BK prefix (Beken)
```

### Example Decoding

```
BK7231
|  |||
|  ||+-- 1 = Variant
|  |+-- 3 = Submodel
|  +-- 72 = WiFi + BLE series
+-- BK = Beken prefix

BK7231-QFN-32
|  |||   |  |
|  |||   |  +-- 32 = 32-pin
|  |||   +-- QFN = Package type
|  ||+-- 1 = Variant
|  |+-- 3 = Submodel
|  +-- 72 = WiFi + BLE series
+-- BK = Beken prefix

BK3432
|  |||
|  ||+-- 2 = BLE 5.0 variant
|  |+-- 3 = Submodel
|  +-- 34 = BLE-only series
+-- BK = Beken prefix
```

---

## Series Overview

| Series | Wireless Type | Protocol | Application |
|--------|---------------|----------|-------------|
| BK7xxx | WiFi + BLE | WiFi 4/6 + BLE | Smart home, audio |
| BK3xxx | BLE only | BLE 4.x/5.x | Wearables, sensors |

---

## Product Families

### BK7xxx Series - WiFi + BLE Combo Chips

| Part Number | WiFi | BLE | Features |
|-------------|------|-----|----------|
| BK7231 | 802.11 b/g/n | BLE 4.2 | Basic combo |
| BK7251 | 802.11 b/g/n | BLE 5.0 | Audio + WiFi |
| BK7256 | 802.11ax (WiFi 6) | BLE 5.2 | Latest gen |

### BK3xxx Series - BLE Only Chips

| Part Number | BLE Version | Features |
|-------------|-------------|----------|
| BK3431 | BLE 4.2 | Basic BLE |
| BK3432 | BLE 5.0 | Enhanced range |

---

## Package Codes

| Code | Package | Pin Count | Description |
|------|---------|-----------|-------------|
| QFN-32 | QFN | 32 | Quad Flat No-lead, 32-pin |
| QFN-40 | QFN | 40 | Quad Flat No-lead, 40-pin |
| QFN-48 | QFN | 48 | Quad Flat No-lead, 48-pin |
| N | QFN | - | QFN (generic) |
| Q | QFN | - | QFN (alternate code) |

---

## Wireless Capabilities

### WiFi + BLE Combo (BK7xxx)

| Feature | BK7231 | BK7251 | BK7256 |
|---------|--------|--------|--------|
| WiFi Standard | 802.11n | 802.11n | 802.11ax |
| WiFi Band | 2.4GHz | 2.4GHz | 2.4GHz |
| BLE Version | 4.2 | 5.0 | 5.2 |
| Audio Support | No | Yes | Yes |
| Target Market | Basic IoT | Audio IoT | Premium IoT |

### BLE Only (BK3xxx)

| Feature | BK3431 | BK3432 |
|---------|--------|--------|
| BLE Version | 4.2 | 5.0 |
| Range | Standard | Extended |
| Power | Low | Ultra-low |

---

## Handler Implementation Notes

### Pattern Matching

```java
// WiFi + BLE combo chips (BK7xxx series)
"^BK7[0-9]{3}.*"

// BLE only chips (BK3xxx series)
"^BK3[0-9]{3}.*"

// Combined matching in matches() method
if (type == ComponentType.IC) {
    return upperMpn.matches("^BK7[0-9]{3}.*") ||
           upperMpn.matches("^BK3[0-9]{3}.*");
}
```

### Package Code Extraction

```java
// Check for QFN-xx pattern (handles BK7231-QFN-32)
int qfnIndex = upperMpn.indexOf("QFN");
if (qfnIndex >= 0) {
    // Extract from QFN including pin count
    // Handle both QFN-32 and QFN32 formats
}

// Check suffix letters if no explicit QFN
if (suffix.startsWith("N") || suffix.startsWith("Q")) {
    return "QFN";
}
```

### Series Extraction

```java
// Extract 6 characters for series (e.g., BK7231, BK3432)
if (upperMpn.matches("^BK7[0-9]{3}.*") ||
    upperMpn.matches("^BK3[0-9]{3}.*")) {
    return upperMpn.substring(0, 6);
}
```

### Wireless Type Detection

```java
// BK7xxx = WiFi + BLE
if (upperMpn.matches("^BK7[0-9]{3}.*")) {
    if (upperMpn.startsWith("BK7256")) return "WIFI6_BLE5";
    return "WIFI_BLE";
}

// BK3xxx = BLE only
if (upperMpn.matches("^BK3[0-9]{3}.*")) {
    if (upperMpn.startsWith("BK3432")) return "BLE5";
    return "BLE";
}
```

---

## Replacement Compatibility

### Same Series Replacements

Parts within the same series are compatible if:
1. Same base series (BK7xxx or BK3xxx)
2. Same or compatible package (QFN with matching pin count)

### Cross-Series Restrictions

- BK7xxx (WiFi+BLE) cannot replace BK3xxx (BLE only) - different interfaces
- BK3xxx cannot replace BK7xxx - missing WiFi capability

### Package Compatibility

```java
// QFN packages with same pin count are compatible
// QFN-32 != QFN-40 (different pinouts)
// Unspecified package assumes compatible
```

---

## Application Guidelines

| Use Case | Recommended Series |
|----------|-------------------|
| Smart home devices | BK7231, BK7256 |
| Audio streaming | BK7251 |
| Wearables | BK3431, BK3432 |
| Low-power sensors | BK3432 |
| WiFi 6 devices | BK7256 |

---

## Development Ecosystem

Beken provides SDK support for:
- FreeRTOS
- Custom Beken OS
- Arduino (community)
- Tuya IoT platform integration

---

## Related Files

- Handler: `manufacturers/BekenHandler.java`
- Component types: `IC`

---

## Learnings & Edge Cases

- **Series determines wireless**: BK7xxx = WiFi+BLE, BK3xxx = BLE only
- **Package in suffix or inline**: Can appear as -QFN-32 or BK7231N
- **Pin count critical**: QFN-32 and QFN-40 are NOT compatible
- **BK7256 special**: Only WiFi 6 (802.11ax) capable chip
- **Audio support varies**: BK7251 has audio codec, BK7231 does not
- **Tuya integration**: Many BK7231 modules are Tuya-based IoT devices
- **WiFi capability**: Only BK7xxx series supports WiFi, all support BLE

<!-- Add new learnings above this line -->
