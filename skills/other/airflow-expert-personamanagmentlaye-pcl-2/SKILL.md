---
name: airflow-expert
version: 1.0.0
description: Expert-level Apache Airflow orchestration, DAGs, operators, sensors, XComs, task dependencies, and scheduling
category: data
author: PCL Team
license: Apache-2.0
tags:
  - airflow
  - orchestration
  - dag
  - workflow
  - scheduling
  - data-pipeline
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
requirements:
  apache-airflow: ">=2.8.0"
---

# Apache Airflow Expert

You are an expert in Apache Airflow with deep knowledge of DAG design, task orchestration, operators, sensors, XComs, dynamic task generation, and production operations. You design and manage complex data pipelines that are reliable, maintainable, and scalable.

## Core Expertise

### DAG Fundamentals

**Basic DAG Structure:**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Default arguments
default_args = {
    'owner': 'data-engineering',
    'depends_on_past': False,
    'email': ['alerts@company.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'execution_timeout': timedelta(hours=2),
}

# Define DAG
dag = DAG(
    dag_id='etl_pipeline',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule='0 2 * * *',  # 2 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'production'],
    doc_md="""
    ## ETL Pipeline

    This pipeline extracts data from source systems,
    transforms it, and loads into the data warehouse.

    ### Schedule
    Runs daily at 2 AM UTC

    ### Owner
    Data Engineering Team
    """
)

# Define tasks
def extract_data(**context):
    """Extract data from source systems"""
    execution_date = context['execution_date']
    print(f"Extracting data for {execution_date}")
    return {'rows_extracted': 10000}

def transform_data(**context):
    """Transform extracted data"""
    ti = context['ti']
    extracted = ti.xcom_pull(task_ids='extract')
    print(f"Transforming {extracted['rows_extracted']} rows")
    return {'rows_transformed': 9950}

def load_data(**context):
    """Load data to warehouse"""
    ti = context['ti']
    transformed = ti.xcom_pull(task_ids='transform')
    print(f"Loading {transformed['rows_transformed']} rows")

# Create tasks
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract_data,
    dag=dag
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform_data,
    dag=dag
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load_data,
    dag=dag
)

# Set dependencies
extract_task >> transform_task >> load_task
```

**TaskFlow API (Recommended):**
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='etl_pipeline_taskflow',
    schedule='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'production']
)
def etl_pipeline():
    """ETL pipeline using TaskFlow API"""

    @task
    def extract() -> dict:
        """Extract data from source"""
        print("Extracting data...")
        return {'rows_extracted': 10000}

    @task
    def transform(data: dict) -> dict:
        """Transform extracted data"""
        print(f"Transforming {data['rows_extracted']} rows")
        return {'rows_transformed': 9950}

    @task
    def load(data: dict) -> None:
        """Load data to warehouse"""
        print(f"Loading {data['rows_transformed']} rows")

    # Define flow (automatic XCom passing)
    extracted_data = extract()
    transformed_data = transform(extracted_data)
    load(transformed_data)

# Instantiate DAG
dag = etl_pipeline()
```

### Task Dependencies and Branching

**Complex Dependencies:**
```python
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator
from datetime import datetime

@dag(
    dag_id='complex_dependencies',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def complex_pipeline():

    start = EmptyOperator(task_id='start')
    end = EmptyOperator(task_id='end', trigger_rule='none_failed')

    @task
    def process_source_1():
        return "source_1_complete"

    @task
    def process_source_2():
        return "source_2_complete"

    @task
    def process_source_3():
        return "source_3_complete"

    @task
    def merge_data(sources: list):
        print(f"Merging data from: {sources}")
        return "merged_complete"

    @task
    def validate_data(merged):
        print(f"Validating: {merged}")
        return "validated"

    @task
    def publish_data(validated):
        print(f"Publishing: {validated}")

    # Parallel processing then merge
    source_1 = process_source_1()
    source_2 = process_source_2()
    source_3 = process_source_3()

    merged = merge_data([source_1, source_2, source_3])
    validated = validate_data(merged)
    published = publish_data(validated)

    # Set dependencies
    start >> [source_1, source_2, source_3]
    published >> end

dag = complex_pipeline()
```

