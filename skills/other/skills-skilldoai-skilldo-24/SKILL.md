---
name: pandas
description: Data manipulation and analysis library providing DataFrame and Series structures for working with structured data
version: 3.0.0
ecosystem: python
license: BSD-3-Clause
generated_with: claude-sonnet-4-5-20250929
---

## Imports

```python
import pandas as pd
from pandas import DataFrame, Series, Index
from pandas import read_csv, read_excel, read_json, read_sql, read_parquet, read_pickle
from pandas import Timestamp, Timedelta, Period
from pandas import get_option, set_option, option_context
from pandas import NA, NaT
from pandas import concat, merge, pivot_table, melt
from pandas import cut, qcut, get_dummies
from pandas import to_datetime, to_timedelta, to_numeric
from pandas import isna, isnull, notna, notnull
from pandas import date_range, timedelta_range, period_range, interval_range
```

## Core Patterns

### Creating DataFrames ✅ Current
```python
import pandas as pd

# From dictionary
df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'city': ['NYC', 'SF', 'LA']
})

# From CSV file
df = pd.read_csv('data.csv', index_col=0)

# From Excel file
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# From JSON
df = pd.read_json('data.json', orient='records')

# From Parquet
df = pd.read_parquet('data.parquet')

# From pickle
df = pd.read_pickle('data.pkl')
```
* DataFrames are two-dimensional labeled data structures with columns of potentially different types
* Use `read_*` functions for loading data from various file formats
* Specify `index_col` to set which column becomes the row index
* `copy` parameter default changed in v3.0 - see Migration section

### Creating Series ✅ Current
```python
import pandas as pd

# From list with index
s = pd.Series([10, 20, 30], index=['a', 'b', 'c'], name='values')

# From dictionary
s = pd.Series({'a': 10, 'b': 20, 'c': 30})

# Extracting from DataFrame
df = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]})
s = df['col1']  # Returns Series
```
* Series are one-dimensional labeled arrays capable of holding any data type
* Index provides labels for fast lookup
* Series maintain their name attribute for identification
* `copy` parameter default changed in v3.0 - see Migration section

### Data Selection and Filtering ✅ Current
```python
import pandas as pd

df = pd.DataFrame({
    'name': ['Alice', 'Bob', 'Charlie'],
    'age': [25, 30, 35],
    'score': [85, 90, 88]
})

# Select single column (returns Series)
ages = df['age']

# Select multiple columns (returns DataFrame)
subset = df[['name', 'age']]

# Boolean filtering
adults = df[df['age'] >= 30]

# Multiple conditions
high_scorers = df[(df['age'] >= 25) & (df['score'] >= 85)]

# Using .loc for label-based indexing
row = df.loc[0]  # First row by index label
value = df.loc[0, 'name']  # Specific cell

# Using .iloc for position-based indexing
row = df.iloc[0]  # First row by position
value = df.iloc[0, 1]  # First row, second column
```
* Use bracket notation for column selection
* Boolean indexing filters rows based on conditions
* `.loc[]` uses labels, `.iloc[]` uses integer positions
* Combine conditions with `&` (and), `|` (or), `~` (not) - wrap each condition in parentheses
* Note: Copy-on-Write behavior changed in v3.0 - selections always return copies

### Working with Time Series ✅ Current
```python
import pandas as pd

# Create Timestamp
ts = pd.Timestamp('2024-01-15 14:30:00')
ts = pd.Timestamp(year=2024, month=1, day=15, hour=14, minute=30)

# Create DatetimeIndex
dates = pd.date_range('2024-01-01', periods=10, freq='D')
df = pd.DataFrame({'value': range(10)}, index=dates)

# Create Timedelta
td = pd.Timedelta('2 days')
td = pd.Timedelta(days=2, hours=3)

# Create TimedeltaIndex
deltas = pd.timedelta_range(start='1 day', periods=5, freq='D')

# Create Period
p = pd.Period('2024-01', freq='M')

# Create PeriodIndex
periods = pd.period_range('2024-01', periods=12, freq='M')

# Convert to datetime
df['date'] = pd.to_datetime(df['date_string'])

# Convert to timedelta
df['duration'] = pd.to_timedelta(df['duration_string'])
```
* `Timestamp` replaces Python's datetime.datetime with nanosecond precision
* `DatetimeIndex` enables time-based indexing and slicing
* `Timedelta` represents duration between two dates or times
* `Period` represents a span of time at a particular frequency
* Use `to_datetime()` and `to_timedelta()` for conversions

