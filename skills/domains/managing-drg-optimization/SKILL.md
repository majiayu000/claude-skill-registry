---
name: managing-drg-optimization
description: Optimizes MS-DRG assignment through accurate principal diagnosis selection and CC/MCC capture. Use when optimizing DRGs, capturing comorbidities, or improving case mix index.
tags:
  - management
  - medical-coding-and-billing
metadata:
  author: casemark
  practice_areas:
    - Medical Coding
    - Revenue Cycle
    - Health Information Management
  document_types:
    - Management Report
  skill_modes:
    - Management
    - Coordination
---

# Managing DRG Optimization

Optimizes Medicare Severity Diagnosis Related Group (MS-DRG) assignment through accurate principal diagnosis selection, complete CC/MCC capture, optimal procedure coding, and discharge disposition validation. Targets accurate case mix index (CMI) representation without upcoding risk.

## Why This Skill Exists

MS-DRG assignment drives inpatient reimbursement for Medicare and most commercial payers using DRG-based payment. The difference between a base DRG and one with an MCC can exceed $10,000–$30,000 per case. Undercoding of secondary diagnoses that qualify as CCs or MCCs is the single largest source of lost inpatient revenue — studies show 15–20% of inpatient cases have undercaptured CCs/MCCs. Conversely, overcoding CCs/MCCs triggers RAC audits, DRG validation reviews, and potential False Claims Act liability. The goal is accurate, documentation-supported DRG optimization — not upcoding.


CMS updates the MS-DRG system annually with the IPPS Final Rule (effective October 1). Changes include DRG splits/merges, CC/MCC list revisions, relative weight updates, and new surgical DRGs. The transition from CMS-HCC V24 to V28 for risk adjustment and annual ICD-10-CM code updates create a continuously evolving landscape that DRG optimization programs must track.
---

## Checkpoint A — Intake

### Questions to Confirm Before Starting

1. What is the principal diagnosis and how was it determined?
2. What secondary diagnoses are documented and which qualify as CCs or MCCs?
3. What procedures were performed (ICD-10-PCS) and do any affect DRG assignment?
4. What is the discharge disposition (home, SNF, LTACH, deceased)?
5. Is there a CDI query pending that might change the diagnosis list?
6. What is the patient's age, sex, and discharge status (these affect DRG logic)?
7. What payer is responsible — Medicare FFS, Medicare Advantage, or commercial DRG-based?

### Documents Required

- Complete inpatient medical record (H&P, progress notes, discharge summary, operative reports)
- Final coded diagnosis and procedure list
- DRG grouper output showing assigned DRG, relative weight, and geometric/arithmetic LOS
- CC/MCC exclusion list (current fiscal year)
- MS-DRG Definitions Manual (current version)
- CDI query log and physician responses
- Discharge planning documentation

---

## Step 1 — Validate the Principal Diagnosis

Apply UHDDS and ICD-10-CM Official Guidelines Section II rigorously.

- The principal diagnosis is the condition established after study to be chiefly responsible for occasioning the admission.
- "After study" means after all testing, workup, and evaluation — not the admitting diagnosis.
- If two or more diagnoses equally meet the principal diagnosis criteria, either may be selected. Choose the one that most accurately reflects the clinical situation and results in the most clinically appropriate DRG (this is legitimate optimization, not upcoding).
- For patients admitted with a symptom and subsequently diagnosed, the confirmed diagnosis is principal (not the symptom) unless the confirmed diagnosis does not fully explain the symptom.
- For patients admitted for a complication of prior treatment, the complication is typically the principal diagnosis.
- Document the clinical reasoning for principal diagnosis selection in audit work papers.

## Step 2 — Capture All Qualifying CCs and MCCs

Review the record for secondary diagnoses that change the DRG severity level.

- **MCC (Major Complication or Comorbidity)**: Conditions that significantly increase resource use — e.g., sepsis (A41.x), acute respiratory failure (J96.0x), severe malnutrition (E43), acute kidney failure with tubular necrosis (N17.0).
- **CC (Complication or Comorbidity)**: Conditions with moderate impact — e.g., chronic kidney disease stage 3 (N18.3), type 2 diabetes with complications (E11.2x–E11.6x), acute blood loss anemia (D62).
- **Non-CC**: Conditions that do not change the DRG — e.g., essential hypertension (I10), type 2 diabetes without complications (E11.9), GERD (K21.0).

