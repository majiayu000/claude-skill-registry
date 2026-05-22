---
name: ml-experiment-tracker
description: Guides ML experiment logging, versioning, and reproducibility using tools like MLflow, Weights & Biases, and DVC for systematic model development.
license: MIT
---

# ML Experiment Tracker

This skill provides guidance for systematic machine learning experimentation with proper tracking, versioning, and reproducibility practices.

## Core Competencies

- **Experiment Tracking**: MLflow, Weights & Biases (wandb), Neptune, Comet
- **Data Versioning**: DVC, Delta Lake, LakeFS
- **Model Registry**: Version control for trained models
- **Reproducibility**: Environment, code, data, and hyperparameter tracking

## Experiment Tracking Fundamentals

### What to Track

Every experiment should log:

| Category | Items | Why |
|----------|-------|-----|
| Code | Git commit hash, branch, diff | Reproduce exact code state |
| Data | Dataset version, hash, lineage | Know which data was used |
| Environment | Python version, dependencies, hardware | Reproduce runtime |
| Hyperparameters | All config values | Understand what changed |
| Metrics | Loss, accuracy, custom metrics | Compare performance |
| Artifacts | Models, plots, predictions | Preserve outputs |

### Experiment Organization

```
project/
├── experiments/
│   ├── baseline/           # Initial experiments
│   ├── feature-engineering/ # Data improvements
│   ├── architecture/       # Model changes
│   └── hyperparameter/     # Tuning runs
├── data/
│   ├── raw/               # Original data (versioned)
│   ├── processed/         # Cleaned data
│   └── features/          # Feature store
└── models/
    ├── staging/           # Candidates
    └── production/        # Deployed models
```

## MLflow Patterns

### Basic Experiment Logging

```python
import mlflow

# Set experiment (creates if not exists)
mlflow.set_experiment("my-classification-project")

with mlflow.start_run(run_name="baseline-v1"):
    # Log parameters
    mlflow.log_param("learning_rate", 0.01)
    mlflow.log_param("batch_size", 32)
    mlflow.log_param("epochs", 100)

    # Training loop
    for epoch in range(epochs):
        train_loss = train_epoch(model, train_loader)
        val_loss, val_acc = evaluate(model, val_loader)

        # Log metrics with step
        mlflow.log_metrics({
            "train_loss": train_loss,
            "val_loss": val_loss,
            "val_accuracy": val_acc
        }, step=epoch)

    # Log model
    mlflow.pytorch.log_model(model, "model")

    # Log artifacts (plots, configs)
    mlflow.log_artifact("confusion_matrix.png")
    mlflow.log_artifact("config.yaml")
```

### Model Registry Workflow

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Training   │───▶│   Staging    │───▶│  Production  │
│    Runs      │    │   Review     │    │   Deployed   │
└──────────────┘    └──────────────┘    └──────────────┘
      │                    │                    │
      ▼                    ▼                    ▼
   Candidate           Validated           Monitored
   Models              Models              Models
```

Stages:
- **None**: Just logged, not registered
- **Staging**: Candidate for production
- **Production**: Active serving
- **Archived**: Historical reference

## Weights & Biases Patterns

### Project Structure

```python
import wandb

# Initialize with config
config = {
    "learning_rate": 0.01,
    "architecture": "ResNet50",
    "dataset": "imagenet-subset",
    "epochs": 100
}

run = wandb.init(
    project="image-classification",
    group="architecture-experiments",  # Group related runs
    tags=["baseline", "resnet"],
    config=config,
    notes="Testing ResNet50 baseline on subset"
)

# Training with automatic logging
for epoch in range(config["epochs"]):
    metrics = train_and_eval(model, train_loader, val_loader)
    wandb.log(metrics)

    # Log media
    wandb.log({"predictions": wandb.Image(pred_grid)})
    wandb.log({"confusion_matrix": wandb.plot.confusion_matrix(...)})

wandb.finish()
```

### Hyperparameter Sweeps

```yaml
# sweep_config.yaml
program: train.py
method: bayes  # or grid, random
metric:
  name: val_accuracy
  goal: maximize
parameters:
  learning_rate:
    distribution: log_uniform_values
    min: 0.0001
    max: 0.1
  batch_size:
    values: [16, 32, 64, 128]
  optimizer:
    values: ["adam", "sgd", "adamw"]
early_terminate:
  type: hyperband
  min_iter: 10
```

## DVC for Data Versioning

### Setup and Usage

```bash
# Initialize DVC in git repo
dvc init

# Track large files
dvc add data/training.csv
git add data/training.csv.dvc data/.gitignore
git commit -m "Add training data v1"

# Push to remote storage
dvc remote add -d storage s3://bucket/dvc
dvc push

# Create pipeline
dvc run -n preprocess \
    -d src/preprocess.py -d data/raw \
    -o data/processed \
    python src/preprocess.py

# Reproduce pipeline
dvc repro
```

### DVC Pipeline Definition

```yaml
# dvc.yaml
stages:
  preprocess:
    cmd: python src/preprocess.py
    deps:
      - src/preprocess.py
      - data/raw/
    outs:
      - data/processed/

  train:
    cmd: python src/train.py
    deps:
      - src/train.py
      - data/processed/
    params:
      - train.epochs
      - train.learning_rate
    outs:
      - models/model.pkl
    metrics:
      - metrics.json:
          cache: false
```

## Reproducibility Checklist

### Code Reproducibility
- [ ] Pin git commit for each experiment
- [ ] Track uncommitted changes (git diff)
- [ ] Version control notebooks (nbstripout)
- [ ] Document manual steps

### Environment Reproducibility
- [ ] Lock dependencies (pip freeze, poetry.lock)
- [ ] Specify Python version
- [ ] Document CUDA/GPU requirements
- [ ] Use containers for full isolation

### Data Reproducibility
- [ ] Version datasets with DVC or similar
- [ ] Document data collection process
- [ ] Track preprocessing steps
- [ ] Save train/val/test split indices

### Training Reproducibility
- [ ] Set random seeds (Python, NumPy, PyTorch/TF)
- [ ] Log all hyperparameters
- [ ] Save model checkpoints
- [ ] Document non-deterministic operations

## Best Practices

### Naming Conventions

```
experiment: {project}-{objective}
run: {date}-{description}-{variant}
model: {architecture}-{dataset}-{version}

Examples:
experiment: fraud-detection-baseline
run: 2024-01-15-xgboost-tuning-lr001
model: xgboost-transactions-v2.3.1
```

### Comparison Dashboards

Track these metrics for model comparison:
- Primary metric (what you optimize)
- Secondary metrics (constraints)
- Resource usage (training time, memory)
- Inference performance (latency, throughput)

### Experiment Documentation

Each significant experiment should document:
1. **Hypothesis**: What change and expected outcome
2. **Method**: What was actually done
3. **Results**: Metrics and observations
4. **Conclusions**: What was learned, next steps

## References

- `references/mlflow-setup.md` - MLflow installation and configuration
- `references/wandb-patterns.md` - Advanced W&B features and sweeps
- `references/reproducibility-checklist.md` - Detailed reproducibility guide
