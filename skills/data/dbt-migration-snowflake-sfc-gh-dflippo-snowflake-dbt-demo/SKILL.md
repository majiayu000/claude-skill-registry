---
name: dbt-migration-snowflake
description:
  Convert Snowflake DDL to dbt models. This skill should be used when converting views, tables, or
  stored procedures from Snowflake to dbt code, generating schema.yml files with tests and
  documentation, or migrating existing Snowflake SQL to follow dbt best practices.
---

# Snowflake to dbt Model Conversion

## Purpose

Transform Snowflake DDL (views, tables, stored procedures) into production-quality dbt models,
maintaining the same business logic and data transformation steps while following dbt best
practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Snowflake views or tables to dbt models
- Migrating Snowflake stored procedures to dbt
- Generating schema.yml files with tests and documentation
- Modernizing existing Snowflake SQL to follow dbt best practices

---

# Task Description

You are a database engineer working for a hospital system. You need to convert Snowflake DDL to
equivalent dbt code, maintaining the same business logic and data transformation steps while
following dbt best practices.

# Input Requirements

I will provide you the Snowflake DDL to convert.

# Audience

The code will be executed by data engineers who are learning Snowflake and dbt.

# Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions
5. Inline comments highlighting any syntax that was converted

# Conversion Guidelines

## General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests
- Use Snowflake SQL functions rather than macros whenever possible

## Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original Object: [database].[schema].[object_name]
   Source Platform: Snowflake
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        account_balance::NUMBER(18,2) AS account_balance,
        created_date::DATE AS created_date
    FROM {{ ref('upstream_model') }}
),

transformed_data AS (
    SELECT
        customer_id,
        UPPER(customer_name)::VARCHAR(100) AS customer_name_upper,
        account_balance,
        created_date,
        CURRENT_TIMESTAMP()::TIMESTAMP_NTZ AS loaded_at
    FROM source_data
)

SELECT
    customer_id,
    customer_name_upper,
    account_balance,
    created_date,
    loaded_at
FROM transformed_data
```

```yaml
# models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from Snowflake [Original object name]"
    columns:
      - name: customer_id
        description: "Primary key - unique customer identifier"
        tests:
          - unique
          - not_null
      - name: customer_name_upper
        description: "Customer name in uppercase"
      - name: account_balance
        description: "Current account balance; Foreign key to OTHER_TABLE"
        tests:
          - relationships:
              to: ref('OTHER_TABLE')
              field: OTHER_TABLE_KEY
      - name: created_date
        description: "Date the customer record was created"
      - name: loaded_at
        description: "Timestamp when the record was loaded by dbt"
```

```yaml
# dbt_project.yml (excerpt)
models:
  my_project:
    +materialized: view
    domain_name:
      +schema: target_schema_name
```

## Specific Translation Rules

### dbt Specific Requirements:

- If the source is a view, use a view materialization in dbt
- Include appropriate dbt model configuration (materialization type)
- Add documentation blocks for a schema.yml
- Add descriptions for tables and columns
- Include relevant tests
- Define primary keys and relationships
- Assume that upstream objects are models
- Comprehensively provide all the columns in the output
- Break complex procedures into multiple models if needed
- Implement appropriate incremental strategies for large tables
- Use Snowflake SQL functions rather than macros whenever possible
- **Always cast columns with explicit precision/scale** using `::TYPE` syntax (e.g.,
  `column_name::VARCHAR(100)`, `amount::NUMBER(18,2)`) to ensure output matches expected data types
- **Always provide explicit column aliases** for clarity and documentation

### Performance Optimization:

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

### Snowflake to dbt Conversion Patterns:

Since the source is Snowflake, focus on converting to dbt best practices:

| Snowflake Object  | dbt Equivalent | Materialization                     |
| ----------------- | -------------- | ----------------------------------- |
| VIEW              | dbt model      | `view`                              |
| TABLE (static)    | dbt model      | `table`                             |
| TABLE (append)    | dbt model      | `incremental` (append)              |
| TABLE (merge)     | dbt model      | `incremental` (merge)               |
| DYNAMIC TABLE     | dbt model      | `incremental` or `table`            |
| MATERIALIZED VIEW | dbt model      | `table` with scheduling             |
| STORED PROCEDURE  | dbt model(s)   | Break into CTEs/models              |
| STREAM + TASK     | dbt model      | `incremental` with is_incremental() |

### Key Conversion Examples

```sql
-- Snowflake VIEW → dbt view model
CREATE VIEW schema.my_view AS SELECT ... →
{{ config(materialized='view') }}
SELECT ...

