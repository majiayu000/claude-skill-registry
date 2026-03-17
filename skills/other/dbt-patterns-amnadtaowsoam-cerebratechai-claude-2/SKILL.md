---
name: dbt Patterns
description: Comprehensive guide to dbt (data build tool) patterns, modeling best practices, testing strategies, and production workflows for modern data transformation
---

# dbt Patterns

## What is dbt?

**dbt (data build tool):** SQL-first transformation tool that enables analytics engineers to transform data in the warehouse using SELECT statements.

### Core Concept
```
Raw Data (Extract & Load) → dbt (Transform) → Analytics-Ready Data

Traditional ETL: Extract → Transform → Load
Modern ELT: Extract → Load → Transform (with dbt)
```

### Why dbt?
- **Version control:** SQL as code (Git)
- **Testing:** Built-in data quality tests
- **Documentation:** Auto-generated docs
- **Modularity:** Reusable models
- **Lineage:** Visual data lineage
- **Collaboration:** Team workflows

---

## dbt Project Structure

### Standard Layout
```
my_dbt_project/
├── dbt_project.yml          # Project configuration
├── profiles.yml             # Connection profiles
├── models/                  # SQL models
│   ├── staging/            # Raw data cleaning
│   ├── intermediate/       # Business logic
│   └── marts/              # Final analytics tables
├── tests/                   # Custom tests
├── macros/                  # Reusable SQL
├── seeds/                   # CSV reference data
├── snapshots/               # SCD Type 2
└── analyses/                # Ad-hoc queries
```

### dbt_project.yml
```yaml
name: 'my_project'
version: '1.0.0'
config-version: 2

profile: 'my_profile'

model-paths: ["models"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

models:
  my_project:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: analytics
```

---

## Model Layers (Staging → Intermediate → Marts)

### Staging Layer
**Purpose:** Clean and standardize raw data

**Pattern:**
```sql
-- models/staging/stg_orders.sql
with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        id as order_id,
        user_id,
        created_at as order_created_at,
        status as order_status,
        total_amount
    from source
)

select * from renamed
```

**Best Practices:**
- One staging model per source table
- Rename columns to consistent naming
- Cast data types
- No business logic
- Materialized as views (lightweight)

### Intermediate Layer
**Purpose:** Business logic and transformations

**Pattern:**
```sql
-- models/intermediate/int_orders_with_customer.sql
with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

joined as (
    select
        orders.*,
        customers.customer_name,
        customers.customer_segment
    from orders
    left join customers
        on orders.user_id = customers.customer_id
)

select * from joined
```

**Best Practices:**
- Complex joins
- Business logic
- Calculations
- Materialized as ephemeral (not persisted)

### Marts Layer
**Purpose:** Final analytics-ready tables

**Pattern:**
```sql
-- models/marts/fct_orders.sql
with orders as (
    select * from {{ ref('int_orders_with_customer') }}
),

aggregated as (
    select
        order_id,
        user_id,
        customer_name,
        order_created_at,
        order_status,
        total_amount,
        case
            when order_status = 'completed' then total_amount
            else 0
        end as completed_revenue
    from orders
)

select * from aggregated
```

**Best Practices:**
- Business-friendly naming
- Denormalized for analytics
- Materialized as tables (fast queries)
- Documented

---

## Naming Conventions

### Model Naming
```
Staging:      stg_<source>_<table>
              stg_salesforce_accounts
              stg_stripe_payments

Intermediate: int_<entity>_<verb>
              int_orders_joined
              int_customers_enriched

Facts:        fct_<entity>
              fct_orders
              fct_revenue

Dimensions:   dim_<entity>
              dim_customers
              dim_products
```

### Column Naming
```
IDs:          <entity>_id
              customer_id, order_id

Dates:        <entity>_<verb>_at
              order_created_at, customer_updated_at

Booleans:     is_<condition> or has_<condition>
              is_active, has_subscription

Amounts:      <entity>_amount
              order_amount, refund_amount
```

---

## Materializations

### View
```sql
{{ config(materialized='view') }}

select * from {{ ref('stg_orders') }}
```
- **Pros:** Always fresh, no storage
- **Cons:** Slow queries (recomputed each time)
- **Use for:** Staging models, rarely queried

### Table
```sql
{{ config(materialized='table') }}

select * from {{ ref('fct_orders') }}
```
- **Pros:** Fast queries
- **Cons:** Storage cost, stale data
- **Use for:** Marts, frequently queried

### Incremental
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select * from {{ ref('stg_orders') }}

{% if is_incremental() %}
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```
- **Pros:** Fast builds, handles large data
- **Cons:** Complex logic
- **Use for:** Large fact tables

### Ephemeral
```sql
{{ config(materialized='ephemeral') }}

