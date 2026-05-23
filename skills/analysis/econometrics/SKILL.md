# Econometrics

name: econometrics
description: Econometric methods — regression, panel data, IV. Cover OLS, panel (FE/RE), instrumental variables, VAR.

## When to Activate

- Specifying and estimating regression models for economic and financial data
- Choosing between OLS, panel data (fixed/random effects), and IV approaches
- Diagnosing and correcting econometric issues (heteroskedasticity, autocorrelation, endogeneity)
- Estimating vector autoregression (VAR) models for time series forecasting
- Interpreting regression results and assessing statistical significance
- Causal inference using instrumental variables, difference-in-differences, or RDD
- Forecasting financial or macroeconomic variables using econometric models
- Evaluating published empirical research for methodological soundness

## Core Concepts

### Ordinary Least Squares (OLS)

**Model:**
```
Y = beta_0 + beta_1 * X_1 + beta_2 * X_2 + ... + beta_k * X_k + epsilon

OLS minimizes: Sum of squared residuals = Sum(Y_i - Y_hat_i)^2
```

**Gauss-Markov assumptions (for OLS to be BLUE — Best Linear Unbiased Estimator):**
1. **Linearity:** Y is a linear function of the parameters (not necessarily of X — log, polynomial OK)
2. **Random sampling:** Observations are independently drawn
3. **No perfect multicollinearity:** No exact linear relationship among independent variables
4. **Zero conditional mean:** E[epsilon | X] = 0 (exogeneity — the critical assumption)
5. **Homoskedasticity:** Var(epsilon | X) = sigma^2 (constant variance)

**Additional for valid inference:**
6. **Normality of errors:** epsilon ~ N(0, sigma^2) — needed for exact t and F tests in small samples (not needed asymptotically)

**Key diagnostics:**
| Issue | Detection | Consequence | Solution |
|-------|-----------|-------------|----------|
| Heteroskedasticity | Breusch-Pagan, White test | Inefficient estimates, biased SEs | Robust (White) SEs, WLS |
| Autocorrelation | Durbin-Watson, Breusch-Godfrey | Inefficient, biased SEs | Newey-West SEs, GLS, add lags |
| Multicollinearity | VIF > 10, condition number | Inflated SEs, unstable coefficients | Drop variable, PCA, ridge |
| Endogeneity | Hausman test, theory | Biased and inconsistent | IV/2SLS, panel FE, natural experiment |
| Omitted variable | Ramsey RESET test | Bias if correlated with X | Add controls, use FE, IV |
| Non-normality | Jarque-Bera test | Invalid small-sample inference | Larger sample, bootstrap, transform |

**Interpreting coefficients:**
```
Linear-linear:  Y = a + bX       → 1 unit increase in X → b unit change in Y
Log-linear:     ln(Y) = a + bX   → 1 unit increase in X → b*100% change in Y
Linear-log:     Y = a + b*ln(X)  → 1% increase in X → b/100 unit change in Y
Log-log:        ln(Y) = a + b*ln(X) → 1% increase in X → b% change in Y (elasticity)
```

### Panel Data Methods

**Panel data structure:** Observations on N entities (firms, countries) over T time periods.

**Pooled OLS:**
```
Y_it = beta_0 + beta_1 * X_it + epsilon_it

Ignores panel structure. Inconsistent if entity-specific effects correlated with X.
```

**Fixed Effects (FE) — Within Estimator:**
```
Y_it = alpha_i + beta * X_it + epsilon_it

alpha_i = entity-specific fixed effect (absorbed / differenced out)

Advantages:
  - Controls for all time-invariant unobserved heterogeneity
  - Consistent even if alpha_i is correlated with X_it
  - Most common panel estimator in applied economics

Limitations:
  - Cannot estimate effects of time-invariant variables (industry, country dummies)
  - Requires within-entity variation for identification
  - Less efficient than RE if RE assumptions hold

Time fixed effects: Y_it = alpha_i + gamma_t + beta * X_it + epsilon_it
  → Also absorbs common shocks affecting all entities in each period
  → Two-way fixed effects (entity + time) is standard practice
```

