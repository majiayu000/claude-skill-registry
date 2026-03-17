---
name: nexteria
description: Nexperia (filename uses "Nexteria" typo) MPN encoding patterns for discrete semiconductors, logic ICs, and ESD protection. Use when working with Nexperia components or NexteriaHandler.
---

# Nexperia (Nexteria) Manufacturer Skill

**Important Note**: The handler filename uses "Nexteria" which is a typo. The actual manufacturer is "Nexperia" (formerly NXP Standard Products/Philips Semiconductors).

## Manufacturer Overview

Nexperia specializes in discrete components and logic ICs:
- **Transistors**: PMBT, PBSS, BC, BF, PN, 2N series (NPN/PNP)
- **MOSFETs**: PSMN (N-ch power), PSMP (P-ch power), PMV (small signal), 2N7002
- **Diodes**: PMEG (Schottky), BAV/BAS (signal), BAT (Schottky), BZX/PZU (Zener)
- **ESD Protection**: PESD, PRTR, PTVS, IP4 series
- **Logic ICs**: 74LVC, 74AHC, 74AUP, 74HC, 74HCT families

---

## MPN Structure

Nexperia MPNs generally follow these patterns:

### Discrete Components (Transistors, MOSFETs, Diodes)

```
[PREFIX][SERIES][SPECS][PACKAGE][,REEL]
   |       |       |       |       |
   |       |       |       |       └── Optional: ,215 or ,315 for tape & reel
   |       |       |       └── Package suffix (varies by series)
   |       |       └── Voltage/current ratings or grade
   |       └── Series identifier
   └── Family prefix (PSMN, PMBT, PMEG, etc.)
```

### Logic ICs

```
74[FAMILY][FUNCTION][PACKAGE]
   |         |          |
   |         |          └── Package code (GW, BQ, PW, D)
   |         └── Logic function number (00, 04, 595, etc.)
   └── Technology family (HC, HCT, LVC, AHC, AUP, etc.)
```

---

## Package Codes

### Tape & Reel Suffixes (Comma-Separated)

| Code | Package | Notes |
|------|---------|-------|
| ,215 | SOT23 | Standard 7" reel |
| ,235 | SOT23 | Alternate SOT23 |
| ,315 | SOD882 | Leadless package |
| ,115 | SOT223 | Power package |

### Letter Suffixes

| Code | Package | Notes |
|------|---------|-------|
| T | SOT23 | Default small signal |
| S | SOT363 | 6-pin SOT |
| U | SOT323 | SC-70 |
| W | SC70 | Very small signal |
| F | SOT89 | Medium power |
| L | TO-220 | Through-hole power |
| FI | TO-220F | Isolated TO-220 |
| D | SO14 | SOIC 14-pin |
| PW | TSSOP | Thin profile |
| BQ | DHVQFN | QFN variant |
| GD | XSON8 | Tiny logic |
| GS | XSON6 | Tiny logic |

### Power MOSFET Packages (PSMN/PSMP)

| Suffix | Package | Notes |
|--------|---------|-------|
| T | LFPAK56 | Standard power MOSFET |
| U | LFPAK88 | Larger power MOSFET |
| V | LFPAK33 | Smaller power MOSFET |
| B | SOT754 | Power-SO8 |
| PE | LFPAK56E | Enhanced thermal |
| L | TO-220 | Through-hole |
| F / FI | TO-220F | Isolated |

### Schottky Rectifier Packages (PMEG)

| Suffix | Package |
|--------|---------|
| AEH | SOD123 |
| AED | SOD323F |
| BEA | SOD128 |
| BEB | CFP3 |
| AET | SOD523 |

### ESD Protection Packages (PESD)

| Suffix | Package |
|--------|---------|
| BL | SOD882 |
| BA | SOD323 |
| UB | SOT23 |
| UD | SOT323 |

---

## Family Prefixes by Component Type

### MOSFETs

| Prefix | Type | Description |
|--------|------|-------------|
| PSMN | N-channel power | High current, low RDS(on) |
| PSMP | P-channel power | Complementary to PSMN |
| PMV | Small signal | Low voltage, small packages |
| BSS | Small signal | Legacy/standard series |
| BUK | Legacy power | Older power MOSFET series |
| PJD | JFET | Junction FET series |
| 2N7002 | N-channel | Popular small signal MOSFET |

### Transistors (BJT)

| Prefix | Type | Description |
|--------|------|-------------|
| PMBT | Small signal | SOT23 transistors (PMBT2222A, etc.) |
| PBSS | Small signal | High performance |
| PMP | Medium power | Higher current capability |
| PXN | High power | High current transistors |
| MMBT | SMD standard | Surface mount TO-92 equivalent |
| BC | Classic series | BC546, BC547, BC548, BC549, BC550 |
| BF | High frequency | RF and switching |
| 2N2222 | NPN | Classic NPN general purpose |
| 2N3904 | NPN | General purpose NPN |
| 2N3906 | PNP | General purpose PNP |
| PN2222 | NPN | TO-92 variant of 2N2222 |

