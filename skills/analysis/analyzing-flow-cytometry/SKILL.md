---
name: analyzing-flow-cytometry
description: Interprets flow cytometry panels for hematologic malignancy classification and minimal residual disease. Use when analyzing flow cytometry, classifying lymphomas/leukemias, or documenting immunophenotyping.
tags:
  - analysis
  - pathology
metadata:
  author: casemark
  practice_areas:
    - Pathology
    - Laboratory Medicine
  document_types:
    - Analysis Report
  skill_modes:
    - Analysis
---

# Analyzing Flow Cytometry

Interprets flow cytometry panels for hematologic malignancy classification and minimal residual disease.

## Why This Skill Exists

Flow cytometry is the cornerstone of hematologic malignancy diagnosis, classification, and monitoring. The WHO Classification of Haematolymphoid Tumours (5th edition, 2022) and the International Clinical Cytometry Society (ICCS) guidelines mandate immunophenotypic characterization for definitive diagnosis of leukemias, lymphomas, and myeloid neoplasms. Accurate gating, correct panel interpretation, and proper integration with morphology and molecular data determine whether a patient receives the right chemotherapy regimen, qualifies for targeted therapy, or is monitored for minimal residual disease (MRD).

Errors in flow cytometry interpretation — misidentification of blast populations, failure to detect aberrant antigen expression, or incorrect T-cell vs. B-cell lineage assignment — lead to misclassification with direct therapeutic consequences. CAP accreditation (FLO checklist series) requires validated panels, documented gating strategies, and correlation with morphology. CLIA mandates that flow cytometry be performed under the supervision of a qualified laboratory director with demonstrated competency.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

1. **Specimen type** — Peripheral blood, bone marrow aspirate, lymph node, body fluid, or tissue disaggregate? Default: peripheral blood.
2. **Clinical indication** — New diagnosis, relapse assessment, MRD monitoring, staging, or T-cell subset enumeration? Default: new diagnosis workup.
3. **Panel requested** — Acute leukemia panel, mature B-cell panel, T-cell panel, plasma cell panel, or MRD panel? Default: acute leukemia screening panel.
4. **CBC/differential** — Current CBC with automated differential available? Default: not provided; flag [VERIFY].
5. **Morphology correlation** — Is a concurrent peripheral smear or bone marrow aspirate smear reviewed? Default: pending.
6. **Prior flow cytometry** — Are there prior immunophenotyping results for comparison? Default: none on file.
7. **Specimen viability** — Time from collection, anticoagulant used (EDTA vs. heparin), specimen temperature? Default: EDTA, < 24 hours.

### Documents to Request

- CBC with automated differential
- Peripheral blood smear or bone marrow aspirate smear review
- Prior flow cytometry reports
- Prior pathology/cytogenetics/molecular reports
- Clinical notes including suspected diagnosis and treatment history
- Panel configuration and antibody-fluorochrome conjugate assignments
- Instrument QC records (daily bead calibration, compensation matrix)

---

## Step 1: Pre-Analytical Assessment and Quality Check

Validate specimen and instrument quality before interpretation:

- **Specimen viability**: > 90% viability by 7-AAD or propidium iodide exclusion for diagnostic interpretation; < 70% viability compromises antigen detection.
- **Cell count**: Minimum 100,000 events acquired for screening panels; 500,000-1,000,000 events for MRD assays (sensitivity target: 10^-4 to 10^-5).
- **Compensation verification**: Confirm single-stain compensation controls were run and compensation matrix applied correctly. Flag any spillover artifacts.
- **Instrument QC**: Verify daily calibration beads are within acceptable CV (< 3% for fluorescence channels per manufacturer specifications).

| Quality Metric | Acceptable | Marginal | Unacceptable |
|---|---|---|---|
| Viability | > 90% | 70-90% | < 70% |
| Events acquired (diagnostic) | > 100,000 | 50,000-100,000 | < 50,000 |
| Events acquired (MRD) | > 500,000 | 200,000-500,000 | < 200,000 |
| Calibration bead CV | < 3% | 3-5% | > 5% |

---

## Step 2: Gating Strategy and Population Identification

Apply systematic gating following ICCS/Euroflow consensus recommendations:

1. **Singlet discrimination**: FSC-H vs. FSC-A to exclude doublets and aggregates.
2. **Viability gating**: Exclude dead cells (7-AAD or viability dye negative).
3. **CD45 vs. SSC backbone**: Identify major populations:
   - Lymphocytes: CD45 bright, SSC low
   - Monocytes: CD45 moderate-bright, SSC intermediate
   - Granulocytes: CD45 moderate, SSC high
   - Blasts: CD45 dim, SSC low
   - Erythroid precursors: CD45 negative-dim, SSC low
