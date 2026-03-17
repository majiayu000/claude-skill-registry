---
name: Regression Modeling
description: Build predictive models using linear regression, polynomial regression, and regularized regression for continuous prediction, trend forecasting, and relationship quantification
---

# Regression Modeling

## Overview

Regression modeling predicts continuous target values based on input features, establishing quantitative relationships between variables for forecasting and analysis.

## When to Use

- Predicting sales, prices, or other continuous numerical outcomes
- Understanding relationships between independent and dependent variables
- Forecasting trends based on historical data
- Quantifying the impact of features on a target variable
- Building baseline models for comparison with more complex algorithms
- Identifying which variables most influence predictions

## Regression Types

- **Linear Regression**: Straight-line fit to data
- **Polynomial Regression**: Non-linear relationships
- **Ridge (L2)**: Regularization to prevent overfitting
- **Lasso (L1)**: Feature selection through regularization
- **ElasticNet**: Combines Ridge and Lasso
- **Robust Regression**: Resistant to outliers

## Key Metrics

- **R² Score**: Proportion of variance explained
- **RMSE**: Root Mean Squared Error
- **MAE**: Mean Absolute Error
- **AIC/BIC**: Model comparison criteria

## Implementation with Python

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import (
    LinearRegression, Ridge, Lasso, ElasticNet, HuberRegressor
)
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import seaborn as sns

# Generate sample data
np.random.seed(42)
X = np.random.uniform(0, 100, 200).reshape(-1, 1)
y = 2.5 * X.squeeze() + 30 + np.random.normal(0, 50, 200)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr = lr_model.predict(X_test)

print("Linear Regression:")
print(f"  R² Score: {r2_score(y_test, y_pred_lr):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.4f}")
print(f"  Coefficient: {lr_model.coef_[0]:.4f}")
print(f"  Intercept: {lr_model.intercept_:.4f}")

# Polynomial Regression (degree 2)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_train)
y_pred_poly = poly_model.predict(X_test_poly)

print("\nPolynomial Regression (degree=2):")
print(f"  R² Score: {r2_score(y_test, y_pred_poly):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_poly)):.4f}")

# Ridge Regression (L2 regularization)
ridge_model = Ridge(alpha=1.0)
ridge_model.fit(X_train, y_train)
y_pred_ridge = ridge_model.predict(X_test)

print("\nRidge Regression (alpha=1.0):")
print(f"  R² Score: {r2_score(y_test, y_pred_ridge):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_ridge)):.4f}")

# Lasso Regression (L1 regularization)
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
y_pred_lasso = lasso_model.predict(X_test)

print("\nLasso Regression (alpha=0.1):")
print(f"  R² Score: {r2_score(y_test, y_pred_lasso):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lasso)):.4f}")

# ElasticNet Regression
elastic_model = ElasticNet(alpha=0.1, l1_ratio=0.5)
elastic_model.fit(X_train, y_train)
y_pred_elastic = elastic_model.predict(X_test)

print("\nElasticNet Regression:")
print(f"  R² Score: {r2_score(y_test, y_pred_elastic):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_elastic)):.4f}")

# Robust Regression (resistant to outliers)
huber_model = HuberRegressor(max_iter=1000, alpha=0.1)
huber_model.fit(X_train, y_train)
y_pred_huber = huber_model.predict(X_test)

print("\nHuber Regression (Robust):")
print(f"  R² Score: {r2_score(y_test, y_pred_huber):.4f}")
print(f"  RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_huber)):.4f}")

# Visualization
fig, axes = plt.subplots(2, 3, figsize=(15, 8))

models_data = [
    (X_test, y_test, y_pred_lr, 'Linear'),
    (X_test_poly, y_test, y_pred_poly, 'Polynomial (deg=2)'),
    (X_test, y_test, y_pred_ridge, 'Ridge'),
    (X_test, y_test, y_pred_lasso, 'Lasso'),
    (X_test, y_test, y_pred_elastic, 'ElasticNet'),
    (X_test, y_test, y_pred_huber, 'Huber'),
]