### Missing Values ✅ Current
```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    'A': [1, np.nan, 3],
    'B': [4, 5, pd.NA],
    'C': [7, pd.NaT, 9]
})

# Detect missing values
has_nulls = df.isna()  # or df.isnull()
has_values = df.notna()  # or df.notnull()

# Check for any nulls
any_nulls = df['A'].isna().any()

# Drop rows with any null values
df_clean = df.dropna()

# Fill null values
df_filled = df.fillna(0)
df_filled = df.fillna(method='ffill')  # Forward fill

# Use pandas NA for missing values
value = pd.NA  # Scalable missing value indicator
nat = pd.NaT  # Not-a-Time for datetime/timedelta
```
* Use `.isna()` or `.isnull()` to detect missing values (they are aliases)
* Use `.notna()` or `.notnull()` to detect non-missing values
* `pd.NA` is the recommended missing value indicator for nullable dtypes
* `pd.NaT` is used specifically for datetime/timedelta missing values
* Never compare to NaN directly with `==` - always use `.isna()`

### Combining DataFrames ✅ Current
```python
import pandas as pd

df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})

# Concatenate along rows (vertical stack)
result = pd.concat([df1, df2], axis=0)

# Concatenate along columns (horizontal stack)
result = pd.concat([df1, df2], axis=1)

# Merge (join) DataFrames
left = pd.DataFrame({'key': ['A', 'B'], 'value': [1, 2]})
right = pd.DataFrame({'key': ['A', 'B'], 'value': [3, 4]})

# Inner join
merged = pd.merge(left, right, on='key', how='inner')

# Left join
merged = pd.merge(left, right, on='key', how='left')

# Outer join
merged = pd.merge(left, right, on='key', how='outer')
```
* `concat()` stacks DataFrames along an axis
* `merge()` performs database-style joins
* Use `how` parameter to specify join type: 'inner', 'left', 'right', 'outer'
* Use `on` parameter to specify join key(s)

### Reshaping Data ✅ Current
```python
import pandas as pd

# Pivot table
df = pd.DataFrame({
    'date': ['2024-01', '2024-01', '2024-02', '2024-02'],
    'product': ['A', 'B', 'A', 'B'],
    'sales': [100, 150, 120, 180]
})

pivot = pd.pivot_table(df, values='sales', index='date', columns='product')

# Melt (unpivot) from wide to long format
melted = pd.melt(df, id_vars=['date'], value_vars=['product'], 
                 var_name='category', value_name='value')

# Create dummy variables (one-hot encoding)
df = pd.DataFrame({'color': ['red', 'blue', 'red', 'green']})
dummies = pd.get_dummies(df['color'], prefix='color')
```
* `pivot_table()` creates spreadsheet-style pivot tables
* `melt()` transforms wide format to long format
* `get_dummies()` creates dummy/indicator variables for categorical data

### Binning and Discretization ✅ Current
```python
import pandas as pd

data = pd.Series([1, 7, 5, 4, 6, 3, 9, 2, 8])

# Cut into equal-width bins
bins = pd.cut(data, bins=3, labels=['low', 'medium', 'high'])

# Cut with custom bin edges
bins = pd.cut(data, bins=[0, 3, 7, 10], labels=['low', 'medium', 'high'])

# Quantile-based discretization (equal-sized bins)
quantiles = pd.qcut(data, q=3, labels=['low', 'medium', 'high'])
```
* `cut()` bins values into discrete intervals with equal width
* `qcut()` bins values based on quantiles (equal frequency)
* Use `labels` parameter to assign custom category names

### Type Conversion ✅ Current
```python
import pandas as pd

df = pd.DataFrame({
    'numbers': ['1', '2', '3'],
    'dates': ['2024-01-01', '2024-01-02', '2024-01-03']
})

# Convert to numeric
df['numbers'] = pd.to_numeric(df['numbers'])

# Convert to datetime
df['dates'] = pd.to_datetime(df['dates'])

# Convert column dtype
df['numbers'] = df['numbers'].astype('int64')

# Convert to categorical
df['category'] = df['category'].astype('category')
```
* `to_numeric()` converts to numeric types with error handling
* `to_datetime()` converts to datetime with flexible parsing
* `astype()` explicitly converts dtypes
* Use `errors='coerce'` parameter to handle conversion failures

