---
name: samtec
description: Samtec high-speed connector MPN encoding patterns, series identification, and handler guidance. Use when working with Samtec connectors or SamtecHandler.
---

# Samtec Manufacturer Skill

## MPN Structure

Samtec MPNs follow a consistent hyphen-delimited structure:

```
[SERIES]-[PINS]-[PITCH]-[MOUNT]-[OPTIONS]...[-TR]
   |       |      |       |        |          |
   |       |      |       |        |          └── Optional: TR for tape & reel
   |       |      |       |        └── Configuration options (S/D, DV, A, K, etc.)
   |       |      |       └── Profile/mounting (L=low, S=standard, etc.)
   |       |      └── Pitch in mm (e.g., 02.5 = 2.5mm)
   |       └── Pin count (e.g., 110 = 110 pins)
   └── Series prefix (LSHM, SEAM, HSEC8, QSH, QTH, TFM, TSM, SSW, TSW)
```

### Example Decoding

```
LSHM-110-02.5-L-DV-A-S-K-TR
│    │   │    │ │  │ │ │ │
│    │   │    │ │  │ │ │ └── TR = Tape & Reel
│    │   │    │ │  │ │ └── K = Keying/polarization
│    │   │    │ │  │ └── S = Surface mount option
│    │   │    │ │  └── A = Alignment option
│    │   │    │ └── DV = Dual row vertical
│    │   │    └── L = Low profile
│    │   └── 02.5 = 2.5mm pitch (displayed as 0.50mm for LSHM)
│    └── 110 = 110 pins
└── LSHM = High-Speed Micro Headers

HSEC8-120-01-L-DV-A
│     │   │  │ │  │
│     │   │  │ │  └── A = Alignment option
│     │   │  │ └── DV = Dual row vertical
│     │   │  └── L = Low profile
│     │   └── 01 = Pitch code (0.80mm for HSEC8)
│     └── 120 = 120 positions
└── HSEC8 = High-Speed Edge Card

TSW-110-01-L-S
│   │   │  │ │
│   │   │  │ └── S = Single row
│   │   │  └── L = Low profile
│   │   └── 01 = Pitch code (2.54mm for TSW)
│   └── 110 = 110 pins
└── TSW = Through-Hole Terminal Strip
```

---

## Product Series

### High-Speed Series (SMT)

| Series | Type | Pitch | Application |
|--------|------|-------|-------------|
| LSHM | Micro Headers | 0.50mm | High-speed board-to-board |
| HSEC8 | Edge Card | 0.80mm | High-speed edge card |
| QSH | Terminal Strip (Socket) | 0.635mm | High-speed terminal |
| QTH | Terminal Strip (Header) | 0.635mm | High-speed terminal |

### General Purpose Series (SMT/THT)

| Series | Type | Pitch | Application |
|--------|------|-------|-------------|
| SEAM | Card Edge | 1.27mm | Card edge connectors |
| TFM | Terminal Strip (Female) | 1.27mm | General purpose |
| TSM | Tiger Eye Terminal Strip | 1.27mm | General purpose |

### Through-Hole Series

| Series | Type | Pitch | Application |
|--------|------|-------|-------------|
| SSW | Socket Strip | 2.54mm | Through-hole socket |
| TSW | Terminal Strip | 2.54mm | Through-hole header |

---

## Series Descriptions

| Series | Full Name |
|--------|-----------|
| LSHM | High-Speed Micro Headers |
| SEAM | Card Edge Connectors |
| HSEC8 | High-Speed Edge Card |
| QSH | High-Speed Terminal Strip (Socket) |
| QTH | High-Speed Terminal Strip (Header) |
| TFM | Terminal Strip (Female) |
| TSM | Tiger Eye Terminal Strip |
| SSW | Through-Hole Socket Strip |
| TSW | Through-Hole Terminal Strip |

---

## Default Pitch by Series

| Series | Default Pitch (mm) |
|--------|-------------------|
| LSHM | 0.50 |
| SEAM | 1.27 |
| HSEC8 | 0.80 |
| QSH | 0.635 |
| QTH | 0.635 |
| TFM | 1.27 |
| TSM | 1.27 |
| SSW | 2.54 |
| TSW | 2.54 |

---

## Rated Current by Series

| Series | Current per Pin (A) |
|--------|---------------------|
| LSHM | 1.7 |
| SEAM | 1.5 |
| HSEC8 | 1.8 |
| QSH | 2.3 |
| QTH | 2.3 |
| TFM | 2.1 |
| TSM | 2.3 |
| SSW | 3.0 |
| TSW | 3.0 |

