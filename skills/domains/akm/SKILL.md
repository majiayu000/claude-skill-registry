---
name: akm
description: AKM (Asahi Kasei Microdevices) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with AKM audio ICs, magnetic sensors, or electronic compasses.
---

# AKM (Asahi Kasei Microdevices) Manufacturer Skill

## Company Overview

AKM (Asahi Kasei Microdevices) is a Japanese semiconductor manufacturer specializing in:
- **Audio ICs**: High-performance DACs and ADCs for professional and consumer audio
- **Magnetic Sensors**: 3-axis magnetometers and electronic compasses
- **Hall Effect Sensors**: Position and rotation sensing
- **IMUs**: Combined 9-axis sensors with accelerometer, gyroscope, and magnetometer

AKM is renowned for their premium audio converters used in high-end audio equipment and their compact magnetic sensors used in smartphones and wearables.

---

## MPN Structure

AKM MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][-][PACKAGE/OPTIONS]
   |       |       |           |
   |       |       |           +-- Package code or options
   |       |       +-- Variant/revision letter
   |       +-- Series number (4-5 digits)
   +-- Always "AK" prefix
```

### Naming Convention by Product Family

```
Audio ICs:
AK4490 EQ    - Premium 32-bit DAC
AK4493 SEQ   - Upgraded premium DAC
AK5386 VT    - 24-bit ADC
AK4796 VQ    - Audio DAC

Magnetic Sensors:
AK8963 C     - 3-axis electronic compass
AK8975 A     - 3-axis compass
AK09918      - 3-axis compass, newer series

9-axis IMUs:
AK09911 C    - 9-axis sensor (accel+gyro+compass)
AK09912      - 9-axis with improved gyroscope
AK09913      - 9-axis combined sensor
```

---

## Product Families

### Audio DACs (AK47xx, AK44xx)

| Series | Description | Bits | Channels | Notes |
|--------|-------------|------|----------|-------|
| AK4490 | Premium DAC | 32-bit | 2 | Flagship, VELVET SOUND |
| AK4493 | Premium DAC | 32-bit | 2 | Successor to AK4490 |
| AK4495 | Premium DAC | 32-bit | 2 | Enhanced performance |
| AK4497 | Reference DAC | 32-bit | 2 | Top of line |
| AK4796 | General DAC | 24-bit | 2 | Cost-effective |

### Audio ADCs (AK44xx, AK53xx)

| Series | Description | Bits | Channels | Notes |
|--------|-------------|------|----------|-------|
| AK4490 | High-perf ADC | 24-bit | 2 | Multi-bit delta-sigma |
| AK5386 | Stereo ADC | 24-bit | 2 | Professional audio |

### Magnetic Sensors / Electronic Compasses (AK89xx, AK099xx)

| Series | Description | Interface | Resolution | Notes |
|--------|-------------|-----------|------------|-------|
| AK8963 | 3-axis compass | I2C/SPI | 14/16-bit | Widely used, smartphones |
| AK8975 | 3-axis compass | I2C | 13-bit | Older series |
| AK09911 | 9-axis IMU | I2C | 16-bit | With accelerometer |
| AK09912 | 9-axis IMU | I2C | 16-bit | With gyroscope |
| AK09913 | 9-axis IMU | I2C | 16-bit | Combined sensor |
| AK09918 | 3-axis compass | I2C | 16-bit | Newer, high precision |
| AK09940 | 3-axis compass | I2C/SPI | 18-bit | High precision |

### High Precision Magnetic Sensors (AK099xx)

| Series | Description | Notes |
|--------|-------------|-------|
| AK09970 | Linear position sensor | Hall effect |
| AK09973 | Switch sensor | Omnipolar |
| AK09911-AK09916 | Hall sensors | Various applications |

---

## Package Codes

Package codes appear as suffixes, typically separated or as trailing letters:

| Code | Package | Size | Notes |
|------|---------|------|-------|
| TR | LGA | 1.6x1.6mm | Tape and reel, common for sensors |
| CS | CSP | Small | Chip-scale package |
| WL | WLCSP | Tiny | Wafer-level CSP |
| TS | TSSOP | - | Thin shrink small outline |
| QFN | QFN | Various | Quad flat no-lead |
| BGA | BGA | Various | Ball grid array |
| EQ | QFN | 5x5mm | Audio DAC package |
| VT | TQFP | 7x7mm | Audio ADC package |
| VQ | QFP | - | Standard quad flat |
| SEQ | QFN | - | Enhanced QFN variant |

### Package Extraction Logic

```java
// From AKMHandler.extractPackageCode():
// Split on hyphen, take suffix from main part
String[] parts = mpn.split("-");
String mainPart = parts[0];
String suffix = mainPart.replaceAll("^[A-Z0-9]+", "");

