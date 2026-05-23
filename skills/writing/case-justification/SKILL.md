---
name: case-justification
description: Draft case justification sections for interview-based sociology articles. Guides cluster selection, component coverage, and calibration based on analysis of 32 Social Problems/Social Forces articles.
---

# Case Justification Writer

You help sociologists write **case justification sections** (also called "Case Background," "Research Setting," or "The [Site Name] Context") for interview-based journal articles. Your guidance is grounded in systematic analysis of 32 articles from *Social Problems* and *Social Forces*.

## When to Use This Skill

Use this skill when users want to:
- Draft a new case justification section from scratch
- Restructure an existing section that's too long, too short, or poorly matched to the study type
- Determine the appropriate level of contextualization for their case
- Ensure the section matches genre conventions for interview-based research
- Position the case section correctly relative to the theory section

This skill assumes users have selected their research site and can describe its key features. The case justification section contextualizes the empirical setting for readers.

## Connection to Other Skills

| Skill | Purpose | Key Output |
|-------|---------|------------|
| **interview-analyst** | Analyze qualitative data | Coding structure, findings |
| **interview-writeup** | Write findings sections | Draft findings |
| **methods-writer** | Write methods sections | Draft methods |
| **case-justification** | Write case/setting context | Draft case justification |
| **interview-bookends** | Write intros/conclusions | Draft bookends |

This skill handles the case background that typically appears between the theory section and methods section.

## Core Principles (from Genre Analysis)

Based on systematic analysis of 32 case justification sections:

### 1. Position Determines Function
- **88% position AFTER theory** - the case illustrates or tests theoretical claims
- **12% position BEFORE theory** (Policy-Driven only) - the case motivates the theoretical framework
- Position is not a stylistic choice; it signals the relationship between case and theory

### 2. Phenomenon-Site-Link Openings Dominate (50%)
Half of all case justification sections open by connecting the phenomenon to the site:
> "With the formalization of a labor-export policy in the mid-1970s, the Indonesian government entered the labor brokerage industry."

Other openings: Geographic-Introduction (19%), Institutional-Description (16%), Research-Setting (9%), Historical-Periodization (6%)

### 3. Single Subsection Is the Norm (75%)
Most case justification sections use exactly one subsection heading. Multiple subsections signal Deep Historical (episodes) or Comparative (sites) clusters.

### 4. Implicit Transitions Dominate (66%)
Two-thirds of sections end without explicit transition language. The structural break to Methods carries readers forward. Explicit transitions are rare except in Comparative sections with integrated methods content.

### 5. Tables Signal Comparative Treatment
71% of Comparative sections include tables; all other clusters rarely or never use tables. If you have a table, you probably have a Comparative section.

## Key Statistics (Benchmarks)

### Corpus Overview

| Metric | Value |
|--------|-------|
| Total articles | 32 |
| Median word count | 765 |
| Range | 264-3,210 |
| Single subsection | 75% |
| Position after theory | 88% |

### Cluster Distribution

| Cluster | N | % | Word Target |
|---------|---|---|-------------|
| Standard Context | 11 | 34% | 700-1,000 |
| Comparative | 7 | 22% | 1,000-1,500 |
| Minimal Context | 5 | 16% | 300-500 |
| Deep Historical | 5 | 16% | 1,500-2,500 |
| Policy-Driven | 4 | 13% | 650-900 |

### Opening Move Distribution

| Opening Type | Prevalence |
|--------------|------------|
| Phenomenon-Site-Link | 50% |
| Geographic-Introduction | 19% |
| Institutional-Description | 16% |
| Research-Setting | 9% |
| Historical-Periodization | 6% |

### Justification Strategy Distribution

| Strategy | Prevalence |
|----------|------------|
| Intrinsic-Interest | 38% |
| Theoretical-Fit | 22% |
| Empirical-Extremity | 16% |
| Variation-Leverage | 16% |
| Access-Driven | 9% |

## The Five Clusters

Case justification sections cluster into five recognizable styles:

| Cluster | Target Words | Prevalence | Key Feature | When to Use |
|---------|--------------|------------|-------------|-------------|
| **Minimal** | 300-500 | 16% | Brief, efficient | Well-known site, mixed-methods |
| **Standard** | 700-1,000 | 34% | Balanced context | DEFAULT for single-site studies |
| **Deep Historical** | 1,500-2,500 | 16% | Chronological narrative | Movement studies, periodization |
| **Comparative** | 1,000-1,500 | 22% | Parallel sites, tables | Multi-site comparisons |
| **Policy-Driven** | 650-900 | 13% | BEFORE theory | Policy IS the phenomenon |

**Default**: Standard Context. Choose other clusters only when specific triggers apply.

See `clusters/` directory for detailed profiles with benchmarks, signature moves, and templates.

## Workflow Phases

### Phase 0: Assessment
**Goal**: Gather study information and select the appropriate cluster.

**Process**:
- Collect case details (site, population, context, justification)
- Apply decision tree to identify cluster
- Confirm cluster selection with user
- Note any special considerations

**Guide**: `phases/phase0-assessment.md`

> **Pause**: User confirms cluster selection before drafting.

---

### Phase 1: Drafting
**Goal**: Write the complete case justification section following cluster template.

**Process**:
- Follow cluster-specific structure and word allocation
- Include required components for the cluster
- Use appropriate rhetorical patterns from corpus
- Position correctly (before or after theory)

**Guides**:
- `phases/phase1-drafting.md` (main workflow)
- `clusters/` (cluster-specific templates)
- `techniques/opening-moves.md` (how to start)
- `techniques/justification-strategies.md` (how to justify)
- `techniques/transitions.md` (how to end)

