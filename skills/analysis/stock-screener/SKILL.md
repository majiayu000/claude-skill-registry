---
name: stock-screener
description: Filter and screen stocks by financial metrics like P/E ratio, market cap, dividend yield, and growth rates. Analyze and compare stocks from CSV data.
---

# Stock Screener

Filter stocks by financial metrics and perform comparative analysis.

## Features

- **Multi-Metric Filtering**: P/E, P/B, market cap, dividend yield, etc.
- **Custom Screens**: Save and reuse filter combinations
- **Comparative Analysis**: Side-by-side stock comparison
- **Sector Analysis**: Group and analyze by sector
- **Ranking**: Score and rank stocks by criteria
- **Export**: CSV, JSON, formatted reports

## Quick Start

```python
from stock_screener import StockScreener

screener = StockScreener()

# Load stock data
screener.load_csv("stocks.csv")

# Apply filters
results = screener.filter(
    pe_ratio=(0, 20),
    market_cap_min=1e9,
    dividend_yield_min=2.0
)

print(results)
```

## CLI Usage

```bash
# Basic screening
python stock_screener.py --input stocks.csv --pe-max 20 --div-min 2.0

# Multiple filters
python stock_screener.py --input stocks.csv --pe 5 25 --pb-max 3 --cap-min 1B

# Sector filter
python stock_screener.py --input stocks.csv --sector Technology --pe-max 30

# Rank by metric
python stock_screener.py --input stocks.csv --rank-by dividend_yield --top 20

# Compare specific stocks
python stock_screener.py --input stocks.csv --compare AAPL MSFT GOOGL

# Export results
python stock_screener.py --input stocks.csv --pe-max 15 --output screened.csv
```

## Input Format

### Stock CSV
```csv
symbol,name,sector,price,pe_ratio,pb_ratio,market_cap,dividend_yield,eps,revenue_growth,profit_margin
AAPL,Apple Inc,Technology,175.50,28.5,45.2,2.8e12,0.5,6.16,8.5,25.3
MSFT,Microsoft,Technology,380.00,35.2,12.8,2.8e12,0.8,10.79,12.3,36.7
JNJ,Johnson & Johnson,Healthcare,155.00,15.2,5.8,3.8e11,2.9,10.20,5.2,22.1
```

## API Reference

### StockScreener Class

```python
class StockScreener:
    def __init__(self)

    # Data Loading
    def load_csv(self, filepath: str) -> 'StockScreener'
    def load_dataframe(self, df: pd.DataFrame) -> 'StockScreener'

    # Filtering
    def filter(self, **criteria) -> pd.DataFrame
    def filter_by_sector(self, sectors: List[str]) -> 'StockScreener'
    def filter_by_metric(self, metric: str, min_val: float = None,
                         max_val: float = None) -> 'StockScreener'

    # Screening Presets
    def value_screen(self) -> pd.DataFrame
    def growth_screen(self) -> pd.DataFrame
    def dividend_screen(self) -> pd.DataFrame
    def quality_screen(self) -> pd.DataFrame
    def custom_screen(self, criteria: Dict) -> pd.DataFrame

    # Analysis
    def compare(self, symbols: List[str]) -> pd.DataFrame
    def rank_by(self, metric: str, ascending: bool = True) -> pd.DataFrame
    def sector_summary(self) -> pd.DataFrame
    def metric_distribution(self, metric: str) -> Dict

    # Scoring
    def score_stocks(self, weights: Dict[str, float] = None) -> pd.DataFrame
    def percentile_rank(self, metrics: List[str]) -> pd.DataFrame

    # Export
    def to_csv(self, filepath: str) -> str
    def to_json(self, filepath: str) -> str
    def summary_report(self) -> str
```

## Filtering Criteria

### Valuation Metrics
```python
screener.filter(
    pe_ratio=(5, 20),      # P/E between 5 and 20
    pb_ratio_max=3.0,      # P/B ratio under 3
    ps_ratio_max=5.0,      # Price/Sales under 5
    peg_ratio_max=1.5      # PEG ratio under 1.5
)
```

### Size Metrics
```python
screener.filter(
    market_cap_min=1e9,    # Min $1B market cap
    market_cap_max=10e9,   # Max $10B (mid-cap)
    revenue_min=500e6      # Min $500M revenue
)
```

### Income Metrics
```python
screener.filter(
    dividend_yield_min=2.0,  # Min 2% dividend
    dividend_yield_max=8.0,  # Max 8% (avoid yield traps)
    payout_ratio_max=75      # Sustainable payout
)
```

