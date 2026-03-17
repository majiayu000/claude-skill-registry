---
name: dbt-migration
description:
  Complete workflow for migrating database tables, views, and stored procedures to dbt projects on
  Snowflake. Orchestrates discovery, planning, placeholder creation, view/procedure conversion,
  testing, and deployment. Delegates platform-specific syntax translation to source-specific skills.
---

# Database to dbt Migration Workflow

## Purpose and When to Use

Guide AI agents through the complete migration lifecycle from Snowflake or legacy database systems
(SQL Server, Oracle, Teradata, etc.) to production-quality dbt projects on Snowflake. This skill
defines a structured, repeatable process while delegating platform-specific syntax translation to
dedicated source-specific skills.

Activate this skill when users ask about:

- Planning a database migration to dbt
- Organizing legacy scripts for migration
- Converting views and stored procedures to dbt models
- Testing migration results against source systems
- Deploying migrated dbt projects to production

---

## Snowflake Migration Tools

### Recommended Two-Step Approach

1. **Convert to Snowflake first**: Use SnowConvert AI and AI Powered Code Conversion to convert
   source database objects (from SQL Server, Oracle, Teradata, etc.) to Snowflake tables, views, and
   stored procedures.
2. **Then convert to dbt**: Use the $dbt-migration-snowflake skill to migrate Snowflake objects to
   dbt models.

### SnowConvert AI (Recommended for Supported Platforms)

[SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/about) converts
source DDL, views, stored procedures, functions, and additional objects (triggers, sequences,
indexes) to Snowflake-compatible SQL.
[Download SnowConvert AI](https://docs.snowflake.com/en/migrations/snowconvert-docs/general/getting-started/download-and-access)

#### Supported Platforms

- **Full support** (tables, views, procedures, functions): SQL Server, Oracle, Teradata, Redshift,
  Azure Synapse, IBM DB2
- **Partial support** (tables, views only): Sybase IQ, BigQuery, PostgreSQL, Spark SQL/Databricks,
  Hive, Vertica, Greenplum/Netezza

#### Platform-Specific Features

- SQL Server: Direct DB connection, data migration, SSIS replatform
- Oracle, Azure Synapse, Sybase IQ, BigQuery: DDL Extraction script
- Teradata: BTEQ/MLOAD/TPUMP support
- Redshift: Direct DB connection, data migration

### Additional Snowflake Migration Tools

| Tool                                                    | Purpose                                                  |
| ------------------------------------------------------- | -------------------------------------------------------- |
| [AI Code Conversion](resources/ai-code-conversion.md)   | AI-powered validation and repair of converted code       |
| [Migration Assistant](resources/migration-assistant.md) | VS Code extension for resolving conversion issues (EWIs) |
| [Data Migration](resources/data-migration.md)           | Transfer data to Snowflake (SQL Server, Redshift)        |
| [Data Validation](resources/data-validation.md)         | GUI-based validation (SQL Server)                        |
| [Data Validation CLI](resources/data-validation-cli.md) | CLI validation (SQL Server, Teradata, Redshift)          |
| [ETL Replatform](resources/etl-replatform.md)           | Convert SSIS packages to dbt projects                    |
| [Power BI Repointing](resources/power-bi-repointing.md) | Redirect Power BI reports to Snowflake                   |

---

## Migration Workflow Overview

The migration process follows seven sequential phases. Each phase has entry criteria, deliverables,
and validation gates that must pass before advancing.

```text
1-Discovery → 2-Planning → 3-Placeholders → 4-Views → 5-Table Logic → 6-Testing → 7-Deployment
```

---

## Phase 1: Discovery and Assessment

Create a complete inventory of source database objects and understand dependencies, volumes, and
complexity to inform migration planning.

**SnowConvert AI Option**: If your platform is supported, SnowConvert AI provides extraction scripts
that automate object inventory, dependency mapping, and initial code conversion.

### Phase 1 Activities

1. **Inventory source objects**: Query system catalogs for tables, views, procedures, functions
2. **Document dependencies**: Map object dependencies to determine migration order
3. **Document volumes**: Record row counts and data sizes
4. **Assess complexity**: Categorize objects as Low/Medium/High/Custom complexity
5. **Create migration tracker**: Document objects in spreadsheet or issue tracker

### Complexity Assessment

| Complexity | Criteria                               | Examples                      |
| ---------- | -------------------------------------- | ----------------------------- |
| **Low**    | Simple SELECT, no/minimal joins        | Lookup tables, simple views   |
| **Medium** | Multiple joins, aggregations, CASE     | Summary views, report queries |
| **High**   | Procedural logic, cursors, temp tables | SCD procedures, bulk loads    |
| **Custom** | Platform-specific features             | Wrapped code, CLR functions   |

### Phase 1 Checklist

- [ ] All tables, views, procedures inventoried
- [ ] Row counts documented
- [ ] Object dependencies mapped
- [ ] Complexity assessment complete
- [ ] Migration tracker created
- [ ] Refresh frequencies identified

---

## Phase 2: Planning and Organization

Organize legacy scripts, map objects to the dbt medallion architecture, and establish naming
conventions before any conversion begins.

### Phase 2 Activities

1. **Organize legacy scripts**: Create folder structure (tables/, views/, stored_procedures/,
   functions/)
2. **Map to medallion layers**: Assign objects to Bronze/Silver/Gold with appropriate prefixes
3. **Define naming conventions**: Follow $dbt-architecture skill patterns
4. **Create dependency graph**: Visualize migration order
5. **Establish validation criteria**: Define success metrics per object

### Layer Mapping Reference

| Source Object Type   | Target Layer | dbt Prefix | Materialization |
| -------------------- | ------------ | ---------- | --------------- |
| Source tables (raw)  | Bronze       | `stg_`     | ephemeral       |
| Simple views         | Bronze       | `stg_`     | ephemeral       |
| Complex views        | Silver       | `int_`     | ephemeral/table |
| Dimension procedures | Gold         | `dim_`     | table           |
| Fact procedures      | Gold         | `fct_`     | incremental     |

### Phase 2 Checklist

- [ ] Legacy scripts organized in folders
- [ ] All objects mapped to medallion layers
- [ ] Naming conventions documented
- [ ] Dependency graph created
- [ ] Migration order established
- [ ] Validation criteria defined

---

## Phase 3: Create Placeholder Models

Create empty dbt models with correct column names, data types, and schema documentation **before**
adding any transformation logic. This establishes the contract for downstream consumers.

### Phase 3 Activities

1. **Generate placeholder models**: Create SQL files with `null::datatype as column_name` pattern
   and `where false`
2. **Map datatypes**: Use platform-specific skill for datatype conversion to Snowflake types
3. **Create schema documentation**: Generate `_models.yml` with column descriptions and tests
4. **Validate compilation**: Run `dbt compile --select tag:placeholder`
5. **Track status**: Add `placeholder` tag to config for tracking

### Placeholder Model Pattern

```sql
{{ config(materialized='ephemeral', tags=['placeholder', 'bronze']) }}

select
    null::integer as column_id,
    null::varchar(100) as column_name,
    -- ... additional columns with explicit types
where false
```

### Phase 3 Checklist

- [ ] Placeholder model created for each target table
- [ ] All columns have explicit datatype casts
- [ ] Column names follow naming conventions
- [ ] `_models.yml` created with descriptions and tests
- [ ] All placeholder models compile successfully
- [ ] Placeholder tag applied for tracking

---

## Phase 4: Convert Views

Convert source database views to dbt models, starting with simple views before tackling complex
ones. Views are typically easier than stored procedures as they contain declarative SQL.

### Phase 4 Activities

1. **Prioritize by complexity**: Simple views (no joins) → Join views → Aggregate views → Complex
   views
2. **Apply syntax translation**: Delegate to platform-specific skill (see Related Skills)
3. **Structure with CTEs**: Use standard CTE pattern from $dbt-modeling skill
4. **Add tests**: Define tests in `_models.yml` using $dbt-testing skill patterns
5. **Replace placeholder logic**: Update placeholder SELECT with converted logic

### Phase 4 Checklist

- [ ] Views prioritized by complexity
- [ ] Platform-specific syntax translated (delegate to source skills)
- [ ] CTE pattern applied consistently
- [ ] dbt tests added for each view
- [ ] Converted views compile successfully
- [ ] Inline comments document syntax changes

---

## Phase 5: Convert Table Logic from Stored Procedures

Transform procedural stored procedure logic into declarative dbt models, selecting appropriate
materializations for different ETL patterns.

### Phase 5 Activities

1. **Analyze ETL patterns**: Identify Full Refresh, SCD Type 1/2, Append, Delete+Insert patterns
2. **Map to materializations**: Use pattern-to-materialization mapping from $dbt-materializations
   skill
3. **Break complex procedures**: Split single procedures into multiple intermediate/final models
4. **Convert procedural constructs**: Replace cursors, temp tables, variables with declarative SQL
5. **Document decisions**: Add header comments explaining conversion approach

### Pattern Mapping Reference

| Source Pattern         | dbt Approach                                |
| ---------------------- | ------------------------------------------- |
| TRUNCATE + INSERT      | `materialized='table'`                      |
| UPDATE + INSERT (SCD1) | `materialized='incremental'` with merge     |
| SCD Type 2             | dbt snapshot or custom incremental          |
| INSERT only            | `materialized='incremental'` append         |
| DELETE range + INSERT  | `incremental` with `delete+insert` strategy |

### Procedural to Declarative Conversion

| Procedural Pattern | dbt Equivalent                   |
| ------------------ | -------------------------------- |
| CURSOR loop        | Window function or recursive CTE |
| Temp tables        | CTEs or intermediate models      |
| Variables          | Jinja variables or macros        |
| IF/ELSE branches   | CASE expressions or `{% if %}`   |
| TRY/CATCH          | Pre-validation tests             |

### Phase 5 Checklist

- [ ] All stored procedures analyzed for patterns
- [ ] ETL patterns mapped to dbt materializations
- [ ] Complex procedures broken into multiple models
- [ ] Procedural logic converted to declarative SQL
- [ ] Conversion decisions documented in model headers
- [ ] All converted models compile successfully

---

## Phase 6: End-to-End Testing and Validation

Verify that migrated dbt models produce identical results to source system, using multiple
validation techniques to ensure data integrity.

**Snowflake Data Validation CLI**: For SQL Server, Teradata, or Redshift migrations, the
[Data Validation CLI](https://docs.snowflake.com/en/migrations/snowconvert-docs/data-validation-cli/index)
provides automated schema validation (columns, data types, row counts) and metrics validation (MIN,
MAX, AVG, NULL count, DISTINCT count).

### Phase 6 Activities

1. **Row count validation**: Compare total counts between source and target
2. **Column checksum validation**: Compare row-level hashes to identify differences
3. **Business rule validation**: Verify calculated fields match source logic
4. **Aggregate validation**: Compare summary metrics (sums, counts, averages)
5. **Mock data testing**: Create seed fixtures for complex transformation testing
6. **Incremental validation**: Test both full-refresh and incremental runs
7. **Document results**: Create validation report for each migrated object

### Validation Techniques

| Technique      | Purpose                   | Implementation                |
| -------------- | ------------------------- | ----------------------------- |
| Row counts     | Detect missing/extra rows | Compare COUNT(\*)             |
| Checksums      | Detect value differences  | SHA2 hash comparison          |
| Business rules | Verify logic accuracy     | Singular tests                |
| Aggregates     | Validate totals           | SUM/AVG comparisons           |
| Mock data      | Test transformations      | Seed files + expected outputs |

### Phase 6 Checklist

- [ ] Row count validation queries created
- [ ] Checksum comparison implemented
- [ ] Business rule tests written
- [ ] Aggregate metrics compared
- [ ] Incremental models tested (full refresh + incremental)
- [ ] All validation queries pass
- [ ] Discrepancies documented and resolved
- [ ] Validation report completed

---

## Phase 7: Deployment and Cutover

Deploy validated dbt models to production with a clear cutover plan and monitoring strategy.

### Phase 7 Activities

1. **Deploy to Development**: Run `dbt build --target dev` and validate
2. **Deploy to Test/UAT**: Run full validation suite with `--store-failures`
3. **Create cutover plan**: Document pre-cutover, cutover, post-cutover, and rollback steps
4. **Deploy to Production**: Execute deployment with production data
5. **Configure scheduled runs**: Set up Snowflake tasks or dbt Cloud scheduling
6. **Monitor post-deployment**: Track run duration, row counts, test failures, performance

### Cutover Plan Template

| Phase              | Activities                                                                     |
| ------------------ | ------------------------------------------------------------------------------ |
| Pre-Cutover (T-1)  | Final validation, stakeholder sign-off, rollback docs, user communication      |
| Cutover (T-0)      | Disable source ETL, final sync, deploy, build, validate, update BI connections |
| Post-Cutover (T+1) | Monitor performance, verify schedules, confirm access, close tickets           |
| Rollback           | Re-enable source ETL, revert BI connections, document issues                   |

### Phase 7 Checklist

- [ ] Development deployment successful
- [ ] Test/UAT deployment successful
- [ ] Cutover plan documented
- [ ] Rollback procedure documented
- [ ] Stakeholder sign-off obtained
- [ ] Production deployment successful
- [ ] Scheduled runs configured
- [ ] Monitoring set up
- [ ] Migration marked complete

---

## Related Skills

### Platform-Specific Translation Skills

For syntax translation, delegate to the appropriate source-specific skill:

| Source Platform                  | Skill                        | Key Considerations                   |
| -------------------------------- | ---------------------------- | ------------------------------------ |
| Snowflake                        | $dbt-migration-snowflake     | Convert Snowflake objects to dbt     |
| SQL Server / Azure Synapse       | $dbt-migration-ms-sql-server | T-SQL, IDENTITY, TOP, #temp tables   |
| Oracle                           | $dbt-migration-oracle        | PL/SQL, ROWNUM, CONNECT BY, packages |
| Teradata                         | $dbt-migration-teradata      | QUALIFY, BTEQ, volatile tables       |
| BigQuery                         | $dbt-migration-bigquery      | UNNEST, STRUCT/ARRAY, backticks      |
| Redshift                         | $dbt-migration-redshift      | DISTKEY/SORTKEY, COPY/UNLOAD         |
| PostgreSQL / Greenplum / Netezza | $dbt-migration-postgres      | Array expressions, psql commands     |
| IBM DB2                          | $dbt-migration-db2           | SQL PL, FETCH FIRST, handlers        |
| Hive / Spark / Databricks        | $dbt-migration-hive          | External tables, PARTITIONED BY      |
| Vertica                          | $dbt-migration-vertica       | Projections, flex tables             |
| Sybase IQ                        | $dbt-migration-sybase        | T-SQL variant, SELECT differences    |

---

## Quick Reference: Phase Summary

<!-- AGENT_WORKFLOW_METADATA: Machine-parseable phase definitions -->

| Phase           | Key Deliverable                             | Exit Criteria                            | Primary Skill                         | Validation Focus                              | Validation Command                     |
| --------------- | ------------------------------------------- | ---------------------------------------- | ------------------------------------- | --------------------------------------------- | -------------------------------------- |
| 1. Discovery    | `migration_inventory.csv`, dependency graph | Inventory complete, dependencies mapped  | This skill                            | Object counts, dependency completeness        | Manual review                          |
| 2. Planning     | Folder structure, `_naming_conventions.md`  | Folder structure created, naming defined | $dbt-architecture                     | Folder hierarchy, naming conventions          | `ls -la models/`                       |
| 3. Placeholders | `.sql` files, `_models.yml`                 | All models compile with `where false`    | This skill                            | YAML structure, column definitions, naming    | `dbt compile --select tag:placeholder` |
| 4. Views        | Converted view models                       | All views converted and compile          | dbt-migration-{source}, $dbt-modeling | Syntax translation, CTE patterns, ref() usage | `dbt build --select tag:view`          |
| 5. Table Logic  | Converted procedure models                  | All procedures converted                 | $dbt-materializations                 | Incremental configs, materialization patterns | `dbt build --select tag:procedure`     |
| 6. Testing      | Validation queries, test results            | All validation queries pass              | $dbt-testing, $dbt-performance        | Test coverage, constraint definitions         | `dbt test --store-failures`            |
| 7. Deployment   | Production models, monitoring               | Production deployment successful         | $dbt-commands, $snowflake-cli         | Run success, schedule configuration           | `dbt build --target prod`              |

### General Skills

- $dbt-core: Local installation, configuration, package management
- $snowflake-connections: Connection setup for Snowflake CLI, Streamlit, dbt

---

## Validation Requirements

**CRITICAL: Agents must not advance to the next phase until all validations pass.**

Before proceeding to each phase, verify:

1. `dbt compile` succeeds
2. `dbt test` passes
3. Validation hooks report no errors

Hook configuration is defined in `.claude/settings.local.json`.
