---
name: isocom
description: Isocom Components MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Isocom optocouplers or IsocomHandler.
---

# Isocom Components Manufacturer Skill

## Overview

Isocom Components is a manufacturer of optocouplers and solid state relays. Their product lines include proprietary ISP/ISQ/ISD series as well as industry-standard compatible devices.

## MPN Structure

Isocom MPNs follow these general patterns:

### ISP/ISQ/ISD Series (Isocom Proprietary)

```
[PREFIX][SERIES][CTR-GRADE][-PACKAGE][X]
   |       |        |          |      |
   |       |        |          |      +-- Optional: X = Lead-free (RoHS)
   |       |        |          +-- Package: -1=DIP-4, -2=DIP-6, -4=DIP-8
   |       |        +-- CTR Grade: A/B/C/D (Current Transfer Ratio)
   |       +-- Series number (e.g., 817, 827, 847)
   +-- Prefix: ISP, ISQ, ISD
```

### Example Decoding

```
ISP817A-1X
|  |  | | |
|  |  | | +-- X = Lead-free
|  |  | +-- -1 = DIP-4 package
|  |  +-- A = CTR grade (highest CTR)
|  +-- 817 = Series number
+-- ISP = Phototransistor output

ISQ827B
|  |  |
|  |  +-- B = CTR grade (medium-high CTR)
|  +-- 827 = Dual channel series
+-- ISQ = High CTR optocoupler
```

---

## Product Lines

### ISP Series - Phototransistor Output

| Series | Description | Channels |
|--------|-------------|----------|
| ISP817 | General purpose phototransistor | 1 |
| ISP827 | Dual channel phototransistor | 2 |
| ISP847 | Quad channel phototransistor | 4 |

### ISQ Series - High CTR

| Series | Description | Channels |
|--------|-------------|----------|
| ISQ817 | High CTR optocoupler | 1 |
| ISQ827 | High CTR dual channel | 2 |

### ISD Series - Darlington Output

| Series | Description | Output |
|--------|-------------|--------|
| ISD817 | Darlington output | Single |
| ISD827 | Darlington dual | Dual |

### 4N Series - Standard Optocouplers

| Part | Description | Isolation |
|------|-------------|-----------|
| 4N25 | Phototransistor output | 5300V |
| 4N26 | Phototransistor output | 5300V |
| 4N27 | Phototransistor output | 5300V |
| 4N28 | Phototransistor output | 5300V |
| 4N35 | Phototransistor, high isolation | 7500V |
| 4N36 | Phototransistor, high isolation | 7500V |
| 4N37 | Phototransistor, high isolation | 7500V |

### 6N Series - Logic Output

| Part | Description | Output |
|------|-------------|--------|
| 6N135 | High speed, TTL compatible | Push-pull |
| 6N136 | High speed, TTL compatible | Push-pull |
| 6N137 | High speed logic output | Totem pole |
| 6N138 | Darlington output | Open collector |
| 6N139 | Darlington output | Open collector |

### MOC Series - Triac/SCR Drivers

| Prefix | Description | Driver Type |
|--------|-------------|-------------|
| MOC30xx | Zero-crossing triac | Safe switch-on at zero |
| MOC31xx | Random phase triac | Switch any phase |
| MOC32xx | SCR output | Thyristor driver |

---

## CTR (Current Transfer Ratio) Grades

For ISP/ISQ/ISD series:

| Grade | CTR Range | Application |
|-------|-----------|-------------|
| A | 80-160% | Highest gain, lowest LED current needed |
| B | 130-260% | High gain |
| C | 200-400% | Medium gain |
| D | 300-600% | Wide range, lower gain |

**Note**: Grade A can typically replace B/C/D in applications. Higher letter = lower minimum CTR.

---

## Package Codes

| Code | Package | Pins | Notes |
|------|---------|------|-------|
| -1 | DIP-4 | 4 | Standard 4-pin DIP |
| -2 | DIP-6 | 6 | 6-pin DIP (dual channel) |
| -4 | DIP-8 | 8 | 8-pin DIP (quad channel) |
| -1S | SMD-4 | 4 | SMD variant |
| -2S | SMD-6 | 6 | SMD variant |
| -4S | SMD-8 | 8 | SMD variant |
| X | Lead-free | - | RoHS compliant suffix |

### Default Packages by Series

| Series | Default Package |
|--------|-----------------|
| 4N | DIP-6 |
| 6N | DIP-8 |
| MOC | DIP-6 |
| H11 | DIP-6 |
| ISP817 | DIP-4 |
| ISQ/ISD | DIP-4 |

---

## Compatible/Equivalent Series

Isocom makes drop-in replacements for:

| Isocom | Original | Manufacturer |
|--------|----------|--------------|
| TLP521 | TLP521 | Toshiba |
| TLP621 | TLP621 | Toshiba |
| PC817 | PC817 | Sharp |
| CNY17 | CNY17 | Vishay |
| IL300 | IL300 | Vishay |
| SFH6xxx | SFH6xxx | OSRAM |
| H11xx | H11xx | Fairchild |

---

## Handler Implementation Notes

### Pattern Matching

```java
// Isocom-specific series (ISP, ISQ, ISD)
"^IS[PQD][0-9]{3}.*"

// Standard optocoupler series
"^4N[0-9]{2}.*"        // 4N25, 4N35, etc.
"^6N1[0-9]{2}.*"       // 6N135, 6N137, etc.

// MOC triac/SCR drivers
"^MOC3[0-2][0-9]{2}.*" // MOC30xx, MOC31xx, MOC32xx
```

### Series Extraction

```java
// ISP/ISQ/ISD returns the prefix
"ISP817A" -> "ISP"
"ISQ827B" -> "ISQ"
"ISD817-1" -> "ISD"

// 4N returns specific part
"4N25" -> "4N25"
"4N35A" -> "4N35"

// MOC returns prefix group
"MOC3020" -> "MOC30xx"
"MOC3162" -> "MOC31xx"
```

### Package Extraction Logic

```java
// Check hyphen-based suffix first
"ISP817A-1" -> "DIP-4"
"ISP817A-1S" -> "SMD-4"

// Trailing digit for IS* series (no hyphen)
"ISP8171" -> "DIP-4"

// Default by series
"4N25" -> "DIP-6"  // No explicit package
"6N137" -> "DIP-8"
"MOC3020" -> "DIP-6"
```

### Replacement Logic

- Same IS* series with different CTR grades: higher grade (A) can replace lower (B/C/D)
- 4N series within same group (25-28 or 35-37) are often interchangeable
- MOC series must match driver type (30xx, 31xx, 32xx not interchangeable)
- Package must be compatible (DIP cannot replace SMD directly)

---

## Related Files

- Handler: `manufacturers/IsocomHandler.java`
- Component types: `ComponentType.IC`

---

## Learnings & Edge Cases

- **4N series package detection**: Do NOT apply trailing digit package logic to 4N series. "4N25" ends with "5" but that's the part number, not a package code. Always return default DIP-6 for 4N.
- **CTR grade position**: CTR grade letter comes immediately after the 3-digit series number, before any hyphen or suffix.
- **MOC compatibility**: MOC30xx (zero-crossing) and MOC31xx (random phase) are NOT interchangeable - they have different triggering behavior.
- **6N series speed**: 6N137 is significantly faster than 6N135/6N136. Not always interchangeable in high-speed applications.
- **Lead-free suffix**: X suffix indicates RoHS compliance. Does not affect electrical compatibility.

<!-- Add new learnings above this line -->
