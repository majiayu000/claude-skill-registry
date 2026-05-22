---
name: ml-pipeline-orchestrator
description: |
  Orchestrates complete machine learning pipelines within SpecWeave increments. Activates when users request "ML pipeline", "train model", "build ML system", "end-to-end ML", "ML workflow", "model training pipeline", or similar. Guides users through data preprocessing, feature engineering, model training, evaluation, and deployment using SpecWeave's spec-driven approach. Integrates with increment lifecycle for reproducible ML development.
---

# ML Pipeline Orchestrator

## Overview

This skill transforms ML development into a SpecWeave increment-based workflow, ensuring every ML project follows the same disciplined approach: spec → plan → tasks → implement → validate. It orchestrates the complete ML lifecycle from data exploration to model deployment, with full traceability and living documentation.

## Core Philosophy

**SpecWeave + ML = Disciplined Data Science**

Traditional ML development often lacks structure:
- ❌ Jupyter notebooks with no version control
- ❌ Experiments without documentation
- ❌ Models deployed with no reproducibility
- ❌ Team knowledge trapped in individual notebooks

SpecWeave brings discipline:
- ✅ Every ML feature is an increment (with spec, plan, tasks)
- ✅ Experiments tracked and documented automatically
- ✅ Model versions tied to increments
- ✅ Living docs capture learnings and decisions

## How It Works

### Phase 1: ML Increment Planning

When you request "build a recommendation model", the skill:

1. **Creates ML increment structure**:
```
.specweave/increments/0042-recommendation-model/
├── spec.md                    # ML requirements, success metrics
├── plan.md                    # Pipeline architecture
├── tasks.md                   # Implementation tasks
├── tests.md                   # Evaluation criteria
├── experiments/               # Experiment tracking
│   ├── exp-001-baseline/
│   ├── exp-002-xgboost/
│   └── exp-003-neural-net/
├── data/                      # Data samples, schemas
│   ├── schema.yaml
│   └── sample.csv
├── models/                    # Trained models
│   ├── model-v1.pkl
│   └── model-v2.pkl
└── notebooks/                 # Exploratory notebooks
    ├── 01-eda.ipynb
    └── 02-feature-engineering.ipynb
```

2. **Generates ML-specific spec** (spec.md):
```markdown
## ML Problem Definition
- Problem type: Recommendation (collaborative filtering)
- Input: User behavior history
- Output: Top-N product recommendations
- Success metrics: Precision@10 > 0.25, Recall@10 > 0.15

## Data Requirements
- Training data: 6 months user interactions
- Validation: Last month
- Features: User profile, product attributes, interaction history

## Model Requirements
- Latency: <100ms inference
- Throughput: 1000 req/sec
- Accuracy: Better than random baseline by 3x
- Explainability: Must explain top-3 recommendations
```

3. **Creates ML-specific tasks** (tasks.md):
```markdown
- [ ] T-001: Data exploration and quality analysis
- [ ] T-002: Feature engineering pipeline
- [ ] T-003: Train baseline model (random/popularity)
- [ ] T-004: Train candidate models (3 algorithms)
- [ ] T-005: Hyperparameter tuning (best model)
- [ ] T-006: Model evaluation (all metrics)
- [ ] T-007: Model explainability (SHAP/LIME)
- [ ] T-008: Production deployment preparation
- [ ] T-009: A/B test plan
```

### Phase 2: Pipeline Execution

The skill guides through each task with best practices:

#### Task 1: Data Exploration
```python
# Generated template with SpecWeave integration
import pandas as pd
import mlflow
from specweave import track_experiment

# Auto-logs to .specweave/increments/0042.../experiments/
with track_experiment("exp-001-eda") as exp:
    df = pd.read_csv("data/interactions.csv")
    
    # EDA
    exp.log_param("dataset_size", len(df))
    exp.log_metric("missing_values", df.isnull().sum().sum())
    
    # Auto-generates report in increment folder
    exp.save_report("eda-summary.md")
```

#### Task 3: Train Baseline
```python
from sklearn.dummy import DummyClassifier
from specweave import track_model

with track_model("baseline-random", increment="0042") as model:
    clf = DummyClassifier(strategy="uniform")
    clf.fit(X_train, y_train)
    
    # Automatically logged to increment
    model.log_metrics({
        "accuracy": 0.12,
        "precision@10": 0.08
    })
    model.save_artifact(clf, "baseline.pkl")
```

#### Task 4: Train Candidate Models
```python
from xgboost import XGBClassifier
from specweave import ModelExperiment

# Parallel experiments with auto-tracking
experiments = [
    ModelExperiment("xgboost", XGBClassifier, params_xgb),
    ModelExperiment("lightgbm", LGBMClassifier, params_lgbm),
    ModelExperiment("neural-net", KerasModel, params_nn)
]

results = run_experiments(
    experiments,
    increment="0042",
    save_to="experiments/"
)

# Auto-generates comparison table in increment docs
```

### Phase 3: Increment Completion

