---
name: evaluator-optimizer
description: Iterative refinement workflow for polishing code, documentation, or designs through systematic evaluation and improvement cycles. Use when refining drafts into production-grade quality.
keywords:
  - refinement
  - iteration
  - code quality
  - evaluation
  - optimization
  - polish
triggers:
  - refine this
  - polish this
  - optimize this
  - improve iteratively
  - evaluator-optimizer
---

# Evaluator-Optimizer

Iterative refinement workflow that takes existing code, documentation, or designs and polishes them through rigorous cycles of evaluation and improvement until they meet production-grade quality standards.

## When to Use This Skill

- Refining a rough draft of code into production quality
- Polishing documentation for clarity, completeness, and accuracy
- Iteratively improving a design or architecture proposal
- Systematic quality improvement where "good enough" is not sufficient
- When you need to converge on high quality through structured iteration

## Quick Reference

| Task | Load reference |
| --- | --- |
| Evaluation criteria and quality rubrics | `skills/evaluator-optimizer/references/evaluation-criteria.md` |

## Workflow: The Loop

For any given artifact (code, text, design):

1. **Accept**: Take the current version of the artifact.
2. **Evaluate**: Act as a harsh critic. Rate the artifact on correctness, clarity, efficiency, style, and safety. Assign a score out of 100.
3. **Decide**:
   - Score >= 90: **Stop** and present the result.
   - Score < 90: **Refine**.
4. **Refine**: Rewrite the artifact, specifically addressing the critique from step 2. List what changed and why.
5. **Repeat**: Return to step 2 with the new version.

## Behavioral Rules

- **Do not settle**: "Good enough" is not good enough. You are here to polish.
- **Be explicit**: When evaluating, list specific flaws. "The function `process_data` is O(n^2) but could be O(n)."
- **Show your work**: Summarize changes in each iteration.
- **Self-correct**: If a refinement breaks something, revert and try a different approach.
- **Converge**: Each iteration must improve the score. If two consecutive iterations do not improve the score, stop and present the best version.

## Iteration Output Template

```markdown
## Iteration [N] Evaluation

| Criterion | Score (1-10) | Notes |
|-----------|-------------|-------|
| Correctness | | |
| Clarity | | |
| Efficiency | | |
| Style | | |
| Safety | | |
| **Total** | **/50** | **[x100/50]** |

### Issues Found
1. [Specific issue with location]
2. [Specific issue with location]

### Refinements Applied
- [Change 1 and rationale]
- [Change 2 and rationale]
```

## Example Interaction

**Input**: "Refine this Python script."

**Iteration 1 Evaluation**:
- Functionality: Good
- Efficiency: Poor - uses nested loops for matching
- Style: Variable names `a` and `b` are unclear
- Score: 60/100

**Refinements applied**:
- Flattened loops using a set lookup (O(n))
- Renamed `a` to `users`, `b` to `active_ids`
- Added type hints

**Iteration 2 Evaluation**:
- Functionality: Good
- Efficiency: Excellent
- Style: Good
- Score: 95/100

Result: Present the refined script.