### Diodes

| Prefix | Type | Description |
|--------|------|-------------|
| PMEG | Schottky rectifier | Low forward voltage |
| BAV | Signal/switching | BAV99, BAV70 (dual diodes) |
| BAS | Signal | General purpose signal |
| BAT | Schottky signal | BAT54, BAT46 |
| BZX | Zener | BZX84 (SOT23), BZX55/79 (DO-35) |
| PZU | Zener | Alternative Zener series |
| 1N4148 | Signal | Standard signal diode |
| 1N914 | Signal | Equivalent to 1N4148 |

### ESD Protection

| Prefix | Type | Description |
|--------|------|-------------|
| PESD | Single/dual line | General ESD protection |
| PRTR | Protection arrays | Multi-line protection |
| PTVS | TVS diodes | Transient voltage suppression |
| IP4 | Interface protection | USB, HDMI specific |

### Logic ICs (74-series)

| Family | Description | Voltage |
|--------|-------------|---------|
| 74HC | High-speed CMOS | 2-6V |
| 74HCT | HC with TTL inputs | 4.5-5.5V |
| 74LVC | Low-voltage CMOS | 1.65-3.6V |
| 74LVCH | LVC with bus hold | 1.65-3.6V |
| 74LVT | Low-voltage BiCMOS | 3.3V |
| 74AHC | Advanced high-speed | 2-5.5V |
| 74AHCT | AHC with TTL inputs | 4.5-5.5V |
| 74AUC | Advanced ultra-low voltage | 0.8-2.7V |
| 74AUP | Advanced ultra-low power | 0.8-3.6V |

### Interface ICs

| Prefix | Type | Description |
|--------|------|-------------|
| PCA | I2C devices | Bus controllers, switches |
| PCF | Interface/control | Legacy interface ICs |
| PTN | Level translators | Voltage translation |

---

## Example MPN Decoding

### Power MOSFET

```
PSMN013-30YLC
│    │   │ ││
│    │   │ │└── C = Tape cut
│    │   │ └── L = TO-220 package
│    │   └── Y = Some variant indicator
│    └── 30 = 30V rating
└── PSMN013 = N-channel MOSFET with 13mOhm RDS(on)
```

### Small Signal Transistor

```
PMBT2222A,215
│    │   │ └── ,215 = SOT23, 7" reel
│    │   └── A = Grade (improved specs)
│    └── 2222 = 2N2222 equivalent
└── PMBT = Plastic small signal transistor (SOT23)
```

### Logic IC

```
74LVC1G04GW,125
│  │   │ ││  └── ,125 = Packaging code (tape & reel)
│  │   │ │└── GW = SOT353 package
│  │   │ └── 04 = Inverter function
│  │   └── 1G = Single gate
│  └── LVC = Low-voltage CMOS family
└── 74 = Logic IC prefix
```

### Schottky Diode

```
PMEG6010AEH
│    │  ││ └── AEH = SOD123 package
│    │  │└── A = Grade
│    │  └── 10 = 1A forward current
│    └── 60 = 60V reverse voltage
└── PMEG = Schottky rectifier series
```

### Zener Diode

```
BZX84-C5V1,215
│   │  │  │ └── ,215 = SOT23, 7" reel
│   │  │  └── 5V1 = 5.1V Zener voltage
│   │  └── C = Grade
│   └── 84 = SOT23 package series
└── BZX = Zener diode
```

### ESD Protection

```
PESD5V0S1BL,315
│    │  │ ││ └── ,315 = SOD882, 7" reel
│    │  │ │└── BL = SOD882 package
│    │  │ └── S1 = Single line
│    │  └── 5V0 = 5.0V working voltage
│    └── PESD = ESD protection device
└── P = Nexperia prefix
```

---

## Supported Component Types

The NexteriaHandler supports these ComponentTypes:

### Base Types
- `MOSFET`
- `TRANSISTOR`
- `DIODE`
- `IC`

### Nexperia-Specific Types
- `MOSFET_NEXPERIA`
- `BIPOLAR_TRANSISTOR_NEXPERIA`
- `ESD_PROTECTION_NEXPERIA`
- `LOGIC_IC_NEXPERIA`

---

## Series Extraction Rules

The handler extracts series using these patterns:

| Pattern | Extracted Series |
|---------|------------------|
| PSMN* | "PSMN" |
| PSMP* | "PSMP" |
| PMV* | "PMV" |
| BSS* | "BSS" |
| 2N7002* | "2N7002" |
| PMBT* | "PMBT" |
| PBSS* | "PBSS" |
| BC5xx* | "BC5xx" |
| BC8xx* | "BC8xx" |
| BC* | "BC" |
| BF* | "BF" |
| MMBT* | "MMBT" |
| PMEG* | "PMEG" |
| BAVxx* | Specific (e.g., "BAV99") |
| BATxx* | Specific (e.g., "BAT54") |
| BZXxx* | Specific (e.g., "BZX84") |
| 74family* | Family (e.g., "74LVC", "74AHC") |
| PCA* | "PCA" |
| PCF* | "PCF" |
| PTN* | "PTN" |

