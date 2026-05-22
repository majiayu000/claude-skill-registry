---
name: finnhub
description: Access Finnhub API for real-time stock quotes, company news, market data, financial statements, and trading signals. Use when you need current stock prices, company news, earnings data, or market analysis.
homepage: https://finnhub.io
metadata:
  {
    "openclaw": {
      "emoji": "📈",
      "requires": { "env": ["FINNHUB_API_KEY"] },
      "primaryEnv": "FINNHUB_API_KEY",
    },
  }
---

# Finnhub API

Access real-time and historical stock market data, company news, financial statements, and market indicators via the Finnhub API.

## Quick Start

Get your API key from [finnhub.io](https://finnhub.io) (free tier available).

Configure in OpenClaw:

```json5
{
  skills: {
    entries: {
      finnhub: {
        enabled: true,
        apiKey: "your-finnhub-api-key",
        env: {
          FINNHUB_API_KEY: "your-finnhub-api-key",
        },
      },
    },
  },
}
```

Or add to `~/.openclaw/.env`:

```
FINNHUB_API_KEY=your-api-key-here
```

## API Endpoints

Base URL: `https://finnhub.io/api/v1`

All requests require `?token=${FINNHUB_API_KEY}` parameter.

### Stock Quotes (Real-time)

Get current stock price:

```bash
curl "https://finnhub.io/api/v1/quote?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

Returns: `c` (current price), `h` (high), `l` (low), `o` (open), `pc` (previous close), `t` (timestamp)

### Company News

Get latest company news:

```bash
# News for a symbol
curl "https://finnhub.io/api/v1/company-news?symbol=AAPL&from=2025-01-01&to=2025-02-01&token=${FINNHUB_API_KEY}"

# General market news
curl "https://finnhub.io/api/v1/news?category=general&token=${FINNHUB_API_KEY}"
```

### Company Profile

Get company information:

```bash
curl "https://finnhub.io/api/v1/stock/profile2?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

### Financial Statements

Get company financials:

```bash
# Income statement
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&token=${FINNHUB_API_KEY}"

# Balance sheet
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&statement=bs&token=${FINNHUB_API_KEY}"

# Cash flow
curl "https://finnhub.io/api/v1/stock/financials-reported?symbol=AAPL&statement=cf&token=${FINNHUB_API_KEY}"

# Search in SEC filings (10-K, 10-Q, etc.)
# Note: This endpoint may require premium tier or have a different path
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=revenue&token=${FINNHUB_API_KEY}"
```

### Market Data

Get market indicators:

```bash
# Stock candles (OHLCV)
curl "https://finnhub.io/api/v1/stock/candle?symbol=AAPL&resolution=D&from=1609459200&to=1640995200&token=${FINNHUB_API_KEY}"

# Stock symbols (search)
curl "https://finnhub.io/api/v1/search?q=apple&token=${FINNHUB_API_KEY}"

# Market status
curl "https://finnhub.io/api/v1/stock/market-status?exchange=US&token=${FINNHUB_API_KEY}"
```

### Trading Signals

Get technical indicators and signals:

```bash
# Technical indicators (may require premium tier)
curl "https://finnhub.io/api/v1/indicator?symbol=AAPL&indicator=rsi&resolution=D&token=${FINNHUB_API_KEY}"

# Support/Resistance (may require premium tier)
curl "https://finnhub.io/api/v1/scan/support-resistance?symbol=AAPL&resolution=D&token=${FINNHUB_API_KEY}"

# Pattern recognition (may require premium tier)
curl "https://finnhub.io/api/v1/scan/pattern?symbol=AAPL&resolution=D&token=${FINNHUB_API_KEY}"
```

**Note:** Some technical indicator endpoints may require a premium subscription. Free tier includes basic market data and quotes.

### Earnings & Calendar

Get earnings data:

```bash
# Earnings calendar
curl "https://finnhub.io/api/v1/calendar/earnings?from=2025-02-01&to=2025-02-28&token=${FINNHUB_API_KEY}"

# Company earnings
curl "https://finnhub.io/api/v1/stock/earnings?symbol=AAPL&token=${FINNHUB_API_KEY}"
```

## Common Use Cases

### Find Trading Opportunities

1. Search for stocks: `GET /search?q=keyword`
2. Get current quote: `GET /quote?symbol=SYMBOL`
3. Check recent news: `GET /company-news?symbol=SYMBOL&from=DATE&to=DATE`
4. Analyze technical indicators: `GET /indicator?symbol=SYMBOL&indicator=rsi`
5. Review financials: `GET /stock/financials-reported?symbol=SYMBOL`
6. Search SEC filings: `GET /stock/search-in-filing?symbol=SYMBOL&query=KEYWORD`

### Monitor Stock Performance

1. Get real-time quote: `GET /quote?symbol=SYMBOL`
2. Get historical candles: `GET /stock/candle?symbol=SYMBOL&resolution=D`
3. Check company profile: `GET /stock/profile2?symbol=SYMBOL`
4. Review earnings: `GET /stock/earnings?symbol=SYMBOL`

### Research Company News

1. Company-specific news: `GET /company-news?symbol=SYMBOL`
2. General market news: `GET /news?category=general`
3. Sector news: `GET /news?category=technology`

### Search SEC Filings

Search within company SEC filings (10-K, 10-Q, 8-K, etc.):

```bash
# Search for specific terms in filings
# Note: This endpoint may require premium tier or have a different path
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=revenue&token=${FINNHUB_API_KEY}"

# Search for risk factors
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=risk&token=${FINNHUB_API_KEY}"

# Search for specific financial metrics
curl "https://finnhub.io/api/v1/stock/search-in-filing?symbol=AAPL&query=EBITDA&token=${FINNHUB_API_KEY}"
```

This endpoint searches through SEC filings (10-K, 10-Q, 8-K, etc.) for specific keywords or phrases, useful for finding mentions of specific topics, risks, or financial metrics in official company documents.

## Rate Limits

Free tier:
- 60 API calls/minute
- Real-time data: limited
- Historical data: available

Paid tiers offer higher limits and additional features.

## Notes

- Always include `token=${FINNHUB_API_KEY}` in query parameters
- Use proper date formats: `YYYY-MM-DD` for date ranges
- Timestamps are Unix epoch seconds
- Symbol format: use exchange prefix if needed (e.g., `US:AAPL` for US stocks)
- For paper trading, combine Finnhub data with Alpaca API for execution

