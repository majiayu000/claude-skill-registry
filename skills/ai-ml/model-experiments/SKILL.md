---
name: ML Experiment Tracking
description: Managing ML experiments, metrics, parameters, and artifacts using MLflow, Weights & Biases, and best practices for reproducible ML experiments and model versioning.
---

# ML Experiment Tracking

> **Current Level:** Advanced  
> **Domain:** Data Science / ML / Experimentation

---

## Overview

Experiment tracking manages ML experiments, metrics, parameters, and artifacts. This guide covers MLflow, Weights & Biases, and best practices for tracking experiments, comparing models, and ensuring reproducibility in ML development.

## Experiment Tracking Importance

**Benefits:**
- Reproducibility
- Comparison of experiments
- Collaboration
- Model versioning
- Hyperparameter optimization

## MLflow

### Installation

```bash
pip install mlflow
mlflow ui  # Start UI on http://localhost:5000
```

### Tracking

```python
# MLflow tracking
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score

# Set experiment
mlflow.set_experiment("my-experiment")

# Start run
with mlflow.start_run(run_name="random-forest-v1"):
    # Log parameters
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 10)
    mlflow.log_param("random_state", 42)
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Log metrics
    mlflow.log_metric("accuracy", accuracy_score(y_test, y_pred))
    mlflow.log_metric("f1_score", f1_score(y_test, y_pred, average='weighted'))
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log artifacts
    import matplotlib.pyplot as plt
    
    plt.figure()
    plt.plot(model.feature_importances_)
    plt.savefig("feature_importance.png")
    mlflow.log_artifact("feature_importance.png")
    
    print(f"Run ID: {mlflow.active_run().info.run_id}")
```

### Autologging

```python
# Automatic logging
import mlflow.sklearn

mlflow.sklearn.autolog()

# Train model (automatically logged)
model = RandomForestClassifier()
model.fit(X_train, y_train)
```

### Model Registry

```python
# Register model
import mlflow

# Log and register model
with mlflow.start_run():
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="my-model"
    )

# Load registered model
model_uri = "models:/my-model/1"  # Version 1
loaded_model = mlflow.sklearn.load_model(model_uri)

# Transition model stage
from mlflow.tracking import MlflowClient

client = MlflowClient()
client.transition_model_version_stage(
    name="my-model",
    version=1,
    stage="Production"
)

# Load production model
model_uri = "models:/my-model/Production"
production_model = mlflow.sklearn.load_model(model_uri)
```

### Projects

```python
# MLproject file
name: my-ml-project

conda_env: conda.yaml

entry_points:
  main:
    parameters:
      n_estimators: {type: int, default: 100}
      max_depth: {type: int, default: 10}
    command: "python train.py --n_estimators {n_estimators} --max_depth {max_depth}"

# Run project
# mlflow run . -P n_estimators=200 -P max_depth=15
```

## Weights & Biases

```python
# Weights & Biases tracking
import wandb
from sklearn.ensemble import RandomForestClassifier

# Initialize run
wandb.init(
    project="my-project",
    name="random-forest-v1",
    config={
        "n_estimators": 100,
        "max_depth": 10,
        "learning_rate": 0.01
    }
)

# Train model
model = RandomForestClassifier(
    n_estimators=wandb.config.n_estimators,
    max_depth=wandb.config.max_depth
)
model.fit(X_train, y_train)

# Log metrics
y_pred = model.predict(X_test)
wandb.log({
    "accuracy": accuracy_score(y_test, y_pred),
    "f1_score": f1_score(y_test, y_pred, average='weighted')
})

# Log confusion matrix
wandb.sklearn.plot_confusion_matrix(y_test, y_pred, labels=class_names)

# Log feature importance
wandb.sklearn.plot_feature_importances(model, feature_names)

# Save model
wandb.save('model.pkl')

# Finish run
wandb.finish()
```

### Hyperparameter Sweeps

```python
# W&B sweep configuration
sweep_config = {
    'method': 'bayes',  # or 'grid', 'random'
    'metric': {
        'name': 'accuracy',
        'goal': 'maximize'
    },
    'parameters': {
        'n_estimators': {
            'values': [50, 100, 200]
        },
        'max_depth': {
            'min': 5,
            'max': 20
        },
        'learning_rate': {
            'distribution': 'log_uniform',
            'min': -5,
            'max': 0
        }
    }
}

# Initialize sweep
sweep_id = wandb.sweep(sweep_config, project="my-project")

# Training function
def train():
    wandb.init()
    
    # Get hyperparameters
    config = wandb.config
    
    # Train model
    model = RandomForestClassifier(
        n_estimators=config.n_estimators,
        max_depth=config.max_depth
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    wandb.log({"accuracy": accuracy})

# Run sweep
wandb.agent(sweep_id, train, count=10)
```

