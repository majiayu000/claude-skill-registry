---
name: data-engineer
description: Use when user needs scalable data pipeline development, ETL/ELT implementation, or data infrastructure design.
---

# Data Engineer

## Purpose

Provides expert data engineering capabilities for building scalable data pipelines, ETL/ELT workflows, data lakes, and data warehouses. Specializes in distributed data processing, stream processing, data quality, and modern data stack technologies (Airflow, dbt, Spark, Kafka) with focus on reliability and cost optimization.

## When to Use

- Designing end-to-end data pipelines from source to consumption layer
- Implementing ETL/ELT workflows with error handling and data quality checks
- Building data lakes or data warehouses with optimal storage and querying
- Setting up real-time stream processing (Kafka, Flink, Kinesis)
- Optimizing data infrastructure costs (storage tiering, compute efficiency)
- Implementing data governance and compliance (GDPR, data lineage)
- Migrating legacy data systems to modern data platforms

## Quick Start

**Invoke this skill when:**
- Designing end-to-end data pipelines from source to consumption layer
- Implementing ETL/ELT workflows with error handling and data quality checks
- Building data lakes or data warehouses with optimal storage and querying
- Setting up real-time stream processing (Kafka, Flink, Kinesis)
- Optimizing data infrastructure costs (storage tiering, compute efficiency)
- Implementing data governance and compliance (GDPR, data lineage)

**Do NOT invoke when:**
- Only SQL query optimization needed (use database-optimizer instead)
- Machine learning model development (use ml-engineer or data-scientist)
- Simple data analysis or visualization (use data-analyst)
- Database administration tasks (use database-administrator)
- API integration without data transformation (use backend-developer)

## Decision Framework

### Pipeline Architecture Selection

```
├─ Batch Processing?
│   ├─ Daily/hourly schedules → Airflow + dbt
│   │   Pros: Mature ecosystem, SQL-based transforms
│   │   Cost: Low-medium
│   │
│   ├─ Large-scale (TB+) → Spark (EMR/Databricks)
│   │   Pros: Distributed processing, handles scale
│   │   Cost: Medium-high (compute-intensive)
│   │
│   └─ Simple transforms → dbt Cloud or Fivetran
│       Pros: Managed, low maintenance
│       Cost: Medium (SaaS pricing)
│
├─ Stream Processing?
│   ├─ Event streaming → Kafka + Flink
│   │   Pros: Low latency, exactly-once semantics
│   │   Cost: High (always-on infrastructure)
│   │
│   ├─ AWS native → Kinesis + Lambda
│   │   Pros: Serverless, auto-scaling
│   │   Cost: Variable (pay per use)
│   │
│   └─ Simple CDC → Debezium + Kafka Connect
│       Pros: Database change capture
│       Cost: Medium
│
└─ Hybrid (Batch + Stream)?
    └─ Lambda Architecture or Kappa Architecture
        Lambda: Separate batch/speed layers
        Kappa: Single stream-first approach
```

### Data Storage Selection

| Use Case | Technology | Pros | Cons |
|----------|------------|------|------|
| **Structured analytics** | Snowflake/BigQuery | SQL, fast queries | Cost at scale |
| **Semi-structured** | Delta Lake/Iceberg | ACID, schema evolution | Complexity |
| **Raw storage** | S3/GCS | Cheap, durable | No query engine |
| **Real-time** | Redis/DynamoDB | Low latency | Limited analytics |
| **Time-series** | TimescaleDB/InfluxDB | Optimized for time data | Specific use case |

### ETL vs ELT Decision

| Factor | ETL (Transform First) | ELT (Load First) |
|--------|----------------------|------------------|
| **Data volume** | Small-medium | Large (TB+) |
| **Transformation** | Complex, pre-load | SQL-based, in-warehouse |
| **Latency** | Higher | Lower |
| **Cost** | Compute before load | Warehouse compute |
| **Best for** | Legacy systems | Modern cloud DW |

## Core Patterns

### Pattern 1: Idempotent Partition Overwrite
**Use case:** Safely re-run batch jobs without creating duplicates.

```python
# PySpark example: Overwrite partition based on execution date
def write_daily_partition(df, target_table, execution_date):
    (df
     .write
     .mode("overwrite")
     .partitionBy("process_date")
     .option("partitionOverwriteMode", "dynamic")
     .format("parquet")
     .saveAsTable(target_table))
```

### Pattern 2: Slowly Changing Dimension Type 2 (SCD2)
**Use case:** Track history of changes without losing past states.

```sql
-- dbt implementation of SCD2
{{ config(materialized='incremental', unique_key='user_id') }}

SELECT 
    user_id, address, email, status, updated_at,
    LEAD(updated_at, 1, '9999-12-31') OVER (
        PARTITION BY user_id ORDER BY updated_at
    ) as valid_to
FROM {{ source('raw', 'users') }}
```

### Pattern 3: Dead Letter Queue (DLQ) for Streaming
**Use case:** Handle malformed messages without stopping the pipeline.

### Pattern 4: Data Quality Circuit Breaker
**Use case:** Stop pipeline execution if data quality drops below threshold.

## Quality Checklist

### Data Pipeline
- [ ] Idempotent (safe to retry)
- [ ] Schema validation enforced
- [ ] Error handling with retries
- [ ] Data quality checks automated
- [ ] Monitoring and alerting configured
- [ ] Lineage documented

### Performance
- [ ] Pipeline completes within SLA (e.g., <1 hour)
- [ ] Incremental loading where applicable
- [ ] Partitioning strategy optimized
- [ ] Query performance <30 seconds (P95)

### Cost Optimization
- [ ] Storage tiering implemented (hot/warm/cold)
- [ ] Compute auto-scaling configured
- [ ] Query cost monitoring active
- [ ] Compression enabled (Parquet/ORC)

## Additional Resources

- **Detailed Technical Reference**: See [REFERENCE.md](REFERENCE.md)
- **Code Examples & Patterns**: See [EXAMPLES.md](EXAMPLES.md)
