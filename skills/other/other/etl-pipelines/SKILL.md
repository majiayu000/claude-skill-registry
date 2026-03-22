---
name: etl-pipelines
description: "Design and build ETL (Extract, Transform, Load) data pipelines for data integration. Use for: data extraction from multiple sources, data transformation and cleaning, data loading strategies, pipeline orchestration, error handling, incremental loading, data quality validation, scheduling and monitoring, cloud ETL tools, and DataOps practices."
---

# ETL Pipelines

Design, build, and maintain data pipelines for extracting, transforming, and loading data across systems.

## Overview

ETL (Extract, Transform, Load) pipelines are the backbone of data integration, moving data from source systems to target destinations while applying transformations and business logic. This skill covers designing robust, scalable, and maintainable pipelines using modern tools and best practices.

## ETL Fundamentals

### Extract

**Data Sources**:
- Relational databases (MySQL, PostgreSQL, SQL Server, Oracle)
- NoSQL databases (MongoDB, Cassandra, DynamoDB)
- APIs and web services (REST, SOAP, GraphQL)
- Files (CSV, JSON, XML, Parquet, Avro)
- Streaming sources (Kafka, Kinesis, Event Hubs)
- Cloud storage (S3, Azure Blob, Google Cloud Storage)

**Extraction Methods**:
- **Full Extract**: Complete data copy (simple but resource-intensive)
- **Incremental Extract**: Only new/changed data (efficient, requires change tracking)
- **CDC (Change Data Capture)**: Real-time change tracking from database logs
- **API Pagination**: Retrieve data in chunks from APIs

### Transform

**Common Transformations**:
- **Data Cleaning**: Remove duplicates, handle nulls, fix formatting
- **Data Validation**: Check data types, ranges, business rules
- **Data Enrichment**: Add calculated fields, lookups, external data
- **Data Normalization**: Standardize formats, units, codes
- **Data Aggregation**: Summarize, group, calculate metrics
- **Data Joining**: Combine data from multiple sources
- **Data Filtering**: Remove irrelevant or invalid records

### Load

**Loading Strategies**:
- **Full Load**: Replace entire target table
- **Incremental Load**: Append new records
- **Upsert (Merge)**: Insert new, update existing
- **SCD (Slowly Changing Dimension)**: Track historical changes
- **Bulk Load**: Optimized for large volumes
- **Micro-batch**: Small, frequent loads
- **Streaming Load**: Continuous, real-time loading

## ETL vs ELT

| Aspect | ETL | ELT |
|--------|-----|-----|
| Transform Location | External ETL server | Target data warehouse |
| Best For | Traditional warehouses | Cloud warehouses |
| Performance | Limited by ETL server | Leverages warehouse compute |
| Flexibility | Less flexible | More flexible |
| Storage | Less storage needed | More storage needed |
| Use Case | On-premise, limited compute | Cloud, powerful compute |

## Pipeline Design Patterns

### Batch Processing

Process data in scheduled intervals (hourly, daily, weekly):
- **Pros**: Simple, predictable, efficient for large volumes
- **Cons**: Latency, not real-time
- **Tools**: Apache Airflow, Azure Data Factory, AWS Glue

### Stream Processing

Process data continuously as it arrives:
- **Pros**: Real-time, low latency
- **Cons**: More complex, higher cost
- **Tools**: Apache Kafka, Apache Flink, AWS Kinesis, Azure Stream Analytics

### Lambda Architecture

Combine batch and stream processing:
- **Batch Layer**: Historical data, accuracy
- **Speed Layer**: Real-time data, low latency
- **Serving Layer**: Merge results

### Kappa Architecture

Simplified Lambda with only streaming:
- Single processing pipeline
- Reprocess from stream for corrections
- Simpler architecture

## ETL Tools and Platforms

### Open Source

**Apache Airflow**: Python-based workflow orchestration
**Apache NiFi**: Visual data flow automation
**Apache Spark**: Distributed data processing
**Talend Open Studio**: Visual ETL designer
**Singer**: Open-source ETL framework

### Cloud-Native

**AWS Glue**: Serverless ETL service
**Azure Data Factory**: Cloud data integration
**Google Cloud Dataflow**: Unified stream and batch processing
**Fivetran**: Automated data pipeline platform
**Stitch**: Simple data pipeline service

### Enterprise

**Informatica PowerCenter**: Enterprise ETL platform
**IBM DataStage**: ETL and data integration
**Microsoft SSIS**: SQL Server Integration Services
**Oracle Data Integrator**: Oracle's ETL tool

## Pipeline Orchestration

### Apache Airflow

**DAG (Directed Acyclic Graph)**:
```python
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'sales_etl_pipeline',
    default_args=default_args,
    schedule_interval='0 2 * * *',  # Daily at 2 AM
    catchup=False
)

def extract_data():
    # Extract logic
    pass

def transform_data():
    # Transform logic
    pass

def load_data():
    # Load logic
    pass

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

extract_task >> transform_task >> load_task
```

