---
name: discover-outcomes
description: Use at the start of product strategy to define or refine desired outcomes and success metrics (e.g., for Opportunity Solution Trees or continuous discovery) before selecting opportunities or solutions.
---

# Discover Outcomes

## Overview
Define outcomes that describe measurable behavior change or business impact, not features. Build a clear outcome ladder so opportunity discovery and solution ideas have a shared target.

## Position in Workflow

Step 1 of product strategy workflow:
1. `/discover-outcomes` - Define outcomes (THIS)
2. `/discover-opportunities` - Identify opportunities
3. `/ideate-solutions` - Explore solution concepts
4. `/discover-assumptions` - Validate with experiments

## Inputs (ask if missing, max 5)
- Business or product goal (north star)
- Target segment or market
- Baseline metrics or current state
- Time horizon for change
- Constraints (budget, compliance, strategy)

## Workflow
1. **Separate outcomes from outputs**
   - Outcomes are measurable changes; outputs are features or deliverables.
2. **Outcome laddering (OST-style)**
   - Start with the top-level outcome.
   - Ask: "What must be true for this to happen?" to create 2-3 supporting levels.
3. **Write precise outcome statements**
   - Use actor + behavior change + context + metric.
4. **Attach metrics and baselines**
   - Include leading and lagging indicators.
   - Specify baseline, target, and time window.
5. **Prioritize outcomes**
   - Score impact, controllability, time-to-learn, and strategic fit.
6. **Handoff**
   - If outcomes are set, move to `/discover-opportunities` or `/discover-assumptions`.

## Outcome Statement Templates
```
Increase [actor behavior] in [context] from [baseline] to [target] within [time].
Reduce [friction/cost/risk] for [actor] during [context] by [amount] within [time].
```

## Output Format
```
## Outcome Discovery

### Context Summary
[1-3 sentences]

### Outcome Ladder
- Level 1 (Top outcome): ...
  - Level 2: ...
    - Level 3: ...

### Metrics
- Outcome: ...
  - Leading indicators: ...
  - Lagging indicators: ...
  - Baseline: ...
  - Target: ...
  - Time window: ...

### Prioritized Outcomes
1) ... (impact X, controllability X, time-to-learn X, strategic fit X)
2) ...

### Open Questions
- ...

### Next Step
Proceed to opportunity discovery. Run `/discover-opportunities`.
```

## Quick Reference
- Outcomes = behavior or business change; outputs = features.
- Always include baseline + target + time window.
- Keep ladder depth to 2-3 levels unless complexity demands more.

## Common Mistakes
- Writing features as outcomes
- No baseline or time window
- Skipping leading indicators
- Ladders that are too deep or too vague
