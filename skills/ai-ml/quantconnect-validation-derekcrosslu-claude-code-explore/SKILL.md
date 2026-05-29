---
name: QuantConnect Validation
description: QuantConnect walk-forward validation and Phase 5 robustness testing (project)
---

# QuantConnect Validation Skill (Phase 5)

**Purpose**: Walk-forward validation for Phase 5 robustness testing before deployment.

**Progressive Disclosure**: This primer contains essentials only. Full details available via `qc_validate.py docs` command.

---

## When to Use This Skill

Load when:
- Running `/qc-validate` command
- Testing out-of-sample performance
- Evaluating strategy robustness
- Making deployment decisions

**Tool**: Use `python SCRIPTS/qc_validate.py` for walk-forward validation

---

## Walk-Forward Validation Overview

**Purpose**: Detect overfitting and ensure strategy generalizes to new data.

**Approach**:
1. **Training (in-sample)**: Develop/optimize on 80% of data
2. **Testing (out-of-sample)**: Validate on remaining 20%
3. **Compare**: Measure performance degradation

**Example** (5-year backtest 2019-2023):
- In-sample: 2019-2022 (4 years) - Training period
- Out-of-sample: 2023 (1 year) - Testing period

---

## Key Metrics

### 1. Performance Degradation

**Formula**: `(IS Sharpe - OOS Sharpe) / IS Sharpe`

| Degradation | Quality | Decision |
|-------------|---------|----------|
| < 15% | Excellent | Deploy with confidence |
| 15-30% | Acceptable | Deploy but monitor |
| 30-40% | Concerning | Escalate to human |
| > 40% | Severe | Abandon (overfit) |

**Key Insight**: < 15% degradation indicates robust strategy that generalizes well.

---

### 2. Robustness Score

**Formula**: `OOS Sharpe / IS Sharpe`

| Score | Quality | Interpretation |
|-------|---------|----------------|
| > 0.75 | High | Strategy robust across periods |
| 0.60-0.75 | Moderate | Acceptable but monitor |
| < 0.60 | Low | Strategy unstable |

**Key Insight**: > 0.75 indicates strategy maintains performance out-of-sample.

---

## Quick Usage

### Run Walk-Forward Validation

```bash
# From hypothesis directory with iteration_state.json
python SCRIPTS/qc_validate.py run --strategy strategy.py

# Custom split ratio (default 80/20)
python SCRIPTS/qc_validate.py run --strategy strategy.py --split 0.70
```

**What it does**:
1. Reads project_id from `iteration_state.json`
2. Splits date range (80/20 default)
3. Runs in-sample backtest
4. Runs out-of-sample backtest
5. Calculates degradation and robustness
6. Saves results to `PROJECT_LOGS/validation_result.json`

---

### Analyze Results

```bash
python SCRIPTS/qc_validate.py analyze --results PROJECT_LOGS/validation_result.json
```

**Output**:
- Performance comparison table
- Degradation percentage
- Robustness assessment
- Deployment recommendation

---

## Decision Integration

After validation, the decision framework evaluates:

**DEPLOY_STRATEGY** (Deploy with confidence):
- Degradation < 15% AND
- Robustness > 0.75 AND
- OOS Sharpe > 0.7

**PROCEED_WITH_CAUTION** (Deploy but monitor):
- Degradation < 30% AND
- Robustness > 0.60 AND
- OOS Sharpe > 0.5

**ABANDON_HYPOTHESIS** (Too unstable):
- Degradation > 40% OR
- Robustness < 0.5 OR
- OOS Sharpe < 0

**ESCALATE_TO_HUMAN** (Borderline):
- Results don't clearly fit above criteria

---

## Best Practices

### 1. Time Splits

- **Standard**: 80/20 (4 years training, 1 year testing)
- **Conservative**: 70/30 (more OOS testing)
- **Very Conservative**: 60/40 (extensive testing)

