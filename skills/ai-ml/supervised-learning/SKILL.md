---
name: supervised-learning
description: Build production-ready classification and regression models with hyperparameter tuning
version: "1.4.0"
sasmp_version: "1.4.0"
bonded_agent: 02-supervised-learning
bond_type: PRIMARY_BOND

# Parameter Validation
parameters:
  required:
    - name: X
      type: array
      validation: "2D array, no NaN"
    - name: y
      type: array
      validation: "1D array, same length as X"
  optional:
    - name: task
      type: string
      default: "classification"
      validation: "[classification|regression]"

# Retry Logic
retry_logic:
  strategy: exponential_backoff
  max_attempts: 3
  base_delay_ms: 1000

# Observability
logging:
  level: info
  metrics: [training_time, cv_score, model_size]
---

# Supervised Learning Skill

> Build, tune, and evaluate classification and regression models.

## Quick Start

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, train_test_split

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='f1_weighted')
print(f"CV F1: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
print(f"Test Accuracy: {model.score(X_test, y_test):.4f}")
```

## Key Topics

### 1. Classification Algorithms

| Algorithm | Best For | Complexity |
|-----------|----------|------------|
| **Logistic Regression** | Baseline, interpretable | O(n*d) |
| **Random Forest** | Tabular, general | O(n*d*trees) |
| **XGBoost** | Competitions, accuracy | O(n*d*trees) |
| **SVM** | High-dim, small data | O(n²) |

```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

classifiers = {
    'lr': LogisticRegression(max_iter=1000, class_weight='balanced'),
    'rf': RandomForestClassifier(n_estimators=100, class_weight='balanced'),
    'xgb': XGBClassifier(n_estimators=100, eval_metric='logloss')
}
```

### 2. Regression Algorithms

| Algorithm | Best For | Key Param |
|-----------|----------|-----------|
| **Ridge** | Multicollinearity | alpha |
| **Lasso** | Feature selection | alpha |
| **Random Forest** | Non-linear | n_estimators |
| **XGBoost** | Best accuracy | learning_rate |

### 3. Hyperparameter Tuning

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(50, 300),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10)
}

search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_dist,
    n_iter=50,
    cv=5,
    scoring='f1_weighted',
    n_jobs=-1,
    random_state=42
)

search.fit(X_train, y_train)
print(f"Best params: {search.best_params_}")
print(f"Best CV score: {search.best_score_:.4f}")
```

### 4. Handling Class Imbalance

| Technique | Implementation |
|-----------|----------------|
| **Class Weights** | `class_weight='balanced'` |
| **SMOTE** | `imblearn.over_sampling.SMOTE()` |
| **Threshold Tuning** | Adjust prediction threshold |

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline

pipeline = Pipeline([
    ('smote', SMOTE(random_state=42)),
    ('classifier', RandomForestClassifier())
])
```

### 5. Model Comparison

```python
from sklearn.model_selection import cross_validate
import pandas as pd

def compare_models(models, X, y, cv=5):
    results = []
    for name, model in models.items():
        cv_results = cross_validate(
            model, X, y, cv=cv,
            scoring=['accuracy', 'f1_weighted', 'roc_auc_ovr_weighted'],
            return_train_score=True
        )
        results.append({
            'model': name,
            'train_acc': cv_results['train_accuracy'].mean(),
            'test_acc': cv_results['test_accuracy'].mean(),
            'test_f1': cv_results['test_f1_weighted'].mean(),
            'test_auc': cv_results['test_roc_auc_ovr_weighted'].mean()
        })
    return pd.DataFrame(results).round(4)
```

## Best Practices

### DO
- Start with a simple baseline
- Use stratified splits for classification
- Log all hyperparameters
- Check for overfitting (train vs test gap)
- Use early stopping for boosting

### DON'T
- Don't tune on test set
- Don't ignore class imbalance
- Don't skip feature importance analysis
- Don't use accuracy for imbalanced data

## Exercises

### Exercise 1: Model Selection
```python
# TODO: Compare 3 different classifiers using cross-validation
# Report F1 score for each
```

### Exercise 2: Hyperparameter Tuning
```python
# TODO: Use RandomizedSearchCV to tune XGBoost
# Find optimal n_estimators, max_depth, learning_rate
```

## Unit Test Template

```python
import pytest
from sklearn.datasets import make_classification

def test_classifier_trains():
    """Test classifier can fit and predict."""
    X, y = make_classification(n_samples=100, random_state=42)
    model = get_classifier()

    model.fit(X[:80], y[:80])
    predictions = model.predict(X[80:])

    assert len(predictions) == 20
    assert set(predictions).issubset({0, 1})

def test_handles_imbalance():
    """Test model handles imbalanced classes."""
    X, y = make_classification(n_samples=100, weights=[0.9, 0.1])
    model = get_balanced_classifier()

    model.fit(X, y)
    predictions = model.predict(X)

    # Should predict both classes
    assert len(set(predictions)) == 2
```

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| Overfitting | Model too complex | Reduce depth, add regularization |
| Underfitting | Model too simple | Increase complexity |
| Class imbalance | Skewed data | Use SMOTE or class weights |
| Slow training | Large data | Use LightGBM, reduce estimators |

## Related Resources

- **Agent**: `02-supervised-learning`
- **Previous**: `ml-fundamentals`
- **Next**: `clustering`

---

**Version**: 1.4.0 | **Status**: Production Ready
