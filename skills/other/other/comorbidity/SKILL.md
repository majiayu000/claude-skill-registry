---
name: comorbidity
description: Generate realistic Condition resources with ICD-10 and SNOMED CT codes, comorbidity clustering, categories, severity, staging, body site, evidence, onset, abatement, and encounter linkage. Use when user mentions conditions, diagnoses, diseases, diabetes, hypertension, COPD, depression, chronic illness, comorbidity, problem list, encounter diagnosis, staging, or ICD-10.
keywords: [comorbidity, condition, diagnosis, disease, diabetes, hypertension, COPD, depression, anxiety, obesity, CKD, cancer, asthma, heart failure, CHF, metabolic, chronic pain, dementia, severity, ICD-10, SNOMED, problem list, encounter diagnosis, staging, acute, chronic, bodySite, evidence]
resource_types: [Condition]
always: false
---

# Conditions

Generate clinically realistic Condition resources with proper coding, categories, and relationships.

## Categories

Every Condition MUST have a category from http://terminology.hl7.org/CodeSystem/condition-category:
- **problem-list-item** — chronic/ongoing conditions on the patient's problem list.
- **encounter-diagnosis** — conditions diagnosed during a specific encounter.
- **health-concern** — patient/provider-identified health concern (US Core).

A single condition can appear as both (e.g., diabetes is a problem-list-item AND an encounter-diagnosis when addressed during a visit).

## Coding Systems

Use dual coding when possible (ICD-10-CM + SNOMED CT):
- **ICD-10-CM**: system = http://hl7.org/fhir/sid/icd-10-cm
- **SNOMED CT**: system = http://snomed.info/sct
- Include both in Condition.code.coding[] for interoperability.

### Common Conditions by Specialty

**Primary Care / Internal Medicine:**
- E11.9 Type 2 diabetes (SNOMED 44054006) — most common chronic condition
- I10 Essential hypertension (SNOMED 38341003)
- E78.5 Hyperlipidemia (SNOMED 55822004)
- E66.01 Morbid obesity (SNOMED 238136002)
- J06.9 Upper respiratory infection (SNOMED 54150009)
- N39.0 Urinary tract infection (SNOMED 68566005)

**Cardiology:**
- I25.10 Coronary artery disease (SNOMED 53741008)
- I50.9 Heart failure (SNOMED 84114007)
- I48.91 Atrial fibrillation (SNOMED 49436004)
- I21.9 Acute MI (SNOMED 57054005)

**Pulmonology:**
- J44.1 COPD with exacerbation (SNOMED 195951007)
- J45.20 Mild asthma (SNOMED 195967001)
- J18.9 Pneumonia (SNOMED 233604007)
- J96.01 Acute respiratory failure (SNOMED 65710008)

**Nephrology:**
- N18.1–N18.6 CKD stages 1–5 (SNOMED 431855005 for CKD)
- N17.9 Acute kidney injury (SNOMED 14669001)

**Endocrinology:**
- E03.9 Hypothyroidism (SNOMED 40930008)
- E05.90 Hyperthyroidism (SNOMED 34486009)
- E11.65 DM with hyperglycemia (SNOMED 609567009)

**Mental Health:**
- F32.1 Major depression, moderate (SNOMED 73867007)
- F41.1 Generalized anxiety (SNOMED 21897009)
- F10.20 Alcohol use disorder (SNOMED 7200002)
- F17.210 Nicotine dependence (SNOMED 56294008)

**Oncology:**
- C34.90 Lung cancer (SNOMED 93880001)
- C50.919 Breast cancer (SNOMED 254837009)
- C61 Prostate cancer (SNOMED 399068003)
- C18.9 Colon cancer (SNOMED 93761005)

**Orthopedic / Pain:**
- M54.5 Low back pain (SNOMED 279039007)
- M17.11 Primary osteoarthritis, knee (SNOMED 239873007)
- S72.001A Hip fracture (SNOMED 5913000)

**Pediatric:**
- J45.20 Asthma (SNOMED 195967001)
- J30.9 Allergic rhinitis (SNOMED 61582004)
- L20.9 Atopic dermatitis (SNOMED 24079001)
- J20.9 Acute bronchitis (SNOMED 10509002)

## Comorbidity Clusters

Generate co-occurring conditions (not random independent diseases):
- **Metabolic syndrome**: E11.9 T2DM + I10 HTN + E78.5 Hyperlipidemia + E66.01 Obesity
- **Cardiovascular cascade**: I10 HTN → I25.10 CAD → I50.9 CHF
- **CKD progression**: N18.1→N18.5, often with HTN and T2DM
- **COPD cluster**: J44.1 COPD + J18.9 Pneumonia + F17.210 Nicotine dependence
- **Mental health**: F32.1 Depression + F41.1 GAD (frequently co-occurring)
- **Chronic pain**: M54.5 Low back pain + G89.29 Chronic pain + F11.20 Opioid use disorder
- **Geriatric**: Dementia (F03.90) + falls (W19) + incontinence (R32)
- **Pediatric atopic triad**: J45.20 Asthma + J30.9 Rhinitis + L20.9 Eczema

## Clinical Status and Severity

- **clinicalStatus** (http://terminology.hl7.org/CodeSystem/condition-clinical):
  active, recurrence, relapse, inactive, remission, resolved.
- **verificationStatus** (http://terminology.hl7.org/CodeSystem/condition-ver-status):
  confirmed, unconfirmed, provisional, differential, refuted, entered-in-error.
- **severity** (http://snomed.info/sct):
  24484000 Severe, 6736007 Moderate, 255604002 Mild.

## Staging

For stageable conditions, include Condition.stage[]:
- **Cancer**: TNM staging (stage I–IV) with summary code from SNOMED or AJCC.
- **CKD**: N18.1 (Stage 1, GFR ≥90) through N18.6 (ESRD, GFR <15).
- **Heart failure**: NYHA Class I–IV.
- **Liver disease**: Child-Pugh A/B/C, MELD score.

## Body Site

Include Condition.bodySite with SNOMED CT codes when anatomically specific:
- Knee (49076000), Hip (29836001), Lung (39607008), Heart (80891009),
  Liver (10200004), Kidney (64033007), Brain (12738006).

## Evidence

Link Condition.evidence[].detail to supporting resources:
- Observations (lab results confirming diagnosis).
- DiagnosticReports (imaging, pathology).

## Onset and Abatement

- **Acute conditions**: onsetDateTime within days of encounter.
- **Chronic conditions**: onsetDateTime or onsetAge years before current encounter.
- **Resolved conditions**: abatementDateTime or abatementString set.
- Use onsetAge for childhood-onset conditions (e.g., Type 1 DM at age 8).

## References

- Condition.subject → Reference(Patient/{id}) — required.
- Condition.encounter → Reference(Encounter/{id}) — link to diagnosing encounter.
- Condition.recorder → Reference(Practitioner/{id}) — who recorded it.
- Condition.asserter → Reference(Practitioner/{id} | Patient/{id}) — who asserted it.

