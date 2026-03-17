---
name: ti
description: Texas Instruments MPN encoding patterns, suffix decoding, and handler guidance. Use when working with TI components or TIHandler.
---

# Texas Instruments (TI) Manufacturer Skill

## MPN Structure

TI MPNs follow this general structure:

```
[PREFIX][SERIES][VARIANT][PACKAGE][TEMP][QUALIFIER]
   │       │        │        │      │       │
   │       │        │        │      │       └── Optional: R=Tape/Reel, E=Lead-free
   │       │        │        │      └── Temperature: I=Industrial, Q=Automotive, M=Military
   │       │        │        └── Package code (see table below)
   │       │        └── Variant letter (A, B, C for improved specs)
   │       └── Series number (e.g., 358, 7805, 317)
   └── Family prefix (LM, TL, TPS, SN, etc.)
```

### Example Decoding

```
LM358DR
│  │  ││
│  │  │└── R = Tape and Reel
│  │  └── D = SOIC package
│  └── 358 = Dual Op-Amp series
└── LM = Linear/Mixed-signal prefix

TPS63020DSJR
│  │    │  │
│  │    │  └── R = Tape and Reel
│  │    └── DSJ = SON package (3x3mm)
│  └── 63020 = Buck-Boost converter
└── TPS = Power Supply prefix
```

---

## Package Codes

### Through-Hole Packages

| Code | Package | Pin Count | Notes |
|------|---------|-----------|-------|
| N | DIP | 8-40 | Plastic DIP |
| P | DIP | 8-40 | Plastic DIP (alternate) |
| T | TO-220 | 3-5 | Power package |
| T3 | TO-220 | 3 | 3-pin TO-220 |
| K | TO-3 | 2-3 | Metal can power |
| H | TO-39 | 8 | Metal can |

### Surface Mount - Small Signal

| Code | Package | Pitch | Notes |
|------|---------|-------|-------|
| D | SOIC | 1.27mm | 8-16 pins |
| DW | SOIC-Wide | 1.27mm | Wide body |
| PW | TSSOP | 0.65mm | Thin profile |
| DGK | MSOP/VSSOP | 0.5mm | Mini SOIC |
| DBV | SOT-23 | 0.95mm | 5-6 pins |
| DRL | SOT-553 | 0.5mm | Very small |
| DRV | SON | 0.5mm | QFN variant |

### Surface Mount - Power

| Code | Package | Notes |
|------|---------|-------|
| KC | TO-252 (DPAK) | Medium power SMD |
| KV | TO-252 | Variant |
| MP | SOT-223 | 4-pin power |
| DT | SOT-223 | Alternate code |

---

## Family Prefixes

### Analog/Linear (LM, TL, NE)

| Prefix | Category | Examples |
|--------|----------|----------|
| LM | General analog | LM358 (op-amp), LM7805 (regulator), LM317 (adj reg) |
| TL | TI Linear | TL072 (JFET op-amp), TL431 (reference) |
| NE | Signetics legacy | NE5532 (low-noise op-amp) |
| UA | Original TI | UA7805 (equivalent to LM7805) |

### Power Management (TPS, TLV, LP)

| Prefix | Category | Examples |
|--------|----------|----------|
| TPS | Power supply | TPS63020 (buck-boost), TPS7350 (LDO) |
| TLV | Low voltage | TLV431 (low-V reference) |
| LP | Low power | LP2950 (LDO) |

### Logic & Interface (SN, CD)

| Prefix | Category | Examples |
|--------|----------|----------|
| SN | TI logic | SN74HC595 (shift register) |
| CD | CMOS logic | CD4017 (decade counter) |

### Microcontrollers (MSP, CC)

| Prefix | Category | Examples |
|--------|----------|----------|
| MSP430 | Ultra-low-power MCU | MSP430G2553 |
| CC | Wireless MCU | CC2541 (BLE), CC3200 (WiFi) |

---

## Temperature Grades

| Suffix | Range | Application |
|--------|-------|-------------|
| (none) | 0°C to +70°C | Commercial |
| I | -40°C to +85°C | Industrial |
| A | -40°C to +85°C | Industrial (alternate) |
| Q | -40°C to +125°C | Automotive |
| M | -55°C to +125°C | Military |

---

## Critical Pattern Conflicts

### LM35 vs LM358

**LM35** = Temperature sensor (letter A-D after "35")
**LM358** = Dual op-amp (digit 8 after "35")

```
LM35DZ   → Temperature sensor (D = grade, Z = TO-92 package)
LM358N   → Dual op-amp (8 = part of series, N = DIP package)
```

