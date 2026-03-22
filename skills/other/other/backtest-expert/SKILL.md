---
name: backtest-expert
description: >
  Expert guidance for systematic backtesting of trading strategies on Indian markets (NSE/BSE).
  Use when developing strategies, testing robustness, avoiding overfitting, or validating trading ideas.
---

# Backtest Expert — Indian Market Strategy Validation

## Core Philosophy

> **"Find strategies that break the least, not profit the most."**

A strategy that survives stress testing across multiple market regimes, transaction cost assumptions, and parameter perturbations is far more valuable than one that shows spectacular returns on a single optimized parameter set. Overfitting is the silent killer of trading accounts.

---

## 6-Step Backtesting Workflow

### Step 1: State the Hypothesis (1 Sentence Edge)

Before writing a single line of code, articulate why the strategy should work in one clear sentence.

**Good hypotheses:**
- "Stocks that gap up >3% on above-average volume after consolidation tend to continue higher for 2-5 days on NSE."
- "Nifty 50 stocks that revert to their 20-day mean after RSI drops below 30 produce positive expectancy within 5 trading sessions."
- "Selling strangles on Bank Nifty on Wednesday expiry with delta <0.15 captures time decay faster than gamma risk materializes."

**Bad hypotheses:**
- "This indicator combination looks good on the chart." (no edge articulated)
- "I saw someone on Twitter making money with this." (no reasoning)

**Ask yourself:**
- What behavioral or structural edge am I exploiting?
- Why would this edge persist? (Structural > Behavioral > Statistical)
- Who is on the other side of this trade, and why are they losing?

---

### Step 2: Codify Rules (No Ambiguity)

Every rule must be binary — a computer must be able to execute it without interpretation.

#### Rule Categories

| Category | What to Define | Example |
|----------|---------------|---------|
| **Universe** | Which stocks/instruments | Nifty 200 constituents, F&O stocks only, market cap >5000 Cr |
| **Entry** | Exact trigger conditions | Close > 20 EMA AND RSI(14) crosses above 40 AND volume > 1.5x 20-day avg |
| **Exit — Target** | Profit-taking rule | Close 3% above entry OR trailing stop of 1.5 ATR |
| **Exit — Stop** | Loss-cutting rule | Close below entry-day low OR 2% fixed stop |
| **Exit — Time** | Maximum holding period | Exit after 10 trading sessions if neither target nor stop hit |
| **Position Sizing** | How much capital per trade | 5% of equity per position, max 10 concurrent positions |
| **Filters** | When NOT to trade | Skip if stock is in F&O ban period, skip 2 days around results |

#### India-Specific Rules to Consider
- **Circuit limits:** Stocks hitting upper/lower circuit cannot be exited. Define handling.
- **F&O ban period:** Stocks crossing 95% MWPL cannot add fresh F&O positions.
- **T+1 settlement:** Cash equity settles next trading day (changed from T+2 in 2023).
- **Pre-open session:** 9:00-9:08 AM orders, 9:08-9:15 AM matching. Define if you use pre-open.
- **Muhurat trading:** Special Diwali session — include or exclude?
- **Corporate actions:** Adjust for splits, bonuses, dividends, rights issues.

---

### Step 3: Run Initial Backtest

#### Minimum Requirements

| Parameter | Minimum | Recommended |
|-----------|---------|-------------|
| **Time period** | 5 years | 8-10+ years |
| **Number of trades** | 100 | 200+ |
| **Market regimes covered** | 2 (bull + bear) | 4+ (bull, bear, sideways, high-vol) |
| **Data quality** | Adjusted for corporate actions | Survivorship-bias-free universe |

#### Indian Market Regimes to Cover

