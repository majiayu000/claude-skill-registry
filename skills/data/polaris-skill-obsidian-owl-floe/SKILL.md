---
name: polaris-catalog
description: ALWAYS USE when configuring Polaris catalog, managing namespaces, or setting up credentials in floe-platform. Use IMMEDIATELY when integrating DuckDB via dbt-duckdb plugin, configuring PyIceberg REST catalog, or debugging access control issues. Provides research steps for REST API, OAuth2 authentication, and multi-engine coordination with DuckDB, dbt, and Dagster.
---

# Apache Polaris Catalog Management (floe-runtime)

## Related ADRs

| ADR | Decision | Relevance |
|-----|----------|-----------|
| [ADR-0005](docs/architecture/adr/0005-iceberg-table-format.md) | Apache Iceberg Enforced | Polaris manages Iceberg table metadata |
| [ADR-0034](docs/architecture/adr/0034-dbt-duckdb-iceberg.md) | dbt-duckdb Workaround | Inline credentials for DuckDB ATTACH |
| [ADR-0010](docs/architecture/adr/0010-target-agnostic-compute.md) | Target-Agnostic Compute | Polaris coordinates multi-engine access |
| [ADR-0036](docs/architecture/adr/0036-storage-plugin-interface.md) | Storage Plugin Interface | Polaris uses pluggable storage backends |
| [ADR-0031](docs/architecture/adr/0031-infisical-secrets.md) | Infisical Secrets | OAuth2 credentials managed via secrets |

## When to Use This Skill

Invoke this skill when working on:
- Polaris catalog configuration in `platform.yaml`
- Namespace creation and management
- Credential setup (OAuth2, static, IAM role)
- DuckDB ATTACH integration via dbt-duckdb plugin
- PyIceberg catalog operations
- Access control (principals, roles, privileges)
- Helm chart initialization jobs

## Core Principles

### 1. Catalog-as-Control-Plane

**NEVER write directly to storage**. All table operations MUST flow through Polaris catalog:

```
Apache Polaris (REST Catalog API)
        ↓
DuckDB (ATTACH) | dbt-duckdb (Plugin) | PyIceberg (Direct)
```

### 2. Two-Tier Configuration Architecture

| File | Audience | Contains |
|------|----------|----------|
| `platform.yaml` | Platform Engineers | Polaris endpoints, credentials, storage |
| `floe.yaml` | Data Engineers | Logical references (`catalog: default`) |

**Data engineers NEVER see credentials.**

## Pre-Implementation Checklist

### Step 1: Discover Existing Patterns (ALWAYS DO FIRST)

```bash
# Check floe-polaris client implementation
cat packages/floe-polaris/src/floe_polaris/client.py

# Review platform.yaml examples
cat demo/platform-config/platform/local/platform.yaml | grep -A 20 "catalogs:"

# Check dbt-duckdb plugin ATTACH logic
cat packages/floe-dbt/src/floe_dbt/plugins/polaris.py

# Review Helm initialization
cat demo/platform-config/charts/floe-infrastructure/templates/polaris-init-job.yaml
```

### Step 2: Verify Polaris Runtime State

```bash
# Check Polaris availability
curl -s http://localhost:8181/api/catalog/v1/config

# Test OAuth2 authentication
curl -X POST http://localhost:8181/api/catalog/v1/oauth/tokens \
  -d "grant_type=client_credentials" \
  -d "client_id=demo_client" \
  -d "client_secret=demo_secret" \
  -d "scope=PRINCIPAL_ROLE:ALL"

# List catalogs
curl -H "Authorization: Bearer $TOKEN" \
  http://localhost:8181/api/management/v1/catalogs
```

### Step 3: Research When Uncertain (Use WebSearch)

- "Apache Polaris REST catalog API 2025"
- "Apache Polaris namespace hierarchical creation 2025"
- "DuckDB Iceberg REST catalog ATTACH syntax 2025"
- "Apache Polaris OAuth2 client credentials flow 2025"

**Official docs**: https://polaris.apache.org

## Quick Reference: Common Patterns

### Pattern 1: Platform Configuration

```yaml
# platform/local/platform.yaml
catalogs:
  default:
    type: polaris
    uri: "http://floe-infra-polaris:8181/api/catalog"
    warehouse: demo_catalog
    credentials:
      mode: oauth2
      client_id:
        secret_ref: polaris-client-id    # → POLARIS_CLIENT_ID env var
      client_secret:
        secret_ref: polaris-client-secret # → POLARIS_CLIENT_SECRET env var
      scope: "PRINCIPAL_ROLE:service_admin"
    access_delegation: none  # Disable vended credentials for LocalStack
    token_refresh_enabled: true
```

### Pattern 2: floe-polaris Client Usage

