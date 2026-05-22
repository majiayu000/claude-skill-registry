---
name: MLflow Patterns
description: ML experiment tracking, model registry, and deployment with MLflow for reproducible machine learning workflows.
---

# MLflow Patterns

## Overview

MLflow เป็น open-source platform สำหรับ managing ML lifecycle ครอบคลุม experiment tracking, model packaging, model registry, และ deployment ช่วยให้ทีม data science ทำงานร่วมกันและ deploy models ได้อย่าง reproducible

## Why This Matters

- **Reproducibility**: Track experiments และ reproduce results
- **Collaboration**: Share experiments และ models across team
- **Deployment**: Package และ deploy models consistently
- **Governance**: Model versioning และ approval workflow

---

## Core Concepts

### 1. Experiment Tracking

```python
import mlflow
from mlflow.tracking import MlflowClient

# Set tracking URI
mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("customer-churn-prediction")

# Start run with auto-logging
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="xgboost-v1") as run:
    # Log parameters
    mlflow.log_params({
        "learning_rate": 0.1,
        "max_depth": 6,
        "n_estimators": 100,
        "subsample": 0.8,
    })
    
    # Train model
    model = XGBClassifier(
        learning_rate=0.1,
        max_depth=6,
        n_estimators=100,
        subsample=0.8,
    )
    model.fit(X_train, y_train)
    
    # Log metrics
    y_pred = model.predict(X_test)
    mlflow.log_metrics({
        "accuracy": accuracy_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
        "f1": f1_score(y_test, y_pred),
        "auc_roc": roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]),
    })
    
    # Log artifacts
    mlflow.log_artifact("feature_importance.png")
    mlflow.log_artifact("confusion_matrix.png")
    
    # Log model
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="churn-prediction-model",
    )
    
    # Log dataset info
    mlflow.log_input(
        mlflow.data.from_pandas(X_train, source="s3://data/train.parquet"),
        context="training"
    )
    
    print(f"Run ID: {run.info.run_id}")
```

### 2. Custom Model Wrapper

```python
import mlflow.pyfunc

class ChurnModelWrapper(mlflow.pyfunc.PythonModel):
    """Custom model wrapper with preprocessing"""
    
    def load_context(self, context):
        """Load model and artifacts"""
        import joblib
        self.model = joblib.load(context.artifacts["model"])
        self.preprocessor = joblib.load(context.artifacts["preprocessor"])
        self.feature_names = context.artifacts["feature_names"]
    
    def predict(self, context, model_input):
        """Predict with preprocessing"""
        # Validate input
        if not all(col in model_input.columns for col in self.feature_names):
            raise ValueError(f"Missing required features: {self.feature_names}")
        
        # Preprocess
        processed = self.preprocessor.transform(model_input[self.feature_names])
        
        # Predict with probability
        predictions = self.model.predict_proba(processed)[:, 1]
        
        return pd.DataFrame({
            "churn_probability": predictions,
            "churn_prediction": (predictions > 0.5).astype(int),
        })

# Log custom model
with mlflow.start_run():
    artifacts = {
        "model": "model.joblib",
        "preprocessor": "preprocessor.joblib",
        "feature_names": "features.json",
    }
    
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=ChurnModelWrapper(),
        artifacts=artifacts,
        conda_env={
            "dependencies": [
                "python=3.10",
                "scikit-learn=1.3.0",
                "xgboost=2.0.0",
                "pandas=2.0.0",
            ]
        },
        signature=mlflow.models.infer_signature(X_test, predictions),
        input_example=X_test.head(5),
    )
```

### 3. Model Registry

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model from run
model_uri = f"runs:/{run_id}/model"
model_version = mlflow.register_model(model_uri, "churn-prediction-model")

# Add description and tags
client.update_model_version(
    name="churn-prediction-model",
    version=model_version.version,
    description="XGBoost model trained on Q4 2024 data"
)

client.set_model_version_tag(
    name="churn-prediction-model",
    version=model_version.version,
    key="validation_status",
    value="pending"
)

# Transition to staging (after validation)
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=model_version.version,
    stage="Staging",
    archive_existing_versions=False
)

# Promote to production (after approval)
client.transition_model_version_stage(
    name="churn-prediction-model",
    version=model_version.version,
    stage="Production",
    archive_existing_versions=True  # Archive old production version
)

# Load production model
model = mlflow.pyfunc.load_model("models:/churn-prediction-model/Production")
predictions = model.predict(new_data)
```

### 4. Model Validation Pipeline

```python
# validation/validate_model.py
import mlflow
from mlflow.tracking import MlflowClient

