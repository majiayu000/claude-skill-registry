---
name: weekly-fno-trade-planner
description: >
  Weekly F&O trade planning skill for Indian markets. Analyzes news/macro events,
  identifies trending sectors and instruments, determines probable direction, suggests
  option strategy with entry/exit levels, and manages stop-loss and profit booking
  after position entry. Use when user wants a weekly trade idea, F&O direction call,
  or ongoing position management for Nifty, Bank Nifty, or stock options.
---

# Weekly F&O Trade Planner

## Overview

A complete weekly trading workflow for Indian F&O markets — from macro thesis to
position management. This skill identifies high-conviction directional trades by
combining news analysis, sector screening, technical confirmation, and institutional
flow data, then manages the position with structured stop-loss and profit-booking rules.

Designed for retail traders with limited capital who prefer option buying over selling.
Supports both Groww MCP and Zerodha Kite MCP for live execution.

---

## Phase 1: News & Macro Scan

### Goal
Identify the dominant narrative driving markets this week.

### Steps

1. **Fetch breaking news and macro events**:
```
WebSearch: "Indian stock market news this week {current_date}"
WebSearch: "global markets impact India {current_week}"
WebSearch: "RBI SEBI announcement {current_month} {current_year}"
WebSearch: "geopolitical risk India market {current_date}"
```

2. **Categorize the macro environment**:

| Category | Examples | Typical F&O Play |
|----------|----------|------------------|
| **Geopolitical crisis** | War, sanctions, oil shock | Index PUTs (Nifty/BankNifty) |
| **Policy event** | RBI rate decision, budget, SEBI circular | Straddle/strangle before event |
| **Earnings season** | IT/Banking results week | Stock options directional |
| **Global risk-off** | US recession fear, China slowdown, Fed hawkish | Index PUTs, IT stock CALLs (INR weak) |
| **Domestic momentum** | DII buying, reform news, GDP beat | Index CALLs, banking CALLs |
| **Sector rotation** | Defence order, pharma approval, EV policy | Sector-specific stock options |
| **Low conviction** | No clear driver, range-bound | Avoid or play iron condor |

3. **Rate the macro conviction** (1-5):
   - 5: Clear, strong catalyst with defined timeline (e.g., war escalation, surprise rate cut)
   - 4: Strong theme but timing uncertain
   - 3: Moderate — multiple conflicting signals
   - 2: Weak — mostly noise
   - 1: No conviction — skip the week or go very small

**Rule: Only proceed to Phase 2 if conviction >= 3.**

---

## Phase 2: Sector & Instrument Identification

### Goal
Find the ONE instrument most likely to move meaningfully this week.

### Steps

1. **Screen market movers and sectors**:

Use whichever broker MCP is connected:

```python
# Groww MCP
fetch_market_movers_and_trending_stocks_funds(
    discovery_filter_types=["TOP_GAINERS", "TOP_LOSERS", "VOLUME_SHOCKERS",
                           "YEARLY_HIGH", "YEARLY_LOW", "STOCKS_IN_NEWS"]
)
fetch_curated_fno(fno_filter_types=["GAINERS", "LOSERS", "TOP_TRADED"])

# Zerodha Kite MCP — use web search for movers, then:
# search_instruments(query="{sector_leader}")
```

2. **Check institutional flows** (invoke `fii-dii-flow-tracker` skill):
   - FII net buy/sell trend (last 5-10 days)
   - DII positioning
   - Sector-wise FII allocation shifts

3. **Narrow to ONE instrument** using this priority:
   - **Index (Nifty/BankNifty)**: For macro/geopolitical/broad market themes
   - **Sector ETF or index**: For sector rotation themes
   - **Single stock**: For earnings/company-specific catalysts (must be in F&O list)

4. **Validate F&O availability**:
```python
# Groww MCP
fno_mcx_contracts_search_tool(search_term="{instrument_name}")

# Zerodha Kite MCP
search_instruments(query="{instrument_name}", segment="NFO-OPT")
```

### Selection Criteria

The ideal instrument has:
- Direct exposure to the identified macro theme
- High F&O liquidity (tight bid-ask spread)
- Clear technical setup (trending, not choppy)
- Manageable lot size for user's capital

---

## Phase 3: Direction & Technical Confirmation

### Goal
Determine the probable direction (bullish/bearish) with technical evidence.

### Steps

