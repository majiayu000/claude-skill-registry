---
name: data-lake-platform
description: "Universal data lake and lakehouse patterns covering ingestion (dlt, Airbyte), transformation (SQLMesh, dbt), storage formats (Iceberg, Delta, Hudi, Parquet), query engines (ClickHouse, DuckDB, Doris, StarRocks), streaming (Kafka, Flink), orchestration (Dagster, Airflow, Prefect), and visualization (Metabase, Superset, Grafana). Self-hosted and cloud options."
---

# Data Lake Platform — Quick Reference

Build production data lakes and lakehouses: ingest from any source, transform with SQL, store in open formats, query at scale.

---

## When to Use This Skill

- Design data lake/lakehouse architecture (medallion, data mesh, lambda/kappa)
- Set up data ingestion pipelines (dlt, Airbyte)
- Build SQL transformation layers (SQLMesh, dbt)
- Choose and configure table formats (Iceberg, Delta Lake, Hudi)
- Deploy analytical query engines (ClickHouse, DuckDB, Doris, StarRocks)
- Implement streaming pipelines (Kafka, Flink, Spark Streaming)
- Set up orchestration (Dagster, Airflow, Prefect)
- Implement data quality and governance (Great Expectations, DataHub)
- Optimize storage costs and query performance
- Migrate from legacy warehouse to lakehouse

---

## Quick Reference

| Layer | Tools | Templates | When to Use |
|-------|-------|-----------|-------------|
| **Ingestion** | dlt, Airbyte | `templates/ingestion/` | Extract from APIs, databases, files |
| **Transformation** | SQLMesh, dbt | `templates/transformation/` | SQL-based data modeling |
| **Storage** | Iceberg, Delta, Hudi | `templates/storage/` | Open table formats with ACID |
| **Query Engines** | ClickHouse, DuckDB, Doris | `templates/query-engines/` | Fast analytical queries |
| **Streaming** | Kafka, Flink, Spark | `templates/streaming/` | Real-time data pipelines |
| **Orchestration** | Dagster, Airflow, Prefect | `templates/orchestration/` | Pipeline scheduling |
| **Cloud** | Snowflake, BigQuery, Redshift | `templates/cloud/` | Managed warehouses |
| **Visualization** | Metabase, Superset, Grafana | `templates/visualization/` | Dashboards, BI, monitoring |

---

## Decision Tree: Choosing Your Stack

```text
Data Lake Architecture?
    ├─ Self-hosted priority?
    │   ├─ OLAP queries? → ClickHouse (Yandex origin, Russian-friendly)
    │   ├─ Embedded analytics? → DuckDB (in-process, no server)
    │   ├─ Complex joins + updates? → Apache Doris or StarRocks
    │   └─ Data lakehouse? → Iceberg + Trino/Spark
    │
    ├─ Cloud-native?
    │   ├─ AWS? → Redshift, Athena + Iceberg
    │   ├─ GCP? → BigQuery
    │   └─ Multi-cloud? → Snowflake
    │
    ├─ Ingestion tool?
    │   ├─ Python-first, simple? → dlt (recommended)
    │   ├─ GUI, many connectors? → Airbyte
    │   └─ Enterprise, CDC? → Debezium, Fivetran
    │
    ├─ Transformation tool?
    │   ├─ SQL-first, CI/CD? → SQLMesh (recommended)
    │   ├─ Large community? → dbt
    │   └─ Python transformations? → Pandas + Great Expectations
    │
    ├─ Table format?
    │   ├─ Multi-engine reads? → Apache Iceberg (industry standard)
    │   ├─ Databricks ecosystem? → Delta Lake
    │   └─ CDC, real-time updates? → Apache Hudi
    │
    ├─ Streaming?
    │   ├─ Event streaming? → Apache Kafka
    │   ├─ Stream processing? → Apache Flink
    │   └─ Batch + streaming? → Spark Streaming
    │
    └─ Orchestration?
        ├─ Data-aware, modern? → Dagster (recommended)
        ├─ Mature, many integrations? → Airflow
        └─ Python-native, simple? → Prefect
```

