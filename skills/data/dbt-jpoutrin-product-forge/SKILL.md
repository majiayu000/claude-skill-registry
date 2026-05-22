---
name: dbt
description: dbt (data build tool) patterns for data transformation and analytics engineering. Use when building data models, implementing data quality tests, or managing data transformation pipelines.
user-invocable: false
---

# dbt Skill

This skill provides dbt patterns for analytics engineering.

## Project Structure

```
dbt_project/
├── dbt_project.yml
├── models/
│   ├── staging/
│   │   └── stg_customers.sql
│   ├── intermediate/
│   │   └── int_customer_orders.sql
│   └── marts/
│       └── fct_orders.sql
├── seeds/
├── macros/
├── tests/
└── snapshots/
```

## Model Patterns

### Staging Models
```sql
-- models/staging/stg_customers.sql
with source as (
    select * from {{ source('raw', 'customers') }}
),

renamed as (
    select
        id as customer_id,
        lower(email) as email,
        created_at
    from source
)

select * from renamed
```

### Incremental Models
```sql
-- models/marts/fct_orders.sql
{{
    config(
        materialized='incremental',
        unique_key='order_id'
    )
}}

select *
from {{ ref('stg_orders') }}
{% if is_incremental() %}
where updated_at > (select max(updated_at) from {{ this }})
{% endif %}
```

## Testing

```yaml
# models/schema.yml
models:
  - name: stg_customers
    columns:
      - name: customer_id
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - unique
```

## Best Practices

- Use staging → intermediate → marts pattern
- Source all raw data with `source()`
- Reference models with `ref()`
- Add documentation and tests
- Use incremental models for large datasets
