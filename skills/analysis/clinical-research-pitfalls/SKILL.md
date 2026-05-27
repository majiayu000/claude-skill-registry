---
name: clinical-research-pitfalls
description: Avoid common methodological mistakes in clinical research with MIMIC-IV and eICU databases. Covers immortal time bias, information leakage, selection bias, and other critical pitfalls.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: both
  category: data-quality
  source: https://github.com/MIT-LCP/mimic-code
  validated: true
---

# Clinical Research Pitfalls

This skill documents common methodological mistakes in ICU database research and how to avoid them. These errors can invalidate study conclusions.

## When to Use This Skill

- Designing research studies
- Reviewing analysis plans
- Debugging unexpected results
- Peer review of methods

## 1. Immortal Time Bias

### Definition
Time during which the outcome cannot occur, often because the exposure has not yet been assigned or identified.

### Common Mistake
```sql
-- WRONG: Patients who "received Drug X during ICU stay"
-- Survival bias: Must survive long enough to receive the drug
SELECT stay_id
FROM mimiciv_derived.antibiotic
WHERE antibiotic LIKE '%vancomycin%';
```

### Correct Approach
```sql
-- CORRECT: Define exposure at a fixed time point (e.g., first 24h)
SELECT DISTINCT stay_id
FROM mimiciv_derived.antibiotic ab
INNER JOIN mimiciv_icu.icustays ie ON ab.stay_id = ie.stay_id
WHERE ab.starttime <= DATETIME_ADD(ie.intime, INTERVAL 24 HOUR);
```

### Key Principle
- Define exposure status at a fixed time point (e.g., ICU admission, 24 hours, 48 hours)
- Time zero should be the same for exposed and unexposed groups
- Consider landmark analysis or time-varying covariates

## 2. Information Leakage (Future Data)

### Definition
Using information that would not be available at the time of prediction/decision.

### Common Mistake
```sql
-- WRONG: Using diagnosis codes for prediction at admission
-- ICD codes are assigned at discharge!
SELECT hadm_id, icd_code
FROM mimiciv_hosp.diagnoses_icd
WHERE icd_code LIKE 'I21%';  -- MI diagnosis
```

### Correct Approach
```sql
-- CORRECT: Use chief complaint or admission diagnosis
-- Or clearly acknowledge this is retrospective phenotyping
SELECT hadm_id
FROM mimiciv_hosp.admissions
WHERE LOWER(admission_type) LIKE '%emergency%';
```

### Common Sources of Leakage
- **Diagnosis codes**: Assigned at discharge
- **Procedure codes**: May be coded after completion
- **Length of stay**: Only known at discharge
- **Discharge disposition**: Future information
- **Labs ordered later**: Not available at admission

## 3. Selection Bias

### Definition
Systematic differences between study groups due to how subjects were selected.

### Common Mistakes

**Survivor Bias:**
```sql
-- WRONG: Selecting patients who have 7-day labs
-- Excludes early deaths and early discharges
SELECT stay_id
FROM mimiciv_derived.chemistry
WHERE charttime >= DATETIME_ADD(
    (SELECT intime FROM mimiciv_icu.icustays WHERE stay_id = chemistry.stay_id),
    INTERVAL 7 DAY
);
```

**Data Availability Bias:**
```sql
-- WRONG: Patients with complete data
-- Complete cases may be systematically different
SELECT *
FROM mimiciv_derived.sofa
WHERE respiration_24hours IS NOT NULL
    AND coagulation_24hours IS NOT NULL
    AND liver_24hours IS NOT NULL
    AND cardiovascular_24hours IS NOT NULL
    AND cns_24hours IS NOT NULL
    AND renal_24hours IS NOT NULL;
```

### Correct Approach
- Report exclusions explicitly in CONSORT diagram
- Analyze whether excluded patients differ
- Consider imputation for missing data
- Use intention-to-treat principles

## 4. Confounding by Indication

