---
name: volcanic-check
description: Check if a speleothem anomaly correlates with volcanic eruptions. Use when ruling out volcanic false positives, checking eVolv2k/VSSI records, or validating seismic interpretations. Triggers on "volcanic check", "eruption correlation", "rule out volcanic", "eVolv2k".
---

# /volcanic-check - Volcanic Correlation Analysis Skill

## Purpose

Cross-reference speleothem anomalies with volcanic eruption records to rule out volcanic false positives. Critical for validating seismic interpretations.

## Usage

```
/volcanic-check <year_CE> [--window YEARS] [--threshold VSSI]
```

**Examples:**
```
/volcanic-check 1275                    # Check around 1275 CE (±20 years default)
/volcanic-check 620 --window 50         # Wider window for uncertain dates
/volcanic-check 1394 --threshold 10     # Only major eruptions (>10 Tg S)
```

## Volcanic Databases

### Primary Source: eVolv2k

The eVolv2k database (Toohey & Sigl 2017) provides:
- Volcanic Stratospheric Sulfur Injection (VSSI) in Tg S
- Ice core dated eruptions back to 500 BCE
- Uncertainty ranges

### Reference Eruptions (VSSI Rankings)

| Rank | Year | Eruption | VSSI (Tg S) | Global Impact |
|------|------|----------|-------------|---------------|
| 1 | 1257 | **Samalas** | 59.42 | Extreme (1258 famine) |
| 2 | 1815 | Tambora | 26.03 | "Year without summer" |
| 3 | 1452 | Kuwae | 31.06 | Major cooling |
| 4 | 1230 | Unknown | 23.78 | Significant |
| 5 | 1108 | Unknown | 19.16 | Significant |
| 6 | 1809 | Unknown | 22.10 | Pre-Tambora event |
| 7 | 939 | Eldgjá | 18.81 | Basaltic flood |
| 8 | 536 | Unknown (Ilopango?) | ~15+ | "Worst year to be alive" |
| 9 | 1783 | Laki | 17.08 | European famine |
| 10 | 1286 | UE6 (Unknown) | ~10 | Post-Samalas cluster |

## Workflow

### Step 1: Define Search Window

```
Center: [input_year]
Window: ±[window] years (default ±20)
Search range: [input_year - window] to [input_year + window]
```

### Step 2: Query eVolv2k Database

Search for eruptions in window:

```markdown
### Volcanic Events Within ±20 Years of [YEAR] CE

| Year | Eruption | VSSI (Tg S) | Rank | Distance (years) |
|------|----------|-------------|------|------------------|
| 1257 | Samalas | 59.42 | #1 | -18 |
| 1286 | UE6 | ~10 | - | +11 |
```

### Step 3: Assess Volcanic Forcing Potential

| VSSI (Tg S) | Classification | Expected Speleothem Response |
|-------------|----------------|------------------------------|
| > 25 | **EXTREME** | Strong δ18O negative, 2-4 year recovery |
| 15-25 | **MAJOR** | Moderate δ18O negative, 1-3 year recovery |
| 5-15 | **MODERATE** | Weak signal possible |
| < 5 | **MINOR** | Unlikely to produce detectable signal |

### Step 4: Generate Correlation Report

```markdown
## Volcanic Correlation Check: [YEAR] CE

### Search Parameters
- Center year: [YEAR] CE
- Search window: ±[WINDOW] years
- VSSI threshold: [THRESHOLD] Tg S

### Eruptions Found

| Year | Eruption | VSSI (Tg S) | Distance | Correlation Risk |
|------|----------|-------------|----------|------------------|
| [year] | [name] | [vssi] | [±N yr] | [HIGH/MOD/LOW] |

### Assessment

**Volcanic forcing detected**: YES/NO

**Correlation risk**: HIGH / MODERATE / LOW / NONE

**Recommendation**: [Interpretation guidance]
```

## Correlation Risk Assessment

