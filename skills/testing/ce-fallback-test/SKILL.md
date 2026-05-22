---
name: ce-fallback-test
description: >
  Author tests that verify fallback visibility through opt-in fixtures, warning
  assertions, and INFO log side effects.
---

# CE Fallback Test

You are writing tests that validate fallback chain behavior. This is a
**deliberate opt-in** — normal tests must NOT trigger fallbacks (the
`disable_fallbacks` autouse fixture prevents this by default).

## The Fundamental Rule

```
Normal test  →  disable_fallbacks autouse fixture applies automatically
                  Do NOT request enable_fallbacks
                  If a fallback fires anyway, fix the underlying issue

Fallback test → request enable_fallbacks fixture explicitly
                  Assert pytest.warns(UserWarning) is raised
                  Assert the operation still produced correct output
```

## Minimal Template

```python
import pytest

def test_should_<succeed_via_fallback>_when_<trigger_condition>(enable_fallbacks):
    """Validates the <X> → <Y> fallback path fires and emits a UserWarning."""
    # Arrange: set up the condition that triggers the fallback
    # (e.g., make a plugin unavailable, force a backend error, etc.)

    # Act + Assert: warn AND correct output
    with pytest.warns(UserWarning, match="<expected fragment from warning message>"):
        result = <operation_under_test>()

    # Assert the output is still correct (not just that it completed)
    assert result is not None          # execution-only — add semantic assertion too
    assert <domain_invariant_holds>    # e.g., interval invariant
```

## Known Fallback Warning Messages (match= fragments)

| Fallback | Match fragment |
|---|---|
| Parallel → sequential execution | `"fallback"` or `"sequential"` |
| Cache backend → minimal LRU | `"Cache backend fallback"` |
| Visualization → simplified bar | `"Visualization fallback"` |
| Plugin execution error → legacy path | `"legacy"` or `"fallback"` |
| Perturbation fallback | `"perturbation"` |

Use `match=` with a substring, not the full message, to avoid brittleness:
```python
with pytest.warns(UserWarning, match="fallback"):
    ...
```

## INFO Log Side-Effect (mandatory per Fallback Visibility Policy)

Every fallback must also emit an INFO log. Assert it when testable:

```python
import logging

def test_should_log_fallback_decision_when_plugin_fails(enable_fallbacks, caplog):
    with caplog.at_level(logging.INFO, logger="calibrated_explanations"):
        with pytest.warns(UserWarning):
            result = explainer.explain_factual(X_query)

    # Assert both the warning (user-visible) and the log (observability)
    assert any("fallback" in record.message.lower() for record in caplog.records)
    assert result is not None
```

## Full Example: Parallel → Sequential Fallback

```python
def test_should_explain_factual_when_parallel_backend_unavailable(
    enable_fallbacks, binary_explainer, monkeypatch
):
    """Parallel execution failure falls back to sequential and emits UserWarning."""
    # Arrange: force the parallel backend to raise on submission
    def broken_submit(*args, **kwargs):
        raise RuntimeError("Mock parallel backend failure")

    monkeypatch.setattr(
        "calibrated_explanations.parallel.backend.submit",
        broken_submit
    )

    # Act + Assert
    with pytest.warns(UserWarning, match="fallback"):
        explanations = binary_explainer.explain_factual(X_query[:2])

    # Semantic assertion: output is still valid
    for exp in explanations:
        assert exp.prediction['low'] <= exp.prediction['predict']
        assert exp.prediction['predict'] <= exp.prediction['high']
```

## Full Example: Cache Backend Fallback

```python
def test_should_use_minimal_cache_when_primary_backend_unavailable(
    enable_fallbacks, monkeypatch
):
    """Cache backend failure falls back to in-package LRU and emits UserWarning."""
    import calibrated_explanations.cache as cache_mod

    # Arrange: corrupt the primary backend
    monkeypatch.setattr(cache_mod, "_primary_backend", None)

    with pytest.warns(UserWarning, match="Cache backend fallback"):
        explanations = explainer.explain_factual(X_query)

    assert explanations is not None
```

## What NOT to Do

```python
# ❌ WRONG: accessing enable_fallbacks in a test that has no fallback code path
def test_explain_factual_basic(enable_fallbacks):
    explainer.explain_factual(X_query)   # no fallback triggered; fixture is wasteful

# ❌ WRONG: asserting a fallback fires but not checking the output is still correct
def test_fallback_fires(enable_fallbacks):
    with pytest.warns(UserWarning):
        pass   # empty act — what is being tested?

# ❌ WRONG: swallowing the fallback warning silently
def test_fallback_fires(enable_fallbacks):
    result = explainer.explain_factual(X_query)
    # No pytest.warns; warning is not asserted — this is an incomplete fallback test
```

## Out of Scope

- Writing standard (non-fallback) tests (see `ce-test-author`).
- Implementing a new fallback (see `ce-fallback-impl`).
- Auditing whether existing tests wrongly trigger fallbacks (see `ce-test-audit`).

## Evaluation Checklist

- [ ] `enable_fallbacks` fixture requested.
- [ ] `pytest.warns(UserWarning, match=...)` wraps the act section.
- [ ] At least one semantic domain assertion on the output.
- [ ] INFO log side-effect asserted via `caplog` when feasible.
- [ ] `match=` uses a substring, not the full warning message.
- [ ] Test name follows `test_should_<succeed_via_fallback>_when_<trigger>`.
