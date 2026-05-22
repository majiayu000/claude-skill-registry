---
name: mlops-advanced
description: "Implement advanced MLOps practices for production ML systems. Use for: building CI/CD pipelines for ML models, implementing continuous training and monitoring, managing model registries and versioning, deploying with blue-green and canary strategies, monitoring model drift and performance degradation, orchestrating ML workflows with Kubeflow/Airflow, implementing feature stores, ensuring model governance and compliance, and scaling ML infrastructure with Kubernetes."
---

# MLOps Advanced

Implement production-grade MLOps practices for scalable, reliable machine learning systems.

## Overview

MLOps (Machine Learning Operations) extends DevOps principles to machine learning, automating and streamlining the entire ML lifecycle from development to deployment and monitoring. Advanced MLOps addresses unique ML challenges including data dependencies, model versioning, continuous training, performance monitoring, and infrastructure scaling. It encompasses CI/CD for ML, automated retraining, drift detection, and governance frameworks.

## MLOps Maturity Levels

**Level 0 - Manual Process:**
- Manual data preparation and training
- Notebook-driven development
- Manual deployment
- No CI/CD or monitoring

**Level 1 - ML Pipeline Automation:**
- Automated training pipelines
- Continuous training (CT)
- Model and data validation
- Automated deployment of prediction service

**Level 2 - CI/CD Pipeline Automation:**
- Full CI/CD system for ML
- Automated testing (data, model, infrastructure)
- Rapid experimentation and deployment
- Comprehensive monitoring and logging

## CI/CD for Machine Learning

### Continuous Integration Components

```yaml
# .github/workflows/ml-ci.yml
name: ML CI Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Data Validation
        run: |
          python scripts/validate_data.py
          python scripts/check_data_drift.py
      
      - name: Feature Validation
        run: python scripts/validate_features.py
      
      - name: Model Training
        run: python scripts/train_model.py
      
      - name: Model Evaluation
        run: |
          python scripts/evaluate_model.py
          python scripts/check_fairness.py
      
      - name: Unit Tests
        run: pytest tests/
      
      - name: Integration Tests
        run: pytest tests/integration/
```

### Continuous Deployment

```python
# deploy_model.py
import mlflow
from kubernetes import client, config

def deploy_model(model_uri, deployment_name, namespace='production'):
    # Load model from registry
    model = mlflow.pyfunc.load_model(model_uri)
    
    # Create deployment configuration
    deployment = create_k8s_deployment(
        name=deployment_name,
        image=f'ml-model-server:{model.metadata.run_id}',
        replicas=3,
        resources={'cpu': '2', 'memory': '4Gi'}
    )
    
    # Deploy to Kubernetes
    config.load_kube_config()
    apps_v1 = client.AppsV1Api()
    apps_v1.create_namespaced_deployment(namespace, deployment)
    
    # Create service
    service = create_k8s_service(deployment_name)
    core_v1 = client.CoreV1Api()
    core_v1.create_namespaced_service(namespace, service)
```

## Model Registry and Versioning

### MLflow Model Registry

```python
import mlflow
from mlflow.tracking import MlflowClient

# Register model
mlflow.set_tracking_uri("http://mlflow-server:5000")
client = MlflowClient()

# Log and register model
with mlflow.start_run():
    mlflow.log_params(params)
    mlflow.log_metrics(metrics)
    mlflow.sklearn.log_model(model, "model")
    
    # Register to model registry
    model_uri = f"runs:/{mlflow.active_run().info.run_id}/model"
    mlflow.register_model(model_uri, "my_model")

# Transition model stage
client.transition_model_version_stage(
    name="my_model",
    version=1,
    stage="Production"
)

# Load production model
model = mlflow.pyfunc.load_model("models:/my_model/Production")
```

### Model Versioning Strategy

```python
class ModelVersion:
    def __init__(self, model_name, version, metadata):
        self.model_name = model_name
        self.version = version
        self.metadata = {
            'training_date': metadata['date'],
            'dataset_version': metadata['data_version'],
            'metrics': metadata['metrics'],
            'hyperparameters': metadata['params'],
            'framework': metadata['framework'],
            'dependencies': metadata['dependencies']
        }
    
    def compare_with(self, other_version):
        return {
            'accuracy_diff': self.metadata['metrics']['accuracy'] - 
                           other_version.metadata['metrics']['accuracy'],
            'latency_diff': self.metadata['metrics']['latency'] - 
                          other_version.metadata['metrics']['latency']
        }
```

## Deployment Strategies

### Blue-Green Deployment

