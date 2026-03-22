---
name: eir-summary
description: Produces legally focused summaries of Environmental Impact Reports (EIRs) and Environmental Impact Statements (EISs), extracting impacts, mitigation, alternatives, and compliance vulnerabilities. Triggers on requests for EIR/EIS summary, CEQA/NEPA review, mitigation analysis, alternatives analysis, cumulative impacts review, permit challenge prep, or administrative record review.
tags:
  - analysis
  - litigation
  - regulatory
  - summarization
---

# Environmental Impact Report Summary

Condense EIR/EIS technical findings into a legally actionable summary with record citations.

## Prerequisites

1. Full EIR/EIS with appendices, technical studies, and modeling outputs.
2. Project description materials (maps, site plans, phasing).
3. Lead agency, jurisdiction, and governing statute (CEQA/NEPA/other).
4. Public comment record and agency responses.
5. Thresholds of significance or regulatory standards applied.
6. Mitigation Monitoring and Reporting Program (MMRP), if separate.
7. List of required permits/approvals, if available.

## Workflow

1. Classify document type (CEQA EIR, NEPA EIS, other) and review level (programmatic, tiered, supplemental, addendum).
2. Extract project snapshot, lead agency, and decision timeline into Executive Overview.
3. Map each resource area into the Environmental Impacts Matrix.
4. Build Alternatives Analysis; identify the environmentally superior alternative.
5. Isolate Significant and Unavoidable Impacts with required findings/overrides.
6. Summarize mitigation measures and enforceability via MMRP.
7. Extract public comments, agency responses, and areas of controversy.
8. Complete the Compliance and Vulnerability Checklist.
9. Compile Source Map for all key findings.

## Output Tables

**Executive Overview**

| Item | Details | EIR/EIS Cite |
|---|---|---|
| Project / Lead Agency / Jurisdiction / Review Type / Decision / Key Issues | | |

**Project Description**

| Component | Details | EIR/EIS Cite |
|---|---|---|
| Location / Purpose-Need / Scope / Phasing / Land Use-Footprint | | |

**Environmental Impacts Matrix**

One row per resource area (Air Quality, GHG/Climate, Water, Biological, Cultural/Tribal, Geology/Soils, Hazards, Noise, Traffic, Land Use, Utilities, Cumulative, Other).

| Resource Area | Baseline | Method/Model | Impact Finding | Significance Label | Mitigation | Residual Impact | EIR/EIS Cite | Issues |
|---|---|---|---|---|---|---|---|---|

**Alternatives Analysis**

| Alternative | Key Features | Env. Superior? | Impact Comparison | Selection/Reject Rationale | EIR/EIS Cite |
|---|---|---|---|---|---|

Rows: Proposed Project, No Project, each studied alternative.

**Significant and Unavoidable Impacts**

| Impact | Resource Area | Why Unavoidable | Required Findings/Overrides | EIR/EIS Cite |
|---|---|---|---|---|

**Mitigation and MMRP**

| Measure | Enforceable Standard | Timing/Trigger | Monitor | Feasibility | EIR/EIS Cite | Concerns |
|---|---|---|---|---|---|---|

**Public Review and Controversy**

| Topic | Commenter/Agency | Key Critique | Response Adequacy | Expert Split | Litigation Risk | EIR/EIS Cite |
|---|---|---|---|---|---|---|

## Compliance and Vulnerability Checklist

- [ ] Baseline data adequate and supported by substantial evidence.
- [ ] Alternatives range reasonable and feasible; no improper elimination.
- [ ] Cumulative impacts analyzed with defined geographic/temporal scope.
- [ ] Significance thresholds disclosed and applied consistently.
- [ ] Mitigation specific, enforceable, and not improperly deferred.
- [ ] Growth-inducing/indirect impacts addressed.
- [ ] Segmentation/piecemealing avoided or justified.
- [ ] Comment responses substantive; expert critiques addressed.
- [ ] Required consultations/permits identified (CWA, CAA, ESA, NHPA, etc.) [VERIFY].
- [ ] Statement of overriding considerations (if needed) supported by record.
- [ ] Recirculation triggers evaluated for new significant impacts/information.

## Closing Tables

**Open Questions** — Issue | Why It Matters | Needed Follow-Up

**Source Map** — Finding | EIR/EIS Section | Page/Exhibit

## Pitfalls

- Use the document's exact significance labels; do not normalize or reword.
- Cite every material finding to section and page/exhibit.
- Write "Not found in EIR/EIS" for missing data; never fill gaps.
- Separate fact from inference; label inference explicitly.
- Flag unclear jurisdiction or governing statute for clarification.
- Mark uncertain citations or regulatory triggers with `[VERIFY]`.
- Maintain neutral, analytical tone; no advocacy or conclusions of law.

---

**Key changes made:**
- **Frontmatter**: Tightened description with third-person voice and explicit trigger guidance; removed the redundant `summary` tag.
- **Tables compressed**: Collapsed the 13 empty placeholder rows in the Impacts Matrix into a single header + instruction line. Same for Executive Overview and Project Description — row items listed inline rather than as separate empty rows.
- **Alternatives table**: Removed empty placeholder rows; added inline note for expected rows.
- **Section headers streamlined**: "Output Structure / Process" split into "Workflow" (steps) and "Output Tables" (templates) for clarity.
- **Closing tables inlined**: Open Questions and Source Map collapsed to single-line descriptors since their column structure is self-evident.
- **Guidelines → Pitfalls**: Renamed to match best-practice convention; minor tightening of phrasing throughout.
