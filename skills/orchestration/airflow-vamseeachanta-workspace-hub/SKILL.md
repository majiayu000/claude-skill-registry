---
name: airflow
version: 1.0.0
description: Python DAG workflow orchestration using Apache Airflow for data pipelines, ETL processes, and scheduled task automation
author: workspace-hub
category: automation
type: skill
capabilities:
  - dag_authoring
  - task_orchestration
  - scheduling
  - sensors
  - operators
  - hooks
  - xcoms
  - variables
  - connections
  - kubernetes_deployment
  - docker_deployment
tools:
  - airflow-cli
  - docker
  - kubernetes
  - helm
tags: [airflow, dag, workflow, orchestration, etl, data-pipeline, scheduling, python, automation]
platforms: [linux, macos, docker, kubernetes]
related_skills:
  - yaml-configuration
  - python-scientific-computing
  - pandas-data-processing
---

# Apache Airflow Skill

Master Apache Airflow for workflow orchestration, data pipeline automation, and scheduled task management. This skill covers DAG authoring, operators, sensors, hooks, XComs, variables, connections, and deployment patterns.

## When to Use This Skill

### USE when:
- Building complex data pipelines with task dependencies
- Orchestrating ETL/ELT workflows
- Scheduling recurring batch jobs
- Managing workflows with retries and error handling
- Coordinating tasks across multiple systems
- Need visibility into workflow execution history
- Requiring audit trails and lineage tracking
- Building ML pipeline orchestration

### DON'T USE when:
- Real-time streaming data (use Kafka, Flink)
- Simple cron jobs (use systemd timers, crontab)
- CI/CD pipelines (use GitHub Actions, Jenkins)
- Low-latency requirements (Airflow has scheduler overhead)
- Simple single-task automation (overkill)
- Need visual workflow design for non-developers (use n8n)

## Prerequisites

### Installation Options

**Option 1: pip (Development)**
```bash
# Create virtual environment
python -m venv airflow-env
source airflow-env/bin/activate

# Set Airflow home
export AIRFLOW_HOME=~/airflow

# Install Airflow with constraints
AIRFLOW_VERSION=2.8.1
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Initialize database
airflow db init

# Create admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin

# Start services
airflow webserver --port 8080 &
airflow scheduler &
```

**Option 2: Docker Compose (Recommended)**
```bash
# Download official docker-compose
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.8.1/docker-compose.yaml'

# Create required directories
mkdir -p ./dags ./logs ./plugins ./config
echo -e "AIRFLOW_UID=$(id -u)" > .env

# Initialize
docker compose up airflow-init

# Start services
docker compose up -d

# Access UI at http://localhost:8080 (airflow/airflow)
```

**Option 3: Kubernetes with Helm**
```bash
# Add Airflow Helm repo
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# Install Airflow
helm install airflow apache-airflow/airflow \
    --namespace airflow \
    --create-namespace \
    --set executor=KubernetesExecutor

# Get web UI password
kubectl get secret --namespace airflow airflow-webserver-secret -o jsonpath="{.data.webserver-secret-key}" | base64 --decode
```

### Development Setup
```bash
# Install development dependencies
pip install apache-airflow[dev,postgres,celery,kubernetes]

# Install testing tools
pip install pytest pytest-airflow

# Install linting
pip install ruff
```

## Core Capabilities

### 1. Basic DAG Structure

