---
name: model-explainer
description: |
  Model interpretability and explainability using SHAP, LIME, feature importance, and partial dependence plots. Activates for "explain model", "model interpretability", "SHAP", "LIME", "feature importance", "why prediction", "model explanation". Generates human-readable explanations for model predictions, critical for trust, debugging, and regulatory compliance.
---

# Model Explainer

## Overview

Makes black-box models interpretable. Explains why models make specific predictions, which features matter most, and how features interact. Critical for trust, debugging, and regulatory compliance.

## Why Explainability Matters

- **Trust**: Stakeholders trust models they understand
- **Debugging**: Find model weaknesses and biases
- **Compliance**: GDPR, fair lending laws require explanations
- **Improvement**: Understand what to improve
- **Safety**: Detect when model might fail

## Explanation Types

### 1. Global Explanations (Model-Level)

**Feature Importance**:
```python
from specweave import explain_model

explainer = explain_model(
    model=trained_model,
    X_train=X_train,
    increment="0042"
)

# Global feature importance
importance = explainer.feature_importance()
```

Output:
```
Top Features (Global):
1. transaction_amount (importance: 0.35)
2. user_history_days (importance: 0.22)
3. merchant_reputation (importance: 0.18)
4. time_since_last_transaction (importance: 0.15)
5. device_type (importance: 0.10)
```

**Partial Dependence Plots**:
```python
# How does feature affect prediction?
explainer.partial_dependence(feature="transaction_amount")
```

### 2. Local Explanations (Prediction-Level)

**SHAP Values**:
```python
# Explain single prediction
explanation = explainer.explain_prediction(X_sample)
```

Output:
```
Prediction: FRAUD (probability: 0.92)

Why?
+ transaction_amount=5000 → +0.45 (high amount increases fraud risk)
+ user_history_days=2 → +0.30 (new user increases risk)
+ merchant_reputation=low → +0.25 (suspicious merchant)
- time_since_last_transaction=1hr → -0.08 (recent activity normal)

Base prediction: 0.10
Final prediction: 0.92
```

**LIME Explanations**:
```python
# Local interpretable model
lime_exp = explainer.lime_explanation(X_sample)
```

## Usage in SpecWeave

```python
from specweave import ModelExplainer

# Create explainer
explainer = ModelExplainer(
    model=model,
    X_train=X_train,
    feature_names=feature_names,
    increment="0042"
)

# Generate all explanations
explainer.generate_all_reports()

# Creates:
# - feature-importance.png
# - shap-summary.png
# - pdp-plots/
# - local-explanations/
# - explainability-report.md
```

## Real-World Examples

### Example 1: Fraud Detection

```python
# Explain why transaction flagged as fraud
transaction = {
    "amount": 5000,
    "user_age_days": 2,
    "merchant": "new_merchant_xyz"
}

explanation = explainer.explain(transaction)
print(explanation.to_text())
```

Output:
```
FRAUD ALERT (92% confidence)

Main factors:
1. Large transaction amount ($5000) - Very unusual for new users
2. Account only 2 days old - Fraud pattern
3. Merchant has low reputation score - Red flag

If this is legitimate:
- User should verify identity
- Merchant should be manually reviewed
```

### Example 2: Loan Approval

```python
# Explain loan rejection
applicant = {
    "income": 45000,
    "credit_score": 620,
    "debt_ratio": 0.45
}

explanation = explainer.explain(applicant)
print(explanation.to_text())
```

Output:
```
LOAN DENIED

Main reasons:
1. Credit score (620) below threshold (650) - Primary factor
2. High debt-to-income ratio (45%) - Risk indicator
3. Income ($45k) adequate but not strong

To improve approval chances:
- Increase credit score by 30+ points
- Reduce debt-to-income ratio below 40%
```

## Regulatory Compliance

### GDPR "Right to Explanation"

```python
# Generate GDPR-compliant explanation
gdpr_explanation = explainer.gdpr_explanation(prediction)

# Includes:
# - Decision rationale
# - Data used
# - How to contest decision
# - Impact of features
```

### Fair Lending Act

```python
# Check for bias in protected attributes
bias_report = explainer.fairness_report(
    sensitive_features=["gender", "race", "age"]
)

# Detects:
# - Disparate impact
# - Feature bias
# - Recommendations for fairness
```

## Visualization Types

1. **Feature Importance Bar Chart**
2. **SHAP Summary Plot** (beeswarm)
3. **SHAP Waterfall** (single prediction)
4. **Partial Dependence Plots**
5. **Individual Conditional Expectation** (ICE)
6. **Force Plots** (interactive)
7. **Decision Trees** (surrogate models)

## Integration with SpecWeave

```bash
# Generate all explainability artifacts
/ml:explain-model 0042

# Explain specific prediction
/ml:explain-prediction --increment 0042 --sample sample.json

# Check for bias
/ml:fairness-check 0042
```

Explainability artifacts automatically included in increment documentation and COMPLETION-SUMMARY.

## Best Practices

1. **Generate explanations for all production models** - No "black boxes" in production
2. **Check for bias** - Test sensitive attributes
3. **Document limitations** - What model can't explain
4. **Validate explanations** - Do they make domain sense?
5. **Make explanations accessible** - Non-technical stakeholders should understand

Model explainability is non-negotiable for responsible AI deployment.
