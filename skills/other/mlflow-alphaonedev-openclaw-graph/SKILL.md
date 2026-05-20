---
name: mlflow
cluster: aimlops
description: "MLflow is an open-source platform for managing the machine learning lifecycle, including tracking, packaging, and deploy"
tags: ["mlflow","mlops","machine-learning"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "mlflow machine learning mlops tracking deployment models"
---

# mlflow

## Purpose
MLflow is an open-source platform for tracking experiments, packaging ML models, and deploying them in the machine learning lifecycle. It helps standardize workflows for reproducibility and collaboration.

## When to Use
Use MLflow when managing multiple ML experiments, comparing models, or deploying to production. It's ideal for teams in MLOps pipelines, such as hyperparameter tuning in Jupyter notebooks, or scaling model deployment in cloud environments like AWS or Azure.

## Key Capabilities
- **Experiment Tracking**: Record metrics, parameters, and artifacts for each run.
- **Model Packaging**: Save models in a standard format (e.g., MLmodel) for easy sharing.
- **Model Deployment**: Serve models as REST APIs or integrate with platforms like Kubernetes.
- **UI and API**: Provides a web UI for visualization and a Python API for programmatic access.
- **Artifact Storage**: Supports backends like S3, Azure Blob, or local files for storing outputs.

## Usage Patterns
Start by initializing a tracking server or using the local backend. For a typical workflow, import MLflow in your script, log metrics during training, and register models after evaluation. Always set the tracking URI first (e.g., via environment variable). For production, package models and deploy via MLflow's serving tools. Avoid running experiments without tracking to prevent loss of reproducibility.

## Common Commands/API
Use the MLflow CLI for quick operations or the Python API for integration in code.

- **CLI Commands**:
  - Start a tracking server: `mlflow server --host 0.0.0.0 --port 5000`
  - Run an experiment: `mlflow run . -e main --experiment-name my_exp`
  - Log metrics in a script: Use flags like `--param key=value` for parameters.
  - Deploy a model: `mlflow models serve -m models:/MyModel/1 -p 5001`

- **Python API Snippets**:
  - Start tracking:  
    ```python
    import mlflow
    mlflow.set_tracking_uri("http://localhost:5000")
    with mlflow.start_run():
        mlflow.log_param("alpha", 0.1)
    ```
  - Log metrics:  
    ```python
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_artifact("model.pkl")
    ```
  - Register a model:  
    ```python
    mlflow.sklearn.log_model(sk_model, "model")
    mlflow.register_model("runs:/<run_id>/model", "MyModel")
    ```

Config formats include YAML for project specifications (e.g., in mlflow projects: `entry_points: main: parameters: alpha: {type: float, default: 0.1}`). Set environment variables for auth, like `export MLFLOW_TRACKING_USERNAME=$YOUR_USERNAME` and `export MLFLOW_TRACKING_PASSWORD=$YOUR_PASSWORD` when using a secured server.

## Integration Notes
Integrate MLflow with frameworks like Scikit-learn, TensorFlow, or PyTorch by using their respective logging functions (e.g., `mlflow.sklearn.autolog()`). For cloud storage, set `MLFLOW_S3_ENDPOINT_URL` for S3 compatibility. When combining with tools like Airflow, use MLflow's API to trigger runs from DAGs. Always specify the tracking URI via `os.environ['MLFLOW_TRACKING_URI'] = 'http://your-server:5000'` before API calls. For authentication in remote setups, use env vars like `$MLFLOW_TRACKING_TOKEN` for API keys.

## Error Handling
Handle common errors by checking for issues like unreachable tracking URIs or invalid model formats. For example, if a server is down, catch `MlflowException` in Python:  
```python
try:
    mlflow.set_tracking_uri("http://localhost:5000")
except mlflow.exceptions.MlflowException as e:
    print(f"Error: {e}. Check server status and retry.")
```
For CLI, use verbose mode with `--verbose` to debug failed runs. Validate inputs before logging (e.g., ensure metrics are numbers). If artifacts fail to upload, verify storage permissions or use alternative backends like `--backend-store-uri sqlite:///mlflow.db`.

## Concrete Usage Examples
1. **Tracking a Scikit-learn Model**: In a script, train a model and log it:  
   ```python
   import mlflow.sklearn
   from sklearn.ensemble import RandomForestClassifier
   model = RandomForestClassifier()
   model.fit(X_train, y_train)
   with mlflow.start_run():
       mlflow.sklearn.log_model(model, "rf_model")
   ```
   Then, view runs via `mlflow ui` and compare metrics.

2. **Deploying a Trained Model**: After training, package and serve:  
   Run `mlflow models build-docker -m runs:/<run_id>/model -n my_image`. Then, deploy with `docker run -p 5000:8080 my_image`, and query the endpoint via `curl -d 'json data' http://localhost:5000/invocations`.

## Graph Relationships
- Related to cluster: aimlops (e.g., connects with other MLOps tools like Kubeflow or DVC).
- Tags: mlflow (direct match), mlops (workflow integration), machine-learning (core functionality).
- Dependencies: Often pairs with Python ML libraries (e.g., scikit-learn) and storage systems (e.g., S3).
