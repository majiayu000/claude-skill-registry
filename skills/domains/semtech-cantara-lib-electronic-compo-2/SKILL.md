---
name: semtech
description: Semtech Corporation MPN encoding patterns, LoRa transceiver decoding, ESD protection, and handler guidance. Use when working with Semtech components or SemtechHandler.
---

# Semtech Corporation Manufacturer Skill

## MPN Structure

Semtech has several product lines with different MPN structures:

### LoRa Transceivers
```
SX[SERIES][VARIANT]-[PACKAGE]
   |   |      |        |
   |   |      |        +-- Package (QFN, etc.)
   |   |      +-- Variant (frequency band, features)
   |   +-- Series (127x, 126x, 130x)
   +-- Semtech Transceiver prefix
```

### LR11xx Series (Newest LoRa)
```
LR[SERIES][VARIANT]-[PACKAGE]
   |   |      |        |
   |   |      |        +-- Package code
   |   |      +-- Variant (GNSS, features)
   |   +-- Series (1110, 1120, 1121)
   +-- Long Range prefix
```

### ESD Protection
```
[FAMILY][SPEC][PACKAGE]
   |       |      |
   |       |      +-- Package suffix (P=SOT-23, T=SC70)
   |       +-- Clamping voltage/channels
   +-- RCLAMP, SLVU, SM series
```

### Example Decoding

```
SX1276IMLTRT
|  |   |  ||
|  |   |  |+-- T = Tape and Reel
|  |   |  +-- R = Reel packaging
|  |   +-- IMLT = IMLT package
|  +-- 1276 = 868/915 MHz transceiver
+-- SX = Semtech Transceiver

RCLAMP0524P
|     |   |
|     |   +-- P = SOT-23 package
|     +-- 0524 = 5V, 24A clamp
+-- RCLAMP = Rail clamp ESD protection
```

---

## Product Families

### LoRa Transceivers - SX127x (Legacy)

| Part | Frequency | Features |
|------|-----------|----------|
| SX1276 | 868/915 MHz | High performance |
| SX1277 | 868/915 MHz | Lower power |
| SX1278 | 433/470 MHz | Lower frequency |
| SX1279 | 433/470 MHz | Variant |

### LoRa Transceivers - SX126x (Current)

| Part | Frequency | Features |
|------|-----------|----------|
| SX1261 | 868/915 MHz | Low power, +15 dBm |
| SX1262 | 868/915 MHz | High power, +22 dBm |
| SX1268 | 433/490 MHz | Low frequency bands |

### LoRa Gateway Chips - SX130x

| Part | Description |
|------|-------------|
| SX1301 | 8-channel digital baseband (legacy) |
| SX1302 | 8-channel, lower power |
| SX1303 | 8-channel with enhanced features |

### LoRa Edge - LR11xx

| Part | Features |
|------|----------|
| LR1110 | LoRa + GNSS + WiFi scanning |
| LR1120 | Multi-band LoRa transceiver |
| LR1121 | Enhanced LR1120 |

### LLCC68 (Low-Cost LoRa)

| Part | Description |
|------|-------------|
| LLCC68 | Cost-optimized LoRa transceiver |

---

## ESD Protection Products

### RCLAMP Series

Rail clamp ESD protection for high-speed interfaces.

| Part | Channels | Clamping |
|------|----------|----------|
| RCLAMP0502A | 2 | 5V |
| RCLAMP0524P | 2 | 5V, 24A |

### SLVU Series

TVS diode arrays for data lines.

| Part | Description |
|------|-------------|
| SLVU2.8-4 | 2.8V, 4-channel |

### SM Series

TVS protection diodes.

| Part | Description |
|------|-------------|
| SM712 | TVS for RS-485 |
| SM15T33A | 33V TVS |

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| QFN | QFN | Standard QFN |
| QFN24 | QFN-24 | 24-pin QFN |
| QFN32 | QFN-32 | 32-pin QFN |
| TQFN | TQFN | Thin QFN |
| SOT23 | SOT-23 | 3-pin SOT |
| SOT23L | SOT-23-6 | 6-pin SOT |
| SC70 | SC70 | Small package |
| DFN8 | DFN-8 | 8-pin DFN |
| IMLT | IMLT | LoRa module package |
| IMLTR | IMLT-TR | IMLT, tape and reel |
| TR | Tape & Reel | Packaging option |
| TRG | Tape & Reel (Green) | RoHS packaging |

