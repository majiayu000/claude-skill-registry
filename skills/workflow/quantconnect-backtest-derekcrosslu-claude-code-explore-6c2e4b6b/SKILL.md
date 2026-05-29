---
name: QuantConnect Backtest
description: QuantConnect backtesting API usage and Phase 3 decision integration (project)
---

# QuantConnect Backtest Skill (Phase 3)

**Purpose**: Run backtests via QuantConnect API and make Phase 3 routing decisions.

**Progressive Disclosure**: This primer contains essentials only. Full details via `qc_backtest.py --help`.

---

## When to Use This Skill

Load when:
- Running `/qc-backtest` command
- Uploading strategy files to QuantConnect
- Making Phase 3 routing decisions
- Debugging backtest API errors

**Critical Rule**: Always store results in `PROJECT_LOGS/`. See `PROJECT_LOGS/README.md` for naming.

---

## Quick Start: Run a Backtest

**Complete workflow (upload + run + evaluate)**:

```bash
python SCRIPTS/qc_backtest.py --run \
    --name "MomentumStrategy_20241110" \
    --file strategy.py \
    --output PROJECT_LOGS/backtest_result.json
```

**What this does**:
1. Creates/reuses QC project
2. Uploads strategy.py as Main.py
3. Compiles and runs backtest
4. Polls for completion (every 5s)
5. Saves results to JSON

**Output** (`backtest_result.json`):
```json
{
  "project_id": 26135853,
  "backtest_id": "abc123def456",
  "performance": {
    "sharpe_ratio": 0.85,
    "max_drawdown": 0.22,
    "total_trades": 67,
    "win_rate": 0.42,
    "profit_factor": 1.8
  },
  "qc_url": "https://www.quantconnect.com/project/26135853"
}
```

---

## Critical Metrics for Phase 3

**Priority order** (most important first):
1. **sharpe_ratio** - Risk-adjusted returns (target: > 0.7)
2. **max_drawdown** - Risk tolerance (target: < 0.30)
3. **total_trades** - Statistical significance (need: > 30)
4. **win_rate** - Overfitting signal (if > 0.75, ESCALATE)

See `backtesting-analysis` skill for metric interpretation.

---

## Phase 3 Decision Integration

**After backtest completes**:

```python
import json, sys
sys.path.insert(0, 'SCRIPTS')
from decision_logic import evaluate_backtest, route_decision

# Load results and state
with open('PROJECT_LOGS/backtest_result.json') as f:
    results = json.load(f)
with open('iteration_state.json') as f:
    state = json.load(f)

# Evaluate metrics
decision, reason, details = evaluate_backtest(
    results['performance'],
    state['thresholds']
)

# Route to next phase
routing = route_decision("backtest", decision, state['workflow']['iteration'])

print(f"Decision: {decision}")
print(f"Next Action: {routing['next_action']}")
```

**Possible decisions**:
- `ABANDON_HYPOTHESIS` → Start new hypothesis
- `PROCEED_TO_OPTIMIZATION` → Run `/qc-optimize`
- `PROCEED_TO_VALIDATION` → Skip optimize, run `/qc-validate`
- `ESCALATE_TO_HUMAN` → Manual review needed

---

## Credentials Setup

**Required in `.env`**:
```bash
QC_USER_ID=your_user_id
QC_API_TOKEN=your_api_token
```

**Get from**: https://www.quantconnect.com → Account → API Access

**Security**: Never commit `.env` (already in `.gitignore`)

---

## Common Errors & Quick Fixes

### 1. Strategy Never Trades (0 trades)
**Fix**: Simplify entry logic
```python
# Start simple - just SMA crossover
if self.sma.IsReady and price > self.sma.Current.Value:
    self.SetHoldings(self.symbol, 1.0)
```

### 2. Object Reference Not Set
**Fix**: Add None checks
```python
def OnData(self, data):
    if not data.ContainsKey(self.symbol):
        return
    if data[self.symbol] is None:
        return
    # Now safe
```

### 3. Indicator Not Ready
**Fix**: Check IsReady
```python
if not self.sma.IsReady:
    return
# Now safe to use indicator
```

### 4. Backtest Timeout
**Fix**: Reduce date range or increase timeout
```python
# Increase timeout
result = api.wait_for_backtest(project_id, backtest_id, timeout=1200)

# Or reduce date range to 3 years
self.SetStartDate(2022, 1, 1)
```

---

## Best Practices

### Trade Count Guidelines
| Trades | Reliability | Action |
|--------|-------------|--------|
| 0 | N/A | Fix entry logic |
| 1-20 | Unreliable | Simplify or abandon |
| 30-100 | Acceptable | Proceed |
| 100+ | Good | High confidence |

### Date Range Guidelines
| Range | Purpose |
|-------|---------|
| 1-2 years | Initial testing (fast) |
| 3-5 years | Full backtest (recommended) |
| < 1 year | Too short |
| > 10 years | Too long (regime changes) |

### Always Check for Errors
```python
if 'error' in result:
    print(f"Backtest failed: {result['error']}")
    # ESCALATE or fix and retry
```

---

## /qc-backtest Command Flow

The `/qc-backtest` command executes this sequence:

1. Read `iteration_state.json` (hypothesis, project_id)
2. Load this skill for patterns
3. Generate `strategy.py` from hypothesis
4. Run `qc_backtest.py --run`
5. Evaluate via `decision_logic.py`
6. Update `iteration_state.json`
7. Git commit with structured message

---

## Reference Documentation (Progressive Disclosure)

**Need detailed information?** Access via `--help`:

```bash
python SCRIPTS/qc_backtest.py --help
```

**Topics available in reference docs**:
- Python API Integration (QuantConnectAPI class methods)
- Complete Backtest Results Structure (25+ metrics explained)
- Error Handling Guide (all errors with solutions)
- Complete Workflow Examples (end-to-end `/qc-backtest` flows)

**Access specific topics**:
```bash
python SCRIPTS/qc_backtest.py docs                  # List all
python SCRIPTS/qc_backtest.py docs api-integration  # Show specific
```

The primer above covers 85% of use cases. Use `--help` and `docs` for edge cases.

---

## Related Skills

- **quantconnect** - Core strategy development (indicators, orders, risk)
- **quantconnect-optimization** - Phase 4 optimization (load AFTER backtest)
- **quantconnect-validation** - Phase 5 validation (walk-forward testing)
- **decision-framework** - Decision thresholds and routing logic
- **backtesting-analysis** - Metric interpretation and overfitting detection

---

## Summary

**This skill covers**:
- ✅ Running backtests via QC API (`qc_backtest.py --run`)
- ✅ Phase 3 decision integration (`decision_logic.py`)
- ✅ Common errors & quick fixes
- ✅ Best practices (trade count, date ranges)

**Load when**: Running `/qc-backtest` or debugging backtest errors

**Key Principle**: Focus ONLY on backtesting. For optimization, load `quantconnect-optimization` skill.

---

**Version**: 2.0.0 (Progressive Disclosure)
**Last Updated**: November 13, 2025
**Lines**: ~200 (was 458)
**Context Reduction**: 56%
