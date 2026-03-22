---
name: ce-plugin-scaffold
description: >
  Scaffold interval, explanation, or plot plugins that satisfy registry metadata
  and trust-model contracts. For non-tabular modalities (vision, audio, timeseries),
  use ce-modality-extension instead.
---

# CE Plugin Scaffold

You are scaffolding a plugin for calibrated_explanations. All plugins must follow
ADR-006 (trust model), ADR-013 (interval calibrators), ADR-014 (plot plugins),
ADR-015 (explanation plugins), and ADR-033 (modality metadata). Plugins live in
`src/calibrated_explanations/plugins/` for built-ins or in a separate
package for third-party extensions.

**Core rule (ADR-001):** `core/` never imports anything from `plugins/`. All new
functionality belongs in `plugins/`, with `core/` delegating via the registry.

---

## Step 1 — Choose the right plugin type

| What you want | Plugin type | Base protocol |
|---|---|---|
| New calibration method | Interval calibrator plugin | `ClassificationIntervalCalibrator` or `RegressionIntervalCalibrator` |
| New explanation strategy | Explanation plugin | `ExplanationPlugin` (ADR-015) |
| New plot renderer / style | Plot plugin | `PlotBuilder` + `PlotRenderer` (ADR-014) |
| Non-tabular modality | Modality extension | ADR-033 + modality metadata |

---

## Step 2 — `plugin_meta` (required for all plugin types)

```python
plugin_meta: dict = {
    "schema_version": 1,            # int — must be 1 for current contract
    "name": "mypkg.my_plugin",      # str — reverse-DNS identifier
    "version": "0.1.0",             # str — semantic version
    "provider": "author/org",       # str — attribution
    "capabilities": [               # list[str] — at least one capability tag
        "interval:classification",  # or "interval:regression", "explanation:factual", etc.
    ],
    "trusted": False,               # bool — True only for built-ins
    # Optional (ADR-033):
    "data_modalities": ("tabular",),    # tuple[str, ...] normalised to lowercase
    "plugin_api_version": "1.0",        # str — "MAJOR.MINOR"
}
```

Validate with:
```python
from calibrated_explanations.plugins.base import validate_plugin_meta
validate_plugin_meta(plugin_meta)   # raises ValidationError on failure
```

### Capability tag reference

| Capability | Plugin type |
|---|---|
| `"interval:classification"` | Classification interval calibrator |
| `"interval:regression"` | Regression interval calibrator |
| `"explanation:factual"` | Factual explanation strategy |
| `"explanation:alternative"` | Alternative explanation strategy |
| `"explanation:fast"` | FAST explanation strategy |
| `"plot:legacy"` | Legacy matplotlib renderer |
| `"plot:plotspec"` | PlotSpec-based renderer |

---

## Step 3 — Scaffold: interval calibrator plugin

```python
from __future__ import annotations

import warnings
import logging
from typing import Any
import numpy as np

from calibrated_explanations.plugins.base import validate_plugin_meta

_LOGGER = logging.getLogger("calibrated_explanations.plugins.my_calibrator")


class MyIntervalCalibratorPlugin:
    """Custom interval calibrator plugin.

    Parameters
    ----------
    (your params here)

    Notes
    -----
    Must implement the ClassificationIntervalCalibrator protocol (ADR-013).
    Probability predictions must delegate to the VennAbers reference to
    preserve calibration guarantees (ADR-021).
    """

    plugin_meta = {
        "schema_version": 1,
        "name": "mypkg.interval.my_calibrator",
        "version": "0.1.0",
        "provider": "your-name",
        "capabilities": ["interval:classification"],
        "trusted": False,
        "data_modalities": ("tabular",),
        "plugin_api_version": "1.0",
    }

    def supports(self, model: Any) -> bool:
        # Return True for model types this plugin handles
        return True

    def create(self, context, *, fast: bool = False):
        """Create and return a ClassificationIntervalCalibrator.

        Parameters
        ----------
        context : IntervalCalibratorContext
            Frozen calibrator context from the explainer.
        fast : bool, optional
            Whether to use the reduced-computation (FAST) path.

        Returns
        -------
        ClassificationIntervalCalibrator
        """
        # Use context.learner, context.calibration_splits, context.bins, etc.
        # DO NOT mutate context fields — they are read-only.
        from calibrated_explanations.core.venn_abers import VennAbers
        # Wrap / extend VennAbers; delegate predict_proba to it.
        return _MyCalibrator(context)

    def explain(self, model: Any, x: Any, **kwargs: Any) -> Any:
        """Not used by interval plugins; included to satisfy ExplainerPlugin protocol."""
        raise NotImplementedError


class _MyCalibrator:
    """Wraps an IntervalCalibratorContext to expose the predict_proba protocol."""

    def __init__(self, context) -> None:
        self._context = context

    def predict_proba(self, x, *, output_interval: bool = False,
                      classes=None, bins=None) -> np.ndarray:
        # MUST delegate to VennAbers / the reference implementation
        raise NotImplementedError("Delegate to VennAbers.predict_proba")

    def is_multiclass(self) -> bool:
        raise NotImplementedError

    def is_mondrian(self) -> bool:
        raise NotImplementedError
```

