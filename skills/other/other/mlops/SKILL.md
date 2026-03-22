---
name: mlops
description: "Implement MLOps practices for ML lifecycle management. Use for CI/CD pipelines, model versioning, experiment tracking, automated training, deployment automation, monitoring, and production ML workflows."
---

# MLOps

Implement MLOps practices for managing the complete ML lifecycle.

## Overview

MLOps applies DevOps principles to machine learning, enabling reliable, scalable, and automated ML systems. This skill covers pipelines, versioning, monitoring, and production workflows.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Experiment tracking and versioning | MLflow, Weights & Biases, DVC | `/references/tracking.md` |
| Automated training and deployment | CI/CD pipelines, Kubeflow, Airflow | `/references/automation.md` |
| Production monitoring and maintenance | Drift detection, retraining, A/B testing | `/references/production.md` |

## Core Principles

1. **Automation** - Automate training, testing, and deployment
2. **Versioning** - Track code, data, and models
3. **Reproducibility** - Ensure consistent results
4. **Monitoring** - Detect performance degradation
5. **Collaboration** - Enable team workflows

## MLOps Components

### Experiment Tracking
Record experiments, metrics, and artifacts.

**Tools:**
- MLflow: Open-source, comprehensive
- Weights & Biases: Collaborative, feature-rich
- TensorBoard: Visualization-focused

**Track:**
- Hyperparameters
- Metrics (loss, accuracy)
- Model artifacts
- Code versions

### Data Versioning
Version control for datasets.

**Tools:**
- DVC (Data Version Control)
- Git LFS
- Delta Lake

**Benefits:**
- Reproducibility
- Lineage tracking
- Collaboration

### Model Registry
Centralized model storage and versioning.

**Features:**
- Version management
- Stage transitions (staging, production)
- Metadata and lineage
- Access control

**Tools:**
- MLflow Model Registry
- AWS SageMaker Model Registry
- Azure ML Model Registry

## CI/CD for ML

### Continuous Integration
Automated testing of code and models.

**Tests:**
- Unit tests for code
- Data validation
- Model performance tests
- Integration tests

### Continuous Deployment
Automated model deployment.

**Steps:**
1. Trigger on model registry update
2. Run validation tests
3. Deploy to staging
4. Run integration tests
5. Deploy to production
6. Monitor performance

### Pipeline Orchestration
Automate ML workflows.

**Tools:**
- Kubeflow Pipelines
- Apache Airflow
- AWS Step Functions
- Azure ML Pipelines

## Production Monitoring

### Model Performance
Track prediction quality.

**Metrics:**
- Accuracy, precision, recall
- Latency, throughput
- Error rates

### Data Drift
Detect changes in input distribution.

**Methods:**
- Statistical tests (KS test, Chi-square)
- Distribution comparison
- Feature drift monitoring

### Model Drift
Detect degradation in model performance.

**Indicators:**
- Decreasing accuracy
- Changing prediction distribution
- Increased errors

**Response:**
- Retrain model
- Update features
- Investigate root cause

## Using the Reference Files

**`/references/tracking.md`** — Experiment tracking with MLflow and W&B, data versioning with DVC, model registry, and reproducibility practices.

**`/references/automation.md`** — CI/CD pipelines for ML, automated training, testing strategies, deployment automation, and orchestration tools.

**`/references/production.md`** — Model monitoring, drift detection, automated retraining, A/B testing, canary deployments, and incident response.

## Best Practices

- Version everything (code, data, models)
- Automate testing and deployment
- Monitor models in production
- Implement automated retraining
- Use feature stores for consistency
- Document pipelines and processes
- Set up alerting for failures
- Practice reproducibility
- Enable collaboration with tools
- Plan for model updates

## Common Pitfalls to Avoid

- Manual deployment processes
- No data versioning
- Insufficient monitoring
- Ignoring data drift
- No automated retraining
- Poor experiment tracking
- Lack of testing
- No rollback strategy
- Inadequate documentation
- Not planning for scale

