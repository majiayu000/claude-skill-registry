---
name: data-pipeline-engineer
description: "Expert data engineer for ETL/ELT pipelines, streaming, data warehousing. Activate on: data pipeline, ETL, ELT, data warehouse, Spark, Kafka, Airflow, dbt, data modeling, star schema, streaming data, batch processing, data quality. NOT for: API design (use api-architect), ML training (use ML skills), dashboards (use design skills)."
allowed-tools: Read,Write,Edit,Bash(dbt:*,spark-submit:*,airflow:*,python:*)
category: Data & Analytics
tags:
  - etl
  - spark
  - kafka
  - airflow
  - data-warehouse
pairs-with:
  - skill: api-architect
    reason: APIs that consume pipeline data
  - skill: devops-automator
    reason: Orchestrate pipeline infrastructure
---

# Data Pipeline Engineer

Expert data engineer specializing in ETL/ELT pipelines, streaming architectures, data warehousing, and modern data stack implementation.

## Quick Start

1. **Identify sources** - data formats, volumes, freshness requirements
2. **Choose architecture** - Medallion (Bronze/Silver/Gold), Lambda, or Kappa
3. **Design layers** - staging → intermediate → marts (dbt pattern)
4. **Add quality gates** - Great Expectations or dbt tests at each layer
5. **Orchestrate** - Airflow DAGs with sensors and retries
6. **Monitor** - lineage, freshness, anomaly detection

## Core Capabilities

| Capability | Technologies | Key Patterns |
|------------|--------------|--------------|
| **Batch Processing** | Spark, dbt, Databricks | Incremental, partitioning, Delta/Iceberg |
| **Stream Processing** | Kafka, Flink, Spark Streaming | Watermarks, exactly-once, windowing |
| **Orchestration** | Airflow, Dagster, Prefect | DAG design, sensors, task groups |
| **Data Modeling** | dbt, SQL | Kimball, Data Vault, SCD |
| **Data Quality** | Great Expectations, dbt tests | Validation suites, freshness |

## Architecture Patterns

### Medallion Architecture (Recommended)
```
BRONZE (Raw)     → Exact source copy, schema-on-read, partitioned by ingestion
      ↓ Cleaning, Deduplication
SILVER (Cleansed) → Validated, standardized, business logic applied
      ↓ Aggregation, Enrichment
GOLD (Business)   → Dimensional models, aggregates, ready for BI/ML
```

### Lambda vs Kappa
- **Lambda**: Batch + Stream layers → merged serving layer (complex but complete)
- **Kappa**: Stream-only with replay → simpler but requires robust streaming

## Reference Examples

Full implementation examples in `./references/`:

| File | Description |
|------|-------------|
| `dbt-project-structure.md` | Complete dbt layout with staging, intermediate, marts |
| `airflow-dag.py` | Production DAG with sensors, task groups, quality checks |
| `spark-streaming.py` | Kafka-to-Delta processor with windowing |
| `great-expectations-suite.json` | Comprehensive data quality expectation suite |

## Anti-Patterns (10 Critical Mistakes)

### 1. Full Table Refreshes
**Symptom**: Truncate and rebuild entire tables every run
**Fix**: Use incremental models with `is_incremental()`, partition by date

### 2. Tight Coupling to Source Schemas
**Symptom**: Pipeline breaks when upstream adds/removes columns
**Fix**: Explicit source contracts, select only needed columns in staging

### 3. Monolithic DAGs
**Symptom**: One 200-task DAG running 8 hours
**Fix**: Domain-specific DAGs, ExternalTaskSensor for dependencies

### 4. No Data Quality Gates
**Symptom**: Bad data reaches production before detection
**Fix**: Great Expectations or dbt tests at each layer, block on failures

### 5. Processing Before Archiving
**Symptom**: Raw data transformed without preserving original
**Fix**: Always land raw in Bronze first, make transformations reproducible

### 6. Hardcoded Dates in Queries
**Symptom**: Manual updates needed for date filters
**Fix**: Use Airflow templating (e.g., `ds` variable) or dynamic date functions

### 7. Missing Watermarks in Streaming
**Symptom**: Unbounded state growth, OOM in long-running jobs
**Fix**: Add `withWatermark()` to handle late-arriving data

### 8. No Retry/Backoff Strategy
**Symptom**: Transient failures cause DAG failures
**Fix**: `retries=3`, `retry_exponential_backoff=True`, `max_retry_delay`

### 9. Undocumented Data Lineage
**Symptom**: No one knows where data comes from or who uses it
**Fix**: dbt docs, data catalog integration, column-level lineage

### 10. Testing Only in Production
**Symptom**: Bugs discovered by stakeholders, not engineers
**Fix**: dbt `--target dev`, sample datasets, CI/CD for models

## Quality Checklist

**Pipeline Design:**
- [ ] Incremental processing where possible
- [ ] Idempotent transformations (re-runnable safely)
- [ ] Partitioning strategy defined and documented
- [ ] Backfill procedures documented

**Data Quality:**
- [ ] Tests at Bronze layer (schema, nulls, ranges)
- [ ] Tests at Silver layer (business rules, referential integrity)
- [ ] Tests at Gold layer (aggregation checks, trend monitoring)
- [ ] Anomaly detection for volumes and distributions

**Orchestration:**
- [ ] Retry and alerting configured
- [ ] SLAs defined and monitored
- [ ] Cross-DAG dependencies use sensors
- [ ] max_active_runs prevents parallel conflicts

**Operations:**
- [ ] Data lineage documented
- [ ] Runbooks for common failures
- [ ] Monitoring dashboards for pipeline health
- [ ] On-call procedures defined

## Validation Script

Run `./scripts/validate-pipeline.sh` to check:
- dbt project structure and conventions
- Airflow DAG best practices
- Spark job configurations
- Data quality setup

## External Resources

- [dbt Best Practices](https://docs.getdbt.com/guides/best-practices)
- [Airflow Best Practices](https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [Delta Lake Guide](https://docs.delta.io/latest/index.html)
- [Kafka Streams](https://kafka.apache.org/documentation/streams/)
