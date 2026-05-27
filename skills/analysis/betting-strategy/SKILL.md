---
name: betting-strategy
description: Details the core betting strategy, including edge calculation, sport-specific thresholds, Kelly Criterion sizing, and portfolio optimization.
version: 1.0.0
---

# Betting Strategy

## Edge Calculation

```python
edge = elo_probability - market_probability
```

A bet is recommended when:
1. `elo_prob > threshold` (high confidence)
2. `edge > 0.05` (5%+ edge over market)

## Sport Thresholds

| Sport | Threshold | Min Edge | Notes |
|-------|-----------|----------|-------|
| NBA   | 73%       | 5%       | High-scoring, predictable |
| NHL   | 66%       | 5%       | High variance sport |
| MLB   | 67%       | 5%       | Lower home advantage |
| NFL   | 70%       | 5%       | Small sample size |

## Confidence Levels

```python
def get_confidence(elo_prob, threshold):
    if elo_prob > threshold + 0.10:
        return "HIGH"
    elif elo_prob > threshold:
        return "MEDIUM"
    return None  # Don't bet
```

## Lift/Gain Analysis

Validate model quality by decile:

```python
from lift_gain_analysis import analyze_sport

overall, current = analyze_sport('nba')

# Key metrics:
# - Lift > 1.0: Better than random
# - Top decile lift > 1.3: Strong signal
# - Gain %: Cumulative wins captured
```

**Interpretation:**
- Decile 10 (highest prob): Should have highest lift
- If lift < 1.0 in high deciles, model is miscalibrated
- Set threshold where lift starts exceeding 1.2-1.3

## Kelly Criterion

Optimal bet sizing:

```python
def kelly_fraction(win_prob, odds):
    """Calculate Kelly bet fraction."""
    # odds in decimal format (2.0 = even money)
    q = 1 - win_prob
    b = odds - 1
    return (win_prob * b - q) / b

# Use fractional Kelly (25-50%) to reduce variance
bet_fraction = kelly_fraction(prob, odds) * 0.25
```

## Portfolio Optimization

```python
from portfolio_optimizer import optimize_bets

# Optimize across all opportunities
optimized = optimize_bets(
    opportunities=bets,
    bankroll=1000,
    max_exposure=0.10,  # 10% max per bet
    correlation_penalty=0.5  # Reduce correlated bets
)
```

## Bet Tracking

All bets saved to `placed_bets` table:

```python
default_db.execute("""
    INSERT INTO placed_bets
    (bet_id, game_id, sport, ticker, side, amount, price, elo_prob, edge, placed_at)
    VALUES (...)
""")
```

## CLV (Closing Line Value)

Track if we beat the closing line:

```python
from clv_tracker import calculate_clv

clv = calculate_clv(bet_id)
# Positive CLV = consistently beating market
```

## Files to Reference

- `plugins/portfolio_optimizer.py` - Kelly and optimization
- `plugins/lift_gain_analysis.py` - Model validation
- `plugins/clv_tracker.py` - CLV tracking
- `docs/VALUE_BETTING_THRESHOLDS.md` - Threshold analysis
