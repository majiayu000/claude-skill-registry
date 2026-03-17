---
name: hypothesis
description: Use Hypothesis for property-based testing to automatically generate comprehensive test cases, find edge cases, and write more robust tests with minimal example shrinking. Includes Polars parametric testing integration.
---

# Hypothesis - Property-Based Testing

Property-based testing framework that generates test cases automatically, finds minimal failing examples through shrinking, and verifies invariants.

**Official Docs:** https://hypothesis.readthedocs.io/en/latest/

**Key Features:**

- Automatic test data generation from strategies
- Minimal failing example shrinking
- Stateful testing with rule-based state machines
- pytest integration
- Deterministic reproducibility

## Quick Start

```python
from hypothesis import given
from hypothesis import strategies as st


@given(st.integers())
def test_property(x):
    """Test properties that should always hold"""
    assert abs(x) >= 0


@given(st.lists(st.integers()))
def test_list_property(lst):
    sorted_lst = sorted(lst)
    assert len(sorted_lst) == len(lst)
    # Check monotonic property
    for i in range(len(sorted_lst) - 1):
        assert sorted_lst[i] <= sorted_lst[i + 1]
```

## Strategies

**Full reference:** https://hypothesis.readthedocs.io/en/latest/data.html

Common strategies:

- Primitives: `st.integers()`, `st.floats()`, `st.text()`, `st.booleans()`
- Collections: `st.lists()`, `st.dictionaries()`, `st.tuples()`, `st.sets()`
- Dates/Times: `st.dates()`, `st.datetimes()`, `st.timedeltas()`
- Combinators: `st.one_of()`, `st.sampled_from()`, `st.recursive()`
- Type-based: `st.from_type(MyClass)`

### Composite Strategies

```python
from hypothesis import strategies as st
from hypothesis.strategies import composite


@composite
def user_strategy(draw):
    age = draw(st.integers(min_value=18, max_value=100))
    name = draw(st.text(min_size=1))
    return {"name": name, "age": age, "is_adult": age >= 18}


@given(user_strategy())
def test_user(user):
    assert user["is_adult"] == (user["age"] >= 18)
```

### Strategy Combinators

```python
st.integers().filter(lambda x: x % 2 == 0)  # Filter
st.integers().map(str)  # Transform
st.one_of(st.integers(), st.text())  # Choose between strategies
st.sampled_from([1, 2, 3, 4, 5])  # Pick from collection
st.from_type(MyClass)  # Infer from type hints
st.builds(MyClass, arg1=st.integers())  # Build instances
```

## Settings

```python
from hypothesis import given, settings
from hypothesis import strategies as st


@given(st.integers())
@settings(
    max_examples=1000,  # Default: 100
    deadline=None,  # Remove time limit
    derandomize=True,  # Deterministic ordering
)
def test_example(x):
    pass


# Profiles for different environments
settings.register_profile("dev", max_examples=10)
settings.register_profile("ci", max_examples=1000, deadline=None)
# Activate: HYPOTHESIS_PROFILE=ci pytest
```

**Full settings reference:** https://hypothesis.readthedocs.io/en/latest/settings.html

## Helpers

```python
from hypothesis import given, assume, note, example, seed


@given(st.integers(), st.integers())
def test_division(x, y):
    assume(y != 0)  # Skip invalid cases (prefer .filter() instead)
    note(f"Testing {x} / {y}")  # Add debug info
    assert (x / y) * y == x


@given(st.integers())
@example(0)  # Always test specific cases
@seed(12345)  # Reproducible run
def test_something(x):
    pass
```

## Stateful Testing

For testing complex stateful systems with rule-based state machines.

```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from hypothesis import strategies as st


class MyStateMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.data = []

    @rule(value=st.integers())
    def add(self, value):
        self.data.append(value)

    @invariant()
    def check_invariant(self):
        assert isinstance(self.data, list)


TestMachine = MyStateMachine.TestCase
```

**Full stateful testing guide:** https://hypothesis.readthedocs.io/en/latest/stateful.html

## Polars Integration

Polars provides built-in parametric testing strategies for generating DataFrames.

**Official docs:** https://docs.pola.rs/api/python/stable/reference/api/polars.testing.parametric.dataframes.html

```python
from hypothesis import given
import polars as pl
from polars.testing.parametric import dataframes, column


# Generate DataFrames with specific column schemas
@given(
    dataframes(
        cols=[
            column("id", dtype=pl.Int64),
            column("name", dtype=pl.String),
            column("value", dtype=pl.Float64),
        ],
        min_size=1,
        max_size=100,
    )
)
def test_dataframe_property(df: pl.DataFrame):
    """Test properties of DataFrame operations"""
    assert df.shape[0] >= 1
    assert set(df.columns) == {"id", "name", "value"}
    assert df["id"].dtype == pl.Int64


# With Narwhals wrapper
import narwhals as nw


@given(dataframes(cols=[column("a", dtype=pl.Int64)]))
def test_narwhals_operation(df: pl.DataFrame):
    nw_df = nw.from_native(df)
    result = nw_df.select(nw.col("a") * 2)
    assert result.shape[0] == nw_df.shape[0]
```

**Key functions:**

- `dataframes()`: Generate DataFrames with specified columns
- `column(name, dtype, ...)`: Define column schemas with constraints
- `series()`: Generate standalone Series

**Column constraints:**

- `null_probability`: Control null value frequency
- `min_size`/`max_size`: Control row count
- `allow_null`: Enable/disable nulls
- `unique`: Generate unique values
- `strategy`: Custom strategy for column values

## Best Practices

- **Use constraints over filters**: `st.integers(min_value=0)` not `st.integers().filter(lambda x: x >= 0)`
- **Test properties, not examples**: Focus on invariants that always hold
- **Combine with `@example()`**: Test specific edge cases explicitly
- **Avoid `assume()` overuse**: Makes tests slow; use filtered strategies
- **Document properties**: Clear docstrings explain what invariant is tested
- **Set size limits**: Always bound collection sizes to prevent memory issues
- **Use `.hypothesis/` in `.gitignore`**: Stores example database locally

## Troubleshooting

Common issues and solutions:

- **HealthCheck failures**: Too many rejected examples → use constrained strategies or `suppress_health_check`
- **Flaky tests**: Non-deterministic code → use `@seed()` or `@settings(derandomize=True)`
- **Slow tests**: Too many examples → reduce `max_examples` or use profiles
- **Deadline exceeded**: Complex operations → increase `deadline` or set to `None`

## Resources

- Main docs: https://hypothesis.readthedocs.io/
- Strategies: https://hypothesis.readthedocs.io/en/latest/data.html
- Stateful testing: https://hypothesis.readthedocs.io/en/latest/stateful.html
- Ghost writer (auto-generate tests): `hypothesis write mymodule.myfunction`