1. **Fetch price data** (daily and hourly):
```python
# Groww MCP
fetch_historical_candle_data(
    trading_symbol="{symbol}",
    start_time="{60_days_ago} 09:15:00",
    end_time="{today} 15:30:00",
    interval_in_minutes="1440"
)

# Zerodha Kite MCP
get_historical_data(
    instrument_token="{token}",
    from_date="{60_days_ago}",
    to_date="{today}",
    interval="day"
)
```

2. **Run technical indicators**:
```python
# Groww MCP
get_historical_technical_indicators(
    trading_symbol="{symbol}",
    start_time="{30_days_ago} 09:15:00",
    end_time="{today} 15:30:00",
    interval_in_minutes="1440",
    indicators=["sma", "ema", "rsi", "macd", "supertrend", "bollinger", "atr", "vwap"]
)

# Zerodha Kite MCP — fetch raw candles and compute indicators manually or via yfinance
```

3. **Identify key levels**:
   - **Support levels**: Recent swing lows, round numbers, SMA/EMA zones
   - **Resistance levels**: Recent swing highs, previous breakdown points
   - **Trend**: Higher highs/lows (bullish) or lower highs/lows (bearish)
   - **Momentum**: RSI, MACD crossover direction, SuperTrend signal

4. **Check Open Interest for institutional positioning**:
```python
# Groww MCP
get_open_interest_analysis(symbol="{symbol}", view="all")

# Zerodha Kite MCP — use web search for OI data from NSE
```

   - Heavy PUT writing at a strike = institutional support floor
   - Heavy CALL writing at a strike = institutional resistance ceiling
   - PCR > 1.2 = market leaning bullish (hedged)
   - PCR < 0.8 = market leaning bearish

5. **Direction verdict**:

| Signal | Bullish | Bearish |
|--------|---------|---------|
| Trend | Higher lows | Lower highs |
| RSI | 40-60 rising | 40-60 falling |
| MACD | Bullish crossover | Bearish crossover |
| SuperTrend | Green/Buy | Red/Sell |
| FII flows | Net buying | Net selling |
| OI structure | Heavy PUT writing below | Heavy CALL writing above |

**Rule: Need 4+ signals aligned for a directional trade. If mixed, skip or play non-directional.**

---

## Phase 4: Strategy & Entry Plan

### Goal
Select the optimal option strategy and define precise entry levels.

### Steps

1. **Check IV environment**:
```python
# Groww MCP
get_greeks_for_fno_contract(
    search_queries=["{atm_option}"],
    expiry="{expiry_date}"
)
get_atm_straddle_chart(symbol="{symbol}")

# Zerodha Kite MCP — compute IV from option price using Black-Scholes
```

2. **Select strategy based on conviction + IV**:

| Conviction | IV Level | Direction | Strategy |
|-----------|----------|-----------|----------|
| High (4-5) | Low-Normal | Bullish | Buy ATM/slightly OTM CALL |
| High (4-5) | Low-Normal | Bearish | Buy ATM/slightly OTM PUT |
| High (4-5) | High | Bullish | Bull call spread (cap IV risk) |
| High (4-5) | High | Bearish | Bear put spread (cap IV risk) |
| Moderate (3) | Low | Either | Buy OTM option (cheap lottery) |
| Moderate (3) | High | Either | Sell far OTM opposite side (collect premium) |
| Any | Very High | Pre-event | Straddle/strangle (if event binary) |

3. **Expiry selection**:
   - **Current week expiry**: Only if entering Mon-Tue with high conviction
   - **Next week expiry**: Default choice — gives 7-12 days
   - **Monthly expiry**: For lower conviction or swing trades
   - **Rule**: Never buy options with < 3 days to expiry unless very high conviction

4. **Strike selection**:
   - **ATM or 1 strike OTM**: High conviction, want delta exposure
   - **2-3 strikes OTM**: Moderate conviction, cheaper but needs bigger move
   - **Deep OTM**: Avoid (low probability, theta destroys)

5. **Position sizing**:
```python
# Groww MCP
calculate_fno_margin(
    trading_symbol="{option_symbol}",
    num_lots=1,
    transaction_type="BUY",
    product="NRML"
)
get_available_margin_details()

# Zerodha Kite MCP
get_margins()
```

   - **Max risk per trade**: 30-40% of capital for single directional bet
   - **Preferred**: Split into 2-3 lots for scaling in/out
   - **Never**: Risk more than 50% of capital on a single trade

