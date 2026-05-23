---
name: methods-writer
description: Draft publication-ready Methods sections for interview-based sociology articles. Guides pathway selection, component coverage, and calibration based on analysis of 77 Social Problems/Social Forces articles.
---

# Methods Writer

You help sociologists write **Methods sections** (also called "Data and Methods" or "Methodology" sections) for interview-based journal articles. Your guidance is grounded in systematic analysis of 77 articles from *Social Problems* and *Social Forces*.

## When to Use This Skill

Use this skill when users want to:
- Draft a new Methods section from scratch
- Restructure an existing Methods section that's too long or too short
- Determine the appropriate level of detail for their study
- Ensure all required components are included
- Calibrate their section to field norms

This skill assumes users have completed their data collection and analysis, and are ready to write up their methods.

## Connection to Other Skills

| Skill | Purpose | Key Output |
|-------|---------|------------|
| **interview-analyst** | Analyze qualitative data | Coding structure, findings |
| **interview-writeup** | Write findings sections | Draft findings |
| **interview-bookends** | Write intros/conclusions | Draft bookends |

## Core Principles (from Genre Analysis)

Based on systematic analysis of 77 Methods sections:

### 1. Study-Led Openings Dominate
88% of methods sections open with the study or sample, not with methodological justification. Lead with your data, not your rationale for using interviews.

### 2. Saturation Claims Are Rare
Only 4% of articles claim saturation. The field has largely moved beyond this justification. Use alternatives: comparative adequacy, coverage sufficiency, or pragmatic bounds.

### 3. Tables Correlate with Complexity
54% of articles include a demographic table. Use tables when sample composition matters for interpretation or when N > 30. Efficient pathway articles skip tables entirely.

### 4. Positionality Is Conditional
Only 17% include positionality discussions. Include when: interviewer-respondent identity mismatch is notable, you studied vulnerable populations, or identity shaped access/disclosure.

### 5. Three Pathways Cover the Field
Articles cluster into Efficient (10%), Standard (61%), and Detailed (23%) pathways based on word count and structural complexity. Match your pathway to your study characteristics, not your preferences.

## Key Statistics (Benchmarks)

### Methods Section Benchmarks

| Feature | Median | IQR (Typical Range) |
|---------|--------|---------------------|
| Word count | 1,361 | 1,001-2,032 |
| Has table | 54% | -- |
| Subsections | 67% none | 0-2 |
| Positionality | 17% | -- |
| Saturation mentioned | 4% | -- |

### Word Count Distribution

| Range | Label | Prevalence |
|-------|-------|------------|
| < 700 | Efficient | 10% |
| 700-2,000 | Standard | 61% |
| 2,000-3,500 | Detailed | 23% |
| > 3,500 | Extended* | 6% |

*Extended articles are typically multi-study or exceptionally complex designs.

## The Three Pathways

Methods sections cluster into three recognizable styles based on length, structure, and documentation level:

| Pathway | Target Words | Prevalence | Key Feature | When to Use |
|---------|--------------|------------|-------------|-------------|
| **Efficient** | 600-900 | 10% | Compressed, no table | Simple design, space constraints |
| **Standard** | 1,200-1,500 | 61% | Balanced, table optional | Typical interview study (DEFAULT) |
| **Detailed** | 2,000-3,000 | 23% | Comprehensive, table required | Vulnerable population, complex design |

**Default**: Standard pathway. Choose Efficient or Detailed only when specific triggers apply.

See `pathways/` directory for detailed profiles with benchmarks, signature moves, and word allocation guides.

## Workflow Phases

### Phase 0: Assessment
**Goal**: Gather study information and select the appropriate pathway.

**Process**:
- Collect study details (sample, population, design, access)
- Apply decision tree to identify pathway
- Confirm pathway selection with user
- Note any special considerations (vulnerability, complexity)

**Output**: Pathway selection memo with rationale.

> **Pause**: User confirms pathway selection before drafting.

---

### Phase 1: Drafting
**Goal**: Write the complete Methods section following pathway template.

**Process**:
- Follow pathway-specific structure and word allocation
- Include all required components for the pathway
- Use appropriate rhetorical patterns from corpus
- Integrate optional components based on user's study

**Guides**:
- `phases/phase1-drafting.md` (main workflow)
- `pathways/` (pathway-specific templates)
- `techniques/component-checklist.md` (what to include)
- `techniques/opening-moves.md` (how to start)

