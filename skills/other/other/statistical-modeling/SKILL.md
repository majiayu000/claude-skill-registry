---
name: statistical-modeling
description: Regression analysis, ANOVA, generalized linear models, Bayesian methods, and model selection. Covers the full modeling workflow from problem formulation through diagnostics -- linear regression, logistic regression, Poisson regression, mixed-effects models, prior specification, posterior inference, AIC/BIC comparison, cross-validation for model selection, and assumption checking. Use when fitting models, testing hypotheses, or selecting among competing statistical explanations.
type: skill
category: data-science
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-12
first_path: examples/skills/data-science/statistical-modeling/SKILL.md
superseded_by: null
---
# Statistical Modeling

Statistical modeling is the practice of fitting mathematical structures to data in order to quantify relationships, test hypotheses, and make predictions. Unlike machine learning, which optimizes prediction, statistical modeling privileges interpretability and inference -- understanding *why* variables relate, not just *that* they do. Leo Breiman's "two cultures" paper (2001) crystallized this distinction. This skill covers the inferential tradition while acknowledging where the two cultures overlap.

**Agent affinity:** tukey (EDA and diagnostics), fisher (experimental design and ANOVA), breiman (model comparison)

**Concept IDs:** data-hypothesis-testing, data-confidence-intervals, data-correlation, data-normal-distribution

## The Modeling Workflow

| Stage | Goal | Key operations |
|---|---|---|
| 1. Formulation | Define the question as a model | Specify response variable, predictors, functional form |
| 2. Exploration | Understand data structure | Scatterplots, correlation matrices, distribution checks |
| 3. Fitting | Estimate parameters | OLS, MLE, MCMC, IRLS depending on model class |
| 4. Diagnostics | Check assumptions | Residual plots, Q-Q plots, leverage, VIF |
| 5. Inference | Draw conclusions | Confidence intervals, hypothesis tests, effect sizes |
| 6. Selection | Compare models | AIC, BIC, cross-validation, likelihood ratio tests |
| 7. Communication | Report results | Effect estimates with uncertainty, not just p-values |

## Linear Regression

### The Model

y = beta_0 + beta_1 * x_1 + beta_2 * x_2 + ... + beta_p * x_p + epsilon

where epsilon ~ N(0, sigma^2) independently. The betas are estimated by ordinary least squares (OLS), minimizing the sum of squared residuals.

### Assumptions (LINE)

| Assumption | Check | Violation consequence |
|---|---|---|
| **L**inearity | Residual vs. fitted plot -- no pattern | Biased estimates, meaningless coefficients |
| **I**ndependence | Study design, Durbin-Watson test | Underestimated standard errors, inflated significance |
| **N**ormality of residuals | Q-Q plot, Shapiro-Wilk test | Unreliable confidence intervals and p-values (less critical for large n by CLT) |
| **E**qual variance (homoscedasticity) | Scale-location plot, Breusch-Pagan test | Inefficient estimates, unreliable standard errors |

### Interpretation

- **beta_j:** The expected change in y for a one-unit increase in x_j, holding all other predictors constant.
- **R-squared:** Proportion of variance in y explained by the model. Not a measure of model quality alone -- a high R-squared with violated assumptions is meaningless.
- **Adjusted R-squared:** Penalizes for number of predictors. Always use this for model comparison.

### Multicollinearity

When predictors are highly correlated, coefficient estimates become unstable. Variance Inflation Factor (VIF) quantifies this: VIF > 5-10 indicates problematic collinearity. Remedies: drop a predictor, combine predictors via PCA, or use regularization (ridge regression).

## Logistic Regression

### The Model

For binary outcome y in {0, 1}:

log(p / (1 - p)) = beta_0 + beta_1 * x_1 + ... + beta_p * x_p

where p = P(y = 1 | x). The left side is the log-odds (logit). Parameters are estimated by maximum likelihood.

### Interpretation

