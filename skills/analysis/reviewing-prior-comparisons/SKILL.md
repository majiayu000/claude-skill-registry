---
name: reviewing-prior-comparisons
description: Structures comparison with prior imaging studies to identify interval changes and trends. Use when comparing imaging studies, identifying interval changes, or tracking disease progression.
tags:
  - review
  - radiology
metadata:
  author: casemark
  practice_areas:
    - Radiology
    - Diagnostic Imaging
  document_types:
    - Review Report
  skill_modes:
    - Review
    - Analysis
---

# Reviewing Prior Comparisons

Structures comparison with prior imaging studies to identify interval changes and trends.

## Why This Skill Exists

Comparison with prior imaging studies is the single most valuable tool for distinguishing significant from insignificant findings. The ACR Practice Parameter for Communication of Diagnostic Imaging Findings mandates that radiologists review all reasonably available prior studies and reference them in the report. Studies show that comparison with priors reduces false-positive rates by 20–30% and significantly improves diagnostic confidence. Failure to compare — or failure to note interval change — is a documented driver of diagnostic errors and malpractice claims.

The challenge is practical: prior studies may exist across multiple PACS systems, outside institutions, or different modalities. Radiologists must systematically identify relevant priors, account for technique differences, use standardized change-assessment language, and make explicit statements about interval change for every significant finding. Vague comparisons ("similar to prior") without specific dates or measurements are clinically unhelpful and medicolegally indefensible. This skill enforces the structured comparison methodology required by ACR standards and best practices.

---

## Checkpoint A: Pre-Draft Intake (Mandatory)

1. **Are prior studies available in PACS?** (Default: Search all linked PACS systems)
2. **What is the most recent comparable study?** (Default: Same modality, same body region)
3. **Are outside studies available (CD, external PACS)?** (Default: Check for imported studies)
4. **What is the clinical question requiring comparison?** (Default: Disease progression, treatment response, post-operative change)
5. **Is this patient on a treatment protocol requiring interval measurement?** (Default: No — if yes, apply RECIST or relevant criteria)
6. **Are prior reports available (even without images)?** (Default: Check report archive)

### Documents to Request

- All prior imaging studies of the same body region (ideally same modality)
- Prior radiology reports with findings and measurements
- Outside imaging records (CDs, imported studies)
- Clinical notes documenting interim events (surgery, treatment, injury)
- Treatment timeline (chemotherapy cycles, radiation dates)
- Prior measurement tables (for oncologic tracking)

---

## Step 1: Identify and Prioritize Relevant Prior Studies

### Comparison Study Selection Hierarchy

| Priority | Study Type | Rationale |
|----------|-----------|-----------|
| 1st | Same modality, same protocol, most recent | Direct measurement comparison |
| 2nd | Same modality, different protocol, most recent | Comparable anatomy, note technique differences |
| 3rd | Different modality, same body region, most recent | Limited comparison; note modality differences |
| 4th | Same modality, older study | Useful for trend over time |
| 5th | Report only (no images available) | Rely on prior measurements/descriptions |

### Multi-Timepoint Comparison
For findings tracked over time, reference multiple timepoints:
- **Most recent prior** — for interval change
- **Baseline** — for overall trend and response assessment
- **Nadir** — for oncologic measurement (smallest recorded size)

Document: "Comparison: CT chest dated MM/DD/YYYY (most recent), CT chest dated MM/DD/YYYY (baseline). Additional reference: PET/CT dated MM/DD/YYYY."

---

## Step 2: Technique Comparison Assessment

Before comparing findings, document any technique differences that affect interpretation.

| Technical Factor | Impact on Comparison | Documentation |
|-----------------|---------------------|---------------|
| Contrast vs. non-contrast | Lesion conspicuity and measurement may differ | "Prior study was non-contrast; current study is contrast-enhanced — limited comparison for lesion enhancement" |
| Different contrast phase | Lesion size and appearance may differ | "Prior obtained in portal venous phase; current in arterial phase" |
| Slice thickness | Small lesions may not be detected on thicker slices | "Prior obtained with 5 mm slices; current with 1.25 mm — improved small-lesion detection" |
| Different modality | Measurement techniques differ (e.g., US vs. CT) | "Comparison with prior ultrasound is limited; CT provides more precise measurement" |
| Patient positioning | Affects organ appearance and measurement | "Prior obtained supine; current obtained prone" |
| Different scanner | Potential calibration differences | Generally not clinically significant; note if image quality differs markedly |
| Reconstruction algorithm | Lung kernel vs. soft tissue kernel affects measurements | "Measurements obtained on soft-tissue kernel for consistency" |

---

## Step 3: Standardized Interval Change Assessment

### Change Descriptors — Use Precise Language

| Descriptor | Definition | Measurement Requirement |
|-----------|-----------|----------------------|
| **New** | Not present on prior study | Confirm not present on all prior timepoints |
| **Resolved** | Previously present, now absent | Confirm absence on current study |
| **Increased/Enlarged** | Measurably larger | Provide measurements (prior and current) |
| **Decreased/Smaller** | Measurably smaller | Provide measurements (prior and current) |
| **Stable** | No significant change in size or character | Provide measurements confirming stability |
| **Unchanged** | Identical appearance | For qualitative findings (e.g., calcification pattern) |
| **Progressed** | Worsened (disease-specific context) | Provide measurements; specify criteria (e.g., RECIST) |
| **Improved** | Better (disease-specific context) | Provide measurements; specify criteria |
| **Interval development** | New finding since prior study | Equivalent to "new" — use consistently |

