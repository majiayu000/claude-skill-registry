---
name: coding-emergency-services
description: Assigns ED-specific E/M codes with critical care time documentation and procedure coding. Use when coding ED visits, documenting critical care, or coding ED procedures.
tags:
  - coding
  - medical-coding-and-billing
metadata:
  author: casemark
  practice_areas:
    - Medical Coding
    - Revenue Cycle
    - Health Information Management
  document_types:
    - Coded Record
  skill_modes:
    - Coding
    - Classification
---

# Coding Emergency Services

Assigns emergency department E/M codes (99281–99285), critical care time documentation (99291–99292), ED procedure codes, and observation services. Covers facility and professional fee coding, new vs. established patient rules specific to ED, split billing scenarios for admissions from the ED, and trauma/resuscitation coding.

## Why This Skill Exists

Emergency department coding has unique rules that differ from office and inpatient E/M coding. ED visits (99281–99285) still use the 1995/1997 Documentation Guidelines rather than the 2021+ MDM framework (as of 2024). Critical care coding requires precise time documentation and understanding of which procedures are bundled into critical care time. ED encounters frequently involve multiple providers, observation-to-inpatient conversions, and high-acuity procedures — all requiring specific coding knowledge. ED coding error rates typically exceed other ambulatory settings due to complexity and volume pressure.

---

## Checkpoint A — Intake

### Questions to Confirm Before Starting

1. What type of ED encounter is this? (straightforward visit, critical care, observation, trauma activation)
2. Is this facility (UB-04) or professional (CMS-1500) coding?
3. Did the patient receive critical care services? If so, is total critical care time documented?
4. Was the patient admitted to observation or inpatient status from the ED?
5. Were procedures performed in the ED (laceration repair, fracture reduction, intubation, central line)?
6. Is this a teaching hospital with residents involved in ED care?
7. Was a trauma activation fee applicable?

### Documents Required

- Complete ED physician note (history, exam, MDM, disposition)
- Nursing triage assessment and vital signs documentation
- Procedure notes for all ED procedures performed
- Critical care time documentation (start time, end time, total time, activities)
- Observation orders and status documentation (if applicable)
- Admission orders and H&P (if admitted from ED)
- Trauma activation documentation (if applicable)
- Radiology, laboratory, and other diagnostic results

---

## Step 1 — Select the ED E/M Code Level (99281–99285)

Apply 1995/1997 Documentation Guidelines for ED visits.

- **99281 — Problem-focused**: Self-limited or minor problem. Brief HPI, limited exam (1 body area or organ system), straightforward MDM.
- **99282 — Expanded problem-focused**: Low to moderate severity. Brief HPI, limited exam (affected area + related systems), low complexity MDM.
- **99283 — Expanded problem-focused**: Moderate severity. Extended HPI, extended exam (2–7 organ systems), moderate complexity MDM.
- **99284 — Detailed**: High severity without immediate threat to life. Extended HPI, detailed exam (extended exam of affected area + related systems, or 8+ organ systems), moderate complexity MDM.
- **99285 — Comprehensive**: Immediate significant threat to life or function. Comprehensive HPI, comprehensive exam (8+ organ systems with complete exam of each), high complexity MDM.

**Key ED-specific rules:**
- New vs. established patient distinction does NOT apply — all ED visits use the same code set regardless of prior visits.
- ED E/M codes can be billed by the ED physician even if the patient is subsequently admitted — the ED service is separately billable from the admitting physician's initial hospital care.
- If the ED physician admits the patient, do NOT bill both an ED E/M and an initial hospital care E/M — bill only the initial hospital care code (99221–99223) with the ED documentation combined.

## Step 2 — Code Critical Care Services (99291–99292)

Apply critical care time-based billing rules strictly.

- **99291**: First 30–74 minutes of critical care. Requires a minimum of 30 minutes.
- **99292**: Each additional 30 minutes beyond the first 74 minutes.
- Time does not need to be continuous but must be documented with total time spent.

**Time calculation:**
| Total Critical Care Time | Codes Reported |
|--------------------------|----------------|
| < 30 minutes | Use ED E/M code, not critical care |
| 30–74 minutes | 99291 × 1 |
| 75–104 minutes | 99291 × 1 + 99292 × 1 |
| 105–134 minutes | 99291 × 1 + 99292 × 2 |
| 135–164 minutes | 99291 × 1 + 99292 × 3 |

**Critical care definition**: Direct delivery by a physician of medical care for a critically ill or injured patient where illness/injury acutely impairs one or more vital organ systems with a high probability of imminent or life-threatening deterioration.

**Procedures bundled into critical care time** (do NOT bill separately):
- Chest X-ray interpretation (71045/71046)
- ABG interpretation (blood gas analysis)
- Pulse oximetry (94760–94762)
- Ventilator management (94002–94004)
- Vascular access procedures (36000, 36410, 36415, 36591, 36600)
- CPR (92950)
- Temporary transcutaneous pacing (92953)
- Gastric intubation (43752, 43753)
- Bladder catheterization (51701, 51702)

