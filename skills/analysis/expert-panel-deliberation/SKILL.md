---
name: expert-panel-deliberation
description: >
  Multi-expert evaluation pattern for structured analysis and decision-making.
  PROACTIVELY activate for: (1) Analyze with expert perspectives, (2) Get multiple
  viewpoints on a topic, (3) Evaluate options with diverse expertise, (4) Build
  consensus from different angles, (5) Structured deliberation on complex topics.
  
  Triggers: "analyze with expert panel", "get expert perspectives", "what would
  experts say", "evaluate from different angles", "run expert deliberation",
  "multi-perspective analysis"
---

# Expert Panel Deliberation

Structured multi-expert evaluation, deliberation, and consensus building.

## Purpose

Provide consistent, high-quality multi-perspective analysis by:
- Instantiating domain-appropriate expert panels
- Executing structured deliberation protocols
- Resolving conflicts between viewpoints
- Building weighted consensus
- Documenting reasoning and dissent

## When to Use

**Ideal for:**
- Decisions requiring multiple perspectives
- Evaluating options with tradeoffs
- Complex topics with no single right answer
- Building confidence through diverse viewpoints

**Avoid when:**
- Simple factual questions
- Time-critical decisions needing speed
- Single-domain technical questions

## Checkpoints

This skill uses interactive checkpoints (see `references/checkpoints.yaml`) to resolve ambiguity:
- **domain_context** — When domain not specified
- **output_format_selection** — When output format not specified
- **deliberation_depth_selection** — When depth could vary based on stakes
- **panel_composition** — When archetype selection is ambiguous
- **panel_size_adjustment** — When specified size conflicts with recommended
- **conflict_resolution_approach** — When unresolved conflicts need user input
- **weighting_approach** — When consensus weighting is ambiguous
- **dissent_documentation** — When minority view significance is unclear

## Workflow

### Step 1: Define Panel Requirements

Determine what evaluation is needed:
- **Subject:** What is being evaluated?
- **Goal:** What should the evaluation determine?
- **Panel size:** 3-8 experts (default: 5)
- **Output format:** findings | scores | ranking | recommendation

**CHECKPOINT: domain_context**
- If domain not specified and not inferable from subject: **AskUserQuestion**
- Options: Architecture, Product, Security, Operations, Business, Custom
- Example: "What domain is this evaluation for?"

**CHECKPOINT: output_format_selection**
- If output format not specified: **AskUserQuestion**
- Options: Findings, Scores, Ranking, Recommendation
- Example: "What output format would be most useful?"

**CHECKPOINT: deliberation_depth_selection**
- If stakes unclear and depth not specified: **AskUserQuestion**
- Options: Quick, Standard, Deep
- Example: "How thorough should the deliberation be?"

### Step 2: Assemble Expert Panel

Select from archetypes based on domain:

| Archetype | Focus | Include When |
|-----------|-------|--------------|
| Technical Authority | Architecture, implementation | Technical subjects |
| Quality Guardian | Standards, testing | Quality assessment |
| User Advocate | Experience, usability | User-facing topics |
| Risk Specialist | Failures, compliance | Risk assessment |
| Efficiency Expert | Cost, automation | Resource decisions |
| Domain Specialist | Best practices | Domain-specific topics |
| Challenger | Questioning assumptions | Always (at least 1) |

**Panel composition rules:**
- Minimum 3 experts for meaningful deliberation
- Maximum 8 experts (diminishing returns beyond)
- Always include at least one challenger perspective
- Balance technical and business viewpoints

**CHECKPOINT: panel_composition**
- If subject matches multiple domains or custom panel needed: **AskUserQuestion**
- Options: Architecture panel, Product panel, Security panel, Custom selection
- Example: "Which expert panel composition fits best?"

**CHECKPOINT: panel_size_adjustment**
- If user-specified size differs significantly from recommended: **AskUserQuestion**
- Example: "You specified 3 experts, but this topic typically benefits from 5. Which size?"

### Step 3: Execute Individual Evaluation

For each expert:
1. **Adopt perspective** — Review role, expertise, concerns
2. **Evaluate subject** — Answer from expert's viewpoint
3. **Score** (if applicable) — Rate relevant dimensions
4. **Document** — Key findings, concerns, recommendations

### Step 4: Execute Deliberation

**Round 1: Finding Presentation**
- Each expert presents top findings
- No debate yet; just surface perspectives

**Round 2: Cross-Examination**
- Experts question each other's findings
- Surface disagreements and gaps

**Round 3: Conflict Resolution**
- Address disagreements systematically
- Document resolved vs. unresolved conflicts

**Round 4: Consensus Building**
- Identify areas of agreement
- Weight by expert influence
- Synthesize combined view

**CHECKPOINT: conflict_resolution_approach**
- If significant conflicts remain unresolved: **AskUserQuestion**
- Options: Weight by domain, Weight by evidence, Document both, Escalate to user
- Example: "Technical Authority and User Advocate disagree. How should we resolve?"

**CHECKPOINT: weighting_approach**
- If weighting algorithm not specified and experts have unequal relevance: **AskUserQuestion**
- Options: Equal weight, Domain relevance, Confidence-adjusted, Evidence-based
- Example: "How should expert perspectives be weighted?"

### Step 5: Generate Output

Format based on requested output type.

**CHECKPOINT: dissent_documentation**
- If minority views exist and significance unclear: **AskUserQuestion**
- Options: Document prominently, Document briefly, Omit
- Example: "Risk Specialist disagrees with consensus. How should we document this?"

## Output Format
```markdown
## Expert Panel Analysis: [Subject]

### Panel Composition
- **[Expert 1 Role]:** [brief expertise]
- **[Expert 2 Role]:** [brief expertise]
...

### Key Findings

**Consensus Views:**
1. [Finding agreed by most/all experts] (Confidence: HIGH/MED/LOW)
2. [Finding agreed by most/all experts] (Confidence: HIGH/MED/LOW)

**Divergent Views:**
- [Expert] believes [X] while [Expert] believes [Y]
  - Resolution: [how addressed or "unresolved"]

### Scores (if applicable)

| Dimension | Score | Confidence |
|-----------|-------|------------|
| [dim] | [X/10] | [H/M/L] |

### Recommendations

1. [Primary recommendation]
2. [Secondary recommendation]

### Dissent Record

[Any unresolved disagreements and minority views]
```

## Quality Gates

- [ ] All requested experts contributed
- [ ] Each expert answered from their perspective
- [ ] Conflicts identified and addressed
- [ ] Weights properly applied
- [ ] Consensus clearly stated
- [ ] Dissent documented if present
- [ ] Confidence levels assigned
- [ ] All applicable checkpoints evaluated (ambiguity resolved via AskUserQuestion)

## Parameters

| Parameter | Default | Options |
|-----------|---------|---------|
| `panel_size` | 5 | 3-8 |
| `deliberation_depth` | standard | quick, standard, deep |
| `output_format` | findings | findings, scores, ranking, recommendation |
| `include_challenger` | true | true, false |

## Examples

**Example 1: Architecture Decision**
User: Analyze our microservices vs monolith decision with an expert panel
Panel: Technical Authority, Quality Guardian, Risk Specialist,
Efficiency Expert, Challenger
[Deliberation proceeds with each expert evaluating from their perspective]

**Example 2: Feature Prioritization**
User: Get expert perspectives on which features to build next quarter
Panel: User Advocate, Domain Specialist, Technical Authority,
Efficiency Expert, Challenger
[Deliberation with scoring output]
