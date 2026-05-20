---
name: ce-test-author
description: >
  Write individual CE test cases for specified modules or behaviors using AAA
  structure, public-API focus, and coverage-gate discipline. Does NOT identify
  coverage gaps; use ce-test-creator for gap-driven test design.
---

# CE Test Author

You are writing tests for `calibrated_explanations`. This skill encodes the
full `tests/README.md` rubric. For any ambiguity, the README is authoritative.

## Quick Decision Tree: Where to Put the Test

```
What are you testing?
├── A single function / class in src/ without external I/O
│   → tests/unit/<package>/test_<module>.py
│
├── The interaction of two+ modules, or CE pipeline end-to-end
│   → tests/integration/<feature>/test_<feature>.py
│
└── A full user workflow (notebook-style, CLI, or API surface)
    → tests/e2e/<flow>/test_<flow>.py
```

**Before creating a new file**, look for the nearest existing test file:
- `tests/unit/core/` for `src/calibrated_explanations/core/`
- `tests/unit/plugins/` for `src/calibrated_explanations/plugins/`
- `tests/integration/` for cross-module feature tests
- Creating a new file requires "Why a new test file?" justification in the PR.

## Naming Convention (mandatory)

```python
def test_should_<behavior>_when_<condition>():
    ...
```

Examples:
- `test_should_return_calibrated_probability_when_explainer_is_fitted`
- `test_should_raise_not_fitted_error_when_calibrate_called_before_fit`
- `test_should_preserve_interval_invariant_when_explain_factual_called`

## AAA Structure Template

```python
def test_should_<behavior>_when_<condition>(fixture_A, fixture_B):
    """One-line docstring: behavior under test."""
    # Arrange
    explainer = WrapCalibratedExplainer(model)
    explainer.fit(x_proper, y_proper)
    explainer.calibrate(x_cal, y_cal)

    # Act
    explanations = explainer.explain_factual(X_query)

    # Assert
    assert explanations[0].prediction['low'] <= explanations[0].prediction['predict']
    assert explanations[0].prediction['predict'] <= explanations[0].prediction['high']
```

One logical assertion block per behavior. Do not mix multiple unrelated
behaviors in a single test function.

## Determinism Requirements

- No real network, clock access, or uncontrolled randomness.
- Seed RNG explicitly: `np.random.seed(42)` in the Arrange section, or use a
  `rng` fixture.
- Freeze time when testing anything that reads `datetime.now()` or similar.
- If a test uses a `tmp_path` fixture for file I/O, that's correct; do not use
  hardcoded paths.

## CE-Specific Fixtures

Standard fixtures available in `tests/conftest.py`:

```python
# Disable fallback chains (DEFAULT — autouse)
# You do NOT need to request this; it is applied automatically.
# It ensures tests fail on the primary code path, not a silent fallback.

# Enable fallback chains (only when TESTING fallback behavior)
def test_my_fallback_behavior(enable_fallbacks):
    ...
```

For CE pipeline tests, use existing dataset/model fixtures from conftest rather
than constructing them inline — keeps tests faster and consistent.

## Testing Fallback Behavior

When a test exists specifically to validate a fallback chain:

```python
def test_should_fallback_to_sequential_when_parallel_plugin_raises(enable_fallbacks):
    """Validates that the parallel→sequential fallback fires and emits a warning."""
    # Arrange: instrument to trigger the failure path
    ...

    # Act + Assert: both the warning AND the correct output
    with pytest.warns(UserWarning, match="fallback"):
        result = explainer.explain_factual(X_query)

    assert result is not None   # execution completed via fallback
```

**Never use `enable_fallbacks` for non-fallback tests.** If your test would
pass only because a fallback silently rescued it, fix the underlying issue.

## What NOT to Test (Anti-Patterns — see ADR-030)

| Anti-pattern | Why | Fix |
|---|---|---|
| `assert "predict" in d` | Dict keys, not behavior | Assert `d['low'] <= d['predict']` |
| `assert hasattr(obj, 'fitted')` | Attribute presence | Assert `explainer.fitted is True` after fit |
| Calling `_private_func()` directly | Implementation detail | Test through public API |
| `assert result is not None` only | Execution-only assertion | Add a semantic assertion too |
| Identical copy-pasted tests | Semantic redundancy | Parametrize with `@pytest.mark.parametrize` |
| `import datetime; datetime.now()` unpatched | Non-determinism | Mock with `monkeypatch` |

## Coverage Gate

```bash
pytest --cov=src/calibrated_explanations --cov-config=pyproject.toml --cov-fail-under=90
```

- Keep unit tests under 100 ms; integration tests under 2 s.
- Mark slow tests: `@pytest.mark.slow`.
- Visualization tests: `@pytest.mark.viz` (ADR-023 exemption applies).

## Parametrized Tests

Use `@pytest.mark.parametrize` instead of copy-pasting for variations:

```python
@pytest.mark.parametrize("percentiles,expected_width", [
    ((5, 95), "wide"),
    ((25, 75), "narrow"),
])
def test_should_produce_correct_interval_width_when_percentiles_set(
    percentiles, expected_width, binary_explainer
):
    explanations = binary_explainer.explain_factual(
        X_query, low_high_percentiles=percentiles
    )
    width = explanations[0].prediction['high'] - explanations[0].prediction['low']
    if expected_width == "wide":
        assert width > 0
    else:
        assert width > 0   # both are valid; assert invariant holds
    assert explanations[0].prediction['low'] <= explanations[0].prediction['predict']
```

## CE Interval Invariant (mandatory assertion for any prediction test)

Always assert `low ≤ predict ≤ high` when testing CE predictions:

```python
pred = explanations[i].prediction
assert pred['low'] <= pred['predict'], "Interval invariant violated (low)"
assert pred['predict'] <= pred['high'], "Interval invariant violated (high)"
```

## Snapshot / Serialization Tests

Combine round-trip with semantic assertion — never test only keys:

```python
def test_should_preserve_interval_invariant_when_serialized_and_deserialized():
    explanations = explainer.explain_factual(X_query)
    d = explanations[0].to_dict()
    restored = CalibratedExplanation.from_dict(d)
    # Semantic, not structural:
    pred = restored.prediction
    assert pred['low'] <= pred['predict'] <= pred['high']
```

## Evaluation Checklist (self-verify)

- [ ] Test placed in correct directory (`unit/`, `integration/`, `e2e/`).
- [ ] Naming follows `test_should_<behavior>_when_<condition>`.
- [ ] AAA structure with one logical assertion block.
- [ ] No real network/clock/randomness; RNG seeded.
- [ ] `enable_fallbacks` NOT used unless test validates a fallback.
- [ ] At least one semantic assertion (not just presence/type checks).
- [ ] CE interval invariant asserted for any prediction-involving test.
- [ ] No `_private` API calls.
- [ ] Coverage gate will be satisfied (no new uncovered branches left).
