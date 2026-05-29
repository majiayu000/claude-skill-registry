---
name: suspicion-of-infection
description: Identify suspected infection events in MIMIC-IV using antibiotic administration plus culture timing. Use as a component of Sepsis-3 definition or for infection research.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: derived-concepts
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/sepsis
  validated: true
---

# Suspicion of Infection

This concept identifies when clinicians suspected infection based on clinical actions: antibiotic administration combined with culture collection within a defined time window.

## When to Use This Skill

- Building Sepsis-3 cohorts (infection component)
- Antibiotic stewardship research
- Time-to-treatment studies
- Infection onset timing
- Culture yield research

## Pre-computed Table

```sql
SELECT
    subject_id,
    stay_id,
    hadm_id,
    ab_id,                     -- Unique antibiotic ID per patient
    antibiotic,                -- Antibiotic name
    antibiotic_time,           -- When antibiotic started
    suspected_infection,       -- 1 if meets criteria, 0 otherwise
    suspected_infection_time,  -- Onset time of suspected infection
    culture_time,              -- When culture was obtained
    specimen,                  -- Culture specimen type
    positive_culture           -- 1 if culture positive, 0 if negative
FROM mimiciv_derived.suspicion_of_infection;
```

## Definition Logic

**Suspected infection** requires BOTH:
1. **Antibiotic administration** (systemic, not topical)
2. **Culture collection** within time window:
   - Culture obtained up to 72h BEFORE antibiotic, OR
   - Culture obtained up to 24h AFTER antibiotic

### Suspected Infection Time
The `suspected_infection_time` is defined as:
- The **culture time** if culture was obtained BEFORE antibiotic
- The **antibiotic time** if antibiotic was given BEFORE culture

This represents when infection was first clinically suspected.

## Antibiotic Filtering

The query includes systemic antibiotics only:
- **Included routes**: IV, PO, NG, etc.
- **Excluded routes**: Topical (OU, OS, OD, AU, AS, AD, TP), eye drops, ear drops
- **Excluded formulations**: Creams, gels, ophthalmic ointments, desensitization

## Culture Matching Logic

Each antibiotic is matched to cultures in two directions:

### Culture Before Antibiotic (Primary)
- Culture obtained within 72 hours before antibiotic start
- If multiple cultures, uses the EARLIEST culture before the antibiotic

### Culture After Antibiotic (Secondary)
- Culture obtained within 24 hours after antibiotic start
- If multiple cultures, uses the EARLIEST culture after the antibiotic

Priority: Culture-before-antibiotic takes precedence when both exist.

## Critical Implementation Notes

1. **One Row Per Antibiotic**: Each antibiotic prescription gets its own row, potentially matched to one culture.

2. **Duplicate Handling**: A single culture may be matched to multiple antibiotics. A single antibiotic is matched to at most one culture (the earliest relevant one).

3. **ICU Association**: The `stay_id` is populated when antibiotic timing overlaps with an ICU stay. May be NULL for floor patients.

4. **Chart Dates vs Times**: Microbiology cultures sometimes only have dates (not times). When charttime is null, the query uses chartdate for matching.

5. **Positive Culture Flag**: Indicates whether organisms grew. Negative cultures still count as suspected infection (clinical suspicion existed).

6. **Specimen Types**: Include all culture types (blood, urine, sputum, etc.). The `specimen` column identifies the type.

## Example: Infection Events Per Patient

```sql
SELECT
    subject_id,
    COUNT(*) AS n_suspected_infections,
    SUM(positive_culture) AS n_positive_cultures
FROM mimiciv_derived.suspicion_of_infection
WHERE suspected_infection = 1
GROUP BY subject_id
ORDER BY n_suspected_infections DESC;
```

## Example: Time from Culture to Antibiotic

```sql
SELECT
    ROUND(
        TIMESTAMP_DIFF(antibiotic_time, culture_time, HOUR), 0
    ) AS culture_to_abx_hours,
    COUNT(*) AS n_events
FROM mimiciv_derived.suspicion_of_infection
WHERE suspected_infection = 1
    AND culture_time < antibiotic_time  -- culture first
GROUP BY 1
ORDER BY 1;
```

## Example: Most Common Antibiotics in Suspected Infection

```sql
SELECT
    antibiotic,
    COUNT(*) AS n_prescriptions,
    SUM(positive_culture) AS n_positive,
    ROUND(AVG(positive_culture), 2) AS positive_rate
FROM mimiciv_derived.suspicion_of_infection
WHERE suspected_infection = 1
GROUP BY antibiotic
ORDER BY n_prescriptions DESC
LIMIT 20;
```

## Example: Culture Specimen Distribution

```sql
SELECT
    specimen,
    COUNT(*) AS n_cultures,
    SUM(positive_culture) AS n_positive,
    ROUND(AVG(positive_culture), 2) AS positive_rate
FROM mimiciv_derived.suspicion_of_infection
WHERE suspected_infection = 1
GROUP BY specimen
ORDER BY n_cultures DESC;
```

## Related Skills

- [sepsis-3-cohort](../sepsis-3-cohort/SKILL.md) - Complete Sepsis-3 definition
- [sofa-score](../sofa-score/SKILL.md) - Organ dysfunction component

## References

- Singer M et al. "The Third International Consensus Definitions for Sepsis and Septic Shock (Sepsis-3)." JAMA. 2016;315(8):801-810.
