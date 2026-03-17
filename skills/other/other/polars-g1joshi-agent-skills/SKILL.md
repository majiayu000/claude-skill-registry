---
name: polars
description: Polars fast DataFrame library. Use for fast data processing.
---

# Polars

Polars is the fast successor to Pandas. Written in Rust, query-optimized, and parallelized. v1.0 (2024) signaled production readiness.

## When to Use

- **Performance**: 10-100x faster than Pandas on large data.
- **Lazy Evaluation**: Define a query plan and execute it efficiently (`.collect()`).
- **Streaming**: Process datasets larger than RAM.

## Core Concepts

### Lazy API (`.lazy()`)

Builds a query plan. Polars optimizes it (predicate pushdown) before reducing it.

### Expressions

`pl.col("a").sum()` is an expression, not a direct calculation.

### Compatibility

Can convert to/from Pandas/PyArrow zero-copy.

## Best Practices (2025)

**Do**:

- **Use Lazy Mode**: `df.lazy().filter(...).collect()`.
- **Use `scan_parquet`**: Don't load the whole file; scan it.
- **Use GPU engine**: Polars has experimental NVIDIA RAPIDS support.

**Don't**:

- **Don't treat it like Pandas**: The API is different (`axis=1` doesn't exist; use expressions).

## References

- [Polars Documentation](https://pola.rs/)
