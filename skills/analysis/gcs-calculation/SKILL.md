---
name: gcs-calculation
description: Extract and calculate Glasgow Coma Scale (GCS) for ICU patients in MIMIC-IV. Use for neurological assessment, consciousness monitoring, or trauma severity scoring.
license: Apache-2.0
metadata:
  author: m4-clinical-extraction
  version: "1.0"
  database: mimic-iv
  category: derived-concepts
  source: https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/concepts/measurement
  validated: true
---

# Glasgow Coma Scale (GCS) Calculation

The Glasgow Coma Scale assesses level of consciousness through three components: Eye opening, Verbal response, and Motor response. This concept extracts and calculates GCS with special handling for intubated patients.

## When to Use This Skill

- Neurological status assessment
- Trauma severity scoring
- Sedation monitoring
- Severity scores (SOFA CNS, APACHE, SAPS)
- Consciousness trajectory analysis

## GCS Components and Scoring

| Response | Score 1 | Score 2 | Score 3 | Score 4 | Score 5 | Score 6 |
|----------|---------|---------|---------|---------|---------|---------|
| **Eye** | None | To pain | To speech | Spontaneous | - | - |
| **Verbal** | None | Incomprehensible | Inappropriate | Confused | Oriented | - |
| **Motor** | None | Extension | Flexion | Withdraws | Localizes | Obeys |

**Total GCS Range**: 3-15 (lower = worse)

## Pre-computed Table

```sql
SELECT
    subject_id,
    stay_id,
    charttime,
    gcs,          -- Total GCS score
    gcs_motor,    -- Motor component (1-6)
    gcs_verbal,   -- Verbal component (1-5)
    gcs_eyes,     -- Eye component (1-4)
    gcs_unable    -- 1 if unable to assess (intubated/sedated)
FROM mimiciv_derived.gcs;
```

## MetaVision Item IDs

| Component | Item ID | Description |
|-----------|---------|-------------|
| Verbal | 223900 | GCS - Verbal Response |
| Motor | 223901 | GCS - Motor Response |
| Eyes | 220739 | GCS - Eye Opening |

## Critical Implementation Notes

1. **Intubated Patients**: When verbal response is documented as "No Response-ETT" (endotracheal tube), the verbal component is set to 0 and flagged with `gcs_unable = 1`. The total GCS is then set to **15** (assumed normal if only intubation prevents assessment).

2. **Component Carry-Forward**: If only one or two components are documented at a time, previous values from the past 6 hours are carried forward. This prevents artificially low scores from incomplete charting.

3. **Calculation Logic**:
   ```
   GCS = Motor + Verbal + Eyes

   IF current verbal = 0 (intubated) THEN GCS = 15
   ELSE IF previous verbal = 0 THEN use current components only (don't carry forward)
   ELSE carry forward missing components from past 6 hours
   ```

4. **Sedated Patients**: Per SAPS-II guidelines, sedated patients should use pre-sedation GCS. In practice, if documented as "unable to score due to medication", this is flagged.

5. **Time Series**: Each row represents a charted observation, not an hourly aggregate. Multiple observations per hour are possible.

## Example: Worst GCS Per ICU Stay

```sql
SELECT
    stay_id,
    MIN(gcs) AS worst_gcs,
    MIN(gcs_motor) AS worst_motor,
    MIN(gcs_verbal) AS worst_verbal,
    MIN(gcs_eyes) AS worst_eyes
FROM mimiciv_derived.gcs
WHERE gcs_unable = 0  -- Exclude intubated/sedated
GROUP BY stay_id;
```

## Example: GCS Categories

```sql
SELECT
    CASE
        WHEN gcs <= 8 THEN 'Severe (3-8)'
        WHEN gcs <= 12 THEN 'Moderate (9-12)'
        ELSE 'Mild (13-15)'
    END AS gcs_category,
    COUNT(*) AS n_observations
FROM mimiciv_derived.gcs
WHERE gcs_unable = 0
GROUP BY 1
ORDER BY 1;
```

## Example: First Day Minimum GCS

```sql
SELECT
    g.stay_id,
    MIN(g.gcs) AS first_day_min_gcs
FROM mimiciv_derived.gcs g
INNER JOIN mimiciv_icu.icustays ie ON g.stay_id = ie.stay_id
WHERE g.charttime BETWEEN ie.intime AND DATETIME_ADD(ie.intime, INTERVAL 24 HOUR)
    AND g.gcs_unable = 0
GROUP BY g.stay_id;
```

## Example: GCS Trajectory

```sql
WITH hourly_gcs AS (
    SELECT
        stay_id,
        DATETIME_TRUNC(charttime, HOUR) AS hour,
        AVG(gcs) AS avg_gcs
    FROM mimiciv_derived.gcs
    WHERE gcs_unable = 0
    GROUP BY stay_id, DATETIME_TRUNC(charttime, HOUR)
)
SELECT
    stay_id,
    hour,
    avg_gcs,
    avg_gcs - LAG(avg_gcs) OVER (PARTITION BY stay_id ORDER BY hour) AS gcs_change
FROM hourly_gcs;
```

## Example: Handle Intubated Patients

```sql
-- Option 1: Exclude intubated patients
SELECT stay_id, MIN(gcs) AS min_gcs
FROM mimiciv_derived.gcs
WHERE gcs_unable = 0
GROUP BY stay_id;

-- Option 2: Use motor score only for intubated (mGCS)
SELECT
    stay_id,
    MIN(CASE WHEN gcs_unable = 1 THEN gcs_motor ELSE gcs END) AS min_gcs_or_motor
FROM mimiciv_derived.gcs
GROUP BY stay_id;
```

## References

- Teasdale G, Jennett B. "Assessment of coma and impaired consciousness: A practical scale." Lancet. 1974;2(7872):81-84.
- Teasdale G et al. "The Glasgow Coma Scale at 40 years: standing the test of time." Lancet Neurology. 2014;13(8):844-854.