select * from {{ ref('stg_orders') }}
```
- **Pros:** No storage, CTE in downstream models
- **Cons:** Recomputed in each downstream model
- **Use for:** Intermediate models

---

## Testing

### Schema Tests
```yaml
# models/schema.yml
version: 2

models:
  - name: fct_orders
    description: "Order facts table"
    columns:
      - name: order_id
        description: "Unique order identifier"
        tests:
          - unique
          - not_null
      
      - name: user_id
        description: "Customer who placed order"
        tests:
          - not_null
          - relationships:
              to: ref('dim_customers')
              field: customer_id
      
      - name: order_status
        tests:
          - accepted_values:
              values: ['pending', 'completed', 'cancelled']
      
      - name: total_amount
        tests:
          - not_null
          - dbt_utils.expression_is_true:
              expression: ">= 0"
```

### Custom Tests
```sql
-- tests/assert_positive_revenue.sql
select *
from {{ ref('fct_orders') }}
where total_amount < 0
```

### Test Types
- **unique:** No duplicates
- **not_null:** No nulls
- **accepted_values:** Value in list
- **relationships:** Foreign key check
- **custom:** SQL query returns 0 rows

---

## Macros

### Reusable SQL
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    ({{ column_name }} / 100.0)::decimal(10,2)
{% endmacro %}
```

**Usage:**
```sql
select
    order_id,
    {{ cents_to_dollars('total_amount_cents') }} as total_amount_dollars
from {{ ref('stg_orders') }}
```

### Common Macros
```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) %}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{% endmacro %}
```

---

## Sources

### Defining Sources
```yaml
# models/staging/sources.yml
version: 2

sources:
  - name: raw
    database: analytics_db
    schema: raw_data
    tables:
      - name: orders
        description: "Raw orders from production DB"
        columns:
          - name: id
            tests:
              - unique
              - not_null
        
        freshness:
          warn_after: {count: 12, period: hour}
          error_after: {count: 24, period: hour}
        
        loaded_at_field: _loaded_at
```

### Using Sources
```sql
select * from {{ source('raw', 'orders') }}
```

### Source Freshness
```bash
dbt source freshness
```

---

## Documentation

### Model Documentation
```yaml
# models/schema.yml
version: 2

models:
  - name: fct_orders
    description: |
      Order facts table containing all orders with customer information.
      
      This table is updated daily at 2 AM UTC.
      
      **Business Rules:**
      - Only includes orders with status 'completed' or 'pending'
      - Cancelled orders are excluded
      
    columns:
      - name: order_id
        description: "Unique identifier for each order"
      
      - name: total_amount
        description: "Total order amount in dollars"
```

### Generate Docs
```bash
dbt docs generate
dbt docs serve
```

**Output:** Interactive documentation website with:
- Model descriptions
- Column descriptions
- Data lineage (DAG)
- Source freshness

---

## Snapshots (SCD Type 2)

### Snapshot Configuration
```sql
-- snapshots/customers_snapshot.sql
{% snapshot customers_snapshot %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at'
    )
}}

select * from {{ source('raw', 'customers') }}

{% endsnapshot %}
```

### Run Snapshots
```bash
dbt snapshot
```

### Output
```
customer_id | name  | updated_at | dbt_valid_from | dbt_valid_to | dbt_scd_id
1           | John  | 2024-01-01 | 2024-01-01     | 2024-01-15   | abc123
1           | John  | 2024-01-15 | 2024-01-15     | null         | def456
```

---

## Incremental Models

### Basic Incremental
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id'
) }}

select
    order_id,
    user_id,
    order_created_at,
    total_amount
from {{ ref('stg_orders') }}

{% if is_incremental() %}
    -- Only process new/updated records
    where order_created_at > (select max(order_created_at) from {{ this }})
{% endif %}
```

### Incremental with Delete+Insert
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='delete+insert'
) }}
```

### Incremental with Merge
```sql
{{ config(
    materialized='incremental',
    unique_key='order_id',
    incremental_strategy='merge',
    merge_update_columns=['order_status', 'total_amount']
) }}
```

---

## Packages

### Installing Packages
```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.0
  
  - package: calogica/dbt_expectations
    version: 0.9.0
  
  - package: dbt-labs/codegen
    version: 0.11.0
```

```bash
dbt deps
```

### Using Packages
```sql
-- dbt_utils
select
    {{ dbt_utils.surrogate_key(['order_id', 'user_id']) }} as unique_key,
    *
from {{ ref('stg_orders') }}

-- dbt_expectations
tests:
  - dbt_expectations.expect_column_values_to_be_between:
      min_value: 0
      max_value: 1000000
```

---

## Production Workflows

