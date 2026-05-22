---
name: Feature Engineering
description: Create and transform features using encoding, scaling, polynomial features, and domain-specific transformations for improved model performance and interpretability
---

# Feature Engineering

## Overview

Feature engineering creates and transforms features to improve model performance, interpretability, and generalization through domain knowledge and mathematical transformations.

## When to Use

- When you need to improve model performance beyond using raw features
- When dealing with categorical variables that need encoding for ML algorithms
- When features have different scales and require normalization
- When creating domain-specific features based on business knowledge
- When handling skewed distributions or non-linear relationships
- When preparing data for different types of ML algorithms with specific requirements

## Engineering Techniques

- **Encoding**: Converting categorical to numerical
- **Scaling**: Normalizing feature ranges
- **Polynomial Features**: Higher-order terms
- **Interactions**: Combining features
- **Domain-specific**: Business-relevant transformations
- **Temporal**: Time-based features

## Key Principles

- Create features based on domain knowledge
- Remove redundant features
- Scale features appropriately
- Handle categorical variables
- Create meaningful interactions

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import (
    StandardScaler, MinMaxScaler, RobustScaler, PolynomialFeatures,
    OneHotEncoder, OrdinalEncoder, LabelEncoder
)
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import seaborn as sns

# Create sample dataset
np.random.seed(42)
df = pd.DataFrame({
    'age': np.random.uniform(18, 80, 1000),
    'income': np.random.uniform(20000, 150000, 1000),
    'experience_years': np.random.uniform(0, 50, 1000),
    'category': np.random.choice(['A', 'B', 'C'], 1000),
    'city': np.random.choice(['NYC', 'LA', 'Chicago'], 1000),
    'purchased': np.random.choice([0, 1], 1000),
})

print("Original Data:")
print(df.head())
print(df.info())

# 1. Categorical Encoding
# One-Hot Encoding
print("\n1. One-Hot Encoding:")
df_ohe = pd.get_dummies(df, columns=['category', 'city'], drop_first=True)
print(df_ohe.head())

# Ordinal Encoding
print("\n2. Ordinal Encoding:")
ordinal_encoder = OrdinalEncoder()
df['category_ordinal'] = ordinal_encoder.fit_transform(df[['category']])
print(df[['category', 'category_ordinal']].head())

# Label Encoding
print("\n3. Label Encoding:")
le = LabelEncoder()
df['city_encoded'] = le.fit_transform(df['city'])
print(df[['city', 'city_encoded']].head())

# 2. Feature Scaling
print("\n4. Feature Scaling:")
X = df[['age', 'income', 'experience_years']].copy()

# StandardScaler (mean=0, std=1)
scaler = StandardScaler()
X_standard = scaler.fit_transform(X)

# MinMaxScaler [0, 1]
minmax_scaler = MinMaxScaler()
X_minmax = minmax_scaler.fit_transform(X)

# RobustScaler (resistant to outliers)
robust_scaler = RobustScaler()
X_robust = robust_scaler.fit_transform(X)

# Visualization
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

axes[0, 0].hist(X['age'], bins=30, edgecolor='black')
axes[0, 0].set_title('Original Age')

axes[0, 1].hist(X_standard[:, 0], bins=30, edgecolor='black')
axes[0, 1].set_title('StandardScaler Age')

axes[1, 0].hist(X_minmax[:, 0], bins=30, edgecolor='black')
axes[1, 0].set_title('MinMaxScaler Age')

axes[1, 1].hist(X_robust[:, 0], bins=30, edgecolor='black')
axes[1, 1].set_title('RobustScaler Age')

plt.tight_layout()
plt.show()

# 3. Polynomial Features
print("\n5. Polynomial Features:")
X_simple = df[['age']].copy()
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X_simple)
X_poly_df = pd.DataFrame(X_poly, columns=['age', 'age^2'])
print(X_poly_df.head())

# Visualization
plt.figure(figsize=(12, 5))
plt.scatter(df['age'], df['income'], alpha=0.5)
plt.xlabel('Age')
plt.ylabel('Income')
plt.title('Age vs Income')
plt.grid(True, alpha=0.3)
plt.show()

# 4. Feature Interactions
print("\n6. Feature Interactions:")
df['age_income_interaction'] = df['age'] * df['income'] / 10000
df['age_experience_ratio'] = df['age'] / (df['experience_years'] + 1)
print(df[['age', 'income', 'age_income_interaction', 'age_experience_ratio']].head())