```python
# dags/basic_dag.py
"""
Basic DAG demonstrating core Airflow concepts.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator

# Default arguments for all tasks
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email': ['alerts@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'execution_timeout': timedelta(hours=2),
}

# DAG definition
with DAG(
    dag_id='basic_etl_pipeline',
    default_args=default_args,
    description='Basic ETL pipeline demonstrating core patterns',
    schedule_interval='0 6 * * *',  # Daily at 6 AM
    start_date=datetime(2026, 1, 1),
    catchup=False,
    max_active_runs=1,
    tags=['etl', 'production'],
    doc_md="""
    ## Basic ETL Pipeline

    This DAG demonstrates:
    - Task dependencies
    - Python and Bash operators
    - Error handling with retries
    - Task documentation

    **Owner**: data-team
    **Schedule**: Daily at 6 AM UTC
    """,
) as dag:

    # Start marker
    start = EmptyOperator(
        task_id='start',
        doc='Pipeline start marker',
    )

    # Extract task
    def extract_data(**context):
        """Extract data from source systems."""
        import logging
        logger = logging.getLogger(__name__)

        # Access execution context
        execution_date = context['ds']
        logger.info(f"Extracting data for {execution_date}")

        # Simulated extraction
        data = {
            'records': 1000,
            'source': 'database',
            'execution_date': execution_date,
        }

        # Return value available via XCom
        return data

    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        doc='Extract data from source database',
    )

    # Transform task
    def transform_data(**context):
        """Transform extracted data."""
        import logging
        logger = logging.getLogger(__name__)

        # Pull data from previous task via XCom
        ti = context['ti']
        extracted_data = ti.xcom_pull(task_ids='extract_data')

        logger.info(f"Transforming {extracted_data['records']} records")

        # Simulated transformation
        transformed = {
            **extracted_data,
            'records_transformed': extracted_data['records'],
            'quality_score': 0.95,
        }

        return transformed

    transform = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        doc='Apply transformations to extracted data',
    )

    # Load task using Bash
    load = BashOperator(
        task_id='load_data',
        bash_command='''
            echo "Loading data to warehouse"
            echo "Execution date: {{ ds }}"
            echo "Previous task output: {{ ti.xcom_pull(task_ids='transform_data') }}"
        ''',
        doc='Load transformed data to data warehouse',
    )

    # End marker
    end = EmptyOperator(
        task_id='end',
        doc='Pipeline end marker',
        trigger_rule='all_success',
    )

    # Define dependencies
    start >> extract >> transform >> load >> end
```

### 2. Advanced Operators

```python
# dags/advanced_operators.py
"""
DAG demonstrating advanced operator patterns.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.trigger_rule import TriggerRule

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='advanced_operators_demo',
    default_args=default_args,
    schedule_interval=None,  # Manual trigger only
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['demo', 'advanced'],
) as dag:

    # BranchPythonOperator for conditional logic
    def choose_branch(**context):
        """Decide which branch to execute based on data."""
        import random

        # Simulated decision logic
        data_volume = random.randint(0, 1000)
        context['ti'].xcom_push(key='data_volume', value=data_volume)

        if data_volume > 500:
            return 'process_large_dataset'
        else:
            return 'process_small_dataset'

    branch_task = BranchPythonOperator(
        task_id='branch_on_data_volume',
        python_callable=choose_branch,
    )

    process_large = PythonOperator(
        task_id='process_large_dataset',
        python_callable=lambda: print("Processing large dataset with parallel workers"),
    )

    process_small = PythonOperator(
        task_id='process_small_dataset',
        python_callable=lambda: print("Processing small dataset directly"),
    )

    # Join branches - triggered when any upstream succeeds
    join = EmptyOperator(
        task_id='join_branches',
        trigger_rule=TriggerRule.NONE_FAILED_MIN_ONE_SUCCESS,
    )

    # TaskGroup for logical grouping
    from airflow.utils.task_group import TaskGroup

    with TaskGroup(group_id='validation_tasks') as validation_group:
        validate_schema = PythonOperator(
            task_id='validate_schema',
            python_callable=lambda: print("Validating data schema"),
        )

        validate_quality = PythonOperator(
            task_id='validate_quality',
            python_callable=lambda: print("Validating data quality"),
        )

        validate_completeness = PythonOperator(
            task_id='validate_completeness',
            python_callable=lambda: print("Validating data completeness"),
        )

        # Parallel validation tasks
        [validate_schema, validate_quality, validate_completeness]

    # Dynamic task mapping (Airflow 2.3+)
    def generate_partitions(**context):
        """Generate partition list for dynamic mapping."""
        return ['partition_a', 'partition_b', 'partition_c', 'partition_d']

    get_partitions = PythonOperator(
        task_id='get_partitions',
        python_callable=generate_partitions,
    )

    def process_partition(partition: str):
        """Process a single partition."""
        print(f"Processing {partition}")
        return f"Processed {partition}"

    # Map over partitions dynamically
    process_partitions = PythonOperator.partial(
        task_id='process_partition',
    ).expand(op_args=get_partitions.output.map(lambda x: [x]))

    # Final aggregation
    def aggregate_results(**context):
        """Aggregate results from all partitions."""
        ti = context['ti']
        results = ti.xcom_pull(task_ids='process_partition', key='return_value')
        print(f"Aggregated {len(results)} partition results")

    aggregate = PythonOperator(
        task_id='aggregate_results',
        python_callable=aggregate_results,
    )

    # Dependencies
    branch_task >> [process_large, process_small] >> join
    join >> validation_group >> get_partitions >> process_partitions >> aggregate
```

