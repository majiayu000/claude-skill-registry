---
name: narwhals
description: Effectively use Narwhals to write dataframe-agnostic code that works seamlessly across multiple Python dataframe libraries. Write correct type annotations for code using Narwhals.
---

# Narwhals - DataFrame Agnostic API

Narwhals is a lightweight, zero-dependency compatibility layer for dataframe libraries in Python that provides a unified interface across different backends.

Docs: https://narwhals-dev.github.io/narwhals/

## What is Narwhals?

Narwhals enables writing dataframe-agnostic code that works seamlessly across multiple Python dataframe libraries:

**Full API Support:**

- cuDF
- Modin
- pandas
- Polars
- PyArrow

**Lazy-Only Support:**

- Dask
- DuckDB
- Ibis
- PySpark
- SQLFrame

## Core Philosophy

**Why Narwhals?**

- Resolves subtle differences between libraries (e.g., pandas checking index vs Polars checking values)
- Provides unified, simple, and predictable API
- Handles backwards compatibility internally
- Tests against nightly builds of supported libraries
- Maintains negligible performance overhead
- Full static typing support
- Zero dependencies

**Target Use Case:**
Anyone building libraries, applications, or services that consume dataframes and need complete backend independence.

## Key Features

1. **Backend Agnostic**: Write once, run on any supported dataframe library
2. **Polars-Like API**: Uses a subset of the Polars API for consistency
3. **Lazy & Eager Execution**: Separate APIs for both execution modes
4. **Expression Support**: Full expression API for complex operations
5. **Type Safety**: Perfect static typing support
6. **100% Branch Coverage**: Thoroughly tested

## Basic Usage Pattern

### Three-Step Workflow

```python
import narwhals as nw

# 1. Convert to Narwhals
df_nw = nw.from_native(df)  # Works with pandas, Polars, PyArrow, etc.

# 2. Perform operations using Polars-like API
result = df_nw.select(a_sum=nw.col("a").sum(), a_mean=nw.col("a").mean(), b_std=nw.col("b").std())

# 3. Convert back to original library
result_native = result.to_native()
```

### Using the @narwhalify Decorator

Simplifies function definitions for automatic conversion:

```python
@nw.narwhalify
def my_func(df: IntoDataFrameT):
    return df.select(nw.col("a").sum(), nw.col("b").mean()).filter(nw.col("a") > 0)


# Automatically handles conversion to/from Narwhals
result = my_func(pandas_df)  # Works!
result = my_func(polars_df)  # Also works!
```

## Top-Level Functions

### Conversion Functions

- `from_native(df, ...)`: Convert native DataFrame/Series to Narwhals object
  - Parameters: `pass_through`, `backend`, `eager_only`, `allow_series`
- `to_native(nw_obj)`: Convert Narwhals object back to native library type
- `narwhalify()`: Decorator for automatic dataframe-agnostic functions

### Data Creation

- `new_series(name, values, dtype)`: Create a new Series
- `from_dict(data)`: Create DataFrame from dictionary
- `from_dicts(data)`: Create DataFrame from sequence of dictionaries

### File I/O

**Eager Loading:**

- `read_csv(source, **kwargs)`: Read CSV file into DataFrame
- `read_parquet(source, **kwargs)`: Read Parquet file into DataFrame

**Lazy Loading:**

- `scan_csv(source, **kwargs)`: Lazily scan CSV file
- `scan_parquet(source, **kwargs)`: Lazily scan Parquet file

### Aggregation Functions

- `sum()`, `mean()`, `min()`, `max()`, `median()`
- `sum_horizontal()`, `mean_horizontal()`, etc.

### Expression Creation

- `col(name)`: Reference column by name
- `lit(value)`: Create literal expression
- `when(condition)`: Create conditional expression
- `format(template, *args)`: Format expression as string

### Utilities

- `generate_temporary_column_name()`: Generate unique column names
- `get_native_namespace(obj)`: Get the native library of an object
- `show_versions()`: Print debugging information

## DataFrame Methods

### Properties

- `columns`: List of column names
- `schema`: Ordered mapping of column names to dtypes
- `shape`: Tuple of (rows, columns)
- `implementation`: Name of native implementation

### Column Operations

- `select(*exprs)`: Select columns using expressions
- `with_columns(*exprs)`: Add or modify columns
- `drop(*columns)`: Remove specified columns
- `rename(mapping)`: Rename columns

### Row Operations

- `filter(predicate)`: Filter rows based on conditions
- `head(n)`: Get first n rows
- `tail(n)`: Get last n rows
- `sample(n)`: Randomly sample n rows
- `drop_nulls()`: Drop rows with null values
- `unique()`: Remove duplicate rows

### Inspection

