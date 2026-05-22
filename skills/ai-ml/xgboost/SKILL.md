---
name: xgboost
description: XGBoost gradient boosting library. Use for tabular ML.
---

# XGBoost

XGBoost is the winningest algorithm in Kaggle history for tabular data. v2.1 (2025) brings native **Blackwell** GPU support and Polars integration.

## When to Use

- **Tabular Data**: It usually beats Deep Learning on structured tables.
- **Speed**: Extremely optimized C++ backend.

## Core Concepts

### Gradient Boosting

Building extensive decision trees sequentially, each correcting the previous one's errors.

### DMatrix

Internal optimized data structure.

### Device Parameter

`device="cuda"` enables GPU acceleration.

## Best Practices (2025)

**Do**:

- **Use `device="cuda"`**: GPU training is 10x faster.
- **Use Early Stopping**: Stop training when validation error rises.
- **Pass Polars Dataframes**: No need to convert to Pandas/NumPy first.

**Don't**:

- **Don't use one-hot encoding**: Use native categorical support (`enable_categorical=True`).

## References

- [XGBoost Documentation](https://xgboost.readthedocs.io/)
