---
name: india-stock-analysis
description: Use when user requests analysis of Indian stocks, fundamental assessment, technical review, comparisons, or investment reports for NSE/BSE listed companies.
---

# India Stock Analysis Skill

Analyze Indian stocks listed on NSE and BSE using broker MCP tools and web search. All analysis is denominated in INR and follows Indian fiscal year conventions (April-March). No API keys are required.

## Data Sources

Use whichever broker MCP is connected. Both provide equivalent data for stock analysis.

### Option A: Groww MCP (if connected)
- `fetch_stocks_fundamental_data` -- Financials, ratios, shareholding, mutual fund holdings
- `fetch_historical_candle_data` -- OHLCV price history
- `get_historical_technical_indicators` -- RSI, MACD, Bollinger, SMA, EMA, SuperTrend, VWAP, ADX, and more
- `get_ltp` -- Live/last traded price and open interest
- `get_quotes_and_depth` -- Real-time bid/ask and market depth
- `curate_symbols` -- Resolve stock symbols and exchange
- `fetch_market_movers_and_trending_stocks_funds` -- Market movers, gainers, losers
- `fetch_fundamentals_screener` -- Screen stocks by fundamental criteria
- `fetch_technical_screener` -- Screen stocks by technical signals
- `search_stock_and_others_symbol` -- Search for stocks, indices, and companies
- `resolve_market_time_and_calendar` -- Current market time, trading days, holidays

### Option B: Zerodha Kite MCP (if connected)
- `get_ltp` -- Last traded price for instruments
- `get_quotes` -- Real-time market quotes with depth
- `get_ohlc` -- OHLC data for instruments
- `get_historical_data` -- Historical OHLCV candle data
- `search_instruments` -- Search and resolve trading instruments
- `get_holdings` -- User's portfolio holdings
- `get_positions` -- Current trading positions
- `get_margins` -- Account margin details
- `get_profile` -- User profile information

### Supplementary
- Web search for news, analyst reports, sector developments, and regulatory updates
- yfinance (free, no API key) as fallback for historical data

## Workflow

When a user requests stock analysis, determine which analysis type is needed and follow the corresponding workflow below. If the user does not specify, default to **Comprehensive Investment Report**.

---

### Analysis Type 1: Basic Stock Information

Use when the user asks for a quick overview, current price, or summary of a stock.

**Steps:**

1. **Resolve the symbol.** Call `curate_symbols` or `search_stock_and_others_symbol` with the company name to obtain the correct trading symbol and exchange (NSE/BSE).

2. **Fetch current price.** Call `get_ltp` with the resolved trading symbol to get the last traded price, day change, and percentage change.

3. **Fetch key fundamental stats.** Call `fetch_stocks_fundamental_data` with `view='stats_only'` and include stats: `marketCap`, `peRatio`, `pbRatio`, `roe`, `epsTtm`, `dividendYieldInPercent`, `industryPe`, `bookValue`, `debtToEquity`, `faceValue`.

4. **Fetch recent price history.** Call `fetch_historical_candle_data` for the last 1 year with daily interval (`interval_in_minutes='1440'`) to determine 52-week high/low and YTD performance.

5. **Search for recent news.** Use web search for recent news about the company (last 30 days).

6. **Present the output** in this format:

```
## [Company Name] ([Exchange]: [Symbol])

**Current Price:** Rs.[LTP] ([+/-change] / [+/-change%])
**Market Cap:** Rs.[value] Cr
**Sector:** [sector]

### Key Metrics
| Metric            | Value         |
|--------------------|---------------|
| PE Ratio           | [value]       |
| Industry PE        | [value]       |
| PB Ratio           | [value]       |
| EPS (TTM)          | Rs.[value]    |
| ROE                | [value]%      |
| Debt/Equity        | [value]       |
| Dividend Yield     | [value]%      |
| Book Value         | Rs.[value]    |
| Face Value         | Rs.[value]    |

### 52-Week Range
- **High:** Rs.[value] ([date])
- **Low:** Rs.[value] ([date])
- **Current vs High:** [x]% below 52W high

### YTD Performance
- **1 Jan to Today:** [+/-x]%

### Recent News
- [headline 1] -- [source, date]
- [headline 2] -- [source, date]
- [headline 3] -- [source, date]
```

