---
name: dbt-migration-hive
description:
  Convert Hive/Spark/Databricks DDL to dbt models compatible with Snowflake. This skill should be
  used when converting views, tables, or UDFs from Hive, Spark, or Databricks to dbt code,
  generating schema.yml files with tests and documentation, or migrating HiveQL to follow dbt best
  practices.
---

# Hive/Spark/Databricks to dbt Model Conversion

## Purpose

Transform Hive/Spark/Databricks DDL (views, tables, UDFs) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Hive/Spark/Databricks views or tables to dbt models
- Migrating HiveQL UDFs to dbt
- Translating HiveQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Hive-specific syntax conversions (external tables, PARTITIONED BY, LATERAL VIEW, file
  formats)

---

## Task Description

You are a database engineer working for a hospital system. You need to convert Hive/Spark/Databricks
DDL to equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

## Input Requirements

I will provide you the HiveQL DDL to convert.

## Audience

The code will be executed by data engineers who are learning Snowflake and dbt.

## Output Requirements

Generate the following:

1. One or more dbt models with complete SQL for every column
2. A corresponding schema.yml file with appropriate tests and documentation
3. A config block with materialization strategy
4. Explanation of key changes and architectural decisions
5. Inline comments highlighting any syntax that was converted

## Conversion Guidelines

### General Principles

- Replace procedural logic with declarative SQL where possible
- Break down complex procedures into multiple modular dbt models
- Implement appropriate incremental processing strategies
- Maintain data quality checks through dbt tests
- Use Snowflake SQL functions rather than macros whenever possible

### Sample Response Format

```sql
-- dbt model: models/[domain]/[target_schema_name]/model_name.sql
{{ config(materialized='view') }}

/* Original Object: [database].[object_name]
   Source Platform: Hive/Spark/Databricks
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        -- Hive BIGINT/INT converted to INTEGER
        customer_id::INTEGER AS customer_id,
        -- STRING converted to VARCHAR
        customer_name::VARCHAR(100) AS customer_name,
        -- DECIMAL converted to NUMBER
        account_balance::NUMBER(18,2) AS account_balance,
        -- TIMESTAMP converted to TIMESTAMP_NTZ
        created_date::TIMESTAMP_NTZ AS created_date
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
## models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from Hive/Spark/Databricks [Original object name]"
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
## dbt_project.yml (excerpt)
models:
  my_project:
    +materialized: view
    domain_name:
      +schema: target_schema_name
```

### Specific Translation Rules

#### dbt Specific Requirements

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

#### Performance Optimization

- Suggest clustering keys if needed
- Recommend materialization strategy (view vs table)
- Identify potential performance improvements

#### Hive/Spark to Snowflake Syntax Conversion

- Convert LATERAL VIEW to LATERAL FLATTEN
- Replace PARTITIONED BY with clustering keys
- Convert file format specifications (PARQUET, ORC) to Snowflake staging
- Handle EXTERNAL TABLE references
- Convert Hive UDFs to Snowflake equivalents
- Replace DISTRIBUTE BY/SORT BY with clustering
- Convert ARRAY/MAP/STRUCT types to VARIANT

#### Key Data Type Mappings

| Hive/Spark                  | Snowflake     | Notes                |
| --------------------------- | ------------- | -------------------- |
| TINYINT/SMALLINT/INT/BIGINT | Same          |                      |
| FLOAT/DOUBLE                | FLOAT         |                      |
| DECIMAL                     | DECIMAL       |                      |
| STRING                      | VARCHAR       |                      |
| CHAR/VARCHAR                | Same          |                      |
| BOOLEAN                     | BOOLEAN       |                      |
| BINARY                      | BINARY        |                      |
| DATE                        | DATE          |                      |
| TIMESTAMP                   | TIMESTAMP_NTZ |                      |
| ARRAY<T>                    | ARRAY         |                      |
| MAP<K,V>                    | VARIANT       | Use OBJECT_CONSTRUCT |
| STRUCT                      | VARIANT       |                      |

#### Key Syntax Conversions

