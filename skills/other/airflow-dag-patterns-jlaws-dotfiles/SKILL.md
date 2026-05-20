---
name: airflow-dag-patterns
description: Build production Apache Airflow DAGs with best practices for operators, sensors, testing, and deployment. Use when creating data pipelines, orchestrating workflows, or scheduling batch jobs.
---

# Apache Airflow DAG Patterns

## DAG Design Principles

| Principle | Description |
|-----------|-------------|
| **Idempotent** | Running twice produces same result |
| **Atomic** | Tasks succeed or fail completely |
| **Incremental** | Process only new/changed data |
| **Observable** | Logs, metrics, alerts at every step |

## Task Dependencies

```python
task1 >> task2 >> task3           # Linear
task1 >> [task2, task3, task4]    # Fan-out
[task1, task2, task3] >> task4    # Fan-in
```

## Pattern 1: TaskFlow API (Airflow 2.0+)

```python
from datetime import datetime
from airflow.decorators import dag, task

@dag(
    dag_id='taskflow_etl',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'taskflow'],
)
def taskflow_etl():
    @task()
    def extract(source: str) -> dict:
        import pandas as pd
        df = pd.read_csv(f's3://bucket/{source}/{{ ds }}.csv')
        return {'data': df.to_dict(), 'rows': len(df)}

    @task()
    def transform(extracted: dict) -> dict:
        import pandas as pd
        df = pd.DataFrame(extracted['data'])
        df['processed_at'] = datetime.now()
        df = df.dropna()
        return {'data': df.to_dict(), 'rows': len(df)}

    @task()
    def load(transformed: dict, target: str):
        import pandas as pd
        df = pd.DataFrame(transformed['data'])
        df.to_parquet(f's3://bucket/{target}/{{ ds }}.parquet')
        return transformed['rows']

    extracted = extract(source='raw_data')
    transformed = transform(extracted)
    load(transformed, target='processed_data')

taskflow_etl()
```

## Pattern 2: Dynamic DAG Generation

```python
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

PIPELINE_CONFIGS = [
    {'name': 'customers', 'schedule': '@daily', 'source': 's3://raw/customers'},
    {'name': 'orders', 'schedule': '@hourly', 'source': 's3://raw/orders'},
    {'name': 'products', 'schedule': '@weekly', 'source': 's3://raw/products'},
]

def create_dag(config: dict) -> DAG:
    dag = DAG(
        dag_id=f"etl_{config['name']}",
        default_args={'owner': 'data-team', 'retries': 3, 'retry_delay': timedelta(minutes=5)},
        schedule=config['schedule'],
        start_date=datetime(2024, 1, 1),
        catchup=False,
        tags=['etl', 'dynamic', config['name']],
    )
    with dag:
        def extract_fn(source, **context):
            print(f"Extracting from {source} for {context['ds']}")
        def transform_fn(**context):
            print(f"Transforming data for {context['ds']}")
        def load_fn(table_name, **context):
            print(f"Loading to {table_name} for {context['ds']}")

        extract = PythonOperator(task_id='extract', python_callable=extract_fn, op_kwargs={'source': config['source']})
        transform = PythonOperator(task_id='transform', python_callable=transform_fn)
        load = PythonOperator(task_id='load', python_callable=load_fn, op_kwargs={'table_name': config['name']})
        extract >> transform >> load
    return dag

for config in PIPELINE_CONFIGS:
    globals()[f"dag_{config['name']}"] = create_dag(config)
```

## Pattern 3: Branching and Conditional Logic

```python
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

@dag(dag_id='branching_pipeline', schedule='@daily', start_date=datetime(2024, 1, 1), catchup=False)
def branching_pipeline():
    @task()
    def check_data_quality() -> dict:
        return {'score': 0.95, 'rows': 10000}

    def choose_branch(**context) -> str:
        metrics = context['ti'].xcom_pull(task_ids='check_data_quality')
        if metrics['score'] >= 0.9: return 'high_quality_path'
        elif metrics['score'] >= 0.7: return 'medium_quality_path'
        else: return 'low_quality_path'

    quality_check = check_data_quality()
    branch = BranchPythonOperator(task_id='branch', python_callable=choose_branch)
    high_quality = EmptyOperator(task_id='high_quality_path')
    medium_quality = EmptyOperator(task_id='medium_quality_path')
    low_quality = EmptyOperator(task_id='low_quality_path')
    join = EmptyOperator(task_id='join', trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS)
    quality_check >> branch >> [high_quality, medium_quality, low_quality] >> join

branching_pipeline()
```

