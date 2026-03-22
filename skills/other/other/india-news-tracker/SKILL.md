---
name: india-news-tracker
description: Track and analyze Indian stock market news, corporate announcements, SEBI circulars, bulk/block deals, and earnings calendars. Auto-fetches headlines from MoneyControl, Economic Times, LiveMint, BSE/NSE filings. Use when the user asks about recent news, corporate actions, upcoming events, or wants a daily market news briefing for NSE/BSE.
---

# India News Tracker

## Overview

This skill fetches, categorizes, scores, and summarizes Indian market news from multiple sources. It tracks corporate announcements, SEBI circulars, bulk/block deals, insider trades, earnings calendars, and breaking market news — then feeds actionable insights to the user or other skills (like Scenario Analyzer).

## Architecture

```
Skill (Orchestrator)
├── Phase 1: News Collection
│   ├── Web search across Indian financial media
│   ├── BSE/NSE corporate filings
│   ├── Regulatory circulars (SEBI, RBI)
│   └── Bulk/block deal data
├── Phase 2: Processing
│   ├── Categorize by event type
│   ├── Score market impact (1-10)
│   ├── Tag affected sectors and stocks
│   └── Detect sentiment (bullish/bearish/neutral)
├── Phase 3: Analysis
│   ├── Identify top movers from news
│   ├── Cross-reference with price action (via broker MCP)
│   ├── Flag earnings surprises and guidance changes
│   └── Detect theme clusters
└── Phase 4: Report
    ├── Daily briefing format
    ├── Stock-specific news digest
    ├── Sector news roundup
    └── Actionable alerts
```

## News Source Priority

Use web search to fetch news from these sources, in order of reliability:

### Tier 1 — Official / Regulatory (Highest Priority)
| Source | What to Fetch | Search Query Pattern |
|--------|--------------|---------------------|
| **BSE India** (bseindia.com) | Corporate announcements, board meeting outcomes, results | `site:bseindia.com [company] announcement` |
| **NSE India** (nseindia.com) | Bulk deals, block deals, insider trades, F&O ban list | `site:nseindia.com [topic]` |
| **SEBI** (sebi.gov.in) | Circulars, new regulations, enforcement orders | `site:sebi.gov.in circular 2026` |
| **RBI** (rbi.org.in) | Monetary policy, banking regulations, forex data | `site:rbi.org.in [topic]` |

### Tier 2 — Financial Media (Primary News)
| Source | Strength | Search Query Pattern |
|--------|----------|---------------------|
| **MoneyControl** | Fastest Indian market news, earnings analysis | `site:moneycontrol.com [topic]` |
| **Economic Times Markets** | Corporate news, policy analysis | `site:economictimes.indiatimes.com markets [topic]` |
| **LiveMint** | Policy, macro, premium analysis | `site:livemint.com [topic]` |
| **Business Standard** | In-depth corporate and policy coverage | `site:business-standard.com [topic]` |

### Tier 3 — Supplementary
| Source | Strength | Search Query Pattern |
|--------|----------|---------------------|
| **NDTV Profit** | Quick market updates | `site:ndtvprofit.com [topic]` |
| **Trendlyne** | Technicals, bulk deals, DII/FII data | `site:trendlyne.com [topic]` |
| **Screener.in** | Financials, results calendar | `site:screener.in [topic]` |
| **Tijori Finance** | Earnings summaries, sector data | `site:tijorifinance.com [topic]` |

### Tier 4 — Social / Real-time Sentiment
| Source | Strength | Search Query Pattern |
|--------|----------|---------------------|
| **X/Twitter** | Breaking news, market sentiment | `site:x.com [topic] NSE OR BSE` |
| **Reddit (ISB)** | Retail sentiment, trading ideas | `site:reddit.com/r/IndianStreetBets [topic]` |

## Broker MCP Integration

Use broker MCP tools to cross-reference news with live market data:

### Groww MCP (if connected)
- `fetch_market_movers_and_trending_stocks_funds` with `STOCKS_IN_NEWS` — stocks currently in news
- `get_ltp` — check price reaction to news
- `fetch_historical_candle_data` — verify price movement post-announcement
- `fetch_stocks_fundamental_data` — earnings data to compare with announced results
- `fetch_market_movers_and_trending_stocks_funds` with `VOLUME_SHOCKERS` — abnormal volume (often news-driven)
- `resolve_market_time_and_calendar` — trading day context

### Zerodha Kite MCP (if connected)
- `get_ltp` — last traded price for news impact verification
- `get_quotes` — real-time quotes with depth
- `get_historical_data` — price history for post-news analysis
- `search_instruments` — resolve company names to trading symbols

