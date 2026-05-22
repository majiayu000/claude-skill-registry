---
name: cost-prediction
description: "Predict construction project costs using Machine Learning. Use Linear Regression, K-Nearest Neighbors, and Random Forest models on historical project data. Train, evaluate, and deploy cost prediction models."
---

# Construction Cost Prediction with Machine Learning

## Overview

Based on DDC methodology (Chapter 4.5), this skill enables predicting construction project costs using historical data and machine learning algorithms. The approach transforms traditional expert-based estimation into data-driven prediction.

**Book Reference:** "Будущее: прогнозы и машинное обучение" / "Future: Predictions and Machine Learning"

> "Предсказания и прогнозы на основе исторических данных позволяют компаниям принимать более точные решения о стоимости и сроках проектов."
> — DDC Book, Chapter 4.5

## Core Concepts

```
Historical Data → Feature Engineering → ML Model → Cost Prediction
    │                    │                │              │
    ▼                    ▼                ▼              ▼
Past projects      Prepare data      Train model    New project
with costs         for ML            on history     cost forecast
```

## Quick Start

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

# Load historical project data
df = pd.read_csv("historical_projects.csv")

# Features and target
X = df[['area_m2', 'floors', 'complexity_score']]
y = df['total_cost']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict
predictions = model.predict(X_test)
print(f"R² Score: {r2_score(y_test, predictions):.2f}")
print(f"MAE: ${mean_absolute_error(y_test, predictions):,.0f}")

# Predict new project
new_project = [[5000, 10, 3]]  # area, floors, complexity
cost = model.predict(new_project)
print(f"Predicted cost: ${cost[0]:,.0f}")
```

## Data Preparation

### Prepare Historical Dataset

```python
import pandas as pd
import numpy as np

def prepare_cost_dataset(df):
    """Prepare historical project data for ML"""
    # Select relevant features
    features = [
        'area_m2',
        'floors',
        'building_type',
        'location',
        'year_completed',
        'complexity_score',
        'material_quality',
        'total_cost'
    ]

    df = df[features].copy()

    # Handle missing values
    df = df.dropna(subset=['total_cost'])
    df['complexity_score'] = df['complexity_score'].fillna(df['complexity_score'].median())

    # Encode categorical variables
    df = pd.get_dummies(df, columns=['building_type', 'location'])

    # Calculate derived features
    df['cost_per_m2'] = df['total_cost'] / df['area_m2']
    df['cost_per_floor'] = df['total_cost'] / df['floors']

    # Adjust for inflation (to current year prices)
    current_year = 2024
    inflation_rate = 0.03  # 3% annual
    df['years_ago'] = current_year - df['year_completed']
    df['adjusted_cost'] = df['total_cost'] * (1 + inflation_rate) ** df['years_ago']

    return df

# Usage
df = pd.read_csv("projects_history.csv")
df_prepared = prepare_cost_dataset(df)
```

### Feature Engineering

```python
def engineer_features(df):
    """Create additional features for better predictions"""
    # Interaction features
    df['area_x_floors'] = df['area_m2'] * df['floors']
    df['area_x_complexity'] = df['area_m2'] * df['complexity_score']

    # Polynomial features
    df['area_squared'] = df['area_m2'] ** 2

    # Log transforms (for skewed features)
    df['log_area'] = np.log1p(df['area_m2'])

    # Binned features
    df['size_category'] = pd.cut(
        df['area_m2'],
        bins=[0, 1000, 5000, 10000, float('inf')],
        labels=['small', 'medium', 'large', 'xlarge']
    )

    return df
```

## Machine Learning Models

### Linear Regression

```python
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

def train_linear_model(X_train, y_train):
    """Train Linear Regression model with scaling"""
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])

    pipeline.fit(X_train, y_train)

    # Feature importance (coefficients)
    coefficients = pd.DataFrame({
        'feature': X_train.columns,
        'coefficient': pipeline.named_steps['regressor'].coef_
    }).sort_values('coefficient', key=abs, ascending=False)

    return pipeline, coefficients