### Configuring Display Options ✅ Current
```python
import pandas as pd

# Get current option value
max_rows = pd.get_option('display.max_rows')

# Set option value
pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 50)
pd.set_option('display.precision', 2)

# Temporarily set options with context manager
with pd.option_context('display.max_rows', 10, 'display.max_columns', 5):
    print(df)  # Uses temporary settings

# Outside context, original settings restored

# Reset option to default
pd.reset_option('display.max_rows')

# Describe available options
pd.describe_option('display')  # All display options
pd.describe_option('display.max_rows')  # Specific option
```
* Use `get_option()` and `set_option()` for global configuration changes
* `option_context()` provides temporary settings that restore automatically
* Common options: `display.max_rows`, `display.max_columns`, `display.precision`, `display.width`

## Configuration

### Display Settings
```python
# Default values
pd.get_option('display.max_rows')  # 60
pd.get_option('display.max_columns')  # 20
pd.get_option('display.width')  # 80
pd.get_option('display.precision')  # 6

# Common customizations
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.float_format', '{:.2f}'.format)  # Format floats
```

### File Reading Options
```python
# CSV reading with common parameters
df = pd.read_csv(
    'data.csv',
    sep=',',  # Delimiter (default: ',')
    header=0,  # Row to use as column names (default: 'infer')
    index_col=0,  # Column to use as row index
    usecols=['col1', 'col2'],  # Columns to read
    dtype={'col1': int, 'col2': str},  # Column data types
    parse_dates=['date_col'],  # Parse as datetime
    na_values=['NA', 'null'],  # Additional NA values
    encoding='utf-8',  # File encoding
    nrows=1000,  # Number of rows to read
    skiprows=5  # Rows to skip at start
)
```

### Index and Data Types
```python
# Creating typed indexes
idx = pd.Index([1, 2, 3], dtype='int64', name='id')
cat_idx = pd.CategoricalIndex(['A', 'B', 'C'], name='category')
range_idx = pd.RangeIndex(start=0, stop=10, step=2)
multi_idx = pd.MultiIndex.from_tuples([('A', 1), ('A', 2), ('B', 1)])

# Creating categoricals
cat = pd.Categorical(['A', 'B', 'A', 'C'], categories=['A', 'B', 'C'], ordered=True)

# Creating intervals
interval = pd.Interval(left=0, right=5, closed='right')
interval_idx = pd.IntervalIndex.from_breaks([0, 1, 2, 3])
```

## Pitfalls

### Wrong: Using chained assignment
```python
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# This may not work as expected and raises SettingWithCopyWarning
df[df['A'] > 1]['B'] = 99
```
**Why:** Chained indexing creates intermediate copies, so assignment may not affect the original DataFrame.

### Right: Use .loc for assignment
```python
import pandas as pd
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Correctly modifies the original DataFrame
df.loc[df['A'] > 1, 'B'] = 99
```

### Wrong: Iterating over DataFrame rows with loops
```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Very slow for large DataFrames
results = []
for i in range(len(df)):
    results.append(df.iloc[i]['A'] + df.iloc[i]['B'])
```
**Why:** Row-by-row iteration is extremely slow and defeats pandas' vectorization.

### Right: Use vectorized operations
```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Much faster - operates on entire columns at once
df['result'] = df['A'] + df['B']
```

---

### Wrong: Not specifying dtype when creating structures
```python
import pandas as pd

# Mixed types cause object dtype (slow operations)
df = pd.DataFrame({'id': ['1', '2', '3'], 'value': [10, 20, 30]})
# df['id'].dtype is 'object', not efficient
```
**Why:** Object dtype prevents optimized operations and uses more memory.

### Right: Specify dtypes explicitly or convert after creation
```python
import pandas as pd

# Specify dtype at creation
df = pd.DataFrame({
    'id': pd.Series([1, 2, 3], dtype='int64'),
    'value': [10, 20, 30]
})

# Or convert after creation
df = pd.DataFrame({'id': ['1', '2', '3'], 'value': [10, 20, 30]})
df['id'] = df['id'].astype('int64')
```

---

### Wrong: Using inplace=True for method chaining
```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Cannot chain - inplace returns None
result = df.drop(columns=['B'], inplace=True).reset_index()  # Error!
```
**Why:** Methods with `inplace=True` return None, breaking method chains.

### Right: Avoid inplace, assign results
```python
import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# Chain operations naturally
result = df.drop(columns=['B']).reset_index(drop=True)

# Or assign back if needed
df = df.drop(columns=['B'])
```

## References