def validate_model(model_name: str, version: str) -> bool:
    """Validate model before promotion"""
    
    client = MlflowClient()
    model_uri = f"models:/{model_name}/{version}"
    
    # Load model
    model = mlflow.pyfunc.load_model(model_uri)
    
    # Load validation dataset
    val_data = pd.read_parquet("s3://data/validation.parquet")
    X_val, y_val = val_data.drop("target", axis=1), val_data["target"]
    
    # Run predictions
    predictions = model.predict(X_val)
    
    # Calculate metrics
    metrics = {
        "val_accuracy": accuracy_score(y_val, predictions["churn_prediction"]),
        "val_auc": roc_auc_score(y_val, predictions["churn_probability"]),
    }
    
    # Get production model metrics (if exists)
    try:
        prod_model = mlflow.pyfunc.load_model(f"models:/{model_name}/Production")
        prod_predictions = prod_model.predict(X_val)
        prod_metrics = {
            "prod_accuracy": accuracy_score(y_val, prod_predictions["churn_prediction"]),
            "prod_auc": roc_auc_score(y_val, prod_predictions["churn_probability"]),
        }
    except:
        prod_metrics = {"prod_accuracy": 0, "prod_auc": 0}
    
    # Validation rules
    validations = [
        ("accuracy_threshold", metrics["val_accuracy"] >= 0.85),
        ("auc_threshold", metrics["val_auc"] >= 0.80),
        ("accuracy_improvement", metrics["val_accuracy"] >= prod_metrics["prod_accuracy"]),
        ("auc_improvement", metrics["val_auc"] >= prod_metrics["prod_auc"] - 0.01),  # Allow 1% drop
    ]
    
    # Log validation results
    with mlflow.start_run(run_name=f"validation-{model_name}-v{version}"):
        mlflow.log_metrics(metrics)
        mlflow.log_metrics(prod_metrics)
        
        for name, passed in validations:
            mlflow.log_metric(f"validation_{name}", int(passed))
    
    # Update model tags
    all_passed = all(passed for _, passed in validations)
    client.set_model_version_tag(
        name=model_name,
        version=version,
        key="validation_status",
        value="passed" if all_passed else "failed"
    )
    
    return all_passed
```

### 5. Model Serving

```python
# serve/model_server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mlflow

app = FastAPI()

# Load model at startup
MODEL_NAME = "churn-prediction-model"
MODEL_STAGE = "Production"
model = None

@app.on_event("startup")
async def load_model():
    global model
    model = mlflow.pyfunc.load_model(f"models:/{MODEL_NAME}/{MODEL_STAGE}")

class PredictionRequest(BaseModel):
    features: dict

class PredictionResponse(BaseModel):
    churn_probability: float
    churn_prediction: int
    model_version: str

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    try:
        input_df = pd.DataFrame([request.features])
        predictions = model.predict(input_df)
        
        return PredictionResponse(
            churn_probability=float(predictions["churn_probability"].iloc[0]),
            churn_prediction=int(predictions["churn_prediction"].iloc[0]),
            model_version=model.metadata.run_id,
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy", "model_loaded": model is not None}

# Or use MLflow's built-in serving
# mlflow models serve -m "models:/churn-prediction-model/Production" -p 5001
```

## Quick Start

1. **Install MLflow:**
   ```bash
   pip install mlflow
   ```

2. **Start tracking server:**
   ```bash
   mlflow server --backend-store-uri sqlite:///mlflow.db \
                 --default-artifact-root s3://mlflow-artifacts \
                 --host 0.0.0.0
   ```

3. **Set tracking URI in code:**
   ```python
   mlflow.set_tracking_uri("http://localhost:5000")
   ```

4. **Run experiment:**
   ```python
   with mlflow.start_run():
       mlflow.log_param("param", value)
       mlflow.log_metric("metric", value)
       mlflow.sklearn.log_model(model, "model")
   ```

5. **View in UI:** Open http://localhost:5000

## Production Checklist

- [ ] Tracking server with persistent backend
- [ ] Artifact storage (S3/GCS/Azure Blob)
- [ ] Authentication enabled
- [ ] Model signature defined
- [ ] Input examples logged
- [ ] Conda/pip environment specified
- [ ] Validation pipeline configured
- [ ] Model approval workflow
- [ ] Monitoring for model drift

## Anti-patterns

1. **No Experiment Naming**: Use meaningful experiment/run names
2. **Skipping Signatures**: Always define model signatures
3. **Manual Promotion**: Use validation pipeline for stage transitions
4. **Missing Environment**: Always specify dependencies

## Integration Points

- **Storage**: S3, GCS, Azure Blob, HDFS
- **Databases**: PostgreSQL, MySQL for backend store
- **Orchestration**: Airflow, Prefect, Dagster
- **Serving**: SageMaker, Kubernetes, Azure ML

## Further Reading

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [MLflow Recipes](https://mlflow.org/docs/latest/recipes.html)
