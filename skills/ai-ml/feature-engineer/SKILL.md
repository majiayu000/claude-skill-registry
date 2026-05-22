---
name: feature-engineer
description: |
  Comprehensive feature engineering for ML pipelines: data quality assessment, feature creation, selection, transformation, and encoding. Activates for "feature engineering", "create features", "feature selection", "data preprocessing", "handle missing values", "encode categorical", "scale features", "feature importance". Ensures features are production-ready with automated validation, documentation, and integration with SpecWeave increments.
---

# Feature Engineer

## Overview

Feature engineering often makes the difference between mediocre and excellent ML models. This skill transforms raw data into model-ready features through systematic data quality assessment, feature creation, selection, and transformation—all integrated with SpecWeave's increment workflow.

## The Feature Engineering Pipeline

### Phase 1: Data Quality Assessment

**Before creating features, understand your data**:

```python
from specweave import DataQualityReport

# Automated data quality check
report = DataQualityReport(df, increment="0042")

# Generates:
# - Missing value analysis
# - Outlier detection
# - Data type validation
# - Distribution analysis
# - Correlation matrix
# - Duplicate detection
```

**Quality Report Output**:
```markdown
# Data Quality Report

## Dataset Overview
- Rows: 100,000
- Columns: 45
- Memory: 34.2 MB

## Missing Values
| Column          | Missing | Percentage |
|-----------------|---------|------------|
| email           | 15,234  | 15.2%      |
| phone           | 8,901   | 8.9%       |
| purchase_date   | 0       | 0.0%       |

## Outliers Detected
- transaction_amount: 234 outliers (>3 std dev)
- user_age: 12 outliers (<18 or >100)

## Data Type Issues
- user_id: Stored as float, should be int
- date_joined: Stored as string, should be datetime

## Recommendations
1. Impute email/phone or create "missing" indicator features
2. Cap/remove outliers in transaction_amount
3. Convert data types for efficiency
```

### Phase 2: Feature Creation

**Create features from domain knowledge**:

```python
from specweave import FeatureCreator

creator = FeatureCreator(df, increment="0042")

# Temporal features (from datetime)
creator.add_temporal_features(
    date_column="purchase_date",
    features=["hour", "day_of_week", "month", "is_weekend", "is_holiday"]
)

# Aggregation features (user behavior)
creator.add_aggregation_features(
    group_by="user_id",
    target="purchase_amount",
    aggs=["mean", "std", "count", "min", "max"]
)
# Creates: user_purchase_amount_mean, user_purchase_amount_std, etc.

# Interaction features
creator.add_interaction_features(
    features=[("age", "income"), ("clicks", "impressions")],
    operations=["multiply", "divide", "subtract"]
)
# Creates: age_x_income, clicks_per_impression, etc.

# Ratio features
creator.add_ratio_features([
    ("revenue", "cost"),
    ("conversions", "visits")
])
# Creates: revenue_to_cost_ratio, conversion_rate

# Binning (discretization)
creator.add_binned_features(
    column="age",
    bins=[0, 18, 25, 35, 50, 65, 100],
    labels=["child", "young_adult", "adult", "middle_aged", "senior", "elderly"]
)

# Text features (from text columns)
creator.add_text_features(
    column="product_description",
    features=["length", "word_count", "unique_words", "sentiment"]
)

# Generate all features
df_enriched = creator.generate()

# Auto-documents in increment folder
creator.save_feature_definitions(
    path=".specweave/increments/0042.../features/feature_definitions.yaml"
)
```

**Feature Definitions** (auto-generated):
```yaml
# .specweave/increments/0042.../features/feature_definitions.yaml

features:
  - name: purchase_hour
    type: temporal
    source: purchase_date
    description: Hour of purchase (0-23)
    
  - name: user_purchase_amount_mean
    type: aggregation
    source: purchase_amount
    group_by: user_id
    description: Average purchase amount per user
    
  - name: age_x_income
    type: interaction
    sources: [age, income]
    operation: multiply
    description: Product of age and income
    
  - name: conversion_rate
    type: ratio
    sources: [conversions, visits]
    description: Conversion rate (conversions / visits)
```

### Phase 3: Feature Selection

**Reduce dimensionality, improve performance**:

```python
from specweave import FeatureSelector

selector = FeatureSelector(X_train, y_train, increment="0042")

# Method 1: Correlation-based (remove redundant features)
selector.remove_correlated_features(threshold=0.95)
# Removes features with >95% correlation

# Method 2: Variance-based (remove constant features)
selector.remove_low_variance_features(threshold=0.01)
# Removes features with <1% variance

# Method 3: Statistical tests
selector.select_by_statistical_test(k=50)
# SelectKBest with chi2/f_classif

# Method 4: Model-based (tree importance)
selector.select_by_model_importance(
    model=RandomForestClassifier(),
    threshold=0.01
)
# Removes features with <1% importance

# Method 5: Recursive Feature Elimination
selector.select_by_rfe(
    model=LogisticRegression(),
    n_features=30
)

# Get selected features
selected_features = selector.get_selected_features()

# Generate selection report
selector.generate_report()
```