# 5. Domain-specific Transformations
print("\n7. Domain-specific Features:")
df['age_group'] = pd.cut(df['age'], bins=[0, 30, 45, 60, 100],
                          labels=['Young', 'Middle', 'Senior', 'Retired'])
df['income_level'] = pd.qcut(df['income'], q=3, labels=['Low', 'Medium', 'High'])
df['log_income'] = np.log1p(df['income'])
df['sqrt_experience'] = np.sqrt(df['experience_years'])

print(df[['age', 'age_group', 'income', 'income_level', 'log_income']].head())

# 6. Temporal Features (if date data available)
print("\n8. Temporal Features:")
dates = pd.date_range('2023-01-01', periods=len(df))
df['date'] = dates
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day_of_week'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['date'].dt.dayofweek >= 5

print(df[['date', 'year', 'month', 'day_of_week', 'is_weekend']].head())

# 7. Feature Standardization Pipeline
print("\n9. Feature Engineering Pipeline:")

# Separate numerical and categorical features
numerical_features = ['age', 'income', 'experience_years']
categorical_features = ['category', 'city']

# Create preprocessing pipeline
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(drop='first'), categorical_features),
    ]
)

X_processed = preprocessor.fit_transform(df[numerical_features + categorical_features])
print(f"Processed shape: {X_processed.shape}")

# 8. Feature Statistics
print("\n10. Feature Statistics:")
X_for_stats = df[numerical_features].copy()
X_for_stats['category_A'] = (df['category'] == 'A').astype(int)
X_for_stats['city_NYC'] = (df['city'] == 'NYC').astype(int)

feature_stats = pd.DataFrame({
    'Feature': X_for_stats.columns,
    'Mean': X_for_stats.mean(),
    'Std': X_for_stats.std(),
    'Min': X_for_stats.min(),
    'Max': X_for_stats.max(),
    'Skewness': X_for_stats.skew(),
    'Kurtosis': X_for_stats.kurtosis(),
})

print(feature_stats)

# 9. Feature Correlations
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

X_numeric = df[numerical_features].copy()
X_numeric['purchased'] = df['purchased']
corr_matrix = X_numeric.corr()

sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=axes[0])
axes[0].set_title('Feature Correlation Matrix')

# Distribution of engineered features
axes[1].hist(df['age_income_interaction'], bins=30, edgecolor='black', alpha=0.7)
axes[1].set_title('Age-Income Interaction Distribution')
axes[1].set_xlabel('Value')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# 10. Feature Binning / Discretization
print("\n11. Feature Binning:")
df['age_bin_equal'] = pd.cut(df['age'], bins=5)
df['age_bin_quantile'] = pd.qcut(df['age'], q=5)
df['income_bins'] = pd.cut(df['income'], bins=[0, 50000, 100000, 150000])

print("Equal Width Binning:")
print(df['age_bin_equal'].value_counts().sort_index())

print("\nEqual Frequency Binning:")
print(df['age_bin_quantile'].value_counts().sort_index())

# 11. Missing Value Creation and Handling
print("\n12. Missing Value Imputation:")
df_with_missing = df.copy()
missing_indices = np.random.choice(len(df), 50, replace=False)
df_with_missing.loc[missing_indices, 'age'] = np.nan

# Mean imputation
age_mean = df_with_missing['age'].mean()
df_with_missing['age_imputed_mean'] = df_with_missing['age'].fillna(age_mean)

# Median imputation
age_median = df_with_missing['age'].median()
df_with_missing['age_imputed_median'] = df_with_missing['age'].fillna(age_median)

# Forward fill
df_with_missing['age_imputed_ffill'] = df_with_missing['age'].fillna(method='ffill')

print(df_with_missing[['age', 'age_imputed_mean', 'age_imputed_median']].head(10))

print("\nFeature Engineering Complete!")
print(f"Original features: {len(df.columns) - 5}")
print(f"Final features available: {len(df.columns)}")
```

## Best Practices

- Understand your domain before engineering features
- Create features that are interpretable
- Avoid data leakage (using future information)
- Test feature importance after engineering
- Document all transformations
- Use appropriate scaling for different algorithms

## Common Transformations

- **Log Transform**: For skewed distributions
- **Polynomial Features**: For non-linear relationships
- **Interaction Terms**: For combined effects
- **Binning**: For categorical approximation
- **Normalization**: For comparison across scales

## Deliverables

- Engineered feature dataset
- Feature transformation documentation
- Correlation analysis of new features
- Distribution comparisons (before/after)
- Feature importance rankings
- Preprocessing pipeline code
- Data dictionary with feature descriptions
