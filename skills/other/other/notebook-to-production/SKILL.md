---
name: notebook-to-production
description: "Use when refactoring Jupyter notebooks into production code, productionizing data science workflows, or converting exploratory analysis into maintainable Python packages."
---

# Notebook to Production

## Refactoring Strategy

Always follow this order. Skipping stages creates brittle pipelines.

| Phase | Goal | Output |
|-------|------|--------|
| 1. Assess | Understand what the notebook actually does | Dependency map, data flow diagram |
| 2. Extract | Pull cells into functions and modules | Python package with clear API |
| 3. Test | Validate behavior matches notebook | Test suite with fixtures |
| 4. Configure | Externalize hardcoded values | Config files, env vars |
| 5. Schedule | Automate execution | DAG, cron job, or CI pipeline |
| 6. Monitor | Track runs, data quality, model drift | Logging, alerts, dashboards |

### Assessment Checklist

Before writing any code, answer these:

- What are the inputs? (files, databases, APIs)
- What are the outputs? (models, reports, tables, plots)
- Which cells are exploratory (delete) vs. essential (keep)?
- What's the execution order? (notebooks hide this)
- Are there hidden dependencies between cells? (shared mutable state)
- How often does this need to run?
- Who consumes the output?

## Notebook Anti-Patterns to Fix

| Anti-Pattern | Problem | Fix |
|---|---|---|
| Global mutable state | `df` modified across 20 cells | Functions with explicit inputs/outputs |
| Magic numbers | `df[df['score'] > 0.73]` | Named constants or config values |
| No error handling | Silent NaN propagation | Explicit validation, fail fast |
| Hidden dependencies | Cell 15 depends on cell 3's side effect | Explicit function call chain |
| Import scatter | `import pandas` in cell 1, `import sklearn` in cell 47 | Single imports block at top |
| Display-as-validation | `df.head()` instead of assertions | Proper assert/test statements |
| Path hardcoding | `pd.read_csv('/Users/alice/data.csv')` | Config-driven paths |
| Mega-cell | One cell with 200 lines | Break into focused functions |
| Re-execution sensitivity | Different results on re-run | Idempotent functions, fixed seeds |
| Credential leakage | API keys in cell output | Environment variables, secrets manager |

## Module Extraction Patterns

### Cell-to-Function Mapping

```python
# BEFORE: notebook cell
# Cell 5: Clean the data
df = pd.read_csv('sales.csv')
df = df.dropna(subset=['revenue'])
df['date'] = pd.to_datetime(df['date'])
df = df[df['revenue'] > 0]
df['month'] = df['date'].dt.to_period('M')

# AFTER: extracted function
def clean_sales_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Remove nulls, parse dates, filter positive revenue."""
    df = raw_df.dropna(subset=['revenue']).copy()
    df['date'] = pd.to_datetime(df['date'])
    df = df[df['revenue'] > 0]
    df['month'] = df['date'].dt.to_period('M')
    return df
```

### Key extraction rules:
- Every function takes explicit inputs, returns explicit outputs
- No function reads from or writes to global state
- `.copy()` DataFrames to prevent mutation leakage
- Type hints on all function signatures
- Docstrings on all public functions

### Function-to-Module Mapping

Group related functions into modules by pipeline stage:

```
cells 1-3   (load data)       → src/ingestion.py
cells 4-8   (clean/transform) → src/preprocessing.py
cells 9-12  (feature eng)     → src/features.py
cells 13-16 (model train)     → src/training.py
cells 17-20 (evaluate)        → src/evaluation.py
cells 21-23 (report/plot)     → src/reporting.py
```

### Pipeline Orchestration

```python
# src/pipeline.py
from src.ingestion import load_sales_data
from src.preprocessing import clean_sales_data
from src.features import build_features
from src.training import train_model
from src.evaluation import evaluate_model
from src.reporting import generate_report

def run_pipeline(config: dict) -> dict:
    raw = load_sales_data(config['data_path'])
    clean = clean_sales_data(raw)
    features = build_features(clean, config['feature_params'])
    model = train_model(features, config['model_params'])
    metrics = evaluate_model(model, features)
    report = generate_report(metrics, config['output_dir'])
    return {'model': model, 'metrics': metrics, 'report': report}
```

