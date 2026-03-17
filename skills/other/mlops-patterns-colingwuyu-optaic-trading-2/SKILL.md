---
name: mlops-patterns
description: Follow these patterns when implementing MLOps features in OptAIC. Use for ML model definitions (5-component structure), model instances, training/inference pipelines, model registry, and monitoring. Covers signal models, macro regime models, relevance models, and signal combining/filtering models.
---

# MLOps Implementation Patterns

Guide for implementing MLOps features that integrate with OptAIC's resource-based architecture.

## When to Use

Apply when:
- Creating ML Model Definitions (MLModuleDef) with 5 code components
- Implementing Model Instances in MLOps Center
- Building training, inference, or monitoring pipelines
- Integrating with model registry (MLflow or internal)
- Implementing model categories (signal, regime, relevance, combining)

## MLOps Three-Tier Model

```
MLModuleDef (Definition)    ModelInstance (Config)       Execution (Runs)
────────────────────────    ──────────────────────       ─────────────────
XGBSignalModelDef       →   SPX_Alpha_Model          →   TrainingRun
  (5 code components)         (datasets + config)          InferenceRun
                                                           MonitoringRun
                                                               ↓
                                                         ModelVersion
```

## ML Model Categories

| Category | Purpose | Typical Outputs |
|----------|---------|-----------------|
| **Signal Model** | Generate alpha signals | Signal dataset [-1, 1] |
| **Macro Regime Model** | Classify market regimes | Regime labels/probabilities |
| **Relevance Model** | Score feature importance | Relevance scores |
| **Signal Combining Model** | Combine multiple signals | Combined signal |
| **Signal Filtering Model** | Filter/rank signals | Filtered signal set |

## Implementation Workflow

### 1. Create MLModuleDef (5 Components)

```
MLModelDef/
├── model/           # Model architecture + hyperparameter schema
├── training/        # Trainer + evaluator
├── inference/       # Predictor + batch inference
├── monitoring/      # Data drift + performance monitoring
├── tests/           # Test suite for all components
└── docs/            # Documentation
```

See [references/mlmodule-structure.md](references/mlmodule-structure.md).

### 2. Create Model Instance

Compose MLModuleDef + datasets + config. See [references/model-instance.md](references/model-instance.md).

### 3. Implement Pipelines

- **TrainingPipeline** → reads datasets, produces ModelVersion
- **InferencePipeline** → reads features + model, writes predictions
- **MonitoringPipeline** → reads data/preds, emits metrics/alerts

See [references/mlops-pipelines.md](references/mlops-pipelines.md).

### 4. Integrate with Registry

See [references/model-registry.md](references/model-registry.md).

### 5. Create UI Components (MLOps Center)

Two views required:
- **Model Instance View** - registered models with configs
- **Execution View** - training, registry, inference, monitoring

See [references/mlops-center-ui.md](references/mlops-center-ui.md).

## Critical Rules

1. **5-component structure** - MLModuleDef must have model, training, inference, monitoring, tests
2. **Activity emission** - All runs emit activities (training, inference, monitoring)
3. **Lineage tracking** - Link dataset versions → model version → prediction dataset
4. **Guardrails** - Validate model outputs (e.g., signal bounds)
5. **PIT correctness** - No lookahead in training or inference

## Tech Stack

| Tool | Purpose | Mode |
|------|---------|------|
| **MLflow** | Experiment tracking, model registry | Optional (`--with-mlflow`) |
| **Evidently** | Data drift, performance monitoring, test suites | Always available |
| **WhyLogs** | Lightweight data profiling | Optional |
| **Prefect** | Workflow orchestration | Optional (`--with-prefect`) |

## Unified ML SDK (`optaic.mlops`)

All MLOps infrastructure is wrapped in a unified SDK for seamless development:

```python
from optaic.mlops import tracking, registry, monitoring, pipeline
from optaic.mlops.base import BaseModel, BaseTrainer
from optaic.mlops.data import load_dataset
```

**Key modules:**
- `tracking` - Experiment logging (wraps MLflow)
- `registry` - Model versioning (wraps MLflow Model Registry)
- `monitoring` - Drift & performance (wraps Evidently)
- `pipeline` - Orchestration (wraps Prefect)
- `data` - PIT-aware dataset access
- `base` - Base classes for model definitions

See [references/unified-sdk.md](references/unified-sdk.md) and Blueprint section 8.9.

## Reference Files

- [Unified SDK](references/unified-sdk.md) - `optaic.mlops` SDK patterns
- [MLModuleDef Structure](references/mlmodule-structure.md) - 5-component package
- [Model Instance](references/model-instance.md) - Configuration patterns
- [MLOps Pipelines](references/mlops-pipelines.md) - Training/inference/monitoring
- [Model Registry](references/model-registry.md) - Version management
- [MLOps Center UI](references/mlops-center-ui.md) - Two-view architecture
- [MLflow + Evidently Integration](references/mlflow-evidently-integration.md) - Experiment tracking & monitoring