**Procedures NOT bundled** (bill separately and subtract time from critical care):
- Intubation (31500)
- Central line placement (36555–36573)
- Chest tube insertion (32551)
- Lumbar puncture (62270)

## Step 3 — Code ED Procedures

Assign CPT codes for procedures performed during the ED visit.

- **Wound repair**: Simple (12001–12021), Intermediate (12031–12057), Complex (13100–13160). Measure wound length in centimeters. Aggregate wounds of the same complexity in the same anatomic group.
- **Fracture/dislocation management**: Code based on type (closed/open), manipulation (with/without), and anatomic site. Example: 25600 (closed treatment distal radius fracture without manipulation).
- **Incision and drainage**: 10060 (simple I&D) vs. 10061 (complicated I&D — multiple, deep, or extensive).
- **Foreign body removal**: Based on depth and complexity — superficial (10120), deep/complicated (10121), eye (65205–65265).
- **Conscious sedation**: 99151–99153 by the performing physician; 99155–99157 by a different provider. Document start time, end time, monitoring intervals.
- When billing ED E/M + procedure on the same date, evaluate whether modifier 25 is needed for the E/M.

## Step 4 — Handle Observation Services

Apply observation coding rules for ED-to-observation transitions.

- **Observation status**: Place of service 22 (on-campus hospital outpatient). Observation services are outpatient, not inpatient.
- **Initial observation care (99218–99220)**: Billed by the physician who orders observation. Includes all E/M services on the date observation begins.
- **Observation discharge (99217)**: Billed on the date the patient is discharged from observation (if different from admission date).
- **Same-day admit/discharge from observation (99234–99236)**: If the patient is admitted to and discharged from observation on the same calendar date.
- **ED E/M + Observation**: If a different physician sees the patient in the ED and a different physician admits to observation, each physician bills their own service. If the SAME physician provides ED and observation care, bill only the observation admission code (not both ED E/M and observation).
- **Observation to inpatient conversion**: If the patient is admitted to inpatient from observation, bill only the initial inpatient code (99221–99223). The observation care is bundled.

## Step 5 — Facility Coding Considerations (UB-04)

Apply facility-specific ED coding rules.

- **Revenue code 0450**: ED general classification (facility charge for ED use).
- **Revenue code 0451–0459**: Specific ED service categories (EMTALA screening, beyond initial examination, etc.).
- **Trauma activation fee (revenue code 068x)**: Billed when a trauma team is activated per hospital protocol. Requires documented trauma activation criteria. Only one trauma activation fee per ED visit.
- **Facility E/M**: Many hospitals use the ACEP (American College of Emergency Physicians) facility ED E/M leveling system or a locally developed system — this is separate from professional E/M coding.
- **APC grouping**: ED visits group into APCs for Medicare OPPS payment. Higher-level E/M codes group into higher-paying APCs. Composite APCs apply to ED visits with certain combinations of services.
- **EMTALA compliance**: All patients presenting to the ED must receive a Medical Screening Examination (MSE) regardless of ability to pay — the facility codes this even if no professional E/M is generated.

---

## Checkpoint B — Review

- [ ] ED E/M code level is supported by 1995/1997 Documentation Guidelines (not 2021+ framework)
- [ ] Critical care time is documented with total minutes and reflects only qualifying activities
- [ ] Procedures bundled into critical care are NOT separately billed
- [ ] Procedures NOT bundled are separately coded with time deducted from critical care total
- [ ] Observation coding follows same-physician vs. different-physician rules
- [ ] Observation-to-inpatient conversion billing is correct (only initial inpatient code)
- [ ] Modifier 25 is applied appropriately for ED E/M + same-day procedure
- [ ] ICD-10-CM diagnoses reflect the ED encounter (not just the admitting diagnosis if admitted)

---

## Quality Audit

- [ ] Critical care time documentation includes start time, activities performed, and total time
- [ ] ED E/M level distribution matches expected acuity mix (bell curve centered around 99283–99284)
- [ ] Procedure coding is complete — all documented procedures are captured on the claim
- [ ] Split billing rules are followed when ED physician also admits the patient
- [ ] Observation hours are tracked for medical necessity (CMS 24-hour/48-hour benchmarks)
- [ ] Trauma activation fees are billed only when documented activation criteria are met
- [ ] Teaching physician attestation requirements are met for resident-provided ED care

---

## Guidelines

- Apply 1995 or 1997 CMS Documentation Guidelines for ED E/M code selection (not 2021+ E/M framework)
- Follow CMS Medicare Claims Processing Manual Chapter 12 §30 for critical care billing rules
- Reference AMA CPT guidelines for critical care (99291–99292) including bundled procedure list
- Apply CMS OPPS rules for facility ED coding and APC assignment
- Follow ACEP guidelines for facility E/M leveling if hospital uses that methodology
- Comply with EMTALA requirements for medical screening examination documentation
- Never bill critical care for time spent on procedures that are separately reportable — deduct that time
- Mark with [VERIFY] any critical care time documentation that lacks specific start/end times or total minutes
- Include disclaimer that ED coding rules are complex and payer-specific variations may affect reimbursement
