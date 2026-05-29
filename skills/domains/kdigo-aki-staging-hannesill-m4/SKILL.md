---
name: kdigo-aki-staging
description: Calculate KDIGO AKI (Acute Kidney Injury) staging for ICU patients in MIMIC-IV using creatinine and urine output criteria. Use for nephrology research, AKI outcome studies, or renal function monitoring.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: organ-failure
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/organfailure
  validated: true
---

# KDIGO AKI Staging

The Kidney Disease: Improving Global Outcomes (KDIGO) criteria define Acute Kidney Injury (AKI) stages based on serum creatinine changes and/or urine output reduction.

## When to Use This Skill

- AKI incidence and outcome studies
- Renal function trajectory analysis
- CRRT initiation studies
- Drug-induced nephrotoxicity research
- ICU quality metrics

## AKI Staging Criteria

### Creatinine-Based Criteria
| Stage | Creatinine Criterion |
|-------|---------------------|
| 1 | >= 1.5x baseline within 7 days OR >= 0.3 mg/dL increase within 48h |
| 2 | >= 2.0x baseline |
| 3 | >= 3.0x baseline OR >= 4.0 mg/dL with acute increase OR RRT initiation |

### Urine Output-Based Criteria
| Stage | Urine Output Criterion |
|-------|----------------------|
| 1 | < 0.5 mL/kg/h for 6-12 hours |
| 2 | < 0.5 mL/kg/h for >= 12 hours |
| 3 | < 0.3 mL/kg/h for >= 24 hours OR anuria for >= 12 hours |

**Final AKI Stage** = MAX(creatinine stage, urine output stage, CRRT stage)

## Pre-computed Tables

### KDIGO Stages (Combined)
```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    charttime,
    -- Creatinine criteria
    creat_low_past_7day,
    creat_low_past_48hr,
    creat,
    aki_stage_creat,
    -- Urine output criteria
    uo_rt_6hr,
    uo_rt_12hr,
    uo_rt_24hr,
    aki_stage_uo,
    -- CRRT
    aki_stage_crrt,
    -- Final stage
    aki_stage,
    aki_stage_smoothed  -- Smoothed over 6-hour window
FROM mimiciv_derived.kdigo_stages;
```

### Creatinine with Baseline
```sql
SELECT
    hadm_id,
    charttime,
    creat,
    creat_low_past_7day,
    creat_low_past_48hr
FROM mimiciv_derived.kdigo_creatinine;
```

### Urine Output Rates
```sql
SELECT
    stay_id,
    charttime,
    weight,
    uo_rt_6hr,   -- mL/kg/h over 6 hours
    uo_rt_12hr,  -- mL/kg/h over 12 hours
    uo_rt_24hr   -- mL/kg/h over 24 hours
FROM mimiciv_derived.kdigo_uo;
```

## Critical Implementation Notes

1. **Baseline Creatinine**: Uses the lowest creatinine in the past 7 days as the baseline. This may underestimate AKI if patient was already in AKI on admission.

2. **48-Hour Window**: The >= 0.3 mg/dL acute increase criterion uses the lowest creatinine in the past 48 hours specifically.

3. **Stage 3 with Cr >= 4.0**: Requires EITHER:
   - An acute increase >= 0.3 mg/dL within 48h, OR
   - An increase >= 1.5x baseline

4. **Urine Output Timing**: UO criteria require the patient to be in ICU for at least 6 hours before staging (KDIGO definition). Earlier times get stage 0.

5. **Weight for UO Calculation**: Uses documented weight from `mimiciv_derived.kdigo_uo`. Weight estimation methods vary.

6. **CRRT as Stage 3**: Any patient on CRRT is automatically Stage 3 AKI.

7. **Smoothed Stage**: `aki_stage_smoothed` carries forward the maximum stage from the past 6 hours to reduce fluctuation between creatinine/UO measurements.

8. **Time Series Data**: AKI is calculated at every creatinine/UO measurement time, not just once per admission.

## Example: AKI Incidence

```sql
WITH max_aki AS (
    SELECT
        stay_id,
        MAX(aki_stage) AS max_aki_stage
    FROM mimiciv_derived.kdigo_stages
    GROUP BY stay_id
)
SELECT
    max_aki_stage,
    COUNT(*) AS n_stays,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
FROM max_aki
GROUP BY max_aki_stage
ORDER BY max_aki_stage;
```

## Example: AKI by Criteria Type

```sql
WITH aki_type AS (
    SELECT
        stay_id,
        MAX(aki_stage_creat) AS max_cr_stage,
        MAX(aki_stage_uo) AS max_uo_stage,
        MAX(COALESCE(aki_stage_crrt, 0)) AS max_crrt_stage
    FROM mimiciv_derived.kdigo_stages
    GROUP BY stay_id
)
SELECT
    CASE
        WHEN max_cr_stage > 0 AND max_uo_stage > 0 THEN 'Both Cr and UO'
        WHEN max_cr_stage > 0 THEN 'Cr only'
        WHEN max_uo_stage > 0 THEN 'UO only'
        WHEN max_crrt_stage > 0 THEN 'CRRT only'
        ELSE 'No AKI'
    END AS aki_type,
    COUNT(*) AS n_stays
FROM aki_type
GROUP BY 1;
```

## Example: Time to AKI Development

```sql
WITH first_aki AS (
    SELECT
        k.stay_id,
        MIN(k.charttime) AS first_aki_time
    FROM mimiciv_derived.kdigo_stages k
    WHERE k.aki_stage >= 1
    GROUP BY k.stay_id
)
SELECT
    ROUND(
        TIMESTAMP_DIFF(f.first_aki_time, ie.intime, HOUR), 0
    ) AS hours_to_aki,
    COUNT(*) AS n_stays
FROM first_aki f
INNER JOIN mimiciv_icu.icustays ie ON f.stay_id = ie.stay_id
GROUP BY 1
HAVING hours_to_aki BETWEEN 0 AND 168  -- First week
ORDER BY 1;
```

## Example: AKI Stage Transitions

```sql
WITH aki_trajectory AS (
    SELECT
        stay_id,
        charttime,
        aki_stage,
        LAG(aki_stage) OVER (PARTITION BY stay_id ORDER BY charttime) AS prev_stage
    FROM mimiciv_derived.kdigo_stages
    WHERE aki_stage IS NOT NULL
)
SELECT
    prev_stage AS from_stage,
    aki_stage AS to_stage,
    COUNT(*) AS n_transitions
FROM aki_trajectory
WHERE prev_stage IS NOT NULL
    AND prev_stage != aki_stage
GROUP BY 1, 2
ORDER BY 1, 2;
```

## References

- KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney International Supplements. 2012;2(1):1-138.
- Kellum JA, Lameire N. "Diagnosis, evaluation, and management of acute kidney injury: a KDIGO summary." Critical Care. 2013;17(1):204.