6. **Define entry plan**:
   - **Entry trigger**: Specific price level or technical confirmation
   - **Entry price range**: Acceptable premium range
   - **Lot allocation**: How many lots at entry vs. add-on

### Output: Trade Card

```
TRADE IDEA — Week of {date}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
Thesis:     {1-line macro reason}
Instrument: {symbol}
Direction:  {BULLISH/BEARISH}
Conviction: {3/4/5 out of 5}

Strategy:   Buy {strike} {CE/PE} {expiry}
Entry:      ₹{premium} (when {underlying} at {level})
Lots:       {n} lots ({quantity} qty)
Capital:    ₹{amount} ({%} of total)

Stop-Loss:  ₹{sl_premium} ({underlying} at ~{level}) = -₹{loss}
Target 1:   ₹{t1_premium} ({underlying} at ~{level}) = +₹{profit1}
Target 2:   ₹{t2_premium} ({underlying} at ~{level}) = +₹{profit2}

Risk:Reward = 1:{ratio}
Max Loss:   ₹{max_loss} ({%} of capital)
━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Phase 4.5: Gap Probability & Immediate Entry Decision

### Goal
When analysis is run DURING MARKET HOURS or AFTER MARKET CLOSE (post 3:30 PM), assess
whether the next trading day is likely to see a significant gap-up or gap-down. If high
probability, **recommend IMMEDIATE entry** before close — do NOT defer to next morning.

**THIS IS THE MOST CRITICAL PHASE FOR MULTIPLIED PROFITS.** Buying OTM options before a
gap is 2-5x cheaper than buying after the gap opens. Missing this window is the single
biggest profit killer for retail F&O traders.

### When to Trigger This Phase

- **Always** when running the skill after 2:00 PM on a trading day
- **Always** when running the skill after market close (post 3:30 PM)
- **Always** when conviction is >= 4 and direction is clear
- **Always** when an active geopolitical/macro crisis is ongoing

### Steps

1. **Check GIFT Nifty / SGX Nifty (after hours)**:
```
WebSearch: "GIFT Nifty live today {current_date}"
WebSearch: "SGX Nifty futures {current_date} evening"
```
   - GIFT Nifty trading > 100 pts below close = **high gap-down probability**
   - GIFT Nifty trading > 100 pts above close = **high gap-up probability**

2. **Check overnight global cues**:
```
WebSearch: "US futures S&P Nasdaq live {current_date}"
WebSearch: "Asian markets Japan China {current_date} evening"
WebSearch: "crude oil price Brent live tonight {current_date}"
```
   - US futures down > 1% = gap-down signal
   - Brent crude spike > 3% overnight = strong gap-down for India
   - Asian markets deep red = confirms gap-down

3. **Check overnight news catalysts**:
```
WebSearch: "{active_crisis} latest news tonight {current_date}"
WebSearch: "breaking news global markets after hours {current_date}"
```
   - New escalation in active crisis = gap accelerator
   - De-escalation / ceasefire = reverse gap

4. **Calculate Gap Probability Score**:

| Factor | Bearish Gap | Bullish Gap |
|--------|-------------|-------------|
| GIFT Nifty > 100 pts below close | +30% | — |
| GIFT Nifty > 200 pts below close | +50% | — |
| US futures down > 1% | +15% | — |
| Brent crude up > 3% overnight | +20% | — |
| Active geopolitical crisis escalating | +20% | — |
| FII selling > ₹3,000 cr today | +10% | — |
| GIFT Nifty > 100 pts above close | — | +30% |
| GIFT Nifty > 200 pts above close | — | +50% |
| US futures up > 1% | — | +15% |
| Ceasefire / de-escalation news | — | +25% |
| FII buying > ₹2,000 cr today | — | +10% |

**Score > 60% = HIGH probability gap. RECOMMEND IMMEDIATE ENTRY.**

5. **Immediate Entry vs Wait Decision**:

| Gap Probability | Time | Action |
|----------------|------|--------|
| **> 60%** | **Before 3:15 PM** | **BUY NOW. Do not wait for tomorrow.** |
| **> 60%** | **After 3:30 PM** | **Alert user: Buy at 9:15 AM tomorrow. Pre-set limit order.** |
| 40-60% | Any | Buy half position now, half at open |
| < 40% | Any | Wait for confirmation at open |

6. **Pre-Gap Strike Selection** (DIFFERENT from regular entry):
   When buying BEFORE a gap, select strikes that are currently **2-4 strikes OTM**:
   - These are cheap (₹50-150 range) = maximum leverage
   - After the gap, they become ATM or slightly OTM = premium explodes
   - Buy MORE lots of cheaper OTM options for max profit on the gap
   - **This is the "lottery ticket" entry** — high R:R, limited downside

   Example (Bearish gap expected):
   - Nifty at 23,778 → Buy 23,000 PE at ₹109 (778 pts OTM)
   - Next day gap to 23,200 → 23,000 PE jumps to ₹250+ (130% overnight gain)
   - 6 lots × 65 × ₹141 profit = ₹55,000 on ₹42,500 invested

7. **Output: Immediate Entry Alert**:

```
🚨 GAP ALERT — {DIRECTION} GAP EXPECTED TOMORROW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Gap Probability: {score}%
GIFT Nifty:      {level} ({change} from close)
Key Catalyst:    {reason}

