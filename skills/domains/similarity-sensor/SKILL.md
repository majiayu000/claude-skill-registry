---
name: similarity-sensor
description: Use when working with sensor similarity calculations - comparing temperature/accelerometer/humidity sensor MPNs, understanding sensor families, equivalent parts, or sensor-specific similarity logic.
---

# Sensor Similarity Calculator Skill

Guidance for working with `SensorSimilarityCalculator` in the lib-electronic-components library.

## Overview

The `SensorSimilarityCalculator` compares sensors based on:
- **Sensor family** - Temperature, accelerometer, humidity, pressure, etc.
- **Equivalent parts** - Known interchangeable sensors
- **Package variants** - Same sensor in different packages

## Applicable Types

```java
ComponentType.SENSOR
ComponentType.TEMPERATURE_SENSOR
ComponentType.ACCELEROMETER
// Any type starting with "SENSOR_", "TEMPERATURE_SENSOR_", "ACCELEROMETER_"
```

Returns `false` for `null` type.

## Similarity Thresholds

```java
HIGH_SIMILARITY = 0.9;   // Same sensor, compatible packages
MEDIUM_SIMILARITY = 0.7; // Same sensor, incompatible packages
LOW_SIMILARITY = 0.3;    // Different sensor families
```

## Sensor Families

| Family | Detection Patterns |
|--------|-------------------|
| Temperature | LM35*, DS18*, TMP*, MAX318* |
| Accelerometer | ADXL*, MMA*, LIS2*, LIS3*, BMI*, ICM* |
| Gyroscope | L3GD*, ITG*, MPU* |
| Humidity | SHT*, HIH*, AM*, HDC* |
| Pressure | BMP*, BME*, MS56*, LPS* |
| Combined | BME* (temp+humidity+pressure), MPU* (accel+gyro) |

**Different sensor families always return LOW_SIMILARITY (0.3)**

## Temperature Sensor Equivalents

| Sensor | Equivalents |
|--------|-------------|
| DS18B20 | DS18B20+, DS18B20Z, DS18B20/T |
| DS18B20 | MAX31820 (compatible) |
| LM35 | LM35D, LM35C, LM35A (grade variants) |
| TMP36 | TMP36GT9Z, TMP36FS |

```java
calculator.calculateSimilarity("DS18B20+", "DS18B20Z", registry);
// Returns 0.9 (same sensor, package variants)
```

## Accelerometer Rules

Accelerometers are compared strictly by model:

```java
// Same accelerometer
calculator.calculateSimilarity("ADXL345BCCZ", "ADXL345BCCZ-RL", registry);
// Returns 0.9 (same part, reel variant)

// Different models
calculator.calculateSimilarity("ADXL345", "ADXL346", registry);
// Returns 0.3 (different accelerometer)
```

## Humidity Sensor Equivalents

| Family | Compatible Parts |
|--------|------------------|
| SHT3x | SHT30, SHT31, SHT35 (within accuracy grades) |
| HIH613x | HIH6130, HIH6131 |
| HDCx080 | HDC1080, HDC2080 |

## Pressure Sensor Equivalents

| Family | Compatible Parts |
|--------|------------------|
| BMx280 | BMP280, BME280 (pressure compatible) |
| MS56xx | MS5611, MS5607 |

## Package Handling

Package compatibility is considered:
- `TO-92`, `TO-226` - Through-hole, compatible
- `SOT-23`, `TO-236` - SMD, compatible
- `LCC`, `LGA`, `LFCSP`, `QFN`, `BCC` - MEMS packages, compatible within group

## Test Examples

```java
// Same sensor
calculator.calculateSimilarity("DS18B20", "DS18B20", registry);
// Returns 0.9

// Temperature variants
calculator.calculateSimilarity("LM35D", "LM35C", registry);
// Returns >= 0.7

// Cross-family (different families)
calculator.calculateSimilarity("DS18B20", "ADXL345", registry);
// Returns 0.3

// Same accelerometer, reel variant
calculator.calculateSimilarity("ADXL345BCCZ", "ADXL345BCCZ-RL", registry);
// Returns 0.9
```

---

