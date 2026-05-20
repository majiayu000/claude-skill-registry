---
name: ce-mondrian-conditional
description: >
  Configure and validate Mondrian and conditional calibration for subgroup-aware
  uncertainty and fairness-sensitive workflows.
---

# CE Mondrian Conditional

You are setting up Mondrian (conditional) calibration, which partitions
calibration data into subgroups so that each group receives its own
uncertainty estimate. This reveals group-specific prediction quality and is
the foundational technique for fairness-aware deployments in CE.

**Research**: [Conditional Calibrated Explanations (xAI 2024)](https://link.springer.com/chapter/10.1007/978-3-031-63787-2_17)

Load `references/mondrian_examples.md` for full code examples (Options A/B/C,
fairness analysis, global vs conditional comparison).

---

## Why Mondrian matters for fairness

Without conditional calibration, the CPS/Venn-Abers calibrator averages over
all calibration instances. A minority group with harder prediction patterns
may receive the same interval width as an easy majority group, hiding bias.

Mondrian splits calibration by a grouping key and fits a separate calibrator
per bin. Resulting intervals are:
- **Narrower** for groups the model predicts reliably.
- **Wider** for groups the model predicts poorly.

---

## Three options for specifying bins

- **Option A — Inline `bins` array**: pass integer group labels directly at calibrate time.
- **Option B — `MondrianCategorizer`** (recommended for continuous features): auto-bins
  via `crepes.extras.MondrianCategorizer`.
- **Option C — Lambda as `mc`**: pass a callable directly for ad-hoc one-off scripts.

---

## Calibration -> predict -> explain consistency rules

| Step | Bins argument |
|---|---|
| `calibrate(...)` | `mc=` (MondrianCategorizer or callable) OR `bins=` (integer array) |
| `predict(x, ...)` | nothing if `mc` was used at calibrate time OR `bins=group_labels_test` |
| `predict_proba(x, ...)` | same as above |
| `explain_factual(x, ...)` | same as above |
| `explore_alternatives(x, ...)` | same as above |

**CRITICAL**: always pass `bins=` at inference time whenever the explainer
was calibrated with Mondrian bins. Omitting it silently falls back to global
calibration, which defeats fairness analysis.

---

## Minimum bin size warning

Mondrian calibration splits the calibration set by group. Too few samples
per bin leads to unreliable or very wide intervals.

> **Rule of thumb**: aim for >= 30-50 calibration samples per bin.

---

## Out of Scope

- DifficultyEstimator (per-instance sigma scaling for regression; see `ce-regression-intervals`).
- Reject policies (deciding whether to defer uncertain predictions; see `ce-reject-policy`).
- Fairness constraint enforcement (CE reveals uncertainty; it does not enforce fairness automatically).

## Evaluation Checklist

- [ ] Group labels at explain/predict time match the label space used at calibrate time.
- [ ] Minimum bin size verified (>= 30 samples per bin recommended).
- [ ] Both `calibrate(mc=...)` and `explain_factual(bins=...)` consistently use the same categorizer.
- [ ] If comparing global vs Mondrian: separate `WrapCalibratedExplainer` instances used.
- [ ] Per-group interval widths inspected to surface differential uncertainty.
- [ ] Coverage rate verified per group (not just pooled).