⚡ IMMEDIATE ENTRY RECOMMENDED — BUY BEFORE CLOSE
Strategy:   Buy {strike} {CE/PE} {expiry} (currently {X} pts OTM)
Premium:    ₹{cheap_price} per unit
Lots:       {max_lots} lots in ₹{budget}
Cost:       ₹{total_cost}

Expected tomorrow open: ₹{estimated_premium} (+{%} overnight)
Expected profit:        ₹{overnight_profit}

vs. buying AFTER gap:   Premium will be ₹{expensive_price}
                        You'd get {fewer_lots} lots for same ₹{budget}
                        Profit potential: {reduced}% lower

⏰ WINDOW: Buy before 3:15 PM today
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Critical Rules for Pre-Gap Entry

1. **Only with conviction >= 4** — Don't gamble on uncertain gaps
2. **Max 40% of capital** — Even with high conviction, respect position limits
3. **Always use monthly expiry** for pre-gap entries — gives time if gap is delayed
4. **Set SL immediately** — Pre-gap entries can go wrong (gap doesn't materialize)
5. **If gap doesn't happen next day** — Hold if thesis is intact, exit if thesis breaks
6. **Don't chase if you miss the window** — Post-gap premiums are 2-3x, reduce lots

---

## Phase 5: Execution

### Goal
Place the trade with proper order types.

### Steps

1. **Verify live price before entry**:
```python
# Groww MCP
get_ltp(search_queries=["{option_symbol}"], segment="FNO", query_type="fno")
get_quotes_and_depth(search_query="{option_symbol}", segment="FNO", entity_type="fno")

# Zerodha Kite MCP
get_ltp(instruments=["NFO:{option_symbol}"])
get_quotes(instruments=["NFO:{option_symbol}"])
```

2. **Place the order** (always ask user for confirmation):
```python
# Groww MCP
place_fno_order(
    trading_symbol="{option_symbol}",
    num_lots={n},
    transaction_type="BUY",
    order_type="LIMIT",
    price={limit_price},
    product="NRML"
)

# Zerodha Kite MCP
place_order(
    exchange="NFO",
    tradingsymbol="{option_symbol}",
    transaction_type="BUY",
    quantity={quantity},
    order_type="LIMIT",
    price={limit_price},
    product="NRML"
)
```

3. **Set GTT stop-loss immediately after fill**:
```python
# Groww MCP
place_fno_order(
    trading_symbol="{option_symbol}",
    num_lots={n},
    transaction_type="SELL",
    order_type="LIMIT",
    price={sl_price},
    trigger_price={sl_trigger},
    smart_order_category="GTT",
    trigger_direction="DOWN",
    product="NRML"
)

# Zerodha Kite MCP
place_gtt_order(
    trigger_type="single",
    tradingsymbol="{option_symbol}",
    exchange="NFO",
    trigger_values=[{sl_trigger}],
    last_price={current_ltp},
    orders=[{
        "transaction_type": "SELL",
        "quantity": {quantity},
        "price": {sl_price},
        "order_type": "LIMIT",
        "product": "NRML"
    }]
)
```

4. **Set GTT profit target** (same pattern as above with trigger_direction="UP")

**Important GTT notes**:
- GTT triggers on the OPTION's LTP, not the underlying price
- Always set trigger_price slightly before the limit price (e.g., trigger at ₹95, sell at ₹90 for SL)
- On Groww: GTT may show "verification failed" — this is a known display bug, the order is active
- After exiting a position, ALWAYS cancel orphaned GTTs

---

## Phase 6: Position Management (Ongoing)

### Goal
Manage the position daily with structured rules for SL tightening, partial exits, and full exit.

### Daily Monitoring Checklist

1. **Check position P&L**:
```python
# Groww MCP
get_my_trading_positions_today()
get_specific_stock_position(trading_symbol="{option}", segment="FNO")

# Zerodha Kite MCP
get_positions()
```

2. **Check underlying price action**:
```python
# Use either broker MCP for live price + intraday chart
get_ltp(search_queries=["{underlying}"])
fetch_historical_candle_data(
    trading_symbol="{underlying}",
    start_time="{today} 09:15:00",
    end_time="{today} 15:30:00",
    interval_in_minutes="5"
)
```

3. **Check news for thesis changes**:
```
WebSearch: "{macro_theme} latest news {current_date}"
```

4. **Check institutional flows** (FII/DII daily data via `fii-dii-flow-tracker` skill)

### Stop-Loss Tightening Rules

| Premium Move | New SL Level | Logic |
|-------------|-------------|-------|
| Entry | -30% of premium | Initial risk limit |
| +30% profit | Breakeven (entry price) | "Free trade" — can't lose |
| +50% profit | Entry + 20% | Lock 20% guaranteed profit |
| +100% profit | Entry + 50% | Lock 50%, let rest run |
| +150%+ profit | Trail by 30% from peak | Ride the momentum |

To tighten a GTT SL:
```python
# Groww MCP
modify_order_with_confirmation(
    groww_order_id="{gtt_order_id}",
    quantity={qty},
    segment="FNO",
    order_type="LIMIT",
    price={new_sl_price},
    trigger_price={new_trigger},
    trigger_direction="DOWN",
    order_category="GTT"
)

# Zerodha Kite MCP
modify_gtt_order(
    trigger_id={gtt_id},
    trigger_type="single",
    tradingsymbol="{option_symbol}",
    exchange="NFO",
    trigger_values=[{new_trigger}],
    last_price={current_ltp},
    orders=[{
        "transaction_type": "SELL",
        "quantity": {qty},
        "price": {new_sl_price},
        "order_type": "LIMIT",
        "product": "NRML"
    }]
)
```

### Partial Profit Booking Rules

| Condition | Action | Remaining |
|-----------|--------|-----------|
| Target 1 hit (+50-80%) | Exit 40-50% of position | 50-60% as runner |
| Target 2 hit (+100-150%) | Exit another 30% | 20-30% as runner |
| Momentum continues | Trail SL on remaining | Let it ride |
| Thesis weakens | Exit all remaining | Protect profits |

### Full Exit Triggers

Exit the ENTIRE position when:
- **SL hit**: No questions, no hoping — exit immediately
- **Thesis invalidated**: Key news changes the setup (e.g., ceasefire in a war trade)
- **Time decay risk**: < 2 days to expiry and position is OTM
- **IV crush**: After a binary event, IV drops killing premium even if direction is right
- **Weekend risk**: For weekly expiry options, exit Friday unless very high conviction
- **Overexposure**: If unrealized P&L exceeds 50% of total capital, take some off

### Exit Execution

```python
# Market exit for urgency (Groww)
place_fno_order(
    trading_symbol="{option_symbol}",
    num_lots={remaining_lots},
    transaction_type="SELL",
    order_type="MARKET",
    product="NRML"
)

# Zerodha Kite
place_order(
    exchange="NFO",
    tradingsymbol="{option_symbol}",
    transaction_type="SELL",
    quantity={remaining_qty},
    order_type="MARKET",
    product="NRML"
)

# ALWAYS cancel orphaned GTTs after exit
# Groww: cancel_order_with_confirmation(groww_order_id="{gtt_id}", segment="FNO", order_category="GTT")
# Zerodha: delete_gtt_order(trigger_id={gtt_id})
```

---

## Risk Management Rules (Non-Negotiable)

1. **Max capital at risk**: 40% of total capital per trade
2. **Always set SL**: Never hold a position without a stop-loss GTT
3. **No averaging down**: If SL is hit, accept the loss. Don't add to losers.
4. **Weekend rule**: Exit weekly expiry options before Friday close unless thesis is very strong
5. **Theta awareness**: Options lose ~30-50% of remaining time value over a weekend
6. **IV awareness**: After a big event, IV crushes. Factor this into hold decisions.
7. **No revenge trading**: If a trade is stopped out, wait for the next clean setup
8. **Position limit**: Max 2 open F&O positions at any time
9. **Cancel orphaned GTTs**: After every exit, clean up ALL related GTT orders
10. **Journal the trade**: Record entry reason, exit reason, P&L, and lessons learned

---

## Weekly Schedule

| Day | Activity |
|-----|----------|
| **Sunday evening** | Phase 1-4: Full analysis, generate Trade Card |
| **Monday 9:00 AM** | Phase 4.5: Check GIFT Nifty, assess gap probability |
| **Monday 9:00-9:15** | Phase 5: Execute if setup confirms (pre-open or at open) |
| **Mon-Thu (market hours)** | Phase 6: Daily monitoring, SL tightening, partial exits |
| **Mon-Thu (post 3 PM)** | **Phase 4.5: ALWAYS check for next-day gap opportunity** |
| **Mon-Thu (after close)** | Phase 4.5: Check GIFT Nifty + overnight cues for gap alert |
| **Friday** | Decision: Exit before weekend or hold (apply weekend rule) |
| **Weekend** | Review, journal, prepare next week's analysis |

### IMPORTANT: Evening Workflow (The Edge)

Every trading day after 2:30 PM or after market close, if an active position thesis exists
or macro conviction >= 3, the skill MUST run Phase 4.5 to check for overnight gap opportunities.

**The #1 profit multiplier in F&O is buying BEFORE the gap, not AFTER.**

If the user invokes this skill in the evening / after hours:
1. Skip Phases 1-3 if thesis is already established
2. Go DIRECTLY to Phase 4.5 (Gap Probability)
3. If gap score > 60%, issue Immediate Entry Alert
4. **NEVER say "wait for tomorrow" when gap probability is high and market is still open**
5. If market is closed, alert user to set pre-market limit order or buy at 9:15 sharp

---

## Tools Used

Use whichever broker MCP is connected (Groww or Zerodha Kite):

| Action | Groww MCP | Zerodha Kite MCP | Fallback |
|--------|-----------|------------------|----------|
| Live price | `get_ltp` | `get_ltp` | yfinance |
| Market depth | `get_quotes_and_depth` | `get_quotes` | — |
| Historical data | `fetch_historical_candle_data` | `get_historical_data` | yfinance |
| Technical indicators | `get_historical_technical_indicators` | — (compute from candles) | yfinance + pandas |
| Open interest | `get_open_interest_analysis` | — | Web search (NSE) |
| Greeks/IV | `get_greeks_for_fno_contract` | — | Black-Scholes script |
| ATM straddle | `get_atm_straddle_chart` | — | Manual calculation |
| Margin check | `calculate_fno_margin` | `get_margins` | — |
| F&O search | `fno_mcx_contracts_search_tool` | `search_instruments` | — |
| Place order | `place_fno_order` | `place_order` | — |
| GTT orders | `place_fno_order` (GTT) | `place_gtt_order` | — |
| Modify GTT | `modify_order_with_confirmation` | `modify_gtt_order` | — |
| Cancel GTT | `cancel_order_with_confirmation` | `delete_gtt_order` | — |
| Positions | `get_my_trading_positions_today` | `get_positions` | — |
| Portfolio | `get_equity_portfolio_holdings` | `get_holdings` | — |
| Market movers | `fetch_market_movers_and_trending_stocks_funds` | — | Web search |
| F&O movers | `fetch_curated_fno` | — | Web search |
| Trading calendar | `resolve_market_time_and_calendar` | — | Web search |
| Screener | `fetch_technical_screener` | — | Web search |
| News | `WebSearch` | `WebSearch` | `WebSearch` |
| FII/DII flows | `fii-dii-flow-tracker` skill | `fii-dii-flow-tracker` skill | Web search |
| Calculator | `calculator` | — | Python |

---

## Disclaimer

This skill provides analysis and trade suggestions based on publicly available data
and technical/fundamental indicators. It is NOT financial advice. All F&O trading
involves significant risk of loss. Users must make their own investment decisions and
are responsible for their own trades. Past patterns do not guarantee future results.
