---
name: screen
description: Run quantitative or thematic stock screens to surface investment ideas. Supports AR (BYMA, CEDEARs) and US markets. Triggers on "screen", "stock screen", "find stocks", "investment ideas", "what looks interesting".
---

# Stock Screener

Surface investment ideas via quantitative screens or thematic sweeps.

## Step 1: Define Screen

If user provides criteria, use them. Otherwise ask:
- **Market:** AR (BYMA panel general/lider, CEDEARs) / US / Both
- **Direction:** Long / Short / Both
- **Style:** Value / Growth / Momentum / Income / Quality
- **Sector/Theme:** (optional) specific sector or thematic filter
- **Size:** Large / Mid / Small / Any
- **Constraints:** (optional) liquidity minimums, max P/E, min dividend, etc.

## Step 2: Quantitative Screen

Apply filters based on style:

**Value:** P/E < sector median, P/B < 1.5, EV/EBITDA below peers, FCF yield > 5%
**Growth:** Revenue growth > 15% YoY, EPS growth > 20%, expanding margins
**Momentum:** Price > 50-day MA > 200-day MA, RSI 50-70, positive earnings revisions
**Income:** Dividend yield > 3%, payout ratio < 70%, dividend growth > 5% CAGR
**Quality:** ROE > 15%, debt/equity < 1.0, consistent earnings (no losses in 5yr)

**AR-specific filters:**
- CEDEARs: check premium/discount vs ADR parity — flag opportunities where discount > 5%
- BYMA local: volume filter (>$1M ARS daily), exclude penny stocks
- Bonds: TIR vs inflation expectations, duration bucket, credit quality

## Step 3: Results Table

| # | Ticker | Name | Market | Price | Key Metric 1 | Key Metric 2 | Key Metric 3 | Signal |
|---|--------|------|--------|-------|-------------|-------------|-------------|--------|
| | | | | | | | | |

## Step 4: Quick Thesis for Top 3-5

For each top idea, provide:
- **Why it passes:** 2-3 sentences on what the screen caught
- **Bull case:** best scenario in 1 sentence
- **Bear case:** worst scenario in 1 sentence
- **Catalyst:** what could move it in next 3-6 months
- **Risk:** primary risk factor

## Step 5: Output

```
═══ SCREEN: [criteria summary] ═══
Market: [AR/US/Both]
Style: [value/growth/momentum/income/quality]
Results: [N] names passed filters
Date: [today]

[Results table]

TOP IDEAS:
1. [TICKER] — [one-liner thesis]
2. [TICKER] — [one-liner thesis]
3. [TICKER] — [one-liner thesis]
```

## Notes

- ALWAYS use current market data — never training data prices
- For AR screens, note if market was open/closed and last trading date
- CEDEARs: always show both CEDEAR price (ARS) and underlying price (USD) with CCL
- Screens are idea generators, not buy recommendations — each needs full thesis development
- If using Cotiza API for AR data, note the data source
