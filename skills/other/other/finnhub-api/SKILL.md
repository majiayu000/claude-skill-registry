---
name: finnhub-api
description: FinnHub financial data API integration for stocks, forex, crypto, news, and fundamentals. Use when fetching real-time quotes, company profiles, financial statements, insider trading, earnings calendars, or market news.
version: 1.0.0
---

# FinnHub API Integration

Complete integration with FinnHub's financial data API providing access to stocks, forex, crypto, company fundamentals, news, and real-time market data.

## Quick Start

### Authentication
```bash
# Environment variable (recommended)
export FINNHUB_API_KEY="your_api_key"

# Or in .env file
FINNHUB_API_KEY=your_api_key
```

### Basic Usage (Python)
```python
import requests
import os

API_KEY = os.getenv("FINNHUB_API_KEY")
BASE_URL = "https://finnhub.io/api/v1"

def get_quote(symbol: str) -> dict:
    """Get real-time quote for a symbol."""
    response = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": symbol, "token": API_KEY}
    )
    return response.json()

# Example
quote = get_quote("AAPL")
print(f"AAPL: ${quote['c']:.2f} ({quote['dp']:+.2f}%)")
```

### Using Official SDK
```python
import finnhub

client = finnhub.Client(api_key="your_api_key")

# Get quote
quote = client.quote("AAPL")

# Get company profile
profile = client.company_profile2(symbol="AAPL")

# Get financials
financials = client.company_basic_financials("AAPL", "all")
```

## API Endpoints Reference

### Stock Market Data

| Endpoint | Description | Free |
|----------|-------------|------|
| `/quote` | Real-time quote | ✅ |
| `/stock/candle` | Historical OHLCV | ✅ |
| `/stock/profile2` | Company profile | ✅ |
| `/stock/peers` | Similar companies | ✅ |
| `/company-news` | Company news | ✅ |
| `/stock/metric` | Basic financials | ✅ |
| `/stock/financials` | Financial statements | ✅ |
| `/stock/insider-transactions` | Insider trades | ⚠️ Premium |
| `/stock/insider-sentiment` | Insider sentiment | ⚠️ Premium |

### Fundamental Data

| Endpoint | Description | Free |
|----------|-------------|------|
| `/stock/financials-reported` | SEC reported | ✅ |
| `/stock/earnings` | Earnings history | ✅ |
| `/stock/recommendation` | Analyst ratings | ✅ |
| `/stock/price-target` | Price targets | ✅ |
| `/stock/revenue-estimate` | Revenue estimates | ⚠️ Premium |
| `/stock/eps-estimate` | EPS estimates | ⚠️ Premium |

### Forex & Crypto

| Endpoint | Description | Free |
|----------|-------------|------|
| `/forex/rates` | Exchange rates | ✅ |
| `/forex/candle` | Forex OHLCV | ✅ |
| `/crypto/candle` | Crypto OHLCV | ✅ |
| `/crypto/exchanges` | Crypto exchanges | ✅ |
| `/crypto/symbol` | Crypto symbols | ✅ |

### News & Sentiment

| Endpoint | Description | Free |
|----------|-------------|------|
| `/company-news` | Company news | ✅ |
| `/news` | Market news | ✅ |
| `/press-releases` | Press releases | ⚠️ Premium |
| `/news-sentiment` | News sentiment | ⚠️ Premium |

### Calendar Events

| Endpoint | Description | Free |
|----------|-------------|------|
| `/calendar/earnings` | Earnings calendar | ✅ |
| `/calendar/ipo` | IPO calendar | ✅ |
| `/stock/dividends` | Dividend history | ✅ |
| `/stock/splits` | Stock splits | ✅ |

## Rate Limits

| Tier | Calls/Minute | Notes |
|------|--------------|-------|
| Free | 60 | US stocks, forex, crypto |
| Paid | 300+ | Per-market pricing |

**Rate limit headers:**
- `X-Ratelimit-Limit`: Max calls per minute
- `X-Ratelimit-Remaining`: Calls remaining
- `X-Ratelimit-Reset`: Reset timestamp

## Common Tasks

### Task: Get Stock Quote with Change
```python
def get_stock_info(symbol: str) -> dict:
    """Get comprehensive stock info."""
    quote = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": symbol, "token": API_KEY}
    ).json()

    profile = requests.get(
        f"{BASE_URL}/stock/profile2",
        params={"symbol": symbol, "token": API_KEY}
    ).json()

    return {
        "symbol": symbol,
        "name": profile.get("name"),
        "price": quote["c"],
        "change": quote["d"],
        "change_percent": quote["dp"],
        "high": quote["h"],
        "low": quote["l"],
        "market_cap": profile.get("marketCapitalization"),
        "industry": profile.get("finnhubIndustry")
    }
```