| Regime | Period Examples | Characteristics |
|--------|----------------|-----------------|
| **Bull market** | 2014-2017, 2020-2021 | Nifty trending up, broad participation |
| **Bear market** | 2008, 2020 (Mar), 2022 (Jun) | Sharp drawdowns, high correlation |
| **Sideways/Range** | 2018-2019, 2023 H1 | Nifty in 10% range, stock-specific moves |
| **High volatility** | 2008, 2020, Budget days | India VIX > 25 |
| **Low volatility** | 2017, 2021 H2 | India VIX < 15 |
| **Pre/Post Budget** | Every Feb 1 | Gap moves, policy-driven sectors |
| **Election cycle** | 2014, 2019, 2024 | Uncertainty then rally pattern |
| **Monsoon impact** | Jun-Sep annually | Agri, FMCG, rural economy impact |
| **RBI policy shifts** | Rate hike/cut cycles | Banking, NBFC, rate-sensitive sectors |
| **Global crude shock** | 2018, 2022 | INR weakness, OMC impact, inflation |

#### Key Metrics to Record

```
Returns: CAGR, total return, monthly returns distribution
Risk: Max drawdown, average drawdown, drawdown duration, Calmar ratio
Efficiency: Sharpe ratio (use 6% risk-free for India), Sortino ratio
Trade quality: Win rate, avg win/loss, profit factor, expectancy per trade
Consistency: % profitable months, worst month, longest losing streak
```

---

### Step 4: Stress Test (Spend 80% of Your Time Here)

This is where most backtests fail — and where the real value lies.

#### 4a. Parameter Sensitivity

Perturb every parameter by +/-20% and check if performance degrades gracefully or collapses.

| Parameter | Base | -20% | -10% | +10% | +20% | Verdict |
|-----------|------|------|------|------|------|---------|
| EMA period | 20 | 16 | 18 | 22 | 24 | Stable if all profitable |
| RSI threshold | 40 | 32 | 36 | 44 | 48 | Fragile if only 40 works |
| Stop loss % | 2% | 1.6% | 1.8% | 2.2% | 2.4% | Check drawdown impact |

**Rule of thumb:** If the strategy only works with exact parameter values, it is overfit. You want a "plateau" of profitability, not a "peak."

#### 4b. Execution Friction (India-Specific Costs)

Apply realistic transaction costs:

| Cost Component | Delivery (CNC) | Intraday (MIS) | F&O |
|----------------|----------------|-----------------|-----|
| Brokerage | ~₹20/order or 0.03% | ~₹20/order or 0.03% | ~₹20/order |
| STT | 0.1% (buy+sell) | 0.025% (sell only) | 0.0125% (sell, options) |
| Exchange charges | 0.00345% (NSE) | 0.00345% (NSE) | 0.05% (options) |
| GST | 18% on brokerage+exchange | 18% on brokerage+exchange | 18% on brokerage+exchange |
| Stamp duty | 0.015% (buy) | 0.003% (buy) | 0.003% (buy) |
| SEBI charges | 0.0001% | 0.0001% | 0.0001% |
| **Slippage** | **0.05-0.1% large-cap** | **0.1-0.2% mid-cap** | **0.1-0.3% options** |

**Total round-trip cost estimates:**
- Delivery large-cap: ~0.3-0.5%
- Intraday large-cap: ~0.1-0.2%
- F&O (options): ~0.15-0.4%
- Small-cap delivery: ~0.5-1.0% (wider spreads)

#### 4c. Time Robustness

- Split data into 3-year rolling windows. Is the strategy profitable in each?
- Check year-by-year returns. Is any single year driving total performance?
- Remove the best month. Is the strategy still positive?

#### 4d. Sample Size Validation

- Minimum 30 trades for any statistical claim (even this is weak)
- 100+ trades: Moderate confidence
- 200+ trades: Good confidence
- Use the t-test: Is average trade return significantly different from zero?

---

### Step 5: Out-of-Sample Validation (Walk-Forward Analysis)

**Never skip this step.**

#### Walk-Forward Method for Indian Markets

1. **In-sample period:** Train on 5 years of data (e.g., 2015-2019)
2. **Out-of-sample period:** Test on next 1-2 years (e.g., 2020-2021)
3. **Roll forward:** Move window, retrain on 2016-2020, test on 2021-2022
4. **Combine:** Aggregate all out-of-sample periods for true performance estimate