for idx, (X_p, y_t, y_p, label) in enumerate(models_data):
    if label in ['Polynomial (deg=2)']:
        x_plot = X_p[:, 1]  # Use quadratic feature for plotting
    else:
        x_plot = X_p

    ax = axes[idx // 3, idx % 3]
    ax.scatter(x_plot, y_t, alpha=0.5, label='Actual')
    ax.scatter(x_plot, y_p, alpha=0.5, color='red', label='Predicted')
    ax.set_title(f'{label}\nR²={r2_score(y_t, y_p):.4f}')
    ax.legend()
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# Residual analysis
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

residuals = y_test - y_pred_lr
axes[0].scatter(y_pred_lr, residuals, alpha=0.5)
axes[0].axhline(y=0, color='r', linestyle='--')
axes[0].set_title('Residual Plot')
axes[0].set_xlabel('Fitted Values')
axes[0].set_ylabel('Residuals')

axes[1].hist(residuals, bins=20, edgecolor='black')
axes[1].set_title('Residuals Distribution')
axes[1].set_xlabel('Residuals')
axes[1].set_ylabel('Frequency')

plt.tight_layout()
plt.show()

# Cross-validation
cv_scores = cross_val_score(LinearRegression(), X, y, cv=5, scoring='r2')
print(f"\nCross-validation R² scores: {cv_scores}")
print(f"Mean CV R²: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

# Regularization parameter tuning
alphas = np.logspace(-3, 3, 100)
ridge_scores = []

for alpha in alphas:
    ridge = Ridge(alpha=alpha)
    scores = cross_val_score(ridge, X_train, y_train, cv=5, scoring='r2')
    ridge_scores.append(scores.mean())

best_alpha_idx = np.argmax(ridge_scores)
best_alpha = alphas[best_alpha_idx]

plt.figure(figsize=(10, 5))
plt.semilogx(alphas, ridge_scores)
plt.axvline(x=best_alpha, color='red', linestyle='--', label=f'Best alpha={best_alpha:.4f}')
plt.xlabel('Alpha (Regularization Strength)')
plt.ylabel('Cross-validation R² Score')
plt.title('Ridge Regression: Alpha Tuning')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

# Feature importance (coefficients)
if hasattr(lr_model, 'coef_'):
    print(f"\nModel Coefficients: {lr_model.coef_}")

# Additional evaluation and diagnostics

# Model prediction intervals
from scipy import stats as sp_stats

predictions = lr_model.predict(X_test)
residuals = y_test - predictions
mse = np.mean(residuals**2)
rmse = np.sqrt(mse)

# Prediction intervals (95%)
n = len(X_test)
p = X_test.shape[1]
dof = n - p - 1
t_val = sp_stats.t.ppf(0.975, dof)
margin = t_val * np.sqrt(mse * (1 + 1/n))
pred_intervals = np.column_stack([
    predictions - margin,
    predictions + margin
])

print(f"\nPrediction Intervals (95%):")
print(f"First prediction: {predictions[0]:.2f} [{pred_intervals[0, 0]:.2f}, {pred_intervals[0, 1]:.2f}]")

# Variance inflation factors for multicollinearity
from statsmodels.stats.outliers_influence import variance_inflation_factor

vif_data = pd.DataFrame()
vif_data["Feature"] = X_test.columns if hasattr(X_test, 'columns') else range(X_test.shape[1])
try:
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    print("\nVariance Inflation Factor (VIF):")
    print(vif_data)
except:
    print("VIF calculation skipped (insufficient features)")

# Prediction by group/segment
if hasattr(X_test, 'columns'):
    segment_results = {}
    for feat in X_test.columns[:2]:
        q1, q3 = X_test[feat].quantile([0.25, 0.75])
        low = X_test[X_test[feat] <= q1]
        high = X_test[X_test[feat] >= q3]

        if len(low) > 0 and len(high) > 0:
            low_pred_rmse = np.sqrt(np.mean((y_test[low.index] - lr_model.predict(low))**2))
            high_pred_rmse = np.sqrt(np.mean((y_test[high.index] - lr_model.predict(high))**2))
            segment_results[feat] = {
                'Low RMSE': low_pred_rmse,
                'High RMSE': high_pred_rmse,
            }

    if segment_results:
        print(f"\nSegment Performance:")
        for feat, results in segment_results.items():
            print(f"  {feat}: Low={results['Low RMSE']:.2f}, High={results['High RMSE']:.2f}")

print("\nRegression model evaluation complete!")
```

## Assumption Checking

- **Linearity**: Relationship is linear
- **Independence**: Observations are independent
- **Homoscedasticity**: Constant variance of errors
- **Normality**: Errors are normally distributed
- **No multicollinearity**: Features not highly correlated

## Model Selection

- **Simple data**: Linear regression
- **Non-linear patterns**: Polynomial regression
- **Many features**: Lasso or ElasticNet
- **Outliers**: Robust regression
- **Prevent overfitting**: Ridge or ElasticNet

## Deliverables

- Fitted models with coefficients
- R² and RMSE metrics
- Residual plots and analysis
- Cross-validation results
- Regularization parameter tuning curves
- Model comparison summary
- Predictions with confidence intervals
