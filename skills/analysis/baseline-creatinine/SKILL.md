---
name: baseline-creatinine
description: Estimate baseline serum creatinine for AKI assessment in MIMIC-IV. Use for KDIGO staging, AKI research, or renal function baseline establishment.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: derived-concepts
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/measurement
  validated: true
---

# Baseline Creatinine Estimation

Estimates the patient's baseline (pre-illness) serum creatinine, which is critical for accurate AKI staging. The true baseline is often unknown; this query uses a hierarchical approach.

## When to Use This Skill

- KDIGO AKI staging (requires baseline comparison)
- AKI research cohorts
- Chronic kidney disease identification
- Renal function trajectory analysis

## Baseline Determination Rules

The baseline creatinine is determined hierarchically:

1. **If lowest admission creatinine <= 1.1 mg/dL**: Use the lowest value (assumed normal)
2. **If patient has CKD diagnosis**: Use the lowest admission value (even if elevated)
3. **Otherwise**: Estimate baseline using MDRD equation assuming GFR = 75 mL/min/1.73m^2

## Pre-computed Table

```sql
SELECT
    hadm_id,
    gender,
    age,
    scr_min,      -- Lowest creatinine during admission
    ckd,          -- 1 if CKD diagnosis present
    mdrd_est,     -- Estimated creatinine from MDRD
    scr_baseline  -- Final baseline determination
FROM mimiciv_derived.creatinine_baseline;
```

## MDRD Estimation Formula

For patients without normal creatinine and without CKD, baseline is estimated:

**Male patients:**
```
scr_baseline = (75 / 186 / age^(-0.203))^(-1/1.154)
```

**Female patients:**
```
scr_baseline = (75 / 186 / age^(-0.203) / 0.742)^(-1/1.154)
```

This back-calculates creatinine assuming eGFR = 75 mL/min/1.73m^2 (lower limit of normal).

## CKD Identification

CKD is identified from ICD codes:
- **ICD-9**: 585 (Chronic kidney disease)
- **ICD-10**: N18 (Chronic kidney disease)

## Critical Implementation Notes

1. **Adults Only**: Query filters to age >= 18 (pediatric creatinine norms differ).

2. **MDRD Limitations**:
   - Less accurate in elderly, extremes of body size, or certain ethnicities
   - Assumes GFR = 75, which may underestimate for young healthy patients

3. **Admission Bias**: Using admission creatinine as baseline may underestimate for patients admitted already in AKI (AKI-on-admission).

4. **CKD May Be Coded Late**: ICD codes are assigned at discharge, so this technically uses future information. In most research this is acceptable.

5. **Missing Values**: If no creatinine measured during admission, baseline will be NULL.

6. **Race Coefficient**: The original MDRD had a race coefficient; this implementation does not use it, consistent with recent guidelines removing race from eGFR calculations.

## Example: Baseline Distribution

```sql
SELECT
    CASE
        WHEN scr_min <= 1.1 THEN 'Normal admission Cr'
        WHEN ckd = 1 THEN 'CKD (using min)'
        ELSE 'MDRD estimated'
    END AS baseline_source,
    COUNT(*) AS n_admissions,
    ROUND(AVG(scr_baseline), 2) AS avg_baseline
FROM mimiciv_derived.creatinine_baseline
GROUP BY 1;
```

## Example: Compare Baseline vs Admission Creatinine

```sql
SELECT
    cb.hadm_id,
    cb.scr_baseline,
    cb.scr_min AS admission_min_cr,
    ROUND(cb.scr_min / NULLIF(cb.scr_baseline, 0), 2) AS cr_ratio,
    CASE
        WHEN cb.scr_min >= cb.scr_baseline * 1.5 THEN 'AKI Stage 1+'
        ELSE 'No AKI at admission'
    END AS admission_aki_status
FROM mimiciv_derived.creatinine_baseline cb
WHERE cb.scr_baseline IS NOT NULL;
```

## Example: Age-Stratified Estimated Baselines

```sql
SELECT
    CASE
        WHEN age < 40 THEN '<40'
        WHEN age < 60 THEN '40-59'
        WHEN age < 80 THEN '60-79'
        ELSE '80+'
    END AS age_group,
    gender,
    ROUND(AVG(mdrd_est), 2) AS avg_mdrd_baseline
FROM mimiciv_derived.creatinine_baseline
WHERE ckd = 0 AND scr_min > 1.1
GROUP BY 1, 2
ORDER BY 1, 2;
```

## Alternative Baseline Methods

Other approaches used in literature (not implemented here):
1. **Outpatient creatinine**: Use pre-admission ambulatory values (requires linked outpatient data)
2. **Rolling minimum**: Lowest value in past 7-365 days
3. **First available**: First creatinine of admission (problematic if AKI present)
4. **Fixed MDRD**: Always use MDRD with assumed GFR (consistent but may miss true normal)

## References

- KDIGO Clinical Practice Guideline for Acute Kidney Injury. Kidney International Supplements. 2012.
- Siew ED et al. "Estimating baseline kidney function in hospitalized patients with impaired kidney function." Clinical Journal of the American Society of Nephrology. 2012;7(5):712-719.