## TensorBoard

```python
# TensorBoard logging
from torch.utils.tensorboard import SummaryWriter
import torch
import torch.nn as nn

# Create writer
writer = SummaryWriter('runs/experiment_1')

# Log scalars
for epoch in range(100):
    loss = train_epoch(model, train_loader)
    accuracy = evaluate(model, test_loader)
    
    writer.add_scalar('Loss/train', loss, epoch)
    writer.add_scalar('Accuracy/test', accuracy, epoch)

# Log model graph
writer.add_graph(model, input_tensor)

# Log images
writer.add_image('predictions', img_grid, epoch)

# Log histograms
for name, param in model.named_parameters():
    writer.add_histogram(name, param, epoch)

# Close writer
writer.close()

# View in TensorBoard
# tensorboard --logdir=runs
```

## Metrics Logging

```python
# Comprehensive metrics logging
class MetricsLogger:
    def __init__(self, experiment_name: str):
        self.experiment_name = experiment_name
        mlflow.set_experiment(experiment_name)
    
    def log_classification_metrics(self, y_true, y_pred, y_prob=None):
        """Log classification metrics"""
        from sklearn.metrics import (
            accuracy_score,
            precision_score,
            recall_score,
            f1_score,
            roc_auc_score,
            confusion_matrix
        )
        
        metrics = {
            "accuracy": accuracy_score(y_true, y_pred),
            "precision": precision_score(y_true, y_pred, average='weighted'),
            "recall": recall_score(y_true, y_pred, average='weighted'),
            "f1_score": f1_score(y_true, y_pred, average='weighted')
        }
        
        if y_prob is not None:
            metrics["roc_auc"] = roc_auc_score(y_true, y_prob, multi_class='ovr')
        
        for name, value in metrics.items():
            mlflow.log_metric(name, value)
        
        # Log confusion matrix
        cm = confusion_matrix(y_true, y_pred)
        self.plot_confusion_matrix(cm)
    
    def log_regression_metrics(self, y_true, y_pred):
        """Log regression metrics"""
        from sklearn.metrics import (
            mean_squared_error,
            mean_absolute_error,
            r2_score
        )
        
        metrics = {
            "mse": mean_squared_error(y_true, y_pred),
            "rmse": mean_squared_error(y_true, y_pred, squared=False),
            "mae": mean_absolute_error(y_true, y_pred),
            "r2": r2_score(y_true, y_pred)
        }
        
        for name, value in metrics.items():
            mlflow.log_metric(name, value)
    
    def plot_confusion_matrix(self, cm):
        """Plot and log confusion matrix"""
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        plt.figure(figsize=(8, 6))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.savefig('confusion_matrix.png')
        mlflow.log_artifact('confusion_matrix.png')
        plt.close()
```

## Hyperparameter Tracking

```python
# Track hyperparameters with Optuna + MLflow
import optuna
import mlflow

def objective(trial):
    """Optuna objective function"""
    with mlflow.start_run(nested=True):
        # Suggest hyperparameters
        params = {
            'n_estimators': trial.suggest_int('n_estimators', 50, 200),
            'max_depth': trial.suggest_int('max_depth', 5, 20),
            'learning_rate': trial.suggest_loguniform('learning_rate', 1e-5, 1e-1)
        }
        
        # Log parameters
        mlflow.log_params(params)
        
        # Train model
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        
        # Evaluate
        accuracy = model.score(X_test, y_test)
        
        # Log metric
        mlflow.log_metric("accuracy", accuracy)
        
        return accuracy

# Run optimization
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Best parameters
print(f"Best params: {study.best_params}")
print(f"Best value: {study.best_value}")
```

## Artifact Storage

```python
# Store various artifacts
with mlflow.start_run():
    # Log model
    mlflow.sklearn.log_model(model, "model")
    
    # Log dataset
    mlflow.log_artifact("data/train.csv", "datasets")
    
    # Log plots
    mlflow.log_artifact("plots/feature_importance.png", "plots")
    
    # Log configuration
    import json
    with open("config.json", "w") as f:
        json.dump(config, f)
    mlflow.log_artifact("config.json")
    
    # Log dictionary as JSON
    mlflow.log_dict({"key": "value"}, "metadata.json")
    
    # Log text
    mlflow.log_text("Model description", "description.txt")
```

