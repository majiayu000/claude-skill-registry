---
name: ice-score
description: "Use to prioritize solutions or opportunities using ICE scoring with evidence-backed confidence."
---

# ICE Score Skill

ICE scoring with integrated confidence meter.

## Workflow

ICE scoring is applied to **OST solution leaves**. Each leaf must have a Four Risks assessment (Torres Product Trio) before it can be scored — the risks are the inputs, ICE is the output.

### Step 1: Verify Four Risks exist

For each solution leaf in `canvas/opportunities.yml`, check that `four_risks` has been assessed:
- **Value** (product lens): Do users want/need this?
- **Usability** (design lens): Can users figure it out?
- **Feasibility** (engineering lens): Can we build it within constraints?
- **Viability** (cross-cutting): Does it align with business/legal/ethical constraints?

If any risk dimension is missing, assess it first. Each dimension must have its own evidence — a single combined statement fails (Torres Product Trio rule).

### Step 2: Derive ICE from the Four Risks

For each solution, score three dimensions (1-10):

**Impact** — derived from value + usability + viability risks:
- What does the value risk assessment say about user demand?
- What does the usability assessment say about adoption likelihood?
- What does the viability assessment say about business alignment?
- 1-3: Low value evidence, high usability risk, or poor viability fit
- 4-6: Moderate value evidence, some usability unknowns
- 7-10: Strong value evidence, low usability risk, clear viability

**Confidence** — how well-tested are the risk assessments (Gilad's meter)?
- 1-3: Risk assessments based on gut feel or desk research
- 4-6: Some direct evidence (interviews, analogues, small tests)
- 7-10: Strong evidence (user tests, prototypes, data). Requires test-validated evidence.

**Ease** — derived from feasibility risk:
- What does the engineering assessment say about complexity?
- What dependencies, unknowns, or technical spikes were identified?
- 1-3: High feasibility risk. Major unknowns, new capabilities needed.
- 4-6: Moderate feasibility risk. Known patterns, some complexity.
- 7-10: Low feasibility risk. Quick win, existing patterns.

### Step 3: Calculate and rank

ICE = Impact x Confidence x Ease. Rank solution leaves by ICE score.

### Step 4: Identify riskiest assumptions

For the top-ranked solutions, extract the **highest-risk assumptions** from the Four Risks assessment — these are what `/assumption-test` should target first. Prioritize assumptions where importance is high but evidence is low.

### Step 5: Bias check

Are high-scoring items benefiting from availability bias, IKEA effect, or anchoring? Review for bias after scoring, before acting.

### Output

```
| Solution | Value | Usability | Feasibility | Viability | I | C | E | ICE | Riskiest Assumption |
|----------|-------|-----------|-------------|-----------|---|---|---|-----|---------------------|
| ...      | risk  | risk      | risk        | risk      | X | X | X | XXX | [what to test]      |
```

## Rules
- Every ICE score must trace back to a Four Risks assessment — no scoring without risk evaluation first.
- Each risk dimension must have separate evidence (Product Trio rule).
- Confidence of 7+ requires test-validated evidence, not analogy or assumption.
- If all items score similarly, the risk assessments need more depth.
- Review for bias after scoring, before acting.

## Canvas Output
Update `canvas/opportunities.yml` — write `four_risks` and `ice_score` per solution leaf.
Update `canvas/gist.yml` with idea ICE scores and confidence levels.

## Theory Citations
- Ellis: ICE scoring (Impact × Confidence × Ease — Sean Ellis invented the ICE framework as part of growth methodology)
- Gilad: Evidence-Guided (Confidence Meter — the evidence-grading layer on top of Ellis's ICE, mapping evidence types to confidence levels)
- Torres: Continuous Discovery Habits (OST leaves as unit of evaluation)
- Torres: Product Trio (three perspectives feeding risk assessment)
- Cagan: Inspired (Four Risks as structured evaluation)
- Kahneman: Thinking, Fast and Slow (bias in estimation)
- Kahneman, Sibony & Sunstein: Noise (2021) — unwanted variability in judgment (see Noise Check below)

### Noise Check (Kahneman, Sibony & Sunstein, 2021)

ICE scores are susceptible to **noise** — unwanted variability where different sessions or assessors produce different scores for the same evidence. Unlike bias (systematic skew in one direction), noise is random scatter.

**Detection**: Re-score the same evidence independently (different session or assessor) and compare. If scores diverge by >1 point on any dimension, investigate why before proceeding.

**Mitigation**: Use structured assessment criteria (the Four Risks inputs above), apply scores independently before discussion, and anchor to evidence types rather than gut feel.
