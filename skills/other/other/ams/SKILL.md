---
name: ams
description: ams-OSRAM MPN encoding patterns, suffix decoding, and handler guidance. Use when working with ams sensor products, optical components, or AMSHandler.
---

# ams-OSRAM Manufacturer Skill

## Manufacturer Overview

**ams-OSRAM** (formerly Austria Microsystems, merged with OSRAM Opto Semiconductors) is a global leader in optical solutions, including:

- **Spectral Sensors** - Multi-channel spectral sensing (AS72xx, AS73xx, AS6xxx)
- **Light Sensors** - Ambient light and light-to-digital sensors (TSL2xxx)
- **Proximity Sensors** - Proximity and gesture detection (TMD2xxx, APDS-9xxx)
- **Color Sensors** - RGB and XYZ color sensing (TCS3xxx)
- **Position Sensors** - Magnetic rotary encoders (AS5xxx)
- **Environmental Sensors** - Air quality, humidity, temperature (ENSxxx)
- **LED Drivers** - Constant current LED drivers (AS3xxx)

**Note**: OSRAM LEDs are handled by the separate `OSRAMHandler`. This handler covers ams sensor products and ICs.

---

## MPN Structure

ams MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][-][PACKAGE/QUALIFIER]
   |       |       |     |        |
   |       |       |     |        +-- Package code, automotive grade, or tape/reel
   |       |       |     +-- Optional hyphen separator
   |       |       +-- Variant digit (channel count, version)
   |       +-- Series number (2-3 digits)
   +-- Family prefix (AS, TSL, TMD, TCS, APDS, ENS)
```

### Example Decodings

```
AS7262-BLGT
|  |   |  |
|  |   |  +-- GT = Green/Tape (RoHS)
|  |   +-- BL = BGA Lead-free
|  +-- 62 = 6-channel visible spectral sensor
+-- AS72 = Spectral sensor family

TSL2591FN
|   |   |
|   |   +-- FN = QFN package
|   +-- 591 = High-dynamic-range light sensor
+-- TSL2 = Light-to-digital sensor family

APDS-9960
|    |  |
|    |  +-- 60 = Gesture-enabled variant
|    +-- 99 = Proximity/gesture series
+-- APDS = Advanced Proximity Detection System

TCS34725FN
|   |   |
|   |   +-- FN = QFN package
|   +-- 725 = Color sensor with IR blocking filter
+-- TCS3 = Color sensor family

