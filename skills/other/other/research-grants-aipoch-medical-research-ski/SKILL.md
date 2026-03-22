---
name: research-grants
description: Write competitive research proposals for NSF, NIH, DOE, DARPA, and Taiwan's NSTC when you need agency-compliant narratives, budgets, and review-criteria alignment for a specific solicitation/FOA/BAA.
license: MIT
skill-author: AIPOCH
---

## When to Use

Use this skill when you need to produce or revise a grant application that must meet strict agency rules and reviewer expectations, for example:

1. **Preparing a new submission** to NSF, NIH, DOE, DARPA, or Taiwan’s NSTC in response to a specific solicitation/FOA/BAA.
2. **Drafting core narrative sections** (NSF Project Description, NIH Research Strategy, DARPA Technical Volume, DOE Project Narrative, NSTC CM03).
3. **Building agency-specific “value” sections**, such as NSF Broader Impacts, NIH Significance/Innovation, or DARPA transition and milestone narratives.
4. **Creating a compliant budget + justification** aligned to scope, timeline, and agency constraints (e.g., NIH modular budgets, DARPA phase/task budgets).
5. **Resubmitting after reviews**, including structured responses to critiques (especially NIH A1) and targeted strengthening of weak criteria.

## Key Features

- **Agency-aware structure and compliance**
  - NSF: Intellectual Merit + Broader Impacts, typical 15-page Project Description norms
  - NIH: Specific Aims + Significance/Innovation/Approach framing, rigor/reproducibility expectations
  - DOE: office-dependent emphasis (Office of Science, ARPA-E, EERE), partnerships/cost-share where applicable
  - DARPA: high-risk/high-reward framing, measurable milestones, transition pathways, phased execution
  - NSTC (Taiwan): CM03-centered technical narrative, bilingual abstract expectations, feasibility emphasis

- **Review-criteria-driven writing**
  - Maps every major claim to what reviewers score (or discuss) and what program staff prioritize.

- **Budget-to-scope alignment**
  - Ensures personnel effort, equipment, travel, subawards, and indirects match the workplan and schedule.

- **Milestones, timeline, and management planning**
  - Produces Gantt-style schedules, go/no-go criteria, deliverables, and risk mitigation (especially important for DARPA/DOE).

- **Mandatory visual communication workflow**
  - Every proposal should include **at least 1–2 diagrams** (e.g., workflow, conceptual framework, timeline). Use the `scientific-schematics` skill to generate publication-quality figures.

- **Reference-driven drafting**
  - Leverages the repository’s detailed guides as needed:
    - `references/nsf_guidelines.md`
    - `references/nih_guidelines.md`
    - `references/doe_guidelines.md`
    - `references/darpa_guidelines.md`
    - `references/nstc_guidelines.md`
    - `references/specific_aims_guide.md`
    - `references/broader_impacts.md`
    - `references/budget_preparation.md`
    - `references/review_criteria.md`
    - `references/timeline_planning.md`
    - `references/team_building.md`
    - `references/resubmission_strategies.md`

## Dependencies

- **Python**: 3.10+ (recommended)
- **Optional local scripts (repository-provided)**:
  - `scripts/compliance_checker.py` (format checks)
  - `scripts/budget_calculator.py` (budget math support)
  - `scripts/deadline_tracker.py` (planning support)
  - `scripts/generate_schematic.py` (diagram generation wrapper; used with `scientific-schematics`)

> Note: Exact third-party Python package requirements are not specified in the source document. If you maintain this skill repository, add a `requirements.txt` (with pinned versions) and list them here.

## Example Usage

The example below is a complete, runnable workflow that (1) generates required visuals, (2) drafts core sections, and (3) performs basic compliance checks using the included scripts.

### 1) Generate required diagrams (minimum 1–2)

```bash
# Conceptual framework / workflow diagram
python scripts/generate_schematic.py \
  "Conceptual workflow for a 3-aim biomedical project: Aim 1 data collection -> Aim 2 model development -> Aim 3 validation; include feedback loop and key deliverables" \
  -o figures/workflow.png

# Timeline / milestones diagram (recommended)
python scripts/generate_schematic.py \
  "Gantt chart for a 3-year project with quarterly milestones; include go/no-go at end of Year 1 and deliverables per aim" \
  -o figures/timeline.png
```

### 2) Draft an NIH-style proposal skeleton (Specific Aims + Strategy)

