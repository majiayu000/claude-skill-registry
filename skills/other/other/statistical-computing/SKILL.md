---
name: statistical-computing
description: Computational tools and algorithms for statistical analysis. Covers simulation, resampling methods (bootstrap, permutation tests), Monte Carlo methods, random number generation, numerical optimization (Newton-Raphson, EM algorithm), cross-validation, and reproducible analysis workflows. Emphasizes the bootstrap revolution and the shift from formula-based to computation-based inference. Use when implementing statistical procedures, running simulations, bootstrapping confidence intervals, performing cross-validation, or building reproducible analysis pipelines.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/statistical-computing/SKILL.md
superseded_by: null
---
# Statistical Computing

Statistical computing transformed the discipline. Before 1970, inference depended on mathematical formulas and tables. The bootstrap (Efron, 1979), permutation tests, and Monte Carlo methods showed that a computer could replace analytical derivations with brute-force resampling -- and often provide more accurate answers with fewer assumptions. This skill covers the computational toolkit that modern statistics depends on.

**Agent affinity:** efron (bootstrap, computational methods), box (simulation for model checking), george (simulation-based pedagogy)

**Concept IDs:** stat-probability-foundations, stat-hypothesis-testing, stat-descriptive-statistics

## The Bootstrap

### The idea

Given a sample of n observations, the bootstrap generates new "samples" by resampling with replacement from the original data. Each bootstrap sample has size n. The distribution of a statistic across many bootstrap samples approximates the sampling distribution of that statistic.

### Algorithm (nonparametric bootstrap)

1. Observe data x_1, x_2, ..., x_n.
2. For b = 1, 2, ..., B (typically B = 1000 to 10000):
   a. Draw a sample of size n with replacement from the original data.
   b. Compute the statistic of interest T_b (e.g., mean, median, regression coefficient).
3. The distribution of T_1, T_2, ..., T_B approximates the sampling distribution of T.

### Bootstrap confidence intervals

| Method | Construction | Properties |
|---|---|---|
| Percentile | [T_(alpha/2), T_(1-alpha/2)] from bootstrap distribution | Simple; can be biased for skewed distributions |
| Basic (reverse percentile) | [2T_obs - T_(1-alpha/2), 2T_obs - T_(alpha/2)] | Corrects for some bias |
| BCa (bias-corrected and accelerated) | Adjusts percentiles for bias and skewness | Gold standard; requires more computation |
| Studentized | Bootstrap the t-statistic, not the raw estimate | Best coverage properties; most complex |

**When to use the bootstrap:**
- When the sampling distribution of the statistic has no closed-form formula.
- When the sample size is too small for the CLT to apply.
- When you want to check whether a formula-based interval is trustworthy.
- For statistics that are not simple means (medians, ratios, trimmed means, correlation coefficients).

### When the bootstrap fails

- Very small samples (n < 10): not enough data to resample meaningfully.
- Extreme quantiles: the bootstrap cannot reliably estimate the tails of a distribution.
- Non-i.i.d. data: dependent data (time series, clustered data) require block bootstrap or other modifications.
- Infinite variance distributions: the bootstrap relies on finite variance for consistency.

## Permutation Tests

### The idea

To test whether two groups differ, randomly permute the group labels many times and compute the test statistic under each permutation. The proportion of permutations where the test statistic is as extreme as the observed one is the p-value.

### Algorithm

1. Observe test statistic T_obs from the original data.
2. For b = 1, 2, ..., B:
   a. Randomly permute the group labels.
   b. Compute T_b under the permuted labels.
3. p-value = (number of T_b >= T_obs) / B (for a one-tailed test).

### Advantages

- Exact test: the permutation distribution is the exact null distribution (no distributional assumptions).
- Valid for any test statistic, not just t or F.
- Works with small samples.
- Conceptually transparent: "if the groups really don't differ, shuffling labels shouldn't matter."

### Limitations

- Computationally expensive for large samples (but approximate permutation tests with B = 10000 are fast).
- Tests equality of distributions, not just means.
- Does not produce confidence intervals (but can be inverted to do so).

## Monte Carlo Simulation

### For probability estimation

When a probability is too complex to compute analytically, simulate the experiment many times and estimate the probability as the proportion of times the event occurs.

**Example:** Estimate P(at least two people in a group of 23 share a birthday).
1. Simulate 10000 groups of 23 random birthdays.
2. Count how many groups have at least one shared birthday.
3. Estimated probability = count / 10000.

### For statistical properties

Simulation is the standard way to study the properties of statistical procedures:

- **Bias:** Simulate data from a known model, apply the estimator, and compare the average estimate to the true parameter.
- **Coverage:** Generate confidence intervals from many simulated datasets and check what fraction contain the true parameter.
- **Power:** Simulate data under the alternative hypothesis and check what fraction of tests reject H_0.
- **Robustness:** Simulate data that violate assumptions and check how the procedure degrades.

