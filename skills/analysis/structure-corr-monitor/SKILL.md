---
name: Structure & Correlation Monitor (Crypto Rotation)
description: Compute rolling 6h/1D correlations and betas vs BTC from local OHLCV CSVs, plus 4H CoC and 1H VWAP status. Use when the user requests rotation eligibility or structure checks.
allowed-tools: Read, Grep, Glob
---

# Structure & Correlation Monitor

## Instructions
1) Load CSVs from data/ohlcv/1h/*.csv for: BTC, ETH, SOL, ADA, ZEC, DASH, PAXG.
   Columns: timestamp, open, high, low, close, volume.
2) Calculate hourly-returns:
   - Pearson correlations: 6h (window=6 bars) and 1D (window=24 bars), EWMA λ=0.94.
   - Rolling OLS beta: β_ALT,BTC (same window + EWMA).
   - 4H Change-of-Character (HH/HL or LL/LH from swing pivots).
   - 1H VWAP reclaim + retest/hold (above/below; hold true/false).
3) Emit JSON:
   {"corr6h":{}, "corr1d":{}, "beta":{},
    "structure":{"btc":{"coc":"up|down|none","vwap_hold":true|false},
                 "ethbtc_slope":"up|down|flat","btcd_slope":"up|down|flat"},
    "eligibility":{"btc_probe":bool,"btc_add":bool,"alt_sleeve":bool,"counterbeta_sleeve":bool},
    "notes":["..."]}
4) Eligibility:
   - btc_probe = true if ≥3 of: 4H CoC up, 1H VWAP hold, MACD 1H>0, 60/10 stoch curl up, ETHBTC slope ≥0.
   - alt_sleeve = true if 6h |ρ(BTC,ALT)|≥0.7 AND 1D ≥0.6 AND ETHBTC slope ≥0.
   - counterbeta_sleeve = true if 6h ρ≤-0.4 AND that alt shows independent 4H momentum.
