---
name: ab-testing
description: "Design and analyze A/B tests and controlled experiments for data-driven decisions. Use for: experiment design, hypothesis formulation, sample size calculation, statistical significance testing, multivariate testing, test implementation, results analysis, avoiding common pitfalls, sequential testing, and experimentation platforms."
---

# A/B Testing

Design and analyze controlled experiments to make data-driven decisions about product changes and optimizations.

## Overview

A/B testing (split testing) is a rigorous method for comparing two or more variants to determine which performs better on a defined metric. This skill covers statistical foundations, experimental design principles, implementation strategies, and analysis techniques for running effective experiments.

## A/B Testing Fundamentals

### Core Concepts

**Control (A)**: Current version or baseline
**Variant (B)**: New version being tested
**Randomization**: Users randomly assigned to control or variant
**Metric**: Quantifiable measure of success (conversion rate, revenue, engagement)
**Statistical Significance**: Confidence that difference is not due to chance

### When to Use A/B Testing

**Good Use Cases**:
- Testing website/app design changes
- Optimizing email subject lines or content
- Comparing pricing strategies
- Evaluating feature changes
- Testing marketing messages

**Not Suitable For**:
- Low-traffic pages (insufficient sample size)
- Long-term strategic decisions
- Understanding "why" (use qualitative research)
- Testing many changes simultaneously (use multivariate testing)

## Experimental Design

### Hypothesis Formulation

**Good Hypothesis**:
- Specific: "Changing button color from blue to green will increase click-through rate"
- Measurable: Clear metric (CTR)
- Relevant: Tied to business goal
- Falsifiable: Can be proven wrong

**Bad Hypothesis**:
- Vague: "New design will be better"
- Unmeasurable: "Users will like it more"
- Multiple changes: "New layout, colors, and copy will improve conversions"

### Sample Size Calculation

**Required Inputs**:
- **Baseline Conversion Rate**: Current metric value
- **Minimum Detectable Effect (MDE)**: Smallest change worth detecting
- **Statistical Significance (α)**: Typically 0.05 (95% confidence)
- **Statistical Power (1-β)**: Typically 0.80 (80% power)

**Formula** (simplified for proportions):
```
n = 16 * σ² / (MDE)²

Where:
σ² = p(1-p) for proportions
p = baseline conversion rate
MDE = minimum detectable effect
```

**Example**:
- Baseline: 10% conversion rate
- MDE: 2% (relative 20% improvement)
- Significance: 0.05
- Power: 0.80
- Required sample size: ~3,900 per variant

### Test Duration

**Factors**:
- Traffic volume
- Required sample size
- Day-of-week effects (run full weeks)
- Seasonality
- Minimum: 1-2 weeks recommended

**Avoid**:
- Stopping test early when results look good (peeking problem)
- Running too long (external factors may interfere)

## Statistical Analysis

### Hypothesis Testing

**Null Hypothesis (H₀)**: No difference between variants
**Alternative Hypothesis (H₁)**: Difference exists between variants

**P-Value**: Probability of observing results if null hypothesis is true
- p < 0.05: Reject null, difference is statistically significant
- p ≥ 0.05: Fail to reject null, no significant difference

### Confidence Intervals

**95% Confidence Interval**: Range where true value likely falls
- If intervals don't overlap, difference is likely significant
- Provides effect size estimate, not just yes/no

**Example**:
- Control CTR: 10% (95% CI: 9.5% - 10.5%)
- Variant CTR: 12% (95% CI: 11.4% - 12.6%)
- Conclusion: Significant improvement

### Statistical Tests

**Two-Sample Z-Test** (proportions):
```python
from statsmodels.stats.proportion import proportions_ztest

# Control: 1000 conversions out of 10000 visitors
# Variant: 1200 conversions out of 10000 visitors
count = [1000, 1200]
nobs = [10000, 10000]

z_stat, p_value = proportions_ztest(count, nobs)
print(f"P-value: {p_value}")
```

**T-Test** (continuous metrics like revenue):
```python
from scipy.stats import ttest_ind

control_revenue = [10, 15, 20, ...]  # Revenue per user
variant_revenue = [12, 18, 22, ...]

t_stat, p_value = ttest_ind(control_revenue, variant_revenue)
print(f"P-value: {p_value}")
```

**Chi-Square Test** (categorical outcomes):
```python
from scipy.stats import chi2_contingency

# Observed frequencies
observed = [[900, 9100],   # Control: 900 conversions, 9100 non-conversions
            [1100, 8900]]  # Variant: 1100 conversions, 8900 non-conversions

chi2, p_value, dof, expected = chi2_contingency(observed)
print(f"P-value: {p_value}")
```

## Common Pitfalls and Solutions

### Multiple Comparisons Problem

**Problem**: Testing multiple variants increases false positive rate
**Solution**: Bonferroni correction (divide α by number of comparisons)
- Testing 3 variants: Use α = 0.05/3 = 0.0167

### Peeking Problem

