---
name: creating-bauplan-pipelines
description: "Creates bauplan data pipeline projects with SQL and Python models. Use when starting a new pipeline, defining DAG transformations, writing models, or setting up bauplan project structure from scratch."
allowed-tools:
  - Bash(bauplan:*)
  - Read
  - Write
  - Glob
  - Grep
  - WebFetch(domain:docs.bauplanlabs.com)
---

# Creating a New Bauplan Data Pipeline

This skill guides you through creating a new bauplan data pipeline project from scratch, including the project configuration and SQL/Python transformation models.

## CRITICAL: Branch Safety

> **NEVER run pipelines on `main` branch.** Always use a development branch.

Branch naming convention: `<username>.<branch_name>` (e.g., `john.feature-pipeline`). Get your username with `bauplan info`. See [Workflow Checklist](#workflow-checklist) for exact commands.

## Prerequisites
Before creating the pipeline, verify that:
1. **You have a development branch** (not `main`)
2. Source tables exist in the bauplan lakehouse (the default namespace is `bauplan`)
3. You understand the schema of the source tables

## Table References
- Always use fully-qualified names: `<namespace>.<table_name>`
- Default namespace: `bauplan`
- Example: `bauplan.taxi_fhvhv`

## Pipeline as a DAG
A bauplan pipeline is a DAG of functions (models). Key rules:
1. **Models**: Python functions (preferred) or SQL queries that transform data
2. **Source Tables**: Existing lakehouse tables - entry points to your DAG
3. **Inputs**: Each model can take **multiple tables** via `bauplan.Model()` references, either from the outputs ofr previous models or as source tables in the lakehouse
4. **Outputs**: Each model produces **exactly one table**:
   - Python: output name = function name (`def clean_trips()` → `clean_trips`)
   - SQL: output name = filename (`trips.sql` → `trips`)
5. **Topology**: Implicitly defined by input references - Bauplan determines the execution order
6. **Expectations**: Data quality functions that take tables as input and return a **boolean**.

### Example DAG
```text
[lakehouse: taxi_fhvhv] ──→ [trips.sql] ──→ [clean_trips] ──→ [daily_summary]
                                                ↑
[lakehouse: taxi_zones] ────────────────────────┘
```

In this example:
- `taxi_fhvhv` and `taxi_zones` are source tables (already in lakehouse)
- `trips.sql` reads from `taxi_fhvhv` (SQL model, first node)
- `clean_trips` takes `trips` and `taxi_zones` as inputs (Python model, multiple inputs)
- `daily_summary` takes `clean_trips` as input (Python model, single input)

## Required User Input
Before writing a pipeline, you MUST gather the following information from the user:
1. **Pipeline purpose** (required): What transformations should the DAG perform? What is the business logic or goal?
2. **Source tables** (required): Which tables from the lakehouse should be used as inputs? Verify they exist with `bauplan table get`
3. **Output tables** (required): Which tables should be materialized at the end of the pipeline? These are the final outputs visible to downstream consumers
4. **Materialization strategy** (optional): Should output tables use `REPLACE` (default) or `APPEND`?
5. **Strict mode** (optional): Should the pipeline run in strict mode? If yes, all CLI commands will use `--strict` flag, which fails on issues like output column mismatches during dry-run, allowing immediate error detection and correction.

**If any required item is missing, ask the user before writing any code.**

### Strict Mode (--strict flag)
When strict mode is enabled, append `--strict` to all `bauplan run` commands:

```bash
# Without strict mode (default)
bauplan run --dry-run
bauplan run

# With strict mode enabled
bauplan run --dry-run --strict
bauplan run --strict
```

**Benefits of strict mode:**
- Fails immediately on output column mismatches
- Fails immediately if an expectation fails
- Allows you to rectify declaration errors before pipeline completion
- Recommended when iterating on pipeline development

## Project Structure
A bauplan project is a folder containing:

```text
my-project/
  bauplan_project.yml    # Required: project configuration
  models.py              # Preferred: Python models (one file can have >1 models and contain an entire data transformation pipeline)
  model.sql              # Optional: SQL models (pipelines should be broken into several files each containing a single SQL model)
  expectations.py        # Optional: data quality tests (if any - one file can have more than one expectation test)
```

## bauplan_project.yml
Every project is a separate folder which requires this configuration file:

```yaml
project:
  id: <unique-uuid>       # Generate a unique UUID
  name: <project_name>    # Descriptive name for the project
```

## Python Models (Preferred)
Python models are individual steps in transformation pipelines.
A pipeline is composed by several models that form a Direct-Acyclic-Graph (DAG).
They are defined as Python functions with decorators.

### Decorators
- `@bauplan.model()` - Registers function as a model
The most important parameters of this decorator are `columns` and `materialization_strategy`:
  - `@bauplan.model(columns=[...])` - Specify expected output columns for validation (Optional but recommended)
  - `@bauplan.model(materialization_strategy='REPLACE')` - Persist the output into lakehouse as an Iceberg table

- `@bauplan.python('3.11', pip={'pandas': '1.5.3'})` - Specifies Python version and the packages needed for the function to run

### Best Practice: Output Columns Validation
> **IMPORTANT**: whenever possible, specify the `columns` parameter in `@bauplan.model()` to define the expected output schema. This enables automatic validation of your model's output.

First, check the schema of your source tables to understand input columns. Then specify the output columns based on your transformation:

```python
# If input has columns: [id, name, age, city]
# And transformation drops 'city' column
# Then output columns should be: [id, name, age]

@bauplan.model(columns=['id', 'name', 'age'])
```

### Best Practice: Docstrings with Output Schema

> **IMPORTANT**: Every Python model should have a docstring describing the transformation and showing the output table structure as an ASCII table (if the table is too wide, show only key columns, if values are too large, truncate them in the cells).

```python
@bauplan.model(columns=['id', 'name', 'age'])
@bauplan.python('3.11')
def clean_users(data=bauplan.Model('raw_users')):
    """
    Cleans user data by removing invalid entries and dropping the city column.

    | id  | name  | age |
    | --- | ----- | --- |
    | 1   | Alice | 30  |
    | 2   | Bob   | 25  |
    """
    # transformation logic
    return data.drop_columns(['city'])
```

### Best Practice: I/O Pushdown with `columns` and `filter`

> **IMPORTANT**:
> Use `columns` and `filter` parameters in `bauplan.Model()` to restrict the data read.
> This enables I/O pushdown, dramatically reducing the amount of data transferred and improving performance.
> Do not read columns you don't need.

**Whenever possible, specify:**
- `columns`: List only the columns your model actually needs
- `filter`: SQL-like filter expression to restrict rows at the storage level, if appropriate
- See [examples.md](examples.md#io-pushdown-with-column-selection-and-filtering) for complete guide on pushing down to the data lake efficiently.


### Base Python Model
```python
# import bauplan globally, but DO NOT import other packages used in the single models
# Use the python decorator, instead and import the dependencies inside the functions
import bauplan

# Use the model decorator to register the function as a step in a pipeline
# and to define the expected output schema and to define the materialization strategy
@bauplan.model(
    columns=['pickup_datetime', 'PULocationID', 'trip_miles'],
    materialization_strategy='REPLACE'
)
# Use the python decorator to specify the Python version and dependencies
@bauplan.python('3.11', pip={'polars': '1.15.0'})
def clean_trips(
    # Use columns and filter for I/O pushdown
    data=bauplan.Model(
        'trips',
        columns=['pickup_datetime', 'PULocationID', 'trip_miles'],
        filter="trip_miles > 0"
    )
):
    """
    Filters trips to include only those with positive mileage.

    | pickup_datetime     | PULocationID | trip_miles |
    | ------------------- | ------------ | ---------- |
    | 2022-12-01 08:00:00 | 123          | 5.2        |
    """
    # import the packages declared in the Python decorator inside the function so the environments remain separated and independent
    import polars as pl

    # write transformation logic in the function
    # inputs are Arrow Tables - conversion is needed to use other DataFrame libraries
    df = pl.from_arrow(data)
    df = df.filter(pl.col('trip_miles') > 0.0)

    # outputs must be table-like objects like Pandas, Polars, Arrow DataFrames or list of dictionaries
    # Each model produces exactly one table
    return df.to_arrow()
```

### Python Model with Multiple Inputs
Models can take multiple tables as input - just add more `bauplan.Model()` parameters:

See [examples.md](examples.md#python-model-with-multiple-inputs) for complete multi-input examples with Polars.

## SQL Models (First Nodes Only)
SQL models are `.sql` files where:
- The **filename** becomes the output table name
- The **FROM clause** defines input tables
- Optional: Add materialization strategy as a comment

Use SQL models only when reading from existing lakehouse tables:

```sql
-- trips.sql
-- First node: reads from taxi_fhvhv table in the lakehouse
SELECT
    pickup_datetime,
    PULocationID,
    trip_miles
FROM taxi_fhvhv
WHERE pickup_datetime >= '2022-12-01'
```

Output table: `trips` (from filename)
Input table: `taxi_fhvhv` (FROM clause, exists in lakehouse)

## When to Use Python Models vs SQL models
- **Python models**: PREFERRED FOR ALL TRANSFORMATIONS
- **SQL models**: Use ONLY for very large nodes that read directly from source tables in the lakehouse (tables outside your pipeline graph)
- **IMPORTANT**: SQL models should be LIMITED to **first nodes** in the pipeline graph only.

This ensures consistency and allows for better control over transformations, output schema validation, and documentation.


## Workflow Checklist
Copy this checklist and track your progress:

Pipeline Creation Progress:
- [ ] Step 1: Get username → `bauplan info`
- [ ] Step 2: Checkout main → `bauplan branch checkout main`
- [ ] Step 3: Create dev branch → `bauplan branch create <username>.<branch_name>`
- [ ] Step 4: Checkout dev branch → `bauplan branch checkout <username>.<branch_name>`
- [ ] Step 5: Verify source tables → `bauplan table get <namespace>.<table_name>`, Optional for data preview: `bauplan query "SELECT * FROM <namespace>.<table_name> LIMIT 3"`
- [ ] Step 6: Create project folder with `bauplan_project.yml`
- [ ] Step 7: Write Python model(s)/SQL models for transformations respecting the guidelines
- [ ] Step 8: Verify materialization decorators (see Materialization Checklist below)
- [ ] Step 9: Dry run → `bauplan run --dry-run [--strict if strict mode]`
- [ ] Step 10: Run pipeline → `bauplan run [--strict if strict mode]`


> **CRITICAL**: NEVER EVER run on `main` branch. Always complete the steps 2-4 to ensure you're on a development branch.

## Materialization Checklist
After writing models, verify that each model has the correct `materialization_strategy` based on user requirements:

| Model Type | No Materialization (intermediate) | Materialized Output                                                     |
| ---------- | --------------------------------- | ----------------------------------------------------------------------- |
| **Python** | `@bauplan.model()` (no strategy)  | `@bauplan.model(materialization_strategy='REPLACE')` or `'APPEND'`      |
| **SQL**    | No comment needed                 | Add comment: `-- bauplan: materialization_strategy=REPLACE` or `APPEND` |

**Verify for each model:**
- [ ] Intermediate tables (not final outputs): NO `materialization_strategy` specified
- [ ] Final output tables requested by user: `materialization_strategy='REPLACE'` (default) or `'APPEND'`
- [ ] If user specified APPEND for any table: confirm `materialization_strategy='APPEND'` is set

Example Python decorator for materialized output:
```python
@bauplan.model(materialization_strategy='REPLACE', columns=['col1', 'col2'])
```

Example SQL comment for materialized output:
```sql
-- bauplan: materialization_strategy=REPLACE
SELECT * FROM source_table
```

## Verifying Pipeline Output
After successful run:
- Check table exists: `bauplan table get <namespace>.<output_table>`
- Preview data: `bauplan query "SELECT * FROM <namespace>.<output_table> LIMIT 5"`

## Advanced Examples
See [examples.md](examples.md) for:
- APPEND materialization strategy
- DuckDB queries in Python models
- Data quality expectations
- Multi-stage pipelines
