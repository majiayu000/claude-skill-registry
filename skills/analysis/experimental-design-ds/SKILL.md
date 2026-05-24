---
name: experimental-design-ds
description: A/B testing, randomization, sample size calculation, confounding control, and causal inference for data science. Covers the full experimental lifecycle from hypothesis formulation through power analysis, randomization strategies, blocking, factorial designs, sequential testing, and the potential outcomes framework for causal claims. Use when designing experiments, planning A/B tests, calculating sample sizes, or reasoning about causation from data.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/experimental-design-ds/SKILL.md
superseded_by: null
---
# Experimental Design for Data Science

Experimental design is the discipline of collecting data so that the analysis can answer the intended question. Ronald Fisher, working at the Rothamsted agricultural station in the 1920s, formalized the three pillars -- randomization, replication, and blocking -- that remain the foundation of every modern experiment, from clinical trials to A/B tests on websites. This skill covers experimental design from the data scientist's perspective: planning experiments, ensuring valid causal inference, and avoiding the pitfalls that invalidate conclusions.

**Agent affinity:** fisher (experimental design, ANOVA), tukey (exploratory analysis of experimental results), benjamin (ethical review of experiments)

**Concept IDs:** data-hypothesis-testing, data-confidence-intervals, data-probability-basics, data-sampling-methods

## Fisher's Three Pillars

### 1. Randomization

Random assignment of experimental units to treatment groups ensures that any observed difference is either due to the treatment or due to chance -- not due to confounders. Without randomization, the groups may differ systematically in ways that bias the result.

**Mechanism:** Each unit is assigned to treatment or control by a random process (coin flip, random number generator). This does not guarantee balance -- it guarantees that imbalances are random and quantifiable by probability theory.

**Why it works:** Randomization breaks the association between treatment assignment and all potential confounders, both observed and unobserved. No observational adjustment method can do this for unobserved confounders.

### 2. Replication

Multiple experimental units per group. Replication serves two purposes:

- **Statistical power:** More units means smaller standard errors and greater ability to detect real effects.
- **Generalizability:** Results from one unit might be idiosyncratic. Results replicated across many units are more convincing.

**Replication is not repetition.** Measuring the same unit 10 times is repetition (estimates measurement error). Measuring 10 different units is replication (estimates treatment effect variability).

### 3. Blocking

Grouping experimental units by a known source of variability and randomizing within blocks. If you know that males and females respond differently to a treatment, block by sex and randomize within each block. This reduces unexplained variance and increases power.

**Blocking vs. stratification:** Same concept, different fields. Blocking is the experimental design term (Fisher); stratification is the sampling term.

## The Experimental Lifecycle

| Stage | Goal | Key decisions |
|---|---|---|
| 1. Hypothesis | Define what you want to learn | Primary hypothesis, secondary hypotheses, directional vs. two-sided |
| 2. Metric selection | Define how you will measure the effect | Primary metric, guardrail metrics, sensitivity metrics |
| 3. Power analysis | Determine required sample size | Minimum detectable effect, significance level, power |
| 4. Design | Choose experimental structure | Completely randomized, blocked, factorial, sequential |
| 5. Randomization | Assign units to groups | Simple, stratified, cluster randomization |
| 6. Execution | Run the experiment | Monitor for implementation errors, compliance |
| 7. Analysis | Test the hypothesis | Pre-specified analysis plan, intention-to-treat |
| 8. Interpretation | Draw conclusions | Effect size, confidence interval, practical significance |

## A/B Testing

### The Basic Framework

An A/B test is the simplest randomized experiment: two groups (A = control, B = treatment), one intervention, one primary metric.

**Steps:**

1. Define the metric (conversion rate, revenue per user, time on page).
2. Define the minimum detectable effect (MDE) -- the smallest change worth detecting.
3. Calculate sample size using power analysis.
4. Randomize users into A and B.
5. Run until the pre-specified sample size is reached.
6. Analyze using the pre-specified test (t-test, chi-squared, Mann-Whitney).
7. Report the effect size with a confidence interval.

