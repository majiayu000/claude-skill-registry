---
name: infineon
description: Infineon Technologies MPN encoding patterns, package codes, and handler guidance. Use when working with Infineon MOSFETs, IGBTs, MCUs, or InfineonHandler.
---

# Infineon Technologies Manufacturer Skill

## MPN Structure

Infineon uses several distinct naming conventions depending on product family:

### Legacy IRF/IRL MOSFETs (from International Rectifier acquisition)

```
[PREFIX][SERIES][VOLTAGE][SUFFIX]
   |       |       |        |
   |       |       |        +-- Package: N=TO-220, L=TO-262, S=D2PAK, U=IPAK, P=TO-247
   |       |       +-- Voltage class/current identifier
   |       +-- F=Standard, L=Logic Level, FP=Power, FB=Bridge
   +-- IR = International Rectifier legacy
```

### OptiMOS/StrongIRFET (Current Infineon)

```
[PKG PREFIX][VOLTAGE][RDS(on)][SERIES][GEN]
     |          |        |       |      |
     |          |        |       |      +-- Generation: 5, 6 (OptiMOS gen)
     |          |        |       +-- N=N-channel, P=P-channel
     |          |        +-- On-resistance in mOhm
     |          +-- Voltage rating (divided by 10)
     +-- Package code (IPP=TO-220, IPB=D2PAK, IPD=DPAK, BSC=SuperSO8)
```

### CoolSiC MOSFETs

```
I[M][PACKAGE][VOLTAGE]R[RDS(on)][GEN]
|  |    |        |       |        |
|  |    |        |       |        +-- M1=Gen 1, M2=Gen 2
|  |    |        |       +-- On-resistance (e.g., R045 = 45mOhm)
|  |    |        +-- Voltage / 10 (120 = 1200V)
|  |    +-- W=TO-247 3pin, Z=TO-247 4pin
|  +-- M = CoolSiC MOSFET technology
+-- I = Infineon
```

### XMC Microcontrollers

```
XMC[SERIES][VARIANT]-[PACKAGE][PINS]X[FLASH]-[REV]
     |        |          |      |      |       |
     |        |          |      |      |       +-- Revision (AB, AA)
     |        |          |      |      +-- Flash size in KB
     |        |          |      +-- Pin count
     |        |          +-- T=TSSOP, Q=QFN, F=LQFP
     |        +-- 00, 01, 02, 03, etc.
     +-- 1000 (Cortex-M0), 4000 (Cortex-M4)
```

---

## Package Codes (Prefix System)

### Through-Hole Packages (Power)

| Prefix | Package | Thermal | Notes |
|--------|---------|---------|-------|
| IPP, SPP | TO-220 | Excellent | Standard power |
| IPA, SPA | TO-220 FullPAK | Excellent | Isolated |
| IPI, SPI | I2PAK (TO-262) | Good | Vertical mount |
| IPW, SPW | TO-247 | Superior | High power |
| IPT | TO-Leadless (TOLL) | Superior | Compact high power |

### Surface Mount - Power

| Prefix | Package | Footprint | Notes |
|--------|---------|-----------|-------|
| IPB, SPB | D2PAK (TO-263) | 15.2x10.2mm | High power SMD |
| IPD, SPD | DPAK (TO-252) | 6.6x6.1mm | Medium power SMD |
| IPS | IPAK Short Leads | 10.4x4.6mm | Low profile |

### Surface Mount - Small Signal

| Prefix | Package | Footprint | Notes |
|--------|---------|-----------|-------|
| BSC | SuperSO8 | 5x6mm | Bottom-side cooling |
| BSZ | PQFN 3.3x3.3 | 3.3x3.3mm | Compact power |
| BSK | PQFN 2x2 | 2x2mm | Ultra-compact |
| BSO | SO-8 | 5x4mm | Standard SMD |

### New Package Nomenclature (2019+)

| Code | Package | Notes |
|------|---------|-------|
| SC | SuperSO8 | 5x6mm |
| SD | SOT-363 | 6-pin small signal |
| SL | TSOP-6 | 6-pin thin |
| SK | PQFN 2x2 | Compact |
| SA | SO8 | Standard 8-pin |
| SP | SOT-223 | Power small signal |
| SZ | PQFN 3.3x3.3 | Mid-size QFN |
| PA | TO-220 FullPAK | Isolated |
| PB | D2PAK | Power SMD |
| PD | DPAK | Medium SMD |
| PP | TO-220 | Standard |
| PS | IPAK Short | Low profile |
| PT | TO-Leadless | TOLL |
| PW | TO-247 | High power |