### Definition
Treatment assignment is associated with prognosis, creating spurious treatment effects.

### Example
Sicker patients receive more aggressive treatment, making treatment appear harmful:

```sql
-- WRONG: Comparing mortality by vasopressor use
-- Vasopressors given to sicker patients
SELECT
    CASE WHEN v.stay_id IS NOT NULL THEN 'Vasopressor' ELSE 'No Vasopressor' END AS treatment,
    AVG(a.hospital_expire_flag) AS mortality
FROM mimiciv_icu.icustays ie
LEFT JOIN mimiciv_derived.vasoactive_agent v ON ie.stay_id = v.stay_id
INNER JOIN mimiciv_hosp.admissions a ON ie.hadm_id = a.hadm_id
GROUP BY 1;
-- This will show higher mortality in vasopressor group (confounding!)
```

### Correct Approaches
- Propensity score matching/weighting
- Instrumental variables
- Regression discontinuity
- Target trial emulation
- Clearly state observational limitations

## 5. Multiple Comparisons

### Definition
Testing many hypotheses increases false positive rate.

### Common Mistake
- Testing 20 lab values without adjustment
- Subgroup analyses without pre-specification
- Feature selection on full dataset

### Correct Approach
- Pre-specify primary outcome
- Use Bonferroni or FDR correction
- Hold out test set for final evaluation
- Register analysis plan prospectively

## 6. Time-Related Errors

### Aggregation Window Mismatch
```sql
-- WRONG: Mixing 24h and 48h windows
SELECT
    s.sofa_24hours,     -- 24-hour worst
    lab.creatinine_max  -- first_day_lab uses 24h
FROM mimiciv_derived.sofa s
INNER JOIN mimiciv_derived.first_day_lab lab
    ON s.stay_id = lab.stay_id
WHERE s.hr = 48;  -- SOFA at 48h, but lab is day 1!
```

### Temporal Alignment
```sql
-- CORRECT: Align time windows
SELECT
    s.sofa_24hours,
    lab.creatinine_max
FROM mimiciv_derived.sofa s
INNER JOIN mimiciv_derived.first_day_lab lab
    ON s.stay_id = lab.stay_id
WHERE s.hr = 24;  -- Both at 24 hours
```

## 7. Handling Missing Data

### Wrong Approaches
- Complete case analysis (introduces bias)
- Single imputation (underestimates variance)
- Zero imputation for labs (not clinically meaningful)

### Better Approaches
- Multiple imputation
- Maximum likelihood estimation
- Sensitivity analyses
- Pattern-mixture models
- Report missingness rates

## 8. Outcome Definition

### Ambiguous Mortality
```sql
-- Be specific about which mortality
SELECT
    hospital_expire_flag,  -- In-hospital only
    -- vs
    CASE WHEN dod IS NOT NULL
         AND dod <= DATETIME_ADD(dischtime, INTERVAL 30 DAY)
         THEN 1 ELSE 0 END AS mortality_30d
FROM mimiciv_hosp.admissions a
INNER JOIN mimiciv_hosp.patients p ON a.subject_id = p.subject_id;
```

### Time Zero Definition
- ICU admission? Hospital admission? First abnormal vital?
- Be explicit and consistent

## Checklist for Study Design

- [ ] Time zero clearly defined
- [ ] Exposure determined at fixed time point
- [ ] No future information used as predictors
- [ ] Selection criteria reported with flow diagram
- [ ] Missing data handling specified
- [ ] Confounders identified and addressed
- [ ] Primary outcome pre-specified
- [ ] Multiple comparison correction planned
- [ ] Sensitivity analyses planned
- [ ] External validation considered

## References

- Suissa S. "Immortal time bias in observational studies of drug effects." Pharmacoepidemiology and Drug Safety. 2007.
- Hernán MA, Robins JM. "Causal Inference: What If." Chapman & Hall/CRC. 2020.
- Johnson AEW et al. "Machine Learning and Decision Support in Critical Care." IEEE. 2016.
