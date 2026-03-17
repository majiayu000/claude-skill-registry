---
name: qualcomm
description: Qualcomm MPN encoding patterns, suffix decoding, and handler guidance. Use when working with Qualcomm mobile SoCs, RF front-end, WiFi/Bluetooth, modems, or power management ICs.
---

# Qualcomm Manufacturer Skill

## Company Overview

Qualcomm is a leading fabless semiconductor company specializing in:

- **Mobile SoCs**: Snapdragon mobile platforms (SM, SD, QSD, MSM series)
- **IoT/Embedded**: QCS/QCM IoT platforms, APQ application processors, IPQ network processors
- **RF Front-End**: RF modules (QM), power modules (QPM), antenna tuners (QAT), envelope trackers (QET)
- **Wireless Connectivity**: WiFi/Bluetooth (QCA, WCN), cellular modems (MDM), small cell (FSM)
- **Power Management**: PMICs (PM, PMI), battery charging (SMB)
- **Audio**: Audio codecs (WCD), smart amplifiers (WSA)

---

## MPN Structure

Qualcomm MPNs follow this general structure:

```
[PREFIX][SERIES][-PACKAGE]
   │       │        │
   │       │        └── Optional: Package suffix (BGA, CSP, QFN, etc.)
   │       └── Numeric series (3-4 digits)
   └── Product family prefix (SM, QCA, PM, etc.)
```

### Example Decoding

```
SM8550-AB
│  │   │
│  │   └── AB = Package/variant designation
│  └── 8550 = Snapdragon 8 Gen 2 series
└── SM = Snapdragon Mobile platform

QCA6390-FCBGA
│   │    │
│   │    └── FCBGA = Flip-Chip BGA package
│   └── 6390 = Wi-Fi 6E / Bluetooth 5.2 combo chip
└── QCA = Qualcomm Connectivity/Atheros (Wi-Fi/BT)

PM8550
│  │
│  └── 8550 = Power management IC for SM8550 platform
└── PM = Power Management IC
```

---

## Product Family Prefixes

### Mobile Platforms (Snapdragon)

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| SM | Snapdragon Mobile | SM8550, SM8450, SM8350 | Current flagship naming |
| SD | Snapdragon | SD888, SD865, SD855 | Legacy flagship naming |
| QSD | Snapdragon (original) | QSD8250, QSD8650 | First-gen Snapdragon |
| MSM | Mobile Station Modem | MSM8996, MSM8953 | Integrated modem SoCs |

### IoT/Embedded Platforms

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| QCS | IoT Platform | QCS400, QCS603, QCS610 | Smart speaker, camera, etc. |
| QCM | IoT Module | QCM2150, QCM6490 | Complete system modules |
| APQ | Application Processor | APQ8064, APQ8084 | No integrated modem |
| IPQ | Network Processor | IPQ8074, IPQ6018 | Routers, networking |

### RF Front-End

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| QM | RF Module | QM42195, QM78207 | Integrated RF front-end |
| QPM | Power Module | QPM2630, QPM5677 | PA power modules |
| QAT | Antenna Tuner | QAT3516, QAT3555 | Impedance tuning |
| QET | Envelope Tracker | QET5100, QET6100 | Power efficiency |

### Wireless Connectivity

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| QCA | Wi-Fi/Bluetooth | QCA6390, QCA9377, QCA6174 | Atheros heritage |
| WCN | Wireless Connectivity | WCN3990, WCN6855 | Combo chips |
| MDM | Modem | MDM9206, MDM9650 | Standalone modems |
| FSM | Small Cell | FSM9955, FSM9900 | Base station |

### Power Management

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| PM | PMIC | PM8550, PM8350, PM8150 | Main PMICs |
| PMI | Power Management IC | PMI8998, PMI632 | Alternate PMIC series |
| SMB | Battery Charger | SMB1360, SMB1350 | Charging ICs |

### Audio

| Prefix | Category | Examples | Notes |
|--------|----------|----------|-------|
| WCD | Audio Codec | WCD9380, WCD9340 | Audio CODEC ICs |
| WSA | Smart Amplifier | WSA8810, WSA8815 | Speaker amplifiers |

---

## Package Codes

Package codes appear after a hyphen in the MPN.

| Suffix | Package | Full Name |
|--------|---------|-----------|
| BGA | BGA | Ball Grid Array |
| CSP | CSP | Chip Scale Package |
| POP / PoP | Package-on-Package | Stacked package |
| QFN | QFN | Quad Flat No-leads |
| PQFN | Power QFN | Power-rated QFN |
| LFCSP | Lead Frame CSP | Lead Frame Chip Scale |
| WLCSP | Wafer Level CSP | Smallest footprint |
| FCBGA | Flip-Chip BGA | Flip-chip interconnect |

