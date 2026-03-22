---
name: ce-plotspec-author
description: >
  Author or extend PlotSpec-based visualizations with validated IR contracts and
  backend-agnostic rendering.
---

# CE PlotSpec Author

You are adding a new plot type using the PlotSpec IR. PlotSpec (ADR-007, ADR-016)
is the backend-agnostic intermediate representation for CE plots.

**Key architecture rule:** The legacy matplotlib renderer remains the default.
The PlotSpec path is **opt-in**. Do not change `.plot()` to use PlotSpec by default
unless ADR-016 explicitly authorises that step.

---

## PlotSpec IR components (`viz/plotspec.py`)

```python
from calibrated_explanations.viz.plotspec import (
    PlotSpec,          # top-level container
    BarHPanelSpec,     # panel with horizontal feature-contribution bars
    BarItem,           # one feature bar (value + optional interval)
    IntervalHeaderSpec, # header panel: scalar prediction with calibrated interval
    validate_plotspec, # structural validation helper
)
```

### `PlotSpec` — top-level container

| Field | Required | Notes |
|---|---|---|
| `kind` | ✅ | `"probabilistic"`, `"regression"`, `"triangular"`, `"global"` |
| `mode` | ✅ | `"classification"` or `"regression"` |
| `title` | `SHOULD` | Human-readable title |
| `feature_order` | `SHOULD` | List of feature names in display order |
| `header` | optional | `IntervalHeaderSpec` |
| `body` | optional | `BarHPanelSpec` |

### `BarItem` — one row in the body panel

```python
BarItem(
    label="age <= 30",           # feature rule label
    value=-0.12,                 # contribution weight
    interval_low=-0.18,          # optional uncertainty band
    interval_high=-0.06,
    color_role="negative",       # "positive" | "negative" | "regression"
    instance_value=25,           # original feature value (displayed on hover)
)
```

---

## Building a new plot type

```python
# src/calibrated_explanations/viz/builders.py (add a new builder function)

from __future__ import annotations

from calibrated_explanations.viz.plotspec import (
    BarHPanelSpec, BarItem, IntervalHeaderSpec, PlotSpec, validate_plotspec
)


def build_my_new_plot(explanation, *, filter_top: int | None = None) -> PlotSpec:
    """Build a PlotSpec for <describe your plot type>.

    Parameters
    ----------
    explanation : FactualExplanation
        The explanation instance to visualise.
    filter_top : int, optional
        Maximum number of features to include. ``None`` = all.

    Returns
    -------
    PlotSpec
        Validated backend-agnostic plot specification.
    """
    pred = explanation.prediction

    # 1. Build header
    header = IntervalHeaderSpec(
        pred=pred["predict"],
        low=pred["low"],
        high=pred["high"],
        xlabel="Predicted probability",
        dual=True,
    )

    # 2. Build bars
    rules = explanation.get_rules()
    items = sorted(rules.items(), key=lambda kv: abs(kv[1]["weight"]), reverse=True)
    if filter_top is not None:
        items = items[:filter_top]

    bars = [
        BarItem(
            label=info["rule"],
            value=info["weight"],
            interval_low=info.get("low"),
            interval_high=info.get("high"),
            color_role="positive" if info["weight"] >= 0 else "negative",
            instance_value=info.get("value"),
        )
        for _, info in items
    ]

    # 3. Assemble and validate
    spec = PlotSpec(
        kind="probabilistic",
        mode="classification",
        title=f"Explanation for instance {explanation.instance_index}",
        feature_order=[b.label for b in bars],
        header=header,
        body=BarHPanelSpec(bars=bars, xlabel="Feature contribution"),
    )
    validate_plotspec(spec)   # MUST call before returning
    return spec
```

---

## Registering a plot builder (opt-in)

```python
# src/calibrated_explanations/viz/plugins.py (thin in-process registry)
from calibrated_explanations.viz import register_builder

register_builder(kind="my_new_plot", builder_fn=build_my_new_plot)
```

Opt-in rendering from an explanation:
```python
from calibrated_explanations.viz import render

spec = build_my_new_plot(explanations[0])
render(spec, backend="matplotlib")  # default backend
```

---

## Validation rules (ADR-016)

`validate_plotspec` checks:
- `kind` and `mode` are present and non-empty.
- `header.pred`, `header.low`, `header.high` are numeric and form a valid interval
  (`low ≤ pred ≤ high`).
- `BarItem.value` is numeric.
- `interval_low ≤ interval_high` when both are provided.

```python
from calibrated_explanations.viz.plotspec import validate_plotspec
validate_plotspec(spec)   # raises ValueError on structural failure
```

---

## Testing PlotSpec output (ADR-016 approach)

Test **semantic correctness**, not pixel-perfect rendering:

```python
# tests/unit/viz/test_my_new_plot.py
import pytest
from calibrated_explanations.viz.plotspec import validate_plotspec


def test_should_produce_valid_spec_when_explanation_is_passed():
    from calibrated_explanations.viz.builders import build_my_new_plot
    # ... set up explanation fixture ...
    spec = build_my_new_plot(explanation)
    validate_plotspec(spec)  # structural assertion

    assert spec.kind == "probabilistic"
    assert spec.mode == "classification"
    assert len(spec.body.bars) > 0


def test_should_respect_filter_top_when_provided():
    from calibrated_explanations.viz.builders import build_my_new_plot
    spec = build_my_new_plot(explanation, filter_top=3)
    assert len(spec.body.bars) <= 3


def test_should_preserve_interval_ordering_when_building_header():
    from calibrated_explanations.viz.builders import build_my_new_plot
    spec = build_my_new_plot(explanation)
    h = spec.header
    assert h.low <= h.pred <= h.high
```

> **ADR-023 note:** matplotlib adapter tests may fail with coverage enabled.
> Mark them with `@pytest.mark.viz` and run via `pytest -m viz --no-cov`.

---

## MUST NOT patterns

```python
# ❌ Default matplotlib import at top level
import matplotlib.pyplot as plt    # top-level

# ❌ Coupling renderer logic to the builder
def build_my_plot(exp):
    import matplotlib.pyplot as plt  # inside a _builder_ function — wrong layer
    fig, ax = plt.subplots()
    ...
    return fig   # must return PlotSpec, not Figure

# ❌ Pixel-specific values in the spec
BarItem(label="age", value=0.3, color="#3B82F6")  # hex colour hardcoded in spec
```

---

## Evaluation Checklist

- [ ] `validate_plotspec(spec)` called before returning.
- [ ] `spec.kind` and `spec.mode` are non-empty strings.
- [ ] `header`: `low ≤ pred ≤ high`.
- [ ] `body` bars: `interval_low ≤ interval_high` when both present.
- [ ] Builder imports matplotlib **only** inside the renderer, not the builder.
- [ ] Test asserts semantic correctness (ordering, required fields), not colours.
- [ ] Viz test decorated with `@pytest.mark.viz` (ADR-023 exemption).
- [ ] Legacy `.plot()` still defaults to legacy renderer.