**CC/MCC exclusion rules:**
- Certain diagnosis codes are excluded from CC/MCC status when they are closely related to the principal diagnosis. Check the CC Exclusion List for each code pair.
- A diagnosis must be clinically validated in the record — documented, monitored, evaluated, treated, or requiring increased nursing care or extended LOS.
- Conditions present on admission (POA) vs. hospital-acquired conditions (HAC) affect reimbursement: CMS HAC Reduction Program penalizes hospitals for certain preventable conditions acquired during the stay.

### High-Impact DRG Pairs Reference

| Clinical Condition | Base DRG (no CC) | With CC | With MCC | Typical RW Difference (MCC vs. no CC) |
|---|---|---|---|---|
| Pneumonia | DRG 195 | DRG 194 | DRG 193 | 1.5-2.0x |
| Heart Failure | DRG 293 | DRG 292 | DRG 291 | 1.5-2.0x |
| Sepsis | DRG 872 | DRG 871 | DRG 870 | 1.5-2.5x |
| COPD | DRG 192 | DRG 191 | DRG 190 | 1.5-2.0x |
| Renal Failure | DRG 684 | DRG 683 | DRG 682 | 1.5-2.0x |
| Hip/Knee Replacement | DRG 470 | DRG 469 | DRG 468 | 1.5-2.5x |

## Step 3 — Optimize Procedure Coding for DRG Impact

Verify ICD-10-PCS procedure codes that affect DRG assignment.

- Certain procedures trigger a surgical DRG rather than a medical DRG, often with higher reimbursement. Verify the procedure's OR indicator in the MS-DRG Definitions Manual.
- Select the correct root operation: Excision (cutting out a portion) vs. Resection (cutting out all of) vs. Extraction (pulling/stripping out) — each maps to different DRG logic.
- Verify approach (open, percutaneous, endoscopic, percutaneous endoscopic) — some DRGs differentiate by approach.
- Check whether the procedure qualifies for a surgical DRG vs. a medical DRG with the principal diagnosis combination.
- Non-OR procedures may affect DRG grouping through their impact on complication/comorbidity logic.

## Step 4 — Run and Analyze the DRG Grouper

Process the coded data through the grouper and evaluate the result.

- Compare the assigned DRG to clinically plausible alternatives by testing different principal diagnosis sequencing or additional CC/MCC capture.
- Review the relative weight (RW) and expected reimbursement against the case's actual resource consumption.
- Evaluate geometric mean LOS (GMLOS) against actual LOS — significant outliers (short-stay or long-stay) may trigger auditor attention.
- If actual LOS is well below GMLOS, verify that the DRG accurately reflects the case — short stays with high-severity DRGs are audit targets.
- If actual LOS exceeds GMLOS, verify all CCs/MCCs are captured — the DRG may be undergrouped.
- Check for DRG pairs where a single additional CC or MCC moves the case to a higher-paying tier (e.g., DRG 193 vs. 194 vs. 195 for pneumonia).
- **Compliance-safe optimization boundaries** --- DRG optimization is legitimate when it ensures accurate code assignment supported by documentation. It crosses into upcoding when: codes are assigned without supporting documentation, physicians are pressured to document conditions not clinically present, CC/MCC codes are added that are not clinically validated (monitored, treated, evaluated), or principal diagnosis sequencing is manipulated without clinical justification

## Step 5 — Evaluate Discharge Disposition Impact

Discharge status affects DRG payment through transfer rules and post-acute care impact.

- **Transfer DRGs**: When a patient is transferred to another acute care hospital, the transferring hospital receives a per-diem payment (not the full DRG) for certain qualifying DRGs.
- **Post-Acute Care Transfer (PACT)**: For designated DRGs, discharge to SNF, IRF, LTACH, or home health triggers per-diem payment instead of full DRG payment. Over 280 MS-DRGs are subject to PACT rules.
- Verify the discharge disposition code accuracy — incorrect disposition codes can result in overpayment or underpayment.
- A patient who leaves against medical advice (AMA) is coded with disposition 07 and is NOT considered a transfer.