- `is_empty()`: Check if DataFrame has no rows
- `is_duplicated()`: Identify duplicated rows
- `is_unique()`: Identify unique rows
- `null_count()`: Count null values per column
- `estimated_size()`: Estimate memory usage

### Transformations

- `sort(*by)`: Sort by one or more columns
- `group_by(*by)`: Group by columns for aggregation
- `join(other, on, how)`: Perform SQL-style joins
- `pivot(on, index, values)`: Create pivot table
- `explode(*columns)`: Expand list columns to long format
- `lazy()`: Convert to LazyFrame

### Export

- `to_native()`: Convert to original library type
- `to_numpy()`: Convert to NumPy array
- `to_pandas()`: Convert to pandas DataFrame
- `to_polars()`: Convert to Polars DataFrame
- `clone()`: Create a copy

## LazyFrame Methods

LazyFrame provides the same API as DataFrame but with lazy evaluation:

### Key Differences

- Operations build an execution plan without computing
- `collect()`: Materialize the LazyFrame into a DataFrame
- `collect_schema()`: Get schema without collecting data
- `sink_parquet(path)`: Write results directly to Parquet

### Common Methods

All DataFrame methods are available on LazyFrame:

- `select()`, `filter()`, `with_columns()`, `drop()`
- `group_by()`, `join()`, `sort()`, `unique()`
- `head()`, `tail()`, `top_k()`
- `gather_every()`: Select rows at regular intervals
- `unpivot()`: Convert from wide to long format
- `with_row_index()`: Add row index column
- `pipe()`: Apply function to LazyFrame

## Expression (Expr) API

Expressions are the building blocks for column operations.

### Creation

```python
nw.col("column_name")  # Reference column
nw.lit(42)  # Literal value
```

### Filtering

- `filter(predicate)`: Filter elements
- `is_in(values)`: Check membership
- `is_between(lower, upper)`: Check range
- `drop_nulls()`: Remove nulls

### Aggregations

- `count()`: Count non-null elements
- `null_count()`: Count null values
- `n_unique()`: Count unique values
- `sum()`, `mean()`, `median()`: Statistical aggregations
- `min()`, `max()`: Extremes
- `std()`, `var()`: Spread measures
- `quantile(q)`: Quantile values

### Transformations

**Mathematical:**

- `abs()`: Absolute value
- `round()`, `floor()`, `ceil()`: Rounding
- `sqrt()`, `log()`, `exp()`: Mathematical functions

**Type/Value Operations:**

- `cast(dtype)`: Change data type
- `fill_null(value)`: Replace null values
- `replace_strict(old, new)`: Replace specific values

**Window Operations:**

- `rolling_mean(window_size)`: Moving average
- `rolling_sum(window_size)`: Moving sum
- `rolling_std(window_size)`: Moving standard deviation
- `shift(n)`: Shift values by n positions
- `over(*by)`: Compute expression over groups

**Ranking/Uniqueness:**

- `rank()`: Assign ranks
- `unique()`: Get unique values
- `is_duplicated()`: Identify duplicates
- `is_first_distinct()`: Mark first distinct occurrences

### Namespace Methods

Expressions have specialized namespaces for specific data types:

**String Operations (`Expr.str`)**

- String manipulation methods

**DateTime Operations (`Expr.dt`)**

- Date/time manipulation methods

**List Operations (`Expr.list`)**

- List column operations

**Categorical Operations (`Expr.cat`)**

- Categorical data methods

**Struct Operations (`Expr.struct`)**

- Struct/nested data methods

**Name Operations (`Expr.name`)**

- Column name operations

## Series API

Series represents a single column:

### Properties

- Same as DataFrame: `shape`, `dtype`, `name`

### Methods

- Similar to DataFrame but for single column operations
- Has specialized namespaces: `str`, `dt`, `list`, `cat`, `struct`

## Type Hints

