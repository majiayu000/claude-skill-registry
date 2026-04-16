---
name: motherduck-model-data
description: Design and build database schemas and data models in MotherDuck. Produces a file-based project scaffold. Use when creating tables, choosing data types, defining relationships, or restructuring data for analytics workloads.
argument-hint: [table-or-model-goal]
license: MIT
---

# Model Data in MotherDuck

Use this skill when creating data models, tables, designing schemas, choosing data types, defining relationships between tables, or restructuring data for analytical workloads.

## Core Behavior

**When a user asks questions like "build a data model", "model my data", or "create a transformation layer", the default output is a file-based project scaffold — not just SQL executed directly in the warehouse.**

The project scaffold includes:

- **SQL files** organized by lifecycle stage (`raw/`, `staging/`, `analytics/`)
- **A manifest** (`model_manifest.yml`) defining the DAG: model names, dependencies, materialization strategy, and target database

This is a lightweight framework-agnostic convention for organizing SQL transformations that can be reviewed, versioned, and rerun.

## Prerequisites

- MotherDuck connection established via `motherduck-connect`
- Existing source shape understood via `motherduck-explore`
- DuckDB SQL syntax available via `motherduck-duckdb-sql`

## Default Posture

- Design for analytical reads, not transactional writes.
- Prefer wide denormalized tables and pre-aggregated serving tables over highly normalized OLTP-style schemas.
- Use fully qualified names and add comments to tables and columns.
- Use `NOT NULL` aggressively; do not assume primary keys or foreign keys are enforced.
- Separate `raw`, `staging`, and `analytics` lifecycle stages when the project is non-trivial.
- Always produce SQL files — never execute transformations directly in the warehouse without first writing them to files.
- Always produce a manifest — every model must declare its dependencies so the DAG is explicit and reproducible.

## Workflow

1. Inspect the current source tables and actual column types before designing new models.
2. Choose the target lifecycle stage and grain for each modeled table. Map dependencies between models.
3. Create the project directory structure with SQL files and manifest.
4. Author each model as a standalone SQL file. Use explicit types, nullability, comments, and fully qualified names. Decide between a table, CTAS rebuild, or view based on freshness and cost.
5. Fill in the manifest with model metadata: name, path, stage, materialization, database, and `depends_on` references.
6. Run the models against the warehouse and verify the resulting tables match expected grain and row counts.

## Expected Project Structure

```
<project-name>/
  models/
    raw/
      raw_<entity>.sql           -- DDL for raw landing tables
    staging/
      stg_<entity>.sql           -- Deduplicated, typed, filtered
    analytics/
      dim_<entity>.sql           -- Dimension tables
      fct_<entity>.sql           -- Fact / metric tables
  model_manifest.yml             -- DAG: names, deps, materialization
```

## When to Skip the Scaffold

If the user explicitly asks for a single table, a quick DDL statement, or an ad-hoc exploration query, produce the SQL directly. The scaffold is the default for **modeling work** — multi-table, multi-stage transformations with dependencies.

## Open Next

- `references/MODELING_PLAYBOOK.md` for schema patterns, data-type guidance, CTAS/view decisions, complex types, constraints, project scaffold conventions, and common modeling mistakes

## Related Skills

- `motherduck-duckdb-sql` for type syntax and function details
- `motherduck-query` for executing DDL, rebuilds, and validation queries
- `motherduck-explore` for understanding the source schema before remodeling
- `motherduck-load-data` for ingestion paths that feed the modeled tables
