---
name: dbt-coder
description: dbt (data build tool) patterns for model organization, incremental strategies, and testing.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# dbt-Coder

Patterns for dbt (data build tool) transform layer development.

## Project Structure

```
my_dbt_project/
├── dbt_project.yml
├── profiles.yml
├── models/
│   ├── staging/          # 1:1 with sources, light transforms
│   │   ├── stg_orders.sql
│   │   └── _staging.yml
│   ├── intermediate/     # Joins, business logic
│   │   └── int_orders_enriched.sql
│   └── marts/            # Final consumption layer
│       ├── finance/
│       │   └── fct_revenue.sql
│       └── marketing/
│           └── dim_customers.sql
├── seeds/                # Static lookup data
├── snapshots/            # SCD Type 2
├── macros/               # Reusable SQL
└── tests/                # Custom tests
```

## dbt_project.yml

```yaml
name: 'my_project'
version: '1.0.0'
config-version: 2

profile: 'my_project'

model-paths: ["models"]
seed-paths: ["seeds"]
test-paths: ["tests"]
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
      +schema: marts
```

## Staging Models

```sql
-- models/staging/stg_orders.sql
-- Naming: stg_<source>_<entity>

with source as (
    select * from {{ source('raw', 'orders') }}
),

renamed as (
    select
        -- Rename to consistent naming
        id as order_id,
        customer_id,
        order_date,
        total_amount as order_total,

        -- Type casting
        cast(status as varchar(50)) as order_status,

        -- Timestamps
        created_at,
        updated_at
    from source
)

select * from renamed
```

## Source Definition

```yaml
# models/staging/_sources.yml
version: 2

sources:
  - name: raw
    database: raw_db
    schema: public
    freshness:
      warn_after: {count: 12, period: hour}
      error_after: {count: 24, period: hour}
    tables:
      - name: orders
        identifier: orders_table
        columns:
          - name: id
            tests:
              - unique
              - not_null
      - name: customers
```

## Intermediate Models

```sql
-- models/intermediate/int_orders_enriched.sql
-- Join staging models, apply business logic

with orders as (
    select * from {{ ref('stg_orders') }}
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    o.order_id,
    o.order_date,
    o.order_total,

    c.customer_id,
    c.customer_name,
    c.customer_segment,

    -- Business logic
    case
        when o.order_total >= 1000 then 'high_value'
        when o.order_total >= 100 then 'medium_value'
        else 'low_value'
    end as order_tier

from orders o
left join customers c on o.customer_id = c.customer_id
```

## Mart Models

```sql
-- models/marts/finance/fct_revenue.sql
-- Final aggregated fact table

{{ config(
    materialized='table',
    partition_by={
      "field": "order_date",
      "data_type": "date",
      "granularity": "month"
    }
) }}

with orders as (
    select * from {{ ref('int_orders_enriched') }}
)

select
    date_trunc('day', order_date) as revenue_date,
    customer_segment,
    order_tier,
    count(*) as order_count,
    sum(order_total) as total_revenue,
    avg(order_total) as avg_order_value
from orders
group by 1, 2, 3
```

## Incremental Models

```sql
-- models/marts/fct_events.sql
{{ config(
    materialized='incremental',
    unique_key='event_id',
    incremental_strategy='merge'  -- or 'delete+insert', 'append'
) }}

select
    event_id,
    user_id,
    event_type,
    event_timestamp,
    properties
from {{ source('raw', 'events') }}

{% if is_incremental() %}
    -- Only new/updated rows since last run
    where event_timestamp > (select max(event_timestamp) from {{ this }})
{% endif %}
```

## Snapshots (SCD Type 2)

```sql
-- snapshots/snap_customers.sql
{% snapshot snap_customers %}

{{
    config(
      target_schema='snapshots',
      unique_key='customer_id',
      strategy='timestamp',
      updated_at='updated_at',
    )
}}

select * from {{ source('raw', 'customers') }}

{% endsnapshot %}
```

## Tests

```yaml
# models/marts/_schema.yml
version: 2

models:
  - name: fct_revenue
    description: Daily revenue aggregations
    columns:
      - name: revenue_date
        tests:
          - not_null
      - name: total_revenue
        tests:
          - not_null
          - dbt_utils.accepted_range:
              min_value: 0

    tests:
      # Model-level tests
      - dbt_utils.unique_combination_of_columns:
          combination_of_columns:
            - revenue_date
            - customer_segment
            - order_tier
```

## Custom Tests

```sql
-- tests/assert_positive_revenue.sql
-- Returns rows that fail the test

select
    revenue_date,
    total_revenue
from {{ ref('fct_revenue') }}
where total_revenue < 0
```

## Macros

```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name) %}
    round({{ column_name }} / 100.0, 2)
{% endmacro %}

-- Usage in model:
-- select {{ cents_to_dollars('amount_cents') }} as amount_dollars
```

```sql
-- macros/generate_schema_name.sql
{% macro generate_schema_name(custom_schema_name, node) %}
    {% if custom_schema_name %}
        {{ custom_schema_name }}
    {% else %}
        {{ target.schema }}
    {% endif %}
{% endmacro %}
```

## dbt Commands

```bash
# Run all models
dbt run

# Run specific model and dependencies
dbt run --select fct_revenue+

# Run models with tag
dbt run --select tag:finance

# Test all
dbt test

# Generate docs
dbt docs generate
dbt docs serve

# Freshness check
dbt source freshness

# Full refresh of incremental
dbt run --full-refresh --select fct_events

# Build (run + test)
dbt build
```

## Best Practices

```yaml
# 1. Use ref() for model references
# BAD:  select * from schema.stg_orders
# GOOD: select * from {{ ref('stg_orders') }}

# 2. Use source() for raw tables
# BAD:  select * from raw_db.orders
# GOOD: select * from {{ source('raw', 'orders') }}

# 3. Document models
models:
  - name: fct_revenue
    description: |
      Daily revenue by segment. Grain: one row per day/segment/tier.
      Updated daily by the finance_dag.
    meta:
      owner: data-team
      pii: false
```

## Packages

```yaml
# packages.yml
packages:
  - package: dbt-labs/dbt_utils
    version: 1.1.1
  - package: dbt-labs/codegen
    version: 0.12.1
  - package: calogica/dbt_expectations
    version: 0.10.1
```

```bash
# Install packages
dbt deps
```
