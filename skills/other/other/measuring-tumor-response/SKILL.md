---
name: measuring-tumor-response
description: Applies RECIST 1.1 and iRECIST criteria for tumor measurement and treatment response assessment. Use when measuring tumor response, applying RECIST criteria, or documenting treatment effects.
tags:
  - radiology
  - treatment
metadata:
  author: casemark
  practice_areas:
    - Radiology
    - Diagnostic Imaging
  document_types:
    - Report
  skill_modes:
    - Analysis
---

# Measuring Tumor Response

Applies RECIST 1.1 and iRECIST criteria for tumor measurement and treatment response assessment.

## Why This Skill Exists

Accurate tumor measurement directly determines whether a patient continues treatment, switches therapy, or proceeds to surgery. RECIST 1.1 (Response Evaluation Criteria in Solid Tumors) is the international standard used in clinical trials and increasingly in routine oncology practice. Measurement errors — wrong axis, wrong lesion selection, inconsistent technique between timepoints — can lead to incorrect response categorization that alters patient management. FDA drug approvals and clinical trial endpoints depend on RECIST-compliant measurements.

iRECIST extends RECIST 1.1 for immunotherapy trials, where pseudoprogression (initial apparent growth followed by response) complicates traditional measurement criteria. The radiologist performing tumor measurements must understand target lesion selection rules, measurement technique standards, and response category definitions. Measurement variability between readers is a recognized problem; this skill enforces the standardized approach that minimizes inter-observer variation and ensures compliance with RECIST 1.1 and iRECIST protocols.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

1. **What response criteria are required?** (Default: RECIST 1.1 — specify if iRECIST, mRECIST, Choi, or RANO)
2. **Is this a baseline or follow-up assessment?** (Default: Identify timepoint)
3. **What is the tumor type and treatment protocol?** (Default: Obtain from oncology notes)
4. **Are prior measurement studies available with target-lesion table?** (Default: Required for follow-up)
5. **What imaging modality and protocol were used?** (Default: CT with IV contrast, portal venous phase)
6. **Is the patient on immunotherapy (requiring iRECIST)?** (Default: No — verify with oncology)
7. **Are there known non-measurable sites of disease (bone, leptomeningeal, effusion)?** (Default: Document all disease sites)

### Documents to Request

- Current imaging study (CT, MRI) with identical protocol to baseline
- Baseline imaging study with original target-lesion measurements
- Prior measurement tables from all timepoints
- Oncology treatment protocol specifying response criteria
- Clinical trial protocol (if applicable) with measurement instructions
- List of known disease sites from staging workup (PET/CT, bone scan)

---

## Step 1: Target Lesion Selection (Baseline Only)

At baseline, select target lesions per RECIST 1.1 rules:

### Selection Criteria

| Rule | Requirement |
|------|------------|
| Maximum target lesions | 5 total (max 2 per organ) |
| Minimum size — solid lesion | ≥10 mm longest diameter on CT |
| Minimum size — lymph node | ≥15 mm short axis on CT |
| Measurability | Reproducibly measurable in at least one dimension |
| Modality consistency | Same modality and protocol at all timepoints |

### Lesion Selection Priority
1. Largest lesions that are clearly measurable
2. Lesions representative of all involved organs
3. Lesions amenable to reproducible measurement (avoid lesions near heart/diaphragm motion)
4. Avoid previously irradiated lesions unless unequivocal progression post-radiation

### Non-Target Lesions
All other sites of disease not selected as targets. Document as present and track qualitatively:
- Bone lesions (lytic only; blastic are non-measurable)
- Leptomeningeal disease
- Pleural/pericardial effusions
- Lymphangitic carcinomatosis
- Lesions <10 mm or lymph nodes 10–14 mm short axis

---

## Step 2: Measurement Technique

| Lesion Type | Measurement Axis | Technique |
|-------------|-----------------|-----------|
| Solid organ mass | Longest diameter in axial plane | Measure at widest point; same axis orientation at each timepoint |
| Lymph node | Short-axis diameter | Perpendicular to longest axis; in axial plane |
| Lung nodule | Longest diameter in lung window | Use consistent window/level settings |
| Liver lesion | Longest diameter in portal venous phase | Same contrast phase at each timepoint |
| Bone lesion (lytic with soft tissue) | Soft-tissue component only | Measure soft tissue, not bone destruction |

### Measurement Rules
- Use electronic calipers on axial images (or coronal/sagittal if specified at baseline)
- Measure to the nearest millimeter
- Use the same slice thickness and reconstruction at each timepoint
- If a lesion splits into fragments, sum the longest diameters of all fragments
- If lesions merge, measure the combined mass as a single lesion
- "Too small to measure" = assign 5 mm value per RECIST convention

---

## Step 3: Calculate Response Category

### Sum of Longest Diameters (SLD)

Calculate the SLD of all target lesions at each timepoint:

```
SLD = Target₁ + Target₂ + Target₃ + ... + Target₅
```