### Sample Size Calculation

For a two-sample test of proportions (e.g., conversion rates):

n = (Z_{alpha/2} + Z_beta)^2 * (p_1 * (1 - p_1) + p_2 * (1 - p_2)) / (p_1 - p_2)^2

Where:
- Z_{alpha/2} = critical value for significance level (1.96 for alpha = 0.05, two-sided)
- Z_beta = critical value for power (0.84 for power = 0.80)
- p_1 = baseline conversion rate
- p_2 = expected conversion rate under treatment

**Key insight:** Sample size scales with the inverse square of the effect size. Detecting a 1% improvement requires 4x the sample size of detecting a 2% improvement. This is why small effects in large populations require enormous experiments.

### Common A/B Testing Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| **Peeking** | Checking results before full sample size; inflates false positive rate | Use sequential testing methods or commit to fixed horizon |
| **Multiple comparisons** | Testing many metrics inflates family-wise error | Bonferroni correction, FDR control, or pre-specify one primary metric |
| **Network effects** | One user's treatment affects another user's outcome (social platforms) | Cluster randomization (randomize by geographic region or social cluster) |
| **Novelty/primacy effects** | Users react differently to new features initially | Run experiments long enough for the effect to stabilize (2-4 weeks) |
| **Sample ratio mismatch** | Unequal assignment ratios indicate implementation bugs | Check actual vs. expected ratio before analyzing results |
| **Simpson's paradox** | Aggregate result reverses when stratified by a confounder | Pre-stratify or check for compositional changes across groups |

## Randomization Strategies

| Strategy | Description | Use when |
|---|---|---|
| **Simple** | Coin flip per unit | Default; works for large samples |
| **Stratified** | Randomize within strata of important covariates | Known prognostic factors (age, gender, etc.) |
| **Cluster** | Randomize groups (classrooms, hospitals, regions) | Treatment applies at group level or interference between individuals |
| **Adaptive** | Adjust allocation probabilities based on interim results | Clinical trials with ethical constraints (avoid allocating to inferior arm) |
| **Switchback** | Same unit alternates between treatment and control over time | Marketplace experiments where user-level randomization causes interference |

## Factorial Designs

### Full Factorial

Test all combinations of multiple factors simultaneously. A 2x2 factorial with factors A and B has four groups: (control, control), (A, control), (control, B), (A, B).

**Advantages:**
- Tests each factor with the full sample (not half).
- Tests interactions: does the effect of A depend on B?
- More efficient than running separate experiments for each factor.

**Disadvantage:** Number of groups grows exponentially with factors. 5 factors with 2 levels each = 32 groups.

### Fractional Factorial

When full factorial is too expensive, run a carefully chosen subset of combinations. Aliasing (confounding) of high-order interactions is the trade-off. Use when interactions are expected to be small relative to main effects.

## Causal Inference

### The Fundamental Problem

We want to know the causal effect of treatment on an individual: Y(treatment) - Y(control). But we can only observe one of these -- the counterfactual is always missing. This is the fundamental problem of causal inference (Holland, 1986).

### Potential Outcomes Framework

For each unit i, define:
- Y_i(1) = outcome if treated
- Y_i(0) = outcome if not treated
- Individual causal effect = Y_i(1) - Y_i(0) (unobservable for any single unit)
- Average Treatment Effect (ATE) = E[Y(1) - Y(0)] (estimable with randomization)

Randomization makes the treatment assignment independent of potential outcomes, so:
ATE = E[Y | treated] - E[Y | control]

This is why randomization enables causal claims and observation alone does not.

### Observational Causal Methods

When experiments are impossible, these methods attempt causal inference from observational data. All require untestable assumptions:

| Method | Assumption | Use when |
|---|---|---|
| **Regression adjustment** | All confounders are measured and included | Known, measurable confounders |
| **Propensity score matching** | Treatment assignment is ignorable given observed covariates | Observational data with rich covariate information |
| **Instrumental variables** | An instrument affects treatment but not outcome directly | Natural experiments (lottery assignment, geographic boundaries) |
| **Difference-in-differences** | Parallel trends in absence of treatment | Policy changes affecting one group but not another |
| **Regression discontinuity** | Treatment assigned by a threshold on a continuous variable | Program eligibility cutoffs (test scores, age) |

