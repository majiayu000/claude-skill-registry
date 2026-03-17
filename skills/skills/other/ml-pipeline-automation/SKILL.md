---
name: ml-pipeline-automation
description: Automate ML workflows with Airflow, Kubeflow, MLflow. Use for reproducible pipelines, retraining schedules, MLOps, or encountering task failures, dependency errors, experiment tracking issues.
keywords: ML pipeline, Airflow, Kubeflow, MLflow, MLOps, workflow orchestration, data pipeline, model training automation, experiment tracking, model registry, Airflow DAG, task dependencies, pipeline monitoring, data quality, drift detection, hyperparameter tuning, model versioning, artifact management, Kubeflow Pipelines, pipeline automation, retries, sensors
license: MIT
---

# ML Pipeline Automation

Orchestrate end-to-end machine learning workflows from data ingestion to production deployment with production-tested Airflow, Kubeflow, and MLflow patterns.

## When to Use This Skill

Load this skill when:
- **Building ML Pipelines**: Orchestrating data → train → deploy workflows
- **Scheduling Retraining**: Setting up automated model retraining schedules
- **Experiment Tracking**: Tracking experiments, parameters, metrics across runs
- **MLOps Implementation**: Building reproducible, monitored ML infrastructure
- **Workflow Orchestration**: Managing complex multi-step ML workflows
- **Model Registry**: Managing model versions and deployment lifecycle

## Quick Start: ML Pipeline in 5 Steps

```bash
# 1. Install Airflow and MLflow (check for latest versions at time of use)
pip install apache-airflow==3.1.5 mlflow==3.7.0

# Note: These versions are current as of December 2025
# Check PyPI for latest stable releases: https://pypi.org/project/apache-airflow/

# 2. Initialize Airflow database
airflow db init

# 3. Create DAG file: dags/ml_training_pipeline.py
cat > dags/ml_training_pipeline.py << 'EOF'
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1)
)

def train_model(**context):
    import mlflow
    import mlflow.sklearn
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import load_iris
    from sklearn.model_selection import train_test_split

    X, y = load_iris(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    mlflow.set_tracking_uri('http://localhost:5000')
    mlflow.set_experiment('iris-training')

    with mlflow.start_run():
        model = RandomForestClassifier(n_estimators=100)
        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)
        mlflow.log_metric('accuracy', accuracy)
        mlflow.sklearn.log_model(model, 'model')

train = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)
EOF

# 4. Start Airflow scheduler and webserver
airflow scheduler &
airflow webserver --port 8080 &

# 5. Trigger pipeline
airflow dags trigger ml_training_pipeline

# Access UI: http://localhost:8080
```

**Result**: Working ML pipeline with experiment tracking in under 5 minutes.

## Core Concepts

### Pipeline Stages

1. **Data Collection** → Fetch raw data from sources
2. **Data Validation** → Check schema, quality, distributions
3. **Feature Engineering** → Transform raw data to features
4. **Model Training** → Train with hyperparameter tuning
5. **Model Evaluation** → Validate performance on test set
6. **Model Deployment** → Push to production if metrics pass
7. **Monitoring** → Track drift, performance in production

### Orchestration Tools Comparison

| Tool | Best For | Strengths |
|------|----------|-----------|
| **Airflow** | General ML workflows | Mature, flexible, Python-native |
| **Kubeflow** | Kubernetes-native ML | Container-based, scalable |
| **MLflow** | Experiment tracking | Model registry, versioning |
| **Prefect** | Modern Python workflows | Dynamic DAGs, native caching |
| **Dagster** | Asset-oriented pipelines | Data-aware, testable |

## Basic Airflow DAG

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'ml_training_pipeline',
    default_args=default_args,
    description='End-to-end ML training pipeline',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False
)

