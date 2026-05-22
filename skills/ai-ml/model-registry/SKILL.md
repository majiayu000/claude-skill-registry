---
name: model-registry
description: |
  Centralized model versioning, staging, and lifecycle management. Activates for "model registry", "model versioning", "model staging", "deploy to production", "rollback model", "model metadata", "model lineage", "promote model", "model catalog". Manages ML model lifecycle from development through production with SpecWeave increment integration.
---

# Model Registry

## Overview

Centralized system for managing ML model lifecycle: versioning, staging (dev/staging/prod), metadata tracking, lineage, and rollback. Ensures production models are tracked, reproducible, and can be safely deployed or rolled back—all integrated with SpecWeave's increment workflow.

## Why Model Registry Matters

**Without Model Registry**:
- ❌ "Which model is in production?"
- ❌ "Can't reproduce model from 3 months ago"
- ❌ "Breaking change deployed, how to rollback?"
- ❌ "Model metadata scattered across notebooks"
- ❌ "No audit trail for model changes"

**With Model Registry**:
- ✅ Single source of truth for all models
- ✅ Full version history with metadata
- ✅ Safe staging pipeline (dev → staging → prod)
- ✅ One-command rollback
- ✅ Complete model lineage
- ✅ Audit trail for compliance

## Model Registry Structure

### Model Lifecycle Stages

```
Development → Staging → Production → Archived

Dev:      Training, experimentation
Staging:  Validation, A/B testing (10% traffic)
Prod:     Production deployment (100% traffic)
Archived: Decommissioned, kept for audit
```

## Core Operations

### 1. Model Registration

```python
from specweave import ModelRegistry

registry = ModelRegistry(increment="0042")

# Register new model version
model_version = registry.register_model(
    name="fraud-detection-model",
    model=trained_model,
    version="v3",
    metadata={
        "algorithm": "XGBoost",
        "accuracy": 0.87,
        "precision": 0.85,
        "recall": 0.62,
        "training_date": "2024-01-15",
        "training_data_version": "v2024-01",
        "hyperparameters": {
            "n_estimators": 673,
            "max_depth": 6,
            "learning_rate": 0.094
        },
        "features": feature_names,
        "framework": "xgboost==1.7.0",
        "python_version": "3.10",
        "increment": "0042"
    },
    stage="dev",  # Initial stage
    tags=["fraud", "production-candidate"]
)

# Creates:
# - Model artifact (model.pkl)
# - Model metadata (metadata.json)
# - Model signature (inputs/outputs)
# - Environment file (requirements.txt)
# - Feature schema (features.yaml)
```

### 2. Model Versioning

```python
# Semantic versioning: major.minor.patch
registry.version_model(
    name="fraud-detection-model",
    version_type="minor"  # v3.0.0 → v3.1.0
)

# Auto-increments based on changes:
# - major: Breaking changes (different features, incompatible)
# - minor: Improvements (better accuracy, new features added)
# - patch: Bugfixes, retraining (same features, slight changes)
```

### 3. Model Promotion

**Stage Progression**:
```python
# Promote from dev to staging
registry.promote_model(
    name="fraud-detection-model",
    version="v3.1.0",
    from_stage="dev",
    to_stage="staging",
    approval_required=True  # Requires review
)

# Validate in staging (A/B test)
ab_test_results = run_ab_test(
    control="fraud-detection-v3.0.0",
    treatment="fraud-detection-v3.1.0",
    traffic_split=0.1,  # 10% to new model
    duration_days=7
)

# Promote to production if successful
if ab_test_results['treatment_is_better']:
    registry.promote_model(
        name="fraud-detection-model",
        version="v3.1.0",
        from_stage="staging",
        to_stage="production"
    )
```

### 4. Model Rollback

```python
# Rollback to previous version
registry.rollback(
    name="fraud-detection-model",
    to_version="v3.0.0",  # Previous stable version
    reason="v3.1.0 causing high false positive rate"
)

# Automatic rollback triggers:
registry.set_auto_rollback_triggers(
    error_rate_threshold=0.05,  # Rollback if >5% errors
    latency_threshold=200,  # Rollback if p95 > 200ms
    accuracy_drop_threshold=0.10  # Rollback if accuracy drops >10%
)
```

### 5. Model Retrieval

```python
# Get latest production model
model = registry.get_model(
    name="fraud-detection-model",
    stage="production"
)

# Get specific version
model_v3 = registry.get_model(
    name="fraud-detection-model",
    version="v3.1.0"
)

# Get model by date
model_jan = registry.get_model_by_date(
    name="fraud-detection-model",
    date="2024-01-15"
)
```

