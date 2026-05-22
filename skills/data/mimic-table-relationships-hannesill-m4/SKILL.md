---
name: mimic-table-relationships
description: Understand MIMIC-IV table relationships, join patterns, and identifier hierarchy. Use for correct data linkage, avoiding duplicates, and proper temporal joins.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: data-quality
  source: https://github.com/MIT-LCP/mimic-code
  validated: true
---

# MIMIC-IV Table Relationships

Understanding the identifier hierarchy and table relationships is essential for correct query construction. Incorrect joins can cause data duplication or missing records.

## When to Use This Skill

- Writing complex queries joining multiple tables
- Understanding why queries return unexpected row counts
- Debugging duplicate or missing data issues
- Learning MIMIC-IV data structure

## Identifier Hierarchy

```
subject_id (patient)
    └── hadm_id (hospital admission)
            └── stay_id (ICU stay)
                    └── Events (chartevents, labevents, etc.)
```

### subject_id
- **Unique per patient**
- Persists across all hospitalizations and ICU stays
- Links to: `patients` table

### hadm_id
- **Unique per hospital admission**
- One patient can have multiple hadm_ids (readmissions)
- Links to: `admissions`, `diagnoses_icd`, `prescriptions`, most lab/hospital tables

### stay_id
- **Unique per ICU stay**
- One hospital admission can have multiple stay_ids (ICU readmission)
- Links to: `icustays`, `chartevents`, ICU-specific tables

## Core Table Relationships

### Hospital Module (mimiciv_hosp)
```sql
patients             -- 1 row per subject_id
    |
    +-- admissions   -- 1 row per hadm_id
    |       |
    |       +-- diagnoses_icd
    |       +-- procedures_icd
    |       +-- prescriptions
    |       +-- labevents
    |       +-- microbiologyevents
    |
    +-- transfers    -- Multiple per hadm_id (ward movements)
```

### ICU Module (mimiciv_icu)
```sql
icustays            -- 1 row per stay_id
    |
    +-- chartevents  -- Vitals, assessments
    +-- inputevents  -- Medications, fluids
    +-- outputevents -- Urine, drains
    +-- procedureevents
    +-- datetimeevents
```

## Common Join Patterns

### Patient -> Hospital -> ICU
```sql
SELECT p.subject_id, a.hadm_id, ie.stay_id
FROM mimiciv_hosp.patients p
INNER JOIN mimiciv_hosp.admissions a
    ON p.subject_id = a.subject_id
INNER JOIN mimiciv_icu.icustays ie
    ON a.hadm_id = ie.hadm_id;
```

### Labs to ICU Stay (Time-Bounded)
```sql
-- Labs drawn during ICU stay only
SELECT ie.stay_id, le.charttime, le.valuenum
FROM mimiciv_icu.icustays ie
INNER JOIN mimiciv_hosp.labevents le
    ON ie.hadm_id = le.hadm_id
    AND le.charttime >= ie.intime
    AND le.charttime <= ie.outtime;
```

### Labs Within N Hours of ICU Admission
```sql
-- First 24 hours
SELECT ie.stay_id, le.charttime, le.valuenum
FROM mimiciv_icu.icustays ie
INNER JOIN mimiciv_hosp.labevents le
    ON ie.hadm_id = le.hadm_id
    AND le.charttime >= ie.intime
    AND le.charttime <= DATETIME_ADD(ie.intime, INTERVAL 24 HOUR);
```

## Critical Join Warnings

### 1. Hospital Labs Duplicate Across ICU Stays
If a patient has multiple ICU stays in one hospitalization, joining labs by `hadm_id` only will duplicate lab values:

```sql
-- WRONG: Duplicates labs for patients with multiple ICU stays
SELECT ie.stay_id, le.*
FROM mimiciv_icu.icustays ie
INNER JOIN mimiciv_hosp.labevents le
    ON ie.hadm_id = le.hadm_id;  -- No time filter!

-- CORRECT: Add time bounds
SELECT ie.stay_id, le.*
FROM mimiciv_icu.icustays ie
INNER JOIN mimiciv_hosp.labevents le
    ON ie.hadm_id = le.hadm_id
    AND le.charttime BETWEEN ie.intime AND ie.outtime;
```

### 2. Derived Tables Already Filtered
Many `mimiciv_derived` tables are pre-joined to ICU stays:
```sql
-- These already have stay_id and time-bounded data
SELECT * FROM mimiciv_derived.vitalsign;  -- Already per stay_id
SELECT * FROM mimiciv_derived.chemistry;  -- Has subject_id and hadm_id
```

### 3. Multiple Measurements Per Time Point
Aggregate or select appropriately:
```sql
-- Get worst GCS per hour
SELECT stay_id,
       DATETIME_TRUNC(charttime, HOUR) AS hour,
       MIN(gcs) AS worst_gcs
FROM mimiciv_derived.gcs
GROUP BY stay_id, DATETIME_TRUNC(charttime, HOUR);
```

## Cardinality Reference

| Relationship | Cardinality |
|-------------|-------------|
| subject_id : hadm_id | 1 : many |
| hadm_id : stay_id | 1 : many |
| stay_id : chartevents | 1 : many |
| hadm_id : labevents | 1 : many |
| hadm_id : diagnoses_icd | 1 : many |
| stay_id : derived tables | 1 : many (usually) |

## Example: Verify Join Correctness

```sql
-- Check for unexpected duplicates
WITH joined AS (
    SELECT ie.stay_id, COUNT(*) AS n_labs
    FROM mimiciv_icu.icustays ie
    INNER JOIN mimiciv_hosp.labevents le
        ON ie.hadm_id = le.hadm_id
    GROUP BY ie.stay_id
)
SELECT
    COUNT(*) AS n_stays,
    AVG(n_labs) AS avg_labs_per_stay,
    MAX(n_labs) AS max_labs  -- Very high = possible duplication
FROM joined;
```

## BigQuery vs PostgreSQL Syntax

MIMIC concepts are written for BigQuery. Key differences:

| BigQuery | PostgreSQL |
|----------|------------|
| `DATETIME_ADD(x, INTERVAL '1' HOUR)` | `x + INTERVAL '1 hour'` |
| `DATETIME_DIFF(a, b, HOUR)` | `EXTRACT(EPOCH FROM (a - b))/3600` |
| `DATETIME_TRUNC(x, HOUR)` | `DATE_TRUNC('hour', x)` |
| `physionet-data.mimiciv_*` | `mimiciv_*` (schema) |

## References

- MIMIC-IV Documentation: https://mimic.mit.edu/docs/iv/
- Johnson AEW et al. "MIMIC-IV, a freely accessible electronic health record dataset." Scientific Data. 2023.
