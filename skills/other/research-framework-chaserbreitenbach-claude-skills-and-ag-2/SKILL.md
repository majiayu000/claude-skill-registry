---
name: research-framework
version: 1.0.0
description: |
  Structured deep research methodology for complex technical questions,
  including source evaluation, synthesis, and comprehensive reporting.
author: QuantQuiver AI R&D
license: MIT

category: workflow
tags:
  - research
  - analysis
  - deep-dive
  - technical-research
  - synthesis
  - methodology

dependencies:
  skills: []
  python: ">=3.9"
  packages: []
  tools:
    - web_fetch
    - web_search
    - code_execution

triggers:
  - "deep research"
  - "investigate topic"
  - "comprehensive analysis"
  - "research question"
  - "technical deep dive"
  - "synthesize information"
---

# Research Framework

## Purpose

A structured deep research methodology for complex technical questions, including source evaluation, synthesis, and comprehensive reporting. Provides systematic approach to gathering, evaluating, and synthesizing information.

**Problem Space:**
- Ad-hoc research lacks rigor and completeness
- Source quality varies widely
- Synthesis often superficial
- Findings not actionable

**Solution Approach:**
- Structured research phases
- Source credibility evaluation
- Multi-perspective synthesis
- Actionable recommendations

## When to Use

- Complex technical questions requiring multiple sources
- Comparative analysis (tools, frameworks, approaches)
- Investigating unfamiliar domains
- Due diligence research
- Technology evaluation
- Market/competitive analysis

## When NOT to Use

- Simple factual questions with clear answers
- Questions answerable from single authoritative source
- When time constraints prevent thorough research
- Opinion-based questions without factual basis

---

## Core Instructions

### Research Framework Phases

```
┌─────────────────────────────────────────────────────────────────┐
│                    RESEARCH FRAMEWORK                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Phase 1: SCOPE DEFINITION                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Define research question precisely                      │ │
│  │  • Identify key sub-questions                              │ │
│  │  • Set scope boundaries                                    │ │
│  │  • Define success criteria                                │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Phase 2: SOURCE GATHERING                                      │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Primary sources (official docs, papers)                │ │
│  │  • Secondary sources (articles, tutorials)                │ │
│  │  • Community sources (forums, discussions)                │ │
│  │  • Code/implementation examples                           │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Phase 3: SOURCE EVALUATION                                     │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Credibility assessment                                  │ │
│  │  • Recency evaluation                                      │ │
│  │  • Bias identification                                     │ │
│  │  • Corroboration checking                                  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Phase 4: ANALYSIS & SYNTHESIS                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Pattern identification                                  │ │
│  │  • Contradiction resolution                               │ │
│  │  • Gap identification                                      │ │
│  │  • Insight extraction                                      │ │
│  └───────────────────────────────────────────────────────────┘ │
│                           │                                     │
│  Phase 5: REPORTING                                             │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  • Executive summary                                       │ │
│  │  • Detailed findings                                       │ │
│  │  • Recommendations                                         │ │
│  │  • Limitations & uncertainties                            │ │
│  └───────────────────────────────────────────────────────────┘ │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Standard Procedures

#### Phase 1: Scope Definition

```yaml
scope_definition:
  primary_question: |
    What specific question are we answering?
    (Single, clear, answerable question)

  sub_questions:
    - What background context is needed?
    - What are the key comparison dimensions?
    - What constraints apply (time, cost, technical)?
    - Who is the audience for this research?

  boundaries:
    in_scope:
      - List what IS included
    out_of_scope:
      - List what is explicitly excluded

  success_criteria:
    - What makes this research "complete"?
    - What decisions will it inform?
    - What level of confidence is needed?
