---
name: create-research-brief
version: "2.0"
description: Two-phase research design and consolidation skill for multi-LLM optimized research
triggers:
  - "create research brief"
  - "design research strategy"
  - "decompose research question"
  - "multi-model research"
  - "consolidate research findings"
  - "research synthesis"
---

# Create Research Brief

A comprehensive two-phase skill for designing multi-LLM research strategies (Phase 1) and consolidating multi-model outputs into actionable intelligence (Phase 2).

---

## 1. Purpose

This skill provides 9 core capabilities:

| # | Capability | Phase | Description |
|---|------------|-------|-------------|
| 1 | **Decompose** | 1 | Break research questions into MECE structures |
| 2 | **Assign** | 1 | Map question categories to optimal LLMs |
| 3 | **Assess** | 1 | Evaluate research risks at appropriate depth |
| 4 | **Generate** | 1 | Produce model-specific optimized prompts |
| 5 | **Consolidate** | 2 | Synthesize multi-model outputs into unified findings |
| 6 | **Resolve** | 2 | Handle conflicting information with WWHTBT protocol |
| 7 | **Classify** | 2 | Score evidence quality and tag uncertainty types |
| 8 | **Detect** | 2 | Identify coverage gaps and unknown unknowns |
| 9 | **Produce** | 2 | Generate tiered, decision-ready research reports |

---

## Checkpoints

This skill uses interactive checkpoints (see `references/checkpoints.yaml`) to resolve ambiguity:
- **research_type_classification** — When research type is ambiguous
- **risk_depth_selection** — When risk assessment depth not specified
- **model_mode_selection** — When model execution mode not specified
- **hypothesis_priors_required** — When multi_hypothesis enabled but priors missing
- **conflict_resolution_approach** — When model outputs have significant conflicts (Phase 2)

---

## 2. Two-Phase Workflow

### Phase 1: Research Design (Before Research)

| Step | Action | Output |
|------|--------|--------|
| 1 | **Validate Objective** | Confirm research question is answerable |
| 2 | **Classify Research Type** | market \| competitive \| technology \| strategic |
|   | **CHECKPOINT: research_type_classification** | If type ambiguous: AskUserQuestion |
| 3 | **Define Scope** | In-scope, out-of-scope, boundaries |
| 4 | **Select MECE Pattern** | 5-category decomposition structure |
| 5 | **Generate Sub-Questions** | 3-4 questions per category |
| 6 | **Assess Risks** | Quick \| Standard \| Comprehensive |
|   | **CHECKPOINT: risk_depth_selection** | If depth not specified: AskUserQuestion |
| 7 | **Assign Models** | Map categories to Claude/Gemini/GPT |
|   | **CHECKPOINT: model_mode_selection** | If mode not specified: AskUserQuestion |
| 8 | **Frame Hypotheses** | If `multi_hypothesis=true` |
|   | **CHECKPOINT: hypothesis_priors_required** | If priors missing: AskUserQuestion |
| 9 | **Recommend Expert Panel** | If `expert_panel=true` |
| 10 | **Produce Research Brief** | XML-structured Phase 1 deliverable |

### Phase 2: Consolidation (After Research)

| Step | Action | Output |
|------|--------|--------|
| 1 | **Ingest Model Outputs** | Parse all LLM research results |
| 2 | **Score Evidence** | Apply 5-point Evidence Strength Rubric |
| 3 | **Detect Conflicts** | Identify where models disagree |
| 4 | **Resolve Conflicts** | Apply WWHTBT for unresolved |
| 5 | **Classify Uncertainty** | Tag as epistemic/aleatory/model |
| 6 | **Audit MECE Coverage** | Check for coverage gaps |
| 7 | **Probe Unknown Unknowns** | Run 5 discovery probes |
| 8 | **Tier Findings** | Assign to Tier 1/2/3 by confidence |
| 9 | **Build Decision Support** | Create if-then decision tree |
| 10 | **Define Kill Criteria** | Conditions that invalidate research |
| 11 | **Produce Report** | XML-structured Phase 2 deliverable |

---

## 3. Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `research_objective` | string | *required* | The core research question or goal |
| `research_type` | enum | `market` | market \| competitive \| technology \| strategic |
| `model_mode` | enum | `parallel` | parallel \| sequential \| convergent |
| `openai_depth` | enum | `balanced` | minimal \| balanced \| exhaustive |
| `risk_depth` | enum | `standard` | quick \| standard \| comprehensive |
| `multi_hypothesis` | bool | `false` | Enable hypothesis-driven framing |
| `expert_panel` | bool | `false` | Include expert panel recommendations |
| `context` | string | `""` | Additional context for research |