- [homepage](https://pandas.pydata.org)
- [documentation](https://pandas.pydata.org/docs/)
- [repository](https://github.com/pandas-dev/pandas)
- [changelog](https://pandas.pydata.org/pandas-docs/stable/whatsnew/index.html)
- [PyPI](https://pypi.org/project/pandas/)

## Migration from v2.x

### Copy Semantics Changed
**v2.x behavior:**
```python
df = pd.DataFrame({'A': [1, 2, 3]})
df2 = df[['A']]  # Creates view in many cases
df2.iloc[0, 0] = 99  # May modify original df
```

**v3.0 behavior:**
```python
df = pd.DataFrame({'A': [1, 2, 3]})
df2 = df[['A']]  # Always creates copy (Copy-on-Write enforced)
df2.iloc[0, 0] = 99  # Never modifies original df
```
**Migration:** Copy-on-Write (CoW) is now the default and only mode in pandas 3.0. All indexing operations that return a subset of data will return a new copy. If you need to modify the original DataFrame, use direct assignment with `.loc[]` or `.iloc[]` rather than chaining operations.

### Constructor Parameter Changes
The `copy` parameter behavior has changed in DataFrame and Series constructors:

**v2.x:**
```python
df = pd.DataFrame(data, copy=True)  # Explicitly copy data
```

**v3.0:**
```python
df = pd.DataFrame(data, copy=None)  # Default changed to None
# copy=None respects Copy-on-Write semantics
# copy=True still available but rarely needed with CoW
```
**Migration:** The default `copy=None` is sufficient for most cases under CoW. Only use `copy=True` if you need to ensure immediate physical copying of data.

### Deprecated Parameters Removed
Several long-deprecated parameters have been removed in v3.0:
- `infer_datetime_format` in `read_csv()` and similar functions (datetime format inference is now automatic)
- Various `convert_*` parameters in IO functions

**Migration:** Remove these parameters from your code. Datetime format inference happens automatically in v3.0.

### Index Constructor Changes
The `tupleize_cols` parameter default behavior may affect MultiIndex creation:

```python
# May need explicit handling for tuple columns
idx = pd.Index(data, tupleize_cols=True)  # Explicit if needed
```

### API Breaking Changes
Refer to the full changelog for comprehensive breaking changes: https://pandas.pydata.org/pandas-docs/stable/whatsnew/v3.0.0.html

Key areas to review:
- Copy-on-Write is now mandatory (no opt-out)
- Index and MultiIndex behavior changes
- DataFrame/Series constructor parameter defaults changed
- IO function parameter updates
- Deprecated method removals

## API Reference

### Core Data Structures
- **DataFrame(data=None, index=None, columns=None, dtype=None, copy=None)** - Two-dimensional labeled data structure with columns of potentially different types
- **Series(data=None, index=None, dtype=None, name=None, copy=None)** - One-dimensional labeled array capable of holding any data type

### Index Types
- **Index(data=None, dtype=None, copy=False, name=None, tupleize_cols=True)** - Immutable sequence used for indexing and alignment
- **RangeIndex(start=None, stop=None, step=None, dtype=None, copy=False, name=None)** - Memory-efficient index for monotonic integer ranges
- **MultiIndex(levels=None, codes=None, sortorder=None, names=None, dtype=None, copy=False, name=None, verify_integrity=True)** - Multi-level or hierarchical index object
- **DatetimeIndex(data=None, freq=None, tz=None, normalize=False, closed=None, ambiguous='raise', dayfirst=False, yearfirst=False, dtype=None, copy=False, name=None)** - Immutable ndarray of datetime64 data
- **TimedeltaIndex(data=None, unit=None, freq=None, closed=None, dtype=None, copy=False, name=None)** - Immutable ndarray of timedelta64 data
- **PeriodIndex(data=None, ordinal=None, freq=None, dtype=None, copy=False, name=None)** - Immutable ndarray holding ordinal values indicating regular periods in time
- **CategoricalIndex(data=None, categories=None, ordered=None, dtype=None, copy=False, name=None)** - Index based on categorical data
- **IntervalIndex(data, closed=None, dtype=None, copy=False, name=None, verify_integrity=True)** - Index of intervals closed on the same side

### Scalars
- **Timestamp(ts_input=None, freq=None, tz=None, unit=None, year=None, month=None, day=None, hour=None, minute=None, second=None, microsecond=None, nanosecond=None, tzinfo=None, fold=None)** - Pandas replacement for datetime.datetime with nanosecond precision
- **Timedelta(value=None, unit=None, **kwargs)** - Duration representing difference between two dates or times
- **Period(value=None, freq=None, ordinal=None, year=None, month=None, quarter=None, day=None, hour=None, minute=None, second=None)** - Represents a time period at a particular frequency
- **Interval(left, right, closed='right')** - Immutable object representing an interval
- **NA** - Scalar missing value indicator
- **NaT** - Pandas Not-A-Time, used to represent null dates/times

### Data Types
- **Categorical(values, categories=None, ordered=None, dtype=None, copy=True)** - Represents categorical variable for memory efficiency and operations

### IO Functions
- **read_csv(filepath_or_buffer, sep=',', delimiter=None, header='infer', names=None, index_col=None, usecols=None, dtype=None, ...)** - Read CSV file into DataFrame
- **read_excel(io, sheet_name=0, header=0, names=None, index_col=None, usecols=None, dtype=None, ...)** - Read Excel file into DataFrame
- **read_json(path_or_buf, orient=None, typ='frame', dtype=None, ...)** - Convert JSON to DataFrame or Series
- **read_sql(sql, con, index_col=None, coerce_float=True, params=None, parse_dates=None, columns=None, chunksize=None, dtype_backend=None, dtype=None)** - Read SQL query or table into DataFrame
- **read_parquet(path, engine='auto', columns=None, storage_options=None, use_nullable_dtypes=False, dtype_backend=None, filesystem=None, filters=None, **kwargs)** - Load parquet object into DataFrame
- **read_pickle(filepath_or_buffer, compression='infer', storage_options=None)** - Load pickled pandas object from file
- **to_pickle(obj, filepath_or_buffer, compression='infer', protocol=5, storage_options=None)** - Pickle (serialize) object to file

### Data Manipulation
- **concat(objs, axis=0, join='outer', ignore_index=False, keys=None, levels=None, names=None, verify_integrity=False, sort=False, copy=True)** - Concatenate pandas objects along a particular axis
- **merge(left, right, how='inner', on=None, left_on=None, right_on=None, left_index=False, right_index=False, sort=False, suffixes=('_x', '_y'), copy=True, indicator=False, validate=None)** - Merge DataFrame or named Series objects with database-style join
- **pivot_table(data, values=None, index=None, columns=None, aggfunc='mean', fill_value=None, margins=False, dropna=True, margins_name='All', observed=False, sort=True)** - Create spreadsheet-style pivot table as DataFrame
- **melt(frame, id_vars=None, value_vars=None, var_name=None, value_name='value', col_level=None, ignore_index=True)** - Unpivot DataFrame from wide to long format
- **cut(x, bins, right=True, labels=None, retbins=False, precision=3, include_lowest=False, duplicates='raise', ordered=True)** - Bin values into discrete intervals
- **qcut(x, q, labels=None, retbins=False, precision=3, duplicates='raise')** - Quantile-based discretization function
- **get_dummies(data, prefix=None, prefix_sep='_', dummy_na=False, columns=None, sparse=False, drop_first=False, dtype=None)** - Convert categorical variable into dummy/indicator variables

### Type Conversion
- **to_datetime(arg, errors='raise', dayfirst=False, yearfirst=False, utc=None, format=None, exact=True, unit=None, infer_datetime_format=False, origin='unix', cache=True)** - Convert argument to datetime
- **to_timedelta(arg, unit=None, errors='raise')** - Convert argument to timedelta
- **to_numeric(arg, errors='raise', downcast=None, dtype_backend=None)** - Convert argument to numeric type

### Missing Value Detection
- **isna(obj)** - Detect missing values for an array-like object
- **isnull(obj)** - Detect missing values (alias of isna)
- **notna(obj)** - Detect non-missing values for an array-like object
- **notnull(obj)** - Detect non-missing values (alias of notna)

### Index Generation
- **date_range(start=None, end=None, periods=None, freq=None, tz=None, normalize=False, name=None, inclusive='both', **kwargs)** - Return fixed frequency DatetimeIndex
- **timedelta_range(start=None, end=None, periods=None, freq=None, name=None, closed=None)** - Return fixed frequency TimedeltaIndex
- **period_range(start=None, end=None, periods=None, freq=None, name=None)** - Return fixed frequency PeriodIndex
- **interval_range(start=None, end=None, periods=None, freq=None, name=None, closed='right')** - Return fixed frequency IntervalIndex

### Other Functions
- **array(data, dtype=None, copy=True)** - Create an ExtensionArray
- **factorize(values, sort=False, use_na_sentinel=True, size_hint=None)** - Encode the object as an enumerated type or categorical variable

### Configuration
- **get_option(pat: str)** - Get value of single configuration option
- **set_option(pat: str, value: Any)** - Set value of single configuration option
- **reset_option(pat: str)** - Reset option to default value
- **option_context(*args)** - Context manager for temporary option changes
- **describe_option(pat: str = '', _print_desc: bool = True)** - Get description of configuration option
- **options** - Configuration options accessor (property)
