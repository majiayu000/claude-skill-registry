---
name: dagster-orchestration
description: |
  ALWAYS USE when working with Dagster assets, resources, IO managers, schedules, sensors, or dbt integration.
  CRITICAL for: @asset decorators, @dbt_assets, DbtCliResource, ConfigurableResource, IO managers, partitions.
  Enforces CATALOG-AS-CONTROL-PLANE architecture - ALL Iceberg writes via catalog (Polaris/Glue).
  Provides pluggable orchestration patterns abstractable to Airflow/Prefect.
  Compute abstraction: DuckDB (default), Spark, Snowflake - all via dbt.
---

# Dagster Orchestration with dbt Integration

## Constitution Alignment

This skill enforces project principles:
- **I. Technology Ownership**: Dagster owns orchestration, dbt owns SQL
- **II. Plugin-First Architecture**: Orchestrator is pluggable (Dagster default, Airflow 3.x alternative)
- **III. Enforced vs Pluggable**: Iceberg format ENFORCED, compute engine PLUGGABLE
- **VIII. Observability By Default**: All operations emit OpenTelemetry traces and OpenLineage events

## Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0011](docs/architecture/adr/0011-pluggable-orchestration.md) | Pluggable Orchestration | Dagster as default, Airflow 3.x as alternative |
| [ADR-0009](docs/architecture/adr/0009-dbt-owns-sql.md) | dbt Owns SQL | NEVER parse SQL in Python - dbt handles all transformations |
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | All tables MUST be Iceberg format |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | DuckDB default, Snowflake/Spark via dbt |
| [ADR-0033](docs/architecture/adr/0033-airflow-3x.md) | Target Airflow 3.x | Alternative orchestrator option |

## Critical Architecture: Catalog-as-Control-Plane

**⚠️ NEVER write directly to storage. ALL table operations MUST flow through catalog:**

```
┌─────────────────────────────────────────────────────────────┐
│                   DAGSTER ORCHESTRATION                      │
│  (Schedule → Sensor → Asset Graph → Materialization)         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    dbt TRANSFORMATIONS                       │
│  (SQL owns transformations - NEVER parse SQL in Python)      │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
              ▼               ▼               ▼
        ┌─────────┐     ┌─────────┐     ┌─────────┐
        │ DuckDB  │     │  Spark  │     │Snowflake│
        │(default)│     │ (scale) │     │(analytic)│
        └────┬────┘     └────┬────┘     └────┬────┘
              │               │               │
              └───────────────┼───────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               POLARIS / GLUE CATALOG (REST API)              │
│     ⚡ CONTROL PLANE - ACID, Schema, Access, Governance ⚡   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ICEBERG TABLES                            │
│                   (S3 / Azure / GCS)                         │
└─────────────────────────────────────────────────────────────┘
```

**Why Catalog-as-Control-Plane?**
- ACID transactions across ALL compute engines
- Schema evolution coordination (engines see same schema)
- Access control and governance (row/column masking)
- Multi-engine interoperability (DuckDB + Spark + dbt query same tables)
- **See**: `references/catalog-control-plane.md`

## Pluggable Orchestration Design

Design assets as **pure functions** runnable in ANY orchestrator:

| Concept | Dagster | Airflow | Prefect |
|---------|---------|---------|---------|
| Unit of Work | `@asset` | `@task` | `@task` |
| Dependencies | Asset deps | Task deps | Task deps |
| Scheduling | `@schedule` | DAG schedule | Deployment |
| Event-driven | `@sensor` | Sensor | Event handlers |
| Configuration | `ConfigurableResource` | Connection/Variable | Block |

**See**: `references/orchestration-abstraction.md`

## Pre-Implementation Checklist

### Step 1: Verify Runtime Environment

```bash
# ALWAYS run first
python -c "import dagster; print(f'Dagster {dagster.__version__}')"
python -c "import dagster_dbt; print(f'dagster-dbt {dagster_dbt.__version__}')"
python -c "import dagster_iceberg; print(f'dagster-iceberg installed')"
dbt --version
```