### Language to Avoid

| Avoid | Use Instead |
|-------|------------|
| "Grossly unchanged" | "Stable, measuring X mm (previously X mm)" |
| "Essentially similar" | "Unchanged in size at X mm" |
| "Cannot exclude interval change" | "Stable within measurement variability" or provide measurements |
| "Compared to prior" (no date) | "Compared to [modality] dated [MM/DD/YYYY]" |
| "As before" | "Stable compared to [date]" |
| "Similar" (without qualification) | "Similar in size, measuring X mm (previously Y mm)" |

---

## Step 4: Structured Comparison Documentation

### Per-Finding Comparison Format

For each significant finding, document:

```
[Finding]: [Current description], measuring [X mm], 
[change descriptor] compared to [prior study date] 
when it measured [Y mm] ([percentage change or absolute change]).
```

**Examples:**
```
Right upper lobe pulmonary nodule: Solid nodule measuring 12 mm, 
increased from 8 mm on CT dated 01/15/2025 (50% increase, 
interval 6 months). Per Fleischner Society criteria, 
recommend PET/CT or tissue sampling.
```

```
Hepatic cyst in segment 7: Simple cyst measuring 3.2 cm, 
stable compared to CT dated 06/10/2024 (3.1 cm). 
No follow-up required.
```

### Comparison Summary Table (for Multiple Findings)

| Finding | Location | Prior Date | Prior Size | Current Size | Change | Recommendation |
|---------|----------|-----------|-----------|-------------|--------|---------------|
| Lung nodule | RUL | 01/15/2025 | 8 mm | 12 mm | Increased (+50%) | PET/CT or biopsy |
| Hepatic cyst | Seg 7 | 06/10/2024 | 3.1 cm | 3.2 cm | Stable | No follow-up |
| Para-aortic LN | L2 level | 01/15/2025 | 14 mm SA | 10 mm SA | Decreased (-29%) | Continue surveillance |

---

## Step 5: Trending and Longitudinal Assessment

For findings tracked over multiple timepoints, provide a trend summary:

### Growth Rate Calculation (Pulmonary Nodules)
- Volume doubling time (VDT) is the gold standard for growth assessment
- VDT <400 days = suspicious for malignancy
- VDT >600 days = likely benign
- Formula: VDT = (t × ln2) / (3 × ln(d₂/d₁)), where t = time interval, d₁ = initial diameter, d₂ = current diameter

### Measurement Variability Thresholds
Not all size changes are clinically meaningful:

| Lesion Size | Clinically Meaningful Change | Rationale |
|-------------|----------------------------|-----------|
| <10 mm | ≥2 mm change | Measurement variability ~1.5 mm for small lesions |
| 10–30 mm | ≥3 mm change | ~10% variability |
| >30 mm | ≥5 mm or ≥20% change | Consistent with RECIST PD criteria |
| Lymph nodes | ≥2 mm short axis change | Standard variability |

If a size change falls within measurement variability, state: "Within expected measurement variability; recommend continued follow-up to establish trend."

---

## Checkpoint B: Post-Draft Alignment (Mandatory)

1. Are all comparison studies identified with specific dates and modalities?
2. Are technique differences documented that may affect comparison?
3. Does every significant finding have an explicit change descriptor with measurements?
4. Are measurements provided for both current and prior studies?
5. Is the comparison language specific and unambiguous?

---

## Quality Audit

- [ ] All reasonably available prior studies are identified and referenced with dates
- [ ] Most recent comparable study is used as the primary comparison
- [ ] Technique differences between studies are documented
- [ ] Every significant finding has an explicit interval change descriptor
- [ ] Measurements are provided for both current and prior timepoints
- [ ] Percentage and/or absolute change is calculated for measurable findings
- [ ] Standardized change language is used (not vague terms like "grossly unchanged")
- [ ] Multiple timepoints are referenced for trending when available
- [ ] New findings are confirmed absent on prior studies
- [ ] Resolved findings are confirmed absent on current study
- [ ] Measurement variability thresholds are applied (not over-interpreting small changes)
- [ ] Outside studies or reports are referenced when institutional priors are unavailable
- [ ] Comparison section of the report lists all comparison studies with dates and modalities
- [ ] Growth rate or volume doubling time is considered for nodule surveillance

---

## Guidelines

1. Always reference prior comparison studies with specific dates and modalities — "compared to prior" without a date is medicolegally insufficient.
2. Provide measurements for both the current and prior study when describing interval change — "increased" without numbers is not actionable.
3. Account for technique differences before concluding interval change; a lesion may appear larger simply due to different contrast timing or slice thickness.
4. Use standardized interval-change descriptors consistently throughout the report.
5. When priors are unavailable, state "No prior comparison available" and recommend comparison on follow-up; do not guess at stability.
6. For oncologic surveillance, reference both the most recent prior (for interval change) and the baseline (for overall response assessment).
7. Apply measurement-variability thresholds — a 1 mm change in a 6 mm nodule is within measurement error, not true growth.
8. When outside imaging is referenced by report only (no images available), state "Per prior report dated [date] from [institution]" and note that direct image comparison was not possible.
