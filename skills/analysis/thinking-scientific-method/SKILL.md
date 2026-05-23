---
name: thinking-scientific-method
description: Hypothesis → Prediction → Test → Revise with explicit falsification. Use for debugging, feature experimentation, performance investigation, and A/B testing design.
---

# Scientific Method

## Overview

The scientific method is a systematic approach to understanding through observation, hypothesis formation, prediction, testing, and revision. In engineering, it provides rigor to debugging, experimentation, and investigation. The key insight: good hypotheses must be falsifiable—you must be able to prove them wrong.

**Core Principle:** Form hypotheses that could be proven false. Design experiments that could falsify them. Update beliefs based on evidence.

## When to Use

- Debugging (systematic cause identification)
- Performance investigation
- A/B test design
- Feature experimentation
- Root cause analysis
- Data analysis
- Any investigation where you're testing theories

Decision flow:

```
Investigating something?
  → Do you have a clear hypothesis? → no → FORM A HYPOTHESIS
  → Can your hypothesis be proven false? → no → MAKE IT FALSIFIABLE
  → Have you designed a test? → no → DESIGN AN EXPERIMENT
  → Did you update beliefs based on results? → no → REVISE AND ITERATE
```

## The Scientific Method Process

### Step 1: Observe

Gather data about the phenomenon:

```markdown
## Observation

What I'm seeing:
- API latency increased from 200ms to 800ms
- Started approximately Monday 9 AM
- Affects /checkout endpoint
- Other endpoints are normal
- Error rate is normal

Initial data:
- P50: 400ms (was 150ms)
- P99: 2.5s (was 500ms)
- Traffic: Normal levels
```

### Step 2: Question

What do you want to understand?

```markdown
## Question

Central question: Why did /checkout latency increase 4x on Monday?

Sub-questions:
- What changed on/around Monday 9 AM?
- Why only /checkout and not other endpoints?
- Why is P99 more affected than P50?
```

### Step 3: Hypothesize

Form a testable explanation:

```markdown
## Hypothesis

Primary hypothesis:
"The latency increase is caused by the payment provider SDK update
deployed Sunday night, which changed from async to sync API calls."

Why this hypothesis:
- SDK was updated Sunday (timing matches)
- /checkout is the only endpoint using payment SDK (scope matches)
- Sync calls would increase variance (P99 impact matches)
```

**Good hypothesis characteristics:**
- **Testable:** Can design an experiment
- **Falsifiable:** Can be proven wrong
- **Specific:** Not vague or unfalsifiable
- **Explanatory:** Accounts for observations

### Step 4: Predict

What would you expect IF the hypothesis is true?

```markdown
## Predictions

If hypothesis is true:
1. Rolling back the SDK should restore previous latency
2. Traffic to payment provider should show increased duration
3. Thread utilization should be higher (blocking calls)
4. Adding async wrapper should reduce latency

If hypothesis is false:
1. Rollback won't change latency
2. Payment provider call duration is unchanged
3. Thread utilization is normal
```

**Prediction requirement:**
Predictions must differentiate hypothesis-true from hypothesis-false. If both would produce the same observation, the prediction is useless.

### Step 5: Experiment

Design and run a test:

```markdown
## Experiment Design

Test: Deploy SDK rollback to canary group

Setup:
- Control: 90% traffic, new SDK
- Treatment: 10% traffic, old SDK
- Duration: 1 hour
- Metric: P50 and P99 latency

Success criteria:
- If P50 < 200ms in treatment → Hypothesis SUPPORTED
- If P50 > 350ms in treatment → Hypothesis FALSIFIED

Confounds controlled:
- Same time of day as original issue
- Same traffic routing rules
- Same downstream dependencies
```

### Step 6: Analyze

Examine the results:

```markdown
## Results

Control (new SDK):
- P50: 410ms
- P99: 2.4s
- n: 45,000 requests

Treatment (old SDK):
- P50: 155ms
- P99: 480ms
- n: 5,000 requests

Statistical significance: p < 0.001
Effect size: 62% reduction in P50

Analysis:
Hypothesis SUPPORTED. Old SDK shows pre-incident latency levels.
```

### Step 7: Conclude and Iterate

Update beliefs and act:

```markdown
## Conclusion

Finding: Payment SDK update caused latency regression
Confidence: High (controlled experiment, clear signal)

Action:
1. Roll back SDK immediately
2. File bug with payment provider
3. Add latency monitoring for SDK calls
4. Evaluate SDK changes before future updates

Next investigation:
Why didn't we catch this in staging?
Hypothesis: Staging doesn't have realistic payment provider latency
```

