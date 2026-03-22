---
name: ce-pipeline-builder
description: >
  Build CE-first end-to-end pipelines using WrapCalibratedExplainer with fit,
  calibrate, and explain or predict sequencing.
---

# CE Pipeline Builder

You are implementing a CE-first pipeline. Load `references/ce-first-policy.md`
for the full policy text. Non-negotiable invariants are repeated inline below
for quick reference.

## Mandatory CE-First Checklist (enforce in order)

1. **Library check** — if `calibrated_explanations` is not importable, fail fast:
   ```python
   pip install calibrated-explanations
   ```
2. **Wrapper** — always use `WrapCalibratedExplainer`. Never invent a new wrapper
   class; never use `CalibratedExplainer` directly in user-facing code.
3. **Fit** — `explainer.fit(x_proper, y_proper)`.
   Assert `explainer.fitted is True` before proceeding.
4. **Calibrate** — `explainer.calibrate(x_cal, y_cal)`.
   Assert `explainer.calibrated is True` before proceeding.
5. **Explain (standard)** — `explainer.explain_factual(X)` or
   `explainer.explore_alternatives(X)`.
6. **Explain (guarded / in-distribution)** — when higher security or
   in-distribution filtering is needed, use `explainer.explain_guarded_factual(X)`
   or `explainer.explore_guarded_alternatives(X)` instead of the standard paths.
   Also use when rule conditions of the form `x < feature <= y` are needed, since
   the guarded APIs support this natively.
7. **Conjunctions** — `explanations.add_conjunctions(...)` or
   `explanations[idx].add_conjunctions(...)`.
8. **Narratives & plots** — `.to_narrative(output_format=...)` and `.plot(...)`.
9. **Calibrated by default** — never return uncalibrated outputs unless
   the user has explicitly requested them.

## Minimal Working Skeleton

Adapt the task type (binary / multiclass / regression) based on the user's
data and model. Choose from the three templates below:

### Binary classification

```python
from __future__ import annotations
import numpy as np
from calibrated_explanations import WrapCalibratedExplainer

# --- Data split ---------------------------------------------------------
# x_proper, y_proper : proper training set (used for model training)
# x_cal, y_cal       : calibration set    (must NOT overlap with x_proper)
# X_query            : instances to explain

# --- Build pipeline -----------------------------------------------------
explainer = WrapCalibratedExplainer(model)           # model: any sklearn-compat
explainer.fit(x_proper, y_proper)
assert explainer.fitted is True

explainer.calibrate(x_cal, y_cal)
assert explainer.calibrated is True

# --- Explain ------------------------------------------------------------
explanations = explainer.explain_factual(X_query)
# Optional: add feature conjunctions
explanations.add_conjunctions(max_rule_size=3)
# Optional: narrative
print(explanations[0].to_narrative())
# Optional: plot
explanations[0].plot()
```

### Multiclass classification

Same scaffold as binary. The `explain_factual` call returns one explanation
object per query instance, with per-class calibrated probabilities available in
`explanations[i].prediction["__full_probabilities__"]`.

### Regression (percentile intervals)

```python
explainer = WrapCalibratedExplainer(reg_model)
explainer.fit(x_proper, y_proper)
assert explainer.fitted is True

explainer.calibrate(x_cal, y_cal)
assert explainer.calibrated is True

# low_high_percentiles controls the conformal interval width (ADR-021)
explanations = explainer.explain_factual(X_query, low_high_percentiles=(10, 90))
```

### Regression (thresholded / probabilistic)

```python
# threshold= activates the CPS + Venn-Abers path (ADR-021 §3)
explanations = explainer.explain_factual(X_query, threshold=my_threshold)
```

## Using `ce_agent_utils` helpers

Prefer the validated helpers from `src/calibrated_explanations/ce_agent_utils.py`
for end-to-end pipelines in agent code:

```python
from calibrated_explanations.ce_agent_utils import (
    ensure_ce_first_wrapper,
    fit_and_calibrate,
    explain_and_narrate,
    wrap_and_explain,
)

# Full pipeline in one call:
explanations = wrap_and_explain(
    model, x_proper, y_proper, x_cal, y_cal, X_query
)
```

## Decision: `explain_factual` vs `explain_guarded_factual`

| Use case | API to use |
|---|---|
| Standard inference | `explain_factual` / `explore_alternatives` |
| Production / unknown input distribution | `explain_guarded_factual` / `explore_guarded_alternatives` |
| Explicit in-distribution filtering required | `explain_guarded_factual` |

Guarded variants apply ADR-032 semantics — see `references/adr-032-guarded-semantics.md`.

## Data Split Rules

- `x_proper` / `y_proper` and `x_cal` / `y_cal` must **not** overlap.
- Typical split: 60% proper training, 20% calibration, 20% test. Adjust based on
  calibration data needs (larger calibration → tighter intervals).
- Never reuse training data for calibration.

## Out of Scope

This skill does NOT:
- Train or tune the underlying model (use your usual scikit-learn workflow).
- Generate plots or visualizations beyond `.plot()` invocation (see `ce-plotspec-author`).
- Cover the serialization / persistence of calibrators (see `ce-serializer-impl`).
- Add new plugins or modify `core/` (see `ce-plugin-scaffold`).

## Evaluation Checklist (self-verify before returning)

- [ ] `WrapCalibratedExplainer` used (not raw `CalibratedExplainer`).
- [ ] `fit()` called with proper training data.
- [ ] `calibrate()` called with separate calibration data.
- [ ] Both `.fitted is True` and `.calibrated is True` asserted.
- [ ] `explain_factual` or `explore_alternatives` (or guarded variants) called.
- [ ] No uncalibrated output returned unless explicitly requested.
- [ ] Skeleton is runnable with the user's model and data shapes.
