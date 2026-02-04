---
name: quodd
description: Fetch real-time stock quotes via Quodd API. Get current prices, daily high/low, and after-hours data for US equities. Use when the user asks for stock prices, quotes, market data, or ticker information.
metadata: {"openclaw":{"emoji":"📈","requires":{"bins":["python3"],"env":["QUODD_USERNAME","QUODD_PASSWORD"]}}}
---

# Quodd Stock Quotes

Fetch real-time stock quotes for US equities via the Quodd API.

For more information, visit: https://www.quodd.com/stock-and-etf-data

## Quick Start

```bash
# Get a quote for Apple
python scripts/quote.py AAPL

# Get quotes for multiple tickers
python scripts/quote.py AAPL MSFT META
```

## Prerequisites

Set the following environment variables:

```bash
export QUODD_USERNAME="your_username"
export QUODD_PASSWORD="your_password"
```

## Usage

### Single Ticker

```bash
python scripts/quote.py AAPL
```

### Multiple Tickers

```bash
python scripts/quote.py AAPL MSFT META GOOGL
```

### JSON Output

```bash
python scripts/quote.py AAPL --format json
```

### Force Token Refresh

```bash
python scripts/quote.py AAPL --no-cache
```

## Output Format

### Text (Default)

```
Quodd Stock Quotes
Symbol   Date        Time      High      Low     Close    AH Time     AH Price
-------------------------------------------------------------------------------
AAPL     01/29/26    14:30    185.50   180.25   182.63   17:45:30     182.80
```

### JSON

```json
{
  "quotes": [
    {
      "symbol": "AAPL",
      "date": "01/29/26",
      "time": "14:30",
      "high": 185.50,
      "low": 180.25,
      "close": 182.63,
      "after_hours_time": "17:45:30",
      "after_hours_price": 182.80
    }
  ]
}
```

## Output Fields

- **Symbol** - Stock ticker symbol
- **Date** - Quote date
- **Time** - Quote time
- **High** - Day high price
- **Low** - Day low price
- **Close** - Last traded price
- **AH Time** - After hours trade time
- **AH Price** - After hours price
