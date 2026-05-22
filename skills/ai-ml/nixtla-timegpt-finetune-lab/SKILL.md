---
name: nixtla-timegpt-finetune-lab
description: "Configure TimeGPT fine-tuning on custom datasets with Nixtla SDK. Use when training domain-specific forecast models. Trigger with 'fine-tune TimeGPT' or 'train custom model'."
allowed-tools: "Read,Write,Glob,Grep,Edit"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla TimeGPT Fine-Tuning Lab

Guide users through production-ready TimeGPT fine-tuning workflows.

## Overview

This skill manages TimeGPT fine-tuning:

- **Dataset preparation**: Validate and format training data
- **Job submission**: Submit fine-tuning jobs to TimeGPT API
- **Status monitoring**: Track job progress until completion
- **Model comparison**: Compare zero-shot vs fine-tuned performance

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla` package
- `NIXTLA_API_KEY` environment variable

**Installation**:
```bash
pip install nixtla pandas utilsforecast
export NIXTLA_API_KEY='your-api-key'
```

**Get API Key**: https://dashboard.nixtla.io

## Instructions

### Step 1: Prepare Dataset

Ensure data is in Nixtla schema:
```bash
python {baseDir}/scripts/prepare_finetune_data.py \
    --input data/sales.csv \
    --output data/finetune_train.csv
```

### Step 2: Configure Fine-Tuning

```bash
python {baseDir}/scripts/configure_finetune.py \
    --train data/finetune_train.csv \
    --model_name "sales-model-v1" \
    --horizon 14 \
    --freq D
```

### Step 3: Submit Job

```bash
python {baseDir}/scripts/submit_finetune.py \
    --config forecasting/finetune_config.yml
```

### Step 4: Monitor Progress

```bash
python {baseDir}/scripts/monitor_finetune.py \
    --job_id <job_id>
```

### Step 5: Compare Models

```bash
python {baseDir}/scripts/compare_finetuned.py \
    --test data/test.csv \
    --finetune_id <model_id>
```

## Output

- **forecasting/finetune_config.yml**: Fine-tuning configuration
- **forecasting/artifacts/finetune_model_id.txt**: Saved model ID
- **forecasting/results/comparison_metrics.csv**: Performance comparison

## Error Handling

1. **Error**: `NIXTLA_API_KEY not set`
   **Solution**: Export your API key: `export NIXTLA_API_KEY='...'`

2. **Error**: `Insufficient training data`
   **Solution**: Need 100+ observations per series

3. **Error**: `Fine-tuning job failed`
   **Solution**: Check data format, ensure no NaN values

4. **Error**: `Model ID not found`
   **Solution**: Verify job completed, check artifacts directory

## Examples

### Example 1: Basic Fine-Tuning

```bash
# Prepare data
python {baseDir}/scripts/prepare_finetune_data.py \
    --input sales.csv --output train.csv

# Submit job
python {baseDir}/scripts/submit_finetune.py \
    --train train.csv \
    --model_name "my-sales-model" \
    --horizon 14
```

**Output**:
```
Fine-tuning job submitted: job_abc123
Model ID saved to: artifacts/finetune_model_id.txt
```

### Example 2: Compare Zero-Shot vs Fine-Tuned

```bash
python {baseDir}/scripts/compare_finetuned.py \
    --test test.csv \
    --finetune_id my-sales-model
```

**Output**:
```
Model Comparison:
  TimeGPT Zero-Shot: SMAPE=12.3%
  TimeGPT Fine-Tuned: SMAPE=8.7%
  Improvement: 29.3%
```

## Resources

- Scripts: `{baseDir}/scripts/`
- TimeGPT Docs: https://docs.nixtla.io/
- Fine-Tuning Guide: https://docs.nixtla.io/docs/finetuning

**Related Skills**:
- `nixtla-schema-mapper`: Prepare data before fine-tuning
- `nixtla-experiment-architect`: Create baseline experiments
- `nixtla-usage-optimizer`: Evaluate cost-effectiveness