Full docs: [narwhals.typing](https://narwhals-dev.github.io/narwhals/api-reference/typing/)

TLDR:

DataFrameT module-attribute

DataFrameT = TypeVar('DataFrameT', bound='DataFrame[Any]')
TypeVar bound to Narwhals DataFrame.

Use this if your function can accept a Narwhals DataFrame and returns a Narwhals DataFrame backed by the same backend.

Examples:

```py
>>> import narwhals as nw
>>> from narwhals.typing import DataFrameT
>>> @nw.narwhalify
>>> def func(df: DataFrameT) -> DataFrameT:
...     return df.with_columns(c=df["a"] + 1)
Frame module-attribute
```

Frame: TypeAlias = Union["DataFrame[Any]", "LazyFrame[Any]"]
Narwhals DataFrame or Narwhals LazyFrame.

Use this if your function can work with either and your function doesn't care about its backend.

Examples:

```py
>>> import narwhals as nw
>>> from narwhals.typing import Frame
>>> @nw.narwhalify
... def agnostic_columns(df: Frame) -> list[str]:
...     return df.columns
FrameT module-attribute
```

FrameT = TypeVar(
"FrameT", "DataFrame[Any]", "LazyFrame[Any]"
)
TypeVar bound to Narwhals DataFrame or Narwhals LazyFrame.

Use this if your function accepts either nw.DataFrame or nw.LazyFrame and returns an object of the same kind.

Examples:

```py
>>> import narwhals as nw
>>> from narwhals.typing import FrameT
>>> @nw.narwhalify
... def agnostic_func(df: FrameT) -> FrameT:
...     return df.with_columns(c=nw.col("a") + 1)
```

IntoDataFrame module-attribute

IntoDataFrame: TypeAlias = NativeDataFrame
Anything which can be converted to a Narwhals DataFrame.

Use this if your function accepts a narwhalifiable object but doesn't care about its backend.

Examples:

```py
>>> import narwhals as nw
>>> from narwhals.typing import IntoDataFrame
>>> def agnostic_shape(df_native: IntoDataFrame) -> tuple[int, int]:
...     df = nw.from_native(df_native, eager_only=True)
...     return df.shape
```

IntoDataFrameT module-attribute

IntoDataFrameT = TypeVar(
"IntoDataFrameT", bound=IntoDataFrame
)
TypeVar bound to object convertible to Narwhals DataFrame.

Use this if your function accepts an object which can be converted to nw.DataFrame and returns an object of the same class.

Examples:

```py
>>> import narwhals as nw
>>> from narwhals.typing import IntoDataFrameT
>>> def agnostic_func(df_native: IntoDataFrameT) -> IntoDataFrameT:
...     df = nw.from_native(df_native, eager_only=True)
...     return df.with_columns(c=df["a"] + 1).to_native()
```

## Common Patterns

### Group By and Aggregate

```python
result = df.group_by("category").agg(
    count=nw.col("id").count(),
    total=nw.col("amount").sum(),
    average=nw.col("amount").mean(),
)
```

### Conditional Operations

```python
result = df.with_columns(category=nw.when(nw.col("value") > 100).then(nw.lit("high")).otherwise(nw.lit("low")))
```

### Joins

```python
result = df1.join(
    df2,
    on="key_column",
    how="left",  # inner, left, outer, cross
)
```

### Chain Operations

```python
result = (
    df.filter(nw.col("status") == "active")
    .select("user_id", "amount")
    .group_by("user_id")
    .agg(total=nw.col("amount").sum())
    .sort("total", descending=True)
    .head(10)
)
```

## Best Practices

1. **Use `@nw.narwhalify` for library functions**: Simplifies API and handles conversion automatically

2. **Prefer expressions over method chaining**: More flexible and composable
   ```python
   # Good
   df.select(nw.col("a").sum(), nw.col("b").mean())

   # Also fine, but less composable
   df.select("a", "b")
   ```

3. **Use lazy evaluation when possible**: Better performance for complex pipelines
   ```python
   result = df.lazy().select(...).filter(...).collect()
   ```

4. **Always convert back to native**: Remember to call `.to_native()` when returning from library functions (unless using `@narwhalify`)

5. **Type hint your functions**: Use `IntoDataFrame` and `FrameT` for better IDE support

6. **Check supported backends**: Some operations may not be available on all backends

## Important Constraints

1. **Zero Dependencies**: Narwhals has no dependencies, keeping it lightweight

2. **Polars API Subset**: Uses Polars-style API but may not support all Polars features

3. **Backend Limitations**: Some backends (lazy-only) have restricted functionality

## Tips

Checking whether a Narwhals frame is a Polars frame:

```py
import polars as pl
import narwhals as nw

df_native = pl.DataFrame({"a": [1, 2, 3]})
df = nw.from_native(df_native)
df.implementation.is_polars()
```

Asserting series equality:

```py
import pandas as pd
import narwhals as nw
from narwhals.testing import assert_series_equal
s1 = nw.from_native(pd.Series([1, 2, 3]), series_only=True)
s2 = nw.from_native(pd.Series([1, 5, 3]), series_only=True)
assert_series_equal(s1, s2)
Traceback (most recent call last):
...
AssertionError: Series are different (exact value mismatch)
[left]:
┌───────────────┐
|Narwhals Series|
|---------------|
| 0    1        |
| 1    2        |
| 2    3        |
| dtype: int64  |
└───────────────┘
[right]:
┌───────────────┐
|Narwhals Series|
|---------------|
| 0    1        |
| 1    5        |
| 2    3        |
| dtype: int64  |
└───────────────┘
```