## Metadata-Driven Implementation (January 2026)

**Status**: ✅ Converted (PR #120)

The `SensorSimilarityCalculator` now uses a **metadata-driven approach** with spec-based comparison.

### Specs Compared

| Spec | Importance | Tolerance Rule | Description |
|------|-----------|----------------|-------------|
| **sensorType** | CRITICAL | exactMatch | TEMPERATURE, ACCELEROMETER, GYROSCOPE, HUMIDITY, PRESSURE, COMBINED |
| **family** | HIGH | exactMatch | LM35, DS18, ADXL, MMA, SHT, BME, BMP, etc. |
| **interface** | MEDIUM | exactMatch | I2C, SPI, 1-Wire, Analog |
| **package** | LOW | exactMatch | TO-92, SOIC, LGA, QFN, BCC, etc. |

### Implementation Pattern

```java
// Short-circuit check for CRITICAL incompatibility
if (!sensorType1.isEmpty() && !sensorType2.isEmpty() && !sensorType1.equals(sensorType2)) {
    return LOW_SIMILARITY;
}

// Extract sensor type from MPN
private String extractSensorType(String mpn) {
    SensorFamily family = determineSensorFamily(mpn);
    return family.name(); // TEMPERATURE, ACCELEROMETER, etc.
}

// Extract sensor family with specific model number
private String extractSensorFamily(String mpn) {
    if (mpn.matches("^ADXL[0-9]+.*")) return "ADXL345", "ADXL362", etc.;
    if (mpn.matches("^DS18.*")) return "DS18B20", "DS18";
    // ... returns specific sensor model
}

// Equivalent sensor boost
if (areEquivalentSensorsByFamily(mpn1, mpn2, family1, family2)) {
    similarity = Math.max(similarity, HIGH_SIMILARITY);
}
```

### Behavior Changes

| Comparison | Legacy Result | Metadata Result | Notes |
|-----------|--------------|-----------------|-------|
| DS18B20 vs DS18B20 | 0.9 | 1.0 | Identical sensor |
| DS18B20+ vs DS18B20Z | 0.9 | 1.0 | Equivalent variants boost |
| ADXL345 vs ADXL345 | 0.9 | 1.0 | Identical |
| ADXL345 vs ADXL346 | 0.3 | 0.703 | Same type + interface = MEDIUM |
| ADXL345BCCZ vs ADXL345BCCZ-RL | 0.9 | 0.976 | Same sensor, packaging variant |
| LM35 vs ADXL345 | 0.3 | 0.3 | Short-circuit on sensor type |

**Why more accurate**: Metadata approach recognizes that ADXL345 vs ADXL346 share sensor type (ACCELEROMETER) and interface (SPI/I2C), giving them MEDIUM similarity instead of LOW. This is more accurate than treating them as completely different sensors.

### Equivalent Sensor Groups

The calculator maintains equivalent sensor families:
- **DS18B20 variants**: DS18B20, DS18B20+, DS18B20Z all equivalent
- **LM35 grades**: LM35D, LM35C, LM35A all equivalent
- **TMP36 variants**: TMP36, TMP36GT9Z all equivalent
- **MAX31820**: Compatible with DS18B20
- **SHT3x series**: SHT30/31/35 within accuracy grades
- **BMP/BME pressure**: BMP280 ≈ BME280 for pressure

---

## Learnings & Quirks

### Temperature Sensors
- DS18B20: Digital, 1-Wire interface, ±0.5°C accuracy
- LM35: Analog output, 10mV/°C
- TMP36: Analog output, 10mV/°C, -40 to +125°C
- MAX31820: Drop-in replacement for DS18B20

### Accelerometer Grades
- ADXL345B vs ADXL345: B is different interface option
- Different grades (BCCZ, BCCZ-RL) are same sensor

### Humidity Sensor Accuracy
- SHT30: ±3% RH typical
- SHT31: ±2% RH typical
- SHT35: ±1.5% RH typical
- Higher number = better accuracy

### Sensors Not Fully Supported
- HDC sensors may not be recognized by `isSensor()` method
- Some newer sensors may need pattern updates

<!-- Add new learnings above this line -->