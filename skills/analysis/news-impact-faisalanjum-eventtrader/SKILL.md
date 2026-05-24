---
name: news-impact
description: Identify what drives stock price moves with drivers, confidence, and returns
argument-hint: TICKER START_DATE END_DATE [THRESHOLD] [--no-perplexity]
context: fork
allowed-tools:
  - Skill
  - mcp__neo4j-cypher__read_neo4j_cypher
  - WebSearch
  - mcp__perplexity__perplexity_search
  - mcp__perplexity__perplexity_research
---

# News Impact

Identify what drives stock price moves with maximum accuracy, comprehensiveness, and confidence.

## Arguments

**Received:** $ARGUMENTS

Parse as: `TICKER START_DATE END_DATE [THRESHOLD] [--no-perplexity]`

- THRESHOLD: `3s` (default), `1.5s`, `2s`, or fixed percent
- `--no-perplexity`: Skip Perplexity for gap days (faster)

**If no arguments received, ask user for TICKER, START_DATE, END_DATE.**

## Flow

### Step 0: Validate Data Availability (REQUIRED FIRST)

**CRITICAL: Run this query BEFORE any other step. STOP if validation fails.**

```cypher
MATCH (c:Company {ticker: $ticker})
OPTIONAL MATCH (d:Date)-[r:HAS_PRICE]->(c)
WITH c, max(d.date) AS latest_date, min(d.date) AS earliest_date, count(r) AS price_count
RETURN c.name AS company_name,
       latest_date,
       earliest_date,
       price_count,
       CASE WHEN latest_date >= date($start) THEN true ELSE false END AS has_start_data,
       CASE WHEN latest_date >= date($end) THEN true ELSE false END AS has_end_data
```

**Validation Rules:**
1. If `company_name` is null → **STOP**: `ERROR: Ticker {ticker} not found in database`
2. If `price_count` = 0 → **STOP**: `ERROR: No price data for {ticker}`
3. If `has_start_data` = false → **STOP**: `ERROR: No price data for {ticker} in requested range. Latest available: {latest_date}`
4. If `has_end_data` = false → **WARN** but continue: `WARNING: Data only available through {latest_date}, analysis will end there`

**DO NOT proceed to Step 1 if validation fails. DO NOT fall back to web search for missing price data.**

### Step 1: Get Benzinga News

Call `/get-bz-news $ARGUMENTS`

Returns news where |daily_adj| >= threshold (default 1.5σ) with:
- `volatility`: trailing adjusted volatility used
- `z_score`: how many sigmas this move was

If `INSUFFICIENT_HISTORY` returned, fall back to fixed 3% threshold.

### Step 2: Analyze Each News Item

For each news item from Step 1:

1. **Read title AND body** - titles can be vague
2. **Check market_session** for timing context:
   - `pre_market`: News likely CAUSED the day's move → HIGH confidence
   - `in_market`: News aligns with intraday action → MEDIUM-HIGH confidence
   - `post_market`: News EXPLAINS today's move, but **impacts NEXT trading day** → MEDIUM confidence (reactive)

   **Note:** Post-market news (earnings, guidance) will move the stock at next market open. Associate post_market news with the NEXT day's return.
3. **Generate driver phrase** (5-15 words explaining why stock moved)
4. **Assess confidence** (0-100%) based on:
   - How clearly news explains the move direction
   - Timing alignment (pre-market earnings → high; post-market commentary → lower)
   - Z-score magnitude (higher z-score + clear news = higher confidence)

### Step 3: Find Gap Days

Query daily returns to find big moves without news coverage.

First, get the volatility (or use the one from Step 1):
```cypher
MATCH (d:Date)-[r:HAS_PRICE]->(c:Company {ticker: $ticker})
WHERE d.date >= date($start) - duration('P365D') AND d.date < date($start)
MATCH (d)-[m:HAS_PRICE]->(idx:MarketIndex {ticker: 'SPY'})
WHERE r.daily_return IS NOT NULL AND m.daily_return IS NOT NULL
WITH stdev(r.daily_return - m.daily_return) AS adj_vol
RETURN adj_vol
```