**Random Effects (RE) — GLS Estimator:**
```
Y_it = beta_0 + beta * X_it + (alpha_i + epsilon_it)

alpha_i treated as random, uncorrelated with X_it
More efficient than FE if assumption holds
Can estimate coefficients on time-invariant variables
```

**Hausman Test — FE vs RE:**
```
H0: alpha_i uncorrelated with X_it (RE is consistent and efficient)
H1: alpha_i correlated with X_it (only FE is consistent)

If p-value < 0.05: Reject H0, use FE
If p-value > 0.05: Fail to reject, RE is preferred (more efficient)

In practice: FE is the default choice in most applied work because
the RE assumption is strong and often implausible
```

**Clustered standard errors:** In panel data, always cluster standard errors at the entity level to account for within-entity correlation of errors over time.

### Instrumental Variables (IV)

**Problem:** Endogeneity — X is correlated with epsilon (due to omitted variables, simultaneity, or measurement error). OLS is biased and inconsistent.

**IV/2SLS approach:**
```
Requirements for a valid instrument Z:
  1. Relevance: Cov(Z, X) ≠ 0 (Z predicts X — testable)
  2. Exclusion restriction: Cov(Z, epsilon) = 0 (Z affects Y only through X — NOT testable)

Two-Stage Least Squares (2SLS):
  Stage 1: X_hat = gamma_0 + gamma_1 * Z + v     (regress X on instrument)
  Stage 2: Y = beta_0 + beta_1 * X_hat + epsilon  (regress Y on predicted X)

Diagnostics:
  - First-stage F-statistic: F > 10 indicates instrument is not weak (Staiger-Stock rule)
  - Overidentification test (Sargan/Hansen J): If more instruments than endogenous variables,
    test whether excluded instruments are uncorrelated with error (if rejected, at least one
    instrument is invalid)
  - Weak instruments: IV estimates are biased toward OLS; use LIML instead of 2SLS
```

**Famous IV examples in economics:**
| Endogenous Variable | Instrument | Paper |
|--------------------|-----------| ------|
| Education → Earnings | Quarter of birth | Angrist & Krueger (1991) |
| Institutions → Growth | Settler mortality | Acemoglu, Johnson, Robinson (2001) |
| Trade → Income | Geographic distance | Frankel & Romer (1999) |
| Police → Crime | Electoral cycles | Levitt (1997) |

### Vector Autoregression (VAR)

**Model:**
```
Y_t = c + A_1 * Y_{t-1} + A_2 * Y_{t-2} + ... + A_p * Y_{t-p} + epsilon_t

Y_t = vector of endogenous variables (e.g., GDP growth, inflation, interest rate)
A_i = coefficient matrices
p   = lag order (selected by information criteria: AIC, BIC, HQ)
epsilon_t = vector of error terms (serially uncorrelated)
```

**VAR toolkit:**
- **Granger causality:** Does X help predict Y beyond Y's own history? F-test on lagged X coefficients in Y equation. Not true causality — just predictive content
- **Impulse response functions (IRFs):** Trace the dynamic response of each variable to a one-standard-deviation shock in another variable. Requires identification (ordering) of shocks
- **Forecast error variance decomposition (FEVD):** What fraction of the forecast error variance of Y is attributable to shocks in X at different horizons?
- **Structural VAR (SVAR):** Imposes economic theory to identify structural shocks. Common identification: Cholesky decomposition (recursive ordering), sign restrictions, long-run restrictions

**Stationarity requirements:**
- VAR requires stationary variables (or cointegrated system → VECM)
- Unit root tests: Augmented Dickey-Fuller (ADF), Phillips-Perron, KPSS
- If variables are I(1) and cointegrated: Use Vector Error Correction Model (VECM) to capture both short-run dynamics and long-run equilibrium

### Difference-in-Differences (DiD)

