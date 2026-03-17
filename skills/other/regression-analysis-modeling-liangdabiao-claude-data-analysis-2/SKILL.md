---
name: regression-analysis-modeling
description: Perform comprehensive regression analysis and predictive modeling using linear regression, decision trees, and random forests. Use when you need to predict continuous values like housing prices, sales forecasts, demand predictions, or any numerical target variables. Includes automated feature engineering, model comparison, and visualization with Chinese language support.
allowed-tools: Read, Write, Bash, Glob
---

# Regression Analysis & Predictive Modeling

A comprehensive regression analysis skill that automates the complete machine learning workflow from data preparation to model evaluation and interpretation, supporting multiple algorithms and business use cases.

## Instructions

### 1. Data Preparation and Exploration
When users provide datasets for regression analysis:
- Load and validate the data structure and quality
- Handle missing values, outliers, and data type conversions
- Perform exploratory data analysis (EDA) with visualizations
- Identify potential predictors and target variables
- Support both English and Chinese column names and data

### 2. Feature Engineering
- **Date Features**: Extract time-based features from datetime columns
- **Categorical Encoding**: Convert categorical variables to numerical representations
- **Feature Creation**: Generate interaction terms, ratios, and derived features
- **Feature Selection**: Identify most predictive features using statistical methods
- **Data Scaling**: Standardize or normalize features as needed for different algorithms

### 3. Model Training and Selection
- **Linear Regression**: Baseline model with coefficient interpretation
- **Decision Tree Regression**: Non-linear relationships with feature importance
- **Random Forest**: Ensemble method for improved accuracy and robustness
- **Cross-Validation**: K-fold CV to ensure model stability
- **Hyperparameter Tuning**: Automatic optimization of model parameters
- **Model Comparison**: Rank models by performance metrics

### 4. Model Evaluation and Diagnostics
- **Performance Metrics**: R², MAE, RMSE, MAPE for comprehensive evaluation
- **Residual Analysis**: Diagnostic plots to check model assumptions
- **Learning Curves**: Analyze model performance with different data sizes
- **Feature Importance**: Identify key predictors for business insights
- **Prediction Intervals**: Quantify uncertainty in predictions

### 5. Visualization and Reporting
- **Prediction vs Actual**: Scatter plots showing prediction accuracy
- **Residual Plots**: Diagnostic visualizations for model assumptions
- **Feature Importance Charts**: Visual ranking of predictive factors
- **Learning Curve Analysis**: Model performance visualization
- **Comprehensive Reports**: Automated analysis summary with business insights

## Usage Examples

### Housing Price Prediction
```
Build a model to predict house prices:
[CSV with square_footage, rooms, location, age, amenities data]
```

### Sales Forecasting
```
Create a sales prediction model:
[CSV with date, product_id, marketing_spend, seasonality data]
```

### Risk Assessment
```
Predict risk scores based on customer attributes:
[CSV with demographic, behavioral, historical data]
```

## Key Features

### Automated ML Pipeline
- **End-to-End Processing**: From raw data to final predictions
- **Multiple Algorithm Support**: Linear, Tree-based, and Ensemble methods
- **Smart Feature Engineering**: Automatic creation of relevant features
- **Model Selection**: Data-driven algorithm recommendation
- **Chinese Language Support**: Full support for Chinese data and outputs

### Business-Focused Outputs
- **Actionable Insights**: Feature importance translated to business context
- **Model Interpretability**: Clear explanations of prediction logic
- **Performance Benchmarks**: Industry-standard evaluation metrics
- **Risk Assessment**: Prediction confidence intervals
- **ROI Analysis**: Business impact quantification

### Advanced Analytics
- **Time Series Features**: Automatic handling of temporal data
- **Cross-Validation**: Robust model performance estimation
- **Ensemble Methods**: Combining multiple models for better accuracy
- **Hyperparameter Optimization**: Automated model tuning

## File Requirements

### For General Regression:
- **target_variable**: Variable to predict (e.g., price, sales, risk score)
- **predictor_variables**: Features used for prediction
- **Sufficient sample size**: Minimum 100 rows for reliable modeling

## Output Files Generated

- **model_results.csv**: Complete predictions with confidence intervals
- **feature_importance.csv**: Ranked feature importance with scores
- **model_comparison.csv**: Performance metrics for all tested models
- **prediction_plots.png**: Comprehensive visualization dashboard
- **regression_analysis_report.md**: Detailed analysis and business insights
- **model_coefficients.csv**: Linear regression model coefficients

## Dependencies

- **Core ML**: scikit-learn, pandas, numpy
- **Visualization**: matplotlib, seaborn (with Chinese font support)
- **Statistical Analysis**: scipy for statistical tests
- **Data Processing**: Standard Python libraries for file operations

## Best Practices

### Data Preparation
- Ensure consistent data formatting and encoding
- Handle missing values appropriately (imputation vs removal)
- Remove or transform outliers based on domain knowledge
- Validate data types and ranges before modeling

### Model Development
- Always split data into training and testing sets
- Use cross-validation for robust performance estimation
- Compare multiple algorithms before final selection
- Consider business constraints and interpretability requirements

### Interpretation and Deployment
- Focus on business-relevant metrics over purely statistical ones
- Validate model predictions against domain expertise
- Document model limitations and appropriate use cases
- Establish monitoring procedures for deployed models

## Advanced Features

### Automated Feature Engineering
- **Temporal Features**: Time-based pattern extraction
- **Interaction Terms**: Automatic feature combination
- **Polynomial Features**: Non-linear relationship capture

### Model Diagnostics
- **Residual Analysis**: Check model assumptions
- **Leverage Points**: Identify influential observations
- **Multicollinearity**: Detect correlated predictors
- **Heteroscedasticity**: Test for constant variance

### Business Integration
- **ROI Calculation**: Business impact quantification
- **Scenario Analysis**: What-if predictions
- **Threshold Optimization**: Business-specific cutoff tuning
- **A/B Testing Support**: Model validation framework