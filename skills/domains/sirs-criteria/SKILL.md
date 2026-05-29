---
name: sirs-criteria
description: Calculate SIRS (Systemic Inflammatory Response Syndrome) criteria for ICU patients in MIMIC-IV. Use for historical sepsis definitions, inflammatory response assessment, or research comparing SIRS vs Sepsis-3.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: severity-scores
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/score
  validated: true
---

# SIRS Criteria Calculation

The Systemic Inflammatory Response Syndrome (SIRS) criteria quantify the inflammatory response. Historically used for sepsis definition (SIRS >= 2 + suspected infection), now largely replaced by Sepsis-3 but still relevant for research and comparison.

## When to Use This Skill

- Historical sepsis research (pre-Sepsis-3 definitions)
- Inflammatory response quantification
- Comparing SIRS vs Sepsis-3 criteria
- Identifying patients with systemic inflammation
- Quality metrics using legacy definitions

## SIRS Criteria (0-4 Points)

Each criterion met = 1 point:

| Criterion | Threshold |
|-----------|-----------|
| **Temperature** | < 36C OR > 38C |
| **Heart Rate** | > 90 bpm |
| **Respiratory** | RR > 20/min OR PaCO2 < 32 mmHg |
| **WBC** | < 4 OR > 12 x10^9/L OR > 10% bands |

**SIRS Positive**: >= 2 criteria met

## Pre-computed Table

```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    sirs,
    temp_score,
    heart_rate_score,
    resp_score,
    wbc_score
FROM mimiciv_derived.sirs;
```

## Component Details

### Temperature
- Uses min and max from first 24 hours
- Score = 1 if temp_min < 36C OR temp_max > 38C

### Heart Rate
- Uses max from first 24 hours
- Score = 1 if heart_rate_max > 90

### Respiratory
- Uses RR max OR PaCO2 min (arterial)
- Score = 1 if resp_rate_max > 20 OR paco2_min < 32

### White Blood Cell Count
- Uses min, max, and bands from first 24 hours
- Score = 1 if wbc_min < 4 OR wbc_max > 12 OR bands_max > 10%

## Critical Implementation Notes

1. **Band Forms**: The presence of > 10% immature neutrophils (bands) counts as the WBC criterion, even if total WBC is normal.

2. **Arterial Blood Gas**: PaCO2 uses only arterial specimens from `first_day_bg_art` table.

3. **Missing Data**: Missing components imputed as 0 (normal). This may underestimate true SIRS.

4. **First Day Only**: Calculated using first 24 hours of ICU stay data.

5. **SIRS vs Sepsis-3**:
   - SIRS >= 2 + suspected infection = old sepsis definition
   - Sepsis-3 uses SOFA >= 2 + suspected infection
   - SIRS is more sensitive but less specific for mortality

## Example: SIRS Distribution

```sql
SELECT
    sirs,
    COUNT(*) AS n_patients,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct
FROM mimiciv_derived.sirs
GROUP BY sirs
ORDER BY sirs;
```

## Example: Compare SIRS vs Sepsis-3 Sensitivity

```sql
WITH classifications AS (
    SELECT
        si.stay_id,
        si.sirs >= 2 AS sirs_positive,
        s3.sepsis3
    FROM mimiciv_derived.sirs si
    LEFT JOIN mimiciv_derived.sepsis3 s3
        ON si.stay_id = s3.stay_id
    WHERE s3.stay_id IS NOT NULL  -- has suspected infection
)
SELECT
    sirs_positive,
    sepsis3,
    COUNT(*) AS n
FROM classifications
GROUP BY sirs_positive, sepsis3
ORDER BY 1, 2;
```

## Example: SIRS Components in Septic Patients

```sql
SELECT
    'Temperature' AS component,
    ROUND(AVG(temp_score), 2) AS prevalence
FROM mimiciv_derived.sirs si
INNER JOIN mimiciv_derived.sepsis3 s3 ON si.stay_id = s3.stay_id
WHERE s3.sepsis3 = TRUE
UNION ALL
SELECT 'Heart Rate', ROUND(AVG(heart_rate_score), 2)
FROM mimiciv_derived.sirs si
INNER JOIN mimiciv_derived.sepsis3 s3 ON si.stay_id = s3.stay_id
WHERE s3.sepsis3 = TRUE
UNION ALL
SELECT 'Respiratory', ROUND(AVG(resp_score), 2)
FROM mimiciv_derived.sirs si
INNER JOIN mimiciv_derived.sepsis3 s3 ON si.stay_id = s3.stay_id
WHERE s3.sepsis3 = TRUE
UNION ALL
SELECT 'WBC', ROUND(AVG(wbc_score), 2)
FROM mimiciv_derived.sirs si
INNER JOIN mimiciv_derived.sepsis3 s3 ON si.stay_id = s3.stay_id
WHERE s3.sepsis3 = TRUE;
```

## Limitations

1. **Low Specificity**: Many non-infectious conditions trigger SIRS (trauma, surgery, pancreatitis)
2. **Sensitivity Issues**: Can miss infected patients who don't mount inflammatory response
3. **Replaced by Sepsis-3**: Current guidelines use SOFA-based Sepsis-3 criteria

## References

- Bone RC et al. "Definitions for sepsis and organ failure and guidelines for the use of innovative therapies in sepsis." Chest. 1992;101(6):1644-1655.
- American College of Chest Physicians/SCCM Consensus Conference. Critical Care Medicine. 1992;20(6):864-874.