### 3. Sensors for Event-Driven Workflows

```python
# dags/sensor_patterns.py
"""
DAG demonstrating sensor patterns for event-driven workflows.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.sensors.external_task import ExternalTaskSensor
from airflow.sensors.python import PythonSensor
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'data-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

with DAG(
    dag_id='sensor_patterns_demo',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['sensors', 'event-driven'],
) as dag:

    # FileSensor - Wait for file to appear
    wait_for_file = FileSensor(
        task_id='wait_for_data_file',
        filepath='/data/incoming/{{ ds }}/data.csv',
        poke_interval=60,  # Check every 60 seconds
        timeout=3600,  # Timeout after 1 hour
        mode='poke',  # 'poke' or 'reschedule'
        soft_fail=False,  # Fail task if timeout
    )

    # S3KeySensor - Wait for S3 object
    wait_for_s3 = S3KeySensor(
        task_id='wait_for_s3_file',
        bucket_name='my-data-bucket',
        bucket_key='incoming/{{ ds }}/data.parquet',
        aws_conn_id='aws_default',
        poke_interval=120,
        timeout=7200,
        mode='reschedule',  # Release worker while waiting
    )

    # HttpSensor - Wait for API endpoint
    wait_for_api = HttpSensor(
        task_id='wait_for_api_ready',
        http_conn_id='api_connection',
        endpoint='/health',
        request_params={},
        response_check=lambda response: response.json().get('status') == 'ready',
        poke_interval=30,
        timeout=600,
    )

    # ExternalTaskSensor - Wait for another DAG
    wait_for_upstream_dag = ExternalTaskSensor(
        task_id='wait_for_upstream_dag',
        external_dag_id='upstream_data_pipeline',
        external_task_id='final_task',
        execution_delta=timedelta(hours=0),  # Same execution date
        poke_interval=60,
        timeout=3600,
        mode='reschedule',
        allowed_states=['success'],
        failed_states=['failed', 'skipped'],
    )

    # PythonSensor - Custom condition
    def check_data_quality(**context):
        """Custom sensor logic to check data quality."""
        import random
        # Simulated quality check
        quality_score = random.random()
        print(f"Quality score: {quality_score}")
        return quality_score > 0.8  # Return True when condition met

    wait_for_quality = PythonSensor(
        task_id='wait_for_data_quality',
        python_callable=check_data_quality,
        poke_interval=120,
        timeout=1800,
        mode='poke',
    )

    # Process after all sensors pass
    def process_data(**context):
        """Process data after all conditions are met."""
        print("All sensors passed, processing data...")

    process = PythonOperator(
        task_id='process_data',
        python_callable=process_data,
    )

    # Dependencies - all sensors must pass
    [wait_for_file, wait_for_s3, wait_for_api, wait_for_upstream_dag, wait_for_quality] >> process
```

### 4. Hooks for External System Integration

