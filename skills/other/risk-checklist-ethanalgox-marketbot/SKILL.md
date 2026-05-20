---
name: risk-checklist
description: Generate a trade risk checklist and position-sizing guidance.
metadata:
  {
    "marketbot": {
      "emoji": "compass"
    }
  }
---

# Risk Checklist

Create a risk checklist for a proposed trade or market view.

## When to use
- User asks "is this trade safe", "risk check", or "position size".
- You are about to propose entries/targets and need guardrails.

## Inputs to confirm (ask if missing)
- Asset + market
- Timeframe
- Entry idea (if any)
- Risk tolerance (low/medium/high)
- Account constraints (optional: max loss %, leverage limits)

## Checklist (cover all)
- Regime risk (range vs trend)
- Volatility state and typical ATR move
- Liquidity/slippage risk
- Event/catalyst risk (earnings, macro, protocol upgrades)
- Correlation risk (beta to index/ETH/BTC/DXY)
- Time-based risk (holding across sessions/weekends)
- Execution risk (spreads, funding, gaps)

## Output format (markdown)
```
# Risk Checklist: <ASSET>

## Risk Summary
- Overall risk: Low/Medium/High
- Key blockers:

## Checklist
- Regime fit: ✅/⚠️/❌
- Volatility: ✅/⚠️/❌
- Liquidity: ✅/⚠️/❌
- Event risk: ✅/⚠️/❌
- Correlation: ✅/⚠️/❌
- Time risk: ✅/⚠️/❌
- Execution: ✅/⚠️/❌

## Position Sizing (guidance)
- Suggested size: Small/Normal/Reduced
- Max loss per trade (%):
- Invalidation level:

> Disclaimer: MarketBot provides research/analysis only. Not financial advice.
```
