---
name: gridstatus-api
description: This skill should be used when the user asks to "get electricity data", "query grid data", "get LMP prices", "fetch load data", "get fuel mix", "query ERCOT data", "query CAISO data", "query PJM data", "get electricity prices", "analyze grid operations", "get ISO data", or mentions electricity market data (load, generation, pricing, LMP, fuel mix, ancillary services, etc.).
version: 1.3.0
---

# GridStatus API Skill

Query electricity grid data from US Independent System Operators (ISOs) using the GridStatus.io API. Access real-time and historical data for load, pricing (LMP), generation, fuel mix, and more.

## Quick Start

**IMPORTANT: Always use the Python SDK.** The direct curl API has issues with date filtering on the free tier and returns stale sample data. The Python SDK correctly handles all parameters.

### Setup

1. **Install SDK** (use uv for isolation):
```bash
cd /tmp && uv venv -q && source .venv/bin/activate && uv pip install gridstatusio pandas -q
```

2. **API Key**: Check for `GRIDSTATUS_API_KEY` in the user's `.env` file. If not present, instruct the user to:
   - Create account at https://www.gridstatus.io
   - Get API key from Settings page
   - Add to `.env`: `GRIDSTATUS_API_KEY=your_key_here`

3. **Query data**:
```python
import os
os.environ['GRIDSTATUS_API_KEY'] = 'key_from_dotenv'

from gridstatusio import GridStatusClient
client = GridStatusClient()

df = client.get_dataset(
    dataset="isone_fuel_mix",
    start="2026-01-25",
    end="2026-01-26",
    limit=100
)
print(df.tail())
```

**Free tier limit**: 500,000 rows per month. Always use `limit` parameter.

## Supported ISOs

| ISO | Region | Key Datasets |
|-----|--------|--------------|
| ERCOT | Texas | `ercot_load`, `ercot_spp_*`, `ercot_fuel_mix` |
| CAISO | California | `caiso_load`, `caiso_lmp_*`, `caiso_fuel_mix` |
| PJM | Mid-Atlantic/Midwest | `pjm_load`, `pjm_lmp_*`, `pjm_standardized_*` |
| MISO | Midwest | `miso_load`, `miso_lmp_*` |
| NYISO | New York | `nyiso_load`, `nyiso_lmp_*` |
| ISO-NE | New England | `isone_load`, `isone_lmp_*`, `isone_fuel_mix` |
| SPP | Southwest/Central | `spp_load`, `spp_lmp_*` |

See `references/datasets-by-iso.md` for complete dataset catalog.

## Standard Query Template

Use this template for all queries. Run in a Python heredoc:

```bash
cd /tmp && source .venv/bin/activate && python3 << 'EOF'
import os
os.environ['GRIDSTATUS_API_KEY'] = 'YOUR_KEY_HERE'

from gridstatusio import GridStatusClient
client = GridStatusClient()

df = client.get_dataset(
    dataset="DATASET_NAME",
    start="YYYY-MM-DD",
    end="YYYY-MM-DD",
    limit=100
)
print(df.to_string())
EOF
```

## Common Query Patterns

### Current Fuel Mix (What's generating now?)
```python
df = client.get_dataset(
    dataset="isone_fuel_mix",  # or ercot_fuel_mix, caiso_fuel_mix
    start="2026-01-25",
    end="2026-01-26",
    limit=500
)
latest = df.iloc[-1]
total = latest[['coal','hydro','natural_gas','nuclear','oil','solar','wind','wood','refuse','other']].sum()
print(f"Oil: {latest['oil']:.0f} MW ({latest['oil']/total*100:.1f}%)")
```

### System Load
```python
df = client.get_dataset(
    dataset="pjm_load",
    start="2026-01-25",
    end="2026-01-26",
    timezone="US/Eastern",
    limit=100
)
print(f"Current load: {df.iloc[-1]['load']:,.0f} MW")
```

### Electricity Prices (LMP)
```python
df = client.get_dataset(
    dataset="ercot_spp_real_time_15_min",
    start="2026-01-25",
    end="2026-01-26",
    filter_column="location",
    filter_value="HB_HOUSTON",
    limit=100
)
print(f"Houston price: ${df.iloc[-1]['spp']:.2f}/MWh")
```

