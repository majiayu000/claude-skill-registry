---
name: designing-clinical-trials
description: Structures clinical trial protocol design with study type selection, endpoint definition, and power calculation. Use when designing trials, writing protocols, or calculating sample sizes.
tags:
  - design
  - clinical-research
  - clinical
metadata:
  author: casemark
  practice_areas:
    - Clinical Research
    - Biostatistics
    - Regulatory Affairs
  document_types:
    - Design Document
  skill_modes:
    - Design
---

# Designing Clinical Trials

## Why This Skill Exists

Clinical trial design is the single highest-leverage decision in drug development. A poorly designed trial wastes years and millions of dollars; a well-designed one produces definitive evidence that regulators, payers, and clinicians can act on. This skill encodes the protocol-design workflow mandated by ICH-GCP E6(R2) Section 6, FDA 21 CFR 312.23(a)(6), and EMA scientific-advice guidance so that every protocol draft starts from regulatory-grade foundations rather than ad-hoc outlines.

---

## Checkpoint A — Intake and Scoping

Before any design work begins, confirm the following inputs with the requesting team:

### Required Intake Questions
1. What is the investigational product (drug, biologic, device, combination)?
2. What is the current development phase (Phase I, II, III, IV, or exploratory)?
3. What is the target indication and patient population (including age range, disease severity, prior treatments)?
4. Is there an existing Investigator's Brochure (IB) or Device Master File?
5. What regulatory pathway is targeted (FDA 505(b)(1), 505(b)(2), BLA, PMA, De Novo, EMA centralized)?
6. Are there existing preclinical or earlier-phase data informing dose selection?
7. What is the competitive landscape — are there approved therapies forming the standard of care comparator?
8. What is the sponsor's target product profile (TPP)?
9. Are there specific regulatory interactions (pre-IND, Type B, scientific advice) already completed?
10. What is the anticipated timeline from first-patient-in to database lock?

### Required Source Documents
- Investigator's Brochure (current edition)
- Target Product Profile or label concept
- Preclinical toxicology and pharmacology summaries
- Earlier-phase clinical data (if any)
- Regulatory meeting minutes (pre-IND, EOP2, scientific advice)
- Relevant FDA guidance documents for the therapeutic area
- Published trials in the same indication (for benchmarking)

---

## Step 1 — Select Study Design Architecture

Determine the trial type based on development phase and regulatory objectives:

- **Phase I**: Dose-escalation (3+3, mTPI, BOIN, CRM); single-ascending / multiple-ascending dose; food-effect; first-in-human
- **Phase II**: Randomized dose-finding (proof-of-concept); Simon two-stage (oncology); adaptive seamless Phase II/III
- **Phase III**: Parallel-group superiority, non-inferiority, or equivalence; factorial; crossover (where appropriate)
- **Phase IV**: Pragmatic, registry-based, or post-marketing commitment designs

For each architecture, document:
1. Rationale for selection (cite ICH E9 and E10 for choice of control)
2. Blinding strategy (open-label, single-blind, double-blind, triple-blind) with justification
3. Randomization method (simple, block, stratified, adaptive) per ICH E9 Section 2.3
4. Use of placebo vs. active comparator vs. standard-of-care with ethical justification

---

## Step 2 — Define Endpoints and Estimands

Specify primary, secondary, and exploratory endpoints following the ICH E9(R1) estimand framework:

- **Primary endpoint**: Must be clinically meaningful or a validated surrogate. Define the variable, population, intercurrent-event handling strategy (treatment-policy, composite, hypothetical, principal-stratum, while-on-treatment), and summary measure.
- **Secondary endpoints**: Rank-order by regulatory and clinical importance. Ensure multiplicity control plan exists (Hochberg, Bonferroni-Holm, hierarchical testing, graphical approach).
- **Exploratory endpoints**: Biomarkers, patient-reported outcomes (PROs using validated instruments like EQ-5D, SF-36, disease-specific tools), pharmacokinetic/pharmacodynamic parameters.
- **Safety endpoints**: Adverse events coded to MedDRA (latest version), laboratory abnormalities by CTCAE grading, ECG parameters, vital signs.

---

## Step 3 — Calculate Sample Size and Statistical Power

Perform formal power calculations and document every assumption:

