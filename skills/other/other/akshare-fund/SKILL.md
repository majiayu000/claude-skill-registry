---
name: "akshare-fund"
description: "Fund data via AkShare/Tencent. Get fund quotes, NAV, rankings, and fund search."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-packages
        kind: pip
        packages: ["requests"]
---

# akshare-fund

Fund data skill powered by AkShare (primary) and Tencent Finance (fallback).

## Setup

Install dependencies:
```bash
pip install requests
```

## Features

- Real-time fund quotes (ETF/LOF)
- Fund NAV (Net Asset Value)
- Fund search by name/code
- Fund ranking (coming soon)

## Commands

### Get fund real-time quote
```bash
python scripts/fund_quote_tx.py <fund_code>
```

### Search funds
```bash
python scripts/fund_search_tx.py <keyword>
```

## Fund Code Format

- ETF: `510300` (沪深300ETF), `512800` (银行ETF)
- LOF: `160106` (南方高增)
- Open-end: `000001` (华夏成长)

## Examples

```bash
# Get ETF quote
python scripts/fund_quote_tx.py 510300

# Search funds with "白酒"
python scripts/fund_search_tx.py 白酒

# Search ETF
python scripts/fund_search_tx.py 科技ETF
```

## File Structure

```
akshare-fund/
├── SKILL.md
└── scripts/
    ├── fund_quote_tx.py      # Real-time quote (Tencent)
    └── fund_search_tx.py     # Fund search (Tencent)
```

## Data Sources

- **Tencent Finance**: Real-time quotes, fund search (stable, fast)
- **AkShare**: NAV data, fund rankings (when network allows)

## Notes

- Tencent APIs work without registration
- ETF/LOF have real-time quotes, open-end funds have daily NAV
- Data is for reference only, not investment advice
