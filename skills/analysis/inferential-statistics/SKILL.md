---
name: inferential-statistics
description: Drawing conclusions about populations from sample data. Covers sampling distributions, confidence intervals, hypothesis testing (z-tests, t-tests, chi-squared tests, ANOVA), p-values, significance levels, power, Type I and Type II errors, effect sizes, and the logic connecting sample statistics to population parameters. Emphasizes the distinction between statistical significance and practical significance. Use when testing hypotheses, constructing confidence intervals, designing studies, or interpreting inferential results.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/inferential-statistics/SKILL.md
superseded_by: null
---
# Inferential Statistics

Inferential statistics is the bridge from sample to population. A researcher observes 200 patients and wants to draw conclusions about all patients. A factory tests 50 parts and wants to guarantee the quality of 10,000. The logical machinery that makes this possible -- sampling distributions, confidence intervals, hypothesis tests, and their attendant concepts of error and power -- forms the core of this skill.

**Agent affinity:** pearson (chi-squared, test design), gosset (t-tests, small-sample inference), wasserstein (p-value interpretation, communication), george (pedagogy)

**Concept IDs:** stat-hypothesis-testing, stat-sampling-bias, stat-descriptive-statistics

## The Logic of Inference

### From sample to population

A **parameter** is a fixed but unknown number describing a population (mu, sigma, p). A **statistic** is a number computed from sample data (x-bar, s, p-hat) that estimates the parameter.

The key question: how much can a statistic vary from sample to sample? The **sampling distribution** of a statistic describes this variability. The standard deviation of a sampling distribution is called the **standard error (SE)**.

### The sampling distribution of the mean

If samples of size n are drawn from a population with mean mu and SD sigma:
- E(X-bar) = mu (unbiased).
- SE(X-bar) = sigma / sqrt(n).
- By the CLT, X-bar is approximately normal for large n.

This is the foundation of virtually every test and interval for means.

## Confidence Intervals

### Construction

A confidence interval for a parameter has the form: point estimate +/- margin of error.

For a population mean with known sigma: X-bar +/- z* (sigma / sqrt(n)), where z* is the critical value from the standard normal distribution.

For a population mean with unknown sigma: X-bar +/- t* (s / sqrt(n)), where t* comes from the t-distribution with n-1 degrees of freedom.

### Interpretation

A 95% confidence interval means: if we repeated this sampling procedure many times, about 95% of the resulting intervals would contain the true parameter. It does NOT mean "there is a 95% probability that the parameter is in this interval." The parameter is fixed; the interval is random.

### Common confidence intervals

| Parameter | Conditions | Formula |
|---|---|---|
| Mean (sigma known) | n >= 30 or normal population | X-bar +/- z*(sigma/sqrt(n)) |
| Mean (sigma unknown) | n >= 30 or normal population | X-bar +/- t*(s/sqrt(n)) |
| Proportion | np-hat >= 10 and n(1-p-hat) >= 10 | p-hat +/- z*sqrt(p-hat(1-p-hat)/n) |
| Difference of means | Independent samples | (X-bar1 - X-bar2) +/- t*SE |
| Difference of proportions | Large samples | (p-hat1 - p-hat2) +/- z*SE |

### Width and precision

The margin of error shrinks with:
- Larger sample size (n in the denominator).
- Lower confidence level (smaller z* or t*).
- Lower population variability (smaller sigma or s).

Doubling precision requires quadrupling the sample size (because of the sqrt(n)).

## Hypothesis Testing

### The framework

1. **State hypotheses.** H_0 (null hypothesis): the default claim, typically "no effect" or "no difference." H_a (alternative): what we seek evidence for.
2. **Choose alpha.** The significance level (typically 0.05). This is the maximum acceptable probability of rejecting H_0 when it is true.
3. **Compute the test statistic.** A standardized measure of how far the sample result is from H_0's claim.
4. **Find the p-value.** The probability of observing a test statistic as extreme as (or more extreme than) the one computed, assuming H_0 is true.
5. **Decide.** If p-value <= alpha, reject H_0. Otherwise, fail to reject H_0.

### Common tests

| Test | Hypotheses about | Test statistic | Distribution | Use when |
|---|---|---|---|---|
| One-sample z-test | Population mean (sigma known) | z = (X-bar - mu_0)/(sigma/sqrt(n)) | N(0,1) | Large n, sigma known |
| One-sample t-test | Population mean (sigma unknown) | t = (X-bar - mu_0)/(s/sqrt(n)) | t(n-1) | Small n, sigma unknown |
| Two-sample t-test | Difference of means | t = (X-bar1 - X-bar2)/SE | t(df) | Comparing two independent groups |
| Paired t-test | Mean difference | t = d-bar/(s_d/sqrt(n)) | t(n-1) | Paired/matched data |
| One-proportion z-test | Population proportion | z = (p-hat - p_0)/sqrt(p_0(1-p_0)/n) | N(0,1) | Testing a claimed proportion |
| Chi-squared goodness-of-fit | Distribution shape | chi^2 = sum((O-E)^2/E) | chi^2(k-1) | Observed vs. expected frequencies |
| Chi-squared independence | Association of two categorical variables | chi^2 = sum((O-E)^2/E) | chi^2((r-1)(c-1)) | Contingency tables |
| One-way ANOVA | Equality of k means | F = MS_between/MS_within | F(k-1, N-k) | Comparing 3+ group means |

### P-Values