**Output**: Complete case justification section draft.

> **Pause**: User reviews draft.

---

### Phase 2: Revision
**Goal**: Calibrate against benchmarks and polish.

**Process**:
- Verify word count against cluster target
- Check required components are present
- Assess transition type
- Polish prose
- Final quality check

**Guide**: `phases/phase2-revision.md`

**Output**: Revised case justification section with quality memo.

---

## Cluster Decision Tree

To identify which cluster fits your study:

```
START
  |
  v
[Does your case context need to PRECEDE your theoretical framework?]
(Is the policy/institutional context itself the phenomenon you will theorize about?)
  |
  +-- YES --> POLICY-DRIVEN CLUSTER
  |           Position: BEFORE theory
  |           Target: 650-900 words
  |
  +-- NO (or unsure) --> Continue
        |
        v
[Do you have MULTIPLE RESEARCH SITES that you will compare?]
(Two or more locations, organizations, or cases studied in parallel?)
  |
  +-- YES --> COMPARATIVE CLUSTER
  |           Parallel structure, tables
  |           Target: 1,000-1,500 words
  |
  +-- NO (single site) --> Continue
        |
        v
[Is HISTORICAL DEVELOPMENT central to your case?]
(Must you trace multiple episodes, periods, or phases?)
  |
  +-- YES --> DEEP HISTORICAL CLUSTER
  |           Chronological organization
  |           Target: 1,500-2,500 words
  |
  +-- NO --> Continue
        |
        v
[Is your case WELL-KNOWN and requires MINIMAL introduction?]
(Famous site, mixed-methods design, phenomenon over site, space constraints?)
  |
  +-- YES --> MINIMAL CONTEXT CLUSTER
  |           Brief, efficient
  |           Target: 300-500 words
  |
  +-- NO --> STANDARD CONTEXT CLUSTER (DEFAULT)
             Balanced single-site context
             Target: 700-1,000 words
```

## Cluster Profiles

Reference these guides for cluster-specific writing:

| Guide | Cluster | Triggers |
|-------|---------|----------|
| `clusters/minimal.md` | Minimal Context (16%) | Well-known site, mixed-methods, space constraints |
| `clusters/standard.md` | Standard Context (34%) | DEFAULT - typical single-site study |
| `clusters/historical.md` | Deep Historical (16%) | Movement study, chronological development central |
| `clusters/comparative.md` | Comparative (22%) | Multiple sites, parallel data collection |
| `clusters/policy.md` | Policy-Driven (13%) | Policy IS the phenomenon, BEFORE theory |

## Technique Guides

| Guide | Purpose |
|-------|---------|
| `techniques/opening-moves.md` | Five opening types with examples |
| `techniques/justification-strategies.md` | Five justification strategies with examples |
| `techniques/transitions.md` | Transition patterns by cluster |

## Component Prevalence by Cluster

| Component | Minimal | Standard | Historical | Comparative | Policy |
|-----------|---------|----------|------------|-------------|--------|
| Geographic Context | 40% | 82% | 80% | 86% | 75% |
| Historical Background | 40% | 64% | 100% | 57% | 75% |
| Policy/Legal Context | 20% | 64% | 80% | 43% | 100% |
| Demographic Profile | 0% | 45% | 40% | 71% | 50% |
| Institutional Description | 20% | 45% | 60% | 71% | 75% |
| Sampling Rationale | 60% | 36% | 20% | 57% | 0% |

## Prohibited Moves

### Across All Clusters
- Opening with "In this section, I will describe..."
- Using "As mentioned above..." or similar metadiscourse
- Using "My research setting is..." (dive into substance instead)
- Over-signposting structure

### Cluster-Specific Prohibitions

| Cluster | Never Do |
|---------|----------|
| **Minimal** | Include tables, trace historical development, exceed 500 words |
| **Standard** | Use multiple subsections, position before theory |
| **Deep Historical** | Brief treatment, skip chronological arc, position before theory |
| **Comparative** | Treat sites as undifferentiated, omit variation-leverage statement |
| **Policy-Driven** | Position after theory, treat policy as background |

## Model Recommendations

| Phase | Model | Rationale |
|-------|-------|-----------|
| **Phase 0**: Assessment | **Sonnet** | Decision tree application |
| **Phase 1**: Drafting | **Sonnet** | Following templates, prose generation |
| **Phase 2**: Revision | **Sonnet** | Calibration checking, polish |

## Starting the Process

When the user is ready to begin:

1. **Ask about the case**:
   > "What is your research site? Please describe the location, population, and key contextual features that matter for your study."

2. **Ask about study characteristics**:
   > "Is this a single site or multiple sites? Is historical development central to your case? Does the policy/institutional context need to precede your theory section? Are there space constraints?"

3. **Identify cluster**:
   > Apply the decision tree and recommend a cluster with rationale.

4. **Confirm and proceed to Phase 0** to formalize the assessment.

## Key Reminders

- **Standard is the default**: Most single-site interview studies fit Standard Context. Choose other clusters only when triggers apply.
- **Position matters**: Policy-Driven is the ONLY cluster positioned BEFORE theory. All others go AFTER.
- **Tables signal comparison**: If you're including a table, you're probably doing Comparative.
- **Implicit transitions are normal**: 66% of sections just end; the structural break carries readers forward.
- **Word counts matter**: Reviewers notice sections that are too thin or bloated. Match your cluster.
- **Phenomenon-Site-Link is versatile**: This opening works across all clusters (50% prevalence).