---

## Option Codes

### Mounting/Profile Options

| Code | Description |
|------|-------------|
| L | Low profile |
| S | Standard profile |
| RA | Right angle |
| R | Right angle (alternate) |

### Row Configuration

| Code | Description |
|------|-------------|
| S | Single row |
| D | Dual row |
| DV | Dual row vertical |

### Additional Options

| Code | Description |
|------|-------------|
| A | Alignment feature |
| K | Keying/polarization |
| TR | Tape and reel packaging |

---

## Handler Implementation Notes

### Pattern Matching

```java
// Each series follows SERIES-PINS-PITCH-OPTIONS format
"^LSHM-[0-9]+-.*"     // High-Speed Micro Headers
"^SEAM-[0-9]+-.*"     // Card Edge
"^HSEC8-[0-9]+-.*"    // High-Speed Edge Card
"^QSH-[0-9]+-.*"      // High-Speed Terminal Socket
"^QTH-[0-9]+-.*"      // High-Speed Terminal Header
"^TFM-[0-9]+-.*"      // Terminal Strip Female
"^TSM-[0-9]+-.*"      // Tiger Eye Terminal Strip
"^SSW-[0-9]+-.*"      // Through-Hole Socket Strip
"^TSW-[0-9]+-.*"      // Through-Hole Terminal Strip
```

### Series Extraction

```java
// Series is the first hyphen-delimited field
// LSHM-110-02.5-L-DV -> LSHM
// TSW-110-01-L-S -> TSW

for (String series : SERIES_FAMILIES.keySet()) {
    if (upperMpn.startsWith(series + "-")) {
        return series;
    }
}
```

### Pin Count Extraction

```java
// Pin count is the second hyphen-delimited field
// LSHM-110-02.5-L-DV -> 110

String[] parts = mpn.split("-");
if (parts.length >= 2) {
    return Integer.parseInt(parts[1]);
}
```

### Pitch Extraction

```java
// Pitch is the third hyphen-delimited field
// LSHM-110-02.5-L-DV -> "02.5"
// But actual pitch may differ from this code

// Use series default pitch for accurate value
String series = extractSeries(mpn);
return SERIES_DEFAULT_PITCH.get(series);
```

### Package Code Extraction

```java
// Package code is everything after pins and pitch
// LSHM-110-02.5-L-DV-A-S-K-TR -> L-DV-A-S-K-TR

String[] parts = mpn.split("-");
if (parts.length >= 4) {
    StringBuilder pkgCode = new StringBuilder();
    for (int i = 3; i < parts.length; i++) {
        if (pkgCode.length() > 0) pkgCode.append("-");
        pkgCode.append(parts[i]);
    }
    return pkgCode.toString();
}
```

---

## Replacement Compatibility

### Same Series Compatibility

For connectors to be interchangeable:
1. **Same series** (e.g., both LSHM)
2. **Same pin count** (must match exactly)
3. **Compatible mounting type** (SMT vs THT)

### Mating Pairs

| Socket/Female | Header/Male |
|---------------|-------------|
| QSH | QTH |
| SSW | TSW |
| TFM | TSM |

---

## Mounting Type by Series

| Series | Mounting |
|--------|----------|
| LSHM | SMT |
| HSEC8 | SMT |
| QSH | SMT |
| QTH | SMT |
| TFM | SMT |
| TSM | SMT |
| SEAM | Card Edge |
| SSW | THT |
| TSW | THT |

---

## High-Speed Capability

**High-speed rated series:**
- LSHM
- HSEC8
- QSH
- QTH

**Standard series (not high-speed rated):**
- SEAM
- TFM
- TSM
- SSW
- TSW

---

## Related Files

- Handler: `manufacturers/SamtecHandler.java`
- Component types: `ComponentType.CONNECTOR`, `ComponentType.IC`

---

## Learnings & Edge Cases

- **Hyphen-delimited format**: Unlike IC manufacturers, Samtec uses hyphens to separate all MPN fields
- **Pitch code vs actual pitch**: The pitch field in MPN may be a code (01, 02.5) rather than actual mm value
- **Component type includes IC**: Handler registers both CONNECTOR and IC types for pattern matching flexibility
- **Pin count in second field**: Always extract from second hyphen-delimited field
- **Series determines most specs**: Series alone determines pitch, mounting type, and current rating
- **Mating connector pairs**: QSH mates with QTH, SSW mates with TSW, TFM mates with TSM
- **TR suffix for packaging**: -TR at end indicates tape and reel packaging, strip for extraction

<!-- Add new learnings above this line -->
