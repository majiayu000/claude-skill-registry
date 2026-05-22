---
name: hugging-face-datasets
description: >-
  Automate Hugging Face dataset lifecycle: create repos, configure schemas,
  stream row uploads with template validation, and query/transform any Hub
  dataset using DuckDB SQL via the hf:// protocol. Includes dataset_manager.py
  for CRUD operations and sql_manager.py for SQL-based exploration, filtering,
  joining, and exporting. Scripts use PEP 723 inline deps and run with uv.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Task
metadata:
  version: "1.0.0"
  author: "platxa-skill-generator"
  tags:
    - automation
    - datasets
    - hugging-face
    - sql
    - data-management
  provenance:
    upstream_source: "hugging-face-datasets"
    upstream_sha: "c0e08fdaa8ed6929110c97d1b867d101fd70218f"
    regenerated_at: "2026-02-04T15:30:00Z"
    generator_version: "1.0.0"
    intent_confidence: 0.58
---

# Hugging Face Dataset Management

Automate dataset creation, content management, and SQL-based querying on the Hugging Face Hub.

## Overview

This skill provides two complementary automation scripts for working with Hugging Face Hub datasets:

- **dataset_manager.py** -- Create repositories, configure schemas with system prompts, validate rows against templates (chat, classification, QA, completion, tabular), and stream uploads via the HfApi.
- **sql_manager.py** -- Query any Hub dataset with DuckDB SQL through the `hf://` protocol. Supports schema discovery, sampling, filtering, aggregation, cross-dataset joins, and exporting results to Parquet/JSONL or pushing back to Hub.

Both scripts use PEP 723 inline dependency metadata and run with `uv run` (no virtual environment setup required).

**Integration with HF MCP Server:** Use the MCP server for dataset discovery and metadata retrieval. Use this skill for dataset creation, editing, SQL queries, and data transformation.

## Triggers

Run this automation when:
- User needs to create a new dataset repository on Hugging Face Hub
- User wants to add rows to an existing dataset with schema validation
- User needs to query, filter, or transform a Hub dataset using SQL
- User wants to create subsets, join datasets, or export data locally
- User asks about dataset templates (chat, QA, classification, tabular)

## Prerequisites

