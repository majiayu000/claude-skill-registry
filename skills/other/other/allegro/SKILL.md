---
name: allegro
description: Allegro MicroSystems MPN encoding patterns, suffix decoding, and handler guidance. Use when working with current sensors, motor drivers, or Hall effect sensors.
---

# Allegro MicroSystems Manufacturer Skill

## MPN Structure

Allegro MPNs follow this general structure:

```
[FAMILY][SERIES][PACKAGE][VARIANT]-[RATING]-[SUFFIX]
   │       │       │        │         │        │
   │       │       │        │         │        └── T = Tape/Reel, Pb-free
   │       │       │        │         └── Current rating (05B = 5A bidirectional)
   │       │       │        └── TR = Tape and Reel
   │       │       └── Package code (ELC, LLC, SE, etc.)
   │       └── Series number (712, 723, 4988, etc.)
   └── Family prefix (ACS, A, AH, AAS)
```

### Example Decoding

```
ACS712ELCTR-05B-T
│  │  │   │  │  │
│  │  │   │  │  └── T = Pb-free/Tape and Reel qualifier
│  │  │   │  └── 05B = 5A bidirectional current sensing
│  │  │   └── TR = Tape and Reel packaging
│  │  └── ELC = SOIC-8 package
│  └── 712 = Series number
└── ACS = Current Sensor family

A4988SETTR-T
│    │   │
│    │   └── T = Tape and Reel
│    └── SETTR = QFN package, Tape and Reel
└── A4988 = Stepper motor driver

A1324LLHLT-T
│    │    │
│    │    └── T = Tape and Reel
│    └── LLHLT = SOT-23 package (LLH), Tape and Reel
└── A1324 = Linear Hall effect sensor
```

---

## Package Codes

### Current Sensors (ACS7xx, ACS37xxx)

| Code | Package | Notes |
|------|---------|-------|
| ELC | SOIC-8 | Standard 8-pin SOIC |
| LLC | SOIC-8 | Leadless version |
| KLC | SOIC-8-EP | Enhanced thermal pad |
| LH | SOT-23 | Small outline package |

### Motor Drivers (A3xxx, A4xxx, A5xxx)

| Code | Package | Notes |
|------|---------|-------|
| SE/SET | QFN | Quad Flat No-leads |
| SL/SLB | SOIC-24 | 24-pin SOIC |
| ET | QFN | QFN variant |
| KLJ | TO-92 | Through-hole |

### Hall Sensors (A1xxx, AH series)

| Code | Package | Notes |
|------|---------|-------|
| LUA | SIP-3 | Single in-line (3-pin) |
| EUA | SIP-4 | Single in-line (4-pin) |
| LH/LLH | SOT-23 | Small outline transistor |
| KUA | TO-92 | Through-hole |

---

## Family Prefixes

### Current Sensors

| Prefix | Category | Examples |
|--------|----------|----------|
| ACS7xx | Hall-effect current sensors | ACS712, ACS723, ACS758 |
| ACS37xxx | Coreless current sensors | ACS37612, ACS37030 |

### Motor Drivers

| Prefix | Category | Examples |
|--------|----------|----------|
| A39xx | Stepper motor drivers | A3967 (Easy Driver) |
| A49xx | Stepper motor drivers | A4988 (common in 3D printers) |
| A59xx | BLDC motor drivers | A5931, A5932 |

### Hall Effect Sensors

| Prefix | Category | Examples |
|--------|----------|----------|
| A13xx | Linear Hall sensors | A1301, A1324, A1325, A1326 |
| AH | Hall switches | AH3362, AH3366 |

### LED Drivers

| Prefix | Category | Examples |
|--------|----------|----------|
| A6xxx | General LED drivers | A6261, A6262 |
| A8xxxx | High power LED drivers | A80601, A80604 |

---

## Current Sensor Rating Codes

| Suffix | Meaning |
|--------|---------|
| 05B | ±5A bidirectional |
| 10B | ±10A bidirectional |
| 20A | ±20A bidirectional |
| 30A | ±30A bidirectional |
| 40AB | ±40A bidirectional |
| 05AU | 0-5A unidirectional |
| 20AU | 0-20A unidirectional |

---

## Common Series Reference

### Current Sensors (most popular)

| Series | Type | Use Case |
|--------|------|----------|
| ACS712 | Hall-effect, isolated | Arduino current sensing, power monitoring |
| ACS723 | Hall-effect, low noise | Precision current measurement |
| ACS758 | Hall-effect, high current | Industrial, automotive |
| ACS37612 | Coreless, differential | Battery management, motor control |

### Motor Drivers (most popular)

| Series | Type | Use Case |
|--------|------|----------|
| A4988 | Stepper, microstepping | 3D printers, CNC machines |
| A3967 | Stepper, Easy Driver | Hobbyist robotics |
| A4950 | DC brushed motor | Simple motor control |
| A4953 | DC brushed, full bridge | H-bridge applications |

### Hall Sensors

| Series | Type | Use Case |
|--------|------|----------|
| A1324/5/6 | Linear, ratiometric | Position sensing, current sensing |
| A1301/2 | Linear, analog output | Proximity sensing |
| AH33xx | Hall switch, latching | RPM measurement, position detection |

---

## Handler Implementation Notes

### Package Code Extraction

```java
// Current sensors use letter codes after series number
// ACS712ELCTR -> ELC = SOIC-8
// ACS723LLCTR -> LLC = SOIC-8 (leadless)
// ACS723KLCTR -> KLC = SOIC-8-EP (enhanced thermal pad)

// Motor drivers use suffix codes
// A4988SETTR -> SET = QFN
// A3967SLBT -> SLB = SOIC-24

// Hall sensors use suffix codes
// A1324LUA -> LUA = SIP-3
// A1324LLH -> LLH = SOT-23
```

### Series Extraction

```java
// Current sensors: Extract full ACSxxx or ACS3xxxx
// ACS712ELCTR-05B-T -> ACS712
// ACS37612LLCATR-030B5-T -> ACS37612

// Motor drivers: Extract Axxxx (5 chars)
// A4988SETTR-T -> A4988
// A3967SLBT -> A3967

// Hall sensors: Extract A1xxx (5 chars) or AHxxxx (6 chars)
// A1324LUA-T -> A1324
// AH3362Q -> AH3362
```

---

## Related Files

- Handler: `manufacturers/AllegroHandler.java`
- Component types: `SENSOR_CURRENT`, `MOTOR_DRIVER`, `HALL_SENSOR`, `LED_DRIVER`, `SENSOR`, `IC`
- Test: `handlers/AllegroHandlerTest.java`

---

## Learnings & Edge Cases

- **ACS712 is extremely common** - Found in nearly every Arduino/hobbyist current sensing project
- **A4988 is the de facto standard** - Used in most 3D printers (Prusa, Creality, etc.)
- **Package code position varies** - Current sensors embed it in part number, motor drivers use suffixes
- **LLC vs ELC** - Both are SOIC-8; LLC is leadless variant with same footprint
- **KLC = Enhanced thermal** - SOIC-8-EP with exposed thermal pad for better heat dissipation
- **TR suffix** - Appears before final -T suffix, indicates tape and reel (e.g., ELCTR = ELC + TR)
- **-T suffix meaning varies** - Can mean tape/reel OR Pb-free; Allegro uses it for both
- **Current rating codes** - B = bidirectional, U = unidirectional, A often appears in newer sensors

<!-- Add new learnings above this line -->
