---
name: dbt
description: |
  dbt (data build tool) transforms data in your warehouse using SQL SELECT statements.
  Learn project setup, models, tests, documentation, incremental materializations,
  and integration with data warehouses like PostgreSQL, BigQuery, and Snowflake.
license: Apache-2.0
compatibility: 'macos, linux, windows'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - dbt
    - data-transformation
    - sql
    - data-warehouse
    - analytics
---

# dbt

dbt lets analytics engineers transform data by writing SQL SELECT statements. It handles materialization (tables, views, incremental), testing, documentation, and lineage tracking.

## Installation

```bash
# Install dbt with PostgreSQL adapter
pip install dbt-postgres

# Or with other adapters
pip install dbt-bigquery
pip install dbt-snowflake

# Initialize a new project
dbt init my_project
cd my_project
```

## Project Structure

```text
my_project/
├── dbt_project.yml      # Project configuration
├── profiles.yml         # Connection profiles (usually in ~/.dbt/)
├── models/
│   ├── staging/         # Raw data cleaning
│   │   ├── _staging.yml # Schema + tests for staging models
│   │   ├── stg_users.sql
│   │   └── stg_orders.sql
│   └── marts/           # Business logic
│       ├── _marts.yml
│       └── fct_revenue.sql
├── tests/               # Custom data tests
├── macros/              # Reusable SQL macros
└── seeds/               # CSV files to load
```

## Configuration

```yaml
# dbt_project.yml: Project configuration
name: my_project
version: '1.0.0'
profile: my_project

models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    marts:
      +materialized: table
      +schema: analytics
```

```yaml
# profiles.yml: Database connection (~/.dbt/profiles.yml)
my_project:
  target: dev
  outputs:
    dev:
      type: postgres
      host: localhost
      port: 5432
      user: analyst
      password: "{{ env_var('DBT_PASSWORD') }}"
      dbname: analytics
      schema: dev
      threads: 4
    prod:
      type: postgres
      host: prod-db.example.com
      port: 5432
      user: dbt_prod
      password: "{{ env_var('DBT_PROD_PASSWORD') }}"
      dbname: analytics
      schema: public
      threads: 8
```

## Staging Models

```sql
-- models/staging/stg_users.sql: Clean raw user data
WITH source AS (
    SELECT * FROM {{ source('raw', 'users') }}
),

cleaned AS (
    SELECT
        id AS user_id,
        LOWER(TRIM(email)) AS email,
        name,
        created_at::timestamp AS signed_up_at,
        CASE WHEN status = 'active' THEN TRUE ELSE FALSE END AS is_active
    FROM source
    WHERE email IS NOT NULL
)

SELECT * FROM cleaned
```

```sql
-- models/staging/stg_orders.sql: Clean raw order data
SELECT
    id AS order_id,
    user_id,
    amount_cents / 100.0 AS amount,
    status,
    created_at::timestamp AS ordered_at
FROM {{ source('raw', 'orders') }}
WHERE status != 'test'
```

## Mart Models

```sql
-- models/marts/fct_revenue.sql: Revenue fact table
{{
    config(
        materialized='incremental',
        unique_key='order_date',
        on_schema_change='sync_all_columns'
    )
}}

WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
    {% if is_incremental() %}
    WHERE ordered_at > (SELECT MAX(order_date) FROM {{ this }})
    {% endif %}
),

daily AS (
    SELECT
        DATE_TRUNC('day', ordered_at)::date AS order_date,
        COUNT(*) AS total_orders,
        COUNT(DISTINCT user_id) AS unique_customers,
        SUM(amount) AS total_revenue,
        AVG(amount) AS avg_order_value
    FROM orders
    WHERE status = 'completed'
    GROUP BY 1
)

SELECT * FROM daily
```

## Schema and Tests

```yaml
# models/staging/_staging.yml: Define sources, columns, and tests
version: 2

sources:
  - name: raw
    schema: public
    tables:
      - name: users
        loaded_at_field: created_at
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
      - name: orders

models:
  - name: stg_users
    description: Cleaned user data
    columns:
      - name: user_id
        tests: [unique, not_null]
      - name: email
        tests: [unique, not_null]

  - name: stg_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
      - name: status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled', 'refunded']
```

## CLI Commands

```bash
# commands.sh: Common dbt CLI commands
# Run all models
dbt run

# Run specific model and its upstream dependencies
dbt run --select +fct_revenue

# Run tests
dbt test

# Generate and serve documentation
dbt docs generate
dbt docs serve --port 8081

# Check source freshness
dbt source freshness

# Full build (run + test + snapshot)
dbt build

# Run against production
dbt run --target prod
```

## Macros

```sql
-- macros/cents_to_dollars.sql: Reusable macro for currency conversion
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::numeric(10,2)
{% endmacro %}

-- Usage in a model: SELECT {{ cents_to_dollars('amount_cents') }} AS amount
```