**Handler Pattern:**
```java
// LM35 sensors: letter A-D immediately after "35"
"^LM35[A-D][A-Z0-9-]*$"

// LM358 op-amps: digit after "35"
"^LM358[A-Z0-9]*(?:N|D|P|DG|PW)?$"
```

### 78xx vs 79xx Regulators

**78xx** = Positive voltage regulator
**79xx** = Negative voltage regulator

```
LM7805CT  → +5V regulator, TO-220
LM7905CT  → -5V regulator, TO-220
```

---

## Common Series Reference

### Op-Amps

| Series | Type | Equivalent |
|--------|------|------------|
| LM358 | Dual, general purpose | MC1458, RC4558 |
| LM324 | Quad, general purpose | MC3403 |
| TL072 | Dual JFET, low noise | TL082 |
| TL074 | Quad JFET | TL084 |
| NE5532 | Dual, low noise | SA5532 |
| LM311 | Comparator | LM211 |

### Voltage Regulators

| Series | Type | Voltage | Equivalent |
|--------|------|---------|------------|
| LM7805 | Fixed positive | +5V | MC7805, UA7805 |
| LM7812 | Fixed positive | +12V | MC7812 |
| LM7905 | Fixed negative | -5V | MC7905 |
| LM317 | Adjustable positive | 1.25-37V | LM350, LM338 |
| LM337 | Adjustable negative | -1.25 to -37V | - |

### Temperature Sensors

| Series | Type | Output |
|--------|------|--------|
| LM35 | Precision analog | 10mV/°C |
| TMP36 | Precision analog | 10mV/°C + 500mV offset |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// TI package codes come AFTER the base part number
// Example: LM358D → base="LM358", package="D"

// For voltage regulators, package often follows voltage
// Example: LM7805CT → base="LM7805", package="CT" (TO-220)

// CRITICAL: Check longer suffixes BEFORE shorter ones!
// "LM7805DT".endsWith("T") is TRUE, but DT=SOT-223, not TO-220
if (suffix.endsWith("CT")) return "TO-220";   // 2-char first
if (suffix.endsWith("DT")) return "SOT-223";  // 2-char first
if (suffix.endsWith("MP")) return "SOT-223";  // 2-char first
if (suffix.endsWith("KC")) return "TO-252";   // 2-char first
if (suffix.endsWith("T")) return "TO-220";    // 1-char LAST

// Same for SOIC vs MSOP vs TSSOP
if (suffix.startsWith("DGK")) return "MSOP";  // 3-char first
if (suffix.startsWith("PW")) return "TSSOP";  // 2-char
if (suffix.startsWith("D")) return "SOIC";    // 1-char LAST
```

**Bug Example (Fixed in PR #78)**:
```java
// WRONG - "DT" ends with "T" so this returns TO-220 incorrectly
if (upperMpn.endsWith("T")) return "TO-220";   // Matches first!
if (upperMpn.endsWith("DT")) return "SOT-223"; // Never reached

// CORRECT - Check longer suffixes first
if (upperMpn.endsWith("DT")) return "SOT-223"; // Matches correctly
if (upperMpn.endsWith("T")) return "TO-220";   // Only bare "T"
```

### Series Extraction

```java
// Extract base series before package/temperature suffix
// LM358APWRQ1 → LM358 (ignore A=variant, PW=package, R=tape, Q1=automotive)

// Voltage regulators include voltage in series
// LM7805 → full series is "LM7805" not just "LM78"
```

---

## Related Files

- Handler: `manufacturers/TIHandler.java`
- Component types: `OPAMP_TI`, `VOLTAGE_REGULATOR_LINEAR_TI`, `VOLTAGE_REGULATOR_SWITCHING_TI`, `TEMPERATURE_SENSOR_TI`, `LED_TI`
- Package registry: `PackageCodeRegistry.java` (standard codes)

---

## Learnings & Edge Cases

- **LM317 vs LM350 vs LM338**: Same adjustable regulator family, different current ratings (1.5A/3A/5A)
- **UA prefix**: Original TI designation, functionally equivalent to LM (UA7805 = LM7805)
- **Automotive suffix Q1/Q**: Indicates AEC-Q100 qualified for automotive use
- **Green/lead-free**: Suffix "G" or "E" sometimes indicates RoHS compliance
- **Suffix ordering bug (PR #78)**: When using `endsWith()` for package detection, ALWAYS check longer suffixes first. "DT" ends with "T", so checking "T" first causes wrong results.
- **TIHandlerTest location**: Tests must be in `handlers` package, NOT `manufacturers` package (causes classpath shadowing)
- **Handler initialization**: Use `MPNUtils.getManufacturerHandler("LM358")` in tests, not `new TIHandler()` (causes circular init)

<!-- Add new learnings above this line -->
