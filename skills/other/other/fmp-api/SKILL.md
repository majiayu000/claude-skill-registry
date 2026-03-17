---
name: fmp-api
description: Financial Modeling Prep API for stocks, fundamentals, SEC filings, institutional holdings (13F), and congressional trading. Use when fetching financial statements, ratios, DCF valuations, insider/institutional ownership, or screening stocks.
version: 1.0.0
---

# Financial Modeling Prep (FMP) API Integration

Comprehensive financial data API specializing in fundamental analysis, SEC filings, institutional holdings (13F), congressional trading data, and pre-computed valuations.

## Quick Start

### Authentication
```bash
# Environment variable (recommended)
export FMP_API_KEY="your_api_key"

# Or in .env file
FMP_API_KEY=your_api_key
```

### Basic Usage (Python)
```python
import requests
import os

API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com/stable"

def get_quote(symbol: str) -> dict:
    """Get real-time quote for a symbol."""
    response = requests.get(
        f"{BASE_URL}/quote",
        params={"symbol": symbol, "apikey": API_KEY}
    )
    data = response.json()
    return data[0] if data else {}

# Example
quote = get_quote("AAPL")
print(f"AAPL: ${quote['price']:.2f} ({quote['changePercentage']:+.2f}%)")
```

### Important: New Endpoint Format
FMP migrated to `/stable/` endpoints. Legacy `/api/v3/` endpoints require existing subscriptions.

```python
# NEW format (use this)
BASE_URL = "https://financialmodelingprep.com/stable"

# OLD format (legacy only)
# BASE_URL = "https://financialmodelingprep.com/api/v3"
```

## API Endpoints Reference

### Stock Quotes & Prices

| Endpoint | Description | Free |
|----------|-------------|------|
| `/quote` | Real-time quote | ✅ |
| `/quote-short` | Quick price | ✅ |
| `/historical-price-eod/full` | Historical EOD | ✅ |
| `/historical-price-intraday` | Intraday prices | ⚠️ Paid |
| `/pre-post-market-quote` | Extended hours | ⚠️ Paid |

### Financial Statements

| Endpoint | Description | Free |
|----------|-------------|------|
| `/income-statement` | Income statement | ✅ |
| `/balance-sheet-statement` | Balance sheet | ✅ |
| `/cash-flow-statement` | Cash flow | ✅ |
| `/income-statement-growth` | Income growth | ✅ |
| `/key-metrics` | Key metrics | ✅ |
| `/financial-ratios` | Financial ratios | ✅ |
| `/enterprise-values` | Enterprise value | ✅ |

### Valuations & Analysis

| Endpoint | Description | Free |
|----------|-------------|------|
| `/discounted-cash-flow` | DCF valuation | ✅ |
| `/historical-discounted-cash-flow` | Historical DCF | ✅ |
| `/rating` | Company rating | ✅ |
| `/historical-rating` | Rating history | ✅ |
| `/company-outlook` | Full company data | ✅ |

### Institutional & Insider Data

| Endpoint | Description | Free |
|----------|-------------|------|
| `/institutional-holder` | Institutional owners | ⚠️ Paid |
| `/mutual-fund-holder` | Mutual fund owners | ⚠️ Paid |
| `/insider-trading` | Insider transactions | ⚠️ Paid |
| `/form-13f` | 13F filings | ⚠️ Paid |
| `/senate-trading` | Senate trades | ⚠️ Paid |
| `/house-trading` | House trades | ⚠️ Paid |

### Screening & Discovery

| Endpoint | Description | Free |
|----------|-------------|------|
| `/stock-screener` | Screen stocks | ⚠️ Paid |
| `/stock-grade` | Stock grades | ✅ |
| `/search` | Search symbols | ✅ |
| `/search-name` | Search by name | ✅ |
| `/profile` | Company profile | ✅ |

### Calendars & Events

| Endpoint | Description | Free |
|----------|-------------|------|
| `/earnings-calendar` | Earnings dates | ✅ |
| `/ipo-calendar` | IPO dates | ✅ |
| `/stock-dividend-calendar` | Dividends | ✅ |
| `/stock-split-calendar` | Stock splits | ✅ |
| `/economic-calendar` | Economic events | ✅ |

### SEC Filings

| Endpoint | Description | Free |
|----------|-------------|------|
| `/sec-filings` | All SEC filings | ✅ |
| `/rss-feed-sec-filings` | SEC RSS feed | ✅ |

## Rate Limits

| Tier | Calls/Day | Calls/Min | Price |
|------|-----------|-----------|-------|
| Free | 250 | N/A | $0 |
| Starter | Unlimited | 300 | $22/mo |
| Premium | Unlimited | 750 | $59/mo |
| Ultimate | Unlimited | 3,000 | $149/mo |