### Zone-Specific Load (Standardized Datasets)
```python
df = client.get_dataset(
    dataset="pjm_standardized_hourly",
    start="2026-01-25",
    end="2026-01-26",
    timezone="market"
)
# Zone data in columns: df['load.comed'], df['load.aep'], etc.
print(f"ComEd load: {df.iloc[-1]['load.comed']:,.0f} MW")
```

## Dataset Discovery

### Check Dataset Metadata (date range, columns)
```python
# Get dataset info including available date range
import requests
import os

api_key = os.environ.get('GRIDSTATUS_API_KEY')
r = requests.get(f"https://api.gridstatus.io/v1/datasets/pjm_load",
                 headers={"x-api-key": api_key})
meta = r.json()
print(f"Available: {meta['earliest_available_time_utc']} to {meta['latest_available_time_utc']}")
print(f"Columns: {[c['name'] for c in meta['all_columns']]}")
```

### List Datasets
```python
client.list_datasets(filter_term="ercot")  # Search by keyword
datasets = client.list_datasets(filter_term="fuel_mix", return_list=True)
```

**Dataset naming convention**: `{iso}_{data_type}_{frequency}`
- `ercot_load` - ERCOT system load
- `caiso_lmp_real_time_5_min` - CAISO 5-minute real-time LMPs
- `pjm_lmp_day_ahead_hourly` - PJM day-ahead hourly LMPs

## Energy Calculations

Load (MW) measures instantaneous power. Energy (MWh) = power x time.

| Data Frequency | Energy Formula | Example |
|----------------|----------------|---------|
| 5-minute | `energy_MWh = load_MW * (5/60)` | 100,000 MW x 0.0833 = 8,333 MWh |
| 15-minute | `energy_MWh = load_MW * (15/60)` | 100,000 MW x 0.25 = 25,000 MWh |
| Hourly | `energy_MWh = load_MW * 1` | 100,000 MW x 1 = 100,000 MWh |

```python
# Total energy for a period (5-min data)
total_mwh = (df['load'] * (5/60)).sum()
total_gwh = total_mwh / 1000
```

## Query Parameters Reference

| Parameter | Type | Description |
|-----------|------|-------------|
| `dataset` | str | **Required**. Dataset ID (e.g., `ercot_load`) |
| `start` | str | Start date (YYYY-MM-DD or ISO format) |
| `end` | str | End date |
| `limit` | int | Max rows to return |
| `timezone` | str | `"market"` for ISO local time, or `"US/Central"` etc. |
| `filter_column` | str | Column to filter on |
| `filter_value` | str/list | Value(s) to match |
| `filter_operator` | str | `=`, `!=`, `>`, `<`, `>=`, `<=`, `in` |
| `resample` | str | Aggregate frequency (`"1 hour"`, `"1 day"`) |
| `resample_function` | str | `mean`, `sum`, `min`, `max` |

See `references/api-reference.md` for complete documentation.

## Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Old/stale data returned | Using curl directly | **Use Python SDK instead** - curl has date filtering issues on free tier |
| 401 Unauthorized | Invalid/missing API key | Check `GRIDSTATUS_API_KEY` is set correctly |
| Empty DataFrame | Date range outside coverage | Check dataset metadata for available date range |
| ModuleNotFoundError | SDK not installed | Run: `cd /tmp && uv venv -q && source .venv/bin/activate && uv pip install gridstatusio pandas -q` |
| "Unknown column" error | Wrong filter column | Zone data is in columns after fetch, not filterable. Use `df['load.comed']` |
| 429 Rate Limited | Too many requests | SDK auto-retries with backoff |

### Why Not curl?

The direct HTTP API has a critical issue on the free tier: **date parameters are ignored** and it returns sample data from years ago. The Python SDK correctly handles date filtering and returns current data.

If you must use curl (e.g., for dataset metadata), it works for non-query endpoints:
```bash
# This works - metadata endpoint
curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/pjm_load"

# This returns stale data - query endpoint has issues
curl -s -H "x-api-key: $GRIDSTATUS_API_KEY" \
  "https://api.gridstatus.io/v1/datasets/pjm_load/query?start=2026-01-25"  # BROKEN
```

## Additional Resources

### Reference Files
- **`references/datasets-by-iso.md`** - Complete dataset catalog by ISO
- **`references/api-reference.md`** - Full API parameter documentation
- **`references/common-queries.md`** - Ready-to-use query patterns

### Example Files
- **`examples/python-query.py`** - Python SDK examples
