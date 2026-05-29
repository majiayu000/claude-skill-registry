---
name: allergies-immunizations
description: Generate allergy intolerances with SNOMED codes, reactions, severity, and criticality; plus immunization records with CVX codes, pediatric vaccine schedules. Use when user mentions allergies, immunizations, vaccines, allergy intolerance, penicillin allergy, anaphylaxis, or vaccination.
keywords: [allergy, intolerance, immunization, vaccine, vaccination, penicillin, anaphylaxis, allergic, reaction, CVX, NKDA, influenza, COVID vaccine, Tdap, MMR, hepatitis, pneumococcal, HPV, pediatric vaccine]
resource_types: [AllergyIntolerance, Immunization]
always: false
---

# Allergies and Immunizations

## Allergy Intolerance
- Types: allergy, intolerance. Categories: food, medication, environment, biologic.
- Common allergies with proper SNOMED codes:
  * Penicillin (91936005), Sulfonamide (387406002), Aspirin (387458008)
  * Latex (111088007), Peanut (91935009), Shellfish (227037002), Egg (91930004)
  * Bee venom (288328004), Dust mite (260147004), Pollen (256259004)
- Reactions with manifestation codes: Urticaria (126485001), Anaphylaxis (39579001),
  Angioedema (41291007), Rash (271807003), Nausea (422587007), Dyspnea (267036007)
- Criticality: low, high, unable-to-assess.
- Clinical status: active, inactive, resolved. Verification: confirmed, unconfirmed.
- Include patients with NKDA (No Known Drug Allergies) using code 716186003.

## Immunizations
- Common vaccines with proper CVX codes (http://hl7.org/fhir/sid/cvx):
  * Influenza (140, 150, 161), COVID-19 mRNA (207, 208, 211, 213, 228, 229, 230, 300, 301),
  * Tdap (115), Td (138), MMR (03), Varicella (21), Hepatitis B (43, 44, 45),
  * Pneumococcal (33, 109, 133, 152, 215, 216), Shingrix (187), HPV (62, 165),
  * Polio (10, 89), Rotavirus (116, 119), DTaP (20, 106, 107, 110)
- Status: completed, entered-in-error, not-done.
- For not-done: include statusReason (immunity, medical-precaution, patient-objection, etc.)
- Site: Left arm (LA), Right arm (RA), Left thigh (LT), etc.
- Route: Intramuscular (C28161), Subcutaneous (C38299), Oral (C38288).
- Include occurrenceDateTime and recorded date.
- Pediatric patients: generate age-appropriate vaccine schedules per CDC guidelines.