**Critical caution:** Observational causal methods are approximations. They can reduce confounding but cannot eliminate it. Always prefer a randomized experiment when feasible and ethical.

## Confounding

A confounder is a variable that influences both the treatment assignment and the outcome, creating a spurious association:

- **Example:** Ice cream sales and drowning deaths are correlated because both are caused by hot weather (the confounder).
- **In experiments:** Randomization eliminates confounding by design.
- **In observational studies:** Must identify and adjust for confounders. Missing a confounder biases the estimated effect.

### Directed Acyclic Graphs (DAGs)

DAGs are the modern tool for reasoning about confounding, mediation, and collider bias:

- **Confounder:** X <- C -> Y. Adjust for C.
- **Mediator:** X -> M -> Y. Do NOT adjust for M if you want the total effect of X.
- **Collider:** X -> C <- Y. Do NOT adjust for C; adjusting opens a spurious path.

Draw the DAG before deciding what to control for. The adjustment set is determined by the causal structure, not by statistical significance.

## Sequential Testing

### The Problem with Peeking

Fixed-horizon tests (e.g., "run until n = 10,000") have a Type I error rate of alpha (e.g., 5%) when analyzed once at the end. Checking the results every day inflates the error rate dramatically -- 26% false positive rate with daily checks over 30 days at alpha = 0.05.

### Solutions

| Method | How it works | Trade-off |
|---|---|---|
| **Group sequential** (O'Brien-Fleming, Pocock) | Pre-specify interim analysis times with adjusted alpha spending | Slightly larger sample size; requires planning |
| **Always-valid p-values** | Construct p-values that are valid at any stopping time | More conservative; wider confidence intervals |
| **Bayesian sequential** | Update posterior continuously; stop when posterior probability exceeds threshold | Requires prior specification; more complex analysis |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| No pre-registration | Post-hoc hypothesis selection inflates false positives (p-hacking) | Write the analysis plan before seeing the data |
| Underpowered experiment | Cannot detect real effects; waste of resources | Power analysis before running |
| Confusing statistical and practical significance | p < 0.05 with a tiny effect size is not actionable | Report effect size and confidence interval alongside p-value |
| Treating observational data as experimental | Cannot make causal claims without randomization | Use causal inference methods and state assumptions |
| Stopping early because "it looks significant" | Inflated false positive rate | Use sequential testing methods |
| Ignoring multiple comparisons | Testing 20 metrics at alpha = 0.05 expects 1 false positive | Bonferroni, Holm, or Benjamini-Hochberg correction |

## Cross-References

- **fisher agent:** Experimental design specialist. Primary agent for power analysis, randomization plans, and ANOVA.
- **tukey agent:** Exploratory analysis of experimental results -- residual analysis, effect visualization, outlier investigation.
- **benjamin agent:** Ethical review of experimental designs -- informed consent, equity, stopping rules for harmful treatments.
- **statistical-modeling skill:** Regression and ANOVA methods used to analyze experimental data.
- **ethics-governance skill:** Ethical frameworks for human subjects research, consent, and algorithmic experimentation.
- **machine-learning-foundations skill:** Cross-validation as the ML analog of experimental replication.

## References

- Fisher, R. A. (1935). *The Design of Experiments*. Oliver and Boyd.
- Rubin, D. B. (1974). "Estimating Causal Effects of Treatments in Randomized and Nonrandomized Studies." *Journal of Educational Psychology*, 66(5), 688-701.
- Holland, P. W. (1986). "Statistics and Causal Inference." *Journal of the American Statistical Association*, 81(396), 945-960.
- Imbens, G. W. & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.
- Kohavi, R., Tang, D., & Xu, Y. (2020). *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing*. Cambridge University Press.
- Pearl, J. (2009). *Causality*. 2nd edition. Cambridge University Press.
