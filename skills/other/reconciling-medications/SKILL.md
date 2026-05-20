---
name: reconciling-medications
description: Compares medication lists across care settings to identify discrepancies, duplications, and omissions. Use when performing medication reconciliation, identifying med discrepancies, or verifying discharge prescriptions.
tags:
  - reconciliation
  - pharmacy
  - patient-safety
metadata:
  author: casemark
  practice_areas:
    - Clinical Pharmacy
    - Pharmacy
  document_types:
    - Reconciliation Report
  skill_modes:
    - Reconciliation
    - Verification
---

# Reconciling Medications

Performs structured medication reconciliation across care transitions by comparing
medication lists from multiple settings, flagging discrepancies, and producing an
actionable reconciliation report suitable for pharmacist or provider review.

---

## Why This Skill Exists

Medication errors injure over 1.3 million Americans annually and kill approximately
7,000. The single highest-risk moment is a **care transition** — admission, transfer,
or discharge — where medication lists from different sources must be merged into one
accurate, current regimen.

The Joint Commission recognizes this risk as **National Patient Safety Goal
NPSG.03.06.01**, requiring organizations to "maintain and communicate an accurate
patient medication list." Despite this mandate, studies consistently show that
**30–70 % of patients** have at least one unintended medication discrepancy at
admission or discharge.

This skill exists to systematically surface those discrepancies before they reach
the patient. It enforces the **Best Possible Medication History (BPMH)**
methodology: a structured interview and multi-source verification process that
goes beyond simply copying a list from the chart.

**When to invoke this skill:**
- Admission med-rec (ED → inpatient)
- Transfer med-rec (ICU → floor, facility → facility)
- Discharge med-rec (inpatient → home/SNF/rehab)
- Post-discharge follow-up or clinic visit reconciliation
- Retrospective chart review for quality or litigation support

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

Before generating any output, **confirm or obtain** every item below. If a source
is unavailable, document it as `[NOT PROVIDED]` — never silently skip it.

### A1. Transition Context

| Field | Required | Notes |
|---|---|---|
| Transition type | Yes | Admission / Transfer / Discharge / Clinic follow-up |
| Sending facility & unit | Yes | Include care level (ICU, med-surg, SNF, home) |
| Receiving facility & unit | Yes | Same |
| Date/time of transition | Yes | Use ISO-8601 when possible |
| Responsible provider (sending) | Yes | Name, role, contact |
| Responsible provider (receiving) | Yes | Name, role, contact |

### A2. Medication Lists Available

Collect **all** lists that exist. Each list becomes a column in the reconciliation
matrix. Common sources:

1. **Home medication list** — patient-reported or pharmacy-verified
2. **Admission orders** — first orders entered on arrival
3. **Inpatient medication administration record (MAR)** — what was actually given
4. **Discharge prescription list** — what the patient leaves with
5. **External pharmacy records** — retail/mail-order fill history
6. **Prior facility transfer summary** — if transferring between facilities

> **BPMH note:** The home list should ideally be built from ≥ 2 sources (patient
> interview + pharmacy records or pill bottles). A single-source list must be
> flagged as `[UNVERIFIED — SINGLE SOURCE]`.

### A3. Patient Context

| Field | Required | Notes |
|---|---|---|
| Age / DOB | Yes | Pediatric and geriatric patients carry extra risk |
| Weight (kg) | When available | Required for weight-based dosing checks |
| Allergies & intolerances | Yes | Drug, food, environmental; include reaction type |
| Renal function (SCr / CrCl / eGFR) | When available | Flag renally-dosed meds if absent |
| Hepatic function (Child-Pugh / MELD) | When available | Flag hepatically-dosed meds if absent |
| Pregnancy / lactation status | When applicable | Category X drugs must be flagged immediately |
| Primary diagnoses | Yes | Needed to validate indication for each med |
| Code status / goals of care | When available | Affects appropriateness of certain therapies |

---

## Workflow

### Step 1 — Normalize Each List

For every medication on every source list, extract and standardize:

| Column | Format | Example |
|---|---|---|
| Generic name | lowercase, INN preferred | metoprolol succinate |
| Brand name | Title Case, if relevant | Toprol-XL |
| Dose | numeric + unit | 50 mg |
| Route | abbreviation (PO, IV, SQ, etc.) | PO |
| Frequency | standard sig codes | daily |
| Indication | short phrase | HTN |
| PRN qualifier | if applicable | PRN headache |
| Prescriber | name or role | Dr. Chen (cardiology) |