### Package Extraction Logic

The handler extracts package codes from the suffix after the last hyphen:

```java
// Direct match
"BGA" -> "BGA"
"CSP" -> "CSP"
"POP" or "PoP" -> "Package-on-Package"
"QFN" -> "QFN"
"PQFN" -> "Power QFN"
"LFCSP" -> "Lead Frame CSP"
"WLCSP" -> "Wafer Level CSP"
"FCBGA" -> "Flip-Chip BGA"

// Contains check (fallback)
Contains "BGA" -> "BGA"
Contains "CSP" -> "CSP"
Contains "QFN" -> "QFN"
```

---

## Series Extraction Logic

The handler extracts series by collecting letters and digits before any hyphen:

```java
// Algorithm: collect alphanumerics until hyphen or end of letter+digit pattern
SM8550-AB → SM8550
QCA6390 → QCA6390
PM8550 → PM8550
MDM9650 → MDM9650
```

The extraction stops when:
1. A hyphen is encountered
2. Letters and digits have both been found, and a non-alphanumeric appears

---

## Snapdragon Naming Evolution

### Modern Naming (2021+)

| Series | Tier | Examples |
|--------|------|----------|
| SM8xxx | Flagship (8-series) | SM8550 (Gen 2), SM8650 (Gen 3) |
| SM7xxx | Premium (7-series) | SM7550, SM7450 |
| SM6xxx | Mainstream (6-series) | SM6350, SM6225 |
| SM4xxx | Budget (4-series) | SM4350, SM4250 |

### Legacy Naming

| Series | Year | Examples |
|--------|------|----------|
| SD8xx | 2017-2021 | SD888, SD865, SD855, SD845 |
| SD7xx | 2018-2021 | SD780, SD765, SD750 |
| SD6xx | 2017-2021 | SD695, SD680, SD660 |
| SD4xx | 2016-2021 | SD480, SD460, SD450 |
| MSM89xx | 2014-2017 | MSM8996, MSM8953 |

### Performance Tiers (Suffix Keywords)

| Tier | Keyword | Description |
|------|---------|-------------|
| Elite | Elite | Highest performance |
| Plus | Plus | Enhanced variant |
| Pro | Pro | Professional variant |
| Standard | (none) | Base variant |

### Generation (Suffix Keywords)

| Generation | Keyword | Year |
|------------|---------|------|
| Gen 1 | Gen1 | 2021 |
| Gen 2 | Gen2 | 2022 |
| Gen 3 | Gen3 | 2023 |

---

## Supported ComponentTypes

The handler registers all patterns under `ComponentType.IC` and declares:

```java
getSupportedTypes() → { WIFI_IC_QUALCOMM }
```

**Known Issue**: The handler registers patterns for many IC categories (SoCs, modems, PMICs, etc.) but only declares `WIFI_IC_QUALCOMM` in `getSupportedTypes()`. Consider adding `IC` to `getSupportedTypes()` for completeness.

---

## Replacement Compatibility Logic

The handler implements sophisticated replacement checking via `isOfficialReplacement()`:

### Compatible Series Pairs

| Series 1 | Series 2 | Category |
|----------|----------|----------|
| SD8xx | SD8xx | Snapdragon flagship |
| SM8xx | SM8xx | Snapdragon mobile |
| QCS4xx | QCS4xx | IoT platform |
| QCM2xx | QCM2xx | IoT module |
| QM4xx | QM4xx | RF module |
| QCA6xx | QCA6xx | Wi-Fi/Bluetooth |
| WCN3xx | WCN3xx | Wireless connectivity |

### Category-Specific Checks

**Snapdragon SoCs** (SM, SD, QSD, MSM):
- Generation compatibility (higher gen can replace lower)
- Performance tier compatibility (Elite > Plus > Pro > Standard)

**Wireless Modules** (QCA, WCN, MDM, FSM):
- Wi-Fi version compatibility (WiFi-6 > WiFi-5 > WiFi-4)
- Bluetooth version compatibility (5.2 > 5.1 > 5.0 > 4.2)

**Power Management** (PM, PMI, SMB):
- Voltage rating compatibility (within 5% tolerance)
- Current rating compatibility (higher can replace lower)

---

## Example MPNs

### Mobile SoCs

