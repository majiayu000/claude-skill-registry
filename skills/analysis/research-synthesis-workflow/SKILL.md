---
name: research-synthesis-workflow
description: Systematic methodology for gathering, analyzing, and synthesizing research from multiple sources into coherent insights and actionable knowledge.
license: MIT
---

# Research Synthesis Workflow

This skill provides a systematic methodology for conducting research, synthesizing findings from multiple sources, and producing actionable knowledge artifacts.

## Core Competencies

- **Source Evaluation**: Assessing credibility, relevance, and bias
- **Information Extraction**: Systematic note-taking and annotation
- **Synthesis Methods**: Thematic analysis, meta-analysis, framework building
- **Knowledge Artifacts**: Reports, literature reviews, decision frameworks

## Research Workflow Overview

```
┌──────────────────────────────────────────────────────────────┐
│                    Research Synthesis Workflow                │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  1. SCOPE         2. GATHER         3. EXTRACT              │
│  ┌─────────┐      ┌─────────┐      ┌─────────┐              │
│  │ Define  │─────▶│ Find    │─────▶│ Capture │              │
│  │ Question│      │ Sources │      │ Insights│              │
│  └─────────┘      └─────────┘      └─────────┘              │
│       │                                  │                   │
│       │          5. PRODUCE         4. SYNTHESIZE           │
│       │          ┌─────────┐      ┌─────────┐              │
│       └─────────▶│ Create  │◀─────│ Connect │              │
│                  │ Artifact│      │ Themes  │              │
│                  └─────────┘      └─────────┘              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

## Phase 1: Scope Definition

### Research Question Framework

Transform vague topics into answerable questions:

| Type | Pattern | Example |
|------|---------|---------|
| Exploratory | What is X? How does X work? | What is vector search? |
| Comparative | How does X compare to Y? | PostgreSQL vs. Neo4j for graphs? |
| Evaluative | Is X effective for Y? | Is RAG effective for technical docs? |
| Causal | What causes X? What are effects of X? | What causes LLM hallucinations? |
| Prescriptive | How should we implement X? | How to design a RAG pipeline? |

### Scope Boundaries

Define explicitly:
- **In scope**: Topics to cover
- **Out of scope**: Adjacent topics to exclude
- **Depth**: Survey (broad) vs. deep-dive (narrow)
- **Time bounds**: Cut-off dates for sources
- **Source types**: Academic, industry, primary data

### Example Scope Document

```markdown
## Research Scope: Vector Database Selection

### Research Question
Which vector database best fits our production RAG system
requiring <50ms latency at 10M+ vectors?

### In Scope
- Pinecone, Weaviate, Milvus, Qdrant, pgvector
- Latency benchmarks at scale
- Cost analysis (cloud vs self-hosted)
- Operational complexity

### Out of Scope
- General-purpose databases with vector extensions
- Sub-million vector use cases
- Academic/research-only systems

### Success Criteria
Recommendation with supporting evidence for 2-3 top candidates
```

## Phase 2: Source Gathering

### Source Quality Assessment

Evaluate each source on:

| Criterion | High Quality | Low Quality |
|-----------|--------------|-------------|
| Authority | Expert author, peer-reviewed | Anonymous, no credentials |
| Currency | Recent, updated | Outdated, no dates |
| Accuracy | Citations, verifiable | Unsupported claims |
| Purpose | Inform, educate | Sell, persuade |
| Coverage | Comprehensive | Superficial |

### Source Types and Uses

```
Primary Sources (original)
├── Research papers
├── Official documentation
├── Benchmark data
└── Expert interviews

Secondary Sources (analysis)
├── Review articles
├── Technical blogs
├── Industry reports
└── Book chapters

Tertiary Sources (summaries)
├── Wikipedia
├── Textbooks
└── Encyclopedias
```

### Search Strategies

**Keyword expansion**:
- Start: "vector database performance"
- Expand: "approximate nearest neighbor", "HNSW benchmark", "embedding search latency"

**Citation chaining**:
- Forward: Who cites this paper?
- Backward: What does this paper cite?

**Author tracking**:
- Find key researchers, follow their work

### Source Documentation

For each source, capture:
```markdown
## Source: [Title]
- **URL/DOI**:
- **Author(s)**:
- **Date**:
- **Type**: [paper/blog/docs/report]
- **Quality Score**: [1-5]
- **Relevance**: [high/medium/low]
- **Key Topics**:
- **Notes**:
```

## Phase 3: Information Extraction

### Structured Note-Taking

Use consistent templates for extraction:

```markdown
## Claim: [Specific assertion]
- **Source**: [reference]
- **Evidence**: [supporting data/reasoning]
- **Strength**: [strong/moderate/weak]
- **My Assessment**: [agree/disagree/uncertain]
- **Related Claims**: [links to other notes]
```

### Evidence Classification

| Type | Description | Weight |
|------|-------------|--------|
| Empirical | Measured data, experiments | High |
| Analytical | Logical derivation | Medium-High |
| Anecdotal | Case studies, examples | Medium |
| Expert Opinion | Authority statements | Medium |
| Theoretical | Model predictions | Medium-Low |

### Contradiction Tracking

When sources disagree:
```markdown
## Conflict: [Topic]

