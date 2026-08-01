---
name: liquidity-depth-analyzer
description: 'DEX liquidity analysis and slippage estimation for MEV trading. Use
  when implementing swaps, route selection, or position sizing. Triggers on: liquidity,
  slippage, price impact, depth, AMM math, Unisw'
---

---
name: liquidity-depth-analyzer
description: DEX liquidity analysis and slippage estimation for MEV trading. Use when implementing swaps, route selection, or position sizing. Triggers on: liquidity, slippage, price impact, depth, AMM math, Uniswap, Curve.
---

# Liquidity Depth Analyzer

DEX liquidity analysis and slippage estimation for MEV trading.

## When to Use

- Implementing swap execution
- Selecting optimal routes
- Sizing positions for trades
- Calculating price impact
- Validating arbitrage profitability

## Workflow

### Step 1: Check Liquidity Depth

Verify depth >= 3x trade size.

### Step 2: Calculate Price Impact

Ensure impact < 0.5% (50 bps).

### Step 3: Validate Profit After Slippage

Confirm profit survives slippage tolerance.

---

## Core Rule

**Never execute without knowing:**
1. Available liquidity at current price
2. Price impact for your size
3. Whether profit survives slippage

## Key Formulas
price_impact_bps = |1 - (in/out) / spot| × 10000
minAmountOut = expected × (1 - slippage_bps / 10000)

## Config
```typescript
const config = {
  max_price_impact_bps: 50,   // 0.5%
  max_slippage_bps: 100,      // 1%
  min_depth_multiplier: 3,    // depth >= 3x trade
};
```

## Abort Reasons

| Code | Action |
|------|--------|
| NO_POOL | Find alternative route |
| LOW_DEPTH | Reduce size or split |
| HIGH_PRICE_IMPACT | Reduce size |
| LOW_PROFIT | Skip opportunity |
