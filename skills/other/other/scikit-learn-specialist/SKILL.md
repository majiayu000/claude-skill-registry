---
name: scikit-learn-specialist
description: Master scikit-learn machine learning patterns including pipeline design, cross-validation, hyperparameter tuning, feature engineering, and model evaluation. Use PROACTIVELY when building ML models, evaluating classifiers/regressors, or designing ML workflows.
---

# Scikit-Learn Specialist

Master machine learning workflows with scikit-learn, focusing on proper pipeline design, validation, and avoiding common pitfalls.

## When to Use This Skill

- Building classification or regression models
- Feature engineering and preprocessing
- Model selection and hyperparameter tuning
- Cross-validation and evaluation
- Creating reproducible ML pipelines
- Deploying trained models

## Quick Reference

```python
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# Basic workflow
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = make_pipeline(StandardScaler(), RandomForestClassifier())
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test)))
```

---

## Data Splitting

### Proper Train/Test Split

```python
from sklearn.model_selection import train_test_split

# ✅ Always split BEFORE any preprocessing
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,      # Reproducibility
    stratify=y            # Preserve class distribution
)

# ❌ WRONG: Preprocessing before split (data leakage!)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # Sees test data!
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y)
```

### Train/Validation/Test Split

```python
# ✅ Three-way split for hyperparameter tuning
# 60% train, 20% validation, 20% test
X_temp, X_test, y_temp, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
X_train, X_val, y_train, y_val = train_test_split(
    X_temp, y_temp, test_size=0.25, random_state=42  # 0.25 of 80% = 20%
)

print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
```

### Time Series Split

```python
from sklearn.model_selection import TimeSeriesSplit

# ✅ For time series data, use temporal splits
tscv = TimeSeriesSplit(n_splits=5)

for train_idx, test_idx in tscv.split(X):
    X_train, X_test = X[train_idx], X[test_idx]
    y_train, y_test = y[train_idx], y[test_idx]
    # Train and evaluate
```

---

## Pipelines

### Why Use Pipelines

```python
# ❌ BAD: Manual preprocessing (prone to data leakage)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)  # Easy to forget transform vs fit_transform

model = RandomForestClassifier()
model.fit(X_train_scaled, y_train)
predictions = model.predict(X_test_scaled)

# ✅ GOOD: Pipeline handles everything correctly
from sklearn.pipeline import make_pipeline

model = make_pipeline(
    StandardScaler(),
    RandomForestClassifier()
)

model.fit(X_train, y_train)  # Pipeline handles scaling
predictions = model.predict(X_test)
```

### Building Complex Pipelines

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import GradientBoostingClassifier

# Define column groups
numeric_features = ['age', 'income', 'balance']
categorical_features = ['gender', 'occupation', 'region']

# ✅ Separate transformers for different column types
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore'))
])

# ✅ Combine with ColumnTransformer
preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numeric_features),
    ('cat', categorical_transformer, categorical_features)
])

# ✅ Full pipeline with model
model = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', GradientBoostingClassifier())
])

model.fit(X_train, y_train)
```

### Feature Union for Multiple Feature Sets

```python
from sklearn.pipeline import FeatureUnion

# ✅ Combine multiple feature extraction methods
feature_pipeline = FeatureUnion([
    ('tfidf', TfidfVectorizer()),
    ('custom', make_pipeline(
        FunctionTransformer(extract_custom_features),
        StandardScaler()
    ))
])

model = make_pipeline(
    feature_pipeline,
    LogisticRegression()
)
```

---

## Cross-Validation

### Basic Cross-Validation

```python
from sklearn.model_selection import cross_val_score, cross_validate

# ✅ K-Fold cross-validation
model = make_pipeline(StandardScaler(), LogisticRegression())
scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print(f"Accuracy: {scores.mean():.3f} ± {scores.std():.3f}")
```

### Multiple Metrics

```python
# ✅ Get multiple metrics at once
from sklearn.model_selection import cross_validate

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

results = cross_validate(
    model, X, y,
    cv=5,
    scoring=scoring,
    return_train_score=True
)

for metric in scoring:
    test_scores = results[f'test_{metric}']
    print(f"{metric}: {test_scores.mean():.3f} ± {test_scores.std():.3f}")
```

### Stratified K-Fold (Imbalanced Data)

```python
from sklearn.model_selection import StratifiedKFold

# ✅ Preserve class distribution in each fold
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scores = cross_val_score(model, X, y, cv=skf)
```

### Cross-Validation with Pipelines

```python
# ✅ Pipeline ensures preprocessing is done correctly per fold
model = make_pipeline(
    StandardScaler(),
    PCA(n_components=10),
    SVC()
)