**Free tier limitations:**
- ~100 sample symbols (AAPL, TSLA, AMZN, etc.)
- End-of-day data only
- 500MB bandwidth (30-day rolling)

## Common Tasks

### Task: Get Financial Statements
```python
def get_financials(symbol: str, period: str = "annual") -> dict:
    """Get comprehensive financial statements."""

    income = requests.get(
        f"{BASE_URL}/income-statement",
        params={"symbol": symbol, "period": period, "apikey": API_KEY}
    ).json()

    balance = requests.get(
        f"{BASE_URL}/balance-sheet-statement",
        params={"symbol": symbol, "period": period, "apikey": API_KEY}
    ).json()

    cashflow = requests.get(
        f"{BASE_URL}/cash-flow-statement",
        params={"symbol": symbol, "period": period, "apikey": API_KEY}
    ).json()

    return {
        "income_statement": income[0] if income else {},
        "balance_sheet": balance[0] if balance else {},
        "cash_flow": cashflow[0] if cashflow else {}
    }

# Example
financials = get_financials("AAPL")
print(f"Revenue: ${financials['income_statement'].get('revenue', 0):,.0f}")
```

### Task: Get Key Metrics & Ratios
```python
def get_key_metrics(symbol: str) -> dict:
    """Get important financial metrics."""

    metrics = requests.get(
        f"{BASE_URL}/key-metrics",
        params={"symbol": symbol, "period": "annual", "apikey": API_KEY}
    ).json()

    ratios = requests.get(
        f"{BASE_URL}/financial-ratios",
        params={"symbol": symbol, "period": "annual", "apikey": API_KEY}
    ).json()

    latest_metrics = metrics[0] if metrics else {}
    latest_ratios = ratios[0] if ratios else {}

    return {
        "market_cap": latest_metrics.get("marketCap"),
        "pe_ratio": latest_ratios.get("priceEarningsRatio"),
        "pb_ratio": latest_ratios.get("priceToBookRatio"),
        "roe": latest_ratios.get("returnOnEquity"),
        "roa": latest_ratios.get("returnOnAssets"),
        "debt_equity": latest_ratios.get("debtEquityRatio"),
        "current_ratio": latest_ratios.get("currentRatio"),
        "gross_margin": latest_ratios.get("grossProfitMargin"),
        "operating_margin": latest_ratios.get("operatingProfitMargin"),
        "net_margin": latest_ratios.get("netProfitMargin"),
        "dividend_yield": latest_ratios.get("dividendYield"),
        "payout_ratio": latest_ratios.get("payoutRatio")
    }
```

### Task: Get DCF Valuation
```python
def get_dcf_valuation(symbol: str) -> dict:
    """Get pre-computed DCF valuation."""
    response = requests.get(
        f"{BASE_URL}/discounted-cash-flow",
        params={"symbol": symbol, "apikey": API_KEY}
    )
    data = response.json()

    if data:
        dcf = data[0]
        return {
            "symbol": dcf.get("symbol"),
            "dcf_value": dcf.get("dcf"),
            "stock_price": dcf.get("stockPrice"),
            "upside": ((dcf.get("dcf", 0) / dcf.get("stockPrice", 1)) - 1) * 100
        }
    return {}

# Example
dcf = get_dcf_valuation("AAPL")
print(f"DCF Value: ${dcf['dcf_value']:.2f} ({dcf['upside']:+.1f}% upside)")
```

### Task: Get Company Profile
```python
def get_company_profile(symbol: str) -> dict:
    """Get comprehensive company information."""
    response = requests.get(
        f"{BASE_URL}/profile",
        params={"symbol": symbol, "apikey": API_KEY}
    )
    data = response.json()

    if data:
        profile = data[0]
        return {
            "name": profile.get("companyName"),
            "symbol": profile.get("symbol"),
            "sector": profile.get("sector"),
            "industry": profile.get("industry"),
            "market_cap": profile.get("mktCap"),
            "price": profile.get("price"),
            "beta": profile.get("beta"),
            "ceo": profile.get("ceo"),
            "website": profile.get("website"),
            "description": profile.get("description"),
            "employees": profile.get("fullTimeEmployees"),
            "exchange": profile.get("exchange"),
            "ipo_date": profile.get("ipoDate")
        }
    return {}
```

