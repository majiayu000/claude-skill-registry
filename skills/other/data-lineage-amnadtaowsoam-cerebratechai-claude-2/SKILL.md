---
name: Data Lineage
description: Mapping the flow of data from source to destination for transparency, impact analysis, and troubleshooting.
---

# Data Lineage

## Overview

Data Lineage is the process of tracking what happens to data as it flows through various stages—from its original source, through transformations (ETL), to its final destination (dashboards, ML models, or external APIs). Lineage provides the "genealogy" of a dataset.

**Core Principle**: "To trust the data, you must know where it came from and how it changed."

## Best Practices

- Capture lineage automatically at orchestration boundaries (Airflow, Spark, dbt) instead of manual docs.
- Standardize dataset naming (`namespace` + `name`) and keep it stable across environments.
- Enrich events with run context (job version/git SHA, run ID, owner/team, and environment).
- Prioritize column-level lineage for PII and business-critical metrics; keep table-level for everything else.
- Make lineage actionable: use it in schema change reviews and incident RCA/impact analysis.

## Quick Start

1. Choose a lineage standard/tooling (e.g., OpenLineage + Marquez/DataHub).
2. Instrument your orchestrator to emit lineage events for each job run.
3. Register stable dataset identifiers (warehouse tables, S3 paths, Kafka topics).
4. Visualize lineage and validate it during schema changes.
5. Alert on missing lineage for critical pipelines (treat as a reliability issue).

```python
from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4


def build_openlineage_run_event(
    *,
    job_namespace: str,
    job_name: str,
    input_dataset: tuple[str, str],
    output_dataset: tuple[str, str],
    event_type: str = "COMPLETE",
) -> dict:
    event_time = datetime.now(tz=timezone.utc).isoformat()
    run_id = str(uuid4())
    input_ns, input_name = input_dataset
    output_ns, output_name = output_dataset

    return {
        "eventType": event_type,
        "eventTime": event_time,
        "run": {"runId": run_id},
        "job": {"namespace": job_namespace, "name": job_name},
        "inputs": [{"namespace": input_ns, "name": input_name}],
        "outputs": [{"namespace": output_ns, "name": output_name}],
        "producer": "https://openlineage.io/",
        "schemaURL": "https://openlineage.io/spec/1-0-0/OpenLineage.json",
    }


if __name__ == "__main__":
    event = build_openlineage_run_event(
        job_namespace="prod-etl",
        job_name="clean_orders_job",
        input_dataset=("db_raw", "raw_orders"),
        output_dataset=("db_prod", "clean_orders"),
    )
    print(json.dumps(event, indent=2))
```

---

## 1. Why Data Lineage Matters

| Benefit | Use Case |
| :--- | :--- |
| **Root Cause Analysis** | A dashboard is wrong; which upstream table caused the error? |
| **Impact Analysis** | I want to delete a column; will it break any downstream reports? |
| **Compliance** | Where exactly does PII (SSN, Email) flow in our system? (GDPR/CCPA) |
| **Data Discovery** | How is the `active_users` metric actually calculated? |

---

## 2. Types of Data Lineage

1.  **Table-Level Lineage**: Shows how data moves between tables (e.g., `raw_orders` -> `clean_orders` -> `orders_summary`).
2.  **Column-Level Lineage**: Shows how a specific field is transformed (e.g., `first_name` + `last_name` -> `full_name`).
3.  **Business Lineage**: High-level view showing how data moves across departments or broad systems (SaaS -> Data Warehouse -> BI Dashboard).

---

## 3. Technical Implementation

### A. SQL Parsing
Reading SQL scripts to identify `INSERT INTO... SELECT FROM` patterns.
*   **Tool**: `sqlglot` or `sqlfluff`.

### B. OpenLineage Standard
OpenLineage is an open standard for lineage metadata collection. It uses "Jobs" and "Datasets" to represent relationships.

```json
{
  "eventTime": "2024-01-15T12:00:00Z",
  "job": { "namespace": "prod-etl", "name": "clean_orders_job" },
  "inputs": [ { "namespace": "db_raw", "name": "raw_orders" } ],
  "outputs": [ { "namespace": "db_prod", "name": "clean_orders" } ]
}
```

### C. dbt Lineage
dbt automatically generates a lineage graph (the "DAG") from your project dependencies.

```bash
# Generate and serve the lineage documentation
dbt docs generate
dbt docs serve
```

---

## 4. Tools for Data Lineage

| Tool | Focus | Best For |
| :--- | :--- | :--- |
| **OpenLineage** | Standard | Orchestrators like Airflow, Spark, dbt. |
| **Amundsen** | Data Discovery | Built by Lyft; focusing on user-collaborative search. |
| **DataHub** | Metadata Platform | Built by LinkedIn; extensive lineage and ownership tracking. |
| **Monte Carlo** | Observability | Automatically infers lineage from query logs. |
| **Marquez** | Metadata Store | Reference implementation for OpenLineage. |

---

## 5. Root Cause Analysis (RCA) with Lineage

Imagine a "Monthly Revenue" dashboard shows $0.

1.  **Check Output**: Dashboard uses `gold_monthly_revenue` table.
2.  **Trace Upstream**: `gold_monthly_revenue` is populated from `silver_orders`.
3.  **Investigate Link**: `silver_orders` is 10GB but usually 50GB.
4.  **Identify Source**: `silver_orders` gets data from `raw_stripe_api`.
5.  **Conclusion**: The Stripe API extraction job failed yesterday, causing missing data downstream.

---

## 6. Impact Analysis Workflow

*Before* running `DROP COLUMN ccv` in a production database:

1.  **Query Lineage Tool**: "Search for usages of `transactions.ccv`."
2.  **Identify Consumers**: Discovery shows it is used by the `fraud_detection_model`.
3.  **Coordinate**: Contact the Fraud Team lead to ensure the model no longer needs the column.
4.  **Action**: Proceed with the "Tombstoning" strategy (see `schema-management`).

---

## 7. Tracking PII Flow

Lineage is the primary tool for privacy compliance. You can "Tag" a source field as `PII` and the lineage tool will propagate that tag down the flow.

*   **Source**: `users.email` (Tagged: **PII**)
*   **Transformation**: `LOWER(email)` (Propagated: **PII**)
*   **Target**: `marketing_leads.contact` (Auto-Propagated: **PII**)

This allows security teams to identify which S3 buckets or BigQuery datasets require encryption at rest without manual audits.

---

## 8. Automated vs. Manual Lineage

*   **Automated**: Captured from query logs or orchestrator (Preferred). Low maintenance, 100% accurate.
*   **Manual**: Documented in a Wiki. High maintenance, quickly becomes outdated, unreliable.

---

## 9. Data Lineage Checklist

- [ ] **Completeness**: Does our lineage cover cross-system boundaries (e.g., Salesforce to Snowflake)?
- [ ] **Granularity**: Do we have column-level lineage for our most sensitive data?
- [ ] **Orchestration**: Is lineage captured automatically from every Airflow/dbt run?
- [ ] **Impact Analysis**: Is there a standard process to check lineage before a schema change?
- [ ] **Ownership**: Does every table in the lineage graph have a defined team/individual owner?

---

## Related Skills
* `43-data-reliability/data-contracts`
* `43-data-reliability/schema-management`
* `44-ai-governance/ai-compliance`
