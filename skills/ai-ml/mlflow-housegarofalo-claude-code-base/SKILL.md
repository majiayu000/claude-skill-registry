---
name: mlflow
description: "ML lifecycle management with MLflow. Track experiments, package models, manage registries, and deploy models. Use for ML operations, experiment tracking, and model deployment."
---

# MLflow Skill

Complete guide for MLflow - ML lifecycle platform.

## Triggers

Use this skill when:
- Tracking ML experiments and parameters
- Managing model registries and versioning
- Deploying ML models to production
- Working with MLflow tracking, projects, or serving
- Implementing MLOps workflows
- Keywords: mlflow, experiment tracking, model registry, mlops, model deployment, ml lifecycle

## Quick Reference

### Components
| Component | Description |
|-----------|-------------|
| **Tracking** | Log experiments |
| **Projects** | Package ML code |
| **Models** | Model packaging |
| **Registry** | Model versioning |
| **Serving** | Model deployment |

### CLI Commands
```bash
mlflow run .                    # Run project
mlflow ui                       # Start UI
mlflow models serve -m model    # Serve model
mlflow server                   # Start tracking server
```

---

## 1. Installation

```bash
# Core
pip install mlflow

# With extras
pip install mlflow[extras]

# Specific integrations
pip install mlflow[gateway]     # AI Gateway
pip install mlflow[genai]       # GenAI tracking
```

---

## 2. Experiment Tracking

### Basic Logging
```python
import mlflow

# Set experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)

    # Log metrics
    mlflow.log_metric("accuracy", 0.95)
    mlflow.log_metric("loss", 0.05)

    # Log multiple metrics over time
    for epoch in range(10):
        mlflow.log_metric("train_loss", 0.1 - epoch * 0.01, step=epoch)

    # Log artifacts
    mlflow.log_artifact("model.pkl")
    mlflow.log_artifacts("./outputs")

    # Log tags
    mlflow.set_tag("model_type", "neural_network")
```

### Auto-Logging
```python
import mlflow

# Scikit-learn
mlflow.sklearn.autolog()
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# PyTorch
mlflow.pytorch.autolog()

# TensorFlow/Keras
mlflow.tensorflow.autolog()

# XGBoost
mlflow.xgboost.autolog()

# LightGBM
mlflow.lightgbm.autolog()
```

### Manual Run Management
```python
# Create run manually
run = mlflow.start_run(run_name="my-run")
try:
    mlflow.log_param("param1", "value1")
    mlflow.log_metric("metric1", 0.9)
finally:
    mlflow.end_run()

# Get run info
run_id = run.info.run_id
print(f"Run ID: {run_id}")

# Resume run
with mlflow.start_run(run_id=run_id):
    mlflow.log_metric("additional_metric", 0.95)
```

### Nested Runs
```python
with mlflow.start_run(run_name="parent"):
    mlflow.log_param("parent_param", "value")

    for i in range(3):
        with mlflow.start_run(run_name=f"child_{i}", nested=True):
            mlflow.log_param("child_param", i)
            mlflow.log_metric("child_metric", i * 0.1)
```

---

## 3. Tracking Server

### Start Server
```bash
# Local file store
mlflow server --host 0.0.0.0 --port 5000

# With database backend
mlflow server \
    --backend-store-uri postgresql://user:pass@localhost/mlflow \
    --default-artifact-root s3://mlflow-artifacts/ \
    --host 0.0.0.0 \
    --port 5000

# With SQLite
mlflow server \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns \
    --host 0.0.0.0
```

### Connect to Server
```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

# Or via environment
# export MLFLOW_TRACKING_URI=http://localhost:5000
```

### Docker Compose
```yaml
services:
  mlflow:
    image: ghcr.io/mlflow/mlflow:latest
    ports:
      - "5000:5000"
    environment:
      - MLFLOW_BACKEND_STORE_URI=postgresql://mlflow:mlflow@postgres/mlflow
      - MLFLOW_DEFAULT_ARTIFACT_ROOT=s3://mlflow-artifacts/
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
    command: >
      mlflow server
      --host 0.0.0.0
      --port 5000
    depends_on:
      - postgres

  postgres:
    image: postgres:15
    environment:
      - POSTGRES_USER=mlflow
      - POSTGRES_PASSWORD=mlflow
      - POSTGRES_DB=mlflow
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## 4. Model Logging

### Log Scikit-learn Model
```python
from sklearn.ensemble import RandomForestClassifier
import mlflow.sklearn

model = RandomForestClassifier()
model.fit(X_train, y_train)

with mlflow.start_run():
    # Log model
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="my-rf-model"
    )

    # With signature
    from mlflow.models import infer_signature
    signature = infer_signature(X_train, model.predict(X_train))
    mlflow.sklearn.log_model(model, "model", signature=signature)
```

### Log PyTorch Model
```python
import mlflow.pytorch

with mlflow.start_run():
    mlflow.pytorch.log_model(
        pytorch_model=model,
        artifact_path="model",
        conda_env="conda.yaml",
        code_paths=["./src"]
    )
```

### Log Custom Model (PyFunc)
```python
import mlflow.pyfunc

class MyModel(mlflow.pyfunc.PythonModel):
    def load_context(self, context):
        # Load any artifacts
        import pickle
        with open(context.artifacts["model_path"], "rb") as f:
            self.model = pickle.load(f)

    def predict(self, context, model_input):
        return self.model.predict(model_input)

