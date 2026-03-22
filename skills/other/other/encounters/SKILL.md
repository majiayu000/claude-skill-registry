---
name: encounters
description: Generate realistic clinical encounters with class codes, types, status, hospitalization details, discharge disposition, telehealth, and longitudinal care. Use when user mentions encounters, visits, admission, discharge, ER, emergency, inpatient, outpatient, telehealth, or hospital.
keywords: [encounter, visit, admission, discharge, emergency, ER, inpatient, outpatient, ambulatory, telehealth, virtual, hospital, office visit, consultation, triage, hospitalization, length of stay]
resource_types: [Encounter]
always: false
---

# Encounter Realism

Model real clinical workflows:
- CLASS codes (http://terminology.hl7.org/CodeSystem/v3-ActCode):
  AMB (ambulatory), IMP (inpatient), EMER (emergency), HH (home health),
  VR (virtual/telehealth), OBSENC (observation encounter), SS (short stay),
  PRENC (pre-admission), ACUTE (inpatient acute), NONAC (inpatient non-acute)
- TYPES (SNOMED): 308335008 (office visit), 183452005 (ER visit), 32485007 (hospital admission),
  185347001 (encounter for problem), 270427003 (routine child health), 185349003 (well woman),
  410620009 (well child), 11429006 (consultation), 371883000 (outpatient procedure)
- STATUS: planned, arrived, triaged, in-progress, onleave, finished, cancelled, entered-in-error
- HOSPITALIZATION: Include admit/discharge details with admitSource and dischargeDisposition:
  * admitSource: home, er, born-in-hospital, transfer
  * dischargeDisposition: home, snf (skilled nursing), rehab, expired, hospice
- REASON codes: Use Encounter.reasonCode with appropriate SNOMED/ICD-10 codes.
- LENGTH: Realistic Encounter.period — office visits ~15–60 min, ER 2–8 hrs,
  inpatient 1–14 days, ICU 3–30 days.
- TELEHEALTH: Mark virtual encounters with serviceType and use VR class code.
  Add location with type "VR" (virtual).
- MULTIPLE ENCOUNTERS per patient: Generate longitudinal care with follow-ups.

