---
name: experiment-tracker
description: |
  Manages ML experiment tracking with MLflow, Weights & Biases, or SpecWeave's built-in tracking. Activates for "track experiments", "MLflow", "wandb", "experiment logging", "compare experiments", "hyperparameter tracking". Automatically configures tracking tools to log to SpecWeave increment folders, ensuring all experiments are documented and reproducible. Integrates with SpecWeave's living docs for persistent experiment knowledge.
---

# Experiment Tracker

## Overview

Transforms chaotic ML experimentation into organized, reproducible research. Every experiment is logged, versioned, and tied to a SpecWeave increment, ensuring team knowledge is preserved and experiments are reproducible.

## Problem This Solves

**Without structured tracking**:
- ❌ "Which hyperparameters did we use for model v2?"
- ❌ "Why did we choose XGBoost over LightGBM?"
- ❌ "Can't reproduce results from 3 months ago"
- ❌ "Team member left, all knowledge in their notebooks"

**With experiment tracking**:
- ✅ All experiments logged with params, metrics, artifacts
- ✅ Decisions documented ("XGBoost: 5% better precision, chose it")
- ✅ Reproducible (environment, data version, code hash)
- ✅ Team knowledge in living docs, not individual notebooks

## How It Works

### Auto-Configuration

When you create an ML increment, the skill detects tracking tools:

```python
# No configuration needed - automatically detects and configures
from specweave import track_experiment

# Automatically logs to:
# .specweave/increments/0042.../experiments/exp-001/
with track_experiment("baseline-model") as exp:
    model.fit(X_train, y_train)
    exp.log_metric("accuracy", accuracy)
```

### Tracking Backends

**Option 1: SpecWeave Built-in** (default, zero-config)
```python
from specweave import track_experiment

# Logs to increment folder automatically
with track_experiment("xgboost-v1") as exp:
    exp.log_param("n_estimators", 100)
    exp.log_metric("auc", 0.87)
    exp.save_model(model, "model.pkl")

# Creates:
# .specweave/increments/0042.../experiments/xgboost-v1/
# ├── params.json
# ├── metrics.json
# ├── model.pkl
# └── metadata.yaml
```

**Option 2: MLflow** (if detected in project)
```python
import mlflow
from specweave import configure_mlflow

# Auto-configures MLflow to log to increment
configure_mlflow(increment="0042")

with mlflow.start_run(run_name="xgboost-v1"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_metric("auc", 0.87)
    mlflow.sklearn.log_model(model, "model")

# Still logs to increment folder, just uses MLflow as backend
```

**Option 3: Weights & Biases**
```python
import wandb
from specweave import configure_wandb

# Auto-configures W&B project = increment ID
configure_wandb(increment="0042")

run = wandb.init(name="xgboost-v1")
run.log({"auc": 0.87})
run.log_model("model.pkl")

# W&B dashboard + local logs in increment folder
```

### Experiment Comparison

```python
from specweave import compare_experiments

# Compare all experiments in increment
comparison = compare_experiments(increment="0042")

# Generates:
# .specweave/increments/0042.../experiments/comparison.md
```

**Output**:
```markdown
| Experiment         | Accuracy | Precision | Recall | F1   | Training Time |
|--------------------|----------|-----------|--------|------|---------------|
| exp-001-baseline   | 0.65     | 0.60      | 0.55   | 0.57 | 2s            |
| exp-002-xgboost    | 0.87     | 0.85      | 0.83   | 0.84 | 45s           |
| exp-003-lightgbm   | 0.86     | 0.84      | 0.82   | 0.83 | 32s           |
| exp-004-neural-net | 0.85     | 0.83      | 0.81   | 0.82 | 320s          |

**Best Model**: exp-002-xgboost
- Highest accuracy (0.87)
- Good precision/recall balance
- Reasonable training time (45s)
- Selected for deployment
```

### Living Docs Integration

After completing increment:

```bash
/sw:sync-docs update
```

Automatically updates:

```markdown
<!-- .specweave/docs/internal/architecture/ml-experiments.md -->

## Recommendation Model (Increment 0042)

### Experiments Conducted: 7
- exp-001-baseline: Random classifier (acc=0.12)
- exp-002-popularity: Popularity baseline (acc=0.18)
- exp-003-xgboost: XGBoost classifier (acc=0.26) ✅ **SELECTED**
- ...

### Selection Rationale
XGBoost chosen for:
- Best accuracy (0.26 vs baseline 0.18, +44% improvement)
- Fast inference (<50ms)
- Good explainability (SHAP values)
- Stable across cross-validation (std=0.02)

### Hyperparameters (exp-003)
- n_estimators: 200
- max_depth: 6
- learning_rate: 0.1
- subsample: 0.8
```