```

#### Phase 2: Source Gathering

**Source Categories:**

| Category | Examples | Typical Quality |
|----------|----------|-----------------|
| **Primary** | Official docs, academic papers, specs | Highest |
| **Secondary** | Tech blogs, tutorials, books | High |
| **Community** | Stack Overflow, Reddit, forums | Variable |
| **Code** | GitHub repos, examples | Practical |
| **Commercial** | Vendor docs, case studies | Biased but useful |

**Search Strategy:**
```
1. Start broad: "[topic] overview"
2. Go deep: "[topic] architecture/internals"
3. Find comparisons: "[topic] vs [alternative]"
4. Find problems: "[topic] issues/problems/limitations"
5. Find success: "[topic] production/case study"
6. Find experts: "[topic] by [known expert]"
```

#### Phase 3: Source Evaluation

**Credibility Rubric:**

| Factor | Score 1-5 | Indicators |
|--------|-----------|------------|
| **Authority** | | Author credentials, publication venue |
| **Accuracy** | | Factual correctness, citations |
| **Objectivity** | | Bias disclosure, balanced view |
| **Currency** | | Publication date, update frequency |
| **Coverage** | | Depth, completeness |

**Red Flags:**
- No author attribution
- No dates
- Sensationalist language
- No sources/citations
- Commercial bias undisclosed
- Contradicts multiple credible sources

#### Phase 4: Analysis & Synthesis

**Synthesis Methods:**

1. **Thematic Analysis**
   - Group findings by theme
   - Identify patterns across sources
   - Note frequency of themes

2. **Comparative Matrix**
   | Aspect | Source A | Source B | Source C | Consensus |
   |--------|----------|----------|----------|-----------|
   | Topic 1 | Finding | Finding | Finding | Summary |

3. **Contradiction Resolution**
   - When sources disagree:
     - Check recency (newer often more accurate)
     - Check authority (prefer primary sources)
     - Check context (different use cases?)
     - Note uncertainty in findings

4. **Gap Analysis**
   - What questions remain unanswered?
   - What would additional research reveal?
   - What assumptions are being made?

#### Phase 5: Reporting

**Report Structure:**
```markdown
# Research Report: [Topic]

## Executive Summary
- Key finding 1 (confidence: high/medium/low)
- Key finding 2
- Key finding 3
- Primary recommendation

## Methodology
- Research question
- Sources consulted (count by category)
- Time period covered
- Limitations

## Detailed Findings

### Finding 1: [Topic]
**Summary**: [1-2 sentences]
**Evidence**: [Sources and data]
**Confidence**: [High/Medium/Low with justification]

### Finding 2: [Topic]
...

## Analysis

### Patterns Identified
- Pattern 1
- Pattern 2

### Contradictions & Uncertainties
- Area of disagreement 1
- Open question 1

### Gaps in Available Information
- Gap 1

## Recommendations

### Recommended Action 1
- **What**: [Specific action]
- **Why**: [Supporting evidence]
- **Risk**: [Potential downsides]
- **Confidence**: [High/Medium/Low]

## Appendix

### Sources
[Full source list with credibility scores]

### Methodology Details
[Search queries, evaluation criteria]
```

### Decision Framework

**Research Depth Selection:**

| Depth | Time | Sources | Use Case |
|-------|------|---------|----------|
| **Quick** | 30 min | 3-5 | Simple factual questions |
| **Standard** | 2-4 hours | 10-15 | Technical decisions |
| **Deep** | 1-2 days | 25+ | Major investments, strategy |
| **Exhaustive** | 1+ week | 50+ | Critical decisions, publications |

**When to Stop Researching:**
- Saturation: New sources repeat existing findings
- Diminishing returns: Additional sources add little value
- Time/budget constraint reached
- Research question answered with sufficient confidence

---

## Templates

### Research Plan Template

```yaml
research_plan:
  title: "[Research Topic]"
  date: "YYYY-MM-DD"
  researcher: "[Name]"

  question:
    primary: "[Main research question]"
    secondary:
      - "[Sub-question 1]"
      - "[Sub-question 2]"

  scope:
    in_scope:
      - "[What's included]"
    out_of_scope:
      - "[What's excluded]"
    time_period: "[Relevant date range]"

  methodology:
    depth: "quick|standard|deep|exhaustive"
    source_types:
      - primary
      - secondary
      - community
    search_queries:
      - "[Query 1]"
      - "[Query 2]"

  deliverables:
    format: "report|presentation|summary"
    audience: "[Who will use this]"
    deadline: "YYYY-MM-DD"
