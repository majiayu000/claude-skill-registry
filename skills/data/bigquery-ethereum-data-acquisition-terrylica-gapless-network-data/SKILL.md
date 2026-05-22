---
name: bigquery-ethereum-data-acquisition
description: Workflow for acquiring historical Ethereum blockchain data using Google BigQuery free tier. Empirically validated for cost estimation, streaming downloads, and DuckDB integration. Use when planning bulk historical data acquisition or comparing data source options for blockchain network metrics.
---

# BigQuery Ethereum Data Acquisition

## Overview

Workflow for acquiring 5 years of Ethereum blockchain data (2020-2025, ~12.44M blocks) using Google BigQuery's public dataset within free tier limits. Includes column selection analysis for ML/time-series forecasting, cost optimization, and empirically validated download workflows.

**Status**: ✅ Empirically validated (v0.2.0, 2025-11-07)

## When to Use This Skill

Use when:

- Evaluating BigQuery as a data source for Ethereum historical data
- Planning bulk historical blockchain data acquisition
- Optimizing column selection for feature engineering
- Calculating query costs and free tier utilization
- Comparing BigQuery vs RPC polling approaches
- Streaming downloads without BigQuery storage

## Core Workflow

This skill follows a 5-step workflow for acquiring Ethereum data from BigQuery:

| Step                    | Purpose                         | Output            | Key Metric                |
| ----------------------- | ------------------------------- | ----------------- | ------------------------- |
| **1. Free Tier Limits** | Understand query/storage limits | Limits documented | 1 TB query, 10 GB storage |
| **2. Column Selection** | Optimize for ML/time-series     | 11 columns chosen | 0.97 GB (97% savings)     |
| **3. Cost Validation**  | Dry-run query cost              | Cost estimate     | 0.1% of free tier         |
| **4. Stream Download**  | Parquet download (no storage)   | .parquet file     | 62 bytes/row              |
| **5. DuckDB Import**    | Load for analysis               | DuckDB database   | <100ms query time         |

**Detailed workflow**: See `references/workflow-steps.md` for complete step-by-step guide with SQL queries, bash commands, and validated results for each step.

**Quick start**: Run `uv run scripts/test_bigquery_cost.py` to validate cost, then `uv run scripts/download_bigquery_to_parquet.py <start> <end> <output>` to download.

## Cost Analysis

**Optimized selection**: 11 columns = 0.97 GB (0.1% of free tier, 97% cost savings vs all 23 columns)

**Key finding**: BigQuery is 624x faster than RPC polling (<1 hour vs 26 days for 12.44M blocks).

**Full analysis**: See `references/cost-analysis.md` for detailed cost comparison, column selection rationale, and RPC provider comparison.

## Prerequisites

**One-time setup**: gcloud auth, Python dependencies (google-cloud-bigquery, pandas, pyarrow, db-dtypes)

**Setup guide**: See `references/setup-guide.md` for complete authentication setup, dependency installation, and verification commands.

## Scripts

Validated scripts (v0.2.0):

- `test_bigquery_cost.py` - Dry-run cost estimation (0.97 GB for 12.44M blocks)
- `download_bigquery_to_parquet.py` - Streaming Parquet download (62 bytes/row validated)

**Templates and usage**: See `scripts/README.md` for complete usage examples, dependencies, and validated results.

## References

### Workflow Documentation

- `references/workflow-steps.md` - Complete 5-step workflow with SQL queries, bash commands, and validated results
- `references/cost-analysis.md` - Detailed cost comparison, column selection rationale, RPC provider comparison
- `references/setup-guide.md` - Authentication setup, dependencies, verification commands

### Research Documents

- `references/bigquery_cost_comparison.md` - Empirical cost analysis (6 vs 11 vs 23 columns)
- `references/ethereum_columns_ml_evaluation.md` - Column-by-column ML value analysis
- `references/bigquery_complete_ethereum_data.md` - Complete dataset catalog (11 tables)
- `references/bigquery_cost_estimate.md` - Free tier limits and methodology
- `references/littleblack-hardware-report.md` - Local vs cloud hardware comparison

### Scripts & Validation

- `scripts/README.md` - Complete script usage guide with validated results
- `VALIDATION_STATUS.md` - Empirical test results, testing methodology, dependencies validated

## Verification After Acquisition

**Important**: This skill covers data acquisition from BigQuery (downloading historical Ethereum blocks), but does NOT verify the data actually landed in ClickHouse.

After completing BigQuery download:

- Use the **historical-backfill-execution** skill
- Run `scripts/clickhouse/verify_blocks.py` to verify database state
- Confirm expected block count (~23.8M blocks for 2015-2025 backfill)

**Common workflow**:

1. Download from BigQuery using this skill (Step 4 above)
2. Insert to ClickHouse via `chunked_backfill.sh`
3. **Verify ClickHouse state** using historical-backfill-execution skill
4. Check yearly breakdown to ensure complete coverage

See `historical-backfill-execution` skill for database verification and troubleshooting missing data.

## Related Skills

- `historical-backfill-execution` - ClickHouse database verification and backfill operations
- `blockchain-rpc-provider-research` - RPC rate limit comparison and provider evaluation
- `blockchain-data-collection-validation` - Empirical validation workflow for data pipelines
