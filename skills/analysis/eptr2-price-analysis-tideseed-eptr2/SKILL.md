---
name: eptr2-price-analysis
description: Query and analyze Turkish electricity market prices including MCP (PTF/Piyasa Takas Fiyatı), SMP (SMF/Sistem Marjinal Fiyatı), WAP (Ağırlıklı Ortalama Fiyat), and imbalance prices. Use when asking about electricity prices, market clearing prices, day-ahead prices, system marginal prices, weighted average prices, or price comparisons in Turkey's energy market. Triggers on: PTF, SMF, GÖP fiyat, GİP fiyat, elektrik fiyatı.
allowed-tools: Read, Bash(python:*)
---

# Turkish Electricity Price Analysis with eptr2

## Overview

This skill helps you query and analyze electricity market prices from Turkey's EPIAS Transparency Platform using the eptr2 Python library.

## Quick Start

```python
from eptr2 import EPTR2

# Initialize with environment variables (recommended)
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get Market Clearing Price (MCP/PTF)
mcp = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
print(mcp)
```

## Available Price Endpoints

| Call | Alias | Description (EN) | Description (TR) |
|------|-------|------------------|------------------|
| `mcp` | `ptf` | Market Clearing Price (Day-Ahead) | Piyasa Takas Fiyatı |
| `smp` | `smf` | System Marginal Price | Sistem Marjinal Fiyatı |
| `wap` | - | Weighted Average Price (Intraday) | Ağırlıklı Ortalama Fiyat |
| `imbalance-price` | - | Positive/Negative Imbalance Prices | Dengesizlik Fiyatları |
| `interim-mcp` | - | Interim MCP (before finalization) | Kesinleşmemiş PTF |
| `mcp-smp-imb` | - | Combined MCP, SMP and Imbalance | PTF, SMF ve Dengesizlik |

## Composite Function for Comprehensive Pricing

For complete price and cost analysis including imbalance costs:

```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-29",
    end_date="2024-07-29",
    include_wap=True,       # Include IDM weighted average price
    add_kupst_cost=True     # Calculate KUPST deviation costs
)
```

### Output Columns

| Column | Description |
|--------|-------------|
| `date` | Datetime in ISO format (+03:00 timezone) |
| `mcp` | Market Clearing Price (TL/MWh) |
| `smp` | System Marginal Price (TL/MWh) |
| `wap` | Weighted Average Price (TL/MWh) |
| `system_direction` | Enerji Açığı (deficit), Enerji Fazlası (surplus), Dengede (balanced) |
| `sd_sign` | -1 (deficit/up-regulation), 1 (surplus/down-regulation), 0 (balanced) |
| `pos_imb_price` | Positive imbalance price (TL/MWh) |
| `neg_imb_price` | Negative imbalance price (TL/MWh) |
| `pos_imb_cost` | Positive imbalance cost = MCP - pos_imb_price |
| `neg_imb_cost` | Negative imbalance cost = neg_imb_price - MCP |
| `kupst_cost` | KUPST unit deviation cost |

## Common Use Cases

### 1. Daily Price Comparison (MCP vs SMP)

```python
mcp_df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")
smp_df = eptr.call("smp", start_date="2024-07-29", end_date="2024-07-29")

# Merge for comparison
import pandas as pd
comparison = mcp_df.merge(smp_df, on="date", suffixes=("_mcp", "_smp"))
```

### 2. Intraday vs Day-Ahead Price Analysis

```python
# Day-ahead price
mcp_df = eptr.call("mcp", start_date="2024-07-29", end_date="2024-07-29")

# Intraday weighted average price
wap_df = eptr.call("wap", start_date="2024-07-29", end_date="2024-07-29")

# Compare DAM vs IDM
comparison = mcp_df.merge(wap_df, on="date")
comparison["dam_idm_spread"] = comparison["price"] - comparison["wap"]
```

### 3. Imbalance Price Analysis

```python
imb_df = eptr.call("imbalance-price", start_date="2024-07-29", end_date="2024-07-29")
# Returns: positiveImbalancePrice, negativeImbalancePrice columns
```

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29")

## Authentication

Set credentials in `.env` file:
```
EPTR_USERNAME=your_email@example.com
EPTR_PASSWORD=your_password
```

Then initialize with:
```python
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)
```

## For More Details

- See [api-reference.md](api-reference.md) for complete endpoint documentation
- See [examples.md](examples.md) for additional code examples
