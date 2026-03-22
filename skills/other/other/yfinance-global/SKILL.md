---
name: "yfinance-global"
description: "全球股票行情数据工具。优先使用国内数据源(腾讯财经)，支持A股、港股、美股和全球指数。自动回退到Yahoo Finance获取海外数据。"
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    install:
      - id: python-packages
        kind: pip
        packages: ["yfinance", "pandas", "numpy", "requests"]
---

# yfinance-global

全球股票数据工具，**优先使用国内数据源**，确保在国内网络环境下的稳定性。

## 数据源优先级

1. **腾讯财经** (qt.gtimg.cn) - A股、港股、指数
2. **新浪财经** (hq.sinajs.cn) - 美股
3. **Yahoo Finance** - 其他海外数据（备用）

## 网络配置

已自动配置：
- 强制使用 IPv4
- 连接超时设置

## Features

- A股股票 (000001, 600000, 300750 等)
- 港股 (00700, 09988, 03690 等)
- 美股 (AAPL, TSLA, NVDA 等)
- 全球指数 (^GSPC, ^IXIC, ^HSI 等)
- 历史价格数据
- 技术指标 (RSI, MACD, MA)
- 多股票对比
- 加密货币数据

## Commands

### 统一行情查询 (推荐)
```bash
python scripts/quote.py <code>
```

支持格式：
- A股: `000001` (上证指数), `600000` (浦发银行)
- 港股: `00700` (腾讯), `09988` (阿里)
- 美股: `AAPL`, `TSLA`
- 指数: `GSPC` (标普500), `IXIC` (纳指)
python scripts/yf_search.py <keyword>
```

### Technical analysis (RSI, MACD, MA)
```bash
python scripts/yf_tech.py <ticker>
```

### Compare multiple stocks
```bash
python scripts/yf_compare.py <ticker1> <ticker2> [ticker3...]
```

### Market overview (global indices)
```bash
python scripts/yf_market.py
```

### Cryptocurrency data
```bash
python scripts/yf_crypto.py <symbol>
```

## Ticker Format

- US Stocks: `AAPL`, `TSLA`, `MSFT`, `GOOGL`
- HK Stocks: `0700.HK`, `9988.HK`, `3690.HK`
- Indices: `^GSPC` (S&P 500), `^IXIC` (Nasdaq)
- ETFs: `SPY`, `QQQ`, `ARKK`
- Crypto: `BTC-USD`, `ETH-USD`, `SOL-USD`

## Examples

```bash
# Apple stock info
python scripts/yf_quote.py AAPL

# Tencent (HK)
python scripts/yf_quote.py 0700.HK

# Tesla history
python scripts/yf_hist.py TSLA 30

# Technical analysis
python scripts/yf_tech.py AAPL

# Compare FAANG stocks
python scripts/yf_compare.py AAPL MSFT GOOGL AMZN META

# Market overview
python scripts/yf_market.py

# Bitcoin
python scripts/yf_crypto.py BTC-USD

# Search
python scripts/yf_search.py apple
```

## File Structure

```
yfinance-global/
├── SKILL.md
└── scripts/
    ├── yf_quote.py       # Stock quote and info
    ├── yf_hist.py        # Historical data
    ├── yf_search.py      # Stock search
    ├── yf_tech.py        # Technical indicators (RSI, MACD, MA)
    ├── yf_compare.py     # Multi-stock comparison
    ├── yf_market.py      # Global market overview
    └── yf_crypto.py      # Cryptocurrency data
```

## Data Sources

- **Yahoo Finance**: Global stock data, free, no API key required

## Technical Indicators

| Indicator | Description |
|-----------|-------------|
| MA5/10/20/60 | Moving Averages |
| RSI (14) | Relative Strength Index (Overbought >70, Oversold <30) |
| MACD | Moving Average Convergence Divergence |
| Support/Resistance | Recent high/low levels |

## Notes

- No API key required
- Data may have 15-20 minute delay
- Some network environments may have access restrictions to Yahoo Finance
- Please respect rate limits (don't spam requests)
