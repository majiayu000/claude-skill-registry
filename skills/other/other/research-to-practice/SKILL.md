---
name: research-to-practice
description: Transform academic research insights into practical workflow optimizations
version: 1.0
author: agent
---

# Research to Practice

Bridge the gap between academic research and practical workflow improvements.

---

## When to Use

Use this skill when:
- You discover a relevant academic paper and want to apply its insights
- You need to optimize existing workflows based on research findings
- You want to systematically extract actionable ideas from research
- Current methods show limitations that research might address

**Typical scenarios:**
- Reading ML/NLP papers for agent system improvements
- Finding optimization techniques for knowledge management
- Applying human-computer interaction research to UI/UX workflows
- Leveraging cognitive science for better user interactions

---

## Prerequisites

- Access to paper (URL, PDF, or bibliographic information)
- Understanding of current workspace workflows
- Knowledge of which systems/components might benefit
- Optional: specific pain points or optimization targets in mind

---

## Workflow

### Step 1: Paper Acquisition & Initial Assessment

**Goal:** Obtain and understand the paper's core contribution

**Actions:**
1. Fetch paper content via URL or search for it
2. Identify: Title, authors, venue, year
3. Extract abstract and key claims
4. Determine: Is this relevant to our workflows?

**Decision Point:**
- If paper is not accessible or not relevant → Stop and report
- If paper is accessible and relevant → Continue to Step 2

**Output Format:**
```markdown
## Paper Overview
- **Title**: [paper title]
- **Authors**: [authors]
- **Venue**: [conference/journal]
- **Year**: [year]
- **Core Contribution**: [1-2 sentence summary]
- **Relevance Score**: [High/Medium/Low] - [reasoning]
```

### Step 2: Deep Reading & Insight Extraction

**Goal:** Extract specific techniques, insights, and principles

**Actions:**
1. Read methodology section → What did they do?
2. Read results section → What did they achieve?
3. Identify novel techniques or approaches
4. Note any ablation studies (what matters most?)
5. Extract key equations, algorithms, or frameworks

**Key Questions to Answer:**
- What is the core innovation?
- What problem does it solve?
- How does it compare to existing methods?
- What are the limitations?

**Output Format:**
```markdown
## Core Insights

### 1. [Insight Category Name]
**Technique/Principle**: [description]
**Key Mechanism**: [how it works]
**Advantage**: [why it's better]
**Limitations**: [constraints or trade-offs]

### 2. [Insight Category Name]
...

## Technical Details
- [Key algorithm/framework]
- [Important parameters or configurations]
- [Evaluation metrics used]
```

### Step 3: Current Workflow Analysis

**Goal:** Map paper insights to existing workflows

**Actions:**
1. Review current relevant workflows/skills
2. Identify pain points or inefficiencies
3. Map paper techniques to specific components
4. Prioritize based on impact and feasibility

**Mapping Framework:**
```
Paper Insight → Current System → Potential Improvement
```

**Output Format:**
```markdown
## Current State Analysis

### Relevant Workflows
1. [Workflow/Skill name]
   - Current approach: [description]
   - Limitations: [problems]
   - Relevant paper insights: [which insights apply]

2. [Workflow/Skill name]
   ...

### Mapping: Insights → Workflows
| Paper Insight | Current Workflow | Improvement Opportunity |
|--------------|------------------|------------------------|
| [insight 1] | [workflow A] | [specific improvement] |
| [insight 2] | [workflow B] | [specific improvement] |
```

### Step 4: Optimization Proposal Generation

**Goal:** Generate specific, actionable optimization proposals

**Actions:**
1. For each insight-workflow mapping:
   - Design concrete changes
   - Estimate impact (High/Medium/Low)
   - Estimate effort (High/Medium/Low)
   - Identify dependencies
2. Group related proposals
3. Prioritize by impact/effort ratio

**Output Format:**
```markdown
## Optimization Proposals

### Proposal 1: [Name]
**Target**: [which workflow/component]
**Based on**: [which paper insight]
**Description**: [what to change]
**Implementation Steps**:
1. [step 1]
2. [step 2]
...

**Expected Benefits**:
- [benefit 1]
- [benefit 2]

**Impact**: [High/Medium/Low]
**Effort**: [High/Medium/Low]
**Dependencies**: [what's needed first]

### Proposal 2: [Name]
...

## Prioritization Matrix
| Proposal | Impact | Effort | Priority |
|----------|--------|--------|----------|
| [P1] | High | Low | ⭐⭐⭐ |
| [P2] | High | Medium | ⭐⭐⭐ |
| [P3] | Medium | Low | ⭐⭐ |
```

### Step 5: Implementation Planning

**Goal:** Create actionable implementation plans for top proposals

**Actions:**
1. Select top 2-3 proposals
2. For each, create detailed implementation plan
3. Define success metrics
4. Identify risks and mitigation strategies

**Output Format:**
```markdown
## Implementation Plans

### Plan 1: [Proposal Name]
**Goal**: [clear objective]

**Steps**:
1. [detailed step]
2. [detailed step]
...

**Files to Modify**:
- [file 1] - [changes]
- [file 2] - [changes]

**Success Metrics**:
- [metric 1]: [how to measure]
- [metric 2]: [how to measure]

**Risks & Mitigation**:
- Risk: [description] → Mitigation: [solution]

**Estimated Time**: [X hours/days]

---

### Plan 2: [Proposal Name]
...

## Recommended Execution Order
1. [Plan X] - [reasoning]
2. [Plan Y] - [reasoning]
```

### Step 6: Validation & Documentation