### Step 2: Discover Existing Patterns

```bash
# Find Dagster definitions
rg "@asset|@multi_asset|@dbt_assets" --type py
rg "ConfigurableResource|IOManager" --type py
rg "dg.Definitions|Definitions\(" --type py

# Find dbt project
find . -name "dbt_project.yml"
find . -name "manifest.json" -path "*/target/*"

# Check catalog configuration
cat platform.yaml | grep -A 20 "catalogs:"
```

### Step 3: Understand Platform Configuration

```bash
# Two-tier config: platform.yaml (credentials) + floe.yaml (logical refs)
cat platform.yaml    # Engineers NEVER see credentials in code
cat floe.yaml        # Data engineers reference: catalog: default
```

## dbt Integration (Primary Pattern)

### Pattern 1: Load dbt Assets from Manifest

```python
from pathlib import Path
from dagster import AssetExecutionContext, Definitions
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets

dbt_project = DbtProject(
    project_dir=Path(__file__).parent / "dbt",
    packaged_project_dir=Path(__file__).parent / "dbt-project",
)
dbt_project.prepare_if_dev()  # Hot-reload in dev

@dbt_assets(manifest=dbt_project.manifest_path)
def my_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """Execute dbt build - yields Dagster events for each model."""
    yield from dbt.cli(["build"], context=context).stream()

defs = Definitions(
    assets=[my_dbt_assets],
    resources={"dbt": DbtCliResource(project_dir=dbt_project)},
)
```

### Pattern 2: Custom DagsterDbtTranslator

```python
from typing import Any, Mapping, Optional
from dagster import AssetKey
from dagster_dbt import DagsterDbtTranslator, DagsterDbtTranslatorSettings

class FloeDbTranslator(DagsterDbtTranslator):
    """Translator for floe-runtime architecture."""

    def __init__(self):
        super().__init__(
            settings=DagsterDbtTranslatorSettings(
                enable_code_references=True,
                enable_source_tests_as_checks=True,
            )
        )

    def get_asset_key(self, dbt_resource_props: Mapping[str, Any]) -> AssetKey:
        """Map dbt models to Dagster asset keys with namespace."""
        schema = dbt_resource_props.get("schema", "default")
        name = dbt_resource_props["name"]
        return AssetKey([schema, name])

    def get_group_name(self, dbt_resource_props: Mapping[str, Any]) -> Optional[str]:
        """Group by dbt folder structure."""
        fqn = dbt_resource_props.get("fqn", [])
        return fqn[1] if len(fqn) > 2 else None

    def get_metadata(self, dbt_resource_props: Mapping[str, Any]) -> Mapping[str, Any]:
        """Extract governance metadata from dbt model meta."""
        meta = dbt_resource_props.get("meta", {})
        return {
            "classification": meta.get("classification"),
            "owner": meta.get("owner"),
            "sla": meta.get("sla"),
        }
```

**See**: `references/dbt-integration.md` for complete patterns

### Pattern 3: Partitioned dbt Assets

```python
from dagster import DailyPartitionsDefinition

daily_partitions = DailyPartitionsDefinition(start_date="2024-01-01")

@dbt_assets(
    manifest=dbt_project.manifest_path,
    partitions_def=daily_partitions,
)
def partitioned_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    partition_date = context.partition_key
    yield from dbt.cli(
        ["build", "--vars", f'{{"run_date": "{partition_date}"}}'],
        context=context,
    ).stream()
```

## Compute Target Integration

### DuckDB (Default - Ephemeral Compute via dbt-duckdb)

DuckDB reads/writes via catalog ATTACH:

```sql
-- dbt-duckdb plugin automatically executes:
ATTACH 'demo_catalog' AS polaris_catalog (
    TYPE ICEBERG,
    CLIENT_ID '{{ env_var("POLARIS_CLIENT_ID") }}',
    CLIENT_SECRET '{{ env_var("POLARIS_CLIENT_SECRET") }}',
    ENDPOINT '{{ env_var("POLARIS_URI") }}'
);
```

### Snowflake (Analytical Compute)

