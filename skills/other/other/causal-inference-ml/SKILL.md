---
name: causal-inference-ml
description: Apply causal inference methods for treatment effect estimation and uplift modeling
---

# Causal Inference for ML

## Method Selection Decision Table

| Scenario | Key Assumption | Method | Library |
|----------|----------------|--------|---------|
| RCT / A/B test | Randomization | Difference-in-means | scipy |
| Observational, known confounders | Unconfoundedness | T/S/X-Learner, CausalForestDML | EconML |
| Observational, high-dim confounders | Unconfoundedness + sparsity | DML (Double ML) | EconML |
| Selection on observables | Strong ignorability | IPW / Hajek estimator | DoWhy |
| Unobserved confounders, instrument exists | Valid instrument | IV / 2SLS / DMLIV | EconML |
| Pre/post with control group | Parallel trends | Difference-in-Differences | statsmodels |
| Full causal graph validation | Graph structure known | DoWhy (identify, estimate, refute) | DoWhy |
| Targeting / personalization | Unconfoundedness | Uplift modeling + Qini curves | EconML |

## DoWhy Pipeline

```python
from dowhy import CausalModel

def run_dowhy_pipeline(df, treatment, outcome, confounders,
                       instruments=None, effect_modifiers=None):
    """Full DoWhy pipeline: model, identify, estimate, refute."""
    model = CausalModel(
        data=df, treatment=treatment, outcome=outcome,
        common_causes=confounders, instruments=instruments,
        effect_modifiers=effect_modifiers,
    )
    # Identify estimand (backdoor, frontdoor, or IV)
    estimand = model.identify_effect(proceed_when_unidentifiable=True)

    # Estimate effect via T-Learner backend
    estimate = model.estimate_effect(
        estimand,
        method_name="backdoor.econml.metalearner_tlearner",
        method_params={"init_params": {"models": "GradientBoostingRegressor()"}},
    )

    # Refutation tests (critical -- skip at your peril)
    refutations = {}
    refutations["random_cause"] = model.refute_estimate(
        estimand, estimate, method_name="random_common_cause",
    )
    refutations["placebo"] = model.refute_estimate(
        estimand, estimate,
        method_name="placebo_treatment_refuter", placebo_type="permute",
    )
    refutations["subset"] = model.refute_estimate(
        estimand, estimate,
        method_name="data_subset_refuter", subset_fraction=0.8, num_simulations=5,
    )
    return estimate, refutations
```

## EconML Meta-Learners

### T-Learner, S-Learner, X-Learner

```python
from econml.metalearners import TLearner, SLearner, XLearner
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

def compare_metalearners(X, T, Y):
    """Compare three meta-learner approaches for CATE estimation."""
    models = {
        # T-Learner: separate models per treatment group (heterogeneous effects)
        "T": TLearner(models=GradientBoostingRegressor(n_estimators=200)),
        # S-Learner: single model, treatment as feature (small effects)
        "S": SLearner(overall_model=GradientBoostingRegressor(n_estimators=200)),
        # X-Learner: cross-estimates (imbalanced treatment/control)
        "X": XLearner(
            models=GradientBoostingRegressor(n_estimators=200),
            propensity_model=GradientBoostingRegressor(n_estimators=100),
        ),
    }
    results = {}
    for name, model in models.items():
        model.fit(Y, T, X=X)
        cate = model.effect(X)
        results[name] = {"ate": np.mean(cate), "cate_std": np.std(cate), "cate": cate}
    return results
```

### CausalForestDML

```python
from econml.dml import CausalForestDML
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier

def fit_causal_forest(X, T, Y, W):
    """Doubly-robust CATE with CIs. X: effect modifiers, W: confounders."""
    est = CausalForestDML(
        model_y=GradientBoostingRegressor(n_estimators=200),
        model_t=GradientBoostingClassifier(n_estimators=200),
        n_estimators=500, min_samples_leaf=5, cv=5, random_state=42,
    )
    est.fit(Y, T, X=X, W=W)
    cate = est.effect(X)
    lb, ub = est.effect_interval(X, alpha=0.05)  # 95% CI
    ate_inf = est.ate_inference(X=X)
    print(f"ATE: {ate_inf.point_estimate:.4f} "
          f"[{ate_inf.conf_int()[0]:.4f}, {ate_inf.conf_int()[1]:.4f}]")
    return est, cate, lb, ub, est.feature_importances_
```

## Propensity Scoring with IPW

