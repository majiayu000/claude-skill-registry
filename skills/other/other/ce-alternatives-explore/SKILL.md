---
name: ce-alternatives-explore
description: >
  Generate and interpret CE alternative and counterfactual explanations, including
  ensured filters and alternatives-specific plot workflows.
---

# CE Alternatives Explorer

You are producing alternative calibrated explanations — counterfactual rules
that show what feature changes would produce a different prediction.

The CE-First pipeline (fit + calibrate) is a prerequisite. If not in place,
invoke `ce-pipeline-builder` first.

For all post-generation interaction (plot, narrative, `add_conjunctions`,
`filter_rule_sizes`, `filter_features`) see `ce-explain-interact`.

Load `references/alternatives_api_reference.md` for the ensured framework,
plot styles, ranking controls, and conjunction API.

---

## Two Entry Points

### Standard path
```python
alternatives = explainer.explore_alternatives(X_query)
```

### Explaining all classes (multiclass)
```python
multi_alts = explainer.explore_alternatives(X_query, multi_labels_enabled=True)
```

### Guarded path (production / unknown distributions — ADR-032)
```python
alternatives = explainer.explore_guarded_alternatives(X_query)
```

Guarded variant: out-of-distribution instances are flagged rather than silently
included. Use in production or when the input distribution is unknown.

---

## Threshold Semantics

For **classification** — change the decision boundary:
```python
alternatives = explainer.explore_alternatives(X_query, threshold=0.7)
```

For **regression** — see `ce-regression-intervals` for full semantics:
```python
alternatives = explainer.explore_alternatives(X_query, threshold=50.0)
alternatives = explainer.explore_alternatives(X_query, threshold=(40.0, 60.0))
```

---

## Output Types

```
AlternativeExplanations      (collection — returned by explore_alternatives)
   [i] -> AlternativeExplanation  (per-instance)
```

The prediction dict structure and interval invariant are identical to factual
explanations (`pred['low'] <= pred['predict'] <= pred['high']`), but the
*direction* of the rules is counterfactual (opposing, not supporting).

---

## Out of Scope

- Factual / supporting rule generation (see `ce-factual-explain`).
- Regression interval configuration (see `ce-regression-intervals`).
- Generic plot / narrative / filter API (see `ce-explain-interact`).
- Building the pipeline (see `ce-pipeline-builder`).

## Evaluation Checklist

- [ ] Correct variant (`explore_alternatives` vs `explore_guarded_alternatives`).
- [ ] Threshold provided if the user wants boundary-crossing alternatives for regression.
- [ ] Ensured-framework filter selected appropriately for the use case.
- [ ] `only_ensured=True` used when narrower-uncertainty alternatives are required.
- [ ] `include_potential` set to `True`/`False` per user intent.
- [ ] Plot style is `"triangular"` or `"ensured"` (not `"regular"`) when showing alternatives in a confidence-uncertainty view.
- [ ] `rnk_metric="ensured"` with appropriate `rnk_weight` when ranking by output/uncertainty trade-off.
- [ ] Interval invariant `low <= predict <= high` verified on at least one output.
