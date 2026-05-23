---
name: alphavantage-routing
description: Reference for all Alpha Vantage MCP tools. Use when exploring available data.
---

# Alpha Vantage Tools Reference

## Currently Active (alphavantage-earnings agent)

| Tool | Description |
|------|-------------|
| EARNINGS_ESTIMATES | Forward + historical consensus EPS/revenue with revision trends |
| EARNINGS | Actual vs estimate with surprise % |
| EARNINGS_CALENDAR | Upcoming earnings dates |

---

## Price Data

| Tool | Description |
|------|-------------|
| TIME_SERIES_INTRADAY | 1min/5min/15min/30min/60min OHLCV |
| TIME_SERIES_DAILY | Daily OHLCV (20+ years) |
| TIME_SERIES_DAILY_ADJUSTED | Daily with splits/dividends adjusted |
| TIME_SERIES_WEEKLY | Weekly OHLCV |
| TIME_SERIES_WEEKLY_ADJUSTED | Weekly adjusted |
| TIME_SERIES_MONTHLY | Monthly OHLCV |
| TIME_SERIES_MONTHLY_ADJUSTED | Monthly adjusted |
| GLOBAL_QUOTE | Latest price/volume snapshot |
| REALTIME_BULK_QUOTES | Up to 100 symbols at once |

## Fundamentals

| Tool | Description |
|------|-------------|
| COMPANY_OVERVIEW | Company info, ratios, metrics |
| INCOME_STATEMENT | Annual/quarterly income statements |
| BALANCE_SHEET | Annual/quarterly balance sheets |
| CASH_FLOW | Annual/quarterly cash flow |
| EARNINGS | Historical EPS actual vs estimate |
| EARNINGS_ESTIMATES | Consensus estimates + revisions |
| EARNINGS_CALENDAR | Upcoming earnings dates |
| DIVIDENDS | Historical + declared dividends |
| SPLITS | Historical stock splits |
| ETF_PROFILE | ETF holdings and allocations |
| LISTING_STATUS | Active/delisted stocks list |
| IPO_CALENDAR | Upcoming IPOs |

## News & Sentiment

| Tool | Description |
|------|-------------|
| NEWS_SENTIMENT | News with sentiment scores, topics filter |
| EARNINGS_CALL_TRANSCRIPT | Quarterly call transcripts |
| INSIDER_TRANSACTIONS | Insider buys/sells |
| TOP_GAINERS_LOSERS | Daily market movers |

## Options

| Tool | Description |
|------|-------------|
| REALTIME_OPTIONS | Current options chain with greeks |
| HISTORICAL_OPTIONS | Historical options data by date |

## Technical Indicators

| Tool | Params |
|------|--------|
| SMA, EMA, WMA, DEMA, TEMA, TRIMA, KAMA | symbol, interval, time_period, series_type |
| MACD, MACDEXT | symbol, interval, series_type |
| RSI, STOCHRSI | symbol, interval, time_period, series_type |
| STOCH, STOCHF | symbol, interval |
| BBANDS | symbol, interval, time_period, series_type |
| ADX, ADXR, DX | symbol, interval, time_period |
| AROON, AROONOSC | symbol, interval, time_period |
| CCI, CMO, MOM, ROC, ROCR | symbol, interval, time_period |
| MFI, WILLR, BOP | symbol, interval |
| ATR, NATR, TRANGE | symbol, interval |
| OBV, AD, ADOSC | symbol, interval |
| SAR, VWAP | symbol, interval |
| HT_TRENDLINE, HT_SINE, HT_TRENDMODE | symbol, interval, series_type |

## Economic Indicators

| Tool | Description |
|------|-------------|
| REAL_GDP | US GDP annual/quarterly |
| REAL_GDP_PER_CAPITA | US GDP per capita |
| TREASURY_YIELD | 3mo/2yr/5yr/7yr/10yr/30yr yields |
| FEDERAL_FUNDS_RATE | Fed funds rate |
| CPI | Consumer Price Index |
| INFLATION | Annual inflation rate |
| RETAIL_SALES | Monthly retail sales |
| DURABLES | Durable goods orders |
| UNEMPLOYMENT | Unemployment rate |
| NONFARM_PAYROLL | Total nonfarm employment |

## Commodities

| Tool | Description |
|------|-------------|
| WTI | West Texas crude oil |
| BRENT | Brent crude oil |
| NATURAL_GAS | Henry Hub natural gas |
| COPPER, ALUMINUM | Industrial metals |
| WHEAT, CORN, COTTON, SUGAR, COFFEE | Agricultural |
| ALL_COMMODITIES | Global commodity index |

## Forex & Crypto

| Tool | Description |
|------|-------------|
| CURRENCY_EXCHANGE_RATE | Realtime FX rate |
| FX_INTRADAY, FX_DAILY, FX_WEEKLY, FX_MONTHLY | FX time series |
| CRYPTO_INTRADAY | Crypto intraday |
| DIGITAL_CURRENCY_DAILY/WEEKLY/MONTHLY | Crypto time series |

## Analytics

| Tool | Description |
|------|-------------|
| ANALYTICS_FIXED_WINDOW | Metrics over fixed date range |
| ANALYTICS_SLIDING_WINDOW | Metrics with moving window |

## Utility

| Tool | Description |
|------|-------------|
| SYMBOL_SEARCH | Find ticker by keyword |
| MARKET_STATUS | Global market open/close status |
| SEARCH | Natural language query |
| FETCH | Fetch by function name |

---

## Note
Free tier has rate limits. Use sparingly.