```python
from sklearn.linear_model import LogisticRegression
import numpy as np

def ipw_ate(X, T, Y, estimator="hajek"):
    """Inverse Probability Weighting with Hajek stabilization."""
    ps_model = LogisticRegression(max_iter=1000, C=0.1)
    ps_model.fit(X, T)
    e = np.clip(ps_model.predict_proba(X)[:, 1], 0.01, 0.99)  # clip extremes

    if estimator == "horvitz_thompson":
        ate = np.mean(T * Y / e) - np.mean((1 - T) * Y / (1 - e))
    elif estimator == "hajek":
        # Normalized weights: lower variance than HT
        w1, w0 = T / e, (1 - T) / (1 - e)
        ate = np.sum(w1 * Y) / np.sum(w1) - np.sum(w0 * Y) / np.sum(w0)
    return ate, e
```

## Instrumental Variables with DMLIV

```python
from econml.iv.dml import DMLIV
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

def fit_dmliv(Y, T, Z, X, W):
    """DMLIV: Double ML + IV. Z: instrument, T: endogenous treatment."""
    est = DMLIV(
        model_y_xw=RandomForestRegressor(n_estimators=200),
        model_t_xw=RandomForestClassifier(n_estimators=200),
        model_t_xwz=RandomForestClassifier(n_estimators=200),
        model_final=RandomForestRegressor(n_estimators=100), cv=3,
    )
    est.fit(Y, T, Z=Z, X=X, W=W)
    return est, est.effect(X)
```

## Difference-in-Differences

```python
import statsmodels.formula.api as smf

def diff_in_diff(df, time_col, treat_col, outcome_col, pre_periods, post_periods):
    """DiD with parallel trends pre-test."""
    # Parallel trends test in pre-period
    pre_df = df[df[time_col].isin(pre_periods)].copy()
    pre_df["time_numeric"] = pre_df[time_col].rank(method="dense")
    trend_fit = smf.ols(
        f"{outcome_col} ~ {treat_col} * time_numeric", data=pre_df
    ).fit()
    interaction_pval = trend_fit.pvalues[f"{treat_col}:time_numeric"]
    if interaction_pval < 0.05:
        print(f"WARNING: Parallel trends violated (p={interaction_pval:.4f})")

    # DiD estimation with robust SEs
    df = df.copy()
    df["post"] = df[time_col].isin(post_periods).astype(int)
    did_fit = smf.ols(f"{outcome_col} ~ {treat_col} * post", data=df).fit(cov_type="HC1")
    att = did_fit.params[f"{treat_col}:post"]
    print(f"ATT: {att:.4f} (SE: {did_fit.bse[f'{treat_col}:post']:.4f})")
    return did_fit, att, interaction_pval
```

## Uplift Modeling with Qini Curves

```python
from econml.metalearners import TLearner
from sklearn.ensemble import GradientBoostingRegressor
import numpy as np

def uplift_with_qini(X_train, T_train, Y_train, X_test, T_test, Y_test):
    """Train uplift model and evaluate with Qini curve."""
    model = TLearner(models=GradientBoostingRegressor(n_estimators=200))
    model.fit(Y_train, T_train, X=X_train)
    scores = model.effect(X_test).flatten()

    # Compute Qini curve: cumulative incremental gain ranked by uplift
    order = np.argsort(-scores)
    n = len(order)
    cum_uplift = []
    for k in range(1, n + 1):
        idx = order[:k]
        t_mask, c_mask = T_test[idx] == 1, T_test[idx] == 0
        if t_mask.sum() == 0 or c_mask.sum() == 0:
            cum_uplift.append(0)
            continue
        gain = Y_test[idx][t_mask].sum() - (
            Y_test[idx][c_mask].sum() * t_mask.sum() / c_mask.sum())
        cum_uplift.append(gain)

    qini_coeff = np.trapz(cum_uplift, dx=1.0 / n) - cum_uplift[-1] / 2
    return scores, cum_uplift, qini_coeff
```

## Gotchas

- **Propensity score overlap**: Scores near 0 or 1 cause exploding IPW weights. Always check overlap histograms and clip (0.01-0.99 minimum)
- **DoWhy refutations are not optional**: An estimate without refutation is meaningless. Random common cause and placebo tests catch specification errors
- **T-Learner bias**: Imbalanced treatment groups cause overfitting on the smaller group. Use X-Learner or CausalForestDML instead
- **DiD parallel trends**: Non-significant pre-trend test does not prove parallel trends -- it only fails to reject. Use multiple pre-periods and visual inspection
- **IV strength**: Weak instruments (first-stage F-stat < 10) cause severe bias. Always report first-stage F-statistic
- **CATE vs ATE**: Averaging CATE gives ATE only under correct specification. Report both with confidence intervals
- **Cross-fitting matters**: DML methods use cross-fitting to avoid overfitting bias. Fewer than 3 folds introduces regularization bias
