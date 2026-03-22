---
name: auditing-coding-accuracy
description: Reviews coded encounters for accuracy using OIG compliance guidelines and CMS documentation requirements. Use when auditing medical codes, reviewing coding accuracy, or conducting compliance audits.
tags:
  - audit
  - medical-coding-and-billing
  - compliance
metadata:
  author: casemark
  practice_areas:
    - Medical Coding
    - Revenue Cycle
    - Health Information Management
  document_types:
    - Audit Report
  skill_modes:
    - Audit
    - Compliance
---

# Auditing Coding Accuracy

Reviews coded encounters for accuracy against OIG compliance guidelines, CMS documentation requirements, AMA CPT rules, and ICD-10-CM/PCS Official Guidelines. Identifies over-coding, under-coding, unbundling errors, and documentation deficiencies that create compliance risk or revenue leakage.

## Why This Skill Exists

Coding accuracy directly determines reimbursement integrity. The OIG Work Plan targets high-error-rate services annually — E/M upcoding, modifier misuse, and diagnosis specificity failures drive the majority of overpayment recoveries. A structured audit process catches errors before they become extrapolated liabilities. CMS CERT reports consistently show national paid-claim error rates between 6–8%, with improper payments exceeding $28 billion annually. Internal audits are the primary defense against external auditor findings and False Claims Act exposure.

---

## Checkpoint A — Intake

### Questions to Confirm Before Starting

1. What is the audit scope? (prospective pre-bill, retrospective post-payment, focused, or random)
2. Which service lines or provider specialties are included?
3. What date-of-service range applies?
4. Is this triggered by an external event (RAC audit, OIG inquiry, payer request)?
5. What sample methodology is required? (random, stratified, targeted by CPT range)
6. What coding systems are in scope? (CPT, ICD-10-CM, ICD-10-PCS, HCPCS Level II)
7. Are there known risk areas from prior audits or denial trends?

### Documents Required

- Coded encounter records with assigned CPT/HCPCS, ICD-10-CM/PCS codes, and modifiers
- Complete medical record documentation (physician notes, operative reports, diagnostic results)
- Chargemaster or fee schedule for billed amounts
- Prior audit findings and corrective action plans
- Applicable LCD/NCD policies for services under review
- NCCI edit files (current quarterly release) for bundling validation
- Payer-specific coding guidelines if non-Medicare claims are in scope

---

## Step 1 — Define Audit Parameters and Sampling

Establish the universe of claims and select the sample.

- **Random sample**: Use statistically valid methodology — minimum 30 records per provider or service line for meaningful error-rate calculation. OIG probe audits use 30-claim samples; RAC audits may extrapolate from as few as 20–40.
- **Stratified sample**: Weight by revenue, denial frequency, or known-risk CPT ranges (e.g., 99213–99215 for E/M, 10021–69990 for surgical).
- **Targeted sample**: Focus on specific codes flagged by comparative billing reports (CBRs), payer audits, or outlier analysis.
- Document the sampling frame, selection method, confidence level, and margin of error.
- Record the audit universe size and sample size in the audit work papers.

## Step 2 — Validate Diagnosis Coding (ICD-10-CM/PCS)

Review each diagnosis code for accuracy, specificity, and guideline compliance.

- Verify the principal diagnosis follows ICD-10-CM Official Guidelines Section II (inpatient) or the reason for the encounter (outpatient).
- Check laterality, episode of care (7th character), and anatomic specificity — e.g., M54.5 (low back pain) vs. M54.51 (vertebrogenic low back pain) vs. M54.59 (other low back pain).
- Validate sequencing rules: manifestation codes cannot be principal; etiology/manifestation pairs must be sequenced correctly (e.g., E11.65 + E08.36).
- Confirm "code first" and "use additional code" notes are followed.
- For inpatient PCS coding, verify the root operation matches the operative report (e.g., Excision vs. Resection vs. Destruction).
- Flag unspecified codes (categories ending in .9) where documentation supports greater specificity.
- Confirm excludes1/excludes2 notes are respected — excludes1 codes cannot coexist on the same claim.

## Step 3 — Validate Procedure Coding (CPT/HCPCS)

Review each procedure or service code for accuracy and documentation support.

- Verify the CPT code descriptor matches the documented service — read the full code description, not just the short descriptor.
- For E/M services, apply the 2021+ framework: confirm MDM level (number/complexity of problems, data reviewed, risk of management) or total time on date of encounter.
- Check that add-on codes (+) are reported with their primary codes and never stand alone.
- Validate that separate procedure codes (designated in CPT) are only reported when performed at a separate site, separate session, or for a distinct purpose.
- Confirm HCPCS Level II codes are used where required (e.g., J-codes for drugs, A/L codes for DME).
- For surgical codes, verify the operative report supports each code element: approach, extent, anatomic site.

