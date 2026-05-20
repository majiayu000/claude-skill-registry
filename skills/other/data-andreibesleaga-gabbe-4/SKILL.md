---
name: data-engineering
description: Design and implement data pipelines (ETL/ELT), warehousing, and analytics engineering.
context_cost: medium
---
# Data Engineering Skill

## Triggers
- data pipeline
- etl
- elt
- spark
- airflow
- dbt
- warehouse
- big data
- sql optimization
- kafka

## Purpose
To assist with moving, transforming, and storing data at scale for analytics and AI.

## Capabilities

### 1. Data Pipelines (ETL/ELT)
-   **Orchestration**: Airflow DAGs, Prefect flows, Dagster.
-   **Processing**: Spark (PySpark) jobs, Python scripts (Polars/Pandas).
-   **Ingestion**: Kafka consumers, Kinesis, File watchers.

### 2. Analytics Engineering (dbt)
-   **Modeling**: Staging -> Intermediate -> Marts (Star Schema).
-   **Testing**: `unique`, `not_null`, custom dbt tests.
-   **Documentation**: `schema.yml` descriptions.

### 3. Warehousing (Snowflake / BigQuery / Redshift)
-   **Schema Design**: OBT (One Big Table) vs Star Schema.
-   **Optimization**: Partitioning, Clustering, Materialized Views.
-   **Cost Control**: Slot management, auto-suspend.

## Instructions
1.  **Pattern Selection**: Prefer ELT (Load -> Transform in Warehouse) for modern stacks.
2.  **Idempotency**: All pipelines must be re-runnable without duplicating data.
3.  **Data Quality**: Always include data validation steps (Great Expectations / dbt tests).
4.  **Privacy**: Identify and hash PII (GDPR/CCPA compliance).

## Deliverables
-   `dags/` for Airflow.
-   `models/` for dbt.
-   `spark_jobs/` for PySpark.