For lymph nodes, use short-axis diameter in the SLD calculation.

### RECIST 1.1 Response Categories

| Category | Target Lesions | Non-Target Lesions | New Lesions |
|----------|---------------|-------------------|-------------|
| **Complete Response (CR)** | All target lesions disappeared; all lymph nodes <10 mm short axis | All non-target disease disappeared | None |
| **Partial Response (PR)** | ≥30% decrease in SLD from baseline | Non-progressive | None |
| **Progressive Disease (PD)** | ≥20% increase in SLD from nadir AND ≥5 mm absolute increase | Unequivocal progression | Any new lesion |
| **Stable Disease (SD)** | Does not meet CR, PR, or PD criteria | Non-progressive | None |

### Key Calculation Points
- **Nadir**: The smallest SLD recorded at any timepoint (not necessarily baseline)
- **Baseline**: The reference for PR calculation
- **5 mm absolute increase rule**: Prevents small absolute changes in small lesions from triggering PD
- **New lesion**: Any unequivocal new lesion = PD regardless of SLD change

---

## Step 4: iRECIST Modifications for Immunotherapy

| RECIST 1.1 Category | iRECIST Equivalent | Action |
|---------------------|-------------------|--------|
| PD (first occurrence) | iUPD (unconfirmed PD) | Confirm with repeat imaging in 4–8 weeks |
| PD confirmed on repeat | iCPD (confirmed PD) | Treatment discontinuation per protocol |
| PR/SD after iUPD | iSD / iPR | Reset — continue treatment |
| CR after iUPD | iCR | Continue treatment |

**Pseudoprogression recognition:**
- New or enlarging lesions on first post-immunotherapy scan
- If clinical status stable, rescan in 4–8 weeks before declaring PD
- iRECIST allows continued treatment through first unconfirmed progression

---

## Step 5: Structured Measurement Report

### Measurement Table Format

| Lesion # | Location | Baseline (mm) | Prior (mm) | Current (mm) | % Change from Baseline | % Change from Nadir |
|----------|----------|--------------|------------|-------------|----------------------|-------------------|
| T1 | Right lung, RUL | 32 | 28 | 25 | -21.9% | -10.7% |
| T2 | Liver segment 6 | 45 | 42 | 40 | -11.1% | -4.8% |
| T3 | Para-aortic LN (SA) | 22 | 18 | 16 | -27.3% | -11.1% |
| **SLD** | | **99** | **88** | **81** | **-18.2%** | **-8.0%** |

### Non-Target Assessment Table

| Site | Status |
|------|--------|
| T12 vertebral body | Stable sclerotic lesion |
| Right pleural effusion | Decreased |
| Peritoneal nodularity | Stable |

### Overall Response: **Stable Disease** (SLD decrease of 18.2% does not meet 30% threshold for PR)

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

1. Are the correct response criteria applied (RECIST 1.1 vs. iRECIST vs. other)?
2. Were target lesions measured using the same technique and axis as baseline?
3. Is the SLD calculated correctly with nadir reference for PD assessment?
4. Are non-target lesions assessed qualitatively?
5. Are new lesions documented and factored into the overall response?

---

## Quality Audit

- [ ] Response criteria version is stated (RECIST 1.1, iRECIST)
- [ ] Target lesion count does not exceed 5 total or 2 per organ
- [ ] All target lesions meet minimum size criteria at baseline
- [ ] Measurements use the correct axis (longest diameter for masses, short axis for nodes)
- [ ] Same imaging modality, protocol, and phase used at each timepoint
- [ ] SLD is calculated and recorded at each timepoint
- [ ] Percentage change calculated from both baseline (for PR) and nadir (for PD)
- [ ] The 5 mm absolute-increase rule is applied for PD determination
- [ ] Non-target lesions are assessed and documented
- [ ] New lesions are explicitly addressed (present/absent)
- [ ] Measurement table includes all timepoints for trending
- [ ] Overall response category is explicitly stated
- [ ] "Too small to measure" lesions are assigned 5 mm per RECIST convention
- [ ] For iRECIST, unconfirmed PD triggers confirmatory imaging at 4–8 weeks

---

## Guidelines

1. Never change target lesions after baseline — measure the same lesions at every timepoint, even if they become difficult to measure.
2. Use the nadir (not baseline) as the reference for progressive disease determination.
3. A single new lesion = progressive disease, regardless of target-lesion response.
4. For immunotherapy patients, always confirm progression with repeat imaging before declaring iCPD.
5. Lymph nodes are measured by short axis; a node must decrease to <10 mm short axis to qualify as CR.
6. If a target lesion becomes "too small to measure," assign 5 mm — do not use 0 mm unless the lesion is truly undetectable.
7. Report the overall response category explicitly in the impression — do not leave the oncologist to calculate it from raw measurements.
8. Include measurement uncertainty: if two timepoints are close to a category boundary, note the clinical significance.