```python
def blue_green_deployment(new_model_uri, service_name):
    # Deploy green (new) version
    deploy_model(new_model_uri, f"{service_name}-green")
    
    # Run smoke tests
    if not run_smoke_tests(f"{service_name}-green"):
        rollback(f"{service_name}-green")
        return False
    
    # Switch traffic from blue to green
    update_service_selector(service_name, version='green')
    
    # Monitor for issues
    if monitor_deployment(service_name, duration=300):
        # Success - remove blue deployment
        delete_deployment(f"{service_name}-blue")
        return True
    else:
        # Rollback to blue
        update_service_selector(service_name, version='blue')
        delete_deployment(f"{service_name}-green")
        return False
```

### Canary Deployment

```python
def canary_deployment(new_model_uri, service_name, canary_percentage=10):
    # Deploy canary version
    deploy_model(new_model_uri, f"{service_name}-canary", replicas=1)
    
    # Route small percentage of traffic to canary
    update_traffic_split(service_name, {
        'stable': 100 - canary_percentage,
        'canary': canary_percentage
    })
    
    # Monitor canary metrics
    canary_metrics = monitor_canary(f"{service_name}-canary", duration=600)
    stable_metrics = monitor_canary(f"{service_name}-stable", duration=600)
    
    if canary_metrics['error_rate'] <= stable_metrics['error_rate'] * 1.1:
        # Gradually increase canary traffic
        for percentage in [25, 50, 75, 100]:
            update_traffic_split(service_name, {
                'stable': 100 - percentage,
                'canary': percentage
            })
            time.sleep(300)
        
        # Replace stable with canary
        delete_deployment(f"{service_name}-stable")
        rename_deployment(f"{service_name}-canary", f"{service_name}-stable")
        return True
    else:
        # Rollback
        delete_deployment(f"{service_name}-canary")
        return False
```

## Continuous Monitoring

### Model Performance Monitoring

```python
import prometheus_client as prom

# Define metrics
prediction_latency = prom.Histogram('model_prediction_latency_seconds', 
                                    'Model prediction latency')
prediction_counter = prom.Counter('model_predictions_total', 
                                 'Total predictions', ['model_version'])
error_counter = prom.Counter('model_errors_total', 
                            'Total errors', ['error_type'])

class MonitoredModel:
    def __init__(self, model, version):
        self.model = model
        self.version = version
    
    @prediction_latency.time()
    def predict(self, features):
        try:
            prediction = self.model.predict(features)
            prediction_counter.labels(model_version=self.version).inc()
            return prediction
        except Exception as e:
            error_counter.labels(error_type=type(e).__name__).inc()
            raise
```

### Data Drift Detection

```python
from scipy.stats import ks_2samp
import numpy as np

class DriftDetector:
    def __init__(self, reference_data, threshold=0.05):
        self.reference_data = reference_data
        self.threshold = threshold
    
    def detect_drift(self, current_data):
        drift_detected = {}
        
        for feature in self.reference_data.columns:
            # Kolmogorov-Smirnov test
            statistic, p_value = ks_2samp(
                self.reference_data[feature],
                current_data[feature]
            )
            
            drift_detected[feature] = {
                'drift': p_value < self.threshold,
                'p_value': p_value,
                'statistic': statistic
            }
        
        return drift_detected
    
    def calculate_psi(self, reference, current, bins=10):
        # Population Stability Index
        ref_hist, bin_edges = np.histogram(reference, bins=bins)
        cur_hist, _ = np.histogram(current, bins=bin_edges)
        
        ref_pct = ref_hist / len(reference)
        cur_pct = cur_hist / len(current)
        
        psi = np.sum((cur_pct - ref_pct) * np.log(cur_pct / (ref_pct + 1e-10)))
        return psi
```

### Model Drift Detection

```python
class ModelDriftDetector:
    def __init__(self, baseline_metrics):
        self.baseline_metrics = baseline_metrics
    
    def detect_performance_drift(self, current_metrics):
        drift_alerts = []
        
        for metric, baseline_value in self.baseline_metrics.items():
            current_value = current_metrics[metric]
            drift_percentage = abs(current_value - baseline_value) / baseline_value * 100
            
            if drift_percentage > 10:  # 10% threshold
                drift_alerts.append({
                    'metric': metric,
                    'baseline': baseline_value,
                    'current': current_value,
                    'drift_percentage': drift_percentage
                })
        
        return drift_alerts
```

## Feature Store

