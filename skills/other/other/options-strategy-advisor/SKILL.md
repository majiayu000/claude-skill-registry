---
name: options-strategy-advisor
description: >
  Options strategy analysis for Indian F&O markets (NSE). Use when user requests
  options strategy recommendations, P/L analysis, Greeks calculation, risk management,
  or F&O strategy planning for Nifty, Bank Nifty, or stock options.
---

# Options Strategy Advisor — Indian F&O Markets (NSE)

## Overview

This skill provides comprehensive options strategy analysis tailored to the Indian
Futures & Options market on the National Stock Exchange (NSE). It covers strategy
selection, live data retrieval, margin estimation, profit/loss simulation, Greeks
analysis, and risk management — all adapted for the specific characteristics of
Indian F&O trading.

---

## Indian F&O Market Characteristics

### Exercise Style
- **European-style exercise only.** Options on NSE can only be exercised at expiry,
  not before. This simplifies pricing (Black-Scholes applies directly without
  early-exercise adjustments) and means time value is always fully captured by
  the seller until expiry.

### Expiry Schedule
| Underlying   | Expiry Day  | Expiry Type          |
|--------------|-------------|----------------------|
| NIFTY        | Thursday    | Weekly + Monthly     |
| BANK NIFTY   | Wednesday   | Weekly + Monthly     |
| FINNIFTY     | Tuesday     | Weekly + Monthly     |
| SENSEX (BSE) | Friday      | Weekly + Monthly     |
| Stock Options | Last Thursday | Monthly only       |

- Monthly expiry is the last Thursday of the month (or preceding trading day if
  Thursday is a holiday).
- Weekly expiries are available only for index options, not individual stocks.

### Lot Sizes
Lot sizes are periodically revised by the exchanges. Always verify current lot
sizes using the Groww MCP tool `fno_mcx_contracts_search_tool` before calculating
margin or position size. Recent reference values:
- NIFTY: 75 (recently changed — confirm via MCP)
- BANK NIFTY: 15 (recently changed — confirm via MCP)
- FINNIFTY: 25
- Stock options: Varies by stock (check contract specifications)

### Margin Requirements
SEBI mandates the following margin components for F&O:
1. **SPAN Margin** — Risk-based margin calculated by the exchange clearing corporation.
2. **Exposure Margin** — Additional margin over SPAN for market-wide risk.
3. **Peak Margin** — Intraday margin snapshots; brokers must collect at least the
   peak margin observed during the day.

Use `calculate_fno_margin` to get exact margin for any trade before placing it.

### Transaction Costs
- **STT (Securities Transaction Tax):** Levied on the sell side of options at
  0.0625% of the intrinsic value on exercise (for ITM options at expiry). For
  futures, STT is 0.0125% on sell side.
- **Brokerage:** Varies by broker (Groww charges per-order flat fees).
- **Exchange charges, GST, SEBI turnover fee, stamp duty** also apply.

### F&O Ban Mechanism
When the market-wide position limit (MWPL) for a stock's F&O contracts exceeds
95%, SEBI places the stock under an F&O ban. During the ban:
- No new positions can be initiated.
- Only squaring off (closing) of existing positions is allowed.
- The ban is lifted when MWPL drops below 80%.

---

## Broker MCP Tool Integration

This skill uses broker MCP tools for live market data and execution support. Use whichever broker is connected (Groww or Zerodha Kite). Always prefer live data over assumptions.

### Groww MCP Tools (if connected)

| Tool | Purpose |
|------|---------|
| `get_ltp` (segment=FNO, query_type=fno) | Live option/futures prices and OI |
| `get_quotes_and_depth` (segment=FNO) | Bid/ask spreads and market depth |
| `fno_mcx_contracts_search_tool` | Search F&O contracts, lot sizes, expiries |
| `fetch_historical_candle_data` (segment=FNO) | Historical option price data |
| `fetch_curated_fno` | F&O gainers, losers, most traded |
| `get_open_interest_analysis` | OI structure, PCR, support/resistance |
| `get_greeks_for_fno_contract` | Live Greeks for specific contracts |
| `get_greeks_for_fno_symbol` | Greeks for all contracts of an underlying |
| `get_atm_straddle_chart` | ATM straddle premium analysis |
| `get_payoff_chart_steps` | Payoff diagram generation instructions |
| `calculate_fno_margin` | Margin requirement calculation |
| `get_available_margin_details` | User's available margin |
| `resolve_market_time_and_calendar` | Market hours and trading calendar |

### Zerodha Kite MCP Tools (if connected)

