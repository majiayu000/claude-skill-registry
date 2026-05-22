---
name: dbt
description: dbt data transformation with SQL. Use for data pipelines.
---

# dbt (Data Build Tool)

dbt manages data transformation in the warehouse using SQL. v2.0 introduces the **Fusion Engine** (Rust) for performance.

## When to Use

- **Data Modeling**: Converting raw tables into "Gold" tables.
- **Testing**: `not_null`, `unique` tests defined in YAML.
- **Documentation**: Auto-generating data dictionaries.

## Core Concepts

### Models (`.sql`)

Select statements that dbt compiles into `CREATE VIEW/TABLE`.

### Refs (`{{ ref('users') }}`)

Dependency management. dbt builds the DAG automatically.

### Semantic Layer

Defining metrics ("Revenue") in code so all BI tools use the same definition.

## Best Practices (2025)

**Do**:

- **Use Git**: Treat data models like software code.
- **Use Incremental Models**: Only process new data to save cost.
- **Use dbt Mesh**: For cross-project dependencies in large orgs.

**Don't**:

- **Don't put logic in BI tools**: Put it in dbt.

## References

- [dbt Documentation](https://docs.getdbt.com/)
