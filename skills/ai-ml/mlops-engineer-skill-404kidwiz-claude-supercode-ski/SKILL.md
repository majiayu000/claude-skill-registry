---
name: mlops-engineer
description: Expert in Machine Learning Operations bridging data science and DevOps. Use when building ML pipelines, model versioning, feature stores, or production ML serving. Triggers include "MLOps", "ML pipeline", "model deployment", "feature store", "model versioning", "ML monitoring", "Kubeflow", "MLflow".
---

# MLOps Engineer

## Purpose
Provides expertise in Machine Learning Operations, bridging data science and DevOps practices. Specializes in end-to-end ML lifecycles from training pipelines to production serving, model versioning, and monitoring.

## When to Use
- Building ML training and serving pipelines
- Implementing model versioning and registry
- Setting up feature stores
- Deploying models to production
- Monitoring model performance and drift
- Automating ML workflows (CI/CD for ML)
- Implementing A/B testing for models
- Managing experiment tracking

## Quick Start
**Invoke this skill when:**
- Building ML pipelines and workflows
- Deploying models to production
- Setting up model versioning and registry
- Implementing feature stores
- Monitoring production ML systems

**Do NOT invoke when:**
- Model development and training → use `/ml-engineer`
- Data pipeline ETL → use `/data-engineer`
- Kubernetes infrastructure → use `/kubernetes-specialist`
- General CI/CD without ML → use `/devops-engineer`

## Decision Framework
```
ML Lifecycle Stage?
├── Experimentation
│   └── MLflow/Weights & Biases for tracking
├── Training Pipeline
│   └── Kubeflow/Airflow/Vertex AI
├── Model Registry
│   └── MLflow Registry/Vertex Model Registry
├── Serving
│   ├── Batch → Spark/Dataflow
│   └── Real-time → TF Serving/Seldon/KServe
└── Monitoring
    └── Evidently/Fiddler/custom metrics
```

## Core Workflows

### 1. ML Pipeline Setup
1. Define pipeline stages (data prep, training, eval)
2. Choose orchestrator (Kubeflow, Airflow, Vertex)
3. Containerize each pipeline step
4. Implement artifact storage
5. Add experiment tracking
6. Configure automated retraining triggers

### 2. Model Deployment
1. Register model in model registry
2. Build serving container
3. Deploy to serving infrastructure
4. Configure autoscaling
5. Implement canary/shadow deployment
6. Set up monitoring and alerts

### 3. Model Monitoring
1. Define key metrics (latency, throughput, accuracy)
2. Implement data drift detection
3. Set up prediction monitoring
4. Create alerting thresholds
5. Build dashboards for visibility
6. Automate retraining triggers

## Best Practices
- Version everything: code, data, models, configs
- Use feature stores for consistency between training and serving
- Implement CI/CD specifically designed for ML workflows
- Monitor data drift and model performance continuously
- Use canary deployments for model rollouts
- Keep training and serving environments consistent

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Manual deployments | Error-prone, slow | Automated ML CI/CD |
| Training-serving skew | Prediction errors | Feature stores |
| No model versioning | Can't reproduce or rollback | Model registry |
| Ignoring data drift | Silent degradation | Continuous monitoring |
| Notebook-to-production | Unmaintainable | Proper pipeline code |
