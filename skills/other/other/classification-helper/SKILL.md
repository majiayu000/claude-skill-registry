---
name: classification-helper
description: Quick classifier training with automatic model selection, hyperparameter tuning, and comprehensive evaluation metrics.
---

# Classification Helper

Train and evaluate classification models with automatic model selection.

## Features

- **Auto Model Selection**: Compare multiple classifiers
- **Hyperparameter Tuning**: Grid/random search
- **Evaluation Metrics**: Accuracy, precision, recall, F1, ROC-AUC
- **Cross-Validation**: K-fold validation
- **Confusion Matrix**: Detailed error analysis
- **Feature Importance**: Top predictive features
- **Model Export**: Save trained models

## CLI Usage

```bash
python classification_helper.py --data train.csv --target class --test test.csv --output model.pkl
```

## Dependencies

- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
- matplotlib>=3.7.0
- seaborn>=0.12.0