### Development Workflow
```bash
# 1. Create feature branch
git checkout -b feature/new-model

# 2. Develop model
# Edit models/marts/fct_new_model.sql

# 3. Run model
dbt run --select fct_new_model

# 4. Test model
dbt test --select fct_new_model

# 5. Document model
# Edit models/schema.yml

# 6. Commit and push
git add .
git commit -m "Add new model"
git push origin feature/new-model

# 7. Create PR
# Review, approve, merge
```

### CI/CD Pipeline
```yaml
# .github/workflows/dbt_ci.yml
name: dbt CI

on: [pull_request]

jobs:
  dbt_run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dbt
        run: pip install dbt-snowflake
      
      - name: Run dbt
        run: |
          dbt deps
          dbt run --select state:modified+ --defer --state ./prod_manifest
          dbt test --select state:modified+ --defer --state ./prod_manifest
```

### Production Deployment
```bash
# Daily production run
dbt run --target prod
dbt test --target prod
dbt source freshness --target prod
```

---

## Performance Optimization

### Optimize Queries
```sql
-- Bad: Multiple CTEs with same source
with orders_1 as (
    select * from {{ ref('stg_orders') }}
    where status = 'completed'
),
orders_2 as (
    select * from {{ ref('stg_orders') }}
    where status = 'pending'
)

-- Good: Single CTE, filter later
with orders as (
    select * from {{ ref('stg_orders') }}
    where status in ('completed', 'pending')
),
completed_orders as (
    select * from orders where status = 'completed'
),
pending_orders as (
    select * from orders where status = 'pending'
)
```

### Use Incremental Models
```sql
-- For large tables (millions of rows)
{{ config(materialized='incremental') }}
```

### Partition Tables
```sql
{{ config(
    materialized='table',
    partition_by={
        "field": "order_date",
        "data_type": "date",
        "granularity": "day"
    }
) }}
```

---

## Best Practices

### 1. One Model Per File
```
✓ models/staging/stg_orders.sql
✗ models/staging/all_staging_models.sql
```

### 2. Use CTEs, Not Subqueries
```sql
-- Good
with orders as (
    select * from {{ ref('stg_orders') }}
)
select * from orders

-- Bad
select * from (
    select * from {{ ref('stg_orders') }}
) as orders
```

### 3. Explicit Column Selection
```sql
-- Good
select
    order_id,
    user_id,
    total_amount
from {{ ref('stg_orders') }}

-- Bad
select * from {{ ref('stg_orders') }}
```

### 4. Test Everything
```yaml
# Every model should have tests
models:
  - name: fct_orders
    columns:
      - name: order_id
        tests: [unique, not_null]
```

### 5. Document Everything
```yaml
# Every model and column should have description
models:
  - name: fct_orders
    description: "Order facts table"
    columns:
      - name: order_id
        description: "Unique order ID"
```

---

## Common Patterns

### Slowly Changing Dimensions (SCD)
```sql
-- Type 1: Overwrite
{{ config(materialized='table') }}
select * from {{ ref('stg_customers') }}

-- Type 2: Historical tracking
{% snapshot customers_snapshot %}
{{ config(strategy='timestamp', updated_at='updated_at') }}
select * from {{ ref('stg_customers') }}
{% endsnapshot %}
```

### Fact Tables
```sql
-- Transactional facts
{{ config(materialized='incremental', unique_key='order_id') }}
select
    order_id,
    customer_id,
    product_id,
    order_date,
    quantity,
    amount
from {{ ref('stg_orders') }}
```

### Dimension Tables
```sql
-- Dimension table
{{ config(materialized='table') }}
select
    customer_id,
    customer_name,
    customer_segment,
    customer_region
from {{ ref('stg_customers') }}
```

---

## Troubleshooting

### Common Errors

**Compilation Error:**
```
Compilation Error in model fct_orders
  Model 'stg_orders' not found
```
**Fix:** Check model name, ensure it exists

**Test Failure:**
```
Failure in test unique_fct_orders_order_id
  Got 5 results, expected 0
```
**Fix:** Investigate duplicate order_ids

**Freshness Error:**
```
Source 'raw.orders' is stale (loaded 25 hours ago)
```
**Fix:** Check ETL pipeline, data loading

---

## Summary

**dbt:** SQL-first transformation tool

**Layers:**
- Staging: Clean raw data
- Intermediate: Business logic
- Marts: Analytics-ready

**Materializations:**
- View: Always fresh, slow
- Table: Fast, stale
- Incremental: Large data
- Ephemeral: No storage

**Testing:**
- unique, not_null, accepted_values, relationships
- Custom SQL tests

**Best Practices:**
- One model per file
- Use CTEs
- Test everything
- Document everything
- Version control

**Workflow:**
- Develop → Test → Document → PR → Merge → Deploy
