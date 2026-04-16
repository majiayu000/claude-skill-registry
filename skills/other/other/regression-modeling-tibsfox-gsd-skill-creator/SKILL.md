---
name: regression-modeling
description: Modeling relationships between variables using regression. Covers simple linear regression, multiple regression, polynomial regression, logistic regression, model fitting (least squares, maximum likelihood), residual analysis, model diagnostics, R-squared, adjusted R-squared, multicollinearity, variable selection, and the Box-Jenkins dictum that all models are wrong but some are useful. Use when predicting outcomes, quantifying relationships, building predictive models, or diagnosing model fit.
type: skill
category: statistics
status: stable
origin: tibsfox
modified: false
first_seen: 2026-04-11
first_path: examples/skills/statistics/regression-modeling/SKILL.md
superseded_by: null
---
# Regression Modeling

Regression models quantify the relationship between a response variable and one or more explanatory variables. The goal may be prediction ("what will Y be when X = 10?"), explanation ("how does Y change when X increases by one unit?"), or both. This skill covers the core regression toolkit from simple linear regression through logistic regression, with emphasis on the diagnostics that separate a useful model from a misleading one.

**Agent affinity:** box (model building, diagnostics, "all models are wrong"), pearson (correlation, regression theory), efron (computational model fitting)

**Concept IDs:** stat-descriptive-statistics, stat-hypothesis-testing

## Simple Linear Regression

### The model

Y = beta_0 + beta_1 * X + epsilon, where epsilon ~ N(0, sigma^2).

- **beta_0:** Y-intercept. The predicted value of Y when X = 0.
- **beta_1:** Slope. The change in predicted Y for a one-unit increase in X.
- **epsilon:** Error term. Captures everything the model does not explain.

### Least squares estimation

The least squares estimates minimize the sum of squared residuals:

b_1 = sum((x_i - x-bar)(y_i - y-bar)) / sum((x_i - x-bar)^2)
b_0 = y-bar - b_1 * x-bar

The fitted line y-hat = b_0 + b_1 * x passes through the point (x-bar, y-bar).

### Interpretation

- **b_1 = 2.3:** "For each one-unit increase in X, Y increases by 2.3 units on average."
- **b_0 = 15.7:** "When X = 0, the predicted Y is 15.7." (Only meaningful if X = 0 is within the data range.)
- **Extrapolation warning:** The model is only trustworthy within the range of observed X values. Extrapolating beyond that range assumes the linear relationship continues, which may be false.

## R-Squared and Model Fit

### R-squared (coefficient of determination)

R^2 = 1 - SS_residual / SS_total = SS_regression / SS_total.

R^2 is the proportion of variance in Y explained by the model. Range: 0 to 1. An R^2 of 0.72 means the model explains 72% of the variability in Y.

### Adjusted R-squared

R^2_adj = 1 - (SS_residual / (n-k-1)) / (SS_total / (n-1)).

Adjusted R^2 penalizes for adding predictors. It can decrease when a useless predictor is added. Use adjusted R^2, not R^2, for comparing models with different numbers of predictors.

### Cautions about R-squared

- A high R^2 does not mean the model is correct. A quadratic relationship fit with a line can have moderate R^2 but systematically wrong predictions.
- A low R^2 does not mean the model is useless. In social science, R^2 = 0.10 with a clear causal mechanism is scientifically important.
- R^2 always increases (or stays the same) when you add a predictor, regardless of that predictor's relevance. This is why adjusted R^2 exists.

## Multiple Regression

### The model

Y = beta_0 + beta_1*X_1 + beta_2*X_2 + ... + beta_k*X_k + epsilon.

Each beta_j is the partial effect of X_j on Y, holding all other predictors constant.

### Interpretation with multiple predictors

"Holding all other variables constant, a one-unit increase in X_2 is associated with a b_2-unit change in Y." The phrase "holding all other variables constant" is critical -- it distinguishes multiple regression from running separate simple regressions.

### Multicollinearity

When predictors are highly correlated with each other, the model has difficulty separating their individual effects.

**Detection:**
- **Correlation matrix:** Pairwise correlations > 0.8 are concerning.
- **Variance Inflation Factor (VIF):** VIF_j = 1 / (1 - R^2_j), where R^2_j is the R^2 from regressing X_j on all other predictors. VIF > 10 is a red flag; VIF > 5 warrants attention.

**Consequences:** Coefficients become unstable (large standard errors), making individual predictor effects unreliable. The overall model's predictive ability may be fine.

**Remedies:** Remove one of the correlated predictors, combine them (e.g., principal components), or accept the instability if prediction is the only goal.

## Residual Analysis and Diagnostics

"All models are wrong, but some are useful." -- George E.P. Box. The diagnostics below determine whether a model is useful enough.

### Assumptions to check

1. **Linearity:** The relationship between predictors and response is linear.
2. **Independence:** Residuals are independent of each other.
3. **Homoscedasticity:** Residuals have constant variance across all levels of X.
4. **Normality:** Residuals are approximately normally distributed.

The acronym LINE captures all four.

### Residual plots