Before running, ensure:
- `uv` package manager is installed (`pip install uv` or download from https://astral.sh/uv/install.sh)
- `HF_TOKEN` environment variable is set with a write-access Hugging Face token
- For private datasets, the token must have read access to the target repository

Verify setup:

```bash
uv --version
echo $HF_TOKEN | head -c 10
```

## Process: Dataset Creation

### Step 1: Initialize a Repository

```bash
uv run scripts/dataset_manager.py init \
  --repo_id "username/my-dataset" \
  --private
```

Creates the repository on Hub with a default README. If the repo already exists, the script continues without error.

### Step 2: Configure the Dataset

Store a system prompt and metadata in `config.json`:

```bash
uv run scripts/dataset_manager.py config \
  --repo_id "username/my-dataset" \
  --system_prompt "You are a helpful coding assistant..."
```

### Step 3: Add Rows with Template Validation

Choose a template that matches your data format:

| Template | Required Fields | Use Case |
|----------|----------------|----------|
| `chat` | messages (role + content array) | Conversational AI training |
| `classification` | text, label | Sentiment, intent, topic |
| `qa` | question, answer | Reading comprehension, factual QA |
| `completion` | prompt, completion | Language modeling, code completion |
| `tabular` | columns, data | Structured regression/classification |
| `custom` | (flexible) | Any schema |

```bash
uv run scripts/dataset_manager.py add_rows \
  --repo_id "username/my-dataset" \
  --template qa \
  --rows_json '[{"question": "What is DuckDB?", "answer": "An in-process SQL OLAP database."}]'
```

### Step 4: Quick Setup (All-in-One)

Create repo, configure, and add template examples in a single command:

```bash
uv run scripts/dataset_manager.py quick_setup \
  --repo_id "username/my-dataset" \
  --template chat
```

## Process: SQL Querying

### Step 1: Explore Dataset Structure

```bash
# Schema discovery
uv run scripts/sql_manager.py describe --dataset "cais/mmlu"

# Random sample
uv run scripts/sql_manager.py sample --dataset "cais/mmlu" --n 5

# Row count with filter
uv run scripts/sql_manager.py count --dataset "cais/mmlu" --where "subject='nutrition'"

# Value distribution
uv run scripts/sql_manager.py histogram --dataset "cais/mmlu" --column "subject" --bins 20
```

### Step 2: Query with SQL

Use `data` as the table alias (replaced internally with the `hf://` path):

```bash
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT subject, COUNT(*) as cnt FROM data GROUP BY subject ORDER BY cnt DESC"
```

Specify config or split:

```bash
uv run scripts/sql_manager.py query \
  --dataset "ibm/duorc" \
  --config "ParaphraseRC" \
  --split "test" \
  --sql "SELECT * FROM data LIMIT 5"
```

### Step 3: Transform and Push

Filter data and push results to a new Hub repository:

```bash
uv run scripts/sql_manager.py query \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject IN ('nutrition', 'anatomy')" \
  --push-to "username/mmlu-medical-subset" \
  --private
```

Use the transform command for structured SQL clauses:

```bash
uv run scripts/sql_manager.py transform \
  --dataset "cais/mmlu" \
  --select "subject, COUNT(*) as cnt" \
  --group-by "subject" \
  --order-by "cnt DESC" \
  --limit 10
```

### Step 4: Export Locally

```bash
# Parquet export
uv run scripts/sql_manager.py export \
  --dataset "cais/mmlu" \
  --sql "SELECT * FROM data WHERE subject='nutrition'" \
  --output "nutrition.parquet" \
  --format parquet

# JSONL export
uv run scripts/sql_manager.py export \
  --dataset "squad" \
  --sql "SELECT * FROM data LIMIT 100" \
  --output "sample.jsonl" \
  --format jsonl
```

### Step 5: Raw SQL and Cross-Dataset Joins

For queries with full `hf://` paths or multi-dataset joins:

```bash
uv run scripts/sql_manager.py raw --sql "
  SELECT a.question, b.context
  FROM 'hf://datasets/cais/mmlu@~parquet/default/train/*.parquet' a
  JOIN 'hf://datasets/squad@~parquet/default/train/*.parquet' b
  ON a.subject = b.title
  LIMIT 100
"
```

## Verification

After running any command, verify:
- **init** -- Repository appears at `https://huggingface.co/datasets/username/my-dataset`
- **add_rows** -- Script prints row count confirmation; check file in `data/` folder on Hub
- **query** -- Results printed to stdout as JSON; validate row count matches expectation
- **push-to** -- Target repository created on Hub with correct row count
- **export** -- Local file exists and is readable (`duckdb -c "SELECT * FROM 'file.parquet' LIMIT 5"`)

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| `HF_TOKEN not set` | Missing env var | `export HF_TOKEN=hf_...` |
| `409 Conflict` on init | Repo already exists | Safe to ignore; script continues |
| `Template not found` | Invalid template name | Run `list_templates` to see available options |
| `JSON parse error` | Malformed --rows_json | Validate JSON with `echo '...' \| python3 -m json.tool` |
| `Query error: hf://` | Invalid dataset path | Verify dataset exists: `uv run scripts/sql_manager.py info --dataset "org/name"` |
| `COPY failed` | Output path not writable | Check directory permissions and disk space |

See `references/sql-patterns.md` for DuckDB SQL functions and `references/hf-path-format.md` for the `hf://` protocol.

## Safety

### Idempotency

- **init**: Idempotent -- re-running on existing repo is safe
- **add_rows**: Not idempotent -- each call appends a new JSONL chunk with a timestamp filename
- **query/describe/sample/count**: Read-only, always safe
- **push-to**: Creates or overwrites the target repository split

### Reversibility

- Hub repos can be deleted from the web UI or via `HfApi().delete_repo()`
- Individual data files can be removed with `HfApi().delete_file()`
- Exported local files can be deleted normally

## Scripts Reference

| Script | Purpose | Key Commands |
|--------|---------|--------------|
| `dataset_manager.py` | Dataset CRUD | init, config, add_rows, quick_setup, stats, list_templates |
| `sql_manager.py` | SQL querying | query, describe, sample, count, histogram, unique, transform, export, raw, info |

All scripts accept `--help` for full argument documentation.

## Commands Reference

```bash
# Dataset Manager
uv run scripts/dataset_manager.py init --repo_id REPO [--private]
uv run scripts/dataset_manager.py config --repo_id REPO --system_prompt "..."
uv run scripts/dataset_manager.py add_rows --repo_id REPO --template TYPE --rows_json JSON
uv run scripts/dataset_manager.py quick_setup --repo_id REPO --template TYPE
uv run scripts/dataset_manager.py stats --repo_id REPO
uv run scripts/dataset_manager.py list_templates

# SQL Manager
uv run scripts/sql_manager.py query -d DATASET --sql SQL [--push-to REPO] [--private]
uv run scripts/sql_manager.py describe -d DATASET
uv run scripts/sql_manager.py sample -d DATASET [--n N] [--seed SEED]
uv run scripts/sql_manager.py count -d DATASET [--where FILTER]
uv run scripts/sql_manager.py histogram -d DATASET --column COL [--bins N]
uv run scripts/sql_manager.py unique -d DATASET --column COL
uv run scripts/sql_manager.py transform -d DATASET [--select ...] [--where ...] [--group-by ...] [--order-by ...]
uv run scripts/sql_manager.py export -d DATASET -o FILE [--format parquet|jsonl] [--sql SQL]
uv run scripts/sql_manager.py raw --sql "SELECT ... FROM 'hf://...'"
uv run scripts/sql_manager.py info -d DATASET
```
