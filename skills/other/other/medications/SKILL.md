---
name: medications
description: Generate realistic medication prescriptions with RxNorm codes, dosage, timing, route, polypharmacy, and PRN medications. Use when user mentions medications, prescriptions, drugs, pharmacy, treatment, MedicationRequest, or polypharmacy.
keywords: [medication, prescription, drug, pharmacy, dosage, treatment, RxNorm, dose, refill, polypharmacy, insulin, metformin, statin, antibiotic, antihypertensive, opioid, SSRI, inhaler, PRN]
resource_types: [MedicationRequest, MedicationStatement, MedicationAdministration, Medication]
always: false
---

# Medication Realism

Generate prescriptions reflecting real clinical practice:
- POLYPHARMACY: Geriatric patients commonly take 5–15 medications. Include:
  * Antihypertensives: Lisinopril (RxNorm 29046), Amlodipine (17767), Metoprolol (6918)
  * Diabetes: Metformin (6809), Glipizide (4815), Insulin glargine (261551)
  * Statins: Atorvastatin (83367), Rosuvastatin (301542)
  * Anticoagulants: Warfarin (11289), Apixaban (1364430), Rivaroxaban (1114195)
  * Pain: Acetaminophen (161), Ibuprofen (5640), Tramadol (10689)
  * Psych: Sertraline (36437), Escitalopram (321988), Quetiapine (51272)
  * GI: Omeprazole (7646), Pantoprazole (40790)
- DOSAGE FORMS: Tablets, capsules, injections, inhalers, patches, liquids, eye drops.
  Use proper route codes from http://snomed.info/sct (26643006=Oral, 78421000=Intramuscular, etc.)
- FREQUENCY: Include timing.repeat with frequency, period, periodUnit, when (AC, PC, HS, etc.)
- STATUS: active, on-hold, cancelled, completed, entered-in-error, stopped, draft.
- INTENT: order, plan, original-order, reflex-order, filler-order, instance-order.
- PRN medications: Set asNeededBoolean=True or asNeededCodeableConcept with indication.
- DRUG ALLERGIES in AllergyIntolerance: Include medication allergies (Penicillin, Sulfa,
  NSAIDs) with reaction severity (mild, moderate, severe) and manifestation codes.

