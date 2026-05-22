---
name: Data Engineering
description: Comprehensive data engineering skills covering dbt patterns, ELT modeling, Kafka streaming, lakehouse architecture, and data quality checks
---

# Data Engineering

## Overview

This batch covers modern data engineering practices including:

1. **dbt Patterns** - SQL-first transformation with dbt (data build tool)
2. **ELT Modeling** - Dimensional modeling and data warehouse design
3. **Kafka Streaming** - Real-time data streaming with Apache Kafka
4. **Lakehouse Patterns** - Modern data lakehouse architecture
5. **Data Quality Checks** - Data validation and observability

---

## Skills

### 1. dbt Patterns
**Location:** `53-data-engineering/dbt-patterns/SKILL.md`

**Topics:**
- dbt project structure (staging, intermediate, marts)
- Materializations (view, table, incremental, ephemeral)
- Testing (schema tests, custom tests)
- Macros and reusable SQL
- Snapshots (SCD Type 2)
- Documentation and lineage
- Production workflows and CI/CD

**Key Takeaways:**
- Use layered approach: staging → intermediate → marts
- Test everything (unique, not_null, relationships)
- Document all models and columns
- Use incremental models for large tables
- Version control SQL as code

---

### 2. ELT Modeling
**Location:** `53-data-engineering/elt-modeling/SKILL.md`

**Topics:**
- ELT vs ETL (modern vs traditional)
- Dimensional modeling (star schema, snowflake schema)
- Fact tables (transaction, periodic snapshot, accumulating snapshot)
- Dimension tables (SCD Type 1, 2, 3)
- Grain definition
- Kimball vs Inmon approaches
- Data Vault modeling
- Conformed dimensions

**Key Takeaways:**
- ELT leverages cloud warehouse power
- Use star schema for analytics (fast queries)
- Define grain clearly (one row represents what?)
- SCD Type 2 for historical tracking
- Surrogate keys for performance

---

### 3. Kafka Streaming
**Location:** `53-data-engineering/kafka-streaming/SKILL.md`

**Topics:**
- Kafka architecture (topics, partitions, brokers)
- Producers and consumers
- Consumer groups and offset management
- Stream processing (Kafka Streams, ksqlDB)
- Schemas and serialization (Avro, Schema Registry)
- Exactly-once semantics
- Kafka Connect (source and sink connectors)
- Monitoring and operations

**Key Takeaways:**
- Partitions enable parallelism
- Consumer groups for scalability
- Monitor consumer lag (critical metric)
- Use Schema Registry for schema evolution
- Replication factor = 3 for fault tolerance

---

### 4. Lakehouse Patterns
**Location:** `53-data-engineering/lakehouse-patterns/SKILL.md`

**Topics:**
- Data lakehouse concept (lake + warehouse)
- Delta Lake, Apache Iceberg, Apache Hudi
- ACID transactions on data lakes
- Time travel and versioning
- Schema evolution
- Medallion architecture (bronze, silver, gold)
- Optimize and Z-ordering
- Governance and security

**Key Takeaways:**
- Lakehouse = cheap storage + fast queries + ACID
- Bronze (raw) → Silver (cleaned) → Gold (analytics)
- Use Delta Lake for ACID transactions
- Compact small files regularly (OPTIMIZE)
- Time travel for debugging and auditing

---

### 5. Data Quality Checks
**Location:** `53-data-engineering/data-quality-checks/SKILL.md`

**Topics:**
- Data quality dimensions (accuracy, completeness, consistency)
- Schema validation
- Completeness and uniqueness checks
- Range and format validation
- Great Expectations framework
- dbt tests
- Anomaly detection
- Data observability
- Monitoring and alerting