```python
# dags/hooks_demo.py
"""
DAG demonstrating hook patterns for external system integration.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.slack.hooks.slack_webhook import SlackWebhookHook

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='hooks_integration_demo',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['hooks', 'integration'],
) as dag:

    # PostgresHook for database operations
    def extract_from_postgres(**context):
        """Extract data from PostgreSQL using hook."""
        hook = PostgresHook(postgres_conn_id='postgres_warehouse')

        # Execute query and fetch results
        sql = """
            SELECT id, name, value, created_at
            FROM source_table
            WHERE created_at >= '{{ ds }}'
            AND created_at < '{{ next_ds }}'
        """

        # Get connection and execute
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(sql)
        results = cursor.fetchall()

        # Or use pandas
        df = hook.get_pandas_df(sql)
        print(f"Extracted {len(df)} rows")

        # Store record count
        context['ti'].xcom_push(key='record_count', value=len(df))

        return df.to_dict()

    extract_postgres = PythonOperator(
        task_id='extract_from_postgres',
        python_callable=extract_from_postgres,
    )

    # S3Hook for file operations
    def upload_to_s3(**context):
        """Upload processed data to S3."""
        import json
        from io import BytesIO

        hook = S3Hook(aws_conn_id='aws_default')

        # Pull data from previous task
        ti = context['ti']
        data = ti.xcom_pull(task_ids='extract_from_postgres')

        # Convert to JSON and upload
        json_data = json.dumps(data)
        key = f"processed/{{ ds }}/data.json"

        hook.load_string(
            string_data=json_data,
            key=key,
            bucket_name='my-data-bucket',
            replace=True,
        )

        print(f"Uploaded to s3://my-data-bucket/{key}")
        return key

    upload_s3 = PythonOperator(
        task_id='upload_to_s3',
        python_callable=upload_to_s3,
    )

    # HttpHook for API calls
    def call_external_api(**context):
        """Make API call using HTTP hook."""
        hook = HttpHook(http_conn_id='api_connection', method='POST')

        # Prepare payload
        payload = {
            'execution_date': context['ds'],
            'dag_id': context['dag'].dag_id,
            'task_id': context['task'].task_id,
        }

        # Make request
        response = hook.run(
            endpoint='/api/v1/notify',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
        )

        return response.json()

    api_call = PythonOperator(
        task_id='call_external_api',
        python_callable=call_external_api,
    )

    # SlackWebhookHook for notifications
    def send_slack_notification(**context):
        """Send completion notification to Slack."""
        hook = SlackWebhookHook(slack_webhook_conn_id='slack_webhook')

        ti = context['ti']
        record_count = ti.xcom_pull(task_ids='extract_from_postgres', key='record_count')

        message = f"""
        :white_check_mark: *Pipeline Completed Successfully*

        *DAG*: {context['dag'].dag_id}
        *Execution Date*: {context['ds']}
        *Records Processed*: {record_count}
        """

        hook.send(text=message)

    notify_slack = PythonOperator(
        task_id='send_slack_notification',
        python_callable=send_slack_notification,
    )

    # Dependencies
    extract_postgres >> upload_s3 >> api_call >> notify_slack
```

### 5. XCom for Task Communication

```python
# dags/xcom_patterns.py
"""
DAG demonstrating XCom patterns for inter-task communication.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import XCom

default_args = {
    'owner': 'data-team',
    'retries': 1,
}

with DAG(
    dag_id='xcom_patterns_demo',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['xcom', 'communication'],
) as dag:

    # Basic XCom push via return value
    def produce_data(**context):
        """Produce data - return value auto-pushed to XCom."""
        data = {
            'records': [
                {'id': 1, 'value': 100},
                {'id': 2, 'value': 200},
                {'id': 3, 'value': 300},
            ],
            'metadata': {
                'source': 'api',
                'timestamp': str(datetime.now()),
            }
        }
        return data  # Automatically pushed to XCom

    producer = PythonOperator(
        task_id='produce_data',
        python_callable=produce_data,
    )

    # Consume XCom from previous task
    def consume_data(**context):
        """Consume data from previous task."""
        ti = context['ti']

        # Pull return value (default key)
        data = ti.xcom_pull(task_ids='produce_data')
        print(f"Received {len(data['records'])} records")

        # Process and return
        total = sum(r['value'] for r in data['records'])
        return {'total': total, 'count': len(data['records'])}

    consumer = PythonOperator(
        task_id='consume_data',
        python_callable=consume_data,
    )

    # Multiple XCom values with custom keys
    def produce_multiple(**context):
        """Push multiple XCom values with different keys."""
        ti = context['ti']

        # Push individual values
        ti.xcom_push(key='status', value='success')
        ti.xcom_push(key='row_count', value=1000)
        ti.xcom_push(key='quality_score', value=0.95)
        ti.xcom_push(key='metadata', value={
            'source': 'database',
            'table': 'transactions',
        })

    multi_producer = PythonOperator(
        task_id='produce_multiple_xcoms',
        python_callable=produce_multiple,
    )

    def consume_multiple(**context):
        """Pull multiple XCom values."""
        ti = context['ti']

        # Pull specific keys
        status = ti.xcom_pull(task_ids='produce_multiple_xcoms', key='status')
        row_count = ti.xcom_pull(task_ids='produce_multiple_xcoms', key='row_count')
        quality = ti.xcom_pull(task_ids='produce_multiple_xcoms', key='quality_score')
        metadata = ti.xcom_pull(task_ids='produce_multiple_xcoms', key='metadata')

        print(f"Status: {status}")
        print(f"Rows: {row_count}, Quality: {quality}")
        print(f"Source: {metadata['source']}")

    multi_consumer = PythonOperator(
        task_id='consume_multiple_xcoms',
        python_callable=consume_multiple,
    )

    # Cross-DAG XCom (use with caution)
    def cross_dag_pull(**context):
        """Pull XCom from another DAG run."""
        ti = context['ti']

        # Pull from specific DAG
        value = ti.xcom_pull(
            dag_id='other_dag_id',
            task_ids='other_task_id',
            key='shared_value',
            include_prior_dates=True,  # Look at previous runs
        )
        print(f"Value from other DAG: {value}")

    # Template-based XCom access
    template_task = PythonOperator(
        task_id='template_xcom_access',
        python_callable=lambda **ctx: print(ctx['templates_dict']),
        templates_dict={
            'data': "{{ ti.xcom_pull(task_ids='produce_data') }}",
            'status': "{{ ti.xcom_pull(task_ids='produce_multiple_xcoms', key='status') }}",
        },
    )

    # Dependencies
    producer >> consumer
    multi_producer >> multi_consumer
    [consumer, multi_consumer] >> template_task
```

