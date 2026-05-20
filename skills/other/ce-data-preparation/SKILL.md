---
name: ce-data-preparation
description: >
  Validate and preprocess input data for CE pipelines, handle mixed types and
  categorical features, and configure encoding per ADR-002 and ADR-009.
---

# CE Data Preparation

You are helping users prepare their data for use with calibrated-explanations.

## Required references

- `docs/improvement/adrs/ADR-002-validation-and-exception-design.md`
- `docs/improvement/adrs/ADR-009-input-preprocessing-and-mapping-policy.md`
- `src/calibrated_explanations/core/validation.py`
- `src/calibrated_explanations/preprocessing/builtin_encoder.py`

## Use this skill when

- A user's data has mixed types, NaN values, or categorical features.
- CE raises input validation errors.
- Configuring automatic encoding (`auto_encode='auto'`).
- Understanding how CE handles feature preprocessing.
- Exporting or importing preprocessing mappings.

## Common scenarios

### 1. Categorical features

CE requires numeric input by default. For categorical features:

```python
explainer = WrapCalibratedExplainer(model, auto_encode='auto')
explainer.fit(X_train, y_train)  # auto-encoding activates here
```

- `auto_encode='auto'`: CE's built-in encoder handles categorical columns
  deterministically.
- Custom preprocessor: Pass your own sklearn transformer via the
  `preprocessor` parameter.

### 2. Mixed types (DataFrame input)

When passing a DataFrame with mixed dtypes:
- Numeric columns pass through unchanged.
- Non-numeric columns require `auto_encode='auto'` or a custom preprocessor.
- Without preprocessing, CE raises a `ValidationError` with actionable
  guidance listing the offending columns.

### 3. Missing values (NaN)

CE does not impute missing values by default:
- Preprocess NaN values before passing to CE.
- The built-in encoder does not handle NaN; use a custom preprocessor
  with imputation if needed.

### 4. Unseen categories at inference

Per ADR-009, the `unseen_category_policy` controls behavior:
- `"error"` (default): Raises `ValidationError` on unseen categories.
- `"ignore"`: Maps unseen categories to a sentinel output with a warning.

### 5. Mapping export/import

After fitting, you can export and import preprocessing mappings:

```python
mapping = explainer.export_mapping()  # JSON-safe dict
# ... save to file or transfer ...
explainer.import_mapping(mapping)     # restore on another instance
```

## Validation error diagnostics

When CE raises input errors, check:
1. **Column types**: Are all columns numeric? If not, enable `auto_encode`.
2. **Shape**: Does `X` have the same number of features as training data?
3. **NaN/Inf**: Are there missing or infinite values?
4. **Unseen categories**: Are there categories in test data not seen during fit?

## Constraints

- Always fit and calibrate before explaining (CE-first invariant).
- The built-in encoder is deterministic given the same `stable_seed`.
- Mapping export produces JSON-safe primitives only; no opaque blobs.
- Preprocessing does not change calibration semantics.
