---
name: sofa-score
description: Calculate SOFA (Sequential Organ Failure Assessment) score for ICU patients in MIMIC-IV. Use for sepsis severity assessment, organ dysfunction quantification, mortality prediction, or Sepsis-3 criteria evaluation.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: severity-scores
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/score
  validated: true
---

# SOFA Score Calculation

The Sequential Organ Failure Assessment (SOFA) score quantifies organ dysfunction across 6 systems. Each component scores 0-4, with a total range of 0-24. Higher scores indicate greater organ dysfunction.

## When to Use This Skill

- User asks about SOFA score calculation
- Sepsis-3 criteria assessment (SOFA >= 2 indicates organ dysfunction)
- Mortality prediction or severity stratification
- Comparing organ dysfunction between cohorts
- Calculating delta-SOFA (change from baseline)

## Components and Scoring

| System | 0 | 1 | 2 | 3 | 4 |
|--------|---|---|---|---|---|
| **Respiration** (PaO2/FiO2 mmHg) | >= 400 | < 400 | < 300 | < 200 + vent | < 100 + vent |
| **Coagulation** (Platelets x10^3/uL) | >= 150 | < 150 | < 100 | < 50 | < 20 |
| **Liver** (Bilirubin mg/dL) | < 1.2 | 1.2-1.9 | 2.0-5.9 | 6.0-11.9 | >= 12.0 |
| **Cardiovascular** | No hypotension | MAP < 70 | Dopa <= 5 or Dob | Dopa > 5 or Epi <= 0.1 or Norepi <= 0.1 | Dopa > 15 or Epi > 0.1 or Norepi > 0.1 |
| **CNS** (GCS) | 15 | 13-14 | 10-12 | 6-9 | < 6 |
| **Renal** (Creatinine mg/dL or UO) | < 1.2 | 1.2-1.9 | 2.0-3.4 | 3.5-4.9 or UO < 500 | >= 5.0 or UO < 200 |

Note: Vasopressor doses are in mcg/kg/min. UO is urine output in mL/day.

## Pre-computed Table

MIMIC-IV provides a pre-computed SOFA table with hourly values:

```sql
SELECT
    stay_id,
    hr,
    starttime,
    endtime,
    respiration_24hours,
    coagulation_24hours,
    liver_24hours,
    cardiovascular_24hours,
    cns_24hours,
    renal_24hours,
    sofa_24hours
FROM mimiciv_derived.sofa
WHERE hr = 24;  -- 24 hours after ICU admission
```

## Required Tables for Custom Calculation

- `mimiciv_icu.icustays` - ICU stay identifiers
- `mimiciv_derived.bg` - Blood gas for PaO2/FiO2 (specimen = 'ART.')
- `mimiciv_derived.chemistry` - Creatinine
- `mimiciv_derived.enzyme` - Bilirubin
- `mimiciv_derived.complete_blood_count` - Platelets
- `mimiciv_derived.gcs` - Glasgow Coma Scale
- `mimiciv_derived.urine_output_rate` - Daily urine output
- `mimiciv_derived.ventilation` - Ventilation status
- `mimiciv_derived.norepinephrine`, `epinephrine`, `dopamine`, `dobutamine` - Vasopressors

## Critical Implementation Notes

1. **Time Window**: The score uses the worst value in a 24-hour rolling window. SOFA calculated at hour 24 uses data from hours 0-24.

2. **Respiratory Score**: Requires interaction between PaO2/FiO2 ratio AND ventilation status:
   - Scores of 3 or 4 require mechanical ventilation
   - The lowest PaO2/FiO2 is tracked separately for ventilated vs non-ventilated periods

3. **FiO2 Sources**: FiO2 can come from blood gas measurement OR charted FiO2. When not documented, estimate from supplemental O2 device.

4. **Vasopressor Units**: All vasopressor doses must be in mcg/kg/min. Weight is often estimated (check `mimiciv_derived.weight_durations`).

5. **GCS in Sedated Patients**: For sedated/intubated patients, use pre-sedation GCS or assume normal (GCS=15). The verbal component may be 0 for intubated patients - this is handled specially.

6. **Arterial Blood Gas**: Use only arterial specimens (`specimen = 'ART.'`) for PaO2/FiO2.

7. **Missing Components**: Missing data is imputed as 0 (normal) in the final score. Document which components are missing; do not claim complete scores when data is absent.

8. **Urine Output Calculation**: Uses `uo_tm_24hr` to verify 24 hours of data available before calculating rate.

## Example: Get SOFA at 24h for All ICU Stays

```sql
SELECT
    ie.stay_id,
    ie.subject_id,
    ie.hadm_id,
    s.sofa_24hours,
    s.respiration_24hours,
    s.coagulation_24hours,
    s.liver_24hours,
    s.cardiovascular_24hours,
    s.cns_24hours,
    s.renal_24hours
FROM mimiciv_icu.icustays ie
LEFT JOIN mimiciv_derived.sofa s
    ON ie.stay_id = s.stay_id
    AND s.hr = 24
ORDER BY s.sofa_24hours DESC NULLS LAST;
```

## Example: Delta-SOFA (Change Over Time)

```sql
WITH sofa_change AS (
    SELECT
        stay_id,
        sofa_24hours AS sofa_day1,
        LEAD(sofa_24hours, 24) OVER (
            PARTITION BY stay_id ORDER BY hr
        ) AS sofa_day2
    FROM mimiciv_derived.sofa
    WHERE hr = 24 OR hr = 48
)
SELECT
    stay_id,
    sofa_day1,
    sofa_day2,
    sofa_day2 - sofa_day1 AS delta_sofa
FROM sofa_change
WHERE sofa_day2 IS NOT NULL;
```

## References

- Vincent JL et al. "The SOFA (Sepsis-related Organ Failure Assessment) score to describe organ dysfunction/failure." Intensive Care Medicine. 1996;24(7):707-710.
- Singer M et al. "The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3)." JAMA. 2016;315(8):801-810.
