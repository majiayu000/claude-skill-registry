---
name: maxim
description: Maxim Integrated (now Analog Devices) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Maxim/Dallas components or MaximHandler.
---

# Maxim Integrated Manufacturer Skill

## MPN Structure

Maxim MPNs follow this general structure:

```
[PREFIX][SERIES][GRADE][TEMP][PACKAGE][PINS][ROHS]
   |       |       |      |      |      |     |
   |       |       |      |      |      |     +-- +/- for RoHS status
   |       |       |      |      |      +-- Pin count designator
   |       |       |      |      +-- Package type letter
   |       |       |      +-- Temperature range code
   |       |       +-- Optional grade (A, B, C for accuracy/specs)
   |       +-- Series number (e.g., 232, 485, 6675)
   +-- Family prefix (MAX, DS, ICL, DG)
```

### Example Decoding

```
MAX232CPE+
|  |  |||+-- + = RoHS compliant
|  |  ||+-- E = 16 pins
|  |  |+-- P = Plastic DIP package
|  |  +-- C = Commercial temp (0 to +70C)
|  +-- 232 = RS-232 driver/receiver
+-- MAX = Maxim prefix

DS18B20+
|  |   |+-- + = RoHS compliant
|  |   +-- (no package code = TO-92 default)
|  +-- 18B20 = Digital temperature sensor series
+-- DS = Dallas Semiconductor prefix

MAX6675ISA+
|  |   |||+-- + = RoHS compliant
|  |   ||+-- A = 8 pins
|  |   |+-- S = SOIC package
|  |   +-- I = Industrial temp (-40 to +85C)
|  +-- 6675 = K-type thermocouple-to-digital converter
+-- MAX = Maxim prefix
```

---

## Temperature Range Codes

| Code | Range | Application |
|------|-------|-------------|
| C | 0C to +70C | Commercial |
| I | -20C to +85C | Industrial (older) |
| E | -40C to +85C | Extended Industrial |
| A | -40C to +85C | Aerospace |
| M | -55C to +125C | Military |

Note: Temperature code is the FIRST letter of the suffix in Maxim's system.

---

## Package Type Codes (Second Letter)

### Through-Hole Packages

| Code | Package | Notes |
|------|---------|-------|
| P | PDIP | Plastic DIP |
| N | PDIP | Plastic DIP (alternate) |
| J | CERDIP | Ceramic DIP |

### Surface Mount - Standard

| Code | Package | Notes |
|------|---------|-------|
| S | SOIC (narrow) | 150mil body |
| A | SOIC (wide) | 208mil or 300mil body |
| W | SOIC (wide) | 300mil body |
| E | QSOP | Quarter-size SOP |
| U | TSSOP/TQFN | Thin packages |

### Surface Mount - Small Form Factor

| Code | Package | Notes |
|------|---------|-------|
| T | SOT-23 | Small outline transistor |
| X | SC70 | Ultra-small |
| K | micro-MAX | Micro footprint |

### Surface Mount - Power/Thermal

| Code | Package | Notes |
|------|---------|-------|
| F | TDFN | Thin dual flat no-lead |
| L | QFN | Quad flat no-lead |
| B | WLP | Wafer-level package |
| G | BGA | Ball grid array |

---

## Pin Count Codes (Third Letter)

| Code | Pin Count |
|------|-----------|
| A | 8 |
| B | 10 |
| C | 12 |
| D | 14 |
| E | 16 |
| G | 24 |
| H | 28 |
| I | 28 (alternate) |
| P | 20 |

---

## RoHS/Lead-Free Status

| Suffix | Meaning |
|--------|---------|
| + | Lead-free, RoHS compliant |
| - | Not RoHS qualified (leaded) |
| # | RoHS compliant with exemption (e.g., high-lead solder) |
| (none) | Pre-RoHS part number, leaded |

---

## Common Prefixes and Product Categories

### MAX Prefix (Maxim Original)

| Series | Category | Examples |
|--------|----------|----------|
| MAX232 | RS-232 interface | MAX232, MAX232A, MAX3232 |
| MAX485 | RS-485 interface | MAX485, MAX485E, MAX487 |
| MAX6xxx | Temperature sensors | MAX6675 (thermocouple), MAX6633 |
| MAX11xxx | ADCs | MAX11100, MAX11200 |
| MAX12xxx | DACs | MAX12555, MAX12900 |
| MAX17xxx | Power management | MAX17043 (fuel gauge), MAX17135 |
| MAX19xxx | Amplifiers | MAX19711, MAX19792 |
| MAX4xxx | Analog switches | MAX4051, MAX4066, MAX4617 |

### DS Prefix (Dallas Semiconductor)

| Series | Category | Examples |
|--------|----------|----------|
| DS18xxx | Temperature sensors | DS18B20, DS18S20 |
| DS12xxx | Real-time clocks | DS1232, DS12885, DS12C887 |
| DS13xxx | Real-time clocks | DS1302, DS1307, DS3231 |
| DS28xxx | EEPROM/Authentication | DS28E05, DS2890 |

### ICL Prefix (Intersil Legacy)

| Series | Category | Examples |
|--------|----------|----------|
| ICL7xxx | ADC/DAC | ICL7106, ICL7135 |

### DG Prefix (Data Gate)

| Series | Category | Examples |
|--------|----------|----------|
| DG4xxx | Analog switches | DG408, DG411, DG441 |

---

## DS18B20 Special Suffixes

The DS18B20 family uses simplified package codes:

| Suffix | Package | Notes |
|--------|---------|-------|
| (none) or + | TO-92 | Standard through-hole |
| Z | TO-92 | Same as above |
| U | MSOP-8 | Surface mount |
| PAR | TO-92 | Parasitic power mode |