---

## Package Code Extraction Logic

### Step 1: Check for Comma-Separated Suffix

```java
// Nexperia uses ,215, ,315, etc. for tape & reel packaging
if (mpn.contains(",")) {
    String suffix = mpn.substring(mpn.indexOf(',') + 1);
    // Lookup in NEXPERIA_PACKAGES map
}
```

### Step 2: Series-Specific Extraction

**Power MOSFETs (PSMN/PSMP):**
- Extract letter suffix after last digit
- T=LFPAK56, U=LFPAK88, V=LFPAK33, B=SOT754, L=TO-220

**Small Signal (PMV/BSS/2N7002):**
- Extract suffix after last digit
- Lookup in package map or return default SOT23

**Transistors (PMBT/PBSS):**
- Single letter suffix after grade letter = default SOT23
- Multi-letter suffix = lookup in map

**Zener Diodes (BZX):**
- BZX84 = SOT23
- BZX384 = SOD323
- BZX55/79 = DO-35
- BZX85 = DO-41

**Signal Diodes (BAV/BAS/BAT):**
- Most default to SOT23

**Schottky Rectifiers (PMEG):**
- Suffix-based: AEH=SOD123, AED=SOD323F, BEA=SOD128

**ESD Protection (PESD):**
- BL=SOD882, BA=SOD323, UB=SOT23, UD=SOT323

**Logic ICs (74xxx):**
- GW=SOT353, GM=XSON6, BQ=DHVQFN, PW=TSSOP, D=SO14
- Also handles underscore format: 74HC00_D

---

## Official Replacement Rules

The handler supports `isOfficialReplacement()` for:

### Logic ICs
- Same function number across families are compatible
- HCT is backward compatible with HC
- Same family, different packages are compatible

### Transistors
- PMBT2222A, 2N2222, PN2222 are equivalent (base "2222")
- PMBT3904 and 2N3904 are equivalent
- PMBT3906 and 2N3906 are equivalent

### MOSFETs
- Same base part, different package = compatible
- e.g., PSMN013-30YL and PSMN013-30YT (same specs, different packages)

---

## Handler Implementation Notes

### MPN Normalization

```java
// Remove tape & reel suffix before pattern matching
private String normalizeForMatching(String mpn) {
    if (mpn.contains(",")) {
        return mpn.substring(0, mpn.indexOf(','));
    }
    return mpn;
}
```

### Pattern Matching

The handler overrides `matches()` with explicit checks to avoid cross-handler false matches. It does NOT fall back to the PatternRegistry default implementation.

### Supported Types Use Set.of()

```java
return Set.of(
    ComponentType.MOSFET,
    ComponentType.TRANSISTOR,
    ComponentType.DIODE,
    ComponentType.IC,
    ComponentType.MOSFET_NEXPERIA,
    ComponentType.BIPOLAR_TRANSISTOR_NEXPERIA,
    ComponentType.ESD_PROTECTION_NEXPERIA,
    ComponentType.LOGIC_IC_NEXPERIA
);
```

---

## Related Files

- Handler: `manufacturers/NexteriaHandler.java` (note: typo in filename)
- Component types: `MOSFET_NEXPERIA`, `BIPOLAR_TRANSISTOR_NEXPERIA`, `ESD_PROTECTION_NEXPERIA`, `LOGIC_IC_NEXPERIA`

---

## Learnings & Quirks

### Handler Filename Typo
- The file is named `NexteriaHandler.java` but the manufacturer is **Nexperia**
- This is documented in the class-level Javadoc comment
- All ComponentTypes use the correct "NEXPERIA" suffix

### Comma-Separated Package Codes
- Unlike most manufacturers, Nexperia uses comma-separated suffixes (,215, ,315)
- These MUST be stripped before pattern matching
- The comma suffix encodes both package AND tape/reel configuration

### Logic IC Families
- When extracting logic family, check longer prefixes first: AHCT before AHC, LVCH before LVC
- The `extractLogicFamily()` method iterates through families in correct order

### Package Extraction Complexity
- Different series have completely different package encoding schemes
- PMEG uses full suffix codes (AEH, AED), while PSMN uses single letters (T, U, V)
- BZX series encodes package in the series name itself (BZX84 = SOT23)

### Transistor Equivalents
- PMBT2222A = 2N2222A = PN2222A (same transistor, different packages)
- The handler correctly identifies these as equivalent in `isOfficialReplacement()`

### No ManufacturerComponentTypes
- `getManufacturerTypes()` returns `Collections.emptySet()`
- All types are standard ComponentType enums

### Pattern Registration
- Each pattern is registered for BOTH base type and Nexperia-specific type
- Example: `MOSFET` and `MOSFET_NEXPERIA` both get the PSMN pattern

<!-- Add new learnings above this line -->
