---
name: vibe-iteration-review
description: Performs end-of-iteration review with quality grading, metrics, and trend analysis. Use at the end of each development iteration or sprint.
user-invocable: true
---

# vibe-iteration-review

What gets measured gets improved. Review every iteration.

## When to Use This Skill

- End of a development sprint or iteration
- After completing a milestone
- Before starting the next iteration (retrospective)
- When the user asks "how did we do?"

## When NOT to Use This Skill

- Mid-iteration (too early, incomplete data)
- After single small tasks
- When there's no defined iteration boundary

## Steps

1. **Gather data**:
   - What was planned for this iteration?
   - What was actually delivered?
   - How many commits? Lines changed? Tests added?
   - Coverage delta? Quality metrics?
   - Known issues introduced?

2. **Grade quality** (A-F):
   - **A**: All planned work delivered, tests pass, no known issues, clean code
   - **B**: Most work delivered, minor issues, good test coverage
   - **C**: Core work delivered, some gaps, acceptable quality
   - **D**: Significant gaps, quality issues, needs rework
   - **F**: Iteration failed, major rework needed

3. **Compare to previous iterations** (if available):
   - Is quality trending up or down?
   - Is velocity improving?
   - Are known issues accumulating?

4. **Extract lessons**:
   - What went well?
   - What went poorly?
   - What to change next iteration?

## Output Format

### Iteration Review: [Iteration Name/Number]

**Quality Grade**: A/B/C/D/F
**Planned vs Delivered**: X/Y (Z%)

| Metric | This Iteration | Previous | Trend |
|--------|---------------|----------|-------|
| Commits | X | Y | ↑/↓/→ |
| Tests added | X | Y | ↑/↓/→ |
| Coverage | X% | Y% | ↑/↓/→ |
| Known issues | X | Y | ↑/↓/→ |

### Delivered
- [x] [Task 1]
- [x] [Task 2]
- [ ] [Task 3] — deferred because [reason]

### Lessons Learned
1. [What to continue]
2. [What to change]
3. [What to stop]