def validate_data(**context):
    """Validate input data quality."""
    import pandas as pd

    data_path = "/data/raw/latest.csv"
    df = pd.read_csv(data_path)

    # Validation checks
    assert len(df) > 1000, f"Insufficient data: {len(df)} rows"
    assert df.isnull().sum().sum() < len(df) * 0.1, "Too many nulls"

    context['ti'].xcom_push(key='data_path', value=data_path)
    logger.info(f"Data validation passed: {len(df)} rows")

def train_model(**context):
    """Train ML model with MLflow tracking."""
    import mlflow
    import mlflow.sklearn
    from sklearn.ensemble import RandomForestClassifier

    data_path = context['ti'].xcom_pull(key='data_path', task_ids='validate_data')

    mlflow.set_tracking_uri('http://mlflow:5000')
    mlflow.set_experiment('production-training')

    with mlflow.start_run():
        # Training logic here
        model = RandomForestClassifier(n_estimators=100)
        # model.fit(X, y) ...

        mlflow.log_param('n_estimators', 100)
        mlflow.sklearn.log_model(model, 'model')

validate = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    dag=dag
)

train = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag
)

validate >> train
```

## Known Issues Prevention

### 1. Task Failures Without Alerts
**Problem**: Pipeline fails silently, no one notices until users complain.

**Solution**: Configure email/Slack alerts on failure:
```python
default_args = {
    'email': ['ml-team@example.com'],
    'email_on_failure': True,
    'email_on_retry': False
}

def on_failure_callback(context):
    """Send Slack alert on failure."""
    from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator

    slack_msg = f"""
    :red_circle: Task Failed: {context['task_instance'].task_id}
    DAG: {context['task_instance'].dag_id}
    Execution Date: {context['ds']}
    Error: {context.get('exception')}
    """

    SlackWebhookOperator(
        task_id='slack_alert',
        slack_webhook_conn_id='slack_webhook',
        message=slack_msg
    ).execute(context)

task = PythonOperator(
    task_id='critical_task',
    python_callable=my_function,
    on_failure_callback=on_failure_callback,
    dag=dag
)
```

### 2. Missing XCom Data Between Tasks
**Problem**: Task expects XCom value from previous task, gets None, crashes.

**Solution**: Always validate XCom pulls:
```python
def process_data(**context):
    data_path = context['ti'].xcom_pull(
        key='data_path',
        task_ids='upstream_task'
    )

    if data_path is None:
        raise ValueError("No data_path from upstream_task - check XCom push")

    # Process data...
```

### 3. DAG Not Appearing in UI
**Problem**: DAG file exists in `dags/` but doesn't show in Airflow UI.

**Solution**: Check DAG parsing errors:
```bash
# Check for syntax errors
python dags/my_dag.py

# View DAG import errors in UI
# Navigate to: Browse → DAG Import Errors

# Common fixes:
# 1. Ensure DAG object is defined in file
# 2. Check for circular imports
# 3. Verify all dependencies installed
# 4. Fix syntax errors
```

### 4. Hardcoded Paths Break in Production
**Problem**: Paths like `/Users/myname/data/` work locally, fail in production.

**Solution**: Use Airflow Variables or environment variables:
```python
from airflow.models import Variable

def load_data(**context):
    # ❌ Bad: Hardcoded path
    # data_path = "/Users/myname/data/train.csv"

    # ✅ Good: Use Airflow Variable
    data_dir = Variable.get("data_directory", "/data")
    data_path = f"{data_dir}/train.csv"

    # Or use environment variable
    import os
    data_path = os.getenv("DATA_PATH", "/data/train.csv")
```

### 5. Stuck Tasks Consume Resources
**Problem**: Task hangs indefinitely, blocks worker slot, wastes resources.

**Solution**: Set execution_timeout on tasks:
```python
from datetime import timedelta

