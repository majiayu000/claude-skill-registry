---
name: claw-betting-ai
description: AI-powered betting advisory for gaming platforms. Provides intelligent bet recommendations, risk analysis, bankroll management, and strategy optimization for crash games, dice, and casino games. Use when building automated betting bots or need AI gambling strategy guidance.
website: https://clawde.xyz
---

# CLAW Betting AI Advisory

AI-powered betting advisory system for gaming platforms like Stake.com. Provides intelligent recommendations based on historical data analysis, risk tolerance, and proven betting strategies.

**Website**: https://clawde.xyz

## Features

- **Smart Bet Recommendations**: AI-analyzed optimal bet amounts and timing
- **Crash Game Analysis**: Historical pattern analysis for crash games
- **Risk Management**: Dynamic stop-loss and take-profit suggestions
- **Bankroll Protection**: Kelly Criterion and flat betting strategies
- **Multi-Strategy Support**: Martingale, Anti-Martingale, Fibonacci, D'Alembert

## Quick Start

```bash
# Install the skill
clawhub install claw-betting-ai

# Configure your settings
cp config/default.json config/local.json
# Edit config/local.json with your preferences
```

## Supported Games

| Game | Analysis Method |
|------|-----------------|
| Crash | Historical crashpoint analysis, multiplier patterns |
| Dice | Probability optimization, streak detection |
| Limbo | Target multiplier recommendations |
| Slide | Pattern recognition |

## Files Included

```
claw-betting-ai/
├── SKILL.md              # This file
├── config/
│   └── default.json      # Default configuration
├── scripts/
│   ├── analyze.py        # Crash history analyzer
│   └── recommend.py      # Bet recommendation engine
└── examples/
    ├── basic-usage.md    # Getting started guide
    └── strategies.md     # Strategy documentation
```

## Configuration

See `config/default.json` for all available options:

- `strategy`: betting strategy (conservative/balanced/aggressive)
- `bankroll`: starting bankroll amount
- `baseBetPercent`: base bet as % of bankroll
- `stopLoss`: stop-loss threshold
- `takeProfit`: take-profit target
- `maxBets`: maximum bets per session

## Core Strategies

### 1. Conservative (Low Risk)
- Target: 1.5x - 2x multipliers
- Win rate: ~50-65%
- Max 1% bankroll per bet

### 2. Balanced (Medium Risk)
- Target: 2x - 5x multipliers
- Win rate: ~25-45%
- Max 2% bankroll per bet

### 3. Aggressive (High Risk)
- Target: 5x - 20x multipliers
- Win rate: ~5-15%
- Max 5% bankroll per bet

## API Reference

See `examples/basic-usage.md` for full API documentation.

### Get Recommendation
```python
from scripts.recommend import get_recommendation

result = get_recommendation(
    bankroll=100,
    strategy="balanced",
    recent_history=[1.2, 3.5, 1.8, 2.1, 5.2]
)
# Returns: { shouldBet: true, amount: 2.0, target: 2.5, confidence: 72 }
```

## Safety Features

- **Tilt Detection**: Warns when betting patterns indicate emotional decisions
- **Session Limits**: Enforces time and loss limits
- **Profit Locking**: Auto-protects portion of winnings
- **Reality Checks**: Periodic reminders

## Disclaimer

This is an advisory system only. Gambling involves risk of loss. Never bet more than you can afford to lose. Past patterns do not guarantee future results.

## Links

- Website: https://clawde.xyz
- Support: Contact via website
