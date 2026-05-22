---
name: duckdb-lakehouse
description: ALWAYS USE when building data lakehouse with DuckDB compute, configuring dbt-duckdb with Polaris plugin, or designing catalog-first architecture in floe-platform. Use IMMEDIATELY when reading/writing Iceberg tables via Polaris catalog, creating Dagster assets with DuckDB, or connecting to REST catalogs with inline credentials. Provides research steps for DuckDB + Dagster + Iceberg/Polaris integration patterns.
---

# DuckDB Data Lakehouse Development (floe-platform)

This skill provides patterns for building modern data lakehouses using **DuckDB** as ephemeral compute, **Dagster** for orchestration, **dbt** for SQL transforms, and **Apache Iceberg/Polaris** for catalog-managed storage.

## Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0034](docs/architecture/adr/0034-dbt-duckdb-iceberg.md) | dbt-duckdb Iceberg Catalog Workaround | **CRITICAL** - Plugin approach adopted after SPIKE-02 |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | DuckDB as default, Snowflake/Spark as alternatives |
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | All tables MUST be Iceberg format |
| [ADR-0009](docs/architecture/adr/0009-dbt-owns-sql.md) | dbt Owns SQL | NEVER parse SQL in Python |
| [ADR-0043](docs/architecture/adr/0043-dbt-runtime-abstraction.md) | dbt Compilation Abstraction | DBTPlugin handles compilation environment |

## floe-platform Architecture

```
platform.yaml → DbtProfilesGenerator → profiles.yml
             → Polaris Plugin → ATTACH polaris_catalog (inline credentials)
             → dbt materialization → DuckDB native Iceberg writes
             → Dagster auto-discovery → Assets from manifest.json
```

**Key Insight**: floe-platform uses a two-tier configuration model where data engineers write `floe.yaml` with logical references (`storage: default`, `catalog: default`) while platform engineers manage `platform.yaml` with infrastructure details (endpoints, credentials via K8s secrets).

## Quick Reference

### DuckDB Connection Patterns

```python
import duckdb

# Ephemeral in-memory (recommended for pipelines)
conn = duckdb.connect(":memory:")

# File-based (for floe-platform)
conn = duckdb.connect("/tmp/floe.duckdb")

# With configuration
conn = duckdb.connect(config={
    'memory_limit': '8GB',
    'threads': 4,
    'temp_directory': '/tmp/duckdb'
})

# Context manager (auto-closes)
with duckdb.connect(":memory:") as conn:
    result = conn.sql("SELECT * FROM my_table").fetchdf()
```

### Iceberg ATTACH with Inline Credentials (floe-platform Pattern)

```python
# CRITICAL: Use inline credentials to bypass DuckDB secret manager timing issues
catalog_uri = "http://floe-infra-polaris:8181/api/catalog"
warehouse = "demo_catalog"
client_id = os.getenv("POLARIS_CLIENT_ID")
client_secret = os.getenv("POLARIS_CLIENT_SECRET")

oauth2_server_uri = f"{catalog_uri}/v1/oauth/tokens"

attach_sql = f"""
ATTACH IF NOT EXISTS '{warehouse}' AS polaris_catalog (
    TYPE ICEBERG,
    CLIENT_ID '{client_id}',
    CLIENT_SECRET '{client_secret}',
    OAUTH2_SERVER_URI '{oauth2_server_uri}',
    ENDPOINT '{catalog_uri}'
)
"""
conn.execute(attach_sql)

# Query Iceberg tables through attached catalog
df = conn.sql("SELECT * FROM polaris_catalog.namespace.table_name").fetchdf()
```

**Why Inline Credentials?**
- DuckDB secret manager initializes BEFORE dbt-duckdb plugin runs
- `CREATE SECRET` fails with "Secret Manager settings cannot be changed"
- Inline credentials bypass secret manager entirely (supported in DuckDB 1.4+)

### Extension Pre-Installation (Container Entrypoint)

```python
# In docker/entrypoint.sh
import duckdb

db_path = '/tmp/floe.duckdb'
conn = duckdb.connect(db_path)

conn.execute("INSTALL iceberg")
conn.execute("INSTALL httpfs")

print(f"✓ Installed DuckDB extensions (iceberg, httpfs)")
conn.close()
```

**Why Pre-Install?**
- Extensions persist across sessions for file-based databases
- Avoids timing issues during dbt execution
- Single installation per container lifecycle

### dbt-duckdb Polaris Plugin