# Usage
model, importance = train_linear_model(X_train, y_train)
print("Feature Importance:")
print(importance)
```

### K-Nearest Neighbors (KNN)

```python
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def train_knn_model(X_train, y_train):
    """Train KNN model with optimal k"""
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_train)

    # Find optimal k using cross-validation
    param_grid = {'n_neighbors': range(3, 20)}
    knn = KNeighborsRegressor()
    grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_absolute_error')
    grid_search.fit(X_scaled, y_train)

    print(f"Best k: {grid_search.best_params_['n_neighbors']}")
    print(f"Best MAE: ${-grid_search.best_score_:,.0f}")

    return grid_search.best_estimator_, scaler

# Usage
knn_model, scaler = train_knn_model(X_train, y_train)
```

### Random Forest

```python
from sklearn.ensemble import RandomForestRegressor

def train_random_forest(X_train, y_train):
    """Train Random Forest model"""
    rf = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        random_state=42
    )

    rf.fit(X_train, y_train)

    # Feature importance
    importance = pd.DataFrame({
        'feature': X_train.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)

    return rf, importance

# Usage
rf_model, importance = train_random_forest(X_train, y_train)
print("Feature Importance:")
print(importance.head(10))
```

### Gradient Boosting

```python
from sklearn.ensemble import GradientBoostingRegressor

def train_gradient_boosting(X_train, y_train):
    """Train Gradient Boosting model"""
    gb = GradientBoostingRegressor(
        n_estimators=200,
        learning_rate=0.1,
        max_depth=5,
        random_state=42
    )

    gb.fit(X_train, y_train)
    return gb

# Usage
gb_model = train_gradient_boosting(X_train, y_train)
```

## Model Evaluation

### Comprehensive Evaluation

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import numpy as np

def evaluate_model(model, X_test, y_test, model_name="Model"):
    """Comprehensive model evaluation"""
    predictions = model.predict(X_test)

    metrics = {
        'MAE': mean_absolute_error(y_test, predictions),
        'RMSE': np.sqrt(mean_squared_error(y_test, predictions)),
        'R²': r2_score(y_test, predictions),
        'MAPE': np.mean(np.abs((y_test - predictions) / y_test)) * 100
    }

    print(f"\n{model_name} Evaluation:")
    print(f"  MAE:  ${metrics['MAE']:,.0f}")
    print(f"  RMSE: ${metrics['RMSE']:,.0f}")
    print(f"  R²:   {metrics['R²']:.3f}")
    print(f"  MAPE: {metrics['MAPE']:.1f}%")

    return metrics, predictions

# Usage
metrics, predictions = evaluate_model(model, X_test, y_test, "Linear Regression")
```

### Compare Multiple Models

```python
def compare_models(models, X_test, y_test):
    """Compare multiple models"""
    results = []

    for name, model in models.items():
        metrics, _ = evaluate_model(model, X_test, y_test, name)
        metrics['Model'] = name
        results.append(metrics)

    comparison = pd.DataFrame(results)
    comparison = comparison.set_index('Model')

    print("\nModel Comparison:")
    print(comparison.round(2))

    return comparison

# Usage
models = {
    'Linear Regression': linear_model,
    'KNN': knn_model,
    'Random Forest': rf_model,
    'Gradient Boosting': gb_model
}
comparison = compare_models(models, X_test, y_test)
```

### Cross-Validation

```python
from sklearn.model_selection import cross_val_score

def cross_validate_model(model, X, y, cv=5):
    """Perform cross-validation"""
    scores = cross_val_score(model, X, y, cv=cv, scoring='neg_mean_absolute_error')
    mae_scores = -scores

    print(f"Cross-Validation MAE: ${mae_scores.mean():,.0f} (+/- ${mae_scores.std():,.0f})")
    return mae_scores

# Usage
cv_scores = cross_validate_model(rf_model, X, y)
```

## Prediction Pipeline

### Complete Prediction Function

```python
import joblib

def create_prediction_pipeline(model, feature_names, scaler=None):
    """Create a reusable prediction pipeline"""

    def predict_cost(project_data):
        """
        Predict cost for new project

        Args:
            project_data: dict with project features

        Returns:
            Predicted cost and confidence interval
        """
        # Create DataFrame from input
        df = pd.DataFrame([project_data])

        # Ensure all required features
        for col in feature_names:
            if col not in df.columns:
                df[col] = 0

        df = df[feature_names]

        # Scale if necessary
        if scaler:
            df = scaler.transform(df)

        # Predict
        prediction = model.predict(df)[0]

        # Confidence interval (simple estimation)
        confidence = 0.15  # 15% margin
        lower = prediction * (1 - confidence)
        upper = prediction * (1 + confidence)

        return {
            'predicted_cost': prediction,
            'lower_bound': lower,
            'upper_bound': upper,
            'confidence_level': f"{(1-confidence)*100:.0f}%"
        }

    return predict_cost

# Usage
predictor = create_prediction_pipeline(rf_model, X.columns.tolist())

# Predict new project
new_project = {
    'area_m2': 5000,
    'floors': 8,
    'complexity_score': 3,
    'material_quality': 2
}

result = predictor(new_project)
print(f"Predicted Cost: ${result['predicted_cost']:,.0f}")
print(f"Range: ${result['lower_bound']:,.0f} - ${result['upper_bound']:,.0f}")
```

### Save and Load Model

```python
import joblib

# Save model
def save_model(model, filepath):
    """Save trained model to file"""
    joblib.dump(model, filepath)
    print(f"Model saved to {filepath}")

# Load model
def load_model(filepath):
    """Load model from file"""
    model = joblib.load(filepath)
    print(f"Model loaded from {filepath}")
    return model

# Usage
save_model(rf_model, "cost_prediction_model.pkl")
loaded_model = load_model("cost_prediction_model.pkl")
```

## Using with ChatGPT

```python
# Prompt for ChatGPT to help with cost prediction

prompt = """
I have historical construction project data with these columns:
- area_m2: Building area in square meters
- floors: Number of floors
- building_type: residential, commercial, industrial
- total_cost: Total project cost in USD

Write Python code using scikit-learn to:
1. Prepare the data for machine learning
2. Train a Random Forest model
3. Evaluate the model
4. Predict cost for a new 3000 m² commercial building with 5 floors
"""
```

## Quick Reference

| Task | Code |
|------|------|
| Split data | `train_test_split(X, y, test_size=0.2)` |
| Linear Regression | `LinearRegression().fit(X, y)` |
| KNN | `KNeighborsRegressor(n_neighbors=5)` |
| Random Forest | `RandomForestRegressor(n_estimators=100)` |
| Predict | `model.predict(X_new)` |
| MAE | `mean_absolute_error(y_true, y_pred)` |
| R² Score | `r2_score(y_true, y_pred)` |
| Cross-validate | `cross_val_score(model, X, y, cv=5)` |
| Save model | `joblib.dump(model, 'file.pkl')` |

## Best Practices

1. **Data Quality**: More historical data = better predictions
2. **Feature Selection**: Include relevant project characteristics
3. **Inflation Adjustment**: Normalize costs to current prices
4. **Regular Retraining**: Update model with new completed projects
5. **Ensemble Methods**: Combine multiple models for robustness
6. **Confidence Intervals**: Always provide prediction ranges

## Resources

- **Book**: "Data-Driven Construction" by Artem Boiko, Chapter 4.5
- **Website**: https://datadrivenconstruction.io
- **scikit-learn**: https://scikit-learn.org

## Next Steps

- See `duration-prediction` for project duration forecasting
- See `ml-model-builder` for custom ML workflows
- See `kpi-dashboard` for visualization
- See `big-data-analysis` for large dataset processing
