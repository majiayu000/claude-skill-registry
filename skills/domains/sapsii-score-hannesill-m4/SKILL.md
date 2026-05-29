---
name: sapsii-score
description: Calculate SAPS-II (Simplified Acute Physiology Score II) for ICU patients in MIMIC-IV. Use for mortality prediction, severity assessment, or international ICU benchmarking.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: severity-scores
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/score
  validated: true
---

# SAPS-II Score Calculation

The Simplified Acute Physiology Score II (SAPS-II) is a widely used severity scoring system developed from a European/North American multicenter study. Calculated on the first day of ICU stay.

## When to Use This Skill

- Hospital mortality prediction
- Severity stratification
- International benchmarking (widely used in European ICUs)
- Research cohort matching
- Quality improvement initiatives

## Score Components (First 24 Hours)

| Variable | Scoring Range | Points |
|----------|---------------|--------|
| Age | <40 to >=80 | 0-18 |
| Heart Rate | <40 to >=160 | 0-11 |
| Systolic BP | <70 to >=200 | 0-13 |
| Temperature | <39 or >=39C | 0-3 |
| PaO2/FiO2 (if ventilated) | <100 to >=200 | 6-11 |
| Urine Output | <500 to >=1000 mL/day | 0-11 |
| BUN | <28 to >=84 mg/dL | 0-10 |
| WBC | <1 to >=20 x10^9/L | 0-12 |
| Potassium | <3 or >=5 mEq/L | 0-3 |
| Sodium | <125 or >=145 mEq/L | 0-5 |
| Bicarbonate | <15 to >=20 mEq/L | 0-6 |
| Bilirubin | <4 to >=6 mg/dL | 0-9 |
| GCS | <6 to >=14 | 0-26 |
| Chronic Disease | AIDS/Hematologic Malignancy/Metastatic Cancer | 9-17 |
| Admission Type | Scheduled Surgical/Medical/Unscheduled Surgical | 0-8 |

## Pre-computed Table

```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    starttime,
    endtime,
    sapsii,
    sapsii_prob,  -- Predicted hospital mortality
    age_score,
    hr_score,
    sysbp_score,
    temp_score,
    pao2fio2_score,
    uo_score,
    bun_score,
    wbc_score,
    potassium_score,
    sodium_score,
    bicarbonate_score,
    bilirubin_score,
    gcs_score,
    comorbidity_score,
    admissiontype_score
FROM mimiciv_derived.sapsii;
```

## Critical Implementation Notes

1. **PaO2/FiO2 Scoring**: Only scored for patients on mechanical ventilation OR CPAP/BiPAP. Non-ventilated patients get 0 points for this component.

2. **Comorbidity Definitions** (ICD-based):
   - **AIDS**: ICD-9 042-044, ICD-10 B20-B22, B24
   - **Hematologic Malignancy**: ICD-9 200xx-208xx, ICD-10 C81-C96
   - **Metastatic Cancer**: ICD-9 196x-199x, ICD-10 C77-C79, C800

3. **Admission Type Classification**:
   - **Scheduled Surgical**: Elective admission + surgical service
   - **Unscheduled Surgical**: Non-elective + surgical service
   - **Medical**: All others

4. **GCS Handling**: GCS < 3 is treated as null (erroneous or tracheostomy). Sedated patients should use pre-sedation GCS.

5. **Mortality Probability**: Calculated using:
   ```
   sapsii_prob = 1 / (1 + exp(-(-7.7631 + 0.0737*sapsii + 0.9971*ln(sapsii+1))))
   ```

6. **Time Window**: Uses data from ICU admission to 24 hours after.

## Example: Severity Distribution

```sql
SELECT
    CASE
        WHEN sapsii < 25 THEN 'Low (<25)'
        WHEN sapsii < 50 THEN 'Moderate (25-49)'
        WHEN sapsii < 75 THEN 'High (50-74)'
        ELSE 'Very High (>=75)'
    END AS severity_category,
    COUNT(*) AS n_patients,
    ROUND(AVG(sapsii_prob), 3) AS avg_predicted_mortality
FROM mimiciv_derived.sapsii
GROUP BY 1
ORDER BY 1;
```

## Example: Component Analysis

```sql
-- Which components contribute most to high SAPS-II?
SELECT
    'Age' AS component, AVG(age_score) AS avg_score FROM mimiciv_derived.sapsii WHERE sapsii >= 50
UNION ALL
SELECT 'Heart Rate', AVG(hr_score) FROM mimiciv_derived.sapsii WHERE sapsii >= 50
UNION ALL
SELECT 'Systolic BP', AVG(sysbp_score) FROM mimiciv_derived.sapsii WHERE sapsii >= 50
UNION ALL
SELECT 'GCS', AVG(gcs_score) FROM mimiciv_derived.sapsii WHERE sapsii >= 50
UNION ALL
SELECT 'Comorbidity', AVG(comorbidity_score) FROM mimiciv_derived.sapsii WHERE sapsii >= 50
ORDER BY avg_score DESC;
```

## References

- Le Gall JR, Lemeshow S, Saulnier F. "A new Simplified Acute Physiology Score (SAPS II) based on a European/North American multicenter study." JAMA. 1993;270(24):2957-2963.
