---
name: "tushare-pro"
description: "Professional financial data via Tushare Pro. High-quality stock fundamentals, financial statements, and quantitative data."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-packages
        kind: pip
        packages: ["tushare", "pandas"]
---

# tushare-pro

Professional financial data skill powered by [Tushare Pro](https://tushare.pro).

## Setup

### 1. Install Dependencies

```bash
pip install tushare pandas
```

### 2. Get Tushare Token

1. Register at [Tushare Pro](https://tushare.pro)
2. Get your API token from user center
3. Set environment variable or pass to scripts

```bash
export TUSHARE_TOKEN="your-token-here"
```

## Features

- **Stock Basics** - Basic info, IPO date, industry classification
- **Financial Data** - Balance sheet, income statement, cash flow
- **Market Data** - Daily prices, real-time quotes
- **Shareholder Data** - Top holders, institutional holdings
- **Quantitative Data** - Technical factors, market indicators

## Commands

### Stock Basic Info
```bash
python scripts/ts_stock_basic.py [ts_code]
```

### Financial Statements
```bash
# Balance Sheet
python scripts/ts_balance_sheet.py <ts_code> [year]

# Income Statement
python scripts/ts_income.py <ts_code> [year]

# Cash Flow
python scripts/ts_cashflow.py <ts_code> [year]
```

### Daily Market Data
```bash
python scripts/ts_daily.py <ts_code> [start_date] [end_date]
```

### Shareholder Data
```bash
python scripts/ts_holders.py <ts_code>
```

## Stock Code Format

Tushare uses `XXXXXX.XX` format:
- A-Shares: `000001.SZ` (Shenzhen), `600519.SH` (Shanghai)
- Index: `000001.SH` (上证指数), `399001.SZ` (深证成指)
- ETFs: `510300.SH` (沪深300ETF)

## Examples

```bash
# Set token
export TUSHARE_TOKEN="your-token"

# Stock basic info
python scripts/ts_stock_basic.py 000001.SZ

# Financial data
python scripts/ts_balance_sheet.py 600519.SH 2023

# Daily prices
python scripts/ts_daily.py 000001.SZ 20240101 20240312

# Top shareholders
python scripts/ts_holders.py 600519.SH
```

## File Structure

```
tushare-pro/
├── SKILL.md
└── scripts/
    ├── ts_stock_basic.py      # Stock basic information
    ├── ts_balance_sheet.py    # Balance sheet data
    ├── ts_income.py           # Income statement
    ├── ts_cashflow.py         # Cash flow statement
    ├── ts_daily.py            # Daily market data
    └── ts_holders.py          # Shareholder data
```

## Data Sources

- **Tushare Pro** - Professional financial data platform

## Usage Limits

| Version | Daily Calls | Features |
|:---|:---:|:---|
| Free | 200 | Basic data, limited history |
| Pro | 5000+ | Full data, longer history |

> Get more points by registering and completing tasks on Tushare website

## Notes

- Requires Tushare account and token
- Free version has daily call limits
- Pro version requires points for advanced data
- Data quality is high, suitable for quantitative analysis
- Financial data is updated quarterly

## Links

- [Tushare Pro](https://tushare.pro)
- [Tushare Documentation](https://tushare.pro/document/2)
