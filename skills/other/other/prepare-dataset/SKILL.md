---
name: prepare-dataset
description: "Process and validate datasets for training. Use when setting up data pipelines."
mcp_fallback: none
category: ml
tier: 2
user-invocable: false
---

# Prepare Dataset

Load, preprocess, and validate datasets for machine learning model training including normalization and augmentation.

## When to Use

- Setting up data pipelines for training
- Normalizing and cleaning raw data
- Splitting into train/validation/test sets
- Applying data augmentation

## Quick Reference

```python
# Dataset preparation pipeline
class DatasetLoader:
    def load(self, path: str) -> Tuple[ndarray, ndarray]:
        # Load raw data
        pass

    def normalize(self, data: ndarray) -> ndarray:
        # Normalize to [0, 1] or standardize
        pass

    def split(self, data: ndarray, ratios: Tuple[float, float, float]):
        # Split into train/val/test
        pass

    def augment(self, data: ndarray) -> ndarray:
        # Apply transformations if needed
        pass
```

## Workflow

1. **Load raw data**: Read dataset from file (CSV, HDF5, NumPy)
2. **Validate data**: Check shape, dtype, missing values
3. **Preprocess**: Normalize, standardize, encode categorical features
4. **Split sets**: Create train/validation/test splits
5. **Augment data**: Apply transformations if needed (rotation, flip, etc.)

## Output Format

Dataset preparation report:

- Raw data shape and statistics
- Data validation results (missing values, outliers)
- Preprocessing applied (normalization, encoding)
- Train/val/test split sizes
- Final dataset shape and statistics
- Augmentation transformations applied

## References

- See `extract-hyperparameters` skill for data preprocessing config
- See `evaluate-model` skill for test set evaluation
- See `/notes/review/mojo-ml-patterns.md` for Mojo data loading