| Risk Level | Criteria | Action |
|------------|----------|--------|
| **HIGH** | VSSI > 15 Tg S within ±10 years | Likely volcanic false positive |
| **MODERATE** | VSSI 5-15 Tg S within ±10 years OR VSSI > 15 within ±20 years | Check proxy decoupling |
| **LOW** | VSSI < 5 Tg S OR > 20 years distant | Volcanic unlikely |
| **NONE** | No eruptions in window | Volcanic ruled out |

## Decoupling Test Integration

If volcanic eruption found, check anomaly coupling:

```
Volcanic signature: DECOUPLED (δ18O >> δ13C)
Seismic signature: COUPLED (δ18O ≈ δ13C)

If HIGH volcanic risk + DECOUPLED → VOLCANIC
If HIGH volcanic risk + COUPLED → Possible CVSE (compound event)
If LOW volcanic risk → Seismic interpretation valid
```

## Known Volcanic False Positives (Yok Balum)

| Period | δ18O z | δ13C z | Ratio | Volcanic Event | Classification |
|--------|--------|--------|-------|----------------|----------------|
| 1273-1279 CE | -3.77 | -1.18 | 3.2 | 1257 Samalas | **VOLCANIC** |
| 1228-1238 CE | -2.93 | -1.91 | 1.5 | 1230 Unknown | **VOLCANIC** |
| 1105-1125 CE | -2.98 | ~-1.3 | 2.3 | 1108 Unknown | **VOLCANIC** |

## Example Full Output

```
User: /volcanic-check 1285

## Volcanic Correlation Check: 1285 CE

### Search Parameters
- Center year: 1285 CE
- Search window: ±20 years (1265-1305 CE)
- VSSI threshold: 5 Tg S

### Eruptions Found

| Year | Eruption | VSSI (Tg S) | Distance | Risk |
|------|----------|-------------|----------|------|
| **1257** | **Samalas** | **59.42** | **-28 yr** | **HIGH** |
| 1286 | UE6 | ~10 | +1 yr | MODERATE |

### Assessment

**Volcanic forcing detected**: YES

**Correlation risk**: **HIGH**
- 1257 Samalas (#1 eruption in 2000 years) is 28 years prior
- 1286 UE6 is 1 year after

**⚠️ WARNING**: This anomaly falls within the post-Samalas volcanic cluster period.

**Recommendation**:
1. Check proxy COUPLING - if decoupled (ratio > 2.5), likely volcanic
2. Check recovery time - if < 5 years, likely volcanic
3. If COUPLED + long recovery, may be CVSE (compound event)

For Italy 1285, this IS a known CVSE-1285 (volcanic + seismic + floods).
```

## Special Cases

### CVSE Detection

If volcanic + seismic indicators present:
```
CVSE requires ALL THREE:
1. Volcanic forcing (eruption in ice cores) ✓
2. Seismic signal (Mg/Ca or δ13C elevation) ✓
3. Hydrological expression (documented floods) ✓

If all three → CVSE (Compound Volcanic-Seismic Event)
```

### Pre-536 CE Events

⚠️ **Ice core dating less certain before 536 CE**
- Add ±50 year uncertainty
- Cross-reference multiple records

### Medieval Quiet Period (1000-1100 CE)

```
If anomaly in 1000-1100 CE:
- eVolv2k shows 55-70% below-average volcanic activity
- Volcanic false positive UNLIKELY
- Strengthens seismic interpretation (e.g., ~1075 CE Yok Balum)
```

## MCP/Web Resources

| Source | Use |
|--------|-----|
| **eVolv2k** | Primary volcanic forcing database |
| **VSSI** | Volcanic Stratospheric Sulfur Injection |
| **Ice cores** | GISP2, NGRIP, Law Dome |
| **WebSearch** | For eruption details, impacts |

## Important Notes

1. **Samalas 1257 dominates** - Any anomaly 1250-1280 CE is suspect
2. **Decoupling is key** - Volcanic = DECOUPLED, Seismic = COUPLED
3. **Recovery time diagnostic** - Volcanic 1-3 yr, Seismic 10-71 yr
4. **CVSE is rare but real** - Don't dismiss compound events
5. **Absence of volcanic ≠ seismic** - Must still show positive seismic indicators