---

## 4. Model Strengths & Assignment

### Model Profiles

| Model | Primary Strength | Best For | Limitation |
|-------|------------------|----------|------------|
| **Claude Opus 4.5** | Judgment, synthesis, nuance | Strategic questions, conflict resolution, synthesis | May not surface all sources |
| **Gemini Pro 3** | Breadth, citations, grounding | Factual lookup, comprehensive sourcing, current data | Less depth on complex reasoning |
| **GPT-5.2 Deep** | Recency, depth, exhaustiveness | Technical details, narrow deep-dives, edge cases | Can miss broader context |

### Default Category Assignments

| Research Type | Claude | Gemini | GPT |
|---------------|--------|--------|-----|
| **Market** | Demand, Trends | Size, Structure, Supply | — |
| **Competitive** | Positioning, Strategy | Product, GTM, Org | Deep Dive |
| **Technology** | Fit, Risk | Maturity, Cost | Capability |
| **Strategic** | Options, Stakeholders | Environment | Implementation |

---

## 5. Risk Assessment Depths

### Quick (5 Factors)
Basic risk identification for time-sensitive research:
- Top 3 risks with likelihood/impact
- No mitigations or scenarios

### Standard (+ Bias Audit)
Adds mitigation planning and cognitive bias check:
- Mitigations and contingencies per risk
- Early warning signals
- Bias audit: confirmation, availability, anchoring

### Comprehensive (+ Base Rates)
Full risk analysis with historical grounding:
- Risk scenarios with trigger conditions
- Risk dependencies and cascades
- Base rate comparison from similar research
- Pre-mortem analysis

---

## 6. MECE Decomposition Patterns

### Pattern 1: Market Research
| Category | Focus | Model |
|----------|-------|-------|
| Market Size & Dynamics | TAM/SAM/SOM, growth rates | Gemini |
| Market Structure | Segmentation, value chain | Gemini |
| Demand Characteristics | Buyers, use cases, criteria | Claude |
| Supply & Competition | Players, barriers, substitutes | Gemini |
| Market Evolution | Trends, regulatory, disruption | Claude |

### Pattern 2: Competitive Intelligence
| Category | Focus | Model |
|----------|-------|-------|
| Product & Offering | Features, pricing, roadmap | GPT |
| Customers & Positioning | Segments, win/loss, messaging | Claude |
| Go-to-Market | Sales, marketing, partnerships | Gemini |
| Organization & Operations | Team, tech stack, cost structure | Gemini |
| Strategy & Trajectory | Direction, investments, SWOT | Claude |

### Pattern 3: Technology Evaluation
| Category | Focus | Model |
|----------|-------|-------|
| Capability & Performance | Features, benchmarks, limits | GPT |
| Maturity & Ecosystem | Stability, community, tools | Gemini |
| Fit & Integration | Use case alignment, migration | Claude |
| Cost & Investment | TCO, licensing, infrastructure | Gemini |
| Risk & Governance | Technical, vendor, compliance | Claude |

### Pattern 4: Strategic Research
| Category | Focus | Model |
|----------|-------|-------|
| Current State | Position, strengths, weaknesses | Claude |
| External Environment | Industry, macro, technology | Gemini |
| Strategic Options | Directions, trade-offs, requirements | Claude |
| Stakeholder Considerations | Customer, competitor, employee | Claude |
| Implementation Requirements | Capabilities, investments, timeline | GPT |

---

## 7. Multi-Hypothesis Framing

### When to Enable
- Testing predictions or forecasts
- Evaluating competing theories
- Decision involves binary or multi-way choice
- Need to avoid confirmation bias

### Process
1. Define core question as testable prediction
2. Generate 2-4 MECE hypotheses covering all outcomes
3. Assign prior probabilities (must sum to 100%)
4. Define supporting and refuting evidence for each
5. Research gathers evidence against criteria
6. Update posteriors based on evidence strength

### Example
```xml
<hypotheses question="Will enterprise adopt GenAI for customer service by 2027?">
  <hypothesis id="H1" position="broad" prior="30%">
    >50% enterprise adoption
  </hypothesis>
  <hypothesis id="H2" position="selective" prior="50%">
    10-50% adoption in specific use cases
  </hypothesis>
  <hypothesis id="H3" position="limited" prior="20%">
    <10% adoption due to barriers
  </hypothesis>
</hypotheses>
```