## Step 6 — Identify CDI Query Opportunities

Flag documentation gaps that could support additional CC/MCC capture.

- Review clinical indicators (lab values, vital signs, treatments) that suggest a condition may exist but is not explicitly documented.
- Draft compliant CDI queries that are non-leading: present clinical indicators and ask the physician to clarify the clinical significance, not to add a specific diagnosis.
- Common CDI opportunities: acute vs. chronic respiratory failure, sepsis vs. SIRS, malnutrition severity, acute kidney injury staging, encephalopathy etiology.
- Track physician response rates and CDI impact metrics (query agreement rate, CMI impact).

- **Annual DRG system updates** --- Track and implement IPPS Final Rule changes annually: new DRGs, DRG splits/merges, CC/MCC list changes (codes added or removed), relative weight updates, and new surgical DRG designations. Update grouper software, CC/MCC reference lists, and CDI query templates within 30 days of the October 1 effective date
---

## Checkpoint B — Review

- [ ] Principal diagnosis follows UHDDS definition and ICD-10-CM Official Guidelines Section II
- [ ] All clinically validated secondary diagnoses are coded with maximum specificity
- [ ] CC/MCC exclusion list has been checked for all secondary diagnosis/principal diagnosis pairs
- [ ] HAC and POA indicators are correctly assigned
- [ ] ICD-10-PCS codes accurately reflect root operations, approaches, and body parts documented in operative reports
- [ ] DRG grouper output has been reviewed for clinical appropriateness
- [ ] Discharge disposition is accurate and transfer/PACT rules are accounted for
- [ ] All pending CDI queries are resolved before final coding

- [ ] Compliance-safe optimization boundaries documented and communicated to CDI and coding staff
- [ ] Annual IPPS Final Rule DRG changes implemented within 30 days of October 1 effective date
- [ ] High-impact DRG pairs identified and prioritized for CDI review focus
---

## Quality Audit

- [ ] Principal diagnosis selection rationale is documented in audit work papers
- [ ] No CC/MCC is coded without supporting clinical documentation (not just lab values alone)
- [ ] DRG assignment is clinically appropriate — not just the highest-paying option
- [ ] CMI trends by service line are tracked and outliers are investigated
- [ ] Short-stay cases with high-severity DRGs are flagged for medical necessity review
- [ ] CDI query language is compliant (non-leading, presents clinical indicators, asks open-ended questions)
- [ ] Physician query response documentation is in the permanent medical record

- [ ] Compliance review of DRG optimization practices conducted at least annually
- [ ] IPPS Final Rule changes (DRG splits, CC/MCC list revisions) implemented by October 1
- [ ] High-impact DRG pairs are targeted for CDI review with documented financial and quality impact
- [ ] RAC and MAC audit results are analyzed for DRG optimization pattern feedback
---

## Guidelines

- Apply ICD-10-CM Official Guidelines Section II for principal diagnosis selection in inpatient settings
- Follow ICD-10-PCS Official Guidelines for procedure code assignment
- Reference the MS-DRG Definitions Manual (current fiscal year) for DRG logic, CC/MCC lists, and OR procedure indicators
- Apply CMS Inpatient Prospective Payment System (IPPS) rules for transfer and PACT policies
- Follow AHIMA and ACDIS practice briefs for compliant CDI query construction
- Never code a diagnosis that is not clinically validated in the record — clinical indicators alone without physician documentation do not support code assignment
- Mark with [VERIFY] any DRG optimization decision where clinical documentation is borderline
- Include disclaimer that DRG optimization must be documentation-supported and does not constitute guidance to upcode beyond what clinical evidence supports

- The line between optimization and upcoding is documentation. Every CC/MCC code must be supported by clinical documentation showing the condition was present (or developed during the stay) and required clinical evaluation, monitoring, treatment, or extended the length of stay. Lab values alone do not support code assignment
- Track RAC and MAC audit denials by DRG. If a specific DRG pair is repeatedly denied on audit, investigate whether the CDI/coding practice for that condition needs recalibration. Audit denial patterns are the most direct feedback on optimization accuracy