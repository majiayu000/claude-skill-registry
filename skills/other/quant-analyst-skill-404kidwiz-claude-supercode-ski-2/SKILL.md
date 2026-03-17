---
name: quant-analyst
description: Expert in quantitative finance, algorithmic trading, and financial data analysis using Python (Pandas/NumPy), statistical modeling, and machine learning.
---

# Quantitative Analyst

## Purpose
Provides expertise in quantitative finance, algorithmic trading strategies, and financial data analysis. Specializes in statistical modeling, risk analytics, and building data-driven trading systems using Python scientific computing stack.

## When to Use
- Building algorithmic trading strategies or backtesting frameworks
- Performing statistical analysis on financial time series data
- Implementing risk models (VaR, CVaR, Greeks calculations)
- Creating portfolio optimization algorithms
- Developing quantitative pricing models for derivatives
- Analyzing market microstructure and order book dynamics
- Building factor models for asset returns
- Implementing Monte Carlo simulations for financial instruments

## Quick Start
**Invoke this skill when:**
- Building algorithmic trading strategies or backtesting frameworks
- Performing statistical analysis on financial time series data
- Implementing risk models (VaR, CVaR, Greeks calculations)
- Creating portfolio optimization algorithms
- Developing quantitative pricing models for derivatives

**Do NOT invoke when:**
- Building general web applications → use fullstack-developer
- Creating data visualizations without financial context → use data-analyst
- Implementing payment processing → use payment-integration
- Building generic ML models → use ml-engineer

## Decision Framework
```
Financial Analysis Task?
├── Trading Strategy → Backtesting framework + signal generation
├── Risk Management → VaR/CVaR models + stress testing
├── Portfolio Optimization → Mean-variance, Black-Litterman, risk parity
├── Derivatives Pricing → Monte Carlo, finite difference, analytical
└── Time Series Analysis → ARIMA, GARCH, cointegration tests
```

## Core Workflows

### 1. Algorithmic Trading Strategy Development
1. Define trading hypothesis and signal generation logic
2. Implement strategy using vectorized Pandas operations
3. Build backtesting engine with realistic execution simulation
4. Calculate performance metrics (Sharpe, Sortino, max drawdown)
5. Perform walk-forward optimization to avoid overfitting
6. Implement live trading hooks with proper risk controls

### 2. Risk Model Implementation
1. Gather historical price/returns data
2. Select appropriate risk metric (VaR, CVaR, Greeks)
3. Implement calculation using parametric, historical, or Monte Carlo methods
4. Validate model with backtesting and stress scenarios
5. Build monitoring dashboard for real-time risk exposure

### 3. Portfolio Optimization
1. Define investment universe and constraints
2. Calculate expected returns and covariance matrix
3. Implement optimization (scipy.optimize or cvxpy)
4. Apply regularization to prevent concentration
5. Rebalance periodically with transaction cost consideration

## Best Practices
- Use vectorized NumPy/Pandas operations for performance on large datasets
- Always account for transaction costs, slippage, and market impact in backtests
- Implement proper cross-validation (walk-forward) to prevent lookahead bias
- Use log returns for statistical properties, simple returns for aggregation
- Store financial data with timezone-aware timestamps (UTC preferred)
- Validate models with out-of-sample testing before deployment

## Anti-Patterns
- **Overfitting to historical data** → Use walk-forward validation and regularization
- **Ignoring transaction costs** → Include realistic costs in all backtests
- **Using future data in signals** → Ensure strict point-in-time correctness
- **Assuming normal distributions** → Use fat-tailed distributions for risk models
- **Hardcoding market assumptions** → Parameterize and stress test assumptions
