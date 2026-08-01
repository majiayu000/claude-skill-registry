---
name: statistical-analysis-drshailesh88-integrated-conten
description: Rigorous statistical analysis guidance for interpreting and reporting
  research findings in cardiology content.
---

# Statistical Analysis

Rigorous statistical analysis guidance for interpreting and reporting research findings in cardiology content.

## Triggers

- User needs to interpret trial statistics
- User is reporting study results
- User asks about statistical significance vs clinical significance
- User needs help with effect sizes, confidence intervals, or p-values
- User is evaluating the strength of evidence

## Core Concepts

### Test Selection Decision Tree

**Comparing Two Groups**:
- Continuous outcome, normal: Independent t-test
- Continuous outcome, non-normal: Mann-Whitney U
- Categorical outcome: Chi-square or Fisher's exact

**Comparing 3+ Groups**:
- Continuous, normal: ANOVA with post-hoc
- Continuous, non-normal: Kruskal-Wallis
- Categorical: Chi-square

**Relationships**:
- Two continuous: Pearson (normal) or Spearman (non-normal)
- Predict continuous: Linear regression
- Predict binary: Logistic regression
- Time-to-event: Cox proportional hazards

### Effect Sizes (Always Report!)

| Measure | Use Case | Interpretation |
|---------|----------|----------------|
| Cohen's d | Mean differences | 0.2 small, 0.5 medium, 0.8 large |
| Hazard Ratio | Survival analysis | <1 protective, >1 harmful |
| Odds Ratio | Case-control | ~RR when outcome rare |
| Risk Ratio | Cohort studies | Direct probability comparison |
| NNT/NNH | Clinical utility | Number needed to treat/harm |
| Absolute Risk Reduction | Clinical impact | ARR = Control rate - Treatment rate |

### Confidence Intervals

**Critical**: Always report 95% CIs alongside point estimates.

- CI crossing 1.0 (for ratios) = not statistically significant
- CI width indicates precision
- Narrow CI = more precise estimate
- Wide CI = less precise, often underpowered

### P-values: What They Are and Aren't

**P-value IS**: Probability of observing data this extreme if null hypothesis true

**P-value IS NOT**:
- Probability hypothesis is true/false
- Measure of effect size
- Indicator of clinical importance

**Reporting**: p < 0.05 is arbitrary; report exact values (p = 0.03, not p < 0.05)

## Clinical Trial Statistics

### Key Metrics for Cardiology Trials

| Metric | Formula | Use |
|--------|---------|-----|
| ARR | Control - Treatment event rate | Absolute benefit |
| RRR | (Control - Treatment) / Control | Relative benefit |
| NNT | 1 / ARR | Number to treat for one benefit |
| HR | Hazard in treatment / Hazard in control | Time-to-event |

### Example Interpretation

> "DAPA-HF showed empagliflozin reduced the composite endpoint (HR 0.74, 95% CI 0.65-0.85, p<0.001). The ARR was 4.9%, yielding an NNT of 21 over 18 months."

This tells us:
- 26% relative risk reduction (1 - 0.74)
- Statistically significant (CI doesn't cross 1.0)
- Need to treat 21 patients to prevent one event
- Clinically meaningful benefit

## Common Errors to Avoid

### P-hacking Red Flags
- Multiple testing without correction
- Selective outcome reporting
- Subgroup fishing
- Stopping trials early for "significance"

### Interpretation Errors
- Confusing statistical and clinical significance
- Ignoring confidence interval width
- Treating absence of evidence as evidence of absence
- Comparing p-values across studies

### Reporting Errors
- Reporting only p-values without effect sizes
- Omitting confidence intervals
- Not specifying statistical tests used
- Rounding inappropriately (keep 2 decimal places for ratios)

## APA-Style Statistical Reporting

```
# t-test
t(48) = 2.31, p = .025, d = 0.67, 95% CI [0.12, 1.22]

# ANOVA
F(2, 87) = 4.56, p = .013, η² = .095

# Correlation
r(58) = .42, p = .001, 95% CI [.18, .62]

# Chi-square
χ²(2, N = 120) = 8.45, p = .015, φ = .27

# Regression
β = 0.34, SE = 0.08, t = 4.25, p < .001

# Hazard ratio
HR = 0.74, 95% CI [0.65, 0.85], p < .001
```

## Power Analysis Guidance

Before interpreting underpowered studies:
- Sample size adequate for expected effect?
- Was power analysis pre-specified?
- What effect size was study powered to detect?

A non-significant result in an underpowered study ≠ no effect

## Checklist for Statistical Reporting

- [ ] Effect size with confidence interval
- [ ] Exact p-value (not just < or > threshold)
- [ ] Statistical test specified
- [ ] Assumptions verified
- [ ] Multiple comparison correction if needed
- [ ] Clinical significance discussed
- [ ] Limitations of analysis noted
