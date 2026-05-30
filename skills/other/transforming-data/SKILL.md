---
name: transforming-data
description: Transform raw data into analytical assets using ETL/ELT patterns, SQL (dbt), Python (pandas/polars/PySpark), and orchestration (Airflow). Use when building data pipelines, implementing incremental models, migrating from pandas to polars, or orchestrating multi-step transformations with testing and quality checks.
---

# Data Transformation

Transform raw data into analytical assets using modern transformation patterns, frameworks, and orchestration tools.

## Purpose

Select and implement data transformation patterns across the modern data stack. Transform raw data into clean, tested, and documented analytical datasets using SQL (dbt), Python DataFrames (pandas, polars, PySpark), and pipeline orchestration (Airflow, Dagster, Prefect).

## When to Use

Invoke this skill when:

- Choosing between ETL and ELT transformation patterns
- Building dbt models (staging, intermediate, marts)
- Implementing incremental data loads and merge strategies
- Migrating pandas code to polars for performance improvements
- Orchestrating data pipelines with dependencies and retries
- Adding data quality tests and validation
- Processing large datasets with PySpark
- Creating production-ready transformation workflows

## Quick Start: Common Patterns

### dbt Incremental Model

```sql
{{
  config(
    materialized='incremental',
    unique_key='order_id'
  )
}}

select order_id, customer_id, order_created_at, sum(revenue) as total_revenue
from {{ ref('int_order_items_joined') }}
group by 1, 2, 3

{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

### polars High-Performance Transformation

```python
import polars as pl

result = (
    pl.scan_csv('large_dataset.csv')
    .filter(pl.col('year') == 2024)
    .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
    .group_by('region')
    .agg(pl.col('revenue').sum())
    .collect()  # Execute lazy query
)
```

### Airflow Data Pipeline

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

with DAG(
    dag_id='daily_sales_pipeline',
    schedule_interval='0 2 * * *',
    default_args={'retries': 2, 'retry_delay': timedelta(minutes=5)},
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    extract = PythonOperator(task_id='extract', python_callable=extract_data)
    transform = PythonOperator(task_id='transform', python_callable=transform_data)
    extract >> transform
```

## Decision Frameworks

### ETL vs ELT Selection

**Use ELT (Extract, Load, Transform)** when:
- Using modern cloud data warehouse (Snowflake, BigQuery, Databricks)
- Transformation logic changes frequently
- Team includes SQL analysts
- Data volume 10GB-1TB+ (leverage warehouse parallelism)

**Tools**: dbt, Dataform, Snowflake tasks, BigQuery scheduled queries

**Use ETL (Extract, Transform, Load)** when:
- Regulatory compliance requires pre-load data redaction (PII/PHI)
- Target system lacks compute power
- Real-time streaming with immediate transformation
- Legacy systems without cloud warehouse

**Tools**: AWS Glue, Azure Data Factory, custom Python scripts

**Use Hybrid** when combining sensitive data cleansing (ETL) with analytics transformations (ELT).

**Default recommendation**: ELT with dbt unless specific compliance or performance constraints require ETL.

For detailed patterns, see `references/etl-vs-elt-patterns.md`.

### DataFrame Library Selection

**Choose pandas** when:
- Data size < 500MB
- Prototyping or exploratory analysis
- Need compatibility with pandas-only libraries

**Choose polars** when:
- Data size 500MB-100GB
- Performance critical (10-100x faster than pandas)
- Production pipelines with memory constraints
- Want lazy evaluation with query optimization

**Choose PySpark** when:
- Data size > 100GB
- Need distributed processing across cluster
- Existing Spark infrastructure (EMR, Databricks)

**Migration path**: pandas → polars (easier, similar API) or pandas → PySpark (requires cluster)

For comparisons and migration guides, see `references/dataframe-comparison.md`.

### Orchestration Tool Selection

**Choose Airflow** when:
- Enterprise production (proven at scale)
- Need 5,000+ integrations
- Managed services available (AWS MWAA, GCP Cloud Composer)

**Choose Dagster** when:
- Heavy dbt usage (native `dbt_assets` integration)
- Data lineage and asset-based workflows prioritized
- ML pipelines requiring testability

**Choose Prefect** when:
- Dynamic workflows (runtime task generation)
- Cloud-native architecture preferred
- Pythonic API with decorators

**Safe default**: Airflow (battle-tested) unless specific needs for Dagster/Prefect.

For detailed patterns, see `references/orchestration-patterns.md`.

## SQL Transformations with dbt

### Model Layer Structure

1. **Staging Layer** (`models/staging/`)
   - 1:1 with source tables
   - Minimal transformations (renaming, type casting, basic filtering)
   - Materialized as views or ephemeral

2. **Intermediate Layer** (`models/intermediate/`)
   - Business logic and complex joins
   - Not exposed to end users
   - Often ephemeral (CTEs only)

3. **Marts Layer** (`models/marts/`)
   - Final models for reporting
   - Fact tables (events, transactions)
   - Dimension tables (customers, products)
   - Materialized as tables or incremental

### dbt Materialization Types

**View**: Query re-run each time model referenced. Use for fast queries, staging layer.

**Table**: Full refresh on each run. Use for frequently queried models, expensive computations.

**Incremental**: Only processes new/changed records. Use for large fact tables, event logs.

**Ephemeral**: CTE only, not persisted. Use for intermediate calculations.

### dbt Testing

```yaml
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests:
          - unique
          - not_null
      - name: customer_id
        tests:
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      - name: total_revenue
        tests:
          - dbt_utils.accepted_range:
              min_value: 0
```

For comprehensive dbt patterns, see:
- `references/dbt-best-practices.md`
- `references/incremental-strategies.md`

## Python DataFrame Transformations

