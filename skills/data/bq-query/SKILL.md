---
name: bq-query
description: Design and execute BigQuery queries. Use for schema exploration, writing SQL from requirements, running queries, checking costs, or validating syntax.
---

# BigQuery Query

**Rules**: Follow [coding-standards](../../rules/coding-standards.md) for SQL naming and readability.

## Prerequisites

Check gcloud configuration before running queries:

```bash
gcloud config get-value project
```

- If authentication error: prompt user to run `gcloud auth login`, then resume
- If project unset: prompt user to run `gcloud config set project <PROJECT_ID>`

## Workflow

1. **Clarify requirements**: Understand what data is needed and why. If requirements are already in context, proceed to next step.

2. **Understand schema**: Explore available datasets. If schema is already in context, proceed to next step.

   ```bash
   bq ls project:dataset                           # List tables
   bq show --schema project:dataset.table          # Show table schema
   ```

3. **Design query**: Write SQL based on requirements and schema.
   - Use CTEs for readability
   - Use fully-qualified table names: `project.dataset.table`
   - Specify exact date ranges to limit scanned data
   - Filter partitioned tables by partition key
   - Avoid correlated subqueries (use JOINs/CTEs)
   - Filter early with CTEs before joining large tables
   - Use `LIMIT` for exploration queries

4. **Dry run**: Validate syntax and estimate cost

   ```bash
   bq query --use_legacy_sql=false --dry_run "SELECT ..."
   ```

   Cost: ~$5/TB. If >2GB, ask user before executing.

5. **Execute**: Run after successful dry run, once any required user confirmation has been given

   ```bash
   bq query --use_legacy_sql=false --format=csv "SELECT ..."
   ```