# Each fold: fit scaler on train, transform test
scores = cross_val_score(model, X, y, cv=5)
```

---

## Hyperparameter Tuning

### Grid Search

```python
from sklearn.model_selection import GridSearchCV

# ✅ Define parameter grid
param_grid = {
    'classifier__n_estimators': [50, 100, 200],
    'classifier__max_depth': [None, 10, 20, 30],
    'classifier__min_samples_split': [2, 5, 10]
}

# ✅ Search with cross-validation
grid_search = GridSearchCV(
    model,
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,          # Use all cores
    verbose=1
)

grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
best_model = grid_search.best_estimator_
```

### Randomized Search (Faster)

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

# ✅ Define distributions for sampling
param_distributions = {
    'classifier__n_estimators': randint(50, 500),
    'classifier__max_depth': randint(5, 50),
    'classifier__min_samples_split': randint(2, 20),
    'classifier__learning_rate': uniform(0.01, 0.3)
}

# ✅ Random search samples n_iter combinations
random_search = RandomizedSearchCV(
    model,
    param_distributions,
    n_iter=100,         # Number of parameter settings sampled
    cv=5,
    scoring='f1',
    n_jobs=-1,
    random_state=42
)

random_search.fit(X_train, y_train)
```

### Halving Grid Search (Faster)

```python
from sklearn.model_selection import HalvingGridSearchCV

# ✅ Progressively eliminate poor configurations
halving_search = HalvingGridSearchCV(
    model,
    param_grid,
    cv=5,
    factor=3,           # Eliminate 2/3 of candidates at each stage
    scoring='f1',
    n_jobs=-1
)

halving_search.fit(X_train, y_train)
```

---

## Feature Engineering

### Scaling Features

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# ✅ StandardScaler: Mean=0, Std=1 (default choice)
scaler = StandardScaler()

# ✅ MinMaxScaler: Scale to [0, 1] (neural networks)
scaler = MinMaxScaler()

# ✅ RobustScaler: Robust to outliers (uses median/IQR)
scaler = RobustScaler()

# Always fit on train, transform on test
scaler.fit(X_train)
X_train_scaled = scaler.transform(X_train)
X_test_scaled = scaler.transform(X_test)
```

### Encoding Categorical Features

```python
from sklearn.preprocessing import OneHotEncoder, LabelEncoder, OrdinalEncoder

# ✅ One-hot encoding for nominal categories
encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
encoded = encoder.fit_transform(X[['category_column']])

# ✅ Ordinal encoding for ordered categories
encoder = OrdinalEncoder(categories=[['low', 'medium', 'high']])
encoded = encoder.fit_transform(X[['priority']])

# ✅ Target encoding (for high cardinality)
from sklearn.preprocessing import TargetEncoder
encoder = TargetEncoder()
encoded = encoder.fit_transform(X[['city']], y)
```

### Feature Selection

```python
from sklearn.feature_selection import (
    SelectKBest, f_classif, mutual_info_classif,
    RFE, SelectFromModel
)

# ✅ Select K best features based on statistical tests
selector = SelectKBest(score_func=f_classif, k=10)
X_selected = selector.fit_transform(X, y)

# ✅ Recursive Feature Elimination
from sklearn.svm import SVC
selector = RFE(estimator=SVC(kernel='linear'), n_features_to_select=10)
X_selected = selector.fit_transform(X, y)

# ✅ Select based on model importance
from sklearn.ensemble import RandomForestClassifier
selector = SelectFromModel(RandomForestClassifier(n_estimators=100))
X_selected = selector.fit_transform(X, y)
```

### Polynomial Features

```python
from sklearn.preprocessing import PolynomialFeatures

# ✅ Generate polynomial and interaction features
poly = PolynomialFeatures(degree=2, include_bias=False, interaction_only=False)
X_poly = poly.fit_transform(X)

# ⚠️ Warning: Number of features grows quickly
# degree=2, n_features=10 → 65 features
```

---

## Model Evaluation

### Classification Metrics

```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score
)

y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)[:, 1]  # For binary classification

# ✅ Comprehensive report
print(classification_report(y_test, y_pred))

# ✅ Individual metrics
print(f"Accuracy: {accuracy_score(y_test, y_pred):.3f}")
print(f"Precision: {precision_score(y_test, y_pred):.3f}")
print(f"Recall: {recall_score(y_test, y_pred):.3f}")
print(f"F1: {f1_score(y_test, y_pred):.3f}")
print(f"ROC-AUC: {roc_auc_score(y_test, y_prob):.3f}")

# ✅ Confusion matrix
cm = confusion_matrix(y_test, y_pred)
```

### Regression Metrics

```python
from sklearn.metrics import (
    mean_squared_error, mean_absolute_error, r2_score,
    mean_absolute_percentage_error
)

