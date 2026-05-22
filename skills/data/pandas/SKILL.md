---
name: pandas
description: Pandas data manipulation with DataFrames. Use for data analysis.
---

# Pandas

Pandas is the Excel of Python. v3.0 (2025/2026) enforces **Copy-on-Write (CoW)**, finally fixing the `SettingWithCopyWarning` confusion.

## When to Use

- **Data Cleaning**: Loading CSV/Excel/SQL and cleaning it.
- **Time Series**: Unmatched datetime indexing capabilities.
- **Small/Medium Data**: Features that fit in RAM.

## Core Concepts

### DataFrame / Series

2D tables and 1D arrays.

### Copy-on-Write (CoW)

Views are always views, copies are always copies. Modifying a view triggers a copy _only if necessary_.

### PyArrow Backend

Using Arrow memory format for speed and string handling (`dtype="string[pyarrow]"`).

## Best Practices (2025)

**Do**:

- **Use PyArrow Strings**: `pd.options.future.infer_string = True` (Default in 3.0).
- **Use `.query()`**: For cleaner filtering syntax.
- **Migrate to CoW**: Ensure your code doesn't rely on side-effects of views.

**Don't**:

- **Don't iterate rows**: Use vectorization (`df['a'] + df['b']`).

## References

- [Pandas Documentation](https://pandas.pydata.org/)