---

## Legacy IRF Package Suffixes

| Suffix | Package | Thermal Rating |
|--------|---------|----------------|
| N | TO-220 | 62W @25C |
| L | TO-262 (I2PAK) | 50W @25C |
| S | D2PAK | 110W @25C |
| U | IPAK | 50W @25C |
| P | TO-247 | 190W @25C |

---

## Temperature Grades

| Suffix | Range | Application |
|--------|-------|-------------|
| (none) | 0C to +70C | Commercial |
| -40 to +85 | Industrial | Most OptiMOS |
| -40 to +125 | Extended | High reliability |
| -40 to +175 | Automotive | AEC-Q101 qualified |

### Automotive Suffix

- **A** suffix typically indicates automotive grade (e.g., CoolMOS S7TA)
- AEC-Q101 qualified parts for automotive applications
- Industrial grade counterparts omit the "A" (e.g., CoolMOS S7T)

---

## Product Family Prefixes

### Power MOSFETs

| Prefix | Technology | Typical Voltage |
|--------|------------|-----------------|
| IRF | Legacy IR planar | 30-500V |
| IRL | Logic-level (low Vgs) | 30-100V |
| IRFP | Power (TO-247) | 100-500V |
| IRFB | Bridge (D2PAK) | 50-200V |
| IRFZ | Z-series standard | 50-100V |
| IPP/IPB/IPD | OptiMOS/StrongIRFET | 25-300V |
| BSC/BSZ | OptiMOS small signal | 25-100V |

### IGBTs

| Prefix | Description | Package |
|--------|-------------|---------|
| IKP | Standard IGBT | TO-220 |
| IKW | High-power IGBT | TO-247 |
| IKB | D2PAK IGBT | D2PAK |

### Voltage Regulators & ICs

| Prefix | Category | Examples |
|--------|----------|----------|
| IFX | Automotive ICs | IFX91041EJ |
| ILD | LED Drivers | ILD4035 |
| IRS | Gate Drivers | IRS2184 |
| TLE | Automotive linear | TLE4271 |

### Microcontrollers

| Prefix | Family | Core |
|--------|--------|------|
| XMC1xxx | XMC1000 | Cortex-M0 |
| XMC4xxx | XMC4000 | Cortex-M4F |
| TC2xx | AURIX | TriCore |

---

## Common Series Reference

### OptiMOS Generations

| Generation | Technology | RDS(on) Improvement |
|------------|------------|---------------------|
| OptiMOS 3 | Trench | Baseline |
| OptiMOS 5 | Advanced trench | 30% lower |
| OptiMOS 6 | 6th gen | 40% lower |
| OptiMOS 7 | Latest | Best-in-class |

### Popular MOSFETs

| Part Number | Type | Vds | Rds(on) | Package |
|-------------|------|-----|---------|---------|
| IRFZ44N | N-ch | 55V | 17.5mOhm | TO-220 |
| IRF3205 | N-ch | 55V | 8mOhm | TO-220 |
| IRF540N | N-ch | 100V | 44mOhm | TO-220 |
| IRF9540N | P-ch | -100V | 117mOhm | TO-220 |
| IRL540N | N-ch Logic | 100V | 44mOhm | TO-220 |
| IRFP460 | N-ch Power | 500V | 270mOhm | TO-247 |
| IPP060N06N | N-ch OptiMOS | 60V | 6mOhm | TO-220 |
| BSC014N06NS | N-ch OptiMOS | 60V | 1.4mOhm | SuperSO8 |

### XMC Microcontrollers

| Part Number | Series | Flash | Pins | Package |
|-------------|--------|-------|------|---------|
| XMC1100-T038X0064-AB | XMC1100 | 64KB | 38 | TSSOP |
| XMC1202-T028X0064-AB | XMC1200 | 64KB | 28 | TSSOP |
| XMC4500-F100F1024-AA | XMC4500 | 1MB | 100 | LQFP |

---

## Handler Implementation Notes

### Issues Found in Current Handler

