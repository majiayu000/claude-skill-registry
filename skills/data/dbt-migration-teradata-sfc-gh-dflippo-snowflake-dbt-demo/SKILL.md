---
name: dbt-migration-teradata
description:
  Convert Teradata DDL to dbt models compatible with Snowflake. This skill should be used when
  converting views, tables, or stored procedures from Teradata to dbt code, generating schema.yml
  files with tests and documentation, or migrating Teradata SQL to follow dbt best practices.
---

# Teradata to dbt Model Conversion

## Purpose

Transform Teradata DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting Teradata views or tables to dbt models
- Migrating Teradata stored procedures to dbt
- Translating Teradata SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling Teradata-specific syntax (QUALIFY, ANSI/TERA modes, volatile tables, DBC views)

---

# Task Description

You are a database engineer working for a hospital system. You need to convert Teradata DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

# Input Requirements

I will provide you the Teradata DDL to convert.

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

/* Original Object: [database].[table_name]
   Source Platform: Teradata
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
    description: "Table description; converted from Teradata [Original object name]"
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

### Teradata to Snowflake Syntax Conversion:

- Convert Teradata-specific functions to Snowflake equivalents
- Adjust date/timestamp functions
- Handle data type mappings
- Convert QUALIFY/ROW_NUMBER syntax if present
- Address any volatile table references
- Replace SET/MULTISET table specifications
- Convert ANSI vs TERA session mode syntax
- Handle DBC view equivalents
- Add inline SQL comments highlighting any syntax that was converted

### Key Data Type Mappings

| Teradata                 | Snowflake      | Notes                              |
| ------------------------ | -------------- | ---------------------------------- |
| BIGINT/INTEGER/SMALLINT  | NUMBER(38,0)   | All integers map to NUMBER         |
| BYTEINT                  | BYTEINT        |                                    |
| DECIMAL/NUMBER           | NUMBER         |                                    |
| FLOAT/REAL               | FLOAT          |                                    |
| CHAR/VARCHAR             | CHAR/VARCHAR   |                                    |
| DATE                     | DATE           |                                    |
| TIME/TIMESTAMP           | TIME/TIMESTAMP |                                    |
| TIMESTAMP WITH TIME ZONE | TIMESTAMP_TZ   |                                    |
| BLOB                     | BINARY         | Limited to 8MB                     |
| CLOB                     | VARCHAR        | Limited to 16MB                    |
| JSON/XML                 | VARIANT        |                                    |
| INTERVAL types           | VARCHAR        | Store as string, use in arithmetic |
| PERIOD types             | VARCHAR        | Store as 'start\*end' format       |
| ST_GEOMETRY              | GEOGRAPHY      |                                    |

### Key Syntax Conversions

```sql
-- QUALIFY (Teradata) → Same in Snowflake (natively supported)
SELECT * FROM table QUALIFY ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2) = 1

-- Volatile tables → Temporary tables
CREATE VOLATILE TABLE temp_data AS ... → CREATE TEMPORARY TABLE temp_data AS ...

-- SET/MULTISET → Remove (Snowflake handles duplicates differently)
CREATE SET TABLE → CREATE TABLE
CREATE MULTISET TABLE → CREATE TABLE

-- FALLBACK/JOURNAL → Remove (Snowflake-managed)
NO FALLBACK, NO JOURNAL → (remove entirely)

-- FORMAT in column definition → Remove
DATE FORMAT 'YYYY-MM-DD' → DATE

-- CASESPECIFIC → Remove (use COLLATE if needed)
VARCHAR(100) NOT CASESPECIFIC → VARCHAR(100)
```

### Common Function Mappings

| Teradata                 | Snowflake                                          | Notes                            |
| ------------------------ | -------------------------------------------------- | -------------------------------- |
| `NVL(a, b)`              | `NVL(a, b)` or `COALESCE(a, b)`                    | Same                             |
| `NULLIFZERO(col)`        | `NULLIF(col, 0)`                                   |                                  |
| `ZEROIFNULL(col)`        | `NVL(col, 0)`                                      |                                  |
| `COALESCE(...)`          | `COALESCE(...)`                                    | Same                             |
| `TRIM(col)`              | `TRIM(col)`                                        | Remove RTRIM for trailing spaces |
| `SUBSTR(s, pos, len)`    | `SUBSTR(s, pos, len)`                              | Same                             |
| `INDEX(str, search)`     | `POSITION(search IN str)`                          |                                  |
| `ADD_MONTHS(d, n)`       | `DATEADD('month', n, d)`                           |                                  |
| `TRUNC(d)`               | `DATE_TRUNC('day', d)`                             |                                  |
| `EXTRACT(part FROM d)`   | `EXTRACT(part FROM d)`                             | Same                             |
| `DATE '2024-01-15'`      | `DATE '2024-01-15'`                                | Same                             |
| `CAST(x AS FORMAT 'Y4')` | `TO_CHAR(x, 'YYYY')`                               |                                  |
| `CASE_N(cond1, cond2)`   | `CASE WHEN cond1 THEN 1 WHEN cond2 THEN 2 ... END` |                                  |
| `HASHROW(cols)`          | `HASH(cols)`                                       |                                  |
| `RANDOM(low, high)`      | `UNIFORM(low, high, RANDOM())`                     |                                  |

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] Teradata-specific syntax converted (QUALIFY, SET/MULTISET, volatile tables, DBC)
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
| **Teradata** | QUALIFY, ANSI/TERA session modes, volatile tables, SET/MULTISET, BTEQ/FastLoad/MultiLoad scripts, DBC views |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

<!-- prettier-ignore -->
| Folder | Description |
|---|---|
| teradata | [Teradata to Snowflake Scripting](translation-references/teradata/teradata-to-snowflake-scripting-translation-reference.md) |
| teradata | [Power BI repointing](translation-references/teradata/etl-bi-repointing/power-bi-teradata-repointing.md) |
| teradata | [Scripts to Python](translation-references/teradata/scripts-to-python/README.md) |
| teradata | [BTEQ to Python](translation-references/teradata/scripts-to-python/bteq-translation.md) |
| teradata | [FastLoad to Python](translation-references/teradata/scripts-to-python/fastload-translation.md) |
| teradata | [MultiLoad to Python](translation-references/teradata/scripts-to-python/multiload-translation.md) |
| teradata | [TPT translation](translation-references/teradata/scripts-to-python/tpt-translation.md) |
| teradata | [Subqueries](translation-references/teradata/subqueries.md) |