### pandas Transformation

```python
import pandas as pd

df = pd.read_csv('sales.csv')
result = (
    df
    .query('year == 2024')
    .assign(revenue=lambda x: x['quantity'] * x['price'])
    .groupby('region')
    .agg({'revenue': ['sum', 'mean']})
)
```

### polars Transformation (10-100x Faster)

```python
import polars as pl

result = (
    pl.scan_csv('sales.csv')  # Lazy evaluation
    .filter(pl.col('year') == 2024)
    .with_columns([(pl.col('quantity') * pl.col('price')).alias('revenue')])
    .group_by('region')
    .agg([
        pl.col('revenue').sum().alias('revenue_sum'),
        pl.col('revenue').mean().alias('revenue_mean')
    ])
    .collect()  # Execute lazy query
)
```

**Key differences**:
- polars uses `scan_csv()` (lazy) vs pandas `read_csv()` (eager)
- polars uses `with_columns()` vs pandas `assign()`
- polars uses `pl.col()` expressions vs pandas string references
- polars requires `collect()` to execute lazy queries

### PySpark for Distributed Processing

```python
from pyspark.sql import SparkSession, functions as F

spark = SparkSession.builder.appName("Transform").getOrCreate()
df = spark.read.csv('sales.csv', header=True, inferSchema=True)

result = (
    df
    .filter(F.col('year') == 2024)
    .withColumn('revenue', F.col('quantity') * F.col('price'))
    .groupBy('region')
    .agg(F.sum('revenue').alias('total_revenue'))
)
```

For migration guides, see `references/dataframe-comparison.md`.

## Pipeline Orchestration

### Airflow DAG Structure

```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data-engineering',
    'retries': 2,
    'retry_delay': timedelta(minutes=5)
}

with DAG(
    dag_id='data_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    start_date=datetime(2024, 1, 1),
    catchup=False
) as dag:
    task1 = PythonOperator(task_id='extract', python_callable=extract_fn)
    task2 = PythonOperator(task_id='transform', python_callable=transform_fn)
    task1 >> task2  # Define dependency
```

### Task Dependency Patterns

**Linear**: `A >> B >> C` (sequential)
**Fan-out**: `A >> [B, C, D]` (parallel after A)
**Fan-in**: `[A, B, C] >> D` (D waits for all)

For Airflow, Dagster, and Prefect patterns, see `references/orchestration-patterns.md`.

## Data Quality and Testing

### dbt Tests

**Generic tests** (reusable): unique, not_null, accepted_values, relationships

**Singular tests** (custom SQL):
```sql
-- tests/assert_positive_revenue.sql
select * from {{ ref('fct_orders') }}
where total_revenue < 0
```

### Great Expectations

```python
import great_expectations as gx

context = gx.get_context()
suite = context.add_expectation_suite("orders_suite")

suite.add_expectation(
    gx.expectations.ExpectColumnValuesToNotBeNull(column="order_id")
)
suite.add_expectation(
    gx.expectations.ExpectColumnValuesToBeBetween(
        column="total_revenue", min_value=0
    )
)
```

For comprehensive testing patterns, see `references/data-quality-testing.md`.

## Advanced SQL Patterns

Window functions for analytics:

```sql
select
    order_date,
    daily_revenue,
    avg(daily_revenue) over (
        partition by region
        order by order_date
        rows between 6 preceding and current row
    ) as revenue_7d_ma,
    sum(daily_revenue) over (
        partition by region
        order by order_date
    ) as cumulative_revenue
from daily_sales
```

For advanced window functions, see `references/window-functions-guide.md`.

## Production Best Practices

### Idempotency

Ensure transformations produce same result when run multiple times:
- Use `merge` statements in incremental models
- Implement deduplication logic
- Use `unique_key` in dbt incremental models

### Incremental Loading

```sql
{% if is_incremental() %}
    where created_at > (select max(created_at) from {{ this }})
{% endif %}
```

### Error Handling

```python
try:
    result = perform_transformation()
    validate_result(result)
except ValidationError as e:
    log_error(e)
    raise
```

### Monitoring

- Set up Airflow email/Slack alerts on task failure
- Monitor dbt test failures
- Track data freshness (SLAs)
- Log row counts and data quality metrics

## Tool Recommendations

**SQL Transformations**: dbt Core (industry standard, multi-warehouse, rich ecosystem)
```bash
pip install dbt-core dbt-snowflake
```

**Python DataFrames**: polars (10-100x faster than pandas, multi-threaded, lazy evaluation)
```bash
pip install polars
```

**Orchestration**: Apache Airflow (battle-tested at scale, 5,000+ integrations)
```bash
pip install apache-airflow
```

## Examples

Working examples in:
- `examples/python/pandas-basics.py` - pandas transformations
- `examples/python/polars-migration.py` - pandas to polars migration
- `examples/python/pyspark-transformations.py` - PySpark operations
- `examples/python/airflow-data-pipeline.py` - Complete Airflow DAG
- `examples/sql/dbt-staging-model.sql` - dbt staging layer
- `examples/sql/dbt-intermediate-model.sql` - dbt intermediate layer
- `examples/sql/dbt-incremental-model.sql` - Incremental patterns
- `examples/sql/window-functions.sql` - Advanced SQL

## Scripts

- `scripts/generate_dbt_models.py` - Generate dbt model boilerplate
- `scripts/benchmark_dataframes.py` - Compare pandas vs polars performance

## Related Skills

For data ingestion patterns, see `ingesting-data`.
For data visualization, see `visualizing-data`.
For database design, see `databases-*` skills.
For real-time streaming, see `streaming-data`.
For data platform architecture, see `ai-data-engineering`.
For monitoring pipelines, see `observability`.
