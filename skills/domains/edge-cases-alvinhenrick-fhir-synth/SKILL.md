---
name: edge-cases
description: Generate edge-case patient scenarios for robustness including neonates, pregnant patients, elderly with polypharmacy, behavioral health, disability, rare diseases, multi-organ conditions, and deceased patients. Use when user mentions neonates, pregnancy, elderly, behavioral health, mental health, substance use, rare disease, cancer, disability, or deceased.
keywords: [neonate, infant, pregnant, pregnancy, prenatal, geriatric, elderly, polypharmacy, behavioral health, mental health, substance use, depression, anxiety, PHQ-9, GAD-7, disability, rare disease, sickle cell, cystic fibrosis, lupus, HIV, cancer, staging, transplant, deceased, death]
resource_types: [Patient, Condition, Observation, MedicationRequest]
always: true
---

# Edge Cases

Include these to ensure robustness:
- NEONATES & INFANTS: Use age in days/weeks, weight in grams, Apgar scores (LOINC 9274-2,
  9271-8), gestational age, birth weight classification (SNOMED), neonatal conditions
  (P07.3 Preterm, P59.9 Jaundice, P22.0 RDS).
- PREGNANT PATIENTS: Include pregnancy-related conditions (O24.4 Gestational DM, O13 Gestational
  HTN, O80 Spontaneous delivery), gravida/para status, EDD, prenatal labs (blood type,
  Rh factor, GBS screen), Pregnancy status observation (LOINC 82810-3).
- ELDERLY/GERIATRIC: Multiple comorbidities, polypharmacy (5+ meds), functional status
  (ADL/IADL scores), fall risk assessments, cognitive screening (MMSE/MoCA), advance
  directives, goals of care.
- BEHAVIORAL HEALTH: Substance use disorders (F10–F19 series), depression screening
  (PHQ-9 LOINC 44249-1), anxiety screening (GAD-7 LOINC 69737-5), suicide risk screening
  (Columbia LOINC 93267-1), psychiatric diagnoses, psychotropic medications.
- DISABILITY & FUNCTIONAL STATUS: Include functional status observations, assistive device
  use, disability conditions. Use Observation category "functional-status".
- RARE/CHRONIC CONDITIONS: Sickle cell (D57.1), Cystic fibrosis (E84.0), Lupus (M32.9),
  Rheumatoid arthritis (M06.9), Multiple sclerosis (G35), HIV (B20), Hepatitis C (B18.2),
  Cancer staging (use TNM codes), Organ transplant status (Z94.*).
- MULTI-ORGAN PATIENTS: Patients with conditions spanning multiple organ systems
  (e.g., diabetic nephropathy + retinopathy + neuropathy: E11.21 + E11.311 + E11.40).
- DECEASED PATIENTS: Include cause of death, death date, relevant final encounter.
- PATIENTS WITH NO DATA: Some patients may have only demographics (newly registered).