## Scientific Debugging

### The Debugging Scientific Method

```markdown
## Bug: Users sometimes see stale data

### Observation
- Reports of stale data from support tickets
- No clear pattern in who/when
- Estimated 5% of users affected

### Hypotheses (Multiple)
| # | Hypothesis | Falsification Test |
|---|------------|-------------------|
| 1 | Cache not invalidating | Check cache hits with stale data |
| 2 | Read replica lag | Check replica lag at time of reports |
| 3 | Browser caching | Check with cache-busted requests |
| 4 | CDN serving old content | Check CDN cache status |

### Testing Strategy
Test in order of: (ease × likelihood)
1. CDN cache status (easy to check)
2. Browser caching (easy to check)
3. Read replica lag (need to correlate times)
4. Cache invalidation (needs instrumentation)

### Test 1: CDN Cache Status
Prediction: If CDN is serving stale content,
            cache headers will show old timestamps
Result: CDN timestamps are fresh
Conclusion: CDN ruled out

### Test 2: Browser Caching
Prediction: If browser caching,
            force-refresh will show correct data
Result: Force-refresh still shows stale data sometimes
Conclusion: Browser caching ruled out

### Test 3: Read Replica Lag
Prediction: If replica lag,
            reports will correlate with lag spikes
Result: Strong correlation (r=0.84) between reports and lag spikes
Conclusion: SUPPORTED - read replica lag is the cause
```

## A/B Test Design

```markdown
## A/B Test: New Checkout Flow

### Hypothesis
"The simplified 2-step checkout will increase conversion rate
compared to current 4-step checkout."

### Predictions
If hypothesis is true:
- Conversion rate increases by >5%
- Time to complete decreases
- Abandonment rate decreases

If hypothesis is false:
- Conversion rate unchanged or decreases
- Potential confusion (errors increase)

### Experiment Design
Control: Current 4-step checkout
Treatment: New 2-step checkout
Traffic split: 50/50
Duration: 2 weeks (for statistical power)
Primary metric: Conversion rate
Guardrail metrics: Error rate, support tickets

### Sample Size Calculation
Baseline conversion: 3.2%
Minimum detectable effect: 5% relative (0.16% absolute)
Required n per group: 150,000 users

### Stopping Criteria
Stop early if:
- Treatment errors > 2x control
- Support tickets > 2x baseline
- p < 0.01 AND effect > 10%
```

## Scientific Method Template

```markdown
# Scientific Investigation: [Topic]

## Observation
What I'm seeing:
- [Observation 1]
- [Observation 2]

Data:
- [Metric]: [Value]

## Question
[Central question to answer]

## Hypotheses
| # | Hypothesis | How to Test | How to Falsify |
|---|------------|-------------|----------------|
| 1 | | | |
| 2 | | | |

## Predictions
If H1 is true:
- [Prediction 1]
- [Prediction 2]

If H1 is false:
- [Counter-prediction 1]

## Experiment
Design: [How to test]
Control: [Baseline]
Treatment: [Intervention]
Metric: [What to measure]
Duration: [How long]
Success criteria: [What constitutes support/falsification]

## Results
[Data from experiment]

## Analysis
Hypothesis [SUPPORTED/FALSIFIED]
Confidence: [High/Medium/Low]
Reasoning: [Why]

## Conclusion
Finding: [What I learned]
Action: [What to do]
Next: [Follow-up investigation]
```

## Verification Checklist

- [ ] Observations documented with data
- [ ] Hypothesis is falsifiable (can be proven wrong)
- [ ] Predictions differentiate true vs. false
- [ ] Experiment controls for confounding variables
- [ ] Results analyzed objectively
- [ ] Conclusion follows from evidence
- [ ] Updated beliefs based on evidence

## Key Questions

- "What would I expect to see if my hypothesis is true?"
- "What would I expect to see if my hypothesis is false?"
- "Can this hypothesis be proven wrong?"
- "Am I testing my hypothesis or confirming my beliefs?"
- "What's the simplest explanation that fits the data?"
- "What evidence would change my mind?"

## Feynman's Wisdom

"The first principle is that you must not fool yourself—and you are the easiest person to fool."

"It doesn't matter how beautiful your theory is, it doesn't matter how smart you are. If it doesn't agree with experiment, it's wrong."

The scientific method protects you from yourself. Your intuition generates hypotheses; the method tests them ruthlessly. When the experiment disagrees with your expectation, the experiment wins.
