---
name: ce-classification
description: >
  Handle CE classification workflows for binary and multiclass prediction semantics
  and class-focused explanation behavior.
---

# CE Classification

You are working with a classification task (binary or multiclass). CE provides
calibrated probability bounds $[p_{low}, p_{high}]$ using Venn-Abers
calibration.

## Prediction Semantics (Venn-Abers)

The `predict` and `predict_proba` methods return calibrated class assignments
and probabilities.

- **Binary**: Rules and probabilities always refer to the **positive class**
  (index 1).
- **Multiclass**:
  - `predict()`: Returns the class label with the highest calibrated probability.
  - `predict_proba()`: Returns a full probability distribution (summing to 1).
- **Intervals**: For any class probability $p$, the calibrated interval $[p_{low}, p_{high}]$
  guarantees that $p_{low} \le p \le p_{high}$ (ADR-021 invariant).

```python
# Multiclass: explain the PREDICTED class (default)
# If the model predicts 'Class 2', rules explain 'Why Class 2?'
explanations = explainer.explain_factual(X_test)
```

## Explaining All Classes (`multi_labels_enabled`)

By default, CE explains the **predicted class**. To explain **all classes**
(e.g., for contrastive analysis or true multi-label tasks), use
`multi_labels_enabled=True`.

```python
# Returns a MultiClassCalibratedExplanations object
multi_explanations = explainer.explain_factual(
    X_test,
    multi_labels_enabled=True
)
```

### `MultiClassCalibratedExplanations` API

This object stores a mapping of `{class_index: Explanation}` for each instance.

```python
# 1. Access instance i (returns a specialized multi-class view for instance i)
inst_exps = multi_explanations[i]

# 2. Access a specific class explanation for instance i
# Returns a standard FactualExplanation or AlternativeExplanation
class_1_exp = multi_explanations[i, 1]

# 3. Plotting
# Plots all class explanations for the instance
multi_explanations[i].plot()
```

## Task-Specific Config

When fitting the explainer, CE automatically detects binary vs multiclass based
on `y_proper`. Use `explainer.class_labels` to check the detected labels.

```python
explainer = WrapCalibratedExplainer(model)
explainer.fit(x_p, y_p)
explainer.calibrate(x_c, y_c)

print(f"Task: {explainer.task}")             # 'classification'
print(f"Labels: {explainer.class_labels}")   # e.g., ['Setosa', 'Versicolor', 'Virginica']
```

---

## Contributor & Agent Checklist

1. [ ] **Binary index** — remember that binary classification in CE is always
   relative to `class 1`.
2. [ ] **Multi-label type** — use `multi_labels_enabled=True` (plural `labels`)
   to trigger the multiclass explanation logic.
3. [ ] **Invariant check** — verify `low <= predict <= high` for any class
   probability being inspected.
4. [ ] **Labels in titles** — when plotting multiclass, ensure class labels (not
   just indices) are used if available in `explainer.class_labels`.