When `/sw:done 0042` runs:

1. **Validates ML-specific criteria**:
   - ✅ All experiments logged
   - ✅ Best model saved
   - ✅ Evaluation metrics documented
   - ✅ Model explainability artifacts present

2. **Generates completion summary**:
```markdown
## Recommendation Model - COMPLETE

### Experiments Run: 7
1. exp-001-baseline (random): precision@10=0.08
2. exp-002-popularity: precision@10=0.18
3. exp-003-xgboost: precision@10=0.26 ✅ BEST
4. exp-004-lightgbm: precision@10=0.24
5. exp-005-neural-net: precision@10=0.22
...

### Best Model
- Algorithm: XGBoost
- Version: model-v3.pkl
- Metrics: precision@10=0.26, recall@10=0.16
- Training time: 45 min
- Model size: 12 MB

### Deployment Ready
- ✅ Inference latency: 35ms (target: <100ms)
- ✅ Explainability: SHAP values computed
- ✅ A/B test plan documented
```

3. **Syncs living docs** (via `/sw:sync-docs`):
   - Updates architecture docs with model design
   - Adds ADR for algorithm selection
   - Documents learnings in runbooks

## When to Use This Skill

Activate this skill when you need to:

- **Build ML features end-to-end** - From idea to deployed model
- **Ensure reproducibility** - Every experiment tracked and documented
- **Follow ML best practices** - Baseline comparison, proper validation, explainability
- **Integrate ML with software engineering** - ML as increments, not isolated notebooks
- **Maintain team knowledge** - Living docs capture why decisions were made

## ML Pipeline Stages

### 1. Data Stage
- Data exploration (EDA)
- Data quality assessment
- Schema validation
- Sample data documentation

### 2. Feature Stage
- Feature engineering
- Feature selection
- Feature importance analysis
- Feature store integration (optional)

### 3. Training Stage
- Baseline model (random, rule-based)
- Candidate models (3+ algorithms)
- Hyperparameter tuning
- Cross-validation

### 4. Evaluation Stage
- Comprehensive metrics (accuracy, precision, recall, F1, AUC)
- Business metrics (latency, throughput)
- Model comparison (vs baseline, vs previous version)
- Error analysis

### 5. Explainability Stage
- Feature importance
- SHAP values
- LIME explanations
- Example predictions with rationale

### 6. Deployment Stage
- Model packaging
- Inference pipeline
- A/B test plan
- Monitoring setup

## Integration with SpecWeave Workflow

### With Experiment Tracking
```bash
# Start ML increment
/sw:inc "0042-recommendation-model"

# Automatically integrates experiment tracking
# All MLflow/W&B logs saved to increment folder
```

### With Living Docs
```bash
# After training best model
/sw:sync-docs update

# Automatically:
# - Updates architecture/ml-models.md
# - Adds ADR for algorithm choice
# - Documents hyperparameters in runbooks
```

### With GitHub Sync
```bash
# Create GitHub issue for model retraining
/sw:github:create-issue "Retrain recommendation model with new data"

# Linked to increment 0042
# Issue tracks model performance over time
```

## Best Practices

### 1. Always Start with Baseline
```python
# Before training complex models, establish baseline
baseline_results = train_baseline_model(
    strategies=["random", "popularity", "rule-based"]
)
# Requirement: New model must beat best baseline by 20%+
```

### 2. Use Cross-Validation
```python
# Never trust single train/test split
cv_scores = cross_val_score(model, X, y, cv=5)
exp.log_metric("cv_mean", cv_scores.mean())
exp.log_metric("cv_std", cv_scores.std())
```

### 3. Track Everything
```python
# Hyperparameters, metrics, artifacts, environment
exp.log_params(model.get_params())
exp.log_metrics({"accuracy": acc, "f1": f1})
exp.log_artifact("model.pkl")
exp.log_artifact("requirements.txt")  # Reproducibility
```

### 4. Document Failures
```python
# Failed experiments are valuable learnings
with track_experiment("exp-006-failed-lstm") as exp:
    # ... training fails ...
    exp.log_note("FAILED: LSTM overfits badly, needs regularization")
    exp.set_status("failed")
# This documents why LSTM wasn't chosen
```

### 5. Model Versioning
```python
# Tie model versions to increments
model_version = f"0042-v{iteration}"
mlflow.register_model(
    f"runs:/{run_id}/model",
    f"recommendation-model-{model_version}"
)
```

## Examples

### Example 1: Classification Pipeline
```bash
User: "Build a fraud detection model for transactions"

Skill creates increment 0051-fraud-detection with:
- spec.md: Binary classification, 99% precision target
- plan.md: Imbalanced data handling, threshold tuning
- tasks.md: 9 tasks from EDA to deployment
- experiments/: exp-001-baseline, exp-002-xgboost, etc.

Guides through:
1. EDA → identify class imbalance (0.1% fraud)
2. Baseline → random/majority (terrible results)
3. Candidates → XGBoost, LightGBM, Neural Net
4. Threshold tuning → optimize for precision
5. SHAP → explain high-risk predictions
6. Deploy → model + threshold + explainer
```

