---
name: vasopressor-equivalents
description: Calculate norepinephrine-equivalent dose for vasopressor comparison in MIMIC-IV. Use for hemodynamic support quantification, shock severity assessment, or vasopressor weaning studies.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: derived-concepts
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/medication
  validated: true
---

# Vasopressor Equivalent Dose

Calculates norepinephrine-equivalent dose (NED) to enable comparison across different vasopressor agents. Based on the Goradia et al. 2020 scoping review of vasopressor dose equivalence.

## When to Use This Skill

- Comparing vasopressor exposure across different agents
- Shock severity quantification
- Vasopressor weaning studies
- Hemodynamic support burden calculation
- Cardiovascular SOFA component (uses vasopressor doses)

## Equivalence Factors

| Vasopressor | Equivalence Ratio | Comparison Dose | Units |
|-------------|------------------|-----------------|-------|
| Norepinephrine | 1:1 | 0.1 | mcg/kg/min |
| Epinephrine | 1:1 | 0.1 | mcg/kg/min |
| Dopamine | 1:100 | 10 | mcg/kg/min |
| Phenylephrine | 1:10 | 1 | mcg/kg/min |
| Vasopressin | 1:0.4* | 0.04 | units/min |

*Vasopressin is converted: `vasopressin_units_per_hr * 2.5 / 60`

## Pre-computed Table

```sql
SELECT
    stay_id,
    starttime,
    endtime,
    norepinephrine_equivalent_dose
FROM mimiciv_derived.norepinephrine_equivalent_dose;
```

## Calculation Formula

```sql
norepinephrine_equivalent_dose = ROUND(
    COALESCE(norepinephrine, 0)
    + COALESCE(epinephrine, 0)
    + COALESCE(phenylephrine / 10, 0)
    + COALESCE(dopamine / 100, 0)
    + COALESCE(vasopressin * 2.5 / 60, 0),
    4
)
```

## Source Tables

Individual vasopressor tables provide dose rates:
- `mimiciv_derived.norepinephrine`
- `mimiciv_derived.epinephrine`
- `mimiciv_derived.dopamine`
- `mimiciv_derived.phenylephrine`
- `mimiciv_derived.vasopressin`

All consolidated in:
- `mimiciv_derived.vasoactive_agent`

## Critical Implementation Notes

1. **Weight-Based Dosing**: All doses are in mcg/kg/min (except vasopressin in units/hr). The underlying tables use patient weight for conversion.

2. **Weight Estimation**: When weight is not documented, it may be estimated. Check `mimiciv_derived.weight_durations` for weight source.

3. **Vasopressin Units**: Vasopressin is charted in units/hour, not units/min. The formula converts appropriately.

4. **Excluded Agents**:
   - Metaraminol: Not used at BIDMC
   - Angiotensin II: Rarely used (could add: angiotensin_ii * 10)
   - Dobutamine: Not a vasopressor (inotrope), excluded from NED

5. **Time Intervals**: Each row has a starttime/endtime representing when that dose was active.

6. **Multiple Simultaneous Agents**: NED sums all concurrent vasopressors.

## Example: Maximum NED Per ICU Stay

```sql
SELECT
    stay_id,
    MAX(norepinephrine_equivalent_dose) AS max_ned
FROM mimiciv_derived.norepinephrine_equivalent_dose
GROUP BY stay_id
ORDER BY max_ned DESC;
```

## Example: Vasopressor Duration

```sql
SELECT
    stay_id,
    SUM(TIMESTAMP_DIFF(endtime, starttime, HOUR)) AS vasopressor_hours
FROM mimiciv_derived.norepinephrine_equivalent_dose
WHERE norepinephrine_equivalent_dose > 0
GROUP BY stay_id;
```

## Example: Time-Weighted Average NED

```sql
WITH weighted AS (
    SELECT
        stay_id,
        norepinephrine_equivalent_dose *
        TIMESTAMP_DIFF(endtime, starttime, MINUTE) AS dose_minutes,
        TIMESTAMP_DIFF(endtime, starttime, MINUTE) AS duration_minutes
    FROM mimiciv_derived.norepinephrine_equivalent_dose
)
SELECT
    stay_id,
    SUM(dose_minutes) / NULLIF(SUM(duration_minutes), 0) AS time_weighted_ned
FROM weighted
GROUP BY stay_id;
```

## Example: Shock Severity Categories

```sql
WITH max_ned AS (
    SELECT
        stay_id,
        MAX(norepinephrine_equivalent_dose) AS max_ned
    FROM mimiciv_derived.norepinephrine_equivalent_dose
    GROUP BY stay_id
)
SELECT
    CASE
        WHEN max_ned = 0 THEN 'No vasopressors'
        WHEN max_ned < 0.1 THEN 'Low dose (<0.1)'
        WHEN max_ned < 0.3 THEN 'Moderate (0.1-0.3)'
        WHEN max_ned < 0.5 THEN 'High (0.3-0.5)'
        ELSE 'Very high (>=0.5)'
    END AS vasopressor_category,
    COUNT(*) AS n_stays
FROM max_ned
GROUP BY 1
ORDER BY 1;
```

## References

- Goradia S et al. "Vasopressor dose equivalence: A scoping review and suggested formula." Journal of Critical Care. 2020;61:233-240.
- Brown SM et al. "Survival after shock requiring high-dose vasopressor therapy." Chest. 2013;143(3):664-671.