**Goal:** Validate proposals and document for future reference

**Actions:**
1. Review proposals against original paper claims
2. Check for misinterpretations
3. Document the entire analysis in workspace
4. Create summary for knowledge base

**Output Format:**
```markdown
## Validation Checklist
- [ ] Proposals align with paper's core contribution
- [ ] Technical details correctly understood
- [ ] Limitations acknowledged in proposals
- [ ] Implementation plans are feasible
- [ ] Success metrics are measurable

## Knowledge Base Entry
**Paper**: [title]
**Applied to**: [workflows]
**Key Improvements**: [summary]
**Status**: [Proposed/In Progress/Implemented]
**Results**: [to be filled after implementation]
```

---

## Best Practices

### Do's
✅ **Verify paper accessibility first** - Don't proceed if you can't read the paper
✅ **Focus on transferable insights** - Not all research applies to practical workflows
✅ **Consider constraints** - Academic methods may have assumptions that don't hold in practice
✅ **Start small** - Implement one insight before moving to the next
✅ **Document everything** - Research insights are valuable institutional knowledge
✅ **Validate assumptions** - What works in the paper's context may not work in yours

### Don'ts
❌ **Don't over-engineer** - Simple solutions are often better than complex research methods
❌ **Don't ignore limitations** - Every paper has constraints; acknowledge them
❌ **Don't apply blindly** - Adapt techniques to your specific context
❌ **Don't skip the mapping step** - Understanding current state is crucial
❌ **Don't promise unrealistic gains** - Be honest about expected improvements

### Quality Checks

Before finalizing proposals, verify:
1. **Correctness**: Do I understand the paper correctly?
2. **Relevance**: Does this actually address a real problem?
3. **Feasibility**: Can this be implemented with available resources?
4. **Measurability**: Can we tell if it worked?

---

## Common Issues

### Issue 1: Paper Not Accessible

**Symptom:** Cannot fetch PDF or paper is behind paywall

**Solutions:**
- Search for arXiv preprint version
- Look for author's personal webpage
- Check if paper is cited in accessible sources
- Use abstract + citations to infer content

**Fallback:**
```
⚠️ Paper not directly accessible
Alternative approaches:
1. Search for: [title] site:arxiv.org
2. Check author pages: [author homepages]
3. Use secondary sources: blog posts, talks, reviews
```

### Issue 2: Paper Too Theoretical

**Symptom:** Techniques are too abstract to apply directly

**Solutions:**
- Look for implementation details or pseudocode
- Find applied papers that cite this work
- Break down into simpler components
- Focus on the core insight rather than full method

### Issue 3: Unclear Relevance

**Symptom:** Not sure if paper applies to current workflows

**Solutions:**
- List current workflow pain points
- Check if paper addresses similar problems
- Look for indirect applications (e.g., evaluation methods)
- Discuss with user to clarify priorities

### Issue 4: Overlapping Insights

**Symptom:** Multiple papers suggest similar improvements

**Solutions:**
- Compare approaches and choose best fit
- Consider combining complementary insights
- Prioritize based on implementation effort
- Document the relationship between papers

### Issue 5: Implementation Too Complex

**Symptom:** Paper's method requires significant infrastructure

**Solutions:**
- Simplify: Use core insight with simpler implementation
- Phase: Break into incremental improvements
- Alternative: Find simpler papers with similar insights
- Hybrid: Combine with existing proven methods

---

## Example: Hierarchical Attention Networks → Workflow Optimization

### Paper Summary
**Hierarchical Attention Networks for Document Classification** (Yang et al., NAACL 2016)

**Core Insight**: Documents have natural hierarchy (words → sentences → document), and attention mechanisms at each level improve classification by focusing on important parts.

### Current Workflows Analyzed
- `knowledge-base-cache`: 3-tier cache system
- `memory`: Daily log and long-term memory
- `code-analysis`: Code understanding workflow

### Optimization Proposals

#### Proposal 1: Attention-Based Knowledge Retrieval
**Target**: `knowledge-base-cache`
**Insight**: Hierarchical attention for information retrieval
**Description**: Add attention weights to cache layers based on query relevance
**Impact**: High | **Effort**: Medium

#### Proposal 2: Hierarchical Memory Filtering
**Target**: `memory` system
**Insight**: Word-level + sentence-level + document-level attention
**Description**: Filter memories at multiple granularities
**Impact**: High | **Effort**: Medium

### Implementation Plan (Selected)
```markdown
## Plan: Attention-Based Knowledge Retrieval

**Goal**: Improve knowledge retrieval relevance using attention weights

**Steps**:
1. Add embedding-based similarity scoring to WorkingMemoryManager
2. Implement attention weight calculation for cache layers
3. Modify retrieval to use weighted assembly
4. Test with historical queries

**Files**:
- `repository/core/working_memory.py` - Add attention scoring
- `repository/adapters/hot_cache_adapter.py` - Weighted retrieval

**Success Metrics**:
- Relevance score: User satisfaction with retrieved context
- Token efficiency: Reduction in irrelevant context

**Time Estimate**: 4-6 hours
```

---

## See Also

- [knowledge-base-cache](./knowledge-base-cache) - Knowledge management system
- [code-analysis](./code-analysis) - Structured code understanding
- [mvp-design](./mvp-design) - Design implementation plans
- [daily-log](./daily-log) - Record research application outcomes

---

## Version History

- **v1.0** (2026-02-12) - Initial release
  - 6-step workflow from paper to practice
  - Mapping framework for insights → workflows
  - Prioritization matrix
  - Common issues and solutions
  - Complete example with HAN paper