## Config Management

### Hierarchy (highest priority wins)

```
CLI arguments  →  Environment variables  →  config.yaml  →  defaults in code
```

### Config File Pattern

```yaml
# config.yaml
data:
  input_path: "s3://bucket/sales/"
  output_path: "s3://bucket/results/"

preprocessing:
  min_revenue: 0
  date_column: "date"

features:
  window_sizes: [7, 14, 30]
  categorical_columns: ["region", "product_type"]

model:
  algorithm: "xgboost"
  hyperparameters:
    max_depth: 6
    learning_rate: 0.1
    n_estimators: 500

random_seed: 42
```

```python
# src/config.py
from pathlib import Path
import yaml

def load_config(config_path: str = "config.yaml", overrides: dict | None = None) -> dict:
    with open(config_path) as f:
        config = yaml.safe_load(f)
    if overrides:
        _deep_merge(config, overrides)
    return config

def _deep_merge(base: dict, override: dict) -> None:
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(base.get(key), dict):
            _deep_merge(base[key], value)
        else:
            base[key] = value
```

### Environment Variable Pattern

```python
import os

# Secrets and environment-specific values ONLY
DATABASE_URL = os.environ["DATABASE_URL"]  # fail fast if missing
API_KEY = os.environ["API_KEY"]
ENV = os.environ.get("ENV", "development")  # default for non-secrets
```

Rule: config files for tunable parameters, env vars for secrets and deployment-specific values.

## Testing Data Pipelines

### Test Fixtures

```python
# tests/conftest.py
import pandas as pd
import pytest

@pytest.fixture
def sample_sales_df():
    return pd.DataFrame({
        'date': ['2025-01-01', '2025-01-02', '2025-01-03', None],
        'revenue': [100.0, -50.0, 200.0, 150.0],
        'region': ['US', 'EU', 'US', 'EU'],
    })

@pytest.fixture
def clean_sales_df(sample_sales_df):
    from src.preprocessing import clean_sales_data
    return clean_sales_data(sample_sales_df)
```

### Snapshot / Golden File Testing

```python
def test_feature_pipeline_output(clean_sales_df, tmp_path):
    result = build_features(clean_sales_df, window_sizes=[7])
    output_path = tmp_path / "features.csv"
    result.to_csv(output_path, index=False)

    golden = Path("tests/golden/features.csv")
    if not golden.exists():
        # First run: create golden file
        result.to_csv(golden, index=False)
        pytest.skip("Golden file created, re-run to validate")

    expected = pd.read_csv(golden)
    pd.testing.assert_frame_equal(result, expected)
```

### Data Contract Testing

```python
def test_clean_data_contract(clean_sales_df):
    """Validate the output schema of the cleaning step."""
    assert set(clean_sales_df.columns) >= {'date', 'revenue', 'month', 'region'}
    assert clean_sales_df['revenue'].min() > 0, "Negative revenue should be filtered"
    assert clean_sales_df['date'].dtype == 'datetime64[ns]'
    assert clean_sales_df['revenue'].isna().sum() == 0, "No null revenue allowed"
```

### What to Test

| Layer | Test Type | Example |
|-------|-----------|---------|
| Functions | Unit test | `clean_sales_data` removes nulls |
| Pipeline stages | Integration | Preprocessing output feeds into features |
| Full pipeline | End-to-end | Config in, report out, on sample data |
| Data quality | Contract | Schema, ranges, uniqueness constraints |
| Model | Regression | Metrics within threshold of baseline |

## Scheduling and Orchestration

### Decision Table