| Plot | What it checks | Healthy pattern | Problem signal |
|---|---|---|---|
| Residuals vs. fitted values | Linearity, homoscedasticity | Random scatter around zero | Curved pattern (nonlinearity), funnel shape (heteroscedasticity) |
| Normal Q-Q plot | Normality | Points on the diagonal line | Systematic departures at the tails |
| Residuals vs. predictor | Linearity for each predictor | Random scatter | Curved pattern |
| Residuals vs. order | Independence | Random scatter | Patterns over time (autocorrelation) |

### Influential observations

- **Leverage:** How far an observation's X value is from the mean of X. High leverage points have outsized potential influence.
- **Cook's distance:** Measures how much all fitted values change when observation i is removed. Cook's D > 4/n is a common threshold.
- **DFFITS:** The change in the fitted value at X_i when observation i is deleted. |DFFITS| > 2*sqrt(k/n) is flagged.

**Action:** Investigate influential points. They may be data entry errors, genuinely unusual observations, or indicators that the model is wrong. Do not automatically remove them.

## Polynomial Regression

Y = beta_0 + beta_1*X + beta_2*X^2 + ... + beta_p*X^p + epsilon.

Used when the scatter plot shows curvature that a straight line cannot capture.

**Cautions:**
- Higher-degree polynomials can overfit, fitting noise rather than signal.
- Polynomial extrapolation is especially dangerous -- polynomial tails diverge wildly.
- Start with degree 2; go higher only with strong evidence and domain justification.

## Logistic Regression

### When the response is binary

When Y is 0 or 1 (success/failure, yes/no), linear regression is inappropriate (predicted values can fall outside [0, 1]). Logistic regression models the log-odds:

log(p / (1-p)) = beta_0 + beta_1*X_1 + ... + beta_k*X_k

where p = P(Y = 1).

### Interpretation

- **Odds ratio:** exp(beta_j) is the multiplicative change in odds for a one-unit increase in X_j. An odds ratio of 1.5 means "50% higher odds of success."
- **Probability curve:** The logistic function p = 1 / (1 + exp(-(beta_0 + beta_1*X))) produces an S-shaped curve mapping the linear predictor to [0, 1].

### Model fitting

Logistic regression is fit by maximum likelihood, not least squares. The log-likelihood is maximized iteratively (usually via Newton-Raphson or Fisher scoring).

### Diagnostics

- **Deviance residuals** replace ordinary residuals.
- **AIC** (Akaike Information Criterion) for model comparison (lower is better).
- **Hosmer-Lemeshow test** for goodness-of-fit.
- **ROC curve and AUC** for classification performance.

## Variable Selection

### Methods

| Method | Approach | Strengths | Weaknesses |
|---|---|---|---|
| Forward selection | Start with no predictors, add the most significant one at each step | Simple | May miss important combinations |
| Backward elimination | Start with all predictors, remove the least significant one at each step | Considers all predictors | Requires n >> k |
| Stepwise | Combination of forward and backward | Flexible | Overfits; inflates significance |
| Best subsets | Evaluate all 2^k possible models | Exhaustive | Computationally expensive for large k |
| LASSO (L1 penalty) | Penalized regression that shrinks some coefficients to zero | Built-in variable selection, handles multicollinearity | Requires tuning of penalty parameter |
| AIC / BIC comparison | Select model with lowest information criterion | Principled tradeoff between fit and complexity | Requires fitting multiple models |

**Box's dictum applied:** No variable selection method guarantees finding the "true" model. Use domain knowledge first, then let statistical methods refine.

## Common Mistakes

| Mistake | Why it fails | Fix |
|---|---|---|
| Interpreting correlation as causation | Regression shows association, not causation | Only causal language if the study design supports it (experiment, not observational) |
| Ignoring residual plots | The model may be systematically wrong | Always plot residuals after fitting |
| Extrapolating beyond data range | No evidence that the relationship holds outside observed X values | State the range of validity |
| Adding too many predictors | Overfitting; R^2 increases but generalization decreases | Use adjusted R^2 or cross-validation |
| Ignoring influential points | One point can change the entire regression line | Check leverage, Cook's distance, DFFITS |
| Using linear regression for binary outcomes | Predicted values outside [0, 1], violates assumptions | Use logistic regression |

## Cross-References

- **box agent:** Model building philosophy, response surface methodology, diagnostics.
- **pearson agent:** Regression theory, correlation, coefficient estimation.
- **efron agent:** Computational fitting, cross-validation, bootstrap for regression.
- **descriptive-statistics skill:** Scatter plots and correlation precede regression.
- **inferential-statistics skill:** Hypothesis tests for regression coefficients.
- **bayesian-methods skill:** Bayesian regression as an alternative to frequentist fitting.

## References

- Box, G. E. P. (1976). "Science and statistics." *Journal of the American Statistical Association*, 71(356), 791-799.
- Kutner, M. H., Nachtsheim, C. J., Neter, J., & Li, W. (2005). *Applied Linear Statistical Models*. 5th edition. McGraw-Hill.
- Agresti, A. (2015). *Foundations of Linear and Generalized Linear Models*. Wiley.
- James, G., Witten, D., Hastie, T., & Tibshirani, R. (2021). *An Introduction to Statistical Learning*. 2nd edition. Springer.
- Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied Logistic Regression*. 3rd edition. Wiley.
