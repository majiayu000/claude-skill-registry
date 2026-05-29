---
name: tech-stack
description: Describes the primary technologies, frameworks, libraries, and language conventions used in this codebase.
---

# Tech Stack Overview

## Language-Specific Conventions

- **Python**: See [PYTHON.md](./PYTHON.md) for detailed conventions and examples

## Primary Languages

| Language | Usage | Version |
|----------|-------|---------|
| Python | datagen, notebooks | 3.10+ |
| PySpark | Fabric notebooks | Spark 3.x |
| KQL | Eventhouse queries | N/A |
| JSON/YAML | Fabric item definitions | N/A |

## Frameworks & Libraries

### Data Generation (datagen)
- **DuckDB**: Local analytical database for historical data
- **Faker**: Synthetic data generation
- **Pydantic**: Data validation and event schemas
- **azure-eventhub**: Event streaming to Azure

### Lakehouse
- **Delta Lake**: ACID transactions, schema enforcement
- **PySpark**: Distributed data processing

### Real-Time Analytics
- **Microsoft Fabric Eventhouse**: KQL-based analytics
- **Eventstream**: Event routing and transformation

## Project Architecture

```
Event Flow:
  datagen (Python)
    → Azure Event Hubs
    → Eventstream
    → KQL Tables + Lakehouse Bronze

Data Layers:
  Bronze (raw JSON)
    → Silver (typed Delta)
    → Gold (aggregated Delta)
    → Semantic Model (Power BI)
```

## Key Dependencies

See `datagen/pyproject.toml` for Python dependencies.

Core packages:
- `pydantic` - Schema validation
- `duckdb` - Local analytics
- `faker` - Data generation
- `azure-eventhub` - Event streaming