## Pattern 4: Sensors and External Dependencies

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.sensors.external_task import ExternalTaskSensor

with DAG(dag_id='sensor_example', schedule='@daily', start_date=datetime(2024, 1, 1), catchup=False) as dag:
    wait_for_file = S3KeySensor(
        task_id='wait_for_s3_file',
        bucket_name='data-lake',
        bucket_key='raw/{{ ds }}/data.parquet',
        aws_conn_id='aws_default',
        timeout=60 * 60 * 2,
        poke_interval=60 * 5,
        mode='reschedule',  # Free up worker slot while waiting
    )

    wait_for_upstream = ExternalTaskSensor(
        task_id='wait_for_upstream_dag',
        external_dag_id='upstream_etl',
        external_task_id='final_task',
        execution_date_fn=lambda dt: dt,
        timeout=60 * 60 * 3,
        mode='reschedule',
    )

    @task.sensor(poke_interval=60, timeout=3600, mode='reschedule')
    def wait_for_api() -> PokeReturnValue:
        import requests
        response = requests.get('https://api.example.com/health')
        return PokeReturnValue(is_done=response.status_code == 200, xcom_value=response.json())

    [wait_for_file, wait_for_upstream, wait_for_api()] >> process
```

## Pattern 5: Error Handling and Alerts

```python
def task_failure_callback(context):
    task_instance = context['task_instance']
    message = f"""
    Task Failed! DAG: {task_instance.dag_id} Task: {task_instance.task_id}
    Execution Date: {context['ds']} Error: {context.get('exception')}
    Log URL: {task_instance.log_url}
    """
    # send_slack_alert(message)

with DAG(
    dag_id='error_handling_example',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    default_args={
        'on_failure_callback': task_failure_callback,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
    },
) as dag:
    risky_task = PythonOperator(task_id='risky_task', python_callable=might_fail)
    cleanup_task = PythonOperator(task_id='cleanup', python_callable=cleanup, trigger_rule=TriggerRule.ALL_DONE)
    success_notification = PythonOperator(task_id='notify_success', python_callable=notify_success, trigger_rule=TriggerRule.ALL_SUCCESS)
    risky_task >> [cleanup_task, success_notification]
```

## Pattern 6: Testing DAGs

```python
import pytest
from airflow.models import DagBag

@pytest.fixture
def dagbag():
    return DagBag(dag_folder='dags/', include_examples=False)

def test_dag_loaded(dagbag):
    assert len(dagbag.import_errors) == 0, f"DAG import errors: {dagbag.import_errors}"

def test_dag_structure(dagbag):
    dag = dagbag.get_dag('example_etl')
    assert dag is not None
    assert len(dag.tasks) == 3

def test_task_dependencies(dagbag):
    dag = dagbag.get_dag('example_etl')
    extract_task = dag.get_task('extract')
    assert 'start' in [t.task_id for t in extract_task.upstream_list]

def test_dag_integrity(dagbag):
    for dag_id, dag in dagbag.dags.items():
        assert dag.test_cycle() is None, f"Cycle detected in {dag_id}"
```

## Project Structure

```
airflow/
├── dags/
│   ├── common/           # Custom operators, sensors, callbacks
│   ├── etl/
│   └── ml/
├── plugins/
├── tests/
├── docker-compose.yml
└── requirements.txt
```

## Do's and Don'ts

- **Use TaskFlow API** -- cleaner code, automatic XCom
- **Set timeouts** -- prevent zombie tasks
- **Use `mode='reschedule'`** for sensors -- free up workers
- **Idempotent tasks** -- safe to retry
- **Don't use `depends_on_past=True`** -- creates bottlenecks
- **Don't hardcode dates** -- use `{{ ds }}` macros
- **Don't put heavy logic in DAG file** -- import from modules
