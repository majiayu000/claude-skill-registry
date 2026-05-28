---
name: Flows Watch (ETF/Derivatives)
description: Summarize ETF net flows and derivatives context (OI Δ, funding, basis, skew, liquidation bands) from local JSON/CSV drops. Use at open/close or when assessing leverage resets.
allowed-tools: Read, Grep, Glob
---

# Flows Watch

## Instructions
1) Read latest files:
   - data/derivs/*.json
   - data/etf/*.csv
2) Extract: ETF_net($), BTC_OI_Δ%, ETH_OI_Δ%, Funding (sign+magnitude), Basis (annualized), 25Δ skew,
   Largest liquidation price bands (range + est. size).
3) Output a compact dashboard + three scenarios (bull/bear/base) ≤60 words.
4) Tag "Leverage Reset" if OI −15% in 24h or liquidations > $3B with funding flip neg→pos.
