---
name: fabric-lakehouse-views-perf-remediate
description: Troubleshoot Microsoft Fabric materialized lake views (MLV) performance issues including slow refresh, incremental refresh failures, full refresh fallback, Spark job failures, lineage execution errors, data quality constraint violations, and optimal refresh configuration. Use when diagnosing MLV refresh duration, monitoring MLV runs in Monitor Hub, analyzing Spark logs for MLV failures, enabling change data feed (CDF), resolving delta table not found errors, or optimizing MLV query definitions for incremental refresh eligibility. Covers Spark SQL syntax, TBLPROPERTIES, PARTITIONED BY, CONSTRAINT CHECK ON MISMATCH DROP/FAIL, and custom environment configuration.
license: Complete terms in LICENSE.txt
---
# Fabric Materialized Lake Views Performance remediate

Diagnose and resolve performance issues with materialized lake views (MLVs) in Microsoft Fabric lakehouses. This skill covers refresh optimization, Spark job diagnostics, data quality constraint tuning, and lineage execution remediate.

## When to Use This Skill

- MLV refresh runs are taking longer than expected
- Incremental refresh is falling back to full refresh unexpectedly
- MLV lineage execution shows Failed or Skipped nodes
- Spark jobs for MLV refresh are failing with errors
- "Delta table not found" errors during MLV creation or refresh
- Data quality constraints causing unexpected pipeline failures
- Need to enable or verify optimal refresh configuration
- Custom Spark environment tuning for MLV workloads
- Monitoring and interpreting MLV run history

## Prerequisites

- Microsoft Fabric workspace with Lakehouse items
- Schema-enabled lakehouse (recommended for MLV support)
- Fabric notebook for executing Spark SQL commands
- Workspace Admin or Contributor role for scheduling and monitoring
- Access to Monitor Hub for viewing MLV run details

## Quick Diagnostics Checklist

Run through these checks in order when remediate MLV performance:

| Step | Check                 | Action                                                                    |
| ---- | --------------------- | ------------------------------------------------------------------------- |
| 1    | Identify refresh mode | Verify optimal refresh toggle is enabled in lineage view                  |
| 2    | Check CDF status      | Confirm `delta.enableChangeDataFeed=true` on ALL source tables          |
| 3    | Review query patterns | Ensure only supported SQL constructs are used (see supported expressions) |
| 4    | Inspect run history   | Open lineage view dropdown to see last 25 runs and their states           |
| 5    | Check node failures   | Click failed nodes in lineage to view error messages                      |
| 6    | Review Spark logs     | Follow Detailed Logs link to Monitor Hub for Spark error logs             |
| 7    | Validate data quality | Check if FAIL constraints are causing "delta table not found" errors      |
| 8    | Assess source data    | Determine if source has updates/deletes (forces full refresh)             |

## Step-by-Step Workflows

### Workflow 1: Diagnose Slow Refresh

