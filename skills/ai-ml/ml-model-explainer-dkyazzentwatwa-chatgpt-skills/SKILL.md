---
name: ml-model-explainer
description: Explain ML model predictions using SHAP values, feature importance, and decision paths with visualizations.
---

# ML Model Explainer

Explain machine learning model predictions using SHAP and feature importance.

## Features

- **SHAP Values**: Explain individual predictions
- **Feature Importance**: Global feature rankings
- **Decision Paths**: Trace prediction logic
- **Visualizations**: Waterfall, force plots, summary plots
- **Multiple Models**: Support for tree-based, linear, neural networks
- **Batch Explanations**: Explain multiple predictions

## Quick Start

```python
from ml_model_explainer import MLModelExplainer

explainer = MLModelExplainer()
explainer.load_model(model, X_train)

# Explain single prediction
explanation = explainer.explain(X_test[0])
explainer.plot_waterfall('explanation.png')

# Feature importance
importance = explainer.feature_importance()
```

## CLI Usage

```bash
python ml_model_explainer.py --model model.pkl --data test.csv --output explanations/
```

## Dependencies

- shap>=0.42.0
- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
