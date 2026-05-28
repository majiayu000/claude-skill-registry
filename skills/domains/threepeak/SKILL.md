---
name: threepeak
description: 3PEAK (Suzhou 3PEAK Electronic Inc.) MPN encoding patterns, suffix decoding, and handler guidance. Use when working with 3PEAK analog ICs or ThreePeakHandler.
---

# 3PEAK Manufacturer Skill

## MPN Structure

3PEAK MPNs follow this general structure:

```
TP[SERIES][VARIANT]-[PACKAGE][OPTIONS]
│    │       │         │        │
│    │       │         │        └── Optional: voltage options (-5, -33)
│    │       │         └── Package code (TR, QR, MR, DR)
│    │       └── Part number within series
│    └── Series (1xxx=Op-Amp, 2xxx=Precision, 5xxx=ADC, 7xxx=LDO, 1xx=Current Sense)
└── 3PEAK prefix
```

### Example Decoding

```
TP1541-TR
│  │   │
│  │   └── TR = SOT-23 package, Tape & Reel
│  └── 1541 = Op-Amp series
└── TP = 3PEAK prefix

TP7150-MR-33
│  │   │  │
│  │   │  └── -33 = 3.3V output option
│  │   └── MR = MSOP package
│  └── 7150 = LDO regulator series
└── TP = 3PEAK prefix
```

---

## Package Codes

| Code | Package | Notes |
|------|---------|-------|
| TR | SOT-23 | Small signal |
| QR | QFN | Quad Flat No-lead |
| MR | MSOP | Mini Small Outline |
| DR | SOIC | Small Outline IC |
| SR | SOP | Small Outline Package |
| PR | TSSOP | Thin Shrink SOP |

---

## Product Series

### Op-Amps (TP1xxx, TP2xxx)

| Series | Type | Key Features |
|--------|------|--------------|
| TP1541 | General Op-Amp | Single supply, rail-to-rail |
| TP2111 | Precision Op-Amp | Low offset, high CMRR |
| TP2304 | Precision Op-Amp | Low noise |
| TP2071 | General Op-Amp | Single supply |
| TP2072 | Dual Op-Amp | Rail-to-rail |
| TP2082 | Dual Op-Amp | Low power |
| TP2092 | Dual Op-Amp | High bandwidth |
| TP2231 | Dual Op-Amp | Low noise |
| TP2232 | Dual Op-Amp | Low power |

### Comparators (TP1xxx, TP2xxx)

| Series | Type | Key Features |
|--------|------|--------------|
| TP1561 | Comparator | Low power |
| TP2345 | Comparator | Fast response |
| TP1393 | Comparator | Open-drain output |
| TP2393 | Dual Comparator | Open-drain |

### LDO Voltage Regulators (TP7xxx)

| Series | Type | Key Features |
|--------|------|--------------|
| TP7140 | LDO | Low dropout |
| TP7150 | LDO | Ultra-low noise |

### ADCs (TP5xxx)

| Series | Type | Key Features |
|--------|------|--------------|
| TP5551 | ADC | Delta-sigma |
| TP5854 | ADC | High precision |

### Current Sense Amplifiers (TP1xx)

| Series | Type | Key Features |
|--------|------|--------------|
| TP181 | Current Sense | High-side sensing |
| TP182 | Current Sense | Bidirectional |

---

## Handler Implementation Notes

### Component Type Detection

The handler distinguishes between similar-looking part numbers:

```java
// Op-amps have 4-digit part numbers (TP1541, TP2111)
// Current sense amps have 3-digit part numbers (TP181, TP182)
// Comparators share prefix but have specific part numbers (TP1561, TP2345)

// CRITICAL: Comparators must be excluded from op-amp detection
if (COMPARATOR_PATTERN.matcher(mpn).matches()) {
    return false; // Not an op-amp
}
```

### Package Code Extraction

```java
// Package code is the 2-letter suffix after the part number
// TP1541-TR -> TR = SOT-23
// TP7150MR  -> MR = MSOP (no hyphen variant)

// Remove voltage options before extracting package
String baseMpn = upperMpn.replaceAll("-[0-9]+$", "");
```

### Series Extraction

```java
// Current sense amps: TP18x -> "TP18"
// Standard 4-digit: TP1541 -> "TP1"
// Standard 4-digit: TP7150 -> "TP7"

if (upperMpn.matches("^TP18[0-9].*")) {
    return "TP18";  // Special case for current sense
}
```

---

## Related Files

- Handler: `manufacturers/ThreePeakHandler.java`
- Component types: `OPAMP`, `VOLTAGE_REGULATOR`, `IC`

---

## Series Descriptions

| Series | Description |
|--------|-------------|
| TP1 | Op-Amps/Comparators |
| TP2 | Precision Op-Amps/Comparators |
| TP5 | ADCs |
| TP7 | LDO Regulators |
| TP18 | Current Sense Amplifiers |

---

## Voltage Options (LDO Regulators)

LDO regulators often have voltage options encoded as suffix:

| Suffix | Output Voltage |
|--------|---------------|
| -5 | 5.0V |
| -33 | 3.3V |
| -25 | 2.5V |
| -18 | 1.8V |
| -12 | 1.2V |

---

## Learnings & Edge Cases

- **3-digit vs 4-digit parts**: TP181 (3-digit) is current sense amplifier, TP1541 (4-digit) is op-amp
- **Comparator exclusion**: TP1561 and TP2345 are comparators, NOT op-amps, despite similar prefixes
- **Package code hyphen**: Both `TP1541-TR` and `TP1541TR` formats are valid
- **Voltage option suffix**: `-33` means 3.3V output, not package variation

<!-- Add new learnings above this line -->
