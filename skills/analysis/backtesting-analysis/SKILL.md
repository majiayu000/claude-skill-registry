---
name: Backtesting Analysis
description: Comprehensive guidance for interpreting backtest results and detecting overfitting (project)
---

# Backtesting Analysis Skill

**Purpose**: Interpret backtest results, understand performance metrics, and detect overfitting or unreliable strategies.

**Progressive Disclosure**: This primer contains essentials only. Full details available via `docs` command.

---

## When to Use This Skill

Load when:
- Evaluating backtest results (Phase 3)
- Detecting potential overfitting
- Understanding strategy-specific performance expectations
- Comparing multiple strategies or explaining results

---

## Quick Reference: Key Metrics

### Sharpe Ratio (Primary Metric)

**Formula**: `(Return - Risk-Free Rate) / Volatility`

| Sharpe | Quality | Action |
|--------|---------|--------|
| < 0.5 | Poor | Abandon |
| 0.5 - 0.7 | Marginal | Consider optimization |
| 0.7 - 1.0 | Acceptable | Optimize |
| 1.0 - 1.5 | Good | Production-ready |
| 1.5 - 2.0 | Very Good | Validate thoroughly |
| > 3.0 | **SUSPICIOUS** | **Likely overfitting** |

**Key Insight**: QuantConnect reports **annual Sharpe**. Sharpe > 1.0 is production-ready for most strategies.

---

### Maximum Drawdown

**Formula**: `(Trough - Peak) / Peak`

| Drawdown | Quality | Action |
|----------|---------|--------|
| < 20% | Excellent | Low risk |
| 20% - 30% | Good | Acceptable for live trading |
| 30% - 40% | Concerning | Needs strong Sharpe to justify |
| > 40% | Too High | Unacceptable for most traders |

**Key Insight**: Drawdowns > 30% are hard to tolerate psychologically. Consider: "Could I stomach this loss in real money?"

---

### Total Trades (Statistical Significance)

| Trade Count | Reliability | Decision Impact |
|-------------|-------------|-----------------|
| < 20 | Unreliable | Abandon or escalate |
| 20 - 30 | Low | Minimum viable |
| 30 - 50 | Moderate | Acceptable |
| 50 - 100 | Good | Strong confidence |
| 100+ | Excellent | Highly reliable |

**Key Insight**: Need **30+ trades** for basic significance, **100+** for high confidence. Few trades = unreliable metrics.

---

### Win Rate

| Win Rate | Quality | Interpretation |
|----------|---------|----------------|
| < 40% | Low | Needs large winners (trend following) |
| 40% - 55% | Average | Typical for most strategies |
| 55% - 65% | Good | Strong edge |
| > 75% | **SUSPICIOUS** | **Likely overfitting** |

**Key Insight**: Win rate alone is misleading. Must consider profit factor and average win/loss ratio.

---

### Profit Factor

**Formula**: `Gross Profit / Gross Loss`

| Profit Factor | Quality | Interpretation |
|---------------|---------|----------------|
| < 1.3 | Marginal | Transaction costs may kill it |
| 1.3 - 1.5 | Acceptable | Decent after costs |
| 1.5 - 2.0 | Good | Strong profitability |
| > 3.0 | Exceptional | Outstanding (verify no overfitting) |

**Key Insight**: Minimum **1.5** for live trading to cover slippage and commissions.

---

## Overfitting Detection (Red Flags)

1. **Too Perfect Sharpe (> 3.0)** → ESCALATE_TO_HUMAN
2. **Too High Win Rate (> 75%)** → Check for look-ahead bias
3. **Too Few Trades (< 20)** → Unreliable metrics
4. **Excessive Optimization Improvement (> 30%)** → Lucky parameters
5. **Severe Out-of-Sample Degradation (> 40%)** → ABANDON_HYPOTHESIS
6. **Equity Curve Too Smooth** → Check unrealistic assumptions
7. **Works Only in One Market Regime** → Not robust

**Remember**: If it looks too good to be true, it probably is.

---

## Strategy-Type Expectations

### Momentum
- **Sharpe**: 0.8 - 1.5 | **Drawdown**: 20-35% | **Win Rate**: 40-55%

