---
name: eptr2-imbalance-costs
description: Calculate and analyze Turkish electricity imbalance costs including KUPST (Kesinleşmiş Üretim Planından Sapma Tutarı/Production Plan Deviation Cost), positive/negative imbalance penalties, and DSG (Dengeden Sorumlu Grup) tolerance calculations. Use when asking about imbalance settlement, deviation costs, KUPST, energy surplus/deficit penalties, or imbalance calculations in Turkey. Triggers on: dengesizlik maliyeti, sapma tutarı, KUPST, KÜPST, enerji açığı, enerji fazlası, imbalance penalty.
allowed-tools: Read, Bash(python:*)
---

# Turkish Electricity Imbalance Cost Calculations with eptr2

## Overview

This skill helps you calculate and analyze electricity imbalance costs in Turkey's energy market using the eptr2 Python library. Imbalance costs are critical for market participants who deviate from their scheduled positions.

## Quick Start

```python
from eptr2 import EPTR2
from eptr2.composite import get_hourly_price_and_cost_data

# Initialize
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get comprehensive imbalance data
df = get_hourly_price_and_cost_data(
    eptr,
    start_date="2024-07-29",
    end_date="2024-07-29"
)

# Columns include: pos_imb_price, neg_imb_price, pos_imb_cost, neg_imb_cost, kupst_cost
print(df[['date', 'mcp', 'smp', 'pos_imb_cost', 'neg_imb_cost', 'kupst_cost']])
```

## Key Concepts

### System Direction (Sistem Yönü)

| Turkish | English | Meaning | sd_sign |
|---------|---------|---------|---------|
| Enerji Açığı | Energy Deficit | System is short, up-regulation | -1 |
| Enerji Fazlası | Energy Surplus | System is long, down-regulation | +1 |
| Dengede | Balanced | System is balanced | 0 |

### Imbalance Types

| Type | Turkish | When Applied |
|------|---------|--------------|
| Positive Imbalance | Pozitif Dengesizlik | You have surplus energy (produced more or consumed less than scheduled) |
| Negative Imbalance | Negatif Dengesizlik | You have deficit energy (produced less or consumed more than scheduled) |

## Imbalance Price Formulas

### Current Regulation (2024)

```python
# Penalty margin = 3%
penalty_margin = 0.03

# Positive imbalance price (you receive)
pos_imb_price = (1 - penalty_margin) * min(MCP, SMP)
pos_imb_price = 0.97 * min(MCP, SMP)

# Negative imbalance price (you pay)
neg_imb_price = (1 + penalty_margin) * max(MCP, SMP)
neg_imb_price = 1.03 * max(MCP, SMP)
```

### Imbalance Cost (Per MWh)

```python
# Cost of positive imbalance (revenue foregone)
pos_imb_cost = MCP - pos_imb_price

# Cost of negative imbalance (penalty paid)
neg_imb_cost = neg_imb_price - MCP
```

## KUPST (Deviation Cost from Production Plan)

KUPST applies to deviations from scheduled production plans (KGÜP).

### Formula

```python
kupst_multiplier = 0.03  # 3%
kupst_floor_price = 750  # TL/MWh

kupst_cost = max(MCP, SMP, kupst_floor_price) * kupst_multiplier
```

### Tolerance Rates by Source

| Source | Tolerance |
|--------|-----------|
| Wind | 17% |
| Solar | 10% |
| Other | 5% |

## Cost Calculation Functions

### Using eptr2 Utility Functions

```python
from eptr2.util.costs import (
    calculate_unit_imbalance_cost,
    calculate_unit_kupst_cost,
    calculate_imb_cost,
    calculate_imbalance_amounts
)

# Unit imbalance cost
mcp, smp = 2500, 2800
unit_costs = calculate_unit_imbalance_cost(mcp=mcp, smp=smp)
print(f"Positive imbalance cost: {unit_costs['pos']:.2f} TL/MWh")
print(f"Negative imbalance cost: {unit_costs['neg']:.2f} TL/MWh")

# KUPST cost
kupst = calculate_unit_kupst_cost(mcp=mcp, smp=smp)
print(f"KUPST cost: {kupst:.2f} TL/MWh")
```

### Full Imbalance Cost Calculation

```python
from eptr2.util.costs import calculate_imb_cost

result = calculate_imb_cost(
    actual=100,       # Actual generation/consumption (MWh)
    forecast=90,      # Scheduled position (MWh)
    mcp=2500,         # Market Clearing Price
    smp=2800,         # System Marginal Price
    is_producer=True, # True for generators
    imb_tol=0.1,      # 10% tolerance
    return_detail=True
)

print(f"Total Imbalance Cost: {result['costs']['total_imb_cost']:.2f} TL")
```

## Common Use Cases

### 1. Estimate Daily Imbalance Exposure

```python
from eptr2.composite import get_hourly_price_and_cost_data

df = get_hourly_price_and_cost_data(eptr, "2024-07-15", "2024-07-15")

# Example: 5 MWh surplus each hour
surplus_mwh = 5
daily_surplus_cost = (df['pos_imb_cost'] * surplus_mwh).sum()
print(f"Daily cost of 5 MWh/h surplus: {daily_surplus_cost:,.0f} TL")

# Example: 5 MWh deficit each hour
deficit_mwh = 5
daily_deficit_cost = (df['neg_imb_cost'] * deficit_mwh).sum()
print(f"Daily cost of 5 MWh/h deficit: {daily_deficit_cost:,.0f} TL")
```

### 2. Analyze System Direction Impact

```python
df = get_hourly_price_and_cost_data(eptr, "2024-07-01", "2024-07-31")

# Group by system direction
direction_analysis = df.groupby('system_direction').agg({
    'pos_imb_cost': 'mean',
    'neg_imb_cost': 'mean',
    'mcp': 'count'
}).rename(columns={'mcp': 'hours'})

print("Average Imbalance Costs by System Direction:")
print(direction_analysis)
```

## Authentication

Set credentials in `.env` file:
```
EPTR_USERNAME=your_email@example.com
EPTR_PASSWORD=your_password
```

## For More Details

- See [formulas.md](formulas.md) for detailed formula documentation
- See [examples.md](examples.md) for additional code examples
