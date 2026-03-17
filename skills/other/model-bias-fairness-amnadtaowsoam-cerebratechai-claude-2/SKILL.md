---
name: Model Bias and Fairness
description: Identifying, measuring, and mitigating algorithmic bias to ensure equitable outcomes in AI systems.
---

# Model Bias and Fairness

## Overview

Model Bias occurs when an AI system produces results that are systematically prejudiced against certain individuals or groups. Fairness is the practice of ensuring that the model's predictions do not vary unfairly across protected attributes (e.g., race, gender, age).

**Core Principle**: "Bias is a feature of data, fairness is a requirement of the system."

---

## 1. Types of Algorithmic Bias

| Bias Type | Description | Example |
| :--- | :--- | :--- |
| **Historical Bias** | Pre-existing prejudice in the world. | Credit scoring models reflecting historical redlining. |
| **Representation Bias**| Underrepresentation of certain groups in training data. | Facial recognition failing on darker skin tones. |
| **Measurement Bias** | Issues with how data is collected or labeled. | Using "Arrests" as a proxy for "Crime" when certain areas are over-policed. |
| **Algorithmic Bias** | The math itself favors a certain outcome. | Maximizing "Total Revenue" might favor high-income zip codes unfairly. |

---

## 2. Quantitative Fairness Metrics

You cannot manage what you do not measure.

| Metric | Goal | Equation |
| :--- | :--- | :--- |
| **Demographic Parity** | Outcome should be equal across groups. | $P(\hat{Y}=1 | G=A) = P(\hat{Y}=1 | G=B)$ |
| **Equal Opportunity** | True Positive Rate should be equal. | $P(\hat{Y}=1 | Y=1, G=A) = P(\hat{Y}=1 | Y=1, G=B)$ |
| **Disparate Impact** | Ratio of selection rates. | Success Rate (B) / Success Rate (A) should be > 0.8. |

---

## 3. Mitigation Strategies

### A. Pre-processing (Data Level)
*   **Reweighing**: Assigning higher weights to underrepresented samples.
*   **Oversampling**: Creating synthetic data for minority groups.

### B. In-processing (Model Level)
*   **Adversarial Debiasing**: Training a "De-biaser" alongside the model.
*   **Fairness Constraints**: Adding a "Fairness Penalty" to the loss function.

### C. Post-processing (Prediction Level)
*   **Threshold Moving**: Adjusting the binary classification threshold differently for different groups to equalize error rates.

---

## 4. Implementation with Fairlearn (Python)

Fairlearn is a popular open-source tool for measuring and mitigating bias.

### Measuring Disparity
```python
from fairlearn.metrics import MetricFrame, selection_rate
from sklearn.metrics import accuracy_score

# Group by 'gender'
gm = MetricFrame(
    metrics=accuracy_score,
    y_true=y_true,
    y_pred=y_pred,
    sensitive_features=X_test['gender']
)

print(gm.by_group)
print(f"Accuracy Disparity: {gm.difference()}")
```

### Mitigating Bias (Threshold Optimization)
```python
from fairlearn.postprocessing import ThresholdOptimizer

optimizer = ThresholdOptimizer(
    estimator=unconstrained_model,
    constraints="equalized_odds"
)

optimizer.fit(X_train, y_train, sensitive_features=X_train['gender'])
```

---

## 5. The Fairness Audit Workflow

1.  **Identify Protected Attributes**: Define which groups (Gender, Race, Age) must be protected.
2.  **Baseline Measurement**: Calculate fairness metrics on the current production model.
3.  **Root Cause Analysis**: Is the bias coming from the dataset size or the labels?
4.  **Mitigation Application**: Select a technique (e.g., Reweighing).
5.  **Trade-off Analysis**: Usually, increasing fairness slightly decreases overall accuracy.
6.  **Continuous Monitoring**: Alerting if fairness metrics drop over time (Bias Drift).

---

## 6. Tools Landscape

1.  **AIF360 (IBM)**: Comprehensive library with over 70 fairness metrics.
2.  **Fairlearn (Microsoft)**: Focused on mitigation and visualization.
3.  **Google What-If Tool**: Interactive dashboard to explore fairness trade-offs without code.
4.  **NIST AI RMF**: Framework for managing AI risks including bias.

---

## 7. Compliance: EU AI Act & NIST

Regulators are increasingly requiring "Fairness Audits" for high-risk AI (Employment, Lending, Law Enforcement).
*   **EU AI Act**: Requires data quality and bias documentation for high-risk systems.
*   **NIST AI 100-1**: Guidelines for identifying and managing bias.

---

## 8. Real-World Scenario: The Recruitment Filter
*   **Scenario**: An AI tool for screening resumes was systematically favoring male candidates.
*   **Investigation**: The model was trained on 10 years of historical hire data. Historically, the company hired mostly men. The model learned that words like "Captain" and "Competitive" (more common on men's resumes) were high-value features.
*   **Action**: Amazon eventually scrapped the tool.
*   **Lesson**: If the historical data is biased, the model will faithfully reproduce and amplify that bias.

---

## 9. Model Fairness Checklist

- [ ] **Protected Attributes**: Have we identified and explicitly tagged sensitive features?
- [ ] **Disparate Impact**: Is our selection rate ratio > 0.8 for all groups?
- [ ] **Equal Opportunity**: Do we have the same "False Negative" rate for all ethnicities?
- [ ] **Representation**: Does our training set match the demographic distribution of our real users?
- [ ] **Trade-off**: Have we documented the accuracy cost of our fairness mitigation?
- [ ] **Governance**: Has the Ethics Review Board approved the model's fairness report?

---

## Related Skills
* `44-ai-governance/ai-ethics-compliance`
* `44-ai-governance/model-explainability`
* `43-data-reliability/data-quality-monitoring`