---

## 8. Evidence Strength Tribunal

5-point scale for evaluating source quality:

| Score | Name | Definition | Examples |
|-------|------|------------|----------|
| **5** | Primary | Direct from entity being researched | SEC filings, earnings calls, official docs |
| **4** | Auth. Secondary | Major analysts with citations | Gartner, Forrester, WSJ investigative |
| **3** | Credible Secondary | Reputable sources, some sourcing | TechCrunch, industry publications |
| **2** | Weak Secondary | Unsourced, outdated, anonymous | LinkedIn self-reports, old reports |
| **1** | Speculative | No verifiable basis | Rumors, predictions, fabrications |

**Time Decay:** Apply -1 for technology data >6 months, market data >1 year.

**Reference:** See `references/evidence-strength-rubric.md` for full scoring guidelines.

---

## 9. Conflict Resolution: WWHTBT

When models or sources disagree and resolution isn't clear, apply **What Would Have To Be True** analysis:

```xml
<conflict claim="Market size for X">
  <position holder="Gartner" value="$50B">
    <evidence score="4">2024 market report with methodology</evidence>
  </position>
  <position holder="IDC" value="$35B">
    <evidence score="4">Different scope definition</evidence>
  </position>

  <wwhtbt>
    <for_gartner>
      <condition>Adjacent markets included in scope</condition>
      <condition>Projected vs. realized revenue counted</condition>
    </for_gartner>
    <for_idc>
      <condition>Only core product category</condition>
      <condition>Realized revenue only</condition>
    </for_idc>
  </wwhtbt>

  <recommendation>
    Report range ($35-50B) with scope dependency noted.
    For our purposes, IDC definition more aligned.
  </recommendation>
</conflict>
```

---

## 10. Uncertainty Decomposition

| Type | Definition | Can Reduce? | Action |
|------|------------|-------------|--------|
| **Epistemic** | Knowledge gaps that COULD be closed | YES | Research further |
| **Aleatory** | Inherent randomness that CANNOT be predicted | NO | Quantify range, build scenarios |
| **Model** | Framework/definition dependencies | DEPENDS | Make choices explicit |

### Classification Questions
- **Epistemic:** "Does someone, somewhere know this?"
- **Aleatory:** "Even with perfect info, would this still be uncertain?"
- **Model:** "Would a different definition change the answer?"

**Reference:** See `references/uncertainty-taxonomy.md` for full classification protocol.

---

## 11. Gap Analysis

### Part 1: MECE Coverage Audit
Compare findings against expected coverage matrix for research type. Flag:
- **Critical gaps:** Core dimensions missing or Score ≤2
- **Significant gaps:** Supporting dimensions weak
- **Minor gaps:** Context items missing

### Part 2: Unknown Unknowns Probes

| Probe | Question |
|-------|----------|
| **Adjacent Domain** | What lessons from related industries apply? |
| **Stakeholder Blind Spot** | Whose voice is missing from sources? |
| **Time Horizon** | What historical precedents or future implications are ignored? |
| **Failure Mode** | What would have to be true for conclusions to be wrong? |
| **Second-Order Effects** | If findings are true, what else must follow? |

**Reference:** See `references/gap-analysis-protocol.md` for full audit process.

---

## 12. Output Specifications

### Phase 1 Deliverable: Research Brief

```
research-brief.xml
├── Header (ID, type, mode, parameters)
├── Section 1: Research Classification
├── Section 2: MECE Question Decomposition
├── Section 3: Multi-Hypothesis Framing (if enabled)
├── Section 4: Risk Assessment
├── Section 5: Expert Panel (if enabled)
├── Section 6: Model Role Assignments
├── Section 7: Ready-to-Execute Prompts
├── Section 8: Consolidation Strategy
├── Section 9: Verification Priorities
└── Section 10: Effort Estimates
```

### Phase 2 Deliverable: Consolidated Report

```
consolidated-report.xml
├── Header (quality summary)
├── Part 1: Executive Summary (≤5 findings, bottom line)
├── Part 2: Tiered Findings (1: >75%, 2: 50-75%, 3: <50%)
├── Part 3: Evidence Quality Assessment
├── Part 4: Contested Claims & Conflict Resolution
├── Part 5: Uncertainty Analysis
├── Part 6: Gap Analysis
├── Part 7: Model Contribution Analysis
├── Part 8: Decision Support (if-then tree)
├── Part 9: Kill Criteria
├── Part 10: Methodology Transparency
├── Part 11: Appendices
└── CRITICAL CONSTRAINTS (at end for context retention)
```

