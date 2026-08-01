---
name: advanced-math-tradingoptimization-advanced
description: 'Advanced optimization for trading: OCO, multi-objective, DRO, MIP, Bayesian
  opt, plus convex/Markowitz/BL references.'
---

---
name: advanced-math-trading/optimization-advanced
description: Advanced optimization for trading: OCO, multi-objective, DRO, MIP, Bayesian opt, plus convex/Markowitz/BL references.
---

# What this covers
- Online convex optimization, multi-objective (NSGA-II), DRO (CVaR/moment), mixed-integer constraints, Bayesian optimization.
- Links to convex/Markowitz/Black-Litterman background.

# Navigation (load on demand)
- docs/knowledge-base/domains/foundations/advanced-mathematics/advanced-optimization.md — main code (OGD/FTRL, NSGA-II, DRO cvxpy, MIP gurobi, Bayesian opt).
- docs/knowledge-base/domains/foundations/advanced-mathematics/convex-optimization.md
- docs/knowledge-base/domains/foundations/advanced-mathematics/optimization.md
- docs/knowledge-base/domains/foundations/advanced-mathematics/mean-variance-optimization-markowitz.md
- docs/knowledge-base/domains/foundations/advanced-mathematics/black-litterman-model.md

# Quick workflows
- Adaptive strategy/portfolio → use OGD/FTRL snippets.
- Return/risk/turnover trade-offs → NSGA-II block in advanced-optimization.
- Tail/robustness → DRO CVaR or moment-based cvxpy blocks.
- Cardinality/round lots → MIP section (gurobi).
- Hyperparameter tuning → Bayesian opt section.

# Notes
- Choose the minimal subset of files; avoid loading everything.
