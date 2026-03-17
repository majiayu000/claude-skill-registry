---
name: stock-analysis
description: Run comprehensive stock analysis workflows combining fundamental, technical, and sentiment analysis. Use when analyzing individual stocks, generating recommendations, or running batch analysis. Trigger on stock analysis, recommendation, or valuation discussions.
metadata: {"clawdbot":{"emoji":"📈","project":"investment-analysis-platform"}}
---

# Stock Analysis Skill

Comprehensive stock analysis combining fundamental, technical, and ML-based sentiment analysis.

## Quick Analysis Commands

### Single Stock Analysis

```bash
# Run full analysis for a single stock
python -c "
from backend.services.analysis import StockAnalyzer

analyzer = StockAnalyzer()
result = analyzer.analyze('AAPL')

print(f'''
=== {result.ticker} Analysis ===

RECOMMENDATION: {result.recommendation}
Confidence: {result.confidence:.1%}
Target Price: \${result.target_price:.2f}

Fundamental Score: {result.fundamental_score:.2f}/10
Technical Score: {result.technical_score:.2f}/10
Sentiment Score: {result.sentiment_score:.2f}/10

Key Thesis:
{result.thesis}

Risk Factors:
{chr(10).join(f\"  - {r}\" for r in result.risk_factors)}
''')
"
```

### Batch Analysis

```bash
# Analyze multiple stocks
python -c "
from backend.services.analysis import BatchAnalyzer

analyzer = BatchAnalyzer()
results = analyzer.analyze_batch(['AAPL', 'GOOGL', 'MSFT', 'AMZN'])

for r in results:
    print(f'{r.ticker}: {r.recommendation} ({r.confidence:.0%})')
"
```

## Analysis Components

### 1. Fundamental Analysis

```python
from backend.analysis.fundamental import FundamentalAnalyzer

fa = FundamentalAnalyzer()
metrics = fa.analyze('AAPL')

# Key metrics calculated:
# - P/E Ratio (trailing and forward)
# - P/B Ratio
# - EV/EBITDA
# - Debt/Equity
# - Current Ratio
# - ROE, ROA, ROI
# - Piotroski F-Score
# - Altman Z-Score
```

### 2. Technical Analysis

```python
from backend.analysis.technical import TechnicalAnalyzer

ta = TechnicalAnalyzer()
signals = ta.analyze('AAPL', period='1y')

# Indicators calculated:
# - Moving Averages (SMA 20, 50, 200)
# - MACD (12, 26, 9)
# - RSI (14)
# - Bollinger Bands
# - Support/Resistance levels
# - Volume analysis
```

### 3. Sentiment Analysis

```python
from backend.analysis.sentiment import SentimentAnalyzer

sa = SentimentAnalyzer()
sentiment = sa.analyze('AAPL')

# Sources analyzed:
# - News articles (FinBERT)
# - Social media mentions
# - Analyst ratings
# - Earnings call transcripts
```

## Analysis Pipeline

```
Input: Ticker Symbol
         │
         ▼
┌─────────────────────────────────────────────┐
│              Data Collection                │
│  ├── Price data (Finnhub/Polygon)          │
│  ├── Fundamentals (Alpha Vantage)          │
│  ├── News (NewsAPI)                        │
│  └── Filings (SEC EDGAR)                   │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│              Analysis Layer                 │
│  ├── Fundamental Analysis  ──────┐         │
│  ├── Technical Analysis    ──────┼──► ML   │
│  └── Sentiment Analysis    ──────┘  Model  │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│           Recommendation Engine             │
│  ├── Score aggregation                     │
│  ├── Confidence calculation                │
│  ├── Target price estimation               │
│  └── Risk factor identification            │
└─────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────┐
│           SEC Compliance Check              │
│  ├── Add required disclosures              │
│  ├── Generate audit log                    │
│  └── Validate output format                │
└─────────────────────────────────────────────┘
         │
         ▼
Output: Compliant Recommendation
```

## Recommendation Scoring

```python
# Scoring weights (configurable)
WEIGHTS = {
    "fundamental": 0.35,
    "technical": 0.30,
    "sentiment": 0.20,
    "momentum": 0.15,
}

def calculate_recommendation(scores: dict) -> tuple[str, float]:
    """
    Calculate final recommendation from component scores.

    Returns: (recommendation, confidence)
    """
    weighted_score = sum(
        scores[k] * WEIGHTS[k]
        for k in WEIGHTS
    )

    if weighted_score >= 7.0:
        return ("STRONG BUY", min(weighted_score / 10, 0.95))
    elif weighted_score >= 5.5:
        return ("BUY", weighted_score / 10)
    elif weighted_score >= 4.5:
        return ("HOLD", 0.5)
    elif weighted_score >= 3.0:
        return ("SELL", (10 - weighted_score) / 10)
    else:
        return ("STRONG SELL", min((10 - weighted_score) / 10, 0.95))
```

## Key Metrics Reference

### Fundamental Metrics

| Metric | Good | Neutral | Poor |
|--------|------|---------|------|
| P/E Ratio | < 15 | 15-25 | > 25 |
| P/B Ratio | < 1.5 | 1.5-3 | > 3 |
| Debt/Equity | < 0.5 | 0.5-1.5 | > 1.5 |
| Current Ratio | > 2 | 1-2 | < 1 |
| ROE | > 15% | 10-15% | < 10% |
| Piotroski F | 7-9 | 4-6 | 0-3 |

### Technical Signals

| Indicator | Bullish | Bearish |
|-----------|---------|---------|
| Price vs SMA200 | Above | Below |
| MACD | Positive crossover | Negative crossover |
| RSI | < 30 (oversold) | > 70 (overbought) |
| Volume | Increasing on up days | Increasing on down days |

## Usage Examples

### Compare Stocks

```python
from backend.services.analysis import ComparisonAnalyzer

comp = ComparisonAnalyzer()
result = comp.compare(['AAPL', 'MSFT', 'GOOGL'])

print("Ranking by overall score:")
for stock in result.ranked:
    print(f"  {stock.ticker}: {stock.score:.2f}")
```

### Sector Analysis

```python
from backend.services.analysis import SectorAnalyzer

sector = SectorAnalyzer()
tech_stocks = sector.analyze_sector('Technology', top_n=10)

print("Top 10 Technology stocks:")
for stock in tech_stocks:
    print(f"  {stock.ticker}: {stock.recommendation}")
```

### Portfolio Screening

```python
from backend.services.screening import StockScreener

screener = StockScreener()
results = screener.screen({
    "pe_ratio": {"max": 20},
    "roe": {"min": 15},
    "debt_equity": {"max": 1},
    "market_cap": {"min": 10_000_000_000},  # $10B+
})

print(f"Found {len(results)} stocks matching criteria")
```

## Best Practices

1. **Always check data freshness** before analysis
2. **Use caching** to minimize API calls
3. **Run batch analysis** during off-hours
4. **Validate with SEC compliance** before publishing
5. **Log all recommendations** for audit trail
6. **Consider market conditions** in recommendations