### ESD Part Package Suffixes

```java
// Package embedded in MPN suffix
RCLAMP0524P -> P = SOT-23
RCLAMP0524T -> T = SC70
```

---

## Signal Integrity Products

### ClearEdge Series

| Prefix | Description |
|--------|-------------|
| GN | ClearEdge clock/data |
| GS | Signal conditioners |

| Part | Description |
|------|-------------|
| GN2033 | Quad LVDS repeater |
| GS12090 | 12G video redriver |

---

## Power Management

### SC Series

| Part | Description |
|------|-------------|
| SC4238 | Buck converter |
| SC5501 | LED driver |

### SY Series (Former Micrel)

| Part | Description |
|------|-------------|
| SY8089 | Sync buck regulator |
| SY8113 | 3A sync buck |

---

## Handler Implementation Notes

### Series Extraction

```java
// LoRa transceivers - extract full series (6 chars)
// SX1276IMLTRT -> SX1276
if (upperMpn.startsWith("SX127")) {
    return extractUpToDigitsOrDash(upperMpn, 6);
}

// ESD protection - extract family name
// RCLAMP0524P -> RCLAMP
if (upperMpn.startsWith("RCLAMP")) {
    return "RCLAMP";
}
```

### Package Code Extraction

```java
// Extract from suffix after last hyphen
// SX1262-QFN24 -> QFN-24

// ESD parts encode package in MPN
// RCLAMP0524P -> P -> SOT-23
```

### Matching Logic

The handler supports multiple component types:
- `ComponentType.IC` - for all Semtech ICs
- `ComponentType.RF_IC_SKYWORKS` - for LoRa transceivers (RF)
- `ComponentType.ESD_PROTECTION_NEXPERIA` - for ESD protection devices

---

## Series Compatibility

### LoRa Transceiver Compatibility

```
SX127x family - NOT compatible with SX126x (different API)
SX1261 <-> SX1262 - Compatible (different power output)
SX1262 <-> SX1268 - Compatible for overlapping frequencies
SX1302 <-> SX1303 - Gateway chips, compatible
LR11xx family - Compatible within family
```

### Handler `isOfficialReplacement()` Logic

```java
// Same series with different packages are compatible
// SX1261 and SX1262 are compatible (power difference)
// SX1302 and SX1303 are compatible (gateway chips)
// LR11xx series are compatible within family
// Different generations (SX127x vs SX126x) are NOT directly compatible
```

---

## Related Files

- Handler: `manufacturers/SemtechHandler.java`
- Component types: `IC`, `RF_IC_SKYWORKS`, `ESD_PROTECTION_NEXPERIA`

---

## Common MPNs

| MPN | Description | Application |
|-----|-------------|-------------|
| SX1276IMLTRT | 868/915 MHz LoRa | Long range IoT |
| SX1262IMLTRT | 868/915 MHz LoRa | Low power IoT |
| SX1302CSS | LoRa gateway | 8-channel gateway |
| LR1110IMLTRT | LoRa + GNSS | Asset tracking |
| LLCC68 | Low-cost LoRa | Consumer IoT |
| RCLAMP0524P | ESD protection | USB interfaces |
| SM712 | RS-485 TVS | Industrial comm |

---

## Applications

- LoRaWAN IoT devices
- Long-range wireless sensors
- Smart meters
- Asset tracking
- LoRa gateways
- ESD protection for USB, HDMI, Ethernet
- Industrial communication (RS-485)

---

## Learnings & Edge Cases

- **LoRa vs LoRaWAN**: SX chips are transceivers; LoRaWAN is a protocol running on top.
- **SX127x vs SX126x API difference**: These generations use different register APIs - not drop-in replacements.
- **Frequency bands in MPN**: Not always explicit - SX1276 supports 868/915, SX1278 supports 433/470.
- **IMLT package**: Common for LoRa modules, includes matching network.
- **ESD protection naming**: RCLAMP = rail clamp (fast), SLVU = TVS array.
- **Power output difference**: SX1261 (+15 dBm) vs SX1262 (+22 dBm) - different power levels, same pinout.
- **LR11xx multi-function**: These include LoRa + GNSS + WiFi scanning in one chip for geolocation.

<!-- Add new learnings above this line -->