**Branching Logic:**
```python
from airflow.decorators import dag, task
from airflow.operators.python import BranchPythonOperator
from datetime import datetime

@dag(
    dag_id='branching_pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def branching_example():

    @task
    def check_data_quality() -> dict:
        """Check data quality"""
        quality_score = 0.95
        return {'score': quality_score}

    @task.branch
    def decide_path(quality_data: dict) -> str:
        """Branch based on quality score"""
        if quality_data['score'] >= 0.9:
            return 'high_quality_path'
        elif quality_data['score'] >= 0.7:
            return 'medium_quality_path'
        else:
            return 'low_quality_path'

    @task
    def high_quality_path():
        print("Processing high quality data")

    @task
    def medium_quality_path():
        print("Processing medium quality data with validation")

    @task
    def low_quality_path():
        print("Rejecting low quality data")

    @task(trigger_rule='none_failed_min_one_success')
    def finalize():
        print("Finalizing pipeline")

    # Define flow
    quality = check_data_quality()
    branch = decide_path(quality)

    high = high_quality_path()
    medium = medium_quality_path()
    low = low_quality_path()
    final = finalize()

    branch >> [high, medium, low] >> final

dag = branching_example()
```

### Dynamic Task Generation

**Dynamic Tasks with expand():**
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='dynamic_tasks',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def dynamic_pipeline():

    @task
    def get_data_sources() -> list:
        """Return list of data sources to process"""
        return ['source_a', 'source_b', 'source_c', 'source_d']

    @task
    def process_source(source: str) -> dict:
        """Process individual source"""
        print(f"Processing {source}")
        return {'source': source, 'rows': 1000}

    @task
    def aggregate_results(results: list) -> dict:
        """Aggregate all results"""
        total_rows = sum(r['rows'] for r in results)
        return {'total_rows': total_rows, 'source_count': len(results)}

    # Dynamic task expansion
    sources = get_data_sources()
    processed = process_source.expand(source=sources)
    aggregate_results(processed)

dag = dynamic_pipeline()
```

**Dynamic Task Generation (Legacy):**
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def process_file(file_name):
    """Process individual file"""
    print(f"Processing {file_name}")

with DAG(
    dag_id='dynamic_file_processing',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:

    # Generate tasks dynamically
    files = ['file_1.csv', 'file_2.csv', 'file_3.csv']

    for file_name in files:
        task = PythonOperator(
            task_id=f'process_{file_name.replace(".", "_")}',
            python_callable=process_file,
            op_kwargs={'file_name': file_name}
        )
```

### Operators and Sensors

**Common Operators:**
```python
from airflow.decorators import dag
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime

@dag(
    dag_id='operator_examples',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def operator_dag():

    # Bash operator
    bash_task = BashOperator(
        task_id='run_bash_script',
        bash_command='echo "Hello Airflow" && date',
        env={'ENV': 'production'}
    )

    # PostgreSQL operator
    create_table = PostgresOperator(
        task_id='create_table',
        postgres_conn_id='postgres_default',
        sql="""
            CREATE TABLE IF NOT EXISTS daily_metrics (
                date DATE PRIMARY KEY,
                metric_value NUMERIC,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
    )

    insert_data = PostgresOperator(
        task_id='insert_data',
        postgres_conn_id='postgres_default',
        sql="""
            INSERT INTO daily_metrics (date, metric_value)
            VALUES ('{{ ds }}', 42.5)
            ON CONFLICT (date) DO UPDATE
            SET metric_value = EXCLUDED.metric_value
        """
    )

    # HTTP operator
    api_call = SimpleHttpOperator(
        task_id='call_api',
        http_conn_id='api_default',
        endpoint='/api/v1/trigger',
        method='POST',
        data='{"date": "{{ ds }}"}',
        headers={'Content-Type': 'application/json'},
        response_check=lambda response: response.status_code == 200
    )

    bash_task >> create_table >> insert_data >> api_call

dag = operator_dag()
```

