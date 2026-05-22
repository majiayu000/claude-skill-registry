---
name: ce-explain-interact
description: >
  Post-process CE explanations by narrating, plotting, inspecting rules, filtering
  features, and managing conjunctions.
---

# CE Explain Interact

This skill covers the generic post-generation API that is shared by every CE
explanation type. It applies to both individual `CalibratedExplanation` instances
and `CalibratedExplanations` collections.

## Conjunctions

Add compound multi-feature rules on top of the existing atomic rules:

```python
# On a single instance (mutates in place, returns self for chaining)
explanations[0].add_conjunctions(max_rule_size=2)          # default
explanations[0].add_conjunctions(max_rule_size=3)          # triples
explanations[0].add_conjunctions(max_rule_size=2, n_top_features=5)  # limit outer

# On the whole collection (applies to each instance)
explanations.add_conjunctions(max_rule_size=2, n_top_features=5)
```

### Parameters

| Parameter | Default | Meaning |
|---|---|---|
| `max_rule_size` | `2` | **Primary control.** Maximum number of features in a conjunctive rule. Must be ≥ 2. Values ≥ 4 require batched mode (internal). |
| `n_top_features` | `5` | Optional: limit the outer feature loop to the N most impactful features. Higher values explore more combinations but take longer. |

**`max_rule_size` is the key knob.** `n_top_features` is a speed/pruning control.

### After adding conjunctions

```python
explanations[0].remove_conjunctions()    # strips conjunctions, keeps atomic rules
explanations[0].reset()                  # resets to original atomic state entirely
```

---

## Narrative

```python
explanations[0].to_narrative(
    expertise_level="beginner",          # or "advanced" or ("beginner", "advanced")
    output_format="text",                # "text", "dataframe", other supported formats
)
```

### Parameters

| Parameter | Default | Options / Notes |
|---|---|---|
| `expertise_level` | `("beginner", "advanced")` | `"beginner"` (plain language), `"advanced"` (technical), or a tuple to get both |
| `output_format` | `"dataframe"` | `"text"` for a string; `"dataframe"` for a DataFrame; others may be supported |
| `conjunction_separator` | `" AND "` | Separator string for conjunctive rule display |
| `align_weights` | `True` | Whether to align feature weights in the narrative |
| `template_path` | `"exp.yaml"` | Template file; only override when using a custom template |

---

## Plotting

```python
# Single instance
explanations[0].plot(filter_top=10)                        # show top-10 rules
explanations[0].plot(filter_top=None)                      # show all rules
explanations[0].plot(filter_top=5, uncertainty=True)       # include interval bands

# Collection (all instances)
explanations.plot(filter_top=10)
explanations.plot(index=2, filter_top=5)                   # plot one instance by index
```

### Common kwargs (all explanation types)

| Parameter | Default | Notes |
|---|---|---|
| `filter_top` | `None` (single) / `10` (collection) | Maximum rules to show. `None` = show all. |
| `uncertainty` | `False` | Show uncertainty interval bands on bars. Not valid for one-sided intervals. |
| `style` | `"regular"` | `"regular"` for all types; `"triangular"` / `"ensured"` for `AlternativeExplanation` only |
| `rnk_metric` | varies by type | `"feature_weight"` (factual/fast default), `"ensured"` (alternative default), `"uncertainty"` |
| `rnk_weight` | `0.5` | Used with `rnk_metric="ensured"`. Range −1 to 1; 0 = uncertainty only, ±1 = output only |
| `show` | `True` | Render inline. Set `False` + `filename=...` to save to disk. |
| `filename` | `""` | Path to save; empty = display only. |

> **Note:** `rnk_metric` and `style` defaults differ between factual and alternative
> explanations — see `ce-factual-explain` and `ce-alternatives-explore`.

---

## Filtering Rules by Size

`filter_rule_sizes` selects rules by the number of features they contain.
Atomic rules have size 1; conjunctions have size ≥ 2.

