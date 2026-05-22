---
name: mimic-eicu-mapping
description: Map equivalent concepts between MIMIC-IV and eICU databases. Use for multi-database studies, external validation, or understanding structural differences between databases.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: both
  category: data-quality
  source: https://github.com/MIT-LCP/mimic-code, https://github.com/MIT-LCP/eicu-code
  validated: true
---

# MIMIC-IV to eICU Mapping

This skill maps equivalent tables, columns, and concepts between MIMIC-IV and eICU databases to enable cross-database research and external validation.

## When to Use This Skill

- External validation of MIMIC-IV models on eICU
- Multi-center studies combining both databases
- Understanding structural differences
- Translating queries between databases

## Database Overview

| Characteristic | MIMIC-IV | eICU |
|---------------|----------|------|
| **Institution** | Beth Israel Deaconess (single center) | 208 hospitals (multi-center) |
| **Patients** | ~300,000 admissions | ~200,000 patients |
| **Time Period** | 2008-2019 | 2014-2015 |
| **ICU Types** | All ICU types | All ICU types |
| **Geography** | Boston, MA | United States (nationwide) |

## Identifier Mapping

| Concept | MIMIC-IV | eICU |
|---------|----------|------|
| Patient ID | subject_id | uniquepid |
| Hospital Admission | hadm_id | patienthealthsystemstayid |
| ICU Stay | stay_id | patientunitstayid |
| Hospital ID | N/A (single center) | hospitalid |
| Unit Visit | icustay_seq | unitvisitnumber |

## Core Table Mapping

### Patient Demographics

| MIMIC-IV | eICU | Notes |
|----------|------|-------|
| mimiciv_hosp.patients | patient | Base demographics |
| mimiciv_hosp.admissions | patient | Admission info combined |
| mimiciv_icu.icustays | patient | ICU stay info in patient table |
| mimiciv_derived.icustay_detail | icustay_detail (concept) | Derived convenience table |

### Vital Signs

| MIMIC-IV | eICU | Notes |
|----------|------|-------|
| mimiciv_derived.vitalsign | vitalperiodic, vitalaperiodic | eICU splits periodic/aperiodic |
| mimiciv_icu.chartevents | nursecharting | Raw charted values |

### Laboratory Values

| MIMIC-IV | eICU | Notes |
|----------|------|-------|
| mimiciv_hosp.labevents | lab | Different labname conventions |
| mimiciv_derived.chemistry | pivoted_lab (concept) | Derived/pivoted |
| mimiciv_derived.complete_blood_count | pivoted_lab (concept) | |

### Medications

| MIMIC-IV | eICU | Notes |
|----------|------|-------|
| mimiciv_hosp.prescriptions | medication | Hospital medications |
| mimiciv_icu.inputevents | infusiondrug | IV infusions |
| mimiciv_derived.antibiotic | - | Concept needs creation for eICU |

### Diagnoses

| MIMIC-IV | eICU | Notes |
|----------|------|-------|
| mimiciv_hosp.diagnoses_icd | diagnosis | eICU uses text descriptions |
| - | admissiondx | eICU has admission diagnosis |
| - | apacheapsvar | APACHE diagnosis categories |

## Concept Availability

### Available in Both (May Require Recalculation)

| Concept | MIMIC-IV | eICU |
|---------|----------|------|
| SOFA | mimiciv_derived.sofa | Requires custom calculation |
| APACHE IV | Not pre-computed | apachepatientresult |
| OASIS | mimiciv_derived.oasis | pivoted_oasis (concept) |
| GCS | mimiciv_derived.gcs | pivoted_score (concept) |
| Urine Output | mimiciv_derived.urine_output | pivoted_uo (concept) |

### MIMIC-IV Only
- Waveform data (vital sign waveforms)
- Radiology reports
- Detailed microbiology (organism/sensitivity)
- ED data

### eICU Only
- APACHE IV scores (pre-computed)
- Multi-center hospital data
- Respiratory care plan documentation
- Nurse care plan

## Key Structural Differences

### 1. Time Representation
```
MIMIC-IV: Absolute timestamps (DATETIME)
eICU: Offset in minutes from unit admission (INTEGER)

-- MIMIC-IV
WHERE charttime BETWEEN ie.intime AND ie.outtime

-- eICU (convert offset to time)
WHERE chartoffset >= 0 AND chartoffset <= unitdischargeoffset
```

### 2. Hospital Structure
```
MIMIC-IV: Single hospital, no hospital identifier
eICU: hospitalid links to hospital table with region, bed count
```

### 3. Diagnosis Coding
```
MIMIC-IV: ICD-9 and ICD-10 codes
eICU: Free-text diagnosis strings + APACHE categories
```

### 4. Lab Value Names
```
MIMIC-IV: itemid (numeric codes) with d_labitems lookup
eICU: labname (text strings), less standardized
```

## Example: Equivalent Queries

### First ICU Stay Selection

**MIMIC-IV:**
```sql
SELECT *
FROM mimiciv_derived.icustay_detail
WHERE first_icu_stay = TRUE;
```

**eICU:**
```sql
SELECT *
FROM patient
WHERE unitvisitnumber = 1;
```

### Mortality Outcome

**MIMIC-IV:**
```sql
SELECT stay_id, hospital_expire_flag
FROM mimiciv_hosp.admissions a
INNER JOIN mimiciv_icu.icustays ie ON a.hadm_id = ie.hadm_id;
```

**eICU:**
```sql
SELECT patientunitstayid,
       CASE WHEN hospitaldischargestatus = 'Expired' THEN 1 ELSE 0 END AS hosp_mort
FROM patient;
```

### Age

**MIMIC-IV:**
```sql
SELECT stay_id, admission_age
FROM mimiciv_derived.icustay_detail;
-- Note: Ages > 89 are shifted
```

**eICU:**
```sql
SELECT patientunitstayid,
       CASE WHEN age = '> 89' THEN 90 ELSE CAST(age AS INT) END AS age
FROM patient;
-- Note: age is stored as string, "> 89" for elderly
```

## Validation Considerations

1. **Population Differences**: eICU is multi-center with different case-mix
2. **Time Period**: Different years may have different practices
3. **Documentation Patterns**: Single vs multi-center charting variability
4. **Missing Data**: Different missingness patterns
5. **Outcome Definitions**: Verify mortality/LOS definitions match

## References

- Johnson AEW et al. "MIMIC-IV, a freely accessible electronic health record dataset." Scientific Data. 2023.
- Pollard TJ et al. "The eICU Collaborative Research Database." Scientific Data. 2018.