**Sensors:**
```python
from airflow.decorators import dag
from airflow.sensors.filesystem import FileSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor
from airflow.sensors.python import PythonSensor
from airflow.sensors.external_task import ExternalTaskSensor
from datetime import datetime, timedelta

@dag(
    dag_id='sensor_examples',
    schedule='@hourly',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def sensor_dag():

    # File sensor
    wait_for_file = FileSensor(
        task_id='wait_for_file',
        filepath='/tmp/data/{{ ds }}/input.csv',
        poke_interval=60,
        timeout=3600,
        mode='poke'  # or 'reschedule'
    )

    # S3 sensor
    wait_for_s3 = S3KeySensor(
        task_id='wait_for_s3',
        bucket_name='my-bucket',
        bucket_key='data/{{ ds }}/input.parquet',
        aws_conn_id='aws_default',
        poke_interval=300,
        timeout=7200
    )

    # Python sensor (custom condition)
    def check_condition(**context):
        """Custom condition to check"""
        from datetime import datetime
        current_hour = datetime.now().hour
        return current_hour >= 9  # Wait until 9 AM

    wait_for_condition = PythonSensor(
        task_id='wait_for_condition',
        python_callable=check_condition,
        poke_interval=300,
        timeout=3600
    )

    # External task sensor (wait for another DAG)
    wait_for_upstream = ExternalTaskSensor(
        task_id='wait_for_upstream',
        external_dag_id='upstream_dag',
        external_task_id='final_task',
        allowed_states=['success'],
        failed_states=['failed', 'skipped'],
        execution_delta=timedelta(hours=1),
        poke_interval=60
    )

    [wait_for_file, wait_for_s3, wait_for_condition, wait_for_upstream]

dag = sensor_dag()
```

### XComs and Task Communication

**XCom Usage:**
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='xcom_example',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def xcom_pipeline():

    @task
    def extract_data() -> dict:
        """Returns data via XCom (automatic)"""
        return {
            'records': 1000,
            'source': 'database',
            'timestamp': '2024-01-15T10:00:00'
        }

    @task
    def validate_data(data: dict) -> bool:
        """Use data from previous task"""
        print(f"Validating {data['records']} records")
        return data['records'] > 0

    @task
    def process_data(data: dict, is_valid: bool):
        """Use multiple XComs"""
        if is_valid:
            print(f"Processing {data['records']} records from {data['source']}")
        else:
            raise ValueError("Invalid data")

    # Manual XCom access
    @task
    def manual_xcom_pull(**context):
        """Manually pull XCom values"""
        ti = context['ti']

        # Pull from specific task
        data = ti.xcom_pull(task_ids='extract_data')

        # Pull from multiple tasks
        values = ti.xcom_pull(task_ids=['extract_data', 'validate_data'])

        # Pull with key
        ti.xcom_push(key='custom_key', value='custom_value')
        custom = ti.xcom_pull(key='custom_key')

        print(f"Data: {data}")
        print(f"Values: {values}")

    # Flow
    data = extract_data()
    is_valid = validate_data(data)
    process_data(data, is_valid)

dag = xcom_pipeline()
```

### Connections and Variables

**Managing Connections:**
```python
from airflow.decorators import dag, task
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from datetime import datetime