ENS160-BLGT
|   |  |
|   |  +-- BLGT = BGA Lead-free Green/Tape
|   +-- 160 = Metal oxide gas sensor (VOC/CO2)
+-- ENS = Environmental sensor family
```

---

## Product Families

### AS72xx - Spectral Sensors (Visible)

| Part | Description | Channels | Wavelengths |
|------|-------------|----------|-------------|
| AS7261 | Spectral ID sensor | 6 | XYZ + NIR |
| AS7262 | 6-channel visible | 6 | 450-650nm |
| AS7263 | 6-channel NIR | 6 | 610-860nm |
| AS7265x | 18-channel combo | 18 | 410-940nm (3 chips) |

### AS73xx - Spectral Sensors (Advanced)

| Part | Description | Channels |
|------|-------------|----------|
| AS7341 | 11-channel spectral | 11 |
| AS7343 | 14-channel spectral | 14 |

### TSL2xxx - Light-to-Digital Sensors

| Part | Description | Dynamic Range |
|------|-------------|---------------|
| TSL2561 | Light sensor | 1:1,000,000 |
| TSL2591 | High-DR light sensor | 1:600,000,000 |

### TMD2xxx - Proximity/ALS Sensors

| Part | Description | Features |
|------|-------------|----------|
| TMD2671 | Proximity sensor | IR LED driver |
| TMD2772 | Prox + ALS combo | IR proximity |
| TMD26721 | Enhanced proximity | Improved sensitivity |

### TCS3xxx - Color Sensors

| Part | Description | Features |
|------|-------------|----------|
| TCS3400 | Color sensor | IR blocking filter |
| TCS3472 | RGB color light | Clear channel |
| TCS34725 | Color sensor | Enhanced IR block |

### APDS-9xxx - Proximity/Gesture Sensors

| Part | Description | Features |
|------|-------------|----------|
| APDS-9930 | Prox + ALS | Digital ambient light |
| APDS-9960 | Gesture + Prox + RGB | 4-way gesture detection |

### AS3xxx - LED Drivers

| Part | Description | Channels |
|------|-------------|----------|
| AS3935 | Lightning sensor IC | - |
| AS3933 | LF wake-up receiver | 3 |

### AS5xxx - Position Sensors (Magnetic Encoders)

| Part | Description | Resolution |
|------|-------------|------------|
| AS5047 | Rotary encoder | 14-bit |
| AS5048 | Rotary encoder | 14-bit |
| AS5600 | Rotary encoder | 12-bit |

### ENSxxx - Environmental Sensors

| Part | Description | Measurements |
|------|-------------|--------------|
| ENS160 | Air quality sensor | VOC, CO2 equivalent |
| ENS210 | Humidity/temp sensor | RH + temperature |
| ENS220 | Barometric pressure | Pressure + temp |

---

## Package Codes

### Suffix Patterns (After Hyphen)

| Suffix | Package | Description |
|--------|---------|-------------|
| BLGT | BGA | BGA Lead-free Green/Tape |
| BGA | BGA | Ball Grid Array |
| FN | QFN | Quad Flat No-leads |
| QFN | QFN | Quad Flat No-leads |
| LGA | LGA | Land Grid Array |
| TSL | DFN | Special TSL suffix (typically DFN) |
| ASIL | (varies) | Automotive Safety Integrity Level variant |
| ASOM | MODULE | Module variant |
| TR | TAPE_REEL | Tape and Reel packaging |

### Direct Suffixes (No Hyphen)

| Suffix | Package | Example |
|--------|---------|---------|
| FN | QFN | TMD26721FN, TCS34725FN |
| LGA | LGA | AS7262LGA |

---

## Supported Component Types

The `AMSHandler` supports these `ComponentType` values:

| ComponentType | Product Families |
|---------------|------------------|
| `SENSOR` | All sensor families (AS72xx, AS73xx, TSL2xxx, TMD2xxx, TCS3xxx, APDS-9xxx, AS5xxx, AS6xxx, ENSxxx) |
| `SENSOR_PROXIMITY` | TMD2xxx, APDS-9xxx |
| `HUMIDITY_SENSOR` | ENSxxx |
| `LED_DRIVER` | AS3xxx |
| `IC` | All families (base type) |

---

## Series Extraction Rules

The handler extracts series using these rules:

| Pattern | Extracted Series | Example |
|---------|------------------|---------|
| `APDS-?9xxx` | `APDS` | APDS-9960 -> APDS |
| `TSLxxxx` | `TSL` | TSL2591 -> TSL |
| `TMDxxxx` | `TMD` | TMD2772 -> TMD |
| `TCSxxxx` | `TCS` | TCS34725 -> TCS |
| `ENSxxx` | `ENS` | ENS160 -> ENS |
| `ASnnxx` | `ASnn` (4 chars) | AS7262 -> AS72, AS5600 -> AS56 |

---

## Package Code Extraction Rules

```java
// 1. Check for hyphenated suffix
int lastHyphen = mpn.lastIndexOf('-');
if (lastHyphen >= 0) {
    String suffix = mpn.substring(lastHyphen + 1);
    // Skip numeric-only suffixes (model numbers like APDS-9960)
    if (!suffix.matches("^[0-9]+$")) {
        // Map known package codes
        switch (suffix) {
            case "BLGT": return "BGA";
            case "FN", "QFN": return "QFN";
            case "LGA": return "LGA";
            case "ASOM": return "MODULE";
            // Check for embedded indicators
            if (suffix.endsWith("FN")) return "QFN";
        }
    }
}