Create `proposal.md`:

```markdown
# Project Title
Mechanistic and Translational Study of X to Enable Y

## NIH Specific Aims (1 page target)
**Knowledge gap:** ...
**Long-term goal:** ...
**Objective:** ...
**Central hypothesis:** ...

**Aim 1 (verb-led):** ...
- Rationale:
- Approach (high level):
- Expected outcomes:

**Aim 2:** ...
**Aim 3:** ...

**Impact:** If successful, this work will ...

## Research Strategy (12 pages target for R01)

### Significance
- Problem and barrier to progress:
- Why now / why this team:
- Expected impact on health/biology:

### Innovation
- Conceptual innovation:
- Methodological innovation:
- Why current approaches are insufficient:

### Approach
#### Overview and rationale
#### Aim 1 Methods
- Design:
- Data:
- Analysis:
- Pitfalls and alternatives:
#### Aim 2 Methods
...
#### Aim 3 Methods
...

### Rigor and Reproducibility (as applicable)
- Controls, replicates, blinding/randomization:
- Power/statistics:
- Data management and sharing:
```

### 3) Run a basic formatting/compliance check (if available)

```bash
python scripts/compliance_checker.py proposal.md
```

### 4) Produce a budget justification draft (outline)

Create `budget_justification.md`:

```markdown
# Budget Justification (Draft)

## Personnel
- PI (X% effort): ...
- Postdoc (100%): ...
- Graduate student (50%): ...

## Equipment
- Item: purpose, necessity, and timing

## Travel
- Conference dissemination
- Collaboration meetings

## Materials and Supplies
- Consumables / software licenses

## Other Direct Costs
- Publication fees / participant incentives / consultants

## Subawards (if any)
- Scope and deliverables per partner

## Indirect Costs (F&A)
- Rate and base per institutional policy
```

## Implementation Details

### 1) Agency-specific narrative mapping (what to write, where, and why)

- **NSF**
  - Two equal pillars: **Intellectual Merit** and **Broader Impacts**
  - Typical narrative pattern: problem → gap → approach → feasibility → outcomes → impacts
  - Ensure Broader Impacts are **specific, measurable, resourced, and scheduled** (not “bolt-on”).

- **NIH**
  - Core scored criteria: **Significance, Investigator(s), Innovation, Approach, Environment**
  - The **Specific Aims page** is the highest-leverage page: 2–4 aims, independent-but-complementary, each feasible with contingencies.
  - Approach must explicitly address **rigor, reproducibility, and risk mitigation**.

- **DOE**
  - Criteria vary by office; common expectations:
    - technical merit, mission relevance, team capability, facilities, and budget reasonableness
  - Often values **integration of computation + experiment**, partnerships, and (sometimes) cost share.

- **DARPA**
  - Emphasize: **transformative payoff**, measurable milestones, and transition.
  - Use phased plans with **deliverables, metrics, and go/no-go criteria**.
  - Answer DARPA-style questions in substance:
    - *What if it works? Who cares? How will it transition?*

- **NSTC (Taiwan)**
  - CM03 is central; feasibility and preliminary evidence are critical.
  - Plan for **bilingual abstracts** and include a clear **research architecture diagram**.

### 2) Visual requirement (mandatory minimum)

- Include **at least 1–2 diagrams**:
  - Workflow/method schematic (reduces reviewer cognitive load)
  - Timeline/Gantt with milestones and decision points
- Use consistent labeling, readable fonts, and captions that allow the figure to stand alone.

### 3) Milestones and risk control parameters

- Define milestones that are:
  - **Measurable** (metric + threshold)
  - **Time-bound** (quarter/year)
  - **Decision-linked** (go/no-go or pivot criteria)
- For each major risk, include:
  - failure mode → detection signal → mitigation → fallback method

### 4) Budget-to-workplan consistency checks

- Every major task should map to:
  - named personnel effort
  - required equipment/supplies
  - travel (if collaboration/fieldwork is claimed)
  - subaward scope (if partners are essential)
- Common rejection trigger: a narrative that promises outcomes without resourcing them in the budget.

### 5) Resubmission mechanics (especially NIH A1)

- Create a 1-page **Introduction to Resubmission** that:
  - lists major critiques
  - states exactly what changed and where
  - remains factual and respectful
- Strengthen the weakest scored criterion first (often Approach or Innovation), then tighten alignment across aims, methods, and milestones.