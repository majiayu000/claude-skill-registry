---
name: bayesian-methods
description: Bayesian approach to statistical inference and decision-making. Covers prior specification, likelihood functions, posterior computation, conjugate priors, Markov chain Monte Carlo (MCMC), credible intervals, Bayesian hypothesis comparison (Bayes factors), hierarchical models, and the philosophical contrast with frequentist methods. Use when updating beliefs with data, specifying priors, computing posteriors, comparing Bayesian and frequentist approaches, or building hierarchical models.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/bayesian-methods/SKILL.md
superseded_by: null
---
# Bayesian Methods

Bayesian statistics treats probability as a measure of belief, updated by data through Bayes' theorem. Where frequentist statistics asks "how likely are these data under H_0?", Bayesian statistics asks "given these data, what should I believe about the parameter?" This skill covers the machinery of Bayesian inference from prior specification through MCMC computation.

**Agent affinity:** bayes (all Bayesian reasoning), efron (empirical Bayes, computational methods), box (model comparison)

**Concept IDs:** stat-conditional-probability, stat-probability-foundations, stat-hypothesis-testing

## The Bayesian Framework

### Bayes' theorem for parameters

P(theta | data) = P(data | theta) * P(theta) / P(data)

- **P(theta):** Prior distribution. What you believe about theta before seeing data.
- **P(data | theta):** Likelihood. The probability of the observed data given theta.
- **P(theta | data):** Posterior distribution. Your updated belief about theta after seeing data.
- **P(data):** Marginal likelihood (evidence). A normalizing constant: integral of P(data | theta) * P(theta) over all theta.

In practice, the posterior is proportional to the likelihood times the prior:

posterior proportional to likelihood * prior.

### Contrast with frequentist inference

| Aspect | Frequentist | Bayesian |
|---|---|---|
| Probability interpretation | Long-run frequency | Degree of belief |
| Parameters | Fixed but unknown | Random variables with distributions |
| Inference output | P-values, confidence intervals | Posterior distributions, credible intervals |
| Prior information | Not formally incorporated | Explicitly modeled via prior |
| Interpretation of interval | "95% of such intervals contain the true parameter" | "There is a 95% probability the parameter is in this interval" |

Neither framework is universally superior. They answer different questions and are appropriate in different contexts.

## Prior Specification

### Types of priors

| Type | Description | Example | When to use |
|---|---|---|---|
| Informative | Concentrates probability on plausible values | N(100, 10^2) for adult systolic BP | Strong prior knowledge from previous studies |
| Weakly informative | Broad but bounded | N(0, 100^2) for a regression coefficient | Some domain knowledge about reasonable scale |
| Non-informative / flat | Uniform or Jeffreys' prior | Uniform(-inf, inf) for a location parameter | "Let the data speak" (but truly flat priors can be improper) |
| Conjugate | Prior family that combines analytically with the likelihood | Beta prior + Binomial likelihood = Beta posterior | Computational convenience; closed-form posterior |
| Empirical Bayes | Prior estimated from the data itself | Estimate the prior hyperparameters from marginal distribution | Large number of similar units (e.g., many hospitals) |

### Conjugate families

| Likelihood | Conjugate prior | Posterior |
|---|---|---|
| Binomial(n, p) | Beta(alpha, beta) | Beta(alpha + x, beta + n - x) |
| Poisson(lambda) | Gamma(alpha, beta) | Gamma(alpha + sum(x_i), beta + n) |
| Normal(mu, sigma^2 known) | Normal(mu_0, sigma_0^2) | Normal(weighted mean, combined precision) |
| Normal(mu known, sigma^2) | Inverse-Gamma(alpha, beta) | Inverse-Gamma(alpha + n/2, beta + SS/2) |
| Exponential(lambda) | Gamma(alpha, beta) | Gamma(alpha + n, beta + sum(x_i)) |

### Prior sensitivity analysis

Always check whether conclusions depend heavily on the prior. If two reasonable priors lead to very different posteriors, the data are not informative enough to overcome prior uncertainty. Report this honestly.

## Posterior Computation

### Analytical posteriors (conjugate case)

When the prior is conjugate to the likelihood, the posterior has a known closed form. This is computationally trivial and pedagogically clean.

**Worked example.** Suppose we observe x = 7 successes in n = 20 trials. With a Beta(1, 1) prior (uniform on [0, 1]):

Posterior: Beta(1 + 7, 1 + 13) = Beta(8, 14).
Posterior mean: 8/22 = 0.364.
Posterior mode: (8-1)/(8+14-2) = 7/20 = 0.35.
95% credible interval: approximately [0.17, 0.58] (from Beta quantiles).

### Markov chain Monte Carlo (MCMC)

When the posterior has no closed form, MCMC generates samples from the posterior distribution.

