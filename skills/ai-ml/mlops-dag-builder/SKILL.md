---
name: mlops-dag-builder
description: Design DAG-based MLOps pipeline architectures with Airflow, Dagster, Kubeflow, or Prefect. Activates for DAG orchestration, workflow automation, pipeline design patterns, CI/CD for ML. Use for platform-agnostic MLOps infrastructure - NOT for SpecWeave increment-based ML (use ml-pipeline-orchestrator instead).
---

# MLOps DAG Builder

Design and implement DAG-based ML pipeline architectures using production orchestration tools.

## Overview

This skill provides guidance for building **platform-agnostic MLOps pipelines** using DAG orchestrators (Airflow, Dagster, Kubeflow, Prefect). It focuses on workflow architecture, not SpecWeave integration.

**When to use this skill vs ml-pipeline-orchestrator:**
- **Use this skill**: General MLOps architecture, Airflow/Dagster DAGs, cloud ML platforms
- **Use ml-pipeline-orchestrator**: SpecWeave increment-based ML development with experiment tracking

## When to Use This Skill

- Designing DAG-based workflow orchestration (Airflow, Dagster, Kubeflow)
- Implementing platform-agnostic ML pipeline patterns
- Setting up CI/CD automation for ML training jobs
- Creating reusable pipeline templates for teams
- Integrating with cloud ML services (SageMaker, Vertex AI, Azure ML)

## What This Skill Provides

### Core Capabilities

1. **Pipeline Architecture**
   - End-to-end workflow design
   - DAG orchestration patterns (Airflow, Dagster, Kubeflow)
   - Component dependencies and data flow
   - Error handling and retry strategies

2. **Data Preparation**
   - Data validation and quality checks
   - Feature engineering pipelines
   - Data versioning and lineage
   - Train/validation/test splitting strategies

3. **Model Training**
   - Training job orchestration
   - Hyperparameter management
   - Experiment tracking integration
   - Distributed training patterns

4. **Model Validation**
   - Validation frameworks and metrics
   - A/B testing infrastructure
   - Performance regression detection
   - Model comparison workflows

5. **Deployment Automation**
   - Model serving patterns
   - Canary deployments
   - Blue-green deployment strategies
   - Rollback mechanisms

## Usage Patterns

### Basic Pipeline Setup

```python
# 1. Define pipeline stages
stages = [
    "data_ingestion",
    "data_validation",
    "feature_engineering",
    "model_training",
    "model_validation",
    "model_deployment"
]

# 2. Configure dependencies between stages
```

### Production Workflow

1. **Data Preparation Phase**
   - Ingest raw data from sources
   - Run data quality checks
   - Apply feature transformations
   - Version processed datasets

2. **Training Phase**
   - Load versioned training data
   - Execute training jobs
   - Track experiments and metrics
   - Save trained models

3. **Validation Phase**
   - Run validation test suite
   - Compare against baseline
   - Generate performance reports
   - Approve for deployment

4. **Deployment Phase**
   - Package model artifacts
   - Deploy to serving infrastructure
   - Configure monitoring
   - Validate production traffic

## Best Practices

### Pipeline Design

- **Modularity**: Each stage should be independently testable
- **Idempotency**: Re-running stages should be safe
- **Observability**: Log metrics at every stage
- **Versioning**: Track data, code, and model versions
- **Failure Handling**: Implement retry logic and alerting

### Data Management

- Use data validation libraries (Great Expectations, TFX)
- Version datasets with DVC or similar tools
- Document feature engineering transformations
- Maintain data lineage tracking

### Model Operations

- Separate training and serving infrastructure
- Use model registries (MLflow, Weights & Biases)
- Implement gradual rollouts for new models
- Monitor model performance drift
- Maintain rollback capabilities

### Deployment Strategies

- Start with shadow deployments
- Use canary releases for validation
- Implement A/B testing infrastructure
- Set up automated rollback triggers
- Monitor latency and throughput

## Integration Points

### Orchestration Tools

- **Apache Airflow**: DAG-based workflow orchestration
- **Dagster**: Asset-based pipeline orchestration
- **Kubeflow Pipelines**: Kubernetes-native ML workflows
- **Prefect**: Modern dataflow automation

### Experiment Tracking

- MLflow for experiment tracking and model registry
- Weights & Biases for visualization and collaboration
- TensorBoard for training metrics

### Deployment Platforms

- AWS SageMaker for managed ML infrastructure
- Google Vertex AI for GCP deployments
- Azure ML for Azure cloud
- Kubernetes + KServe for cloud-agnostic serving

## Progressive Disclosure

Start with the basics and gradually add complexity:

1. **Level 1**: Simple linear pipeline (data → train → deploy)
2. **Level 2**: Add validation and monitoring stages
3. **Level 3**: Implement hyperparameter tuning
4. **Level 4**: Add A/B testing and gradual rollouts
5. **Level 5**: Multi-model pipelines with ensemble strategies

## Common Patterns

### Batch Training Pipeline

```yaml
stages:
  - name: data_preparation
    dependencies: []
  - name: model_training
    dependencies: [data_preparation]
  - name: model_evaluation
    dependencies: [model_training]
  - name: model_deployment
    dependencies: [model_evaluation]
```

### Real-time Feature Pipeline

```python
# Stream processing for real-time features
# Combined with batch training for production
```

### Continuous Training

```python
# Automated retraining on schedule
# Triggered by data drift detection
```

## Troubleshooting

### Common Issues

- **Pipeline failures**: Check dependencies and data availability
- **Training instability**: Review hyperparameters and data quality
- **Deployment issues**: Validate model artifacts and serving config
- **Performance degradation**: Monitor data drift and model metrics

### Debugging Steps

1. Check pipeline logs for each stage
2. Validate input/output data at boundaries
3. Test components in isolation
4. Review experiment tracking metrics
5. Inspect model artifacts and metadata

## Next Steps

After setting up your pipeline:

1. Explore **hyperparameter-tuning** skill for optimization
2. Learn **experiment-tracking-setup** for MLflow/W&B
3. Review **model-deployment-patterns** for serving strategies
4. Implement monitoring with observability tools

## Related Skills

- **ml-pipeline-orchestrator**: SpecWeave-integrated ML development (use for increment-based ML)
- **experiment-tracker**: MLflow and Weights & Biases experiment tracking
- **automl-optimizer**: Automated hyperparameter optimization with Optuna/Hyperopt
- **ml-deployment-helper**: Model serving and deployment patterns