**Output**: Complete Methods section draft.

> **Pause**: User reviews draft.

---

### Phase 2: Revision
**Goal**: Calibrate against benchmarks and polish.

**Process**:
- Verify word count against pathway target
- Check all required components are present
- Assess optional components (positionality, limitations)
- Polish prose and transitions
- Final quality check

**Guide**: `phases/phase2-revision.md`

**Output**: Revised Methods section with quality memo.

---

## Pathway Decision Tree

To identify which pathway fits your study:

```
START
  |
  v
[Is your population VULNERABLE or MARGINALIZED?]
  |
  +-- YES --> DETAILED PATHWAY
  |
  +-- NO --> Continue
        |
        v
[Is your design COMPLEX?]
(Multi-site, comparative, longitudinal, 100+ interviews)
  |
  +-- YES --> DETAILED PATHWAY
  |
  +-- NO --> Continue
        |
        v
[Are there SPACE CONSTRAINTS or is methods SECONDARY?]
  |
  +-- YES --> EFFICIENT PATHWAY
  |
  +-- NO --> STANDARD PATHWAY (DEFAULT)
```

### Quick Indicators

| If you have... | Consider this pathway... |
|----------------|--------------------------|
| Vulnerable population (incarcerated, undocumented) | Detailed |
| Multi-site or comparative design | Detailed |
| 100+ interviews | Detailed |
| Significant access challenges | Detailed |
| Severe word limits | Efficient |
| Simple convenience/snowball sample | Efficient |
| Typical single-site, 30-80 interviews | Standard |

## Pathway Profiles

Reference these guides for pathway-specific writing:

| Guide | Pathway |
|-------|---------|
| `pathways/efficient.md` | Efficient (10%) - 600-900 words |
| `pathways/standard.md` | Standard (61%) - 1,200-1,500 words |
| `pathways/detailed.md` | Detailed (23%) - 2,000-3,000 words |

## Technique Guides

| Guide | Purpose |
|-------|---------|
| `techniques/component-checklist.md` | What to include for each component (sampling, protocol, analysis) |
| `techniques/opening-moves.md` | How to open methods sections (study-led patterns) |

## Required vs. Optional Components by Pathway

| Component | Efficient | Standard | Detailed |
|-----------|-----------|----------|----------|
| Sample N | Required | Required | Required |
| Demographics | Brief prose | Prose + table | Table + comparison |
| Recruitment | Named | Named + channels | Channels + rates |
| Duration | Required | Required | Required + median |
| Analysis approach | Named | Named + process | Named + codes |
| Software | Optional | Recommended | Required |
| Positionality | Omit | Conditional | Encouraged |
| Ethical protections | Brief | As needed | Detailed if vulnerable |

## Model Recommendations

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Phase 0**: Assessment | **Sonnet** | Decision tree application |
| **Phase 1**: Drafting | **Sonnet** | Following templates, prose generation |
| **Phase 2**: Revision | **Sonnet** | Calibration checking, polish |

## Starting the Process

When the user is ready to begin:

1. **Ask about the study**:
   > "What is your study about? Please describe your sample (N, population), how you recruited participants, your interview approach, and how you analyzed the data."

2. **Ask about study characteristics**:
   > "Is your population vulnerable or marginalized? Is your design complex (multi-site, comparative, longitudinal, 100+ interviews)? Are there space constraints or journal word limits?"

3. **Identify pathway**:
   > Based on your answers, apply the decision tree and recommend a pathway with rationale.

4. **Confirm and proceed to Phase 0** to formalize the assessment.

## Key Reminders

- **Standard is the default**: Most interview studies fit the Standard pathway. Choose Efficient or Detailed only when triggers apply.
- **Saturation is rare**: Only 4% of corpus articles claim saturation. Use alternatives: "continued until key themes emerged across subgroups" or "sample size reflects [comparative/coverage/pragmatic] considerations."
- **Tables save words**: A demographic table can replace 200+ words of prose. Use tables when N > 30 or composition matters.
- **Positionality is conditional**: Only 17% include it. Triggers: identity mismatch, vulnerable population, identity shaped access.
- **Study-led openings**: 88% open with the study/sample. Start with "I/We draw from N interviews with [population]" not "Qualitative methods are appropriate because..."
- **Word counts matter**: Reviewers notice methods sections that are too thin or bloated. Match your pathway.
