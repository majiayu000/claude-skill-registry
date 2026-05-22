---
name: feature-stores
version: "2.0.0"
sasmp_version: "1.3.0"
description: Master feature stores - Feast, data validation, versioning, online/offline serving
bonded_agent: 03-data-pipelines
bond_type: PRIMARY_BOND

# SKILL METADATA
category: data_engineering
difficulty: intermediate_to_advanced
estimated_hours: 35
prerequisites:
  - mlops-basics

# VALIDATION
validation:
  pre_conditions:
    - "Completed mlops-basics skill"
    - "Understanding of data pipelines"
  post_conditions:
    - "Can design feature store architecture"
    - "Can implement features with Feast"
    - "Can validate data quality"

# OBSERVABILITY
observability:
  metrics:
    - features_created
    - validation_checks_passed
    - latency_measurements
---

# Feature Stores Skill

> **Learn**: Build production feature stores for ML systems.

## Skill Overview

| Attribute | Value |
|-----------|-------|
| **Bonded Agent** | 03-data-pipelines |
| **Difficulty** | Intermediate to Advanced |
| **Duration** | 35 hours |
| **Prerequisites** | mlops-basics |

---

## Learning Objectives

1. **Understand** feature store architecture
2. **Implement** features with Feast
3. **Validate** data quality with Great Expectations
4. **Serve** features online and offline
5. **Version** datasets with DVC

---

## Topics Covered

### Module 1: Feature Store Architecture (8 hours)

**Components:**

```
┌─────────────────────────────────────────────────────────────┐
│                   FEATURE STORE ARCHITECTURE                 │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │ Offline     │    │  Feature    │    │  Online     │     │
│  │ Store       │───▶│  Registry   │◀───│  Store      │     │
│  │ (Parquet)   │    │  (Metadata) │    │  (Redis)    │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│        │                   │                   │            │
│        ▼                   ▼                   ▼            │
│   [Training]         [Discovery]        [Inference]        │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

**Exercises:**
- [ ] Design feature store for e-commerce use case
- [ ] Compare Feast vs Tecton vs Hopsworks

---

### Module 2: Feast Implementation (12 hours)

**Feature Definition Example:**

```python
from feast import Entity, Feature, FeatureView, FileSource
from feast.types import Float32, Int64
from datetime import timedelta

# Entity definition
customer = Entity(
    name="customer_id",
    value_type=ValueType.INT64,
    description="Customer identifier"
)

# Feature view
customer_features = FeatureView(
    name="customer_features",
    entities=["customer_id"],
    ttl=timedelta(days=7),
    schema=[
        Feature(name="total_purchases", dtype=Float32),
        Feature(name="avg_order_value", dtype=Float32),
        Feature(name="days_since_last_order", dtype=Int64),
    ],
    online=True,
    source=customer_stats_source
)
```

**Exercises:**
- [ ] Set up Feast repository locally
- [ ] Create entity and feature views
- [ ] Materialize features to online store
- [ ] Retrieve features for training and inference

---

### Module 3: Data Validation (8 hours)

**Great Expectations Setup:**

```python
import great_expectations as gx

# Create validation suite
suite = context.add_expectation_suite("ml_data_validation")

# Add expectations
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(
        column="target",
        mostly=0.99
    )
)

suite.add_expectation(
    gx.expectations.ExpectColumnMeanToBeBetween(
        column="feature_a",
        min_value=0.0,
        max_value=100.0
    )
)
```

---

### Module 4: Data Versioning (7 hours)

**DVC Workflow:**

```bash
# Initialize DVC
dvc init

# Add data to tracking
dvc add data/training_data.parquet

# Push to remote storage
dvc push

# Checkout specific version
git checkout v1.0.0
dvc checkout
```

---

## Code Templates

### Template: Feature Engineering Pipeline

```python
# templates/feature_pipeline.py
from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd

class FeaturePipeline(BaseEstimator, TransformerMixin):
    """Production feature engineering pipeline."""

    def __init__(self, config: dict):
        self.config = config
        self.feature_names = []

    def fit(self, X: pd.DataFrame, y=None):
        """Learn feature statistics."""
        self.means = X.select_dtypes(include=['number']).mean()
        self.stds = X.select_dtypes(include=['number']).std()
        return self

    def transform(self, X: pd.DataFrame) -> pd.DataFrame:
        """Apply feature transformations."""
        X = X.copy()

        # Numerical normalization
        for col in X.select_dtypes(include=['number']).columns:
            X[f"{col}_normalized"] = (X[col] - self.means[col]) / self.stds[col]

        # Temporal features
        for col in self.config.get("datetime_columns", []):
            X[f"{col}_hour"] = pd.to_datetime(X[col]).dt.hour
            X[f"{col}_dow"] = pd.to_datetime(X[col]).dt.dayofweek

        return X
```

---

## Troubleshooting Guide

| Issue | Cause | Solution |
|-------|-------|----------|
| Slow feature serving | Online store bottleneck | Scale Redis, add caching |
| Training-serving skew | Different transformations | Use unified feature pipeline |
| Stale features | Materialization lag | Increase refresh frequency |

---

## Resources

- [Feast Documentation](https://docs.feast.dev/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [DVC Documentation](https://dvc.org/doc)
- [See: training-pipelines] - Use features in training

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2024-12 | Production-grade with Feast examples |
| 1.0.0 | 2024-11 | Initial release |
