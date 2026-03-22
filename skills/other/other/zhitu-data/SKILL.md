---
name: "zhitu-data"
description: "Free stock data via 智兔数服. Real-time quotes, historical data, and technical indicators for A-shares, HK stocks, and funds. No registration required."
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-packages
        kind: pip
        packages: ["requests"]
---

# zhitu-data

Free stock data skill powered by [智兔数服](https://zhituapi.com).

## Setup

### 1. Install Dependencies

```bash
pip install requests
```

### 2. No Registration Required

智兔数服 provides a free test token, no registration needed!

```bash
# Free test token (built into scripts)
export ZHITU_TOKEN="ZHITU_TOKEN_LIMIT_TEST"
```

## Features

- **A-Share Real-time** - Real-time quotes for all A-shares
- **Hong Kong Stocks** - HK stock data
- **Fund Data** - ETF and LOF fund quotes
- **Beijing Exchange** - 北交所 stock data
- **Historical K-line** - Daily, weekly, monthly data
- **Technical Indicators** - MACD, KDJ, BOLL, MA built-in
- **No Registration** - Completely free, no signup needed
- **No Rate Limits** - Unlimited calls with test token

## Commands

### Real-time Quotes
```bash
python scripts/zhitu_quote.py <code>
```

### Historical Data
```bash
python scripts/zhitu_hist.py <code> [start_date] [end_date]
```

### Technical Indicators
```bash
python scripts/zhitu_tech.py <code> <indicator>
```

### Stock List
```bash
python scripts/zhitu_list.py [market]
```

## Stock Code Format

- **Shanghai A-share**: `600000.SH` or just `600000`
- **Shenzhen A-share**: `000001.SZ` or just `000001`
- **ChiNext**: `300001.SZ` or just `300001`
- **STAR Market**: `688001.SH` or just `688001`
- **Beijing Exchange**: `430047.BJ` or just `430047`
- **Hong Kong**: `00001.HK` or just `00001`
- **Fund**: `510300.SH` or just `510300`

## Examples

```bash
# A-share real-time quote
python scripts/zhitu_quote.py 000001
python scripts/zhitu_quote.py 600519.SH

# Historical data
python scripts/zhitu_hist.py 600519 20240101 20240312

# Technical indicators
python scripts/zhitu_tech.py 000001 MACD
python scripts/zhitu_tech.py 600519 KDJ

# Stock list
python scripts/zhitu_list.py
python scripts/zhitu_list.py sh
```

## Technical Indicators

| Indicator | Description |
|:---|:---|
| MACD | Moving Average Convergence Divergence |
| KDJ | Stochastic Oscillator |
| BOLL | Bollinger Bands |
| MA | Moving Average |

## File Structure

```
zhitu-data/
├── SKILL.md
└── scripts/
    ├── zhitu_quote.py      # Real-time quotes
    ├── zhitu_hist.py       # Historical K-line data
    ├── zhitu_tech.py       # Technical indicators
    └── zhitu_list.py       # Stock list
```

## Data Sources

- **智兔数服** - Free stock data API for A-shares, HK, funds

## Features Comparison

| Feature | 智兔数服 | Other APIs |
|:---|:---|:---|
| **Registration** | Not required | Usually required |
| **Cost** | Completely free | Free/Paid |
| **A-Share Data** | ✅ Full coverage | Partial |
| **HK Stocks** | ✅ Supported | Varies |
| **北交所** | ✅ Supported | Rare |
| **Technical Indicators** | ✅ Built-in | Varies |
| **Rate Limits** | Generous | Strict |

## Notes

- Test token may have usage limits for high-frequency calls
- For production use, consider registering for a free API key
- Data is suitable for personal research and learning
- HK stock data may be delayed

## Links

- [智兔数服官网](https://zhituapi.com)
- [API Documentation](https://zhituapi.com/docs)
