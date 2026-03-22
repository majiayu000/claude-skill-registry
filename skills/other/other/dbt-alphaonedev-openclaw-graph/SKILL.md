---
name: dbt
cluster: data-engineering
description: "dbt is a tool for transforming data in warehouses using SQL-based models, enabling testing and documentation."
tags: ["dbt","sql","data-modeling"]
dependencies: []
composes: []
similar_to: []
called_by: []
authorization_required: false
scope: general
model_hint: claude-sonnet
embedding_hint: "dbt data build tool sql data modeling warehouse transformation testing documentation"
---

## Purpose

dbt (data build tool) is a command-line tool for transforming data in warehouses using SQL-based models. It enables developers to write, test, and document data transformations, ensuring reliable ETL processes.

## When to Use

Use dbt when building SQL data models for warehouses like Snowflake, BigQuery, or Redshift. Apply it for incremental data loading, schema evolution, or automated testing in data pipelines. Avoid it for real-time processing or non-SQL data sources; opt for dbt when you need version-controlled SQL code with built-in validation.

## Key Capabilities

- Define reusable SQL models in .sql files with Jinja templating for dynamic queries (e.g., `{{ var('date') }}` for parameter injection).
- Run automated tests like schema checks or custom assertions via YAML configs (e.g., `not_null` or `unique` tests).
- Generate documentation automatically from models using `dbt docs generate`, outputting HTML with model dependencies and descriptions.
- Handle incremental models with the `is_incremental()` macro to process only new data, reducing warehouse load.
- Support for macros and packages via dbt hub for extending functionality, like adding utility functions.

## Usage Patterns

Follow this workflow: 1) Initialize a project with `dbt init`. 2) Write models in the `models/` directory as SQL files. 3) Configure connections in `profiles.yml`. 4) Run and test models iteratively. 5) Use seeds for static data and snapshots for slowly changing dimensions. For CI/CD, integrate dbt into scripts: run `dbt run` in a Docker container with mounted volumes. Always specify targets like `--target dev` to switch environments.

## Common Commands/API

dbt is primarily CLI-based; use it directly or via scripts. Key commands:

- `dbt init --name project_name`: Create a new project; specify a directory with `--project-dir /path`.
  
  Example:
  ```
  dbt init --name sales_dbt --project-dir ./sales_project
  ```

- `dbt run --models model_name --select tag:nightly`: Execute models; use `--full-refresh` to rebuild all data.

  Example:
  ```
  dbt run --models orders --target prod --threads 8
  ```

- `dbt test --models model_name`: Run tests; add flags like `--store-failures` to log errors.

  Example:
  ```
  dbt test --select source:raw_data
  ```

- `dbt docs generate && dbt docs serve`: Build and serve documentation; integrate with CI for auto-deployment.
- For API-like usage, wrap dbt in Python scripts using subprocess: `subprocess.run(['dbt', 'run', '--models', 'my_model'])`. Use environment variables for profiles, e.g., set `$DBT_PROFILES_DIR` to `/path/to/profiles.yml`.

## Integration Notes

Integrate dbt with warehouses by configuring `profiles.yml`. For Snowflake, use:

```
your_profile:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: your_account
      user: your_user
      password: "{{ env_var('SNOWFLAKE_PASSWORD') }}"
      database: your_db
      schema: your_schema
```

For BigQuery, specify:

```
bigquery_profile:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: your-gcp-project
      dataset: your_dataset
      keyfile: "{{ env_var('GOOGLE_KEYFILE') }}"
```

Use env vars for secrets (e.g., `export SNOWFLAKE_PASSWORD=your_key`). Integrate with Git for version control, and tools like Airflow for orchestration: call `dbt run` as a task. For VS Code, install the dbt extension for syntax highlighting.

## Error Handling

Handle errors by first running `dbt debug` to validate connections and profiles. For SQL compilation errors, check model files for syntax (e.g., missing semicolons) and use `dbt compile` to preview. If tests fail, inspect output logs for details like "column not found"; fix by updating schemas in `.yml` files. Use `--fail-fast` in `dbt run` to halt on first error. Common patterns: wrap commands in try-catch for scripts (e.g., in Python: `try: subprocess.run(['dbt', 'run']) except Exception as e: log_error(e)`). For authentication failures, ensure env vars like `$SNOWFLAKE_PASSWORD` are set; test with `dbt run --target dev --log-level debug`.

## Concrete Usage Examples

1. Building a simple incremental model: Create `models/orders.sql` with:
   ```
   {{ config(materialized='incremental') }}
   select order_id, customer_id from source_orders
   where order_date > (select max(order_date) from {{ this }})
   ```
   Then run: `dbt run --models orders --target dev`. This processes only new orders.

2. Running and testing a data model: Define a test in `models/schema.yml`:
   ```
   models:
     - name: customers
       columns:
         - name: customer_id
           tests:
             - unique
             - not_null
   ```
   Execute: `dbt run --models customers && dbt test --models customers`. This builds the model and verifies no duplicates or nulls.

## Graph Relationships

- Cluster: data-engineering (connects to skills like SQL and ETL tools).
- Tags: dbt, sql, data-modeling (links to related tags in other skills, e.g., SQL for query optimization).
- Relationships: Depends on warehouse connectors; integrates with data pipelines in data-engineering cluster.
