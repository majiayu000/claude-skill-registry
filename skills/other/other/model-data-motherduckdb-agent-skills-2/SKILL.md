---
name: model-data
description: Design database schemas and data models in MotherDuck. Use when creating tables, choosing data types, defining relationships, or restructuring data for analytics workloads.
license: MIT
---

# Model Data in MotherDuck

Use this skill when creating tables, designing schemas, choosing data types, defining relationships between tables, or restructuring data for analytical workloads.

## Prerequisites

- MotherDuck connection established via `connect`
- Existing source shape understood via `explore`
- DuckDB SQL syntax available via `duckdb-sql`

## Default Posture

- Design for analytical reads, not transactional writes.
- Prefer wide denormalized tables and pre-aggregated serving tables over highly normalized OLTP-style schemas.
- Use fully qualified names and add comments to tables and columns.
- Use `NOT NULL` aggressively; do not assume primary keys or foreign keys are enforced.
- Separate `raw`, `staging`, and `analytics` lifecycle stages when the project is non-trivial.

## Workflow

1. Inspect the current source tables and actual column types before designing new models.
2. Choose the target lifecycle stage and grain for each modeled table.
3. Pick explicit types, nullability, and comments before writing DDL.
4. Decide between a table, CTAS rebuild, or view based on freshness and cost.
5. Validate the resulting model against the analytical queries or dashboards it must support.

## Open Next

- `references/MODELING_PLAYBOOK.md` for schema patterns, data-type guidance, CTAS/view decisions, complex types, constraints, and common modeling mistakes

## Related Skills

- `duckdb-sql` for type syntax and function details
- `query` for executing DDL, rebuilds, and validation queries
- `explore` for understanding the source schema before remodeling
- `load-data` for ingestion paths that feed the modeled tables
