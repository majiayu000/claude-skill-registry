---
name: feature-engineering-kit
description: Auto-generate features with encodings, scaling, polynomial features, and interaction terms for ML pipelines.
---

# Feature Engineering Kit

Automated feature engineering with encodings, scaling, and transformations.

## Features

- **Encodings**: One-hot, label, target encoding
- **Scaling**: Standard, min-max, robust scaling
- **Polynomial Features**: Generate interactions
- **Binning**: Discretize continuous features
- **Date Features**: Extract time-based features
- **Text Features**: TF-IDF, word counts
- **Missing Value Handling**: Imputation strategies

## CLI Usage

```bash
python feature_engineering.py --data train.csv --output engineered.csv --config config.json
```

## Dependencies

- scikit-learn>=1.3.0
- pandas>=2.0.0
- numpy>=1.24.0