---

## Step 4 — Register the plugin

```python
from calibrated_explanations.plugins.registry import register, trust_plugin

# Register (built-ins do this at import time; third-party at application startup)
register(MyIntervalCalibratorPlugin())

# Trust explicitly — required for third-party usage (ADR-006)
trust_plugin("mypkg.interval.my_calibrator")

# Or via environment variable:
# CE_TRUST_PLUGIN=mypkg.interval.my_calibrator

# Or in pyproject.toml:
# [tool.calibrated_explanations.plugins]
# trusted = ["mypkg.interval.my_calibrator"]
```

---

## Step 5 — Register via entry points (third-party packaging)

```toml
# pyproject.toml
[project.entry-points."calibrated_explanations.plugins"]
my_calibrator = "mypkg.plugins:MyIntervalCalibratorPlugin"
```

---

## Step 6 — Test your plugin

```python
# tests/unit/plugins/test_my_calibrator_plugin.py
import pytest
from calibrated_explanations.plugins.base import validate_plugin_meta


def test_should_pass_meta_validation_when_plugin_meta_is_defined():
    from mypkg.plugins import MyIntervalCalibratorPlugin
    validate_plugin_meta(MyIntervalCalibratorPlugin.plugin_meta)  # no exception


def test_should_return_true_for_supports_when_given_compatible_model():
    from mypkg.plugins import MyIntervalCalibratorPlugin
    plugin = MyIntervalCalibratorPlugin()
    assert plugin.supports(object()) is True
```

---

## Fallback visibility rule (mandatory — ADR §7)

If your plugin provides a fallback path:
```python
import warnings
import logging

_LOGGER = logging.getLogger("calibrated_explanations.plugins.my_plugin")

def _fallback_to_legacy(reason: str) -> None:
    msg = f"MyPlugin fallback: {reason}. Using legacy path."
    _LOGGER.info(msg)
    warnings.warn(msg, UserWarning, stacklevel=3)
```

---

## Out of Scope

- Adding new explanation types to `core/` directly (all new strategies go in `plugins/`).
- Non-tabular modality plugins (see `ce-modality-extension`).
- Plot plugins (ADR-014 opt-in; kept minimal — just `PlotBuilder.build` + `PlotRenderer.render`).

## Evaluation Checklist

- [ ] `plugin_meta` passes `validate_plugin_meta()` without error.
- [ ] `data_modalities` and `plugin_api_version` present if targeting ADR-033.
- [ ] `create()` / `explain()` do NOT mutate the context object.
- [ ] Calibrator `predict_proba` delegates to VennAbers / IntervalRegressor reference logic.
- [ ] Plugin registered and trusted before use.
- [ ] Fallback path emits `warnings.warn(..., UserWarning)` + `_LOGGER.info(...)`.
- [ ] Unit test calls `validate_plugin_meta(plugin.plugin_meta)`.
