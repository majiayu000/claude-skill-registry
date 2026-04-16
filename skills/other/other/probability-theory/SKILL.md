---
name: probability-theory
description: Mathematical foundations of uncertainty and random phenomena. Covers sample spaces, events, axioms, conditional probability, Bayes' theorem, independence, random variables, distributions (discrete and continuous), expected value, variance, the law of large numbers, and the central limit theorem. Use when computing probabilities, reasoning about random events, working with probability distributions, or building the foundation for statistical inference.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/probability-theory/SKILL.md
superseded_by: null
---
# Probability Theory

Probability is the mathematical language of uncertainty. It provides the axiomatic foundation on which all of statistical inference rests: without probability, there is no hypothesis testing, no confidence intervals, no Bayesian updating, no regression. This skill covers the core machinery from sample spaces through the central limit theorem.

**Agent affinity:** bayes (conditional probability, Bayes' theorem), pearson (distributional theory), efron (computational probability)

**Concept IDs:** stat-probability-foundations, stat-experimental-theoretical, stat-expected-value, stat-conditional-probability

## Axioms and Sample Spaces

### Kolmogorov's axioms

A probability function P on a sample space S satisfies:

1. **Non-negativity:** P(A) >= 0 for every event A.
2. **Normalization:** P(S) = 1.
3. **Countable additivity:** For mutually exclusive events A_1, A_2, ..., P(A_1 union A_2 union ...) = P(A_1) + P(A_2) + ...

Everything in probability follows from these three axioms plus set theory.

### Sample space and events

- **Sample space (S):** The set of all possible outcomes of a random experiment.
- **Event (A):** A subset of S. "The die shows an even number" = {2, 4, 6}.
- **Complement (A^c):** Everything in S not in A. P(A^c) = 1 - P(A).
- **Empty event:** P(empty set) = 0.

### Counting and equally likely outcomes

When all outcomes are equally likely: P(A) = |A| / |S|.

This requires the fundamental counting tools:
- **Multiplication principle:** If task 1 has n_1 outcomes and task 2 has n_2 outcomes, the sequence has n_1 * n_2 outcomes.
- **Permutations:** n! / (n-k)! ordered arrangements of k items from n.
- **Combinations:** C(n,k) = n! / (k!(n-k)!) unordered selections.

## Conditional Probability

### Definition

P(A | B) = P(A intersect B) / P(B), provided P(B) > 0.

Read as "the probability of A given B." Conditioning restricts the sample space to the event B.

### The multiplication rule

P(A intersect B) = P(A | B) * P(B) = P(B | A) * P(A).

For three events: P(A intersect B intersect C) = P(A) * P(B | A) * P(C | A intersect B).

### The law of total probability

If B_1, B_2, ..., B_n partition S (mutually exclusive and exhaustive):

P(A) = sum over i of P(A | B_i) * P(B_i).

This is essential for "breaking a problem into cases" in probability.

## Bayes' Theorem

P(B_j | A) = P(A | B_j) * P(B_j) / P(A)

where P(A) is computed via the law of total probability.

**Terminology:**
- P(B_j) = **prior** probability of B_j (before observing A).
- P(A | B_j) = **likelihood** of observing A given B_j.
- P(B_j | A) = **posterior** probability of B_j (after observing A).
- P(A) = **marginal likelihood** or **evidence**.

**Worked example.** A disease affects 1% of the population. A test has 95% sensitivity (true positive rate) and 90% specificity (true negative rate). If a person tests positive, what is the probability they have the disease?

P(Disease | Positive) = P(Positive | Disease) * P(Disease) / P(Positive)
= (0.95)(0.01) / [(0.95)(0.01) + (0.10)(0.99)]
= 0.0095 / (0.0095 + 0.099)
= 0.0095 / 0.1085
= 0.0876 (about 8.8%)

Despite a positive test, the probability of disease is only ~9%. This is the base rate fallacy in action: when the disease is rare, even a good test produces many false positives relative to true positives.

## Independence

Events A and B are independent if P(A intersect B) = P(A) * P(B), equivalently if P(A | B) = P(A).

**Mutual independence** of n events requires all 2^n - n - 1 subset product conditions, not just pairwise independence.

**Common error:** Assuming independence when events share a common cause. Drawing cards without replacement creates dependence between draws.

## Random Variables and Distributions

### Discrete random variables

A discrete random variable X maps outcomes to countable values. Its **probability mass function (PMF)** is p(x) = P(X = x).

| Distribution | PMF | Parameters | Mean | Variance | Use when |
|---|---|---|---|---|---|
| Bernoulli | p^x (1-p)^(1-x) | p | p | p(1-p) | Single yes/no trial |
| Binomial | C(n,x) p^x (1-p)^(n-x) | n, p | np | np(1-p) | Count of successes in n independent trials |
| Geometric | (1-p)^(x-1) p | p | 1/p | (1-p)/p^2 | Trials until first success |
| Poisson | e^(-lambda) lambda^x / x! | lambda | lambda | lambda | Count of rare events in a fixed interval |
| Hypergeometric | C(K,x)C(N-K,n-x)/C(N,n) | N, K, n | nK/N | complex | Sampling without replacement |

### Continuous random variables

A continuous random variable X has a **probability density function (PDF)** f(x) where P(a <= X <= b) = integral from a to b of f(x) dx.

| Distribution | PDF | Parameters | Mean | Variance | Use when |
|---|---|---|---|---|---|
| Uniform | 1/(b-a) on [a,b] | a, b | (a+b)/2 | (b-a)^2/12 | All values in an interval equally likely |
| Normal | (1/(sigma*sqrt(2pi))) exp(-(x-mu)^2/(2sigma^2)) | mu, sigma | mu | sigma^2 | Sums of many independent effects (CLT) |
| Exponential | lambda * exp(-lambda*x) | lambda | 1/lambda | 1/lambda^2 | Time between Poisson events |
| t-distribution | complex | df | 0 (df>1) | df/(df-2) | Small-sample inference, unknown sigma |
| Chi-squared | complex | df | df | 2*df | Sum of squared standard normals |

### The CDF

The cumulative distribution function F(x) = P(X <= x). For discrete: sum of PMF up to x. For continuous: integral of PDF up to x.

## Expected Value and Variance

### Expected value

E(X) = sum of x * p(x) [discrete] or integral of x * f(x) dx [continuous].

**Linearity:** E(aX + bY) = aE(X) + bE(Y). Always. No independence required.

### Variance

Var(X) = E[(X - mu)^2] = E(X^2) - [E(X)]^2.

**For independent X and Y:** Var(X + Y) = Var(X) + Var(Y).
**For any X and Y:** Var(X + Y) = Var(X) + Var(Y) + 2Cov(X, Y).

### Covariance and correlation

Cov(X, Y) = E[(X - mu_X)(Y - mu_Y)] = E(XY) - E(X)E(Y).
Corr(X, Y) = Cov(X, Y) / (SD(X) * SD(Y)).

## Limit Theorems

### Law of large numbers (LLN)

As sample size n grows, the sample mean X-bar converges to the population mean mu.

- **Weak LLN:** For any epsilon > 0, P(|X-bar - mu| > epsilon) -> 0 as n -> infinity.
- **Strong LLN:** P(X-bar -> mu) = 1.

This is why averages stabilize and why gambling houses make money in the long run.

### Central limit theorem (CLT)

If X_1, X_2, ..., X_n are independent with mean mu and finite variance sigma^2, then as n -> infinity:

(X-bar - mu) / (sigma / sqrt(n)) converges in distribution to N(0, 1).

**Practical rule:** The CLT approximation is usually adequate for n >= 30, though this depends on the shape of the parent distribution. More skewed distributions need larger n.

**Why it matters:** The CLT explains why the normal distribution appears everywhere in statistics. It justifies using z-tests and t-tests for sample means even when the population is not normal.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Confusing P(A given B) with P(B given A) | The prosecutor's fallacy; these are generally not equal | Apply Bayes' theorem explicitly |
| Assuming independence without justification | Creates dramatically wrong probability calculations | State the independence assumption; verify it |
| Adding probabilities of non-mutually-exclusive events | P(A or B) != P(A) + P(B) unless A and B are disjoint | Use inclusion-exclusion: P(A or B) = P(A) + P(B) - P(A and B) |
| Ignoring the base rate | Rare events + imperfect tests = high false positive rates | Always incorporate the prior P(B) via Bayes' theorem |
| Applying CLT to small n | The approximation breaks down for small samples | Use exact distributions or the t-distribution |

## Cross-References

- **bayes agent:** Bayesian reasoning, prior-to-posterior updating, probabilistic modeling.
- **pearson agent:** Distributional theory, correlation, chi-squared tests.
- **efron agent:** Computational approaches to probability (simulation, bootstrap).
- **descriptive-statistics skill:** Empirical distributions that probability theory models.
- **inferential-statistics skill:** Uses probability theory to draw conclusions from data.
- **bayesian-methods skill:** Extends Bayes' theorem into a complete inferential framework.

## References

- Ross, S. M. (2019). *A First Course in Probability*. 10th edition. Pearson.
- Blitzstein, J. K., & Hwang, J. (2019). *Introduction to Probability*. 2nd edition. CRC Press.
- Kolmogorov, A. N. (1933). *Foundations of the Theory of Probability*. Chelsea Publishing (1956 English translation).
- Feller, W. (1968). *An Introduction to Probability Theory and Its Applications*. Vol. 1, 3rd edition. Wiley.