---

## Architecture Patterns

### Pattern 1: Medallion Architecture (Bronze/Silver/Gold)

**Use when:** Building enterprise data lake with clear data quality tiers.

```text
Sources → Bronze (raw) → Silver (cleaned) → Gold (business-ready)
            ↓              ↓                  ↓
         Iceberg        Iceberg            Iceberg
         append-only    deduped            aggregated
```

**Tools:** dlt → SQLMesh → ClickHouse/DuckDB → Metabase

See `templates/cross-platform/template-medallion-architecture.md`

### Pattern 2: Data Mesh (Domain-Oriented)

**Use when:** Large organization, multiple domains, decentralized ownership.

```text
Domain A ──→ Domain A Lake ──→ Data Products
Domain B ──→ Domain B Lake ──→ Data Products
Domain C ──→ Domain C Lake ──→ Data Products
                   ↓
            Federated Catalog (DataHub/OpenMetadata)
```

**Tools:** dlt (per domain) → SQLMesh → Iceberg → DataHub

See `resources/architecture-patterns.md`

### Pattern 3: Lambda/Kappa (Streaming + Batch)

**Use when:** Real-time + historical analytics required.

```text
Lambda: Kafka → Flink (speed layer) ───→ Serving
                   ↓                        ↑
        Batch (Spark) → Iceberg ───────────┘

Kappa:  Kafka → Flink → Iceberg → Serving (single path)
```

**Tools:** Kafka → Flink → Iceberg → ClickHouse

See `resources/streaming-patterns.md`

---

## Core Capabilities

### 1. Data Ingestion (dlt, Airbyte)

Extract data from any source: REST APIs, databases, files, SaaS platforms.

**dlt (Python-native, recommended):**
- Simple pip install, Python scripts
- 100+ verified sources
- Incremental loading, schema evolution
- Destinations: ClickHouse, DuckDB, Snowflake, BigQuery, Postgres

**Airbyte (GUI, connectors):**
- 300+ pre-built connectors
- Self-hosted or cloud
- CDC replication
- Declarative YAML configuration

See `templates/ingestion/dlt/` and `templates/ingestion/airbyte/`

### 2. SQL Transformation (SQLMesh, dbt)

Build data models with SQL, manage dependencies, test data quality.

**SQLMesh (recommended):**
- Virtual data environments
- Automatic change detection
- Plan/apply workflow (like Terraform)
- Built-in unit testing

**dbt (popular alternative):**
- Large community
- Many packages
- Cloud offering
- Jinja templating

See `templates/transformation/sqlmesh/` and `templates/transformation/dbt/`

### 3. Open Table Formats (Iceberg, Delta, Hudi)

Store data in open formats with ACID transactions, time travel, schema evolution.

**Apache Iceberg (recommended):**
- Multi-engine support (Spark, Trino, Flink, ClickHouse)
- Hidden partitioning
- Snapshot isolation
- Industry momentum (Snowflake, Databricks, AWS)

**Delta Lake:**
- Databricks native
- Z-ordering optimization
- Change data feed

**Apache Hudi:**
- Optimized for CDC/updates
- Record-level indexing
- Near real-time ingestion

See `templates/storage/`

### 4. Query Engines (ClickHouse, DuckDB, Doris, StarRocks)

Fast analytical queries on large datasets.

**ClickHouse (self-hosted priority):**
- 100+ GB/s scan speed
- Columnar storage + compression
- Russian origin (Yandex), fully open source
- MergeTree engine family

**DuckDB (embedded):**
- In-process, no server
- Parquet/CSV native
- Python/R integration
- Laptop-scale analytics

**Apache Doris / StarRocks:**
- MPP architecture
- Complex joins
- Real-time updates
- MySQL protocol compatible

See `templates/query-engines/`

### 5. Streaming (Kafka, Flink, Spark)

