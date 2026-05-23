---
name: estimating-work
description: Estimate effort for development tasks. Use when planning sprints, roadmaps, or project timelines. Covers story points, relative estimation, and uncertainty.
allowed-tools: Read, Glob, Grep
---

# Estimating Work

## Estimation Approaches

### Story Points
Relative complexity, not time.

| Points | Complexity |
|--------|------------|
| 1 | Trivial, well understood |
| 2 | Simple, minor unknowns |
| 3 | Moderate complexity |
| 5 | Complex, some unknowns |
| 8 | Very complex, significant unknowns |
| 13 | Extremely complex, many unknowns |
| 21+ | Too big, needs decomposition |

### T-Shirt Sizing
For high-level estimates.

| Size | Relative Effort |
|------|-----------------|
| XS | Hours |
| S | 1-2 days |
| M | 3-5 days |
| L | 1-2 weeks |
| XL | 2-4 weeks |

## Estimation Factors

Consider:
- **Complexity**: How difficult is the problem?
- **Uncertainty**: How much is unknown?
- **Effort**: How much work is involved?
- **Risk**: What could go wrong?

## Estimation Techniques

### Planning Poker
1. Present the task
2. Everyone selects estimate privately
3. Reveal simultaneously
4. Discuss outliers
5. Re-estimate if needed

### Three-Point Estimation
```
Expected = (Optimistic + 4×Likely + Pessimistic) / 6
```

### Reference Stories
Keep calibration stories:
- "This 3-point story took 2 days"
- "This 8-point story took a week"

## Common Pitfalls

- **Anchoring**: First estimate biases others
- **Optimism**: Underestimating unknowns
- **Scope Creep**: Original estimate doesn't match final scope
- **Ignoring Overhead**: Code review, testing, deployment

## Tips

1. Estimate in ranges, not points
2. Include buffer for unknowns
3. Track actual vs. estimated
4. Re-estimate when scope changes
5. Don't estimate in hours (use relative sizing)
