---
name: fii-dii-flow-tracker
description: >
  Track and analyze FII/DII daily buy/sell flows in Indian markets.
  Use when user asks about institutional flows, FII selling/buying trends,
  DII activity, or institutional impact on Nifty/market direction.
tags:
  - india
  - fii
  - dii
  - institutional-flows
  - nifty
  - market-analysis
triggers:
  - FII
  - DII
  - institutional flow
  - foreign investor
  - domestic investor
  - FII selling
  - FII buying
  - DII buying
  - institutional activity
  - FII DII data
  - net buy
  - net sell
  - institutional impact
  - FII outflow
  - FII inflow
---

# FII/DII Flow Tracker

## Purpose

This skill tracks Foreign Institutional Investor (FII) and Domestic Institutional Investor (DII) daily buy/sell flows in Indian equity markets and correlates them with Nifty 50 movement. It provides actionable insights on institutional positioning, flow trends, regime changes, and market implications.

## When to Use

Activate this skill when the user asks about:

- FII or DII daily, weekly, or monthly buy/sell data
- Institutional flow trends and their market impact
- Whether FII are net buyers or net sellers
- DII activity and mutual fund flow support
- Correlation between institutional flows and Nifty direction
- Sector-wise institutional allocation
- Impact of FII flows on INR (Indian Rupee)
- Historical institutional flow patterns during market events
- Flow regime assessment (bullish/bearish/neutral institutional positioning)

## Workflow

Follow these steps in order when the user requests FII/DII flow analysis:

### Step 1: Fetch Current FII/DII Flow Data

Use web search to retrieve the latest FII/DII cash market data from authoritative sources:

```
WebSearch: "FII DII data today {current_date} cash market net buy sell"
WebSearch: "NSDL FII activity {current_month} {current_year}"
WebSearch: "MoneyControl FII DII activity {current_date}"
```

Primary data sources to query:
- **NSDL** (National Securities Depository Limited): Official FII/FPI transaction data
- **NSE** (National Stock Exchange): Daily institutional trading statistics
- **MoneyControl FII/DII page**: Aggregated daily flow data with historical tables
- **CDSL** (Central Depository Services Limited): Supplementary FPI data
- **Trendlyne / Tickertape**: Pre-computed flow summaries and charts

Extract the following data points:
- FII gross buy value (in crores)
- FII gross sell value (in crores)
- FII net buy/sell value (in crores)
- DII gross buy value (in crores)
- DII gross sell value (in crores)
- DII net buy/sell value (in crores)
- Date of the data

### Step 2: Fetch Historical Flow Data for Trend Analysis

Use web search to gather flow data for the trailing period:

```
WebSearch: "FII DII data last 10 trading days {current_month} {current_year}"
WebSearch: "FII net investment {current_month} {current_year} month to date"
WebSearch: "FII DII yearly data {current_year} year to date"
```

Build a table of the last 10 trading days with daily FII and DII net values.

### Step 3: Fetch Nifty 50 Price Data

Use Groww MCP tools to get Nifty price data for correlation analysis:

```python
# Get current Nifty LTP
get_ltp(search_queries=["NIFTY"], segment="CASH", query_type="stocks")

# Get historical Nifty data for correlation (last 30 trading days, daily candles)
fetch_historical_candle_data(
    trading_symbol="NIFTY",
    start_time="{30_trading_days_ago} 09:15:00",
    end_time="{today} 15:30:00",
    interval_in_minutes="1440",
    exchange="NSE",
    segment="CASH"
)
```

Use `resolve_market_time_and_calendar` to determine the correct trading day range:

```python
resolve_market_time_and_calendar(
    time_period_unit="day",
    number_of_periods=30,
    period_relative_position="previous"
)
```

### Step 4: Analyze Flow Patterns

Perform the following analyses on the collected data:

**A. Daily Flow Assessment**
- Classify today's FII flow: significant buy (> +2000cr), significant sell (< -2000cr), or neutral
- Classify today's DII flow using the same thresholds
- Compare FII vs DII: Are they aligned or divergent?

**B. Trend Analysis (10-day rolling)**
- Count net buying days vs net selling days for both FII and DII
- Calculate cumulative 10-day net flow
- Identify if selling/buying is accelerating or decelerating (compare last 5 days vs prior 5 days)

**C. Monthly and Yearly Context**
- MTD (Month-to-Date) cumulative flow for FII and DII
- YTD (Year-to-Date) cumulative flow for FII and DII
- Compare current month's pace to previous months

**D. FII:DII Flow Ratio**
- Calculate the ratio of FII net to DII net
- Positive ratio with both positive = strong bullish signal
- FII negative, DII positive = DII absorbing FII selling (support floor)
- Both negative = danger signal

### Step 5: Identify Flow Regime

Classify the current institutional flow regime:

| Regime | Definition | Market Implication |
|--------|------------|-------------------|
| **FII Net Buyer** | FII net positive for 5+ consecutive days or MTD > +5000cr | Bullish for Nifty, INR strengthening |
| **FII Net Seller** | FII net negative for 5+ consecutive days or MTD < -5000cr | Bearish pressure, INR weakening |
| **DII Absorption** | FII selling but DII buying offsetting >70% of FII outflow | Market finds floor, limited downside |
| **Dual Buying** | Both FII and DII net buyers for 3+ days | Strong rally likely, broad-based buying |
| **Dual Selling** | Both FII and DII net sellers (rare) | Sharp correction risk, liquidity withdrawal |
| **Transition Phase** | FII switching from seller to buyer (or vice versa) within last 5 days | Trend reversal potential, watch for confirmation |

### Step 6: Correlate Flows with Nifty Movement

Analyze the relationship between institutional flows and Nifty price action:

- Map daily FII net flow to Nifty daily change (same day)
- Check if FII flows are leading Nifty (flow change precedes price change by 1-2 days)
- Identify divergences: FII selling but Nifty rising (DII support or retail buying) or FII buying but Nifty falling (other factors dominating)

Use the calculator tool for correlation computation if needed:

```python
calculator(list_of_expressions=[
    "correlation coefficient formula components"
])
```

### Step 7: Assess Sector-Level Impact

If the user requests sector-level analysis, use web search:

```
WebSearch: "FII DII sector wise investment {current_month} {current_year}"
WebSearch: "FII portfolio allocation India sectors {current_year}"
```

Key sector dynamics:
- **Banking/Financials**: Largest FII holding, most sensitive to FII flows
- **IT Services**: Benefits from INR depreciation caused by FII outflows
- **FMCG**: DII/MF favorite, relatively insulated from FII selling
- **Oil & Gas, Metals**: Driven by global commodity + FII positioning

### Step 8: Generate the Flow Report

Use the report template from `assets/flow_report_template.md` to structure the output. Fill in all sections with the analyzed data.

Present the report in a clear, structured format with:
- Summary box at the top (today's key numbers)
- Tables for historical data
- Clear trend assessment with directional language
- Actionable implications
- Appropriate disclaimer

## Key Metrics Reference

| Metric | Calculation | Significance |
|--------|-------------|-------------|
| FII Daily Net | FII Buy - FII Sell | Direction of foreign capital flow |
| DII Daily Net | DII Buy - DII Sell | Direction of domestic capital flow |
| FII MTD | Sum of FII daily net for current month | Monthly trend strength |
| FII YTD | Sum of FII daily net for current calendar year | Annual positioning |
| DII MTD | Sum of DII daily net for current month | Monthly domestic support |
| DII YTD | Sum of DII daily net for current calendar year | Annual domestic positioning |
| FII:DII Ratio | FII Net / DII Net | Institutional alignment |
| Flow-Nifty Correlation | Statistical correlation over 20 days | Predictive strength |
| Absorption Rate | DII Net / abs(FII Net) when FII selling | DII's ability to offset FII |

## Significance Thresholds

| Level | Daily (crores) | MTD (crores) | YTD (crores) |
|-------|---------------|--------------|--------------|
| Minor | < 1,000 | < 5,000 | < 25,000 |
| Moderate | 1,000 - 2,000 | 5,000 - 10,000 | 25,000 - 50,000 |
| Significant | 2,000 - 5,000 | 10,000 - 25,000 | 50,000 - 1,00,000 |
| Major | > 5,000 | > 25,000 | > 1,00,000 |

## Important Notes

- FII/DII data is typically released by exchanges after market hours (around 6-7 PM IST for provisional data, next day for final data).
- There can be discrepancies between provisional and final data; always note which version is being used.
- FII data includes all Foreign Portfolio Investors (FPIs) registered with SEBI.
- DII data includes mutual funds, insurance companies, banks, and financial institutions.
- Derivative market FII positions (available from NSE) are a leading indicator and should be consulted alongside cash market data.
- Always present flows in Indian Rupee crores (the standard unit for institutional flow reporting).
- Always include a disclaimer that institutional flow data alone should not be used as the sole basis for investment decisions.

## Reference Materials

- `references/flow_analysis_methodology.md` - Comprehensive methodology for analyzing FII/DII flows
- `references/flow_interpretation_guide.md` - Practical guide for interpreting flow signals
- `assets/flow_report_template.md` - Markdown template for generating flow reports

## Tools Used

Use whichever broker MCP is connected (Groww or Zerodha Kite):

| Action | Groww MCP | Zerodha Kite MCP | Fallback |
|--------|-----------|------------------|----------|
| Nifty LTP | `get_ltp` | `get_ltp` | yfinance |
| Historical data | `fetch_historical_candle_data` | `get_historical_data` | yfinance |
| Trading calendar | `resolve_market_time_and_calendar` | — | Web search |
| Market movers | `fetch_market_movers_and_trending_stocks_funds` | — | Web search |
| Shareholding data | `fetch_stocks_fundamental_data` | — | Web search |
| Portfolio check | `get_equity_portfolio_holdings` | `get_holdings` | — |

| Tool | Purpose |
|------|---------|
| `WebSearch` | Fetch latest FII/DII data from NSDL, NSE, MoneyControl |
| `WebFetch` | Scrape specific FII/DII data pages for structured data |
| `calculator` | Compute flow ratios, correlations, and aggregates |
