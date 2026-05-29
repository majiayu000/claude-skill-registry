---
name: evaluation-to-growth
description: Systematic content evaluation framework progressing through Critique → Reinforcement → Risk Analysis → Growth. Use when reviewing writing, arguments, proposals, code documentation, or any content requiring rigorous multi-dimensional assessment. Supports interactive guided mode or autonomous full-report mode, with output as markdown report, structured checklist, or inline revision suggestions. Triggers on requests to evaluate, critique, improve, strengthen, or review content quality.
license: MIT
---

# Evaluation to Growth

A systematic framework for transforming content through rigorous evaluation into stronger, more resilient final products.

## Mode Selection

Before beginning, determine execution mode and output format.

### Execution Modes

**Interactive Mode**: Walk through each phase step-by-step, pausing for user input and direction between stages. Best for collaborative refinement or learning the framework.

**Autonomous Mode**: Execute all phases and deliver comprehensive results. Best for efficient batch evaluation or when user wants complete analysis upfront.

### Output Formats

**Markdown Report**: Structured document with sections for each phase, findings, and recommendations. Best for documentation or sharing.

**Structured Checklist**: Itemized findings with status indicators and action items. Best for tracking and implementation.

**Inline Revisions**: Suggestions embedded within or alongside the original content. Best for direct editing workflow.

---

## The Framework

```
[Evaluation] → [Reinforcement] → [Risk Analysis] → [Growth]
```

### Phase 1: Evaluation

Comprehensive assessment across five dimensions.

#### 1.1 Critique
Identify strengths and weaknesses holistically.

**Prompt**: "Evaluate this content thoroughly. Identify its key strengths and weaknesses. Highlight which parts are effective and which need improvement, providing specific reasons."

**Output structure**:
- Strengths: [list with specific examples]
- Weaknesses: [list with specific examples]
- Priority areas: [ranked improvement opportunities]

#### 1.2 Logic Check
Ensure internal consistency and sound reasoning.

**Prompt**: "Examine the content for logical consistency. Identify contradictions, gaps in reasoning, or unsupported claims, and suggest how to strengthen coherence."

**Output structure**:
- Contradictions found: [list]
- Reasoning gaps: [list]
- Unsupported claims: [list]
- Coherence recommendations: [list]

#### 1.3 Logos Review
Assess rational and factual appeal.

**Prompt**: "Assess the rational and factual appeal of this content. Are the arguments clear, well-supported, and persuasive? Suggest ways to enhance the logical impact."

**Output structure**:
- Argument clarity: [assessment]
- Evidence quality: [assessment]
- Persuasive strength: [assessment]
- Enhancement recommendations: [list]

#### 1.4 Pathos Review
Evaluate emotional resonance.

**Prompt**: "Analyze the emotional tone and resonance of this content. Does it create an emotional connection with its intended audience? Recommend adjustments to increase engagement."

**Output structure**:
- Current emotional tone: [description]
- Audience connection: [assessment]
- Engagement level: [assessment]
- Recommendations: [list]

#### 1.5 Ethos Review
Examine credibility and authority.

**Prompt**: "Evaluate the credibility and authority of this content. Does it reflect expertise and trustworthiness? Suggest ways to reinforce its reliability and professional tone."

**Output structure**:
- Perceived expertise: [assessment]
- Trustworthiness signals: [list present/missing]
- Authority markers: [assessment]
- Credibility recommendations: [list]

---

### Phase 2: Reinforcement

Consolidate and strengthen based on evaluation findings.

#### 2.1 Synthesis
Integrate logic check findings to eliminate contradictions and reinforce coherence.

**Actions**:
- Resolve identified contradictions
- Fill reasoning gaps
- Support unsupported claims or remove them
- Strengthen transitional logic

---

### Phase 3: Risk Analysis

Identify vulnerabilities before they become failures.

#### 3.1 Blind Spots
Reveal overlooked areas or hidden assumptions.

**Prompt**: "Identify any areas in this content that may be overlooked, biased, or based on hidden assumptions. Provide suggestions to address these gaps or risks."

**Output structure**:
- Hidden assumptions: [list]
- Overlooked perspectives: [list]
- Potential biases: [list]
- Mitigation strategies: [list]

#### 3.2 Shatter Points
Pinpoint critical vulnerabilities.

**Prompt**: "Analyze the content for potential vulnerabilities or weak points that could cause failure or serious criticism. Recommend preventive measures or reinforcements."

**Output structure**:
- Critical vulnerabilities: [list with severity]
- Potential attack vectors: [how critics might respond]
- Preventive measures: [list]
- Contingency preparations: [list]

---

### Phase 4: Growth

Transform evaluation into evolution.

#### 4.1 Bloom (Emergent Insights)
Generate new directions from the analysis.

**Prompt**: "From the reviewed content, generate innovative ideas, new directions, or insights that could enhance or expand its impact."

**Output structure**:
- Emergent themes: [patterns noticed across analysis]
- Expansion opportunities: [where content could grow]
- Novel angles: [unexpected directions]
- Cross-domain connections: [links to other areas]

#### 4.2 Evolve (Iterative Refinement)
Produce the strengthened final version.

**Prompt**: "Incorporate all feedback and refinements to create a polished, stronger, and more resilient final version of the content."

**Output structure**:
- Revision summary: [changes made]
- Strength improvements: [before/after]
- Risk mitigations applied: [list]
- Final product: [revised content]

---

## Execution Templates

### Interactive Mode Script

```
Step 1: "I'll evaluate your content using the Evaluation-to-Growth framework. 
        First, let's assess strengths and weaknesses. [Critique results]
        Would you like to discuss these findings before moving to logic check?"

Step 2: [Wait for response, then proceed to Logic Check]

Step 3: [Continue through each phase with pause points]

Step 4: "We've completed the evaluation phases. Ready to move into Risk Analysis?"

[Continue through all phases with user checkpoints]
```

### Autonomous Mode Script

```
"I'll provide a complete Evaluation-to-Growth analysis of your content.

## Evaluation Phase
[All five dimensions with findings]

## Reinforcement
[Synthesis and coherence improvements]

## Risk Analysis
[Blind spots and shatter points]

## Growth
[Emergent insights and evolved version]

## Summary
[Key findings and recommended next steps]"
```

---

## Output Format Templates

### Markdown Report Template

See `references/report-template.md`

### Checklist Template

See `references/checklist-template.md`

### Inline Revision Template

See `references/inline-template.md`

---

## Quick Reference

| Phase | Purpose | Key Question |
|-------|---------|--------------|
| Critique | Holistic assessment | What works? What doesn't? |
| Logic Check | Internal consistency | Does it contradict itself? |
| Logos | Rational appeal | Is the argument sound? |
| Pathos | Emotional appeal | Does it connect? |
| Ethos | Credibility | Is it trustworthy? |
| Blind Spots | Hidden risks | What am I not seeing? |
| Shatter Points | Critical vulnerabilities | Where could this fail? |
| Bloom | Emergent growth | What new possibilities emerge? |
| Evolve | Final refinement | What's the strongest version? |

## References

- `references/report-template.md` - Full markdown report format
- `references/checklist-template.md` - Structured checklist format
- `references/inline-template.md` - Inline revision format
