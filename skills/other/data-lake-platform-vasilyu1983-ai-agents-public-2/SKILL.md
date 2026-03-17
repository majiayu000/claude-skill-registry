---
name: data-lake-platform
description: "Data lake and lakehouse platform patterns: ingestion/CDC, transformations, open table formats (Iceberg/Delta/Hudi), query and serving engines (Trino/ClickHouse/DuckDB), orchestration, governance/lineage, cost and operations. Self-hosted and cloud options."
---

# Data Lake Platform

Build and operate production data lakes and lakehouses: ingest, transform, store in open formats, and serve analytics reliably.

## When to Use

- Design data lake/lakehouse architecture
- Set up ingestion pipelines (batch, incremental, CDC)
- Build SQL transformation layers (SQLMesh, dbt)
- Choose table formats and catalogs (Iceberg, Delta, Hudi)
- Deploy query/serving engines (Trino, ClickHouse, DuckDB)
- Implement streaming pipelines (Kafka, Flink)
- Set up orchestration (Dagster, Airflow, Prefect)
- Add governance, lineage, data quality, and cost controls

## Triage Questions

1. Batch, streaming, or hybrid? What is the freshness SLO?
2. Append-only vs upserts/deletes (CDC)? Is time travel required?
3. Primary query pattern: BI dashboards (high concurrency), ad-hoc joins, embedded analytics?
4. PII/compliance: row/column-level access, retention, audit logging?
5. Platform constraints: self-hosted vs cloud, preferred engines, team strengths?

## Default Baseline (Good Starting Point)

- Storage: object storage + open table format (usually Iceberg)
- Catalog: REST/Hive/Glue/Nessie/Unity (match your platform)
- Transforms: SQLMesh or dbt (pick one and standardize)
- Lake query: Trino (or Spark for heavy compute/ML workloads)
- Serving (optional): ClickHouse/StarRocks/Doris for low-latency BI
- Governance: DataHub/OpenMetadata + OpenLineage
- Orchestration: Dagster/Airflow/Prefect

## Workflow

1. Pick table format + catalog: `references/storage-formats.md` (use `assets/cross-platform/template-schema-evolution.md` and `assets/cross-platform/template-partitioning-strategy.md`)
2. Design ingestion (batch/incremental/CDC): `references/ingestion-patterns.md` (use `assets/cross-platform/template-ingestion-governance-checklist.md` and `assets/cross-platform/template-incremental-loading.md`)
3. Design transformations (bronze/silver/gold or data products): `references/transformation-patterns.md` (use `assets/cross-platform/template-data-pipeline.md`)
4. Choose lake query vs serving engines: `references/query-engine-patterns.md`
5. Add governance, lineage, and quality gates: `references/governance-catalog.md` (use `assets/cross-platform/template-data-quality-governance.md` and `assets/cross-platform/template-data-quality.md`)
6. Plan operations + cost controls: `references/operational-playbook.md` and `references/cost-optimization.md` (use `assets/cross-platform/template-data-quality-backfill-runbook.md` and `assets/cross-platform/template-cost-optimization.md`)

## Architecture Patterns

- Medallion (bronze/silver/gold): `references/architecture-patterns.md`
- Data mesh (domain-owned data products): `references/architecture-patterns.md`
- Streaming-first (Kappa): `references/streaming-patterns.md`
- Diagrams/mermaid snippets: `references/overview.md`

## Quick Start

### dlt + ClickHouse

```bash
pip install "dlt[clickhouse]"
dlt init rest_api clickhouse
python pipeline.py
```

### SQLMesh + DuckDB

```bash
pip install sqlmesh
sqlmesh init duckdb
sqlmesh plan && sqlmesh run
```

## Reliability and Safety

### Do

- Define data contracts and owners up front
- Add quality gates (freshness, volume, schema, distribution) per tier
- Make every pipeline idempotent and re-runnable (backfills are normal)
- Treat access control and audit logging as first-class requirements

### Avoid

- Skipping validation to "move fast"
- Storing PII without access controls
- Pipelines that can't be re-run safely
- Manual schema changes without version control

## Resources

| Resource | Purpose |
|----------|---------|
| [references/overview.md](references/overview.md) | Diagrams and decision flows |
| [references/architecture-patterns.md](references/architecture-patterns.md) | Medallion, data mesh |
| [references/ingestion-patterns.md](references/ingestion-patterns.md) | dlt vs Airbyte, CDC |
| [references/transformation-patterns.md](references/transformation-patterns.md) | SQLMesh vs dbt |
| [references/storage-formats.md](references/storage-formats.md) | Iceberg vs Delta |
| [references/query-engine-patterns.md](references/query-engine-patterns.md) | ClickHouse, DuckDB |
| [references/streaming-patterns.md](references/streaming-patterns.md) | Kafka, Flink |
| [references/orchestration-patterns.md](references/orchestration-patterns.md) | Dagster, Airflow |
| [references/bi-visualization-patterns.md](references/bi-visualization-patterns.md) | Metabase, Superset |
| [references/cost-optimization.md](references/cost-optimization.md) | Cost levers and maintenance |
| [references/operational-playbook.md](references/operational-playbook.md) | Monitoring and incident response |
| [references/governance-catalog.md](references/governance-catalog.md) | Catalog, lineage, access control |

## Templates

| Template | Purpose |
|----------|---------|
| [assets/cross-platform/template-medallion-architecture.md](assets/cross-platform/template-medallion-architecture.md) | Baseline bronze/silver/gold plan |
| [assets/cross-platform/template-data-pipeline.md](assets/cross-platform/template-data-pipeline.md) | End-to-end pipeline skeleton |
| [assets/cross-platform/template-ingestion-governance-checklist.md](assets/cross-platform/template-ingestion-governance-checklist.md) | Source onboarding checklist |
| [assets/cross-platform/template-incremental-loading.md](assets/cross-platform/template-incremental-loading.md) | Incremental + backfill plan |
| [assets/cross-platform/template-schema-evolution.md](assets/cross-platform/template-schema-evolution.md) | Schema change rules |
| [assets/cross-platform/template-cost-optimization.md](assets/cross-platform/template-cost-optimization.md) | Cost control checklist |
| [assets/cross-platform/template-data-quality-governance.md](assets/cross-platform/template-data-quality-governance.md) | Quality contracts + SLOs |
| [assets/cross-platform/template-data-quality-backfill-runbook.md](assets/cross-platform/template-data-quality-backfill-runbook.md) | Backfill incident/runbook |

## Related Skills

| Skill | Purpose |
|-------|---------|
| [ai-mlops](../ai-mlops/SKILL.md) | ML deployment |
| [ai-ml-data-science](../ai-ml-data-science/SKILL.md) | Feature engineering |
| [data-sql-optimization](../data-sql-optimization/SKILL.md) | OLTP optimization |