| Complexity | Frequency | Tool |
|---|---|---|
| Single script | Daily/weekly | cron / systemd timer |
| Linear pipeline, <5 steps | Daily | Makefile + cron |
| DAG with dependencies | Daily+ | Airflow / Dagster / Prefect |
| Event-driven | On data arrival | Cloud Functions + triggers |
| ML-specific (train/deploy) | Varies | Dagster / Kubeflow / MLflow |

### Minimal Dagster Example

```python
# pipelines/daily_sales.py
from dagster import asset, Definitions

@asset
def raw_sales():
    return load_sales_data("s3://bucket/sales/")

@asset
def clean_sales(raw_sales):
    return clean_sales_data(raw_sales)

@asset
def sales_features(clean_sales):
    return build_features(clean_sales, window_sizes=[7, 14, 30])

@asset
def sales_model(sales_features):
    return train_model(sales_features, {"max_depth": 6})

defs = Definitions(assets=[raw_sales, clean_sales, sales_features, sales_model])
```

### Cron + Script (Simplest)

```bash
# crontab -e
0 6 * * * cd /opt/pipeline && python -m src.pipeline --config config.yaml >> /var/log/pipeline.log 2>&1
```

Add a `__main__.py` entry point:

```python
# src/__main__.py
import argparse
from src.pipeline import run_pipeline
from src.config import load_config

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    args = parser.parse_args()
    config = load_config(args.config)
    result = run_pipeline(config)
    print(f"Pipeline complete. Metrics: {result['metrics']}")
```

## Artifact Management

| Artifact | Storage | Versioning |
|----------|---------|------------|
| Trained models | S3/GCS + model registry | Semantic version or run ID |
| Reports (HTML/PDF) | S3/GCS + link in Slack | Date-stamped |
| Data snapshots | S3/GCS partitioned by date | Date partition |
| Feature sets | Feature store or parquet | Git hash + timestamp |
| Config used | Logged with each run | Stored alongside artifacts |

Always log which config + code version produced which artifact. Reproducibility requires both.

## Project Structure Template

```
project/
├── config.yaml
├── pyproject.toml
├── README.md
├── notebooks/           # Exploratory only, not part of prod
│   └── exploration.ipynb
├── src/
│   ├── __init__.py
│   ├── __main__.py      # CLI entry point
│   ├── config.py
│   ├── pipeline.py      # Orchestration
│   ├── ingestion.py
│   ├── preprocessing.py
│   ├── features.py
│   ├── training.py
│   ├── evaluation.py
│   └── reporting.py
├── tests/
│   ├── conftest.py
│   ├── golden/          # Snapshot test data
│   ├── test_preprocessing.py
│   ├── test_features.py
│   ├── test_training.py
│   └── test_pipeline.py
├── pipelines/           # DAG definitions (Airflow/Dagster)
│   └── daily_sales.py
└── data/                # Local dev data only, gitignored
    ├── raw/
    └── processed/
```

## Gotchas

- **Notebook execution order**: Cells may have been run out of order. Restart-and-run-all before extracting to verify the actual flow.
- **Display side effects**: `df.head()`, `plt.show()`, and print statements are not logic. Remove them from production code; add proper logging instead.
- **Implicit pandas state**: `pd.set_option()` calls in early cells affect all subsequent cells. Make these explicit in config or function scope.
- **Memory assumptions**: Notebooks run on beefy dev machines. Production may have less RAM. Profile memory usage, consider chunked processing.
- **Package version drift**: Pin all dependencies in `pyproject.toml`. The notebook worked 6 months ago with different library versions.
- **Seed management**: `np.random.seed(42)` as a global is fragile. Pass `random_state` explicitly to every function that needs it.
- **Credential handling**: Never commit the notebook with cell outputs that contain API keys, tokens, or PII. Clear outputs before committing, or use `nbstripout`.
- **Circular imports**: When splitting one notebook into many modules, dependency cycles are common. Draw the import graph first.
- **Premature orchestration**: Get the pipeline working as a single script before adding Airflow/Dagster. Complexity layers should be earned.