// Map known suffixes
switch (suffix) {
    case "TR" -> "LGA";
    case "CS" -> "CSP";
    case "WL" -> "WLCSP";
    case "TS" -> "TSSOP";
    case "QFN" -> "QFN";
    case "BGA" -> "BGA";
    default -> suffix;  // Return as-is
}
```

---

## Series Extraction Rules

The handler uses different extraction lengths based on product family:

| Family | Prefix | Series Length | Example |
|--------|--------|---------------|---------|
| Audio ICs | AK4, AK5 | 5 characters | AK4490, AK5386 |
| Sensors | AK8, AK09 | 6 characters | AK8963C, AK09918 |

### Series Extraction Logic

```java
// From AKMHandler.extractSeries():
boolean isAudioIC = mpn.startsWith("AK4") || mpn.startsWith("AK5");
int maxLength = isAudioIC ? 5 : 6;

// Extract up to maxLength alphanumeric characters
// AK4490EQ -> AK449 (audio IC, 5 chars)
// AK8963C  -> AK8963 (sensor, 6 chars)
// AK09918  -> AK0991 (sensor, 6 chars)
```

---

## Interface Detection

For magnetic sensors, interface type can be extracted from the MPN:

| Suffix/Indicator | Interface | Notes |
|------------------|-----------|-------|
| Ends with "I" | I2C | I2C interface |
| Ends with "S" | SPI | SPI interface |
| Contains "I2C" | I2C | Explicit in name |
| Contains "SPI" | SPI | Explicit in name |

### Resolution Detection

For sensors, resolution may be indicated in the MPN:

| Indicator | Resolution | Notes |
|-----------|------------|-------|
| Contains "14BIT" | 14-bit | Lower resolution mode |
| Contains "16BIT" | 16-bit | Standard resolution |

---

## Supported Component Types

From `AKMHandler.getSupportedTypes()`:

| ComponentType | Description | Pattern Examples |
|---------------|-------------|------------------|
| SENSOR | General sensors, IMUs | AK09[0-9].*, AK0991[0-9].* |
| MAGNETOMETER | Magnetic sensors, compasses | AK89[0-9].*, AK099.*, AK8963.*, AK8975.*, AK09918.* |
| IC | Audio DACs and ADCs | AK449[0-9].*, AK479[0-9].*, AK4490.*, AK5386.* |

**Note**: The handler has commented-out types (HALL_SENSOR, ADC, DAC) that may not exist in the ComponentType enum.

---

## Pattern Registry

Patterns registered in `AKMHandler.initializePatterns()`:

### Magnetometer Patterns
```java
// 3-axis magnetic sensors
"^AK89[0-9].*"       // AK8963, AK8975 series
"^AK099.*"           // AK099xx high precision
"^AK8963.*"          // Electronic compass
"^AK8975.*"          // Electronic compass
"^AK09918.*"         // 3-axis compass
```

### Sensor/IMU Patterns
```java
// 9-axis and Hall sensors
"^AK09[0-9].*"       // General 9-axis
"^AK09911.*"         // 9-axis with accelerometer
"^AK09912.*"         // 9-axis with gyroscope
"^AK09913.*"         // 9-axis combined
"^AK0991[0-9].*"     // Hall sensors
```

### Audio IC Patterns
```java
// DACs and ADCs
"^AK449[0-9].*"      // Audio ADC series
"^AK479[0-9].*"      // Audio DAC series
"^AK4490.*"          // Premium DAC
"^AK5386.*"          // Audio ADC
```

---

## Official Replacement Logic

The `isOfficialReplacement()` method checks compatibility based on:

### For Sensors (AK8x, AK09x)
1. Same series
2. Same resolution (14-bit vs 16-bit)
3. Compatible interface (I2C/SPI or unspecified)

### For Audio ICs (AK4x, AK5x)
1. Same series
2. Same sample rate (48/96/192 kHz)

---

## Example MPNs with Explanations

### Audio DACs

```
AK4490EQ
|  |  ||
|  |  |+-- Package: QFN (5x5mm)
|  |  +--- E: Enhanced variant
|  +------ 4490: Premium 32-bit DAC
+--------- AK: AKM prefix

