---
name: pricing-equity-options
description: Structures equity option pricing with Black-Scholes, binomial models, and implied volatility analysis. Use when pricing options, calculating Greeks, or analyzing implied volatility.
tags:
  - valuation
  - quantitative-finance
metadata:
  author: casemark
  practice_areas:
    - Derivatives
    - Quantitative Analysis
    - Structured Products
  document_types:
    - Valuation Report
  skill_modes:
    - Valuation
    - Calculation
---
# Pricing Equity Options

## When To Use

- Pricing European or American equity options (calls and puts) for valuation reports, trade analysis, or structured product design
- Calculating option Greeks (delta, gamma, theta, vega, rho) for hedging or risk management
- Extracting implied volatility from market prices to assess relative value or calibrate models
- Valuing employee stock options (ESOs) or warrant grants under ASC 718 / IFRS 2
- Building or auditing option pricing models for derivatives desks, fund managers, or corporate treasury

## Inputs To Gather

- **Underlying price (S):** Current spot price of the equity or index
- **Strike price (K):** Contract strike; confirm currency and adjustment for splits/dividends
- **Time to expiration (T):** In years; clarify calendar vs. trading days convention used
- **Risk-free rate (r):** Matching-tenor rate; typically Treasury yield or OIS rate [VERIFY jurisdiction and curve source]
- **Volatility (σ):** Historical realized vol, implied vol from market quotes, or model-calibrated vol — specify which
- **Dividend yield or schedule (q):** Continuous yield for indices; discrete dividend dates and amounts for single stocks
- **Option style:** European (exercise at expiry only) or American (early exercise permitted)
- **Exercise features:** Bermudan windows, knock-in/knock-out barriers, or other exotic terms if applicable

## Workflow

1. **Validate inputs and market data**
   - Confirm spot price source and timestamp (delayed vs. real-time)
   - Verify strike conventions (percentage of spot, absolute, adjusted for corporate actions)
   - Check dividend assumptions: use ex-dates and declared amounts for near-term; analyst estimates for longer-dated [VERIFY dividend source]
   - Select risk-free rate tenor matching option expiry; document curve date and source

2. **Select pricing model**
   - **Black-Scholes-Merton (BSM):** Default for European options on non-dividend-paying or continuous-dividend equities. Closed-form; fast for Greeks computation.
   - **BSM with discrete dividends:** Subtract PV of expected dividends from spot price, or use the Escrowed Dividend approach for near-term known dividends.
   - **Binomial tree (Cox-Ross-Rubinstein):** Required for American options where early exercise may be optimal (deep ITM puts, high-dividend calls). Use ≥100 steps for convergence; 500+ for Greeks stability.
   - **Trinomial tree:** Better convergence properties than binomial for barrier options or when computing smooth Greeks.
   - **Monte Carlo:** Use for path-dependent exotics (Asian, lookback) or when payoff cannot be handled by lattice methods. Minimum 100,000 paths with variance reduction (antithetic variates, control variates).

3. **Run pricing calculations**
   - Compute theoretical value (TV) under the selected model
   - Calculate first- and second-order Greeks:
     - **Delta (Δ):** Sensitivity to underlying price; hedge ratio
     - **Gamma (Γ):** Rate of change of delta; convexity risk
     - **Theta (Θ):** Time decay per day (specify calendar or trading day convention)
     - **Vega (ν):** Sensitivity to 1-point change in implied vol
     - **Rho (ρ):** Sensitivity to interest rate shift
   - For American options, identify the early exercise boundary and report whether early exercise is optimal at current levels

4. **Implied volatility extraction**
   - If market price is available, back-solve for implied vol using Newton-Raphson or Brent's method on the BSM formula
   - Report bid/ask implied vol separately when spread is material
   - Construct vol smile or surface if multiple strikes/expiries are available — note skew and term structure features
   - Compare implied vol to realized vol (20-day, 60-day, 252-day) to flag rich/cheap assessment

5. **Cross-validate results**
   - Put-call parity check: C − P = S·e^(−qT) − K·e^(−rT) (European). Deviations beyond 1–2 cents indicate input or model error.
   - Compare model price to market mid-price; explain residual as model risk, liquidity premium, or data staleness
   - Sensitivity/scenario analysis: reprice at ±1σ underlying move, ±5 vol points, ±50 bps rate shift
   - For American options, confirm binomial price ≥ BSM price (early exercise premium must be non-negative)

## Output

Structure the deliverable as a **Valuation Report** containing:

- **Summary table:** Option terms, model used, theoretical value, market price (if available), implied vol
- **Greeks table:** All first- and second-order Greeks with units clearly labeled
- **Assumptions & inputs:** Spot source/date, vol type and lookback, rate curve, dividend treatment
- **Sensitivity matrix:** Option value across a grid of spot prices (rows) and volatilities (columns)
- **Model commentary:** Why the selected model is appropriate; known limitations (e.g., BSM assumes constant vol, log-normal returns, no jumps)
- **Early exercise analysis** (American only): Boundary level and whether current conditions favor early exercise

## Quality Checks

- Greeks satisfy finite-difference consistency: e.g., delta from bumping spot ±$0.01 matches analytical delta within tolerance
- Implied vol solver converges (residual < $0.001); flag if vol is negative or unreasonably high (>200%)
- Put-call parity holds within bid-ask spread for European options
- Binomial tree price converges as steps increase (compare 100 vs. 500 vs. 1000 steps)
- All rates, yields, and times are on consistent day-count and compounding conventions [VERIFY ACT/365 vs. ACT/360 vs. 30/360]
- Dividend assumptions match between pricing model and Greeks computation
- Report carries appropriate disclaimer: model output is not a trade recommendation; actual execution prices depend on liquidity, market conditions, and counterparty terms