-- Snowflake TABLE with CTAS → dbt table model
CREATE TABLE schema.my_table AS SELECT ... →
{{ config(materialized='table') }}
SELECT ...

-- Snowflake MERGE pattern → dbt incremental
MERGE INTO target USING source ON ... →
{{ config(
    materialized='incremental',
    unique_key='id',
    merge_update_columns=['col1', 'col2']
) }}
SELECT ... FROM {{ ref('source_model') }}
{% if is_incremental() %}
WHERE updated_at > (SELECT MAX(updated_at) FROM {{ this }})
{% endif %}

-- Snowflake STREAM/TASK → dbt incremental
CREATE STREAM my_stream ON TABLE source;
CREATE TASK my_task ... INSERT INTO target SELECT * FROM my_stream →
{{ config(materialized='incremental', unique_key='id') }}
SELECT * FROM {{ ref('source') }}
{% if is_incremental() %}
WHERE _metadata_timestamp > (SELECT MAX(_metadata_timestamp) FROM {{ this }})
{% endif %}

-- Stored procedure logic → CTE pattern
BEGIN ... multiple statements ... END →
WITH step1 AS (...), step2 AS (...), step3 AS (...)
SELECT * FROM step3
```

### Snowflake-Specific Features in dbt

```sql
-- Clustering keys
{{ config(
    materialized='table',
    cluster_by=['date_col', 'category']
) }}

-- Transient tables (no Time Travel/Fail-safe)
{{ config(
    materialized='table',
    transient=true
) }}

-- Copy grants
{{ config(copy_grants=true) }}

-- Query tags
{{ config(query_tag='dbt_model_name') }}
```

### Data Type Handling:

Snowflake data types map directly - no conversion needed.

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake (already native)
- [] All business logic preserved
- [] All columns included in output
- [] Data types correctly mapped
- [] Functions translated to Snowflake equivalents
- [] Materialization strategy selected
- [] Tests added
- [] SQL logic description complete
- [] Table descriptions added
- [] Column descriptions added
- [] Dependencies correctly mapped
- [] Incremental logic (if applicable) verified
- [] Inline comments added for converted syntax

---

## Related Skills

- **dbt-modeling**: For CTE patterns and SQL structure guidance
- **dbt-testing**: For implementing comprehensive dbt tests
- **dbt-architecture**: For project organization and folder structure
- **dbt-materializations**: For choosing materialization strategies (view, table, incremental,
  snapshots)
- **dbt-performance**: For clustering keys, warehouse sizing, and query optimization
- **dbt-commands**: For running dbt commands and model selection syntax
- **dbt-core**: For dbt installation, configuration, and package management
- **snowflake-cli**: For executing SQL and managing Snowflake objects

---

## Supported Source Database

<!-- prettier-ignore -->
| Database | Key Considerations |
|---|---|
| **Snowflake** | Native syntax, focus on dbt patterns and best practices. Convert views to dbt views, tables to dbt tables/incremental models, stored procedures to dbt models with appropriate materialization. |

## Translation References

Since Snowflake is the target platform, no syntax translation is needed. The focus is on converting
Snowflake objects to dbt best practices.

### Reference Index

<!-- prettier-ignore -->
| Folder | Description |
|---|---|
| snowflake | [Subqueries for dbt Conversion](translation-references/snowflake/subqueries.md) |