### Random number generation

All simulation depends on pseudo-random number generators (PRNGs).

- **Uniform generation:** Mersenne Twister (MT19937) is the standard. Period of 2^19937 - 1.
- **From uniform to any distribution:** Inverse CDF method (F^(-1)(U)), acceptance-rejection, Box-Muller (for normals).
- **Seeds and reproducibility:** Always set the random seed before a simulation so results are reproducible.

## Cross-Validation

### The idea

To estimate how well a model generalizes to new data, partition the data into training and validation sets. Fit the model on training data, evaluate on validation data.

### Methods

| Method | Procedure | Properties |
|---|---|---|
| Holdout | Split data 70/30 or 80/20 | Simple but high variance; depends on the split |
| k-fold CV | Split into k equal parts; rotate which part is held out | Standard choice (k = 5 or 10); lower variance than holdout |
| Leave-one-out (LOOCV) | k = n; each observation is held out once | Unbiased but high variance; expensive |
| Repeated k-fold | Run k-fold CV multiple times with different splits | Lower variance than single k-fold |
| Stratified k-fold | Each fold preserves the class distribution | Essential for imbalanced classification |

### Bias-variance tradeoff in CV

- **Small k (e.g., k = 2):** High bias (training sets are small), low variance.
- **Large k (e.g., LOOCV):** Low bias (training sets are nearly full-sized), but high variance (folds are very similar).
- **k = 10:** Widely accepted as a good compromise.

## Numerical Optimization

### Maximum likelihood estimation

Most statistical models are fit by maximizing the log-likelihood:

theta-hat = argmax_theta log L(theta | data).

For simple models, this has a closed form. For complex models, numerical optimization is required.

### Newton-Raphson method

theta_{t+1} = theta_t - [H(theta_t)]^(-1) * g(theta_t)

where g is the gradient (score) and H is the Hessian (observed information matrix). Converges quadratically near the maximum.

### Fisher scoring

Replace the Hessian with the expected information matrix I(theta). More stable than Newton-Raphson when far from the maximum. This is the standard method for fitting generalized linear models.

### EM algorithm

For models with latent variables (mixture models, missing data):

1. **E-step:** Compute the expected value of the complete-data log-likelihood, given current parameter estimates and observed data.
2. **M-step:** Maximize that expected log-likelihood to get new parameter estimates.
3. Repeat until convergence.

The EM algorithm always increases the likelihood but can converge to local maxima. Run from multiple starting points.

## Reproducible Analysis

### Principles

1. **Script everything.** No point-and-click analyses. Every step from data loading to final figure should be in code.
2. **Set seeds.** Every simulation and resampling procedure should record its random seed.
3. **Version control.** Track analysis code in git.
4. **Document dependencies.** Record the versions of all packages used.
5. **Literate programming.** Use Jupyter notebooks, R Markdown, or Quarto to interleave code, output, and narrative.

### Common tools

| Tool | Language | Strengths |
|---|---|---|
| R + tidyverse | R | Statistical modeling, visualization (ggplot2), CRAN ecosystem |
| Python + scipy/statsmodels | Python | General-purpose, integration with ML (scikit-learn), Jupyter |
| Stan | Stan (called from R/Python) | Bayesian modeling, MCMC, Hamiltonian Monte Carlo |
| Julia | Julia | Speed for numerical work, growing statistics ecosystem |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Too few bootstrap replicates | Noisy confidence intervals | Use B >= 1000 for CIs; B >= 10000 for BCa |
| Not setting random seeds | Results are not reproducible | Set seed before every simulation |
| Using LOOCV when k-fold suffices | LOOCV has high variance and is expensive | Use 10-fold CV as default |
| Ignoring bootstrap failures | Small n, extreme quantiles, or dependence violate bootstrap assumptions | Check bootstrap conditions; use block bootstrap for dependent data |
| Fitting and evaluating on the same data | Overly optimistic performance estimates | Always use held-out data or cross-validation |

## Cross-References

- **efron agent:** Bootstrap methods, empirical Bayes, computational statistics philosophy.
- **box agent:** Simulation for model checking, iterative model building.
- **george agent:** Simulation-based inference as a teaching approach.
- **probability-theory skill:** Random variables and distributions that simulation draws from.
- **inferential-statistics skill:** The hypothesis tests and intervals that computational methods extend.
- **bayesian-methods skill:** MCMC as a computational Bayesian tool.

## References

- Efron, B. (1979). "Bootstrap methods: another look at the jackknife." *The Annals of Statistics*, 7(1), 1-26.
- Efron, B., & Tibshirani, R. J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall/CRC.
- Good, P. I. (2005). *Permutation, Parametric, and Bootstrap Tests of Hypotheses*. 3rd edition. Springer.
- Rizzo, M. L. (2019). *Statistical Computing with R*. 2nd edition. CRC Press.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning*. 2nd edition. Springer.