---

### Analysis Type 2: Fundamental Analysis

Use when the user asks for fundamental analysis, business quality, financials, valuation, or investment merit.

**Steps:**

1. **Resolve the symbol** as in Analysis Type 1.

2. **Fetch full fundamental data.** Call `fetch_stocks_fundamental_data` with `view='all'` and stats: `marketCap`, `peRatio`, `pbRatio`, `roe`, `epsTtm`, `dividendYieldInPercent`, `industryPe`, `bookValue`, `debtToEquity`, `faceValue`, `returnOnAssets`, `returnOnEquity`, `operatingProfitMargin`, `netProfitMargin`, `quickRatio`, `cashRatio`, `debtToAsset`, `evToSales`, `evToEbitda`, `earningsYield`, `sectorPe`, `sectorPb`, `sectorDivYield`, `sectorRoe`, `sectorRoce`, `priceToOcf`, `priceToFcf`, `pePremiumVsSector`, `pbPremiumVsSector`, `divYieldVsSector`, `currentRatio`, `priceToSales`, `pegRatio`, `roic`. Include optional financial items `['*']` to get complete financial statements.

3. **Fetch shareholding data.** Call `fetch_stocks_fundamental_data` with `view='shareholders_and_mutual_funds'` to get promoter holding, FII/DII breakdown, pledge percentage, and top mutual fund holders.

4. **Perform web search** for analyst reports, management commentary, and sector outlook.

5. **Analyze and present** using the framework in `references/fundamental-analysis.md`:

   **a. Business Quality Assessment**
   - What does the company do? What is its competitive moat?
   - Management quality and promoter track record
   - Market position and competitive advantages
   - Corporate governance indicators

   **b. Financial Health**
   - Revenue and profit trends (3-5 year view using financial statements)
   - Margin analysis (operating, net, EBITDA)
   - Cash flow quality (operating cash flow vs reported profit)
   - Balance sheet strength (debt levels, current ratio, interest coverage)

   **c. Shareholding Pattern (India-Specific)**
   - Promoter holding percentage (>50% generally positive, <30% caution)
   - Promoter pledge percentage (>20% is a red flag, >50% is a serious concern)
   - FII holding trend (increasing = positive signal)
   - DII holding trend
   - Change in shareholding over recent quarters

   **d. Valuation**
   - PE vs Industry PE and Sector PE (premium/discount)
   - PB vs Sector PB
   - PEG ratio assessment
   - EV/EBITDA comparison
   - Earnings yield vs risk-free rate (India 10Y government bond yield ~7%)

   **e. Growth Assessment**
   - Revenue growth trajectory
   - EPS growth trend
   - Order book / pipeline visibility (if applicable)
   - Capex plans and return on invested capital

   **f. Risk Factors**
   - Company-specific risks
   - Sector/regulatory risks
   - Promoter-related risks (pledge, related party transactions)
   - Macro risks (currency, interest rates, commodity prices)

6. **Assign a fundamental score** from 1-10 based on the framework in `references/fundamental-analysis.md`.

---

### Analysis Type 3: Technical Analysis

Use when the user asks for technical analysis, chart patterns, entry/exit levels, or trading signals.

**Steps:**

1. **Resolve the symbol** as in Analysis Type 1.

2. **Determine the market time context.** Call `resolve_market_time_and_calendar` to get the current date and market status.

3. **Fetch price history.** Call `fetch_historical_candle_data` for multiple timeframes:
   - Daily candles for the last 6 months (trend analysis)
   - Weekly candles for the last 2 years (long-term trend)
   - If intraday analysis is needed: 5-minute or 15-minute candles for the last few days