| MPN | Description |
|-----|-------------|
| SM8550-AB | Snapdragon 8 Gen 2 flagship SoC |
| SM8450-3-AB | Snapdragon 8 Gen 1 SoC |
| SD888 | Snapdragon 888 flagship (legacy naming) |
| MSM8996 | Snapdragon 820/821 SoC |
| QSD8250 | First-gen Snapdragon |

### IoT Platforms

| MPN | Description |
|-----|-------------|
| QCS603 | Vision Intelligence Platform |
| QCM6490 | IoT module with 5G |
| APQ8064 | Application processor (no modem) |
| IPQ8074 | Networking processor for routers |

### RF Front-End

| MPN | Description |
|-----|-------------|
| QM42195 | RF front-end module |
| QPM5677 | Power amplifier module |
| QAT3555 | Antenna tuner |
| QET6100 | Envelope tracking module |

### Wireless Connectivity

| MPN | Description |
|-----|-------------|
| QCA6390 | Wi-Fi 6E / Bluetooth 5.2 |
| QCA6174A-3-FCBGA | Wi-Fi 5 / BT 4.2, FCBGA package |
| WCN6855 | Wi-Fi 6E combo chip |
| MDM9650 | LTE Cat-9 modem |

### Power Management

| MPN | Description |
|-----|-------------|
| PM8550 | Main PMIC for SM8550 |
| PMI8998 | Power management IC |
| SMB1360-1-BGA | Battery charging IC, BGA package |

### Audio

| MPN | Description |
|-----|-------------|
| WCD9380 | Audio codec |
| WSA8810 | Smart speaker amplifier |

---

## Handler Implementation Notes

### Pattern Matching

All patterns are registered under `ComponentType.IC`:

```java
// Mobile Platforms
"^SM[0-9]{3}.*"       // SM8550, SM7450
"^SD[0-9]{3}.*"       // SD888, SD865
"^QSD[0-9]{4}.*"      // QSD8250
"^MSM[0-9]{4}.*"      // MSM8996

// IoT/Embedded
"^QCS[0-9]{3}.*"      // QCS603
"^QCM[0-9]{3}.*"      // QCM2150
"^APQ[0-9]{4}.*"      // APQ8064
"^IPQ[0-9]{4}.*"      // IPQ8074

// RF Front-End
"^QM[0-9]{4}.*"       // QM42195
"^QPM[0-9]{4}.*"      // QPM5677
"^QAT[0-9]{4}.*"      // QAT3555
"^QET[0-9]{4}.*"      // QET6100

// Wireless
"^QCA[0-9]{4}.*"      // QCA6390
"^WCN[0-9]{4}.*"      // WCN6855
"^MDM[0-9]{4}.*"      // MDM9650
"^FSM[0-9]{4}.*"      // FSM9955

// Power Management
"^PM[0-9]{4}.*"       // PM8550
"^PMI[0-9]{4}.*"      // PMI8998
"^SMB[0-9]{3}.*"      // SMB1360

// Audio
"^WCD[0-9]{4}.*"      // WCD9380
"^WSA[0-9]{4}.*"      // WSA8810
```

### Known Issues

1. **HashSet in getSupportedTypes()**: Uses `HashSet` instead of `Set.of()` - should be updated for consistency
2. **IC type not in getSupportedTypes()**: Handler registers patterns for `ComponentType.IC` but only declares `WIFI_IC_QUALCOMM` - may cause `matches()` to return true but type not in supported set
3. **Commented-out code**: Line 54 has commented-out `WIFI_IC` type

---

## Related Files

- Handler: `manufacturers/QualcommHandler.java`
- Component types: `WIFI_IC_QUALCOMM`
- Tests: (None currently - handler needs test coverage)

---

## Learnings & Quirks

- **PMIC naming convention**: PM/PMI part numbers often match the SoC they're designed for (PM8550 pairs with SM8550)
- **Atheros heritage**: QCA prefix comes from Qualcomm Atheros acquisition (2011) - Wi-Fi/Bluetooth expertise
- **Package suffix variability**: Many Qualcomm parts are sold without explicit package suffix in MPN
- **Generation extraction**: The handler extracts generation from 3-digit numeric portions (first digit = generation, second digit = tier)
- **Wi-Fi capability keywords**: Some MPNs include "ax", "ac", "n" to indicate Wi-Fi version
- **BT version in MPN**: Bluetooth version may appear as "BT5.2", "BT5.1", etc. in some variants

<!-- Add new learnings above this line -->