### No Broker Available
- Use web search for all data (MoneyControl, Google Finance for prices)
- yfinance as fallback for historical price data

## Workflow

### Mode 1: Daily Market Briefing

Trigger: "What's the market news today?", "Daily briefing", "Morning update", "What happened in markets today?"

**Steps:**

1. **Determine market context**
   - Call `resolve_market_time_and_calendar` to get current date and market status
   - If market is closed, note it and provide previous day's wrap + upcoming catalysts

2. **Fetch top market news** (run searches in parallel)
   ```
   WebSearch: "Indian stock market news today [date]"
   WebSearch: "NSE BSE market update today [date]"
   WebSearch: "site:moneycontrol.com market news today"
   WebSearch: "site:economictimes.indiatimes.com stock market today"
   ```

3. **Fetch stocks in news** (if broker MCP available)
   ```
   Groww: fetch_market_movers_and_trending_stocks_funds(["STOCKS_IN_NEWS"])
   Groww: fetch_market_movers_and_trending_stocks_funds(["VOLUME_SHOCKERS"])
   Groww: fetch_market_movers_and_trending_stocks_funds(["TOP_GAINERS", "TOP_LOSERS"])
   ```

4. **Fetch regulatory updates**
   ```
   WebSearch: "SEBI circular [current month] [year]"
   WebSearch: "RBI announcement today [date]"
   ```

5. **Fetch corporate actions**
   ```
   WebSearch: "corporate actions NSE [date] ex-date dividend bonus split"
   WebSearch: "board meeting results today NSE BSE"
   ```

6. **Categorize each news item** using the Event Classification table below

7. **Score market impact** for each news item (1-10 scale, see Scoring Framework)

8. **Cross-reference with price action**
   - For top 5-10 news items, check stock price movement using `get_ltp`
   - Flag significant gaps or volume spikes matching news

9. **Generate Daily Briefing** using `assets/daily_briefing_template.md`

---

### Mode 2: Stock-Specific News

Trigger: "News about Reliance", "What's happening with TCS?", "Any announcements from HDFC Bank?"

**Steps:**

1. **Resolve the company symbol**
   - Use `curate_symbols` or `search_instruments` to get the correct trading symbol

2. **Fetch company-specific news** (parallel searches)
   ```
   WebSearch: "[company name] stock news [current month] [year]"
   WebSearch: "site:moneycontrol.com [company name] [year]"
   WebSearch: "site:bseindia.com [company name] announcement"
   WebSearch: "[company name] quarterly results [year]"
   WebSearch: "[company name] corporate action dividend bonus split"
   ```

3. **Fetch fundamental context**
   ```
   Groww: fetch_stocks_fundamental_data(company, view='stats_only')
   Groww: get_ltp([company])
   ```

4. **Check for recent price impact**
   ```
   Groww: fetch_historical_candle_data(symbol, last 30 days, daily)
   ```

5. **Compile and present** categorized news with impact scores

6. **Highlight actionable items:**
   - Upcoming earnings dates
   - Pending corporate actions (ex-dates)
   - Regulatory changes affecting the company
   - Management changes or M&A activity
   - Insider trading activity

---

### Mode 3: Sector News Roundup

Trigger: "What's happening in banking sector?", "IT sector news", "Pharma sector update"

**Steps:**

1. **Map sector to NSE sectoral index and constituent stocks**
   - See `references/sector_mapping.md` for sector → index → stocks mapping

2. **Fetch sector-specific news** (parallel searches)
   ```
   WebSearch: "[sector] sector India stock market [current month] [year]"
   WebSearch: "site:moneycontrol.com [sector] sector India"
   WebSearch: "[sector] policy regulation India [year]"
   ```

3. **Fetch sector movers** (if Groww MCP connected)
   ```
   Groww: fetch_market_movers_and_trending_stocks_funds(sector-specific filters)
   Groww: fetch_technical_screener(sector filter)
   ```

4. **Identify sector themes:**
   - Policy/regulatory changes (e.g., banking NPA norms, pharma FDA)
   - Earnings trend across sector
   - FII/DII sector rotation signals
   - Commodity input cost changes

5. **Present sector roundup** with:
   - Top 3-5 sector headlines
   - Sector index performance
   - Notable stock moves within sector
   - Upcoming sector catalysts

---

### Mode 4: Earnings Tracker

Trigger: "Upcoming earnings", "Results calendar", "Who's reporting this week?", "How were [company] results?"

**Steps:**