**Feature Selection Report**:
```markdown
# Feature Selection Report

## Original Features: 125
## Selected Features: 35 (72% reduction)

## Selection Process
1. Removed 12 correlated features (>95% correlation)
2. Removed 8 low-variance features
3. Statistical test: Selected top 50 (chi-squared)
4. Model importance: Removed 15 low-importance features (<1%)

## Top 10 Features (by importance)
1. user_purchase_amount_mean (0.18)
2. days_since_last_purchase (0.12)
3. total_purchases (0.10)
4. age_x_income (0.08)
5. conversion_rate (0.07)
...

## Removed Features
- user_id_hash (constant)
- temp_feature_1 (99% correlated with temp_feature_2)
- random_noise (0% importance)
...
```

### Phase 4: Feature Transformation

**Scale, normalize, encode for model compatibility**:

```python
from specweave import FeatureTransformer

transformer = FeatureTransformer(increment="0042")

# Numerical transformations
transformer.add_numerical_transformer(
    columns=["age", "income", "purchase_amount"],
    method="standard_scaler"  # Or: min_max, robust, quantile
)

# Categorical encoding
transformer.add_categorical_encoder(
    columns=["country", "device_type", "product_category"],
    method="onehot",  # Or: label, target, binary
    handle_unknown="ignore"
)

# Ordinal encoding (for ordered categories)
transformer.add_ordinal_encoder(
    column="education",
    order=["high_school", "bachelors", "masters", "phd"]
)

# Log transformation (for skewed distributions)
transformer.add_log_transform(
    columns=["transaction_amount", "page_views"],
    method="log1p"  # log(1 + x) to handle zeros
)

# Box-Cox transformation (for normalization)
transformer.add_power_transform(
    columns=["revenue", "engagement_score"],
    method="box-cox"
)

# Custom transformation
def clip_outliers(x):
    return np.clip(x, x.quantile(0.01), x.quantile(0.99))

transformer.add_custom_transformer(
    columns=["outlier_prone_feature"],
    func=clip_outliers
)

# Fit and transform
X_train_transformed = transformer.fit_transform(X_train)
X_test_transformed = transformer.transform(X_test)

# Save transformer pipeline
transformer.save(
    path=".specweave/increments/0042.../features/transformer.pkl"
)
```

### Phase 5: Feature Validation

**Ensure features are production-ready**:

```python
from specweave import FeatureValidator

validator = FeatureValidator(
    X_train, X_test,
    increment="0042"
)

# Check for data leakage
leakage_report = validator.check_data_leakage()
# Detects: perfectly correlated features, future data in training

# Check for distribution drift
drift_report = validator.check_distribution_drift()
# Compares train vs test distributions

# Check for missing values after transformation
missing_report = validator.check_missing_values()

# Check for infinite/NaN values
invalid_report = validator.check_invalid_values()

# Generate validation report
validator.generate_report()
```

**Validation Report**:
```markdown
# Feature Validation Report

## Data Leakage: ✅ PASS
No perfect correlations detected between train and test.

## Distribution Drift: ⚠️  WARNING
Features with significant drift (KS test p < 0.05):
- user_age: p=0.023 (minor drift)
- device_type: p=0.001 (major drift)

Recommendation: Check if test data is from different time period.

## Missing Values: ✅ PASS
No missing values after transformation.

## Invalid Values: ✅ PASS
No infinite or NaN values detected.

## Overall: READY FOR TRAINING
2 warnings, 0 critical issues.
```

## Integration with SpecWeave

### Automatic Feature Documentation

```python
# All feature engineering steps logged to increment
with track_experiment("feature-engineering-v1", increment="0042") as exp:
    # Create features
    df_enriched = creator.generate()
    
    # Select features
    selected = selector.select()
    
    # Transform features
    X_transformed = transformer.fit_transform(X)
    
    # Validate
    validation = validator.validate()
    
    # Auto-logs:
    exp.log_param("original_features", 125)
    exp.log_param("created_features", 45)
    exp.log_param("selected_features", 35)
    exp.log_metric("feature_reduction", 0.72)
    exp.save_artifact("feature_definitions.yaml")
    exp.save_artifact("transformer.pkl")
    exp.save_artifact("validation_report.md")
```

### Living Docs Integration

After completing feature engineering:

```bash
/sw:sync-docs update
```