## Model Metadata

### Tracked Metadata

```python
model_metadata = {
    # Core Info
    "name": "fraud-detection-model",
    "version": "v3.1.0",
    "stage": "production",
    "created_at": "2024-01-15T10:30:00Z",
    "updated_at": "2024-01-20T14:00:00Z",
    
    # Training Info
    "algorithm": "XGBoost",
    "framework": "xgboost==1.7.0",
    "python_version": "3.10",
    "training_duration": "45min",
    "training_data_size": "100k rows",
    
    # Performance Metrics
    "accuracy": 0.87,
    "precision": 0.85,
    "recall": 0.62,
    "roc_auc": 0.92,
    "f1_score": 0.72,
    
    # Deployment Info
    "inference_latency_p50": "35ms",
    "inference_latency_p95": "80ms",
    "model_size": "12MB",
    "cpu_usage": "0.2 cores",
    "memory_usage": "256MB",
    
    # Lineage
    "increment": "0042-fraud-detection",
    "experiment": "exp-003-xgboost",
    "training_data_version": "v2024-01",
    "feature_engineering_version": "v1",
    "parent_model": "fraud-detection-v3.0.0",
    
    # Features
    "features": [
        "amount_vs_user_average",
        "days_since_last_purchase",
        "merchant_risk_score",
        ...
    ],
    "num_features": 35,
    
    # Tags & Labels
    "tags": ["fraud", "production", "high-precision"],
    "owner": "[email protected]",
    "approver": "[email protected]"
}
```

## Model Lineage

### Tracking Model Lineage

```python
# Full lineage: data → features → training → model
lineage = registry.get_lineage(
    name="fraud-detection-model",
    version="v3.1.0"
)

# Lineage graph:
"""
data:v2024-01
  └─> feature-engineering:v1
        └─> experiment:exp-003-xgboost
              └─> model:fraud-detection-v3.1.0
                    └─> deployment:production
"""

# Answer questions like:
# - "What data was used to train this model?"
# - "Which experiments led to this model?"
# - "What models use this feature set?"
# - "Impact of changing feature X?"
```

### Model Comparison

```python
# Compare two model versions
comparison = registry.compare_models(
    model_a="fraud-detection-v3.0.0",
    model_b="fraud-detection-v3.1.0"
)

# Output:
"""
Comparison: v3.0.0 vs v3.1.0
============================

Metrics:
- Accuracy:  0.85 → 0.87 (+2.4%) ✅
- Precision: 0.83 → 0.85 (+2.4%) ✅
- Recall:    0.60 → 0.62 (+3.3%) ✅

Performance:
- Latency:   40ms → 35ms (-12.5%) ✅
- Size:      15MB → 12MB (-20.0%) ✅

Features:
- Added: merchant_reputation_score
- Removed: obsolete_feature_x
- Modified: 3 features rescaled

Recommendation: ✅ v3.1.0 is better (improvement in all metrics)
"""
```

## Integration with SpecWeave

### Automatic Registration

```python
# Models automatically registered during increment completion
with track_experiment("xgboost-v1", increment="0042") as exp:
    model = train_model(X_train, y_train)
    
    # Auto-registers model to registry
    exp.register_model(
        model=model,
        name="fraud-detection-model",
        auto_version=True  # Auto-increment version
    )
```

### Increment-Model Mapping

```
.specweave/increments/0042-fraud-detection/
├── models/
│   ├── fraud-detection-v3.0.0/
│   │   ├── model.pkl
│   │   ├── metadata.json
│   │   ├── requirements.txt
│   │   └── features.yaml
│   └── fraud-detection-v3.1.0/
│       ├── model.pkl
│       ├── metadata.json
│       ├── requirements.txt
│       └── features.yaml
└── registry/
    ├── model_catalog.yaml
    ├── lineage_graph.json
    └── deployment_history.md
```

### Living Docs Integration

```bash
/sw:sync-docs update
```

Updates:
```markdown
<!-- .specweave/docs/internal/architecture/model-registry.md -->

## Fraud Detection Model - Production

### Current Production Model
- Version: v3.1.0
- Deployed: 2024-01-20
- Accuracy: 87%
- Latency: 35ms (p50)

### Version History
| Version | Stage | Accuracy | Deployed | Notes |
|---------|-------|----------|----------|-------|
| v3.1.0  | Prod  | 0.87     | 2024-01-20 | Current ✅ |
| v3.0.0  | Archived | 0.85  | 2024-01-10 | Replaced by v3.1.0 |
| v2.5.0  | Archived | 0.83  | 2023-12-01 | Retired |

### Rollback Plan
If v3.1.0 issues detected:
1. Rollback to v3.0.0 (tested, stable)
2. Investigate issue in staging
3. Deploy fix as v3.1.1
```