task = PythonOperator(
    task_id='long_running_task',
    python_callable=my_function,
    execution_timeout=timedelta(hours=2),  # Kill after 2 hours
    dag=dag
)
```

### 6. No Data Validation = Bad Model Training
**Problem**: Train on corrupted/incomplete data, model performs poorly in production.

**Solution**: Add data quality validation tasks:
```python
def validate_data_quality(**context):
    """Comprehensive data validation."""
    import pandas as pd

    df = pd.read_csv(data_path)

    # Schema validation
    required_cols = ['user_id', 'timestamp', 'feature_a', 'target']
    missing_cols = set(required_cols) - set(df.columns)
    if missing_cols:
        raise ValueError(f"Missing columns: {missing_cols}")

    # Statistical validation
    if df['target'].isnull().sum() > 0:
        raise ValueError("Target column contains nulls")

    if len(df) < 1000:
        raise ValueError(f"Insufficient data: {len(df)} rows")

    logger.info("✅ Data quality validation passed")
```

### 7. Untracked Experiments = Lost Knowledge
**Problem**: Can't reproduce results, don't know which hyperparameters worked.

**Solution**: Use MLflow for all experiments:
```python
import mlflow

mlflow.set_tracking_uri('http://mlflow:5000')
mlflow.set_experiment('model-experiments')

with mlflow.start_run(run_name='rf_v1'):
    # Log ALL hyperparameters
    mlflow.log_params({
        'model_type': 'random_forest',
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    })

    # Log ALL metrics
    mlflow.log_metrics({
        'train_accuracy': 0.95,
        'test_accuracy': 0.87,
        'f1_score': 0.89
    })

    # Log model
    mlflow.sklearn.log_model(model, 'model')
```

## When to Load References

Load reference files for detailed production implementations:

- **Airflow DAG Patterns**: Load `references/airflow-patterns.md` when building complex DAGs with error handling, dynamic generation, sensors, task groups, or retry logic. Contains complete production DAG examples.

- **Kubeflow & MLflow Integration**: Load `references/kubeflow-mlflow.md` when using Kubeflow Pipelines for container-native orchestration, integrating MLflow tracking, building KFP components, or managing model registry.

- **Pipeline Monitoring**: Load `references/pipeline-monitoring.md` when implementing data quality checks, drift detection, alert configuration, or pipeline health monitoring with Prometheus.

## Best Practices

1. **Idempotent Tasks**: Tasks should produce same result when re-run
2. **Atomic Operations**: Each task does one thing well
3. **Version Everything**: Data, code, models, dependencies
4. **Comprehensive Logging**: Log all important events with context
5. **Error Handling**: Fail fast with clear error messages
6. **Monitoring**: Track pipeline health, data quality, model drift
7. **Testing**: Test tasks independently before integrating
8. **Documentation**: Document DAG purpose, task dependencies

## Common Patterns

### Conditional Execution
```python
from airflow.operators.python import BranchPythonOperator

def choose_branch(**context):
    accuracy = context['ti'].xcom_pull(key='accuracy', task_ids='evaluate')

    if accuracy > 0.9:
        return 'deploy_to_production'
    else:
        return 'retrain_with_more_data'

branch = BranchPythonOperator(
    task_id='check_accuracy',
    python_callable=choose_branch,
    dag=dag
)

train >> evaluate >> branch >> [deploy, retrain]
```

### Parallel Training
```python
from airflow.utils.task_group import TaskGroup

with TaskGroup('train_models', dag=dag) as train_group:
    train_rf = PythonOperator(task_id='train_rf', ...)
    train_lr = PythonOperator(task_id='train_lr', ...)
    train_xgb = PythonOperator(task_id='train_xgb', ...)

# All models train in parallel
preprocess >> train_group >> select_best
```

### Waiting for Data
```python
from airflow.sensors.filesystem import FileSensor

wait_for_data = FileSensor(
    task_id='wait_for_data',
    filepath='/data/input/{{ ds }}.csv',
    poke_interval=60,  # Check every 60 seconds
    timeout=3600,  # Timeout after 1 hour
    mode='reschedule',  # Don't block worker
    dag=dag
)

wait_for_data >> process_data
```
