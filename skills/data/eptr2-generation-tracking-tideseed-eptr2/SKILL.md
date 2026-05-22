---
name: eptr2-generation-tracking
description: Query Turkish electricity generation data including real-time generation by resource type, plant-level production, UEVM (settlement generation/Uzlaştırmaya Esas Veriş Miktarı), and generation forecasts. Use when asking about power generation, renewable energy output, plant production, solar/wind generation, or UEVM data in Turkey. Triggers on: elektrik üretimi, santral üretimi, rüzgar üretimi, güneş üretimi, UEVM, generation by fuel type.
allowed-tools: Read, Bash(python:*)
---

# Turkish Electricity Generation Tracking with eptr2

## Overview

This skill helps you query electricity generation data from Turkey's EPIAS Transparency Platform using the eptr2 Python library.

## Quick Start

```python
from eptr2 import EPTR2

# Initialize with environment variables
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# Get real-time generation by resource type
rt_gen = eptr.call("rt-generation", start_date="2024-07-29", end_date="2024-07-29")
print(rt_gen)
```

## Available Generation Endpoints

| Call | Description (EN) | Description (TR) |
|------|------------------|------------------|
| `rt-generation` | Real-time generation by resource type | Kaynak Bazlı Gerçek Zamanlı Üretim |
| `rt-gen` | Real-time generation (same as above) | Gerçek Zamanlı Üretim |
| `uevm` | Settlement generation (UEVM) | Uzlaştırmaya Esas Veriş Miktarı |
| `dpp` / `kgup` | Daily Production Plan | Kesinleşmiş Günlük Üretim Planı (KGÜP) |
| `rt-gen-org` | Real-time generation by organization | Organizasyon Bazlı GZÜ |
| `uevm-pp` | UEVM by power plant | Santral Bazlı UEVM |

## Resource Types (Fuel Types)

| Turkish | English | Code |
|---------|---------|------|
| Doğalgaz | Natural Gas | naturalGas |
| Kömür | Coal | coal |
| Linyit | Lignite | lignite |
| İthal Kömür | Imported Coal | importedCoal |
| Rüzgar | Wind | wind |
| Güneş | Solar | sun |
| Hidroelektrik | Hydro | river, dammedHydro |
| Biyokütle | Biomass | biomass |
| Jeotermal | Geothermal | geothermal |
| Nükleer | Nuclear | nuclear |

## Composite Function for Generation Data

```python
from eptr2.composite import get_hourly_production_data

df = get_hourly_production_data(
    eptr,
    start_date="2024-07-29",
    end_date="2024-07-29",
    verbose=True
)
```

### Output Columns

Columns include `_rt` (real-time) and `_uevm` (settlement) suffixes:

| Column | Description |
|--------|-------------|
| `dt` | Datetime in ISO format |
| `naturalGas_rt` | Natural gas real-time generation |
| `wind_rt` | Wind real-time generation |
| `sun_rt` | Solar real-time generation |
| `total_rt` | Total real-time generation |
| `naturalGas_uevm` | Natural gas settlement generation |
| `total_uevm` | Total settlement generation |
| `contract` | Contract symbol |

## Common Use Cases

### 1. Total Generation Mix

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

# Sum by resource type
fuel_mix = rt_gen.drop(columns=['date', 'hour']).sum()
total = fuel_mix.sum()

print("Generation Mix (July 15, 2024):")
for fuel, gen in fuel_mix.items():
    pct = (gen / total) * 100
    print(f"  {fuel}: {gen:,.0f} MWh ({pct:.1f}%)")
```

### 2. Renewable Energy Share

```python
rt_gen = eptr.call("rt-generation", start_date="2024-07-15", end_date="2024-07-15")

# Define renewable columns
renewables = ['wind', 'sun', 'river', 'dammedHydro', 'geothermal', 'biomass']
renewable_cols = [c for c in rt_gen.columns if any(r in c.lower() for r in renewables)]

rt_gen['renewable'] = rt_gen[renewable_cols].sum(axis=1)
rt_gen['total'] = rt_gen.drop(columns=['date', 'hour']).sum(axis=1)
rt_gen['renewable_share'] = (rt_gen['renewable'] / rt_gen['total']) * 100

print(f"Average Renewable Share: {rt_gen['renewable_share'].mean():.1f}%")
```

### 3. Plant-Specific Generation

```python
from eptr2.composite import get_hourly_production_data

# Example: Atatürk Dam (HES)
df = get_hourly_production_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    rt_pp_id=641,    # Real-time ID for Atatürk HES
    uevm_pp_id=142   # UEVM ID for Atatürk HES
)

print(f"Atatürk Dam Daily Generation: {df['total_rt'].sum():,.0f} MWh")
```

### 4. Production Plan vs Actual

```python
from eptr2.composite import get_hourly_production_plan_data

df = get_hourly_production_plan_data(
    eptr,
    start_date="2024-07-15",
    end_date="2024-07-15",
    org_id=195,      # ELEKTRİK ÜRETİM AŞ
    uevcb_id=733     # ATATÜRK HES DB
)

# Compare KGUP (plan) with actual
```

## Understanding Generation Data Types

### Real-Time Generation (GZÜ)
- **What**: Measured generation in near real-time
- **When**: Available ~15 minutes after each hour
- **Use**: Monitoring, market tracking

### UEVM (Uzlaştırmaya Esas Veriş Miktarı)
- **What**: Official settlement generation after reconciliation
- **When**: Available after settlement period (~T+10 days)
- **Use**: Settlement, billing, final analysis

### KGÜP (Kesinleşmiş Günlük Üretim Planı)
- **What**: Finalized daily production plan
- **When**: Published day-ahead
- **Use**: Market planning, deviation analysis

## Date Format

Always use ISO format: `YYYY-MM-DD` (e.g., "2024-07-29")

## Authentication

Set credentials in `.env` file:
```
EPTR_USERNAME=your_email@example.com
EPTR_PASSWORD=your_password
```

## For More Details

- See [examples.md](examples.md) for additional code examples