1. **Determine current refresh strategy** - Navigate to Manage materialized lake views in the lakehouse ribbon. Check if Optimal refresh toggle is ON.
2. **Verify change data feed** - Run the diagnostic script to check CDF status on all source tables. See [scripts/check-cdf-status.sql](./scripts/check-cdf-status.sql).
3. **Check for unsupported expressions** - Review the MLV definition for constructs that force full refresh. See [Supported Expressions](#supported-expressions-for-incremental-refresh).
4. **Inspect source data patterns** - If source tables have UPDATE or DELETE operations, Fabric always performs full refresh regardless of CDF status.
5. **Review partition strategy** - Consider adding `PARTITIONED BY` to large MLVs to improve refresh parallelism.
6. **Attach custom environment** - Configure a custom Spark environment with optimized compute for heavy workloads. See [references/custom-environment-guide.md](./references/custom-environment-guide.md).

### Workflow 2: Resolve Failed Refresh Runs

1. **Open lineage view** - Navigate to Manage materialized lake views, select the failed run from the dropdown (last 25 runs available).
2. **Identify failed node** - Click the failed node in the lineage graph. Review the error message in the right-side panel.
3. **Access Spark logs** - Click the Detailed Logs link to navigate to Monitor Hub. Review Apache Spark error logs.
4. **Common failure patterns** - See [references/common-failure-patterns.md](./references/common-failure-patterns.md) for resolution steps.
5. **Retry or recreate** - For transient Spark failures, retry the run. For persistent errors, drop and recreate the MLV.

### Workflow 3: Enable Optimal Refresh

1. **Enable CDF on all source tables:**

```sql
ALTER TABLE bronze.customers SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
ALTER TABLE bronze.orders SET TBLPROPERTIES (delta.enableChangeDataFeed = true);
```

2. **Verify CDF is enabled:**

```sql
DESCRIBE DETAIL bronze.customers;
-- Check properties column for delta.enableChangeDataFeed=true
```

3. **Create MLV with CDF property:**

```sql
CREATE OR REPLACE MATERIALIZED LAKE VIEW silver.customer_orders
TBLPROPERTIES (delta.enableChangeDataFeed=true)
AS
SELECT 
    c.customerID,
    c.customerName,
    c.region,
    o.orderDate,
    o.orderAmount
FROM bronze.customers c INNER JOIN bronze.orders o
ON c.customerID = o.customerID;
```

4. **Enable optimal refresh toggle** - Navigate to Manage materialized lake views and verify the Optimal refresh toggle is ON (enabled by default).

## Supported Expressions for Incremental Refresh

MLVs using only these constructs qualify for incremental refresh:

| SQL Construct            | Notes                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| `SELECT`               | Only deterministic built-in functions. Non-deterministic and window functions force full refresh. |
| `FROM`                 | Standard table references                                                                         |
| `WHERE`                | Only deterministic built-in functions                                                             |
| `INNER JOIN`           | Supported for incremental                                                                         |
| `WITH` (CTE)           | Common table expressions supported                                                                |
| `UNION ALL`            | Supported                                                                                         |
| `CONSTRAINT ... CHECK` | Only deterministic built-in functions in constraint conditions                                    |

**Unsupported constructs that force full refresh:**

- `LEFT JOIN`, `RIGHT JOIN`, `FULL OUTER JOIN`
- Window functions (`ROW_NUMBER`, `RANK`, `LAG`, `LEAD`, etc.)
- Non-deterministic functions (`current_timestamp()`, `rand()`, etc.)
- Subqueries in `SELECT` or `WHERE`
- `GROUP BY` with `HAVING`
- `DISTINCT`
- User-defined functions (UDFs)

## Key Spark SQL Reference

### List All MLVs

```sql
SHOW MATERIALIZED LAKE VIEWS IN silver;
```

### View MLV Definition

```sql
SHOW CREATE MATERIALIZED LAKE VIEW silver.customer_orders;
```

### Force Full Refresh

```sql
REFRESH MATERIALIZED LAKE VIEW silver.customer_orders FULL;
```

### Drop and Recreate

```sql
DROP MATERIALIZED LAKE VIEW silver.customer_orders;

CREATE OR REPLACE MATERIALIZED LAKE VIEW silver.customer_orders
TBLPROPERTIES (delta.enableChangeDataFeed=true)
AS
SELECT ...;
```

## Known Issues and Limitations

| Issue                                     | Impact                               | Workaround                                                   |
| ----------------------------------------- | ------------------------------------ | ------------------------------------------------------------ |
| FAIL constraint + "delta table not found" | MLV creation or refresh fails        | Recreate MLV using DROP action instead of FAIL               |
| Schema names with ALL CAPS                | MLV creation fails                   | Use lowercase or mixed-case schema names                     |
| Session-level Spark properties            | Not applied during scheduled refresh | Set properties in custom environment instead                 |
| Delta time travel in MLV definition       | Not supported                        | Remove `VERSION AS OF` or `TIMESTAMP AS OF` from queries |
| DML statements on MLVs                    | Not supported                        | MLVs are read-only; modify source tables instead             |
| UDFs in SELECT                            | Not supported                        | Use built-in Spark SQL functions                             |
| Temporary views as MLV source             | Not supported                        | Reference base tables or other MLVs directly                 |
| Cross-lakehouse lineage                   | Not supported                        | Keep all related MLVs within same lakehouse                  |
| Updating data quality constraints         | Not supported                        | Drop and recreate the MLV with new constraints               |
| LIKE/regex in constraint conditions       | Not supported                        | Use simple comparison operators in constraints               |
| Service principal authentication          | Not supported for MLV APIs           | Use Microsoft Entra user authentication                      |
| Single schedule per lineage               | UI instability if exceeded           | Maintain only one active schedule per lineage                |
| South Central US region                   | Feature not available                | Use a workspace in a different region                        |

## Run States Reference

| State       | Meaning                                       | Action                                         |
| ----------- | --------------------------------------------- | ---------------------------------------------- |
| Completed   | All nodes executed successfully               | No action needed                               |
| Failed      | One or more nodes failed; child nodes skipped | Review failed node error, check Spark logs     |
| Skipped     | Previous run still in progress                | Wait for current run to complete, or cancel it |
| In Progress | Run started, not yet terminal                 | Monitor progress in lineage view               |
| Canceled    | Manually canceled from Monitor Hub            | Re-trigger if needed                           |

## remediate

| Symptom                                           | Likely Cause                              | Resolution                                                                                   |
| ------------------------------------------------- | ----------------------------------------- | -------------------------------------------------------------------------------------------- |
| Refresh always full, never incremental            | CDF not enabled on source tables          | Run `ALTER TABLE ... SET TBLPROPERTIES (delta.enableChangeDataFeed = true)` on ALL sources |
| Refresh always full despite CDF enabled           | Unsupported SQL constructs in MLV         | Review definition for window functions, LEFT JOIN, non-deterministic functions               |
| Refresh always full despite CDF and supported SQL | Source has UPDATE/DELETE operations       | Incremental only supports append-only; redesign ETL to be append-only or accept full refresh |
| "Delta table not found" on create                 | FAIL constraint issue                     | Recreate MLV without FAIL; use DROP action instead                                           |
| Node shows Skipped state                          | Parent node failed                        | Fix the parent node failure first                                                            |
| Schedule not running                              | Previous run still in progress            | Cancel the stuck run from Monitor Hub, or wait                                               |
| Environment not accessible                        | User lacks access to selected environment | Select an accessible environment from dropdown                                               |
| Deleted environment error                         | Associated environment was removed        | Choose a new environment in lineage settings                                                 |
| MLV names changed to lowercase                    | Expected behavior                         | MLV names are case-insensitive and stored as lowercase                                       |
| Workspace names with spaces cause errors          | Backtick syntax required                  | Use backtick notation:`` `My Workspace`.lakehouse.schema.view_name ``                        |

## References

- [Common Failure Patterns](./references/common-failure-patterns.md) - Detailed resolution for frequent MLV errors
- [Custom Environment Guide](./references/custom-environment-guide.md) - Spark environment tuning for MLV workloads
- [Monitoring Deep Dive](./references/monitoring-deep-dive.md) - Advanced Monitor Hub usage for MLV diagnostics
- [CDF Status Check Script](./scripts/check-cdf-status.sql) - T-SQL/Spark SQL script to audit CDF property
- [MLV Health Check Script](./scripts/mlv-health-check.sql) - Comprehensive MLV configuration audit
- [MLV Diagnostic Template](./templates/diagnostic-notebook.sql) - Notebook template for systematic MLV remediate
