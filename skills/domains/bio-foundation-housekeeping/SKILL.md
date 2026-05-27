---
name: bio-foundation-housekeeping
description: Initialize a bioinformatics project scaffold with reproducible environments, schemas, and data cataloging. Use for new projects or repo setup.
---

# Bio Foundation Housekeeping

## When to use
- Initialize a bioinformatics project scaffold with reproducible environments, schemas, and data cataloging. Use for new projects or repo setup.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Target project root is writable.

## Inputs
- project root (path)
- metadata schema requirements
- workflow engine preference (optional)

## Outputs
- pixi.toml
- pixi.lock
- schemas/
- data/catalog.duckdb
- results/bio-foundation-housekeeping/report.md
- results/bio-foundation-housekeeping/logs/

## Steps
1. Create standard directory layout (data/, results/, schemas/, workflows/, src/, notebooks/).
2. Initialize Pixi workspace and lockfile; define tasks.
3. Define LinkML schemas and generate Pydantic models.
4. Create DuckDB catalog and register parquet tables.

## QC gates
- Schema generation succeeds and models are importable.
- pixi.lock is created and consistent with pixi.toml.
- DuckDB catalog is readable.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify project root exists and is writable.
- Validate generated schemas against expected fields.

## Tools
- pixi v0.43.0
- linkml v1.9.6
- pydantic v2.12.5
- duckdb v1.4.3

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [Pixi](docs/pixi.html) - Package and environment management
- [LinkML](docs/linkml.html) - Data modeling and schema generation
- [Pydantic](docs/pydantic.html) - Data validation using Python type hints
- [DuckDB](docs/duckdb.html) - In-process analytical database

## References
- See ../bio-skills-references.md
