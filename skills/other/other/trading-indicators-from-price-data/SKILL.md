---
name: trading-indicators-from-price-data
description: Compute common trading indicators from OHLCV price data for analysis and strategy development.
---

# Trading Indicators from Price Data (20 common indicators)

Calculate 20 widely used trading indicators from OHLCV candles (open, high, low, close, volume) using Python.

This skill is useful for:
- signal generation
- strategy backtesting
- feature engineering for ML models
- market condition dashboards

## Requirements

Install dependencies:

```bash
pip install pandas pandas-ta
```

Input data must include these columns:
- `open`
- `high`
- `low`
- `close`
- `volume`

## 20 indicators included

1. RSI (14)
2. MACD line (12,26)
3. MACD signal (9)
4. MACD histogram
5. SMA (20)
6. SMA (50)
7. EMA (20)
8. EMA (50)
9. WMA (20)
10. Bollinger upper band (20,2)
11. Bollinger middle band (20,2)
12. Bollinger lower band (20,2)
13. Stochastic %K (14,3,3)
14. Stochastic %D (14,3,3)
15. ATR (14)
16. ADX (14)
17. CCI (20)
18. OBV
19. MFI (14)
20. ROC (12)

## Notes

- Indicators need warmup candles (first rows can be `NaN`).
- For stable output, use at least 200 candles.
- If you run this on minute candles, indicators are intraday; on daily candles, they are swing/position oriented.

## Agent prompt

```text
You have a trading-indicators skill.

When given OHLCV price data, calculate the following 20 indicators:
RSI(14), MACD line/signal/histogram (12,26,9), SMA(20), SMA(50), EMA(20), EMA(50), WMA(20),
Bollinger upper/middle/lower (20,2), Stoch %K/%D (14,3,3), ATR(14), ADX(14), CCI(20), OBV, MFI(14), ROC(12).

Return a table with the latest value of each indicator and include the last 50 rows when requested.
If data is insufficient, ask for more candles.
```