```python
from floe_polaris import create_catalog, PolarisCatalogConfig
from pydantic import SecretStr

config = PolarisCatalogConfig(
    uri="http://polaris:8181/api/catalog",
    warehouse="demo_catalog",
    client_id="demo_client",
    client_secret=SecretStr("demo_secret"),
    scope="PRINCIPAL_ROLE:service_admin",
    token_refresh_enabled=True,
)
catalog = create_catalog(config)

# Create namespace with parents
catalog.create_namespace("demo.bronze", create_parents=True)

# Load table
table = catalog.load_table("demo.bronze.raw_events")
```

### Pattern 3: DuckDB ATTACH (dbt-duckdb plugin handles this)

```sql
-- Plugin automatically executes on dbt run:
ATTACH 'demo_catalog' AS polaris_catalog (
    TYPE ICEBERG,
    CLIENT_ID 'demo_client',
    CLIENT_SECRET 'demo_secret',
    OAUTH2_SERVER_URI 'http://polaris:8181/api/catalog/v1/oauth/tokens',
    ENDPOINT 'http://polaris:8181/api/catalog'
);

-- Data engineers just write dbt models:
-- models/gold/metrics.sql
{{ config(materialized='table', schema='gold') }}
SELECT customer_id, SUM(amount) as total
FROM {{ ref('silver_orders') }}
GROUP BY 1
```

## Critical Implementation Notes

### S3 Storage Config (OpenAPI Spec)

**CRITICAL**: Use **flat keys**, NOT nested objects:

```python
# ✅ CORRECT
storage_config = {
    "storageType": "S3",
    "endpoint": "http://localstack:4566",      # Flat key
    "pathStyleAccess": True,                    # CRITICAL for LocalStack/MinIO
    "region": "us-east-1"
}

# ❌ WRONG
storage_config = {
    "s3": {"endpoint": "..."}  # Not accepted by Polaris API
}
```

**Without `pathStyleAccess: true`**:
```
UnknownHostException: iceberg-data.localstack: Name or service not known
```

### Catalog Storage Config is Immutable

**Known limitation**: Cannot update storage config after catalog creation.

**Workaround**: Delete and recreate catalog (Helm init job checks existence first).

### Access Control: Three-Tier RBAC

```
Principal (demo_client)
  ↓
Principal Role (service_admin)
  ↓
Catalog Role (demo_data_admin)
  ↓
Privileges (CATALOG_MANAGE_CONTENT, TABLE_*, NAMESPACE_*)
```

## Common Errors and Solutions

**1. Authentication failure (401)**
- Verify `POLARIS_CLIENT_ID` and `POLARIS_CLIENT_SECRET` env vars
- Check `token_refresh_enabled: true`
- Test OAuth2 token manually

**2. DuckDB ATTACH fails**
- Check `catalog_uri` includes `/api/catalog`
- Verify environment variables in dbt profiles.yml

**3. S3 path resolution fails**
- Ensure `pathStyleAccess: true` in storage config
- Set `access_delegation: ""` (empty string) for LocalStack

**4. Namespace not found**
- Use `create_parents=True` when creating nested namespaces
- Check hierarchical creation order (parent before child)

## Detailed Documentation

For comprehensive details, see:
- **Integration Patterns**: `.claude/skills/polaris-skill/docs/integration-patterns.md`
- **API Reference**: `.claude/skills/polaris-skill/docs/api-reference.md`
- **Helm Initialization**: `demo/platform-config/charts/floe-infrastructure/templates/polaris-init-job.yaml`
- **floe-polaris Package**: `packages/floe-polaris/README.md`
- **Platform Config Guide**: `docs/platform-config.md`
- **Apache Polaris Docs**: https://polaris.apache.org

## Implementation Workflow

1. ✅ Discover existing patterns in `packages/floe-polaris`
2. ✅ Verify Polaris availability (local or K8s)
3. ✅ Research unfamiliar features (WebSearch)
4. ✅ Use floe-polaris factory functions (`create_catalog`)
5. ✅ Follow two-tier configuration (credentials in `platform.yaml`)
6. ✅ Test DuckDB ATTACH (run `dbt debug`)
7. ✅ Verify table writes via DuckDB native Iceberg
8. ✅ Run integration tests (`pytest packages/floe-polaris/tests/integration`)

## Security Best Practices

- Use `SecretStr` for all credentials
- Never log secrets or credentials
- Use `PRINCIPAL_ROLE:<role_name>` (least-privilege scope)
- NEVER use `PRINCIPAL_ROLE:ALL` in production
- Rotate credentials via K8s secrets
- Enable audit logging in production

---

**Remember**: This skill provides research guidance. Always discover existing patterns first, verify runtime state, and validate against two-tier architecture.
