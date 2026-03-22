---
name: vitals-and-labs
description: Generate vital signs using FHIR Vital Signs profile and lab panels (CBC, BMP, CMP, lipid, HbA1c, urinalysis, COVID) with LOINC codes, reference ranges, and interpretation. Use when user mentions vitals, labs, observations, blood pressure, heart rate, HbA1c, glucose, CBC, lab results, or test results.
keywords: [vital, vitals, lab, labs, observation, blood pressure, heart rate, temperature, oxygen, BMI, weight, height, CBC, BMP, CMP, HbA1c, glucose, cholesterol, lipid, hemoglobin, platelet, creatinine, sodium, potassium, urinalysis, COVID, LOINC, reference range]
resource_types: [Observation]
always: false
---

# Vital Signs and Lab Panels

## Vital Signs

Use the FHIR Vital Signs profile (LOINC panel 85353-1):
- Blood pressure: LOINC 85354-9 (panel), 8480-6 systolic, 8462-4 diastolic. Use component[].
  Realistic ranges: systolic 90–200 mmHg, diastolic 50–120 mmHg. Vary by age/condition.
- Heart rate: LOINC 8867-4, range 40–150 /min (vary for athletes, elderly, tachycardia)
- Respiratory rate: LOINC 9279-1, range 12–30 /min
- Temperature: LOINC 8310-5, range 35.5–40.5 Cel
- Oxygen saturation: LOINC 2708-6, range 85–100 %
- Height: LOINC 8302-2, Weight: LOINC 29463-7, BMI: LOINC 39156-5
- Pediatric growth: Head circumference (LOINC 9843-4), weight-for-age percentiles.
- Use Observation.category = "vital-signs" (http://terminology.hl7.org/CodeSystem/observation-category)
- Include Observation.interpretation codes: N=Normal, H=High, L=Low, HH=Critical High, LL=Critical Low

## Lab Panels

Use realistic lab results with proper reference ranges:
- CBC: WBC (6690-2), RBC (789-8), Hemoglobin (718-7), Hematocrit (4544-3), Platelets (777-3)
- BMP: Sodium (2951-2), Potassium (2823-3), Chloride (2075-0), CO2 (2028-9),
  BUN (3094-0), Creatinine (2160-0), Glucose (2345-7), Calcium (17861-6)
- CMP: Add ALT (1742-6), AST (1920-8), Alk Phos (6768-6), Total Bilirubin (1975-2),
  Albumin (1751-7), Total Protein (2885-2)
- Lipid panel: Total cholesterol (2093-3), LDL (13457-7), HDL (2085-9), Triglycerides (2571-8)
- HbA1c: LOINC 4548-4 (range 4.0–14.0 %)
- Urinalysis: LOINC 24356-8 (panel)
- COVID-19: LOINC 94500-6 (PCR), 94558-4 (antigen)
- Include referenceRange with low/high values and text (e.g. "4.5-11.0 x10^9/L").
- Flag abnormal results with interpretation codes.

