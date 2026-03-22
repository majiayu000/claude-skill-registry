---
name: managing-hospital-handoffs
description: Creates structured handoff communications using I-PASS methodology for shift transitions. Use when performing sign-outs, creating handoff documents, or transitioning patient care between providers.
tags:
  - management
  - hospital-medicine
  - patient-care
metadata:
  author: casemark
  practice_areas:
    - Hospital Medicine
    - Internal Medicine
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---

# Managing Hospital Handoffs

Creates structured handoff communications using I-PASS methodology for shift transitions between providers.

## Why This Skill Exists

Communication failures during handoffs cause an estimated 80% of serious medical errors according to The Joint Commission. The landmark I-PASS study (Starmer et al., NEJM 2014) demonstrated a 30% reduction in preventable adverse events when structured handoff tools replaced unstructured sign-outs. The Joint Commission NPSG 02.05.01 mandates standardized handoff communication, and CMS Conditions of Participation require documented transfer of essential patient information at every care transition.

Hospitalists perform 2-4 handoffs per 24-hour cycle (day-to-night, night-to-day, weekend cross-cover, service changes). Each handoff represents a discontinuity point where critical information — pending results, active titrations, family concerns, anticipated deterioration — can be lost. Incomplete handoffs are the single most common contributing factor in malpractice cases involving delayed diagnosis or treatment in the inpatient setting.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

Before creating handoff documentation, confirm:

1. What **type of handoff** is this — shift change, service transfer, cross-cover sign-out, or discharge-to-PCP? *(Default: Shift change)*
2. How many **patients** are being handed off? *(Default: Full census)*
3. What is the **acuity distribution** — any ICU, step-down, or rapid-response patients? *(Default: Review by unit)*
4. Are there **pending critical results** (cultures, biopsies, imaging reads) expected during the receiving shift? *(Default: Flag all pending orders > 4 hours old)*
5. Are there **active titrations** — drips, insulin sliding scale adjustments, diuretic challenges — that require monitoring? *(Default: Review active IV orders)*
6. Are there **family meetings** or **goals-of-care discussions** scheduled or anticipated? *(Default: Check social work and case management notes)*
7. Are there **anticipated discharges** the receiving provider should execute? *(Default: Flag patients meeting discharge criteria)*

### Documents to Request

- Current patient list with room numbers and admitting diagnoses
- Most recent progress note for each patient
- Active medication list including IV drips and titration parameters
- Pending orders and expected result times
- Nursing concern list or charge nurse summary
- Consultant recommendations not yet acted upon
- Case management discharge planning status

---

## Step 1: Apply the I-PASS Framework

Structure every patient handoff using all five I-PASS elements:

### I — Illness Severity

Classify each patient into one of three categories:

| Classification | Definition | Action Required |
|---------------|------------|-----------------|
| **Stable** | Expected clinical course, no active concerns | Routine monitoring per current orders |
| **Watcher** | Potential for deterioration, requires closer monitoring | Specify what to watch and when to escalate |
| **Unstable** | Actively deteriorating or high risk for acute decompensation | Immediate bedside assessment by receiving provider |

### P — Patient Summary

One-liner format: "[Age] [sex] with [PMH] admitted [date] for [diagnosis], currently [clinical status]."

Example: "72M with COPD, CHF (EF 30%), CKD3 admitted 3 days ago for COPD exacerbation, currently on 2L NC, weaning steroids, anticipated discharge tomorrow."

### A — Action List

Categorize pending actions by urgency:

- **To-Do (must complete this shift)**: Labs to follow up, medications to titrate, consults to call, procedures to schedule
- **To-Do (can wait)**: Non-urgent follow-ups, routine reassessments
- **FYI (awareness only)**: Pending results not expected this shift, social issues, family preferences

### S — Situation Awareness and Contingency Planning

For each Watcher and Unstable patient, document:
- "If [specific event], then [specific action]"
- Example: "If SBP < 90, bolus 500 mL LR and call me. If no response after 1L, activate rapid response."
- Example: "If K > 5.5 on PM labs, hold spironolactone and give kayexalate 30g PO."

### S — Synthesis by Receiver

The receiving provider must:
- Read back key action items
- Ask clarifying questions
- Confirm understanding of all Watcher and Unstable patients

---

## Step 2: Prioritize the Handoff Order

Present patients in this order to frontload critical information:

1. **Unstable patients** — full I-PASS with detailed contingency plans
2. **Watcher patients** — full I-PASS with specific monitoring parameters
3. **Anticipated overnight events** — admissions expected, pending discharges, scheduled procedures
4. **Stable patients** — abbreviated handoff (one-liner + any pending items)

---

## Step 3: Document Cross-Cover Essentials

For cross-cover sign-out (covering unfamiliar patients), include additional fields:

- **Code status**: Full code / DNR / DNI / Comfort measures only
- **Allergies**: Top 3 critical allergies with reaction type
- **Weight**: For dosing calculations (especially anticoagulants)
- **Isolation status**: Contact, droplet, airborne, or standard
- **Key contacts**: Primary nurse, consultant on call, family point of contact
- **Recent procedures**: Within 48 hours, with complication watch parameters
- **Lines and devices**: Central lines (type, day count), Foley (day count), drains

---

## Step 4: Conduct the Verbal Handoff

Follow these communication standards:

1. **Environment**: Quiet, uninterrupted space; no hallway handoffs for unstable patients
2. **Duration**: 2-3 minutes per Watcher/Unstable patient; 30-60 seconds per Stable patient
3. **Face-to-face preferred**: For Unstable patients, in-person handoff at bedside when possible
4. **Written + verbal**: Never rely solely on written sign-out — verbal synthesis catches nuance
5. **Closed-loop**: Receiver summarizes back; sender confirms or corrects

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

After completing handoff documentation:

1. Has every **Watcher and Unstable** patient been given specific contingency plans?
2. Are all **pending critical results** flagged with expected timing and follow-up action?
3. Has the **code status** been documented for every patient?
4. Are **active titrations** and drips documented with current parameters and targets?
5. Has the receiving provider confirmed understanding through **read-back** of key items?

---

## Quality Audit

- [ ] Every patient is classified as Stable, Watcher, or Unstable
- [ ] One-liner patient summary is present for each patient
- [ ] Action items are categorized by urgency (must-do vs. FYI)
- [ ] Contingency plans use "If…then" format for all Watcher/Unstable patients
- [ ] Code status is documented for every patient
- [ ] Allergies are listed for cross-cover patients
- [ ] Pending results include expected timing and responsible action
- [ ] Active drips and titrations include current rate and target parameters
- [ ] Anticipated admissions or discharges during receiving shift are noted
- [ ] Family/social concerns are flagged when relevant
- [ ] Handoff was conducted in an appropriate environment (not hallway)
- [ ] Receiver read-back was completed and documented

---

## Guidelines

- Never omit the Situation Awareness (contingency) element — it is the most safety-critical component of I-PASS
- Update handoff documents in real-time throughout the shift, not just at sign-out
- Flag any patient with a sentinel event risk (active GI bleed, new chest pain, recent procedural complication) at the top of the list regardless of current stability
- Include antibiotic day counts and stop dates for all patients on antimicrobials
- Document the time of handoff and names of sender/receiver for medicolegal traceability
- If a critical pending result is expected during the transition, both sender and receiver should agree on who is responsible for follow-up
- Use standardized printed or EMR-generated handoff templates rather than free-text notes
- Limit interruptions — studies show each interruption during handoff increases error risk by 12%
