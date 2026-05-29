---
name: Decision Framework
description: Autonomous decision-making CLI for strategy development (project)
---

# Decision Framework CLI

Evaluate results and route to next phase: `venv/bin/python SCRIPTS/decision_cli.py` (use as `decision`)

## When to Load This Skill

- After backtest completes (Phase 3 decision)
- After optimization completes (Phase 4 decision)
- After validation completes (Phase 5 decision)
- Need to route to next phase

## CLI Commands (Progressive Disclosure)

### Evaluate Backtest (Phase 3)
```bash
# Evaluate backtest results
venv/bin/python SCRIPTS/decision_cli.py evaluate-backtest \
  --results PROJECT_LOGS/backtest_result.json \
  --state iteration_state.json

# JSON output
venv/bin/python SCRIPTS/decision_cli.py evaluate-backtest --results backtest.json --json
```

**Decisions**: PROCEED_TO_OPTIMIZATION | PROCEED_TO_VALIDATION | ABANDON_HYPOTHESIS | ESCALATE_TO_HUMAN

### Evaluate Optimization (Phase 4)
```bash
# Evaluate optimization results
venv/bin/python SCRIPTS/decision_cli.py evaluate-optimization \
  --results PROJECT_LOGS/optimization_result.json \
  --state iteration_state.json
```

**Decisions**: PROCEED_TO_VALIDATION | USE_BASELINE_PARAMS | ESCALATE_TO_HUMAN | PROCEED_WITH_ROBUST_PARAMS

### Evaluate Validation (Phase 5)
```bash
# Evaluate validation results
venv/bin/python SCRIPTS/decision_cli.py evaluate-validation \
  --results PROJECT_LOGS/validation_result.json \
  --state iteration_state.json
```

**Decisions**: DEPLOY_STRATEGY | PROCEED_WITH_CAUTION | ABANDON_HYPOTHESIS | ESCALATE_TO_HUMAN

### Route to Next Phase
```bash
# Determine next action based on decision
venv/bin/python SCRIPTS/decision_cli.py route \
  --phase backtest \
  --decision PROCEED_TO_OPTIMIZATION \
  --iteration 1
```

## Workflow

1. **Run Phase**: Execute backtest/optimization/validation
2. **Evaluate**: `decision evaluate-<phase> --results results.json`
3. **Route**: `decision route --phase <phase> --decision <DECISION>`
4. **Execute Next**: Proceed to next phase based on routing

## Decision Thresholds

**Loaded from `iteration_state.json` (single source of truth)**:
- `performance_criteria.minimum_viable` - Sharpe 0.5, DD 0.35, Trades 20
- `performance_criteria.optimization_worthy` - Sharpe 0.7, DD 0.30, Trades 30
- `performance_criteria.production_ready` - Sharpe 1.0, DD 0.20, Trades 50
- `overfitting_signals.too_perfect_sharpe` - Sharpe > 3.0
- `overfitting_signals.too_few_trades` - Trades < 10

**Do not hardcode thresholds. Always read from iteration_state.json.**

## Progressive Disclosure Pattern

**Load only what you need:**
- Phase 3: Use `evaluate-backtest` (only backtest logic loaded)
- Phase 4: Use `evaluate-optimization` (only optimization logic loaded)
- Phase 5: Use `evaluate-validation` (only validation logic loaded)

**Before (old approach)**:
- Load 500-line decision-framework skill
- Load 300-line backtesting-analysis skill
- Total: 800 lines for any decision

**After (CLI approach)**:
- Run `decision evaluate-backtest` (instant, 100-line skill)
- Progressive disclosure: 87.5% context reduction

## Authoritative Documentation

**When confused about decision logic or thresholds:**
- Read: `PREVIOUS_WORK/PROJECT_DOCUMENTATION/autonomous_decision_framework.md`
- Contains: Complete decision tree, all thresholds, routing logic

**Do not guess thresholds. Use authoritative docs as source of truth.**

## CLI Help

Use `--help` for command details:
```bash
venv/bin/python SCRIPTS/decision_cli.py --help
venv/bin/python SCRIPTS/decision_cli.py evaluate-backtest --help
venv/bin/python SCRIPTS/decision_cli.py route --help
```

**IMPORTANT: Do not read decision_cli.py source code unless strictly needed for debugging. Use --help for usage.**

---

**Context Savings**: 100 lines (vs 800 lines loading multiple skills) = 87.5% reduction

**Progressive Disclosure**: Load only the evaluation logic you need (backtest vs optimization vs validation)

**Trifecta**: CLI works for humans, teams, AND agents

**Beyond MCP Pattern**: Use --help, not source code. Load only what you need.