- **exp(beta_j):** The odds ratio for a one-unit increase in x_j, holding other predictors constant. An odds ratio of 1.5 means 50% higher odds of the outcome.
- **Predicted probability:** p = 1 / (1 + exp(-(beta_0 + beta_1 * x_1 + ...))). The sigmoid function maps the linear predictor to [0, 1].
- **No R-squared analog that works well.** Use pseudo-R-squared measures (McFadden, Nagelkerke) with caution. Prefer ROC-AUC or calibration plots for assessing fit.

### Assumptions

- Observations are independent.
- The log-odds are a linear function of the predictors (check with partial residual plots).
- No perfect multicollinearity.
- No assumption of normality or equal variance -- this is not linear regression with a binary outcome.

## Generalized Linear Models (GLMs)

Logistic regression is one instance of the GLM framework. The general structure:

| Component | Role |
|---|---|
| **Random component** | Distribution of y (Normal, Binomial, Poisson, Gamma, ...) |
| **Systematic component** | Linear predictor eta = X * beta |
| **Link function** | g(mu) = eta, connecting the mean to the linear predictor |

### Common GLMs

| Response type | Distribution | Link | Model name |
|---|---|---|---|
| Continuous | Normal | Identity | Linear regression |
| Binary | Binomial | Logit | Logistic regression |
| Count | Poisson | Log | Poisson regression |
| Count (overdispersed) | Negative binomial | Log | Negative binomial regression |
| Positive continuous | Gamma | Log or inverse | Gamma regression |
| Proportion (not 0/1) | Beta | Logit | Beta regression |

### Poisson Regression

For count data: log(mu) = beta_0 + beta_1 * x_1 + ... Assumes the mean equals the variance (equidispersion). When variance > mean (overdispersion), use negative binomial or quasi-Poisson. Always check for overdispersion.

## Analysis of Variance (ANOVA)

### Purpose

ANOVA tests whether group means differ. It is a special case of linear regression where all predictors are categorical.

### One-Way ANOVA