### 6. Variables and Connections

```python
# dags/config_management.py
"""
DAG demonstrating Variables and Connections for configuration.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.models import Variable
from airflow.hooks.base import BaseHook

default_args = {
    'owner': 'data-team',
    'retries': 1,
}

with DAG(
    dag_id='config_management_demo',
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['config', 'variables'],
) as dag:

    # Using Airflow Variables
    def use_variables(**context):
        """Access Airflow Variables."""
        import json

        # Get simple variable
        environment = Variable.get('environment', default_var='development')
        print(f"Environment: {environment}")

        # Get JSON variable (auto-deserialize)
        config = Variable.get('pipeline_config', deserialize_json=True)
        print(f"Config: {config}")

        # Set variable programmatically
        Variable.set('last_run', str(datetime.now()))

        # Get with default
        threshold = Variable.get('quality_threshold', default_var='0.9')

        return {
            'environment': environment,
            'config': config,
            'threshold': float(threshold),
        }

    var_task = PythonOperator(
        task_id='use_variables',
        python_callable=use_variables,
    )

    # Using Connections
    def use_connections(**context):
        """Access Airflow Connections."""
        # Get connection object
        conn = BaseHook.get_connection('postgres_warehouse')

        print(f"Host: {conn.host}")
        print(f"Port: {conn.port}")
        print(f"Schema: {conn.schema}")
        print(f"Login: {conn.login}")
        # Password accessible but don't log it: conn.password

        # Get extra fields (JSON)
        extra = conn.extra_dejson
        print(f"Extra config: {extra}")

        # Build connection URI
        uri = conn.get_uri()

        return {
            'host': conn.host,
            'schema': conn.schema,
        }

    conn_task = PythonOperator(
        task_id='use_connections',
        python_callable=use_connections,
    )

    # Template-based variable access
    def template_vars(**context):
        """Access variables via templates."""
        # Variables accessible in templates
        print(context['var']['value'])
        print(context['var']['json'])

    template_task = PythonOperator(
        task_id='template_variable_access',
        python_callable=template_vars,
        op_kwargs={
            # Access variable in template
            'config': "{{ var.json.pipeline_config }}",
            'env': "{{ var.value.environment }}",
        },
    )

    # Environment-specific configuration pattern
    def environment_config(**context):
        """Load environment-specific configuration."""
        import json

        env = Variable.get('environment', default_var='development')

        # Load environment-specific config
        config_key = f'config_{env}'
        config = Variable.get(config_key, deserialize_json=True, default_var={})

        # Merge with defaults
        defaults = {
            'batch_size': 1000,
            'timeout': 300,
            'retry_count': 3,
        }

        final_config = {**defaults, **config}
        print(f"Final config for {env}: {final_config}")

        return final_config

    env_config = PythonOperator(
        task_id='load_environment_config',
        python_callable=environment_config,
    )

    # Dependencies
    [var_task, conn_task] >> template_task >> env_config
```