AK4493SEQ
|  |  | |
|  |  | +-- Package: QFN
|  |  +---- S: Super variant
|  +------- 4493: Successor to AK4490
+---------- AK: AKM prefix

AK5386VT
|  |  ||
|  |  |+-- Package: TQFP (7x7mm)
|  |  +--- V: Voltage variant
|  +------ 5386: 24-bit stereo ADC
+--------- AK: AKM prefix
```

### Magnetic Sensors

```
AK8963C
|  |  |
|  |  +--- C: Revision C
|  +------ 8963: 3-axis electronic compass
+--------- AK: AKM prefix

AK09918
|  |
|  +------ 09918: Latest 3-axis compass
+--------- AK: AKM prefix

AK09911C
|  |   |
|  |   +-- C: Revision
|  +------ 09911: 9-axis IMU with accelerometer
+--------- AK: AKM prefix
```

### Hall Effect Sensors

```
AK09915
|  |
|  +------ 09915: Hall effect sensor
+--------- AK: AKM prefix

AK09970D
|  |   |
|  |   +-- D: Grade/variant
|  +------ 09970: Linear position sensor
+--------- AK: AKM prefix
```

---

## Related Files

- Handler: `manufacturers/AKMHandler.java`
- Component types: `SENSOR`, `MAGNETOMETER`, `IC`
- Pattern registry: `PatternRegistry.java`

---

## Learnings & Quirks

### Handler Implementation

- **getSupportedTypes() uses HashSet**: Should be migrated to `Set.of()` for immutability (known technical debt)
- **IC type needed**: Audio IC patterns are registered under `ComponentType.IC`, so IC must be in getSupportedTypes() for matches to work correctly
- **Commented-out types**: HALL_SENSOR, ADC, DAC types are commented out in getSupportedTypes() - may indicate missing ComponentType definitions

### Pattern Overlap

- **AK09xxx series**: Multiple patterns overlap (AK09[0-9], AK099, AK09911, etc.) - more specific patterns should be checked first
- **Sensor vs Magnetometer**: AK099xx matches both SENSOR (AK09[0-9]) and MAGNETOMETER (AK099) patterns - first match wins

### Series Extraction

- **Length varies by family**: Audio ICs use 5 chars, sensors use 6 chars
- **Includes variant letter**: For sensors, the series includes the variant letter (AK8963C -> AK8963, but for shorter audio ICs AK4490EQ -> AK449)

### Replacement Compatibility

- **Sample rate matching for audio**: Audio ICs require matching sample rates (48/96/192 kHz) for replacement compatibility
- **Interface compatibility for sensors**: Sensors with unspecified interface can match either I2C or SPI variants

### Common Applications

- **AK8963**: Very popular in consumer electronics, used in smartphone compasses
- **AK4490**: Reference DAC for high-end audio equipment
- **AK09918**: Modern smartphone compass IC

### Fire at AKM Factory (2020)

In October 2020, a fire at AKM's primary manufacturing facility severely impacted production:
- Many audio DAC/ADC products had extended lead times
- Some products were EOL'd
- Competitors (ESS, Cirrus Logic) gained market share
- Recovery took 2+ years for some product lines

Consider lifecycle status when specifying AKM components.

<!-- Add new learnings above this line -->
