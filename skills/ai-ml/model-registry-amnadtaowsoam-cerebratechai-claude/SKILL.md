---
name: AI Model Registry
description: Centralized management of machine learning models throughout their lifecycle, including versioning, metadata, and production deployment.
---

# AI Model Registry

## Overview

An AI Model Registry is a central repository used by data scientists and ML engineers to store, manage, and version machine learning models. It acts as the "source of truth" for models, tracking everything from hyperparameters to production status.

**Core Principle**: "Models are software artifacts. They must be versioned, audited, and controlled with the same rigor as source code."

---

## 1. Why a Model Registry is Essential

Without a registry, models are often stored as files like `model_v2_final_final.pkl` in S3 buckets, leading to:
*   **Shadow Models**: Models running in production that no one can find the source for.
*   **Version Mismatch**: Predicting with `v2` code but `v1` model weights.
*   **Lack of Audit**: Inability to explain why a model was promoted to production.

---

## 2. Core Components of a Registry

| Component | Description |
| :--- | :--- |
| **Versioning** | Tracking major and minor changes (e.g., `v1.0.0` -> `v1.1.0`). |
| **Metadata** | Storing hyperparameters, training datasets, and performance metrics. |
| **Artifacts** | The actual binary files (Pickles, ONNX, TensorFlow SavedModel). |
| **Lineage** | Linking the model to the exact code commit and data contract used. |
| **Stages** | Defining the lifecycle: `Staging`, `Production`, `Archived`. |

---

## 3. Implementation with MLflow

MLflow is the industry standard for model registries.

### Registering a Model (Python)
```python
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor

# 1. Start a training run
with mlflow.start_run():
    model = RandomForestRegressor().fit(X_train, y_train)
    mlflow.log_metric("accuracy", 0.95)
    
    # 2. Log and register the model
    mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name="CustomerChurnModel"
    )
```

### Transitioning Stages
```python
client = mlflow.tracking.MlflowClient()

# Promote to Production
client.transition_model_version_stage(
    name="CustomerChurnModel",
    version=3,
    stage="Production"
)
```

---

## 4. Model Metadata: The "Model Card"

A Registry should enforce the creation of a **Model Card** (Google Standard) for every production model:

```yaml
# model_card.yaml
name: "FaceSentimentAnalyzer"
version: "2.4.0"
intended_use: "Analyzing user engagement in video calls."
limitations: "Performance drops in low-light conditions."
training_dataset: "internal_video_dataset_v4"
fairness_metrics:
  demographic_parity: 0.95
  equal_opportunity: 0.92
owner: "ai-vision-team"
```

---

## 5. Model Deployment Patterns

How models move from Registry to Serving:

1.  **Direct Loading**: Serving app pulls the "Production" model from the registry at startup.
2.  **Containerized**: The model is baked into a Docker image (more stable for scaling).
3.  **Inference Proxy**: A service (like Seldon or BentoML) talks to the Registry and handles the routing.

---

## 6. Registry Tools Landscape

| Tool | Focus | Best For |
| :--- | :--- | :--- |
| **MLflow Registry** | Open Source | Standard data science workflows. |
| **Weights & Biases**| Visual experimentation| Deep learning and collaborative teams. |
| **AWS SageMaker** | Managed Cloud | Integrated "Model Monitor" and "Model Registry". |
| **Azure ML Registry**| Enterprise | Large organizations with strict compliance. |
| **Hugging Face Hub**| Pre-trained models | Community and open-source foundation models. |

---

## 7. Model Audit and Compliance

For regulated industries (Finance, Healthcare), the registry must answer:
*   Who trained this model?
*   What data was it trained on?
*   Was the model validated by a third party before production?
*   Are there biases documented in the metadata?

---

## 8. Real-World Scenario: The "Zombie" Pricing Model
*   **Scenario**: A travel app saw prices fluctuating wildly. Engineers couldn't find the bug in the code.
*   **Discovery**: The Model Registry showed that a "Candidate" model with an experimental pricing algorithm had accidentally been pulled into production because of a misconfigured "Latest" tag.
*   **Remediation**: Reverted the stage to "Archive" in MLflow. The serving layer automatically pulled the previous "Production" version within 30 seconds.

---

## 9. AI Model Registry Checklist

- [ ] **Versioning**: Is every change to hyperparameters tracked as a new version?
- [ ] **Code Link**: Is the Git commit hash stored in the model metadata?
- [ ] **Metric Logging**: Are P95/P99 accuracy metrics logged for comparison?
- [ ] **Role-Based Access**: Can only authorized leads promote models to "Production"?
- [ ] **Format**: Are models stored in an interoperable format like **ONNX**?
- [ ] **Alerting**: Does the team get notified when a model's stage changes?

---

## Related Skills
* `44-ai-governance/model-risk-management`
* `44-ai-governance/model-explainability`
* `43-data-reliability/data-lineage`