**Templates:** See `templates/research-brief-template.md` and `templates/consolidated-report-template.md`

---

## 13. Expert Panel Integration

### When to Enable
- High-stakes decisions
- Multi-disciplinary topics
- Need for challenge/red-teaming
- Regulatory or compliance implications

### Process
1. Identify panel size (3-8 experts) and balance
2. Select domain-appropriate experts
3. Define deliberation format (round-robin, debate, Delphi)
4. Assign challenger role for assumption testing
5. Synthesize panel perspectives into findings

### Expert Selection by Domain

| Domain | Recommended Experts |
|--------|---------------------|
| **Market** | Market analyst, Customer representative, Industry veteran |
| **Competitive** | Competitive intel analyst, Former competitor employee, Sales leader |
| **Technology** | Technical architect, Security specialist, Operations lead |
| **Strategic** | Strategy consultant, Board member, Industry analyst |

---

## 14. Quality Gates

### Phase 1 Gates (Research Design)

| # | Gate | Criterion |
|---|------|-----------|
| 1 | Objective Clarity | Single, answerable research question |
| 2 | MECE Validity | Categories non-overlapping and exhaustive |
| 3 | Question Quality | All sub-questions researchable |
| 4 | Model Fit | Assignments match model strengths |
| 5 | Prompt Executability | Prompts can run without modification |
| 6 | Completeness | All required sections populated |

### Phase 2 Gates (Consolidation)

| # | Gate | Criterion |
|---|------|-----------|
| 1 | Evidence Scored | All findings have evidence scores |
| 2 | Conflicts Surfaced | No hidden disagreements |
| 3 | Uncertainty Classified | All gaps tagged by type |
| 4 | Coverage Audited | MECE matrix reviewed |
| 5 | Probes Executed | ≥3 of 5 unknown-unknowns probes run |
| 6 | Tiers Justified | Confidence matches evidence profile |
| 7 | Decision Support | Actionable if-then structure |
| 8 | Constraints Verified | All 7 critical constraints checked |

---

## 15. Use Cases

| Use Case | Type | Mode | Risk | Hypothesis | Panel |
|----------|------|------|------|------------|-------|
| **Market sizing** | market | parallel | quick | no | no |
| **Competitor deep-dive** | competitive | sequential | standard | no | no |
| **Build vs buy** | technology | convergent | comprehensive | yes | yes |
| **Strategic planning** | strategic | parallel | comprehensive | yes | yes |
| **Trend monitoring** | market | parallel | quick | no | no |
| **Investment due diligence** | competitive | convergent | comprehensive | yes | yes |

---

## 16. Workflow Integration

This skill integrates with the broader research workflow:

```
┌─────────────────────┐
│ research-interviewer│  Elicit research requirements
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│create-research-brief│  ◀── THIS SKILL (Phase 1)
│     (Phase 1)       │  Design multi-LLM research strategy
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Execute Research  │  Run prompts across models
│  (Manual or Agent)  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│create-research-brief│  ◀── THIS SKILL (Phase 2)
│     (Phase 2)       │  Consolidate into report
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ consolidate-research│  Additional synthesis if needed
└─────────────────────┘
```

---

## 17. References and Templates

### Reference Files
| File | Purpose |
|------|---------|
| `references/evidence-strength-rubric.md` | 5-point evidence scoring with special cases |
| `references/uncertainty-taxonomy.md` | 3 uncertainty types with classification protocol |
| `references/gap-analysis-protocol.md` | MECE audit + 5 unknown-unknowns probes |
| `references/mece-decomposition-guide.md` | Full decomposition patterns with examples |

### Template Files
| File | Purpose |
|------|---------|
| `templates/research-brief-template.md` | Phase 1 output structure (XML) |
| `templates/consolidated-report-template.md` | Phase 2 output structure (XML) |

---

## Quick Start

### Phase 1: Create Research Brief
```
/create-research-brief
research_objective: "What is the market opportunity for AI legal research tools?"
research_type: market
risk_depth: standard
```

### Phase 2: Consolidate Research
```
/create-research-brief --phase=2
input: [model outputs from Phase 1 execution]
```
