---
name: thinking-probabilistic
description: Express confidence in ranges, update predictions with new information, and track calibration over time. Use for project estimation, risk assessment, and decision making under uncertainty.
---

# Probabilistic Thinking

## Overview

Probabilistic thinking, informed by the research of Philip Tetlock's "Superforecasting," treats beliefs as probabilities rather than certainties. Good probabilistic thinkers express confidence in ranges, update beliefs when evidence changes, and track their accuracy to improve calibration over time.

**Core Principle:** Express beliefs as probabilities. Track predictions. Update when wrong. Calibrate over time.

## When to Use

- Project timeline estimation
- Risk assessment
- Predicting outcomes (launches, decisions, events)
- Evaluating uncertain technical choices
- Making decisions without complete information
- Any forecast or prediction

Decision flow:

```
Making a prediction?
  → Is outcome uncertain? → yes → EXPRESS AS PROBABILITY
  → Can you track the outcome? → yes → RECORD AND CALIBRATE
  → New information available? → yes → UPDATE PROBABILITY
```

## Core Concepts

### Probability as Confidence

Convert vague language to numbers:

| Vague Statement | Probability Range |
|-----------------|-------------------|
| "Certain" | 99%+ |
| "Almost certain" | 90-99% |
| "Very likely" | 80-90% |
| "Likely" / "Probable" | 65-80% |
| "Better than even" | 55-65% |
| "Toss-up" | 45-55% |
| "Unlikely" | 20-35% |
| "Very unlikely" | 10-20% |
| "Almost impossible" | 1-10% |
| "Impossible" | <1% |

### Confidence Intervals

Express estimates as ranges, not points:

```
BAD: "The project will take 6 weeks"
GOOD: "I'm 80% confident the project will take 4-8 weeks"
BETTER: "50% confidence: 5-7 weeks; 90% confidence: 3-10 weeks"
```

### Base Rates

Start with how often similar things happen:

```
Question: Will this feature launch on time?
Base rate: What % of similar features launched on time? ~40%
Adjustment: This team is experienced (+10%), scope is clear (+10%)
Estimate: ~60% probability of on-time launch
```

## The Probabilistic Process

### Step 1: Express Initial Probability

State your belief as a number:

```markdown
## Prediction: Will we hit Q2 revenue target?

Initial estimate: 65%
Reasoning:
- Last 4 quarters: Hit 3/4 targets (75% base rate)
- Current pipeline: Slightly below historical (-10%)
- New product launching: Uncertain impact
```

### Step 2: Identify Key Uncertainties

What could change the probability?

```markdown
Key uncertainties:
1. Will Enterprise deal close? (+15% if yes)
2. Will new product cannibalize existing? (-10% if significant)
3. Will competitor launch disrupt? (-20% if aggressive)
```

### Step 3: Create Probability Tree

For complex predictions, branch scenarios:

```
Project success: ?
├── Technical risk resolves well (60%)
│   ├── Team stays intact (80%) → 0.60 × 0.80 = 48% → SUCCESS
│   └── Key person leaves (20%) → 0.60 × 0.20 × 0.50 = 6% → PARTIAL
├── Technical risk causes delays (30%)
│   ├── Scope reduced (60%) → 0.30 × 0.60 × 0.70 = 12.6% → SUCCESS
│   └── Scope maintained (40%) → 0.30 × 0.40 = 12% → FAILURE
└── Technical risk blocks project (10%) → 10% → FAILURE

P(Success) = 48% + 12.6% = 60.6% ≈ 60%
```

### Step 4: Update with New Information

When new evidence arrives, update:

```markdown
Original estimate: 65% hit revenue target

New information: Enterprise deal delayed to Q3
Impact: -15% (was +15% if closed, now neutral)
Updated estimate: 50%

New information: Competitor launch was weak
Impact: +10% (was -20% if aggressive)
Updated estimate: 60%
```

### Step 5: Record and Track

Keep a prediction log:

```markdown
## Prediction Log

| Date | Prediction | Probability | Actual | Brier Score |
|------|------------|-------------|--------|-------------|
| 2024-01-01 | Q1 launch | 70% | Yes | 0.09 |
| 2024-01-15 | Deal closes | 60% | No | 0.36 |
| 2024-02-01 | Bug resolved in 1 week | 80% | Yes | 0.04 |
```

### Step 6: Calibrate Over Time

Review your accuracy:

```markdown
## Calibration Review

For predictions I rated 70%:
- Total predictions: 20
- Actual outcomes "Yes": 12 (60%)
- I'm overconfident by 10% at this level

Adjustment: When I feel "70%", actual is closer to 60%
```

## Calibration Techniques

### The Equivalent Bet Test

"Would I bet at these odds?"

```
Prediction: 80% confident project finishes on time
Equivalent: Would I bet $4 to win $1?
If that feels wrong, adjust the probability.
```

### The Outside View