Updates:
```markdown
<!-- .specweave/docs/internal/architecture/feature-engineering.md -->

## Recommendation Model Features (Increment 0042)

### Feature Engineering Pipeline
1. Data Quality: 100K rows, 45 columns
2. Created: 45 new features (temporal, aggregation, interaction)
3. Selected: 35 features (72% reduction via importance + RFE)
4. Transformed: StandardScaler for numerical, OneHot for categorical

### Key Features
- user_purchase_amount_mean: Average user spend (top feature, 18% importance)
- days_since_last_purchase: Recency indicator (12% importance)
- age_x_income: Interaction feature (8% importance)

### Feature Store
All features documented in: `.specweave/increments/0042.../features/`
- feature_definitions.yaml: Feature catalog
- transformer.pkl: Production transformation pipeline
- validation_report.md: Quality checks
```

## Best Practices

### 1. Document Feature Rationale

```python
# Bad: Create features without explanation
df["feature_1"] = df["col_a"] * df["col_b"]

# Good: Document why features were created
creator.add_interaction_feature(
    sources=["age", "income"],
    operation="multiply",
    rationale="High-income older users have different behavior patterns"
)
```

### 2. Handle Missing Values Systematically

```python
# Options for missing values:
# 1. Imputation (mean, median, mode)
creator.impute_missing(column="age", strategy="median")

# 2. Indicator features (flag missing as signal)
creator.add_missing_indicator(column="email")
# Creates: email_missing (0/1)

# 3. Forward/backward fill (for time series)
creator.fill_missing(column="sensor_reading", method="ffill")

# 4. Model-based imputation
creator.impute_with_model(column="income", model=RandomForestRegressor())
```

### 3. Avoid Data Leakage

```python
# ❌ WRONG: Fit on all data (includes test set!)
scaler.fit(X)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# ✅ CORRECT: Fit only on train, transform both
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# SpecWeave's transformer enforces this pattern
transformer.fit_transform(X_train)  # Fits
transformer.transform(X_test)        # Only transforms
```

### 4. Version Feature Engineering Pipeline

```python
# Version features with increment
transformer.save(
    path=".specweave/increments/0042.../features/transformer-v1.pkl",
    metadata={
        "version": "v1",
        "features": selected_features,
        "transformations": ["standard_scaler", "onehot"]
    }
)

# Load specific version for reproducibility
transformer_v1 = FeatureTransformer.load(
    ".specweave/increments/0042.../features/transformer-v1.pkl"
)
```

### 5. Test Feature Engineering on New Data

```python
# Before deploying, test on held-out data
X_production_sample = load_production_data()

try:
    X_transformed = transformer.transform(X_production_sample)
except Exception as e:
    raise FeatureEngineeringError(f"Failed on production data: {e}")
    
# Check for unexpected values
validator = FeatureValidator(X_train, X_production_sample)
validation_report = validator.validate()

if validation_report["status"] == "CRITICAL":
    raise FeatureEngineeringError("Feature engineering failed validation")
```

## Common Feature Engineering Patterns

### Pattern 1: RFM (Recency, Frequency, Monetary)

```python
# For e-commerce / customer analytics
creator.add_rfm_features(
    user_id="user_id",
    transaction_date="purchase_date",
    transaction_amount="purchase_amount"
)
# Creates:
# - recency: days since last purchase
# - frequency: total purchases
# - monetary: total spend
```

### Pattern 2: Rolling Window Aggregations

```python
# For time series
creator.add_rolling_features(
    column="daily_sales",
    windows=[7, 14, 30],
    aggs=["mean", "std", "min", "max"]
)
# Creates: daily_sales_7day_mean, daily_sales_7day_std, etc.
```

### Pattern 3: Target Encoding (Categorical → Numerical)

```python
# Encode categorical as target mean (careful: can leak!)
creator.add_target_encoding(
    column="product_category",
    target="purchase_amount",
    cv_folds=5  # Cross-validation to prevent leakage
)
# Creates: product_category_target_encoded
```

### Pattern 4: Polynomial Features

```python
# For non-linear relationships
creator.add_polynomial_features(
    columns=["age", "income"],
    degree=2,
    interaction_only=True
)
# Creates: age^2, income^2, age*income
```

## Commands

```bash
# Generate feature engineering pipeline for increment
/ml:engineer-features 0042

# Validate features before training
/ml:validate-features 0042

# Generate feature importance report
/ml:feature-importance 0042
```

## Integration with Other Skills

- **ml-pipeline-orchestrator**: Task 2 is "Feature Engineering" (uses this skill)
- **experiment-tracker**: Logs all feature engineering experiments
- **model-evaluator**: Uses feature importance from models
- **ml-deployment-helper**: Packages feature transformer for production

## Summary

Feature engineering is 70% of ML success. This skill ensures:
- ✅ Systematic approach (quality → create → select → transform → validate)
- ✅ No data leakage (train/test separation enforced)
- ✅ Production-ready (versioned, validated, documented)
- ✅ Reproducible (all steps tracked in increment)
- ✅ Traceable (feature definitions in living docs)

Good features make mediocre models great. Great features make mediocre models excellent.