Then find all significant move days:
```cypher
MATCH (d:Date)-[r:HAS_PRICE]->(c:Company {ticker: $ticker})
WHERE d.date >= date($start) - duration('P365D') AND d.date < date($start)
MATCH (d)-[m:HAS_PRICE]->(idx:MarketIndex {ticker: 'SPY'})
WHERE r.daily_return IS NOT NULL AND m.daily_return IS NOT NULL
WITH c, stdev(r.daily_return - m.daily_return) AS adj_vol

MATCH (d2:Date)-[r2:HAS_PRICE]->(c)
WHERE d2.date >= $start AND d2.date < $end
MATCH (d2)-[m2:HAS_PRICE]->(idx:MarketIndex {ticker: 'SPY'})
WITH d2.date AS date,
     r2.daily_return AS stock,
     m2.daily_return AS macro,
     (r2.daily_return - m2.daily_return) AS daily_adj,
     adj_vol
WHERE abs(daily_adj) >= $multiplier * adj_vol
RETURN date, stock, macro, daily_adj, adj_vol,
       abs(daily_adj) / adj_vol AS z_score
ORDER BY date
```

Compare with news dates from Step 1. **Gap = date with big move but no news.**

### Step 4: Research Gaps (WebSearch → Perplexity)

**Skip this step if `--no-perplexity` flag is set.** Just list gaps as UNKNOWN with confidence=0.

Otherwise, for each gap day:

**4a. WebSearch first** (faster, multi-source validation):
1. Search: "{ticker} stock news {date}" or "{company name} {date} move"
2. Look for **2+ independent sources** corroborating the same explanation
3. If 2+ sources agree → accept with confidence based on source quality:
   - 3+ sources: 70-85% confidence
   - 2 sources: 50-70% confidence
4. If <2 sources found → escalate to Perplexity

**4b. Perplexity fallback** (if WebSearch insufficient):
1. `perplexity_search` - "{ticker} stock news {date}"
2. `perplexity_research` - only for major moves (>5%) with no results

Generate driver and confidence from research. Include z-score context.

### Step 5: Merge and Return

Combine news (Step 2) + gaps (Step 4), sort by date ASC.

## Output Format

Pipe-delimited, one per line:

```
date|news_id|driver|confidence|daily_stock|daily_adj|sector_adj|industry_adj|z_score|volatility|market_session|source
```

| Field | Description |
|-------|-------------|
| date | Event timestamp |
| news_id | Neo4j ID or URL(s) for external research |
| driver | Short phrase (5-15 words) explaining move |
| confidence | 0-100% certainty |
| daily_stock | Raw daily return |
| daily_adj | daily_stock - daily_macro (vs SPY) |
| sector_adj | daily_stock - daily_sector (idiosyncratic vs sector) |
| industry_adj | daily_stock - daily_industry (idiosyncratic vs industry) |
| z_score | How many sigmas (e.g., 2.1) |
| volatility | Trailing adjusted vol used |
| market_session | pre_market / in_market / post_market (empty for perplexity) |
| source | neo4j, websearch, or perplexity |

**Move Type Interpretation:**
- If |daily_adj| >> |sector_adj| → Sector-driven (not company-specific)
- If |sector_adj| ≈ |industry_adj| ≈ |daily_adj| → Idiosyncratic (company-specific)
- If all small but daily_stock large → Market beta

## Rules

- All adjusted returns and volatility calculated in Cypher, NOT by LLM
- **WebSearch first** for gap days — validate with 2+ sources before accepting
- **Perplexity fallback** only if WebSearch finds <2 sources
- Always read news body, not just title, for accurate driver extraction
- Use market_session timing to assess causation vs explanation
- Post-market news impacts NEXT trading day, not current day
- If no explanation found, driver = "UNKNOWN", confidence = 0
- Default threshold: 1.5σ of trailing adjusted returns
- Minimum 60 days history required; fall back to 3% if insufficient

**CRITICAL - Date Range Enforcement:**
- **ONLY return results for dates within the requested START_DATE to END_DATE range**
- If no significant moves found in the range, return: `NO_SIGNIFICANT_MOVES: No moves exceeding {threshold} found for {ticker} between {start} and {end}`
- **NEVER substitute other dates** - do not search for or return data from outside the requested range
- **NEVER compensate** for empty results by finding "interesting" moves from other periods
