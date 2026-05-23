---
name: thinking-bayesian
description: Update beliefs systematically based on new evidence using probabilistic reasoning. Use when estimating probabilities, learning from data, or making decisions under uncertainty.
---

# Bayesian Reasoning

## Overview
Bayesian thinking provides a framework for updating beliefs based on new evidence. Rather than treating beliefs as binary (true/false), it recognizes degrees of confidence that should shift as evidence accumulates. This approach, rooted in Bayes' Theorem, helps avoid both overconfidence and underreaction to new information.

**Core Principle:** Beliefs are probabilities that should update incrementally as evidence arrives. Strong priors require strong evidence to shift.

## When to Use
- Estimating probabilities or likelihoods
- Interpreting test results or metrics
- Making decisions with incomplete information
- Evaluating competing hypotheses
- Learning from experiments or A/B tests
- Diagnosing problems with uncertain causes
- Predicting outcomes based on historical data

Decision flow:
```
Uncertain about something? → yes → Have prior belief? → yes → New evidence? → APPLY BAYESIAN UPDATE
                                                      ↘ no → Establish base rate first
                         ↘ no → Standard analysis may suffice
```

## Key Concepts

### Prior Probability
Your belief BEFORE seeing new evidence:
```
P(H) = probability that hypothesis H is true

Example: Before any symptoms, what's the probability someone has disease X?
         Use base rate: If 1 in 1000 people have it, P(disease) = 0.001
```

### Likelihood
How probable is the evidence IF the hypothesis is true?
```
P(E|H) = probability of seeing evidence E, given H is true

Example: If someone HAS the disease, what's the probability of a positive test?
         If test is 99% sensitive: P(positive|disease) = 0.99
```

### Posterior Probability
Your belief AFTER seeing the evidence:
```
P(H|E) = updated probability of H, given you observed E

This is what Bayes' Theorem calculates.
```

## Bayes' Theorem

```
                P(E|H) × P(H)
P(H|E) = ─────────────────────────
                   P(E)

Where:
  P(H|E) = posterior (what we want)
  P(E|H) = likelihood (how expected is evidence if H true)
  P(H)   = prior (initial belief)
  P(E)   = total probability of evidence
```

### Intuitive Form

```
Posterior odds = Prior odds × Likelihood ratio

If evidence is 10x more likely under H than under not-H,
your odds should shift by factor of 10.
```

## The Process

### Step 1: Establish Your Prior
What did you believe before this evidence?
- Use base rates when available
- Be explicit about uncertainty
- Don't anchor on 50% just because you're unsure

```
Question: Will this feature increase conversion?
Prior: Based on similar features, ~30% succeed significantly
       P(success) = 0.30
```

### Step 2: Assess the Evidence
How strong is this evidence? Consider:
- How likely is this evidence if hypothesis is TRUE?
- How likely is this evidence if hypothesis is FALSE?
- What's the ratio?

```
Evidence: Early A/B test shows 5% lift (p=0.08)
P(this result | feature works) = 0.60 (moderately expected)
P(this result | feature doesn't work) = 0.15 (possible but less likely)
Likelihood ratio = 0.60 / 0.15 = 4x
```

### Step 3: Update Your Belief
Apply the likelihood ratio to your prior:

```
Prior odds: 0.30 / 0.70 = 0.43
Likelihood ratio: 4x
Posterior odds: 0.43 × 4 = 1.72
Posterior probability: 1.72 / (1 + 1.72) = 0.63

Updated belief: 63% confidence feature will succeed
(up from 30% prior)
```

### Step 4: Iterate as More Evidence Arrives
Yesterday's posterior becomes today's prior:

```
New evidence: Week 2 shows lift holding at 4.5%
Prior (from step 3): 0.63
[Repeat update process]
New posterior: 0.78
```

## Common Applications

### Interpreting Test Results
```
Scenario: Test for rare disease (1 in 10,000 prevalence)
Test: 99% sensitive, 99% specific

Prior: P(disease) = 0.0001
If positive test:
  P(positive|disease) = 0.99
  P(positive|no disease) = 0.01
  P(positive) = 0.99 × 0.0001 + 0.01 × 0.9999 ≈ 0.0101

Posterior: P(disease|positive) = (0.99 × 0.0001) / 0.0101 ≈ 0.0098

Even with 99% accurate test, positive result only means ~1% chance of disease!
Base rate dominates when condition is rare.
```

### Debugging
```
Bug report: Users see error X
Prior beliefs:
  P(database issue) = 0.20
  P(network issue) = 0.30
  P(code bug) = 0.40
  P(user error) = 0.10

Evidence: Error happens only on mobile
  P(mobile-only | database) = 0.05
  P(mobile-only | network) = 0.30
  P(mobile-only | code bug) = 0.60
  P(mobile-only | user error) = 0.40

Update: Code bug becomes most likely (posterior ~0.55)
Next step: Investigate mobile-specific code paths
```

### Project Estimation
```
Prior: Based on similar projects, P(on-time) = 0.40

Evidence 1: Team is experienced with this stack
  Likelihood ratio: 1.5x → Posterior: 0.50

Evidence 2: Requirements are unclear
  Likelihood ratio: 0.6x → Posterior: 0.38

Evidence 3: Critical dependency has risk
  Likelihood ratio: 0.7x → Posterior: 0.30

Final estimate: 30% chance of on-time delivery
```

## Mental Shortcuts

### Strong vs Weak Evidence
| Evidence Type | Typical Likelihood Ratio |
|---------------|-------------------------|
| Definitive proof | 100x+ |
| Strong evidence | 10-100x |
| Moderate evidence | 3-10x |
| Weak evidence | 1.5-3x |
| Noise | ~1x (no update) |

### When to Update Significantly
Update strongly when:
- Evidence is surprising under your current belief
- Evidence comes from reliable source
- Evidence is specific to your hypothesis

Update weakly when:
- Evidence is expected regardless of hypothesis
- Source has unknown reliability
- Evidence is circumstantial

### Base Rate Neglect (Avoid This)
Common error: Ignoring prior probability when evidence arrives
```
Wrong: "Positive test = probably have disease"
Right: "Positive test shifts probability, but base rate matters"
```

## Calibration Check

### Are You Well-Calibrated?
Track predictions and outcomes:
- Of things you said were "70% likely," did ~70% happen?
- If you're always overconfident, widen your uncertainty
- If you're always underconfident, trust your assessments more

### Confidence Levels
| Stated Confidence | Should Mean |
|-------------------|-------------|
| 50% | Coin flip |
| 70% | Would bet 2:1 |
| 90% | Would bet 9:1 |
| 99% | Would bet 99:1 |

## Verification Checklist
- [ ] Established explicit prior probability (not just "I think...")
- [ ] Assessed likelihood ratio of evidence
- [ ] Applied update mathematically (not just "more/less likely")
- [ ] Considered base rates for rare events
- [ ] Checked for base rate neglect
- [ ] Documented reasoning for future calibration

## Key Questions
- "What was my belief before this evidence?"
- "How likely is this evidence if my belief is true? If false?"
- "What's the likelihood ratio?"
- "Am I anchoring on the evidence and ignoring base rates?"
- "How would I bet on this? At what odds?"

## Kahneman's Warning
"People tend to assess the relative importance of issues by the ease with which they are retrieved from memory—and this is largely determined by the extent of coverage in the media."

Don't let vivid evidence override base rates. A plane crash doesn't make flying more dangerous than driving, even though it feels that way.
