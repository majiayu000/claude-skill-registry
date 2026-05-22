---
name: data-governance
description: Data lineage, cataloging, access control, and compliance.
---

# Data Governance

## Data Lineage

Track data flow from source to consumption:

```
Source Systems → Raw Layer → Staging → Marts → Reports
     │              │           │        │        │
     └──────────────┴───────────┴────────┴────────┘
                    Lineage Graph
```

### dbt Lineage

```bash
dbt docs generate
dbt docs serve
# View DAG at http://localhost:8080
```

### OpenLineage

```python
from openlineage.client import OpenLineageClient

client = OpenLineageClient(url="http://marquez:5000")

# Emit lineage events
client.emit(run_event)
```

## Data Catalog

### Metadata to Track

| Category | Examples |
|----------|----------|
| **Technical** | Schema, types, partitions |
| **Business** | Description, owner, SLA |
| **Operational** | Freshness, quality scores |
| **Access** | PII classification, roles |

### dbt Documentation

```yaml
models:
  - name: dim_customer
    description: "Customer master data"
    meta:
      owner: "data-team"
      pii: true
      freshness_sla: "24h"
    columns:
      - name: email
        description: "Customer email"
        meta:
          pii: true
          masking: "hash"
```

## Access Control

### Column-Level Security

```sql
-- Snowflake
CREATE MASKING POLICY email_mask AS (val STRING)
RETURNS STRING ->
  CASE
    WHEN CURRENT_ROLE() IN ('ADMIN') THEN val
    ELSE '***@***.com'
  END;

ALTER TABLE customers MODIFY COLUMN email
SET MASKING POLICY email_mask;
```

### Row-Level Security

```sql
-- Snowflake
CREATE ROW ACCESS POLICY region_policy AS (region VARCHAR)
RETURNS BOOLEAN ->
  region = CURRENT_ROLE();
```

## Compliance

- **GDPR** - Right to deletion, data export
- **CCPA** - Consumer data rights
- **SOC2** - Access logging, encryption
- **HIPAA** - PHI protection