# Log custom model
with mlflow.start_run():
    mlflow.pyfunc.log_model(
        artifact_path="model",
        python_model=MyModel(),
        artifacts={"model_path": "model.pkl"},
        conda_env={
            "dependencies": ["scikit-learn==1.0.0", "pandas"]
        }
    )
```

### Load Model
```python
# From run
model = mlflow.sklearn.load_model(f"runs:/{run_id}/model")

# From registry
model = mlflow.sklearn.load_model("models:/my-model/1")
model = mlflow.sklearn.load_model("models:/my-model/Production")

# As PyFunc
model = mlflow.pyfunc.load_model(f"runs:/{run_id}/model")
predictions = model.predict(X_test)
```

---

## 5. Model Registry

### Register Model
```python
# During logging
mlflow.sklearn.log_model(
    model,
    "model",
    registered_model_name="my-model"
)

# After logging
result = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="my-model"
)
```

### Manage Versions
```python
from mlflow import MlflowClient

client = MlflowClient()

# Get model versions
versions = client.search_model_versions("name='my-model'")

# Transition stage
client.transition_model_version_stage(
    name="my-model",
    version=1,
    stage="Production"  # None, Staging, Production, Archived
)

# Add description
client.update_model_version(
    name="my-model",
    version=1,
    description="Production model v1"
)

# Add tags
client.set_model_version_tag(
    name="my-model",
    version=1,
    key="validation_status",
    value="approved"
)
```

### Model Aliases
```python
# Set alias (MLflow 2.0+)
client.set_registered_model_alias(
    name="my-model",
    alias="champion",
    version=1
)

# Load by alias
model = mlflow.pyfunc.load_model("models:/my-model@champion")

# Delete alias
client.delete_registered_model_alias(
    name="my-model",
    alias="champion"
)
```

---

## 6. Model Serving

### Local Serving
```bash
# Serve from run
mlflow models serve -m runs:/<run_id>/model -p 5001

# Serve from registry
mlflow models serve -m models:/my-model/Production -p 5001

# With environment
mlflow models serve -m models:/my-model/1 -p 5001 --env-manager=conda
```

### Make Predictions
```bash
curl -X POST http://localhost:5001/invocations \
  -H "Content-Type: application/json" \
  -d '{"dataframe_split": {"columns": ["a", "b"], "data": [[1, 2]]}}'
```

### Docker Deployment
```bash
# Build Docker image
mlflow models build-docker -m models:/my-model/1 -n my-model-image

# Run container
docker run -p 5001:8080 my-model-image
```

---

## 7. MLflow Projects

### MLproject File
```yaml
# MLproject
name: my-project

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      learning_rate: {type: float, default: 0.01}
      epochs: {type: int, default: 100}
    command: "python train.py --lr {learning_rate} --epochs {epochs}"

  validate:
    parameters:
      model_path: {type: string}
    command: "python validate.py --model {model_path}"
```

### Run Project
```bash
# Local
mlflow run . -P learning_rate=0.001 -P epochs=50

# From Git
mlflow run https://github.com/user/repo -P param=value

# Specific entry point
mlflow run . -e validate -P model_path=./model

# With environment
mlflow run . --env-manager=conda
```

---

## 8. GenAI Tracking

### Track LLM Calls
```python
import mlflow

mlflow.set_experiment("llm-experiment")

with mlflow.start_run():
    # Log LLM params
    mlflow.log_params({
        "model": "gpt-4",
        "temperature": 0.7,
        "max_tokens": 1000
    })

    # Make LLM call
    response = openai_client.chat.completions.create(...)

    # Log input/output
    mlflow.log_text(prompt, "input.txt")
    mlflow.log_text(response.choices[0].message.content, "output.txt")

    # Log usage
    mlflow.log_metrics({
        "prompt_tokens": response.usage.prompt_tokens,
        "completion_tokens": response.usage.completion_tokens
    })
```

### Auto-log LangChain
```python
import mlflow

mlflow.langchain.autolog()

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o")
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm

# Automatically logged
result = chain.invoke({"topic": "MLflow"})
```

---

## 9. Querying Runs

### Search Runs
```python
from mlflow import MlflowClient

client = MlflowClient()

# Search runs
runs = client.search_runs(
    experiment_ids=["1"],
    filter_string="metrics.accuracy > 0.9 AND params.model_type = 'rf'",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

for run in runs:
    print(f"Run: {run.info.run_id}")
    print(f"  Accuracy: {run.data.metrics.get('accuracy')}")
    print(f"  Params: {run.data.params}")

# Get best run
best_run = runs[0]
```

### Compare Runs
```python
import mlflow

# Get runs
runs = mlflow.search_runs(
    experiment_names=["my-experiment"],
    filter_string="status = 'FINISHED'"
)

# Compare as DataFrame
print(runs[["run_id", "params.learning_rate", "metrics.accuracy"]])

# Get artifacts
client = MlflowClient()
artifacts = client.list_artifacts(run_id)
```

---

## Best Practices

1. **Always set experiment** - Organize runs
2. **Log signatures** - Model input/output schemas
3. **Use auto-logging** - Reduce boilerplate
4. **Version models** - Track production models
5. **Use artifacts** - Store plots, configs
6. **Tag runs** - Searchable metadata
7. **Nested runs** - Hyperparameter tuning
8. **Remote tracking** - Collaborate with team
9. **CI/CD integration** - Automated training
10. **Monitor serving** - Track predictions