### Task Dependencies

- **Sequential**: A >> B >> C
- **Parallel**: [A, B, C] >> D
- **Conditional**: Branch based on conditions
- **Dynamic**: Generate tasks programmatically

## Data Quality and Validation

### Validation Checks

**Schema Validation**:
- Column names and order
- Data types
- Required fields

**Data Quality Rules**:
- Range checks (age between 0 and 120)
- Format validation (email, phone, date)
- Referential integrity (foreign keys exist)
- Business rules (order date <= ship date)
- Uniqueness constraints

**Implementation**:
```python
def validate_data(df):
    errors = []
    
    # Check for nulls in required fields
    if df['customer_id'].isnull().any():
        errors.append("Null customer_id found")
    
    # Check data ranges
    if (df['age'] < 0).any() or (df['age'] > 120).any():
        errors.append("Invalid age values")
    
    # Check referential integrity
    valid_customers = get_valid_customer_ids()
    invalid = df[~df['customer_id'].isin(valid_customers)]
    if len(invalid) > 0:
        errors.append(f"{len(invalid)} invalid customer IDs")
    
    return errors
```

## Error Handling and Monitoring

### Error Handling Strategies

**Retry Logic**:
- Exponential backoff
- Maximum retry attempts
- Different strategies for different error types

**Dead Letter Queue**:
- Store failed records for manual review
- Separate processing for problematic data
- Prevent pipeline failure from bad data

**Alerting**:
- Email/Slack notifications on failure
- Escalation for critical pipelines
- Dashboard for pipeline health

### Monitoring Metrics

- **Pipeline Success Rate**: % of successful runs
- **Data Volume**: Records processed per run
- **Processing Time**: Duration of each stage
- **Data Quality**: % of records passing validation
- **Resource Usage**: CPU, memory, storage
- **Cost**: Cloud resource costs

## Incremental Loading Patterns

### Timestamp-Based

Track last modified timestamp:
```sql
SELECT *
FROM source_table
WHERE updated_at > :last_run_timestamp
```

### Change Data Capture (CDC)

Capture changes from database logs:
- **Log-Based CDC**: Read transaction logs
- **Trigger-Based CDC**: Database triggers capture changes
- **Query-Based CDC**: Compare snapshots

### Delta Detection

Compare current state with previous:
```python
# Load current and previous snapshots
current = load_current_data()
previous = load_previous_data()

# Identify changes
new_records = current[~current['id'].isin(previous['id'])]
updated_records = current.merge(previous, on='id', how='inner', suffixes=('_new', '_old'))
updated_records = updated_records[updated_records['hash_new'] != updated_records['hash_old']]
deleted_records = previous[~previous['id'].isin(current['id'])]
```

## Performance Optimization

### Parallel Processing

- **Partition Data**: Split by date, region, or hash
- **Parallel Execution**: Process partitions simultaneously
- **Thread Pools**: Multi-threaded processing
- **Distributed Computing**: Spark, Dask for large-scale

### Batch Size Optimization

- **Too Small**: High overhead, slow processing
- **Too Large**: Memory issues, long transactions
- **Optimal**: Balance between throughput and resource usage
- **Typical Range**: 1,000 - 100,000 records per batch

### Connection Pooling

Reuse database connections:
```python
from sqlalchemy import create_engine, pool

engine = create_engine(
    'postgresql://user:pass@host/db',
    poolclass=pool.QueuePool,
    pool_size=10,
    max_overflow=20
)
```

## Best Practices

### Design Principles

- **Idempotency**: Re-running pipeline produces same result
- **Modularity**: Separate extract, transform, load logic
- **Reusability**: Create reusable components
- **Testability**: Unit tests for transformations
- **Observability**: Logging, monitoring, alerting

### Data Pipeline Checklist

- [ ] Clear data lineage documentation
- [ ] Error handling and retry logic
- [ ] Data quality validation
- [ ] Incremental loading where possible
- [ ] Monitoring and alerting
- [ ] Performance optimization
- [ ] Security and access control
- [ ] Disaster recovery plan
- [ ] Cost optimization
- [ ] Documentation and runbooks

### Security

- **Encryption**: At rest and in transit
- **Access Control**: Least privilege principle
- **Secrets Management**: Use vaults (AWS Secrets Manager, Azure Key Vault)
- **Audit Logging**: Track data access and changes
- **Data Masking**: Protect sensitive data in non-production

## Using the Reference Files

### When to Read Each Reference

**`/references/tool-comparison.md`** — Read when selecting ETL tools, comparing platforms, or evaluating cloud vs on-premise solutions.

**`/references/advanced-patterns.md`** — Read when implementing complex transformations, handling large-scale data, or optimizing pipeline performance.

**`/references/monitoring-alerting.md`** — Read when setting up pipeline monitoring, configuring alerts, or troubleshooting pipeline failures.