**Key Takeaways:**
- Test early and often (bronze, silver, gold)
- Use Great Expectations or dbt tests
- Quarantine bad data (don't drop)
- Monitor trends (freshness, volume, null rate)
- Fail fast on critical checks

---

## Modern Data Stack

### Architecture
```
Sources (Databases, APIs, Files)
    ↓
Extract & Load (Fivetran, Airbyte)
    ↓
Data Lake/Lakehouse (S3 + Delta Lake)
    ↓
Transform (dbt)
    ↓
Data Warehouse (Snowflake, BigQuery)
    ↓
BI Tools (Tableau, Looker, Power BI)
```

### ELT Pipeline
```
1. Extract & Load: Fivetran/Airbyte → S3/Snowflake
2. Transform: dbt (staging → intermediate → marts)
3. Quality: Great Expectations, dbt tests
4. Serve: BI tools, ML models, APIs
```

### Real-Time Pipeline
```
1. Stream: Kafka (events from applications)
2. Process: Kafka Streams, ksqlDB
3. Store: Delta Lake, Snowflake
4. Serve: Real-time dashboards, alerts
```

---

## Best Practices

### 1. Layered Data Architecture
```
Bronze: Raw data (as-is from source)
Silver: Cleaned data (validated, deduplicated)
Gold: Analytics-ready (dimensional models)
```

### 2. Test-Driven Data Development
```
1. Write test first (what should data look like?)
2. Write transformation
3. Run test
4. Fix until test passes
```

### 3. Documentation as Code
```
- Document models in YAML (dbt)
- Auto-generate docs (dbt docs)
- Keep docs in version control
- Review docs in PRs
```

### 4. Monitoring and Observability
```
Track:
- Data freshness (how old?)
- Data volume (row count)
- Data quality (test pass rate)
- Pipeline health (success/failure)
```

### 5. Incremental Processing
```
- Use incremental models (dbt)
- Process only new/changed data
- Reduces cost and latency
- Handles large datasets
```

---

## Tools Ecosystem

### Orchestration
- **Airflow:** Workflow orchestration
- **Dagster:** Data orchestration
- **Prefect:** Modern workflow engine

### Extract & Load
- **Fivetran:** Managed EL
- **Airbyte:** Open-source EL
- **Stitch:** Simple EL

### Transform
- **dbt:** SQL transformations
- **Spark:** Large-scale processing
- **Dataform:** SQL workflows

### Quality
- **Great Expectations:** Data validation
- **dbt tests:** SQL-based tests
- **Monte Carlo:** Data observability
- **Soda:** Data quality checks

### Storage
- **Snowflake:** Cloud data warehouse
- **BigQuery:** Google's data warehouse
- **Databricks:** Lakehouse platform
- **S3 + Delta Lake:** DIY lakehouse

---

## Career Path

### Junior Data Engineer
```
Skills:
- SQL (advanced)
- Python (basic)
- dbt (core concepts)
- Data modeling (basics)

Focus:
- Write dbt models
- Write data quality tests
- Debug data issues
```

### Mid-Level Data Engineer
```
Skills:
- SQL (expert)
- Python (intermediate)
- dbt (advanced)
- Spark (basic)
- Kafka (basic)

Focus:
- Design data models
- Build data pipelines
- Optimize performance
- Mentor juniors
```

### Senior Data Engineer
```
Skills:
- All of the above (expert)
- Architecture design
- Performance tuning
- Team leadership

Focus:
- Design data architecture
- Set standards and best practices
- Lead complex projects
- Mentor team
```

---

## Summary

**Data Engineering:** Building reliable, scalable data pipelines

**Key Skills:**
1. **dbt:** SQL transformations
2. **ELT Modeling:** Dimensional design
3. **Kafka:** Real-time streaming
4. **Lakehouse:** Modern architecture
5. **Data Quality:** Validation and monitoring

**Modern Stack:**
- Extract & Load: Fivetran, Airbyte
- Transform: dbt
- Store: Snowflake, Delta Lake
- Quality: Great Expectations, dbt tests
- Orchestrate: Airflow, Dagster

**Best Practices:**
- Layered architecture (bronze, silver, gold)
- Test-driven development
- Documentation as code
- Monitoring and observability
- Incremental processing

**Next Steps:**
1. Learn SQL (advanced)
2. Master dbt
3. Understand dimensional modeling
4. Practice with real datasets
5. Build portfolio projects
