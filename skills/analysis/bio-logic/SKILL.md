---
name: bio-logic
description: Evaluates scientific research rigor using systematic frameworks. Assesses methodology, statistics, biases, and evidence quality. Use when reviewing papers, critiquing claims, designing studies, rating evidence strength (GRADE/Cochrane ROB), checking study design, statistical critique, or risk of bias assessment.
---

# Bio-Logic: Scientific Reasoning Evaluation

## Instructions

1. **Identify the task** using Quick Reference below
2. **Use the appropriate framework** from this file or references
3. **Adapt depth to context** - use full checklists for thorough reviews, key items for quick assessments
4. **Structure output** using the Output Format template

## Quick Reference

Navigate to the right tool for your task:

| Task | Location |
|------|----------|
| Review a paper | [Critique Checklist](#critique-checklist) below |
| Evaluate a claim | [Claim Assessment](#claim-assessment) below |
| Assess evidence strength | [references/evidence.md](references/evidence.md) |
| Identify biases | [references/biases.md](references/biases.md) |
| Spot statistical errors | [references/stats.md](references/stats.md) |
| Detect logical fallacies | [references/fallacies.md](references/fallacies.md) |
| Design/review a study | [references/design.md](references/design.md) |

## Critique Checklist

Use relevant sections based on the review scope. Skip items not applicable to the study type.

```
## Methodology
- [ ] Design matches research question (causal claim → RCT needed)
- [ ] Sample size justified (power analysis reported)
- [ ] Randomization/blinding implemented where feasible
- [ ] Confounders identified and controlled
- [ ] Measurements validated and reliable

## Statistics
- [ ] Tests appropriate for data type
- [ ] Assumptions checked
- [ ] Multiple comparisons corrected
- [ ] Effect sizes + CIs reported (not just p-values)
- [ ] Missing data handled appropriately

## Interpretation
- [ ] Conclusions match evidence strength
- [ ] Limitations acknowledged
- [ ] Causal claims only from experimental designs
- [ ] No cherry-picking or overgeneralization

## Red Flags
- [ ] P-values clustered just below .05
- [ ] Outcomes differ from registration
- [ ] Correlation presented as causation
- [ ] Subgroups analyzed without preregistration
```

## Claim Assessment

For any scientific claim:

1. **Identify claim type**: Causal, associational, or descriptive?
2. **Match evidence to claim**: Does study design support this claim type?
3. **Check logical connection**: Do conclusions follow from data?
4. **Evaluate proportionality**: Is confidence matched to evidence strength?

**Causal claims require**: Temporal precedence + covariation + alternative explanations ruled out (ideally experimental manipulation).

**Claim strength ladder**:
| Language | Requires |
|----------|----------|
| "Proves" / "Demonstrates" | Strong experimental evidence |
| "Suggests" / "Indicates" | Observational with controlled confounds |
| "Associated with" | Observational, no causal claim |
| "May" / "Might" | Preliminary or hypothesis-generating |

## Output Format

Structure critiques as:

```markdown
## Summary
[1-2 sentences: What was studied and main finding]

## Strengths
- [Specific methodological strengths]

## Concerns
### Critical (threaten main conclusions)
- [Issue + why it matters]

### Important (affect interpretation)
- [Issue + why it matters]

### Minor (worth noting)
- [Issue]

## Evidence Rating
[GRADE level: High/Moderate/Low/Very Low with justification]

## Bottom Line
[What can/cannot be concluded from this evidence]
```

## Examples

### Example 1: Quick Paper Critique

**Input**: "Review this RCT on vitamin D and depression"

**Output**:
```
## Summary
RCT of 200 adults testing vitamin D supplementation for depression over 12 weeks.

## Strengths
- Randomized, double-blind, placebo-controlled
- Validated depression scale (PHQ-9)
- Adequate power analysis

## Concerns
### Critical
- 35% dropout, differential by group (attrition bias)
- ITT analysis not performed

### Important
- Single-site limits generalizability

## Evidence Rating
Moderate (downgraded from high due to attrition bias)

## Bottom Line
Suggestive but not conclusive due to differential attrition.
```

### Example 2: Claim Assessment

**Input**: "This study proves that coffee prevents Alzheimer's"

**Assessment**: Claim uses causal language ("prevents") but if based on observational data, this is a correlation→causation fallacy. Would need RCT or strong observational evidence (large effect, dose-response, controlled confounds) to support causal claim. Appropriate language: "Coffee consumption is associated with lower Alzheimer's risk."

## Principles

1. **Be constructive** - Identify strengths, suggest improvements
2. **Be specific** - Quote problematic statements, cite specific issues
3. **Be proportionate** - Match criticism severity to impact on conclusions
4. **Be consistent** - Same standards regardless of whether you agree with findings
5. **Distinguish** - Data vs interpretation, correlation vs causation, statistical vs practical significance

## Reference Materials

Detailed frameworks for specific evaluation tasks:

- **[references/evidence.md](references/evidence.md)** - GRADE system, evidence hierarchy, validity types, Bradford Hill criteria
- **[references/biases.md](references/biases.md)** - Bias taxonomy with detection strategies
- **[references/stats.md](references/stats.md)** - Statistical pitfalls and correct interpretations
- **[references/fallacies.md](references/fallacies.md)** - Logical fallacies in scientific arguments
- **[references/design.md](references/design.md)** - Experimental design checklist