1. **Fetch earnings calendar**
   ```
   WebSearch: "NSE BSE quarterly results schedule [current month] [year]"
   WebSearch: "site:trendlyne.com earnings calendar"
   WebSearch: "board meeting intimate NSE [date range]"
   ```

2. **For upcoming earnings**, present:
   ```
   | Company | Date | Quarter | Analyst Estimate | Previous Quarter |
   ```

3. **For reported earnings**, fetch and analyze:
   ```
   WebSearch: "[company] quarterly results Q[x] FY[xx]"
   Groww: fetch_stocks_fundamental_data(company, view='financials_only')
   ```

4. **Earnings analysis includes:**
   - Revenue vs estimate (beat/miss/inline)
   - PAT vs estimate
   - Margin expansion/compression
   - Management guidance highlights
   - YoY and QoQ growth rates
   - Stock price reaction post-results

---

### Mode 5: Corporate Actions Tracker

Trigger: "Upcoming dividends", "Stock splits this month", "Bonus shares", "Corporate actions"

**Steps:**

1. **Fetch corporate actions calendar**
   ```
   WebSearch: "NSE corporate actions [current month] [year] ex-date"
   WebSearch: "upcoming dividend ex-date NSE [month] [year]"
   WebSearch: "stock split bonus issue NSE BSE [year]"
   ```

2. **Present corporate actions** organized by type:

   **Dividends:**
   ```
   | Company | Type | Amount (Rs.) | Ex-Date | Record Date |
   ```

   **Bonus Issues:**
   ```
   | Company | Ratio | Ex-Date | Record Date |
   ```

   **Stock Splits:**
   ```
   | Company | From FV | To FV | Ex-Date |
   ```

   **Rights Issues:**
   ```
   | Company | Ratio | Price (Rs.) | Open Date | Close Date |
   ```

---

### Mode 6: Bulk/Block Deal Monitor

Trigger: "Bulk deals today", "Block deals", "Who's buying/selling large quantities?"

**Steps:**

1. **Fetch bulk/block deal data**
   ```
   WebSearch: "NSE bulk deals today [date]"
   WebSearch: "BSE block deals today [date]"
   WebSearch: "site:nseindia.com bulk deals"
   WebSearch: "site:trendlyne.com bulk deals"
   ```

2. **Analyze and present:**
   ```
   | Stock | Deal Type | Buyer/Seller | Quantity | Price (Rs.) | % of Equity |
   ```

3. **Flag significant deals:**
   - Promoter buying/selling
   - FII/DII bulk transactions
   - PE fund entries/exits
   - Deals > 1% of equity

---

### Mode 7: Regulatory & Policy Monitor

Trigger: "SEBI updates", "RBI policy impact", "New regulations", "Policy changes"

**Steps:**

1. **Fetch regulatory updates**
   ```
   WebSearch: "SEBI circular [current month] [year] new regulation"
   WebSearch: "RBI monetary policy [current month] [year]"
   WebSearch: "India financial regulation change [year]"
   ```

2. **Categorize by impact:**
   - **Market-wide**: F&O margin changes, STT changes, settlement cycle changes
   - **Sector-specific**: Banking NPA norms, insurance regulations, telecom spectrum
   - **Company-specific**: SEBI enforcement, listing requirements

3. **Assess impact and affected stocks/sectors**

---

## Event Classification

Categorize every news item into one of these categories:

| Category | Examples | Typical Impact |
|----------|----------|---------------|
| **Earnings** | Quarterly results, annual results, earnings surprise | High (on specific stock) |
| **Corporate Action** | Dividend, bonus, split, buyback, rights issue | Medium (on specific stock) |
| **M&A** | Merger, acquisition, demerger, stake sale | High (on involved companies) |
| **Management** | CEO change, board reshuffle, key hire/exit | Medium |
| **Regulatory** | SEBI order, RBI circular, govt policy | Medium-High (sector-wide) |
| **Institutional** | FII/DII flow data, bulk/block deals, MF holdings | Medium |
| **Sector** | Industry trend, commodity price, global peer news | Medium |
| **Macro** | GDP data, inflation, IIP, PMI, trade deficit | Medium-High (market-wide) |
| **Global** | Fed decision, US markets, crude oil, China data | Medium-High |
| **IPO** | New filing, listing, subscription data | Medium (on IPO stock) |
| **Legal** | Court order, NCLT, arbitration, penalty | Variable |
| **Rating** | Analyst upgrade/downgrade, target price change | Medium |
| **Insider** | Promoter buy/sell, SAST disclosure, pledge change | Medium-High |
| **ESG** | Environmental violation, governance issue, social impact | Low-Medium |

## Impact Scoring Framework

Score each news item on a 1-10 scale:

| Score | Label | Criteria | Example |
|-------|-------|----------|---------|
| **9-10** | Critical | Market-wide impact, will move indices | RBI emergency rate cut, SEBI bans F&O |
| **7-8** | High | Sector-wide or large-cap stock impact | Major M&A, earnings shock on Nifty 50 stock |
| **5-6** | Medium | Significant for specific stocks | Mid-cap earnings beat, analyst upgrade |
| **3-4** | Low | Limited impact, FYI value | Minor corporate action, routine filing |
| **1-2** | Noise | Background info, no trading signal | Industry conference, routine compliance |

**Scoring Adjustments:**
- +1 if the stock is in Nifty 50 or Bank Nifty
- +1 if unexpected (vs market expectations)
- +1 if involves promoter/insider activity
- -1 if already priced in (market didn't react)
- -1 if from low-reliability source

## Sentiment Classification

For each news item, classify sentiment:

| Sentiment | Signal | Indicators |
|-----------|--------|------------|
| **Bullish** | 🟢 | Earnings beat, upgrade, promoter buying, positive guidance, policy tailwind |
| **Bearish** | 🔴 | Earnings miss, downgrade, promoter selling/pledging, negative guidance, regulatory action |
| **Neutral** | 🟡 | In-line results, routine filing, mixed signals |
| **Ambiguous** | ⚪ | Complex event requiring analysis (e.g., M&A — good for buyer or target?) |

## Integration with Other Skills

This skill is designed to feed actionable news into other skills:

| News Type | Feed To | How |
|-----------|---------|-----|
| Major headline / policy event | **Scenario Analyzer** | "Analyze: [headline]" → 3 scenarios |
| Stock earnings / corporate action | **India Stock Analysis** | "Analyze [stock] in context of [news]" |
| Sector rotation signals | **India Market Breadth** | Check if breadth confirms sector narrative |
| FII/DII bulk deal activity | **FII/DII Flow Tracker** | "What are institutional flows telling us about [sector]?" |
| F&O regulatory change | **Options Strategy Advisor** | Check strategy impact of rule change |
| Breakout candidate in news | **NSE VCP Screener** | Verify if news stock has VCP setup |

## Output Guidelines

- **Recency**: Always show the most recent news first
- **Source attribution**: Every news item must cite the source
- **Timestamp**: Include date and time for each item
- **Currency**: All amounts in INR (Rs., Cr, L)
- **Fiscal year**: Use Indian FY convention (FY25 = April 2024 - March 2025)
- **Trading symbol**: Always include NSE symbol alongside company name
- **Market hours context**: Note if news came pre-market, during market, or post-market (affects price impact timing)
- **Sentiment icon**: Use 🟢/🔴/🟡/⚪ for quick visual scanning
- **Impact score**: Show [1-10] score for each significant item

## Quality Standards

- Never present news older than requested timeframe without flagging it
- Cross-reference breaking news across at least 2 sources before treating as confirmed
- Distinguish between "rumor/report" and "confirmed announcement"
- Flag if a news source has known bias or is promotional content
- Include "price reaction" data when available — news without market reaction context is incomplete
- Always note the market status (open/closed) when presenting news, as impact timing differs

## Error Handling

- If web search returns no results for a specific source, move to next source in priority
- If broker MCP is unavailable, proceed with web-only data
- If a company cannot be resolved, ask user to clarify
- If market is closed, note the timing context and present previous session's news
- Always provide at least a basic briefing even if some sources fail

## Example Usage

```
User: "Market news today"

News Tracker:
1. Fetches date context → Thursday, March 12, 2026, market open
2. Parallel web searches across MoneyControl, ET, LiveMint
3. Fetches STOCKS_IN_NEWS via Groww MCP
4. Fetches VOLUME_SHOCKERS for unusual activity
5. Categorizes 15-20 news items
6. Scores each item (1-10)
7. Cross-references top items with LTP for price reaction
8. Generates daily briefing with:
   - Market overview (Nifty, Sensex, Bank Nifty)
   - Top 5 stories with impact scores
   - Stocks in focus (with price change)
   - Upcoming events (earnings, corporate actions)
   - Regulatory updates
   - Global cues for tomorrow
```

## Resources

### references/news_source_guide.md
Detailed guide on Indian financial news sources, their strengths, biases, and optimal search patterns.

### references/sector_mapping.md
Mapping of NSE sectors to indices, constituent stocks, and relevant news categories.

### references/sentiment_patterns.md
Historical patterns of how Indian markets react to different news categories, with lag analysis.

### assets/daily_briefing_template.md
Template for the daily market briefing output format.
