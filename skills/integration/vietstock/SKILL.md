---
name: fireant-stock
description: Automated Vietnamese stock price checking on FireAnt.vn. Use when checking current stock prices, market data, trading volumes, or financial information for Vietnamese stocks (HOSE, HNX, UPCOM). Accepts stock symbols like DPM, VCB, FPT, etc. and returns formatted price data, market statistics, and key financial metrics.
---

# FireAnt Stock Price Checker

## Overview

Automatically retrieves real-time stock information from FireAnt.vn for Vietnamese equities. Handles the full workflow from searching to data extraction and formatting.

## Quick Start

Check a single stock:
```bash
scripts/check_stock.py DPM
```

Check multiple stocks:
```bash
scripts/check_stock.py VCB FPT BID
```

## Core Workflow

1. **Search** - Uses Google search to find the FireAnt stock page for the symbol
2. **Navigate** - Opens the FireAnt stock page via browser automation  
3. **Extract** - Parses current price, volume, market cap, and key statistics
4. **Format** - Returns structured data in readable format

## Supported Data

- **Current Price** - Real-time price with change percentage
- **Trading Data** - Volume, value, opening/high/low prices  
- **Market Metrics** - Market cap, beta, P/E ratio, reference price
- **Technical Analysis** - Moving averages (MA10, MA50)
- **Company Info** - Full company name, stock exchange listing

## Usage Patterns

**Single stock inquiry:**
"Check giá cổ phiếu DPM"
"What's the current price of VCB?"

**Multiple stocks:**
"Compare VCB, BID, and CTG prices"
"Show me bank stocks: VCB BID CTG"

**Market research:**
"Find information about DPM stock on FireAnt"
"Get latest trading data for FPT"

## Scripts

### scripts/check_stock.py

Main script that automates the full stock checking workflow for one or more symbols.

**Usage:** `python3 scripts/check_stock.py <SYMBOL1> [SYMBOL2] ...`

**Returns:** Formatted stock data including price, volume, market cap, and key metrics.