### Example 2: Regression Pipeline
```bash
User: "Predict customer lifetime value"

Skill creates increment 0063-ltv-prediction with:
- spec.md: Regression, RMSE < $50 target
- plan.md: Time-based validation, feature engineering
- tasks.md: Customer cohort analysis, feature importance

Key difference: Regression-specific evaluation (RMSE, MAE, R²)
```

### Example 3: Time Series Forecasting
```bash
User: "Forecast weekly sales for next 12 weeks"

Skill creates increment 0072-sales-forecasting with:
- spec.md: Time series, MAPE < 10% target
- plan.md: Seasonal decomposition, ARIMA vs Prophet
- tasks.md: Stationarity tests, residual analysis

Key difference: Time series validation (no random split)
```

## Framework Support

This skill works with all major ML frameworks:

### Scikit-Learn
```python
from sklearn.ensemble import RandomForestClassifier
from specweave import track_sklearn_model

model = RandomForestClassifier(n_estimators=100)
with track_sklearn_model(model, increment="0042") as tracked:
    tracked.fit(X_train, y_train)
    tracked.evaluate(X_test, y_test)
```

### PyTorch
```python
import torch
from specweave import track_pytorch_model

model = NeuralNet()
with track_pytorch_model(model, increment="0042") as tracked:
    for epoch in range(epochs):
        tracked.train_epoch(train_loader)
        tracked.log_metric(f"loss_epoch_{epoch}", loss)
```

### TensorFlow/Keras
```python
from tensorflow import keras
from specweave import KerasCallback

model = keras.Sequential([...])
model.fit(
    X_train, y_train,
    callbacks=[KerasCallback(increment="0042")]
)
```

### XGBoost/LightGBM
```python
import xgboost as xgb
from specweave import track_boosting_model

dtrain = xgb.DMatrix(X_train, label=y_train)
with track_boosting_model("xgboost", increment="0042") as tracked:
    model = xgb.train(params, dtrain, callbacks=[tracked.callback])
```

## Integration Points

### With `experiment-tracker` skill
- Auto-detects MLflow/W&B in project
- Configures tracking URI to increment folder
- Syncs experiment metadata to increment docs

### With `model-evaluator` skill
- Generates comprehensive evaluation reports
- Compares models across experiments
- Highlights best model with confidence intervals

### With `feature-engineer` skill
- Generates feature engineering pipeline
- Documents feature importance
- Creates feature store schemas

### With `ml-engineer` agent
- Delegates complex ML decisions to specialized agent
- Reviews model architecture
- Suggests improvements based on results

## Skill Outputs

After running `/sw:do` on an ML increment, you get:

```
.specweave/increments/0042-recommendation-model/
├── spec.md ✅
├── plan.md ✅
├── tasks.md ✅ (all completed)
├── COMPLETION-SUMMARY.md ✅
├── experiments/
│   ├── exp-001-baseline/
│   │   ├── metrics.json
│   │   ├── params.json
│   │   └── logs/
│   ├── exp-002-xgboost/ ✅ BEST
│   │   ├── metrics.json
│   │   ├── params.json
│   │   ├── model.pkl
│   │   └── shap_values.pkl
│   └── comparison.md
├── models/
│   ├── model-v3.pkl (best)
│   └── model-v3.metadata.json
├── data/
│   ├── schema.yaml
│   └── sample.parquet
└── notebooks/
    ├── 01-eda.ipynb
    ├── 02-feature-engineering.ipynb
    └── 03-model-analysis.ipynb
```

## Commands

This skill integrates with SpecWeave commands:

```bash
# Create ML increment
/sw:inc "build recommendation model"
→ Activates ml-pipeline-orchestrator
→ Creates ML-specific increment structure

# Execute ML tasks
/sw:do
→ Guides through data → train → eval workflow
→ Auto-tracks experiments

# Validate ML increment
/sw:validate 0042
→ Checks: experiments logged, model saved, metrics documented
→ Validates: model meets success criteria

# Complete ML increment
/sw:done 0042
→ Generates ML completion summary
→ Syncs model metadata to living docs
```

## Tips

1. **Start simple** - Always begin with baseline, then iterate
2. **Track failures** - Document why approaches didn't work
3. **Version data** - Use DVC or similar for data versioning
4. **Reproducibility** - Log environment (requirements.txt, conda env)
5. **Incremental improvement** - Each increment improves on previous model
6. **Team collaboration** - Living docs make ML decisions visible to all

## Advanced: Multi-Increment ML Projects

For complex ML systems (e.g., recommendation system with multiple models):

```
0042-recommendation-data-pipeline
0043-recommendation-candidate-generation
0044-recommendation-ranking-model
0045-recommendation-reranking
0046-recommendation-ab-test
```

Each increment:
- Has its own spec, plan, tasks
- Builds on previous increments
- Documents model interactions
- Maintains system-level living docs