### 7. Error Handling and Callbacks

```python
# dags/error_handling.py
"""
DAG demonstrating error handling and callback patterns.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.trigger_rule import TriggerRule

def on_success_callback(context):
    """Callback executed on task success."""
    print(f"Task {context['task_instance'].task_id} succeeded!")
    # Send success notification, update metrics, etc.

def on_failure_callback(context):
    """Callback executed on task failure."""
    import logging
    logger = logging.getLogger(__name__)

    ti = context['task_instance']
    dag_id = ti.dag_id
    task_id = ti.task_id
    execution_date = context['execution_date']
    exception = context.get('exception')

    error_msg = f"""
    Task Failed!
    DAG: {dag_id}
    Task: {task_id}
    Execution Date: {execution_date}
    Exception: {exception}
    """

    logger.error(error_msg)

    # Send alert (Slack, PagerDuty, email, etc.)
    # slack_hook.send(text=error_msg)

def on_retry_callback(context):
    """Callback executed on task retry."""
    ti = context['task_instance']
    print(f"Task {ti.task_id} retrying (attempt {ti.try_number})")

def sla_miss_callback(dag, task_list, blocking_task_list, slas, blocking_tis):
    """Callback when SLA is missed."""
    print(f"SLA missed for tasks: {task_list}")
    # Send SLA alert

default_args = {
    'owner': 'data-team',
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
    'max_retry_delay': timedelta(minutes=30),
    'on_success_callback': on_success_callback,
    'on_failure_callback': on_failure_callback,
    'on_retry_callback': on_retry_callback,
}

with DAG(
    dag_id='error_handling_demo',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    sla_miss_callback=sla_miss_callback,
    tags=['error-handling', 'callbacks'],
) as dag:

    # Task with potential failure
    def potentially_failing_task(**context):
        """Task that might fail."""
        import random
        if random.random() < 0.3:
            raise ValueError("Random failure for demonstration")
        return "Success!"

    risky_task = PythonOperator(
        task_id='risky_task',
        python_callable=potentially_failing_task,
        sla=timedelta(minutes=30),  # SLA deadline
    )

    # Cleanup task - always runs
    cleanup = BashOperator(
        task_id='cleanup',
        bash_command='echo "Cleaning up resources..."',
        trigger_rule=TriggerRule.ALL_DONE,  # Run regardless of upstream status
    )

    # Error handler task - only runs on upstream failure
    def handle_error(**context):
        """Handle upstream failures."""
        ti = context['ti']
        upstream_tasks = ti.get_dagrun().get_task_instances()

        failed_tasks = [t for t in upstream_tasks if t.state == 'failed']
        if failed_tasks:
            print(f"Failed tasks: {[t.task_id for t in failed_tasks]}")
            # Implement recovery logic

    error_handler = PythonOperator(
        task_id='handle_errors',
        python_callable=handle_error,
        trigger_rule=TriggerRule.ONE_FAILED,  # Run if any upstream fails
    )

    # Success notification - only runs if all succeeded
    success_notify = BashOperator(
        task_id='success_notification',
        bash_command='echo "All tasks completed successfully!"',
        trigger_rule=TriggerRule.ALL_SUCCESS,
    )

    # Dependencies
    risky_task >> [cleanup, error_handler, success_notify]
```

### 8. Docker and Kubernetes Deployment

