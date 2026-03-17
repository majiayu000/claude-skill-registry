---
name: nixtla-timegpt2-migrator
description: |
  Assists users in migrating their codebase and data pipelines from TimeGPT-1 to TimeGPT-2.
  Use when upgrading to the latest version of TimeGPT, ensuring compatibility, and optimizing performance.
  Trigger with "migrate to TimeGPT-2", "upgrade TimeGPT", "TimeGPT compatibility".
allowed-tools: "Read,Write,Edit,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT-2 Migrator

Facilitates a smooth transition from TimeGPT-1 to TimeGPT-2.

## Purpose

Automates the migration process from TimeGPT-1 to TimeGPT-2, identifying compatibility issues and generating updated code.

## Overview

Evaluates existing TimeGPT-1 workflows for compatibility with TimeGPT-2. Identifies potential breaking changes and suggests necessary code modifications. Employs API checks and data schema validation. Provides updated code snippets and configuration examples for TimeGPT-2. Generates a migration report summarizing the changes required.

## Prerequisites

**Tools**: Read, Write, Edit, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas matplotlib statsforecast pyyaml
```

## Instructions

### Step 1: Analyze codebase

Scan the codebase for TimeGPT-1 API usage patterns using the analysis script.

Script: `{baseDir}/scripts/analyze_codebase.py`

**Usage**:
```bash
python {baseDir}/scripts/analyze_codebase.py /path/to/your/codebase
```

The script searches for:
- `timegpt.forecast()` calls
- `timegpt.create_model()` calls
- `timegpt.load_data()` calls
- `timegpt.train()` calls

**Output**: `analysis_report.txt` listing all TimeGPT-1 usage instances.

### Step 2: Run compatibility check

Execute the compatibility checker to validate data schema and identify unsupported features.

Script: `{baseDir}/scripts/compatibility_check.py`

**Usage**:
```bash
python {baseDir}/scripts/compatibility_check.py --data sample_data.csv
```

The script validates:
- Data schema (unique_id, ds, y columns)
- Data types (datetime for ds, numeric for y)
- API availability
- Unsupported TimeGPT-1 features

**Output**: `migration_report.txt` with compatibility assessment.

### Step 3: Apply migration changes

Use the migration script to update your codebase with TimeGPT-2 compatible code.

Script: `{baseDir}/scripts/apply_migration.py`

**Usage**:
```bash
python {baseDir}/scripts/apply_migration.py main.py
```

The script performs automatic replacements:
- `timegpt.forecast()` → `client.forecast()`
- `from timegpt import TimeGPT` → `from nixtla import NixtlaClient`
- `timegpt = TimeGPT()` → `client = NixtlaClient(api_key=...)`
- Removes deprecated `timegpt.create_model()` calls
- Updates data schema conversion code

**Important**: Review all changes before committing to version control.

### Step 4: Generate TimeGPT-2 configuration

Create a TimeGPT-2 configuration file with recommended settings.

Script: `{baseDir}/scripts/generate_config.py`

**Usage**:
```bash
python {baseDir}/scripts/generate_config.py
```

**Output**: `timegpt2_config.yaml` with configuration parameters.

## Output

- **analysis_report.txt**: Summary of TimeGPT-1 usage in codebase.
- **migration_report.txt**: Compatibility assessment and migration plan.
- **updated_codebase/**: Modified source code with TimeGPT-2 compatible calls (after applying changes).
- **timegpt2_config.yaml**: Configuration file for TimeGPT-2.

## Error Handling

1. **Error**: `TimeGPT-1 API endpoint not found`
   **Solution**: Ensure TimeGPT-1 API is accessible or skip API validation step.

2. **Error**: `Incompatible data schema`
   **Solution**: Update data input format to match TimeGPT-2 requirements (unique_id, ds, y columns).

3. **Error**: `Missing API Key`
   **Solution**: Set the `NIXTLA_TIMEGPT_API_KEY` environment variable.

4. **Error**: `Unsupported TimeGPT-1 feature`
   **Solution**: Refactor code to use equivalent TimeGPT-2 functionality or alternative approaches.

5. **Error**: `File not found during migration`
   **Solution**: Verify the file path and ensure the file exists before running the migration script.

## Examples

### Example 1: Basic Migration

**Before (TimeGPT-1)**:
```python
from timegpt import TimeGPT
timegpt = TimeGPT()
forecast = timegpt.forecast(data, h=24)
```

**After (TimeGPT-2)**:
```python
from nixtla import NixtlaClient
import os
client = NixtlaClient(api_key=os.getenv('NIXTLA_TIMEGPT_API_KEY'))
forecast = client.forecast(df=data, h=24, freq='H')
```

### Example 2: Configuration Update

**Before (config.json)**:
```json
{
  "model": "timegpt-1",
  "horizon": 24
}
```

**After (timegpt2_config.yaml)**:
```yaml
api_key: YOUR_API_KEY_HERE
model_name: TimeGPT-2
frequency: H
forecast_horizon: 24
data_format: Nixtla
```

### Example 3: Full Migration Workflow

```bash
# Step 1: Analyze codebase
python {baseDir}/scripts/analyze_codebase.py ./my_project

# Step 2: Check compatibility
python {baseDir}/scripts/compatibility_check.py --data ./data/sample.csv

# Step 3: Apply migration (review migration_report.txt first)
python {baseDir}/scripts/apply_migration.py ./my_project/main.py

# Step 4: Generate config
python {baseDir}/scripts/generate_config.py
```

## Resources

- TimeGPT-2 API documentation: https://docs.nixtla.io/
- Migration guide: https://docs.nixtla.io/docs/migration-guide
- NixtlaClient reference: https://nixtlaverse.nixtla.io/nixtla/
- Scripts: `{baseDir}/scripts/` directory contains all migration tools
