---
name: catalyst-tracker
description: Build a catalyst list and event calendar for an asset.
metadata:
  {
    "marketbot": {
      "emoji": "calendar"
    }
  }
---

# Catalyst Tracker

Compile relevant catalysts and events for a given asset and timeframe.

## When to use
- User asks for "catalysts", "upcoming events", or "news drivers".
- You need context before making a directional call.

## Inputs to confirm (ask if missing)
- Asset + market
- Time horizon (days/weeks/months)
- Geographic focus (if macro-sensitive)

## Process
1. List known catalyst categories for the market type.
2. If web search is available, pull the latest events/news for the asset.
3. Separate confirmed events vs speculative risks.
4. Provide dates (or "TBD") and expected impact direction/volatility.

## Output format (markdown)
```
# Catalyst Tracker: <ASSET>

## Upcoming (Confirmed)
- <date>: <event> — expected impact: low/medium/high

## Recent (Last 7-30 days)
- <date>: <event> — market reaction summary

## Macro/Industry Watchlist
- <event>: why it matters

## Data Gaps
- Missing sources or unverified events

> Disclaimer: MarketBot provides research/analysis only. Not financial advice.
```
