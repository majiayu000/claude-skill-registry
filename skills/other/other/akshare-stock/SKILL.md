---
name: "akshare-stock"
description: "A-share stock market data via AkShare/Tencent. Real-time quotes, historical data, sector analysis, capital flow, and more."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-packages
        kind: pip
        packages: ["akshare", "pandas", "requests"]
---

# akshare-stock

Comprehensive A-share stock data skill powered by AkShare and Tencent Finance.

## Setup

Install dependencies:
```bash
pip install akshare pandas requests
```

## Features

### Core Features
- Real-time stock quotes
- Stock search by name/code
- Historical price data
- Stock list with filters

### Advanced Features
- Sector/Industry analysis
- Capital flow (资金流向)
- Dragon Tiger List (龙虎榜)
- Fund data (ETF/LOF)

## Commands

### Real-time Quote
```bash
python scripts/stock_quote_tx.py <stock_code>
```

### Stock Search
```bash
python scripts/stock_search_tx.py <keyword>
```

### Stock List
```bash
python scripts/stock_list.py
python scripts/stock_list.py --market sh --limit 30
python scripts/stock_list.py --type etf
```

### Sector/Industry Analysis
```bash
python scripts/stock_sector.py              # List all sectors
python scripts/stock_sector.py 半导体        # Get sector stocks
python scripts/stock_sector.py 银行
```

### Capital Flow
```bash
python scripts/stock_capital.py
python scripts/stock_capital.py --market sh --limit 30
```

### Dragon Tiger List
```bash
python scripts/stock_lhb.py                 # Today's data
python scripts/stock_lhb.py 20250311        # Specific date
```

## Stock Code Format

- Shanghai: `600000` (6xxxxx)
- Shenzhen: `000001` (0xxxxx)
- ChiNext: `300001` (3xxxxx)
- STAR Market: `688001` (688xxx)
- Beijing: `8xxxxx`, `4xxxxx`

## Examples

```bash
# Real-time quotes
python scripts/stock_quote_tx.py 600519
python scripts/stock_quote_tx.py 000001

# Search
python scripts/stock_search_tx.py 茅台
python scripts/stock_search_tx.py 银行

# Stock list
python scripts/stock_list.py --market sz --limit 20

# Sector analysis
python scripts/stock_sector.py 半导体
python scripts/stock_sector.py 新能源

# Capital flow
python scripts/stock_capital.py --limit 20

# Dragon Tiger List
python scripts/stock_lhb.py
```

## File Structure

```
akshare-stock/
├── SKILL.md
└── scripts/
    ├── stock_quote_tx.py      # Real-time quote (Tencent)
    ├── stock_search_tx.py     # Stock search (Tencent)
    ├── stock_list.py          # Stock list with filters
    ├── stock_sector.py        # Sector/Industry analysis
    ├── stock_capital.py       # Capital flow
    ├── stock_lhb.py           # Dragon Tiger List
    ├── stock_quote.py         # Real-time quote (AkShare)
    ├── stock_hist.py          # Historical data (AkShare)
    └── stock_search.py        # Stock search (AkShare)
```

## Data Sources

- **Tencent Finance**: Real-time quotes, stock search (stable, fast)
- **AkShare**: Sector data, capital flow, Dragon Tiger List (East Money)

## Popular Sectors

半导体, 银行, 白酒, 新能源, 医药, 房地产, 汽车, 人工智能, 芯片, 5G

## Notes

- Tencent APIs work without registration
- AkShare may be blocked in some network environments
- Dragon Tiger data available for trading days only
- Data is for reference only, not investment advice