```

### Source Evaluation Template

```yaml
source:
  title: "[Source Title]"
  url: "[URL]"
  type: "primary|secondary|community|code|commercial"
  date_published: "YYYY-MM-DD"
  date_accessed: "YYYY-MM-DD"

  author:
    name: "[Author Name]"
    credentials: "[Relevant expertise]"
    affiliation: "[Organization]"

  evaluation:
    authority: 4  # 1-5
    accuracy: 4
    objectivity: 3
    currency: 5
    coverage: 4
    overall: 4

  key_findings:
    - "[Finding 1]"
    - "[Finding 2]"

  notes: |
    [Additional observations about this source]

  bias_concerns: |
    [Any potential biases identified]
```

### Comparative Analysis Template

```markdown
# Comparative Analysis: [Options Being Compared]

## Overview

| Criterion | Option A | Option B | Option C |
|-----------|----------|----------|----------|
| [Criterion 1] | | | |
| [Criterion 2] | | | |
| [Criterion 3] | | | |

## Detailed Comparison

### [Criterion 1]

**Option A**: [Details with sources]
**Option B**: [Details with sources]
**Option C**: [Details with sources]
**Winner**: [Option] because [reason]

### [Criterion 2]
...

## Summary

### Strengths by Option
- **Option A**: [Key strengths]
- **Option B**: [Key strengths]
- **Option C**: [Key strengths]

### Weaknesses by Option
- **Option A**: [Key weaknesses]
- **Option B**: [Key weaknesses]
- **Option C**: [Key weaknesses]

## Recommendation

**For [use case 1]**: Option A because [reason]
**For [use case 2]**: Option B because [reason]
**Default recommendation**: Option [X] because [reason]

## Confidence Level

[High/Medium/Low] - [Justification]

## Limitations

- [What this analysis doesn't cover]
- [Assumptions made]
```

---

## Examples

### Example 1: Framework Evaluation

**Input**: "Research which Python web framework to use for our new API"

**Process**:
1. Define scope: REST API, medium scale, team familiarity
2. Gather sources: Official docs (Django, FastAPI, Flask), benchmarks, case studies
3. Evaluate: Weight performance benchmarks higher (primary source)
4. Synthesize: Create comparison matrix on key criteria
5. Report: Recommendation with confidence levels

**Output Summary**:
- FastAPI recommended for greenfield API projects
- Django REST Framework for complex apps with admin needs
- Flask for maximum flexibility/minimal structure

### Example 2: Technology Deep Dive

**Input**: "I need to understand how WebSocket scaling works"

**Process**:
1. Define scope: Focus on horizontal scaling, ignore single-server
2. Gather: Architecture docs, scaling guides, production case studies
3. Evaluate: Prioritize production experience reports
4. Synthesize: Identify common patterns and pitfalls
5. Report: Architecture recommendations with trade-offs

---

## Validation Checklist

Before finalizing research:

- [ ] Primary question clearly answered
- [ ] Multiple credible sources consulted
- [ ] Source credibility evaluated
- [ ] Contradictions identified and addressed
- [ ] Confidence levels assigned to findings
- [ ] Limitations documented
- [ ] Recommendations are actionable
- [ ] Report formatted for audience

---

## Related Resources

- Skill: `technical-documentation-generator` - Format research into docs
- Skill: `branded-document-suite` - Professional report formatting
- Critical thinking frameworks
- Academic research methodology

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Five-phase research framework
- Source evaluation rubric
- Synthesis methods
- Report templates
