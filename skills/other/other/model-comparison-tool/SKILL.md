---
name: model-comparison-tool
description: Use when asked to compare multiple ML models, perform cross-validation, evaluate metrics, or select the best model for a classification/regression task.
---

# Model Comparison Tool

Compare multiple machine learning models systematically with cross-validation, metric evaluation, and automated model selection.

## Purpose

Model comparison for:
- Algorithm selection and benchmarking
- Hyperparameter tuning comparison
- Model performance validation
- Feature engineering evaluation
- Production model selection

## Features

- **Multi-Model Comparison**: Test 5+ algorithms simultaneously
- **Cross-Validation**: K-fold, stratified, time-series splits
- **Comprehensive Metrics**: Accuracy, F1, ROC-AUC, RMSE, MAE, R²
- **Statistical Testing**: Paired t-tests for significance
- **Visualization**: Performance charts, ROC curves, learning curves
- **Auto-Selection**: Recommend best model based on criteria

## Quick Start

```python
from model_comparison_tool import ModelComparisonTool

# Compare classifiers
comparator = ModelComparisonTool()
comparator.load_data(X_train, y_train, task='classification')

results = comparator.compare_models(
    models=['rf', 'gb', 'lr', 'svm'],
    cv_folds=5
)

best_model = comparator.get_best_model(metric='f1')
```

## CLI Usage

```bash
# Compare models on CSV data
python model_comparison_tool.py --data data.csv --target target --task classification

# Custom model comparison
python model_comparison_tool.py --data data.csv --target price --task regression --models rf,gb,lr --cv 10

# Export results
python model_comparison_tool.py --data data.csv --target y --output comparison_report.html
```

## Limitations

- Requires sufficient data for meaningful cross-validation
- Large datasets may have long comparison times
- Deep learning models not included (use dedicated frameworks)
- Feature engineering must be done beforehand