1. **Effect size**: Minimum clinically important difference (MCID) — justify from literature, earlier phases, or regulatory guidance
2. **Variability estimate**: Standard deviation or event rate from prior data; apply conservative estimates
3. **Alpha level**: Typically 0.05 two-sided; adjust for interim analyses (alpha-spending functions: O'Brien-Fleming, Lan-DeMets)
4. **Power**: 80% minimum; 90% preferred for pivotal trials
5. **Dropout rate**: Inflate sample by expected attrition (typically 10–20% for chronic disease trials)
6. **Statistical test**: Specify exact test (log-rank, ANCOVA, MMRM, CMH, etc.) matching the primary analysis
7. **Software and method**: Document tool used (EAST, nQuery, PASS, R package) and version

Present results as: N per arm, total N, power achieved at specified effect size, sensitivity analyses at ±20% of assumed effect.

---

## Step 4 — Draft Eligibility Criteria

Write inclusion/exclusion criteria that balance internal validity with generalizability:

- **Inclusion criteria**: Confirmed diagnosis (specify method — histology, imaging, lab value), age range, disease stage/severity score, adequate organ function (define thresholds for hepatic, renal, hematologic), informed consent capacity
- **Exclusion criteria**: Contraindicated comorbidities, prior/concurrent therapies with washout periods, pregnancy/lactation, known hypersensitivity, psychiatric conditions affecting compliance, participation in another interventional trial within defined window
- **Vulnerable populations**: Apply 21 CFR Part 50 Subparts B-D protections (children, prisoners, pregnant women); justify inclusion or exclusion per FDA guidance on broadening eligibility

Flag overly restrictive criteria that would compromise recruitment feasibility or external validity.

---

## Step 5 — Design Visit Schedule and Assessments

Build the Schedule of Assessments (SoA) table:

1. **Screening period**: Duration (typically 14–28 days), required evaluations, rescreening rules
2. **Treatment period**: Dosing schedule, visit windows (±days), required assessments per visit
3. **Follow-up period**: Duration post-last-dose, safety follow-up requirements (typically 30 days for AEs, 90 days for SAEs or per protocol)
4. **Assessment alignment**: Map each endpoint to specific visit assessments; ensure primary-endpoint data are collected at optimal timepoints
5. **Burden assessment**: Evaluate total blood draws, imaging procedures, and visit frequency against patient burden; remove non-essential assessments

---

## Step 6 — Define Safety Monitoring and Stopping Rules

Specify the safety architecture:

- **Adverse event collection**: Define solicited vs. unsolicited AEs, collection period, severity grading (CTCAE v5 or investigator judgment), causality assessment method (WHO-UMC or Naranjo)
- **Dose-limiting toxicity (DLT)** definitions (Phase I): Enumerate specific toxicities, grade thresholds, evaluation window
- **Stopping rules**: Futility boundaries (beta-spending), safety stopping rules (predefined thresholds for specific AEs), DSMB charter triggers
- **DSMB/DMC**: Determine whether required (generally yes for Phase III, recommended for Phase II); define composition, meeting frequency, charter elements

---

## Step 7 — Write Protocol Synopsis

Compile the protocol synopsis per ICH E6(R2) Section 6 with these required elements:

| Section | Content |
|---------|---------|
| Title | Full protocol title with compound identifier |
| Protocol Number | Sponsor's unique identifier |
| Phase | Development phase |
| Objectives | Primary, secondary, exploratory — one sentence each |
| Design | Study type, blinding, randomization, duration |
| Population | Key inclusion/exclusion, target N |
| Endpoints | Primary, secondary, safety |
| Statistical Methods | Primary analysis, sample size justification |
| Duration | Per-patient and overall study duration |

---

## Checkpoint B — Design Review

Before advancing to full protocol draft, verify:

1. [ ] Primary endpoint aligns with the TPP and regulatory pathway expectations
2. [ ] Sample size is adequately powered with documented assumptions
3. [ ] Eligibility criteria balance validity and feasibility — recruitment projections are realistic
4. [ ] Randomization and blinding strategy are operationally implementable
5. [ ] Safety monitoring plan meets ICH-GCP and FDA 21 CFR 312.32 requirements
6. [ ] Schedule of assessments captures all endpoint data without excessive patient burden
7. [ ] Comparator choice is ethically and scientifically justified per ICH E10
8. [ ] Statistical analysis plan outline addresses multiplicity, missing data, and estimand specification
9. [ ] Protocol synopsis has been reviewed by regulatory affairs, biostatistics, and clinical operations

---

## Quality Audit

- [ ] All design decisions are traceable to regulatory guidance or published evidence
- [ ] Effect-size assumptions cite specific prior data sources
- [ ] Estimand framework is explicitly defined per ICH E9(R1)
- [ ] MedDRA version for AE coding is specified
- [ ] CTCAE version for severity grading is specified
- [ ] Randomization methodology is described with sufficient detail for reproducibility
- [ ] Adaptive design features (if any) are pre-specified with simulation results
- [ ] CONSORT-compliant participant flow can be generated from the design
- [ ] Protocol deviations likely to occur are anticipated with mitigation strategies
- [ ] All [VERIFY] flags have been resolved or escalated

---

## Guidelines

1. Never fabricate effect-size estimates — always anchor to published data or earlier-phase results
2. Apply CONSORT 2010 standards to ensure the design supports transparent reporting
3. For non-inferiority trials, justify the non-inferiority margin per FDA guidance ("Non-Inferiority Clinical Trials to Establish Effectiveness")
4. For adaptive designs, follow FDA guidance on "Adaptive Designs for Clinical Trials of Drugs and Biologics" (2019)
5. Always consider patient diversity (ICH E17 for multi-regional trials) and FDA guidance on enhancing diversity in clinical trials
6. Distinguish between regulatory endpoints (for approval) and clinical endpoints (for practice-changing evidence)
7. When recommending Bayesian designs, pre-specify prior distributions and justify informativeness
8. Escalate to senior biostatistician and regulatory affairs when pivotal-trial design choices involve novel endpoints or surrogate markers
9. Mark any assumption lacking empirical support with [VERIFY] for human review
10. This skill produces design documents — it does not replace protocol committee review or IRB approval
