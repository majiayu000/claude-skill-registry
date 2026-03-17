---
name: eptr2-consumption-data
description: Query Turkish electricity consumption and demand forecast data including real-time consumption, UECM (settlement consumption/Uzlaştırmaya Esas Çekiş Miktarı), and load plan forecasts. Use when asking about electricity demand, consumption patterns, load forecasting, or UECM data in Turkey. Triggers on: elektrik tüketimi, talep tahmini, yük planı, UEÇM, consumption forecast.
allowed-tools: Read, Bash(python:*)
---

# Turkish Electricity Consumption Data with eptr2

## Overview

This skill helps you query electricity consumption and demand forecast data from Turkey's EPIAS Transparency Platform using the eptr2 Python library.

## Quick Start

```python
from eptr2 import EPTR2

# Initialize with environment variables
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get real-time consumption
rt_cons = eptr.call("rt-cons", start_date="2024-07-29", end_date="2024-07-29")
print(rt_cons)
```

## Available Consumption Endpoints

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `rt-cons` | Real-time electricity consumption | Gerçek Zamanlı Tüketim |
| `uecm` | Settlement consumption (UECM) | Uzlaştırmaya Esas Çekiş Miktarı |
| `load-plan` | Demand forecast (Load Plan) | Yük Tahmini / Yük Planı |
| `rt-consumption` | Same as rt-cons | Gerçek Zamanlı Tüketim |

## Composite Function for Consumption Analysis

The composite function combines load plan, UECM, and real-time consumption:

```python
from eptr2.composite import get_hourly_consumption_and_forecast_data

df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-29",
    end_date="2024-07-29",
    verbose=True  # Print progress
)
```

### Output Columns

| Column | Description |
|--------|-------------|
| `dt` | Datetime in ISO format (+03:00 timezone) |
| `load_plan` | Demand forecast / load plan (MWh) |
| `uecm` | Settlement consumption - UECM (MWh) |
| `rt_cons` | Real-time consumption (MWh) |
| `consumption` | Best available: UECM if available, otherwise real-time |
| `contract` | Contract symbol (optional) |

## Understanding Consumption Data Types

### Load Plan (Yük Planı)
- **What**: Day-ahead demand forecast published by TEIAS
- **When**: Available before delivery day
- **Use**: Planning and forecasting

### Real-Time Consumption (Gerçek Zamanlı Tüketim)
- **What**: Actual measured consumption in near real-time
- **When**: Available ~15 minutes after each hour
- **Use**: Monitoring, real-time decisions

### UECM (Uzlaştırmaya Esas Çekiş Miktarı)
- **What**: Official settlement consumption after meter reconciliation
- **When**: Available after settlement period (~T+10 days)
- **Use**: Settlement, billing, final analysis

## Common Use Cases

### 1. Compare Forecast vs Actual

```python
from eptr2.composite import get_hourly_consumption_and_forecast_data

df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15"
)

# Calculate forecast error
df['forecast_error'] = df['consumption'] - df['load_plan']
df['forecast_error_pct'] = (df['forecast_error'] / df['load_plan']) * 100

print(f"Average Forecast Error: {df['forecast_error'].mean():.2f} MWh")
print(f"MAPE: {df['forecast_error_pct'].abs().mean():.2f}%")
```

### 2. Daily Consumption Pattern

```python
import pandas as pd

df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15"
)

df['dt'] = pd.to_datetime(df['dt'])
df['hour'] = df['dt'].dt.hour

# Peak consumption hour
peak_hour = df.loc[df['consumption'].idxmax()]
print(f"Peak Hour: {peak_hour['hour']}:00")
print(f"Peak Consumption: {peak_hour['consumption']:.2f} MWh")
```

### 3. Monthly Consumption Trends

```python
df = get_hourly_consumption_and_forecast_data(
    eptr,
    start_date="2024-07-01",
    end_date="2024-07-31"
)

total_consumption = df['consumption'].sum()
print(f"Total July Consumption: {total_consumption:,.0f} MWh")
print(f"Daily Average: {total_consumption / 31:,.0f} MWh")
```

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29")

## Data Availability Notes

| Data Type | Availability |
|-----------|--------------|
| Load Plan | Published day-ahead (D-1 by 17:00) |
| Real-Time | Available with ~15 min delay |
| UECM | Available after settlement (T+10 days typically) |

## Authentication

Set credentials in `.env` file:
```
EPTR_USERNAME=your_email@example.com
EPTR_PASSWORD=your_password
```

## For More Details

- See [examples.md](examples.md) for additional code examples
