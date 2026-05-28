---
name: procedures
description: Generate Procedure resources with CPT, SNOMED CT, and HCPCS codes, body sites, performers, outcomes, and complication details. Use when user mentions procedures, surgery, operations, biopsy, catheterization, endoscopy, imaging procedures, physical therapy, or CPT codes.
keywords: [procedure, surgery, operation, biopsy, catheterization, endoscopy, colonoscopy, appendectomy, C-section, cesarean, joint replacement, stent, dialysis, intubation, ventilation, physical therapy, CPT, HCPCS, SNOMED, performed, surgical, operative, wound care, debridement, transplant]
resource_types: [Procedure]
always: false
---

# Procedures

Generate realistic Procedure resources with proper coding and clinical context.

## Coding Systems

Use dual coding when possible:
- **CPT** (Current Procedural Terminology): system = http://www.ama-assn.org/go/cpt
- **SNOMED CT**: system = http://snomed.info/sct
- **HCPCS**: system = https://www.cms.gov/Medicare/Coding/HCPCSReleaseCodeSets
- **ICD-10-PCS** (inpatient): system = http://www.cms.gov/Medicare/Coding/ICD10

### Common Procedures by Specialty

**General Surgery:**
- 47562 Laparoscopic cholecystectomy (SNOMED 45595009)
- 44970 Laparoscopic appendectomy (SNOMED 80146002)
- 49505 Inguinal hernia repair (SNOMED 44558001)

**Orthopedic:**
- 27447 Total knee arthroplasty (SNOMED 609588000)
- 27130 Total hip arthroplasty (SNOMED 52734007)
- 27245 ORIF femur fracture (SNOMED 179097006)
- 29881 Knee arthroscopy with meniscectomy (SNOMED 112727005)

**Cardiology:**
- 93458 Left heart catheterization (SNOMED 41976001)
- 92928 PCI with stent placement (SNOMED 36969009)
- 33533 CABG (SNOMED 232717009)
- 33208 Pacemaker insertion (SNOMED 307280005)

**GI / Endoscopy:**
- 43239 EGD with biopsy (SNOMED 386810004)
- 45380 Colonoscopy with biopsy (SNOMED 73761001)
- 47563 Lap cholecystectomy with cholangiogram (SNOMED 45595009)

**Pulmonary / Critical Care:**
- 31600 Tracheostomy (SNOMED 48387007)
- 94002 Mechanical ventilation initiation (SNOMED 40617009)
- 32405 Lung biopsy (SNOMED 15081005)

**OB/GYN:**
- 59510 Cesarean delivery (SNOMED 11466000)
- 59400 Vaginal delivery (SNOMED 177184002)
- 58661 Laparoscopic salpingectomy (SNOMED 287664005)

**Urology:**
- 52601 TURP (SNOMED 90199006)
- 50590 Lithotripsy (SNOMED 236990002)

**Dermatology / Minor:**
- 11102 Skin biopsy punch (SNOMED 240977001)
- 17000 Cryotherapy destruction (SNOMED 26782000)

**Radiology (Interventional):**
- 36556 Central line insertion (SNOMED 392230005)
- 75625 Aortography (SNOMED 77343006)

**Emergency / Bedside:**
- 36415 Venipuncture (SNOMED 82078001)
- 12001 Wound repair simple (SNOMED 225358003)
- 31500 Intubation (SNOMED 112798008)

## Status

- preparation, in-progress, not-done, on-hold, stopped, completed, entered-in-error, unknown.
- For not-done: include statusReason (medical contraindication, patient refusal, etc.).

## Body Site

Include Procedure.bodySite with SNOMED CT lateralized codes:
- Left knee (82169009), Right hip (62175007), Abdomen (818983003),
  Chest (51185008), Heart (80891009), Colon (71854001), Lung (39607008).

## Outcome

Use Procedure.outcome with codes from http://snomed.info/sct:
- 385669000 Successful, 385671000 Unsuccessful, 385670004 Partially successful.

## Complications

Include Procedure.complication and complicationDetail:
- Infection (SNOMED 128241005), Hemorrhage (131148009), Wound dehiscence (225553008).

## Performers

- Procedure.performer[].actor → Reference(Practitioner/{id}).
- Procedure.performer[].function — primary surgeon, first assistant, anesthesiologist.

## References

- Procedure.subject → Reference(Patient/{id}) — required.
- Procedure.encounter → Reference(Encounter/{id}).
- Procedure.reasonReference → Reference(Condition/{id}) — indication.
- Procedure.report → Reference(DiagnosticReport/{id}) — operative report.
- Procedure.basedOn → Reference(ServiceRequest/{id}).

