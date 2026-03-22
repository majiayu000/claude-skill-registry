---
name: ce-plot-review
description: >
  Review visualization code for ADR-compliant PlotSpec behavior, lazy imports, and
  renderer correctness.
---

# CE Plot Review

You are auditing plot code for conformance with CE visualization ADRs.
Work through each dimension below and produce a finding per violation.

---

## Dimension 1 — Lazy matplotlib import (CRITICAL)

```python
# FAIL — top-level import in any module reachable from the package root
import matplotlib.pyplot as plt

# PASS — lazily imported inside the function body
def render(self, spec, **opts):
    import matplotlib.pyplot as plt
    ...
```

```bash
# Scan command
grep -rn "^import matplotlib\|^from matplotlib" src/calibrated_explanations/
```

---

## Dimension 2 — Legacy renderer is still the default (ADR-014)

`.plot()` on any `FactualExplanation` or `AlternativeExplanation` must call the
legacy renderer by default; PlotSpec-based renderers are opt-in.

```python
# FAIL — silently switching to PlotSpec path without opt-in
def plot(self, **kwargs):
    spec = build_spec(self)
    return render_plotspec(spec)     # wrong if this is now the default

# PASS — legacy default with explicit opt-in
def plot(self, *, use_plotspec: bool = False, **kwargs):
    if use_plotspec:
        spec = build_spec(self)
        return render_plotspec(spec)
    return _legacy_plot(self, **kwargs)
```

---

## Dimension 3 — PlotSpec validation (ADR-016)

Any code that produces a `PlotSpec` must call `validate_plotspec()`:

```python
from calibrated_explanations.viz.plotspec import validate_plotspec

# FAIL — PlotSpec created but not validated before use
spec = PlotSpec(kind="probabilistic", mode="classification", ...)
render(spec)

# PASS
spec = PlotSpec(...)
validate_plotspec(spec)   # must raise on bad structure before rendering
render(spec)
```

Minimum semantic fields (ADR-016):
- `spec.kind`: non-empty string (e.g. `"probabilistic"`, `"regression"`, `"triangular"`, `"global"`).
- `spec.mode`: `"classification"` or `"regression"`.
- `header.low ≤ header.pred ≤ header.high` when header present.

---

## Dimension 4 — Renderer / builder separation

The builder produces a `PlotSpec`; the renderer receives a `PlotSpec` and draws.
Mixing these responsibilities is a code smell:

```python
# FAIL — builder imports matplotlib and creates a figure
def build_my_plot(explanation):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ...
    return fig   # should return PlotSpec

# PASS
def build_my_plot(explanation) -> PlotSpec:
    ...
    return PlotSpec(...)

def render_my_plot(spec: PlotSpec):
    import matplotlib.pyplot as plt
    ...
```

---

## Dimension 5 — ADR-023 matplotlib test exemption

Tests that exercise matplotlib rendering must:
- Be marked with `@pytest.mark.viz`.
- Not be run as part of the coverage job (only `pytest -m viz --no-cov`).
- The module `viz/matplotlib_adapter.py` is explicitly excluded from coverage.

```python
# PASS
import pytest

@pytest.mark.viz
def test_should_render_without_error_when_valid_spec_provided():
    import matplotlib.pyplot as plt
    ...
```

```python
# FAIL — viz test not marked, runs in coverage job, causes ADR-023 failure
def test_render_my_plot():
    import matplotlib.pyplot as plt
    ...
```

---

## Dimension 6 — `filter_top` not `n_top_features` in plot interface

The public `.plot()` signature uses `filter_top`:

```python
# FAIL
explanation.plot(n_top_features=5)   # wrong parameter name

# PASS
explanation.plot(filter_top=5)
```

---

## Dimension 7 — PlotSpec IR colour roles (ADR-016)

`BarItem.color_role` must use one of the defined semantic roles:
`"positive"`, `"negative"`, `"regression"`. Hex colours and RGB tuples
must stay inside the renderer / adapter, not in the spec.

```python
# FAIL — colour hardcoded in spec
BarItem(label="age", value=0.3, color="#3B82F6")

# PASS — semantic role
BarItem(label="age", value=0.3, color_role="positive")
```

---

## Review Report Template

```
CE Plot Review: <module/PR name>
==================================
Lazy matplotlib import:       PASS / FAIL
  violations:                 <list file:line>

Legacy renderer as default:   PASS / FAIL
  violations:                 <list>

validate_plotspec() called:   PASS / FAIL / N_A
  missing at:                 <list>

Builder/renderer separation:  PASS / FAIL
  violations:                 <list>

ADR-023 viz test marking:     PASS / FAIL / N_A
  unmarked viz tests:         <list>

Plot interface (filter_top):  PASS / FAIL
  wrong params:               <list>

PlotSpec colour roles:        PASS / FAIL / N_A
  hardcoded colours:          <list>

Overall: CONFORMANT / NON-CONFORMANT (<N> issues)
```

---

## Evaluation Checklist

- [ ] All 7 dimensions checked.
- [ ] Lazy import violations are blocking.
- [ ] Legacy renderer as default verified.
- [ ] All `PlotSpec` construction is followed by `validate_plotspec()`.
- [ ] Viz tests marked `@pytest.mark.viz` and excluded from coverage runs.
- [ ] Public API uses `filter_top`, not `n_top_features`.
- [ ] Report produced with file:line references for each issue.