**Minimum OOS period**: 6 months (1 year preferred)

---

### 2. Never Peek at Out-of-Sample

**CRITICAL RULE**: Never adjust strategy based on OOS results.
- OOS is for **testing only**
- Adjusting based on OOS defeats validation purpose
- If you adjust, OOS becomes in-sample

---

### 3. Check Trade Count

Both periods need sufficient trades:
- **In-sample**: Minimum 30 trades (50+ preferred)
- **Out-of-sample**: Minimum 10 trades (20+ preferred)

Too few trades = unreliable validation.

---

### 4. Compare Multiple Metrics

Don't just look at Sharpe:
- Sharpe Ratio degradation
- Max Drawdown increase
- Win Rate change
- Profit Factor degradation
- Trade Count consistency

All metrics should degrade similarly for robust strategy.

---

## Common Issues

### Severe Degradation (> 40%)

**Cause**: Strategy overfit to in-sample period

**Example**:
- IS Sharpe: 1.5 → OOS Sharpe: 0.6
- Degradation: 60%

**Decision**: ABANDON_HYPOTHESIS

**Fix for next hypothesis**: Simplify (fewer parameters), longer training period

---

### Different Market Regimes

**Cause**: IS was bull market, OOS was bear market

**Example**:
- 2019-2022 (bull): Sharpe 1.2
- 2023 (bear): Sharpe -0.3

**Decision**: Not necessarily overfit, but not robust across regimes

**Fix**: Test across multiple regimes, add regime detection

---

### Low Trade Count in OOS

**Cause**: Strategy stops trading in OOS period

**Example**:
- IS: 120 trades → OOS: 3 trades

**Decision**: ESCALATE_TO_HUMAN (insufficient OOS data)

---

## Integration with /qc-validate

The `/qc-validate` command workflow:

1. Read `iteration_state.json` for project_id and parameters
2. Load this skill for validation approach
3. Modify strategy for time splits (80/20)
4. Run in-sample and OOS backtests
5. Calculate degradation and robustness
6. Evaluate using decision framework
7. Update `iteration_state.json` with results
8. Git commit with validation summary

---

## Reference Documentation

**Need implementation details?** All reference documentation accessible via `--help`:

```bash
python SCRIPTS/qc_validate.py --help
```

**That's the only way to access complete reference documentation.**

Topics covered in `--help`:
- Walk-forward validation methodology
- Performance degradation thresholds
- Monte Carlo validation techniques
- PSR/DSR statistical metrics
- Common errors and fixes
- Phase 5 decision criteria

The primer above covers 90% of use cases. Use `--help` for edge cases and detailed analysis.

---

## Related Skills

- **quantconnect** - Core strategy development
- **quantconnect-backtest** - Phase 3 backtesting (qc_backtest.py:**)
- **quantconnect-optimization** - Phase 4 optimization (qc_optimize.py:**)
- **decision-framework** - Decision thresholds
- **backtesting-analysis** - Metric interpretation

---

## Key Principles

1. **OOS is sacred** - Never adjust strategy based on OOS results
2. **Degradation < 15% is excellent** - Strategy generalizes well
3. **Robustness > 0.75 is target** - Maintains performance OOS
4. **Trade count matters** - Need sufficient trades in both periods
5. **Multiple metrics** - All should degrade similarly for robustness

---

## Example Decision

```
In-Sample (2019-2022):
  Sharpe: 0.97, Drawdown: 18%, Trades: 142

Out-of-Sample (2023):
  Sharpe: 0.89, Drawdown: 22%, Trades: 38

Degradation: 8.2% (< 15%)
Robustness: 0.92 (> 0.75)

→ DEPLOY_STRATEGY (minimal degradation, high robustness)
```

---

**Version**: 2.0.0 (Progressive Disclosure)
**Last Updated**: November 13, 2025
**Lines**: ~190 (was 463)
**Context Reduction**: 59%