```python
# packages/floe-dbt/src/floe_dbt/plugins/polaris.py
from dbt.adapters.duckdb.plugins import BasePlugin
from floe_polaris.client import PolarisCatalog
from floe_polaris.config import PolarisCatalogConfig

class Plugin(BasePlugin):
    def initialize(self, config: dict[str, Any]) -> None:
        """Initialize Polaris catalog connection for metadata operations."""
        catalog_config = PolarisCatalogConfig(
            uri=config["catalog_uri"],
            warehouse=config["warehouse"],
            client_id=config.get("client_id") or os.getenv("POLARIS_CLIENT_ID"),
            client_secret=config.get("client_secret") or os.getenv("POLARIS_CLIENT_SECRET"),
            scope=config.get("scope", "PRINCIPAL_ROLE:ALL"),
            s3_endpoint=config.get("s3_endpoint"),
            s3_region=config.get("s3_region", "us-east-1"),
            s3_access_key_id=config.get("s3_access_key_id") or os.getenv("AWS_ACCESS_KEY_ID"),
            s3_secret_access_key=config.get("s3_secret_access_key") or os.getenv("AWS_SECRET_ACCESS_KEY"),
            s3_path_style_access=True,
        )
        self.catalog = PolarisCatalog(catalog_config)

    def configure_connection(self, conn: Any) -> None:
        """ATTACH Polaris catalog to DuckDB for native Iceberg writes."""
        catalog_uri = self.config["catalog_uri"]
        warehouse = self.config["warehouse"]
        client_id = self.config.get("client_id") or os.getenv("POLARIS_CLIENT_ID")
        client_secret = self.config.get("client_secret") or os.getenv("POLARIS_CLIENT_SECRET")

        oauth2_server_uri = f"{catalog_uri}/v1/oauth/tokens"

        attach_sql = f"""
        ATTACH IF NOT EXISTS '{warehouse}' AS polaris_catalog (
            TYPE ICEBERG,
            CLIENT_ID '{client_id}',
            CLIENT_SECRET '{client_secret}',
            OAUTH2_SERVER_URI '{oauth2_server_uri}',
            ENDPOINT '{catalog_uri}'
        )
        """
        conn.execute(attach_sql)
```

**Architecture Notes**:
- `initialize()` creates PolarisCatalog for metadata operations
- `configure_connection()` runs AFTER secret manager initialization
- Inline credentials in ATTACH bypass CREATE SECRET timing issue
- Environment variables set by platform.yaml → K8s secrets

### Dagster DuckDB Resource

```python
from dagster_duckdb import DuckDBResource
import dagster as dg

@dg.asset(kinds={"duckdb"})
def my_asset(duckdb: DuckDBResource):
    with duckdb.get_connection() as conn:
        conn.execute("CREATE TABLE ... AS SELECT ...")

defs = dg.Definitions(
    assets=[my_asset],
    resources={"duckdb": DuckDBResource(database="/tmp/floe.duckdb")}
)
```

### Dagster I/O Manager (DataFrame auto-storage)

```python
from dagster_duckdb_pandas import DuckDBPandasIOManager
import pandas as pd

@dg.asset
def my_table() -> pd.DataFrame:
    return pd.DataFrame({"col": [1, 2, 3]})

defs = dg.Definitions(
    assets=[my_table],
    resources={
        "io_manager": DuckDBPandasIOManager(
            database="/tmp/floe.duckdb",
            schema="analytics"
        )
    }
)
```

## When to Use Each Component

| Task | Use This |
|------|----------|
| Complex SQL transforms | dbt with DuckDB |
| Reading Iceberg tables | DuckDB + ATTACH polaris_catalog |
| Writing to Iceberg | DuckDB native via ATTACH (catalog-coordinated) |
| DataFrame persistence | Dagster I/O Manager |
| Raw SQL in pipelines | DuckDB Resource |
| Partitioned assets | Dagster + partition_expr metadata |

## floe-platform Configuration

### Two-Tier Configuration Architecture

**floe.yaml** (Data Engineer - same across all environments):
```yaml
name: customer-analytics
version: "1.0.0"
storage: default      # Logical reference
catalog: default      # Logical reference
compute: default      # Logical reference
```

**platform.yaml** (Platform Engineer - environment-specific):
```yaml
version: "1.1.0"

compute:
  default:
    type: duckdb
    properties:
      path: "/tmp/floe.duckdb"  # File-based for extension persistence
      threads: 4
    credentials:
      mode: static

catalogs:
  default:
    type: polaris
    uri: "http://floe-infra-polaris:8181/api/catalog"
    warehouse: demo_catalog
    namespace: default
    credentials:
      mode: oauth2
      client_id:
        secret_ref: polaris-client-id    # K8s secret
      client_secret:
        secret_ref: polaris-client-secret # K8s secret
      scope: "PRINCIPAL_ROLE:service_admin"
    access_delegation: none
    token_refresh_enabled: true

storage:
  bronze:
    type: s3
    endpoint: "http://floe-infra-localstack:4566"
    region: us-east-1
    bucket: iceberg-bronze
    path_style_access: true
    credentials:
      mode: static
      secret_ref: aws-credentials
```