@dag(
    dag_id='connections_and_variables',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def connections_dag():

    @task
    def use_connection():
        """Access connection details"""
        # Get connection
        conn = BaseHook.get_connection('postgres_default')

        print(f"Host: {conn.host}")
        print(f"Port: {conn.port}")
        print(f"Schema: {conn.schema}")
        print(f"Login: {conn.login}")
        # Password: conn.password
        # Extra: conn.extra_dejson

    @task
    def use_variables():
        """Access Airflow Variables"""
        # Get variable
        environment = Variable.get("environment")
        api_url = Variable.get("api_url")

        # Get with default
        timeout = Variable.get("timeout", default_var=30)

        # Get JSON variable
        config = Variable.get("config", deserialize_json=True)

        print(f"Environment: {environment}")
        print(f"API URL: {api_url}")
        print(f"Config: {config}")

    use_connection()
    use_variables()

dag = connections_dag()

# Set variables via CLI
# airflow variables set environment production
# airflow variables set config '{"key": "value"}' --json

# Set connection via CLI
# airflow connections add postgres_default \
#   --conn-type postgres \
#   --conn-host localhost \
#   --conn-login airflow \
#   --conn-password airflow \
#   --conn-port 5432 \
#   --conn-schema airflow
```

### Error Handling and Retries

**Retry Logic and Callbacks:**
```python
from airflow.decorators import dag, task
from airflow.exceptions import AirflowFailException
from datetime import datetime, timedelta

def task_failure_callback(context):
    """Called when task fails"""
    task_instance = context['task_instance']
    exception = context['exception']
    print(f"Task {task_instance.task_id} failed: {exception}")
    # Send alert, create ticket, etc.

def task_success_callback(context):
    """Called when task succeeds"""
    print(f"Task succeeded after {context['task_instance'].try_number} tries")

def dag_failure_callback(context):
    """Called when DAG fails"""
    print("DAG failed, sending notifications...")

@dag(
    dag_id='error_handling',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    on_failure_callback=dag_failure_callback,
    default_args={
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'retry_exponential_backoff': True,
        'max_retry_delay': timedelta(hours=1),
        'on_failure_callback': task_failure_callback,
        'on_success_callback': task_success_callback,
        'execution_timeout': timedelta(hours=2)
    }
)
def error_handling_dag():

    @task(retries=5, retry_delay=timedelta(minutes=2))
    def risky_task():
        """Task with custom retry settings"""
        import random
        if random.random() < 0.7:
            raise Exception("Random failure")
        return "success"

    @task
    def task_with_skip(**context):
        """Task that can skip"""
        from airflow.exceptions import AirflowSkipException

        execution_date = context['execution_date']
        if execution_date.weekday() in [5, 6]:  # Weekend
            raise AirflowSkipException("Skipping on weekends")

        return "processed"

    @task
    def cleanup_on_failure(**context):
        """Cleanup task that runs even on failure"""
        print("Running cleanup...")

    risky = risky_task()
    skip = task_with_skip()
    cleanup = cleanup_on_failure()

    [risky, skip] >> cleanup

dag = error_handling_dag()
```

### Production Best Practices

**DAG Configuration:**
```python
from airflow.decorators import dag, task
from airflow.models import Variable
from datetime import datetime, timedelta

@dag(
    dag_id='production_pipeline',
    schedule='0 2 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    max_active_runs=1,
    max_active_tasks=16,
    dagrun_timeout=timedelta(hours=4),
    tags=['production', 'etl', 'critical'],
    default_args={
        'owner': 'data-engineering',
        'depends_on_past': True,
        'wait_for_downstream': False,
        'retries': 3,
        'retry_delay': timedelta(minutes=5),
        'email': ['alerts@company.com'],
        'email_on_failure': True,
        'email_on_retry': False,
        'sla': timedelta(hours=3),
    }
)
def production_dag():

    @task(pool='database_pool', priority_weight=10)
    def extract_from_database():
        """High priority database task"""
        print("Extracting from database...")

    @task(pool='api_pool', priority_weight=5)
    def call_external_api():
        """Lower priority API task"""
        print("Calling external API...")

    @task(
        execution_timeout=timedelta(minutes=30),
        trigger_rule='all_success'
    )
    def transform_data():
        """Transform data with timeout"""
        print("Transforming data...")

    extract_from_database() >> transform_data()
    call_external_api() >> transform_data()

dag = production_dag()
```

**Idempotent DAGs:**
```python
from airflow.decorators import dag, task
from datetime import datetime

@dag(
    dag_id='idempotent_pipeline',
    schedule='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False
)
def idempotent_dag():

    @task
    def extract_data(**context):
        """Extract data for specific date"""
        execution_date = context['ds']  # YYYY-MM-DD
        print(f"Extracting data for {execution_date}")
        # Always extract for execution_date, not "today"
        return {'date': execution_date, 'rows': 1000}

    @task
    def load_data(data: dict):
        """Load data with upsert (idempotent)"""
        # Use MERGE/UPSERT instead of INSERT
        # So rerunning doesn't create duplicates
        sql = f"""
            MERGE INTO target_table t
            USING source_table s
            ON t.date = '{data['date']}' AND t.id = s.id
            WHEN MATCHED THEN UPDATE SET value = s.value
            WHEN NOT MATCHED THEN INSERT VALUES (s.date, s.id, s.value)
        """
        print(f"Loading {data['rows']} rows for {data['date']}")

    data = extract_data()
    load_data(data)

dag = idempotent_dag()
```

## Best Practices

### 1. DAG Design
- Keep DAGs simple and focused on single workflows
- Use TaskFlow API for cleaner code and automatic XCom handling
- Set catchup=False for new DAGs to avoid backfilling
- Use meaningful task_ids and add documentation
- Make DAGs idempotent for safe reruns

### 2. Task Configuration
- Set appropriate retries and retry_delay
- Use execution_timeout to prevent stuck tasks
- Configure proper depends_on_past for sequential processing
- Use pools to limit concurrent tasks
- Set priority_weight for critical tasks

### 3. Performance
- Minimize DAG file size and complexity
- Avoid top-level code that executes on every parse
- Use dynamic task mapping instead of creating many tasks
- Leverage sensors with reschedule mode for long waits
- Use task pools to prevent resource exhaustion

### 4. Production Operations
- Monitor DAG run duration and SLA misses
- Set up alerting for failures
- Use Variables and Connections instead of hardcoded values
- Enable DAG versioning and testing
- Implement proper logging

### 5. Security
- Store credentials in Connections, not code
- Use Secrets Backend (AWS Secrets Manager, Vault)
- Limit access with RBAC
- Audit DAG changes
- Encrypt sensitive XCom data

## Anti-Patterns

### 1. Non-Idempotent DAGs
```python
# Bad: Using current date
@task
def extract():
    today = datetime.now().date()
    return extract_data_for_date(today)

# Good: Using execution date
@task
def extract(**context):
    date = context['ds']
    return extract_data_for_date(date)
```

### 2. Heavy Top-Level Code
```python
# Bad: Expensive operation at top level
expensive_config = fetch_config_from_api()  # Runs on every parse

dag = DAG(...)

# Good: Load config in task
@task
def get_config():
    return fetch_config_from_api()
```

### 3. Not Using Connections
```python
# Bad: Hardcoded credentials
DATABASE_URL = "postgresql://user:pass@host:5432/db"

# Good: Use Airflow Connection
conn = BaseHook.get_connection('postgres_default')
```

### 4. Ignoring Task Failures
```python
# Bad: No retry or alert configuration
@task
def important_task():
    critical_operation()

# Good: Proper error handling
@task(retries=3, on_failure_callback=alert_team)
def important_task():
    critical_operation()
```

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [TaskFlow API](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Airflow Providers](https://airflow.apache.org/docs/apache-airflow-providers/)
- [Astronomer Guides](https://docs.astronomer.io/learn)
- [Airflow GitHub](https://github.com/apache/airflow)
- [Airflow Slack Community](https://apache-airflow-slack.herokuapp.com/)
