---
name: sdoh
description: Generate Social Determinants of Health (SDOH) observations and conditions using Gravity Project value sets. Use when user mentions social determinants, food insecurity, housing, transportation, financial strain, social isolation, employment, veteran, or SDOH screening.
keywords: [sdoh, social determinants, food insecurity, housing, homelessness, transportation, financial, social isolation, employment, veteran, education, stress, gravity project, intimate partner violence]
resource_types: [Observation, Condition, Goal, ServiceRequest]
always: false
---

# Social Determinants of Health

Generate SDOH Observations and Conditions:
- Use Gravity Project value sets and SDOH Clinical Care IG categories:
  * Food insecurity: LOINC 88124-3 (Food insecurity risk), SNOMED 733423003
  * Housing instability: LOINC 71802-3, SNOMED 32911000, ICD-10 Z59.0 (Homelessness)
  * Transportation: LOINC 93030-3, ICD-10 Z59.82
  * Financial strain: LOINC 76513-1, ICD-10 Z59.7 (Insufficient social insurance)
  * Social isolation: LOINC 93029-5, ICD-10 Z60.2
  * Education level: LOINC 82589-3
  * Employment status: LOINC 67875-5
  * Intimate partner violence: LOINC 76499-3, ICD-10 Z63.0
  * Stress: LOINC 76542-0
  * Veteran status: LOINC 63028-3 (include former military patients)
- Encode SDOH screening results as Observations with category =
  http://hl7.org/fhir/us/sdoh-clinicalcare/CodeSystem/SDOHCC-CodeSystemTemporaryCodes
  or social-history (http://terminology.hl7.org/CodeSystem/observation-category)
- Link SDOH Conditions to Goals and ServiceRequests for care coordination.