### Mean Reversion
- **Sharpe**: 0.7 - 1.3 | **Drawdown**: 15-30% | **Win Rate**: 55-70%

### Trend Following
- **Sharpe**: 0.5 - 1.0 | **Drawdown**: 25-40% | **Win Rate**: 30-50%

### Breakout
- **Sharpe**: 0.6 - 1.2 | **Drawdown**: 20-35% | **Win Rate**: 40-55%

**Use these to calibrate expectations** - different strategies have different profiles.

---

## Example Decisions

### GOOD (Optimization Worthy)
```
Sharpe: 0.85, Drawdown: 22%, Trades: 67, Win Rate: 42%, PF: 1.8
→ PROCEED_TO_OPTIMIZATION (decent baseline, worth improving)
```

### EXCELLENT (Production Ready)
```
Sharpe: 1.35, Drawdown: 18%, Trades: 142, Win Rate: 53%, PF: 2.1
→ PROCEED_TO_VALIDATION (already strong, skip optimization)
```

### SUSPICIOUS (Overfitting)
```
Sharpe: 4.2, Drawdown: 5%, Trades: 25, Win Rate: 88%, PF: 5.8
→ ESCALATE_TO_HUMAN (too perfect, likely look-ahead bias or bug)
```

### POOR (Abandon)
```
Sharpe: 0.3, Drawdown: 38%, Trades: 89, Win Rate: 35%, PF: 1.1
→ ABANDON_HYPOTHESIS (poor risk-adjusted returns)
```

---

## Common Confusion Points

**Q: "Strategy made 200% returns, but Sharpe is only 0.6 - is this good?"**
A: No. We prioritize **risk-adjusted returns** (Sharpe), not raw returns. High returns with high volatility = bad Sharpe = risky.

**Q: "Sharpe 2.5 with 15 trades - should I proceed?"**
A: ESCALATE_TO_HUMAN. Too few trades (<20) for statistical significance. High Sharpe with few trades = luck, not skill.

**Q: "Optimization improved Sharpe from 0.8 to 1.5 (87% improvement) - is this good?"**
A: ESCALATE_TO_HUMAN. 87% > 30% threshold = likely overfitting to in-sample period.

**Q: "Win rate is 78%, Sharpe is 1.2 - why is this flagged?"**
A: Win rate > 75% is an overfitting signal. Real strategies rarely achieve such high win rates.

---

## Key Principles

1. **Sharpe ratio is king** - Primary metric for risk-adjusted returns
2. **Trade count matters** - Need 30+ for reliability, 100+ for confidence
3. **Beware overfitting** - Too perfect results are suspicious
4. **Context by strategy type** - Different strategies have different expectations
5. **Risk-adjusted, not raw returns** - High returns with high volatility = bad

---

## Reference Documentation (Progressive Disclosure)

**Need detailed analysis?** All reference documentation accessible via `--help`:

```bash
python SCRIPTS/backtesting_analysis.py --help
```

**That's the only way to access complete reference documentation.**

Topics covered in `--help`:
- Sharpe Ratio Deep Dive
- Maximum Drawdown Analysis
- Trade Count Statistical Significance
- Win Rate Analysis
- Profit Factor Analysis
- Complete Overfitting Detection Guide
- Strategy-Type Profiles (Momentum, Mean Reversion, Trend Following, Breakout)
- 10+ Annotated Example Backtests
- Common Confusion Points

The primer above covers 90% of use cases. Use `--help` for edge cases and detailed analysis.

---

## Integration with Decision Framework

This skill **complements** the decision-framework skill:

- **decision-framework**: Provides thresholds and decision logic
- **backtesting-analysis**: Provides interpretation and context

**Workflow**:
1. Load decision-framework to apply thresholds
2. Load backtesting-analysis to understand what metrics mean
3. Combine insights to make informed decisions

---

## Related Files

- `.claude/skills/decision-framework/skill.md` - Decision thresholds
- `SCRIPTS/decision_logic.py` - Decision implementation
- `.claude/commands/qc-backtest.md` - Backtest execution

---

**Version**: 2.0.0 (Progressive Disclosure)
**Last Updated**: November 13, 2025
**Lines**: ~200 (was 555)
**Context Reduction**: 64%
