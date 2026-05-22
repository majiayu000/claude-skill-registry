---
name: airflow-workflows
description: Apache Airflow DAG design, operators, and scheduling best practices.
---

# Airflow Workflows

## DAG Structure

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'daily_etl',
    default_args=default_args,
    description='Daily ETL pipeline',
    schedule_interval='0 6 * * *',  # 6 AM daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['etl', 'daily'],
) as dag:

    extract = PythonOperator(
        task_id='extract_data',
        python_callable=extract_function,
    )

    transform = SQLExecuteQueryOperator(
        task_id='transform_data',
        conn_id='warehouse',
        sql='sql/transform.sql',
    )

    load = PythonOperator(
        task_id='load_data',
        python_callable=load_function,
    )

    extract >> transform >> load
```

## Common Operators

| Operator | Use Case |
|----------|----------|
| `PythonOperator` | Custom Python code |
| `BashOperator` | Shell commands |
| `SQLExecuteQueryOperator` | Database queries |
| `S3ToSnowflakeOperator` | Cloud data transfers |
| `DbtCloudRunJobOperator` | dbt Cloud jobs |

## Best Practices

1. **Idempotent tasks** - Safe to re-run
2. **Small tasks** - Easy to debug, retry
3. **XCom sparingly** - Only small data
4. **Templating** - Use `{{ ds }}` for dates
5. **Sensors wisely** - Avoid blocking workers

## Task Dependencies

```python
# Linear
task1 >> task2 >> task3

# Parallel
[task1, task2] >> task3

# Complex
task1 >> [task2, task3]
[task2, task3] >> task4
```

## Dynamic DAGs

```python
for table in ['users', 'orders', 'products']:
    task = PythonOperator(
        task_id=f'process_{table}',
        python_callable=process_table,
        op_kwargs={'table': table},
    )
```
