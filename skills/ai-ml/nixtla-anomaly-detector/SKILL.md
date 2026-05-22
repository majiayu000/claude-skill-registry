---
name: nixtla-anomaly-detector
description: Detects anomalies in time series data using TimeGPT. Identifies outliers, level shifts, and trend breaks without model training. Use when identifying anomalies, outliers, or unusual patterns in time series. Trigger with "detect anomalies", "find outliers", "anomaly detection".
allowed-tools: "Read,Write,Bash(python:*),Glob,Grep"
version: "1.0.0"
author: "Jeremy Longshore <jeremy@intentsolutions.io>"
license: MIT
---

# Nixtla Anomaly Detector

Automatically detect and flag anomalies in time series data using TimeGPT.

## Overview

This skill leverages TimeGPT's anomaly detection capabilities to identify outliers, level shifts, and trend breaks in time series data without requiring model training. It accepts CSV data, runs anomaly detection via the Nixtla API, and produces a detailed report with visualizations.

## Prerequisites

**Required**:
- Python 3.8+
- `nixtla`, `pandas`, `matplotlib` packages

**Environment Variables**:
- `NIXTLA_TIMEGPT_API_KEY`: Your TimeGPT API key

**Installation**:
```bash
pip install nixtla pandas matplotlib
```

## Instructions

### Step 1: Prepare Input Data

Ensure your CSV file has the required Nixtla schema columns:

| Column | Type | Description |
|--------|------|-------------|
| `unique_id` | string | Series identifier |
| `ds` | datetime | Timestamp |
| `y` | numeric | Value to analyze |

### Step 2: Set API Key

```bash
export NIXTLA_TIMEGPT_API_KEY=your_api_key_here
```

### Step 3: Run Anomaly Detection

Execute the detection script:

```bash
python {baseDir}/scripts/detect_anomalies.py --input your_data.csv
```

**Available options**:
- `--input`, `-i`: Input CSV file (required)
- `--output-csv`, `-o`: Anomaly output CSV (default: `anomalies.csv`)
- `--output-plot`, `-p`: Visualization plot (default: `anomalies_plot.png`)
- `--output-summary`, `-s`: Summary text file (default: `anomaly_summary.txt`)

### Step 4: Review Results

The script generates three output files:
1. **anomalies.csv** - Detailed anomaly records
2. **anomalies_plot.png** - Visual highlighting of anomalies
3. **anomaly_summary.txt** - Summary counts by type

## Output

- **anomalies.csv**: Contains detected anomalies with timestamps, values, and anomaly types (outlier, level_shift, trend_break)
- **anomalies_plot.png**: Time series visualization with anomalies highlighted in red
- **anomaly_summary.txt**: Human-readable summary of detection results

## Error Handling

1. **Error**: `NIXTLA_TIMEGPT_API_KEY not set`
   **Solution**: Run `export NIXTLA_TIMEGPT_API_KEY=your_key`

2. **Error**: `CSV file missing required columns`
   **Solution**: Ensure CSV has `unique_id`, `ds`, and `y` columns

3. **Error**: `No anomalies detected`
   **Solution**: This is valid output - data may have no anomalies

4. **Error**: `Connection error to TimeGPT API`
   **Solution**: Check network connection and API key validity

## Examples

### Example 1: Detect outliers in website traffic

**Input** (`traffic.csv`):
```csv
unique_id,ds,y
website_1,2024-01-01,1000
website_1,2024-01-02,1050
website_1,2024-01-03,300
website_1,2024-01-04,980
```

**Command**:
```bash
python {baseDir}/scripts/detect_anomalies.py --input traffic.csv
```

**Output** (anomalies.csv):
```csv
unique_id,ds,y,anomaly_type
website_1,2024-01-03,300,outlier
```

### Example 2: Identify trend break in sales data

**Input** (`sales.csv`):
```csv
unique_id,ds,y
store_1,2023-12-28,50
store_1,2023-12-29,55
store_1,2023-12-30,60
store_1,2023-12-31,150
store_1,2024-01-01,145
```

**Command**:
```bash
python {baseDir}/scripts/detect_anomalies.py -i sales.csv -o sales_anomalies.csv
```

**Output**: Detects trend break at 2023-12-31

## Resources

- Script: `{baseDir}/scripts/detect_anomalies.py`
- Nixtla Docs: https://nixtla.github.io/
- TimeGPT API: https://docs.nixtla.io/