## Step 4 — Validate Modifier Application

Audit every modifier for clinical justification and correct usage.

- **Modifier 25**: Confirm a separately identifiable E/M service is documented beyond the procedure's typical pre/post work. Look for a distinct chief complaint, history, exam, or MDM unrelated to the procedure decision.
- **Modifier 59 / XE, XS, XP, XU**: Verify distinct procedural service — separate encounter (XE), separate structure (XS), separate practitioner (XP), or unusual non-overlapping service (XU). Modifier 59 is the modifier of last resort when X-modifiers do not apply.
- **Modifier 26/TC**: Confirm correct component billing — 26 for professional interpretation only, TC for technical component only.
- **Modifiers 76/77**: Verify repeat procedure documentation with clinical necessity for the repeat.
- Flag any modifier used without supporting documentation as a coding error.

## Step 5 — NCCI and Bundling Edit Validation

Check all code pairs against current NCCI edits.

- Run all CPT code pairs on the same claim through the current NCCI Procedure-to-Procedure (PTP) edit table.
- Column 1/Column 2 pairs: the Column 2 code is bundled into Column 1 and should not be separately reported unless an appropriate modifier is appended AND documentation supports the exception.
- Check the Mutually Exclusive Edits (MUE) table — confirm units billed do not exceed the MUE value for each code.
- Validate Medically Unlikely Edits against the claim's units of service.
- Document each bundling exception with the specific clinical rationale.

## Step 6 — Score and Classify Findings

Apply a consistent error classification to each finding.

- **Over-coded**: Higher-level code assigned than documentation supports (e.g., 99215 billed when MDM supports 99214).
- **Under-coded**: Lower-level code assigned, resulting in missed legitimate revenue.
- **Unbundled**: Separately reported codes that should be bundled per NCCI or CPT guidelines.
- **Incorrect code**: Wrong CPT/ICD code entirely (e.g., wrong anatomic site, wrong procedure type).
- **Missing code**: Documented service not coded at all.
- **Modifier error**: Incorrect, missing, or unsupported modifier.
- **Documentation deficiency**: Code may be correct but documentation is insufficient to support it.
- Calculate per-provider and per-service-line error rates. OIG considers >5% error rate a significant compliance concern.

---

## Checkpoint B — Review

### Before Finalizing the Audit Report

- [ ] Every sampled record has been independently re-coded from source documentation
- [ ] Error classifications are consistent across all reviewers
- [ ] Financial impact has been calculated for each error type (over-payments and under-payments)
- [ ] Extrapolation methodology is documented if projecting to the full universe
- [ ] Provider-specific feedback summaries are prepared with concrete examples
- [ ] Corrective action recommendations are prioritized by financial impact and compliance risk
- [ ] All findings reference specific coding guidelines (CPT Assistant, Coding Clinic, ICD-10-CM Guidelines section)
- [ ] The audit report distinguishes between coder errors and documentation deficiencies requiring physician education

---

## Quality Audit

- [ ] Sample selection methodology is documented and defensible
- [ ] Each finding cites the specific guideline, rule, or reference supporting the auditor's conclusion
- [ ] Error rate calculations use correct numerator/denominator (errors / total code assignments reviewed)
- [ ] Financial impact includes both overpayment exposure and underpayment recovery opportunity
- [ ] Findings are categorized by root cause (coder knowledge gap, documentation gap, system configuration)
- [ ] Corrective action plan includes responsible party, deadline, and re-audit date
- [ ] Report includes comparison to prior audit periods for trend analysis
- [ ] Disclaimers note that audit findings are based on documentation available at time of review

---

## Guidelines

- Follow OIG Compliance Program Guidance for Individual and Small Group Physician Practices and Hospital Compliance Programs
- Apply ICD-10-CM Official Guidelines for Coding and Reporting (current fiscal year edition) for all diagnosis code validation
- Use CPT codebook conventions, instructions, and guidelines — including parenthetical notes and symbol definitions — for procedure code validation
- Reference CMS Internet-Only Manuals (IOM) Chapter 12 for physician billing and Chapter 23 for fee schedule policies
- Apply AHIMA Standards of Ethical Coding — coders shall not change codes or narratives of code descriptions to misrepresent diagnoses or procedures
- Never extrapolate without documented statistical methodology and confidence intervals
- Mark any finding where auditor confidence is below 90% with [VERIFY] and escalate to a credentialed coding specialist (CCS, CPC, or RHIA)
- All audit work papers must be retained per organizational policy and applicable state/federal record retention requirements
