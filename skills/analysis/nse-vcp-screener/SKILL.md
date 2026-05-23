---
name: nse-vcp-screener
description: Screen Nifty 500 stocks for Mark Minervini's Volatility Contraction Pattern (VCP) — identifying Stage 2 uptrends with tightening price ranges and declining volume before potential breakouts. Use this skill when the user requests VCP screening, Minervini-style setups, Stage 2 breakout candidates, or volatility contraction patterns on NSE/BSE stocks.
---

# NSE VCP Screener

## Overview

This skill screens Indian stocks (Nifty 50/200/500) for Mark Minervini's Volatility Contraction Pattern (VCP). The VCP identifies stocks in Stage 2 uptrends that are forming tightening bases with declining volume — the classic setup before a potential breakout.

The screening pipeline has 3 phases:
1. **Pre-filter**: Quick quote-based filtering to eliminate obvious non-candidates
2. **Trend Template**: Apply Minervini's 7-point Stage 2 criteria using 260-day histories
3. **VCP Detection & Scoring**: Pattern analysis with 5-component composite scoring

## Data Source

This screener uses **yfinance** with `.NS` suffix for NSE stocks and the **niftystocks** package for stock universe lists. No paid API keys required.

## Execution

```bash
python3 scripts/screen_vcp.py --universe nifty500
```

### Command-Line Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--universe` | `nifty50` | Stock universe: `nifty50`, `nifty200`, `nifty500`, or `custom` |
| `--custom-tickers` | — | Comma-separated tickers for custom universe (e.g., `RELIANCE,TCS,INFY`) |
| `--min-contractions` | `2` | Minimum number of contractions (2-4) |
| `--t1-depth-min` | `10` | Minimum T1 contraction depth % |
| `--t1-depth-max` | `40` | Maximum T1 contraction depth % |
| `--contraction-ratio` | `0.75` | Each contraction must be ≤ this ratio of the previous |
| `--min-contraction-days` | `5` | Minimum days per contraction |
| `--lookback-days` | `120` | Days to look back for pattern detection |
| `--breakout-volume-ratio` | `1.5` | Minimum volume ratio for breakout confirmation |
| `--trend-min-score` | `85` | Minimum trend template score (0-100) |
| `--output-dir` | `reports/` | Output directory for results |

## Workflow

### Step 1: Execute the Screener

Run the Python script with desired parameters:

```bash
python3 skills/nse-vcp-screener/scripts/screen_vcp.py \
  --universe nifty500 \
  --output-dir reports/
```

### Step 2: Review Results

Load and review the generated reports:
- **JSON**: `reports/vcp_screener_YYYY-MM-DD_HHMMSS.json` (structured data)
- **Markdown**: `reports/vcp_screener_YYYY-MM-DD_HHMMSS.md` (human-readable report)

### Step 3: Load References for Interpretation

```
Read: references/vcp_methodology.md
Read: references/scoring_system.md
```

### Step 4: Present Top Candidates

For each top-scoring candidate, present:
1. **Composite Score** (0-100)
2. **Contraction Structure** (T1/T2/T3 depths and durations)
3. **Volume Pattern** (dry-up ratio)
4. **Pivot Level** (breakout price)
5. **Relative Strength** vs Nifty 50

### Step 5: Actionable Insights

For the top 5-10 candidates:
- Note proximity to pivot/breakout level
- Assess if volume is confirming or diverging
- Check for upcoming F&O expiry or result season impacts
- Identify F&O lot size (if stock is in F&O segment)

## Scoring System

The composite score (0-100) weights 5 components:

| Component | Weight | What It Measures |
|-----------|--------|-----------------|
| Trend Template | 25% | Minervini's 7-point Stage 2 criteria |
| Contraction Quality | 25% | Tightening base structure |
| Volume Pattern | 20% | Volume dry-up ratio |
| Pivot Proximity | 15% | Distance from breakout level |
| Relative Strength | 15% | Performance vs Nifty 50 |

## Indian Market Adaptations

- **Universe**: Nifty 50/200/500 instead of S&P 500
- **Benchmark**: Relative strength measured vs Nifty 50 (^NSEI) instead of S&P 500
- **Volatility**: T1 depth range widened to 10-40% (vs 8-35% for US) due to higher small-cap volatility
- **Circuit Limits**: Stocks hitting circuits may show false VCP patterns — flagged in results
- **Liquidity Filter**: Minimum average daily volume of ₹1 crore to filter illiquid stocks
- **F&O Availability**: Results indicate whether the stock is in the F&O segment

## Resources

### references/vcp_methodology.md
Mark Minervini's VCP theory, Stage 2 criteria, contraction rules, and entry methodology adapted for Indian markets.

### references/scoring_system.md
Detailed breakdown of the 5-component composite scoring system with thresholds and examples.