**Problem**: Checking results repeatedly and stopping when significant
**Solution**:
- Pre-determine sample size and duration
- Use sequential testing methods (e.g., always-valid p-values)
- Implement stopping rules

### Novelty Effect

**Problem**: Users react to change itself, not the actual improvement
**Solution**:
- Run test longer (2-4 weeks)
- Analyze new vs returning users separately
- Look for sustained effect over time

### Selection Bias

**Problem**: Non-random assignment or different user populations
**Solution**:
- Ensure proper randomization
- Check for balance in user characteristics
- Use stratified randomization if needed

### Insufficient Sample Size

**Problem**: Test ends before reaching statistical power
**Solution**:
- Calculate required sample size before starting
- Wait for sufficient data
- Consider increasing traffic or MDE

## Advanced Techniques

### Multivariate Testing (MVT)

Test multiple elements simultaneously:
- **Example**: Test 2 headlines × 2 images × 2 CTAs = 8 combinations
- **Pros**: Test interactions between elements
- **Cons**: Requires much larger sample size

### Sequential Testing

Continuously monitor test with valid stopping rules:
- **Bayesian A/B Testing**: Update beliefs as data arrives
- **Always-Valid P-Values**: Allow peeking without inflation
- **Multi-Armed Bandits**: Dynamically allocate traffic to better variant

### Stratified Sampling

Ensure balance across important segments:
- Randomize within strata (e.g., mobile vs desktop)
- Improves precision and power
- Reduces variance

### CUPED (Controlled-Experiment Using Pre-Experiment Data)

Use pre-experiment data to reduce variance:
- Measure metric before experiment
- Adjust post-experiment metric for pre-experiment value
- Reduces required sample size by 30-50%

## Implementation

### Randomization

**User-Level**: Consistent experience for each user
**Session-Level**: Different experience each session
**Page-Level**: Different experience each page view

**Hash-Based Assignment**:
```python
import hashlib

def assign_variant(user_id, experiment_id, num_variants=2):
    hash_input = f"{user_id}_{experiment_id}"
    hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
    return hash_value % num_variants
```

### Tracking

**Events to Track**:
- Exposure: User saw variant
- Conversion: User completed goal action
- Metadata: Timestamp, user properties, context

**Example Schema**:
```json
{
  "user_id": "12345",
  "experiment_id": "homepage_redesign",
  "variant": "B",
  "timestamp": "2026-03-15T10:30:00Z",
  "converted": true,
  "revenue": 49.99
}
```

### Platforms

**Open Source**:
- GrowthBook: Feature flagging and experimentation
- Unleash: Feature toggle system
- Statsig: Experimentation platform

**Commercial**:
- Optimizely: Enterprise A/B testing
- VWO: Conversion optimization platform
- Google Optimize: Free A/B testing (integrated with Analytics)
- Adobe Target: Personalization and testing

## Analysis and Reporting

### Metrics to Report

**Primary Metric**: Main success criterion
**Secondary Metrics**: Supporting metrics
**Guardrail Metrics**: Ensure no negative impact (page load time, error rate)

**Example Report**:
```
Experiment: Homepage CTA Button Color
Duration: March 1-14, 2026 (2 weeks)
Sample Size: 50,000 per variant

Primary Metric: Click-Through Rate
- Control (Blue): 10.2% (95% CI: 9.9% - 10.5%)
- Variant (Green): 11.8% (95% CI: 11.5% - 12.1%)
- Lift: +15.7% (p < 0.001)

Secondary Metrics:
- Conversion Rate: +8.3% (p = 0.02)
- Revenue per User: +5.2% (p = 0.15, not significant)

Guardrail Metrics:
- Page Load Time: No change (p = 0.82)
- Bounce Rate: No change (p = 0.45)

Recommendation: Ship variant (green button)
```

### Segmentation Analysis

Analyze results by segment:
- Device type (mobile, desktop, tablet)
- User type (new, returning)
- Geography
- Traffic source

**Simpson's Paradox**: Overall result may differ from segment results

## Best Practices

### Before Testing

- Define clear hypothesis and success metrics
- Calculate required sample size
- Set up proper tracking
- Document experiment design
- Get stakeholder alignment

### During Testing

- Don't peek at results (or use sequential methods)
- Monitor for technical issues
- Ensure balanced traffic allocation
- Run for predetermined duration

### After Testing

- Analyze primary and secondary metrics
- Check for segment differences
- Document learnings
- Communicate results clearly
- Implement winning variant or iterate

## Using the Reference Files

### When to Read Each Reference

**`/references/statistical-methods.md`** — Read when calculating sample sizes, choosing statistical tests, or understanding p-values and confidence intervals.

**`/references/experiment-design-patterns.md`** — Read when designing complex experiments, implementing multivariate tests, or using advanced techniques like CUPED.

**`/references/common-mistakes.md`** — Read when troubleshooting experiments, avoiding pitfalls, or understanding why results may be misleading.
