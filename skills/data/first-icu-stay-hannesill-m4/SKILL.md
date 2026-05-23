---
name: first-icu-stay
description: Identify first ICU stays and first hospital admissions in MIMIC-IV for cohort selection. Use to exclude readmissions, create independent observations, or build adult patient cohorts.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: cohort-definitions
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/demographics
  validated: true
---

# First ICU Stay Selection

Identifies first ICU stays and hospital admissions for cohort construction. Critical for avoiding correlated observations and inflated sample sizes from readmissions.

## When to Use This Skill

- Creating research cohorts with independent observations
- Excluding readmissions that may have different characteristics
- Selecting incident (first-time) ICU patients
- Matching cohorts by admission characteristics

## Pre-computed Table

```sql
SELECT
    subject_id,
    hadm_id,
    stay_id,
    -- Demographics
    gender,
    dod,  -- Date of death (if applicable)
    -- Hospital admission
    admittime,
    dischtime,
    los_hospital,  -- Hospital length of stay (days)
    admission_age,
    race,
    hospital_expire_flag,
    hospstay_seq,       -- Hospital admission sequence number
    first_hosp_stay,    -- TRUE if first hospitalization
    -- ICU stay
    icu_intime,
    icu_outtime,
    los_icu,            -- ICU length of stay (days)
    icustay_seq,        -- ICU stay sequence within hospitalization
    first_icu_stay      -- TRUE if first ICU stay of this hospitalization
FROM mimiciv_derived.icustay_detail;
```

## Key Columns Explained

### Hospital-Level
- `hospstay_seq`: Order of hospital admission for this patient (1 = first ever)
- `first_hosp_stay`: TRUE if this is the patient's first hospital admission

### ICU-Level (Within Hospitalization)
- `icustay_seq`: Order of ICU stays within this hospitalization (1 = first ICU stay)
- `first_icu_stay`: TRUE if this is the first ICU stay of the current hospitalization

## Age Calculation

Age is calculated as:
```sql
anchor_age + (YEAR(admittime) - anchor_year)
```

**Important**: MIMIC-IV shifts ages for patients > 89 years old at any admission. These patients have `anchor_age = 91` and ages are not exact.

## Common Cohort Selection Patterns

### First ICU Stay Only (Most Common)
```sql
SELECT *
FROM mimiciv_derived.icustay_detail
WHERE first_icu_stay = TRUE;
```

### First-Ever ICU Stay (Strictest)
```sql
SELECT *
FROM mimiciv_derived.icustay_detail
WHERE first_hosp_stay = TRUE
    AND first_icu_stay = TRUE;
```

### Adult Patients Only
```sql
SELECT *
FROM mimiciv_derived.icustay_detail
WHERE admission_age >= 18
    AND first_icu_stay = TRUE;
```

### Exclude Very Short Stays
```sql
SELECT *
FROM mimiciv_derived.icustay_detail
WHERE first_icu_stay = TRUE
    AND los_icu >= 1  -- At least 24 hours in ICU
    AND los_hospital >= 1;
```

## Critical Implementation Notes

1. **Multiple ICU Stays**: One hospitalization can have multiple ICU stays. `first_icu_stay` identifies the first ICU stay within each hospitalization.

2. **Patient-Level vs Stay-Level**: Choose the right level of independence:
   - `first_hosp_stay = TRUE AND first_icu_stay = TRUE`: Most independent
   - `first_icu_stay = TRUE`: Independent within each hospitalization
   - All stays: May have correlated outcomes

3. **Age Shifting**: Ages > 89 are shifted to protect privacy. Anchor age is 91, actual age is approximated.

4. **Mortality Flags**:
   - `hospital_expire_flag`: Died during this hospitalization
   - `dod`: Date of death (may be after discharge)

5. **LOS Calculations**:
   - `los_hospital`: Days from admission to discharge
   - `los_icu`: Days from ICU admission to ICU discharge

## Example: Standard Adult Cohort

```sql
SELECT
    stay_id,
    subject_id,
    hadm_id,
    admission_age,
    gender,
    los_icu,
    hospital_expire_flag
FROM mimiciv_derived.icustay_detail
WHERE first_icu_stay = TRUE
    AND admission_age >= 18
    AND admission_age < 90  -- Exclude age-shifted patients
    AND los_icu >= 1;
```

## Example: Readmission Analysis

```sql
-- Patients with multiple ICU stays in same hospitalization
SELECT
    hadm_id,
    COUNT(*) AS n_icu_stays
FROM mimiciv_derived.icustay_detail
GROUP BY hadm_id
HAVING COUNT(*) > 1;

-- Compare first vs subsequent stays
SELECT
    first_icu_stay,
    COUNT(*) AS n_stays,
    ROUND(AVG(los_icu), 1) AS avg_los,
    ROUND(AVG(hospital_expire_flag), 3) AS mortality
FROM mimiciv_derived.icustay_detail
GROUP BY first_icu_stay;
```

## Example: Age Distribution

```sql
SELECT
    CASE
        WHEN admission_age < 40 THEN '<40'
        WHEN admission_age < 60 THEN '40-59'
        WHEN admission_age < 80 THEN '60-79'
        WHEN admission_age < 90 THEN '80-89'
        ELSE '90+'
    END AS age_group,
    COUNT(*) AS n_patients
FROM mimiciv_derived.icustay_detail
WHERE first_icu_stay = TRUE
GROUP BY 1
ORDER BY 1;
```

## Related Exclusion Criteria

Common additional exclusions for research cohorts:
- Comfort care / DNR orders (see `mimiciv_derived.code_status`)
- Organ donors
- Very short stays (< 4-24 hours)
- Missing key data elements
- Specific diagnoses (trauma, cardiac surgery, etc.)

## References

- Johnson AEW et al. "MIMIC-IV, a freely accessible electronic health record dataset." Scientific Data. 2023.