```python
# Keep only atomic rules (size 1)
atomic_only = explanations[0].filter_rule_sizes(rule_sizes=1)

# Keep conjunctions of size 2 and 3
pair_and_triple = explanations[0].add_conjunctions(max_rule_size=3) \
                                  .filter_rule_sizes(rule_sizes=[2, 3])

# Inclusive range
up_to_triples = explanations[0].filter_rule_sizes(size_range=(1, 3))

# On the whole collection
filtered = explanations.filter_rule_sizes(rule_sizes=[1, 2])
```

### Parameters

| Parameter | Default | Notes |
|---|---|---|
| `rule_sizes` | — | `int` or list of `int`. Must NOT be combined with `size_range`. |
| `size_range` | — | `(min_size, max_size)` inclusive. Must NOT be combined with `rule_sizes`. |
| `copy` | `True` | Return a filtered copy. `False` = mutate in place. |

Exactly one of `rule_sizes` or `size_range` must be provided.

---

## Filtering Rules by Feature

`filter_features` selects or excludes rules based on which features they involve.
Works with single instances and collections.

```python
# Keep only rules involving "age" or feature index 2
filtered = explanations[0].filter_features(include_features=["age", 2])

# Exclude rules involving "gender"
filtered = explanations[0].filter_features(exclude_features="gender")

# On the whole collection
filtered = explanations.filter_features(include_features=["age", "income"])
```

### Parameters

| Parameter | Default | Notes |
|---|---|---|
| `include_features` | — | `str`, `int`, or list of `str`/`int`. Keep only matching features. |
| `exclude_features` | — | `str`, `int`, or list of `str`/`int`. Remove matching features. |
| `copy` | `True` | Return a filtered copy. `False` = mutate in place. |

Exactly one of `include_features` or `exclude_features` must be provided.

### Notes for conjunctive rules

For conjunctive rules, a rule is kept if **any** of its constituent features match
the include/exclude criterion — the entire rule is the unit of filtering.

---

## Inspecting Explanation Contents

```python
exp = explanations[0]

# Prediction dict (same structure for all types)
pred = exp.prediction
pred['predict']   # point prediction
pred['low']       # interval lower bound
pred['high']      # interval upper bound
# Invariant: pred['low'] <= pred['predict'] <= pred['high']

# Feature weights
exp.feature_weights   # array of per-feature impact scores
exp.feature_predict   # per-feature calibrated predictions

# Rules
rules = exp.get_rules()        # materialise all rules as a dict payload
rules_list = exp.list_rules()  # normalised list of rule dicts (FactualExplanation)

# Conjunction state
exp.has_conjunctive_rules   # bool
exp.conjunctive_rules       # None or rule payload dict

# Mode helpers
exp.is_regression()         # bool
exp.is_probabilistic()      # bool — True for thresholded regression
```

---

## Chaining

All mutation methods return `self` and can be chained:

```python
narrative = (
    explanations[0]
    .add_conjunctions(max_rule_size=3)
    .filter_rule_sizes(rule_sizes=[2, 3])
    .to_narrative(expertise_level="beginner", output_format="text")
)
```

---

## Out of Scope

- Generating explanations (see `ce-factual-explain`, `ce-alternatives-explore`).
- Alternatives-specific filtering (see `ce-alternatives-explore`).
- Regression interval semantics (see `ce-regression-intervals`).

## Evaluation Checklist

- [ ] `max_rule_size` used (not `n_top_features`) as the primary conjunction control.
- [ ] `expertise_level` passed to `to_narrative` when output audience is known.
- [ ] `filter_top` (not `n_top_features`) used on `plot()`.
- [ ] Exactly one of `rule_sizes` / `size_range` for `filter_rule_sizes`.
- [ ] Exactly one of `include_features` / `exclude_features` for `filter_features`.
- [ ] `copy=True` preserved (default) unless in-place mutation is intended.
- [ ] Interval invariant `low ≤ predict ≤ high` still holds after filtering.