| Tool | Purpose |
|------|---------|
| `get_ltp` | Last traded price for F&O instruments |
| `get_quotes` | Real-time quotes with bid/ask depth |
| `get_ohlc` | OHLC data for options/futures contracts |
| `get_historical_data` | Historical candle data for F&O |
| `search_instruments` | Search for F&O contracts by name/expiry |
| `get_margins` | Account margins and available funds |
| `get_positions` | Current F&O positions |
| `get_orders` / `get_order_history` | Order status and execution details |
| `place_order` / `modify_order` / `cancel_order` | Order management |
| `place_gtt_order` / `get_gtts` | GTT order management |

### Tool Equivalence Map

| Action | Groww MCP | Zerodha Kite MCP |
|--------|-----------|------------------|
| Live price | `get_ltp` | `get_ltp` |
| Market depth | `get_quotes_and_depth` | `get_quotes` |
| Historical data | `fetch_historical_candle_data` | `get_historical_data` |
| Search contracts | `fno_mcx_contracts_search_tool` | `search_instruments` |
| Margin check | `calculate_fno_margin` / `get_available_margin_details` | `get_margins` |
| Positions | `get_my_trading_positions_today` | `get_positions` |
| Place orders | `place_fno_order` | `place_order` |

---

## Supported Strategies

### Income Strategies
1. **Covered Call** — Long underlying futures + Short OTM Call
   - Objective: Generate income on existing long position.
   - Best when: Mildly bullish, want to earn premium.
   - Indian note: Use futures as underlying (no direct stock delivery for covered calls in F&O segment).

2. **Cash-Secured Put** — Short OTM Put (with margin set aside)
   - Objective: Earn premium while waiting to buy at a lower price.
   - Best when: Bullish on underlying, willing to take delivery equivalent.
   - Indian note: Physical settlement applies for stock options (ITM at expiry).

### Protection Strategies
3. **Protective Put** — Long underlying + Long Put
   - Objective: Insure existing long position against downside.
   - Best when: Want to cap losses while maintaining upside.

4. **Collar** — Long underlying + Long Put + Short Call
   - Objective: Cap both upside and downside. Zero-cost collar if premiums offset.
   - Best when: Want protection without paying net premium.

### Directional Strategies
5. **Bull Call Spread** — Long lower-strike Call + Short higher-strike Call
   - Objective: Limited-risk bullish bet.
   - Best when: Moderately bullish, want defined risk.

6. **Bear Put Spread** — Long higher-strike Put + Short lower-strike Put
   - Objective: Limited-risk bearish bet.
   - Best when: Moderately bearish, want defined risk.

7. **Bull Put Spread** — Short higher-strike Put + Long lower-strike Put
   - Objective: Credit spread, profit if price stays above short strike.
   - Best when: Mildly bullish, want to collect premium.

8. **Bear Call Spread** — Short lower-strike Call + Long higher-strike Call
   - Objective: Credit spread, profit if price stays below short strike.
   - Best when: Mildly bearish, want to collect premium.

### Volatility Strategies
9. **Long Straddle** — Long ATM Call + Long ATM Put
   - Objective: Profit from large move in either direction.
   - Best when: Expecting high volatility (e.g., pre-budget, RBI policy, earnings).
   - Indian note: Popular before Union Budget day, election results, RBI MPC.

10. **Short Straddle** — Short ATM Call + Short ATM Put
    - Objective: Profit from time decay when expecting range-bound movement.
    - Best when: Low implied volatility expected, range-bound market.
    - Indian note: Very popular on weekly expiry day for Nifty/Bank Nifty.

11. **Long Strangle** — Long OTM Call + Long OTM Put
    - Objective: Cheaper alternative to straddle for volatility plays.
    - Best when: Expecting very large move, want lower cost than straddle.

12. **Short Strangle** — Short OTM Call + Short OTM Put
    - Objective: Wider profit zone than short straddle, less premium received.
    - Best when: Expecting range-bound, comfortable with wider risk.

### Range-Bound Strategies
13. **Iron Condor** — Bull Put Spread + Bear Call Spread
    - Objective: Defined-risk range-bound strategy.
    - Best when: Expecting low volatility, want defined max loss.
    - Indian note: Very popular for weekly Nifty expiry plays.

14. **Iron Butterfly** — Short ATM Call + Short ATM Put + Long OTM Call + Long OTM Put
    - Objective: Defined-risk version of short straddle.
    - Best when: Expecting pin at a specific strike (max pain).