Always check base rates:

```
Inside view: "Our team is great, we'll definitely finish on time"
Outside view: "What % of similar projects finished on time?"

Inside tends toward overconfidence
Outside provides calibration anchor
```

### The Pre-Mortem Adjustment

Imagine failure, then adjust:

```
Initial estimate: 85% success
After pre-mortem: Identified 5 failure modes I hadn't considered
Adjusted estimate: 70%
```

### The Confidence Interval Check

Are your intervals too narrow?

```
Test: Of your 90% confidence intervals, do 90% contain the actual?
Common finding: Only 60-70% do
Fix: Widen intervals by 50%
```

## Application Examples

### Project Estimation

```markdown
## Project: Payment System Rewrite

Timeline estimate:
- 50% confidence: 8-12 weeks
- 80% confidence: 6-16 weeks
- 95% confidence: 4-24 weeks

Key variables:
- API complexity: High uncertainty (+/- 3 weeks)
- Team availability: Medium uncertainty (+/- 2 weeks)
- Integration testing: High uncertainty (+/- 4 weeks)

Commitment: "We're 80% confident we'll deliver in Q2"
```

### Risk Assessment

```markdown
## Risk: Database migration causes extended downtime

Probability assessment:
- Base rate for similar migrations: 20% have issues
- Our preparation level: Above average (-5%)
- Complexity of our schema: Above average (+5%)
- Rollback plan quality: Strong (-5%)

Estimate: 15% probability of extended downtime

Mitigation value:
- If issue occurs: 4 hours downtime × $10K/hour = $40K
- Expected loss: 15% × $40K = $6K
- Mitigation cost: $3K for additional testing
- Decision: Mitigation worth it (ROI positive)
```

### Technical Decision

```markdown
## Decision: Adopt new framework

Success probability factors:
| Factor | Probability | Weight |
|--------|-------------|--------|
| Team learns quickly | 70% | 0.3 |
| Framework matures | 80% | 0.2 |
| Performance meets needs | 60% | 0.3 |
| Integration works | 75% | 0.2 |

Combined probability (simplified):
0.70 × 0.80 × 0.60 × 0.75 = 25% (if all must succeed)
OR weighted average: 70% (if partial success acceptable)

Decision: High uncertainty suggests pilot first
```

## Brier Score for Calibration

Track prediction accuracy with Brier Score:

```
Brier Score = (probability - outcome)²

Where outcome = 1 if happened, 0 if not

Example:
Predicted 70% (0.70), it happened (1)
Brier = (0.70 - 1)² = 0.09

Predicted 70% (0.70), it didn't happen (0)
Brier = (0.70 - 0)² = 0.49

Lower is better. Perfect = 0, Random = 0.25
```

## Probabilistic Thinking Template

```markdown
# Probabilistic Assessment: [Prediction]

## Prediction
[Clear, falsifiable statement with timeframe]

## Initial Probability
Estimate: [X]%
Base rate: [Similar events: Y%]
Adjustment rationale: [Why different from base rate]

## Confidence Interval
- 50% CI: [Range]
- 80% CI: [Range]
- 95% CI: [Range]

## Key Uncertainties
| Uncertainty | If positive | If negative |
|-------------|-------------|-------------|
| [Factor 1] | +X% | -Y% |
| [Factor 2] | +X% | -Y% |

## Update Log
| Date | New Information | Old P | New P |
|------|-----------------|-------|-------|
| | | | |

## Resolution
Date: [When known]
Outcome: [What happened]
Brier Score: [Calculation]
Lessons: [What to learn]
```

## Verification Checklist

- [ ] Expressed prediction as specific probability
- [ ] Checked base rate for similar events
- [ ] Created appropriate confidence intervals
- [ ] Identified key uncertainties and their impacts
- [ ] Recorded prediction for future calibration
- [ ] Applied equivalent bet test for sanity check
- [ ] Willing to update when new information arrives

## Key Questions

- "What probability would I assign to this?"
- "What's the base rate for similar things?"
- "What would change my estimate up or down?"
- "Am I being overconfident? (Usually yes)"
- "What's my track record at this confidence level?"
- "Would I bet at these odds?"

## Tetlock's Superforecaster Traits

1. **Update often:** Change predictions when evidence changes
2. **Granular probabilities:** Use 65% not "likely"
3. **Outside view:** Start with base rates
4. **Seek disconfirming evidence:** Look for reasons you're wrong
5. **Track record:** Keep score, learn from errors
6. **Intellectual humility:** Know you're often wrong

## Tetlock's Wisdom

"The fox knows many things, but the hedgehog knows one big thing."

Superforecasters are foxes—they integrate many perspectives, update frequently, and avoid ideological certainty. They're not smarter; they're more calibrated.

"Beliefs are hypotheses to be tested, not treasures to be protected."

Your predictions should change as evidence changes. Holding steady when you should update is a calibration failure.
