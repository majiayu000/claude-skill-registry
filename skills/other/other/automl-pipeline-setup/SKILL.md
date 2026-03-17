---
name: automl-pipeline-setup
description: Эксперт AutoML. Используй для automated machine learning, hyperparameter tuning и model selection.
---

# AutoML Pipeline Setup Expert

Эксперт по проектированию и реализации автоматизированных систем машинного обучения.

## Архитектура пайплайна

### Модульные компоненты
```
Data Ingestion → Validation → Feature Engineering → Model Training → Evaluation → Deployment
```

### Конфигурация через YAML
```yaml
pipeline:
  name: customer_churn_prediction
  version: "1.0"

data:
  source: "s3://bucket/data.parquet"
  validation:
    null_threshold: 0.1
    duplicate_check: true

features:
  numerical:
    - age
    - tenure
    - monthly_charges
  categorical:
    - contract_type
    - payment_method
  target: churn

automl:
  framework: h2o
  max_runtime_secs: 3600
  max_models: 20
  stopping_metric: AUC
  sort_metric: AUC

deployment:
  platform: mlflow
  model_registry: true
```

## Data Validation с Great Expectations

```python
import great_expectations as gx

def validate_data(df, expectation_suite_name="default"):
    context = gx.get_context()

    # Создание expectation suite
    suite = context.add_expectation_suite(expectation_suite_name)

    # Определение expectations
    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=expectation_suite_name
    )

    # Проверки качества данных
    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_be_between("age", min_value=18, max_value=100)
    validator.expect_column_values_to_be_in_set(
        "contract_type",
        ["month-to-month", "one_year", "two_year"]
    )

    # Валидация
    results = validator.validate()
    return results.success
```

## Feature Engineering Pipeline

```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from feature_engine.creation import CyclicalFeatures
from feature_engine.selection import DropCorrelatedFeatures

def create_feature_pipeline(numerical_cols, categorical_cols):
    numerical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    preprocessor = ColumnTransformer([
        ('num', numerical_transformer, numerical_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

    feature_pipeline = Pipeline([
        ('preprocessor', preprocessor),
        ('drop_correlated', DropCorrelatedFeatures(threshold=0.95))
    ])

    return feature_pipeline
```

## H2O AutoML

```python
import h2o
from h2o.automl import H2OAutoML

def train_automl_model(train_df, target_col, config):
    h2o.init()

    # Конвертация в H2O Frame
    h2o_train = h2o.H2OFrame(train_df)

    # Определение типов колонок
    h2o_train[target_col] = h2o_train[target_col].asfactor()

    # Предикторы
    predictors = [col for col in h2o_train.columns if col != target_col]

    # AutoML
    aml = H2OAutoML(
        max_runtime_secs=config.get('max_runtime_secs', 3600),
        max_models=config.get('max_models', 20),
        stopping_metric=config.get('stopping_metric', 'AUC'),
        sort_metric=config.get('sort_metric', 'AUC'),
        seed=42,
        exclude_algos=['DeepLearning'],  # Опционально исключить алгоритмы
        nfolds=5
    )

    aml.train(
        x=predictors,
        y=target_col,
        training_frame=h2o_train
    )

    # Лидерборд
    leaderboard = aml.leaderboard.as_data_frame()
    print(leaderboard)

    return aml.leader
```

## MLflow Experiment Tracking

```python
import mlflow
from mlflow.tracking import MlflowClient

class ExperimentTracker:
    def __init__(self, experiment_name):
        mlflow.set_experiment(experiment_name)
        self.client = MlflowClient()

    def log_automl_run(self, model, metrics, params, artifacts_path=None):
        with mlflow.start_run():
            # Логирование параметров
            for key, value in params.items():
                mlflow.log_param(key, value)

            # Логирование метрик
            for key, value in metrics.items():
                mlflow.log_metric(key, value)

            # Логирование модели
            mlflow.h2o.log_model(model, "model")

            # Логирование артефактов
            if artifacts_path:
                mlflow.log_artifacts(artifacts_path)

            run_id = mlflow.active_run().info.run_id
            return run_id

    def register_best_model(self, run_id, model_name):
        model_uri = f"runs:/{run_id}/model"
        mlflow.register_model(model_uri, model_name)
```

## Optuna для Hyperparameter Tuning

```python
import optuna
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

def objective(trial, X, y):
    params = {
        'n_estimators': trial.suggest_int('n_estimators', 50, 500),
        'max_depth': trial.suggest_int('max_depth', 3, 20),
        'min_samples_split': trial.suggest_int('min_samples_split', 2, 20),
        'min_samples_leaf': trial.suggest_int('min_samples_leaf', 1, 10),
        'max_features': trial.suggest_categorical('max_features', ['sqrt', 'log2', None])
    }

    model = RandomForestClassifier(**params, random_state=42, n_jobs=-1)
    scores = cross_val_score(model, X, y, cv=5, scoring='roc_auc')

    return scores.mean()

def run_optimization(X, y, n_trials=100):
    study = optuna.create_study(direction='maximize')
    study.optimize(lambda trial: objective(trial, X, y), n_trials=n_trials)

    print(f"Best trial: {study.best_trial.value}")
    print(f"Best params: {study.best_params}")

    return study.best_params
```

## Airflow DAG для оркестрации

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG(
    'automl_pipeline',
    default_args=default_args,
    description='AutoML Training Pipeline',
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)

validate_data_task = PythonOperator(
    task_id='validate_data',
    python_callable=validate_data,
    dag=dag
)

feature_engineering_task = PythonOperator(
    task_id='feature_engineering',
    python_callable=run_feature_engineering,
    dag=dag
)

automl_training_task = PythonOperator(
    task_id='automl_training',
    python_callable=train_automl_model,
    dag=dag
)

model_validation_task = PythonOperator(
    task_id='model_validation',
    python_callable=validate_model,
    dag=dag
)

validate_data_task >> feature_engineering_task >> automl_training_task >> model_validation_task
```

## Рекомендации по фреймворкам

| Сценарий | Рекомендация |
|----------|--------------|
| Enterprise, табличные данные | H2O.ai |
| Cloud-native | Google Vertex AI, AWS SageMaker |
| Быстрое прототипирование | AutoGluon, FLAML |
| Кастомизация | MLflow + Optuna |
| Deep Learning | AutoKeras, Neural Architecture Search |

## Лучшие практики

1. **Data sampling** — для ускорения экспериментов
2. **Early stopping** — прекращение неперспективных моделей
3. **Resource management** — лимиты памяти и CPU
4. **Distributed training** — Ray Tune, Dask для масштабирования
5. **Model versioning** — отслеживание всех экспериментов
6. **Reproducibility** — фиксация random seeds