4. **Fetch technical indicators.** Call `get_historical_technical_indicators` with these indicators:
   - Trend: `sma` (20, 50, 200 period), `ema` (20 period), `supertrend`
   - Momentum: `rsi` (14 period), `macd` (12, 26, 9), `stochastic`, `williams_r`, `adx`
   - Volatility: `bollinger` (20 period, 2 std), `atr`, `keltner`
   - Volume: `vwap`, `obv`, `mfi`
   - Reversal: `parabolic_sar`
   - Support/Resistance: `pivot_points`

   Note: Run multiple calls if needed for different SMA periods (20, 50, 200).

5. **Fetch candlestick patterns** (optional). Call `get_historical_candlestick_patterns` if the user asks for pattern analysis.

6. **Analyze and present:**

   **a. Trend Analysis**
   - Primary trend (weekly): uptrend / downtrend / sideways
   - Secondary trend (daily): direction and strength
   - Price position relative to key SMAs (20, 50, 200 DMA)
   - Golden cross / death cross status (50 DMA vs 200 DMA)
   - SuperTrend direction

   **b. Support and Resistance Levels**
   - Identify key support levels from pivot points, recent swing lows, and round numbers
   - Identify key resistance levels from pivot points, recent swing highs, and round numbers
   - Present as a clear table

   **c. Momentum Indicators**
   - RSI: Current value, overbought/oversold, divergences
   - MACD: Signal line crossover, histogram trend, zero-line position
   - Stochastic: %K/%D crossover, overbought/oversold zones
   - ADX: Trend strength (>25 = trending, <20 = ranging)

   **d. Volatility Assessment**
   - Bollinger Band width and position (near upper/lower/middle band)
   - ATR value and trend (expanding/contracting volatility)
   - Keltner Channel position

   **e. Volume Analysis**
   - Volume trend (increasing/decreasing with price moves)
   - OBV trend (confirming or diverging from price)
   - MFI reading (money flow)
   - VWAP position (intraday context)

   **f. Pattern Recognition** (if applicable)
   - Candlestick patterns detected
   - Chart patterns (head and shoulders, triangles, channels)
   - Significance and reliability rating

   **g. Trading Levels**
   ```
   | Level Type       | Price (Rs.) | Notes                  |
   |-------------------|-------------|------------------------|
   | Resistance 3      | [value]     | [context]              |
   | Resistance 2      | [value]     | [context]              |
   | Resistance 1      | [value]     | [context]              |
   | Current Price      | [value]     | --                     |
   | Support 1          | [value]     | [context]              |
   | Support 2          | [value]     | [context]              |
   | Support 3          | [value]     | [context]              |
   ```

   **h. Technical Outlook**
   - Short-term (1-2 weeks): bullish / bearish / neutral
   - Medium-term (1-3 months): bullish / bearish / neutral
   - Key levels to watch and potential triggers

---

### Analysis Type 4: Comprehensive Investment Report

Use when the user asks for a full report, comprehensive analysis, or investment recommendation. This is the default when no specific type is requested.

**Steps:**

1. **Execute all steps from Analysis Types 1, 2, and 3** above. Make parallel tool calls wherever possible to speed up data gathering.

2. **Perform additional research:**
   - Web search for recent analyst recommendations and target prices
   - Web search for upcoming catalysts (earnings dates, AGM, corporate actions)
   - Web search for sector/macro developments affecting the stock
   - Fetch peer comparison data using `fetch_stocks_fundamental_data` for 3-5 peers

