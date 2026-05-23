---
name: classify-anomaly
description: Classify speleothem anomalies as seismic, climatic, volcanic, or compound events. Use when discriminating earthquake signals from climate/volcanic false positives. Triggers on "classify anomaly", "seismic or climatic", "discrimination", "is this an earthquake".
---

# /classify-anomaly - Multi-Proxy Discrimination Skill

## Purpose

Apply the multi-proxy discrimination framework to classify geochemical anomalies as SEISMIC, CLIMATIC, VOLCANIC, or COMPOUND (CVSE). This is the core methodology for distinguishing earthquake signals from false positives.

## Usage

```
/classify-anomaly <d18O_z> <d13C_z> [--MgCa Z] [--recovery YEARS] [--date YEAR]
```

**Examples:**
```
/classify-anomaly -2.46 +1.60                    # Basic two-proxy
/classify-anomaly -2.16 N/A --MgCa +1.60         # Missing δ13C, use Mg/Ca
/classify-anomaly -3.77 -1.18 --date 1275        # Check volcanic correlation
/classify-anomaly -3.6 -2.36 --recovery 46       # With recovery time
```

## Discrimination Framework

### Primary Decision Tree

```
Is there a significant anomaly (|z| ≥ 2.0)?
├─ NO → NORMAL (no event detected)
└─ YES → Check proxy coupling...
         │
         ├─ COUPLED (δ18O and δ13C both anomalous, same sign)
         │   └─ Coupling ratio < 2.0 → **SEISMIC CANDIDATE**
         │
         ├─ DECOUPLED (δ18O anomalous, δ13C normal or opposite)
         │   ├─ Volcanic correlation? → **VOLCANIC**
         │   └─ No volcanic correlation → **CLIMATIC** (drought/wet)
         │
         └─ δ13C ONLY anomalous (δ18O normal)
             └─ Check geogenic CO₂ sources → **SEISMIC CANDIDATE**
```

### Proxy Rules

| Proxy | Seismic Signal | Climatic Signal | Volcanic Signal |
|-------|----------------|-----------------|-----------------|
| **δ18O** | Negative (deep water) | Variable | Negative (wet) |
| **δ13C** | Positive > -8‰ (geogenic CO₂) | Negative < -10‰ (biogenic) | Variable |
| **Mg/Ca** | Positive (old water) | Negative (dilution) | Variable |
| **Coupling ratio** | < 2.0 (COUPLED) | > 3.0 (DECOUPLED) | > 3.0 (DECOUPLED) |
| **Recovery time** | 5-71 years | 1-7 years | 1-3 years |

### Coupling Ratio Calculation

```
Coupling ratio = |δ18O_z| / |δ13C_z|

< 2.0  → COUPLED (seismic)
2.0-3.0 → AMBIGUOUS
> 3.0  → DECOUPLED (climatic/volcanic)
```

### Recovery Time Assessment

| Duration | Classification | Example |
|----------|----------------|---------|
| 1-3 years | **VOLCANIC** | Samalas 1257 recovery |
| 3-7 years | **CLIMATIC** | Drought recovery |
| 10-30 years | **SEISMIC** | Typical earthquake |
| 30-71 years | **MAJOR SEISMIC** | Lapa Grande ~96 CE (71 yr) |

### Temporal Shape (Mg/Ca)

| Shape | Onset Rate | Classification |
|-------|------------|----------------|
| **SHARK FIN** | > 0.5 σ/mm | SEISMIC (rapid onset) |
| **HUMP** | < 0.5 σ/mm | CLIMATIC (gradual onset) |

## Classification Output

