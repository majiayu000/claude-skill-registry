---
name: dbt-migration-db2
description:
  Convert IBM DB2 DDL to dbt models compatible with Snowflake. This skill should be used when
  converting views, tables, or stored procedures from DB2 to dbt code, generating schema.yml files
  with tests and documentation, or migrating DB2 SQL to follow dbt best practices.
---

# IBM DB2 to dbt Model Conversion

## Purpose

Transform IBM DB2 DDL (views, tables, stored procedures) into production-quality dbt models
compatible with Snowflake, maintaining the same business logic and data transformation steps while
following dbt best practices.

## When to Use This Skill

Activate this skill when users ask about:

- Converting DB2 views or tables to dbt models
- Migrating DB2 stored procedures to dbt
- Translating DB2 SQL syntax to Snowflake
- Generating schema.yml files with tests and documentation
- Handling DB2-specific syntax conversions (Inline SQL PL, FETCH FIRST, CONTINUE/EXIT handlers)

---

# Task Description

You are a database engineer working for a hospital system. You need to convert IBM DB2 DDL to
equivalent dbt code compatible with Snowflake, maintaining the same business logic and data
transformation steps while following dbt best practices.

# Input Requirements

I will provide you the DB2 DDL to convert.

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
   Source Platform: IBM DB2
   Purpose: [brief description]
   Conversion Notes: [key changes]
   Description: [SQL logic description] */

WITH source_data AS (
    SELECT
        customer_id::INTEGER AS customer_id,
        customer_name::VARCHAR(100) AS customer_name,
        account_balance::NUMBER(18,2) AS account_balance,
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
# models/[domain]/[target_schema_name]/_models.yml
version: 2

models:
  - name: model_name
    description: "Table description; converted from IBM DB2 [Original object name]"
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

### DB2 to Snowflake Syntax Conversion:

- Convert FETCH FIRST n ROWS ONLY to LIMIT n
- Replace compound statements with Snowflake Scripting
- Convert CONTINUE/EXIT handlers to exception handling
- Translate inline SQL PL to Snowflake Scripting
- Handle CURRENT DATE/TIMESTAMP differences
- Convert DB2 string functions
- Replace EXCEPT/INTERSECT if using non-ANSI syntax

### Key Data Type Mappings

| DB2             | Snowflake | Notes    |
| --------------- | --------- | -------- |
| INTEGER/INT     | INTEGER   |          |
| BIGINT          | BIGINT    |          |
| SMALLINT        | SMALLINT  |          |
| DECIMAL/NUMERIC | DECIMAL   |          |
| REAL/FLOAT      | FLOAT     |          |
| DOUBLE          | DOUBLE    |          |
| CHAR/VARCHAR    | Same      |          |
| CLOB            | VARCHAR   | Max 16MB |
| BLOB            | BINARY    | Max 8MB  |
| DATE            | DATE      |          |
| TIME            | TIME      |          |
| TIMESTAMP       | TIMESTAMP |          |
| XML             | VARIANT   |          |

### Key Syntax Conversions

```sql
-- FETCH FIRST -> LIMIT
SELECT * FROM table FETCH FIRST 10 ROWS ONLY -> SELECT * FROM table LIMIT 10

-- CURRENT DATE/TIMESTAMP (no parentheses in DB2)
CURRENT DATE -> CURRENT_DATE()
CURRENT TIMESTAMP -> CURRENT_TIMESTAMP()

-- CONTINUE/EXIT handlers -> Exception handling
DECLARE CONTINUE HANDLER FOR SQLEXCEPTION ... ->
EXCEPTION WHEN OTHER THEN ...

-- VALUES clause
VALUES (1, 'a'), (2, 'b') -> SELECT 1, 'a' UNION ALL SELECT 2, 'b'
```

### Common Function Mappings

| DB2                     | Snowflake                          | Notes            |
| ----------------------- | ---------------------------------- | ---------------- |
| `COALESCE(a, b)`        | `COALESCE(a, b)`                   | Same             |
| `IFNULL(a, b)`          | `IFNULL(a, b)`                     | Same             |
| `VALUE(a, b)`           | `NVL(a, b)`                        |                  |
| `NULLIF(a, b)`          | `NULLIF(a, b)`                     | Same             |
| `SUBSTR(str, pos, len)` | `SUBSTR(str, pos, len)`            | Same             |
| `TRIM(str)`             | `TRIM(str)`                        | Same             |
| `UPPER/LOWER`           | Same                               |                  |
| `LENGTH(str)`           | `LENGTH(str)`                      | Same             |
| `LOCATE(search, str)`   | `POSITION(search IN str)`          |                  |
| `DECIMAL(val, p, s)`    | `val::NUMBER(p, s)`                |                  |
| `INTEGER(val)`          | `val::INTEGER`                     |                  |
| `VARCHAR(val)`          | `val::VARCHAR`                     |                  |
| `DATE(val)`             | `val::DATE`                        |                  |
| `CURRENT DATE`          | `CURRENT_DATE()`                   | Add parentheses  |
| `CURRENT TIMESTAMP`     | `CURRENT_TIMESTAMP()`              | Add parentheses  |
| `DAYS(d)`               | `DATEDIFF('day', '0001-01-01', d)` | Days since epoch |
| `YEAR/MONTH/DAY(d)`     | `YEAR/MONTH/DAY(d)`                | Same             |

### Dependencies:

- List any upstream dependencies
- Suggest model organization in dbt project

---

# Validation Checklist

- [] Every DDL statement has been accounted for in the dbt models
- [] SQL in models is compatible with Snowflake
- [] DB2-specific syntax converted (FETCH FIRST, compound statements, handlers)
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
| **IBM DB2** | Inline SQL PL, FETCH FIRST, CONTINUE/EXIT handlers, compound statements |

## Translation References

Detailed syntax translation guides are available in the `translation-references/` folder.

> **Copyright Notice:** The translation reference documentation in this repository is derived from
> [Snowflake SnowConvert Documentation](https://docs.snowflake.com/en/migrations/snowconvert-docs)
> and is © Copyright Snowflake Inc. All rights reserved. Used for reference purposes only.

### Reference Index

<!-- prettier-ignore -->
| Folder | Description |
|---|---|
| db2 | [CONTINUE handler](translation-references/db2/db2-continue-handler.md) |
| db2 | [CREATE FUNCTION](translation-references/db2/db2-create-function.md) |
| db2 | [CREATE PROCEDURE](translation-references/db2/db2-create-procedure.md) |
| db2 | [EXIT handler](translation-references/db2/db2-exit-handler.md) |
| db2 | [Subqueries](translation-references/db2/subqueries.md) |
