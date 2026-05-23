---
name: "trading-signals"
description: "Technical analysis patterns - Elliott Wave, Wyckoff, Fibonacci, Markov Regime, and Turtle Trading with confluence detection. Use when analyzing charts, identifying trading signals, or calculating technical levels."
---

<objective>
Provide standardized technical analysis patterns for trading projects, combining Elliott Wave, Wyckoff, Fibonacci, Markov Regime, and Turtle Trading methodologies. Enables confluence detection through regime-weighted methodology fusion and cost-effective multi-LLM consensus.
</objective>

<quick_start>
**Confluence analysis (methodologies agree = high-probability setup):**
```python
score = sum(signal.strength * weights[signal.method] for signal in signals)
action = 'BUY' if score >= 0.7 else 'WAIT'
```

**Score interpretation:**
- 0.7-1.0: High conviction entry
- 0.4-0.7: Wait for more confluence
- 0.0-0.4: No trade

**Cost-effective routing:** DeepSeek-V3 for pattern detection → Claude Sonnet for critical decisions
</quick_start>

<success_criteria>
Analysis is successful when:
- Multiple methodologies provide signals (not just one)
- Regime identified (trending/ranging/volatile) before analysis
- Confluence score calculated with regime-weighted methodology fusion
- Cost-optimized: bulk processing on DeepSeek, critical decisions on Claude
- Clear action (BUY/SELL/WAIT) with supporting rationale
- NO OPENAI used in model routing
</success_criteria>

<core_patterns>
Standardized patterns for technical analysis across trading projects.

## Quick Reference

| Methodology | Purpose | When to Use |
|-------------|---------|-------------|
| Elliott Wave | Wave position + targets | Trend structure, cycle timing |
| Turtle Trading | Breakout system | Trend following |
| Fibonacci | Support/resistance | Entry/exit zones, golden pocket |
| Wyckoff | Accumulation/distribution | Institutional activity |
| Markov Regime | Market state classification | Position sizing, strategy selection |
| Pattern Recognition | Candlestick + chart patterns | Entry confirmation |
| Swarm Consensus | Multi-LLM voting | High-conviction decisions |

## Confluence Detection

When methodologies agree = high-probability setup.

```python
class ConfluenceAnalyzer:
    """Regime-weighted methodology fusion"""

    REGIME_WEIGHTS = {
        'trending_up':   {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
        'trending_down': {'elliott': 0.30, 'turtle': 0.30, 'fib': 0.20, 'wyckoff': 0.15},
        'ranging':       {'fib': 0.35, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.05},
        'volatile':      {'fib': 0.30, 'wyckoff': 0.30, 'elliott': 0.20, 'turtle': 0.10},
    }

    def analyze(self, df, regime: str) -> dict:
        weights = self.REGIME_WEIGHTS[regime]
        signals = self._collect_signals(df)

        score = sum(s.strength * weights[s.method] for s in signals)
        return {
            'score': score,  # 0-1.0
            'action': 'BUY' if score >= 0.7 else 'WAIT',
            'confluence': self._calc_agreement(signals)
        }
```

**Score Interpretation:**
- 0.7-1.0: High conviction entry
- 0.4-0.7: Wait for more confluence
- 0.0-0.4: No trade

## File Structure

```
trading-project/
├── methodologies/
│   ├── elliott_wave.py     # Wave detection + halving cycle
│   ├── turtle_system.py    # Donchian breakouts
│   ├── fibonacci.py        # Levels + golden pocket
│   ├── wyckoff.py          # Phase detection + VSA
│   └── markov_regime.py    # State classification
├── patterns/
│   ├── candlestick.py      # Engulfing, hammer, doji
│   └── chart_patterns.py   # H&S, double bottom, triangles
├── aggregator.py           # Regime-weighted fusion
└── swarm/
    ├── consensus.py        # Multi-LLM voting
    └── adapters/           # Claude, DeepSeek, Gemini
```

## Cost-Effective Model Routing

| Task | Model | Cost |
|------|-------|------|
| Pattern detection | DeepSeek-V3 | $0.27/1M |
| Confluence scoring | Qwen-72B | $0.40/1M |
| Critical decisions | Claude Sonnet | $3.00/1M |
| Swarm consensus | Mixed tier | ~$1.50/1M avg |

## Integration Notes

- **Data Sources:** yfinance, CCXT, Alpaca API
- **Pairs with:** runpod-deployment-skill (model serving)
- **Projects:** ThetaRoom, swaggy-stacks, alpha-lens

## Reference Files

**Core Methodologies:**
- `reference/elliott-wave.md` - Wave rules, halving supercycle, targets
- `reference/turtle-trading.md` - Donchian channels, ATR sizing, pyramiding
- `reference/fibonacci.md` - Levels, golden pocket, on-chain enhanced
- `reference/wyckoff.md` - Phase state machines, VSA, composite operator
- `reference/markov-regime.md` - 7-state model, transition probabilities

**Advanced Patterns:**
- `reference/pattern-recognition.md` - Candlestick + chart patterns
- `reference/swarm-consensus.md` - Multi-LLM voting system
- `reference/chinese-llm-stack.md` - Cost-optimized Chinese LLMs for trading