```markdown
## Anomaly Classification: [Date/Window]

### Input Metrics

| Metric | Value | Notes |
|--------|-------|-------|
| δ18O z-score | -2.46σ | Significant negative |
| δ13C z-score | +1.60σ | Marginal positive |
| Mg/Ca z-score | +2.25σ | Significant positive |
| Recovery time | 15 years | Extended |
| Coupling ratio | 1.54 | COUPLED |

### Discrimination Tests

| Test | Result | Interpretation |
|------|--------|----------------|
| δ18O significance | ✓ PASS | z ≤ -2.0 |
| δ13C coupling | ✓ PASS | Same direction, ratio < 2 |
| Mg/Ca elevation | ✓ PASS | Deep/old water signature |
| Recovery duration | ✓ PASS | > 10 years |
| Volcanic correlation | ✗ NONE | No major eruptions ±5 years |

### CLASSIFICATION: **SEISMIC CANDIDATE** (Tier 1)

**Confidence**: HIGH
**Evidence tier**: Tier 1 (multi-proxy)

**Rationale**:
- Coupled proxies (ratio 1.54) indicate Chiodini mechanism
- Elevated Mg/Ca confirms deep water mobilization
- Extended recovery (15 yr) rules out volcanic/climatic
- No volcanic forcing in time window
```

## Evidence Tiers

| Tier | Requirements | Confidence |
|------|--------------|------------|
| **Tier 1** | Multi-proxy (δ18O + Mg/Ca OR δ13C) + recovery > 10 yr + no volcanic | HIGH |
| **Tier 2** | δ18O + historical documentation OR single additional proxy | MODERATE |
| **Tier 3** | Single proxy OR weak correlation | LOW |

## Volcanic Correlation Check

When `--date` is provided, check against major eruptions:

| Date Window | Major Eruptions | VSSI (Tg S) |
|-------------|-----------------|-------------|
| 1255-1260 CE | **Samalas 1257** | 59.42 |
| 1228-1235 CE | Unknown 1230 | 23.78 |
| 1105-1115 CE | Unknown 1108 | 19.16 |
| 1452-1458 CE | Kuwae 1452 | 31.06 |
| 1808-1816 CE | Unknown 1809 + Tambora 1815 | 22.10 + 26.03 |

**If date ±5 years overlaps major eruption AND proxies are DECOUPLED → VOLCANIC**

## Output Classifications

| Classification | Criteria |
|----------------|----------|
| **SEISMIC** | Coupled proxies, no volcanic, recovery > 10 yr |
| **CLIMATIC** | Decoupled proxies, no volcanic |
| **VOLCANIC** | Decoupled proxies, volcanic correlation |
| **CVSE** | Compound event: volcanic + seismic + hydrological |
| **EQUIVOCAL** | Insufficient evidence to classify |

## CVSE (Compound Volcanic-Seismic Event) Criteria

All THREE must be present:
1. **Volcanic forcing** - Documented eruption in ice cores
2. **Seismic signal** - Mg/Ca or δ13C proxy confirmation
3. **Hydrological expression** - Documented floods or aquifer disruption

**Known CVSEs:**
- 1285 Italy (UE6 + earthquake + Genoa floods)
- 936 Belize (Eldgjá + seismic + global floods)
- 853 Pacific NW (Churchill VEI 6 + Cascadia S + drought)

## Example Full Analysis

```
User: /classify-anomaly -3.77 -1.18 --date 1275 --recovery 3

Classification Analysis:

Input:
- δ18O z = -3.77σ (EXTREME NEGATIVE)
- δ13C z = -1.18σ (not significant)
- Date: ~1275 CE
- Recovery: 3 years

Tests:
- Coupling ratio: 3.77/1.18 = 3.19 → DECOUPLED
- Volcanic check: 1257 Samalas (59.42 Tg S) within 18 years
- Recovery: 3 years (volcanic range)

CLASSIFICATION: **VOLCANIC**

Rationale:
- Decoupled signature (δ18O >> δ13C)
- Temporal proximity to 1257 Samalas (largest eruption in 2000 years)
- Short recovery (3 yr) matches volcanic pattern
- NOT seismic despite extreme δ18O

This is the documented Samalas volcanic response at Yok Balum.
```

## Important Notes

1. **Missing δ13C** - Use Mg/Ca as substitute coupling test
2. **Uncertainty propagates** - Single proxy = Tier 3 max
3. **CVSE is rare** - Requires ALL THREE components
4. **Recovery time is diagnostic** - "Order of magnitude gap" between volcanic (1-3 yr) and seismic (10-71 yr)
5. **Update ANOMALY_CATALOG.md** - After classification with approval
