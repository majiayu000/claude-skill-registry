---
name: ce-reject-policy
description: >
  Configure reject and defer decision policies and interpret RejectResult behavior
  in prediction and explanation flows.
---

# CE Reject Policy

You are configuring reject / defer logic for production decision pipelines.
Reject policies let the framework flag, skip, or selectively process
instances where the model's prediction is ambiguous, novel, or uncertain —
all without modifying the underlying model.

**ADR reference**: ADR-029 (Reject Integration Strategy).

Load `references/reject_policy_examples.md` for full code examples.

---

## The four policies

```python
from calibrated_explanations.core.reject.policy import RejectPolicy
```

| Policy | Behaviour |
|---|---|
| `RejectPolicy.NONE` (default) | No reject logic. Returns the same type as without any policy. |
| `RejectPolicy.FLAG` | Process ALL instances. Annotate rejected ones in `RejectResult.rejected`. |
| `RejectPolicy.ONLY_REJECTED` | Process and return **only** rejected instances. |
| `RejectPolicy.ONLY_ACCEPTED` | Process and return **only** accepted (non-rejected) instances. |

**Legacy policy strings** (deprecated, emit `DeprecationWarning`):

| Old name | Maps to |
|---|---|
| `"predict_and_flag"` / `"explain_all"` | `FLAG` |
| `"explain_rejects"` | `ONLY_REJECTED` |
| `"explain_non_rejects"` / `"skip_on_reject"` | `ONLY_ACCEPTED` |

Use the enum members directly, not string values, to avoid deprecation warnings.

---

## RejectResult envelope

When any non-`NONE` policy is active, the return type changes to a `RejectResult`:

```python
from calibrated_explanations.explanations.reject import RejectResult

result.prediction   # calibrated predictions (array or None if policy skips them)
result.explanation  # CalibratedExplanations or None
result.rejected     # boolean mask: True = rejected, False = accepted
result.policy       # RejectPolicy member that generated this result
result.metadata     # dict with telemetry: error_rate, reject_rate, etc.
```

---

## Policy selection guide

| When to use | Policy |
|---|---|
| Audit mode: flag all uncertain, explain everything | `FLAG` |
| Focus investigation on uncertain instances | `ONLY_REJECTED` |
| Production only-confident mode (skip uncertain) | `ONLY_ACCEPTED` |
| Legacy behavior / benchmarking | `NONE` |

---

## Out of Scope

- Mondrian group calibration (see `ce-mondrian-conditional`).
- Calibrated predictions without reject logic (see `ce-calibrated-predict`).
- Guarded factual explanations (`explain_guarded_factual` — legacy interface,
  use `explain_factual` + reject policy instead).

## Evaluation Checklist

- [ ] `RejectPolicy` enum member used (not deprecated string value).
- [ ] Return type checked: `RejectResult` when policy != `NONE`, plain type otherwise.
- [ ] `result.rejected` mask inspected for actual rejection counts.
- [ ] Initialization failure path tested (`metadata["init_error"]`).
- [ ] Per-call override tested alongside explainer-level default.
- [ ] Regression: `initialize_reject_learner(threshold=t)` called before `predict_reject`.
- [ ] Tests use `pytest.warns(UserWarning)` when fallback warning is expected.