**Walk-Forward Efficiency (WFE):**
```
WFE = Out-of-Sample Return / In-Sample Return
```
- WFE > 50%: Good — strategy generalizes
- WFE 30-50%: Acceptable — some overfitting present
- WFE < 30%: Poor — likely overfit

#### Paper Trading Validation

Before deploying capital, paper trade for at least:
- 30 trades minimum
- 2 months minimum
- Cover at least one volatile period (expiry week, results season, RBI policy)

---

### Step 6: Evaluate Results (Deploy / Refine / Abandon)

Use the evaluation script to get an objective score:

```bash
python3 evaluate_backtest.py \
  --total-trades 150 \
  --win-rate 62 \
  --avg-win-pct 1.8 \
  --avg-loss-pct 1.2 \
  --max-drawdown-pct 15 \
  --years-tested 8 \
  --num-parameters 3 \
  --slippage-tested
```

#### Decision Framework

| Score | Verdict | Action |
|-------|---------|--------|
| **80-100** | **Deploy** | Size small initially (25% of intended), scale up over 50+ live trades |
| **60-79** | **Refine** | Identify weakest dimension, address it, re-test |
| **40-59** | **Refine with caution** | Multiple issues — may not be salvageable |
| **0-39** | **Abandon** | Fundamental edge likely does not exist. Document lessons and move on. |

#### Before Deploying

- [ ] Strategy has positive expectancy after ALL costs
- [ ] Survived parameter sensitivity testing
- [ ] Walk-forward efficiency > 50%
- [ ] Maximum drawdown is psychologically tolerable
- [ ] Sample size > 100 trades
- [ ] No more than 3-4 free parameters
- [ ] Slippage and transaction costs included
- [ ] Paper traded for 30+ trades
- [ ] Written trade plan with exact rules
- [ ] Risk management plan for live trading (position sizing, max daily loss, max drawdown circuit breaker)

---

## Using Broker MCP Tools for Backtesting Support

While the MCP tools are not backtesting engines, they support the process. Use whichever broker is connected:

### Groww MCP (if connected)
- **`fetch_historical_candle_data`**: Fetch OHLCV data for strategy development and spot-checking
- **`get_historical_technical_indicators`**: Calculate indicators (SMA, EMA, RSI, MACD, Bollinger, SuperTrend, etc.) on historical data
- **`get_historical_candlestick_patterns`**: Identify candle patterns in historical data
- **`fetch_stocks_fundamental_data`**: Screen for universe construction (PE, ROE, market cap filters)
- **`fetch_fundamentals_screener`**: Natural language screening for universe building
- **`fetch_technical_screener`**: Technical screening for strategy ideas
- **`get_ltp`**: Current price for live validation
- **`fetch_market_movers_and_trending_stocks_funds`**: Discover momentum and volume patterns

### Zerodha Kite MCP (if connected)
- **`get_historical_data`**: Fetch OHLCV candle data for strategy development
- **`get_ltp`** / **`get_quotes`**: Current prices for live validation
- **`search_instruments`**: Find instruments for universe construction
- **`get_holdings`** / **`get_positions`**: Verify live portfolio against strategy signals

---

## Quick Reference: Red Flags

| Red Flag | Why It Matters |
|----------|---------------|
| CAGR > 50% with no drawdowns | Too good to be true — check for look-ahead bias |
| Win rate > 80% | Likely not accounting for slippage or adverse fills |
| Only works on specific parameters | Overfitting — no edge, just noise |
| < 50 trades in backtest | Statistically meaningless |
| No losing months in 5+ years | Data error or survivorship bias |
| Strategy stops working after 2020 | Market structure may have changed (T+1, algo proliferation) |
| Uses > 5 parameters | Degrees of freedom too high — curve-fitted |
| No transaction costs modeled | Real returns could be negative |
| Tested on Nifty 50 only | Survivorship bias in universe selection |

---

## Files in This Skill

- `scripts/evaluate_backtest.py` — CLI scoring tool for backtest evaluation
- `references/methodology.md` — Comprehensive backtesting methodology for Indian markets
- `references/failed_tests.md` — Common failure patterns and documentation framework
