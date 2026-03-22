---
name: ce-factual-explain
description: >
  Generate factual CE explanations and select the correct guarded versus standard
  factual workflow.
---

# CE Factual Explain

You are producing factual calibrated explanations  rules that explain *why*
the current prediction is what it is.

The CE-First pipeline (fit  calibrate) is a prerequisite. If not in place,
invoke `ce-pipeline-builder` first.

For all post-generation interaction (plot, narrative, `add_conjunctions`,
`filter_rule_sizes`, `filter_features`) see `ce-explain-interact`.

---

## Two Entry Points

### Standard path
```python
explanations = explainer.explain_factual(X_query)
```

### Explaining all classes (multiclass)
```python
# Returns a MultiClassCalibratedExplanations for all class labels
multi_exps = explainer.explain_factual(X_query, multi_labels_enabled=True)
```

### Guarded path (production / unknown input distribution)
```python
explanations = explainer.explain_guarded_factual(X_query)
```

See `references/adr-032-guarded-semantics.md` for the full guarded semantics.
Use the guarded variant when:
- Processing user-submitted data with unknown distribution.
- Building API endpoints that accept arbitrary inputs.
- Calibration set coverage is limited.

---

## When to Use Standard vs Guarded

| Scenario | API |
|---|---|
| Training / development / research | `explain_factual` |
| Production endpoint | `explain_guarded_factual` |
| Unknown input distribution | `explain_guarded_factual` |
| Limited calibration set | `explain_guarded_factual` |

---

## Output Type: `FactualExplanation`

```
CalibratedExplanations        (collection)
   [i]  FactualExplanation  (per-instance)
```

Access the i-th instance: `explanations[i]`

---

## Prediction Dict Structure

```python
exp = explanations[i]
pred = exp.prediction

pred['predict']    # point prediction (probability for classification, y or P(yt) for regression)
pred['low']        # lower bound of calibrated interval
pred['high']       # upper bound of calibrated interval

# Classification only:
pred.get('__full_probabilities__')   # all-class probability cube (Venn-Abers)
```

**Interval invariant (ADR-021 §4  must always hold):**
```python
assert pred['low'] <= pred['predict'] <= pred['high']
```

---

## Factual-Specific Rule Access

```python
exp = explanations[i]

# All atomic rules as a list of normalised dicts
rules_list = exp.list_rules()

# Rules for a specific feature
rules_for_age = exp.get_rules_by_feature("age")

# Raw rule payload (dict with 'rule', 'value', 'feature', 'weight', etc.)
rules_dict = exp.get_rules()
```

---

## Factual Conjunctions (Quick Reference)

The primary parameter is `max_rule_size`; `n_top_features` limits the search
space (optional speed control):

```python
explanations[i].add_conjunctions(max_rule_size=2)          # pairs (default)
explanations[i].add_conjunctions(max_rule_size=3)          # triples
explanations[i].add_conjunctions(max_rule_size=2, n_top_features=5)  # limit search
```

For the full conjunction + filtering API, see `ce-explain-interact`.

---

## Factual Plot (Quick Reference)

Factual explanations default to `rnk_metric="feature_weight"` and `style="regular"`:

```python
explanations[i].plot(filter_top=10)
explanations[i].plot(filter_top=5, uncertainty=True)   # show uncertainty bands
```

- Supported styles for `FactualExplanation`: `'regular'` only.
- Default `rnk_metric` for factuals: `"feature_weight"` (differs from alternatives default `"ensured"`).

For the full plot API, see `ce-explain-interact`.

---

## Factual Narrative (Quick Reference)

```python
text = explanations[i].to_narrative(
    expertise_level="beginner",   # or "advanced" or ("beginner", "advanced")
    output_format="text",
)
```

For the full narrative API including `template_path`, `output_format`, and
`conjunction_separator`, see `ce-explain-interact`.

---

## Guarded Audit API

When using `explain_guarded_factual`, a dedicated audit is available:

```python
audit = explanations.get_guarded_audit()
# {
#   "intervals_removed_guard": int,   # rules removed because conforming == False
#   "interval_records": [...],        # per-rule details
# }
```

---

## Out of Scope

- Exploring counterfactual / alternative predictions (see `ce-alternatives-explore`).
- Regression interval configuration (`threshold=` / `low_high_percentiles=`) (see `ce-regression-intervals`).
- Generic plot / narrative / filter API (see `ce-explain-interact`).
- Building the pipeline (see `ce-pipeline-builder`).

## Evaluation Checklist

- [ ] Correct entry point chosen (`explain_factual` vs `explain_guarded_factual`).
- [ ] Interval invariant `low  predict  high` verified for at least one output.
- [ ] `list_rules()` / `get_rules_by_feature()` used for rule introspection (not raw dict keys).
- [ ] Guarded audit called if `explain_guarded_factual` was used.
- [ ] No uncalibrated output returned.
