---
name: ce-modality-extension
description: >
  Extend CE to non-tabular data modalities (vision, audio, timeseries, text) via
  ADR-033 plugin contracts, modality naming rules, and extension safety guardrails.
---

# CE Modality Extension

You are implementing or evaluating a modality extension plugin per ADR-033.
Modality extensions keep the CE core dependency-light while enabling non-tabular
inputs via separately packaged plugins.

---

## Core principle (ADR-033 + ADR-001)

Modality-specific runtime code MUST NOT be added directly to
`calibrated_explanations` core. A thin shim module (`calibrated_explanations.vision`,
`calibrated_explanations.audio`) is allowed; it must raise `MissingExtensionError`
if the extension package is absent.

---

## Canonical modality taxonomy

| Canonical name | Aliases (registry-normalised) |
|---|---|
| `"tabular"` | — (default) |
| `"image"` | `"vision"` |
| `"audio"` | — |
| `"text"` | — |
| `"timeseries"` | `"time_series"` |
| `"multimodal"` | `"multi-modal"` |
| `"x-<vendor>-<name>"` | Custom extension namespace |

---

## `plugin_meta` for a modality extension

```python
plugin_meta = {
    "schema_version": 1,
    "name": "mypkg.vision.explanation",
    "version": "0.1.0",
    "provider": "author/org",
    "capabilities": ["explanation:factual"],
    "trusted": False,
    # ADR-033 required for non-tabular:
    "data_modalities": ("image",),     # normalised canonical name(s)
    "plugin_api_version": "1.0",       # "MAJOR.MINOR" — must match CE contract
}
```

### Compatibility policy (ADR-033 §1.4)

| CE `plugin_api_version` | Extension `plugin_api_version` | Registry result |
|---|---|---|
| `"1.0"` | `"1.0"` | ✅ accepted |
| `"1.0"` | `"1.1"` | ⚠️ `UserWarning` + governance log; accepted |
| `"1.0"` | `"2.0"` | ❌ `ValidationError` — major mismatch |
| `"1.0"` | not present | ⚠️ treated as `"1.0"` (backward-compat default) |

---

## Shim module pattern

CE ships thin shims for first-party modality namespaces:
```python
# src/calibrated_explanations/vision.py
"""Thin shim for image/vision modality extensions (ADR-033)."""
from __future__ import annotations

try:
    from ce_vision import _register_vision_plugin  # first-party extension package
except ImportError:
    def __getattr__(name: str):  # noqa: ANN001
        from calibrated_explanations.utils.exceptions import MissingExtensionError
        raise MissingExtensionError(
            f"calibrated_explanations.vision.{name} requires the 'ce-vision' package. "
            "Install it with: pip install ce-vision"
        )
```

---

## Monorepo multi-package structure (ADR-033 §7)

Preferred layout for first-party modality packages:
```
calibrated-explanations/        ← core package (this repo)
ce-vision/                      ← separate package, independent versioning
  pyproject.toml                   version = "0.1.0"
  src/ce_vision/
    plugins.py                     VisionExplanationPlugin
    preprocessing.py               image → tabular feature extraction
    tests/
      test_packaging_smoke.py      entry-point discovery + import smoke test
```

Entry-point declaration:
```toml
# ce-vision/pyproject.toml
[project.entry-points."calibrated_explanations.plugins"]
ce_vision = "ce_vision.plugins:VisionExplanationPlugin"
```

---

## CI smoke test (ADR-033 §8)

A lightweight "dummy" modality plugin must be present in `tests/` to validate
the contract in CI:
```python
# tests/unit/plugins/test_modality_contract.py
import pytest
from calibrated_explanations.plugins.base import validate_plugin_meta


DUMMY_VISION_META = {
    "schema_version": 1,
    "name": "test.vision.dummy",
    "version": "0.1.0",
    "provider": "test-author",
    "capabilities": ["explanation:factual"],
    "trusted": False,
    "data_modalities": ("image",),
    "plugin_api_version": "1.0",
}

def test_should_pass_meta_validation_when_vision_plugin_meta_is_valid():
    validate_plugin_meta(DUMMY_VISION_META)  # no exception


def test_should_raise_on_major_version_mismatch_when_plugin_api_version_incompatible():
    from calibrated_explanations.plugins.registry import _check_plugin_api_compat
    import pytest
    with pytest.raises(Exception, match="major"):
        _check_plugin_api_compat(required="1.0", provided="2.0")
```

---

## Release timeline (ADR-033)

| Release | What ships |
|---|---|
| `v0.11.0` | Metadata contract validation + modality taxonomy enforcement + resolver tie-break |
| `v0.11.1` | CLI `--modality`, shim modules (`vision`/`audio`), packaging smoke-test gate |
| `v0.12.0` | First-party modality package promotions (after `v0.11.0` contract stabilises) |

---

## Out of Scope

- Adding modality preprocessing code to `core/` — it belongs in the extension package.
- Modality-specific plot renderers in `core/` — use a `PlotPlugin` variant.
- Cross-modality explanation fusion — deferred to a future ADR.

## Evaluation Checklist

- [ ] `plugin_meta` includes `data_modalities` (canonical or `x-<vendor>-<name>`).
- [ ] `plugin_api_version` present; major-version compatibility verified.
- [ ] No modality-specific code added to `calibrated_explanations.core`.
- [ ] Shim module present if using a CE namespace (`vision`, `audio`).
- [ ] Shim raises `MissingExtensionError` (not `ImportError`) when extension absent.
- [ ] CI smoke test validates entry-point discovery and import behaviour.
- [ ] Extension packaged independently with its own version.