```yaml
# docker-compose.yml - Production-ready Airflow deployment
version: '3.8'

x-airflow-common:
  &airflow-common
  image: apache/airflow:2.8.1
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth'
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: 'true'
    # Production settings
    AIRFLOW__CORE__PARALLELISM: 32
    AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG: 16
    AIRFLOW__CORE__MAX_ACTIVE_RUNS_PER_DAG: 3
    AIRFLOW__SCHEDULER__PARSING_PROCESSES: 4
    AIRFLOW__CELERY__WORKER_CONCURRENCY: 8
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
    - ./plugins:/opt/airflow/plugins
    - ./config:/opt/airflow/config
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    &airflow-common-depends-on
    redis:
      condition: service_healthy
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5
      start_period: 5s
    restart: always

  redis:
    image: redis:7
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 30s
      retries: 50
      start_period: 30s
    restart: always

  airflow-webserver:
    <<: *airflow-common
    command: webserver
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8974/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-worker:
    <<: *airflow-common
    command: celery worker
    healthcheck:
      test:
        - "CMD-SHELL"
        - 'celery --app airflow.providers.celery.executors.celery_executor.app inspect ping -d "celery@$${HOSTNAME}"'
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-triggerer:
    <<: *airflow-common
    command: triggerer
    healthcheck:
      test: ["CMD-SHELL", 'airflow jobs check --job-type TriggererJob --hostname "$${HOSTNAME}"']
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s
    restart: always
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-init:
    <<: *airflow-common
    entrypoint: /bin/bash
    command:
      - -c
      - |
        airflow db init
        airflow users create \
          --username admin \
          --password admin \
          --firstname Admin \
          --lastname User \
          --role Admin \
          --email admin@example.com
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
    user: "0:0"

volumes:
  postgres-db-volume:
```

```yaml
# kubernetes/values.yaml - Helm chart values for Kubernetes deployment
executor: KubernetesExecutor

# Airflow configuration
config:
  core:
    dags_are_paused_at_creation: 'true'
    load_examples: 'false'
    parallelism: 32
    max_active_tasks_per_dag: 16
  scheduler:
    parsing_processes: 4
  kubernetes:
    delete_worker_pods: 'true'
    delete_worker_pods_on_failure: 'false'

# Web server
webserver:
  replicas: 2
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

# Scheduler
scheduler:
  replicas: 2
  resources:
    requests:
      memory: "2Gi"
      cpu: "1000m"
    limits:
      memory: "4Gi"
      cpu: "2000m"

# Worker pod template
workers:
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "1000m"

# DAGs configuration
dags:
  persistence:
    enabled: true
    size: 10Gi
  gitSync:
    enabled: true
    repo: https://github.com/org/airflow-dags.git
    branch: main
    wait: 60

# Logs
logs:
  persistence:
    enabled: true
    size: 50Gi

# Database
postgresql:
  enabled: true
  persistence:
    enabled: true
    size: 20Gi

# Redis (for Celery if using)
redis:
  enabled: false

# Ingress
ingress:
  enabled: true
  web:
    annotations:
      kubernetes.io/ingress.class: nginx
      cert-manager.io/cluster-issuer: letsencrypt-prod
    hosts:
      - name: airflow.example.com
        tls:
          enabled: true
          secretName: airflow-tls
```

## Integration Examples

### Integration with AWS Services

```python
# dags/aws_integration.py
"""
DAG integrating with AWS services.
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.s3 import S3CreateBucketOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.transfers.s3_to_redshift import S3ToRedshiftOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator

default_args = {
    'owner': 'data-team',
    'retries': 2,
}

with DAG(
    dag_id='aws_integration_pipeline',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['aws', 'integration'],
) as dag:

    # Upload to S3
    upload_to_s3 = LocalFilesystemToS3Operator(
        task_id='upload_to_s3',
        filename='/data/output/{{ ds }}/data.parquet',
        dest_key='raw/{{ ds }}/data.parquet',
        dest_bucket='my-data-lake',
        aws_conn_id='aws_default',
        replace=True,
    )

    # Run Glue ETL job
    run_glue_job = GlueJobOperator(
        task_id='run_glue_etl',
        job_name='my-etl-job',
        script_args={
            '--input_path': 's3://my-data-lake/raw/{{ ds }}/',
            '--output_path': 's3://my-data-lake/processed/{{ ds }}/',
        },
        aws_conn_id='aws_default',
        wait_for_completion=True,
    )

    # Query with Athena
    run_athena_query = AthenaOperator(
        task_id='run_athena_analysis',
        query="""
            SELECT date, COUNT(*) as count, SUM(value) as total
            FROM processed_data
            WHERE partition_date = '{{ ds }}'
            GROUP BY date
        """,
        database='analytics',
        output_location='s3://my-data-lake/athena-results/',
        aws_conn_id='aws_default',
    )

    # Load to Redshift
    load_to_redshift = S3ToRedshiftOperator(
        task_id='load_to_redshift',
        schema='public',
        table='fact_daily_metrics',
        s3_bucket='my-data-lake',
        s3_key='processed/{{ ds }}/',
        redshift_conn_id='redshift_warehouse',
        aws_conn_id='aws_default',
        copy_options=['FORMAT AS PARQUET'],
    )

    upload_to_s3 >> run_glue_job >> run_athena_query >> load_to_redshift
```