Real-time data pipelines and stream processing.

**Apache Kafka:**
- Event streaming platform
- Durable log storage
- Connect ecosystem

**Apache Flink:**
- True stream processing
- Exactly-once semantics
- Stateful computations

**Spark Streaming:**
- Micro-batch processing
- Unified batch + stream API
- ML integration

See `templates/streaming/`

### 6. Orchestration (Dagster, Airflow, Prefect)

Schedule and monitor data pipelines.

**Dagster (recommended):**
- Software-defined assets
- Data-aware scheduling
- Built-in observability
- Type system

**Airflow:**
- Mature, battle-tested
- Many operators
- Large community

**Prefect:**
- Python-native
- Hybrid execution
- Simple deployment

See `templates/orchestration/`

### 7. Visualization (Metabase, Superset, Grafana)

Business intelligence dashboards and operational monitoring.

**Metabase (business users):**

- Intuitive question builder
- Self-serve analytics
- Signed embedding
- Caching and permissions

**Apache Superset (analysts):**

- SQL Lab for exploration
- Advanced visualizations
- Row-level security
- Custom chart plugins

**Grafana (infrastructure):**

- Time-series dashboards
- Real-time alerting
- Prometheus/InfluxDB native
- Data pipeline monitoring

See `templates/visualization/` and `resources/bi-visualization-patterns.md`

---

## Navigation

### Resources (Deep Guides)

| Resource | Description |
|----------|-------------|
| [architecture-patterns.md](resources/architecture-patterns.md) | Medallion, data mesh, lakehouse design |
| [ingestion-patterns.md](resources/ingestion-patterns.md) | dlt vs Airbyte, CDC, incremental loading |
| [transformation-patterns.md](resources/transformation-patterns.md) | SQLMesh vs dbt, testing, CI/CD |
| [storage-formats.md](resources/storage-formats.md) | Iceberg vs Delta vs Hudi comparison |
| [query-engine-patterns.md](resources/query-engine-patterns.md) | ClickHouse, DuckDB, Doris optimization |
| [streaming-patterns.md](resources/streaming-patterns.md) | Kafka, Flink, Spark Streaming |
| [orchestration-patterns.md](resources/orchestration-patterns.md) | Dagster, Airflow, Prefect comparison |
| [governance-catalog.md](resources/governance-catalog.md) | DataHub, OpenMetadata, lineage |
| [cost-optimization.md](resources/cost-optimization.md) | Storage, compute, query optimization |
| [operational-playbook.md](resources/operational-playbook.md) | Monitoring, incidents, migrations |
| [bi-visualization-patterns.md](resources/bi-visualization-patterns.md) | Metabase, Superset, Grafana operations |

### Templates (Copy-Paste Ready)

| Category | Templates |
|----------|-----------|
| **Cross-platform** | medallion, pipeline, incremental, quality, schema, partitioning, cost, migration |
| **Ingestion/dlt** | pipeline, rest-api, database-source, incremental, warehouse-loading |
| **Ingestion/Airbyte** | connection, custom-connector |
| **Transformation/SQLMesh** | project, model, incremental, dag, testing, production, security |
| **Transformation/dbt** | project, incremental, testing |
| **Storage** | iceberg-table, iceberg-maintenance, delta-table, hudi-table, parquet-optimization |
| **Query Engines** | clickhouse (setup, ingestion, optimization, materialized-views, replication), duckdb, doris, starrocks |
| **Streaming** | kafka-ingestion, flink-processing, spark-streaming |
| **Orchestration** | dagster-pipeline, airflow-dag, prefect-flow |
| **Cloud** | snowflake-setup, bigquery-setup, redshift-setup |
| **Visualization** | metabase (connection-checklist, dashboard-request, incident-playbook) |

---

## Data Quality & Governance

**[templates/cross-platform/template-ingestion-governance-checklist.md](templates/cross-platform/template-ingestion-governance-checklist.md)** — Intake checklist for new datasets (contracts, access control, operability, cost).