### Task: Get Historical Candles
```python
import time

def get_candles(symbol: str, resolution: str = "D", days: int = 30) -> dict:
    """
    Get historical OHLCV data.

    Resolutions: 1, 5, 15, 30, 60, D, W, M
    """
    end = int(time.time())
    start = end - (days * 24 * 60 * 60)

    response = requests.get(
        f"{BASE_URL}/stock/candle",
        params={
            "symbol": symbol,
            "resolution": resolution,
            "from": start,
            "to": end,
            "token": API_KEY
        }
    )
    return response.json()
```

### Task: Get Earnings Calendar
```python
def get_earnings_calendar(from_date: str, to_date: str) -> list:
    """Get upcoming earnings releases."""
    response = requests.get(
        f"{BASE_URL}/calendar/earnings",
        params={
            "from": from_date,
            "to": to_date,
            "token": API_KEY
        }
    )
    return response.json().get("earningsCalendar", [])

# Example: Get next week's earnings
earnings = get_earnings_calendar("2025-12-05", "2025-12-12")
```

### Task: Get Company News
```python
def get_company_news(symbol: str, days: int = 7) -> list:
    """Get recent company news."""
    from datetime import datetime, timedelta

    end = datetime.now()
    start = end - timedelta(days=days)

    response = requests.get(
        f"{BASE_URL}/company-news",
        params={
            "symbol": symbol,
            "from": start.strftime("%Y-%m-%d"),
            "to": end.strftime("%Y-%m-%d"),
            "token": API_KEY
        }
    )
    return response.json()
```

### Task: Get Financial Metrics
```python
def get_financials(symbol: str) -> dict:
    """Get key financial metrics."""
    response = requests.get(
        f"{BASE_URL}/stock/metric",
        params={
            "symbol": symbol,
            "metric": "all",
            "token": API_KEY
        }
    )
    data = response.json()

    metrics = data.get("metric", {})
    return {
        "pe_ratio": metrics.get("peBasicExclExtraTTM"),
        "pb_ratio": metrics.get("pbQuarterly"),
        "ps_ratio": metrics.get("psAnnual"),
        "roe": metrics.get("roeTTM"),
        "roa": metrics.get("roaTTM"),
        "debt_equity": metrics.get("totalDebt/totalEquityQuarterly"),
        "current_ratio": metrics.get("currentRatioQuarterly"),
        "gross_margin": metrics.get("grossMarginTTM"),
        "operating_margin": metrics.get("operatingMarginTTM"),
        "52w_high": metrics.get("52WeekHigh"),
        "52w_low": metrics.get("52WeekLow"),
        "beta": metrics.get("beta")
    }
```

## WebSocket Real-Time Data

```python
import websocket
import json

def on_message(ws, message):
    data = json.loads(message)
    if data["type"] == "trade":
        for trade in data["data"]:
            print(f"{trade['s']}: ${trade['p']:.2f} x {trade['v']}")

def on_open(ws):
    # Subscribe to symbols
    ws.send(json.dumps({"type": "subscribe", "symbol": "AAPL"}))
    ws.send(json.dumps({"type": "subscribe", "symbol": "MSFT"}))

ws = websocket.WebSocketApp(
    f"wss://ws.finnhub.io?token={API_KEY}",
    on_message=on_message,
    on_open=on_open
)
ws.run_forever()
```

## Error Handling

```python
def safe_api_call(endpoint: str, params: dict) -> dict:
    """Make API call with error handling."""
    params["token"] = API_KEY

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()

        # Check for rate limit
        remaining = response.headers.get("X-Ratelimit-Remaining")
        if remaining and int(remaining) < 5:
            print(f"Warning: Only {remaining} API calls remaining")

        return response.json()

    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            print("Rate limit exceeded. Waiting 60 seconds...")
            time.sleep(60)
            return safe_api_call(endpoint, params)
        raise
    except Exception as e:
        print(f"API error: {e}")
        return {}
```

## Free vs Premium Features

### Free Tier Includes
- Real-time US stock quotes
- Historical data (1 year)
- Company profiles & peers
- Basic financials & metrics
- Earnings calendar
- Company news
- Forex & crypto data
- WebSocket (US stocks, forex, crypto)

### Premium Required
- Insider transactions & sentiment
- SEC filings
- ESG scores
- Patent data
- Congressional trading
- International markets
- Revenue/EPS estimates
- Lobbying data
- Extended historical data

## Best Practices

1. **Cache static data** - Company profiles, metrics rarely change
2. **Use WebSocket** - For real-time quotes instead of polling
3. **Batch where possible** - Reduce API calls
4. **Handle rate limits** - Implement exponential backoff
5. **Store API key securely** - Use environment variables

## Installation

```bash
# Python SDK
pip install finnhub-python

# JavaScript SDK
npm install finnhub
```

## Related Skills
- `twelvedata-api` - Alternative market data source
- `alphavantage-api` - Technical indicators focus
- `fmp-api` - Fundamental analysis focus

## References
- [Official Documentation](https://finnhub.io/docs/api)
- [Python SDK](https://github.com/Finnhub-Stock-API/finnhub-python)
- [Pricing](https://finnhub.io/pricing)