---

## Common Series Reference

### Interface ICs

| Series | Type | Equivalent/Related |
|--------|------|-------------------|
| MAX232 | RS-232 driver | MAX232A (faster), MAX3232 (3V) |
| MAX485 | RS-485 transceiver | MAX485E (ESD protected), MAX487 |
| MAX3232 | 3V RS-232 | - |
| MAX3485 | 3V RS-485 | - |

### Temperature Sensors

| Series | Type | Output |
|--------|------|--------|
| DS18B20 | 1-Wire digital | 9-12 bit resolution |
| DS18S20 | 1-Wire digital | 9-bit resolution |
| MAX6675 | K-thermocouple | SPI, 12-bit |
| MAX6633 | Local/remote sensor | I2C |

### Real-Time Clocks

| Series | Type | Interface |
|--------|------|-----------|
| DS1302 | RTC with RAM | 3-wire serial |
| DS1307 | RTC with RAM | I2C |
| DS3231 | High-precision RTC | I2C, TCXO |
| DS12887 | RTC with battery | Parallel |

### Power Management

| Series | Type | Application |
|--------|------|-------------|
| MAX17043 | Fuel gauge | Li-Ion battery |
| MAX17135 | PMIC | E-paper displays |
| MAX17xxx | Battery management | Various |

---

## Handler Implementation Notes

### Current Issues in MaximHandler

1. **HashSet Usage**: Uses `new HashSet<>()` instead of immutable `Set.of()`:
   ```java
   // CURRENT (problematic)
   Set<ComponentType> types = new HashSet<>();
   types.add(...);

   // RECOMMENDED
   return Set.of(
       ComponentType.INTERFACE_IC_MAXIM,
       ComponentType.VOLTAGE_REGULATOR_MAXIM,
       ...
   );
   ```

2. **Missing Pattern Coverage**: Many product families lack patterns:
   - MAX232/MAX485 interface ICs (only generic IC patterns)
   - MAX6675 thermocouple converters
   - MAX17xxx power management
   - MAX4xxx analog switches

3. **Incomplete Package Extraction**: Only handles DS18B20 specifically:
   ```java
   // Current implementation only handles DS18B20
   if (mpn.startsWith("DS18")) {
       if (mpn.endsWith("Z")) return "TO-92";
       // etc.
   }
   ```

4. **Limited Series Extraction**: Only extracts DS18B20 and MAX6xxx series.

### Recommended Pattern Additions

```java
// Interface ICs
registry.addPattern(ComponentType.INTERFACE_IC_MAXIM, "^MAX[234]8[0-9][A-Z0-9]*$");

// Thermocouple converters
registry.addPattern(ComponentType.TEMPERATURE_SENSOR_MAXIM, "^MAX66[0-9]{2}[A-Z0-9-]*$");

// RTCs
registry.addPattern(ComponentType.RTC_MAXIM, "^DS1[23][0-9]{2}[A-Z0-9]*$");
registry.addPattern(ComponentType.RTC_MAXIM, "^DS3[0-9]{3}[A-Z0-9]*$");

// Power management
registry.addPattern(ComponentType.BATTERY_MANAGEMENT_MAXIM, "^MAX17[0-9]{3}[A-Z0-9-]*$");

// Analog switches
registry.addPattern(ComponentType.IC, "^MAX4[0-9]{3}[A-Z0-9-]*$");
registry.addPattern(ComponentType.IC, "^DG4[0-9]{2}[A-Z0-9-]*$");
```

### Package Code Extraction

```java
// Maxim package codes follow TEMP+PACKAGE+PINS format
// Example: MAX232CPE+ -> C=temp, P=PDIP, E=16-pin

// Extract package from 3-letter suffix
String suffix = extractSuffix(mpn);  // e.g., "CPE"
if (suffix.length() >= 2) {
    char packageCode = suffix.charAt(1);  // Second char is package
    switch (packageCode) {
        case 'P': case 'N': return "PDIP";
        case 'S': return "SOIC (narrow)";
        case 'A': case 'W': return "SOIC (wide)";
        case 'E': return "QSOP";
        case 'U': return "TSSOP";
        case 'T': return "SOT-23";
        // etc.
    }
}
```

---

## Related Files

- Handler: `manufacturers/MaximHandler.java`
- Component types: `INTERFACE_IC_MAXIM`, `VOLTAGE_REGULATOR_MAXIM`, `RTC_MAXIM`, `TEMPERATURE_SENSOR_MAXIM`, `BATTERY_MANAGEMENT_MAXIM`, `MEMORY_MAXIM`
- Manufacturer entry: `ComponentManufacturer.MAXIM` with regex `(?:MAX|DS|ICL|DG|UP|LT|LTC|LTM)`

---

## Learnings & Edge Cases

- **Dallas Semiconductor**: Acquired by Maxim in 2001; DS-prefix parts are Maxim products
- **Analog Devices acquisition**: Maxim was acquired by ADI in 2021; parts still use Maxim naming
- **MAX232 vs MAX232A**: The "A" suffix indicates improved specs (faster slew rate, smaller caps)
- **ESD-protected variants**: MAX485E has enhanced ESD protection vs standard MAX485
- **Temperature code position**: In Maxim's 3/4-letter suffix, temperature is FIRST letter
- **DS18B20 authenticity**: Counterfeit DS18B20 sensors are common; genuine parts have laser-etched markings
- **LT/LTC/LTM prefixes**: These are Linear Technology products (also owned by ADI), but registered in Maxim handler

<!-- Add new learnings above this line -->