```sql
-- LATERAL VIEW -> LATERAL FLATTEN
SELECT * FROM table LATERAL VIEW EXPLODE(array_col) t AS elem ->
SELECT * FROM table, LATERAL FLATTEN(input => array_col) AS f

-- PARTITIONED BY -> Clustering
CREATE TABLE t (...) PARTITIONED BY (dt STRING) ->
CREATE TABLE t (...) CLUSTER BY (dt)

-- External tables
CREATE EXTERNAL TABLE t LOCATION 's3://...' ->
CREATE EXTERNAL TABLE t WITH LOCATION = @stage/path

-- collect_list/collect_set
collect_list(col) -> ARRAY_AGG(col)
collect_set(col) -> ARRAY_AGG(DISTINCT col)

-- size() -> ARRAY_SIZE()
size(array_col) -> ARRAY_SIZE(array_col)
```

#### Common Function Mappings

| Hive/Spark              | Snowflake                                      | Notes               |
| ----------------------- | ---------------------------------------------- | ------------------- |
| `collect_list(col)`     | `ARRAY_AGG(col)`                               |                     |
| `collect_set(col)`      | `ARRAY_AGG(DISTINCT col)`                      |                     |
| `size(arr)`             | `ARRAY_SIZE(arr)`                              |                     |
| `explode(arr)`          | `LATERAL FLATTEN(input => arr)`                |                     |
| `posexplode(arr)`       | `LATERAL FLATTEN(input => arr)`                | Use `f.index`       |
| `concat_ws(sep, ...)`   | `CONCAT_WS(sep, ...)`                          | Same                |
| `nvl(a, b)`             | `NVL(a, b)` or `COALESCE(a, b)`                | Same                |
| `coalesce(...)`         | `COALESCE(...)`                                | Same                |
| `if(cond, a, b)`        | `IFF(cond, a, b)`                              |                     |
| `unix_timestamp()`      | `DATE_PART(epoch_second, CURRENT_TIMESTAMP())` |                     |
| `from_unixtime(ts)`     | `TO_TIMESTAMP(ts)`                             |                     |
| `to_date(str, fmt)`     | `TO_DATE(str, fmt)`                            | Same                |
| `date_format(d, fmt)`   | `TO_CHAR(d, fmt)`                              | Format codes differ |
| `datediff(d1, d2)`      | `DATEDIFF('day', d2, d1)`                      | Arg order differs   |
| `regexp_replace(...)`   | `REGEXP_REPLACE(...)`                          | Same                |
| `regexp_extract(...)`   | `REGEXP_SUBSTR(...)`                           |                     |
| `split(str, delim)`     | `SPLIT(str, delim)`                            | Same                |
| `get_json_object(j, p)` | `GET_PATH(PARSE_JSON(j), p)`                   |                     |

#### Dependencies

- List any upstream dependencies
- Suggest model organization in dbt project

---

## Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Hive-specific syntax converted (external tables, PARTITIONED BY, file formats, LATERAL VIEW)
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

- $dbt-migration - For the complete migration workflow (discovery, planning, placeholder models,
  testing, deployment)
- $dbt-modeling - For CTE patterns and SQL structure guidance
- $dbt-testing - For implementing comprehensive dbt tests
- $dbt-architecture - For project organization and folder structure
- $dbt-materializations - For choosing materialization strategies (view, table, incremental,
  snapshots)
- $dbt-performance - For clustering keys, warehouse sizing, and query optimization
- $dbt-commands - For running dbt commands and model selection syntax
- $dbt-core - For dbt installation, configuration, and package management
- $snowflake-cli - For executing SQL and managing Snowflake objects

---

## Supported Source Database

| Database                      | Key Considerations                                                               |
| ----------------------------- | -------------------------------------------------------------------------------- |
| **Hive / Spark / Databricks** | External tables, PARTITIONED BY, LATERAL VIEW, file formats (PARQUET, ORC), UDFs |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

- [Built In Functions](translation-references/hive-built-in-functions.md)
- [Data Types](translation-references/hive-data-types.md)
- [Ddls Create External Table](translation-references/hive-ddls-create-external-table.md)
- [Ddls Create View](translation-references/hive-ddls-create-view.md)
- [Ddls Readme](translation-references/hive-ddls-readme.md)
- [Ddls Select](translation-references/hive-ddls-select.md)
- [Ddls Tables](translation-references/hive-ddls-tables.md)
- [Overview (README)](translation-references/hive-readme.md)
- [Subqueries](translation-references/hive-subqueries.md)