3. **Compile the report** using the template in `assets/report-template.md`:

   **a. Executive Summary**
   - Investment recommendation: Strong Buy / Buy / Hold / Sell / Strong Sell
   - Conviction level: High / Medium / Low
   - Key thesis in 2-3 sentences

   **b. Company Overview**
   - Business description, history, and market position
   - Sector classification and listing details (NSE/BSE)
   - Market cap category (Large Cap / Mid Cap / Small Cap / Micro Cap)

   **c. Investment Thesis**
   - Bull case: 3-5 reasons to buy
   - Bear case: 3-5 reasons for caution
   - Base case scenario

   **d. Fundamental Analysis** (from Analysis Type 2)

   **e. Technical Analysis** (from Analysis Type 3)

   **f. Valuation Analysis**
   - Relative valuation vs peers (PE, PB, EV/EBITDA table)
   - Historical valuation range (PE band over 3-5 years)
   - Sector premium/discount analysis

   **g. Risk Assessment**
   - Risk matrix with probability and impact
   - Company-specific, sector, and macro risks
   - SEBI regulatory considerations if applicable

   **h. Peer Comparison**
   - Table comparing 4-6 key metrics across the company and 3-5 peers
   - Relative positioning commentary

   **i. Catalysts**
   - Near-term (0-3 months): earnings, results, corporate actions
   - Medium-term (3-12 months): expansion plans, order wins, regulatory changes
   - Long-term (1-3 years): structural growth drivers

   **j. Conclusion**
   - Summary of the investment case
   - Key monitoring parameters
   - Suggested review triggers

   **k. Disclaimer**
   - Standard investment disclaimer (this is not investment advice, for educational purposes only)

4. **Format the entire report** following the structure in `assets/report-template.md`.

---

## India-Specific Considerations

Throughout all analysis types, apply these India-specific guidelines:

- **Currency**: All prices and financial figures in INR (Rs.). Use Cr (Crore = 10 million) and L (Lakh = 100,000) as appropriate for Indian market convention.
- **Fiscal Year**: Indian companies follow April-March fiscal year. Reference as FY24 (April 2023 - March 2024), FY25, etc.
- **Market Hours**: NSE/BSE trade 9:15 AM to 3:30 PM IST, Monday to Friday (excluding market holidays).
- **Promoter Holding**: A critical India-specific metric. Interpret as follows:
  - Above 70%: Very high promoter control, could limit free float
  - 50-70%: Strong promoter confidence
  - 30-50%: Moderate, watch for changes
  - Below 30%: Low promoter stake, potential governance concern
- **Promoter Pledge**: Shares pledged by promoters as collateral for loans.
  - 0%: Best case
  - 1-10%: Acceptable
  - 10-20%: Monitor closely
  - Above 20%: Red flag
  - Above 50%: Serious concern
- **FII/DII Holdings**: Foreign and Domestic Institutional Investor holdings indicate institutional confidence.
- **Regulatory Context**: SEBI regulations, LODR compliance, insider trading norms.
- **Index Membership**: Nifty 50, Nifty Next 50, Nifty 100, Nifty 500, Nifty Midcap 100, Nifty Smallcap 100, sectoral indices.
- **Dual Listing**: Most Indian companies are listed on both NSE and BSE. NSE is typically preferred for liquidity. Use NSE data unless BSE is specifically requested.
- **Circuit Limits**: Indian exchanges have upper and lower circuit limits. Mention if relevant.
- **T+1 Settlement**: Indian markets follow T+1 settlement cycle.
- **Lot Size (F&O)**: If the stock is in the F&O segment, mention the lot size.

## Output Guidelines

- Use clear markdown formatting with tables, headers, and bullet points.
- Present numerical data in tables where possible for easy comparison.
- Bold key metrics and important observations.
- Include data timestamps so the user knows how current the data is.
- Always end reports with the standard disclaimer.
- When comparing with peers, use the same set of metrics consistently.
- Round financial ratios to 2 decimal places.
- Express large numbers in Indian convention: Cr (Crores) and L (Lakhs).
- Include percentage changes with directional indicators (up/down arrows or +/- signs).

## Error Handling

- If a broker MCP tool call fails (Groww or Zerodha), note the missing data point and proceed with available data. Try the alternative broker's equivalent tool if available. Use web search as a fallback for critical data.
- If the stock symbol cannot be resolved, ask the user to clarify the company name or provide the NSE/BSE symbol directly.
- If the company is not listed on Indian exchanges, inform the user that this skill is designed for NSE/BSE listed companies.
- If historical data is limited (e.g., recently listed IPO), adjust the analysis timeframes accordingly and note the limitation.