**Include OTC medications, herbals, vitamins, and supplements.** These are the
most commonly omitted categories and frequently cause interactions (e.g.,
St. John's Wort + SSRIs, fish oil + anticoagulants).

### Step 2 — Build the Reconciliation Matrix

Create a row per unique medication (match by generic name + route). Columns
represent each source list. Mark the status in each cell:

| Status Code | Meaning |
|---|---|
| `CONTINUED` | Same drug, dose, route, frequency — no change |
| `DOSE CHANGED` | Same drug, different dose or frequency |
| `NEW` | Not present on prior list |
| `DISCONTINUED` | Present on prior list, absent on current |
| `OMITTED — UNINTENTIONAL?` | Absent without documented rationale — **flag for review** |
| `THERAPEUTIC DUPLICATE` | Different drug, same pharmacologic class, overlapping indication |
| `DUPLICATE` | Same drug appears more than once |
| `HELD` | Temporarily suspended (e.g., NPO, peri-operative) |
| `SUBSTITUTED` | Formulary or insurance swap to a different agent in the same class |

### Step 3 — Flag Discrepancies

Every row that is **not** `CONTINUED` is a discrepancy requiring attention.
Prioritize by severity:

**Critical (resolve before patient leaves the current setting):**
- Omission of a high-alert medication (see ISMP list below)
- Duplicate anticoagulant, insulin, or opioid
- Drug-drug interaction rated as "major" or "contraindicated"
- Allergy mismatch — medication on list conflicts with documented allergy
- Category X drug in pregnancy

**High (resolve within the same shift):**
- Unintentional dose change on a narrow therapeutic index drug
- Renal/hepatic dose adjustment needed but not made
- Omission of chronic disease maintenance medication (e.g., anticonvulsant, immunosuppressant)

**Moderate (resolve before next transition):**
- Therapeutic duplicate with no documented rationale
- OTC/supplement omission with interaction potential
- Frequency discrepancy (e.g., BID vs TID)

**Low (document for follow-up):**
- Brand/generic discrepancy with no clinical impact
- Cosmetic sig differences (e.g., "daily" vs "once daily")

### Step 4 — High-Alert Medication Cross-Check

Per the **ISMP List of High-Alert Medications in Acute Care Settings**, give
extra scrutiny to:

| Class | Examples | Key Checks |
|---|---|---|
| Anticoagulants | warfarin, heparin, enoxaparin, DOACs | Duplication, bridging protocols, INR/anti-Xa monitoring |
| Insulins | all formulations | Sliding scale vs scheduled, basal/bolus pairing, hypoglycemia risk |
| Opioids | morphine, hydromorphone, fentanyl, oxycodone | MME calculation, duplicate opioids, naloxone co-prescribing |
| Antiarrhythmics | amiodarone, sotalol, flecainide | QTc interactions, thyroid/pulmonary monitoring |
| Chemotherapy | all agents | Protocol verification, hold criteria, supportive meds |
| Concentrated electrolytes | KCl > 40 mEq, NaCl 23.4 %, MgSO4 | Concentration, rate, cardiac monitoring |
| Neuromuscular blockers | succinylcholine, rocuronium | Context-appropriate only (OR/ICU), never on floor orders |
| Sedatives (IV) | propofol, midazolam, ketamine | Setting-appropriate, monitoring orders in place |

If **any** high-alert medication has a discrepancy of any severity, escalate the
finding to the top of the report regardless of the general severity tier.

### Step 5 — Allergy & Interaction Screen

- Cross-reference every medication on the reconciled list against the patient's
  **allergy and intolerance record**.
- Flag **cross-sensitivities** (e.g., penicillin allergy → cephalosporin caution).
- Run a drug-drug interaction check across the **final reconciled list**. Report
  interactions at the "major" or "contraindicated" level. Note "moderate"
  interactions only if clinically relevant given patient context.

### Step 6 — Renal & Hepatic Dose Review

If renal or hepatic function data is available:
- Flag every renally-cleared medication where the dose has **not** been adjusted
  for the patient's CrCl/eGFR.
- Flag hepatically-metabolized medications where Child-Pugh or MELD suggests
  dose reduction.
- If lab values are `[NOT PROVIDED]`, append a blanket caveat:
  `⚠ Renal/hepatic function not available — dose appropriateness not verified.`

---

## Output Structure

The final reconciliation report must contain these sections in order.
See `references/RECONCILIATION-TEMPLATE.md` for formatted table templates.

1. **Header** — Patient identifier, transition type, date, facilities, providers
2. **Summary Dashboard** — Total meds reconciled, counts by status code,
   critical/high/moderate/low discrepancy counts
3. **Reconciliation Matrix** — Full table, sorted by discrepancy severity
   (critical first), then alphabetically
4. **High-Alert Medication Detail** — Dedicated section for any high-alert med
   with a non-CONTINUED status
5. **Allergy & Interaction Findings** — Allergy mismatches and major DDIs
6. **Renal/Hepatic Flags** — Dose adjustment concerns
7. **Unresolved Items** — Anything marked `[VERIFY]` or `[NOT PROVIDED]`
8. **Pharmacist Attestation Block** — Name, credentials, date, signature line

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

Before finalizing, verify **every** item:

- [ ] Every medication from every source list appears in the matrix (no silent drops)
- [ ] Every non-CONTINUED row has a severity rating
- [ ] High-alert medications are called out in their dedicated section
- [ ] Allergy list has been cross-checked against the final reconciled list
- [ ] OTC meds, herbals, and supplements are included
- [ ] Renal/hepatic caveat is present if labs were unavailable
- [ ] All `[VERIFY]` and `[NOT PROVIDED]` tags are collected in Unresolved Items
- [ ] Transition context (sending/receiving facility, providers) is complete
- [ ] Output follows the template structure in `references/RECONCILIATION-TEMPLATE.md`
- [ ] No medication was assumed to be intentionally discontinued without documentation

---

## Quality Audit

| Criterion | Pass | Fail |
|---|---|---|
| All source lists accounted for | Every provided list appears as a column | Any list silently omitted |
| BPMH sourcing documented | ≥ 2 sources for home med list, or flagged as single-source | Single source used without flag |
| High-alert meds highlighted | Dedicated section present with zero omissions | Any high-alert med buried in general matrix only |
| Allergy cross-check completed | Explicit statement of check; findings listed or "none" | No mention of allergy screen |
| Severity tiers assigned | Every discrepancy has Critical / High / Moderate / Low | Any discrepancy without a tier |
| Renal/hepatic addressed | Dose flags present or caveat for missing labs | No mention of organ function |
| OTC/supplement inclusion | Explicitly listed or noted as `[NOT PROVIDED]` | Category entirely absent |
| `[VERIFY]` tags collected | All uncertain items in Unresolved section | Uncertain items unmarked or scattered |
| Attestation block present | Pharmacist name, credentials, date, signature line | Missing or incomplete |

---

## Reference Files

- [`references/RECONCILIATION-TEMPLATE.md`](references/RECONCILIATION-TEMPLATE.md) —
  Output table templates for the reconciliation matrix, summary dashboard,
  high-alert detail section, and attestation block.

### External References (do not fetch — for human context only)

- Joint Commission NPSG.03.06.01 — Medication Reconciliation
- ISMP List of High-Alert Medications in Acute Care Settings (updated annually)
- WHO High 5s Project — Standard Operating Protocol for Medication Reconciliation
- ASHP Guidelines on Pharmacy-Directed Medication Reconciliation

---

## Guidelines

- Never assume a medication was intentionally discontinued without explicit documentation from the prescribing provider. Unexplained absences from a medication list must be flagged as `[OMITTED — UNINTENTIONAL?]` until resolved.
- The Best Possible Medication History (BPMH) must be sourced from at least two independent sources (e.g., patient interview plus pharmacy fill records). A single-source medication history must always be flagged as `[UNVERIFIED — SINGLE SOURCE]`.
- High-alert medications per the ISMP list require individual line-by-line reconciliation at every care transition — they must never be batch-processed or assumed continued without verification.
- All OTC medications, herbal supplements, and vitamins must be explicitly included in the reconciliation matrix. Their omission is the most common source of undetected drug-drug interactions at care transitions.
- When renal or hepatic function data is unavailable, append a blanket caveat to the reconciliation report rather than assuming doses are appropriate. Never silently pass a renally-cleared medication without organ function verification.
- Every discrepancy must be assigned a severity tier (Critical, High, Moderate, Low) before the reconciliation report is finalized. Untiered discrepancies are considered incomplete reconciliation.
- Reconciliation reports are draft documents until attested by a licensed pharmacist or credentialed provider. AI-generated output must never be transmitted to a receiving facility without human review and signature.
- For cross-facility transfers, confirm formulary compatibility between sending and receiving institutions before finalizing therapeutic substitutions to prevent gaps in medication availability at the receiving site.
