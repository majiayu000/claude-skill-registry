---
name: mlflow
description: MLflow ML lifecycle management. Use for ML experiment tracking.
---

# MLflow

MLflow is the standard for tracking experiments. v3.0 (2025) pivots to **GenAI**, adding LLM Tracing, Prompt Management, and "LLM-as-a-Judge".

## When to Use

- **Experiment Tracking**: Logging hyperparameters (`lr=0.01`) and metrics (`accuracy=0.98`).
- **GenAI Tracing**: Visualizing the full chain of a RAG application.
- **Model Registry**: Versioning models (`my-model/v3`) for deployment.

## Core Concepts

### Tracking URI

Where logs are stored (local `./mlruns` or remote `http://mlflow-server`).

### Autologging

`mlflow.autolog()` automatically captures params from Scikit-learn, PyTorch, etc.

### LLM Tracing

OpenTelemetry-based tracing to debug prompt chains.

## Best Practices (2025)

**Do**:

- **Use `mlflow.evaluate()`**: To run "LLM-as-a-Judge" metrics on your RAG pipeline.
- **Use Prompt Engineering UI**: MLflow 3.0 has a UI to iterate on prompts.

**Don't**:

- **Don't use it for data storage**: Log artifacts (models), not datasets. Log metadata about datasets instead.

## References

- [MLflow Documentation](https://mlflow.org/)