The p-value is the probability, under H_0, of observing data as extreme as or more extreme than what was actually observed.

**What the p-value is:** A measure of the compatibility of the data with H_0.

**What the p-value is NOT:**
- Not the probability that H_0 is true.
- Not the probability that the result is due to chance.
- Not a measure of effect size.
- Not a measure of practical importance.

**The ASA statement on p-values (Wasserstein & Lazar, 2016):** "Informally, a p-value is the probability under a specified statistical model that a statistical summary of the data would be equal to or more extreme than its observed value." The ASA emphasized six principles, including that p-values do not measure the probability that the studied hypothesis is true and that scientific conclusions should not be based only on whether a p-value passes a specific threshold.

## Errors and Power

### Type I and Type II errors

| | H_0 true | H_0 false |
|---|---|---|
| **Reject H_0** | Type I error (alpha) | Correct (Power = 1 - beta) |
| **Fail to reject H_0** | Correct | Type II error (beta) |

- **Type I error (alpha):** Rejecting H_0 when it is true. The significance level controls this.
- **Type II error (beta):** Failing to reject H_0 when it is false. Harder to control.
- **Power (1 - beta):** The probability of correctly rejecting a false H_0.

### What affects power

Power increases with:
- Larger sample size (more information).
- Larger effect size (bigger signal).
- Higher alpha (more willingness to reject -- but more Type I errors).
- Lower variability in the population.
- One-tailed vs. two-tailed test (directionality focuses the rejection region).

**Standard target:** Power >= 0.80 (80%). A study with low power risks "detecting nothing" even when a real effect exists.

## Effect Size and Practical Significance

### Statistical vs. practical significance

A tiny effect can be statistically significant with a large enough sample. A large effect can be statistically non-significant with a small sample. Statistical significance (small p) and practical significance (large enough effect to matter) are independent concepts.

### Common effect size measures

| Measure | Formula | Interpretation |
|---|---|---|
| Cohen's d | (X-bar1 - X-bar2) / s_pooled | Small: 0.2, Medium: 0.5, Large: 0.8 |
| Pearson's r | Correlation coefficient | Small: 0.1, Medium: 0.3, Large: 0.5 |
| Cohen's f | sqrt(eta^2 / (1 - eta^2)) for ANOVA | Small: 0.1, Medium: 0.25, Large: 0.4 |
| Odds ratio | (a/b) / (c/d) in 2x2 table | 1 = no effect; farther from 1 = larger effect |

**Always report effect sizes alongside p-values.** A result that is both statistically significant and practically meaningful is the gold standard.

## ANOVA

### One-way ANOVA

Tests whether three or more group means are all equal.

- **H_0:** mu_1 = mu_2 = ... = mu_k.
- **H_a:** At least one mean differs.
- **Test statistic:** F = MS_between / MS_within.
- **If F is large (p < alpha):** At least one group differs, but ANOVA does not say which. Use post-hoc tests (Tukey HSD, Bonferroni) for pairwise comparisons.

### Assumptions

1. Independence of observations.
2. Normality within each group (or large enough n per group).
3. Equal variances across groups (Levene's test to check; Welch's ANOVA if violated).

## Multiple Comparisons

Testing many hypotheses inflates the familywise error rate. With m independent tests at alpha = 0.05, the probability of at least one Type I error is 1 - (0.95)^m.

### Corrections

- **Bonferroni:** Test each at alpha/m. Conservative but simple.
- **Holm-Bonferroni:** Step-down procedure. Less conservative than Bonferroni.
- **Tukey HSD:** Designed for all pairwise comparisons after ANOVA.
- **False Discovery Rate (BH procedure):** Controls the expected proportion of false discoveries. More powerful than familywise corrections for large m.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| "Fail to reject" interpreted as "H_0 is true" | Absence of evidence is not evidence of absence | Say "insufficient evidence to conclude H_a" |
| Ignoring assumptions | Tests are invalid when assumptions are violated | Check assumptions; use robust alternatives |
| Reporting only p-values | P-values without context are uninformative | Report effect sizes, confidence intervals, and sample sizes |
| Data dredging / p-hacking | Testing many hypotheses and reporting only significant ones | Pre-register hypotheses; correct for multiple comparisons |
| Confusing one-tailed and two-tailed | One-tailed tests have more power but assume direction | Use two-tailed unless the direction is specified before data collection |

## Cross-References

- **pearson agent:** Chi-squared tests, ANOVA design, test selection.
- **gosset agent:** t-tests, small-sample inference, paired designs.
- **wasserstein agent:** P-value interpretation, moving beyond significance thresholds.
- **box agent:** Model diagnostics, assumption checking.
- **probability-theory skill:** Theoretical foundation (sampling distributions, CLT).
- **bayesian-methods skill:** Alternative inferential framework that replaces p-values with posterior probabilities.

## References

- Wasserstein, R. L., & Lazar, N. A. (2016). "The ASA statement on p-values." *The American Statistician*, 70(2), 129-133.
- Wasserstein, R. L., Schirm, A. L., & Lazar, N. A. (2019). "Moving to a world beyond p < 0.05." *The American Statistician*, 73(sup1), 1-19.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences*. 2nd edition. Lawrence Erlbaum.
- Lehmann, E. L. (2005). *Testing Statistical Hypotheses*. 3rd edition. Springer.
- Moore, D. S., McCabe, G. P., & Craig, B. A. (2021). *Introduction to the Practice of Statistics*. 10th edition. W.H. Freeman.