### Advanced Strategies
15. **Calendar Spread (Time Spread)** — Short near-expiry option + Long far-expiry option (same strike)
    - Objective: Profit from differential time decay.
    - Best when: Expecting current expiry to decay faster, longer-term view intact.
    - Indian note: Useful between weekly and monthly expiry cycles.

16. **Diagonal Spread** — Calendar spread with different strikes.
    - Objective: Directional bias + time decay benefit.
    - Best when: Have a directional view and want to finance via near-expiry sale.

17. **Ratio Spread** — Buy N options at one strike, sell M options at another (N != M).
    - Objective: Reduce cost of directional trade; accept risk on extreme moves.
    - Best when: Strong view on direction but want reduced cost.
    - Caution: Naked leg creates unlimited risk on one side.

---

## Workflow

Follow this sequence when advising on an options strategy:

### Step 1: Gather Input
Collect the following from the user:
- **Underlying:** Which index or stock? (NIFTY, BANKNIFTY, FINNIFTY, or a specific stock)
- **Market View:** Bullish, bearish, neutral, volatile, or range-bound?
- **Strategy Preference:** Specific strategy or let the advisor recommend?
- **Expiry:** Weekly or monthly? Specific date?
- **Risk Tolerance:** Maximum loss acceptable? Capital available?
- **Objective:** Income generation, hedging, speculation, or volatility play?

### Step 2: Fetch Live Data via Groww MCP

1. **Resolve market time and calendar:**
   ```
   resolve_market_time_and_calendar() → confirm market is open, get trading days to expiry
   ```

2. **Search for contracts:**
   ```
   fno_mcx_contracts_search_tool(search_term="NIFTY 25 MAR") → get exact trading symbols
   ```

3. **Get live prices:**
   ```
   get_ltp(search_queries=["nifty 24000 CE mar", "nifty 24000 PE mar"], segment="FNO", query_type="fno")
   ```

4. **Get Greeks:**
   ```
   get_greeks_for_fno_contract(search_queries=["nifty 24000 mar CE"], expiry="2026-03-26")
   ```

5. **Analyze Open Interest:**
   ```
   get_open_interest_analysis(symbol="NIFTY", view="all")
   ```

6. **Check ATM straddle premium (for volatility assessment):**
   ```
   get_atm_straddle_chart(symbol="NIFTY")
   ```

### Step 3: Calculate Margin Requirement

For each leg of the strategy that involves selling (writing) options:
```
calculate_fno_margin(
    trading_symbol="NIFTY25MAR24000CE",
    num_lots=1,
    transaction_type="SELL",
    product="NRML"
)
```

Also check user's available margin:
```
get_available_margin_details()
```

### Step 4: Simulate P/L Across Price Range

Use the `scripts/black_scholes.py` script or manual calculation:
- Define a price range (e.g., underlying +/- 5% from current price).
- For each price point, calculate P/L for each leg.
- Sum up P/L across all legs.
- Identify breakeven points, max profit, max loss.

Key calculations:
- **Breakeven** = Strike +/- Net Premium (for single-leg strategies)
- **Max Profit** = Net Premium Received (for credit strategies) or Strike Width - Net Debit (for debit spreads)
- **Max Loss** = Net Premium Paid (for debit strategies) or Strike Width - Net Credit (for credit spreads)

### Step 5: Generate ASCII P/L Diagram

Create a visual payoff diagram showing:
- X-axis: Underlying price at expiry
- Y-axis: Profit/Loss per lot
- Breakeven point(s) marked
- Max profit and max loss zones labeled

Also use `get_payoff_chart_steps()` for Groww's built-in payoff chart generation.

### Step 6: Provide Risk Management Guidance

Include in every recommendation:
- **Position sizing:** How many lots based on capital and risk tolerance.
- **Stop-loss levels:** When to exit (e.g., if loss exceeds 2x premium received).
- **Adjustment triggers:** When and how to adjust the strategy.
- **Expiry management:** Roll, close, or let expire — guidance based on ITM/OTM status.
- **STT warning:** Remind about STT on ITM options at expiry (can erode profits significantly).
- **Margin monitoring:** Warn about peak margin requirements and potential margin calls.

### Step 7: Save Report

Present the complete analysis as a structured report:

```
=== OPTIONS STRATEGY REPORT ===
Date: [current date]
Underlying: [symbol] @ [current price]
Strategy: [strategy name]
Expiry: [expiry date] ([days to expiry] days)

--- LEGS ---
Leg 1: [BUY/SELL] [qty] [CALL/PUT] @ Strike [strike] for [premium]
Leg 2: [BUY/SELL] [qty] [CALL/PUT] @ Strike [strike] for [premium]

--- KEY METRICS ---
Net Premium: [debit/credit] [amount] per lot
Max Profit: [amount] per lot (at [price])
Max Loss: [amount] per lot (at [price])
Breakeven: [price(s)]
Risk-Reward Ratio: [ratio]
Probability of Profit: [estimate based on delta]

--- GREEKS (NET POSITION) ---
Delta: [value] | Gamma: [value] | Theta: [value] | Vega: [value]

--- MARGIN REQUIREMENT ---
Total Margin: [amount]
Available Margin: [amount]
Margin Utilization: [percentage]

--- P/L DIAGRAM ---
[ASCII payoff chart]

--- RISK MANAGEMENT ---
- Stop Loss: [criteria]
- Adjustment Plan: [when and how]
- Expiry Action: [recommendation]
- STT Impact: [if applicable]
```

---

## Strategy Selection Guide

Use this decision tree to recommend strategies based on user's market view:

### Bullish View
- **Strong bullish:** Long Call or Bull Call Spread
- **Mildly bullish:** Bull Put Spread (credit) or Covered Call
- **Bullish + high IV:** Bull Put Spread (sell expensive puts)
- **Bullish + low IV:** Long Call or Bull Call Spread (buy cheap options)

### Bearish View
- **Strong bearish:** Long Put or Bear Put Spread
- **Mildly bearish:** Bear Call Spread (credit)
- **Bearish + high IV:** Bear Call Spread (sell expensive calls)
- **Bearish + low IV:** Long Put or Bear Put Spread

### Neutral / Range-Bound View
- **Tight range expected:** Short Straddle or Iron Butterfly
- **Wider range expected:** Short Strangle or Iron Condor
- **Neutral + want defined risk:** Iron Condor or Iron Butterfly

### Volatile View (Expecting Big Move)
- **Direction unknown, big move expected:** Long Straddle
- **Direction unknown, very big move expected:** Long Strangle (cheaper)
- **Pre-event (budget, RBI, earnings):** Long Straddle or Long Strangle

### Time Decay Play
- **Near-term decay focus:** Calendar Spread
- **Directional + decay:** Diagonal Spread

---

## Important Indian Market Considerations

### India VIX
- India VIX measures the market's expectation of 30-day volatility.
- VIX > 20: High volatility environment — favor long volatility strategies.
- VIX < 15: Low volatility environment — favor short volatility strategies.
- VIX between 15-20: Normal range — use directional or range-bound strategies.
- VIX typically spikes before elections, budgets, RBI policy, and global crises.

### Weekly Expiry Trading
- **Thursday (Nifty):** Most liquid expiry. Short straddle/strangle sellers dominate.
  Theta decay is highest on the expiry day.
- **Wednesday (Bank Nifty):** High gamma risk. Moves can be sharp near expiry.
- Premium sellers should be cautious of gamma risk on expiry day — a small move
  in the underlying can cause large P/L swings.

### Physical Settlement (Stock Options)
- Stock options that expire ITM are physically settled — actual delivery of shares.
- This requires full delivery margin (value of shares). Plan exits before expiry
  to avoid unexpected margin requirements.
- Index options are cash-settled — no delivery concerns.

### Max Pain
- Max Pain is the strike price at which the maximum number of options (calls + puts)
  expire worthless, causing minimum payout by option writers.
- Indian markets tend to gravitate toward max pain on expiry day, especially for
  Nifty weekly expiry.
- Use OI analysis to identify max pain and position accordingly.

### OI-Based Analysis
- **High Call OI at a strike:** Acts as resistance. Call writers are betting the
  price won't cross this level.
- **High Put OI at a strike:** Acts as support. Put writers are betting the price
  won't fall below this level.
- **PCR (Put-Call Ratio):**
  - PCR > 1.2: Bullish signal (more puts written, indicating support)
  - PCR < 0.8: Bearish signal (more calls written, indicating resistance)
  - PCR between 0.8-1.2: Neutral

---

## Error Handling

- If broker MCP tools (Groww or Zerodha) return errors, inform the user and suggest checking market
  hours or contract availability. Try the alternative broker's equivalent tool if available.
- If a contract search yields no results, try alternative search terms or check
  if the expiry has passed.
- If margin data is unavailable, provide theoretical estimates with a disclaimer.
- Always validate that the market is open before fetching live data — use
  `resolve_market_time_and_calendar()`.
- If a stock is under F&O ban, alert the user immediately and suggest alternative
  underlyings.