### Growth Metrics
```python
screener.filter(
    revenue_growth_min=10,   # Min 10% revenue growth
    earnings_growth_min=15,  # Min 15% earnings growth
    eps_growth_min=10        # Min 10% EPS growth
)
```

### Quality Metrics
```python
screener.filter(
    profit_margin_min=15,    # Min 15% profit margin
    roe_min=15,              # Min 15% return on equity
    debt_to_equity_max=1.0,  # Max 1.0 D/E ratio
    current_ratio_min=1.5    # Min 1.5 current ratio
)
```

## Preset Screens

### Value Screen
```python
results = screener.value_screen()
# Finds undervalued stocks:
# - P/E < 15
# - P/B < 2
# - Dividend yield > 2%
# - Profit margin > 10%
```

### Growth Screen
```python
results = screener.growth_screen()
# Finds growth stocks:
# - Revenue growth > 15%
# - Earnings growth > 20%
# - PEG ratio < 2
```

### Dividend Screen
```python
results = screener.dividend_screen()
# Finds dividend stocks:
# - Dividend yield 2-8%
# - Payout ratio < 75%
# - 5+ years dividend history
```

### Quality Screen
```python
results = screener.quality_screen()
# Finds high-quality stocks:
# - ROE > 15%
# - Profit margin > 15%
# - D/E < 0.5
# - Current ratio > 2
```

## Stock Comparison

```python
comparison = screener.compare(["AAPL", "MSFT", "GOOGL"])
# Returns:
#                  AAPL    MSFT    GOOGL
# price           175.50  380.00  140.00
# pe_ratio        28.50   35.20   25.30
# market_cap      2.8T    2.8T    1.7T
# dividend_yield  0.50    0.80    0.00
# profit_margin   25.30   36.70   22.50
# ...
```

## Ranking and Scoring

### Rank by Single Metric
```python
# Top 20 by dividend yield
top_dividend = screener.rank_by("dividend_yield", ascending=False).head(20)
```

### Composite Scoring
```python
# Score stocks with custom weights
scores = screener.score_stocks({
    "pe_ratio": -0.2,        # Lower is better
    "dividend_yield": 0.3,   # Higher is better
    "profit_margin": 0.3,    # Higher is better
    "revenue_growth": 0.2    # Higher is better
})
# Returns stocks ranked by composite score
```

### Percentile Ranking
```python
# See where each stock ranks on multiple metrics
ranked = screener.percentile_rank(["pe_ratio", "dividend_yield", "profit_margin"])
# Returns percentile (0-100) for each metric
```

## Sector Analysis

```python
sector_stats = screener.sector_summary()
# Returns:
#   sector        | count | avg_pe | avg_div | avg_margin
#   Technology    | 45    | 28.5   | 1.2     | 22.3
#   Healthcare    | 32    | 18.2   | 2.1     | 18.7
#   Financials    | 28    | 12.5   | 3.2     | 25.1
```

## Example Workflows

### Find Undervalued Dividend Stocks
```python
screener = StockScreener()
screener.load_csv("sp500.csv")

# Apply filters
results = screener.filter(
    pe_ratio=(5, 15),
    dividend_yield_min=3.0,
    payout_ratio_max=70,
    profit_margin_min=10
)

# Rank by dividend yield
top = results.sort_values("dividend_yield", ascending=False).head(10)
print(top[["symbol", "name", "pe_ratio", "dividend_yield", "payout_ratio"]])
```

### Growth at Reasonable Price (GARP)
```python
results = screener.filter(
    revenue_growth_min=15,
    earnings_growth_min=15,
    peg_ratio_max=1.5,
    pe_ratio_max=25
)
```

### Sector Comparison
```python
# Filter to technology sector
tech = screener.filter_by_sector(["Technology"]).filter(
    market_cap_min=10e9,
    profit_margin_min=15
)

# Compare top tech stocks
comparison = screener.compare(tech["symbol"].head(5).tolist())
```

## Output Format

### CSV Export
```python
screener.filter(pe_ratio_max=20).to_csv("value_stocks.csv")
```

### JSON Export
```python
screener.filter(dividend_yield_min=3).to_json("dividend_stocks.json")
```

### Summary Report
```python
report = screener.summary_report()
# Returns formatted text summary of screening results
```

## Dependencies

- pandas>=2.0.0
- numpy>=1.24.0
