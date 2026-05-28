---
name: lods-score
description: Calculate LODS (Logistic Organ Dysfunction Score) for ICU patients in MIMIC-IV. Use for organ dysfunction assessment across 6 systems with weighted scoring.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: severity-scores
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/score
  validated: true
---

# LODS Score Calculation

The Logistic Organ Dysfunction Score (LODS) assesses organ dysfunction across 6 systems with logistic regression-derived weights. It provides mortality prediction based on the first ICU day.

## When to Use This Skill

- Multi-organ dysfunction assessment
- Mortality prediction with organ-specific weighting
- Research on organ failure patterns
- Alternative to SOFA for organ dysfunction quantification

## Score Components (First 24 Hours)

| System | Variables | Score Range |
|--------|-----------|-------------|
| **Neurologic** | GCS | 0-5 |
| **Cardiovascular** | HR, SBP | 0-5 |
| **Renal** | BUN, Creatinine, Urine Output | 0-5 |
| **Pulmonary** | PaO2/FiO2 (ventilated only) | 0-3 |
| **Hematologic** | WBC, Platelets | 0-3 |
| **Hepatic** | PT, Bilirubin | 0-1 |

**Total Range**: 0-22

## Pre-computed Table

```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    lods,
    neurologic,
    cardiovascular,
    renal,
    pulmonary,
    hematologic,
    hepatic
FROM mimiciv_derived.lods;
```

## Component Scoring Details

### Neurologic (GCS)
| GCS | Score |
|-----|-------|
| <= 5 | 5 |
| 6-8 | 3 |
| 9-13 | 1 |
| 14-15 | 0 |

### Cardiovascular
| Condition | Score |
|-----------|-------|
| HR < 30 OR SBP < 40 | 5 |
| SBP < 70 OR SBP >= 270 | 3 |
| HR >= 140 OR SBP >= 240 OR SBP < 90 | 1 |
| Normal | 0 |

### Renal
| Condition | Score |
|-----------|-------|
| UO < 500 OR BUN >= 56 | 5 |
| Cr >= 1.6 OR UO < 750 OR BUN >= 28 OR UO >= 10000 | 3 |
| Cr >= 1.2 OR BUN >= 7.5 | 1 |
| Normal | 0 |

### Pulmonary (Ventilated Patients Only)
| PaO2/FiO2 | Score |
|-----------|-------|
| < 150 | 3 |
| >= 150 | 1 |
| Not ventilated | 0 |

### Hematologic
| Condition | Score |
|-----------|-------|
| WBC < 1.0 | 3 |
| WBC < 2.5 OR Platelets < 50 OR WBC >= 50 | 1 |
| Normal | 0 |

### Hepatic
| Condition | Score |
|-----------|-------|
| Bilirubin >= 2.0 OR PT > 15s OR PT < 3s | 1 |
| Normal | 0 |

## Critical Implementation Notes

1. **Prothrombin Time (PT)**: The "standard" PT is assumed to be 12 seconds. Abnormal is > 15s (12 + 3) or < 3s (12 * 0.25).

2. **Pulmonary Scoring**: Only scored for patients on mechanical ventilation or CPAP. Non-ventilated patients get 0.

3. **CPAP Detection**: Identified from oxygen delivery device documentation containing "cpap" or "bipap mask".

4. **GCS < 3**: Treated as null (erroneous value or tracheostomy).

5. **Missing Data**: Missing components are imputed as 0 (normal).

## Example: Organ Dysfunction Profile

```sql
SELECT
    stay_id,
    lods,
    neurologic,
    cardiovascular,
    renal,
    pulmonary,
    hematologic,
    hepatic,
    CASE WHEN neurologic > 0 THEN 1 ELSE 0 END +
    CASE WHEN cardiovascular > 0 THEN 1 ELSE 0 END +
    CASE WHEN renal > 0 THEN 1 ELSE 0 END +
    CASE WHEN pulmonary > 0 THEN 1 ELSE 0 END +
    CASE WHEN hematologic > 0 THEN 1 ELSE 0 END +
    CASE WHEN hepatic > 0 THEN 1 ELSE 0 END AS n_failing_organs
FROM mimiciv_derived.lods
ORDER BY lods DESC;
```

## Example: Multi-Organ Failure Analysis

```sql
-- Patients with >= 3 organ systems failing
SELECT
    l.stay_id,
    l.lods,
    adm.hospital_expire_flag AS mortality
FROM mimiciv_derived.lods l
INNER JOIN mimiciv_icu.icustays ie ON l.stay_id = ie.stay_id
INNER JOIN mimiciv_hosp.admissions adm ON ie.hadm_id = adm.hadm_id
WHERE
    (CASE WHEN neurologic > 0 THEN 1 ELSE 0 END +
     CASE WHEN cardiovascular > 0 THEN 1 ELSE 0 END +
     CASE WHEN renal > 0 THEN 1 ELSE 0 END +
     CASE WHEN pulmonary > 0 THEN 1 ELSE 0 END +
     CASE WHEN hematologic > 0 THEN 1 ELSE 0 END +
     CASE WHEN hepatic > 0 THEN 1 ELSE 0 END) >= 3;
```

## References

- Le Gall JR et al. "The Logistic Organ Dysfunction system: a new way to assess organ dysfunction in the intensive care unit." JAMA. 1996;276(10):802-810.