```python
from feast import FeatureStore, Entity, FeatureView, Field
from feast.types import Float32, Int64
from datetime import timedelta

# Define entity
user = Entity(name="user", join_keys=["user_id"])

# Define feature view
user_features = FeatureView(
    name="user_features",
    entities=[user],
    ttl=timedelta(days=1),
    schema=[
        Field(name="age", dtype=Int64),
        Field(name="avg_purchase", dtype=Float32),
        Field(name="total_purchases", dtype=Int64)
    ],
    source=parquet_source
)

# Initialize feature store
store = FeatureStore(repo_path=".")

# Get online features
features = store.get_online_features(
    features=["user_features:age", "user_features:avg_purchase"],
    entity_rows=[{"user_id": 123}, {"user_id": 456}]
).to_dict()

# Get historical features for training
training_data = store.get_historical_features(
    entity_df=entity_df,
    features=["user_features:age", "user_features:avg_purchase"]
).to_df()
```

## ML Pipeline Orchestration

### Kubeflow Pipeline

```python
import kfp
from kfp import dsl

@dsl.component
def preprocess_data(input_path: str, output_path: str):
    # Data preprocessing logic
    pass

@dsl.component
def train_model(data_path: str, model_path: str, params: dict):
    # Model training logic
    pass

@dsl.component
def evaluate_model(model_path: str, test_data_path: str) -> dict:
    # Model evaluation logic
    pass

@dsl.pipeline(name='ML Training Pipeline')
def ml_pipeline(input_data: str, model_output: str):
    preprocess_task = preprocess_data(input_path=input_data, output_path='/data/processed')
    
    train_task = train_model(
        data_path=preprocess_task.outputs['output_path'],
        model_path=model_output,
        params={'learning_rate': 0.001, 'epochs': 10}
    )
    
    evaluate_task = evaluate_model(
        model_path=train_task.outputs['model_path'],
        test_data_path='/data/test'
    )
    
    with dsl.Condition(evaluate_task.outputs['accuracy'] > 0.9):
        deploy_model(model_path=train_task.outputs['model_path'])

# Compile and run
kfp.compiler.Compiler().compile(ml_pipeline, 'pipeline.yaml')
```

## Model Governance

```python
class ModelGovernance:
    def __init__(self):
        self.approval_required = True
        self.compliance_checks = []
    
    def register_compliance_check(self, check_func):
        self.compliance_checks.append(check_func)
    
    def validate_model(self, model, metadata):
        results = {
            'fairness': self.check_fairness(model, metadata),
            'explainability': self.check_explainability(model),
            'performance': self.check_performance(metadata),
            'compliance': all(check(model, metadata) for check in self.compliance_checks)
        }
        
        return all(results.values()), results
    
    def check_fairness(self, model, metadata):
        # Check for bias across protected attributes
        fairness_metrics = metadata.get('fairness_metrics', {})
        return all(metric < 0.1 for metric in fairness_metrics.values())
    
    def check_explainability(self, model):
        # Ensure model has explanation capabilities
        return hasattr(model, 'explain') or hasattr(model, 'feature_importances_')
```

## Best Practices

**Pipeline Design:**
- Modularize components for reusability
- Implement idempotent operations
- Use containerization for reproducibility
- Version all artifacts (data, code, models)

**Monitoring:**
- Track both technical and business metrics
- Set up automated alerts for drift
- Monitor model latency and throughput
- Log predictions for debugging

**Deployment:**
- Use gradual rollout strategies
- Implement automated rollback
- Maintain model lineage
- Document deployment procedures

**Governance:**
- Establish approval workflows
- Implement audit logging
- Ensure regulatory compliance
- Document model decisions

## Tools and Platforms

**Experiment Tracking:** MLflow, Weights & Biases, Neptune.ai
**Model Registry:** MLflow, Vertex AI, SageMaker
**Pipeline Orchestration:** Kubeflow, Airflow, Prefect, Metaflow
**Feature Stores:** Feast, Tecton, Hopsworks
**Monitoring:** Prometheus, Grafana, Evidently, WhyLabs
**Deployment:** Kubernetes, Docker, TensorFlow Serving, TorchServe
**Cloud Platforms:** AWS SageMaker, Google Vertex AI, Azure ML

## Learning Path

1. **Foundations**: CI/CD basics, containerization, version control
2. **ML Pipelines**: Experiment tracking, model registry, orchestration
3. **Deployment**: Kubernetes, serving infrastructure, scaling
4. **Monitoring**: Drift detection, performance tracking, alerting
5. **Governance**: Compliance, auditing, model documentation

See `references/` for pipeline templates, monitoring dashboards, and deployment configurations.