## When to Use This Skill

Activate when you need to:

- **Track ML experiments** systematically
- **Compare multiple models** objectively
- **Document experiment decisions** for team
- **Reproduce past results** exactly
- **Maintain experiment history** across increments

## Key Features

### 1. Automatic Logging

```python
# Logs everything automatically
from specweave import AutoTracker

tracker = AutoTracker(increment="0042")

# Just wrap your training code
@tracker.track(name="xgboost-auto")
def train_model():
    model = XGBClassifier(**params)
    model.fit(X_train, y_train)
    score = model.score(X_test, y_test)
    return model, score

# Automatically logs: params, metrics, model, environment, git hash
model, score = train_model()
```

### 2. Hyperparameter Tracking

```python
from specweave import track_hyperparameters

params_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [3, 6, 9],
    "learning_rate": [0.01, 0.1, 0.3]
}

# Tracks all parameter combinations
results = track_hyperparameters(
    model=XGBClassifier,
    param_grid=params_grid,
    X_train=X_train,
    y_train=y_train,
    increment="0042"
)

# Generates parameter importance analysis
```

### 3. Cross-Validation Tracking

```python
from specweave import track_cross_validation

# Tracks each fold separately
cv_results = track_cross_validation(
    model=model,
    X=X,
    y=y,
    cv=5,
    increment="0042"
)

# Logs: mean, std, per-fold scores, fold distribution
```

### 4. Artifact Management

```python
from specweave import track_artifacts

with track_experiment("xgboost-v1") as exp:
    # Training artifacts
    exp.save_artifact("preprocessor.pkl", preprocessor)
    exp.save_artifact("model.pkl", model)
    
    # Evaluation artifacts
    exp.save_artifact("confusion_matrix.png", cm_plot)
    exp.save_artifact("roc_curve.png", roc_plot)
    
    # Data artifacts
    exp.save_artifact("feature_importance.csv", importance_df)
    
    # Environment artifacts
    exp.save_artifact("requirements.txt", requirements)
    exp.save_artifact("conda_env.yaml", conda_env)
```

### 5. Experiment Metadata

```python
from specweave import ExperimentMetadata

metadata = ExperimentMetadata(
    name="xgboost-v3",
    description="XGBoost with feature engineering v2",
    tags=["production-candidate", "feature-eng-v2"],
    git_commit="a3b8c9d",
    data_version="v2024-01",
    author="[email protected]"
)

with track_experiment(metadata) as exp:
    # ... training ...
    pass
```

## Best Practices

### 1. Name Experiments Clearly

```python
# ❌ Bad: Generic names
with track_experiment("exp1"):
    ...

# ✅ Good: Descriptive names
with track_experiment("xgboost-tuned-depth6-lr0.1"):
    ...
```

### 2. Log Everything

```python
# Log more than you think you need
exp.log_param("random_seed", 42)
exp.log_param("data_version", "2024-01")
exp.log_param("python_version", sys.version)
exp.log_param("sklearn_version", sklearn.__version__)

# Future you will thank present you
```

### 3. Document Failures

```python
try:
    with track_experiment("neural-net-attempt") as exp:
        model.fit(X_train, y_train)
except Exception as e:
    exp.log_note(f"FAILED: {str(e)}")
    exp.log_note("Reason: Out of memory, need smaller batch size")
    exp.set_status("failed")
    
# Failure documentation prevents repeating mistakes
```

### 4. Use Experiment Series

```python
# Related experiments in series
experiments = [
    "xgboost-baseline",
    "xgboost-tuned-v1",
    "xgboost-tuned-v2",
    "xgboost-tuned-v3-final"
]

# Track progression and improvements
```

### 5. Link to Data Versions

```python
with track_experiment("xgboost-v1") as exp:
    exp.log_param("data_commit", "dvc:a3b8c9d")
    exp.log_param("data_url", "s3://bucket/data/v2024-01")
    
# Enables exact reproduction
```

## Integration with SpecWeave

### With Increments

```bash
# Experiments automatically tied to increment
/sw:inc "0042-recommendation-model"
# All experiments logged to: .specweave/increments/0042.../experiments/
```

### With Living Docs