y_pred = model.predict(X_test)

print(f"RMSE: {mean_squared_error(y_test, y_pred, squared=False):.3f}")
print(f"MAE: {mean_absolute_error(y_test, y_pred):.3f}")
print(f"R²: {r2_score(y_test, y_pred):.3f}")
print(f"MAPE: {mean_absolute_percentage_error(y_test, y_pred):.3f}")
```

### Visualizing Model Performance

```python
import matplotlib.pyplot as plt
from sklearn.metrics import (
    ConfusionMatrixDisplay, RocCurveDisplay, PrecisionRecallDisplay
)

# ✅ Confusion matrix visualization
ConfusionMatrixDisplay.from_estimator(model, X_test, y_test)
plt.title('Confusion Matrix')
plt.show()

# ✅ ROC curve
RocCurveDisplay.from_estimator(model, X_test, y_test)
plt.title('ROC Curve')
plt.show()

# ✅ Precision-Recall curve (better for imbalanced data)
PrecisionRecallDisplay.from_estimator(model, X_test, y_test)
plt.title('Precision-Recall Curve')
plt.show()

# ✅ Learning curve
from sklearn.model_selection import learning_curve

train_sizes, train_scores, test_scores = learning_curve(
    model, X, y, cv=5, train_sizes=np.linspace(0.1, 1.0, 10)
)

plt.plot(train_sizes, train_scores.mean(axis=1), label='Train')
plt.plot(train_sizes, test_scores.mean(axis=1), label='Validation')
plt.xlabel('Training Set Size')
plt.ylabel('Score')
plt.legend()
plt.title('Learning Curve')
plt.show()
```

---

## Handling Imbalanced Data

### Class Weights

```python
# ✅ Use class_weight parameter
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(class_weight='balanced')
model.fit(X_train, y_train)
```

### Oversampling with SMOTE

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline as ImbPipeline

# ✅ Use imbalanced-learn pipeline for SMOTE
model = ImbPipeline([
    ('smote', SMOTE(random_state=42)),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])

# SMOTE only applied to training data in cross-validation
model.fit(X_train, y_train)
```

---

## Model Persistence

### Saving and Loading Models

```python
import joblib

# ✅ Save trained pipeline
joblib.dump(model, 'model.joblib')

# ✅ Load model
loaded_model = joblib.load('model.joblib')
predictions = loaded_model.predict(X_new)
```

### Versioning with Metadata

```python
import json
from datetime import datetime

# ✅ Save model with metadata
model_info = {
    'model_path': 'model.joblib',
    'version': '1.0.0',
    'trained_at': datetime.now().isoformat(),
    'features': list(X.columns),
    'metrics': {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred))
    },
    'parameters': model.get_params()
}

joblib.dump(model, 'model.joblib')
with open('model_metadata.json', 'w') as f:
    json.dump(model_info, f, indent=2)
```

---

## Common Pitfalls

| Pitfall                 | Problem           | Solution                         |
| ----------------------- | ----------------- | -------------------------------- |
| Preprocess before split | Data leakage      | Use Pipeline, split first        |
| fit_transform on test   | Leaking test info | Use transform only on test       |
| Ignore class imbalance  | Biased model      | class_weight, SMOTE              |
| Tune on test set        | Overly optimistic | Use validation set or CV         |
| Default hyperparameters | Suboptimal        | GridSearchCV, RandomizedSearchCV |
| Forget random_state     | Not reproducible  | Set seed everywhere              |

## ML Workflow Checklist

```markdown
## Scikit-Learn Workflow Checklist

- [ ] Split data BEFORE any preprocessing
- [ ] Use Pipeline for all preprocessing + model
- [ ] Cross-validate for reliable estimates
- [ ] Use stratified splits for classification
- [ ] Handle class imbalance appropriately
- [ ] Tune hyperparameters with GridSearchCV/RandomizedSearchCV
- [ ] Evaluate with multiple metrics
- [ ] Check for overfitting (train vs test gap)
- [ ] Set random_state for reproducibility
- [ ] Save model with metadata for versioning
```

## Best Practices Summary

1. **Always Use Pipelines** - Prevent data leakage automatically
2. **Split First** - Train/test split before any preprocessing
3. **Cross-Validate** - Never trust single train/test split
4. **Stratify Splits** - Preserve class distribution
5. **Tune Hyperparameters** - Don't use defaults blindly
6. **Handle Imbalance** - class_weight or SMOTE
7. **Evaluate Properly** - Multiple metrics, confusion matrix
8. **Set random_state** - Reproducibility is essential


## Parent Hub
- [_data-ai-mastery](../_data-ai-mastery/SKILL.md)
