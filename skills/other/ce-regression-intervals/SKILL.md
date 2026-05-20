---
name: ce-regression-intervals
description: >
  Configure and interpret CE regression intervals for percentile conformal and
  thresholded probabilistic modes.
---

# CE Regression Intervals

You are configuring or interpreting regression intervals in CE. This skill
covers the three distinct regression modes defined in ADR-021. A fully
fit + calibrated `WrapCalibratedExplainer` (regression model) is required.

Load `references/difficulty_estimator_guide.md` for per-instance adaptive
intervals using `DifficultyEstimator`.

## Three Modes — Decision Tree

```
Is threshold= provided?
├── NO  -> Mode 2: Percentile conformal intervals (CPS)
│         Use low_high_percentiles=(low%, high%)
│         Result: interval is a percentile band (e.g., 5th-95th percentile)
│
└── YES -> Mode 3: Thresholded probabilistic regression (CPS + Venn-Abers)
          Result: calibrated P(y <= threshold) with probability interval
          Interval semantics = probability mass (NOT a percentile band)
```

Mode 1 (classification) is handled by `ce-pipeline-builder` and `ce-factual-explain`.

---

## Mode 2: Percentile Conformal Intervals

**Use when:** you want a confidence band around the regression prediction.

```python
explanations = explainer.explain_factual(X_query)                              # default 5th-95th, 90% condfidence
explanations = explainer.explain_factual(X_query, low_high_percentiles=(10, 90))  # tighter, 80% confidence
explanations = explainer.explain_factual(X_query, low_high_percentiles=(-np.Inf, 90))  # upper bounded, 90% condfidence
explanations = explainer.explain_factual(X_query, low_high_percentiles=(10, np.Inf))  # lower bounded, 90% condfidence
```

**How to read the output:**
```python
exp = explanations[0]
median = exp.prediction['predict']    # point estimate (CPS median)
low    = exp.prediction['low']        # e.g., 5th percentile
high   = exp.prediction['high']       # e.g., 95th percentile
# Invariant (ADR-021 §4): low <= median <= high
```

---

## Mode 3: Thresholded Probabilistic Regression

**Use when:** you want the calibrated probability that the output exceeds a threshold.

```python
explanations = explainer.explain_factual(X_query, threshold=50.0)              # scalar
explanations = explainer.explain_factual(X_query, threshold=(40.0, 60.0))      # two-sided
```

**Key difference from Mode 2:**
- The `predict` value is a **probability** (0-1), not a value in y-space.
- The interval bounds are probability bounds, not regression value bounds.
- Do NOT mix `low_high_percentiles` and `threshold` in the same call.

---

## Calibration Engine (Context — ADR-021)

| Mode | Engine | What is calibrated |
|---|---|---|
| Classification | Venn-Abers only | P(class=k) with interval |
| Regression (percentile) | CPS only | Percentile bands |
| Regression (threshold) | CPS -> Venn-Abers | P(y <= t) with interval |

---

## Choosing Interval Width

| Goal | Setting |
|---|---|
| Standard 90% interval | `low_high_percentiles=(5, 95)` (default) |
| Tighter 80% interval | `low_high_percentiles=(10, 90)` |
| Tight 50% IQR | `low_high_percentiles=(25, 75)` |
| Wider 98% interval | `low_high_percentiles=(1, 99)` |

---

## Alternatives in Regression

```python
alternatives = explainer.explore_alternatives(X_query, threshold=50.0)
alternatives = explainer.explore_alternatives(X_query, low_high_percentiles=(10, 90))
```

---

## Out of Scope

- Classification interval semantics (see `ce-factual-explain`).
- Building the pipeline (see `ce-pipeline-builder`).
- Persisting the calibrated regression model (see `ce-serializer-impl`).

## Evaluation Checklist

- [ ] Mode correctly identified (percentile vs threshold).
- [ ] `low_high_percentiles` and `threshold` not used simultaneously.
- [ ] Interval invariant `low <= predict <= high` verified.
- [ ] Correct semantic interpretation of `predict` stated (probability vs y-value).
- [ ] Calibration set size and expected interval width proportional.
- [ ] If DifficultyEstimator used: estimator is `fitted=True` before assignment.
- [ ] If DifficultyEstimator used: interval widths vary per instance (not uniform).
- [ ] `set_difficulty_estimator(None)` tested if removal path is needed.