```
Y_it = beta_0 + beta_1 * Treat_i + beta_2 * Post_t + beta_3 * (Treat_i x Post_t) + epsilon_it

beta_3 = DiD estimator = causal effect of treatment

Key assumption: Parallel trends — absent treatment, treated and control groups
would have followed the same trend

Diagnostics:
  - Pre-treatment trend test: Plot outcomes for treated vs control before treatment
  - Placebo tests: Apply DiD to periods before treatment (should find no effect)
  - Event study specification: Estimate treatment effect at each time period
```

## Methodology

1. **Specification**: Define the economic relationship to estimate. Select dependent and independent variables based on theory
2. **Data assessment**: Check for stationarity, missing values, outliers, and measurement quality
3. **Estimator selection**: Choose OLS, panel FE/RE, IV/2SLS, or VAR based on data structure and endogeneity concerns
4. **Estimation**: Run the model with appropriate standard errors (robust, clustered, Newey-West)
5. **Diagnostics**: Test for heteroskedasticity, autocorrelation, endogeneity, multicollinearity, and specification error
6. **Robustness**: Re-estimate with alternative specifications, subsamples, and controls to check stability of results
7. **Interpretation**: Report coefficients with economic interpretation, statistical significance, and practical significance

## Templates

### Regression Results Table

```
=== REGRESSION RESULTS ===

Dependent variable: __________    N = ____    R-squared = ____

                    (1) OLS      (2) FE       (3) IV/2SLS
Variable 1          ____         ____          ____
                   (SE)         (SE)          (SE)
Variable 2          ____         ____          ____
                   (SE)         (SE)          (SE)
Variable 3          ____         ____          ____
                   (SE)         (SE)          (SE)
Constant            ____         —             ____
                   (SE)                       (SE)

Entity FE           No           Yes           No
Time FE             No           Yes           No
Clustered SEs       No           Entity        No
First-stage F       —            —             ____
Hausman test p      —            ____          —
Observations        ____         ____          ____
R-squared           ____         ____          ____

Standard errors in parentheses. * p<0.10, ** p<0.05, *** p<0.01
```

### Diagnostic Checklist

```
=== ECONOMETRIC DIAGNOSTIC CHECKLIST ===

Model: __________    Estimator: __________

[ ] Heteroskedasticity test (Breusch-Pagan / White):      p = ____
    → If rejected: using robust SEs? [ ] Yes
[ ] Autocorrelation test (Durbin-Watson / Breusch-Godfrey): DW = ____
    → If detected: using Newey-West SEs? [ ] Yes
[ ] Multicollinearity (max VIF):                           VIF = ____
    → If VIF > 10: action taken? ____
[ ] Endogeneity (Hausman test for panel / theory for IV):  p = ____
    → If suspected: IV or FE used? [ ] Yes
[ ] Specification (Ramsey RESET):                          p = ____
    → If rejected: functional form reviewed? [ ] Yes
[ ] Normality of residuals (Jarque-Bera):                  p = ____
    → If rejected and small sample: bootstrap used? [ ] Yes
[ ] Stationarity (ADF test on each variable):              ____
    → If I(1): differenced or cointegration tested? [ ] Yes
```

## Quality Gate

- [ ] Economic theory guides variable selection and functional form
- [ ] Gauss-Markov assumptions assessed and violations addressed
- [ ] Standard errors appropriate for data structure (robust, clustered, HAC)
- [ ] Endogeneity explicitly discussed; IV instruments validated (relevance and exclusion)
- [ ] Panel model choice (FE vs RE) justified by Hausman test and economic reasoning
- [ ] VAR lag order selected by information criteria; stationarity confirmed
- [ ] IRFs reported with confidence bands; identification strategy (ordering) justified
- [ ] Causal claims supported by appropriate identification strategy (IV, DiD, RDD)
- [ ] Robustness checks performed (alternative specifications, subsamples, placebo tests)
- [ ] Results reported with both statistical significance and economic significance
- [ ] Limitations acknowledged (external validity, measurement error, data quality)
