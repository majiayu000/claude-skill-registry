---
name: ce-fallback-impl
description: >
  Implement fallback chains that always emit UserWarning and INFO logs per CE
  fallback-visibility policy.
---

# CE Fallback Implementation

You are implementing a fallback path. The CE fallback visibility policy
(copilot-instructions.md §7) is **mandatory**: every fallback must be visible
to users via both a `UserWarning` and an `INFO` log. Silent fallbacks are a
blocking code-review failure.

---

## Mandatory pattern

```python
from __future__ import annotations

import logging
import warnings

_LOGGER = logging.getLogger("calibrated_explanations.<domain>.<module>")
# Domain guidance (ADR-028):
#   core.*     — core runtime (explain, predict, cache, parallel)
#   plugins.*  — plugins (interval, explanation, plot)
#   governance.* — trust/deny decisions


def _emit_fallback(msg: str, *, stacklevel: int = 2) -> None:
    """Emit a mandatory visible fallback notification.

    Parameters
    ----------
    msg : str
        Human-readable reason and chosen fallback path.
    stacklevel : int, optional
        Stack depth for the warning (default 2 — immediate caller).
    """
    _LOGGER.info(msg)
    warnings.warn(msg, UserWarning, stacklevel=stacklevel + 1)
```

Usage:
```python
def _run_parallel(self, data):
    try:
        return self._parallel_backend.run(data)
    except Exception as exc:          # noqa: BLE001
        _emit_fallback(
            f"{self.__class__.__name__}: parallel execution failed "
            f"({exc!r}). Falling back to sequential.",
            stacklevel=2,
        )
        return self._sequential_fallback(data)
```

---

## Common fallback scenarios

### Parallel → sequential execution

```python
import warnings, logging
_LOGGER = logging.getLogger("calibrated_explanations.core.parallel")

def _parallel_or_sequential(tasks, *, backend):
    try:
        return backend.run(tasks)
    except Exception as exc:  # noqa: BLE001
        msg = (
            f"Parallel backend '{backend.__class__.__name__}' failed "
            f"({type(exc).__name__}). Falling back to sequential execution. "
            "Set backend='sequential' to suppress this warning."
        )
        _LOGGER.info(msg)
        warnings.warn(msg, UserWarning, stacklevel=2)
        return [task() for task in tasks]
```

### Plugin not found → legacy path

```python
def _resolve_plugin_or_legacy(name: str):
    plugin = registry.find_plugin(name, trusted=True)
    if plugin is None:
        msg = (
            f"Plugin '{name}' not found or not trusted. "
            "Falling back to legacy path. Register and trust the plugin to use it."
        )
        _LOGGER.info(msg)
        warnings.warn(msg, UserWarning, stacklevel=3)
        return _LEGACY_PLUGIN
    return plugin
```

### Visualization simplification

```python
def _render_with_fallback(spec, backend):
    try:
        return backend.render(spec)
    except RuntimeError as exc:
        msg = (
            f"Visualization backend '{backend}' failed ({exc!r}). "
            "Falling back to simplified legend-only view."
        )
        _LOGGER.info(msg)
        warnings.warn(msg, UserWarning, stacklevel=2)
        return _render_simplified(spec)
```

---

## Testing a fallback

Tests that verify a fallback must assert the `UserWarning` is raised.
The project autouse fixture `disable_fallbacks` (from `tests/conftest.py`)
makes the fallback chain empty by default, so only tests that are
**explicitly about fallback behaviour** should trigger warnings.

```python
import pytest

def test_should_warn_when_parallel_backend_fails(monkeypatch):
    """Fallback warning must be raised when parallel execution fails."""
    # Arrange
    from calibrated_explanations.core.parallel import _parallel_or_sequential

    def _failing_backend(tasks):
        raise RuntimeError("connection refused")

    # Act + Assert
    with pytest.warns(UserWarning, match="Falling back to sequential"):
        result = _parallel_or_sequential(tasks=[lambda: 1], backend=_failing_backend)

    assert result == [1]
```

For tests that do NOT depend on a fallback, ensure the fallback chain is empty
(the `disable_fallbacks` fixture handles this automatically via `conftest.py`):
```python
# No extra setup needed if using the autouse fixture.
# If the autouse fixture is not applied for some reason:
@pytest.fixture(autouse=True)
def _disable_fallbacks(disable_fallbacks):
    pass
```

---

## Logger domain guidance (ADR-028)

| Code location | Logger name |
|---|---|
| `core/` runtime code | `calibrated_explanations.core.<submodule>` |
| `plugins/` code | `calibrated_explanations.plugins.<name>` |
| Governance/trust decisions | `calibrated_explanations.governance.<submodule>` |

---

## Anti-patterns (FAIL in code review)

```python
# ❌ Silent fallback — no warn, no log
try:
    do_fast_path()
except Exception:
    do_slow_path()   # user has no idea this happened

# ❌ Log only — no UserWarning
_LOGGER.warning("Using sequential")  # Python 'logging' warning != warnings.warn

# ❌ print() instead of proper channels
print("WARNING: falling back")

# ❌ RuntimeError/ValueError for a recoverable decision
raise RuntimeError("parallel failed")  # should fall back, not raise
```

---

## Evaluation Checklist

- [ ] Every fallback calls both `_LOGGER.info(...)` AND `warnings.warn(..., UserWarning)`.
- [ ] Warning message clearly states what failed and what path is chosen.
- [ ] `stacklevel` is set so the warning points to the user's call site (not the helper).
- [ ] Test uses `pytest.warns(UserWarning, match=...)` to assert the warning.
- [ ] Tests NOT about fallback behaviour rely on `disable_fallbacks` fixture.
- [ ] Logger domain matches the module's location (ADR-028).