// 2. Check for direct suffix (no hyphen)
if (mpn.endsWith("FN")) return "QFN";
if (mpn.endsWith("LGA")) return "LGA";
```

---

## Compatible Replacement Rules

The handler defines these compatibility groups:

### AS72xx Spectral Sensors
- AS7261, AS7262, AS7263 are compatible (same interface, different wavelengths)
- AS7265x variants are compatible with each other

### TSL Light Sensors
- TSL2561 and TSL2591 are compatible (same family, different specs)

### TCS Color Sensors
- TCS3472x variants are compatible (TCS3472, TCS34725)

### APDS Proximity/Gesture
- APDS-99xx variants are compatible within the series

### AS5xxx Position Sensors
- AS50xx variants are compatible (same interface, different resolution)
- AS56xx variants are compatible with each other

### ENS Environmental Sensors
- ENS sensors are NOT interchangeable (different measurements)

---

## Interface Extraction

Some ams parts indicate interface type in the MPN:

| Suffix | Interface |
|--------|-----------|
| `-I2C` or `I` | I2C |
| `-SPI` or `S` | SPI |
| `-ANA` or `A` | Analog |

---

## Example MPNs with Full Decoding

| MPN | Family | Type | Package | Notes |
|-----|--------|------|---------|-------|
| AS7262-BLGT | AS72xx | Spectral Sensor | BGA | 6-ch visible, lead-free tape |
| AS7341 | AS73xx | Spectral Sensor | (default) | 11-channel spectral |
| TSL2591FN | TSL2xxx | Light Sensor | QFN | High dynamic range |
| TMD26721FN | TMD2xxx | Proximity Sensor | QFN | Enhanced proximity |
| TCS34725FN | TCS3xxx | Color Sensor | QFN | RGB with IR block |
| APDS-9960 | APDS-9xxx | Gesture Sensor | (default) | 4-way gesture |
| APDS-9960-ASIL | APDS-9xxx | Gesture Sensor | QFN | Automotive variant |
| AS5600-ASOM | AS5xxx | Position Sensor | MODULE | 12-bit magnetic encoder |
| ENS160-BLGT | ENSxxx | Air Quality | BGA | VOC/CO2 sensor |
| ENS210-LQFN | ENSxxx | Humidity Sensor | QFN | Humidity + temp |

---

## Related Files

- Handler: `manufacturers/AMSHandler.java`
- Component types: `SENSOR`, `SENSOR_PROXIMITY`, `HUMIDITY_SENSOR`, `LED_DRIVER`, `IC`
- Note: No manufacturer-specific ComponentTypes (e.g., `SENSOR_AMS`) defined

---

## Handler Implementation Notes

### Pattern Matching

The handler uses pre-compiled patterns for performance:

```java
private static final Pattern AS72XX_PATTERN = Pattern.compile("^AS72[0-9]{2}.*", Pattern.CASE_INSENSITIVE);
private static final Pattern APDS9XXX_PATTERN = Pattern.compile("^APDS-?9[0-9]{3}.*", Pattern.CASE_INSENSITIVE);
```

### matches() Override

The handler explicitly overrides `matches()` to avoid cross-handler pattern matching issues:

```java
@Override
public boolean matches(String mpn, ComponentType type, PatternRegistry patterns) {
    // Each family explicitly checked
    if (AS72XX_PATTERN.matcher(upperMpn).matches()) {
        return type == ComponentType.SENSOR || type == ComponentType.IC;
    }
    // ... etc for each family
}
```

### getSupportedTypes() Uses Set.of()

The handler correctly uses immutable `Set.of()`:

```java
@Override
public Set<ComponentType> getSupportedTypes() {
    return Set.of(
        ComponentType.SENSOR,
        ComponentType.SENSOR_PROXIMITY,
        ComponentType.HUMIDITY_SENSOR,
        ComponentType.LED_DRIVER,
        ComponentType.IC
    );
}
```

---

## Learnings & Quirks

- **APDS hyphen handling**: The APDS family uses a hyphen in the name (APDS-9960), which complicates package extraction. The handler correctly skips numeric-only suffixes after the hyphen.

- **Multiple sensor types**: Many ams sensors are registered under both `SENSOR` (generic) and more specific types like `SENSOR_PROXIMITY` or `HUMIDITY_SENSOR`. Always check for the most specific type first.

- **No manufacturer-specific ComponentTypes**: Unlike TI or ST, ams does not have manufacturer-specific component types (e.g., `SENSOR_AMS`). All types are generic.

- **ENS sensors not interchangeable**: Unlike other families where variants are compatible, ENS160 (air quality), ENS210 (humidity), and ENS220 (pressure) measure different things and are NOT replacements for each other.

- **AS5xxx resolution differences**: Position sensors in the same sub-family (AS50xx, AS56xx) are compatible but have different resolutions (12-bit vs 14-bit). Consider application requirements when substituting.

- **OSRAM LED separation**: LED products from OSRAM are handled by `OSRAMHandler`, not `AMSHandler`. This handler focuses on ams sensor products only.

- **BLGT suffix decoding**: BLGT = BGA Lead-free Green/Tape - a common packaging designation for RoHS-compliant BGA parts on tape for pick-and-place.

<!-- Add new learnings above this line -->
