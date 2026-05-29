---
name: QuantConnect Optimization
description: QuantConnect optimization API and Phase 4 parameter tuning (project)
---

# QuantConnect Optimization (Phase 4)

**Progressive Disclosure**: This primer loads essential information. Detailed guides in `reference/` (load on-demand).

---

## When to Use

Load when running `/qc-optimize` command for parameter tuning after successful backtest (Phase 3).

---

## ⚠️ CRITICAL CONSTRAINT: Project ID Rule

**YOU MUST USE project_id FROM iteration_state.json (created during /qc-backtest)**

### Why This Matters

1. **QC API requires baseline backtest** - Cannot optimize empty project
2. **Must optimize correct strategy** - Use project from Phase 3
3. **Prevents API errors** - Missing baseline causes failures
4. **Maintains audit trail** - Same project through all phases

### Correct Workflow

```python
# ✅ CORRECT: Read from iteration_state.json
with open('iteration_state.json', 'r') as f:
    state = json.load(f)

project_id = state['project']['project_id']  # REQUIRED
backtest_id = state['phase_results']['backtest']['backtest_id']  # Validate exists

# Validate before optimization
if not project_id or not backtest_id:
    raise ValueError("Run /qc-backtest first - no baseline found")

# Now safe to optimize
```

### Wrong Examples (DO NOT DO)

```python
# ❌ WRONG: Creating new project
project_id = api.create_project("Optimization")  # ERROR: No baseline!

# ❌ WRONG: Hardcoded project_id
project_id = 26135853  # ERROR: Wrong hypothesis!

# ❌ WRONG: Arbitrary project_id
project_id = 12345  # ERROR: Not our strategy!
```

**See `qc_optimize.py --help` for complete validation logic.**

---

## CLI Command

```bash
# Using qc_optimize.py CLI (progressive disclosure pattern)
qc_optimize.py run --config optimization_params.json --state iteration_state.json

# Check status
qc_optimize.py status --optimization-id <id>

# Get results
qc_optimize.py results --optimization-id <id>
```

**⚠️ IMPORTANT: Access all information via CLI:**
- `qc_optimize.py --help` - All commands and complete reference documentation
- Do NOT read source code or skill files directly

---

## Quick Start

### 1. Define Parameter Grid

```json
{
  "parameters": {
    "rsi_period": [10, 14, 20],
    "stop_loss": [0.03, 0.05, 0.07]
  },
  "target": "TotalPerformance.PortfolioStatistics.SharpeRatio",
  "strategy": "grid"
}
```

**Start small (3-6 combinations)** to avoid long execution times.

### 2. Run Optimization

```bash
qc_optimize.py run --config optimization_params.json
```

### 3. Evaluate Results (Phase 4 Decision)

**Automatic decision thresholds:**
- Improvement < 5%: **USE_BASELINE** (too small)
- Improvement 5-30%: **PROCEED_TO_VALIDATION** (good improvement)
- Improvement > 30%: **ESCALATE_TO_HUMAN** (overfitting risk)

Results automatically update `iteration_state.json` with decision.

---

## Common Issues

### 1. "No baseline backtest found"
**Fix**: Run `/qc-backtest` first, verify project_id in iteration_state.json

### 2. "Grid too large" (>100 combinations)
**Fix**: Use Euler strategy with limit:
```bash
qc_optimize.py run --strategy euler --max-backtests 50
```

### 3. API Authentication Errors
**Fix**: Check `.env` for `QUANTCONNECT_USER_ID` and `QUANTCONNECT_API_TOKEN`

---

## Documentation Rules (CRITICAL)

**Always store optimization results in `PROJECT_LOGS/` folder.**

**Naming convention**: `PROJECT_LOGS/optimization_result_<hypothesis_id>.json`

**See `qc_optimize.py --help` for complete logging standards.**

---

## Reference Documentation

**Need detailed information?** All reference documentation accessible via `--help`:

```bash
python SCRIPTS/qc_optimize.py --help
```

**That's the only way to access complete reference documentation.**

Topics covered in `--help`:
- Optimization strategies (Grid search, Euler sampling, custom)
- Parameter grid setup guidelines
- Phase 4 decision criteria and thresholds
- Manual optimization approach (free tier)
- Native QC optimization API (paid tier)
- Project ID validation workflow
- Common errors and fixes
- Overfitting detection patterns
- Cost estimation methods
- Complete workflow examples

The primer above covers 90% of use cases. Use `--help` for edge cases and detailed analysis.

---

## Authoritative Documentation

**When confused about workflow:**
- `PROJECT_DOCUMENTATION/autonomous_workflow_architecture.md`
- `PROJECT_DOCUMENTATION/autonomous_decision_framework.md`

**When confused about schemas:**
- `PROJECT_SCHEMAS/optimization_strategies_guide.md`
- `PROJECT_SCHEMAS/performance_thresholds.json`

---

## Related Skills

- **quantconnect-backtest** - Phase 3 (MUST run before optimization)
- **quantconnect-validation** - Phase 5 (runs after optimization)
- **decision-framework** - Decision routing logic
- **quantconnect** - Core strategy development

---

## Summary

**This primer covers:**
- ✅ Critical project_id constraint
- ✅ CLI commands for optimization
- ✅ Phase 4 decision thresholds
- ✅ Common issues and fixes
- ✅ Documentation rules
- ✅ Pointers to detailed reference docs

**Context usage:**
- **Before**: 582 lines (monolithic)
- **After**: ~150 lines (primer) + reference docs (load on-demand)
- **Savings**: 74% immediate context reduction

**Key rule**: MUST use project_id from iteration_state.json. Cannot optimize without baseline backtest.

---

**Version**: 2.0.0 (Progressive Disclosure)
**Last Updated**: November 13, 2025
**Status**: Production Ready
