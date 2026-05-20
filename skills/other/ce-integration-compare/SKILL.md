---
name: ce-integration-compare
description: >
  Guide CE integration with SHAP and LIME, compare explanation outputs, and
  configure the calibrated-explanations integration adapters.
---

# CE Integration Compare

You are helping users work with the CE integrations for SHAP and LIME.

## Required references

- `src/calibrated_explanations/integrations/shap.py`
- `src/calibrated_explanations/integrations/lime.py`
- `src/calibrated_explanations/integrations/__init__.py`

## Use this skill when

- A user asks how to use CE with SHAP or LIME.
- Comparing CE explanations with SHAP/LIME outputs.
- Configuring or debugging the integration adapters.
- Understanding the differences between calibrated explanations and
  feature-attribution methods.

## Key concepts

### CE vs. feature attribution methods

Calibrated explanations provide **rule-based explanations with calibrated
uncertainty intervals**. SHAP and LIME provide **feature attribution values**
(importance scores per feature). The approaches are complementary:

- CE rules tell you *which conditions* justify a prediction with calibrated
  confidence.
- SHAP/LIME tell you *how much* each feature contributed to the prediction.

### Integration architecture

The integration modules provide adapter classes that:
1. Wrap a fitted CE explainer to produce SHAP-compatible or LIME-compatible
   outputs.
2. Allow side-by-side comparison of CE rules with feature attributions.
3. Preserve CE calibration semantics while exposing familiar interfaces.

## Workflow

1. **Fit and calibrate a CE pipeline first** (use `ce-pipeline-builder`).
2. **Import the integration adapter**:
   ```python
   from calibrated_explanations.integrations.shap import CESHAPAdapter
   # or
   from calibrated_explanations.integrations.lime import CELIMEAdapter
   ```
3. **Generate comparison explanations** using both CE and the adapter.
4. **Interpret the results**: CE rules for conditions, SHAP/LIME values for
   attribution magnitudes.

## Constraints

- Always fit and calibrate the CE pipeline before using integration adapters.
- Integration adapters are convenience wrappers; the underlying CE explainer
  must be properly configured.
- Do not use integration adapters as replacements for CE explanations; they
  are comparison tools.
