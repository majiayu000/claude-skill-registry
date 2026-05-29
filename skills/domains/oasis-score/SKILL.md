---
name: oasis-score
description: Calculate OASIS (Oxford Acute Severity of Illness Score) for ICU patients in MIMIC-IV. Use for mortality prediction with fewer variables than APACHE/SAPS, or when lab data is limited.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: severity-scores
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/score
  validated: true
---

# OASIS Score Calculation

The Oxford Acute Severity of Illness Score (OASIS) is a parsimonious severity score that achieves comparable predictive accuracy to APACHE using fewer variables. It does not require laboratory values, making it useful when lab data is missing.

## When to Use This Skill

- Mortality prediction when lab data is incomplete
- Quick severity assessment with minimal variables
- Real-time severity scoring (no lab turnaround time)
- Research requiring a validated, simple severity metric
- Comparison with APACHE/SAPS scores

## Score Components (First 24 Hours)

| Variable | Range | Points |
|----------|-------|--------|
| Age | <24 to >=90 | 0-9 |
| Pre-ICU LOS | <10 min to >=18708 min | 0-5 |
| GCS | <=7 to >=15 | 0-10 |
| Heart Rate | <33 to >125 | 0-6 |
| Mean BP | <20.65 to >143.44 | 0-4 |
| Respiratory Rate | <6 to >44 | 0-10 |
| Temperature | <33.22 to >39.88 C | 0-6 |
| Urine Output | <671 to >6897 mL/day | 0-10 |
| Mechanical Ventilation | Yes/No | 0 or 9 |
| Elective Surgery | Yes/No | 0 or 6 |

**Total Range**: 0-67 (theoretical maximum)

## Pre-computed Table

```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    oasis,
    oasis_prob,  -- Predicted in-hospital mortality
    age, age_score,
    preiculos, preiculos_score,
    gcs, gcs_score,
    heartrate, heart_rate_score,
    meanbp, mbp_score,
    resprate, resp_rate_score,
    temp, temp_score,
    urineoutput, urineoutput_score,
    mechvent, mechvent_score,
    electivesurgery, electivesurgery_score
FROM mimiciv_derived.oasis;
```

## Critical Implementation Notes

1. **No Laboratory Values Required**: OASIS uses only vital signs, urine output, and administrative data - no labs needed.

2. **Pre-ICU LOS Scoring**: Time from hospital admission to ICU admission in minutes. Scoring is non-linear:
   - < 10.2 min: 5 points (immediate ICU)
   - 10.2-297 min: 3 points
   - 297-1440 min: 0 points (optimal)
   - 1440-18708 min: 2 points
   - > 18708 min: 1 point

3. **Mechanical Ventilation**: Binary flag - any invasive ventilation during first 24 hours scores 9 points.

4. **Elective Surgery**: Requires BOTH:
   - Elective admission type AND
   - Surgical service (identified from first service transfer)

5. **Ventilation Flag Cannot Be Missing**: Unlike other components, ventilation defaults to 0 (no ventilation) if no data found.

6. **Mortality Probability**:
   ```
   oasis_prob = 1 / (1 + exp(-(-6.1746 + 0.1275 * oasis)))
   ```

## Advantages Over APACHE/SAPS

- Simpler to calculate (10 variables vs 15-17)
- No laboratory data required
- Can be calculated earlier in admission
- Similar predictive accuracy

## Example: Quick Severity Assessment

```sql
SELECT
    stay_id,
    oasis,
    oasis_prob,
    CASE
        WHEN oasis < 20 THEN 'Low Risk'
        WHEN oasis < 30 THEN 'Moderate Risk'
        WHEN oasis < 40 THEN 'High Risk'
        ELSE 'Very High Risk'
    END AS risk_category
FROM mimiciv_derived.oasis
ORDER BY oasis DESC;
```

## Example: Compare OASIS vs SAPS-II Predictions

```sql
SELECT
    o.stay_id,
    o.oasis,
    o.oasis_prob AS oasis_mortality,
    s.sapsii,
    s.sapsii_prob AS sapsii_mortality,
    ABS(o.oasis_prob - s.sapsii_prob) AS prediction_difference
FROM mimiciv_derived.oasis o
INNER JOIN mimiciv_derived.sapsii s
    ON o.stay_id = s.stay_id
ORDER BY prediction_difference DESC;
```

## References

- Johnson AEW, Kramer AA, Clifford GD. "A new severity of illness scale using a subset of Acute Physiology And Chronic Health Evaluation data elements shows comparable predictive accuracy." Critical Care Medicine. 2013;41(7):1711-1718.
