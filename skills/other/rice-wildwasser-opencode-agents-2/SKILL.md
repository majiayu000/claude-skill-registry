---
name: rice
description: RICE prioritization scoring initiatives by Reach, Impact, Confidence, and Effort. Use for feature prioritization, roadmap planning, or when comparing initiatives objectively.
user-invocable: true
---

# RICE Prioritization Scoring

Score and rank initiatives using Reach, Impact, Confidence, and Effort to make prioritization decisions more objective.

## Instructions

For each initiative, estimate the four RICE factors, calculate the score, and rank them. Be explicit about assumptions behind each estimate.

### Output Format

**Context**
What are we prioritizing? What's the time horizon for Reach?

**Factor Definitions**
- **Reach**: [Define for this context, e.g., "users affected per quarter"]
- **Impact**: [Define for this context, e.g., "effect on conversion rate"]
- **Effort**: [Define unit, e.g., "engineer-weeks"]

**Scoring Table**

| Initiative | Reach | Impact | Confidence | Effort | RICE Score |
|------------|-------|--------|------------|--------|------------|
| [Name A] | [#] | [0.25-3] | [%] | [#] | [calculated] |
| [Name B] | [#] | [0.25-3] | [%] | [#] | [calculated] |
| [Name C] | [#] | [0.25-3] | [%] | [#] | [calculated] |

**Ranked Results**

1. **[Highest score]** — RICE: X
2. **[Second]** — RICE: X
3. **[Third]** — RICE: X

**Detailed Breakdown**

For each initiative:

### [Initiative Name]
- **Reach**: [X] — [Assumption: how did you estimate this?]
- **Impact**: [X] — [Reasoning for impact level]
- **Confidence**: [X%] — [What would increase confidence?]
- **Effort**: [X] — [What's included in this estimate?]
- **RICE Score**: (R × I × C) / E = [score]

**Sensitivity Analysis**
Which scores would change significantly if assumptions are wrong?

**Recommendation**
Based on the scores and analysis:
> [What to prioritize and why, including any caveats]

**What RICE Doesn't Capture**
- Strategic alignment
- Dependencies
- Team capability gaps
- Technical risk

## Scoring Guide

**Impact Scale**
| Score | Meaning |
|-------|---------|
| 3 | Massive — core value prop |
| 2 | High — significant improvement |
| 1 | Medium — noticeable improvement |
| 0.5 | Low — minor enhancement |
| 0.25 | Minimal — nice to have |

**Confidence Scale**
| Score | Meaning |
|-------|---------|
| 100% | High — have data |
| 80% | Medium — reasonable estimate |
| 50% | Low — mostly guessing |

$ARGUMENTS