**[templates/cross-platform/template-data-quality-backfill-runbook.md](templates/cross-platform/template-data-quality-backfill-runbook.md)** — Runbook for data incidents, backfills, and safe reprocessing.

**[templates/cross-platform/template-data-quality-governance.md](templates/cross-platform/template-data-quality-governance.md)** — Comprehensive checklist for production data platforms.

### Key Sections

- **Data Quality Contracts** — Schema, freshness SLAs, volume bounds, uniqueness
- **Governance & Access Control** — RBAC, row/column security, classification
- **Security** — Encryption at rest/transit, network isolation, audit trails
- **Reliability** — Backfill procedures, idempotency patterns, reprocessing
- **Cost Control** — Storage optimization, compute governance, monitoring

### Do / Avoid

#### GOOD: Do

- Define data contracts before building pipelines
- Implement quality gates at each tier (Bronze → Silver → Gold)
- Use idempotent operations for all transformations
- Enable audit logging from day one
- Plan for backfills in pipeline design
- Document SLAs for every critical table

#### BAD: Avoid

- Skipping data quality validation to "move fast"
- Storing PII without classification and access controls
- Creating pipelines that can't be re-run safely
- Using shared service accounts without audit trails
- Ignoring cost controls until the bill arrives
- Manual schema changes without version control

### Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **Schema on read only** | Quality issues discovered too late | Add schema validation at Bronze layer |
| **No freshness SLA** | Stale data used in decisions | Define and monitor freshness contracts |
| **Single partition strategy** | Query costs explode | Partition by most common filter column |
| **Unversioned schemas** | Breaking changes surprise consumers | Use schema registry + contracts |
| **No data owner** | Accountability vacuum | Assign owner to every dataset |

---

## Optional: AI/Automation

> **Note**: These are enhancements, not requirements. Implement only after core governance is solid.

- **Automated Quality Monitoring** — Anomaly detection on volumes and distributions
- **AI-Assisted Governance** — Auto-classification of PII columns, metadata enrichment
- **Bounded Claims** — AI detection should supplement, not replace, explicit rules; human review required for PII classification

---

## Related Skills

- **[ai-mlops](../ai-mlops/SKILL.md)** — ML deployment, drift detection, model registry
- **[ai-ml-data-science](../ai-ml-data-science/SKILL.md)** — Feature engineering, ML modeling, EDA
- **[data-sql-optimization](../data-sql-optimization/SKILL.md)** — OLTP database optimization (PostgreSQL, MySQL, Oracle)
- **[ops-devops-platform](../ops-devops-platform/SKILL.md)** — Infrastructure, CI/CD, Kubernetes

---

## Quick Start Examples

### Example 1: dlt + ClickHouse + Metabase

```bash
# Install dlt with ClickHouse
pip install "dlt[clickhouse]"

# Initialize pipeline
dlt init rest_api clickhouse

# Configure and run
python pipeline.py
```

### Example 2: SQLMesh + DuckDB (Local Development)

```bash
# Install SQLMesh
pip install sqlmesh

# Initialize project
sqlmesh init duckdb

# Plan and apply
sqlmesh plan
sqlmesh run
```

### Example 3: Dagster + dlt + SQLMesh

```python
# dagster_pipeline.py
from dagster import asset, Definitions
import dlt
import sqlmesh

@asset
def raw_data():
    pipeline = dlt.pipeline("my_pipeline", destination="duckdb")
    return pipeline.run(source_data())

@asset(deps=[raw_data])
def transformed_data():
    ctx = sqlmesh.Context()
    ctx.run()
```

---

## Sources

See [data/sources.json](data/sources.json) for 100+ curated sources covering:
- Official documentation (dlt, SQLMesh, ClickHouse, Iceberg, etc.)
- Architecture guides (medallion, data mesh)
- Comparison articles (2024-2025 benchmarks)
- Community resources (Discord, Stack Overflow)
- Russian ecosystem (Yandex DataLens, Arenadata, Altinity)
