---
name: run-research-pipeline
description: >
  Full research workflow orchestration from knowledge elicitation to consolidated findings.
  PROACTIVELY activate for: (1) end-to-end research projects, (2) comprehensive analysis,
  (3) strategic research requiring multiple phases, (4) complex research questions.
  Triggers: "run research pipeline", "full research workflow", "comprehensive research",
  "end-to-end research", "complete research process"
argument-hint: [topic]
disable-model-invocation: true
context: fork
agent: general-purpose
---

# Run Research Pipeline

Execute a complete research workflow from problem definition through consolidated findings.

## When to Use

Use this skill when you need:
- End-to-end research on a complex topic
- Structured progression through all research phases
- Multi-LLM research design and synthesis
- Comprehensive analysis with quality gates at each phase

## Pipeline Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH PIPELINE                         │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Phase 1: ELICITATION                                       │
│  ┌─────────────────────┐                                    │
│  │ research-interview  │ → PROBLEM-STATEMENT                │
│  └─────────────────────┘                                    │
│            ↓                                                 │
│  Phase 2: DESIGN                                            │
│  ┌─────────────────────┐                                    │
│  │ research-brief      │ → Model-optimized prompts          │
│  └─────────────────────┘                                    │
│            ↓                                                 │
│  Phase 3: EXECUTION (User)                                  │
│  ┌─────────────────────┐                                    │
│  │ Run prompts in      │ → Raw model outputs                │
│  │ Claude, Gemini, GPT │                                    │
│  └─────────────────────┘                                    │
│            ↓                                                 │
│  Phase 4: SYNTHESIS                                         │
│  ┌─────────────────────┐                                    │
│  │ consolidate-research│ → CONSOLIDATED-REPORT              │
│  └─────────────────────┘                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Workflow

Execute complete research pipeline for: "$ARGUMENTS"

### Phase 1: Knowledge Elicitation

Run `research-interviewer` to produce PROBLEM-STATEMENT:

**Objective:** Define the research question clearly with:
- Core question and sub-questions
- Key constraints and assumptions
- Success criteria
- Known information vs gaps

**Output:** `<problem-statement>` artifact with confidence scores

**Quality Gate:**
- [ ] Research question is specific and answerable
- [ ] Assumptions surfaced and examined
- [ ] Scope boundaries defined
- [ ] Success criteria measurable

### Phase 2: Research Design

Run `create-research-brief` Phase 1 to generate:

**Objective:** Design multi-LLM research strategy with:
- MECE question decomposition (5 categories)
- Model-optimized prompts for Claude, Gemini, GPT
- Risk assessment for the research approach

**Model Assignment Strategy:**

| Model | Strength | Best For |
|-------|----------|----------|
| Claude Opus 4.5 | Judgment, synthesis | Strategic questions, nuance |
| Gemini Pro 3 | Breadth, citations | Factual lookup, sourcing |
| GPT-5.2 Deep | Recency, depth | Technical details, edge cases |

**Output:** `<research-brief>` with prompts for each model

**Quality Gate:**
- [ ] MECE decomposition complete (no overlaps/gaps)
- [ ] Each sub-question independently researchable
- [ ] Model assignments match model strengths
- [ ] Prompts optimized for each model's style

### Phase 3: User Executes Prompts

**PAUSE POINT** - Display prompts for user to execute:

```markdown
## Ready for Multi-Model Research

Execute the following prompts in each model:

### Claude (Opus 4.5)
[Display Claude prompt]

### Gemini (Pro 3)
[Display Gemini prompt]

### GPT (5.2 Deep)
[Display GPT prompt]

---

**Instructions:**
1. Copy each prompt to its designated model
2. Collect the responses
3. Paste all responses back here to continue to Phase 4
```

**Wait for user to provide model outputs before continuing.**

### Phase 4: Consolidation

Run `create-research-brief` Phase 2 to synthesize:

**Objective:** Produce unified findings with:
- Evidence scoring (5-point scale)
- Conflict resolution (WWHTBT protocol)
- Uncertainty classification
- MECE coverage audit

**Output:** `<consolidated-report>` with:
- Executive summary
- Findings by category with evidence scores
- Conflicts resolved and rationale
- Remaining gaps and recommendations

**Quality Gate:**
- [ ] All model outputs incorporated
- [ ] Evidence scores assigned
- [ ] Conflicts explicitly resolved
- [ ] Actionable recommendations provided

## Output Format

Final pipeline output includes all artifacts:

```xml
<research-pipeline-output>
  <metadata>
    <topic>$ARGUMENTS</topic>
    <pipeline_id>[unique identifier]</pipeline_id>
    <completed_phases>[1,2,3,4]</completed_phases>
  </metadata>

  <phase-1-output>
    <problem-statement>...</problem-statement>
  </phase-1-output>

  <phase-2-output>
    <research-brief>...</research-brief>
  </phase-2-output>

  <phase-3-inputs>
    <model-response model="claude">...</model-response>
    <model-response model="gemini">...</model-response>
    <model-response model="gpt">...</model-response>
  </phase-3-inputs>

  <phase-4-output>
    <consolidated-report>...</consolidated-report>
  </phase-4-output>

  <next-steps>
    [Recommended follow-up actions]
  </next-steps>
</research-pipeline-output>
```

## Quality Gates (Pipeline-Level)

- [ ] All four phases completed
- [ ] Each phase passed its quality gates
- [ ] Artifacts linked and traceable
- [ ] Final recommendations actionable
- [ ] Confidence levels appropriate for decision-making

## Post-Pipeline Options

After completing the research pipeline:

| If you need to... | Use skill... |
|-------------------|--------------|
| Evaluate options from findings | `/compare-options` |
| Get expert validation | `/run-expert-panel` |
| Document the methodology | `/write-reference` |
| Create implementation guide | `/write-howto` |
| Optimize follow-up prompts | `/optimize-prompt` |
