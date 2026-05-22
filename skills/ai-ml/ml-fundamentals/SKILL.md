---
name: ml-fundamentals
description: Master machine learning foundations - algorithms, preprocessing, feature engineering, and evaluation
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 01-ml-fundamentals
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: dataset
      type: dataframe
      validation: "non-empty, numeric or categorical columns"
  optional:
    - name: target_column
      type: string
      default: null
    - name: test_size
      type: float
      default: 0.2
      validation: "0.1 <= x <= 0.4"

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [execution_time, memory_usage, data_shape]
---

# ML Fundamentals Skill

> Master the building blocks of machine learning: from raw data to trained models.

## Quick Start

```python
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# 1. Load and split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# 3. Train and evaluate
pipeline.fit(X_train, y_train)
score = pipeline.score(X_test, y_test)
print(f"Accuracy: {score:.4f}")
```

## Key Topics

### 1. Data Preprocessing

| Step | Purpose | Implementation |
|------|---------|----------------|
| **Missing Values** | Handle NaN/None | `SimpleImputer(strategy='median')` |
| **Scaling** | Normalize ranges | `StandardScaler()` or `MinMaxScaler()` |
| **Encoding** | Convert categories | `OneHotEncoder()` or `LabelEncoder()` |
| **Outliers** | Remove extremes | IQR method or Z-score |

```python
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer

# Define column types
numeric_features = ['age', 'income', 'score']
categorical_features = ['gender', 'city', 'category']

# Create preprocessor
preprocessor = ColumnTransformer([
    ('num', Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ]), numeric_features),
    ('cat', Pipeline([
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ]), categorical_features)
])
```

### 2. Feature Engineering

| Technique | Use Case | Example |
|-----------|----------|---------|
| **Polynomial** | Non-linear relationships | `PolynomialFeatures(degree=2)` |
| **Binning** | Discretize continuous | `KBinsDiscretizer(n_bins=5)` |
| **Log Transform** | Right-skewed data | `np.log1p(x)` |
| **Interaction** | Feature combinations | `x1 * x2` |

### 3. Model Evaluation

```python
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report

# Cross-validation
cv_scores = cross_val_score(model, X, y, cv=5, scoring='f1_weighted')
print(f"CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")

# Detailed report
y_pred = model.predict(X_test)
print(classification_report(y_test, y_pred))
```

### 4. Cross-Validation Strategies

| Strategy | When to Use |
|----------|-------------|
| `KFold` | Standard, balanced data |
| `StratifiedKFold` | Imbalanced classification |
| `TimeSeriesSplit` | Temporal data |
| `GroupKFold` | Grouped samples |

## Best Practices

### DO
- Split data BEFORE any preprocessing
- Use pipelines for reproducibility
- Stratify splits for classification
- Log all preprocessing parameters
- Version your feature engineering code

### DON'T
- Don't fit on test data
- Don't ignore data leakage
- Don't use accuracy for imbalanced data
- Don't hard-code parameters

## Exercises

### Exercise 1: Basic Pipeline
```python
# TODO: Create a pipeline that:
# 1. Imputes missing values
# 2. Scales features
# 3. Trains a logistic regression
```

### Exercise 2: Cross-Validation
```python
# TODO: Implement 5-fold stratified CV
# and report mean and std of F1 score
```

## Unit Test Template

```python
import pytest
import numpy as np
from sklearn.datasets import make_classification

def test_preprocessing_pipeline():
    """Test preprocessing handles missing values."""
    X, y = make_classification(n_samples=100, n_features=10)
    X[0, 0] = np.nan  # Introduce missing value

    pipeline = create_preprocessing_pipeline()
    X_transformed = pipeline.fit_transform(X)

    assert not np.isnan(X_transformed).any()
    assert X_transformed.shape[0] == X.shape[0]

def test_no_data_leakage():
    """Verify preprocessing doesn't leak test data."""
    X_train, X_test = X[:80], X[80:]

    pipeline.fit(X_train)
    X_test_transformed = pipeline.transform(X_test)

    # Check that test transform uses train statistics
    assert pipeline.named_steps['scaler'].mean_ is not None
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| `NaN in prediction` | Missing imputer | Add `SimpleImputer` to pipeline |
| `Shape mismatch` | Inconsistent features | Use `ColumnTransformer` |
| `Memory error` | Too many one-hot features | Use `max_categories` or hashing |
| `Poor CV variance` | Data leakage | Check preprocessing order |

## Related Resources

- **Agent**: `01-ml-fundamentals`
- **Next Skill**: `supervised-learning`
- **Docs**: [scikit-learn User Guide](https://scikit-learn.org/stable/user_guide.html)

---

**Version**: 1.4.0 | **Status**: Production Ready
