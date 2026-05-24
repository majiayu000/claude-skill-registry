---
name: sepsis-3-cohort
description: Identify Sepsis-3 patients in MIMIC-IV using the consensus definition (SOFA >= 2 + suspected infection). Use for sepsis cohort studies, outcome research, or quality metrics.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: cohort-definitions
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/sepsis
  validated: true
---

# Sepsis-3 Cohort Identification

The Sepsis-3 definition (2016) identifies sepsis as life-threatening organ dysfunction caused by a dysregulated host response to infection. Operationalized as:
- **Suspected infection** (antibiotics + culture within time window) AND
- **SOFA score >= 2** (within 48h before to 24h after suspected infection)

## When to Use This Skill

- Creating sepsis patient cohorts for research
- Sepsis outcome studies
- Quality improvement and benchmarking
- Comparing sepsis populations across studies
- Validating machine learning models on sepsis data

## Pre-computed Table

```sql
SELECT
    subject_id,
    stay_id,
    -- Infection details
    antibiotic_time,
    culture_time,
    suspected_infection_time,
    -- SOFA details
    sofa_time,
    sofa_score,
    respiration,
    coagulation,
    liver,
    cardiovascular,
    cns,
    renal,
    -- Sepsis flag
    sepsis3
FROM mimiciv_derived.sepsis3;
```

## Sepsis-3 Definition Details

### Suspected Infection Criteria
A patient has suspected infection when:
1. **Antibiotics are administered** (IV or oral routes, excluding topical) AND
2. **Cultures are obtained** within a time window:
   - Culture within 72h BEFORE antibiotic, OR
   - Culture within 24h AFTER antibiotic

### SOFA Criteria
SOFA >= 2 points, where SOFA is calculated using the 24-hour worst values:
- Must occur within 48h before to 24h after suspected infection time

### Important Assumption
**Baseline SOFA is assumed to be 0** for all patients. The true Sepsis-3 definition requires acute change of >= 2 points from baseline, but pre-hospital baseline is rarely available.

## Critical Implementation Notes

1. **ICU-Only Definition**: This query identifies sepsis onset WITHIN the ICU. It cannot detect sepsis present at ICU admission or ED sepsis.

2. **Time of Sepsis Onset**: Defined as the earliest of:
   - `suspected_infection_time` (when infection was suspected)
   - This is typically the culture time if culture preceded antibiotics

3. **Multiple Antibiotics**: A patient may have multiple antibiotic-culture pairs. The query returns the first (earliest) suspected infection event.

4. **Culture Types**: All culture types are included (blood, urine, respiratory, etc.). Each culture specimen is identified.

5. **Positive vs Negative Cultures**: The `positive_culture` flag indicates whether the culture grew organisms. Sepsis-3 does not require positive cultures.

6. **SOFA Time Window**: SOFA must be >= 2 within:
   - 48 hours BEFORE suspected_infection_time, OR
   - 24 hours AFTER suspected_infection_time

## Example: Identify Sepsis Cohort

```sql
SELECT
    s.stay_id,
    ie.subject_id,
    ie.hadm_id,
    s.suspected_infection_time AS sepsis_onset,
    s.sofa_score,
    adm.hospital_expire_flag AS mortality
FROM mimiciv_derived.sepsis3 s
INNER JOIN mimiciv_icu.icustays ie ON s.stay_id = ie.stay_id
INNER JOIN mimiciv_hosp.admissions adm ON ie.hadm_id = adm.hadm_id
WHERE s.sepsis3 = TRUE;
```

## Example: Sepsis Severity Distribution

```sql
SELECT
    CASE
        WHEN sofa_score < 5 THEN 'Mild (SOFA 2-4)'
        WHEN sofa_score < 10 THEN 'Moderate (SOFA 5-9)'
        WHEN sofa_score < 15 THEN 'Severe (SOFA 10-14)'
        ELSE 'Very Severe (SOFA 15+)'
    END AS severity,
    COUNT(*) AS n_patients,
    ROUND(AVG(adm.hospital_expire_flag), 3) AS mortality_rate
FROM mimiciv_derived.sepsis3 s
INNER JOIN mimiciv_icu.icustays ie ON s.stay_id = ie.stay_id
INNER JOIN mimiciv_hosp.admissions adm ON ie.hadm_id = adm.hadm_id
WHERE s.sepsis3 = TRUE
GROUP BY 1
ORDER BY 1;
```

## Example: Time from ICU Admit to Sepsis Onset

```sql
SELECT
    ROUND(
        TIMESTAMP_DIFF(s.suspected_infection_time, ie.intime, HOUR), 0
    ) AS hours_to_sepsis,
    COUNT(*) AS n_patients
FROM mimiciv_derived.sepsis3 s
INNER JOIN mimiciv_icu.icustays ie ON s.stay_id = ie.stay_id
WHERE s.sepsis3 = TRUE
GROUP BY 1
ORDER BY 1;
```

## Limitations

1. **Baseline SOFA Unknown**: Assumes baseline SOFA = 0, may over-classify chronic organ dysfunction as sepsis
2. **ICU-Only**: Cannot identify ED sepsis or sepsis present on admission
3. **Antibiotic-Dependent**: Requires antibiotic administration - may miss untreated infections
4. **Culture-Dependent**: Requires cultures obtained - may miss clinically diagnosed infections

## Related Skills

- [suspicion-of-infection](../suspicion-of-infection/SKILL.md) - Detailed infection timing
- [sofa-score](../sofa-score/SKILL.md) - SOFA calculation details

## References

- Singer M et al. "The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3)." JAMA. 2016;315(8):801-810.
- Seymour CW et al. "Assessment of Clinical Criteria for Sepsis." JAMA. 2016;315(8):762-774.