4. **Lineage assignment for abnormal populations**:
   - B-cell lineage: CD19, CD20, CD22, CD79a, cytoplasmic CD79a
   - T-cell lineage: CD2, CD3 (surface and cytoplasmic), CD5, CD7
   - Myeloid lineage: CD13, CD33, CD117, MPO
   - Monocytic: CD14, CD64, CD36
   - Megakaryocytic: CD41, CD61
   - Erythroid: CD71, CD235a (glycophorin A)

---

## Step 3: Immunophenotype Interpretation by Disease Category

### Acute Leukemia Classification

| Marker | B-ALL | T-ALL | AML | MPAL |
|---|---|---|---|---|
| CD19 | + | - | - | +/- (B-lineage component) |
| CD10 | Often + | - | - | Variable |
| cCD3 | - | + | - | +/- (T-lineage component) |
| MPO | - | - | + | +/- (myeloid component) |
| CD34 | Usually + | Variable | Variable | Variable |
| TdT | + | + | Usually - | Variable |

### Mature B-Cell Neoplasms — Key Discriminators

| Entity | CD5 | CD10 | CD23 | FMC7 | CD200 | Light Chain |
|---|---|---|---|---|---|---|
| CLL/SLL | + | - | + | - | + | Dim, restricted |
| MCL | + | - | - | + | - | Moderate, restricted |
| FL | - | + | +/- | + | - | Moderate, restricted |
| MZL | - | - | - | + | +/- | Moderate, restricted |
| HCL | - | - | - | + | + | Bright, restricted |

### MRD Detection

- Apply leukemia-associated immunophenotype (LAIP) approach or different-from-normal (DfN) approach.
- Report MRD as percentage of evaluable cells and absolute events counted.
- Sensitivity: state achieved sensitivity level (e.g., 0.01% = 10^-4).

---

## Step 4: Integration with Morphology and Molecular Data

- Correlate immunophenotype with peripheral smear or bone marrow morphology (blast percentage, Auer rods, dysplasia).
- Integrate cytogenetic results: t(9;22) BCR::ABL1, t(8;21) RUNX1::RUNX1T1, inv(16) CBFB::MYH11, t(15;17) PML::RARA.
- Cross-reference molecular findings: FLT3-ITD, NPM1, CEBPA, TP53, IKZF1 for risk stratification.
- For mature B-cell neoplasms, integrate FISH for t(11;14) cyclin D1 (MCL), t(14;18) BCL2 (FL), and MYC rearrangement.

---

## Step 5: Report Construction

Structure the flow cytometry report per ICCS recommendations:

1. **Specimen information**: Type, collection time, anticoagulant, viability.
2. **Clinical indication**: Stated reason for testing.
3. **Panel summary**: List antibodies tested with fluorochrome assignments.
4. **Findings**: Describe each abnormal population with percentage, antigen expression profile, and light chain status.
5. **Interpretation**: Provide a conclusive statement linking immunophenotype to WHO diagnostic category.
6. **Correlation statement**: Note agreement or discordance with morphology/molecular data.
7. **Comment**: Recommendations for additional testing (cytogenetics, molecular, biopsy).

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

1. Were all populations identified using standardized CD45/SSC gating with singlet and viability discrimination?
2. Does the immunophenotype assignment match a recognized WHO 5th edition entity?
3. Is light chain restriction (kappa:lambda ratio) quantified for B-cell populations?
4. Are MRD results reported with sensitivity level and event count?
5. Is there documented correlation with concurrent morphology and any available molecular data?

---

## Quality Audit

- [ ] Specimen viability assessed and documented
- [ ] Minimum event acquisition thresholds met for assay type
- [ ] Compensation matrix validated with single-stain controls
- [ ] CD45/SSC backbone gating strategy applied per ICCS guidelines
- [ ] Singlet and viability discrimination gates documented
- [ ] Lineage assignment supported by multiple markers (not single-antigen calls)
- [ ] Light chain restriction quantified with kappa:lambda ratio
- [ ] Immunophenotype matched to WHO 5th edition diagnostic entity
- [ ] MRD sensitivity level explicitly stated
- [ ] Morphology correlation documented
- [ ] Molecular/cytogenetic integration addressed
- [ ] Instrument QC records reviewed and within specification
- [ ] Report signed by qualified hematopathologist

---

## Guidelines

- Never assign lineage based on a single marker; require at least two lineage-defining antigens per WHO/ICCS criteria
- Report light chain restriction quantitatively (kappa:lambda ratio) rather than qualitatively; a ratio > 3:1 or < 0.3:1 supports clonality
- For MRD, always state the achieved sensitivity level and whether the result is below, at, or above the detection threshold
- Use WHO 5th edition terminology for all diagnostic classifications; retire outdated FAB nomenclature in final reports
- Flag specimens with < 70% viability as compromised and note potential for false-negative antigen loss
- Document the gating strategy in sufficient detail that another hematopathologist could reproduce the analysis
- Correlate flow cytometry with morphology and molecular results in every case; never issue a standalone flow report without context
- Maintain daily instrument QC logs and review compensation matrices at least weekly per CAP FLO checklist requirements
