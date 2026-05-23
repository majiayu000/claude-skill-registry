---
name: eptr2-api-discovery
description: Discover and explore available eptr2 API endpoints for Turkish electricity market data. List all 213+ API calls, find endpoints by category (GÖP, GİP, DGP, Üretim, Tüketim), search for specific data types, and get parameter requirements. Use when asking what data is available, how to find endpoints, or exploring the API. Triggers on: available endpoints, API calls, list endpoints, what data, which API, how to find, hangi veri, mevcut servisler.
allowed-tools: Read, Bash(python:*)
---

# eptr2 API Discovery Guide

## Overview

This skill helps you discover and explore the 213+ API endpoints available in eptr2 for Turkish electricity market data. Use this when you need to find the right endpoint for your data needs.

## Quick Start

```python
from eptr2 import EPTR2

# Initialize
eptr = EPTR2(use_dotenv=True, recycle_tgt=True)

# List all available API calls
all_calls = eptr.get_available_calls()
print(f"Total available calls: {len(all_calls)}")
print(all_calls[:20])  # First 20 calls
```

## Discovery Methods

### 1. Get All Available Calls

```python
# List all endpoint names
calls = eptr.get_available_calls()
print(calls)
```

### 2. Get Number of Calls

```python
# Get count of available endpoints
count = eptr.get_number_of_calls()
print(f"Available endpoints: {count}")
```

### 3. Get Aliases

```python
# Some endpoints have shorthand aliases
aliases = eptr.get_aliases()
print(aliases)
# Example: 'ptf' is alias for 'mcp', 'smf' is alias for 'smp'
```

### 4. Get Help for Specific Call

```python
from eptr2.mapping.help import get_help_d

# Get detailed info about an endpoint
help_info = get_help_d("mcp")
print(f"Category: {help_info['category']}")
print(f"Title (EN): {help_info['title']['en']}")
print(f"Title (TR): {help_info['title']['tr']}")
print(f"Description: {help_info['desc']['en']}")
print(f"URL: {help_info['url']}")
```

## API Categories

| Category | Turkish | Description | Example Calls |
|----------|---------|-------------|---------------|
| GÖP | Gün Öncesi Piyasası | Day-Ahead Market | `mcp`, `dam-clearing`, `dam-volume` |
| GİP | Gün İçi Piyasası | Intraday Market | `wap`, `idm-qty`, `idm-log` |
| DGP | Dengeleme Güç Piyasası | Balancing Power Market | `smp`, `bpm-up`, `bpm-down` |
| Üretim | Üretim | Generation | `rt-generation`, `uevm`, `dpp` |
| Tüketim | Tüketim | Consumption | `rt-cons`, `uecm`, `load-plan` |
| Dengesizlik | Dengesizlik | Imbalance | `imbalance-price`, `imb-qty`, `imb-vol` |
| İA | İkili Anlaşmalar | Bilateral Contracts | `bi-long`, `bi-short` |
| Barajlar | Barajlar | Dams/Reservoirs | `dams-daily-level`, `dams-active-fullness` |
| Kurulu Güç | Kurulu Güç | Installed Capacity | `installed-capacity`, `lic-pp-list` |

## Common Endpoint Patterns

### Price Data
- `mcp` / `ptf` - Market Clearing Price
- `smp` / `smf` - System Marginal Price
- `wap` - Weighted Average Price (IDM)
- `imbalance-price` - Imbalance prices

### Quantity Data
- `rt-generation` - Real-time generation
- `rt-cons` - Real-time consumption
- `dam-clearing` - DAM cleared quantity
- `idm-qty` - IDM matched quantity

### Plan Data
- `load-plan` - Demand forecast
- `dpp` / `kgup` - Daily production plan
- `kudup` - Settlement production plan

### Settlement Data
- `uevm` - Settlement generation
- `uecm` - Settlement consumption

## Finding the Right Endpoint

### Search by Keyword

```python
from eptr2.mapping.help import get_help_d

# Get all help entries
all_help = get_help_d()

# Search for keywords
keyword = "price"  # or "fiyat" for Turkish
matches = {
    k: v for k, v in all_help.items()
    if keyword.lower() in v['title']['en'].lower()
    or keyword.lower() in v['desc']['en'].lower()
}

for call, info in matches.items():
    print(f"{call}: {info['title']['en']}")
```

### List by Category

```python
all_help = get_help_d()

# Filter by category
category = "GÖP"  # Day-Ahead Market
gop_calls = {
    k: v for k, v in all_help.items()
    if v['category'] == category
}

print(f"GÖP (Day-Ahead Market) endpoints:")
for call, info in gop_calls.items():
    print(f"  {call}: {info['title']['en']}")
```

## Parameter Requirements

### Get Required Parameters

```python
from eptr2.mapping.parameters import get_required_parameters, get_optional_parameters

# Check what parameters an endpoint needs
required = get_required_parameters("mcp")
optional = get_optional_parameters("mcp")

print(f"Required: {required}")
print(f"Optional: {optional}")
```

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `start_date` | str | Start date (YYYY-MM-DD) |
| `end_date` | str | End date (YYYY-MM-DD) |
| `org_id` | int/str | Organization ID |
| `pp_id` | int/str | Power plant ID |
| `uevcb_id` | int/str | Production unit ID |

## Quick Reference Tables

### Most Used Price Endpoints
| Call | Description |
|------|-------------|
| `mcp` | Market Clearing Price |
| `smp` | System Marginal Price |
| `wap` | IDM Weighted Average Price |
| `imbalance-price` | Imbalance prices |
| `mcp-smp-imb` | Combined MCP, SMP, Imbalance |

### Most Used Quantity Endpoints
| Call | Description |
|------|-------------|
| `rt-generation` | Real-time generation by type |
| `rt-cons` | Real-time consumption |
| `load-plan` | Demand forecast |
| `dam-clearing` | DAM cleared volume |
| `idm-qty` | IDM matched volume |

### Production Plan Endpoints
| Call | Description |
|------|-------------|
| `dpp` / `kgup` | Daily Production Plan (KGÜP) |
| `kgup-v1` | KGUP Version 1 |
| `kudup` | Settlement Production Plan |
| `uevm` | Settlement Generation (UEVM) |

## For More Details

- See [endpoint-categories.md](endpoint-categories.md) for complete category listings
- Run the helper script in `scripts/list_endpoints.py` for interactive discovery