### Task: Get Earnings Calendar
```python
def get_earnings_calendar(from_date: str, to_date: str) -> list:
    """Get upcoming earnings announcements."""
    response = requests.get(
        f"{BASE_URL}/earnings-calendar",
        params={
            "from": from_date,
            "to": to_date,
            "apikey": API_KEY
        }
    )
    return response.json()

# Example
from datetime import datetime, timedelta
today = datetime.now()
next_week = today + timedelta(days=7)

earnings = get_earnings_calendar(
    today.strftime("%Y-%m-%d"),
    next_week.strftime("%Y-%m-%d")
)

for e in earnings[:5]:
    print(f"{e['symbol']}: {e['date']} ({e.get('time', 'N/A')})")
```

### Task: Get Historical Prices
```python
def get_historical_prices(symbol: str, start: str = None, end: str = None) -> list:
    """Get historical end-of-day prices."""
    params = {"symbol": symbol, "apikey": API_KEY}
    if start:
        params["from"] = start
    if end:
        params["to"] = end

    response = requests.get(
        f"{BASE_URL}/historical-price-eod/full",
        params=params
    )
    data = response.json()
    return data.get("historical", [])

# Example
prices = get_historical_prices("AAPL", "2025-01-01", "2025-12-01")
print(f"Got {len(prices)} days of data")
```

### Task: Search for Companies
```python
def search_companies(query: str, limit: int = 10) -> list:
    """Search for companies by name or symbol."""
    response = requests.get(
        f"{BASE_URL}/search",
        params={
            "query": query,
            "limit": limit,
            "apikey": API_KEY
        }
    )
    return response.json()

# Example
results = search_companies("Apple")
for r in results[:5]:
    print(f"{r['symbol']}: {r['name']} ({r['exchangeShortName']})")
```

### Task: Get SEC Filings
```python
def get_sec_filings(symbol: str, filing_type: str = None) -> list:
    """Get SEC filings for a company."""
    params = {"symbol": symbol, "apikey": API_KEY}
    if filing_type:
        params["type"] = filing_type  # 10-K, 10-Q, 8-K, etc.

    response = requests.get(
        f"{BASE_URL}/sec-filings",
        params=params
    )
    return response.json()

# Example: Get 10-K filings
filings = get_sec_filings("AAPL", "10-K")
for f in filings[:3]:
    print(f"{f['type']}: {f['fillingDate']} - {f['link']}")
```

## Error Handling

```python
def safe_api_call(endpoint: str, params: dict) -> dict:
    """Make API call with error handling."""
    params["apikey"] = API_KEY

    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        data = response.json()

        # Check for error messages
        if isinstance(data, dict) and "Error Message" in data:
            print(f"API Error: {data['Error Message']}")
            return {}

        # Check for empty response
        if not data:
            print(f"No data returned for {endpoint}")
            return {}

        return data

    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return {}
    except ValueError as e:
        print(f"JSON decode error: {e}")
        return {}
```

## Free vs Paid Features

### Free Tier Includes
- 250 API calls/day
- ~100 sample symbols
- Financial statements
- Key metrics & ratios
- DCF valuations
- Company profiles
- Earnings calendar
- SEC filings list
- Basic historical data

### Paid Features (Starter+)
- Unlimited symbols
- Intraday data
- Stock screener
- International stocks
- Institutional holders
- Mutual fund holders
- ETF holdings breakdown

### Paid Features (Premium+)
- Higher rate limits
- 13F filings
- Insider trading
- Congressional trading (Senate/House)
- Analyst estimates
- Earnings transcripts
- Extended hours data

## Unique FMP Features

1. **Pre-computed DCF** - Ready-to-use valuations
2. **Congressional Trading** - Senate/House STOCK Act data
3. **13F Filings** - Institutional holdings analysis
4. **Standardized Financials** - Normalized line items
5. **Company Outlook** - All data in one endpoint
6. **Rating System** - Proprietary company ratings

## Best Practices

1. **Use stable endpoints** - `/stable/` not `/api/v3/`
2. **Cache static data** - Profiles, historical data
3. **Monitor daily limits** - 250 calls goes fast
4. **Batch symbol lookups** - Where supported
5. **Store financials** - They only update quarterly
6. **Use company-outlook** - Single call for all data

## Installation

```python
# Recommended Python wrapper
pip install --upgrade FinancialModelingPrep-Python

# Basic usage
from fmp_python.fmp import FMP
fmp = FMP(api_key="your_api_key")
profile = fmp.get_company_profile("AAPL")
```

## Related Skills
- `finnhub-api` - Real-time quotes and news
- `twelvedata-api` - Technical indicators
- `alphavantage-api` - Economic indicators

## References
- [Official Documentation](https://site.financialmodelingprep.com/developer/docs)
- [Pricing Plans](https://site.financialmodelingprep.com/pricing-plans)
- [Python Wrapper](https://github.com/thinh-vu/FinancialModelingPrep)
- [Stable API Migration](https://site.financialmodelingprep.com/developer/docs/stable-api)