- **Null hypothesis:** mu_1 = mu_2 = ... = mu_k (all group means are equal).
- **Test statistic:** F = (between-group variance) / (within-group variance).
- **Assumptions:** Independence, normality within groups, equal variances (Levene's test).
- **Post-hoc:** If the F-test rejects, pairwise comparisons identify which groups differ. Use Tukey's HSD or Bonferroni correction to control family-wise error rate.

### Two-Way ANOVA

Adds a second factor and their interaction. The interaction term tests whether the effect of one factor depends on the level of the other. Always plot the interaction (mean response by factor A, colored by factor B) before interpreting the F-test.

### ANOVA as Regression

One-way ANOVA with k groups is equivalent to linear regression with k-1 dummy variables. The F-test in ANOVA is the same as the overall F-test in regression. Understanding this equivalence clarifies that ANOVA is not a separate method -- it is regression with categorical predictors.

## Bayesian Methods

### The Framework

Bayesian inference updates prior beliefs with data to produce posterior beliefs:

posterior is proportional to likelihood times prior

P(theta | data) proportional to P(data | theta) * P(theta)

### Prior Specification

| Prior type | When to use | Example |
|---|---|---|
| **Informative** | Strong domain knowledge | "The effect is between 0.5 and 1.5 based on prior studies" |
| **Weakly informative** | Some domain knowledge, want to regularize | Normal(0, 10) for regression coefficients -- centered at zero, wide but not flat |
| **Non-informative** | Want the data to dominate | Uniform or Jeffreys prior. Rarely truly "non-informative" -- all priors carry assumptions |

### Posterior Inference

- **Credible interval:** The 95% credible interval contains the parameter with 95% probability. This is what people *think* frequentist confidence intervals mean (but they don't).
- **Posterior predictive checks:** Simulate data from the posterior and compare to observed data. If the model is good, simulated data should look like real data.
- **Model comparison:** Bayes factors, WAIC, LOO-CV. These naturally penalize complexity without needing a separate penalty term.

### Practical Bayesian Workflow

1. Specify the model (likelihood + priors).
2. Fit using MCMC (Stan, PyMC, JAGS) or variational inference.
3. Check convergence: R-hat < 1.01, effective sample size > 400, no divergent transitions.
4. Posterior predictive checks.
5. Report posterior summaries with credible intervals.

## Model Selection

### Information Criteria

| Criterion | Formula | Interpretation |
|---|---|---|
| **AIC** | -2 * log-likelihood + 2k | Estimates out-of-sample prediction error. Lower is better. |
| **BIC** | -2 * log-likelihood + k * log(n) | Penalizes complexity more heavily than AIC. Consistent (selects true model as n -> infinity). |
| **WAIC** | Bayesian analog of AIC | Uses the full posterior, not point estimates. Preferred for Bayesian models. |

AIC favors prediction accuracy; BIC favors parsimony. When they disagree, consider the goal: prediction -> AIC, explanation -> BIC.

### Cross-Validation

- **k-fold CV:** Split data into k folds, fit on k-1, evaluate on the held-out fold, rotate. Average performance across folds.
- **Leave-one-out (LOO):** k = n. Expensive but lowest variance. Approximated efficiently by PSIS-LOO for Bayesian models.
- **Repeated CV:** Run k-fold multiple times with different splits to reduce variance in the estimate.

### Nested vs. Non-Nested Models

- **Nested models** (one is a special case of the other): Use likelihood ratio test, F-test, or compare AIC/BIC.
- **Non-nested models** (different functional forms): Use AIC/BIC or cross-validation. Likelihood ratio tests are not valid.

## Diagnostics Checklist

| Check | Tool | What to look for |
|---|---|---|
| Linearity | Residual vs. fitted plot | No systematic pattern |
| Normality | Q-Q plot | Points on the diagonal line |
| Homoscedasticity | Scale-location plot | Horizontal band, no funnel |
| Independence | Durbin-Watson, ACF plot | DW near 2, no significant autocorrelation |
| Influential points | Cook's distance | No points with Cook's D > 4/n |
| Multicollinearity | VIF | All VIF < 5 |
| Overdispersion (GLM) | Residual deviance / df | Ratio near 1 |

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Interpreting p > 0.05 as "no effect" | Absence of evidence is not evidence of absence | Report effect size with confidence interval |
| Stepwise variable selection | Inflates Type I error, unstable results | Use AIC/BIC or cross-validation |
| Ignoring multicollinearity | Unstable coefficients, misleading significance | Check VIF, consider combining or dropping predictors |
| Extrapolating beyond data range | Model has no support outside observed x-range | State the range of validity explicitly |
| Confusing correlation with causation | Regression coefficients are associations unless the design is experimental | Use causal language only with randomized experiments or strong causal inference methods |
| Reporting R-squared without diagnostics | High R-squared with violated assumptions is meaningless | Always check assumptions before interpreting fit statistics |

## Cross-References

- **tukey agent:** Exploratory data analysis that precedes and informs model specification. Tukey's box plots and stem-and-leaf plots reveal the structure that guides model choice.
- **fisher agent:** Experimental design that produces data suitable for causal inference via ANOVA and regression.
- **breiman agent:** Machine learning models as alternatives when prediction dominates inference.
- **data-wrangling skill:** Data cleaning and transformation that produces analysis-ready inputs for modeling.
- **experimental-design-ds skill:** A/B testing and randomization that make causal claims from regression valid.
- **machine-learning-foundations skill:** The prediction-focused counterpart to this inference-focused skill.

## References

- Breiman, L. (2001). "Statistical Modeling: The Two Cultures." *Statistical Science*, 16(3), 199-231.
- Gelman, A., Carlin, J. B., Stern, H. S., Dunson, D. B., Vehtari, A., & Rubin, D. B. (2013). *Bayesian Data Analysis*. 3rd edition. CRC Press.
- Kutner, M. H., Nachtsheim, C. J., Neter, J., & Li, W. (2005). *Applied Linear Statistical Models*. 5th edition. McGraw-Hill.
- McCullagh, P. & Nelder, J. A. (1989). *Generalized Linear Models*. 2nd edition. Chapman & Hall.
- McElreath, R. (2020). *Statistical Rethinking*. 2nd edition. CRC Press.