1. **HashSet usage** (line 41): Should use `Set.of()` or `EnumSet` for immutability
2. **Series extraction order bug**: Checks `IRF` before `IRFP/IRFB`, so "IRFP4560" returns "IRF"
3. **Missing patterns**: No patterns for XMC MCUs, OptiMOS (IPP, BSC series), despite being in getSupportedTypes()
4. **Package extraction incomplete**: Only handles legacy IRF suffix codes, not new prefix-based system

### Series Extraction Fix

```java
// WRONG - "IRF" matches before "IRFP" is checked
if (mpn.startsWith("IRF")) return "IRF";
if (mpn.startsWith("IRFP")) return "IRFP";  // Never reached for IRFP4560!

// CORRECT - Check longer prefixes FIRST
if (mpn.startsWith("IRFP")) return "IRFP";  // Specific series first
if (mpn.startsWith("IRFB")) return "IRFB";  // Specific series first
if (mpn.startsWith("IRFZ")) return "IRFZ";  // Specific series first
if (mpn.startsWith("IRF")) return "IRF";    // General fallback last
```

### Package Code Extraction

```java
// Legacy IRF suffix-based
if (mpn.matches(".*[0-9]N$")) return "TO-220";
if (mpn.matches(".*[0-9]S$")) return "D2PAK";
if (mpn.matches(".*[0-9]L$")) return "TO-262";
if (mpn.matches(".*[0-9]P$")) return "TO-247";

// New prefix-based (OptiMOS/StrongIRFET)
if (upperMpn.startsWith("IPP") || upperMpn.startsWith("SPP")) return "TO-220";
if (upperMpn.startsWith("IPB") || upperMpn.startsWith("SPB")) return "D2PAK";
if (upperMpn.startsWith("IPD") || upperMpn.startsWith("SPD")) return "DPAK";
if (upperMpn.startsWith("IPW") || upperMpn.startsWith("SPW")) return "TO-247";
if (upperMpn.startsWith("IPI") || upperMpn.startsWith("SPI")) return "I2PAK";
if (upperMpn.startsWith("BSC")) return "SuperSO8";
if (upperMpn.startsWith("BSZ")) return "PQFN-3.3x3.3";
```

### Missing Pattern Registration

```java
// OptiMOS/StrongIRFET (should be added)
registry.addPattern(ComponentType.MOSFET, "^IP[PBDIWTA][0-9].*");
registry.addPattern(ComponentType.MOSFET, "^SP[PBDIW][0-9].*");
registry.addPattern(ComponentType.MOSFET, "^BS[CZKOA][0-9].*");

// XMC Microcontrollers (should be added)
registry.addPattern(ComponentType.MICROCONTROLLER_INFINEON, "^XMC[14][0-9]{3}.*");
registry.addPattern(ComponentType.MCU_INFINEON, "^XMC[14][0-9]{3}.*");

// CoolSiC MOSFETs (should be added)
registry.addPattern(ComponentType.MOSFET_INFINEON, "^IM[WZ][0-9]+R[0-9]+.*");
```

---

## Related Files

- Handler: `manufacturers/InfineonHandler.java`
- Component types: `MOSFET_INFINEON`, `IGBT_INFINEON`, `VOLTAGE_REGULATOR_LINEAR_INFINEON`, `VOLTAGE_REGULATOR_SWITCHING_INFINEON`, `LED_DRIVER_INFINEON`, `GATE_DRIVER_INFINEON`, `MICROCONTROLLER_INFINEON`, `MCU_INFINEON`, `OPAMP_INFINEON`, `MEMORY_INFINEON`

---

## Learnings & Edge Cases

- **IRF acquisition**: Infineon acquired International Rectifier in 2015, inheriting the IRF/IRL nomenclature
- **Dual naming**: Many parts have both old IRF names and new Infineon names (cross-reference needed)
- **Package prefix vs suffix**: Legacy IRF uses suffix (IRFZ44N), new OptiMOS uses prefix (IPP060N06N)
- **Logic level**: IRL series has lower gate threshold voltage (Vgs < 5V) for direct MCU drive
- **PbF suffix**: Lead-free (RoHS compliant) designation on some parts
- **-7 suffix**: Sometimes indicates 7-pin variant (e.g., D2PAK-7)

<!-- Add new learnings above this line -->