### Generated profiles.yml

```python
# packages/floe-core/src/floe_core/compiler/dbt_profiles_generator.py
from pathlib import Path
from floe_core.compiler.dbt_profiles_generator import DbtProfilesGenerator

DbtProfilesGenerator.generate_from_env(
    floe_path=Path("/app/demo/data_engineering/floe.yaml"),
    output_path=Path("/app/demo/data_engineering/dbt/profiles.yml"),
    platform_file_env="FLOE_PLATFORM_FILE",
    profile_name="default",
)
```

**Generated Output**:
```yaml
default:
  outputs:
    dev:
      type: duckdb
      path: "/tmp/floe.duckdb"
      threads: 4
      plugins:
        - module: floe_dbt.plugins.polaris
          config:
            catalog_uri: "{{ env_var('FLOE_POLARIS_URI') }}"
            warehouse: "{{ env_var('FLOE_POLARIS_WAREHOUSE') }}"
            client_id: "{{ env_var('POLARIS_CLIENT_ID') }}"
            client_secret: "{{ env_var('POLARIS_CLIENT_SECRET') }}"
            scope: "PRINCIPAL_ROLE:service_admin"
            s3_endpoint: "{{ env_var('FLOE_S3_ENDPOINT') }}"
            s3_region: "{{ env_var('FLOE_S3_REGION') }}"
  target: dev
```

## Detailed Documentation

For comprehensive patterns and examples, see:
- `references/floe-platform-integration.md` - Platform-specific architecture
- `references/duckdb-core.md` - Python API, extensions, performance tuning
- `references/dagster-integration.md` - Resources, I/O managers, partitioning
- `references/iceberg-polaris.md` - REST catalog, PyIceberg, credentials
- `references/architecture.md` - Design patterns and anti-patterns

## Anti-Patterns to Avoid

❌ **Don't** use CREATE SECRET in plugin (secret manager already initialized)
❌ **Don't** use :memory: database (extensions don't persist)
❌ **Don't** run dbt compile in entrypoint (triggers secret manager errors)
❌ **Don't** use DuckDB as a persistent shared database (single-writer limitation)
❌ **Don't** write Iceberg tables without ATTACH (bypasses catalog coordination)
❌ **Don't** share connections across threads
❌ **Don't** hardcode credentials (use env vars from K8s secrets)

## Common Error: Secret Manager Initialization

**Error**: `Invalid Input Error: Changing Secret Manager settings after the secret manager is used is not allowed!`

**Root Cause**: DuckDB secret manager initializes when dbt-duckdb opens its first connection, BEFORE the plugin's `configure_connection()` method runs.

**Solution**: Use inline credentials in ATTACH statement:
```python
attach_sql = f"""
ATTACH IF NOT EXISTS '{warehouse}' AS polaris_catalog (
    TYPE ICEBERG,
    CLIENT_ID '{client_id}',
    CLIENT_SECRET '{client_secret}',
    OAUTH2_SERVER_URI '{oauth2_server_uri}',
    ENDPOINT '{catalog_uri}'
)
"""
```

**Anti-Pattern (Don't Do This)**:
```python
# ❌ This fails because secret manager is already initialized
conn.execute("""
CREATE SECRET polaris_secret (
    TYPE ICEBERG,
    CLIENT_ID 'client_id',
    CLIENT_SECRET 'client_secret'
)
""")
```

## Performance Tuning (K8s Environment)

```yaml
# demo/platform-config/platform/local/platform.yaml
infrastructure:
  resource_profiles:
    transform:
      requests:
        cpu: "1000m"
        memory: "4Gi"
      limits:
        cpu: "8000m"
        memory: "12Gi"
      env:
        DUCKDB_MEMORY_LIMIT: "8GB"   # 67% of 12Gi limit
        DUCKDB_THREADS: "4"
        DUCKDB_TEMP_DIRECTORY: "/tmp/duckdb"
```

**Memory Guidelines**:
- Minimum: 125 MB per thread
- Aggregation: 1-2 GB per thread
- Joins: 3-4 GB per thread
- Optimal: 5 GB per thread

## References

- DuckDB Iceberg Extension: https://duckdb.org/docs/extensions/iceberg
- DuckDB Issue #18021: Lazy loading of persistent secrets
- dagster-duckdb: https://docs.dagster.io/_apidocs/libraries/dagster-duckdb
- PyIceberg: https://py.iceberg.apache.org/
- Apache Polaris: https://polaris.apache.org/