```sql
-- External Iceberg via Polaris integration
CREATE OR REPLACE ICEBERG TABLE gold.metrics
    CATALOG = 'polaris_catalog'
    EXTERNAL_VOLUME = 'iceberg_volume'
AS SELECT * FROM silver.orders;
```

### Spark (Distributed Compute)

```python
@asset(kinds={"spark"})
def spark_asset(spark: SparkResource):
    spark.spark_session.sql("""
        INSERT INTO polaris_catalog.gold.metrics
        SELECT * FROM polaris_catalog.silver.orders
    """)
```

**See**: `references/compute-abstraction.md`

## IO Manager Patterns

### Iceberg IO Manager (Catalog-Controlled)

```python
from dagster_iceberg.config import IcebergCatalogConfig
from dagster_iceberg.io_manager.arrow import PyArrowIcebergIOManager

iceberg_io_manager = PyArrowIcebergIOManager(
    name="polaris_catalog",
    config=IcebergCatalogConfig(
        properties={
            "type": "rest",
            "uri": "http://polaris:8181/api/catalog",
            "credential": f"{client_id}:{client_secret}",
            "warehouse": "demo_catalog",
        }
    ),
    namespace="default",
)
```

**See**: `references/io-managers.md`

### Environment-Based Resource Switching

```python
import os
from dagster import EnvVar

def get_resources_for_env() -> dict:
    env = os.getenv("DAGSTER_DEPLOYMENT", "local")

    base_resources = {"dbt": DbtCliResource(project_dir=dbt_project)}

    if env == "local":
        return {**base_resources, "io_manager": local_iceberg_io()}
    elif env == "production":
        return {**base_resources, "io_manager": prod_iceberg_io()}
```

## Validation Workflow

### Before Implementation
- [ ] Verified Dagster + dagster-dbt versions
- [ ] Located dbt project and manifest.json
- [ ] Understood catalog configuration (Polaris/Glue)
- [ ] Identified compute targets (DuckDB/Snowflake/Spark)
- [ ] Read `/docs/` for CompiledArtifacts contract

### During Implementation
- [ ] Using `@dbt_assets` for dbt models
- [ ] Custom DagsterDbtTranslator for metadata
- [ ] IO manager uses catalog (NOT direct storage writes)
- [ ] Resources configured per environment
- [ ] Partitions aligned with dbt vars

### After Implementation
- [ ] Run `dagster dev` - verify assets appear
- [ ] Materialize assets manually
- [ ] Verify data lineage in UI
- [ ] Check Polaris catalog for table metadata
- [ ] Test schedules/sensors

## Anti-Patterns to Avoid

❌ **Don't** write to Iceberg without going through catalog
❌ **Don't** hardcode compute logic (use dbt for SQL transforms)
❌ **Don't** mix Dagster partitions with dbt incremental without alignment
❌ **Don't** use deprecated `load_assets_from_dbt_manifest()`
❌ **Don't** bypass `DbtCliResource` for dbt execution
❌ **Don't** store credentials in code (use `EnvVar` or `secret_ref`)
❌ **Don't** parse SQL in Python (dbt owns SQL)

## Reference Documentation

| Document | Purpose |
|----------|---------|
| `references/dbt-integration.md` | Complete dbt-Dagster patterns |
| `references/compute-abstraction.md` | DuckDB, Spark, Snowflake patterns |
| `references/io-managers.md` | Iceberg IO managers, storage layer |
| `references/orchestration-abstraction.md` | Pluggable Airflow/Prefect patterns |
| `references/catalog-control-plane.md` | **CRITICAL** architecture doc |
| `API-REFERENCE.md` | Dagster SDK quick reference |

## Quick Reference: Research Queries

When uncertain, search:
- "Dagster dbt_assets decorator examples 2025"
- "DagsterDbtTranslator custom implementation 2025"
- "dagster-iceberg PyArrowIcebergIOManager 2025"
- "DuckDB Iceberg REST catalog ATTACH 2025"

---

**Remember**: Design for abstraction. Dagster orchestrates, dbt owns SQL, catalog controls storage.