## Best Practices

### 1. DAG Design Principles
```python
# Use meaningful DAG and task IDs
dag_id='sales_daily_etl_pipeline'  # Good
dag_id='dag1'  # Bad

# Set appropriate concurrency limits
max_active_runs=1  # For data pipelines with dependencies
max_active_tasks_per_dag=16  # Limit resource usage

# Use tags for organization
tags=['production', 'etl', 'sales']

# Always set catchup=False unless backfill needed
catchup=False

# Use execution_timeout to prevent stuck tasks
execution_timeout=timedelta(hours=2)
```

### 2. Task Best Practices
```python
# Keep tasks atomic and idempotent
def process_partition(partition_date: str):
    """Idempotent: can be safely re-run."""
    # Delete existing data for this partition
    delete_partition(partition_date)
    # Process and insert new data
    insert_data(partition_date)

# Use retries with exponential backoff
default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'retry_exponential_backoff': True,
}

# Avoid heavy processing in sensors
# Bad: sensor does complex computation
# Good: sensor checks simple condition, processing in separate task
```

### 3. Configuration Management
```python
# Use Variables for configuration, not hardcoded values
batch_size = Variable.get('batch_size', default_var=1000)

# Use Connections for credentials
conn = BaseHook.get_connection('my_database')

# Environment-specific configuration
env = Variable.get('environment')
config = Variable.get(f'config_{env}', deserialize_json=True)
```

### 4. Testing DAGs
```python
# tests/test_dags.py
import pytest
from airflow.models import DagBag

def test_dag_loads():
    """Test that DAGs load without errors."""
    dagbag = DagBag()
    assert len(dagbag.import_errors) == 0

def test_dag_structure():
    """Test DAG has expected structure."""
    dagbag = DagBag()
    dag = dagbag.get_dag('my_pipeline')

    assert dag is not None
    assert len(dag.tasks) == 5
    assert dag.schedule_interval == '@daily'
```

## Troubleshooting

### Common Issues

**Issue: DAG not appearing in UI**
```bash
# Check for import errors
airflow dags list-import-errors

# Validate DAG file
python dags/my_dag.py

# Check scheduler logs
docker logs airflow-scheduler-1 | grep -i error
```

**Issue: Tasks stuck in queued state**
```bash
# Check worker status
airflow celery status

# Verify executor configuration
airflow config get-value core executor

# Check for resource constraints
kubectl top pods -n airflow
```

**Issue: XCom size limits**
```python
# Use external storage for large data
def store_large_result(**context):
    # Store in S3 instead of XCom
    s3_hook.load_string(large_data, key='results/data.json', bucket='my-bucket')
    return 's3://my-bucket/results/data.json'  # Return reference only
```

**Issue: Scheduler performance**
```yaml
# Tune scheduler settings
AIRFLOW__SCHEDULER__PARSING_PROCESSES: 4
AIRFLOW__SCHEDULER__MIN_FILE_PROCESS_INTERVAL: 30
AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: 60
```

### Debugging Tips

```python
# Add detailed logging
import logging
logger = logging.getLogger(__name__)

def my_task(**context):
    logger.info(f"Starting task with context: {context}")
    # ... task logic
    logger.debug(f"Intermediate result: {result}")
```

```bash
# Test specific task
airflow tasks test my_dag my_task 2026-01-15

# Clear task state for re-run
airflow tasks clear my_dag -t my_task -s 2026-01-15 -e 2026-01-15

# Trigger DAG run
airflow dags trigger my_dag --conf '{"key": "value"}'
```

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-01-17 | Initial release with comprehensive workflow patterns |

## Resources

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Airflow Helm Chart](https://airflow.apache.org/docs/helm-chart/stable/index.html)
- [Astronomer Guides](https://www.astronomer.io/guides/)
- [Airflow Providers](https://airflow.apache.org/docs/apache-airflow-providers/)

---

*This skill provides production-ready patterns for Apache Airflow workflow orchestration, tested across enterprise data pipelines.*
