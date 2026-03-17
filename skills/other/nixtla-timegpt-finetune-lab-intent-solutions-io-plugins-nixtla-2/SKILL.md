---
name: nixtla-timegpt-finetune-lab
description: |
  Fine-tunes TimeGPT on custom datasets to improve forecasting accuracy.
  Use when TimeGPT's zero-shot performance is insufficient or domain-specific accuracy is needed.
  Trigger with "finetune TimeGPT", "train TimeGPT", "adapt TimeGPT".
allowed-tools: "Read,Write,Bash,Glob,Grep"
version: "1.0.0"
---

# Nixtla TimeGPT Fine-Tuning Lab

Adapts the TimeGPT model to specific datasets for enhanced forecasting performance.

## Purpose

Improves forecasting accuracy by fine-tuning the pre-trained TimeGPT model on custom time series data.

## Overview

This skill guides users through the process of fine-tuning TimeGPT on their own datasets. It handles data preprocessing, training configuration, and evaluation. Use when domain-specific accuracy is crucial or when the general TimeGPT model underperforms. It outputs a fine-tuned model and performance metrics.

## Prerequisites

**Tools**: Read, Write, Bash, Glob, Grep

**Environment**: `NIXTLA_TIMEGPT_API_KEY`

**Packages**:
```bash
pip install nixtla pandas scikit-learn matplotlib
```

## Instructions

### Step 1: Prepare data

Load and preprocess time series data into Nixtla format (unique_id, ds, y).

```bash
python {baseDir}/scripts/prepare_data.py \
  --input data.csv \
  --train_output train_data.csv \
  --val_output val_data.csv
```

**Requirements**:
- CSV file with columns: unique_id, ds, y
- ds column in recognizable datetime format
- y column with numeric values
- No missing values (will be dropped automatically)

**Output**:
- train_data.csv (80% split)
- val_data.csv (20% split)
- time_series_visualization.png (first 3 series)

### Step 2: Configure training

Create or validate training configuration.

```bash
# Create default config
python {baseDir}/scripts/configure_training.py \
  --create_default \
  --output config.json

# Or validate existing config
python {baseDir}/scripts/configure_training.py \
  --config config.json
```

**Configuration parameters**:
- learning_rate: 0.001 (default)
- epochs: 10 (default)
- batch_size: 32 (default)
- num_workers: 4 (default)
- model_name: TimeGPT
- freq: D (daily), H (hourly), etc.

### Step 3: Execute fine-tuning

Run the fine-tuning process using prepared data and configuration.

```bash
export NIXTLA_TIMEGPT_API_KEY=your_api_key

python {baseDir}/scripts/finetune_model.py \
  --train_data train_data.csv \
  --config config.json \
  --output finetuned_model.pkl
```

**Output**: finetuned_model.pkl (serialized fine-tuned model)

### Step 4: Evaluate and save

Evaluate the fine-tuned model on validation data and save metrics.

```bash
python {baseDir}/scripts/evaluate_model.py \
  --val_data val_data.csv \
  --model finetuned_model.pkl \
  --config config.json \
  --output metrics.json
```

**Output**: metrics.json (MAE, RMSE metrics)

## Output

- **train_data.csv**: Training dataset (80% split)
- **val_data.csv**: Validation dataset (20% split)
- **time_series_visualization.png**: Visualization of training data
- **config.json**: Training configuration
- **finetuned_model.pkl**: Fine-tuned TimeGPT model
- **metrics.json**: Evaluation metrics (MAE, RMSE)

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: `export NIXTLA_TIMEGPT_API_KEY=your_api_key`

2. **Error**: `Invalid data format`
   **Solution**: Ensure data has columns: unique_id, ds, y

3. **Error**: `Insufficient training data`
   **Solution**: Provide a larger training dataset (at least 50 time series points per series)

4. **Error**: `Fine-tuning failed`
   **Solution**: Adjust the fine-tuning parameters (learning rate, epochs) in config.json

5. **Error**: `Missing required column`
   **Solution**: Verify CSV has unique_id, ds, y columns with correct data types

## Examples

### Example 1: Fine-tuning on Retail Sales Data

**Input**:
```csv
unique_id,ds,y
store_1,2023-01-01,100
store_1,2023-01-02,110
```

**Command**:
```bash
python {baseDir}/scripts/finetune_model.py \
  --train_data train_data.csv \
  --config config.json \
  --output finetuned_model.pkl
```

**Output**: finetuned_model.pkl (a serialized, fine-tuned TimeGPT model)

### Example 2: Fine-tuning on Energy Consumption Data

**Input**:
```csv
unique_id,ds,y
building_1,2023-01-01 00:00,50
building_1,2023-01-01 01:00,55
```

**Command**:
```bash
python {baseDir}/scripts/evaluate_model.py \
  --val_data val_data.csv \
  --model finetuned_model.pkl \
  --config config.json \
  --output metrics.json
```

**Output**: metrics.json (performance metrics of the fine-tuned model)

## Resources

- Data preparation: `{baseDir}/scripts/prepare_data.py`
- Training configuration: `{baseDir}/scripts/configure_training.py`
- Fine-tuning execution: `{baseDir}/scripts/finetune_model.py`
- Model evaluation: `{baseDir}/scripts/evaluate_model.py`
