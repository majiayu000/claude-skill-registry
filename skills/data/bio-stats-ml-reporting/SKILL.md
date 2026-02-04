---
name: bio-stats-ml-reporting
description: Aggregate results, train ML models, and produce reports with validated references.
---

# Bio Stats ML Reporting

## When to use
- Aggregate results, train ML models, and produce reports with validated references.

## Prerequisites
- Tools installed via pixi (see pixi.toml).
- Results tables and metadata are available.

## Inputs
- results/*.parquet or results/*.tsv
- metadata.tsv

## Outputs
- results/bio-stats-ml-reporting/models/
- results/bio-stats-ml-reporting/metrics.tsv
- results/bio-stats-ml-reporting/report.md
- results/bio-stats-ml-reporting/logs/

## Steps
1. Join outputs in DuckDB and build feature tables.
2. Train baseline models and evaluate with cross-validation.
3. Generate reports and validate references.

## QC gates
- Model performance sanity checks pass.
- Reference validation passes.
- On failure: retry with alternative parameters; if still failing, record in report and exit non-zero.

## Validation
- Verify input tables are readable and schema-consistent.

## Tools
- duckdb v1.4.3
- scikit-learn v1.8.0
- xgboost v3.1.3
- crossrefapi v1.7.0

## Paper summaries (2023-2025)
- summaries/ (include example use cases and tool settings used)

## Tool documentation
- [DuckDB](docs/duckdb.md) - In-process analytical database for data aggregation
- [scikit-learn](docs/scikit-learn.html) - Machine learning library
- [XGBoost](docs/xgboost.html) - Gradient boosting framework
- [Crossref API](docs/crossref.html) - Reference validation and metadata retrieval

## References
- See ../bio-skills-references.md
