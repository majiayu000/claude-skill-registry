---
name: ce-plugin-audit
description: >
  Audit plugin implementations for registry trust rules, metadata validity, and ADR
  contract compliance.
---

# CE Plugin Audit

You are auditing a plugin's conformance with the CE plugin contract.
Run through each audit dimension below and produce a structured report.

---

## Audit Dimension 1 — `plugin_meta` (ADR-006)

Run `validate_plugin_meta(plugin.plugin_meta)` and check:

| Field | Required | Correct type | Notes |
|---|---|---|---|
| `schema_version` | ✅ | `int` | Must be `1` for current contract |
| `name` | ✅ | non-empty `str` | Recommend reverse-DNS |
| `version` | ✅ | non-empty `str` | Semantic version |
| `provider` | ✅ | non-empty `str` | Author/org attribution |
| `capabilities` | ✅ | non-empty `list[str]` | Each tag non-empty |
| `trusted` | optional | `bool` | Built-ins set `True`; third-party `False` |
| `data_modalities` | optional (ADR-033) | `tuple[str, ...]` | Normalised lowercase; validated taxonomy |
| `plugin_api_version` | optional (ADR-033) | `"MAJOR.MINOR"` str | Default `"1.0"` |

```python
from calibrated_explanations.plugins.base import validate_plugin_meta
validate_plugin_meta(plugin.plugin_meta)   # raises ValidationError on non-conformance
```

---

## Audit Dimension 2 — Capability tags (ADR-015)

Each capability tag must match a defined CE capability:

| Expected tag | Plugin type |
|---|---|
| `"interval:classification"` | Classification calibrator |
| `"interval:regression"` | Regression calibrator |
| `"explanation:factual"`, `"explanation:alternative"`, `"explanation:fast"` | Explanation |
| `"plot:legacy"`, `"plot:plotspec"` | Plot |

**Red flag:** Plugin lists no capability tags, or lists tags it doesn't implement.

---

## Audit Dimension 3 — Interval calibrator protocol (ADR-013)

If `"interval:classification"` or `"interval:regression"` in capabilities:

```python
# Required: predict_proba must match VennAbers surface exactly
def predict_proba(
    self, x, *, output_interval: bool = False, classes=None, bins=None
) -> np.ndarray: ...
# Shapes: (n_samples, n_classes) when output_interval=False
#         (n_samples, n_classes, 3) when output_interval=True (predict, low, high)

def is_multiclass(self) -> bool: ...
def is_mondrian(self) -> bool: ...
```

For regression (`"interval:regression"`), additional surface required:
```python
def predict_probability(self, x) -> np.ndarray: ...  # shape (n_samples, 2): (low, high)
def predict_uncertainty(self, x) -> np.ndarray: ...  # shape (n_samples, 2): (width, confidence)
def pre_fit_for_probabilistic(self, x, y) -> None: ...
def compute_proba_cal(self, x, y, *, weights=None) -> np.ndarray: ...
def insert_calibration(self, x, y, *, warm_start: bool = False) -> None: ...
```

**Critical:** `predict_proba` must delegate to VennAbers/IntervalRegressor reference logic
to preserve calibration guarantees (ADR-021). A plugin that replaces the probability
maths wholesale is non-conformant.

**Context immutability:** The plugin must NOT mutate fields in the
`IntervalCalibratorContext` passed to `create()`.

---

## Audit Dimension 4 — ADR-001: Core / plugin boundary

**FAIL if** the plugin imports anything from `calibrated_explanations.core.*`
that is not a protocol, dataclass, or exception:

```python
# OK — passive types
from calibrated_explanations.core.exceptions import ValidationError

# NOT OK — implementation details
from calibrated_explanations.core.calibrated_explainer import CalibratedExplainer  # red flag
```

Check with:
```bash
grep -r "from calibrated_explanations.core" src/your_plugin/
```

---

## Audit Dimension 5 — Fallback visibility (mandatory copilot-instructions.md §7)

All fallback decisions inside the plugin must be visible:
```python
import warnings, logging
_LOGGER = logging.getLogger("calibrated_explanations.plugins.<name>")

# BAD — silent fallback
if something_failed:
    use_legacy_path()

# GOOD — visible fallback
if something_failed:
    msg = "MyPlugin: <reason>. Falling back to legacy path."
    _LOGGER.info(msg)
    warnings.warn(msg, UserWarning, stacklevel=2)
    use_legacy_path()
```

---

## Audit Dimension 6 — Lazy imports (source-code.instructions.md)

Heavy optional dependencies must be imported lazily:
```python
# BAD
import matplotlib.pyplot as plt   # top-level in a module reachable from package root

# GOOD
def render(self, ...):
    import matplotlib.pyplot as plt  # inside function body
```

---

## Audit Dimension 7 — ADR-033 modality contract (if applicable)

If the plugin targets a non-tabular modality (`"image"`, `"audio"`, `"text"`,
`"timeseries"`, `"multimodal"`, or `"x-<vendor>-<name>"`):

- `data_modalities` must be present in `plugin_meta`.
- Modality strings must be in the canonical taxonomy or use the `x-<vendor>-<name>` namespace.
- Aliases (`"vision" → "image"`, `"time_series" → "timeseries"`) are acceptable inputs but
  are normalised to canonical form by the registry.
- `plugin_api_version` must be present; major-version mismatch causes a registry rejection.

---

## Report Template

```
Plugin Audit Report: <plugin name>
===================================
plugin_meta validation:        PASS / FAIL
  details: <fieldname: issue>

Capability tags:               PASS / FAIL / N_A
  declared: [...]
  implemented: [...]

Interval protocol (ADR-013):   PASS / FAIL / N_A
  predict_proba shape:         PASS / FAIL
  context immutability:        PASS / FAIL
  delegates to reference:      YES / NO

ADR-001 core boundary:         PASS / FAIL
  violations: <list>

Fallback visibility:           PASS / FAIL
  missing warn():              <method names>

Lazy imports:                  PASS / FAIL
  eager heavy imports:         <list>

ADR-033 modality (if used):    PASS / FAIL / N_A
  data_modalities:             <value>
  plugin_api_version:          <value>

Overall:   CONFORMANT / NON-CONFORMANT (N issues)
```

---

## Evaluation Checklist

- [ ] `validate_plugin_meta()` called and passes.
- [ ] All declared capabilities have corresponding implementations.
- [ ] Context not mutated in `create()`.
- [ ] `predict_proba` delegates to VennAbers / IntervalRegressor for probability maths.
- [ ] No imports of `core/` implementation details.
- [ ] Every fallback emits `warnings.warn + _LOGGER.info`.
- [ ] No eager top-level imports of matplotlib/pandas/joblib.
- [ ] ADR-033 metadata present if non-tabular modality targeted.