## Model Registry Providers

### MLflow Model Registry

```python
from specweave import MLflowRegistry

# Use MLflow as backend
registry = MLflowRegistry(
    tracking_uri="http://mlflow.company.com",
    increment="0042"
)

# All SpecWeave operations work with MLflow backend
registry.register_model(...)
registry.promote_model(...)
```

### Custom Registry

```python
from specweave import CustomRegistry

# Use custom storage (S3, GCS, Azure Blob)
registry = CustomRegistry(
    storage_uri="s3://ml-models/registry",
    increment="0042"
)
```

## Best Practices

### 1. Semantic Versioning

```python
# Breaking change (different features)
registry.version_model(version_type="major")  # v3.0.0 → v4.0.0

# Feature addition (backward compatible)
registry.version_model(version_type="minor")  # v3.0.0 → v3.1.0

# Bugfix or retraining (no API change)
registry.version_model(version_type="patch")  # v3.0.0 → v3.0.1
```

### 2. Model Signatures

```python
# Document input/output schema
registry.set_model_signature(
    model="fraud-detection-v3.1.0",
    inputs={
        "amount": "float",
        "merchant_id": "int",
        "location": "str"
    },
    outputs={
        "fraud_probability": "float",
        "fraud_flag": "bool",
        "risk_score": "float"
    }
)

# Prevents breaking changes (validate on registration)
```

### 3. Model Approval Workflow

```python
# Require approval before production
registry.set_approval_required(
    stage="production",
    approvers=["[email protected]", "[email protected]"]
)

# Approve model promotion
registry.approve_model(
    name="fraud-detection-model",
    version="v3.1.0",
    approver="[email protected]",
    comments="Tested in staging, accuracy improved 2%, latency reduced 12%"
)
```

### 4. Model Deprecation

```python
# Mark old models as deprecated
registry.deprecate_model(
    name="fraud-detection-model",
    version="v2.5.0",
    reason="Superseded by v3.x series",
    end_of_life="2024-06-01"
)
```

## Commands

```bash
# List all models
/ml:registry-list

# Get model info
/ml:registry-info fraud-detection-model

# Promote model
/ml:registry-promote fraud-detection-model v3.1.0 --to production

# Rollback model
/ml:registry-rollback fraud-detection-model --to v3.0.0

# Compare models
/ml:registry-compare fraud-detection-model v3.0.0 v3.1.0
```

## Advanced Features

### 1. Model Monitoring Integration

```python
# Automatically track production model performance
monitor = ModelMonitor(registry=registry)

monitor.track_model(
    name="fraud-detection-model",
    stage="production",
    metrics=["accuracy", "latency", "error_rate"]
)

# Auto-rollback if metrics degrade
monitor.set_auto_rollback(
    metric="accuracy",
    threshold=0.80,  # Rollback if < 80%
    window="24h"
)
```

### 2. Model Governance

```python
# Compliance and audit trail
governance = ModelGovernance(registry=registry)

# Generate audit report
audit_report = governance.generate_audit_report(
    model="fraud-detection-model",
    start_date="2023-01-01",
    end_date="2024-01-31"
)

# Includes:
# - All model versions deployed
# - Who approved deployments
# - Performance metrics over time
# - Data sources used
# - Compliance checkpoints
```

### 3. Multi-Environment Registry

```python
# Separate registries for dev, staging, prod
registry_dev = ModelRegistry(environment="dev")
registry_staging = ModelRegistry(environment="staging")
registry_prod = ModelRegistry(environment="production")

# Promote across environments
registry_dev.promote_to(
    model="fraud-detection-v3.1.0",
    target_env="staging"
)
```

## Summary

Model Registry is essential for:
- ✅ Model versioning (track all model versions)
- ✅ Safe deployment (dev → staging → prod pipeline)
- ✅ Fast rollback (one-command revert to stable version)
- ✅ Audit trail (who deployed what, when, why)
- ✅ Model lineage (data → features → model → deployment)
- ✅ Compliance (regulatory requirements, governance)

This skill brings enterprise-grade model lifecycle management to SpecWeave, ensuring all models are tracked, reproducible, and safely deployed.