```bash
# Sync experiment findings to docs
/sw:sync-docs update
# Updates: architecture/ml-models.md, runbooks/model-training.md
```

### With GitHub

```bash
# Create issue for model retraining
/sw:github:create-issue "Retrain model with Q1 2024 data"
# Links to previous experiments in increment
```

## Examples

### Example 1: Baseline Experiments

```python
from specweave import track_experiment

baselines = ["random", "majority", "stratified"]

for strategy in baselines:
    with track_experiment(f"baseline-{strategy}") as exp:
        model = DummyClassifier(strategy=strategy)
        model.fit(X_train, y_train)
        
        accuracy = model.score(X_test, y_test)
        exp.log_metric("accuracy", accuracy)
        exp.log_note(f"Baseline: {strategy}")

# Generates baseline comparison report
```

### Example 2: Hyperparameter Grid Search

```python
from sklearn.model_selection import GridSearchCV
from specweave import track_grid_search

param_grid = {
    "n_estimators": [100, 200, 500],
    "max_depth": [3, 6, 9]
}

# Automatically logs all combinations
best_model, results = track_grid_search(
    XGBClassifier(),
    param_grid,
    X_train,
    y_train,
    increment="0042"
)

# Creates visualization of parameter importance
```

### Example 3: Model Comparison

```python
from specweave import compare_models

models = {
    "xgboost": XGBClassifier(),
    "lightgbm": LGBMClassifier(),
    "random-forest": RandomForestClassifier()
}

# Trains and compares all models
comparison = compare_models(
    models,
    X_train,
    y_train,
    X_test,
    y_test,
    increment="0042"
)

# Generates markdown comparison table
```

## Tool Compatibility

### MLflow

```python
# Option 1: Pure MLflow (auto-configured)
import mlflow
mlflow.set_tracking_uri(".specweave/increments/0042.../experiments")

# Option 2: SpecWeave wrapper (recommended)
from specweave import mlflow as sw_mlflow
with sw_mlflow.start_run("xgboost"):
    # Logs to both MLflow and increment docs
    pass
```

### Weights & Biases

```python
# Option 1: Pure wandb
import wandb
wandb.init(project="0042-recommendation-model")

# Option 2: SpecWeave wrapper (recommended)
from specweave import wandb as sw_wandb
run = sw_wandb.init(increment="0042", name="xgboost")
# Syncs to increment folder + W&B dashboard
```

### TensorBoard

```python
from specweave import TensorBoardCallback

# Keras callback
model.fit(
    X_train,
    y_train,
    callbacks=[
        TensorBoardCallback(
            increment="0042",
            log_dir=".specweave/increments/0042.../tensorboard"
        )
    ]
)
```

## Commands

```bash
# List all experiments in increment
/ml:list-experiments 0042

# Compare experiments
/ml:compare-experiments 0042

# Load experiment details
/ml:show-experiment exp-003-xgboost

# Export experiment data
/ml:export-experiments 0042 --format csv
```

## Tips

1. **Start tracking early** - Track from first experiment, not after 20 failed attempts
2. **Tag production models** - `exp.add_tag("production")` for deployed models
3. **Version everything** - Data, code, environment, dependencies
4. **Document decisions** - Why model A over model B (not just metrics)
5. **Prune old experiments** - Archive experiments >6 months old

## Advanced: Multi-Stage Experiments

For complex pipelines with multiple stages:

```python
from specweave import ExperimentPipeline

pipeline = ExperimentPipeline("recommendation-full-pipeline")

# Stage 1: Data preprocessing
with pipeline.stage("preprocessing") as stage:
    stage.log_metric("rows_before", len(df))
    df_clean = preprocess(df)
    stage.log_metric("rows_after", len(df_clean))

# Stage 2: Feature engineering
with pipeline.stage("features") as stage:
    features = engineer_features(df_clean)
    stage.log_metric("num_features", features.shape[1])

# Stage 3: Model training
with pipeline.stage("training") as stage:
    model = train_model(features)
    stage.log_metric("accuracy", accuracy)

# Logs entire pipeline with stage dependencies
```

## Integration Points

- **ml-pipeline-orchestrator**: Auto-tracks experiments during pipeline execution
- **model-evaluator**: Uses experiment data for model comparison
- **ml-engineer agent**: Reviews experiment results and suggests improvements
- **Living docs**: Syncs experiment findings to architecture docs

This skill ensures ML experimentation is never lost, always reproducible, and well-documented.