### Position A: [Claim]
- Sources: [list]
- Evidence: [summary]

### Position B: [Claim]
- Sources: [list]
- Evidence: [summary]

### Analysis
- Methodological differences:
- Context differences:
- Possible resolution:
- My conclusion:
```

## Phase 4: Synthesis

### Thematic Analysis

1. **Code** individual insights with tags
2. **Cluster** related codes into themes
3. **Review** themes for coherence
4. **Define** each theme clearly
5. **Relate** themes to research question

```
Codes                    Themes                 Findings
├─ fast queries     ─┐
├─ low latency      ─┼── Performance      ─┬── Theme 1: Performance
├─ high throughput  ─┘                     │   varies significantly
├─ managed service  ─┐                     │   by workload type
├─ self-hosted      ─┼── Deployment      ─┼── Theme 2: Cloud vs
├─ kubernetes       ─┘                     │   self-hosted tradeoff
├─ pricing tiers    ─┐                     │
├─ compute costs    ─┼── Economics       ─┴── Theme 3: Total cost
├─ hidden costs     ─┘                         drives final choice
```

### Framework Building

Create decision frameworks from synthesis:

```markdown
## Vector Database Selection Framework

### Decision Tree
1. Scale requirement?
   - <1M vectors → pgvector (simplicity)
   - 1M-100M vectors → Continue to 2
   - >100M vectors → Milvus/Weaviate (distributed)

2. Operational capacity?
   - Limited DevOps → Pinecone (managed)
   - Strong DevOps → Continue to 3

3. Cost sensitivity?
   - Budget constrained → Qdrant (open source)
   - Budget flexible → Evaluate all options

### Comparison Matrix
| Criterion      | Weight | Pinecone | Milvus | Qdrant |
|----------------|--------|----------|--------|--------|
| Latency        | 30%    | 4        | 5      | 4      |
| Scalability    | 25%    | 5        | 5      | 4      |
| Operations     | 20%    | 5        | 3      | 4      |
| Cost           | 15%    | 2        | 4      | 5      |
| Features       | 10%    | 4        | 5      | 4      |
| **Weighted**   |        | **4.0**  | **4.4**| **4.2**|
```

## Phase 5: Knowledge Artifact Production

### Artifact Types

| Format | Purpose | Audience |
|--------|---------|----------|
| Executive Summary | Quick decision support | Leadership |
| Technical Report | Detailed analysis | Engineers |
| Literature Review | Academic synthesis | Researchers |
| Decision Framework | Structured evaluation | Decision makers |
| Reference Guide | Quick lookup | Practitioners |

### Structure Templates

**Executive Summary** (1-2 pages):
1. Context and question
2. Key findings (3-5 bullets)
3. Recommendation
4. Risks and considerations

**Technical Report** (5-20 pages):
1. Executive summary
2. Background and scope
3. Methodology
4. Findings by theme
5. Analysis and discussion
6. Recommendations
7. Appendices (data, sources)

### Quality Checklist

Before finalizing:
- [ ] Research question answered?
- [ ] All claims supported by evidence?
- [ ] Contradictions addressed?
- [ ] Limitations acknowledged?
- [ ] Actionable recommendations?
- [ ] Sources properly cited?
- [ ] Appropriate for audience?

## Best Practices

### Avoiding Bias

- Seek disconfirming evidence actively
- Include multiple perspectives
- Note your priors and update them
- Separate observation from interpretation
- Document methodology for transparency

### Managing Scope Creep

- Return to research question frequently
- Park interesting tangents in "Future Research"
- Time-box each phase
- Define "good enough" criteria upfront

### Iteration

Research is rarely linear:
- New sources may require scope adjustment
- Synthesis may reveal gaps requiring more gathering
- Artifacts may need multiple drafts

## References

- `references/evaluation-rubrics.md` - Source quality scoring guides
- `references/synthesis-methods.md` - Detailed synthesis techniques
- `references/artifact-templates.md` - Document templates and examples