## Experiment Comparison

```python
# Compare experiments
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get experiment
experiment = client.get_experiment_by_name("my-experiment")

# Get all runs
runs = client.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"],
    max_results=10
)

# Compare runs
import pandas as pd

comparison = []
for run in runs:
    comparison.append({
        'run_id': run.info.run_id,
        'accuracy': run.data.metrics.get('accuracy'),
        'f1_score': run.data.metrics.get('f1_score'),
        'n_estimators': run.data.params.get('n_estimators'),
        'max_depth': run.data.params.get('max_depth')
    })

df = pd.DataFrame(comparison)
print(df)
```

## Reproducibility

```python
# Ensure reproducibility
import random
import numpy as np
import torch

def set_seed(seed=42):
    """Set random seeds for reproducibility"""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Log environment
with mlflow.start_run():
    # Log seed
    mlflow.log_param("random_seed", 42)
    
    # Log Python version
    import sys
    mlflow.log_param("python_version", sys.version)
    
    # Log package versions
    import pkg_resources
    packages = [str(d) for d in pkg_resources.working_set]
    mlflow.log_text("\n".join(packages), "requirements.txt")
    
    # Log git commit
    import subprocess
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    mlflow.log_param("git_commit", commit)
```

## Best Practices

1. **Track Everything** - Log params, metrics, artifacts
2. **Naming** - Use descriptive experiment names
3. **Versioning** - Version datasets and models
4. **Reproducibility** - Set seeds and log environment
5. **Comparison** - Compare experiments systematically
6. **Cleanup** - Archive old experiments
7. **Documentation** - Document experiment goals
8. **Collaboration** - Share experiments with team
9. **Automation** - Automate logging
10. **Storage** - Manage artifact storage

---

## Quick Start

### MLflow Tracking

```python
import mlflow

mlflow.set_experiment("my-experiment")

with mlflow.start_run():
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("epochs", 100)
    
    # Train model
    model = train_model(X_train, y_train)
    
    # Log metrics
    accuracy = evaluate_model(model, X_test, y_test)
    mlflow.log_metric("accuracy", accuracy)
    
    # Log model
    mlflow.sklearn.log_model(model, "model")
```

---

## Production Checklist

- [ ] **Experiment Tracking**: Set up experiment tracking
- [ ] **Parameter Logging**: Log all hyperparameters
- [ ] **Metric Logging**: Log all metrics
- [ ] **Artifact Storage**: Store model artifacts
- [ ] **Reproducibility**: Ensure reproducibility
- [ ] **Comparison**: Compare experiments
- [ ] **Cleanup**: Archive old experiments
- [ ] **Documentation**: Document experiment goals
- [ ] **Collaboration**: Share experiments
- [ ] **Automation**: Automate logging
- [ ] **Storage**: Manage artifact storage
- [ ] **Versioning**: Model versioning

---

## Anti-patterns

### ❌ Don't: No Tracking

```python
# ❌ Bad - No tracking
model = train_model(X, y)
# No record of what was done!
```

```python
# ✅ Good - Track everything
with mlflow.start_run():
    mlflow.log_params(params)
    model = train_model(X, y)
    mlflow.log_metrics(metrics)
    mlflow.log_model(model)
```

### ❌ Don't: Inconsistent Logging

```python
# ❌ Bad - Inconsistent
run1: log_metric("acc", 0.95)
run2: log_metric("accuracy", 0.96)
# Different metric names!
```

```python
# ✅ Good - Consistent
run1: log_metric("accuracy", 0.95)
run2: log_metric("accuracy", 0.96)
# Same metric names
```

---

## Integration Points

- **Model Training** (`05-ai-ml-core/model-training/`) - Training process
- **Feature Engineering** (`39-data-science-ml/feature-engineering/`) - Features
- **ML Serving** (`39-data-science-ml/ml-serving/`) - Model deployment

---

## Further Reading

- [MLflow](https://mlflow.org/)
- [Weights & Biases](https://wandb.ai/)
- [Experiment Tracking Best Practices](https://mlflow.org/docs/latest/tracking.html)

## Resources
- [Weights & Biases](https://wandb.ai/)
- [TensorBoard](https://www.tensorflow.org/tensorboard)
- [Neptune.ai](https://neptune.ai/)
- [Comet.ml](https://www.comet.ml/)