**Metropolis-Hastings algorithm:**
1. Start at an initial theta_0.
2. Propose theta* from a proposal distribution q(theta* | theta_current).
3. Compute acceptance ratio: alpha = min(1, [P(theta* | data) * q(theta_current | theta*)] / [P(theta_current | data) * q(theta* | theta_current)]).
4. Accept theta* with probability alpha; otherwise stay at theta_current.
5. Repeat for thousands of iterations.

**Gibbs sampling:** A special case where each parameter is sampled from its full conditional distribution in turn. Often more efficient when full conditionals are available.

**Diagnostics:**
- **Trace plots:** The chain should look like random noise around a stable level (good mixing), not trending or stuck.
- **R-hat (Gelman-Rubin):** Run multiple chains; R-hat should be close to 1.0 (< 1.05).
- **Effective sample size (ESS):** Account for autocorrelation; ESS should be at least several hundred.
- **Burn-in:** Discard initial iterations before the chain reaches its stationary distribution.

## Credible Intervals

### Posterior credible intervals

A 95% credible interval [a, b] satisfies P(a <= theta <= b | data) = 0.95.

Unlike a confidence interval, this directly states the probability that theta lies in the interval (given the model and data).

### Types

- **Equal-tailed interval:** 2.5th and 97.5th posterior percentiles. Simple and commonly reported.
- **Highest posterior density (HPD) interval:** The narrowest interval containing 95% of the posterior mass. More efficient but harder to compute.

## Bayesian Hypothesis Comparison

### Bayes factors

The Bayes factor BF_10 compares two hypotheses:

BF_10 = P(data | H_1) / P(data | H_0)

where each marginal likelihood integrates over the parameter space under that hypothesis.

**Interpretation (Kass & Raftery scale):**
- BF < 1: Evidence favors H_0.
- 1 < BF < 3: Barely worth mentioning.
- 3 < BF < 20: Positive evidence for H_1.
- 20 < BF < 150: Strong evidence.
- BF > 150: Very strong evidence.

### Comparison with p-values

Bayes factors and p-values can disagree. A p-value of 0.04 might correspond to a Bayes factor near 1, providing essentially no evidence against H_0. This "Jeffreys-Lindley paradox" arises because the p-value measures tail probability while the Bayes factor measures overall fit.

## Hierarchical Models

### The idea

When data come in groups (students within schools, patients within hospitals), hierarchical models let each group have its own parameter while "borrowing strength" from the overall distribution.

Level 1: Y_ij | theta_j ~ F(theta_j) (within-group model)
Level 2: theta_j ~ G(phi) (between-group model)
Level 3: phi ~ H() (hyperprior)

### Shrinkage

Hierarchical models produce "shrinkage": group-level estimates are pulled toward the overall mean. Groups with small samples are pulled more; groups with large samples are pulled less. This is a natural form of regularization.

### Empirical Bayes

Efron's empirical Bayes approach estimates the hyperparameters phi from the marginal distribution of the data, then treats them as known. This is computationally simpler than full Bayes but ignores uncertainty in phi.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Using an improper prior without checking | Can produce an improper posterior (no valid probability distribution) | Verify the posterior integrates to 1 |
| Ignoring prior sensitivity | Conclusions may be driven by the prior, not the data | Run prior sensitivity analysis |
| Too short MCMC chain | Posterior estimates are noisy and biased | Check convergence diagnostics (R-hat, ESS, trace plots) |
| Treating credible intervals as confidence intervals | Different definitions, different coverage properties | State which you are reporting and interpret accordingly |
| Bayes factor with vague priors (Bartlett's paradox) | Diffuse priors inflate the marginal likelihood denominator, biasing against H_1 | Use principled, finite-variance priors for hypothesis comparison |

## Cross-References

- **bayes agent:** All Bayesian reasoning, prior-to-posterior updating, model comparison.
- **efron agent:** Empirical Bayes, bootstrap, computational Bayesian methods.
- **box agent:** Model comparison, diagnostics, the interplay of Bayesian and frequentist approaches.
- **probability-theory skill:** Bayes' theorem and conditional probability as the foundation.
- **inferential-statistics skill:** Frequentist framework for contrast.
- **statistical-computing skill:** Computational tools for MCMC and posterior summaries.

## References

- Bayes, T. (1763). "An essay towards solving a problem in the doctrine of chances." *Philosophical Transactions of the Royal Society*, 53, 370-418.
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis*. 3rd edition. CRC Press.
- McElreath, R. (2020). *Statistical Rethinking*. 2nd edition. CRC Press.
- Efron, B. (2010). *Large-Scale Inference: Empirical Bayes Methods for Estimation, Testing, and Prediction*. Cambridge University Press.
- Kass, R. E., & Raftery, A. E. (1995). "Bayes factors." *Journal of the American Statistical Association*, 90(430), 773-795.
