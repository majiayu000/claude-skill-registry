---
name: analyzing-yield-curves
description: Interprets yield curve shapes with term structure analysis and relative value identification. Use when analyzing yield curves, identifying curve trades, or interpreting interest rate expectations.
tags:
  - analysis
  - fixed-income
metadata:
  author: casemark
  practice_areas:
    - Fixed Income
    - Credit Research
    - Bond Trading
  document_types:
    - Analysis Report
  skill_modes:
    - Analysis
---
# Analyzing Yield Curves

## When To Use

- Interpreting the current shape of a government or credit yield curve (normal, flat, inverted, humped)
- Identifying relative value opportunities across maturities for curve trades (steepeners, flatteners, butterflies)
- Extracting market-implied expectations for future interest rates, inflation, or recession probability
- Comparing curves across issuers, sectors, or sovereigns to assess credit term structure
- Supporting portfolio duration and key-rate duration positioning decisions

## Inputs To Gather

- **Curve data**: Par yields, zero-coupon (spot) rates, or forward rates for the relevant curve (e.g., UST, OIS/SOFR, EUR swap, issuer-specific)
- **Tenor points**: At minimum 2Y, 5Y, 10Y, 30Y; include 3M, 6M, 1Y for short-end analysis and money-market signal extraction
- **As-of date and source**: Bloomberg, FRED, ICE, or broker runs — note any interpolation or bootstrap methodology used
- **Historical comparison dates**: Prior curve snapshots for slope change analysis (e.g., 1 week, 1 month, 6 months ago)
- **Benchmark reference**: Identify the risk-free curve and any spread curves needed (e.g., IG OAS curve, HY spread curve, sovereign spread vs. Bunds)
- **Context**: Current Fed/ECB/BoJ policy rate, dot plot or forward guidance, recent CPI/PCE prints, and upcoming auction calendar

## Workflow

1. **Classify curve shape**
   - Determine current regime: normal (positive slope), flat, inverted, or humped
   - Compute key slope measures: 2s10s spread, 2s5s, 5s30s, 3m10s
   - Compare current slopes to 1-year and 5-year percentile ranks to gauge how extreme the shape is

2. **Decompose term structure**
   - Bootstrap spot rates from par curve if only par yields are provided
   - Derive implied forward rates (e.g., 1y1y, 2y3y, 5y5y) to read market expectations for future short rates
   - Separate the yield into components: expected path of short rates + term premium (use ACM, KW, or similar model estimates where available) [VERIFY: model source and vintage]

3. **Identify relative value signals**
   - Compute Z-scores of spreads between tenor pairs vs. rolling historical windows (60-day, 250-day)
   - Flag butterfly richness/cheapness: belly vs. wings (e.g., 2s5s10s, 5s10s30s)
   - Identify roll-down advantage by comparing yield pickup from 6-month or 12-month roll along the curve
   - Note on-the-run vs. off-the-run spread anomalies for liquidity-driven dislocations

4. **Assess macro and policy implications**
   - Compare implied forward rates to central bank dot plots or OIS-implied policy path [VERIFY: confirm latest meeting date and statement]
   - Evaluate inversion signals: 3m10s inversion duration as recession indicator (historical lead time ~12–18 months)
   - Cross-reference breakeven inflation curve (nominal minus TIPS) for real rate vs. inflation expectations decomposition
   - Flag divergences between swap curve and government curve that signal credit or liquidity stress

5. **Formulate curve trade ideas**
   - Map findings to actionable trade structures: outright duration, steepener/flattener (2s10s, 5s30s), butterfly, or barbell vs. bullet
   - Specify DV01-weighted or regression-weighted hedge ratios
   - Estimate carry and roll-down P&L over a defined horizon (e.g., 3 months, assuming no rate change)
   - State key risks: parallel shift exposure, convexity, funding cost, and event risk (auction, payroll, FOMC)

## Output

- **Curve snapshot table**: Tenors, par yields, spot rates, implied forwards, and changes vs. prior dates
- **Shape classification**: Current regime label with slope measures and percentile context
- **Relative value heatmap**: Tenor-pair Z-scores and butterfly spreads flagged as rich/cheap
- **Macro signal summary**: Forward rate vs. policy path comparison, inversion status, term premium estimate
- **Trade recommendations**: 1–3 curve trade ideas with entry rationale, hedge ratios, carry/roll estimate, and risk factors
- **Charts** (if supported): Curve overlay (current vs. prior), slope time series, forward rate vs. dot plot

## Quality Checks

- Confirm all yield data is from the same close date and quote convention (mid, bid, ask) — mixing sources distorts slope readings
- Verify spot and forward rate derivations are internally consistent (forwards should re-price par curve)
- Ensure Z-scores use an appropriate lookback window; regime changes can make long-history Z-scores misleading
- Cross-check that DV01-neutral ratios account for actual durations at current yield levels, not approximations
- Flag any tenors with thin liquidity or wide bid-ask spreads that could distort relative value signals [VERIFY: check for off-the-run or illiquid points]
- Mark all recession probability estimates and term premium figures with model source and date [VERIFY]
- Do not present curve-implied rate expectations as forecasts — they embed risk premia and positioning effects
